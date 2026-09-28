# Saxagliptin — 4-Level Quantitative Profile

> **Role in PoC:** DPP-4 inhibitor. Class: Diabetes.
> **Label note:** Active metabolite (half potency, same t½); SAVOR-TIMI 53 HF hospitalization signal; renal dose adjustment

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **DPP-4** | 8.0 -log10 Ki |

**Selectivity:** DPP-4 > DPP-8/9 (>10-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 67% |
| **Half-life** | 2.5 h |
| **Volume of distribution** | 0.5 L/kg |
| **Metabolism** | Hepatic CYP3A4/CYP3A5 → active metabolite (5-hydroxy saxagliptin) |
| **Renal excretion** | 75% |
| **Special** | Active metabolite (half potency, same t½); SAVOR-TIMI 53 HF hospitalization signal; renal dose adjustment |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 3 of 4 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; highest risk (3) on ddi_risk. Evidence pool: 31 PMIDs (relevance 79.5%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.6 % at 2.5-5mg |

### Indications

- T2DM

| Success rate (monotherapy) | 0.5 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 18355324 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19650754 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19743938 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19791828 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20518802 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20590741 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21651615 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22029001 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22098472 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22149369 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22668067 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23137182 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+19 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Saxagliptin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

