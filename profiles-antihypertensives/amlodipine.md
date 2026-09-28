# Amlodipine — 4-Level Quantitative Profile

> **Role in PoC:** Dihydropyridine CCB, blocks L-type Ca channels in vascular smooth muscle. Class: Antihypertensive.
> **Label note:** Very long t½ permits once-daily dosing; slow onset avoids reflex tachycardia

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **L-type calcium channel** | 9.2 -log10 IC50 |

**Selectivity:** Vascular >>> cardiac (no significant negative inotropy)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 74% |
| **Half-life** | 40.0 h |
| **Volume of distribution** | 21.0 L/kg |
| **Metabolism** | CYP3A4 (extensive hepatic) |
| **Renal excretion** | 10% |
| **Special** | Very long t½ permits once-daily dosing; slow onset avoids reflex tachycardia |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 1 of 3 pk/pd-filtered sentences) |
| **electrolyte_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |
| **metabolic_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 26 PMIDs, relevance gate pass) |
| **renal_protection** | 2 | benefit | batch4_rescore: held (value confirmed, no change proposed) |

**L3 Signature:** top score (3) on bp_reduction; heart-rate effect: bradycardia. Evidence pool: 26 PMIDs (relevance 50.9%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-5) at 5-10mg |

### Indications

- Hypertension
- Stable angina
- Vasospastic angina

| Success rate (monotherapy) | 0.6 |
| Onset | 360 min |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | caution |
| **Lactation** | safe |
| **Pregnancy** | C |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 11372598 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11574741 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15220015 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16894055 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28560779 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28598202 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 29441826 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30341872 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32762115 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34752256 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38447973 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38880037 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+14 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Amlodipine

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

