# Hydrochlorothiazide — 4-Level Quantitative Profile

> **Role in PoC:** Thiazide diuretic; inhibits Na-Cl cotransporter in distal convoluted tubule. Class: Antihypertensive. L3 values updated by the N1 batch-5 rescore (2026-09-28).
> **Label note:** Duration longer than t½ suggests prolonged tissue binding to RBC CA

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **NCC** | 7.2 -log10 IC50 |

**Selectivity:** NCC > CA (weak carbonic anhydrase inhibition)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 70% |
| **Half-life** | 10.0 h |
| **Volume of distribution** | 3.0 L/kg |
| **Metabolism** | Not metabolized (eliminated unchanged in urine) |
| **Renal excretion** | 95% |
| **Special** | Duration longer than t½ suggests prolonged tissue binding to RBC CA |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 35 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 35 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 35 PMIDs, relevance gate pass) |
| **metabolic_effect** | 2 | direction-agnostic | auto-extracted; batch4_rescore proposed 3 (not applied) |
| **renal_protection** | 3 | benefit | N1 batch-5 rescore 2026-09-28 (applied 2→3): hydrochlorothiazide and prevention of kidney-stone recurrence (PMID 36856614, NEJM RCT); strong:2 |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk; heart-rate effect: none. Evidence pool: 35 PMIDs (relevance 76.2%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 12.5-50mg |

### Indications

- Hypertension
- Edema
- Nephrogenic DI

| Success rate (monotherapy) | 0.48 |
| Onset | 120 min |

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
| PMID 10353300 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10586840 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12461303 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18705533 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19052124 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22314115 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23778914 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23993697 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25335110 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25733245 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26049382 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26760416 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+23 more PMIDs in the evidence pool)* | |
| batch5_rescore_adjudication.json | N1-applied L3 cells (2026-09-28) |

---

## Framework Takeaways for Hydrochlorothiazide

1. **N1 rescore (2→3 on renal_protection):** hydrochlorothiazide and prevention of kidney-stone recurrence (PMID 36856614, NEJM RCT); strong:2
2. **Unapplied adjudication proposal:** hydrochlorothiazide|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.
3. **Unapplied adjudication proposal:** hydrochlorothiazide|metabolic_effect: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

