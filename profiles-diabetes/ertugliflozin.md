# Ertugliflozin — 4-Level Quantitative Profile

> **Role in PoC:** SGLT2 inhibitor. Class: Diabetes.
> **Label note:** High SGLT2 selectivity; VERTIS CV trial; no significant SGLT1 activity

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SGLT2** | 8.2 -log10 Ki |

**Selectivity:** SGLT2 > SGLT1 (>2,000-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 70% |
| **Half-life** | 16.0 h |
| **Volume of distribution** | 0.9 L/kg |
| **Metabolism** | Hepatic O-glucuronidation (UGT1A9, UGT2B7) |
| **Renal excretion** | 50% |
| **Special** | High SGLT2 selectivity; VERTIS CV trial; no significant SGLT1 activity |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 31 PMIDs (relevance 77.8%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.7 % at 5-15mg |

### Indications

- T2DM

| Success rate (monotherapy) | 0.55 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 29042751 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29476348 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30223693 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30427588 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30724637 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31219248 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31797522 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32202075 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32337660 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32372382 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32966714 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34223210 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+19 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Ertugliflozin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

