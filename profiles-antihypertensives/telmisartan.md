# Telmisartan — 4-Level Quantitative Profile

> **Role in PoC:** AT1 receptor antagonist; PPARgamma partial agonist. Class: Antihypertensive.
> **Label note:** Longest t½ (24h); PPARgamma partial agonism adds metabolic benefit; biliary elimination ~95%

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **AT1 receptor** | 9.5 -log10 Ki |

**Selectivity:** AT1 > AT2 (>3,000-fold); PPARgamma moderate

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 45% |
| **Half-life** | 24.0 h |
| **Volume of distribution** | 0.5 L/kg |
| **Metabolism** | Hepatic glucuronidation |
| **Renal excretion** | 5% |
| **Special** | Longest t½ (24h); PPARgamma partial agonism adds metabolic benefit; biliary elimination ~95% |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **electrolyte_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | batch4_rescore: held (value confirmed, no change proposed) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 28 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; heart-rate effect: none. Evidence pool: 28 PMIDs (relevance 59.6%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-6) at 40-80mg |

### Indications

- Hypertension
- CV risk reduction

| Success rate (monotherapy) | 0.54 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11014323 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11185637 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11408526 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12799094 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14712886 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15061687 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15618736 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17122147 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18705533 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18757085 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20223228 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22272064 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+16 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Telmisartan

1. **Unapplied adjudication proposal:** telmisartan|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

