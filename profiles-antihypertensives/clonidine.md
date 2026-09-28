# Clonidine — 4-Level Quantitative Profile

> **Role in PoC:** Central alpha2 agonist; reduces sympathetic outflow from medulla. Class: Antihypertensive. L3 values updated by the N1 batch-5 rescore (2026-09-28).
> **Label note:** Rebound hypertension on abrupt cessation; transdermal patch available; sedation common

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **alpha2-adrenergic receptor** | 7.5 -log10 Ki |

**Selectivity:** alpha2 > alpha1 (~200:1)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 90% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 2.0 L/kg |
| **Metabolism** | Hepatic (50%) |
| **Renal excretion** | 50% |
| **Special** | Rebound hypertension on abrupt cessation; transdermal patch available; sedation common |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 4 of 8 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | N1 batch-5 rescore 2026-09-28 (applied 2→3): clonidine withdrawn -> glucose intolerance subsided (PMID 6279379); strong:2 - old study (1979) |
| **renal_protection** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |

**L3 Signature:** top score (3) on bp_reduction; bottom score (1) on electrolyte_risk; heart-rate effect: bradycardia. Evidence pool: 36 PMIDs (relevance 69.6%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-7) at 0.1-0.6mg/day |

### Indications

- Hypertension

| Success rate (monotherapy) | 0.5 |
| Onset | 90 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10423643 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10596256 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12126186 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15883756 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16545874 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16829723 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1700217 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20484620 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21192246 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22773717 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23365239 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24467572 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+24 more PMIDs in the evidence pool)* | |
| batch5_rescore_adjudication.json | N1-applied L3 cells (2026-09-28) |

---

## Framework Takeaways for Clonidine

1. **N1 rescore (2→3 on metabolic_effect):** clonidine withdrawn -> glucose intolerance subsided (PMID 6279379); strong:2 - old study (1979)
2. **Unapplied adjudication proposal:** clonidine|renal_protection: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

