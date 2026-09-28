# Chlorthalidone — 4-Level Quantitative Profile

> **Role in PoC:** Thiazide-like diuretic; inhibits Na-Cl cotransporter, longer-acting than HCTZ. Class: Antihypertensive.
> **Label note:** Very long t½ due to extensive RBC partitioning; superior to HCTZ in ALLHAT trial

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **NCC** | 7.5 -log10 IC50 |

**Selectivity:** NCC (does NOT inhibit CA)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 65% |
| **Half-life** | 50.0 h |
| **Volume of distribution** | 4.0 L/kg |
| **Metabolism** | Not metabolized (eliminated unchanged in urine) |
| **Renal excretion** | 50% |
| **Special** | Very long t½ due to extensive RBC partitioning; superior to HCTZ in ALLHAT trial |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 3 of 12 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **metabolic_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |

**L3 Signature:** top score (3) on bp_reduction; highest risk (3) on electrolyte_risk; bottom score (1) on ddi_risk; heart-rate effect: none. Evidence pool: 22 PMIDs (relevance 69.9%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-4) at 12.5-25mg |

### Indications

- Hypertension
- Edema

| Success rate (monotherapy) | 0.52 |
| Onset | 180 min |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | safe |
| **Lactation** | safe |
| **Pregnancy** | B |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 12479763 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15238589 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16760687 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24070321 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25733245 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26760416 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28711447 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30354828 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32568361 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34739197 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35404993 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35727171 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+10 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Chlorthalidone

1. **Unapplied adjudication proposal:** chlorthalidone|renal_protection: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

