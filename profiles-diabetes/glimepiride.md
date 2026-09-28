# Glimepiride — 4-Level Quantitative Profile

> **Role in PoC:** SU receptor (SUR1) on beta-cell K_ATP channel; insulin secretagogue. Class: Diabetes.
> **Label note:** Once-daily; M1 metabolite has ~1/3 potency; extra-pancreatic effects?; lower hypoglycemia risk than glyburide

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SUR1** | 7.8 -log10 Ki |

**Selectivity:** SUR1 > SUR2A > SUR2B

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 100% |
| **Half-life** | 9.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic CYP2C9 (oxidation → M1 metabolite active) |
| **Renal excretion** | 60% |
| **Special** | Once-daily; M1 metabolite has ~1/3 potency; extra-pancreatic effects?; lower hypoglycemia risk than glyburide |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **renal_benefit** | 2 | benefit | batch4_rescore: held (value confirmed, no change proposed) |
| **weight_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 22 PMIDs (relevance 59.2%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.2 % at 1-8mg |

### Indications

- T2DM

| Success rate (monotherapy) | 0.57 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11190420 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12475777 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12849919 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17728849 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21952951 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23028231 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25722307 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25812374 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27121788 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27829515 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28792171 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30605064 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+10 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Glimepiride

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

