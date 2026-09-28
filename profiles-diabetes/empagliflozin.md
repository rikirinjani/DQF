# Empagliflozin — 4-Level Quantitative Profile

> **Role in PoC:** SGLT2 inhibitor; blocks renal glucose reabsorption → glycosuria. Class: Diabetes.
> **Label note:** EMPA-REG OUTCOME showed 14% CV mortality reduction

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SGLT2** | 8.3 -log10 IC50 |

**Selectivity:** SGLT2 >>> SGLT1 (>2500x)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 78% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 1.6 L/kg |
| **Metabolism** | UGT2B7, UGT1A9 (glucuronidation) |
| **Renal excretion** | 55% |
| **Special** | EMPA-REG OUTCOME showed 14% CV mortality reduction |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 1 of 4 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 25 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk. Evidence pool: 25 PMIDs (relevance 43.9%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.8 % at 10-25mg |

### Indications

- T2DM
- Heart failure (EMPEROR-Reduced)
- CKD (EMPA-KIDNEY)

| Success rate (monotherapy) | 0.6 |
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
| PMID 23253948 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26040302 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27085585 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30586757 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31378154 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32256445 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32915523 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33050931 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35216342 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 36224542 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 36702979 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 36716212 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+13 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Empagliflozin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

