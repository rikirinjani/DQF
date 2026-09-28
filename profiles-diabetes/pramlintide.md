# Pramlintide — 4-Level Quantitative Profile

> **Role in PoC:** Synthetic amylin analog; slows gastric emptying + suppresses glucagon. Class: Diabetes.
> **Label note:** Only non-GLP-1 injectable; requires TID dosing; nausea common; weight loss; adjunct to mealtime insulin

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **amylin receptor** | 7.0 -log10 Ki |

**Selectivity:** AmylinR (calcitonin receptor + RAMP)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 40% |
| **Half-life** | 0.5 h |
| **Volume of distribution** | 0.1 L/kg |
| **Metabolism** | Renal proteolysis |
| **Renal excretion** | 40% |
| **Special** | Only non-GLP-1 injectable; requires TID dosing; nausea common; weight loss; adjunct to mealtime insulin |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | batch4_rescore: held (value confirmed, no change proposed) |
| **renal_benefit** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on a1c_reduction, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 23 PMIDs (relevance 57.1%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.5 % at 30-120mcg SC before meals |

### Indications

- T1DM (adjunct to insulin)
- T2DM (adjunct to insulin)

| Success rate (monotherapy) | 0.4 |
| Onset | hours |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11220287 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14617226 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15090634 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15891954 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16278328 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16492555 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16504599 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17109659 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17128544 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17463219 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19244569 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20518811 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+11 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Pramlintide

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

