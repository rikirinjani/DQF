# Phase 1 — Antiplatelet class (E2): definition + template/scorer design (draft for review)

Scope: define the new `Antiplatelet` class (clopidogrel, ticagrelor, prasugrel) and design the
L3 pipeline wiring (templates, scorer, audit directions, salt vocabulary) so evidence can be
fetched and scored. Implementation is mechanical once this draft is approved.

**Prerequisite (Phase 0): the 3 drug records do not yet exist in `api/drugs.json`** (verified
2026-09-28: only aspirin, class NSAID). They must be added first with `l3_systems: {}` —
mirroring E1 Phase 1 (`da124aa`, 6 anticoagulant records). Aspirin stays in NSAID; reference
only, not part of E2.

Design principle (from Batch 4 / E1): dim **direction** is declared up front and carried in
`classifier_audit.DIM_DIRECTION`, so the artifact gate works on day one.

---

## 1. Class definition

| drug | sub-class | activation profile | key label facts |
|---|---|---|---|
| clopidogrel | thienopyridine prodrug | CYP2C19-dependent activation (boxed warning: poor metabolizers) | boxed warning CYP2C19 LOF; omeprazole/esomeprazole reduce activation |
| ticagrelor | cyclopentyltriazolopyrimidine | **not a prodrug** — active parent + CYP3A4-formed active metabolite (AR-C124910XX); reversible binding | dyspnea adverse effect; no routine monitoring |
| prasugrel | thienopyridine prodrug | faster, more complete activation (CYP3A4/CYP2B6); less CYP2C19-dependent | contraindicated prior TIA/stroke; caution age ≥75, weight <60 kg |

Class-level contrast intended by the dim set: clopidogrel scores **high** on
`prodrug_activation_dependence` (boxed warning), ticagrelor **low** (direct-acting); all three
score **low** on `reversal_availability` (no specific antidote — unlike anticoagulants with
andexanet/idarucizumab) and **low** on `monitoring_burden` (no routine monitoring — unlike
warfarin INR).

## 2. Proposed L3 dim set (7)

| dim | direction | keyword/audit rationale | source of truth |
|---|---|---|---|
| `platelet_inhibition_efficacy` | benefit | P2Y12/ADP-mediated aggregation inhibition; outcome evidence = MACE, stent thrombosis, CV death | FDA labels; PLATO, TRITON-TIMI 38, CAPRIE, CREDO |
| `bleeding_risk` | risk | major bleeding, TIMI/BARC types, hemorrhage | FDA labels; RCT bleeding endpoints |
| `prodrug_activation_dependence` | risk | CYP2C19 LOF, poor metabolizer, prodrug activation, active metabolite formation | FDA label boxed warning; CPIC guidance |
| `ddi_risk` | risk | CYP3A4 (ticagrelor substrate + weak inhibitor), CYP2C19 inhibitors (omeprazole), aspirin/NSAID coadministration | FDA labels |
| `monitoring_burden` | risk | platelet function testing (VerifyNow), routine monitoring — expect flat low | FDA labels |
| `reversal_availability` | benefit | reversal, antidote, platelet transfusion, bentracimab (investigational) — expect low | FDA labels |
| `gi_bleeding_risk` | risk | upper GI bleeding, dyspepsia, GI hemorrhage | FDA labels; RCT GI endpoints |

**Renal dependence deliberately excluded**: no dose adjustment exists for any of the 3 — the
evidence would be flat/low and add noise. Revisit post-triage only if sourced evidence emerges
(open question §8).

## 3. `rag-queries/l3_query_templates.json` — add class entry (to implement later)

```json
"Antiplatelet": {
  "tissue_sites": ["vasculature", "gastrointestinal tract", "liver"],
  "tissue_queries": [
    "{drug} P2Y12 receptor platelet aggregation inhibition mechanism",
    "{drug} active metabolite CYP2C19 CYP3A4 activation pharmacokinetics",
    "{drug} hepatic metabolism drug interaction",
    "{drug} gastrointestinal bleeding mucosal effect"
  ],
  "off_target_queries": ["{drug} {target} off-target effect"],
  "class_mechanism_queries": [
    "antiplatelet major bleeding TIMI BARC randomized trial",
    "antiplatelet reversal platelet transfusion antidote",
    "antiplatelet platelet function testing monitoring requirement",
    "{drug} major adverse cardiovascular events stent thrombosis prevention"
  ],
  "l3_fields": {
    "platelet_inhibition_efficacy": null,
    "bleeding_risk": null,
    "prodrug_activation_dependence": null,
    "ddi_risk": null,
    "monitoring_burden": null,
    "reversal_availability": null,
    "gi_bleeding_risk": null
  }
}
```

All three drugs bind P2Y12, so `{target}` off-target probes resolve to the P2Y12 receptor
entry once L1 targets are populated; `build_l3_queries` handles the empty fallback.

## 4. `rag-queries/extract_l3.py` — scorer block plan (describe only, do not implement)

Add `elif drug_class == "Antiplatelet":` (umbrella: thienopyridine prodrugs + reversible
P2Y12). All 7 dims use `_score_risk` (no custom scorer needed), with keyword families per §2.

Scorer design notes (non-obvious choices, mirroring E1):

1. **`pk_contexts` deliberately EMPTY for `prodrug_activation_dependence` and `ddi_risk`.**
   There, "activation"/"interaction" *is* the evidence; the pk_context gate would skip every
   relevant sentence. It is set only on `platelet_inhibition_efficacy` (PK statements must not
   count as outcome evidence).
2. **No `adverse_context_terms` on risk dims.** For `bleeding_risk`/`gi_bleeding_risk` the
   harm mention is the evidence.
3. **`monitoring_burden` is risk-typed** (higher = worse) and expected to score flat-low for
   this class — triage will matter more than usual (same caveat as E1).
4. **`ddi_risk` carries `negations=["limited","few"]`** (consistent with the other 10 classes).
5. Intended contrasts (§1): clopidogrel high / ticagrelor low on
   `prodrug_activation_dependence`; all three low on `reversal_availability` and
   `monitoring_burden`.

## 5. `rag-queries/classifier_audit.py` — `DIM_DIRECTION` additions

```python
    "platelet_inhibition_efficacy": "benefit",
    "bleeding_risk": "risk",
    "prodrug_activation_dependence": "risk",
    "monitoring_burden": "risk",
    "reversal_availability": "benefit",
    "gi_bleeding_risk": "risk",
    # "ddi_risk": "risk"  (already present)
```

## 6. Salt vocabulary (`extract_l3.py`)

Names are **auto-covered**: `_build_salt_name_re()` reads `load_drugs()`, so clopidogrel /
ticagrelor / prasugrel (salt-free base ids) are masked automatically once records exist.
`_SALT_ANIONS` already contains `sulfate|sulphate` and `etexilate|tosilate` — but **not
`bisulfate`**: "clopidogrel bisulfate" (USP salt name) would not be masked and could leak into
keyword matching. **Add `bisulfate`** to the anion alternation.

```python
    r"etexilate|tosilate|bisulfate|"           # <- extend here
```

Guard check: `_SALT_KEEP_PREFIXES` already contains `renal|hepatic|gastrointestinal|...`, so
"renal clearance" etc. are not consumed by the generic drug+suffix rule.

## 7. Batch-triage plan (mirrors Batch-6 anticoagulant run)

- **Batch number**: next available (Batch-7) — Batch-5 was full-corpus, Batch-6 anticoagulants.
- **Kernel**: Kaggle script-type (`kernel_type: script`), GPU on, internet on; input fetched
  from GH raw master → **push-before-run is a hard prerequisite**.
- **Staging**: `rag-queries/kaggle/kaggle-push staging` procedure (Option B CLI push) with
  staged `kernel-metadata.json`; slug `rikirinjani/dqf-antiplatelet-triage-batch-7`.
- **No live logs** for script kernels — status polling + output pull only.
- **Validation script** (same shape as batch5): group/sentence counts vs pool, label
  distribution (`strong/moderate/negative/none`; `ddi_risk` → `pk/pd/none`), 0 missing /
  0 length mismatch gate before adjudication.

## 8. Adjudication rule sketch

Two families (E1 pattern) + sourced-override layer:

- **`ddi_risk`**: pk/pd/none family — keep pk/pd, drop none, re-run `_score_risk` (R7). Empty
  filtered pool → null (R6).
- **Other 6 dims**: strength labels on audit-clean counts — R0 empty→null, R5 all-none→null,
  R1a/R1b/R1c clean strong, R4 all-flagged→null, R2 moderate-only→cap 2, R3 negative→1.
- **Sourced-override layer**: a label/PMID field already sourced in `api/drugs.json` beats the
  keyword score when the pool is empty or contradicted.

**Batch-5 lesson (mandatory)**: single-none-sentence drops are dangerous — the mechanical rule
converted mislabeled sentences into drops that contradicted their own cited text (ibuprofen
`gi_risk` 3→1 from a GI-bleeding OR study labeled "none"; sucralfate `barrier_protection`
3→1 from a sentence affirming mucoprotection). The adjudication pass must **check every basis
sentence**; drops resting on one none-labeled sentence that contradicts its own text are
demoted to open questions, never auto-applied.

## 9. Fetch plan

- FDA labels via DailyMed v2 SPL route:
  `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml` (openFDA `spl_set_id`
  search 404s — known dead route).
- PMIDs from the class RCTs (PLATO, TRITON-TIMI 38, CAPRIE, CREDO) + label-cited studies.
- Cap any fetching at ~10 minutes per drug; otherwise leave null + query plan.
- Every value sourced or null — never invent.

## 10. Open questions

- **Phase 0**: 3 drug records must be added to `api/drugs.json` (`l3_systems: {}`) before any
  template/scorer wiring — mirror E1 Phase 1 (`da124aa`). L1/L4 values for the new records
  (P2Y12 Ki, NNT/HR) are a separate fetch.
- **L1 target potency**: P2Y12 binding-assay Ki values are sparse/inconsistent in literature —
  expect nulls; do not fabricate.
- **Ticagrelor dyspnea**: distinctive adverse effect with no L3 dim — fetching it adds pool
  noise (relevance gate). Open question whether a respiratory dim should exist; for now
  dyspnea text is not probed.
- **`monitoring_burden` / `reversal_availability`** expected flat-low — if triage proves noisy,
  fold into a `note` field (E1 precedent).
- **Prasugrel special populations** (prior TIA/stroke contraindication, age ≥75, weight
  <60 kg) — L4/label facts with no L3 dim; captured in the spec's safety queries only.
- **Renal dependence** excluded from the dim set — revisit post-triage if sourced evidence
  emerges.

## 11. Acceptance criteria

1. Phase 0 done: 3 records in `api/drugs.json` with `l3_systems: {}`.
2. Template entry present; `build_l3_queries` returns the antiplatelet probes.
3. Scorer block present; all 7 dims scored by `_score_risk`; `py_compile` clean.
4. Unit tests pass (extend `rag-queries/test_scorer_hardening.py` or add
   `rag-queries/test_antiplatelet_scorer.py`):
   - clopidogrel "CYP2C19 poor metabolizer" sentence → `prodrug_activation_dependence` >= 2
   - ticagrelor "not a prodrug / direct-acting" sentence → `prodrug_activation_dependence` <= 2
   - "no routine monitoring" → `monitoring_burden` = 1
   - "no specific antidote" → `reversal_availability` = 1
   - salt masking: "clopidogrel bisulfate" does not leak into a keyword
   - `pk_contexts` guard: a pure PK sentence scores 1 on `platelet_inhibition_efficacy`
5. `DIM_DIRECTION` covers all 7 dims.
6. Commit + QMS verification + trace.
