# Search Protocol — RAG Query Methodology

## Overview

Profile data was collected through two parallel pipelines: structured database queries (L2, L4) and literature mining via a PubMed RAG system (L1 off-target, L3 mechanisms, L4 updates). This document describes the RAG search protocol for reproducibility.

## RAG System

- **Endpoint:** `https://balade-pubmed-rag-bot.hf.space/search?q={query}&k=3`
- **Index:** 27.7 million PubMed abstracts (1975–January 2026)
- **Embedding:** bge-small-en-v1.5 (FAISS IVF-PQ)
- **Reranker:** cross-encoder MiniLM-L-6
- **Top-k retrieved:** 3 per query

This is a third-party hosted service. As of publication, the index is frozen at January 2026. Future index updates may produce different results.

## Query Construction

### Principles

1. **L1 (binding):** Structured queries using `{drug} {target} {mechanism}` format. Example: `ibuprofen ASIC TRPV1 ion channel off-target mechanism`
2. **L3 (systems):** Open-ended queries targeting mechanistic pathways. Example: `diclofenac P2X3 purinergic COX-independent analgesic mechanism`
3. **L4 (clinical):** Outcome-focused queries using standard terminology. Example: `ibuprofen NNT number needed to treat postoperative`

### Query Log

All queries are archived in `rag-queries/README.md` with the PMIDs extracted. Raw JSON outputs are stored in `rag-queries/raw/`.

### Inclusion Criteria

Results were included if they:
- Are indexed in PubMed with an available PMID
- Present original data, systematic review, or meta-analysis relevant to the query
- Published in a peer-reviewed journal (preprints excluded unless explicitly noted)

### Exclusion Criteria

Results were excluded if they:
- Are conference abstracts only (no full paper)
- Present in silico predictions without experimental validation
- Are retracted publications
- Discuss the drug in a context unrelated to the profiled dimension (e.g., a binding paper used as "context" without direct evidence — see [ibr:l3:rag:1])

### Citation Extraction

From each RAG result, we extract:
- PMID
- Key quantitative data (Ki, NNT, half-life, etc.)
- Relevant qualitative findings (mechanism descriptions, pathway involvement)
- Evidence level assignment per `evidence-hierarchy.md`

Non-RAG sources (DrugBank, Inxight FRDB, Cochrane reviews accessed directly, UK Medicines Compendium) are cited separately in each profile's reference table.

## Limitations

- RAG retrieval is limited to abstracts — full-text access may reveal additional data not captured in the index
- k=3 per query means potentially relevant papers may be missed; queries were iterated when initial results were insufficient
- The RAG index ends January 2026 — papers published after this date are not captured
- Binding affinity values from literature may vary by assay conditions; we report the most commonly cited value and note variability where known
