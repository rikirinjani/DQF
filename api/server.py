"""
DQF Interactive Query Tool — FastAPI backend.

Endpoints:
  GET  /api/health   → {"status": "ok", "drugs_count": 9}
  GET  /api/drugs    → full drugs.json payload
  POST /api/query    → ranked drugs with dimension scores
"""

import json, os
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Literal

# N6b narrow vertical slice: eligibility gate + evidence contract (api/eligibility.py).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import eligibility

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
DATA_PATH = Path(__file__).resolve().parent / "drugs.json"
with open(DATA_PATH, encoding="utf-8") as f:
    drugs_data = json.load(f)

drugs = drugs_data["drugs"]

REGIMENS_PATH = Path(__file__).resolve().parent / "regimens.json"
regimens_data = {}
if REGIMENS_PATH.exists():
    with open(REGIMENS_PATH, encoding="utf-8") as f:
        regimens_data = json.load(f)

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class QueryRequest(BaseModel):
    age: int
    renal_function: Literal["normal", "mild", "moderate", "severe"]
    cv_risk: Literal["low", "moderate", "high"]
    gi_risk: Literal["low", "moderate", "high"]
    pain_type: Literal["acute", "chronic", "inflammatory", "none"]
    drug_class: str = "any"
    prioritize: Literal["efficacy", "safety", "balanced"]
    pregnancy_status: Literal["not_pregnant", "first_trimester", "second_trimester", "third_trimester"]
    lactation: Literal["no", "yes"]
    hepatic_function: Literal["normal", "mild", "moderate", "severe"]
    # N6b: optional treatment objective. When set, the request takes the
    # objective-scoped path (eligibility gate + evidence contract + three-state
    # response). When absent, the legacy path runs (flagged deprecated).
    objective: Optional[str] = None

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(title="DQF Interactive Query Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

UI_PATH = Path(__file__).resolve().parent / "query-tool.html"

_UI_CACHE: Optional[str] = None

def _serve_ui():
    global _UI_CACHE
    if _UI_CACHE is None and UI_PATH.exists():
        _UI_CACHE = UI_PATH.read_text(encoding="utf-8")
    if _UI_CACHE:
        return HTMLResponse(_UI_CACHE)
    return HTMLResponse("<h1>DQF Query Tool</h1><p>UI not found.</p>")

@app.get("/", response_class=HTMLResponse)
async def root():
    return _serve_ui()

@app.get("/query-tool.html", response_class=HTMLResponse)
async def query_tool_ui():
    return _serve_ui()

# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

def _num(v, default=0.0):
    """Null-safe numeric coercion for data-fed reads.

    drugs.json carries explicit nulls (e.g. lovastatin.half_life_h,
    cimetidine.cdi_risk, warfarin.onset_min). For an existing key holding
    null, dict.get(key, default) returns None — NOT the default — so any
    downstream comparison (None < 4) raises TypeError. This guard treats
    None / NaN / bool / non-numeric as `default`.
    """
    if isinstance(v, (int, float)) and not isinstance(v, bool) and v == v:
        return v
    return default


def _norm_preg(raw):
    """Normalize pregnancy_safety (code or narrative) to its A..X code.

    Negation-aware (re-assessment regression): _PREG_NORM substring matching
    previously mapped "not contraindicated" to X, imposing the -8 teratogen
    penalty on drugs whose narrative explicitly denies contraindication.
    """
    if raw in ("A", "B", "C", "C/D", "D", "X"):
        return raw
    if not isinstance(raw, str):
        return "C"
    low = raw.lower()
    for frag, code in (("contraindicated", "X"), ("avoid", "D"), ("high risk", "D")):
        if frag in low and ("not " + frag) not in low:
            return code
    return "C"


def _norm_lact(raw):
    """Normalize lactation_safety (code or narrative) to safe/caution/avoid.

    Unknown/null/missing safety data -> caution, never a silent safe.
    """
    if raw in ("safe", "caution", "avoid"):
        return raw
    if not isinstance(raw, str):
        return "caution"
    low = raw.lower()
    if low.startswith("safe"):
        return "safe"
    if low.startswith("caution"):
        return "caution"
    if low.startswith("avoid"):
        return "avoid"
    if low.startswith("compatible"):
        return "safe"  # compatible with breastfeeding (label)
    if low.startswith("unknown"):
        return "caution"  # unknown safety -> caution, never a silent 0
    return "caution"


def _compute_efficacy(drug, pain_type, cv_risk):
    """Efficacy score based on L4 clinical data, respecting indication boundaries."""
    cls = drug["class"]
    l3 = drug["l3_systems"]
    l4 = drug["l4_clinical"]
    score = 5.0  # Default fallback

    if cls == "NSAID":
        # NSAIDs treat pain — NNT for pain relief is the right metric
        nnt_raw = (l4.get("nnt_50_pain_relief") or {}).get("value")
        if not isinstance(nnt_raw, (int, float)) or isinstance(nnt_raw, bool) \
                or nnt_raw != nnt_raw or nnt_raw <= 0:
            nnt = 4.0  # documented fallback (class-median NNT); invalid/absent data must not crash
        else:
            nnt = float(nnt_raw)
        # NaN guard: NaN != NaN above; arithmetic below stays finite
        score = max(0.0, 10.0 - (nnt - 2.0) * 2.5)

        # pain_type matches indications → +1
        indications = [ind.lower() for ind in (l4.get("indications") or [])]
        if any(pain_type in ind for ind in indications):
            score += 1

        # Paracetamol penalty for inflammatory pain (no anti-inflammatory effect)
        if not drug["l3_systems"].get("anti_inflammatory", True) and pain_type == "inflammatory":
            score -= 3

    elif cls == "Statin":
        # Statins prevent CV events — they don't treat pain
        nnt_raw = (l4.get("nnt_mace_5yr") or {}).get("value")
        nnt_ok = isinstance(nnt_raw, (int, float)) and not isinstance(nnt_raw, bool) \
            and nnt_raw == nnt_raw and nnt_raw > 0
        if pain_type and pain_type != "none":
            if cv_risk in ("moderate", "high"):
                # No valid NNT data -> neutral 5.0, never best-in-class
                # (re-assessment RES-01: the old 40.0 anchor scored 9.0,
                # ranking data-less statins at the top of the class)
                score = (9.0 - (float(nnt_raw) - 40.0) * (2.0 / 15.0)) if nnt_ok else 5.0
            else:
                score = 0.5
        else:
            score = (9.0 - (float(nnt_raw) - 40.0) * (2.0 / 15.0)) if nnt_ok else 5.0

    elif cls in ("PPI", "H2RA", "Antacid", "Alginate"):
        # GI drugs — score based on healing rate + acid suppression
        ee_8wk = _num(l4.get("ee_healing_8wk_pct"))
        du_4wk = _num(l4.get("duodenal_ulcer_healing_4wk_pct"))
        healing = l3.get("healing_ability", False)

        if healing and ee_8wk > 0:
            # PPIs and H2RAs — score by EE healing rate (gold standard)
            if ee_8wk >= 90:
                score = 9.0
            elif ee_8wk >= 83:
                score = 8.0
            elif ee_8wk >= 50:
                score = 5.5
            else:
                score = 4.0
        elif healing and du_4wk > 0 and ee_8wk == 0:
            # H2RAs with only DU data — score is adequate for ulcers
            score = 6.0
        elif cls == "Antacid":
            score = 3.0  # Symptomatic relief only, no healing
        elif cls == "Alginate":
            if l3.get("regurgitation_targeted", False):
                score = 4.5  # Unique benefit for regurgitation, but no healing
            else:
                score = 3.5
        else:
            score = 4.0

    elif cls == "Mucosal Protectant":
        # Sucralfate — topical barrier healing with moderate efficacy
        du_8wk = _num(l4.get("du_healing_8wk_pct"))
        if du_8wk >= 78:
            score = 7.0
        elif du_8wk >= 70:
            score = 6.0
        else:
            score = 5.0

    return round(max(0.0, min(10.0, score)), 1)


def _compute_safety(drug, gi_risk, cv_risk, renal_function, age, pregnancy_status, lactation, hepatic_function):
    """Safety score from L3 systems data + patient risk factors."""
    l3 = drug["l3_systems"]
    score = 10.0

    # GI risk penalty when patient has GI risk. Anticoagulants carry the GI
    # dimension as gi_bleeding_risk (no gi_risk key at all) — coalesce so
    # they don't silently escape the penalty (re-assessment REG-01).
    if gi_risk in ("moderate", "high"):
        gi = l3.get("gi_risk")
        if gi is None:
            gi = l3.get("gi_bleeding_risk")
        score -= _num(gi)

    # CV risk penalty for NSAIDs when patient has CV risk
    if drug["class"] == "NSAID" and cv_risk in ("moderate", "high"):
        score -= _num(l3.get("cv_risk"))

    # Renal risk penalty when patient has impaired renal function
    if renal_function != "normal":
        score -= _num(l3.get("renal_risk"))

    # ── Pregnancy penalty ──────────────────────────────────────
    # Normalize narrative statuses ("contraindicated ... (label)") to the
    # worst-case code so they hit the intended branch instead of the else
    # default; keep the original string for the concern generator.
    preg_raw = drug.get("pregnancy_safety", "C")
    preg = _norm_preg(preg_raw)
    if pregnancy_status != "not_pregnant":
        penalty = 2  # default when no specific category matches
        if preg == "A":
            penalty = 0  # Antacids/alginate — non-systemic
        elif preg == "B":
            if drug["id"] in ("paracetamol",):
                penalty = 0  # Safest analgesic in pregnancy
            else:
                penalty = 1  # PPIs, H2RAs, sucralfate
        elif preg == "C":
            penalty = 3  # Omeprazole
        elif preg == "C/D":
            if pregnancy_status == "third_trimester":
                penalty = 6  # NSAID 3rd tri — ductus closure
            else:
                penalty = 2  # NSAID 1st/2nd tri — caution
        elif preg == "X":
            penalty = 8  # Statins — teratogenic
        elif preg == "D":
            penalty = 6
        score -= penalty

    # ── Lactation penalty ──────────────────────────────────────
    # penalty is ALWAYS initialized (the pregnancy block above no longer owns
    # this variable: with pregnancy_status == "not_pregnant" it never ran, and
    # the old fall-through raised NameError / reused a stale pregnancy value
    # for unrecognized lactation strings like "compatible (label)").
    if lactation == "yes":
        lact = _norm_lact(drug.get("lactation_safety"))
        if lact == "safe":
            penalty = 0
        elif lact == "caution":
            penalty = 1
        elif lact == "avoid":
            penalty = 4  # Statins — limited data
        else:
            penalty = 1
        score -= penalty

    # ── Hepatic impairment penalty ──────────────────────────────
    if hepatic_function != "normal":
        hep = drug.get("hepatic_safety", "safe")
        if hep == "contraindicated":
            penalty = 6 if hepatic_function in ("moderate", "severe") else 3
        elif hep == "caution":
            penalty = 2 if hepatic_function in ("moderate", "severe") else 1
        elif hep == "safe":
            penalty = 0
        else:
            penalty = 1
        score -= penalty

    # ── Elderly GI amplification (age > 65 + NSAID + GI risk) ──
    if drug["class"] == "NSAID" and age > 65 and gi_risk in ("moderate", "high"):
        additional_gi = _num(l3.get("gi_risk")) * 0.5
        score -= additional_gi

    # Paracetamol gets +2 safety bonus (zero COX-mediated risks)
    if drug["id"] == "paracetamol":
        score += 2

    # Pravastatin / Pitavastatin get +1 (zero DDI, low myopathy)
    if drug["id"] in ("pravastatin", "pitavastatin"):
        score += 1

    # GI drug safety

    if drug["class"] == "PPI":
        # PPI-specific safety considerations
        score -= _num(l3.get("cdi_risk")) * 0.5
        ddi = _num(l3.get("ddi_risk"))
        if ddi >= 3:
            score -= 2
        elif ddi >= 2:
            score -= 1
        if renal_function != "normal":
            score -= 1  # CKD risk signal

    elif drug["class"] == "H2RA":
        if drug["id"] == "cimetidine":
            score -= 3  # Broad CYP inhibition, antiandrogenic effects
        elif drug["id"] == "ranitidine":
            score -= 1  # NDMA concern (withdrawn)
        # famotidine: no deductions — cleanest profile

    elif drug["class"] == "Antacid":
        if renal_function != "normal":
            if drug["id"] == "calcium-carbonate":
                score -= 3  # Milk-alkali syndrome, hypercalcemia in CKD
            else:
                score -= 2  # Aluminum/magnesium accumulation in CKD
        if drug["id"] == "calcium-carbonate":
            score -= 1  # Acid rebound concern

    elif drug["class"] == "Alginate":
        # Sodium load concern — minor penalty for CKD/hypertension
        if renal_function != "normal":
            score -= 1

    elif drug["class"] == "Mucosal Protectant":
        # Sucralfate — safe in general population, critical in CKD
        if renal_function != "normal":
            score -= 4  # Aluminum accumulation in CKD
        if _num(l3.get("ddi_risk")) >= 3:
            score -= 2  # chelation/adsorption interactions (1-3 scale)

    return round(max(0.0, min(10.0, score)), 1)


def _compute_pk(drug, age, renal_function):
    """PK appropriateness score from L2 data + patient factors."""
    pk = drug["l2_pk"]
    l3 = drug["l3_systems"]
    score = 5.0
    # Null-safe half-life: explicit null (e.g. lovastatin) or missing must not
    # crash the comparison; treated as "no long-half-life bonus".
    half_life = pk.get("half_life_h")
    half_life = half_life if isinstance(half_life, (int, float)) and not isinstance(half_life, bool) else 0.0

    # Half-life vs age — longer t½ is better for elderly (adherence)
    if age > 65 and half_life >= 8:
        score += 1

    # Renal clearance penalty when drug is renally cleared and patient impaired.
    # H2RA block below re-applies its own renal rule; the generic one is skipped
    # for H2RA to avoid double-counting the same clearance up to -6.
    renal_pct = pk.get("renal_excretion_pct", 0)
    renal_pct = renal_pct if isinstance(renal_pct, (int, float)) and not isinstance(renal_pct, bool) else 0
    if drug["class"] != "H2RA" and renal_pct > 50 and renal_function != "normal":
        penalties = {"mild": 1, "moderate": 2, "severe": 3}
        score -= penalties[renal_function]

    # DDI penalty for elderly on high-DDI drugs
    if age > 65:
        ddi = _num(l3.get("ddi_risk"))
        if ddi >= 3:
            score -= 2
        elif ddi == 2:
            score -= 1

    # Special features bonus (enterohepatic recirc, active metabolites, etc.)
    special = (pk.get("special") or "").lower()
    bonus_keywords = [
        "enterohepatic",
        "active metabolite",
        "qd dosing",
        "prolonged synovial",
        "unique bcrp",
    ]
    if any(kw in special for kw in bonus_keywords):
        score += 1

    # GI drug PK considerations
    if drug["class"] == "PPI":
        # CYP2C19 genotype dependency → penalty for high dependency
        cyp_pct = _num(l3.get("cyp2c19_metabolism_pct"))
        if cyp_pct >= 80:
            score -= 1.5  # Unpredictable in poor/extensive metabolizers
        elif cyp_pct >= 50:
            score -= 0.5
        # Bioavailability bonus (null-safe: explicit null/missing = no bonus)
        bioavail = pk.get("bioavailability")
        bioavail = bioavail if isinstance(bioavail, (int, float)) and not isinstance(bioavail, bool) else 0
        if bioavail >= 70:
            score += 1
        # PK pattern non-linear → penalty
        if "non-linear" in (pk.get("special") or "").lower():
            score -= 1

    elif drug["class"] == "H2RA":
        # Renal clearance → penalty in renal impairment (sole renal rule for
        # this class — the generic penalty above is skipped for H2RA)
        # > 50 (not >= 50) — harmonized with the generic renal-clearance
        # boundary above so the two paths agree at exactly 50%
        if _num(pk.get("renal_excretion_pct")) > 50 and renal_function != "normal":
            penalties = {"mild": 1, "moderate": 2, "severe": 3}
            score -= penalties[renal_function]
        # Longer t½ → convenience bonus (null-safe; same guard as generic path)
        if half_life >= 3:
            score += 1
        # CSF penetration → CNS risk penalty in elderly
        if drug["id"] == "ranitidine" and age > 65:
            score -= 1

    elif drug["class"] in ("Antacid", "Alginate"):
        # Local action only — PK is not a differentiator
        score = 5.0  # Neutral
        # Alginate sodium load → minor elderly penalty
        if drug["class"] == "Alginate" and age > 65:
            score -= 0.5

    elif drug["class"] == "Mucosal Protectant":
        # Non-systemic — unique PK; QID dosing burden
        score = 4.0
        if age > 65:
            score -= 0.5  # QID adherence concern in elderly
        if renal_function != "normal":
            score -= 1  # Aluminum accumulation concern

    return round(max(0.0, min(10.0, score)), 1)


def _compute_mechanism(drug, pain_type, cv_risk):
    """Mechanism-match score from L1 binding data + pain type."""
    cls = drug["class"]
    l1 = drug["l1_binding"]
    l3 = drug["l3_systems"]

    if cls == "NSAID":
        if pain_type == "inflammatory":
            # COX-2 selectivity scoring for inflammatory pain
            selectivity = (l1.get("selectivity") or "").lower()
            if "300x" in selectivity or "cox-2 selective" in selectivity:
                score = 8
            elif "preferential" in selectivity:
                score = 7
            elif "balanced" in selectivity:
                score = 5
            else:
                score = 3  # non-COX (paracetamol)

            # Off-target bonus — diclofenac P2X3 blockade
            off_targets = [str(ot).lower() for ot in (l3.get("off_targets") or [])]
            if any("p2x3" in ot for ot in off_targets):
                score += 2
        else:
            # Non-inflammatory pain (acute, chronic)
            score = 5
            # Paracetamol matches mild pain profile
            if drug["id"] == "paracetamol":
                score += 1
    else:  # Statin
        # Statins don't treat pain — mechanism score reflects indication match
        if pain_type and pain_type != "none" and cv_risk == "low":
            score = 0  # Pain is the concern and no CV risk → statins irrelevant
        elif cv_risk in ("moderate", "high"):
            score = 7  # CV risk present → HMGCR inhibition is relevant
        else:
            score = 3

    # GI drugs — mechanism scores based on target precision
    if cls in ("PPI", "H2RA", "Antacid", "Alginate"):
        if cls == "PPI":
            score = 8  # Highly targeted (single enzyme, irreversible)
            # Bonus for unique binding features
            if drug["id"] == "pantoprazole":
                score += 1  # Cys822 deep binding → longest duration
            elif drug["id"] == "rabeprazole":
                score += 1  # CYP2C19-independent → consistent across genotypes
        elif cls == "H2RA":
            score = 6  # Targeted receptor antagonism
            if drug["id"] == "famotidine":
                score += 1  # Most potent, inverse agonist, no off-targets
            elif drug["id"] == "cimetidine":
                score -= 1  # Off-target androgen receptor binding
            elif drug["id"] == "ranitidine":
                score -= 1  # NDMA concern
        elif cls == "Antacid":
            score = 3  # Non-targeted chemical neutralization
            if drug["id"] == "aluminum-magnesium-hydroxide":
                score += 1  # Balanced formulation (offset GI effects)
        elif cls == "Alginate":
            score = 6  # Unique physical barrier — differentiated mechanism

    # Mucosal Protectant — highly differentiated mechanism
    if cls == "Mucosal Protectant":
        score = 7  # Unique topical barrier + cytoprotection, zero acid suppression

    return round(max(0.0, min(10.0, score)), 1)


def _get_combo_suggestions(drug, regimens):
    """For a given top-ranked drug, find relevant combo regimens."""
    suggestions = []
    condition = regimens.get("conditions", {}).get("gastritis_gerd", {})
    regimens_list = condition.get("regimens", [])

    drug_class = drug["class"]
    for reg in regimens_list:
        if reg.get("type") == "combo":
            if reg.get("base_class") != drug_class:
                continue
            add_on_class = reg["add_on_class"]
            # Find a representative drug from that class
            add_on_drugs = [d for d in drugs if d["class"] == add_on_class]
            add_on_name = add_on_drugs[0]["name"] if add_on_drugs else add_on_class
            suggestions.append({
                "regimen_id": reg["id"],
                "label": reg["label"],
                "type": "combo",
                "add_on_class": add_on_class,
                "add_on_drug": add_on_name,
                "mechanism": reg.get("incremental_benefit", ""),
                "evidence": reg.get("evidence", ""),
                "safety_delta": reg.get("safety_delta", ""),
                "note": reg.get("note", ""),
            })
        elif reg.get("type") == "mono" and reg.get("drug_class") == drug_class:
            # NOTE: previously UNREACHABLE — an early `continue` on non-combo
            # regimens skipped this branch entirely, so monotherapy suggestions
            # never appeared in the output.
            suggestions.append({
                "regimen_id": reg["id"],
                "label": f"Best as monotherapy — {reg['label']}",
                "type": "mono",
                "evidence": reg.get("evidence", ""),
                "healing_rate": reg.get("healing_8wk_pct"),
                "note": reg.get("note", ""),
            })

    return suggestions


# ---------------------------------------------------------------------------
# Strengths / concerns generators
# ---------------------------------------------------------------------------

def _generate_strengths(drug, scores):
    """Generate 1–4 bullet-point strengths from drug data."""
    strengths = []
    l3 = drug["l3_systems"]
    l4 = drug["l4_clinical"]
    pk = drug["l2_pk"]

    if drug["class"] == "NSAID":
        onset = _num(l4.get("onset_min"), 999)
        if onset <= 30:
            strengths.append("Fast onset")
        gi = _num(l3.get("gi_risk"), 2)
        if gi == 0:
            strengths.append("GI-sparing")
        elif gi <= 1:
            strengths.append("Low GI risk")
    elif drug["class"] == "Statin":
        ldl = _num(l3.get("ldl_reduction_pct"))
        if ldl >= 50:
            strengths.append("Potent LDL reduction")
        if _num(l3.get("ddi_risk"), 3) == 0:
            strengths.append("No DDI concerns")
        if _num(l3.get("myopathy_risk"), 2) <= 0:
            strengths.append("Lowest myopathy risk")
    elif drug["class"] == "PPI":
        ee = _num(l4.get("ee_healing_8wk_pct"))
        if ee >= 88:
            strengths.append("Best healing rates")
        if _num(l3.get("ddi_risk"), 3) == 0:
            strengths.append("No DDI concerns")
        if "fastest onset" in (pk.get("special") or "").lower():
            strengths.append("Fastest onset")
        if "cyp2c19-independent" in (pk.get("special") or "").lower():
            strengths.append("CYP2C19-independent")
    elif drug["class"] == "H2RA":
        if drug["id"] == "famotidine":
            strengths.append("Safest DDI profile")
            if "longest" in (pk.get("special") or "").lower():
                strengths.append("Longest duration")
        if drug["id"] == "ranitidine":
            strengths.append("High potency")
    elif drug["class"] == "Antacid":
        strengths.append("Fast symptom relief")
    elif drug["class"] == "Alginate":
        strengths.append("Targets regurgitation")
        strengths.append("Safest in pregnancy")
    elif drug["class"] == "Mucosal Protectant":
        strengths.append("Unique barrier mechanism")
        strengths.append("No acid suppression side effects")

    # Efficacy-based
    if scores.get("efficacy", 0) >= 7:
        strengths.append("Good efficacy")

    # Special features
    special = (pk.get("special") or "").lower()
    if "active metabolite" in special:
        strengths.append("Active metabolites")
    if "hydrophilic" in special:
        strengths.append("Hydrophilic")

    # Drug-specific
    if drug["id"] == "ibuprofen":
        if "Low cost" not in strengths:
            strengths.append("Low cost")

    return strengths[:4]


def _generate_concerns(drug, scores, gi_risk, cv_risk, renal_function, pain_type, pregnancy_status, lactation, hepatic_function):
    """Generate 1–4 bullet-point concerns from drug data + patient risk."""
    concerns = []
    l3 = drug["l3_systems"]
    pk = drug["l2_pk"]

    if drug["class"] == "NSAID":
        gi = _num(l3.get("gi_risk"))
        if gi >= 2 and gi_risk in ("moderate", "high"):
            concerns.append("GI risk")
        cv = _num(l3.get("cv_risk"))
        if cv >= 2 and cv_risk in ("moderate", "high"):
            concerns.append("CV risk")
        renal = _num(l3.get("renal_risk"))
        if renal >= 1 and renal_function != "normal":
            concerns.append("Renal risk")

    # Indication mismatch: statins don't treat pain (pain_type "none" is not
    # a pain request — never penalize statins for it, re-assessment RES-04)
    if drug["class"] == "Statin" and pain_type and pain_type != "none" and cv_risk == "low":
        concerns.append("Not indicated for pain")

    # Short half-life → frequent dosing. Unknown/zero half-life (explicit
    # null or 0 in drugs.json, e.g. lovastatin) emits nothing — a missing
    # value is not evidence of a short t½ (re-assessment REG-02).
    half_life = _num(pk.get("half_life_h"))
    if 0 < half_life < 4:
        concerns.append("Short t½ requires frequent dosing")

    # Low efficacy
    if scores.get("efficacy", 10) < 6:
        concerns.append("Lower efficacy")

    # DDI burden
    if _num(l3.get("ddi_risk")) >= 3:
        concerns.append("High DDI burden")

    # Paracetamol
    if drug["id"] == "paracetamol":
        concerns.append("No anti-inflammatory effect")

    # Statin myopathy
    if drug["class"] == "Statin" and _num(l3.get("myopathy_risk"), 2) >= 2:
        concerns.append("Myopathy risk")

    # PPI concerns
    if drug["class"] == "PPI":
        if _num(l3.get("cdi_risk")) >= 2:
            concerns.append("CDI risk (long-term)")
        # (DDI burden is emitted by the generic block above; this block's
        # duplicate consumed two advisory display slots — re-assessment RES-06)
        if _num(l3.get("cyp2c19_metabolism_pct")) >= 80:
            concerns.append("CYP2C19 genotype-dependent")

    # H2RA concerns
    if drug["class"] == "H2RA":
        if drug["id"] == "cimetidine":
            concerns.append("Broad CYP inhibition")
            concerns.append("Antiandrogenic effects")
        elif drug["id"] == "ranitidine":
            concerns.append("Withdrawn (NDMA)")
        if l3.get("tolerance", False):
            concerns.append("Tolerance develops (14d)")

    # Antacid concerns
    if drug["class"] == "Antacid":
        if drug["id"] == "calcium-carbonate":
            concerns.append("Acid rebound")
        concerns.append("No mucosal healing")

    # Alginate concerns
    if drug["class"] == "Alginate":
        concerns.append("No mucosal healing")

    # Mucosal Protectant concerns
    if drug["class"] == "Mucosal Protectant":
        if renal_function != "normal":
            concerns.append("Aluminum toxicity (CKD)")
        concerns.append("QID dosing burden")

    # Pregnancy concern — normalize narrative statuses the same way the
    # safety scorer does, so "contraindicated (label)" emits the critical
    # warning instead of falling through to the generic caution.
    if pregnancy_status != "not_pregnant":
        preg = _norm_preg(drug.get("pregnancy_safety", "C"))
        if preg == "X":
            concerns.append("Contraindicated in pregnancy (Category X)")
        elif preg == "C/D" and pregnancy_status == "third_trimester":
            concerns.append("Avoid in 3rd trimester (premature ductus closure)")
        elif preg == "D":
            concerns.append("Avoid in pregnancy (Category D)")
        elif preg in ("C", "C/D"):
            concerns.append("Pregnancy caution — limited safety data")

    # Lactation concern — same narrative normalization as the safety scorer.
    if lactation == "yes":
        if _norm_lact(drug.get("lactation_safety")) == "avoid":
            concerns.append("Avoid while breastfeeding (lack of safety data)")

    # Hepatic concern
    if hepatic_function != "normal":
        hep = drug.get("hepatic_safety", "safe")
        if hep == "contraindicated":
            concerns.append("Contraindicated in liver disease")
        elif hep == "caution" and hepatic_function in ("moderate", "severe"):
            concerns.append("Caution in hepatic impairment")

    # Critical safety warnings (contraindication-grade) must survive any
    # truncation: they are emitted verbatim at the FRONT of the list, ahead
    # of the [:4] display cap applied to the advisory remainder.
    _CRITICAL_MARKERS = ("Contraindicated", "Avoid in", "Avoid while")
    critical = [c for c in concerns if any(c.startswith(m) for m in _CRITICAL_MARKERS)]
    advisory = [c for c in concerns if c not in critical]
    return (critical + advisory[:max(0, 4 - len(critical))])


# ---------------------------------------------------------------------------
# Weights per prioritization mode
# ---------------------------------------------------------------------------
WEIGHTS = {
    "efficacy":  {"efficacy": 0.40, "safety": 0.25, "pk": 0.20, "mechanism": 0.15},
    "safety":    {"efficacy": 0.20, "safety": 0.50, "pk": 0.20, "mechanism": 0.10},
    "balanced":  {"efficacy": 0.30, "safety": 0.30, "pk": 0.20, "mechanism": 0.20},
}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health():
    return {"status": "ok", "drugs_count": len(drugs)}


@app.get("/api/drugs")
async def get_drugs():
    return drugs_data


def _compute_mechanism_scoped(drug, objective):
    """Condition-aware mechanism for the scoped path (no pain/cv inputs).

    The legacy `_compute_mechanism` treats every non-NSAID class as a statin and
    lets pain_type/cv_risk influence the score (re-assessment F09). The scoped
    path scores mechanism from the objective's class only; unsupported classes
    get a documented neutral rather than a statin-derived value.
    """
    cls = drug["class"]
    if cls == "PPI":
        score = 8  # highly targeted (single enzyme, irreversible)
        if drug["id"] == "pantoprazole":
            score += 1  # Cys822 deep binding -> longest duration
        elif drug["id"] == "rabeprazole":
            score += 1  # CYP2C19-independent -> consistent across genotypes
        return round(max(0.0, min(10.0, score)), 1)
    return 5.0  # unsupported class for this objective -> documented neutral


def _query_scoped(req):
    """Objective-scoped path: eligibility gate -> evidence contract -> ranking.

    Three states (review F02): eligible_ranked / eligible_unranked / excluded.
    No neutral-score imputation; no cross-endpoint fallback; combo suggestions
    disabled in v1 (review F08).
    """
    objective = req.objective
    if not eligibility.objective_exists(objective):
        return {
            "schema_version": "2.0",
            "mode": "objective_scoped",
            "status": "unsupported",
            "objective": objective,
            "eligible_ranked": [],
            "eligible_unranked": [],
            "excluded": [],
            "filter_effects": {},
            "summary": f"Objective '{objective}' is not supported in v1.",
        }

    # Optional class narrowing filter (reported separately from clinical exclusions)
    candidate_drugs = drugs
    filter_effects = {}
    if req.drug_class != "any":
        selected_classes = set(c.strip().title() for c in req.drug_class.split(",") if c.strip())
        class_name_map = {
            "Nsai": "NSAID", "Nsaid": "NSAID", "Statin": "Statin", "Ppi": "PPI",
            "H2ra": "H2RA", "H2Ra": "H2RA", "Antacid": "Antacid", "Alginate": "Alginate",
            "Mucosal": "Mucosal Protectant",
        }
        resolved = set(class_name_map.get(s, s) for s in selected_classes)
        candidate_drugs = [d for d in drugs if d["class"] in resolved]
        filter_effects = {"class_filter": sorted(resolved),
                          "removed": len(drugs) - len(candidate_drugs)}

    patient = {
        "pregnancy_status": req.pregnancy_status,
        "hepatic_function": req.hepatic_function,
        "renal_function": req.renal_function,
        "age": req.age,
    }
    res = eligibility.assess(candidate_drugs, objective, patient)

    ranked = []
    for item in res["eligible_ranked"]:
        drug = item["drug"]
        scores = {
            "efficacy": item["efficacy"],
            "safety": _compute_safety(drug, req.gi_risk, req.cv_risk, req.renal_function,
                                      req.age, req.pregnancy_status, req.lactation,
                                      req.hepatic_function),
            "pk": _compute_pk(drug, req.age, req.renal_function),
            "mechanism": _compute_mechanism_scoped(drug, objective),
        }
        w = WEIGHTS[req.prioritize]
        overall = (w["efficacy"] * scores["efficacy"] + w["safety"] * scores["safety"]
                   + w["pk"] * scores["pk"] + w["mechanism"] * scores["mechanism"])
        ranked.append({
            "id": drug["id"], "name": drug["name"], "class": drug["class"],
            "scores": scores,
            "_overall_raw": overall,
            "overall": round(overall, 1),
            "evidence": item["evidence"],
            "strengths": _generate_strengths(drug, scores),
            "concerns": _generate_concerns(drug, scores, req.gi_risk, req.cv_risk,
                                           req.renal_function, req.pain_type,
                                           req.pregnancy_status, req.lactation,
                                           req.hepatic_function),
            "combo_suggestions": [],  # disabled in scoped v1 (review F08)
        })
    ranked.sort(key=lambda r: r["_overall_raw"], reverse=True)
    for r in ranked:
        r.pop("_overall_raw", None)

    status = res["status"]
    if status == "ok":
        best = ranked[0]
        summary = (f"Best option among ranked candidates for {objective} in the evaluated "
                   f"catalogue: {best['name']} (overall {best['overall']}/10).")
    elif status == "no_rankable":
        summary = (f"No rankable option for {objective}: eligible drugs lack compatible "
                   f"evidence in the evaluated catalogue.")
    else:
        summary = (f"No eligible option found for {objective} in the evaluated "
                   f"catalogue/filter.")

    return {
        "schema_version": "2.0",
        "mode": "objective_scoped",
        "status": status,
        "objective": objective,
        "eligible_ranked": ranked,
        "eligible_unranked": res["eligible_unranked"],
        "excluded": res["excluded"],
        "filter_effects": filter_effects,
        "summary": summary,
    }


@app.post("/api/query")
async def query_drugs(req: QueryRequest):
    # N6b: objective-scoped path (eligibility gate + evidence contract).
    if req.objective:
        return _query_scoped(req)

    # Filter by drug class
    candidate_drugs = drugs
    if req.drug_class != "any":
        selected_classes = set(c.strip().title() for c in req.drug_class.split(",") if c.strip())
        # Map short names to display names
        class_name_map = {
            "Nsai": "NSAID",
            "Nsaid": "NSAID",
            "Statin": "Statin",
            "Ppi": "PPI",
            "H2ra": "H2RA",
            "H2Ra": "H2RA",
            "Antacid": "Antacid",
            "Alginate": "Alginate",
            "Mucosal": "Mucosal Protectant",
        }
        resolved = set()
        for s in selected_classes:
            resolved.add(class_name_map.get(s, s))
        candidate_drugs = [d for d in drugs if d["class"] in resolved]

    results = []
    for drug in candidate_drugs:
        scores = {
            "efficacy": _compute_efficacy(drug, req.pain_type, req.cv_risk),
            "safety": _compute_safety(drug, req.gi_risk, req.cv_risk, req.renal_function,
                                      req.age, req.pregnancy_status, req.lactation, req.hepatic_function),
            "pk": _compute_pk(drug, req.age, req.renal_function),
            "mechanism": _compute_mechanism(drug, req.pain_type, req.cv_risk),
        }

        w = WEIGHTS[req.prioritize]
        overall = (
            w["efficacy"] * scores["efficacy"]
            + w["safety"] * scores["safety"]
            + w["pk"] * scores["pk"]
            + w["mechanism"] * scores["mechanism"]
        )

        strengths = _generate_strengths(drug, scores)
        concerns = _generate_concerns(
            drug, scores, req.gi_risk, req.cv_risk, req.renal_function, req.pain_type,
            req.pregnancy_status, req.lactation, req.hepatic_function
        )
        combo_suggestions = _get_combo_suggestions(drug, regimens_data)

        results.append({
            "id": drug["id"],
            "name": drug["name"],
            "class": drug["class"],
            "scores": scores,
            # full precision kept on the dict for sorting; display rounding
            # happens at serialization so ranking is not tie-broken by
            # dataset order
            "_overall_raw": overall,
            "overall": round(overall, 1),
            "strengths": strengths,
            "concerns": concerns,
            "combo_suggestions": combo_suggestions,
        })

    # Sort by overall score descending at FULL precision (rounding only for
    # display; premature rounding created artificial ties resolved by
    # dataset order)
    results.sort(key=lambda r: r["_overall_raw"], reverse=True)
    for r in results:
        r.pop("_overall_raw", None)

    # Generate summary
    if results:
        best = results[0]
        summary = (
            f"Best choice for this profile: {best['name']} "
            f"(scores {best['overall']}/10 overall — "
            f"efficacy {best['scores']['efficacy']}, "
            f"safety {best['scores']['safety']})"
        )
    else:
        summary = "No drugs match the specified criteria."

    return {
        "schema_version": "1.0",
        "mode": "legacy",
        "deprecated": True,
        "deprecation_note": "Legacy cross-indication ranking is not objective-scoped; "
                            "pass `objective` for the scoped path (N6b).",
        "query": req.model_dump(),
        "results": results,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# CLI runner
# ---------------------------------------------------------------------------

def main():
    counts = {}
    for d in drugs:
        cls = d['class']
        counts[cls] = counts.get(cls, 0) + 1
    labels = [f"{v} {k}s" if not k.endswith('s') else f"{v} {k}" for k, v in counts.items()]
    banner = f"""
{'=' * 60}
  DQF Interactive Query Tool
  Drug Quantification Framework
{'=' * 60}
  Loaded {len(drugs)} drugs: {', '.join(labels)}
  Endpoints:
    GET  /api/health
    GET  /api/drugs
    POST /api/query
{'=' * 60}
"""
    print(banner)

    legend = """
  ─── SCORE LEGEND ──────────────────────────────────────────
  9–10  Best-in-class        │  7–8   Strong performer
  5–6   Adequate             │  3–4   Limited
  1–2   Poor fit for profile │
  ─── CLASS LEGEND ──────────────────────────────────────────
  NSAID            Pain & inflammation      Statin         CV prevention
  PPI              Acid suppression (best)   H2RA           Acid suppression (moderate)
  Antacid          Symptom relief only       Alginate       Regurgitation barrier
  Mucosal Prot.    Barrier + cytoprotection
  --- SCORE COMPONENTS ---------------------------------────────
  Efficacy   Healing rates / NNT for the target indication
  Safety     AE profile, drug interactions (DDI), organ toxicity
  PK         Dosing convenience — half-life, frequency, clearance, absorption
  Mechanism  How precisely the MOA fits the patient's condition
  Overall    Weighted composite (default 30/30/20/20 efficacy/safety/PK/mech)

  Adapted from the Drug Quantification Framework [Manuscript — TB Submitted]
"""
    print(legend)
    uvicorn.run("server:app", host="0.0.0.0", port=8765, reload=False)


if __name__ == "__main__":
    main()
