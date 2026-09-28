# Methyldopa — 4-Level Quantitative Profile

> **Role in PoC:** Central alpha2 agonist; converted to alpha-methylnorepinephrine; stimulates central alpha2 receptors reducing SNS outflow. Class: Antihypertensive.
> **Label note:** Preferred for pregnancy-induced hypertension (safety record); positive Coombs test ~20%; sedating

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **alpha2-adrenergic receptor** | 6.5 -log10 Ki |

**Selectivity:** alpha2 > alpha1, central (prodrug)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 45% |
| **Half-life** | 2.0 h |
| **Volume of distribution** | 0.4 L/kg |
| **Metabolism** | Hepatic O-methylation + renal elimination of metabolites |
| **Renal excretion** | 70% |
| **Special** | Preferred for pregnancy-induced hypertension (safety record); positive Coombs test ~20%; sedating |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 0 of 2 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **metabolic_effect** | 1 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction; bottom score (1) on metabolic_effect, electrolyte_risk, ddi_risk; heart-rate effect: none. Evidence pool: 28 PMIDs (relevance 51.3%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-8) at 250-3000mg/day |

### Indications

- Hypertension (pregnancy)

| Success rate (monotherapy) | 0.48 |
| Onset | 300 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11642029 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12464717 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1315815 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1486880 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15860966 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17395120 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1863186 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19821316 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21289717 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22147655 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22813366 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26033778 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+16 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Methyldopa

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

