# Alogliptin — 4-Level Quantitative Profile

> **Role in PoC:** DPP-4 inhibitor. Class: Diabetes.
> **Label note:** Longest t½ among gliptins; renal dose adjustment; EXAMINE CV safety

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **DPP-4** | 8.8 -log10 Ki |

**Selectivity:** DPP-4 > DPP-8/9 (>10,000-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 70% |
| **Half-life** | 21.0 h |
| **Volume of distribution** | 0.8 L/kg |
| **Metabolism** | Minimal hepatic (<10%) |
| **Renal excretion** | 75% |
| **Special** | Longest t½ among gliptins; renal dose adjustment; EXAMINE CV safety |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 2 | benefit | batch4_rescore: held (value confirmed, no change proposed) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted; batch4_rescore proposed 3 (not applied) |

**L3 Signature:** top score (3) on a1c_reduction, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 29 PMIDs (relevance 81.5%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.6 % at 25mg |

### Indications

- T2DM

| Success rate (monotherapy) | 0.5 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 18405788 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18405789 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19758359 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20590741 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21595274 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22029001 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22149369 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23452780 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24373234 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24421482 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24532820 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25074280 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+17 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Alogliptin

1. **Unapplied adjudication proposal:** alogliptin|weight_effect: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

