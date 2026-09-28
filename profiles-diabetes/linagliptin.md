# Linagliptin — 4-Level Quantitative Profile

> **Role in PoC:** DPP-4 inhibitor. Class: Diabetes.
> **Label note:** No renal dose adjustment (biliary excretion); highest DPP-4 binding affinity; CARMELINA CV safety

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **DPP-4** | 9.0 -log10 Ki |

**Selectivity:** DPP-4 > DPP-8/9 (>10,000-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 30% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 10.0 L/kg |
| **Metabolism** | Minimal (unchanged parent ~90%) |
| **Renal excretion** | 5% |
| **Special** | No renal dose adjustment (biliary excretion); highest DPP-4 binding affinity; CARMELINA CV safety |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 2 of 2 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 27 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | batch4_rescore: held (value confirmed, no change proposed) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk. Evidence pool: 27 PMIDs (relevance 54.4%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.6 % at 5mg |

### Indications

- T2DM

| Success rate (monotherapy) | 0.53 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 21053992 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21205122 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21352464 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21681003 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21803422 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23468467 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24248503 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25215428 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 25780262 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26631506 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29853297 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30731650 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+15 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Linagliptin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

