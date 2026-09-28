# Perindopril — 4-Level Quantitative Profile

> **Role in PoC:** ACE inhibitor prodrug. Class: Antihypertensive.
> **Label note:** Highest tissue ACE penetration among ACEi

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **ACE** | 8.5 -log10 Ki |

**Selectivity:** ACE > ACE2

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 35% |
| **Half-life** | 17.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic → perindoprilat |
| **Renal excretion** | 75% |
| **Special** | Highest tissue ACE penetration among ACEi |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 2 of 13 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk, ddi_risk; heart-rate effect: none. Evidence pool: 31 PMIDs (relevance 76.5%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 4-8mg |

### Indications

- Hypertension
- Heart failure
- Stable CAD
- CV risk reduction

| Success rate (monotherapy) | 0.52 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11589932 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11591359 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11728296 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11903318 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12076191 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12092009 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 13678872 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15133535 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15982858 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16154016 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16370923 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17765963 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+19 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Perindopril

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

