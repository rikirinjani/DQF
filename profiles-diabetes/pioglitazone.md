# Pioglitazone — 4-Level Quantitative Profile

> **Role in PoC:** PPARgamma agonist; increases insulin sensitivity in adipose, muscle, liver. Class: Diabetes.
> **Label note:** PROactive trial CV benefit?; weight gain (2-4kg); edema; bladder cancer concern; no renal dose adjustment

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **PPARgamma** | 7.5 -log10 Ki |

**Selectivity:** PPARgamma > PPARalpha (weak partial agonist)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 83% |
| **Half-life** | 8.0 h |
| **Volume of distribution** | 0.3 L/kg |
| **Metabolism** | Hepatic CYP2C8, CYP3A4 (active metabolites) |
| **Renal excretion** | 20% |
| **Special** | PROactive trial CV benefit?; weight gain (2-4kg); edema; bladder cancer concern; no renal dose adjustment |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 1 of 2 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability. Evidence pool: 23 PMIDs (relevance 43.9%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.9 % at 15-45mg |

### Indications

- T2DM
- Stroke risk reduction (IRIS)

| Success rate (monotherapy) | 0.58 |
| Onset | weeks |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11594240 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11594241 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11900311 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16466323 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16506273 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18220664 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20175701 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25157285 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32978507 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38558280 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38684131 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38699792 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+11 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Pioglitazone

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

