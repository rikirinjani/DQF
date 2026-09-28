# Terazosin — 4-Level Quantitative Profile

> **Role in PoC:** Selective alpha1 antagonist. Class: Antihypertensive.
> **Label note:** Also BPH indication; first-dose syncope; no longer first-line for HTN (ALLHAT)

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **alpha1-adrenergic receptor** | 8.0 -log10 Ki |

**Selectivity:** alpha1 > alpha2

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 90% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 0.8 L/kg |
| **Metabolism** | Minimal hepatic |
| **Renal excretion** | 40% |
| **Special** | Also BPH indication; first-dose syncope; no longer first-line for HTN (ALLHAT) |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 30 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 3 of 9 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 30 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 30 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 30 PMIDs, relevance gate pass) |
| **renal_protection** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 30 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction; highest risk (3) on electrolyte_risk, ddi_risk; bottom score (1) on renal_protection; heart-rate effect: none. Evidence pool: 30 PMIDs (relevance 62.5%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-7) at 1-20mg |

### Indications

- Hypertension
- BPH

| Success rate (monotherapy) | 0.5 |
| Onset | 150 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10094095 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10414731 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10737482 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11028256 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11711348 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11750250 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12519611 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12938521 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16613526 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1678920 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1678922 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1678924 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+18 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Terazosin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

