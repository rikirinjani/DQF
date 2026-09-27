# Edoxaban — 4-Level Quantitative Profile

> **Role in PoC:** Oral direct factor Xa inhibitor, once-daily, with the largest volume of distribution and lowest protein binding among the sourced DOACs. The only drug in the set whose record carries a partial reversal agent only, giving the class-unique `reversal_availability` = 2.

---

## L1 — Molecular Binding

### Primary Target: Factor Xa

| Target | Potency | Functional Effect |
|--------|---------|-------------------|
| **Factor Xa (FXa)** | Ki 0.561 nmol/L, recorded as 9.25 (-log10 Ki) | Oral direct FXa inhibition (PMID 25966665; PMID 18624979) |

### Selectivity

| Feature | Finding | Source |
|---------|---------|--------|
| **FXa selectivity** | >10,000-fold selectivity for FXa | PMID 18624979 |

Edoxaban's Ki (0.561 nmol/L, PMID 18624979) sits close to rivaroxaban's (0.4 nmol/L) against the same target; both are an order of magnitude tighter than dabigatran's thrombin Ki, which is a different protein and not directly comparable.

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 62% absolute (label); 67.2% relative (PMID 25186833) |
| **Half-life** | 10-14 h (label); 12 h recorded in drugs.json |
| **Volume of distribution** | 107 L, SD 19.9 (PMID 26620048; label) |
| **Protein binding** | 55% (label) |
| **Metabolism** | P-gp substrate; minimal CYP metabolism (label) |
| **Renal excretion** | ~50% of total clearance (PMID 26620048; 24861792) |

**PK Signature:** Edoxaban has the largest Vd (107 L) and lowest protein binding (55%) of the sourced DOACs, and its elimination splits roughly evenly between renal and non-renal routes (~50%, PMID 24861792). Metabolism is P-gp-mediated with minimal CYP contribution (label), which is the mechanistic background for its moderate `ddi_risk` = 2. Peak pharmacodynamic effect occurs within 1-2 h (label, 12 Pharmacodynamics).

---

## L3 — Systems Response

Scale: each dimension is scored 1-3; higher = more of the named quantity. `anticoagulation_efficacy` and `reversal_availability` are benefit dimensions (higher is better); the other five are risk dimensions (higher is worse). Scores are the adjudicated cells of 2026-09-27 (`rag-queries/curation/anticoagulant_adjudication.json`), already merged into `api/drugs.json`; basis text is from the adjudication record.

| Dimension | Score | Direction | Basis (adjudication) |
|-----------|-------|-----------|----------------------|
| **anticoagulation_efficacy** | 3 | benefit | R1a: auto 3 supported by 4 audit-clean strong |
| **bleeding_risk** | 3 | risk | R1a: auto 3 supported by 7 audit-clean strong |
| **renal_clearance_dependence** | 3 | risk | Override: renal excretion 50%; dose reduction to 30 mg if CrCl 15-50 (label) |
| **ddi_risk** | 2 | risk | R7: filtered re-score on 2 pk/pd sentences |
| **monitoring_burden** | 1 | risk | Override: SAVAYSA label, 12.2 Pharmacodynamics: PT/INR/aPTT changes "are small, subject to a high degree of variability and not useful in monitoring the anticoagulant effect of edoxaban" |
| **reversal_availability** | 2 | benefit | Override: reversal agent recorded as "andexanet alfa (partial)" (PMID 29345686) |
| **gi_bleeding_risk** | 2 | risk | R1c: keep 2 on 1 clean strong, 0 flagged |

**L3 Signature:** Edoxaban is the only non-3 reversal score in the class: the record qualifies andexanet as partial (PMID 29345686), so 1 (no agent) would understate it and 3 (full antidote) would overstate it (adjudication `why_pool_differs`). DDI risk landed at 2 after the filtered re-score on pk/pd sentences, consistent with P-gp-only labeling and minimal CYP metabolism (label).

---

## L4 — Clinical Outcomes

### ENGAGE AF-TIMI 48 vs Warfarin

| Outcome | Result | Source |
|---------|--------|--------|
| **Stroke/SE** | Favorable trend, HR 0.87; superior net clinical outcome | PMID 38828563 |
| **Major bleeding** | HR 0.80 | label (ENGAGE AF-TIMI 48) |
| **Clinically relevant non-major bleeding** | HR 0.81 | label |
| **ICH** | null (not sourced) | drugs.json |

### Dosing

| Item | Value | Source |
|------|-------|--------|
| **Dose reduction** | 30 mg once daily if CrCl 15-50 mL/min, or weight 60 kg or less, or concomitant P-gp inhibitor | label |
| **Onset** | 120 min (drugs.json); peak pharmacodynamic effect within 1-2 h (label, 12 Pharmacodynamics) | drugs.json; label |

### Reversal

| Agent | Effect | Source |
|-------|--------|--------|
| **Andexanet alfa** | Partial reversal | PMID 29345686 |

### Indications

- Stroke prevention in non-valvular AF
- VTE treatment

(drugs.json; label)

### Special-Population Safety

| Population | Rating | Source |
|------------|--------|--------|
| **Pregnancy** | Insufficient data | label |
| **Lactation** | Unknown | label |
| **Hepatic** | Moderate/severe impairment: not recommended | label |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 18624979 | FXa Ki 0.561 nmol/L; >10,000-fold selectivity |
| PMID 25186833 | Relative bioavailability 67.2% |
| PMID 26620048 | Vd 107 L (SD 19.9); renal clearance ~50% |
| PMID 24861792 | Renal excretion cross-class estimate |
| PMID 25966665 | Direct FXa inhibitor mechanism |
| PMID 29345686 | Andexanet alfa (partial) |
| PMID 38828563 | ENGAGE AF-TIMI 48: HR 0.87 trend, superior net clinical outcome |
| label (DailyMed setid e77d3400-56ad-11e3-949a-0800200c9a66) | F 62%; t½ 10-14 h; protein binding 55%; bleeding HRs; dose-reduction criteria; monitoring not useful; pregnancy/lactation/hepatic |
| label_sourcing_e1.json | Verbatim SAVAYSA monitoring quote |
| anticoagulant_adjudication.json | All seven L3 cells |

## Framework Takeaways for Edoxaban

1. **Partial reversal is a distinct state:** neither "no antidote" (1) nor "full antidote" (3); the adjudication created the 2 from the record's own qualification ("partial", PMID 29345686).
2. **Widest labeled dose-reduction trigger set:** CrCl band, weight threshold, and P-gp inhibitor coadministration each independently halve the dose (label), more criteria than any other DOAC in this set.
3. **Transporter-only interaction profile:** minimal CYP metabolism (label) matches the R7-filtered `ddi_risk` = 2, against 3 for the CYP3A4-dependent apixaban and rivaroxaban.
4. **PK extremes without outcome extremes:** the largest Vd (107 L) and lowest protein binding (55%) produce no corresponding L4 outlier; distribution alone does not differentiate outcomes here.
