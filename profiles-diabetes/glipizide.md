# Glipizide — 4-Level Quantitative Profile

> **Role in PoC:** SU receptor (SUR1) on beta-cell K_ATP channel; stimulates insulin secretion. Class: Diabetes.
> **Label note:** Short t½; meal-time dosing; hypoglycemia risk (dose-dependent); weight gain 2-3kg

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SUR1** | 7.2 -log10 Ki |

**Selectivity:** SUR1 > SUR2

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 95% |
| **Half-life** | 3.5 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic CYP2C9 (hydroxylation → inactive metabolites) |
| **Renal excretion** | 80% |
| **Special** | Short t½; meal-time dosing; hypoglycemia risk (dose-dependent); weight gain 2-3kg |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | batch4_rescore: held (value confirmed, no change proposed) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 28 PMIDs (relevance 60.6%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.2 % at 5-20mg |

### Indications

- T2DM

| Success rate (monotherapy) | 0.56 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10323267 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15871634 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15979893 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16596036 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17352516 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19799532 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2117388 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21477878 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21923736 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25466239 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26941817 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34721294 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+16 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Glipizide

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

