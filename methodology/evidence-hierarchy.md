# Evidence Hierarchy

Every data point in the Drug Quantification Framework is tagged with an evidence level. This document defines how those levels are assigned.

## Why This Matters

Drug profiling requires evidence from multiple domains — binding assays, pharmacokinetic studies, clinical trials, mechanistic papers. These study types have different standards of evidence. A binding Ki from a single crystal structure is not comparable to a Cochrane meta-analysis of 10,000 patients. Our hierarchy makes the distinction explicit.

## The 4-Level System

We use a simplified GRADE-derived hierarchy adapted for multi-domain pharmacological evidence:

| Level | Label | Applies To | Definition |
|-------|-------|-----------|------------|
| **HIGH** | Strong evidence | L4 clinical outcomes, well-established L2 PK | Multiple consistent studies, meta-analyses, or widely accepted pharmacological consensus |
| **MODERATE** | Moderate evidence | L1 binding data, L3 mechanistic studies, single clinical trials | Replicated findings with some methodological heterogeneity, or single high-quality study |
| **LOW** | Limited evidence | Emerging findings, single studies, in vitro only | Single publication without replication, or data with significant methodological caveats |
| **VERY LOW** | Insufficient evidence | Case reports, unpublished data, extrapolated values | Expert opinion, indirect evidence, or data with major limitations |

## Mapping Study Types to Levels

### HIGH
- Cochrane systematic reviews with meta-analysis
- Large multicenter RCTs (n > 1000)
- Established pharmacokinetic parameters (consistent across ≥3 independent studies)
- Pharmacological consensus (IUPHAR recommendations, Goodman & Gilman textbook)

### MODERATE
- Single RCTs (n 100–1000)
- Systematic reviews without pooled analysis
- Binding data from peer-reviewed structure-activity studies
- Mechanistic studies with cellular or in vivo validation
- PK parameters from a single Phase I study but not replicated
- Population PK studies

### LOW
- Small clinical studies (n < 100)
- Single in vitro binding measurements without replication
- Case series
- Mechanistic studies with indirect evidence only
- Extrapolated data (e.g., animal data used for human predictions)

### VERY LOW
- Individual case reports
- Conference abstracts
- Unpublished data
- Expert opinion without published basis
- Computational predictions without experimental validation

## Confidence Tags

Alongside evidence level, each datum may carry a confidence qualifier if the reviewer judges the evidence level does not capture the full uncertainty:

- **Replicated** — finding confirmed by ≥2 independent groups
- **Single source** — only one publication supports this claim
- **Emerging** — finding published within last 2 years, not independently replicated
- **Assay-dependent** — value known to vary substantially by assay conditions (common for binding affinities)
- **Extrapolated** — derived from structurally similar compound or animal data

## How to Use in Profiles

Every reference table entry in a profile should include:
1. **PMID** (or DOI) — traceable identifier
2. **Evidence level** — HIGH / MODERATE / LOW / VERY LOW
3. **Confidence qualifier** — optional, only when the evidence level alone is insufficient

### Example

| PMID | Title | Evidence Level | Confidence |
|------|-------|----------------|------------|
| 28949138 | ASIC1a Allosteric Inhibition by Ibuprofen | MODERATE | Single source |
| 38180091 | Ibuprofen Postoperative Pain Children (Cochrane) | HIGH | Replicated |

## Relationship to GRADE and Oxford CEBM

This framework is a simplified adaptation. Our levels correspond roughly to:

| DQF Level | Oxford CEBM (Therapy) | GRADE |
|-----------|----------------------|-------|
| HIGH | 1a–1b | High |
| MODERATE | 2a–2b | Moderate |
| LOW | 3–4 | Low |
| VERY LOW | 5 | Very Low |

We deviate from GRADE where appropriate for pharmacological data: binding affinities from well-executed SAR studies are rated MODERATE (not LOW, as GRADE would rate non-randomized evidence) because they reflect direct physical measurements with established reproducibility.

## Limitations of This System

- Evidence levels for L1 binding data can be misleading — a single high-quality SPR measurement may be more reliable than a meta-analysis of low-quality clinical data, yet the latter receives a higher level rating. The confidence qualifiers partially address this.
- "Established textbook knowledge" may lack a specific PMID and is therefore difficult to grade. We cite secondary sources (reviews, textbooks) in such cases.
- Emerging findings from 2025–2026 are tagged with "Emerging" confidence qualifier and should be treated as provisional.
