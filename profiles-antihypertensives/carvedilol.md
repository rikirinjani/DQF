# Carvedilol — 4-Level Quantitative Profile

> **Role in PoC:** Non-selective beta + alpha1 antagonist; antioxidant. Class: Antihypertensive.
> **Label note:** Added mortality benefit in HFrEF; vasodilation via alpha1 block; antioxidant properties

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **beta1-adrenergic receptor** | 8.5 -log10 Ki |
| **beta2-adrenergic receptor** | 8.0 -log10 Ki |
| **alpha1-adrenergic receptor** | 7.5 -log10 Ki |

**Selectivity:** Non-selective

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 25% |
| **Half-life** | 7.0 h |
| **Volume of distribution** | 1.5 L/kg |
| **Metabolism** | Hepatic CYP2D6/CYP2C9 (glucuronidation) |
| **Renal excretion** | 15% |
| **Special** | Added mortality benefit in HFrEF; vasodilation via alpha1 block; antioxidant properties |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 3 of 6 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction; highest risk (3) on ddi_risk; bottom score (1) on electrolyte_risk; heart-rate effect: bradycardia. Evidence pool: 27 PMIDs (relevance 52.2%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-7) at 12.5-50mg |

### Indications

- Hypertension
- Heart failure
- Post-MI with LV dysfunction

| Success rate (monotherapy) | 0.5 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10169635 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11214769 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15075055 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16379664 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17023229 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22048841 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24863629 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27137712 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28469221 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37272562 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38850570 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38852609 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+15 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Carvedilol

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

