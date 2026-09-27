# DQF — Project Resume
> What the Drug Quantification Framework is, what its core is, and everything done so far.
> Compiled 2026-09-27 · repo `github.com/rikirinjani/DQF` · branch `master` @ `05f6498`

---

## 1. What DQF Is

**Drug Quantification Framework (DQF)** is a pharmacist-built, evidence-grounded system for comparing drugs as **multi-axis fingerprints instead of a single score**.

The motivating problem: when you compare two analgesics today you get *a number* — NNT, NNH, effect size. That number collapses mechanism, safety, and pharmacokinetics into one dimension. But paracetamol and ibuprofen don't share a mechanism, don't share a risk profile, and the "right" choice depends on whether your patient is bleeding, has heart disease, or just needs a tooth pulled. A single number cannot answer that.

DQF's answer is **dimensional profiling**: every drug is described by four independently-populated levels. Ranking is possible only *after* the user applies context-specific weights — the framework itself stays agnostic. "Quantification" here means standardized schema, comparable metrics, per-datum evidence grading, and dimensional separation — not a composite score.

**Non-negotiable data rule:** every value is either sourced (PMID / FDA label / named database) or explicitly `null`. No fabrication, no backfilling missing labels with plausible-looking numbers.

---

## 2. The Core — The 4 Levels

| Layer | Focus | Primary source | Readiness |
|-------|-------|----------------|-----------|
| **L1 — Molecular Binding** | Ki/Kd/IC50/EC50 at primary *and* off-target targets | PDSP Ki, IUPHAR/GtoPdb, SAR literature | Literature-mining essential (PDSP weak on many targets) |
| **L2 — Pharmacokinetics** | ADME: bioavailability, half-life, Vd, protein binding, metabolism, clearance, food effect | DrugBank, Inxight FRDB, FDA clinical pharmacology reviews, PopPK studies | ~70 % structured |
| **L3 — Systems Response** | Biological consequence of L1 binding at tissue/pathway level (e.g. COX dynamics, tissue penetration, off-target engagement) | **No structured database exists** → literature mining via RAG is the only practical path | 🔴 hardest level |
| **L4 — Clinical Outcomes** | NNT/NNH, effect sizes, adverse-event rates, condition-specific outcomes | Cochrane, Oxford Pain League Table, RCTs, FDA labeling | Strong for acute, weaker for chronic |

### Causal chain (the reason four levels, not one)

```
L1 (binding) → L3 (tissue consequences) → L4 (clinical outcomes)
        └── modulated by L2: how much drug reaches the target ──┘
```

The same feature appears at several levels *on purpose* — COX-2 selectivity shows up as an L1 binding ratio, an L3 PGI2/TXA2 imbalance, and an L4 GI-sparing-but-CV-risk profile. Deduplicating it would destroy the causal chain.

### What the levels buy you that a score can't (proven in the PoC)

- Paracetamol NNT 3.6 "looks worse" than ibuprofen 2.5 — but zero GI/CV toxicity and a wholly different mechanism (AM404 → TRPV1 + Nav1.8 + CB1).
- Celecoxib's COX-2 selectivity traces cleanly L1 → L3 → L4: same feature = advantage *and* harm.
- Diclofenac plasma t½ = 1.2 h yet dosing is BID — explained only by L3 (synovial-fluid accumulation) + L2 (enterohepatic recirculation).
- Every drug wins at least one dimension and loses another → no drug "wins"; choice is patient-dependent.

### Ontology rules that matter

- **Active metabolites get full profiles** (parent + metabolite): paracetamol→AM404, sulindac→sulfide, nabumetone→6-MNA, codeine→morphine.
- **Evidence grading per datum** (HIGH/MODERATE/LOW), not per block.
- **Condition/population stratification** — NNT differs acute vs chronic; pharmacogenomic flags (CYP2C9, HLA) as qualifiers on L4.
- **L4 schema is class-specific** (locked 2026-07-31, machine-readable in `api/l4_schema_map.json`; the known `nnt_bp_control` false-sharing risk is documented, not silently renamed).

---

## 3. What Exists in the Repo

**Data**
- `api/drugs.json` — **95 drugs, 10 classes**: Antihypertensive 33, Diabetes 28, NSAID 10, Statin 6, Anticoagulant 6, PPI 5, H2RA 3, Antacid 2, Alginate 1, Mucosal Protectant 1.
  - **95/95** have `l3_systems` and `l4_clinical`; **798 L3 numeric cells, 50 null** (documented gaps).
  - Every record: `id, class, name, l1_binding, l2_pk, l3_systems, l4_clinical, pregnancy_safety, lactation_safety, hepatic_safety`.
- `api/l4_schema_map.json` (per-class field inventory + risk register), `api/regimens.json`, `api/server.py`, `api/query-tool.html`, root `dqf-dashboard.html`.

**Profiles (56 docs)** — `profiles/` (NSAID), `profiles-statins/`, `profiles-gi/` (PPI/H2RA/antacid/alginate/protectant), `profiles-anticoagulants/` — each per-drug doc plus a class `comparison.md`, in one house format.

**Scoring / pipeline (`rag-queries/`, 55 files)**
- `extract_l3.py` (~2,060 lines) — evidence fetch + `_score_risk` scorer, class-specific dimension definitions, keyword/negation/salt handling.
- `merge_l3.py` — profiles → `drugs.json`, with backups and (new) `--only` scoping.
- `kaggle_batch*.py` / `kaggle_judge_*.py` — LLM-judge triage scripts (Mistral-7B-Instruct-v0.3, 4-bit, T4×2), resumable per group.
- `test_scorer_hardening.py` (22 checks) + `test_anticoagulant_scorer.py` (24 checks) — script-style suites, **both passing** (run `python rag-queries/test_*.py`; pytest collects 0 by design).

**Validation (`validation/`, 8 reports)** — V1 PPI/NSAID/statin guideline concordance vs 6 major guidelines, V1c PPI L3 risk concordance (ACG), V2 formulary-tier comparison (DoD/VA/health systems), V4 edge-case audit (pregnancy, CKD, polypharmacy), plus Tier-2 leave-one-drug-out holdout for NSAIDs and statins.

**Methodology (6 docs)** — `framework-ontology.md` (4-level design), `evidence-hierarchy.md`, `search-protocol.md`, `limitations.md`, `validation-protocol.md`.

**Quality system** — QMS records under `Agentic Layer/qms/`: **13 nonconformities, 33 requirements, 154 verifications**, 2 reviews; PM-1 traces in `self-harness/traces/`; MemPalace drawers; crashlog + retrace gates.

---

## 4. What Has Been Done (chronology over 45 commits)

### Phase A — PoC foundation
- `556acdb` v1: 4-level framework, NSAID PoC (4 drugs, 5 PDF iterations), statin PoC (5 drugs + PDF), cross-class comparison, methodology docs, dashboard/query tool, `drugs.json` + server.
- RAG ground layer: MedQuery PubMed RAG (27.7M abstracts, FAISS + cross-encoder), evidence trail, `INDEX.md`, `CONCLUSION.md` — verdict: *the 4-level framework is viable; L1 off-target + L3 systems are the differentiators; RAG makes L1/L3 practical at scale.*

### Phase B — Scale-out to a real formulary
- Class implementations for L3 pipeline: PPI, H2RA, **Antacid**, **Alginate**, **Mucosal Protectant**; **Antihypertensive (33) + Diabetes (28)** records (`_add_e3_e4_drugs.py`), lovastatin added → 89, L4 schema map + ora-7 audit.
- L4 field coverage completed 88/88 → now 95/95.

### Phase C — RAG & fetch hardening
- LanceDB backend (bypasses the paused HF Space), cached model/table handles (**704 model loads → 1**), `--refresh` mode, per-class timeout/retry.
- Fix A–E in `extract_l3.py`: full text, PMID dedup, co-mention gate, confusable-token filter, still-loading retry, source provenance, `--eutils-first` alias; 512-char truncation cap + cross-angle duplication audit (VER-2026-018, CHAIN-2026-016).
- **Salt guard**: USP/RxNorm cation/anion/suffix vocabulary + RxNorm validation; drug-salt phrases masked before scoring so "warfarin sodium" doesn't inflate a general risk keyword.

### Phase D — Scorer hardening (the keyword-scoring war)
- `_score_risk` compacted (punctuation-insensitive) keyword matching: `cytochrome p450 (cyp) 3a4` now matches `cyp3a4`; short keywords excluded from fallback so they can't match across fused words.
- Absence-of-effect negation phrases ("no clinically important", "free of", "unaffected by" …) negate within a 5-word window; the previously **dead `negations=` argument wired in** (ddi pools pass "limited"/"few").
- Antacid `ddi_risk` made a real dimension; statin `ddi_risk` keywords gained BCRP.
- 8 off-scale curated L3 values fixed (data hygiene).
- **Regression suites: 22/22 + 24/24 passing.**

### Phase E — LLM-judge triage on Kaggle (Batches 1–6)
Because L3 is literature-only, evidence pools are graded by an LLM judge on Kaggle GPU, then human-adjudicated:
- **Batch 1** — Mistral-7B judge, 89 drugs / 413 cells → `judge_verdicts.json`.
- **Batch 2** — adversarial re-judge input + script; 2 adjudicated ddi_risk FP fixes (double-confirmation).
- **Batch 3** — ddi_risk sentence triage, `pk/pd/none` taxonomy, 8-sentence chunks, lenient array parser; 401 candidate sentences across 62 drugs; **9 pool drops applied**, then **28 held conflicts adjudicated (14 drops / 14 kept)** → ddi_risk adjudication cumulative 47 cells.
- **Batch 4** — evidence-strength triage for still-diluted cells → **17 raises to 3, 5 drops to 1** (`batch4_rescore.json` is the recipe format used by all later applies).
- **Batch 5** — full-corpus re-triage input + detach support (resume after every group, headless `kaggle kernels push`, `kaggle-detach-guide.md`).
- **Batch 6** — anticoagulant triage: 42/42 groups, 310/313 sentences; auditor vocabulary fix (flags 56→8); **one-verdict-per-sentence walk** fixes the sentence-drop bug permanently.
- Infrastructure: `classifier_audit.py` gate for suspect `strong` labels (catches negated/comparator text before it becomes a score).

### Phase F — E1 Anticoagulants (the class added this cycle)
1. **Evidence harvest** — mechanism-specific specs + curated values for all 6 drugs (PMIDs + labels), `f9edd18`/`817f7d1`.
2. **Records** — 6 anticoagulant entries added (`da124aa`, 89 → 95).
3. **Scorer** — anticoagulant template + **7-dim scorer** (`anticoagulation_efficacy, bleeding_risk, renal_clearance_dependence, ddi_risk, monitoring_burden, reversal_availability, gi_bleeding_risk`), audit directions, salt coverage (`6067bd5`).
4. **Fetch + triage input** (`8fd32c0`) → **Batch-6 Kaggle run** (`325ce7f`).
5. **Adjudication** — two rule families (ddi cells → filtered re-score R7; other 36 cells → R0–R5 caps) **plus a sourced-override layer** where an already-sourced label/PMID beats the keyword score. **14 of 42 cells changed; 13 sourced overrides.** LLM mislabels (negated sentences, comparator-arm text) corrected in the record; `batch6_verdicts.json` left verbatim.
6. **Label sourcing via DailyMed v2 SPL** — openFDA `spl_set_id` 404s and a wrong-hostname bug produced a false "DNS-blocked" claim (corrected in `5bae2f1`; NCR filed). Results: rivaroxaban GI bleed **HR 1.61 (1.30–1.99) → 3**; rivaroxaban/dabigatran/edoxaban `monitoring_burden → 1`; enoxaparin `ddi_risk → 2`; enoxaparin `gi_bleeding_risk` honestly left **`null`** (no GI rate in the LOVENOX label).
7. **Merge** — `merge_l3.py` gained **`--only`**: a repo-wide re-merge would have reverted 7 earlier hand-adjudicated classes (their profiles still hold pre-adjudication auto-scores). Applied with backup; validation **PASS** — only the 6 anticoagulants changed, all 42 cells match the approved table, prior adjudications untouched.
8. **Profile docs** — `profiles-anticoagulants/` (6 per-drug + comparison), verified cell-by-cell against the adjudication source of truth.
9. **Committed `54208fe`** → pushed to GH.

### Phase G — Batch 5 executed (just completed)
- Launched detached (`kaggle kernels push`, GPU on/internet on so the script can fetch input from GH raw), polled 09:40 → 11:12 **COMPLETE (~92 min)**.
- **Validation PASS**: 413/413 groups, **2573/2573 sentences, 0 missing, 0 length mismatch** — the Batch-6 drop bug is confirmed fixed.
- Class counts: `none` 1137 · `strong` 725 · `moderate` 488 · `pd` 103 · `pk` 77 · `negative` 43 → **905 kept (35.2 %)**; ddi subset 471 sentences (291/103/77).
- Committed **`05f6498`** and pushed; `origin/master` ahead 0, tree clean.

### Governance thread (runs through all phases)
Every session: PM-1 traces, failure records when something broke, QMS verification/NCR/requirement records, MemPalace drawers for what was learned, crashlog checkpoints, retrace gate (0 untraced files). Source policy formalized as a QMS requirement (2026-09-25): FDA labels (DailyMed SPL / openFDA) accepted alongside PMIDs, labels primary for L2 PK/safety.

---

## 5. Where Things Stand Now

**Done:** 95 drugs / 10 classes with L1+L2+L3+L4 populated (50 documented nulls), 56 profile docs, 8 validation reports, hardened RAG fetch + scorer with 46 passing regression checks, 6 Kaggle LLM-judge batches, E1 anticoagulants fully adjudicated and merged, Batch-5 full-corpus verdicts in-repo, everything pushed to GitHub.

**Open:**
1. **Consume `batch5_verdicts.json`** — rescore/adjudicate the non-anticoagulant evidence pools (`batch4_rescore.json` precedent) or hold as baseline for E2 antiplatelets.
2. **Refresh `TODO.md`** — untouched since 7/26, still shows E1 as in-progress.
3. **HF RAG endpoint** `balade-pubmed-rag-bot.hf.space` still 503 → `extract_l3.py` runs `--eutils-first` at 3 req/s (no `NCBI_API_KEY`).
4. **Next class** — E2 antiplatelets is the 🔴 High candidate per the roadmap.
5. Known debt: `l4_schema_map.json` Risk 1 (`nnt_bp_control` false-sharing) needs a coordinated rename + consumer update (`server.py` has 6 hardcoded L4 refs).
