# Captopril — 4-Level Quantitative Profile

> **Role in PoC:** Direct ACE inhibitor (not prodrug); contains sulfhydryl group. Class: Antihypertensive.
> **Label note:** SH group confers free-radical scavenging; short t½ requires BID/TID

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **ACE** | 8.2 -log10 Ki |

**Selectivity:** ACE > ACE2

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 65% |
| **Half-life** | 2.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Partial hepatic oxidation |
| **Renal excretion** | 95% |
| **Special** | SH group confers free-radical scavenging; short t½ requires BID/TID |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 5 of 14 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk, ddi_risk; heart-rate effect: none. Evidence pool: 36 PMIDs (relevance 73.8%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-6) at 25-150mg |

### Indications

- Hypertension
- Heart failure
- Post-MI
- Diabetic nephropathy

| Success rate (monotherapy) | 0.5 |
| Onset | 60 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11474160 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11834188 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11890606 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12817017 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1373306 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1546641 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1644089 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2408245 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25465731 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2674438 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26871774 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26883147 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+24 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Captopril

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

