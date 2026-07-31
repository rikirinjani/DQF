# Limitations — Drug Quantification Framework

This document states the known limitations of the framework and the current PoC. These should be read as inherent constraints, not deficiencies to be fixed in a future version — some are structural, some are scoping choices.

## 1. Domain Restriction

The PoC covers one drug class (NSAIDs/analgesics) with four drugs. This is a methods validation, not a dataset release. Generalizability to other drug classes (antibiotics, antihypertensives, psychotropics) is untested. The framework ontology is class-agnostic by design, but each class may require level-specific adaptations (e.g., MIC for antibiotics substitutes for NNT).

## 2. Selection Bias

All four PoC drugs are among the most-studied compounds in pharmacology (thousands of publications each). The framework's viability for drugs with sparse literature, limited clinical data, or no PK studies is unproven. Drugs with incomplete profiles will have "No data" entries at one or more levels.

## 3. L3 Is the Weakest Level

Systems response (L3) has no single structured database equivalent to PDSP (L1) or DrugBank (L2). It is populated primarily through literature mining. This means:
- L3 entries reflect what has been studied, not what is true
- Publication bias inflates L3 data for well-studied drugs
- Two researchers independently profiling the same drug may produce different L3 profiles
- L3 is the most labor-intensive level to populate per drug

## 4. Binding Affinity Variability

Ki values reported in L1 tables are drawn from published sources but vary by assay conditions (temperature, buffer, radioligand, species, membrane preparation). Two labs measuring the same drug-target pair can report values differing by 10×. We report the most commonly cited value or range, but the precision implied by a single number is misleading.

## 5. Evidence Hierarchy Limitations

Our evidence hierarchy (HIGH/MODERATE/LOW/VERY LOW) is a GRADE-adapted system designed for pharmacological data. It has two structural weaknesses:

- A single high-quality binding measurement (MODERATE) may be more reliable than a poor meta-analysis (HIGH) — the level reflects study design, not necessarily confidence
- "Established textbook knowledge" (e.g., "ibuprofen is a reversible COX inhibitor") lacks a specific PMID and is difficult to grade

## 6. Levels Are Not Independent

L1→L3→L4 forms a causal chain. Representing them as separate dimensions double-counts information. For example, celecoxib's COX-2 selectivity appears at L1 (binding ratio), L3 (PGI2/TXA2 balance), and L4 (GI/CV outcomes). We preserve this because the causal path is the insight — but readers should not treat the four levels as orthogonal measurements.

## 7. Recency of Evidence

Several mechanisic findings cited (PNAS 2025, J Med Chem 2026, Front Pharmacol 2025) are very recent and lack independent replication. We tag these with "Emerging" confidence qualifier, but the possibility that some may not replicate is real.

## 8. No Clinical Validation

The framework claims improved drug comparison for clinical decision-making, but this has not been tested. No user study, no comparison to unaided clinician judgment, no clinical vignette validation has been performed. Claims about clinical utility are conceptual.

## 9. Reproducibility

The RAG endpoint is a third-party service. Raw query outputs are archived (rag-queries/raw/) but the retrieval system may change or become unavailable. A local RAG pipeline would be needed for production-grade reproducibility.

## 10. Dose and Condition Dependence

Clinical outcomes vary by dose and condition. The framework reports dose-specific NNTs where evidence exists, but many entries reflect single-dose comparisons that may not translate to chronic use. The "best choice" for a patient depends on factors the framework does not capture: individual genetics, comorbidities, concomitant medications, patient preference, and cost.

## 11. The Framework Does Not Rank

The framework profiles. It does not produce a ranked output, a composite score, or a "best drug" recommendation. Rankings require context-specific weights that only a user can supply. This is a design choice — but readers expecting a single answer will be disappointed.
