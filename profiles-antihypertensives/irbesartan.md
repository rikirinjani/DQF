# Irbesartan — 4-Level Quantitative Profile

> **Role in PoC:** Competitive AT1 receptor antagonist. Class: Antihypertensive.
> **Label note:** Highest bioavailability among ARBs

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **AT1 receptor** | 9.2 -log10 Ki |

**Selectivity:** AT1 > AT2 (>10,000-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 70% |
| **Half-life** | 15.0 h |
| **Volume of distribution** | 0.3 L/kg |
| **Metabolism** | Hepatic CYP2C9 glucuronidation |
| **Renal excretion** | 20% |
| **Special** | Highest bioavailability among ARBs |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 4 of 8 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; bottom score (1) on electrolyte_risk; heart-rate effect: none. Evidence pool: 31 PMIDs (relevance 79.7%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-6) at 150-300mg |

### Indications

- Hypertension
- Diabetic nephropathy

| Success rate (monotherapy) | 0.53 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10321426 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10902066 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10934672 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11565517 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11683476 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18971554 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19355995 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19601700 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20030566 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25925925 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30361325 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33461698 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+19 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Irbesartan

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

