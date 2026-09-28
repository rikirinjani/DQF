# Indapamide — 4-Level Quantitative Profile

> **Role in PoC:** Thiazide-like diuretic; blocks Na⁺-Cl⁻ cotransporter in DCT. Class: Antihypertensive.
> **Label note:** Lipophilic; high Vd; extrarenal vasodilatory effect; longer t½ than HCTZ

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **NCC** | 6.5 -log10 Ki |

**Selectivity:** NCC-selective

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 95% |
| **Half-life** | 17.0 h |
| **Volume of distribution** | 25.0 L/kg |
| **Metabolism** | Hepatic (extensive) |
| **Renal excretion** | 60% |
| **Special** | Lipophilic; high Vd; extrarenal vasodilatory effect; longer t½ than HCTZ |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 5 of 15 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | batch4_rescore: 3 (applied) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |

**L3 Signature:** top score (3) on bp_reduction; highest risk (3) on electrolyte_risk; heart-rate effect: none. Evidence pool: 25 PMIDs (relevance 74.6%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 1.25-5mg |

### Indications

- Hypertension
- Edema

| Success rate (monotherapy) | 0.52 |
| Onset | 150 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10796061 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11589932 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12016800 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17588853 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17765963 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20819002 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2184650 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23447043 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25733245 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28711447 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30354828 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 3311532 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+13 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Indapamide

1. **Unapplied adjudication proposal:** indapamide|renal_protection: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

