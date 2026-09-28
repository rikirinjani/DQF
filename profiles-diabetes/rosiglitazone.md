# Rosiglitazone — 4-Level Quantitative Profile

> **Role in PoC:** PPARgamma agonist (high potency). Class: Diabetes.
> **Label note:** RECORD trial; controversially associated with MI risk; restricted access in many markets; withdrawn in EU

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **PPARgamma** | 8.2 -log10 Ki |

**Selectivity:** PPARgamma-selective

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 99% |
| **Half-life** | 4.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic CYP2C8 (N-demethylation + hydroxylation) |
| **Renal excretion** | 25% |
| **Special** | RECORD trial; controversially associated with MI risk; restricted access in many markets; withdrawn in EU |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 33 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 2 | benefit | batch4_rescore: held (value confirmed, no change proposed) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 33 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 1 | risk | batch4_rescore: 1 (applied) |
| **renal_benefit** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 33 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on a1c_reduction, gi_tolerability; bottom score (1) on hypoglycemia_risk. Evidence pool: 33 PMIDs (relevance 69.6%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.8 % at 4-8mg |

### Indications

- T2DM

| Success rate (monotherapy) | 0.55 |
| Onset | weeks |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10400405 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10859151 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10954962 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11213884 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11336599 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11417440 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12803733 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14532954 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16033298 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17100408 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17145742 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17517854 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+21 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Rosiglitazone

1. **Unapplied adjudication proposal:** rosiglitazone|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

