# Warfarin — 4-Level Quantitative Profile

> **Role in PoC:** Reference comparator for the anticoagulant class. Every DOAC outcome field in this PoC is expressed against warfarin. Vitamin K antagonist with genotype-dependent dosing, mandatory INR monitoring, hepatic elimination, and full reversal available. The only drug in this set carrying a mechanical-heart-valve indication.

---

## L1 — Molecular Binding

### Primary Target: Vitamin K Epoxide Reductase (VKOR/VKORC1)

| Target | Potency | Functional Effect |
|--------|---------|-------------------|
| **VKOR (VKORC1)** | not sourced (no Ki in the label or the curated pool) | Blocks vitamin K recycling, reducing synthesis of active factors II, VII, IX, and X (label) |

Warfarin carries **no small-molecule potency value**: `l1_binding.targets` is empty and the values draft lists warfarin L1 potency under "Still null". The anticoagulant effect is indirect and delayed: inhibiting VKOR depletes active clotting factors, so the pharmacodynamic effect lags plasma concentration. L1 alone cannot predict warfarin's clinical behavior.

### Genotype Dependence (carried into L2 and L4)

| Feature | Effect | Source |
|---------|--------|--------|
| **CYP2C9** | Oxidizes the more potent S-enantiomer; poor metabolizers need lower doses | PMID 9014207 |
| **VKORC1** | Polymorphism changes the dose requirement | label; PMID 9014207 |
| **Net effect** | CYP2C9/VKORC1 genotype-dependent dose variability | label; PMID 9014207 |

Warfarin is the only drug in this class whose dose is titrated to a laboratory endpoint (INR) rather than fixed, and the only one with pharmacogenomic dosing.

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | null (not sourced; not stated in the label) |
| **Half-life (single-dose reference)** | ~35 h (PMID 3542339) |
| **Effective half-life** | 20-60 h (label) |
| **Volume of distribution** | 0.14 L/kg, ~10 L per 70 kg (PMID 3542339; label) |
| **Protein binding** | 99%, albumin (label) |
| **Metabolism** | S-warfarin: CYP2C9; R-warfarin: CYP1A2/CYP3A4 (PMID 9014207) |
| **Plasma clearance** | 0.2 L/h per 70 kg (PMID 3542339) |
| **Renal excretion** | null for parent (not sourced); up to 92% of dose recovered in urine as metabolites (label) |

**PK Signature:** Small Vd (~10 L, close to albumin space), 99% protein binding, and a long effective half-life (20-60 h, label). Elimination is hepatic oxidation by CYP2C9, CYP1A2, and CYP3A4 (PMID 9014207). The label's 92% urinary recovery figure refers to metabolites, not renal clearance of parent drug; that distinction is the basis of the adjudicated `renal_clearance_dependence` = 1.

---

## L3 — Systems Response

Scale: each dimension is scored 1-3; higher = more of the named quantity. `anticoagulation_efficacy` and `reversal_availability` are benefit dimensions (higher is better); the other five are risk dimensions (higher is worse). Scores are the adjudicated cells of 2026-09-27 (`rag-queries/curation/anticoagulant_adjudication.json`), already merged into `api/drugs.json`; basis text is from the adjudication record.

| Dimension | Score | Direction | Basis (adjudication) |
|-----------|-------|-----------|----------------------|
| **anticoagulation_efficacy** | 3 | benefit | R1a: auto 3 supported by 5 audit-clean strong |
| **bleeding_risk** | 3 | risk | R1a: auto 3 supported by 2 audit-clean strong |
| **renal_clearance_dependence** | 1 | risk | Override: hepatic metabolism CYP2C9/CYP1A2/CYP3A4 (PMID 9014207); INR-titrated, no fixed dose and no renal dose adjustment (label); urinary 92% is metabolites (label) |
| **ddi_risk** | 2 | risk | R7: filtered re-score on 4 pk/pd sentences |
| **monitoring_burden** | 3 | risk | R1a: auto 3 supported by 3 audit-clean strong |
| **reversal_availability** | 3 | benefit | R1a: auto 3 supported by 2 audit-clean strong |
| **gi_bleeding_risk** | 3 | risk | R1a: auto 3 supported by 2 audit-clean strong |

**L3 Signature:** Warfarin defines the top of the monitoring scale and the bottom of the renal-dependence scale. The renal score of 1 is the largest adjudication correction in the class: the auto-score of 3 was a keyword false positive (CrCl/creatinine/dialysis terms matched cohort-exclusion text), and the single clean strong sentence was one 1996 CrCl/half-life correlation contradicted by an explicit negative in ESKD (adjudication record, `why_pool_differs`). DDI risk is real but scored 2 after filtering to pharmacokinetic/pharmacodynamic interaction sentences (R7).

---

## L4 — Clinical Outcomes

### Comparator Role

| Outcome field | Value | Source |
|---------------|-------|--------|
| **stroke_se_reduction_vs_warfarin** | reference comparator | drugs.json |
| **major_bleeding_hr_vs_warfarin** | reference comparator | drugs.json |
| **ich_reduction** | reference comparator | drugs.json |

Warfarin is the shared control arm of the DOAC evidence base: ARISTOTLE (apixaban, PMID 21870978), ROCKET AF (rivaroxaban, label), ENGAGE AF-TIMI 48 (edoxaban, PMID 38828563), and RE-LY (dabigatran, PMID 22435606) are all expressed as effects vs warfarin.

### Dosing and Monitoring

| Item | Value | Source |
|------|-------|--------|
| **Dose** | INR-titrated, target 2-3; no fixed dose | label |
| **Time in therapeutic range** | 44% in RENAL-AF | PMID 37952132 |
| **Onset** | null (not sourced) | drugs.json |

### Reversal

| Agent | Effect | Source |
|-------|--------|--------|
| **Vitamin K + prothrombin complex concentrate** | Reverses anticoagulation | label |

### Indications

- Stroke prevention in AF
- VTE treatment/prophylaxis
- Mechanical heart valves

(drugs.json; label)

### Special-Population Safety

| Population | Rating | Source |
|------------|--------|--------|
| **Pregnancy** | Contraindicated, except mechanical heart valves | label |
| **Lactation** | Compatible | label |
| **Hepatic** | Caution; effect may be increased | label |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 9014207 | CYP2C9/CYP1A2/CYP3A4 metabolism; genotype-dependent dosing |
| PMID 3542339 | t½ ~35 h; Vd 0.14 L/kg; clearance 0.2 L/h per 70 kg |
| PMID 37952132 | TTR 44% in RENAL-AF |
| label (DailyMed setid 654ca5d2-d4c1-48f8-90c4-130a21162bb0) | INR 2-3 target; 99% protein binding; metabolite recovery in urine; reversal agents; pregnancy/lactation/hepatic |
| anticoagulant_adjudication.json | All seven L3 cells |

## Framework Takeaways for Warfarin

1. **Metabolites are not renal clearance:** the label's "92% recovered in urine" describes metabolites of a hepatically cleared drug. Reading it as renal elimination would flip `renal_clearance_dependence` from 1 to 3; the adjudication override documents the distinction.
2. **Monitoring burden is a process dimension:** warfarin scores 3 on `monitoring_burden` while matching the DOACs on efficacy and bleeding. The dimension captures INR logistics, not clinical outcomes.
3. **The comparator cannot compare itself:** warfarin's vs-warfarin L4 fields read "reference comparator", so its profile is completed by the other five drugs' HRs.
4. **Genotype chain:** L1/L2 (CYP2C9, VKORC1) → dose variability → INR titration (L4). No other class member has a pharmacogenomic dosing chain.
