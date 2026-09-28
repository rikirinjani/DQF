# Metformin — 4-Level Quantitative Profile

> **Role in PoC:** AMPK activation via mitochondrial complex I inhibition; decreases hepatic gluconeogenesis. Class: Diabetes.
> **Label note:** Contraindicated if eGFR <30; lactic acidosis risk with renal impairment

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **AMPK** | 5.8 -log10 Ki |
| **mitochondrial complex I** | 4.2 -log10 IC50 |

**Selectivity:** Broad pleiotropic

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 55% |
| **Half-life** | 6.0 h |
| **Volume of distribution** | 1.0 L/kg |
| **Metabolism** | Not metabolized (eliminated unchanged in urine) |
| **Renal excretion** | 90% |
| **Special** | Contraindicated if eGFR <30; lactic acidosis risk with renal impairment |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **a1c_reduction** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **cv_outcome_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **ddi_risk** | 2 | risk | ddi_rescore: 2 (applied; kept 1 of 2 pk/pd-filtered sentences) |
| **gi_tolerability** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **hypoglycemia_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **renal_benefit** | 3 | benefit | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |
| **weight_effect** | 2 | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 32 PMIDs, relevance gate pass) |

**L3 Signature:** top score (3) on a1c_reduction, cv_outcome_benefit, renal_benefit, gi_tolerability; highest risk (3) on hypoglycemia_risk. Evidence pool: 32 PMIDs (relevance 55.6%, gate pass).

---

## L4 — Clinical Outcomes

### Glycemic Efficacy

> Record note: the drugs.json entry stores HbA1c data under the key `nnt_bp_control` — a schema quirk (the field name predates the diabetes class); the values below are the HbA1c fields it holds.

| Outcome | Value |
|--------|-------|
| **HbA1c reduction** | 1.5 % at 2000mg |

### Indications

- T2DM
- Prediabetes
- PCOS
- GDM

| Success rate (monotherapy) | 0.65 |
| Onset | days |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | caution |
| **Lactation** | safe |
| **Pregnancy** | B |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 10759019 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 19096023 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 23141431 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27052588 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 28116648 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32495867 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 32905164 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 37051071 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38251680 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38466134 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38837240 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 38863255 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+20 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Metformin

1. No adjudication corrections or nulls recorded; the profile reflects the L3-pipeline extraction as merged.

