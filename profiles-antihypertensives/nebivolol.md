# Nebivolol — 4-Level Quantitative Profile

> **Role in PoC:** Highly cardioselective beta1 antagonist; NO-mediated vasodilation. Class: Antihypertensive.
> **Label note:** NO-mediated vasodilation (unlike other betaBs); L-arginine/NO pathway

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **beta1-adrenergic receptor** | 8.8 -log10 Ki |

**Selectivity:** beta1 > beta2 (~50-fold, highest selectivity)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 85% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 10.0 L/kg |
| **Metabolism** | Hepatic CYP2D6 (extensive polymorphic metabolism) |
| **Renal excretion** | 40% |
| **Special** | NO-mediated vasodilation (unlike other betaBs); L-arginine/NO pathway |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 2 of 4 pk/pd-filtered sentences) |
| **electrolyte_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |
| **renal_protection** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction; highest risk (3) on ddi_risk; bottom score (1) on renal_protection; heart-rate effect: bradycardia. Evidence pool: 18 PMIDs (relevance 45.6%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-6) at 5-20mg |

### Indications

- Hypertension
- Heart failure (elderly)

| Success rate (monotherapy) | 0.52 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 12092233 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16772759 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17786067 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19527321 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19655820 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23331709 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23977191 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24845234 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37849071 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39525432 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39673185 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39713902 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+6 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Nebivolol

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

