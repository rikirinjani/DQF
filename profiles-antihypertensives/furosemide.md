# Furosemide — 4-Level Quantitative Profile

> **Role in PoC:** Loop diuretic; blocks Na⁺-K⁺-2Cl⁻ cotransporter in TALH. Class: Antihypertensive. L3 values updated by the N1 batch-5 rescore (2026-09-28).
> **Label note:** Short t½; natriuretic effect outlasts serum levels; ototoxic at high doses

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **NKCC2** | 6.8 -log10 Ki |

**Selectivity:** NKCC2 > NKCC1

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 60% |
| **Half-life** | 2.0 h |
| **Volume of distribution** | 0.15 L/kg |
| **Metabolism** | Minimal hepatic glucuronidation |
| **Renal excretion** | 65% |
| **Special** | Short t½; natriuretic effect outlasts serum levels; ototoxic at high doses |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION` (note: `bp_reduction` is absent from DIM_DIRECTION; benefit by semantics). Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **bp_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 8 of 12 pk/pd-filtered sentences) |
| **electrolyte_risk** | 3 | risk | N1 batch-5 rescore 2026-09-28 (applied 2→3): urinary spot sodium and urine output measured at baseline, 2, and 6 h after 40 mg iv (PMID 41569687); strong:5 - loop diuretic electrolyte loss |
| **heart_rate_effect** | tachycardia | direction-agnostic (string-typed) | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |
| **metabolic_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |
| **renal_protection** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 21 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on bp_reduction, renal_protection; highest risk (3) on electrolyte_risk; heart-rate effect: tachycardia. Evidence pool: 21 PMIDs (relevance 42.4%, gate pass).

---

## L4 — Clinical Outcomes

### Blood-Pressure Control

| Outcome | Value |
|--------|-------|
| **NNT for BP control** | 5 (95% CI 3-9) at 20-80mg |

### Indications

- Hypertension
- Edema (CHF/CKD)
- Nephrotic syndrome

| Success rate (monotherapy) | 0.4 |
| Onset | 60 min |

---

## Special-Population Safety

Not sourced (no safety fields in the drugs.json record).

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10047639 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 12620696 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15222723 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 18067045 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33356004 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34121726 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37214156 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38485054 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38683125 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39352583 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39472392 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 39620306 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+9 more PMIDs in the evidence pool)* | |
| batch5_rescore_adjudication.json | N1-applied L3 cells (2026-09-28) |

---

## Framework Takeaways for Furosemide

1. **N1 rescore (2→3 on electrolyte_risk):** urinary spot sodium and urine output measured at baseline, 2, and 6 h after 40 mg iv (PMID 41569687); strong:5 - loop diuretic electrolyte loss

