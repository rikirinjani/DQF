# V1c — PPI L3 Risk-Score Concordance (ACG Guideline Validation)

**Date:** 2026-07-30  
**Validator:** L3 pipeline (risk extraction) vs ACG CDI guideline + clinical pharmacology literature  
**Class:** PPIs — safety/risk dimensions  
**Predecessor:** V1-ppi-guideline-concordance.md (validated efficacy/overall scores)

---

## Overview

This report validates the **L3-derived risk scores** (extracted via PubMed/EUtils pipeline) against published ACG guideline data and clinical pharmacology references. The L3 pipeline extracted 7 risk dimensions for each PPI; only 2 had non-null values across all 5 drugs.

---

## L3 Risk Scores (from `l3_systems`)

| Drug | DDI Risk (1–3) | CDI Risk (1–3) | Healing Ability | CYP2C19 Metab% | Bone Fracture | Acid Rebound |
|------|:--------------:|:--------------:|:---------------:|:--------------:|:-------------:|:------------:|
| Omeprazole | **3** | **3** | null | null | null | null |
| Esomeprazole | **3** | **1** | null | null | null | null |
| Lansoprazole | **3** | **2** | null | null | null | null |
| Pantoprazole | **3** | **1** | null | null | null | null |
| Rabeprazole | **3** | **2** | null | null | null | null |

**Evidence counts:** Omeprazole 23 PMIDs · Lansoprazole 14 · Pantoprazole 13 · Esomeprazole 12 · Rabeprazole 10

---

## Dimension 1: DDI Risk

### DQF Scores (uniform: all 3/3)

All five PPIs receive the maximum DDI risk score.

### Clinical Pharmacology Reference

| Drug | CYP2C19 Inhibition | CYP3A4 Involvement | Non-enzymatic pathway | Clinically significant DDIs | Reference |
|------|:------------------:|:------------------:|:---------------------:|:---------------------------:|:---------:|
| Omeprazole | **Strong** (Ki=2–6 µM) | Minor | No | **Clopidogrel, citalopram, methotrexate, warfarin** | Li 2004, FDA labeling |
| Esomeprazole | **Moderate** (S-isomer, same target) | Minor | No | Clopidogrel (weaker than OME), citalopram | Andersson 2001 |
| Lansoprazole | **Moderate** | Moderate (CYP3A4) | Minor | Theophylline, tacrolimus | Pearce 1996 |
| Pantoprazole | **Weak** (Ki=14–69 µM) | Minor | Yes (sulfotransferase) | **Minimal** — preferred in polypharmacy | Meyer 1996, Steinijans 1996 |
| Rabeprazole | **Weak** | None | Yes (thioether reduction) | **Minimal** — CYP2C19/3A4 independent | Humphries 1996 |

*Sources: FDA prescribing information, Li et al. 2004 (Drug Metab Dispos), Andersson 2001 (Aliment Pharmacol Ther), Steinijans 1996 (Int J Clin Pharmacol Ther).*

### Assessment

| Scoring | Verdict |
|---------|---------|
| **Between-class differentiation** | ❌ **ALL FIVE scored 3** — fails to separate severe (omeprazole), moderate (esomeprazole, lansoprazole), and minimal (pantoprazole, rabeprazole) DDI profiles |
| **Rank order correlation** | Omeprazole >> Esomeprazole > Lansoprazole >> Pantoprazole ≈ Rabeprazole → DQF gives all equal |
| **Clinical accuracy** | Pantoprazole and rabeprazole are the preferred PPIs in polypharmacy or for patients on clopidogrel — 3/3 penalizes them equally with omeprazole |

**Severity: HIGH.** Uniform DDI scoring is a flat-out guideline-discordant. Every major formulary differentiates PPI DDI profiles (VA, Kaiser, NHS formularies).

---

## Dimension 2: CDI Risk

### DQF Scores

| Drug | DQF CDI Risk | ACG CDI OR (95% CI) | Rank by DQF | Rank by ACG OR |
|------|:------------:|:-------------------:|:-----------:|:--------------:|
| Omeprazole | **3 (highest)** | **3.24** (3.16–3.32) — LOWEST | #1 | #4 |
| Lansoprazole | **2** | **4.81** (4.58–5.06) — HIGHEST | #3 | #1 |
| Esomeprazole | **1** | **4.2** (4.05–4.36) | #4 | #2 |
| Pantoprazole | **1** | **4.15** (4.02–4.29) | #4 | #3 |
| Rabeprazole | **2** | *(no OR in this study)* | #3 | — |

*Source: ACG 2020 abstract (S0232), LWW AJG — national PPI-CDI study in >1 million patients.*

### Assessment

| Scoring | Verdict |
|---------|---------|
| **Rank correlation (DQF vs ACG OR)** | **INVERTED.** Omeprazole has lowest OR (3.24) but DQF scores highest risk (3). Lansoprazole has highest OR (4.81) but DQF scores only 2. Spearman ρ would be **negative** if we had full data. |
| **Possible explanation** | DQF may be scoring omeprazole's general side-effect profile or using a different source. The ACG-level evidence suggests omeprazole has the lowest CDI risk among PPIs. |
| **Esomeprazole/Pantoprazole** | DQF scores both 1 (lowest risk) but ACG shows OR 4.2 and 4.15 — substantial 4-fold increased risk. 1/3 is too low. |
| **Rabeprazole** | Not studied in the large ACG CDI dataset. Score of 2 is unvalidated. |

**Severity: HIGH.** The CDI risk scoring is inverted relative to the best available ACG evidence. This is a systematic error, not a borderline call.

---

## Dimension 3-6: Missing Fields

Four of seven L3 dimensions are **null for all 5 PPIs**:

| Field | DQF Status | Expected (from guidelines) | Root Cause |
|-------|-----------|---------------------------|------------|
| `healing_ability` | null | Esomeprazole > Lansoprazole ≈ Rabeprazole ≈ Omeprazole > Pantoprazole (EE healing rates: 91-94% vs 82-89%) | L3 query templates for PPIs do not target healing rate studies. The MESH/RCT terms in `extract_l3.py` focus on safety signals, not efficacy endpoints. |
| `cyp2c19_metabolism_pct` | null | Omeprazole 60-80% via CYP2C19, Esomeprazole 60-70%, Lansoprazole 40-60%, Pantoprazole 20-30%, Rabeprazole <10% | Pipeline did not extract CYP-specific pharmacogenetic data despite it being a key PPI differentiator (see ASGE 2025, AGA 2022). |
| `bone_fracture_risk` | null | FDA class-label warning (2010). All PPIs associated with ~1.2-1.4x hip fracture risk with long-term use. Meta-analyses show class effect, not drug-specific. | The search template (PPI + "bone fracture" + "risk") likely returned non-specific class-effect studies that don't differentiate within class. Expected to be uniform. |
| `acid_rebound` | null | Well-documented class effect after >8 weeks of use. No meaningful within-class differences for clinical rebound severity. | Not targeted by current L3 queries. |

**Severity: MEDIUM.** The pipeline succeeds at extracting safety-risk signals (DDI, CDI) but fails on efficacy and pharmacogenetic dimensions. The missing fields are not pipeline errors per se — the query templates were designed for toxicity/safety extraction and were not tested on PPI class before deployment.

---

## Summary of Findings

### Concordance by Dimension

| Dimension | Drugs Scored | Non-null Rate | Guideline Concordance | Grade |
|-----------|:-----------:|:-------------:|:---------------------:|:----:|
| DDI Risk | 5/5 | 100% | ❌ **Uniform 3/3 — fails to differentiate** | 🔴 FAIL |
| CDI Risk | 5/5 | 100% | ❌ **Inverted rank vs ACG OR data** | 🔴 FAIL |
| Healing Ability | 0/5 | 0% | N/A (not extracted) | ⚪ Not scored |
| CYP2C19 Metab% | 0/5 | 0% | N/A (not extracted) | ⚪ Not scored |
| Bone Fracture Risk | 0/5 | 0% | N/A (not extracted) | ⚪ Not scored |
| Acid Rebound | 0/5 | 0% | N/A (not extracted) | ⚪ Not scored |

### Root Causes

| Issue | Cause | Affects |
|-------|-------|---------|
| **DDI uniform scoring** | L3 extraction detected DDI signal for all PPIs equally. The scoring rubric (1-3) maps DDI presence, not DDI severity. Risk score should be graded by CYP inhibition potency + number of known interactions. | All PPIs |
| **CDI score inversion** | Likely the pipeline extracted omeprazole's broader side-effect profile and generalized to CDI scoring. The ACG-level data (n > 1M) shows omeprazole has the lowest CDI OR. | Omeprazole (over-scored), Lansoprazole (under-scored) |
| **Missing dimensions** | L3 query templates are optimized for NSAID safety signals (GI bleed, CV risk, renal) and were not calibrated for PPI-specific endpoints (healing, CYP metabolism, rebound). | All PPIs |

---

## Recommendations

### Immediate (V1.1 scoring fix)

1. **Fix CDI risk scoring.** Invert the rank: Lansoprazole → 3, Esomeprazole → 2, Pantoprazole → 2, Omeprazole → 2, Rabeprazole → 2 (unvalidated, default to class median). Source: ACG S0232 data.

2. **Fix DDI risk scoring.** Differentiate by CYP inhibition:
   - Omeprazole → 3 (strong CYP2C19 inhibitor)
   - Esomeprazole → 2 (moderate inhibitor)
   - Lansoprazole → 2 (moderate, also CYP3A4)
   - Pantoprazole → 1 (weak, non-enzymatic escape)
   - Rabeprazole → 1 (CYP-independent)

### Pipeline (L3 query improvement)

3. **Add PPI-specific query templates** targeting:
   - EE healing rates (RCTs: esomeprazole 40mg vs omeprazole 20mg)
   - CYP2C19 genotype impact (PubMed MESH: "Cytochrome P-450 CYP2C19" + "proton pump inhibitors")
   - Bone fracture risk (FDA Adverse Event Reporting System)

4. **Implement within-class scoring calibration** — the current 1-3 risk scale is uniform across classes but needs class-specific anchors (what is "3" for PPIs ≠ what is "3" for NSAIDs).

---

## Appendix: Evidence Sources Used

| Source | Type | Citation |
|--------|------|----------|
| ACG CDI Large Cohort | Abstract (S0232), AJG 2020 | ORs: Lansoprazole 4.81, Esomeprazole 4.2, Pantoprazole 4.15, Omeprazole 3.24 |
| PPI CYP2C19 Inhibition | Original research, Drug Metab Dispos 2004 | Li et al. — Ki values for CYP2C19 inhibition |
| Pantoprazole DDI Safety | Review, Int J Clin Pharmacol Ther 1996 | Steinijans et al. — minimal DDI profile |
| Rabeprazole Metabolism | Review, Aliment Pharmacol Ther 1999 | Humphries et al. — non-enzymatic thioether reduction |
| PPI CDI Meta-analysis | PMC5643276, World J Gastroenterol 2017 | Trifan et al. — systematic review of PPI-CDI association |
| PPI Bone Fracture | FDA Drug Safety Communication 2010 | Class-label update for fracture risk |
| ACG CDI Guideline | Am J Gastroenterol 2021;116:1124-1147 | Kelly CR et al. — prevention, diagnosis, treatment |
