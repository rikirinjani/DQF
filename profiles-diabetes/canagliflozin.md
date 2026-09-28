# Canagliflozin — 4-Level Quantitative Profile

> **Role in PoC:** SGLT2 inhibitor; blocks renal glucose reabsorption in proximal tubule. Class: Diabetes.
> **Label note:** Weak SGLT1 inhibition in gut; CREDENCE trial renal benefit; amputation signal (CANVAS)

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **SGLT2** | 8.0 -log10 Ki |

**Selectivity:** SGLT2 > SGLT1 (~250-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 65% |
| **Half-life** | 13.0 h |
| **Volume of distribution** | 1.0 L/kg |
| **Metabolism** | Hepatic O-glucuronidation (UGT1A9, UGT2B4) |
| **Renal excretion** | 30% |
| **Special** | Weak SGLT1 inhibition in gut; CREDENCE trial renal benefit; amputation signal (CANVAS) |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 0 of 2 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 21 PMIDs (relevance 38.6%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.8 % at 100-300mg |

### Indications

- T2DM
- CKD (CREDENCE)
- CV risk reduction (CANVAS)

| Success rate (monotherapy) | 0.58 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 23370138 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24918789 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27136910 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27160639 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27567160 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27899497 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27977934 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 36757426 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37227388 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38188970 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38513740 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38964727 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+9 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Canagliflozin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

