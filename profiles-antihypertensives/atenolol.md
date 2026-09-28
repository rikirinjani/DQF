# Atenolol — 4-Level Quantitative Profile

> **Role in PoC:** Cardioselective beta1 antagonist. Class: Antihypertensive.
> **Label note:** Hydrophilic; renal clearance; low CNS penetration

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **beta1-adrenergic receptor** | 7.5 -log10 Ki |

**Selectivity:** beta1 > beta2 (~5-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 50% |
| **Half-life** | 7.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Minimal hepatic (hydrophilic) |
| **Renal excretion** | 90% |
| **Special** | Hydrophilic; renal clearance; low CNS penetration |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **electrolyte_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 36 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |

**L3 Signature:** top score (3) on bp_reduction; heart-rate effect: bradycardia. Evidence pool: 36 PMIDs (relevance 68.8%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-7) at 25-100mg |

### Indications

- Hypertension
- Angina
- Post-MI
- SVT

| Success rate (monotherapy) | 0.5 |
| Onset | 90 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10862260 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11113718 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11937178 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12841816 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15025846 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15530629 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16154016 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16417067 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16431379 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16833041 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1764953 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17686376 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+24 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Atenolol

1. **Unapplied adjudication proposal:** atenolol|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.
2. **Unapplied adjudication proposal:** atenolol|renal_protection: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

