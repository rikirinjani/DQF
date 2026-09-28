# Verapamil — 4-Level Quantitative Profile

> **Role in PoC:** Non-dihydropyridine CCB; phenylalkylamine class. Class: Antihypertensive.
> **Label note:** Strong CYP3A4 inhibitor; constipation side effect; negative inotrope

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **L-type calcium channel** | 8.2 -log10 Ki |

**Selectivity:** Cardiac > vascular (rate-limiting)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 22% |
| **Half-life** | 6.0 h |
| **Volume of distribution** | 4.0 L/kg |
| **Metabolism** | Hepatic CYP3A4 (norverapamil active) |
| **Renal excretion** | 70% |
| **Special** | Strong CYP3A4 inhibitor; constipation side effect; negative inotrope |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 52 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 6 of 11 pk/pd-filtered sentences) |
| **electrolyte_risk** | 1 | risk | batch4_rescore: 1 (applied) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 52 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 52 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 52 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; bottom score (1) on electrolyte_risk; heart-rate effect: bradycardia. Evidence pool: 52 PMIDs (relevance 85.9%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-6) at 120-480mg ER |

### Indications

- Hypertension
- Stable angina
- SVT
- HOCM

| Success rate (monotherapy) | 0.55 |
| Onset | 150 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10233206 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10804447 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11174354 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11467760 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12973671 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15779502 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15961013 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1625195 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1650135 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16596036 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1678924 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19947891 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+40 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Verapamil

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

