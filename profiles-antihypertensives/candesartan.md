# Candesartan — 4-Level Quantitative Profile

> **Role in PoC:** AT1 receptor antagonist (insurmountable); prodrug candesartan cilexetil. Class: Antihypertensive.
> **Label note:** Insurmountable AT1 blockade; tight receptor binding

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **AT1 receptor** | 9.0 -log10 Ki |

**Selectivity:** AT1 > AT2 (>10,000-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 42% |
| **Half-life** | 9.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic esterase → active candesartan |
| **Renal excretion** | 60% |
| **Special** | Insurmountable AT1 blockade; tight receptor binding |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 2 of 7 pk/pd-filtered sentences) |
| **electrolyte_risk** | 2 | risk | batch4_rescore: held (value confirmed, no change proposed) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; heart-rate effect: none. Evidence pool: 28 PMIDs (relevance 75.7%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-6) at 8-32mg |

### Indications

- Hypertension
- Heart failure

| Success rate (monotherapy) | 0.53 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10902066 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11318085 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11683476 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11825094 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 13678870 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 13678871 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15526237 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15592574 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18046913 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21421652 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21651457 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22820775 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+16 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Candesartan

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

