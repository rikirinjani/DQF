# Hydralazine — 4-Level Quantitative Profile

> **Role in PoC:** Direct vasodilator; NO-mediated cGMP activation. Class: Antihypertensive.
> **Label note:** Reflex tachycardia; drug-induced lupus (slow acetylators); typically combo with BB + diuretic

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **smooth muscle NO pathway** | 5.5 -log10 Ki |

**Selectivity:** Arteriolar > venous

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 35% |
| **Half-life** | 3.0 h |
| **Volume of distribution** | 1.5 L/kg |
| **Metabolism** | Hepatic N-acetylation (polymorphic: slow/fast acetylators) |
| **Renal excretion** | 15% |
| **Special** | Reflex tachycardia; drug-induced lupus (slow acetylators); typically combo with BB + diuretic |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **electrolyte_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **heart_rate_effect** | tachycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **metabolic_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction; heart-rate effect: tachycardia. Evidence pool: 29 PMIDs (relevance 69.2%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 5 (95% CI 3-8) at 25-100mg TID |

### Indications

- Hypertension
- Heart failure (with ISDN)

| Success rate (monotherapy) | 0.45 |
| Onset | 45 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 12466730 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16292990 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17854237 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19092641 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20687078 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21781652 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21896152 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22071816 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2524348 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2656046 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2866863 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28711448 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+17 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Hydralazine

1. **Unapplied adjudication proposal:** hydralazine|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

