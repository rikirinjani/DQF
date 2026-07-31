"""
DQF Interactive Query Tool — FastAPI backend.

Endpoints:
  GET  /api/health   → {"status": "ok", "drugs_count": 9}
  GET  /api/drugs    → full drugs.json payload
  POST /api/query    → ranked drugs with dimension scores
"""

import json, os
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Literal

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

def _compute_efficacy(drug, pain_type, cv_risk):
    """Efficacy score based on L4 clinical data, respecting indication boundaries."""
    cls = drug["class"]
    l3 = drug["l3_systems"]
    l4 = drug["l4_clinical"]
    score = 5.0  # Default fallback

    if cls == "NSAID":
        # NSAIDs treat pain — NNT for pain relief is the right metric
        nnt = l4["nnt_50_pain_relief"]["value"]
        score = max(0.0, 10.0 - (nnt - 2.0) * 2.5)

        # pain_type matches indications → +1
        indications = [ind.lower() for ind in l4["indications"]]
        if any(pain_type in ind for ind in indications):
            score += 1

        # Paracetamol penalty for inflammatory pain (no anti-inflammatory effect)
        if not drug["l3_systems"].get("anti_inflammatory", True) and pain_type == "inflammatory":
            score -= 3

    elif cls == "Statin":
        # Statins prevent CV events — they don't treat pain
        if pain_type and pain_type != "none":
            if cv_risk in ("moderate", "high"):
                nnt = l4["nnt_mace_5yr"]["value"]
                score = 9.0 - (nnt - 40.0) * (2.0 / 15.0)
            else:
                score = 0.5
        else:
            nnt = l4["nnt_mace_5yr"]["value"]
            score = 9.0 - (nnt - 40.0) * (2.0 / 15.0)

    elif cls in ("PPI", "H2RA", "Antacid", "Alginate"):
        # GI drugs — score based on healing rate + acid suppression
        ee_8wk = l4.get("ee_healing_8wk_pct", 0)
        du_4wk = l4.get("duodenal_ulcer_healing_4wk_pct", 0)
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
        du_8wk = l4.get("du_healing_8wk_pct", 0)
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

    # GI risk penalty when patient has GI risk
    if gi_risk in ("moderate", "high"):
        score -= l3.get("gi_risk", 0)

    # CV risk penalty for NSAIDs when patient has CV risk
    if drug["class"] == "NSAID" and cv_risk in ("moderate", "high"):
        score -= l3.get("cv_risk", 0)

    # Renal risk penalty when patient has impaired renal function
    if renal_function != "normal":
        score -= l3.get("renal_risk", 0)

    # ── Pregnancy penalty ──────────────────────────────────────
    if pregnancy_status != "not_pregnant":
        preg = drug.get("pregnancy_safety", "C")
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
        else:
            penalty = 2
        score -= penalty

    # ── Lactation penalty ──────────────────────────────────────
    if lactation == "yes":
        lact = drug.get("lactation_safety", "caution")
        if lact == "safe":
            penalty = 0
        elif lact == "caution":
            penalty = 1
        elif lact == "avoid":
            penalty = 4  # Statins — limited data
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
        additional_gi = l3.get("gi_risk", 0) * 0.5
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
        score -= l3.get("cdi_risk", 0) * 0.5
        if l3.get("ddi_risk", 0) >= 3:
            score -= 2
        elif l3.get("ddi_risk", 0) >= 2:
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
        if l3.get("ddi_risk", 0) >= 100:
            score -= 2  # 166 drug interactions

    return round(max(0.0, min(10.0, score)), 1)


def _compute_pk(drug, age, renal_function):
    """PK appropriateness score from L2 data + patient factors."""
    pk = drug["l2_pk"]
    l3 = drug["l3_systems"]
    score = 5.0

    # Half-life vs age — longer t½ is better for elderly (adherence)
    if age > 65 and pk["half_life_h"] >= 8:
        score += 1

    # Renal clearance penalty when drug is renally cleared and patient impaired
    renal_pct = pk.get("renal_excretion_pct", 0)
    if renal_pct > 50 and renal_function != "normal":
        penalties = {"mild": 1, "moderate": 2, "severe": 3}
        score -= penalties[renal_function]

    # DDI penalty for elderly on high-DDI drugs
    if age > 65:
        ddi = l3.get("ddi_risk", 0)
        if ddi >= 3:
            score -= 2
        elif ddi == 2:
            score -= 1

    # Special features bonus (enterohepatic recirc, active metabolites, etc.)
    special = pk.get("special", "").lower()
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
        cyp_pct = l3.get("cyp2c19_metabolism_pct", 0)
        if cyp_pct >= 80:
            score -= 1.5  # Unpredictable in poor/extensive metabolizers
        elif cyp_pct >= 50:
            score -= 0.5
        # Bioavailability bonus
        if pk["bioavailability"] >= 70:
            score += 1
        # PK pattern non-linear → penalty
        if "non-linear" in pk.get("special", "").lower():
            score -= 1

    elif drug["class"] == "H2RA":
        # Renal clearance → penalty in renal impairment
        if pk.get("renal_excretion_pct", 0) >= 50 and renal_function != "normal":
            penalties = {"mild": 1, "moderate": 2, "severe": 3}
            score -= penalties[renal_function]
        # Longer t½ → convenience bonus
        if pk["half_life_h"] >= 3:
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
            selectivity = l1.get("selectivity", "").lower()
            if "300x" in selectivity or "co-2 selective" in selectivity:
                score = 8
            elif "preferential" in selectivity:
                score = 7
            elif "balanced" in selectivity:
                score = 5
            else:
                score = 3  # non-COX (paracetamol)

            # Off-target bonus — diclofenac P2X3 blockade
            off_targets = [str(ot).lower() for ot in l3.get("off_targets", [])]
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
        if pain_type and cv_risk == "low":
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
        if reg["type"] != "combo":
            continue
        if reg.get("base_class") == drug_class:
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
        onset = l4.get("onset_min", 999)
        if onset <= 30:
            strengths.append("Fast onset")
        gi = l3.get("gi_risk", 2)
        if gi == 0:
            strengths.append("GI-sparing")
        elif gi <= 1:
            strengths.append("Low GI risk")
    elif drug["class"] == "Statin":
        ldl = l3.get("ldl_reduction_pct", 0)
        if ldl >= 50:
            strengths.append("Potent LDL reduction")
        if l3.get("ddi_risk", 3) == 0:
            strengths.append("No DDI concerns")
        if l3.get("myopathy_risk", 2) <= 0:
            strengths.append("Lowest myopathy risk")
    elif drug["class"] == "PPI":
        ee = l4.get("ee_healing_8wk_pct", 0)
        if ee >= 88:
            strengths.append("Best healing rates")
        if l3.get("ddi_risk", 3) == 0:
            strengths.append("No DDI concerns")
        if "fastest onset" in pk.get("special", "").lower():
            strengths.append("Fastest onset")
        if "cyp2c19-independent" in pk.get("special", "").lower():
            strengths.append("CYP2C19-independent")
    elif drug["class"] == "H2RA":
        if drug["id"] == "famotidine":
            strengths.append("Safest DDI profile")
            if "longest" in pk.get("special", "").lower():
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
    special = pk.get("special", "").lower()
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
        gi = l3.get("gi_risk", 0)
        if gi >= 2 and gi_risk in ("moderate", "high"):
            concerns.append("GI risk")
        cv = l3.get("cv_risk", 0)
        if cv >= 2 and cv_risk in ("moderate", "high"):
            concerns.append("CV risk")
        renal = l3.get("renal_risk", 0)
        if renal >= 1 and renal_function != "normal":
            concerns.append("Renal risk")

    # Indication mismatch: statins don't treat pain
    if drug["class"] == "Statin" and pain_type and cv_risk == "low":
        concerns.append("Not indicated for pain")

    # Short half-life → frequent dosing
    half_life = pk.get("half_life_h", 0)
    if half_life < 4:
        concerns.append("Short t½ requires frequent dosing")

    # Low efficacy
    if scores.get("efficacy", 10) < 6:
        concerns.append("Lower efficacy")

    # DDI burden
    if l3.get("ddi_risk", 0) >= 3:
        concerns.append("High DDI burden")

    # Paracetamol
    if drug["id"] == "paracetamol":
        concerns.append("No anti-inflammatory effect")

    # Statin myopathy
    if drug["class"] == "Statin" and l3.get("myopathy_risk", 2) >= 2:
        concerns.append("Myopathy risk")

    # PPI concerns
    if drug["class"] == "PPI":
        if l3.get("cdi_risk", 0) >= 2:
            concerns.append("CDI risk (long-term)")
        if l3.get("ddi_risk", 3) >= 3:
            concerns.append("High DDI burden")
        if l3.get("cyp2c19_metabolism_pct", 0) >= 80:
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

    # Pregnancy concern
    if pregnancy_status != "not_pregnant":
        preg = drug.get("pregnancy_safety", "C")
        if preg == "X":
            concerns.append("Contraindicated in pregnancy (Category X)")
        elif preg == "C/D" and pregnancy_status == "third_trimester":
            concerns.append("Avoid in 3rd trimester (premature ductus closure)")
        elif preg in ("C", "C/D"):
            concerns.append("Pregnancy caution — limited safety data")

    # Lactation concern
    if lactation == "yes":
        lact = drug.get("lactation_safety", "caution")
        if lact == "avoid":
            concerns.append("Avoid while breastfeeding (lack of safety data)")

    # Hepatic concern
    if hepatic_function != "normal":
        hep = drug.get("hepatic_safety", "safe")
        if hep == "contraindicated":
            concerns.append("Contraindicated in liver disease")
        elif hep == "caution" and hepatic_function in ("moderate", "severe"):
            concerns.append("Caution in hepatic impairment")

    return concerns[:4]


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


@app.post("/api/query")
async def query_drugs(req: QueryRequest):
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
            "overall": round(overall, 1),
            "strengths": strengths,
            "concerns": concerns,
            "combo_suggestions": combo_suggestions,
        })

    # Sort by overall score descending
    results.sort(key=lambda r: r["overall"], reverse=True)

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
