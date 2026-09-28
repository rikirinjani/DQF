# Liraglutide — 4-Level Quantitative Profile

> **Role in PoC:** GLP-1 receptor agonist (97% sequence homology to human GLP-1). Class: Diabetes. L3 values updated by the N1 batch-5 rescore (2026-09-28).
> **Label note:** Once-daily SC; LEADER trial CV benefit; 4.3% weight loss; also approved for obesity

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **GLP-1 receptor** | 8.5 -log10 Ki |

**Selectivity:** GLP-1R selective

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 55% |
| **Half-life** | 13.0 h |
| **Volume of distribution** | 0.05 L/kg |
| **Metabolism** | Proteolytic degradation (DPP-4 resistant via fatty acid) |
| **Renal excretion** | 5% |
| **Special** | Once-daily SC; LEADER trial CV benefit; 4.3% weight loss; also approved for obesity |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | N1 batch-5 rescore 2026-09-28 (applied 2→3): mean hba1c and weight reductions were 12.3 mmol/mol (1.13%; p<0.001) and 3.8 kg (PMID 29527308); strong:3 |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 28 PMIDs (relevance 52.6%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.2 % at 1.2-1.8mg SC |

### Indications

- T2DM
- CV risk reduction (LEADER)
- Obesity (3.0mg SC)

| Success rate (monotherapy) | 0.65 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 24535553 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26279440 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26662611 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27193270 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28124822 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29471700 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29527308 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29637460 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30072400 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31055780 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34032121 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35076486 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+16 more PMIDs in the evidence pool)* | |
| batch5_rescore_adjudication.json | N1-applied L3 cells (2026-09-28) |

---

## Framework Takeaways for Liraglutide

1. **N1 rescore (2→3 on weight_effect):** mean hba1c and weight reductions were 12.3 mmol/mol (1.13%; p<0.001) and 3.8 kg (PMID 29527308); strong:3

