# Dapagliflozin — 4-Level Quantitative Profile

> **Role in PoC:** SGLT2 inhibitor; glycosuria, modest diuretic effect. Class: Diabetes.
> **Label note:** DAPA-HF showed 26% CV death/HF hospitalization reduction irrespective of diabetes status

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SGLT2** | 8.0 -log10 IC50 |

**Selectivity:** SGLT2 >> SGLT1

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 78% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 1.5 L/kg |
| **Metabolism** | UGT1A9 (glucuronidation to inactive metabolite) |
| **Renal excretion** | 75% |
| **Special** | DAPA-HF showed 26% CV death/HF hospitalization reduction irrespective of diabetes status |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | batch4_rescore: held (value confirmed, no change proposed) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 1 of 3 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 29 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; bottom score (1) on ddi_risk. Evidence pool: 29 PMIDs (relevance 56.1%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.7 % at 5-10mg |

### Indications

- T2DM
- Heart failure (DAPA-HF)
- CKD (DAPA-CKD)

| Success rate (monotherapy) | 0.58 |
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
| PMID 28583425 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30222367 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31077437 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32239659 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32247210 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32274678 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32353360 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33543924 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33595593 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34224699 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 36702979 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37655809 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+17 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Dapagliflozin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

