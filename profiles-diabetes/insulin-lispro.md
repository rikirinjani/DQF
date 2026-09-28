# Insulin Lispro — 4-Level Quantitative Profile

> **Role in PoC:** Rapid-acting insulin analog; LysB28ProB29 → reduced dimerization. Class: Diabetes.
> **Label note:** First rapid-acting analog (1996); onset 5-15min; duration 4-6h; mealtime flexibility

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **insulin receptor** | 8.5 -log10 Ki |

**Selectivity:** IR > IGF-1R

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 80% |
| **Half-life** | 1.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Proteolytic degradation |
| **Renal excretion** | 30% |
| **Special** | First rapid-acting analog (1996); onset 5-15min; duration 4-6h; mealtime flexibility |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 37 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 37 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 37 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 37 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 37 PMIDs, relevance gate pass) |
| **renal_benefit** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 37 PMIDs, relevance gate pass) |
| **weight_effect** | 1 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 37 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on weight_effect, cv_outcome_benefit, renal_benefit, ddi_risk. Evidence pool: 37 PMIDs (relevance 75.0%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.3 % at 0.5-1.0 U/kg prandial |

### Indications

- T1DM
- T2DM (prandial)

| Success rate (monotherapy) | 0.62 |
| Onset | hours |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10067027 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10192689 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10524089 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15377436 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17593235 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18991400 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24325997 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25612348 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27202668 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29471700 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33151101 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38223574 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+25 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Insulin Lispro

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

