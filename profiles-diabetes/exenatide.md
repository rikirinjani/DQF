# Exenatide — 4-Level Quantitative Profile

> **Role in PoC:** GLP-1 receptor agonist (synthetic exendin-4 from Gila monster). Class: Diabetes. L3 values updated by the N1 batch-5 rescore (2026-09-28).
> **Label note:** First GLP-1 RA; BID for immediate-release, once-weekly for ER; EXSCEL CV neutral; nausea common

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **GLP-1 receptor** | 8.0 -log10 Ki |

**Selectivity:** GLP-1R selective

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 65% |
| **Half-life** | 2.5 h |
| **Volume of distribution** | 0.1 L/kg |
| **Metabolism** | Renal proteolysis + glomerular filtration |
| **Renal excretion** | 90% |
| **Special** | First GLP-1 RA; BID for immediate-release, once-weekly for ER; EXSCEL CV neutral; nausea common |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 19 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | N1 batch-5 rescore 2026-09-28 (applied 2→3): long-term changes in cardiovascular risk markers during exenatide twice daily (PMID 26338040); strong:2 |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 19 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 19 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 19 PMIDs, relevance gate pass) |
| **renal_benefit** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 19 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk; bottom score (1) on ddi_risk. Evidence pool: 19 PMIDs (relevance 33.3%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 0.9 % at 5-10mcg BID / 2mg ER/week |

### Indications

- T2DM

| Success rate (monotherapy) | 0.6 |
| Onset | days |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 21138825 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21142268 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21902291 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23404321 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23748507 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23885352 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26338040 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27896683 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28573708 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32803900 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34873344 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 36128537 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+7 more PMIDs in the evidence pool)* | |
| batch5_rescore_adjudication.json | N1-applied L3 cells (2026-09-28) |

---

## Framework Takeaways for Exenatide

1. **N1 rescore (2→3 on cv_outcome_benefit):** long-term changes in cardiovascular risk markers during exenatide twice daily (PMID 26338040); strong:2

