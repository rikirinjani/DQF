# DQF Session Handoff — Hepatic severe-only, legacy no-best-choice, Phase 2 P2-0/P2-1

**Date:** 2026-10-17
**Repo:** `C:\Users\think\Project_v2\drug-quantification-framework` (branch `master`, GitHub `rikirinjani/DQF`)
**Latest push:** `8344847` + this handoff commit (clean tree, in sync with origin)
**Previous handoff:** `handoffs/2026-10-17-n6b-phase1-label-safety.md` (its §0 standing rules still apply; summary below)

---

## 0. Standing user rules (unchanged; also in Claude memory)

1. **Kaggle, not local.** Tests, the grid and experiments run in Kaggle kernels. Local = editing, git, light inspection, and running small data scripts (dry-run/apply).
2. **Watch token usage**; hand off via `handoffs/` rather than compacting.
3. **Evidence first.** Data changes: PROPOSED commit → explicit user approval → separate apply commit. Never change `drugs.json` values without approval.
4. **Commit/push only when the user asks** (approving a flow like "commit + apply + verify + records" counts).
5. **Records after every apply/verification:** QMS JSON in `C:\Users\think\Agentic Layer\qms\records\verifications\`; `pm1-trace trace --agent orchestrator --outcome pass --key-files ... --action "..."` from `C:\Users\think`; MemPalace note in `C:\Users\think\AppData\Local\Temp\opencode\mempalace-inbox\`; `python C:\Users\think\self-harness\tools\crashlog.py --complete`; `retrace.py --project-root <repo> --traces-dir C:\Users\think\self-harness\traces`.

---

## 1. What this session did

| Commit | What |
|---|---|
| `c3ab28c` | **4a** `eligibility._rule_hepatic_contraindicated` gates only `hepatic_function == "severe"`; mild/moderate stay penalties + "Contraindicated in liver disease" concern in `server`. **4b** legacy `query_drugs` (no objective): `status: "objective_required"`, summary `"<n> drugs scored, not recommended: scores are not comparable across indications. Pass \`objective\` for a recommendation."` — never names a drug. `results` shape/scores unchanged. `query-tool.html` labels the box "Scores only — not a recommendation" for that status. Tests: `test_legacy_hepatic_mild_moderate_not_excluded`, `test_legacy_never_recommends`; grid asserts status per query. `kaggle_gate_verify.py` gained `PATCH_B64` (see §4) + `hepatic_moderate`/legacy-summary snapshot fields. |
| `9367623` | 4a+4b Kaggle PASS @ c3ab28c (`rag-queries/curation/hepatic-legacy-4ab-verification*.json`). |
| `d673c61` | **P2-0** (user decision D1): `api/evidence.json` 1.1.0 gains top-level `endpoints` — 77 typed records (NSAID `nnt_50_pain_relief` 10, Statin `nnt_mace_5yr` 6, Antihypertensive `nnt_bp_control` 33, Diabetes `a1c_reduction` 28), values/doses verbatim, comparator/horizon/population/source null, all `status: "legacy_unsourced"`. Script `rag-queries/curation/migrate_typed_evidence.py`; tests `rag-queries/test_typed_evidence.py` (10, in the gate). Implemented by a side session under a fixed brief + 13-point rubric, audited here. Also the Phase 2 plan with D1–D4. |
| `15f860b` | P2-0 Kaggle PASS @ d673c61. |
| `005a7a0` | **P2-1 evidence (PROPOSED):** `apply_a1c_efficacy.py --dry-run` → proposal + dry-run diff (140 added / 0 removed) + pre-apply Kaggle PASS. |
| `3ed7642` | **P2-1 apply (approved):** 28 Diabetes drugs gain `l4_clinical.a1c_efficacy = {value, unit: "percentage_points", dose}` right after `nnt_bp_control` (kept as legacy alias, D4). Name `a1c_efficacy` (L4 schema audit proposal) because `l3_systems.a1c_reduction` already exists as a keyword score — user-approved. `l4_schema_map.json` (field + RISK 1 resolution), `_add_e3_e4_drugs.py` (6 seeds) updated. Backup `rag-queries/l3_output/_backups/drugs_20261017_215741_p2_1.json`. |
| `8344847` | P2-1 Kaggle PASS @ 3ed7642. |

QMS records: `VER-2026-10-17-DQF-HEPATIC-LEGACY-001`, `...-P2-0-TYPED-EVIDENCE-001`, `...-P2-1-A1C-EFFICACY-001`.

---

## 2. Current state (Kaggle @ 3ed7642, kernel `rikirinjani/dqf-gate-verify-cpu` v8)

- `test_indication_gate` 30/30 · `test_typed_evidence` 10/10 · scorer hardening + anticoagulant ALL PASSED · `test_merge_lock` 8/8 · `smoke_api_grid` 352/0.
- Scoped `erosive_esophagitis_healing`: ok, ranked pantoprazole > rabeprazole > esomeprazole > lansoprazole > omeprazole, 0 unranked, 90 excluded.
- Legacy: pregnant → excluded {lovastatin, warfarin}; hepatic moderate → 0 excluded; hepatic severe → 10 excluded (5 statins + lovastatin, carvedilol, nebivolol, methyldopa, acarbose).
- Nothing reads `evidence.json` `endpoints` or `l4_clinical.a1c_efficacy` yet (Diabetes/AH efficacy still flat in the legacy scorer).

---

## 3. User decisions (2026-10-17) — in `rag-queries/curation/n6b-phase2-typed-evidence-plan.md` §5

- **D1** P2-0 approved (done). **D2** Diabetes A1c objective contract = placebo-adjusted change from baseline at ~24–26 wk, monotherapy, absolute percentage points; applies when A1c is label-sourced (P2-5), never to legacy values. **D3** efficacy tiers (P2-4) ship *after* a second objective. **D4** legacy `l4_clinical` keys stay as aliases until Phase 3.

---

## 4. NEXT WORK (plan §4)

### P2-2 — field-by-field evidence contract check (code only, no data)
- `api/eligibility.py:152` `contract_ok(ev, contract)` only checks non-null. Make it compare `unit`, `comparator`, `horizon_weeks`, `population` against the objective contract in `api/conditions.json` (normalised vocabulary), and return `contract_mismatch:<field>`; also reject `status == "legacy_unsourced"` → `unsourced_evidence`.
- **Watch out:** the contract text is free-form today (`"unit": "percent healed"`, `"horizon": "8 weeks"`, `"comparator": "placebo / active"`) while PPI records say `"percent"`, `8`, `"placebo"`. Design a normalised contract shape (e.g. `unit: "percent"`, `horizon_weeks: 8`, `comparators: ["placebo", "active"]`) — this is a `conditions.json` change, so propose it first. The 5 PPI rows must still rank (scoped snapshot unchanged) or the change is wrong.
- Tests: one mismatch per field → `eligible_unranked` with that reason; unsourced → unranked; PPI still ok.

### P2-3 — PPI re-sourcing (credibility gaps G1, G2, G4)
- `evidence.json` PPI `source` is circular (`"api/drugs.json l4_clinical.ee_healing_8wk_pct"`), `uncertainty` null; pantoprazole 89% vs 82–87% in `validation/V1-ppi-guideline-concordance.md`.
- Kaggle kernel pulls DailyMed §14 for the 5 PPIs (copy the pattern of `rag-queries/curation/kaggle_label_safety_sourcing.py` + `classify_label_safety.py`: every value keeps its deciding quote), output PROPOSED values + CI + setid. User approves → apply; keep old pointer as `derived_from`.
- Then G5 (pantoprazole #1 despite mid-pack healing — ranking is safety/PK-weighted) is addressed via tiers after a second objective (D3).

### Later (plan §4): P2-4 tiers, P2-5 Diabetes A1c label sourcing under the D2 contract (vildagliptin/gliclazide from EMA SmPC). Everything in the previous handoff §5 still open (Phase 3 UI/`/api/conditions`/rendering `excluded`, invented scoring constants, `smoke_audit_fixes.py` lost, N7 antiplatelets, data hygiene).

---

## 5. Tooling notes

- **Kaggle gate:** copy `rag-queries/kaggle_gate_verify.py` to `<dir>/dqf-gate-verify-cpu.py`, set `EXPECTED_HEAD` (7-char pushed commit); `kernel-metadata.json`: id `rikirinjani/dqf-gate-verify-cpu`, script, `enable_internet` true, `enable_gpu` false, private. `PYTHONIOENCODING=utf-8 PYTHONUTF8=1`; `kaggle kernels push -p <dir>`; poll `status` in a background loop; `kaggle kernels output ... -p <out>` → `gate_results.json`.
- **Pre-commit verification:** keep `EXPECTED_HEAD` at the pushed HEAD and set `PATCH_B64` = base64 of the patch (do the substitution in Python). Untracked files: `git add -N <paths>`, `git diff --binary`, `git reset -q -- <paths>`. Check the patch with `git archive HEAD | tar -x -C <scratch>` + `git apply --check` there (checking in the working tree fails if the change is already present).
- **Gotchas found this session:**
  - Windows text-mode writes give CRLF; a CRLF diff fails `git apply` on Kaggle → write diffs with `newline="\n"`.
  - Python heredoc: `"\\n"` in a string literal became a real newline (same trap as `'\\b'`); use the Edit tool for escapes.
  - `api/l4_schema_map.json` is hand-formatted (inline objects) — edit as text. `api/drugs.json` round-trips exactly with `json.dumps(indent=2, ensure_ascii=False)`, no trailing newline.
- **Delegating code:** a fixed brief + rubric worked well (P2-0 brief: side-session-notes folder `brief-P2-0-typed-evidence-unwrap.md`, outside the repo). Audit the diff and data yourself before asking the user to commit.

---

## 6. Resume commands

```bash
git -C "C:/Users/think/Project_v2/drug-quantification-framework" log --oneline -10
```

Files to read first: this handoff; `rag-queries/curation/n6b-phase2-typed-evidence-plan.md`; `api/eligibility.py` (`contract_ok`, `evidence_for`, `assess`); `api/conditions.json`; `api/evidence.json` (`evidence` section).
