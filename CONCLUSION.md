# Drug Quantification Framework — PoC Conclusion

Right now if you compare two analgesics you get a number — NNT, NNH, effect size. That number collapses mechanism, safety, pharmacokinetics, everything into one dimension. But paracetamol and ibuprofen don't share a mechanism, don't share a risk profile, and the "right" choice depends on whether your patient is bleeding, has heart disease, or just needs a tooth pulled. You can't answer that with a single number. The framework keeps all four dimensions separate and lets the question decide the weight.

## What We Built

A 4-level drug profiling framework applied to 4 analgesics: ibuprofen, diclofenac, celecoxib, and paracetamol. Each profile covers molecular binding (L1), pharmacokinetics (L2), systems response (L3), and clinical outcomes (L4), sourced from the MedQuery PubMed RAG (27.7M abstracts, FAISS + cross-encoder) plus authoritative PK databases and Cochrane reviews.

## Did It Work?

**Yes — the 4-level structure generates insights a single score cannot.** Specifically:

| Claim | Evidence from PoC |
|-------|-------------------|
| Single scores obscure mechanism | Paracetamol NNT 3.6 "looks worse" than ibuprofen 2.5, but has zero GI/CV toxicity and a completely different mechanism (AM404 → TRPV1 + Nav1.8 + CB1) |
| L1→L3→L4 causality is traceable | Celecoxib's COX-2 selectivity (L1) → PGI2 suppression without TXA2 effect (L3) → ↑ MACE (L4). Same feature → both advantage and harm. |
| PK doesn't predict tissue effect | Diclofenac's plasma t½ = 1.2 h but dosing is BID — explained by L3 (synovial fluid accumulation) + L2 (enterohepatic recirculation) |
| Off-target effects are real and drug-specific | Diclofenac has P2X3 antagonism (unique), ibuprofen has ASIC1a inhibition (unique), paracetamol has Nav1.8/1.7 block (unique) — all invisible at L4 alone |
| No drug "wins" across all dimensions | Every drug wins on at least one dimension and loses on another. The right choice is patient-dependent. |

## Where the RAG Proved Its Value

The MedQuery RAG directly enabled L1 and L3 extraction that would otherwise require days of manual literature review:

- **L1 off-target profiles:** The ASIC1a-ibuprofen paper (PMID:28949138), the AM404-Nav1.8 PNAS paper (PMID:40465624), the celecoxib oncology review (PMID:41383482) — all came from targeted RAG queries, not from structured databases.
- **L3 mechanisms:** The paracetamol dual-site mechanism (central TRPV1 + peripheral Nav block) was synthesized from RAG-retrieved papers.
- **L4 clinical updates:** The SCOT trial biomarker paper (2024), the imrecoxib-celecoxib meta-analysis (2025), the diclofenac renal colic trial (2024) — all recent enough to not be in static databases.

**The RAG is not optional for L1/L3 — it is the primary data source.**

## Data Availability Per Level

| Level | Data Source | Readiness | RAG Role |
|-------|------------|-----------|----------|
| L1 Binding | PDSP + literature | ⚠️ PDSP weak on NSAID targets; literature mining via RAG essential | Primary for off-targets |
| L2 PK | Inxight FRDB, Lombardo, DrugBank | ✅ 70% structured; minor harmonization needed | Supplementary |
| L3 Systems | **No structured source exists** | 🔴 Must be built from literature | **Primary** — only practical path |
| L4 Clinical | Cochrane, Oxford | ✅ Strong for acute pain; chronic pain less organized | Supplementary + updates |

## Key Gaps Found

1. **L3 remains the hardest level** — no structured database for pathway activation, tissue dynamics, or off-target pharmacology consequences. Every PoC drug needed custom L3 extraction.
2. **Dose standardization is complex** — ibuprofen 200 mg vs 400 mg NNTs differ (2.7 vs 2.5). The framework must handle dose as a parameter.
3. **Condition matters** — acute postoperative pain NNT ≠ chronic OA pain. Paracetamol is first-line for OA despite worse NNT. The framework needs a condition dimension.
4. **Active metabolites need ontology** — paracetamol→AM404 is the canonical example, but sulindac and nabumetone also work this way.

## What the Next Phase Would Build

```
v1.0 (structured data layer)
├── Standardized L2 extraction from Inxight FRDB (20 NSAIDs)
├── L4 compilation from Cochrane reviews (dose-specific NNT/NNH tables)
├── RAG pipeline for L1+L3 automated extraction
└── JSON schema for 4-level profiles

v1.1 (scalable query layer)
├── 20 NSAID profiles (full class)
├── Context-aware query: "compare ibuprofen vs diclofenac for elderly OA with CV risk"
└── Interactive ranked comparison with patient factors

v2.0 (prediction layer)
├── L1+L2 → predict L3+L4 for novel drugs
├── TxGNN / Enchant integration for binding prediction
└── Missing data imputation
```

## Bottom Line

**The 4-level framework is viable.** The most distinctive contribution is the L1 off-target profile + L3 systems response — these are the levels that differentiate drugs within a class where NNT doesn't. The MedQuery RAG makes L1/L3 extraction practical at scale.

**The framework does not rank drugs. It fingerprints them.** The user asks "for this patient, with this condition, what matters?" — not "which drug is best."
