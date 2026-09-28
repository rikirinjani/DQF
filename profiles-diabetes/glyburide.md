# Glyburide — 4-Level Quantitative Profile

> **Role in PoC:** SU receptor (SUR1) on beta-cell K_ATP channel; potent insulin secretagogue. Class: Diabetes.
> **Label note:** Highest hypoglycemia risk among SUs (long t½ + active hepatic metabolites); contraindicated in renal impairment; ADOPT trial fastest monotherapy failure

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SUR1** | 8.0 -log10 Ki |

**Selectivity:** SUR1-selective

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 90% |
| **Half-life** | 10.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic CYP2C9 (hydroxylation → inactive metabolites) |
| **Renal excretion** | 50% |
| **Special** | Highest hypoglycemia risk among SUs (long t½ + active hepatic metabolites); contraindicated in renal impairment; ADOPT trial fastest monotherapy failure |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |
| **renal_benefit** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, gi_tolerability; highest risk (3) on hypoglycemia_risk. Evidence pool: 26 PMIDs (relevance 60.8%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.3 % at 2.5-20mg |

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
| PMID 10496299 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11368292 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12589230 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14617228 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1660613 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17145742 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19791828 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21952951 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24720590 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25828275 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26796130 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30422193 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+14 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Glyburide

1. **Unapplied adjudication proposal:** glyburide|cv_outcome_benefit: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.
2. **Unapplied adjudication proposal:** glyburide|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

