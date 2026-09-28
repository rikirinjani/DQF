# Lisinopril — 4-Level Quantitative Profile

> **Role in PoC:** Competitive ACE inhibitor, blocks AngI → AngII conversion. Class: Antihypertensive.
> **Label note:** Long ACE-binding half-life permits once-daily dosing despite short serum t½

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **ACE** | 8.5 -log10 IC50 |

**Selectivity:** ACE > ACE2 (no bradykinin breakdown)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 25% |
| **Half-life** | 12.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Not metabolized (renal elimination unchanged) |
| **Renal excretion** | 100% |
| **Special** | Long ACE-binding half-life permits once-daily dosing despite short serum t½ |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | ddi_rescore: 1 (applied; kept 3 of 12 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **heart_rate_effect** | none | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **metabolic_effect** | 1 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; bottom score (1) on metabolic_effect, electrolyte_risk, ddi_risk; heart-rate effect: none. Evidence pool: 32 PMIDs (relevance 77.6%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 10-40mg |

### Indications

- Hypertension
- Heart failure
- Post-MI
- Diabetic nephropathy

| Success rate (monotherapy) | 0.55 |
| Onset | 60 min |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | safe |
| **Lactation** | safe |
| **Pregnancy** | D |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10587334 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11834188 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12479763 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1338526 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 14553956 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16484515 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16894055 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17216247 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 17487821 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19792996 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19840529 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22980373 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+20 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Lisinopril

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

