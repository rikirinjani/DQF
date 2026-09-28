# Lovastatin — 4-Level Quantitative Profile

> **Role in PoC:** Lactone prodrug -> active beta-hydroxyacid; competitive HMG-CoA reductase inhibitor. Class: Statin. The data-poor statin: 3 L3 and 3 L2 fields not sourced.

---

## L1 — Molecular Binding

| Target | Potency |
|--------|---------|
| **HMGCR (prodrug)** | 7.0 -log10 IC50 |

**Selectivity:** Hepatic; lipophilic (lactone prodrug, like simvastatin)

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 5% |
| **Half-life** | null (not sourced) |
| **Volume of distribution** | null (not sourced) |
| **Metabolism** | CYP3A4 (intestinal + hepatic; prodrug activation + clearance) |
| **Renal excretion** | null (not sourced) |
| **Special** | Low oral F (<5%, poor solubility + extensive CYP3A4 metabolism); strong DDI surface (P-gp inhibitor + CYP3A4 substrate: diltiazem raises AUC ~3.6x) |

## L3 — Systems Response

Scale: each dimension 1-3; higher = more of the named quantity. Directions per `classifier_audit.DIM_DIRECTION`. Scores are the current `api/drugs.json` values; basis cites the governing adjudication record where one exists.

| Dimension | Score | Direction | Basis |
|-----------|-------|-----------|-------|
| **anti_inflammatory** | null (not sourced) | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 20 PMIDs, relevance gate pass) |
| **ddi_risk** | 3 | risk | auto-extracted; ddi_rescore proposed 2 (not applied) |
| **hmgcr_inhibition** | null (not sourced) | benefit | auto-extracted by the L3 pipeline (evidence pool 20 PMIDs, relevance gate pass) |
| **lipophilicity** | null (not sourced) | direction-agnostic | auto-extracted by the L3 pipeline (evidence pool 20 PMIDs, relevance gate pass) |
| **myopathy_risk** | 3 | risk | auto-extracted by the L3 pipeline (evidence pool 20 PMIDs, relevance gate pass) |

**Record note:** 6th major statin (per methodology/second-class-proposal.md); first drug curated via LanceDB RAG index + NCBI EUtils with PMID provenance

**pleiotropic_effects:** Anti-Inflammatory, Antioxidant, Endothelial, Immunomodulatory, Smooth Muscle, Thrombosis, Vascular

**L3 Signature:** highest risk (3) on myopathy_risk, ddi_risk. Evidence pool: 20 PMIDs (relevance 76.0%, gate pass).

---

## L4 — Clinical Outcomes

### Lipid + Safety Outcomes

| Outcome | Value |
|--------|-------|
| **LDL reduction at 1 yr** | 22% (PMID 8615705 (n=612 RCT)) |
| **Myopathy** | Extremely low risk (PMID 15820170) |

### Indications

- Primary hypercholesterolemia

| Success rate (monotherapy) | null (not sourced) |
| Onset | null (not sourced) |

---

## Special-Population Safety

| Population | Rating |
|------------|--------|
| **Hepatic** | null (not sourced) |
| **Lactation** | null (not sourced) |
| **Pregnancy** | null (not sourced) |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 12434405 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15660968 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 15871634 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 16484515 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1673788 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 1894526 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2159099 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 21833028 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 2565206 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 26773364 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 27602089 | evidence-pool finding (see `_evidence` in drugs.json) |
| PMID 30054755 | evidence-pool finding (see `_evidence` in drugs.json) |
| *(+8 more PMIDs in the evidence pool)* | |

---

## Framework Takeaways for Lovastatin

1. **Unapplied adjudication proposal:** lovastatin|ddi_risk: ddi_rescore proposed 2, drugs.json has 3 — the current value is the L3-pipeline value; the prior rescore's proposal is recorded but not reflected.
2. **Data-poor record:** 3 L3 fields (hmgcr_inhibition, lipophilicity, anti_inflammatory) and 3 L2 fields (half-life, Vd, renal excretion) are null; `l4_clinical.nnt_mace_5yr` is missing, which makes the Statin class query crash server-side (`_compute_efficacy` KeyError) — lovastatin is unrankable by DQF until that field is sourced.

