# Phase 2 — Anticoagulant class: template + scorer design (draft for review)

Scope: wire the new `Anticoagulant` class into the L3 pipeline (templates, scorer, audit
directions, salt vocabulary) so evidence can be fetched and scored. Implementation is
mechanical once this draft is approved. Prerequisite: Phase 1 done (`da124aa`, 6 records in
`api/drugs.json`, `l3_systems: {}`).

Design principle (from Batch 4): dim **direction** is declared up front and carried in
`classifier_audit.DIM_DIRECTION`, so the artifact gate works on day one.

---

## 1. `rag-queries/l3_query_templates.json` — add class entry

```json
"Anticoagulant": {
  "tissue_sites": ["liver", "kidney", "vasculature", "gastrointestinal tract"],
  "tissue_queries": [
    "{drug} anticoagulant mechanism factor Xa thrombin inhibition",
    "{drug} renal clearance elimination pharmacokinetics",
    "{drug} hepatic metabolism CYP3A4 CYP2C9 drug interaction",
    "{drug} gastrointestinal bleeding mucosal effect"
  ],
  "off_target_queries": ["{drug} {target} off-target effect"],
  "class_mechanism_queries": [
    "anticoagulant major bleeding risk intracranial hemorrhage randomized trial",
    "anticoagulant reversal agent antidote andexanet idarucizumab",
    "anticoagulant monitoring INR coagulation assay requirement",
    "{drug} stroke systemic embolism prevention atrial fibrillation"
  ],
  "l3_fields": {
    "anticoagulation_efficacy": null,
    "bleeding_risk": null,
    "renal_clearance_dependence": null,
    "ddi_risk": null,
    "monitoring_burden": null,
    "reversal_availability": null,
    "gi_bleeding_risk": null
  }
}
```
(No `{target}` off-target terms are populated by default — warfarin/enoxaparin have no small-
molecule L1 target; the empty `off_target_queries` fallback simply yields no off-target probes.
`build_l3_queries` already handles an empty list.)

## 2. `rag-queries/extract_l3.py` — add scorer block

Add `elif drug_class == "Anticoagulant":` (umbrella: VKA / direct-FXa / DTI / LMWH). All 7
dims use `_score_risk` (no custom scorer needed).

```python
    elif drug_class == "Anticoagulant":
        # Umbrella class: VKA (warfarin), direct FXa inhibitors (apixaban,
        # rivaroxaban, edoxaban), direct thrombin inhibitor (dabigatran),
        # LMWH (enoxaparin). Dimensions:
        #   anticoagulation_efficacy    1-3 benefit (stroke/SE + VTE prevention)
        #   bleeding_risk               1-3 risk    (major bleeding / ICH)
        #   renal_clearance_dependence  1-3 risk    (renal elimination -> accumulation)
        #   ddi_risk                    1-3 risk    (CYP3A4/P-gp/CYP2C9)
        #   monitoring_burden           1-3 risk    (INR/coag monitoring; higher = worse)
        #   reversal_availability       1-3 benefit (specific antidote exists)
        #   gi_bleeding_risk            1-3 risk    (gastrointestinal bleeding)
        profile["anticoagulation_efficacy"] = _score_risk(findings,
            keywords=["stroke", "systemic embolism", "venous thromboembolism",
                      "vte", "deep vein thrombosis", "dvt", "pulmonary embolism",
                      "non-inferior", "noninferior", "prevention of stroke"],
            intensifiers=["superior", "significant reduction", "reduced risk",
                          "effective", "significant"],
            mitigators=["no difference", "not superior", "inferior", "no benefit"],
            default=1,
            pk_contexts=["clearance", "pharmacokinetic", "half-life",
                         "bioavailability", "absorption"],
            drug_name=drug_name)
        profile["bleeding_risk"] = _score_risk(findings,
            keywords=["major bleeding", "bleeding", "hemorrhage", "haemorrhage",
                      "intracranial hemorrhage", "intracranial haemorrhage", "ich",
                      "gastrointestinal bleeding", "fatal bleeding",
                      "clinically relevant non-major", "crnm"],
            intensifiers=["severe", "fatal", "life-threatening", "major",
                          "significantly increased", "higher risk"],
            mitigators=["no significant", "similar", "comparable", "lower risk",
                        "less bleeding", "rare", "well-tolerated"],
            default=1,
            drug_name=drug_name)
        profile["renal_clearance_dependence"] = _score_risk(findings,
            keywords=["renal clearance", "renal impairment", "renal excretion",
                      "creatinine clearance", "crcl", "renal function", "dialysis",
                      "accumulation", "renal elimination"],
            intensifiers=["severe", "contraindicated", "dose reduction",
                          "dose adjustment", "significant", "accumulation"],
            mitigators=["no dose adjustment", "minimal", "not renally",
                        "renal-independent", "no accumulation"],
            default=1,
            drug_name=drug_name)
        profile["ddi_risk"] = _score_risk(findings,
            keywords=["drug interaction", "interaction", "cyp3a4", "cyp2c9",
                      "p-gp", "p-glycoprotein", "bcrp", "inducer", "inhibitor",
                      "coadministration", "co-administration"],
            intensifiers=["contraindicated", "major", "significant", "avoid",
                          "caution"],
            mitigators=["no interaction", "safe", "well-tolerated", "minimal",
                        "not clinically relevant", "no clinically significant"],
            negations=["limited", "few"],
            default=1,
            drug_name=drug_name)
        profile["monitoring_burden"] = _score_risk(findings,
            keywords=["inr", "international normalized ratio", "monitoring",
                      "coagulation monitoring", "laboratory monitoring",
                      "dose titration", "dose adjustment",
                      "time in therapeutic range", "ttr", "anticoagulation clinic",
                      "anti-xa"],
            intensifiers=["frequent", "requires", "mandatory", "periodic",
                          "regular", "unpredictable"],
            mitigators=["no monitoring", "no routine", "does not require",
                        "without monitoring", "predictable"],
            default=1,
            drug_name=drug_name)
        profile["reversal_availability"] = _score_risk(findings,
            keywords=["reversal", "antidote", "andexanet", "idarucizumab",
                      "vitamin k", "prothrombin complex", "pcc", "protamine",
                      "ciraparantag"],
            intensifiers=["specific", "approved", "rapid", "complete", "effective"],
            mitigators=["no specific", "no antidote", "partial", "not available",
                        "lack of"],
            default=1,
            drug_name=drug_name)
        profile["gi_bleeding_risk"] = _score_risk(findings,
            keywords=["gastrointestinal bleeding", "gi bleeding",
                      "gastrointestinal hemorrhage", "gastrointestinal haemorrhage",
                      "dyspepsia", "gastrointestinal adverse", "upper gastrointestinal"],
            intensifiers=["significant", "higher", "increased", "severe"],
            mitigators=["lower", "similar", "no significant", "less"],
            default=1,
            drug_name=drug_name)
```

### Scorer design notes (non-obvious choices)

1. **`pk_contexts` deliberately EMPTY for `renal_clearance_dependence` and `ddi_risk`.**
   In those dims "clearance"/"interaction" *is* the evidence; the pk_context gate would skip
   every relevant sentence. It is set only on `anticoagulation_efficacy` (there, PK statements
   must not count as outcome evidence).
2. **No `adverse_context_terms` on risk dims.** That gate exists to stop harm mentions counting
   as *benefit* evidence; for `bleeding_risk`/`gi_bleeding_risk` the harm mention is the evidence.
3. **`monitoring_burden` is risk-typed** (higher = worse). Its keywords overlap `dose adjustment`
   with renal dims — acceptable; scoping is per-dimension.
4. **`ddi_risk` carries `negations=["limited","few"]`** (consistent with the other 8 classes).
5. Warfarin will legitimately score **low** on `renal_clearance_dependence` (hepatic metabolism)
   and **high** on `monitoring_burden` (INR mandatory) — the intended contrast.

## 3. `rag-queries/classifier_audit.py` — `DIM_DIRECTION` additions

```python
    "anticoagulation_efficacy": "benefit",
    "bleeding_risk": "risk",
    "renal_clearance_dependence": "risk",
    "monitoring_burden": "risk",
    "reversal_availability": "benefit",
    "gi_bleeding_risk": "risk",
    # "ddi_risk": "risk"  (already present)
```

## 4. Salt vocabulary (`extract_l3.py`)

Names are **auto-covered**: `_build_salt_name_re()` reads `load_drugs()`, so apixaban /
rivaroxaban / edoxaban / dabigatran / enoxaparin / warfarin (already in `_SALT_EXTRA_DRUGS`) are
masked automatically. Suffixes: `sodium` ✓ and `tosylate` ✓ are already in `_SALT_ANIONS`;
**add `etexilate`** (dabigatran etexilate) and, for UK spelling, **`tosilate`**.

```python
    r"embonate|napsylate|isethionate|mandelate|alginate|polystyrene|"
    r"etexilate|tosilate|"                      # <- add here
```
Guard check: `_SALT_KEEP_PREFIXES` already contains `renal|hepatic|gastrointestinal|...`, so
"renal clearance" etc. are not consumed by the generic drug+suffix rule.

## 5. Verification plan (proportionate)

- `python -m py_compile rag-queries/extract_l3.py`; template JSON parses; 7 `l3_fields` present.
- New unit tests (extend `rag-queries/test_scorer_hardening.py` or add
  `rag-queries/test_anticoagulant_scorer.py`), asserting:
  - warfarin INR sentence → `monitoring_burden` >= 2; apixaban "no routine monitoring" → 1
  - dabigatran "80% renal" sentence → `renal_clearance_dependence` >= 2
  - rivaroxaban "combined P-gp and strong CYP3A4" → `ddi_risk` >= 2
  - "andexanet alfa reverses anti-Xa" → `reversal_availability` >= 2
  - salt masking: "dabigatran etexilate" sentence does not leak into a keyword
  - `pk_contexts` guard: a pure PK sentence scores 1 on `anticoagulation_efficacy`
- `build_l3_queries` check for an anticoagulant drug (emits tissue + class_mechanism probes).
- **Deferred to post-fetch:** the full-dimensional before/after diff (it iterates
  `judge_input.json` pools; anticoagulant pools don't exist until the L3 fetch runs).

## 6. Risks / open questions

- **Keyword lists are first-pass** and will be calibrated by the Kaggle triage →
  `classifier_audit --strict` → adjudication loop (as ddi_risk was).
- `monitoring_burden` is a **process** dimension, not a clinical outcome; evidence may be
  sparse → expect triage to matter more than usual. Alternative if it proves noisy: fold into a
  `note` field.
- Warfarin's mode of action is not FXa/thrombin — `anticoagulation_efficacy` keywords are
  outcome-based (stroke/VTE), so it applies cleanly; L1 stays `targets: []`.
- **L1/L4 nulls remain** (apixaban/warfarin/enoxaparin potency; dabigatran MB HR; apixaban
  stroke HR; warfarin F) — unaffected by Phase 2.

## 7. Acceptance criteria

1. Template entry present; `build_l3_queries` returns the anticoagulant probes.
2. Scorer block present; all 7 dims scored by `_score_risk`; `py_compile` clean.
3. Unit tests pass (listed in §5).
4. `DIM_DIRECTION` covers all 7 dims.
5. Salt mask adds `etexilate`/`tosilate`.
6. Commit + QMS verification + trace.
