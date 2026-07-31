# Drug Quantification Framework — Proof of Concept

A multi-dimensional drug comparison framework profiling drugs across **4 levels**: molecular binding, pharmacokinetics, systems response, and clinical outcomes. Multi-axis fingerprints, not a single score.

---

## Project Overview

**Drug Quantification Framework (DQF)** profiles therapeutic agents through a standardized 4-level schema. Each drug gets a structured, evidence-graded profile spanning molecular to clinical data. This PoC covers **2 drug classes** (NSAIDs + Statins) with **9 drugs** total.

| Layer | Focus | Primary Source |
|-------|-------|---------------|
| **L1 — Molecular Binding** | Ki/Kd at all known targets | PDSP Ki + literature |
| **L2 — Pharmacokinetics** | Bioavailability, half-life, Vd, metabolism | Inxight FRDB, Lombardo 2018 |
| **L3 — Systems Response** | Pathway activation, tissue penetration | PubMed RAG extraction |
| **L4 — Clinical Outcomes** | NNT/NNH, effect sizes per indication | Cochrane reviews, Oxford League Table |

---

## Drug Classes

### NSAIDs — 4 drugs, 5 PDF iterations

| Drug | Profile | Size |
|------|---------|------|
| Ibuprofen | `profiles/ibuprofen.md` | 8 KB |
| Diclofenac | `profiles/diclofenac.md` | 8 KB |
| Celecoxib | `profiles/celecoxib.md` | 8 KB |
| Paracetamol | `profiles/paracetamol.md` | 10 KB |

Output PDFs (root):
| File | Size |
|------|------|
| `DQF_PoC_NSAID_v2.pdf` | 991 KB |
| `DQF_PoC_NSAID_v3.pdf` | 994 KB |
| `DQF_PoC_NSAID_v4.pdf` | 994 KB |
| `DQF_PoC_NSAID_v5.pdf` | 996 KB |

### Statins — 5 drugs, 6 files

| Drug | Profile | Size |
|------|---------|------|
| Atorvastatin | `profiles-statins/atorvastatin.md` | 10 KB |
| Rosuvastatin | `profiles-statins/rosuvastatin.md` | 11 KB |
| Simvastatin | `profiles-statins/simvastatin.md` | 11 KB |
| Pravastatin | `profiles-statins/pravastatin.md` | 12 KB |
| Pitavastatin | `profiles-statins/pitavastatin.md` | 11 KB |
| Comparison | `profiles-statins/comparison.md` | 13 KB |

Output PDF:
| File | Size |
|------|------|
| `DQF_PoC_Statin_v1-statin.pdf` | 218 KB |

### Cross-Class Comparison

| File | Size | Description |
|------|------|-------------|
| `cross-class-comparison.md` | 15 KB | NSAIDs vs Statins — framework analysis across all 4 levels |

---

## Build Scripts

| File | Size | Description |
|------|------|-------------|
| `build_pdf_fpdf.py` | 35 KB | NSAID PDF builder (fpdf2) |
| `build_pdf_fpdf_statins.py` | 43 KB | Statin PDF builder |
| `build_pdf.py` | 23 KB | Original weasyprint-based builder |
| `debug_l3.py` | 1 KB | L3 page positioning debug helper |

---

## Methodology — 6 files

| File | Size | Description |
|------|------|-------------|
| `methodology/framework-ontology.md` | 6 KB | Framework design, schema definitions, multi-dimensional fingerprint rationale |
| `methodology/evidence-hierarchy.md` | 5 KB | Evidence grading criteria, GRADE/Oxford CEBM adaptation |
| `methodology/search-protocol.md` | 3 KB | PubMed RAG search strategy per drug per layer |
| `methodology/validation-protocol.md` | 5 KB | Holdout validation design, confidence metrics |
| `methodology/limitations.md` | 4 KB | Framework boundaries, known gaps, caveats |
| `methodology/second-class-proposal.md` | 10 KB | Proposal for second-class drug coverage extension |

---

## Validation — 2 files

| File | Size | Description |
|------|------|-------------|
| `validation/holdout-results.md` | 14 KB | NSAID holdout validation — L1 binding, L2 PK, L3 systems |
| `validation/statin-holdout-results.md` | 12 KB | Statin holdout validation — independent class verification |

---

## RAG Evidence — 17 raw query outputs

Directory: `rag-queries/raw/` — raw PubMed RAG query outputs (JSON) with README per file.

| File | Size |
|------|------|
| `ibuprofen-cox-bind.json` | 3 KB |
| `ibuprofen-asic.json` | 3 KB |
| `ibuprofen-nnt.json` | 3 KB |
| `ibuprofen-oxford.json` | 3 KB |
| `diclofenac-cox-bind.json` | 3 KB |
| `diclofenac-p2x3.json` | 3 KB |
| `diclofenac-trpa.json` | 3 KB |
| `diclofenac-sr.json` | 3 KB |
| `diclofenac-nnt.json` | 3 KB |
| `celecoxib-cox-bind.json` | 3 KB |
| `celecoxib-pk.json` | 2 KB |
| `celecoxib-cv.json` | 3 KB |
| `paracetamol-cox.json` | 3 KB |
| `paracetamol-am404.json` | 3 KB |
| `nsaid-pk.json` | 3 KB |
| `nsaid-gi-nnh.json` | 3 KB |
| `rag-queries/README.md` | 2 KB |
| `rag-queries/raw/README.md` | 2 KB |

---

## Key Comparisons & Conclusions

| File | Size | Description |
|------|------|-------------|
| `comparison.md` | 8 KB | Cross-NSAID comparison — all 4 drugs, all 4 levels, side-by-side |
| `cross-class-comparison.md` | 15 KB | NSAIDs vs Statins — framework generalization analysis (215 lines) |
| `CONCLUSION.md` | 5 KB | PoC wrap-up — what worked, what didn't, lessons learned |

---

## Figures — 6 assets

| File | Size | Description |
|------|------|-------------|
| `figures/figure1_architecture.py` / `.png` | 3 KB / 214 KB | Framework architecture diagram |
| `figures/figure2_binding_heatmap.py` / `.png` | 3 KB / 177 KB | L1 binding affinity heatmap |
| `figures/figure3_pk_comparison.py` / `.png` | 2 KB / 119 KB | L2 PK parameter comparison |
| `figures/figure4_nnt_forest.py` / `.png` | 3 KB / 163 KB | L4 NNT forest plot |
| `figures/figure5_systems_heatmap.py` / `.png` | 4 KB / 202 KB | L3 systems response heatmap |
| `figures/figure6_pk_disconnect.py` / `.png` | 2 KB / 110 KB | PK-clinical disconnect visualization |

---

## Quick Reference

```
drug-quantification-framework/
├── profiles/               # 4 NSAID profiles
├── profiles-statins/       # 5 statin profiles + comparison
├── methodology/            # 6 files: ontology, evidence, search, validation, limits, proposals
├── validation/             # 2 holdout validation reports
├── rag-queries/            # 17 RAG evidence files + READMEs
├── figures/                # 6 publication figures (.py + .png)
├── DQF_PoC_NSAID_v2-5.pdf  # NSAID PDF builds (991–996 KB)
├── DQF_PoC_Statin_v1.pdf   # Statin PDF build (218 KB)
├── build_pdf_fpdf.py       # NSAID PDF builder
├── build_pdf_fpdf_statins.py # Statin PDF builder
├── comparison.md           # Cross-NSAID comparison
├── cross-class-comparison.md # NSAIDs vs Statins
└── CONCLUSION.md           # PoC wrap-up
```

---

*Generated July 2026. Built on MedQuery PubMed RAG (27.7M abstracts, FAISS IVF-PQ + cross-encoder reranker). 2 drug classes • 9 drugs • 4 levels • 6 methodology docs • 17 RAG evidence queries.*
