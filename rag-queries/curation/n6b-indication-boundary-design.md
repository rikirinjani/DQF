# N6b — Indication-Boundary Design (v2, post-review)

Scope: design the **eligibility gate**, **evidence-compatibility contract**, and
**indication-scoped ranking** that the re-assessment flagged as missing. Design only — no
code or data changes. Implementation is a separate S-arc (§12).

Provenance:
- Re-assessment `dqf-reeval` (gpt-6-astra), residual findings **RES-01** and **RES-02**
  (both major). Source: `kaggle-ai/dqf-out-reeval-astra/.../dqf_reeval/verify-server.md`.
- **Independent design review** by GPT-6 Astra (Kaggle benchmark `dqf-n6b-review`, run
  3914507) of v1 (`6c02909`): 23 findings, verdict *not ready to implement as specified*.
  Full review: `rag-queries/curation/n6b-review-gpt6-astra.md`. Disposition of every
  finding: §16.

**v2 changes at a glance** (driven by the review): eligibility is separated from
*rankability*; cross-endpoint fallback and neutral-score imputation are removed; a typed
evidence contract replaces "same endpoint key"; contraindication rules become global
(drug/subclass) rather than condition-local; every recommendation path (legacy, combo
suggestions, mechanism) is brought inside the safety boundary; the taxonomy is corrected;
and the rollout becomes one narrow, fully-supported vertical slice after an
evidence-readiness audit.

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
- hepatic `contraindicated` → `-6` for moderate/severe impairment, `-3` for mild
  (`server.py:292-303`; severity-dependent, not a blanket `-6`)

A drug can therefore absorb the penalty and still rank first; and when it is the only
candidate, `query_drugs` still emits `"Best choice for this profile: …"`
(`server.py:850-857`). Moving warnings earlier in the display does not stop the
recommendation.

### Root cause

The engine has **no representation of the treatment objective**, **no eligibility stage**,
and **no evidence-compatibility contract**. `pain_type` is pain-specific; `cv_risk`/
`gi_risk` are patient risk factors, not indications. `l4_clinical.indications` exists for
all 95 drugs but is free text (e.g. NSAID: `["Acute pain","Dental pain","Dysmenorrhea","OA","RA"]`)
and is used only for a `+1` substring bonus (`server.py:158-161`).

---

## 2. Design principles

1. **Eligibility before ranking.** A drug that is not indicated, or is contraindicated for
   this patient, is never scored against the others and never recommended.
2. **Eligibility ≠ rankability.** Being indicated and non-contraindicated does not imply the
   drug has *comparable evidence*. Drugs with insufficient evidence are shown as
   `eligible_unranked`, never given an invented score (§6, §7).
3. **No fabricated evidence.** Missing efficacy is never imputed as a neutral number; a
   drug with no measurement cannot win a ranking through safety/PK scores.
4. **Comparability is a contract, not a key.** Ranking requires compatible evidence
   (outcome, unit, comparator, horizon, population, dose/regimen, source, uncertainty) —
   not merely the same field name (§7).
5. **Safety is global.** Contraindication rules apply by drug/subclass independently of the
   selected indication; a contraindication cannot disappear because the drug was queried
   under a different condition (§5).
6. **Unknown ≠ false.** When a required safety fact is unknown, the drug is not silently
   treated as safe; the recommendation is withheld or flagged (§5).
7. **Every recommendation path is gated.** Ranked rows, summaries, strengths, and
   combination suggestions all consume the assessed eligible set (§9).
8. **Curated, sourced, no fabrication.** Taxonomy, mappings, rules, and anchors are curated
   artifacts (N6 batch pattern: evidence → approval → apply), not runtime guesses.
9. **Explicit absence.** "No eligible option found in the evaluated catalogue" is a
   first-class, scoped result — never a misleading "Best choice".
10. **One narrow slice first.** Ship fewer objectives completely rather than all 95 drugs
    partially calibrated (§12).

---

## 3. Proposed architecture — three states

```
request (objective + patient factors)
        │
        ▼
┌──────────────────────────────────────────────┐
│ STAGE 1 — ELIGIBILITY (binary, no scores)    │
│  a) objective match (curated mapping)        │
│  b) hard contraindication (global + specific)│
│  c) safety-assessment completeness           │
└──────────────────────────────────────────────┘
   │ eligible + safety-known        │ excluded[] (reason)
   ▼                                ▼
┌──────────────────────────────────────────────┐
│ STAGE 2 — RANKABILITY (evidence contract)    │
│  compatible evidence? ── no ──► eligible_unranked[]
│  yes                                          │
│  ▼                                            │
│  RANKING (efficacy + safety + pk + mechanism) │
└──────────────────────────────────────────────┘
        │
        ▼
  eligible_ranked[] + eligible_unranked[] + excluded[]
  + status + reasons[] + scoped summary
```

Three outcomes, not two:

| state | meaning | has overall score? |
|---|---|---|
| `eligible_ranked` | indicated, non-contraindicated, safety known, **compatible evidence** | yes |
| `eligible_unranked` | indicated, non-contraindicated, but **no compatible evidence** (or safety unknown) | **no** (null) |
| `excluded` | not indicated, or hard-contraindicated | no |

Stage 1 is a pure filter. Stage 2 is the existing scoring engine, but efficacy is driven by
the objective's **evidence contract**, and drugs that cannot satisfy it are not ranked.

---

## 4. Data model

### 4.1 Objective registry — `api/conditions.json` (new)

A small controlled vocabulary of **treatment objectives** (not disease labels). Each
objective is a distinct clinical question with its own evidence population and endpoint.
Not ICD-10 (too granular) and not SNOMED (licensing).

```jsonc
{
  "version": "1.0.0",
  "objectives": {
    "acute_pain": {
      "display": "Acute pain (symptomatic relief)",
      "eligible_classes": ["NSAID"],
      "evidence": {
        "outcome": "pain relief (50% reduction)",
        "unit": "NNT",
        "comparator": "placebo",
        "horizon": "6-12 h / short-term",
        "population": "acute nociceptive pain, adults",
        "dose_regimen": "standard analgesic dose",
        "source": "label / RCT",
        "transform": "nnt_lower_better",
        "anchor": { "best": 2, "worst": 6 }
      },
      "contraindication_rules": ["pregnancy_third_trimester"]
    },
    "erosive_esophagitis_healing": {
      "display": "Erosive esophagitis healing",
      "eligible_classes": ["PPI"],
      "evidence": {
        "outcome": "endoscopic healing (LA grade)",
        "unit": "percent healed",
        "comparator": "placebo / active",
        "horizon": "8 weeks",
        "population": "erosive esophagitis",
        "dose_regimen": "standard once-daily",
        "source": "label / RCT",
        "transform": "percent_higher_better",
        "anchor": { "best": 95, "worst": 50 }
      },
      "contraindication_rules": []
    },
    "reflux_symptom_relief": {
      "display": "Reflux symptom relief",
      "eligible_classes": ["PPI", "H2RA", "Antacid", "Alginate"],
      "evidence": {
        "outcome": "heartburn/regurgitation symptom relief",
        "unit": "NNT / symptom score",
        "comparator": "placebo",
        "horizon": "short-term",
        "population": "symptomatic GERD without erosive disease",
        "dose_regimen": "standard / as-needed",
        "source": "label / RCT",
        "transform": "nnt_lower_better",
        "anchor": { "best": 2, "worst": 8 }
      },
      "contraindication_rules": []
    }
    // … one objective per distinct clinical question; see §4.4 for the corrected split
  }
}
```

Notes:
- **`evidence` is the contract** (§7). Two drugs are comparable only if their evidence
  matches on outcome, unit, comparator, horizon, population, and dose/regimen.
- `eligible_classes` is a **lint check**, not clinical authority (review F10/F12). The gate
  is the per-drug mapping (§4.2).
- `contraindication_rules` here are **objective-specific additions**; global/subclass/drug
  rules live in the rule table (§5) and apply regardless of objective.
- `transform` + `anchor` are versioned, prospectively reviewed constants — never derived
  from the current catalogue distribution (review F10).

### 4.2 Drug → objective mapping (curated, one authoritative location)

**One authoritative, versioned mapping location** (review F10/F12): `api/condition_map.json`
(not "embedded or sibling"). Each drug gets an explicit disposition:

```jsonc
{
  "version": "1.0.0",
  "map": {
    "ibuprofen": { "objectives": ["acute_pain", "inflammatory_arthritis_symptoms", "dysmenorrhea"] },
    "omeprazole": { "objectives": ["erosive_esophagitis_healing", "reflux_symptom_relief", "h_pylori_regimen"] },
    "metformin": { "objectives": ["t2dm_glycemic_control"] },
    "sucralfate": { "objectives": ["peptic_ulcer_healing"], "note": "8-week outcome; not comparable to 4-week PPI endpoint" },
    "calcium-carbonate": { "objectives": ["reflux_symptom_relief"], "evidence_status": "symptomatic_only" }
  },
  "unsupported_in_v1": ["drug_id_a", "drug_id_b"]
}
```

- Every drug has an explicit disposition: mapped objectives **or** `unsupported_in_v1`
  (review F10). No drug is silently absent.
- Mapping is generated from the free-text `indications` via registry synonyms, then
  **human-reviewed**; the synonyms are a curation aid only, never evaluated at runtime.
- **Completeness invariant**: a coverage report asserts every drug is either mapped or
  explicitly unsupported; unmapped drugs surface in `excluded` with reason
  `unsupported_in_v1`, never silently dropped.

### 4.3 Evidence storage

Flat `l4_clinical` fields cannot represent different evidence for multiple
objectives/populations (review F10). Evidence is stored **by drug–objective–population**:

```jsonc
// api/evidence.json (new) — or a typed block per drug
{
  "omeprazole": {
    "erosive_esophagitis_healing": {
      "value": 92, "unit": "percent", "comparator": "placebo", "horizon_weeks": 8,
      "population": "erosive esophagitis", "dose": "20mg qd", "source": "label §14",
      "uncertainty": null
    }
  }
}
```

The existing `l4_clinical` fields remain for legacy consumers; the typed store is the
source of truth for scoped ranking. Migration is coordinated per objective (§7.4).

### 4.4 Corrected taxonomy (review F04)

The v1 synonym lists conflated clinically distinct contexts. v2 splits them:

| v1 (unsafe) | v2 (split) |
|---|---|
| `gerd` (symptoms + erosive esophagitis) | `reflux_symptom_relief` **and** `erosive_esophagitis_healing` |
| `t2dm` (T2DM + GDM + prediabetes) | `t2dm_glycemic_control`; GDM/prediabetes excluded from v1 |
| `af_stroke_prevention` (AF + mechanical valves) | `af_stroke_prevention`; mechanical valves excluded from v1 |
| `inflammatory_arthritis` (OA + RA) | `oa_symptom_management` **and** `ra_disease_modification` (separate populations) |
| `peptic_ulcer` (ulcer healing + H. pylori eradication) | `peptic_ulcer_healing` **and** `h_pylori_regimen` (regimen objective) |
| monotherapy vs adjunct | explicit `dose_regimen` in the evidence contract; adjunct-only drugs not ranked against monotherapy |

Unsupported populations/objectives are **excluded from v1**, not forced into a mapping.

---

## 5. Eligibility & safety

A drug is **eligible** for `(objective, patient)` iff:

1. `objective ∈ map[drug].objectives` (objective match), **and**
2. no **hard** contraindication rule applies, **and**
3. all **required patient inputs** for the applicable rules are known.

### 5.1 Rule applicability is global, not condition-local (review F05)

Contraindications attach to **drugs/subclasses**, not to objectives. A drug's hepatic or
ACEi/ARB-pregnancy contraindication must not disappear because it was queried under a
different indication. Evaluation order:

1. **Global rules** (apply to any objective): e.g. pregnancy category X, active liver
   disease, active bleeding.
2. **Subclass rules**: e.g. NSAID in third trimester; ACEi/ARB in pregnancy.
3. **Drug rules**: e.g. a specific drug's contraindication.
4. **Objective-specific rules**: genuinely indication-specific additions.

The same evaluator is shared across **all** request paths (scoped, legacy, combo).

### 5.2 Hard vs soft (unchanged from v1, still correct)

- **`contraindication_rules` (hard, gate)** — absolute contraindications only.
- **`caution_rules` (soft, penalty)** — risk stratification (high GI risk + NSAID, severe
  renal) stays in Stage 2 safety scoring.

### 5.3 Sourced rules and required inputs (review F06)

Coarse fields cannot establish all absolute contraindications. v2 requires:

- A **small, sourced declarative rule table** with explicit applicability, thresholds,
  exceptions, **required inputs**, and evidence references.
- **Required patient inputs added before enabling affected recommendations** (e.g. an
  active-bleeding field before an `active_bleeding` gate; a validated active-liver-disease
  field rather than "moderate/severe hepatic impairment").
- **Unknown ≠ false**: an unevaluable rule yields `unknown`, not `pass`. When a required
  safety fact is unknown, the drug is **not ranked** (it may appear in `eligible_unranked`
  with reason `safety_unknown`) and never recommended.
- Narrative/category fields (`pregnancy_safety`, `hepatic_safety`) are **evidence inputs
  requiring review**, not authoritative executable gates (review F11).

---

## 6. Response contract (versioned)

The current response uses `results` with row fields `name`, `class`, `combo_suggestions`
(review F12/F17). v2 defines **versioned** schemas and preserves legacy shape.

```jsonc
{
  "schema_version": "2.0",
  "query": { "...": "echoed, incl. objective" },
  "mode": "objective_scoped",              // or "legacy"
  "status": "ok",                          // ok | no_eligible | no_rankable | unsupported | incomplete_safety
  "eligible_ranked":   [ { "id": "...", "scores": {...}, "overall": 8.4, "evidence": {...} } ],
  "eligible_unranked": [ { "id": "...", "reason": "no_compatible_evidence" } ],
  "excluded":          [ { "id": "...", "reasons": [ { "rule": "pregnancy_third_trimester", "evidence": "..." } ] } ],
  "filter_effects":    { "class_filter": ["PPI"], "removed": 3 },
  "summary": "Best option among ranked candidates for <objective> in the evaluated catalogue …"
}
```

- **`eligible_unranked`** carries no overall score (review F02).
- **`excluded[].reasons[]`** is structured with stable rule IDs; all evaluated failures are
  returned, with one optional primary display reason (review F21). Passed / failed /
  unknown / unevaluated are distinguished.
- **Result-state semantics** (review F13/F18): `status` distinguishes
  `no_eligible` (none indicated/non-contraindicated), `no_rankable` (eligible but no
  compatible evidence), `unsupported` (objective not in v1), `incomplete_safety` (required
  inputs missing). Unknown objective/class IDs are **request errors**.
- **Summaries are scoped**: "No eligible option found in the evaluated catalogue/filter",
  never "no treatment exists". `filter_effects` reports class-filter removals separately
  from clinical exclusions.
- **Legacy compatibility**: `mode: "legacy"` preserves the `results` shape and required row
  fields (or an explicit adapter), so existing consumers keep working (review F12).

---

## 7. Evidence compatibility & calibration

### 7.1 The evidence contract (review F03/F09)

Matching an endpoint **key** is insufficient. Two drugs are comparable only if their
evidence matches on: **outcome definition, unit, comparator, horizon, population,
dose/regimen, source, uncertainty**. The registry's `evidence` block (§4.1) is that
contract; the typed store (§4.3) supplies per-drug values.

Ranking is restricted to drugs whose evidence satisfies the objective's contract. Drugs
that cannot satisfy it are `eligible_unranked` — **not** given a fallback endpoint and
**not** given a neutral score.

### 7.2 No cross-endpoint fallback, no neutral imputation (review F01/F02)

v1's fallback/neutral design is removed:

- **No per-drug cross-endpoint fallback** within a ranking. Mixing esophagitis healing,
  symptom-relief NNT, and an invented relief tier recreates RES-01 inside a narrower list.
  Distinct outcomes become **distinct objectives** with separate rankings; their overall
  scores are never merged and no cross-objective winner is declared.
- **No neutral efficacy score.** Missing evidence is not a number. The drug appears in
  `eligible_unranked` with null efficacy/overall and an explicit reason.

### 7.3 Transforms (review F10)

Each objective declares a **bounded, monotonic** transform with prospectively reviewed
clinical anchors and a version:

- `nnt_lower_better`: bounded (e.g. `max(0, min(10, 10 - (nnt - best) * k))`), with the
  upper bound explicit (v1's cited expression lacked one).
- `percent_higher_better`: bounded banded mapping with reviewed anchors.
- No dataset-min/max normalization. Transforms are versioned with the registry.

### 7.4 The three flat-5.0 classes — resolve by evidence validation, not new branches

(review F07/F08/F09/F16)

| class | v1 assumption | v2 action |
|---|---|---|
| **Antihypertensive** | `nnt_bp_control` present 33/33 → add branch | **Audit first.** Presence ≠ comparability. Define the BP-control endpoint fully (target, comparator, horizon, population) and approve an anchored transform; withhold ranking where the evidence cannot satisfy the contract. |
| **Diabetes** | `a1c_reduction_pct` "missing" | **Typed migration.** A1c data already exists under `nnt_bp_control.a1c_reduction` (semantic/type collision, not absence). Introduce a typed, versioned A1c endpoint preserving dose/source/units; use **absolute percentage-point** reduction, not healing bands; validate all 28 records and update consumers together. |
| **Anticoagulant** | `stroke_se_reduction_vs_warfarin` → add branch | **Split objectives.** Define separate AF stroke/systemic-embolism, VTE-treatment recurrence, and VTE-prophylaxis contracts with explicit horizons/comparators. Handle warfarin as a comparator without treating zero relative benefit vs itself as zero efficacy. Unsupported contexts stay unranked. |

### 7.5 Evidence-readiness matrix (review F16)

Before any objective ships, produce a **drug × objective × endpoint readiness matrix**:
eligibility, usable values, compatibility, provenance, ranking status. Audit absent, null,
malformed, and non-finite values separately. Note: all five PPIs have both
`ee_healing_8wk_pct` and `duodenal_ulcer_healing_4wk_pct` (v1's premise that some have only
the latter was wrong); the real gaps are Antacid/Alginate (no efficacy keys) and the
Mucosal Protectant's different outcome horizon (8-week vs the selected 4-week endpoint).

---

## 8. Back-compatibility & migration

- `objective` is **optional** in the request. Absent → `mode: "legacy"`.
- **Legacy is not a safety bypass** (review F06/F07): hard gates that can be evaluated are
  applied to legacy requests too. Without an explicit or unambiguously confirmed objective,
  legacy returns a **clarification / non-ranking** response — never a clinical winner.
- `drug_class` remains an optional **narrowing** filter inside the eligible set; its effect
  is reported in `filter_effects`.
- **Dated retirement milestone** for legacy mode; the minimum UI migrates with the first
  safe scoped release (not Phase 3).
- Versioned request/response schemas; legacy `results` shape preserved or adapted.

---

## 9. Closing every recommendation path (review F07/F08/F15)

Gating ranked rows is not enough. v2 brings all recommendation-bearing outputs inside the
safety boundary:

- **Combination suggestions** (`_get_combo_suggestions`, `server.py:524`): **disabled in the
  first scoped release** unless every component and the regimen pass objective,
  patient-safety, and combination checks. It currently selects from the global catalogue,
  ignores patient factors, and uses a fixed `gastritis_gerd` collection.
- **Mechanism scoring** (`_compute_mechanism`, `server.py:455`): currently treats
  Antihypertensive/Diabetes/Anticoagulant as statins, and `pain_type`/`cv_risk` can
  influence their mechanism scores (up to 20% of overall). v2 passes validated objective
  context through scoring and explanations; obsolete indication bonuses are removed;
  unsupported dimensions are disabled with documented weights.
- **Summaries, strengths, concerns**: generated only from the assessed eligible set; no
  excluded drug may reappear in any recommendation-bearing field.

---

## 10. UI changes (`api/query-tool.html`)

- Add an **objective selector** populated from a new read-only `GET /api/conditions`
  endpoint (review F22); keep the class checkbox group as an optional narrowing filter.
- Render three sections: **ranked**, **eligible but not ranked** (with reason), and
  **excluded** (with structured reasons).
- When `status` is `no_eligible` / `no_rankable` / `unsupported` / `incomplete_safety`,
  render the scoped message — never a best-choice card.
- `pain_type` becomes a sub-attribute of pain objectives (or is derived), not a top-level
  driver; non-pain requests are validated (review F12).

---

## 11. Test plan / acceptance criteria

1. **Gate tests**: ibuprofen + `acute_pain` + third-trimester → excluded; simvastatin +
   `acute_pain` → excluded (objective mismatch); omeprazole + `erosive_esophagitis_healing`
   → eligible; lisinopril + `hypertension` → eligible **only if** the evidence contract is
   satisfied.
2. **Hard vs soft**: high-GI-risk + NSAID → still eligible (penalized); pregnancy X statin →
   excluded.
3. **Global rule applicability** (review F05): a multi-indication drug is tested against the
   same contraindication under **every** mapped objective.
4. **Unknown safety** (review F06): a required input missing → `incomplete_safety` /
   `eligible_unranked`, never a silent pass.
5. **No fabricated evidence** (review F02): a drug with no compatible evidence appears in
   `eligible_unranked` with null overall and **cannot** win; assert the scorer is not called
   for excluded drugs.
6. **No cross-endpoint merge** (review F01): assert no response mixes two objectives'
   overall scores; distinct outcomes produce distinct rankings.
7. **Evidence compatibility** (review F03): assert ranking requires matching contract
   metadata, not just the field name.
8. **Recommendation leakage** (review F15): assert excluded drugs never appear in summaries,
   strengths, concerns, or combo suggestions; combo suggestions disabled in v1.
9. **Result-state semantics** (review F13): `no_eligible` vs `no_rankable` vs `unsupported`
   vs `incomplete_safety`; unknown IDs are request errors; `filter_effects` reported.
10. **Legacy safety** (review F06): legacy requests apply evaluable hard gates and return
    non-ranking output when the objective is absent.
11. **Back-compat**: legacy `results` shape preserved; the 352-query grid passes in legacy
    mode (compatibility, not resolution of RES-01/02).
12. **Taxonomy integrity**: every mapped objective exists; `eligible_classes` are real;
    no class/objective contradiction; every drug mapped or `unsupported_in_v1`.
13. **Evidence-readiness matrix** exists for every shipped objective.
14. `py_compile` clean; commit + QMS verification + trace.

---

## 12. Phasing & release gates (review F14/F19)

Implementation order is separated from **release approval**.

| phase | deliverable | release gate |
|---|---|---|
| **0** | **Evidence-readiness audit** + corrected taxonomy + one fully-supported objective's mappings | audit reviewed; objective evidence contract approved |
| **1** | Eligibility + safety (global rules, required inputs, unknown handling) + versioned response contract | safety gate: excluded/unknown drugs cannot be recommended |
| **2** | Evidence-compatible ranking for the one objective + typed endpoint migration | **riskiest phase** (review F14): calibration + compatibility gate |
| **3** | UI + `/api/conditions` + grid update + legacy retirement milestone | joint safety + calibration + UI gate |

- **Phase 2 is the greatest evidence/calibration risk**, not a mechanical follow-on.
- **Release one narrow vertical slice** containing taxonomy, gates, compatible scoring,
  response/UI handling, and tests — not gate-only deployment followed by old scoring.
- Broader taxonomy, generic rule machinery, and fallback frameworks wait; essential safety
  inputs and clinical sourcing do not.

---

## 13. Adjacent findings (corrected per review)

The review verified several v1 claims about adjacent findings; corrected status:

| finding | v1 claim | corrected status |
|---|---|---|
| `_norm_preg` maps "not contraindicated" → X | open | **already fixed** (`server.py:100-115` checks `"not " + frag`); broader narrative parsing still unsuitable as a hard-gate basis |
| RES-04 literal-`"none"` truthiness | open | **already fixed** (`server.py:484-491`, `:169-183`); the separate non-NSAID fall-through into statin mechanism logic **remains open** |
| `special=None` / `selectivity=None` abort queries | open | **already fixed** (`server.py:366-451`, `:454-491`); `None` entries in `indications` **remain unsafe** (`server.py:158-161`) |
| duplicate "High DDI burden" concerns | open | **already fixed** (`server.py:640-657`) |
| hepatic `contraindicated` blanket `-6` | stated | **severity-dependent**: `-6` moderate/severe, `-3` mild (`server.py:292-303`); the substantive point (penalties not gates) stands |

Still open and out of N6b scope: RES-03 (combo context), the non-NSAID mechanism
fall-through, `None` indication entries, and broader narrative parsing.

---

## 14. Open questions

1. **Initial objective scope** — which single objective ships first? (Recommend a
   well-evidenced one, e.g. `erosive_esophagitis_healing` or `acute_pain`.)
2. **Required patient inputs** — which fields must be added before which gates (active
   bleeding, active liver disease)?
3. **Contraindication sourcing** — the sourced rule table needs a curation round; who owns
   it and what is the evidence bar?
4. **Typed evidence store** — `api/evidence.json` vs a typed block per drug; migration of
   the 28 Diabetes records and the 6 anticoagulant records.
5. **Legacy retirement date** and the minimum UI migration.
6. **Population calibration** — RES-01 says "within indication and population"; v2 scopes
   by objective and encodes population in the evidence contract. Confirm that is sufficient
   or whether a separate population-adjustment layer is needed.
7. **Transform anchors** — who sources and reviews the clinical anchors, and how are they
   versioned?
8. **Combination therapy** — when (if ever) to re-enable combo suggestions, and under what
   regimen-level gate.

---

## 15. Non-goals

- No change to L3 extraction, templates, or the N6 curation artifacts.
- No new drug classes (that is N7).
- No generalized rules DSL or ontology service (review F10/F12: not needed for v1).
- No implementation in this document.

---

## 16. Review disposition (GPT-6 Astra, run 3914507)

| id | sev | v2 disposition |
|---|---|---|
| F01 | critical | §7.2 — cross-endpoint fallback removed; distinct outcomes become distinct objectives, never merged |
| F02 | critical | §3, §6, §7.2 — `eligible_unranked` state; no neutral imputation; eligibility ≠ rankability |
| F03 | critical | §4.1, §7.1 — typed evidence contract (outcome/unit/comparator/horizon/population/dose/source/uncertainty) |
| F04 | critical | §4.4 — taxonomy split (GERD symptoms vs erosive esophagitis; T2DM vs GDM/prediabetes; AF vs mechanical valves; OA vs RA; ulcer healing vs H. pylori; mono vs adjunct) |
| F05 | critical | §5.1 — global/subclass/drug rules evaluated independently of objective; shared evaluator |
| F06 | critical | §5.3 — sourced rule table, required inputs, unknown ≠ false, withhold recommendation |
| F07 | critical | §8, §9 — legacy applies hard gates; no objective → non-ranking; combo suggestions disabled |
| F08 | critical | §9 — all recommendation paths gated |
| F09 | major | §7.1 — evidence contract per objective |
| F10 | major | §4.2 — one authoritative versioned mapping location; class lists as lint; `unsupported_in_v1` |
| F11 | major | §5.3 — subclasses/exceptions curated; narrative/category fields as evidence inputs |
| F12 | major | §6, §8 — versioned request/response schemas; legacy `results` preserved/adapted |
| F13 | major | §6 — result-state semantics; unknown IDs are errors; scoped summaries |
| F14 | major | §12 — evidence-readiness audit first; narrow vertical slice; Phase 2 riskiest |
| F15 | major | §11 — evaluator-not-called, unknown-input, missing-evidence-cannot-win, leakage tests |
| F16 | major | §7.5 — evidence-readiness matrix; corrected PPI premise; Antacid/Alginate + Mucosal horizon gaps |
| F17 | major | §6, §8 — API/consumer compatibility |
| F18 | major | §6 — result-state semantics |
| F19 | major | §12 — release sequencing |
| F20 | major | §11 — acceptance coverage |
| F21 | minor | §6 — structured `reasons[]`; passed/failed/unknown/unevaluated |
| F22 | minor | §10 — `GET /api/conditions`; versioned config artifact |
| F23 | minor | §7.1/§7.3 — cross-references corrected (transforms are §7.3) |
