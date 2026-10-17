#!/usr/bin/env python3
"""N6b narrow vertical slice tests — eligibility gate + evidence contract + three states.

Covers the Astra review's required assertions:
  - objective match / mismatch
  - hard contraindication (global, objective-independent)
  - unknown safety withholds ranking (unknown != false)
  - no neutral-score imputation (missing evidence -> eligible_unranked, null score)
  - no cross-endpoint fallback (one objective, one contract)
  - recommendation-path closure (combo suggestions disabled in scoped v1)
  - legacy path flagged deprecated + runs the shared hard gate (Phase 1)
Run: python rag-queries/test_indication_gate.py
"""
import asyncio
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))

import eligibility
import server
from server import QueryRequest

OBJECTIVE = "erosive_esophagitis_healing"
PPIS = ["omeprazole", "esomeprazole", "pantoprazole", "lansoprazole", "rabeprazole"]
BY_ID = {d["id"]: d for d in server.drugs}


def _req(**kw):
    base = dict(age=45, renal_function="normal", cv_risk="low", gi_risk="low",
                pain_type="none", drug_class="any", prioritize="balanced",
                pregnancy_status="not_pregnant", lactation="no", hepatic_function="normal")
    base.update(kw)
    return QueryRequest(**base)


def _patient(**kw):
    base = dict(pregnancy_status="not_pregnant", hepatic_function="normal",
                renal_function="normal", age=45)
    base.update(kw)
    return base


# --- registry / mapping -----------------------------------------------------
def test_objective_exists():
    assert eligibility.objective_exists(OBJECTIVE)
    assert not eligibility.objective_exists("no_such_objective")


def test_mapping_disposition_complete():
    mapped = set(eligibility.CONDITION_MAP["map"])
    unsupported = set(eligibility.CONDITION_MAP["unsupported_in_v1"])
    all_ids = {d["id"] for d in server.drugs}
    assert mapped | unsupported == all_ids, "every drug must have an explicit disposition"
    assert mapped & unsupported == set(), "mapped and unsupported must be disjoint"
    assert mapped == set(PPIS)


# --- stage 1: eligibility ---------------------------------------------------
def test_objective_mismatch_excludes():
    statin = BY_ID["atorvastatin"]
    state, reasons = eligibility.evaluate(statin, OBJECTIVE, _patient())
    assert state == "excluded"
    assert reasons[0]["rule"] == "objective_mismatch"


def test_hard_contraindication_pregnancy_x():
    drug = copy.deepcopy(BY_ID["omeprazole"])
    drug["pregnancy_safety"] = "X"  # synthetic: mapped drug with an absolute contraindication
    state, reasons = eligibility.evaluate(drug, OBJECTIVE, _patient(pregnancy_status="first_trimester"))
    assert state == "excluded", state
    assert any(r["rule"] == "pregnancy_x" and r["state"] == "failed" for r in reasons)


def test_hard_contraindication_hepatic():
    drug = copy.deepcopy(BY_ID["omeprazole"])
    drug["hepatic_safety"] = "contraindicated"
    state, reasons = eligibility.evaluate(drug, OBJECTIVE, _patient(hepatic_function="severe"))
    assert state == "excluded"
    assert any(r["rule"] == "hepatic_contraindicated" for r in reasons)


def test_contraindication_is_objective_independent():
    # same drug, same patient, different objective -> the global rule still applies
    drug = copy.deepcopy(BY_ID["omeprazole"])
    drug["pregnancy_safety"] = "X"
    for obj in (OBJECTIVE, "some_other_objective"):
        state, reasons = eligibility.evaluate(drug, obj, _patient(pregnancy_status="third_trimester"))
        assert state == "excluded"
        # for the other objective the mismatch fires first, but the drug is excluded either way
        assert reasons


def test_unknown_safety_withholds_ranking():
    orig = eligibility.HARD_RULES
    eligibility.HARD_RULES = orig + [{"id": "test_unknown", "applies": lambda d, p: None}]
    try:
        state, reasons = eligibility.evaluate(BY_ID["omeprazole"], OBJECTIVE, _patient())
        assert state == "eligible_unranked", state
        assert any(r["rule"] == "safety_unknown" for r in reasons)
    finally:
        eligibility.HARD_RULES = orig


# --- stage 2: evidence contract --------------------------------------------
def test_contract_rejects_missing_evidence():
    ok, why = eligibility.contract_ok(None, eligibility.objective_contract(OBJECTIVE))
    assert not ok and why == "no_compatible_evidence"


def test_contract_rejects_incomplete_evidence():
    ev = {"value": 90, "unit": "percent", "comparator": None, "horizon_weeks": 8,
          "population": "erosive esophagitis"}
    ok, why = eligibility.contract_ok(ev, eligibility.objective_contract(OBJECTIVE))
    assert not ok and why == "incomplete_evidence"


def _assess_omeprazole_with(**overrides):
    """assess() omeprazole alone with its evidence record patched."""
    orig = eligibility.EVIDENCE
    ev = copy.deepcopy(orig)
    ev["evidence"]["omeprazole"][OBJECTIVE].update(overrides)
    eligibility.EVIDENCE = ev
    try:
        return eligibility.assess([BY_ID["omeprazole"]], OBJECTIVE, _patient())
    finally:
        eligibility.EVIDENCE = orig


def test_contract_mismatch_per_field():
    cases = {"unit": {"unit": "nnt"},
             "comparator": {"comparator": "no treatment"},
             "horizon_weeks": {"horizon_weeks": 4},
             "population": {"population": "non-erosive reflux disease"}}
    for field, override in cases.items():
        res = _assess_omeprazole_with(**override)
        assert res["eligible_ranked"] == [], field
        rules = [r["rule"] for r in res["eligible_unranked"][0]["reasons"]]
        assert rules == ["contract_mismatch:" + field], (field, rules)


def test_contract_rejects_unsourced_evidence():
    res = _assess_omeprazole_with(status="legacy_unsourced")
    assert res["eligible_ranked"] == [] and res["status"] == "no_rankable"
    assert res["eligible_unranked"][0]["reasons"][0]["rule"] == "unsourced_evidence"


def test_contract_normalised_match():
    contract = eligibility.objective_contract(OBJECTIVE)
    ev = {"value": 88, "unit": " Percent ", "comparator": "ACTIVE", "horizon_weeks": 8,
          "population": "Erosive Esophagitis"}
    assert eligibility.contract_ok(ev, contract) == (True, None)
    # horizon range form (for the D2 ~24-26 wk contract)
    rng = dict(contract, horizon_weeks={"min": 6, "max": 8})
    assert eligibility.contract_ok(dict(ev, horizon_weeks=6), rng) == (True, None)
    assert eligibility.contract_ok(dict(ev, horizon_weeks=12), rng) == \
        (False, "contract_mismatch:horizon_weeks")


def test_contract_missing_field_fails_closed():
    contract = dict(eligibility.objective_contract(OBJECTIVE))
    del contract["populations"]
    ev = eligibility.evidence_for("omeprazole", OBJECTIVE)
    assert eligibility.contract_ok(ev, contract) == (False, "contract_incomplete:population")


def test_ppi_evidence_meets_contract():
    contract = eligibility.objective_contract(OBJECTIVE)
    for pid in PPIS:
        ok, why = eligibility.contract_ok(eligibility.evidence_for(pid, OBJECTIVE), contract)
        assert ok, (pid, why)


def test_transform_bounded_monotonic():
    contract = eligibility.objective_contract(OBJECTIVE)
    hi = eligibility.transform({"value": 90}, contract)
    lo = eligibility.transform({"value": 84}, contract)
    assert hi > lo, "higher healing must score higher"
    assert 0.0 <= lo <= 10.0 and 0.0 <= hi <= 10.0
    assert eligibility.transform({"value": 200}, contract) == 10.0  # bounded above
    assert eligibility.transform({"value": 0}, contract) == 0.0    # bounded below


def test_no_neutral_imputation():
    # a mapped drug with its evidence removed must be unranked, never given a number
    orig = eligibility.EVIDENCE
    ev = copy.deepcopy(orig)
    del ev["evidence"]["omeprazole"]
    eligibility.EVIDENCE = ev
    try:
        res = eligibility.assess([BY_ID["omeprazole"]], OBJECTIVE, _patient())
        assert res["status"] == "no_rankable"
        assert res["eligible_ranked"] == []
        assert res["eligible_unranked"][0]["id"] == "omeprazole"
        assert "overall" not in res["eligible_unranked"][0]
    finally:
        eligibility.EVIDENCE = orig


# --- server scoped path -----------------------------------------------------
def test_scoped_three_states():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE)))
    assert res["mode"] == "objective_scoped"
    assert res["status"] == "ok"
    assert len(res["eligible_ranked"]) == 5
    assert len(res["eligible_unranked"]) == 0
    assert len(res["excluded"]) == 90
    assert {r["id"] for r in res["eligible_ranked"]} == set(PPIS)


def test_scoped_ranking_uses_evidence_transform():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE)))
    ranked = res["eligible_ranked"]
    # esomeprazole (90%) must out-score rabeprazole (84%) on efficacy
    eff = {r["id"]: r["scores"]["efficacy"] for r in ranked}
    assert eff["esomeprazole"] > eff["rabeprazole"], eff
    # overall sorted descending
    overalls = [r["overall"] for r in ranked]
    assert overalls == sorted(overalls, reverse=True)


def test_scoped_combo_suggestions_disabled():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE)))
    assert all(r["combo_suggestions"] == [] for r in res["eligible_ranked"])


def test_scoped_unsupported_objective():
    res = asyncio.run(server.query_drugs(_req(objective="not_a_real_objective")))
    assert res["status"] == "unsupported"
    assert res["eligible_ranked"] == []


def test_scoped_class_filter_reported():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE, drug_class="PPI")))
    assert res["filter_effects"]["class_filter"] == ["PPI"]
    assert res["filter_effects"]["removed"] == 90
    assert len(res["eligible_ranked"]) == 5


def test_scoped_excluded_reasons_structured():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE)))
    ex = res["excluded"][0]
    assert "reasons" in ex and ex["reasons"][0]["rule"] == "objective_mismatch"


# --- legacy path ------------------------------------------------------------
def test_legacy_flagged_deprecated():
    res = asyncio.run(server.query_drugs(_req()))
    assert res["mode"] == "legacy"
    assert res["deprecated"] is True
    assert "results" in res and len(res["results"]) == 95


def test_legacy_never_recommends():
    """Legacy (no objective) scores but never names a best choice (RES-01)."""
    for kw in ({}, dict(age=70, pain_type="inflammatory"), dict(drug_class="NSAID"),
               dict(drug_class="Statin", hepatic_function="severe")):
        res = asyncio.run(server.query_drugs(_req(**kw)))
        assert res["status"] == "objective_required", kw
        assert "Best choice" not in res["summary"], kw
        for r in res["results"]:
            assert {"id", "name", "overall", "scores"} <= set(r), kw
            assert r["name"] not in res["summary"], (kw, r["name"])


# --- legacy hard gates (design Phase 1, review F06/F07/F15) -----------------
# Label-sourced (2026-10-17, label_sourcing_safety_fields.json): current statin
# labels no longer contraindicate pregnancy (-> D, penalty only); lovastatin's
# old-format labels still do. Hepatic: label contraindications (acute liver failure /
# decompensated cirrhosis / active liver disease / severe impairment / cirrhosis).
PREG_X = {"lovastatin", "warfarin"}
HEP_CI = {"atorvastatin", "rosuvastatin", "simvastatin", "pravastatin", "pitavastatin",
          "lovastatin", "carvedilol", "nebivolol", "methyldopa", "acarbose"}


def _ids(rows):
    return {r["id"] for r in rows}


def _rules(row):
    return {r["rule"] for r in row["reasons"] if r.get("state") == "failed"}


def test_legacy_no_patient_factors_unchanged():
    res = asyncio.run(server.query_drugs(_req()))
    assert res["excluded"] == [] and res["eligible_unranked"] == []
    assert set(res["hard_gates_applied"]) == {"pregnancy_x", "hepatic_contraindicated"}


def test_legacy_pregnancy_x_excluded():
    res = asyncio.run(server.query_drugs(_req(pregnancy_status="third_trimester")))
    assert _ids(res["excluded"]) == PREG_X
    assert not (_ids(res["results"]) & PREG_X), "excluded drug was ranked"
    assert len(res["results"]) + len(res["excluded"]) == 95
    for row in res["excluded"]:
        assert "pregnancy_x" in _rules(row)


def test_legacy_hepatic_contraindicated_excluded():
    res = asyncio.run(server.query_drugs(_req(hepatic_function="severe")))
    assert _ids(res["excluded"]) == HEP_CI
    assert "omeprazole" in _ids(res["results"])


def test_legacy_hepatic_mild_moderate_not_excluded():
    """Hepatic gate is severe-only; mild/moderate stay safety penalties."""
    base = {r["id"]: r for r in asyncio.run(server.query_drugs(_req()))["results"]}
    for level in ("mild", "moderate"):
        res = asyncio.run(server.query_drugs(_req(hepatic_function=level)))
        assert res["excluded"] == [], f"{level}: {_ids(res['excluded'])}"
        ranked = {r["id"]: r for r in res["results"]}
        assert HEP_CI <= set(ranked), level
        for i in HEP_CI:
            assert ranked[i]["scores"]["safety"] < base[i]["scores"]["safety"], (level, i)
        state, _ = eligibility.hard_gate(BY_ID["atorvastatin"],
                                         _patient(hepatic_function=level))
        assert state == "pass", level


def test_legacy_all_failures_reported():
    res = asyncio.run(server.query_drugs(
        _req(pregnancy_status="first_trimester", hepatic_function="severe")))
    row = next(r for r in res["excluded"] if r["id"] == "lovastatin")
    assert _rules(row) == {"pregnancy_x", "hepatic_contraindicated"}


def test_legacy_class_filter_all_excluded_scoped_summary():
    res = asyncio.run(server.query_drugs(
        _req(drug_class="Statin", pregnancy_status="second_trimester")))
    assert _ids(res["excluded"]) == {"lovastatin"}
    assert len(res["results"]) == 5
    res = asyncio.run(server.query_drugs(_req(drug_class="Statin", hepatic_function="severe")))
    assert res["results"] == [] and len(res["excluded"]) == 6
    rule = {"id": "test_block", "applies": lambda drug, p: drug["class"] == "Statin"}
    eligibility.HARD_RULES.append(rule)
    try:
        res = asyncio.run(server.query_drugs(_req(drug_class="Statin")))
    finally:
        eligibility.HARD_RULES.remove(rule)
    assert res["results"] == [] and len(res["excluded"]) == 6
    assert "No eligible option found in the evaluated catalogue/filter" in res["summary"]
    assert "Best choice" not in res["summary"]


def test_legacy_no_excluded_leakage():
    res = asyncio.run(server.query_drugs(
        _req(pregnancy_status="third_trimester", hepatic_function="severe")))
    blocked_names = {BY_ID[i]["name"] for i in PREG_X | HEP_CI}
    text = res["summary"] + " ".join(
        " ".join(r["strengths"] + r["concerns"]) for r in res["results"])
    for name in blocked_names:
        assert name not in text, f"{name} leaked into recommendation text"
    for r in res["results"]:
        for c in r["combo_suggestions"]:
            assert c.get("add_on_drug") not in blocked_names


def test_legacy_combo_skips_blocked_add_on():
    """Block the first-listed drug of each combo add-on class; the combo must
    fall back to an admissible drug, or be dropped when none is left."""
    first = {}
    for d in server.drugs:
        first.setdefault(d["class"], d["id"])
    blocked = {first[c] for c in ("Alginate", "H2RA", "Antacid", "Mucosal Protectant")}
    rule = {"id": "test_block", "applies": lambda drug, p: drug["id"] in blocked}
    eligibility.HARD_RULES.append(rule)
    try:
        res = asyncio.run(server.query_drugs(_req(drug_class="PPI")))
    finally:
        eligibility.HARD_RULES.remove(rule)
    blocked_names = {BY_ID[i]["name"] for i in blocked}
    combos = [c for r in res["results"] for c in r["combo_suggestions"]
              if c["type"] == "combo"]
    assert combos, "expected PPI combos with admissible add-ons"
    for c in combos:
        assert c["add_on_drug"] not in blocked_names
    # single-drug classes (Alginate, Mucosal Protectant) have no admissible add-on
    assert not {c["add_on_class"] for c in combos} & {"Alginate", "Mucosal Protectant"}


def test_legacy_unknown_safety_withheld():
    rule = {"id": "test_unknown", "applies":
            lambda drug, p: None if drug["id"] == "omeprazole" else False}
    eligibility.HARD_RULES.append(rule)
    try:
        res = asyncio.run(server.query_drugs(_req()))
    finally:
        eligibility.HARD_RULES.remove(rule)
    assert "omeprazole" not in _ids(res["results"]), "unknown safety must not rank"
    row = next(r for r in res["eligible_unranked"] if r["id"] == "omeprazole")
    assert {r["rule"] for r in row["reasons"]} == {"test_unknown", "safety_unknown"}


def test_no_null_safety_fields_left():
    """Every drug except the two non-US drugs has all three safety fields set,
    except the four whose labels are silent on hepatic impairment."""
    no_label = {"vildagliptin", "gliclazide"}
    hep_silent = {"atenolol", "terazosin", "clonidine", "hydralazine"}
    for d in server.drugs:
        if d["id"] in no_label:
            continue
        assert d.get("pregnancy_safety") is not None, d["id"]
        assert d.get("lactation_safety") is not None, d["id"]
        if d["id"] not in hep_silent:
            assert d.get("hepatic_safety") is not None, d["id"]


def test_scoped_and_legacy_share_gate():
    """Same hard verdicts on both paths (design §5.1: one shared evaluator)."""
    patient = _patient(pregnancy_status="third_trimester", hepatic_function="severe")
    for d in server.drugs:
        state, _ = eligibility.hard_gate(d, patient)
        assert (state == "failed") == (d["id"] in PREG_X | HEP_CI), d["id"]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL {t.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR {t.__name__}: {e!r}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
