# Propranolol — 4-Level Quantitative Profile

> **Role in PoC:** Non-selective beta antagonist. Class: Antihypertensive.
> **Label note:** Lipophilic; CNS penetration; migraine + tremor indications

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **beta1-adrenergic receptor** | 8.2 -log10 Ki |
| **beta2-adrenergic receptor** | 8.0 -log10 Ki |

**Selectivity:** Non-selective (beta1 = beta2)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 25% |
| **Half-life** | 4.0 h |
| **Volume of distribution** | 4.0 L/kg |
| **Metabolism** | Hepatic CYP2D6/CYP1A2 (high first-pass) |
| **Renal excretion** | 5% |
| **Special** | Lipophilic; CNS penetration; migraine + tremor indications |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 0 of 1 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |
| **metabolic_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |
| **renal_protection** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 18 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction; highest risk (3) on electrolyte_risk; bottom score (1) on renal_protection, ddi_risk; heart-rate effect: bradycardia. Evidence pool: 18 PMIDs (relevance 38.1%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-8) at 80-320mg |

### Indications

- Hypertension
- Angina
- Post-MI
- Migraine prophylaxis
- Essential tremor

| Success rate (monotherapy) | 0.48 |
| Onset | 90 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10759091 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12783630 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15106196 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15133405 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27473874 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31120143 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31133517 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38930938 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39533554 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39570058 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39655516 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 40052723 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+6 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Propranolol

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

