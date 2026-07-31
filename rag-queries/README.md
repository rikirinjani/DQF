# RAG Query Evidence Trail

Raw PubMed RAG (MedQuery) query outputs used to compile the 4-level drug profiles.

## Query Log

All queries against `https://balade-pubmed-rag-bot.hf.space/search?q=...&k=3`
Backend: FAISS IVF-PQ (bge-small-en-v1.5) + cross-encoder rerank (MiniLM-L-6)
Index: 27.7M PubMed abstracts (1975–Jan 2026)

### L1 — Binding Queries
- `ibuprofen COX-1 COX-2 Ki binding affinity selectivity`
- `diclofenac COX-1 COX-2 binding Ki potency anti-inflammatory`
- `celecoxib COX-2 selective Ki binding affinity sulfonamide`
- `paracetamol acetaminophen COX mechanism COX-1 COX-2 inhibition`

### L3 — Mechanism / Off-Target Queries
- `ibuprofen ASIC TRPV1 ion channel off-target mechanism`
- `diclofenac P2X3 purinergic COX-independent analgesic mechanism`
- `diclofenac TRPA1 TRPV1 ion channel NSAID off-target analgesic`
- `celecoxib COX-2 selective cardiovascular risk safety`
- `paracetamol AM404 FAAH TRPV1 CB1 central analgesic pathway`

### L4 — Clinical Outcome Queries
- `ibuprofen acute pain NNT number needed to treat postoperative`
- `ibuprofen NNT 200mg 400mg analgesic Oxford league`
- `diclofenac 50mg NNT analgesic efficacy number needed to treat`
- `NSAID gastrointestinal bleeding risk NNH number needed to harm`
- `paracetamol diclofenac ibuprofen naproxen pharmacokinetics half-life bioavailability`

### L2 — PK Queries
- `celecoxib pharmacokinetics half-life CYP2C9 metabolism bioavailability`
- `diclofenac SR sustained-release pharmacokinetics bioavailability half-life`

## Raw Output Storage

Query outputs were processed inline. Key PMIDs extracted:

| PMID | Source Query |
|------|-------------|
| 28949138 | ibuprofen ASIC TRPV1 |
| 38180091 | ibuprofen NNT postoperative |
| 39677212 | ibuprofen acute pain NNT |
| 41338520 | ibuprofen OAT interaction |
| 41465841 | diclofenac COX binding |
| 41556714 | diclofenac COX-1 role |
| 40716177 | diclofenac quinazoline |
| 39763427 | diclofenac renal colic |
| 39660078 | celecoxib CV SCOT trial |
| 41560736 | celecoxib imrecoxib meta |
| 40028763 | celecoxib AS cohort |
| 41383482 | celecoxib oncology |
| 40465624 | paracetamol AM404 Nav1.8 (PNAS 2025) |
| 40402381 | paracetamol pathways |
| 40967389 | Nav1.8 TRPV1 targets |
| 38653785 | paracetamol ibuprofen combination |
