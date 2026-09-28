# Repaglinide — 4-Level Quantitative Profile

> **Role in PoC:** Meglitinide; closes beta-cell K_ATP channel at different binding site than SU; rapid insulin secretion. Class: Diabetes.
> **Label note:** Ultra-short t½ (1h); mealtime dosing (prandial glucose regulator); gemfibrozil interaction (CYP2C8)

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SUR1** | 7.5 -log10 Ki |

**Selectivity:** SUR1-selective

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 56% |
| **Half-life** | 1.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic CYP2C8, CYP3A4 (glucuronidation) |
| **Renal excretion** | 10% |
| **Special** | Ultra-short t½ (1h); mealtime dosing (prandial glucose regulator); gemfibrozil interaction (CYP2C8) |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 2 of 3 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **renal_benefit** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, gi_tolerability; highest risk (3) on hypoglycemia_risk. Evidence pool: 32 PMIDs (relevance 69.9%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.9 % at 0.5-4mg before meals |

### Indications

- T2DM
- Renal impairment (safe)

| Success rate (monotherapy) | 0.52 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10363735 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10522841 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10631622 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11112092 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11157993 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11190420 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11220287 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11728565 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12083976 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12365816 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12475777 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12623163 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+20 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Repaglinide

1. **Unapplied adjudication proposal:** repaglinide|renal_benefit: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

