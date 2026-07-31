# Raw RAG Query Archive

Raw JSON responses from the PubMed RAG endpoint used to populate DQF profiles.
Archived **July 2026** to close limitation #9 (RAG reproducibility).

## Caveat

These are archival snapshots taken *after* the original query time. The PubMed
abstract index (27.7M abstracts, 1975–Jan 2026) and reranker state may have
shifted between the original queries (early 2026) and this archive (July 2026).
Key PMIDs from the original queries were preserved in `../README.md` and may
differ from current results.

## Format

Each `.json` file contains the endpoint response:

```json
{
  "results": [
    {
      "id": "PMID:...",
      "text": "Abstract snippet...",
      "score": 0.42
    }
  ]
}
```

`score` is the cross-encoder reranker relevance (range 0–1, `k=3` returned).

## Files

| File | Query |
|------|-------|
| ibuprofen-cox-bind.json | ibuprofen COX-1 COX-2 Ki binding affinity selectivity |
| diclofenac-cox-bind.json | diclofenac COX-1 COX-2 binding Ki potency anti-inflammatory |
| celecoxib-cox-bind.json | celecoxib COX-2 selective Ki binding affinity sulfonamide |
| paracetamol-cox.json | paracetamol acetaminophen COX mechanism COX-1 COX-2 inhibition |
| ibuprofen-asic.json | ibuprofen ASIC TRPV1 ion channel off-target mechanism |
| diclofenac-p2x3.json | diclofenac P2X3 purinergic COX-independent analgesic mechanism |
| diclofenac-trpa.json | diclofenac TRPA1 TRPV1 ion channel NSAID off-target analgesic |
| celecoxib-cv.json | celecoxib COX-2 selective cardiovascular risk safety |
| paracetamol-am404.json | paracetamol AM404 FAAH TRPV1 CB1 central analgesic pathway |
| ibuprofen-nnt.json | ibuprofen acute pain NNT number needed to treat postoperative |
| ibuprofen-oxford.json | ibuprofen NNT 200mg 400mg analgesic Oxford league |
| diclofenac-nnt.json | diclofenac 50mg NNT analgesic efficacy number needed to treat |
| nsaid-gi-nnh.json | NSAID gastrointestinal bleeding risk NNH number needed to harm |
| nsaid-pk.json | paracetamol diclofenac ibuprofen naproxen pharmacokinetics half-life bioavailability |
| celecoxib-pk.json | celecoxib pharmacokinetics half-life CYP2C9 metabolism bioavailability |
| diclofenac-sr.json | diclofenac SR sustained-release pharmacokinetics bioavailability half-life |

## Reproducibility

To reproduce: query `https://balade-pubmed-rag-bot.hf.space/search?q=<query>&k=3`
with any HTTP client. The archive script is not preserved (cleaned up after use).
