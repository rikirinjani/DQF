# Insulin Degludec — 4-Level Quantitative Profile

> **Role in PoC:** Ultra-long basal insulin analog; multihexamer depot formation after SC injection; slow monomer release. Class: Diabetes.
> **Label note:** Ultra-long t½ (~25h); flat PK profile; duration >42h; flexible dosing (8-40h window); lower hypoglycemia vs glargine

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **insulin receptor** | 8.0 -log10 Ki |

**Selectivity:** IR > IGF-1R

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 70% |
| **Half-life** | 25.0 h |
| **Volume of distribution** | 0.5 L/kg |
| **Metabolism** | Proteolytic degradation → inactive metabolites |
| **Renal excretion** | 5% |
| **Special** | Ultra-long t½ (~25h); flat PK profile; duration >42h; flexible dosing (8-40h window); lower hypoglycemia vs glargine |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 38 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 38 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 38 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 38 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 38 PMIDs, relevance gate pass) |
| **renal_benefit** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 38 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 38 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on cv_outcome_benefit, renal_benefit, ddi_risk. Evidence pool: 38 PMIDs (relevance 80.7%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.2 % at 0.2-0.5 U/kg basal |

### Indications

- T1DM
- T2DM (basal)

| Success rate (monotherapy) | 0.63 |
| Onset | hours |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 22577639 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24134602 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24277680 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25179915 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25330628 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25451191 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25538879 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26490811 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29471700 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29770552 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30552800 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32746676 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+26 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Insulin Degludec

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

