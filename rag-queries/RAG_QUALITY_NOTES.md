# RAG Quality Notes — for the RAG Agent

> Submitted by: DQF orchestrator (2026-07-31) — evidence back-fill task (P4 Task 1), updated after the all-88-drug run
> Basis: 704 live queries (88 drugs × 8 angles; furosemide +2 extra angles) against `balade-pubmed-rag-bot.hf.space/search?q=...&k=3`, 2118 results (706 files) measured in full; plus prior pipeline history (TICKET-001/002/003).

## 1. Critical: response text is hard-truncated at exactly 512 chars — this is the #1 blocker

- The endpoint's `text` field (title + abstract) is hard-capped at **exactly 512 characters** — not "~512". Measured across the full all-88 pool: **1716 of 2118 results (81.0%) sit at exactly 512**, max observed = 512, and **1649 (77.8%) end mid-sentence** (no terminal punctuation). Earlier "513" note was a one-off counting artifact; the cap is exactly 512.
- **Impact**: 81.6% of all results (1728/2118, ≥500 chars) are cut before the abstract's quantitative payload. No NNT, BP reduction, A1c change, or onset value survives intact in any back-fill snippet → L4 adjudication could not update a single value across all 88 drugs, even where drug-relevant RCTs were returned (e.g. acarbose HbA1c evidence cut at "...reduces blood pressur", terazosin PMID:2872809 cut at "After a two-week placebo lead-in period, e").
- **Ask**: return full abstracts (or a much larger cap, e.g. 3000+ chars), or expose an option to fetch full text/abstract by PMID. The framework's own `extract_l3.py` compounds this with a further `text[:300]` truncation (phantom-field root cause); both should go away.

## 2. Drug-name blindness: retriever embeds concepts, not drug names

- Even with drug-name-first queries, pools fill with same-class drugs: DPP-4 queries returned evogliptin/trelagliptin, GLP-1 queries returned semaglutide/tirzepatide, off-drug rate ~40-60%.
- **Ask**: embed the drug name explicitly (e.g. prepend "{drug}" as a hard token), or add a post-retrieval exact-name filter (title OR ≥2 mentions — the framework already does this client-side as a patch; a server-side fix would remove the need).
- Expected gain: pool self-relevance would jump from the pre-fix mean 46% toward the 80% level the EUtils-anchored refetch achieves.

## 3. Confusable drug names cause toxic off-drug returns (methyldopa case)

- Methyldopa queries returned MDMA, methylphenidate, and methylone content; only 4 of 24 snippets referenced actual methyldopa (pregnancy, absorption PK, PBPK model — none quantitative). Framework pool relevance for methyldopa: 26.9% even post-fix.
- **Ask**: exact-token matching / synonym list for drug names (methyldopa vs methyl-dopa vs α-methyldopa), and a negative filter for confusable tokens (methylphenidate, methylone, MDMA) when the query drug is methyldopa.

## 4. "Still loading" cold starts silently shrink pools

- History shows many ~200 B raw files that are exactly `{"error": "Still loading"}`; these count as source hits but contribute zero snippets.
- **Ask**: server-side warm-up / retry, or return a proper 503 so clients can retry with backoff. Clients should retry ≥2× on this error (the back-fill run retried with 5 s backoff; endpoint was warm so 0 failures observed, but the failure mode is real).

## 5. Schema/documentation drift in the response

- Actual response object: `{id, text, score, doi, journal, year, rerank_score, evidence}` (no `title`/`metadata` fields; title is first line of `text`).
- Documented elsewhere: `{id, text, title, rerank_score, metadata: {...}}`. Stale docs caused a wasted validation pass in the back-fill.
- **Ask**: keep API docs in sync (or add `title` + `metadata.mesh_terms` — both were expected by consumers).

## 6. Scoring is heuristic, not value extraction

- Keyword-count scoring saturates (e.g. all PPIs `ddi_risk=3`); CYP2C19 percentages parse via one narrow regex. NNT / effect sizes are never extracted as numbers.
- Measured on the full pool: `score` sits in a very narrow band **0.317–0.538 (median 0.404)** — almost no discriminative range; `rerank_score` spans **-9.41 to +8.24 (median 1.888)** and can be **negative**, so any consumer must not assume positive/ranked semantics.
- **Ask**: return structured numeric extractions (value + unit + confidence) or at least larger text so consumers can extract values themselves.

## 7. Storage sprawl

- Raw results duplicated across `l3_output/`, legacy `raw/`, `l3_output_backup_pre_eutils/`; digests live in `%TEMP%` (volatile); 26 drugs have no L2b digest.
- **Ask**: single canonical store with a `source` tag (rag/eutils/refetch) per record, so evidence provenance is unambiguous.

## 8. Relevance gate may drop legitimate evidence

- Client gate requires drug name in title OR ≥2 mentions; this excludes single-mention comparison/head-to-head RCTs. TICKET-003 flagged this.
- **Ask**: "title-only OR co-mention-in-abstract" rule would preserve RCTs where the drug appears once alongside the comparator.

## 9. Angle C (EUtils) is the reliable fallback — promote it

- EUtils `({drug}[tiab] OR {drug}[nm]) AND (concept...)` is drug-anchored by construction and delivered the only measurable relevance improvement seen in the framework (TICKET-002: 48% → 80% mean). The back-fill verified the path works (esearch→5 PMIDs→efetch→full abstracts, 0.35 s throttle at 3 req/s no-key).
- **Ask**: if full-abstract retrieval (item 1) is not feasible, at minimum expose the EUtils path as a first-class query mode rather than a fallback.

## 10. NEW: cross-angle PMID duplication — pool diversity is lower than file count suggests

- Measured on the full pool: **1530 distinct PMIDs from 2118 results** → **588 results (27.8%) are duplicate PMIDs** appearing in more than one file; **275 PMIDs appear in >1 file**.
- Worst offenders: **PMID:40802044 appears in 28 files**, PMID:38876401 in 18, PMID:41562647 in 16, PMID:38344757 in 13, PMID:40817763 in 12 — the same paper re-returned across many drug/angle queries.
- **Impact**: the 8 angles are not independent retrievals; a single highly-ranked paper can dominate several angles for a drug, so effective evidence diversity per drug is less than 8×3=24 slots. Any pooling that counts files will overcount real evidence.
- **Ask**: de-duplicate by PMID at the server (or expose `id` filter params), and/or report per-query novelty (new PMIDs vs already-seen). Clients should de-dupe by PMID before adjudication.

## Outcome of this back-fill

- **88/88 drugs backfilled** (706 query files, 2118 results, 0 empty result arrays, 0 HTTP errors on a warm endpoint; resumable runner `rag-queries/backfill_all_queries.py` with skip-if-exists semantics, canonical 9-class version).
- Evidence integrity: 706/706 JSON valid; all results carry `id` (PMID), `text`, `score`, `rerank_score`, and a non-empty `evidence` dict.
- Adjudication result: **0 L4 value changes across all 88 drugs** — current class-anchored values retained as "insufficient evidence", not "confirmed". The truncated-abstract blocker (item 1) is the single fix that would unlock a real back-fill; item 10 (dedup) is the second.
