# Trandolapril — 4-Level Quantitative Profile

> **Role in PoC:** ACE inhibitor prodrug. Class: Antihypertensive.
> **Label note:** Longest t½; once-daily dosing with 24h BP coverage

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **ACE** | 9.2 -log10 Ki |

**Selectivity:** ACE > ACE2

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 40% |
| **Half-life** | 24.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic → trandolaprilat |
| **Renal excretion** | 70% |
| **Special** | Longest t½; once-daily dosing with 24h BP coverage |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 2 of 12 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk; bottom score (1) on ddi_risk; heart-rate effect: none. Evidence pool: 27 PMIDs (relevance 67.2%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 1-8mg |

### Indications

- Hypertension
- Heart failure
- Post-MI with LV dysfunction

| Success rate (monotherapy) | 0.52 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10668225 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10709442 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11030016 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11030019 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11067783 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12852701 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14706664 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16114984 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16939632 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17472822 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17583177 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19337528 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+15 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Trandolapril

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

