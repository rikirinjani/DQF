# Dulaglutide — 4-Level Quantitative Profile

> **Role in PoC:** GLP-1 receptor agonist (Fc-fusion protein, once-weekly). Class: Diabetes.
> **Label note:** Once-weekly SC; REWIND trial CV benefit; Fc fusion extends t½ to 5 days; 3-4lb weight loss

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **GLP-1 receptor** | 8.0 -log10 Ki |

**Selectivity:** GLP-1R selective

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 50% |
| **Half-life** | 120.0 h |
| **Volume of distribution** | 0.1 L/kg |
| **Metabolism** | Proteolytic degradation |
| **Renal excretion** | 1% |
| **Special** | Once-weekly SC; REWIND trial CV benefit; Fc fusion extends t½ to 5 days; 3-4lb weight loss |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 0 of 1 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; bottom score (1) on ddi_risk. Evidence pool: 22 PMIDs (relevance 45.6%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.2 % at 0.75-4.5mg SC/week |

### Indications

- T2DM
- CV risk reduction (REWIND)

| Success rate (monotherapy) | 0.63 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 24918645 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26507721 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29852875 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30762290 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31055780 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31302140 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33606902 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35027802 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35546790 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37743669 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38310883 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38942076 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+10 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Dulaglutide

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

