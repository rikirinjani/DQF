# Diltiazem — 4-Level Quantitative Profile

> **Role in PoC:** Non-dihydropyridine CCB; benzothiazepine class. Class: Antihypertensive. L3 values updated by the N1 batch-5 rescore (2026-09-28).
> **Label note:** Negative chronotrope; AV nodal blockade; contraindicated with HFrEF

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **L-type calcium channel** | 7.8 -log10 Ki |

**Selectivity:** Cardiac > vascular (rate-limiting)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 40% |
| **Half-life** | 5.0 h |
| **Volume of distribution** | 3.0 L/kg |
| **Metabolism** | Hepatic CYP3A4 (desacetyl metabolite active) |
| **Renal excretion** | 65% |
| **Special** | Negative chronotrope; AV nodal blockade; contraindicated with HFrEF |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 49 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | ddi_rescore: 3 (applied; kept 4 of 13 pk/pd-filtered sentences) |
| **electrolyte_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 49 PMIDs, relevance gate pass) |
| **heart_rate_effect** | bradycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 49 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 49 PMIDs, relevance gate pass) |
| **renal_protection** | 3 | benefit | N1 batch-5 rescore 2026-09-28 (applied 2→3): IV infusion of diltiazem improves renal function (PMID 36354148); strong:3 |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on ddi_risk; heart-rate effect: bradycardia. Evidence pool: 49 PMIDs (relevance 86.8%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 3 (95% CI 2-6) at 120-360mg ER |

### Indications

- Hypertension
- Stable angina
- Rate control (AF/AFL)

| Success rate (monotherapy) | 0.55 |
| Onset | 150 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10226758 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10716041 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 10741630 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11195610 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11372598 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 11684211 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12220021 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12555384 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12973671 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15850765 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1590448 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1706010 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+37 more PMIDs in the evidence pool)* | |
| batch5_rescore_adjudication.json | N1-applied L3 cells (2026-09-28) |

---

## Framework Takeaways for Diltiazem

1. **N1 rescore (2→3 on renal_protection):** IV infusion of diltiazem improves renal function (PMID 36354148); strong:3

