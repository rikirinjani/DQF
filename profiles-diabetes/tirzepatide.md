# Tirzepatide — 4-Level Quantitative Profile

> **Role in PoC:** Dual GIP/GLP-1 receptor agonist; superior glycemic control + weight loss vs GLP-1 monotherapy. Class: Diabetes.
> **Label note:** SURPASS trials: 1.5-2.1% A1c reduction; SURMOUNT-1: 15-21% body weight loss

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **GIP receptor** | 10.3 -log10 EC50 |
| **GLP-1 receptor** | 9.0 -log10 EC50 |

**Selectivity:** GIPR ~ GLP-1R (balanced dual agonist)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 80% |
| **Half-life** | 120.0 h |
| **Volume of distribution** | 10.0 L/kg |
| **Metabolism** | Proteolysis (amino acid catabolism) |
| **Renal excretion** | 3% |
| **Special** | SURPASS trials: 1.5-2.1% A1c reduction; SURMOUNT-1: 15-21% body weight loss |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | batch4_rescore: held (value confirmed, no change proposed) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **renal_benefit** | 2 | benefit | auto-extracted; batch4_rescore proposed 3 (not applied) |
| **weight_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 24 PMIDs (relevance 42.9%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 2.1 % at 5-15mg SC |

### Indications

- T2DM
- Obesity (SURMOUNT)

| Success rate (monotherapy) | 0.75 |
| Onset | days |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | safe |
| **Lactation** | unknown |
| **Pregnancy** | C |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 33778934 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35468322 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 36750526 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37141329 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37246796 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37279858 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38089044 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39212900 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39263564 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39344853 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39464637 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39681390 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+12 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Tirzepatide

1. **Unapplied adjudication proposal:** tirzepatide|renal_benefit: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

