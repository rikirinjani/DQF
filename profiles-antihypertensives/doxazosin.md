# Doxazosin — 4-Level Quantitative Profile

> **Role in PoC:** Selective alpha1 antagonist; vasodilation via alpha1b subtype blockade. Class: Antihypertensive.
> **Label note:** Long t½ (22h); first-dose syncope risk; ALSO used for BPH

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **alpha1-adrenergic receptor** | 8.5 -log10 Ki |

**Selectivity:** alpha1 > alpha2 (~100-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 65% |
| **Half-life** | 22.0 h |
| **Volume of distribution** | 1.0 L/kg |
| **Metabolism** | Hepatic CYP3A4 (O-demethylation) |
| **Renal excretion** | 65% |
| **Special** | Long t½ (22h); first-dose syncope risk; ALSO used for BPH |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 0 of 1 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **metabolic_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; bottom score (1) on electrolyte_risk, ddi_risk; heart-rate effect: none. Evidence pool: 24 PMIDs (relevance 66.2%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-7) at 1-16mg |

### Indications

- Hypertension
- BPH

| Success rate (monotherapy) | 0.5 |
| Onset | 180 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10631624 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10720596 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12045387 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12496911 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12496921 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14681504 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15711605 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16330901 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16596036 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16613526 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21896142 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22147655 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+12 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Doxazosin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

