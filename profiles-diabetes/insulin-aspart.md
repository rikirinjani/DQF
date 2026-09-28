# Insulin Aspart — 4-Level Quantitative Profile

> **Role in PoC:** Rapid-acting insulin analog; AspB28 substitution reduces hexamer formation → faster absorption. Class: Diabetes.
> **Label note:** Onset 5-15min; duration 3-5h; faster than regular insulin; also available as faster aspart

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
| **Metabolism** | Proteolytic degradation in liver, kidney, muscle |
| **Renal excretion** | 30% |
| **Special** | Onset 5-15min; duration 3-5h; faster than regular insulin; also available as faster aspart |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 40 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 40 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 40 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 40 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 40 PMIDs, relevance gate pass) |
| **renal_benefit** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 40 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 40 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, gi_tolerability; bottom score (1) on cv_outcome_benefit, renal_benefit, ddi_risk. Evidence pool: 40 PMIDs (relevance 75.0%, gate pass).

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
| PMID 11606897 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11679481 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12387040 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15135305 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16957759 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25180608 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25846340 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28597216 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29471700 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30547388 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31069935 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31999478 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+28 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Insulin Aspart

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

