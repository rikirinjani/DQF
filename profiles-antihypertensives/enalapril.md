# Enalapril — 4-Level Quantitative Profile

> **Role in PoC:** ACE inhibitor prodrug; blocks AngI→AngII conversion. Class: Antihypertensive.
> **Label note:** Active metabolite enalaprilat; prolonged terminal t½ ~35h

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **ACE** | 9.0 -log10 Ki |

**Selectivity:** ACE > ACE2

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 60% |
| **Half-life** | 11.0 h |
| **Volume of distribution** | 0.2 L/kg |
| **Metabolism** | Hepatic esterase → enalaprilat |
| **Renal excretion** | 90% |
| **Special** | Active metabolite enalaprilat; prolonged terminal t½ ~35h |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 1 of 4 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk; heart-rate effect: bradycardia. Evidence pool: 22 PMIDs (relevance 40.4%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 5-40mg |

### Indications

- Hypertension
- Heart failure
- Post-MI
- Asymptomatic LV dysfunction

| Success rate (monotherapy) | 0.53 |
| Onset | 120 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 12154520 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15985045 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1638712 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1895531 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22022012 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 22395404 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26871774 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 31969300 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38084196 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38330576 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38373878 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38789633 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+10 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Enalapril

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

