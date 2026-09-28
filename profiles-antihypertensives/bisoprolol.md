# Bisoprolol — 4-Level Quantitative Profile

> **Role in PoC:** Cardioselective beta1 antagonist. Class: Antihypertensive.
> **Label note:** Highest cardioselectivity; balanced clearance; once-daily

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **beta1-adrenergic receptor** | 8.2 -log10 Ki |

**Selectivity:** beta1 > beta2 (~14-fold, highest)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 90% |
| **Half-life** | 11.0 h |
| **Volume of distribution** | 3.0 L/kg |
| **Metabolism** | Hepatic CYP2D6 (50%) + renal clearance (50%) |
| **Renal excretion** | 50% |
| **Special** | Highest cardioselectivity; balanced clearance; once-daily |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **metabolic_effect** | 1 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 23 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction; bottom score (1) on metabolic_effect, electrolyte_risk; heart-rate effect: bradycardia. Evidence pool: 23 PMIDs (relevance 47.4%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-7) at 5-20mg |

### Indications

- Hypertension
- Heart failure
- Angina

| Success rate (monotherapy) | 0.52 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 22571411 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23719964 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25577782 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26996442 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28256104 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30408572 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34353555 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34741999 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38447973 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38886107 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39124839 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39469919 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+11 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Bisoprolol

1. **Unapplied adjudication proposal:** bisoprolol|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

