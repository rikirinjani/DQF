# Losartan — 4-Level Quantitative Profile

> **Role in PoC:** Selective AT1 receptor antagonist; active metabolite E-3174 more potent. Class: Antihypertensive. L3 values updated by the N1 batch-5 rescore (2026-09-28).
> **Label note:** Active metabolite E-3174 has 10-40x greater AT1 affinity

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **AT1 receptor** | 8.8 -log10 Ki |

**Selectivity:** AT1 >>> AT2

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 33% |
| **Half-life** | 2.0 h |
| **Volume of distribution** | 0.4 L/kg |
| **Metabolism** | CYP2C9, CYP3A4 (prodrug → E-3174 active metabolite, t½ 6-9h) |
| **Renal excretion** | 60% |
| **Special** | Active metabolite E-3174 has 10-40x greater AT1 affinity |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | auto-extracted; ddi_rescore proposed 1 (not applied) |
| **electrolyte_risk** | 3 | risk | N1 batch-5 rescore 2026-09-28 (applied 1→3): double-blind randomized study evaluating losartan potassium monotherapy or in combination (PMID 18328120); strong:2 - potassium salt, hyperkalemia risk; note 2-step jump |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |

**L3 Signature:** top score (3) on bp_reduction; highest risk (3) on electrolyte_risk; heart-rate effect: none. Evidence pool: 21 PMIDs (relevance 46.7%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-6) at 50-100mg |

### Indications

- Hypertension
- Diabetic nephropathy
- Stroke prevention (LIFE)

| Success rate (monotherapy) | 0.52 |
| Onset | 120 min |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | caution |
| **Lactation** | safe |
| **Pregnancy** | D |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10404953 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10455478 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10463203 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18328120 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18800461 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24524371 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38377482 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38775910 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38815786 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39281239 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39851122 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 40013202 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+9 more PMIDs in the evidence pool)* | |
| batch5_rescore_adjudication.json | N1-applied L3 cells (2026-09-28) |

---

## Framework Takeaways for Losartan

1. **N1 rescore (1→3 on electrolyte_risk):** double-blind randomized study evaluating losartan potassium monotherapy or in combination (PMID 18328120); strong:2 - potassium salt, hyperkalemia risk; note 2-step jump
2. **Unapplied adjudication proposal:** losartan|ddi_risk: ddi_rescore proposed 1, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.
3. **Unapplied adjudication proposal:** losartan|renal_protection: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

