# Felodipine — 4-Level Quantitative Profile

> **Role in PoC:** Dihydropyridine CCB; L-type Cav1.2 blocker. Class: Antihypertensive.
> **Label note:** High vascular selectivity; grapefruit juice interaction (CYP3A4)

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **L-type calcium channel** | 8.8 -log10 Ki |

**Selectivity:** Vascular-selective > cardiac

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 15% |
| **Half-life** | 25.0 h |
| **Volume of distribution** | 4.0 L/kg |
| **Metabolism** | Hepatic CYP3A4 |
| **Renal excretion** | 70% |
| **Special** | High vascular selectivity; grapefruit juice interaction (CYP3A4) |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 3 of 9 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **heart_rate_effect** | tachycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **metabolic_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk, ddi_risk; heart-rate effect: tachycardia. Evidence pool: 36 PMIDs (relevance 86.8%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 5-10mg |

### Indications

- Hypertension
- Stable angina

| Success rate (monotherapy) | 0.58 |
| Onset | 240 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10984813 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11096527 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11146977 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11281514 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11347860 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11368286 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14620396 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1519636 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15777109 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1614069 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1693722 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1693735 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+24 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Felodipine

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

