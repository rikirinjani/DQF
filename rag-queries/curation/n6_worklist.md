# N6 — Sourced Adjudication Backlog: Worklist & Source Plan

> Generated 2026-09-29. Every value change in N6 follows the E1 sourcing pattern
> (`label_sourcing_e1.json`): verbatim quotes sliced from fetched sources, never
> retyped; absence of evidence = keep current + document, never fabricate.
>
> **COMPLETE 2026-10-02** — batches N6.1–N6.5 all applied and pushed
> (scorecard: 2a = 6 changes, 2b = 11, 3 = 0 changes/35 keeps, 4 = 9 changes +
> 45 keeps, 5 = policy + 2 HR fixes; every batch evidence-committed first,
> user-approved, verified 352-query grid + suites green).

---

## 1. Inventory

| # | Category | Count | Source of record | Item shape |
|---|----------|-------|------------------|------------|
| A | N1-demoted proposals (batch5) | 25 | `curation/batch5_rescore_adjudication.json` → `demoted_to_open_questions` (group + demotion reason) | drug\|dim, proposed change, why the basis failed vetting |
| B | Conflicts with prior adjudication | 44 | `curation/batch5_rescore_draft.json` → `conflicts_with_prior_adjudication` (keys incl. `prior_source`, `why`) | drug\|dim where batch5 evidence disagrees with the E1 42-cell adjudication |
| C | Pre-existing open questions | 44 | `curation/batch5_rescore_draft.json` → `open_questions` (keys incl. `question`) | drug\|dim + question text |
| D | Unapplied batch4 raises | **32** of 54 | `rag-queries/batch4_rescore.json` → `results`, diffed vs `api/drugs.json` (N6.1) | 22 already applied, 0 superseded |
| E | Unapplied ddi changes | **14** of 37 | `rag-queries/ddi_rescore.json` → `changes`, diffed (N6.1) | 15 applied, **8 superseded** (later merges moved them differently — treat as close-or-re-propose) |
| F | String-typed heart_rate_effect cells | **33** | `curation/n6_worklist.json` → `F_heart_rate_effect_strings` (full-corpus scan; batch5 saw only 25 in its 89-drug scope) | distinct values: {bradycardia, tachycardia, none}; beta-blocker bradycardia = real class effect, DHP-CCB entries = artifacts |

> **Machine-readable worklist:** `curation/n6_worklist.json` (N6.1 output) — all
> categories with current values embedded; the authoritative counts. The earlier
> "22 unapplied proposals (12+10)" figure in TODO Known Debt was an undercount
> of what N4 profiles happened to document; the diff is ground truth.
| G | Named specials | 4 | see §4 | lovastatin NNT, metformin hypo, amlodipine HR attribution, AH template wording |
| H | Policy: merge lock semantics | 1 | re-assessment REG-02/RES-03 | `DEFAULT_LOCKED_FIELDS` + deletion-respecting merge |

Total items: **~135 cells + 2 policy decisions + 1 design item (N6b, tracked separately in TODO).**

**Mechanical first step (D/E):** diff proposals against current `api/drugs.json` —
a proposal is "unapplied" iff current value ≠ proposed value (some may have been
overtaken by later merges). Script this; do not hand-count.

---

## 2. Sourcing route (E1 pattern, priority order)

1. **FDA label via DailyMed SPL** — verbatim quote + setid + section (route:
   `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml`).
   Highest authority for risk/tolerability dims. E1 setids for anticoagulants
   already in `label_sourcing_e1.json`; others resolved per drug at fetch time.
2. **PMID from the drug's own `_evidence.pmids` pool** — for RCT/meta-analysis
   dims (cv_outcome_benefit, renal_protection, weight_effect). Basis sentences
   must come from that pool (batch5 verification pattern: no evidence changes
   needed when the PMID is already in-pool).
3. **Class-label consensus** — only when 1–2 fail and the class label text is
   identical across member drugs (e.g. class warnings section). Must be quoted,
   not paraphrased.

Every sourced cell records: `cell, drug, dim, label{setid,url} or pmid, quote,
section, numbers_found, status(sourced|not_found), note` — same schema as
`label_sourcing_e1.json`.

---

## 3. Decision rules (carried from N1 vetting + re-assessment additions)

- **Raise** needs ≥2 independent supporting sentences (or 1 verbatim label
  quantifier). **Drop** needs the basis to actually negate the dimension —
  N1 demoted 8 proposals whose bases *affirmed* the current value.
- Wrong-drug / wrong-dimension bases (metformin text for ertugliflozin,
  HbA1c text for weight_effect) are **not re-usable** — discard, source fresh.
- Conflicts (B): the prior E1 adjudication wins **unless** the new evidence is
  a quantified label/RCT statement and the prior basis was narrative — record
  the tie-break reason per cell.
- `not_found` after full-label search = keep current value, log the note
  (enoxaparin `gi_bleeding_risk` precedent in `label_sourcing_e1.json`).
- **Batch-6 guardrails now in force:** gi coalesce means anticoagulant
  `gi_bleeding_risk` values directly drive GI penalties — adjudicate those
  cells before any anticoagulant scoring regression run.

---

## 4. Named specials

| Item | Current state | Action |
|------|--------------|--------|
| lovastatin `nnt_mace_5yr` | null; API falls back to neutral 5.0 (crash fixed `fde0203`) | ✅ **N6.4** — LIPID 3.5% vs 5.5% arithmetic on label rates → `{value: 50, ci_95: null, dose: "20-40mg"}` (`1da2dd4`) |
| metformin `hypoglycemia_risk` = 3 | monotherapy hypo risk is low (label: "hypoglycemia uncommon with monotherapy") | ✅ **N6.2a** — DailyMed 5.3 combo-only hypo + 6.1 1–5pct band → 3→1 (`278fccd`) |
| amlodipine bradycardia attribution | traced to template noise (bradycardia query removed `667fd49`) | ✅ **N6.4** — label adjudication: bradycardia→none (`1da2dd4`); enalapril/ramipril suspects likewise fixed in **N6.5** |
| AH template wording | bradycardia removed; **cough/angioedema are ACEi effects, edema is CCB** — one generic query mixes class-incompatible effects | ✅ **N6.5** — shared stem `{drug} side effect` applied (approved option A); per-subclass split deferred to R1 |

---

## 5. Policy decisions (no sourcing needed)

1. **Merge lock semantics (H):** ✅ **DECIDED N6.5 (approved option B)** —
   `DEFAULT_LOCKED_FIELDS` = the 6-dim worklist candidate ∪ every l3 dim
   actually adjudicated in N6.1–6.4 = **25 fields** (`nnt_mace_5yr` excluded,
   it is l4_clinical). Deletion-respecting list merge implemented: locked
   check hoisted before type branches — a locked list with a non-empty expert
   value is kept verbatim, never `expert + incoming` (expert deletions now
   survive re-merges). Rescore flows unlock explicitly: `--unlock field1,field2`
   or `--unlock-all`. Tests: `rag-queries/test_merge_lock.py` (8/8).
2. **heart_rate_effect typing (F):** ✅ **DECIDED N6.5 (approved option b)** —
   keep descriptive string (bradycardia/tachycardia/none) + formally exclude
   from scoring; documented in `classifier_audit.DIM_DIRECTION`. No scorer
   consumes it (server.py has no heart_rate consumer; research-only:
   build_l2b_digests). Option (a) numeric mapping rejected: needs a sourced
   direction for all 33 cells — no sourcing round this arc. The two
   class-inconsistent suspects (enalapril bradycardia, ramipril tachycardia)
   were label-sourced and fixed to none in N6.5 (`n6_batch5_policy.json`).
3. **Holds triage:** 192 holds stay held unless a category A–E pass surfaces
   their group — no dedicated sourcing round this arc.

---

## 6. Batch plan (priority = clinical impact on scoring)

| Batch | Contents | Est. |
|-------|----------|------|
| N6.1 | Mechanical: unapplied-proposal diff (D/E) + worklist JSON assembly | ½ d |
| N6.2 | High-impact risk cells first: hypoglycemia_risk, gi_risk/gi_bleeding_risk, bleeding, ddi drops (metformin special included) | 2–3 d |
| N6.3 | Benefit cells: cv_outcome_benefit, renal_protection/benefit, weight_effect (25 demoted + conflicts in these dims) | 2–3 d |
| N6.4 | Tolerability + remaining dims (gi_tolerability, raft_strength, reflux_suppression, barrier_protection, myopathy_risk, electrolyte_risk…) + lovastatin NNT + amlodipine re-pull | 2–3 d |
| N6.5 | Policy: lock semantics implementation + heart_rate_effect typing + template wording split | ✅ **done 2026-10-02** (evidence `9b8c85f`, apply pending this commit) |
| — | Each batch: source JSON (`label_sourcing_n6_batch<k>.json`) → user review → `merge_l3` apply → grid+suite verification → commit | — |

**Gate:** batches 6.2–6.5 each end with a summary of proposed changes for user
approval before anything touches `api/drugs.json` (N1 pattern: APPROVED marker
in the adjudication file). ✅ All gates observed.
