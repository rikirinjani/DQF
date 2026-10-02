"""N6b narrow vertical slice — eligibility gate + evidence contract + three-state ranking.

Implements the Astra-reviewed design (rag-queries/curation/n6b-indication-boundary-design.md v2):

  Stage 1 ELIGIBILITY (binary, no scores)
    a) objective match (curated condition_map)
    b) hard contraindication (global rules, evaluated independently of objective)
    c) safety-assessment completeness (unknown != false)
  Stage 2 RANKABILITY (typed evidence contract)
    compatible evidence -> eligible_ranked
    no compatible evidence -> eligible_unranked (null score, never imputed)

Design invariants enforced here:
  - no neutral-score imputation (missing evidence is not a number)
  - no cross-endpoint fallback (one objective, one evidence contract)
  - unknown safety facts withhold ranking, never silently pass
  - every drug has an explicit disposition (mapped or unsupported_in_v1)

This module is data-driven: conditions.json / condition_map.json / evidence.json.
"""
import json
from pathlib import Path

_DIR = Path(__file__).resolve().parent


def _load(name):
    p = _DIR / name
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


REGISTRY = _load("conditions.json")
CONDITION_MAP = _load("condition_map.json")
EVIDENCE = _load("evidence.json")


# ---------------------------------------------------------------------------
# Hard contraindication rules (global; evaluated independently of objective)
# ---------------------------------------------------------------------------
def _norm_preg(raw):
    """Normalize pregnancy_safety to A..X (mirrors server._norm_preg semantics)."""
    if raw in ("A", "B", "C", "C/D", "D", "X"):
        return raw
    if not isinstance(raw, str):
        return "C"
    low = raw.lower()
    for frag, code in (("contraindicated", "X"), ("avoid", "D"), ("high risk", "D")):
        if frag in low and ("not " + frag) not in low:
            return code
    return "C"


def _rule_pregnancy_x(drug, patient):
    if patient.get("pregnancy_status", "not_pregnant") == "not_pregnant":
        return False
    return _norm_preg(drug.get("pregnancy_safety")) == "X"


def _rule_hepatic_contraindicated(drug, patient):
    if patient.get("hepatic_function", "normal") == "normal":
        return False
    return drug.get("hepatic_safety") == "contraindicated"


# Each rule returns True (applies -> exclude), False (does not apply), or None (unknown).
HARD_RULES = [
    {"id": "pregnancy_x", "applies": _rule_pregnancy_x},
    {"id": "hepatic_contraindicated", "applies": _rule_hepatic_contraindicated},
]


def objective_exists(objective):
    return objective in (REGISTRY.get("objectives") or {})


def objective_contract(objective):
    return (REGISTRY.get("objectives", {}).get(objective, {}) or {}).get("evidence", {})


def mapped_objectives(drug_id):
    return (CONDITION_MAP.get("map", {}).get(drug_id, {}) or {}).get("objectives", []) or []


def is_unsupported(drug_id):
    return drug_id in (CONDITION_MAP.get("unsupported_in_v1") or [])


def evaluate(drug, objective, patient):
    """Stage 1. Return (state, reasons).

    state: "eligible" | "eligible_unranked" | "excluded"
    reasons: list of {rule, ...} dicts (structured; all evaluated failures returned)
    """
    reasons = []

    # (a) objective match
    if objective not in mapped_objectives(drug["id"]):
        reasons.append({"rule": "objective_mismatch", "objective": objective})
        return "excluded", reasons

    # (b) hard contraindications (global, objective-independent)
    unknown = False
    for rule in HARD_RULES:
        try:
            res = rule["applies"](drug, patient)
        except Exception:
            res = None
        if res is True:
            reasons.append({"rule": rule["id"], "state": "failed"})
            return "excluded", reasons
        if res is None:
            reasons.append({"rule": rule["id"], "state": "unknown"})
            unknown = True

    # (c) safety completeness: an unevaluable hard rule withholds ranking
    if unknown:
        reasons.append({"rule": "safety_unknown", "state": "unknown"})
        return "eligible_unranked", reasons

    return "eligible", reasons


# ---------------------------------------------------------------------------
# Stage 2 — typed evidence contract
# ---------------------------------------------------------------------------
def evidence_for(drug_id, objective):
    return (EVIDENCE.get("evidence", {}).get(drug_id, {}) or {}).get(objective)


def contract_ok(ev, contract):
    """Return (ok, reason). A drug is rankable only if its evidence satisfies the contract."""
    if not ev:
        return False, "no_compatible_evidence"
    for field in ("unit", "comparator", "horizon_weeks", "population"):
        if ev.get(field) is None:
            return False, "incomplete_evidence"
    if ev.get("value") is None:
        return False, "no_compatible_evidence"
    return True, None


def transform(ev, contract):
    """Bounded, monotonic transform per contract.transform. Returns None if not applicable."""
    kind = contract.get("transform")
    anchor = contract.get("anchor", {}) or {}
    v = ev.get("value")
    if v is None:
        return None
    if kind == "percent_higher_better":
        best = anchor.get("best", 95)
        worst = anchor.get("worst", 50)
        if best == worst:
            return 5.0
        s = (v - worst) / (best - worst) * 10.0
        return round(max(0.0, min(10.0, s)), 1)
    if kind == "nnt_lower_better":
        best = anchor.get("best", 2)
        worst = anchor.get("worst", 8)
        if best == worst:
            return 5.0
        s = (worst - v) / (worst - best) * 10.0
        return round(max(0.0, min(10.0, s)), 1)
    return None


def assess(drugs, objective, patient):
    """Run both stages over a drug list.

    Returns dict with eligible_ranked / eligible_unranked / excluded and status.
    """
    contract = objective_contract(objective)
    ranked, unranked, excluded = [], [], []
    for drug in drugs:
        state, reasons = evaluate(drug, objective, patient)
        if state == "excluded":
            excluded.append({"id": drug["id"], "name": drug["name"],
                             "class": drug["class"], "reasons": reasons})
            continue
        if state == "eligible_unranked":
            unranked.append({"id": drug["id"], "name": drug["name"],
                             "class": drug["class"], "reasons": reasons})
            continue
        # eligible -> rankability
        ev = evidence_for(drug["id"], objective)
        ok, why = contract_ok(ev, contract)
        if not ok:
            unranked.append({"id": drug["id"], "name": drug["name"], "class": drug["class"],
                             "reasons": [{"rule": why, "state": "unrankable"}]})
            continue
        ranked.append({"drug": drug, "evidence": ev, "efficacy": transform(ev, contract)})

    if ranked:
        status = "ok"
    elif unranked:
        status = "no_rankable"
    else:
        status = "no_eligible"
    return {"eligible_ranked": ranked, "eligible_unranked": unranked,
            "excluded": excluded, "status": status}
