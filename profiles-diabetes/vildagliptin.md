# Vildagliptin — 4-Level Quantitative Profile

> **Role in PoC:** DPP-4 inhibitor (cyanopyrrolidine class). Class: Diabetes.
> **Label note:** BID dosing (short t½); liver enzyme monitoring required; not available in US

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **DPP-4** | 8.2 -log10 Ki |

**Selectivity:** DPP-4 > DPP-8/9

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 85% |
| **Half-life** | 2.5 h |
| **Volume of distribution** | 0.7 L/kg |
| **Metabolism** | Hepatic hydrolysis (cyano group → inactive metabolite) |
| **Renal excretion** | 85% |
| **Special** | BID dosing (short t½); liver enzyme monitoring required; not available in US |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 1 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 24 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, renal_benefit, gi_tolerability; bottom score (1) on cv_outcome_benefit, ddi_risk. Evidence pool: 24 PMIDs (relevance 48.3%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.6 % at 50mg BID |

### Indications

- T2DM

| Success rate (monotherapy) | 0.52 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 15886245 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17509069 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17698900 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17713976 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17961192 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18355325 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 20616619 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21415917 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22162539 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22191695 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22456294 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23039321 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+12 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Vildagliptin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

