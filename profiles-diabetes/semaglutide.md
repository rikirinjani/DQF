# Semaglutide — 4-Level Quantitative Profile

> **Role in PoC:** GLP-1 receptor agonist; glucose-dependent insulin secretion, delayed gastric emptying, satiety. Class: Diabetes.
> **Label note:** Once-weekly dosing; SUSTAIN-6 showed 26% CV risk reduction

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **GLP-1 receptor** | 9.5 -log10 EC50 |

**Selectivity:** GLP-1R >>> glucagon receptor

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 89% |
| **Half-life** | 168.0 h |
| **Volume of distribution** | 8.0 L/kg |
| **Metabolism** | Proteolysis (peptide backbone degraded to amino acids) |
| **Renal excretion** | 3% |
| **Special** | Once-weekly dosing; SUSTAIN-6 showed 26% CV risk reduction |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **ddi_risk** | 1 | risk | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 2 | risk | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 22 PMIDs, relevance gate pass) |
| **weight_effect** | 3 | direction-agnostic | batch4_rescore: 3 (applied) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; bottom score (1) on ddi_risk. Evidence pool: 22 PMIDs (relevance 43.9%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.5 % at 0.5-2.0mg SC |

### Indications

- T2DM
- Obesity (2.4mg SC)
- CV risk reduction

| Success rate (monotherapy) | 0.7 |
| Onset | days |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | safe |
| **Lactation** | unknown |
| **Pregnancy** | C |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 29766634 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32998732 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33108617 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33854484 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 33969456 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34260945 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34514682 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34881835 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 34942372 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35263432 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 35778801 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 36471818 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+10 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Semaglutide

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

