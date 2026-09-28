# Metoprolol — 4-Level Quantitative Profile

> **Role in PoC:** Selective β1 blocker; reduces CO, HR, and renin release. Class: Antihypertensive.
> **Label note:** CYP2D6 PM phenotype mimics supratherapeutic dosing

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **beta1-adrenergic receptor** | 8.7 -log10 Ki |

**Selectivity:** β1 >> β2 (dose-dependent loss of selectivity at high doses)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 50% |
| **Half-life** | 4.0 h |
| **Volume of distribution** | 4.0 L/kg |
| **Metabolism** | CYP2D6 (polymorphic; poor metabolizers have 3-5x higher concentrations) |
| **Renal excretion** | 5% |
| **Special** | CYP2D6 PM phenotype mimics supratherapeutic dosing |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 48 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 3 of 7 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 48 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 48 PMIDs, relevance gate pass) |
| **metabolic_effect** | 2 | direction-agnostic | auto-extracted; batch4_rescore proposed 3 (not applied) |
| **renal_protection** | 2 | benefit | auto-extracted by the L3 pipeline (evidence pool 48 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction; highest risk (3) on ddi_risk; bottom score (1) on electrolyte_risk; heart-rate effect: bradycardia. Evidence pool: 48 PMIDs (relevance 81.8%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 4 (95% CI 3-7) at 50-200mg |

### Indications

- Hypertension
- Angina
- Post-MI
- Heart failure (succinate)

| Success rate (monotherapy) | 0.5 |
| Onset | 120 min |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | caution |
| **Lactation** | safe |
| **Pregnancy** | C/D |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10376614 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10613615 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10862260 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11192361 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11968069 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12853193 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14671567 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15075055 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15259762 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16624680 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18479744 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19164422 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+36 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Metoprolol

1. **Unapplied adjudication proposal:** metoprolol|metabolic_effect: batch4_rescore proposed 3, drugs.json has 2 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.

