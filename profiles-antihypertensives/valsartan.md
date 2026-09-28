# Valsartan — 4-Level Quantitative Profile

> **Role in PoC:** Competitive AT1 receptor antagonist. Class: Antihypertensive.
> **Label note:** Biliary excretion (70%); food reduces AUC 40%

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **AT1 receptor** | 8.5 -log10 Ki |

**Selectivity:** AT1 > AT2 (>20,000-fold)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 25% |
| **Half-life** | 6.0 h |
| **Volume of distribution** | 0.4 L/kg |
| **Metabolism** | Not metabolized (<20%) |
| **Renal excretion** | 30% |
| **Special** | Biliary excretion (70%); food reduces AUC 40% |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 2 of 8 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 31 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; bottom score (1) on electrolyte_risk, ddi_risk; heart-rate effect: none. Evidence pool: 31 PMIDs (relevance 59.6%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-6) at 80-320mg |

### Indications

- Hypertension
- Heart failure
- Post-MI with LV dysfunction

| Success rate (monotherapy) | 0.52 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10333347 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12444541 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17621800 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27128457 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33763167 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34062069 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35470677 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38419057 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38814606 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38922973 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39094905 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39260836 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+19 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Valsartan

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

