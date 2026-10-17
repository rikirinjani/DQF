# N6b Design Phase 2 — Typed Evidence Migration: Plan (PROPOSED, no data changed)

**Date:** 2026-10-17 · **Base:** `1d58157` + 4a/4b · **Design:** `n6b-indication-boundary-design.md` §4.3, §7, §12
**Status:** PROPOSED; D1–D4 decided by the user on 2026-10-17 (§5). P2-0 approved; later steps still need their own approval before data changes.

---

## 1. Inventory (read from `api/drugs.json` today)

| `l4_clinical` key | Class | Shape found | Problem |
|---|---|---|---|
| `nnt_50_pain_relief` | NSAID 10/10 | `{value, ci_95, dose}` | nested; no comparator/horizon/population/source |
| `nnt_mace_5yr` | Statin 6/6 | `{value, ci_95, dose}` | nested; no population (primary vs secondary prevention), no source |
| `nnt_bp_control` | Antihypertensive 33/33 | `{value, ci_95, dose}` | nested; "BP control" target/comparator/horizon undefined |
| `nnt_bp_control` | **Diabetes 28/28** | `{a1c_reduction, unit:"%", dose}` | **collision**: A1c reduction stored under a BP NNT key; no `value`, no comparator/baseline/horizon/source |
| `stroke_se_reduction_vs_warfarin` | Anticoagulant | 4 str, 1 dict, 1 null | mixed types; free-text trial summaries |
| `ich_reduction`, `major_bleeding_hr_vs_warfarin` | Anticoagulant | dict / str / null mix | warfarin stored as the string "reference comparator" |
| `ldl_reduction_1yr_pct` | Statin 1/6 (lovastatin) | dict with PMID | only one statin has it |
| `nnh_gi`, `nnh_cv` | NSAID | dict / null | harms, not efficacy; out of Phase 2 scope |

Consumers: `server._compute_efficacy` reads `nnt_50_pain_relief.value` and `nnt_mace_5yr.value` (lines ~158, ~178). Diabetes and Antihypertensive efficacy fall through to a flat score. `rag-queries/_add_e3_e4_drugs.py` wrote the collided A1c shape.

## 2. Credibility gaps (from the handoff §4c), with proposed fixes

| Gap | Evidence | Proposed fix |
|---|---|---|
| G1 `evidence.json` `source` is circular (`"api/drugs.json l4_clinical.ee_healing_8wk_pct"`) | all 5 PPI rows | Replace with primary source (label §14 / named RCT + PMID) sourced on Kaggle, keep a `derived_from` field for the old pointer |
| G2 `uncertainty` null everywhere | all 5 PPI rows | Fill `ci_95` or a range from the same source; if the source gives none, record `"uncertainty": {"kind": "not_reported"}` rather than null |
| G3 `contract_ok()` checks non-null only | `api/eligibility.py:152` | Compare unit, comparator, horizon, population against the objective contract (normalised vocab), reject on mismatch with a `contract_mismatch:<field>` reason |
| G4 Pantoprazole 89% vs 82–87% in `validation/V1-ppi-guideline-concordance.md` | V1 lines 34, 76 | Re-source all 5 PPI healing values from one comparable source family; record which; the disagreement goes away or is documented |
| G5 Pantoprazole ranks #1 for healing although its healing value is mid-pack and potency is lowest | Kaggle snapshot: pantoprazole > rabeprazole > esomeprazole > lansoprazole > omeprazole | Ranking is driven by safety/PK weights, not efficacy. Proposal: report **tiers/ties** when efficacy values overlap within uncertainty (needs G2), and show the efficacy-only order alongside |

## 3. Proposed typed record (one per drug × objective × population)

```jsonc
{
  "value": 1.5, "unit": "percentage_points", "direction": "higher_better",
  "endpoint": "a1c_change_from_baseline_placebo_adjusted",
  "comparator": "placebo", "horizon_weeks": 24, "population": "T2DM, monotherapy",
  "dose": "2000 mg/day",
  "source": {"kind": "label", "setid": "...", "section": "14", "quote": "..."},
  "uncertainty": {"kind": "ci_95", "low": 1.2, "high": 1.8},
  "derived_from": "drugs.json l4_clinical.nnt_bp_control.a1c_reduction",
  "status": "sourced" | "legacy_unsourced"
}
```

`status: legacy_unsourced` rows are kept for the legacy path but `contract_ok()` rejects them (→ `eligible_unranked`, reason `unsourced_evidence`), so nothing unsourced gets ranked on the scoped path.

## 4. Steps (each is evidence → user approval → apply → Kaggle gate → records)

1. **P2-0 Unwrap, no value changes (mechanical).** Script `rag-queries/curation/migrate_typed_evidence.py --dry-run` emits typed records into `evidence.json` for NNT/A1c endpoints with `status: legacy_unsourced`, values copied verbatim. Diabetes moves from `nnt_bp_control` to a new `a1c_reduction` key. `drugs.json` keeps the old keys for legacy consumers in this step (read-only alias); a test asserts every typed value equals its legacy source. Output: PROPOSED diff + counts.
2. **P2-1 Fix the collision in `drugs.json`.** After P2-0 is verified: add `l4_clinical.a1c_efficacy` for the 28 Diabetes drugs (name from the L4 schema audit; `a1c_reduction` would clash with the `l3_systems.a1c_reduction` keyword score — user-approved), keeping `nnt_bp_control` as a legacy alias until Phase 3 (D4); update `_add_e3_e4_drugs.py` and `api/l4_schema_map.json`. Grid 352/0 must hold. **DONE 2026-10-17** (evidence 005a7a0, apply after it).
3. **P2-2 Contract check (G3).** Code change in `eligibility.contract_ok()` + tests (mismatch on each field → unranked). No data change.
4. **P2-3 PPI re-sourcing (G1, G2, G4).** Kaggle kernel pulls DailyMed §14 for the 5 PPIs (reuse `kaggle_label_safety_sourcing.py` pattern), classifier keeps the deciding quote; PROPOSED values + CI. User approves → apply.
5. **P2-4 Tiers (G5).** Response adds `efficacy_tier` (overlapping CIs share a tier) and an efficacy-only order; summary names a tier, not a single winner, when the top is tied. Needs P2-3.
6. **P2-5 Next objective sourcing.** Diabetes A1c from labels (28 drugs, vildagliptin/gliclazide from EMA SmPC) or H2RA/statins — user picks.

## 5. User decisions (2026-10-17)

- **D1 — APPROVED:** P2-0 mechanical unwrap, values verbatim, every record `status: legacy_unsourced`.
  Scope fixed for P2-0: the 77 nested records (NSAID `nnt_50_pain_relief` 10, Statin `nnt_mace_5yr` 6,
  Antihypertensive `nnt_bp_control` 33, Diabetes A1c under `nnt_bp_control` 28) go into a new top-level
  `endpoints` section of `api/evidence.json`. The objective-scoped `evidence` section (5 PPI rows) is untouched.
  Anticoagulant (mixed str/dict/null), `ldl_reduction_1yr_pct`, `nnh_*` are out of P2-0 scope.
- **D2 — APPROVED:** the Diabetes A1c objective contract is **placebo-adjusted change from baseline at
  ~24–26 weeks, monotherapy, absolute percentage points**. It applies when A1c is label-sourced (P2-5);
  P2-0 does not assert it on the unsourced legacy values (their comparator/horizon/population stay null).
- **D3 — AFTER:** efficacy tiers (P2-4) ship after a second objective.
- **D4 — YES:** legacy `l4_clinical` keys stay in `drugs.json` as aliases until Phase 3 legacy retirement;
  P2-1 adds the correct Diabetes key alongside the old one instead of removing it.
