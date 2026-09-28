# Acarbose — 4-Level Quantitative Profile

> **Role in PoC:** alpha-glucosidase inhibitor; delays carbohydrate digestion in small intestine. Class: Diabetes.
> **Label note:** Minimal systemic absorption (<2%); works locally in gut; flatulence common; postprandial glucose reduction

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **alpha-glucosidase** | 6.5 -log10 Ki |

**Selectivity:** Intestinal alpha-glucosidases > pancreatic alpha-amylase

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 2% |
| **Half-life** | 2.0 h |
| **Volume of distribution** | 0.1 L/kg |
| **Metabolism** | Intestinal metabolism by gut bacteria |
| **Renal excretion** | 50% |
| **Special** | Minimal systemic absorption (<2%); works locally in gut; flatulence common; postprandial glucose reduction |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | batch4_rescore: 3 (applied) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 1 of 3 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability. Evidence pool: 32 PMIDs (relevance 61.3%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.6 % at 50-100mg TID |

### Indications

- T2DM
- Prediabetes (STOP-NIDDM)

| Success rate (monotherapy) | 0.45 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10400405 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11893070 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12547847 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12965108 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14669056 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15051749 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15704043 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16855517 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17532702 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20568489 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24558078 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 24853116 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+20 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Acarbose

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

