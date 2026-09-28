# Nifedipine — 4-Level Quantitative Profile

> **Role in PoC:** Dihydropyridine CCB; blocks L-type Ca²⁺ channel (Cav1.2). Class: Antihypertensive.
> **Label note:** Extended-release formulations used; reflex tachycardia with immediate-release

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **L-type calcium channel** | 8.5 -log10 Ki |

**Selectivity:** Vascular > cardiac

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 60% |
| **Half-life** | 2.0 h |
| **Volume of distribution** | 0.8 L/kg |
| **Metabolism** | Hepatic CYP3A4 |
| **Renal excretion** | 80% |
| **Special** | Extended-release formulations used; reflex tachycardia with immediate-release |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 47 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 8 of 14 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | batch4_rescore: 3 (applied) |
| **heart_rate_effect** | tachycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 47 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 47 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 47 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk, ddi_risk; heart-rate effect: tachycardia. Evidence pool: 47 PMIDs (relevance 75.0%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 30-90mg ER |

### Indications

- Hypertension
- Stable angina
- Vasospastic angina

| Success rate (monotherapy) | 0.58 |
| Onset | 180 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10900233 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11066620 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11336775 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11986915 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15175561 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15715601 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15898828 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16033250 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19337538 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19501083 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2076408 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21967023 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+35 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Nifedipine

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

