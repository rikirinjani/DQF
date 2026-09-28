# Spironolactone — 4-Level Quantitative Profile

> **Role in PoC:** Competitive MR antagonist; potassium-sparing diuretic. Class: Antihypertensive.
> **Label note:** Active metabolites carry longer t½ (canrenone ~16h); gynecomastia risk; hyperkalemia

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **mineralocorticoid receptor** | 8.2 -log10 Ki |

**Selectivity:** MR > AR,PR,GR (weak antiandrogen)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 70% |
| **Half-life** | 1.5 h |
| **Volume of distribution** | 0.9 L/kg |
| **Metabolism** | Hepatic (active metabolites: 7alpha-thiomethylspironolactone, canrenone) |
| **Renal excretion** | 30% |
| **Special** | Active metabolites carry longer t½ (canrenone ~16h); gynecomastia risk; hyperkalemia |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 3 of 6 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk; heart-rate effect: none. Evidence pool: 28 PMIDs (relevance 53.3%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 25-100mg |

### Indications

- Hypertension (resistant)
- Heart failure
- Primary aldosteronism

| Success rate (monotherapy) | 0.5 |
| Onset | 1440 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 16649723 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17448412 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18488807 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19006114 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21804623 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2191584 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23866347 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23900882 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25967959 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26221266 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27057293 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28700781 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+16 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Spironolactone

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

