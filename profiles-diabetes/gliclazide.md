# Gliclazide — 4-Level Quantitative Profile

> **Role in PoC:** SU receptor (SUR1) on beta-cell K_ATP channel; insulin secretagogue; antioxidant. Class: Diabetes.
> **Label note:** Modified-release (MR) formulation; ADVANCE trial microvascular benefit; antioxidant properties; preferred SU in some guidelines

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SUR1** | 7.0 -log10 Ki |

**Selectivity:** SUR1 > SUR2 (less vascular binding)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 80% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic CYP2C9 (multiple metabolites) |
| **Renal excretion** | 70% |
| **Special** | Modified-release (MR) formulation; ADVANCE trial microvascular benefit; antioxidant properties; preferred SU in some guidelines |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk. Evidence pool: 31 PMIDs (relevance 80.8%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.1 % at 30-120mg MR |

### Indications

- T2DM

| Success rate (monotherapy) | 0.58 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10656221 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11078471 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12076188 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12475777 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12623163 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12934650 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17415747 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18539916 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19719333 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19799532 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20964454 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21923736 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+19 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Gliclazide

1. **Unapplied adjudication proposal:** gliclazide|cv_outcome_benefit: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.
2. **Unapplied adjudication proposal:** gliclazide|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

