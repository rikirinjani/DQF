# Insulin Glargine — 4-Level Quantitative Profile

> **Role in PoC:** Long-acting basal insulin analog; forms microprecipitate at injection site for sustained release. Class: Diabetes. L3 values updated by the N1 batch-5 rescore (2026-09-28).
> **Label note:** Flat PK profile with no pronounced peak; once-daily basal coverage

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **insulin receptor** | 9.0 -log10 Ki |

**Selectivity:** IR >> IGF-1R

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | SC only% |
| **Half-life** | 24.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Proteolysis (metabolites M1 and M2 retain some activity) |
| **Renal excretion** | 0% |
| **Special** | Flat PK profile with no pronounced peak; once-daily basal coverage |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 1 | benefit | N1 batch-5 rescore 2026-09-28 (applied 2→1): DEVOTE trial - cardiovascular outcomes by treatment group (PMID 38344820): CV safety demonstrated, no CV benefit; kw=1 confirms direction |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **renal_benefit** | 1 | benefit | N1 batch-5 rescore 2026-09-28 (applied 2→1): safety analysis of insulin glargine u300 in 21,359 patients (PMID 39972199): no renal benefit demonstrated; kw=1 confirms direction |
| **weight_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on cv_outcome_benefit, renal_benefit, ddi_risk. Evidence pool: 32 PMIDs (relevance 71.9%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.2 % at 0.2-0.6 U/kg |

### Indications

- T1DM
- T2DM (advanced)

| Success rate (monotherapy) | 0.65 |
| Onset | hours |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | safe |
| **Lactation** | safe |
| **Pregnancy** | B |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11130552 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11553198 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12828834 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15336483 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17279454 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18199142 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18577151 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18585815 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23132625 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26840338 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29471700 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29872460 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+20 more PMIDs in the evidence pool)* | |
| batch5_rescore_adjudication.json | N1-applied L3 cells (2026-09-28) |

---

## Framework Takeaways for Insulin Glargine

1. **N1 rescore (2→1 on cv_outcome_benefit):** DEVOTE trial - cardiovascular outcomes by treatment group (PMID 38344820): CV safety demonstrated, no CV benefit; kw=1 confirms direction
2. **N1 rescore (2→1 on renal_benefit):** safety analysis of insulin glargine u300 in 21,359 patients (PMID 39972199): no renal benefit demonstrated; kw=1 confirms direction

