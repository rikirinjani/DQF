# DQF Session Handoff — N6b Phase 1 + Label-Sourced Safety Fields

**Date:** 2026-10-17
**Repo:** `C:\Users\think\Project_v2\drug-quantification-framework` (branch `master`, GitHub `rikirinjani/DQF`)
**Latest push:** `b7c2894` + this handoff commit (clean tree, in sync with origin)
**Previous handoff:** `C:\Users\think\AppData\Local\Temp\opencode\handoff-dqf-n6b-indication-boundary.md` (2026-10-02; Temp is NOT durable, so handoffs now live in `handoffs/` in the repo)

---

## 0. Standing user rules (also saved in Claude memory)

1. **Run things on Kaggle, not locally.** Test suites, the grid and experiments all run in Kaggle kernels, to save the local machine. Local work is editing, git, and light inspection only.
2. **Watch token usage.** When a session gets large, write a handoff like this one in `handoffs/` and continue in a new session. The user prefers that to compacting.
3. **Evidence first, then apply.** Data changes are committed as PROPOSED ONLY, the user explicitly approves, then a separate apply commit follows. Never change `drugs.json` values without approval.
4. **Commit and push only when the user asks.** Approving a flow like "commit + apply + verify + records" counts as asking.
5. **Records after every apply or verification:**
   - QMS verification JSON in `C:\Users\think\Agentic Layer\qms\records\verifications\`
   - `pm1-trace trace ...`, run from `C:\Users\think`
   - MemPalace note in `C:\Users\think\AppData\Local\Temp\opencode\mempalace-inbox\`
   - `python C:\Users\think\self-harness\tools\crashlog.py --complete`
   - `retrace.py --project-root <repo> --traces-dir C:\Users\think\self-harness\traces`

---

## 1. What this session did

| Commit | What |
|---|---|
| `6164210` | **Design Phase 1.** `eligibility.hard_gate()` is the single shared evaluator, used by both the scoped and legacy paths and reporting all failed or unknown rules. Legacy `/api/query`: failed → `excluded[]` (never scored), unknown → `eligible_unranked[]`; combo add-ons skip blocked drugs; schema 1.1 (`hard_gates_applied`, `excluded`, `eligible_unranked`; results shape kept). Also recovered the 352-query grid into the repo as `rag-queries/smoke_api_grid.py`, with per-query gate invariants (the Temp copy was lost). |
| `277962a` | **Safety-field label evidence (PROPOSED).** Kaggle kernel `rikirinjani/dqf-label-safety-sourcing-cpu` pulled DailyMed SPL labels for the 50 drugs with null pregnancy, lactation and hepatic fields, plus a re-check of the 6 drugs the gate excluded. `rag-queries/curation/classify_label_safety.py` turns the label text into values using ordered rules; every value keeps its deciding quote. |
| `a272dfe` | **Apply (user APPROVED in full, including the statin pregnancy downgrade).** 152 cells across 53 drugs via `rag-queries/curation/apply_label_safety.py`. Backup: `rag-queries/l3_output/_backups/drugs_20261017_205417_label_safety.json`. Warfarin's earlier E1 label-sourced values were kept (the script never overwrites a value ending in `(label)`). |
| `b7c2894` | **Kaggle verification PASS at `a272dfe`.** Kernel `rikirinjani/dqf-gate-verify-cpu`, script `rag-queries/kaggle_gate_verify.py`; artifact `rag-queries/curation/label-safety-verification.json`. |

Also this session: a credibility assessment (summary in §5) and memory rules (§0).

---

## 2. Current state (verified on Kaggle at `a272dfe`)

- **Gate:** `test_indication_gate` 28/28 · `test_scorer_hardening` ALL PASSED · `test_anticoagulant_scorer` ALL PASSED · `test_merge_lock` 8/8 · `smoke_api_grid` 352/0.
- **Scoped objective `erosive_esophagitis_healing`:** status ok, 5 ranked (pantoprazole, rabeprazole, esomeprazole, lansoprazole, omeprazole), 0 unranked, 90 excluded.
- **Legacy, pregnant:** 93 ranked; excluded {lovastatin, warfarin}.
- **Legacy, severe hepatic impairment:** 85 ranked; 10 excluded (atorvastatin, rosuvastatin, simvastatin, pravastatin, pitavastatin, lovastatin, carvedilol, nebivolol, methyldopa, acarbose).
- **Null safety fields left:**
  - pregnancy and lactation: vildagliptin, gliclazide (not US-approved, so no DailyMed label);
  - hepatic: those two, plus atenolol, terazosin, clonidine and hydralazine (their labels say nothing about the liver).

---

## 3. Decisions and approvals (user's words)

- "APPROVED: apply all proposed label values including the statin pregnancy downgrade, commit evidence + apply, verify on Kaggle, and write records."
- **Statins:** current labels dropped the pregnancy contraindication (FDA 2021), so 5 statins went from X to "avoid ..." (D). They are out of the `pregnancy_x` gate but still take a −6 safety penalty. Lovastatin's old-format generic labels still contraindicate pregnancy, so it is X. This inconsistency is deliberate: labels as found.
- **Phase 1 scope:** legacy without an objective still returns a ranking. Design §8's "clarification / non-ranking" behaviour was deferred so the 352-grid stays a compatibility gate. The next session's first task changes this (see §4).

---

## 4. NEXT WORK (user-chosen order)

### 4a. Hepatic gate: severe only (do first, small)
- **Problem:** `api/eligibility.py` `_rule_hepatic_contraindicated` fires on any non-normal `hepatic_function`, mild included. The label contraindications it now enforces name severe states: acute liver failure, decompensated cirrhosis, active liver disease, severe impairment, cirrhosis.
- **Fix:** gate only when `hepatic_function == "severe"`. Mild and moderate stay as penalties in `server._compute_safety`, which is unchanged. The proper fix, an `active_liver_disease` input (design F06), waits for Phase 3 UI work.
- **Tests:** in `rag-queries/test_indication_gate.py`, the tests using `hepatic_function="moderate"` or `"mild"` expect exclusion: `test_legacy_all_failures_reported` uses moderate, and `test_legacy_class_filter_all_excluded_scoped_summary` uses mild. Update them, and add a mild/moderate → not excluded test.

### 4b. Legacy: no "Best choice" without an objective (small)
- **Problem:** `server.query_drugs` legacy summary says "Best choice for this profile: <drug>". For a 70-year-old with inflammatory pain the top answer is rosuvastatin, a cross-indication ranking (RES-01).
- **Fix:** keep the `results` shape and scores (grid compatibility), but:
  - add `status: "objective_required"` (or similar);
  - make the summary non-recommending, e.g. "Scores are not comparable across indications; pass `objective` for a recommendation."
- **Tests:** check the UI `api/query-tool.html` still renders. Add a test asserting the legacy summary never contains "Best choice".

### 4c. Design Phase 2: typed evidence migration (riskiest; design `rag-queries/curation/n6b-indication-boundary-design.md` §7, §12)
- **Problems:**
  - NNT endpoints in `l4_clinical` are nested `{value, ci_95, dose}` dicts: `nnt_bp_control`, `nnt_mace_5yr`, `nnt_50_pain_relief`.
  - Diabetes stores A1c under `nnt_bp_control` (e.g. metformin `{a1c_reduction: 1.5, unit: "%", dose}`).
- **Evidence-readiness matrix:** `rag-queries/curation/n6b-slice-verification.json`. PPI is best evidenced; H2RA and statins are next.
- **Known credibility gaps to fix in this phase:**
  - `evidence.json` `source` points back to `drugs.json` (circular), and `uncertainty` is null everywhere;
  - `eligibility.contract_ok()` only checks fields are non-null, not that they match the objective's contract;
  - pantoprazole is ranked #1 for healing despite the lowest `healing_ability` and potency, and its 89% value disagrees with the 82–87% in `validation/V1-ppi-guideline-concordance.md`.
- **Suggestion:** report tiers or ties when values overlap within uncertainty.

---

## 5. Everything else still open (priority order)

1. **Phase 3:** UI objective selector, `GET /api/conditions`, a scoped grid, legacy retirement, and rendering the `excluded` / `eligible_unranked` lists in `query-tool.html`.
2. **Second objective:** H2RA or statins.
3. **Credibility:**
   - the scoring constants are invented (NSAID `10-(NNT-2)*2.5`, statin `9-(NNT-40)*2/15`, PPI step cutoffs, weights 30/30/20/20);
   - L3 risk values are keyword counts, not effect sizes;
   - the V3 inter-rater study needs real pharmacists.
4. **Sourcing:** vildagliptin and gliclazide from their EMA SmPCs.
5. **Docs:** regenerate the profile documents (`profiles-antihypertensives/`, `profiles-diabetes/`, `profiles-statins/`) with the new safety fields.
6. **Tooling:**
   - `smoke_audit_fixes.py` (18/18) was lost from Temp; rewrite it into the repo;
   - `EXPECTED_HEAD` is out of date in `kaggle-ai/dqf_reeval_task.py` (not under `Project_v2`; probably a Kaggle benchmark task);
   - the `kbench.chats.new()`-per-chunk fix is still unapplied.
7. **N7 antiplatelets:** clopidogrel, ticagrelor, prasugrel (design `cafe082`).
8. **N6 cleanup:**
   - R1 per-class query wording;
   - PPI `cdi_risk` spread;
   - electrolyte keyword inflation;
   - `gi_tolerability` flat at 3;
   - calcium carbonate and aspirin evidence pool refresh;
   - `extract_l3` heart-rate keyword hardening.
9. **Data hygiene:** mojibake (e.g. `"Lowest â€" no CYP2C19..."` in PPI `l4_clinical.ddi_burden`).

---

## 6. Tooling and environment notes

- **Kaggle CLI on Windows:** set `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` first.
  - Push a kernel: `kaggle kernels push -p <dir>`.
  - Check status: `kaggle kernels status <id>`.
  - Get results: `kaggle kernels output <id> -p <dir>`.
  - Recover a kernel's source: `kaggle kernels pull <id> -p <dir> -m`.
- **Gate on Kaggle:**
  1. Push the commit to GitHub first; the kernel clones it.
  2. Copy `rag-queries/kaggle_gate_verify.py` into a scratch dir as `dqf-gate-verify-cpu.py` and replace `__HEAD__` with the 7-char commit.
  3. Add `kernel-metadata.json`: id `rikirinjani/dqf-gate-verify-cpu`, `kernel_type` script, `enable_internet` true, `enable_gpu` false, `is_private` true.
  4. Push, wait, then pull `gate_results.json`, which has the verdict plus a snapshot.
- **Label sourcing (reusable):** `rag-queries/curation/kaggle_label_safety_sourcing.py` → `classify_label_safety.py` → `apply_label_safety.py [--dry-run]`.
- **Gotchas:**
  - DailyMed SPL `<title>` is the highlights header ("...safely and effectively..."), so filter single-entity products on the search-result title, and reject hyphenated combinations.
  - "delivery" contains "liver".
  - In a Python heredoc, `'\\b'` inside a non-raw string writes a backspace character; check with `repr()`.
  - Don't `rm "$VAR"/*` (blocked by the safety check); write to a fresh directory instead.
  - Commit messages: write a file, then `git commit -F`.
- **Direct `@oracle` dispatch fails.** For independent design review, use a Kaggle benchmark task with `gpt-6-astra` (`kaggle b t ...`).

---

## 7. Resume commands

```bash
git -C "C:/Users/think/Project_v2/drug-quantification-framework" log --oneline -8
```

```bash
cat "C:/Users/think/Project_v2/drug-quantification-framework/handoffs/2026-10-17-n6b-phase1-label-safety.md"
```

Files to read first for §4:
- `api/eligibility.py` (`_rule_hepatic_contraindicated`, `hard_gate`)
- `api/server.py` (legacy `query_drugs`, summary block)
- `rag-queries/test_indication_gate.py`
- `rag-queries/curation/n6b-indication-boundary-design.md` (§7, §12)
