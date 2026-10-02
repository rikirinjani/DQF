# N6b — Indication-Boundary Design (draft for review)

Scope: design the **eligibility gate** and **indication-scoped scoring** that the
re-assessment flagged as missing. This is a design document only — no code or data
changes. Implementation is a separate S-arc (phased in §11).

Provenance: re-assessment `dqf-reeval` (gpt-6-astra), residual findings **RES-01** and
**RES-02** (both *major*), plus adjacent RES-03/04/05/06 noted in §12. Source:
`kaggle-ai/dqf-out-reeval-astra/.../dqf_reeval/verify-server.md`.

---

## 1. Problem statement

### RES-01 — indication boundaries are not enforced

`POST /api/query` defaults to `drug_class="any"` (`api/server.py:43`, `:783`). Every one of
the 95 drugs is then scored by `_compute_efficacy(drug, pain_type, cv_risk)`
(`api/server.py:140`) and ranked in a single list. That function branches by **class**, so
the "efficacy" number means a different thing per row:

| class | efficacy endpoint used | source |
|---|---|---|
| NSAID | `nnt_50_pain_relief` (pain relief) | `server.py:149` |
| Statin | `nnt_mace_5yr` (CV events) | `server.py:169` |
| PPI / H2RA | `ee_healing_8wk_pct` / `duodenal_ulcer_healing_4wk_pct` | `server.py:185-201` |
| Antacid / Alginate | hardcoded 3.0 / 3.5–4.5 | `server.py:202-208` |
| Mucosal Protectant | `du_healing_8wk_pct` | `server.py:210-216` |
| **Antihypertensive** | **none — default 5.0** | `server.py:145` |
| **Diabetes** | **none — default 5.0** | `server.py:145` |
| **Anticoagulant** | **none — default 5.0** | `server.py:145` |

A pain NNT of 4 and a 5-year MACE NNT of 50 are not the same quantity; normalizing weights
(`WEIGHTS`, `server.py:758`) do not make them comparable. The result is a cross-indication
ranking that is clinically meaningless, and three whole classes silently score a flat 5.0
because no efficacy branch exists for them.

### RES-02 — contraindications are compensable deductions, not gates

Contraindication-grade facts are implemented as score penalties, not eligibility:

- pregnancy category X → `-8` (`server.py:269-270`)
- hepatic `contraindicated` → `-6` (`server.py:295-296`)

A drug can therefore absorb the penalty and still rank first; and when it is the only
candidate, `query_drugs` still emits `"Best choice for this profile: …"`
(`server.py:850-857`). Moving warnings earlier in the display does not stop the
recommendation.

### Root cause

The engine has **no representation of the treatment indication** and **no eligibility
stage**. `pain_type` is pain-specific; `cv_risk`/`gi_risk` are patient risk factors, not
indications. `l4_clinical.indications` exists for all 95 drugs but is free text
(e.g. NSAID: `["Acute pain","Dental pain","Dysmenorrhea","OA","RA"]`) and is used only for a
`+1` substring bonus (`server.py:158-161`).

---

## 2. Design principles

1. **Eligibility before ranking.** A drug that is not indicated, or is contraindicated for
   this patient, is never scored against the others and never recommended.
2. **One condition, one endpoint.** Within a ranking, every drug is scored on the *same*
   efficacy endpoint for the *same* condition. Cross-endpoint comparison is structurally
   impossible.
3. **Curated, sourced, no fabrication.** The condition taxonomy and drug→condition mapping
   are curated artifacts (N6 batch pattern: evidence → approval → apply), not runtime
   guesses over free text.
4. **Back-compatible.** The existing request shape keeps working (legacy mode) so the
   352-query grid and current UI do not break during migration.
5. **Explicit absence.** "No eligible treatment" is a first-class result, not an empty list
   with a misleading summary.

---

## 3. Proposed architecture — two stages

```
request (target_condition + patient factors)
        │
        ▼
┌─────────────────────────────┐
│ STAGE 1 — ELIGIBILITY GATE  │   binary, no scores
│  a) indication match        │
│  b) absolute contraindication│
└─────────────────────────────┘
        │ eligible[]                    │ excluded[] (id, reason)
        ▼                               ▼
┌─────────────────────────────┐   returned as-is,
│ STAGE 2 — RANKING           │   never ranked
│  efficacy = endpoint(cond)  │
│  safety / pk / mechanism    │
│  weighted overall           │
└─────────────────────────────┘
        │
        ▼
  ranked eligible[] + excluded[] + no_eligible_treatment flag
```

Stage 1 is a pure filter. Stage 2 is the existing scoring engine, but with efficacy driven
by the **condition's endpoint** rather than the class branch.

---

## 4. Data model

### 4.1 Condition registry — `api/conditions.json` (new)

A small controlled vocabulary covering the 10 classes' indications. Not ICD-10 (too
granular) and not SNOMED (licensing); a curated DQF list of ~15–25 conditions.

```jsonc
{
  "conditions": {
    "acute_pain": {
      "display": "Acute pain",
      "synonyms": ["acute pain", "dental pain", "post-operative pain", "renal colic"],
      "eligible_classes": ["NSAID"],
      "endpoint": { "key": "nnt_50_pain_relief", "kind": "nnt", "direction": "lower_better" },
      "contraindication_rules": ["pregnancy_third_trimester", "gi_bleed_active", "severe_renal"]
    },
    "inflammatory_arthritis": {
      "display": "Inflammatory arthritis (OA/RA)",
      "synonyms": ["oa", "ra", "ankylosing spondylitis", "inflammatory arthritis"],
      "eligible_classes": ["NSAID"],
      "endpoint": { "key": "nnt_50_pain_relief", "kind": "nnt", "direction": "lower_better" },
      "contraindication_rules": ["pregnancy_third_trimester", "gi_bleed_active", "severe_renal"]
    },
    "cv_prevention": {
      "display": "Cardiovascular event prevention",
      "synonyms": ["primary + secondary cvd prevention", "cv risk reduction", "familial hypercholesterolemia"],
      "eligible_classes": ["Statin"],
      "endpoint": { "key": "nnt_mace_5yr", "kind": "nnt", "direction": "lower_better" },
      "contraindication_rules": ["pregnancy", "active_liver_disease"]
    },
    "gerd": {
      "display": "GERD / reflux",
      "synonyms": ["gerd", "erosive esophagitis", "heartburn", "regurgitation"],
      "eligible_classes": ["PPI", "H2RA", "Antacid", "Alginate"],
      "endpoint": { "key": "ee_healing_8wk_pct", "kind": "percent", "direction": "higher_better" },
      "contraindication_rules": []
    },
    "peptic_ulcer": {
      "display": "Peptic ulcer disease",
      "synonyms": ["duodenal ulcer", "gastric ulcer", "h. pylori eradication"],
      "eligible_classes": ["PPI", "H2RA", "Mucosal Protectant"],
      "endpoint": { "key": "duodenal_ulcer_healing_4wk_pct", "kind": "percent", "direction": "higher_better" },
      "contraindication_rules": []
    },
    "hypertension": {
      "display": "Hypertension",
      "synonyms": ["hypertension", "bp control", "resistant hypertension"],
      "eligible_classes": ["Antihypertensive"],
      "endpoint": { "key": "nnt_bp_control", "kind": "nnt", "direction": "lower_better" },
      "contraindication_rules": ["pregnancy_acei_arb"]
    },
    "t2dm": {
      "display": "Type 2 diabetes",
      "synonyms": ["t2dm", "prediabetes", "gdm"],
      "eligible_classes": ["Diabetes"],
      "endpoint": { "key": "a1c_reduction_pct", "kind": "percent", "direction": "higher_better" },
      "contraindication_rules": []
    },
    "af_stroke_prevention": {
      "display": "Stroke prevention in AF",
      "synonyms": ["stroke prevention in non-valvular af", "stroke prevention in af", "mechanical heart valves"],
      "eligible_classes": ["Anticoagulant"],
      "endpoint": { "key": "stroke_se_reduction_vs_warfarin", "kind": "percent", "direction": "higher_better" },
      "contraindication_rules": ["active_bleeding", "severe_renal"]
    }
    // … vte_treatment, heart_failure, angina, post_mi, ckd_progression, obesity, etc.
  }
}
```

Notes:
- `endpoint.key` names an `l4_clinical` field. Where the field does not yet exist
  (Diabetes `a1c_reduction_pct`, Anticoagulant endpoint normalization) it is a **Phase 2
  data task** — see §7.
- `endpoint` may carry a `fallback` (secondary endpoint) for drugs that lack the primary —
  see §7.3.
- `endpoint.kind` selects the score transform: `nnt` (lower better) vs `percent` (higher
  better) — see §7.2.
- `synonyms` is a **curation aid only** (used to generate `condition_ids`), never evaluated
  at runtime. Runtime matching over free text is exactly the fragility that produced the
  `pain_type in ind` partial-match bug (astra REG-02).
- `eligible_classes` is a guardrail, not the gate itself; the gate is the per-drug
  condition mapping (§4.2). It catches taxonomy mistakes (a Statin can never be eligible
  for `acute_pain`).

### 4.2 Drug → condition mapping (curated)

Add `condition_ids: [...]` to each drug's `l4_clinical` (or a sibling
`api/condition_map.json`). Source of truth is **explicit curation**, generated from the
free-text `indications` via the registry `synonyms` and then human-reviewed (N6 batch
pattern). Example:

```jsonc
// api/drugs.json → ibuprofen.l4_clinical
"condition_ids": ["acute_pain", "inflammatory_arthritis", "dysmenorrhea"]
```

Rationale for explicit over runtime matching: the free-text `indications` are
heterogeneous ("OA (pain only)", "Stroke prevention in non-valvular AF"), and a runtime
substring match is exactly the fragility that produced the `pain_type in ind` partial-match
bug (astra REG-02). Curation is auditable and testable.

**Completeness invariant (must be enforced, not assumed).** A drug with an empty or missing
`condition_ids` would silently become ineligible for *every* condition — a dangerous
over-exclusion. Therefore:

- Phase 0 must produce a **coverage report**: every drug has ≥1 `condition_id`, and every
  drug's `condition_ids` are consistent with its free-text `indications`.
- At load time, a drug with no `condition_ids` is **flagged** (`unmapped: true`) and
  surfaced in the response's `excluded` list with reason `unmapped_condition`, never
  silently dropped.
- A test asserts 95/95 coverage (see §10.5).

### 4.3 Contraindication rules (normalized)

Today contraindication-grade facts are scattered across `pregnancy_safety`,
`lactation_safety`, `hepatic_safety` and narrative strings. The gate needs a normalized,
machine-checkable form. Two options:

- **(A) Rule table** in `conditions.json` evaluated against existing patient factors +
  drug fields. Lowest data churn; reuses `_norm_preg` etc.
- **(B) Per-drug `contraindications` block** listing `{rule, basis}`. More explicit, more
  curation.

Recommendation: **(A) now, (B) as the sourced follow-up.** The rule table can express the
high-value gates immediately using fields that already exist, while (B) is where sourced
per-drug contraindications land later.

**Hard vs soft — the critical distinction.** The rule table must separate two kinds of
rule, because conflating them causes over-exclusion:

- **`contraindication_rules` (hard, gate).** Absolute contraindications only: the drug must
  not be used in this patient for this condition. Examples: pregnancy category X for a
  statin; `hepatic_safety == contraindicated`; ACEi/ARB in pregnancy; NSAID in the third
  trimester. These remove the drug from `eligible`.
- **`caution_rules` (soft, penalty).** Risk stratification that should lower the score but
  not exclude: high-GI-risk patient + NSAID, severe renal + a renally-cleared drug, etc.
  These stay in Stage 2 safety scoring exactly as today.

A high-risk patient is **not** the same as a contraindicated one. Encoding "high GI risk +
NSAID" as a hard gate would wrongly exclude a legitimate, monitorable option; it belongs in
`caution_rules`. Only contraindication-grade facts gate.

---

## 5. Eligibility gate rules

A drug is **eligible** for `(target_condition, patient)` iff:

1. `target_condition ∈ drug.condition_ids` (indication match), **and**
2. no **hard** `contraindication_rule` for that condition evaluates true for this patient.

Rules are evaluated in a fixed order and the **first** failing rule is the exclusion
reason. Illustrative **hard** rules (gate):

| rule | true when |
|---|---|
| `pregnancy` | `pregnancy_status != not_pregnant` and normalized category == X |
| `pregnancy_third_trimester` | third trimester and drug is an NSAID (ductus arteriosus) |
| `pregnancy_acei_arb` | pregnant and drug is ACEi/ARB |
| `active_liver_disease` | `hepatic_function` in (moderate, severe) and `hepatic_safety == contraindicated` |
| `active_bleeding` | anticoagulant and an active-bleeding flag is set (Phase 1: not yet modeled — see §13) |

Illustrative **soft** rules (penalty, Stage 2 — *not* gates):

| rule | effect |
|---|---|
| `high_gi_risk_nsaid` | `gi_risk == high` and NSAID → existing GI penalty |
| `severe_renal_risk` | `renal_function == severe` and `renal_risk` ≥ 3 → existing renal penalty |
| `lactation_avoid` | lactation `avoid` → existing `-4` |

**Caution ≠ exclusion.** Existing penalties (e.g. pregnancy category C `-3`, lactation
`avoid` `-4`) remain in Stage 2 safety scoring. Only contraindication-grade facts gate.

---

## 6. Response contract

```jsonc
{
  "query": { "...": "echoed, incl. target_condition" },
  "mode": "indication_scoped",          // or "legacy"
  "eligible": [ { "id": "...", "scores": {...}, "overall": 8.4, "strengths": [...], "concerns": [...] } ],
  "excluded": [ { "id": "ibuprofen", "name": "Ibuprofen", "reason": "pregnancy_third_trimester" } ],
  "no_eligible_treatment": false,
  "summary": "Best choice for this profile: …"
}
```

- `excluded` is always present (possibly empty) and is **never** ranked.
- When `eligible` is empty: `no_eligible_treatment: true` and `summary` must state that no
  eligible treatment exists for this condition/profile — never "Best choice".
- `mode: "legacy"` is returned when `target_condition` is absent (see §8).

---

## 7. Endpoint calibration (fills the three flat-5.0 classes)

Stage 2 efficacy becomes `score_efficacy(drug, condition)`:

| condition | endpoint | current state | action |
|---|---|---|---|
| acute/inflammatory pain | `nnt_50_pain_relief` | works (NSAID) | reuse |
| cv_prevention | `nnt_mace_5yr` | works (Statin) | reuse |
| gerd / peptic_ulcer | healing % | works (PPI/H2RA/Mucosal) | reuse |
| **hypertension** | `nnt_bp_control` | data present (33/33), **no scorer** | add branch |
| **t2dm** | `a1c_reduction_pct` | **key missing**; Diabetes records carry a mislabeled `nnt_bp_control` | data fix + branch |
| **af_stroke_prevention / vte** | `stroke_se_reduction_vs_warfarin` etc. | data present, **no scorer** | add branch |

The Diabetes `nnt_bp_control` false-share is the known `l4_schema_map.json` Risk 1 debt
(TODO Known Debt) — N6b Phase 2 is where it must be resolved, because the condition
registry makes the endpoint key explicit.

### 7.1 Endpoint → score transform

Each `endpoint.kind` needs a documented 0–10 transform so that different endpoint types
are scored consistently *within* a condition (they are never compared *across* conditions):

- `nnt` (lower better): reuse the existing NSAID shape `max(0, 10 - (nnt - 2) * 2.5)`
  (`server.py:156`), with a per-condition anchor where the NNT scale differs (e.g. MACE
  NNT ~40–55 uses the statin shape `9 - (nnt - 40) * (2/15)`, `server.py:177`).
- `percent` (higher better): banded mapping (e.g. healing ≥90 → 9.0, ≥83 → 8.0, ≥50 → 5.5,
  else 4.0 — the existing PPI bands, `server.py:191-198`).

The transform lives with the condition, not the class, so a new class added to a condition
inherits the correct scale automatically.

### 7.2 Missing-endpoint handling (do not silently drop an indicated drug)

Within a condition, eligible drugs may lack the primary endpoint. Example: for `gerd`, PPI
and H2RA carry `ee_healing_8wk_pct`, but Antacid and Alginate carry **no** efficacy keys at
all (they are symptomatic-relief agents). A drug that is *indicated* must not vanish just
because its endpoint is absent. Rules:

1. If the primary endpoint is missing, try the condition's `fallback` endpoint (§7.3).
2. If no endpoint is available, score efficacy as a documented **neutral** and attach a
   `data_quality: "endpoint_missing"` flag to the row — never a silent 5.0 that looks like
   a real score, and never exclusion.
3. The response surfaces the flag so the UI can show "efficacy not quantified" rather than
   implying equivalence.

### 7.3 Fallback endpoints

A condition may declare a `fallback` endpoint for drugs that lack the primary. For `gerd`,
the fallback is symptom relief (`gerd_symptom_nnt`, present for PPI/H2RA) or, for
Antacid/Alginate, a documented symptomatic-relief tier. This keeps the ranking
same-endpoint where possible and explicitly tiered where not.

---

## 8. Back-compatibility & migration

- `target_condition` is **optional** in `QueryRequest`. Absent → `mode: "legacy"`, current
  behaviour (class filter + `pain_type`), so the 352-query grid and the current UI keep
  passing during migration.
- Present → `mode: "indication_scoped"`, gate enforced.
- `drug_class` remains as an optional **narrowing** filter inside the eligible set (e.g.
  "any GI drug for GERD" vs "PPI only").

**Legacy mode is a temporary shim, not a permanent feature.** It preserves the RES-01
defect (cross-indication ranking), so:

- Legacy responses carry `"deprecated": true` and a warning that the ranking is not
  indication-scoped.
- The **UI default becomes scoped** as soon as Phase 3 ships; legacy is API-only.
- The 352-query grid is a test artifact we own — Phase 3 updates it to condition-scoped
  requests, after which legacy mode can be retired (or kept only for external API
  consumers, still flagged deprecated).

---

## 9. UI changes (`api/query-tool.html`)

- Add a **condition selector** (required for scoped mode) populated from
  `conditions.json`; keep the class checkbox group as an optional narrowing filter.
- Show an **excluded** section with reasons ("Not eligible: contraindicated in pregnancy").
- When `no_eligible_treatment`, render the explicit message instead of a best-choice card.
- `pain_type` becomes a sub-attribute of pain conditions (or is derived), not a top-level
  driver.

---

## 10. Test plan / acceptance criteria

1. **Gate unit tests** (`rag-queries/test_indication_gate.py` or extend the smoke suite):
   - ibuprofen + `acute_pain` + third-trimester pregnancy → excluded (`pregnancy_third_trimester`)
   - simvastatin + `acute_pain` → excluded (indication mismatch)
   - omeprazole + `gerd` → eligible; scored on `ee_healing_8wk_pct`
   - lisinopril + `hypertension` → eligible; scored on `nnt_bp_control` (not 5.0)
   - metformin + `t2dm` → eligible; scored on the A1c endpoint
2. **Hard vs soft**: high-GI-risk patient + NSAID → **still eligible** (penalized, not
   excluded); pregnancy category X statin → excluded.
3. **Missing endpoint**: antacid + `gerd` → eligible with `data_quality: "endpoint_missing"`
   (or fallback tier), never dropped and never a silent 5.0.
4. **Unmapped drug**: a drug with no `condition_ids` appears in `excluded` with reason
   `unmapped_condition`, never silently absent.
5. **No-eligible-treatment**: a condition/profile with all candidates excluded returns
   `no_eligible_treatment: true` and a non-recommending summary.
6. **Comparability invariant**: within one response, every eligible row's efficacy is
   derived from the same `endpoint.key` (assertable in a test).
7. **Back-compat**: the existing 352-query grid passes unchanged in legacy mode.
8. **Taxonomy integrity**: every `condition_ids` value exists in `conditions.json`; every
   condition's `eligible_classes` are real classes; no drug maps to a condition whose
   `eligible_classes` excludes its class; 95/95 coverage.
9. `py_compile` clean; commit + QMS verification + trace.

---

## 11. Phasing (S-arc)

| phase | deliverable | depends on |
|---|---|---|
| **0** | `conditions.json` taxonomy + curated `condition_ids` for 95 drugs (N6 batch pattern: evidence → approval → apply) | — |
| **1** | Eligibility gate + response contract (`eligible`/`excluded`/`no_eligible_treatment`) + contraindication rule table | Phase 0 |
| **2** | Condition-scoped efficacy: add Antihypertensive / Diabetes / Anticoagulant branches; resolve `l4_schema_map` Risk 1 (Diabetes `nnt_bp_control` false-share) | Phase 0; data fix |
| **3** | UI condition selector + excluded display + grid update to scoped requests | Phases 1–2 |

Phase 0 is the long pole (curation of 95 drugs); Phases 1–2 are mechanical once the
taxonomy exists.

---

## 12. Adjacent findings (out of N6b scope, tracked)

From the same re-assessment, not addressed by this design:

- **RES-03** — combo suggestions ignore patient context (`server.py:524`).
- **RES-04** — `"none"` truthiness / non-NSAID classes falling into statin mechanism logic
  (`server.py:484-491`).
- **RES-05** — nullable string/collection paths can abort a query (`special=None`,
  `selectivity=None`, `None` in `indications`).
- **RES-06** — duplicate "High DDI burden" concerns (`server.py:640-657`).
- **astra REG-01** — `_norm_preg` maps "not contraindicated" to X (negation handling).
- **astra REG-02** — `pain_type in ind` partial-match (superseded by the explicit
  `condition_ids` mapping in §4.2).

---

## 13. Open questions

1. **Taxonomy granularity** — how many conditions? Start with the ~15–25 that cover the
   current 10 classes; expand with N7 antiplatelets.
2. **Multi-condition drugs** — eligibility is per-condition, so a drug may be eligible for
   one condition and excluded for another; confirm the UI can express this.
3. **Contraindication sourcing** — rule table (A) vs per-drug block (B); (B) needs a
   sourced curation round.
4. **Combination/regimen eligibility** — RES-03 implies the gate should eventually evaluate
   the whole regimen, not a single drug. Out of scope for Phase 1.
5. **Legacy retirement** — when (if ever) to drop `mode: "legacy"`.
6. **Population calibration** — RES-01 says "calibrate scores within indication and
   population"; this design scopes by indication. Population (age/renal/hepatic) remains a
   Stage 2 modifier, not a separate calibration — confirm that is sufficient.
7. **`active_bleeding` modeling** — Phase 1 has no patient field for active bleeding, so
   that hard rule cannot be evaluated yet. Either add a request field or defer the rule;
   do not fake it from `gi_risk`.
8. **Endpoint anchors** — the `nnt` transform needs a per-condition anchor (the NNT scale
   differs: pain ~2–6, MACE ~40–55, BP control ~10–20). Who sources these anchors, and are
   they curated constants or derived from the data distribution?

---

## 14. Non-goals

- No change to L3 extraction, templates, or the N6 curation artifacts.
- No new drug classes (that is N7).
- No change to the safety/PK/mechanism scoring formulas beyond the eligibility split.
- No implementation in this document.
