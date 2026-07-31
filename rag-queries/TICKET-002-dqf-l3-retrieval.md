# TICKET #2 (2026-07-31) — DQF L3: retrieval still failing for 30/61 drugs + HCTZ renal query returns no renoprotection evidence

**From:** DQF audit (orchestrator) **To:** RAG agent **Status:** OPEN

Push-back on Ticket #1 fixes. Ticket #1 result verified WORKING (partial) — see below — but two query-side problems remain.

---

## Ticket #1 result — verified WORKING (partial)

Re-fetch of 4 drugs (glyburide, chlorthalidone, atenolol, hydrochlorothiazide) + pipeline upgrades confirmed in `extract_l3.py` (11:06):
- New reranked endpoint schema (`rerank_score`/`doi`/`journal`/`year`/`evidence`), drug-anchored queries, relevance gate (pass >=30%), `filtered_off_drug` tracking, NCBI EUtils auto-refetch when pool <30%
- glyburide relevance 0% -> 78% (39/50), chlorthalidone HR effect bradycardia->none, atenolol metabolic 3->2, HCTZ pool 24 off-drug snippets filtered
- L3 anchors 3 fail -> 1 fail; L2a 0 diffs in AHT/DM scope after re-merge

---

## Remaining failures — this ticket

### 1. hydrochlorothiazide renal_protection=3 STILL WRONG (only surviving L3 anchor failure)

Evidence pool (10 kept PMIDs) has ZERO renoprotection support for HCTZ:
- File: `rag-queries/l3_output/hydrochlorothiazide/hydrochlorothiazide_renal_protection_nephropathy_kidney_mech.json` returns:
  - PMID 38931369 "Protective Role of Rosmarinic Acid in Experimental Urolithiasis" (urolithiasis, not HCTZ)
  - PMID 39656458 "Chlorthalidone vs Hydrochlorothiazide and Kidney Outcomes" (argues AGAINST HCTZ renoprotection — chlorthalidone favored)
  - PMID 40241207 "Trimetazidine effect on kidney function" (not HCTZ)
- The renal query is not surfacing HCTZ renal-outcome literature. Heuristic then scores 3 from incidental "renal" keyword hits in unrelated abstracts (rash/sepsis case report PMID 39092405).
- **Ask:** what query/anchor would return actual HCTZ renal-protection-or-neutrality evidence? (e.g. thiazide nephrolithiasis calcium, thiazide kidney outcomes hypertension trials, ALLHAT renal outcomes)

### 2. 30/61 drugs STILL <50% self-relevance — only 4 of the worst were re-fetched

Relevance gauge re-run 11:15 (same `audit_relevance.py`): mean 48%, 30/61 <50%. Worst unchanged:
- gliclazide 3% (1/33), methyldopa 6% (2/36), terazosin 6% (2/33), ertugliflozin 12%, felodipine 12%, pramlintide 17%, alogliptin 18%, doxazosin 18%, glimepiride 18%, repaglinide 19%, hydralazine 21%, perindopril 22%, glipizide 24%, candesartan 27%, captopril 28%
- methyldopa + terazosin still share boilerplate generic hypertension PMIDs (10678283, 41224908, 2941267)
- These drugs were NOT re-fetched; their profiles still sit on garbage pools.
- **Ask:** re-fetch all <50% drugs with the new drug-anchored query templates + relevance gate (30 drugs). The pipeline now self-heals <30% pools via EUtils, but 30-50% pools pass the gate yet are still half-irrelevant — consider raising the gate or re-running extraction for these 30.

### 3. Side-effect: L4 phantom fields 11 -> 12 (glyburide ddi_risk now default-with-no-evidence)

Stricter filtering removed the junk that previously inflated ddi_risk to 2. Score is honest (1) but unproven. Acceptable — informational.

---

## Data locations

- Raw pools: `rag-queries/l3_output/<drug_id>/*.json` (new schema: `result.results[].id/text/doi/journal/year/rerank_score/evidence`)
- Profiles: `rag-queries/l3_output/<drug_id>_l3_profile.json`; merged: `api/drugs.json` (re-merged 11:17, backup `l3_output/_backups/drugs_20260731_111733.json`)
- Scorer: `rag-queries/extract_l3.py` (`_score_risk`, `extract_l3_profile`, relevance gate ~L585-592, EUtils refetch ~L998)
- Relevance gauge: `%TEMP%\opencode\audit_relevance.py` (reproducible)
- Full <50% drug list: see section 2 (30 drugs)

## Status

OPEN — Ticket #2. L2b semantic review + L4 quantification remain blocked until retrieval relevance is acceptable (target: <10 drugs <50%, or explicit acceptance of the heuristic limitation).

---

# RESPONSE — RAG agent (2026-07-31)

**Status: RESOLVED — both asks addressed; full 61-drug batch now on anchored pools.**

## Ask #1 — HCTZ renal query: ANSWERED

The fix is the drug-anchored EUtils anchor, not a new RAG query. The RAG endpoint has no renal-outcome literature for HCTZ; the anchor
`(hydrochlorothiazide[tiab] OR hydrochlorothiazide[nm]) AND (renal[tiab] OR protection[tiab] OR nephropathy[tiab] OR kidney[tiab])`
returns actual HCTZ renal literature:

- PMID 36856614 "Hydrochlorothiazide and Prevention of Kidney-Stone Recurrence" (nephrolithiasis — genuine HCTZ renal benefit)
- PMID 36595088 "Diuretics in pediatrics" (renal physiology + diuretic renal effects)
- PMID 38465625 "Potassium-Switch Signaling Pathway..." (thiazide-K+ renal axis)

Re-ran HCTZ through `--pubmed-only`: pool relevance 33% -> **85%** (23 kept PMIDs, 9 filtered), rosmarinic/trimetazidine excluded, chlorthalidone-vs-HCTZ RCT retained as genuine HCTZ renal-outcome evidence. `renal_protection` value left to the L2b semantic review — the pool now contains real HCTZ renal evidence; whether the heuristic's 3 survives review is your call (scorer tuning scope, per PARSER_SUGGESTION.md).

## Ask #2 — all 30 sub-50% drugs re-fetched: DONE

Re-ran extraction through the drug-anchored EUtils path (`--pubmed-only`) for **all 30 flagged drugs** (12 queries each, 5 results/query). Verification via `audit_relevance.py`:

- **Before:** mean 48%, 30/61 <50% (worst: gliclazide 3%, methyldopa 6%, terazosin 6%)
- **After:** mean **80%**, **0/61 <50%** (all 61 ≥50%, 22 drugs ≥90%)
- Boilerplate PMIDs gone: methyldopa/terazosin/gliclazide pools no longer contain 10678283 / 41224908 / 2941267 (34/26/28 unique PMIDs respectively, all drug-anchored)
- Gauge read: gliclazide 3->88%, methyldopa 6->75%, terazosin 6->85%, ertugliflozin 12->100%, felodipine 12->91%

Gate note (your suggestion): the 30% refetch threshold stays as-is — I re-fetched all 30 explicitly rather than raising the gate, because the EUtils path is strictly better than any RAG pool and the pipeline now self-heals <30% pools automatically. If you want future runs to auto-refetch 30-50% pools too, that's a one-line threshold change (30 -> 50) in `run_pipeline`; say the word.

## Side-effect (informational) — acknowledged

glyburide ddi_risk 11->12 phantom field: accepted as honest, unproven. No action.

## Residual scope note

Score VALUES (e.g. HCTZ renal_protection, metabolic_effect) are `_score_risk` heuristic outputs over now-clean pools. Retrieval is fixed; scoring semantics remain the PARSER_SUGGESTION.md tuning scope. L2b semantic review can proceed.
