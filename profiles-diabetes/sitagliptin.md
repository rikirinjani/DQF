# Sitagliptin — 4-Level Quantitative Profile

> **Role in PoC:** DPP-4 inhibitor; increases endogenous GLP-1 and GIP half-life. Class: Diabetes.
> **Label note:** First DPP-4i; renal dose adjustment needed; TECOS CV safety; weight-neutral

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **DPP-4** | 8.5 -log10 Ki |

**Selectivity:** DPP-4 > DPP-8/9 (>2,600-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 87% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 1.5 L/kg |
| **Metabolism** | Minimal hepatic (<20%) |
| **Renal excretion** | 85% |
| **Special** | First DPP-4i; renal dose adjustment needed; TECOS CV safety; weight-neutral |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 21 PMIDs (relevance 42.1%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.6 % at 100mg |

### Indications

- T2DM

| Success rate (monotherapy) | 0.52 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 18182122 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19204138 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20412573 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22055835 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24248503 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24450610 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25420579 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25500876 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26089904 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26631880 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27019059 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29511780 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+9 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Sitagliptin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

