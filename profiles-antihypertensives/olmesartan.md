# Olmesartan — 4-Level Quantitative Profile

> **Role in PoC:** AT1 receptor antagonist; prodrug olmesartan medoxomil. Class: Antihypertensive.
> **Label note:** Enterohepatic recirculation

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **AT1 receptor** | 8.8 -log10 Ki |

**Selectivity:** AT1 > AT2 (>12,500-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 28% |
| **Half-life** | 13.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Intestinal esterase → olmesartan |
| **Renal excretion** | 50% |
| **Special** | Enterohepatic recirculation |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 2 of 12 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; bottom score (1) on electrolyte_risk, ddi_risk; heart-rate effect: none. Evidence pool: 25 PMIDs (relevance 48.3%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-5) at 20-40mg |

### Indications

- Hypertension

| Success rate (monotherapy) | 0.54 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 15291377 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15323064 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15592575 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16372830 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17364587 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17532689 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20434053 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20974325 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21254872 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22920046 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27404671 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30369568 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+13 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Olmesartan

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

