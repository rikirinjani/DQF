# DQF Roadmap — Clinical Tool

> *Pharmacist-built, evidence-grounded, patient-personalized drug ranking.*
> **Last refreshed 2026-09-29** — external-audit round complete: 10-fix batch + null-safety sweep (`fde0203`), re-assessment + Batch-6 (`667fd49`). N6 next.

---

## Current State (verified 2026-09-27)

| Metric | Value |
|--------|-------|
| Drugs | **95** across **10 classes** — Antihypertensive 33, Diabetes 28, NSAID 10, Statin 6, Anticoagulant 6, PPI 5, H2RA 3, Antacid 2, Alginate 1, Mucosal Protectant 1 |
| L3 coverage | 95/95 drugs; 798 numeric cells, 50 documented nulls (NSAID 24, Statin 20, H2RA 5, Anticoagulant 1); **N1 applied 2026-09-28** — 11 vetted changes (8 raises, 3 drops), 25 demoted to open questions |
| L4 coverage | 95/95, class-specific schema locked in `api/l4_schema_map.json` |
| Profile docs | **94** — `profiles/` (4), `profiles-statins/` (7, incl. lovastatin), `profiles-gi/` (13), `profiles-anticoagulants/` (7), `profiles-antihypertensives/` (34), `profiles-diabetes/` (29) |
| Validation | 8 reports + **V3 instrument** (`v3-scenarios.json` 12 scenarios/57 items, `v3-inter-rater-protocol.md`, `v3_rater_sheet.md`, `v3_agreement.py`) — results pending real raters |
| Scorer tests | 46 checks passing — `python rag-queries/test_scorer_hardening.py` (22) + `test_anticoagulant_scorer.py` (24) |
| LLM triage | Batches 1–6 run; **Batch 5 full corpus landed 2026-09-27** (413 groups / 2573 sentences / 905 kept); Batch-7 (antiplatelet) planned in N2 design |
| External audit | **2-round Kaggle LLM audit** — 10 fixes + null-safety sweep (`fde0203`); re-assessment `dqf-reeval` (Gemini full 12/14 CORRECT, score 1.0) → **Batch-6** (`667fd49`): anticoagulant GI coalesce, pregnancy negation guard, concerns normalization, NNT neutral fallback, template fixes. Grid 352/0, all suites green |
| Latest commit | `667fd49` on `master`, pushed |

---

## Immediate — Next

| # | Task | Why | Est. |
|---|------|-----|------|
| N1 | **Consume `rag-queries/batch5_verdicts.json`** — rescore/adjudicate the non-anticoagulant evidence pools | ✅ **done 2026-09-28** (`767d1d9`) — 11 vetted changes applied, 25 demoted, audit in `batch5_rescore_adjudication.json` | — |
| N2 | **E2 — Antiplatelets** Phase-1 design: clopidogrel, ticagrelor, prasugrel | ✅ **design done 2026-09-28** (`cafe082`) — 7-dim L3 set, template/scorer plan, Batch-7 triage plan, 3 drug specs; Phase 0 (drug records) + Phase 2 (wiring) pending | — |
| N3 | **Inter-rater reliability (V3)** instrument | ✅ **instrument done 2026-09-28** (`1a2716d`) — 12 scenarios, protocol, rater sheet, agreement script (self-test passes); S04 refreshed post-N1 | — |
| N4 | **Profile docs for Antihypertensive + Diabetes** (+ lovastatin) | ✅ **done 2026-09-28** (`3612e16`) — 64 files, generator-assisted, no fabrication | — |
| N5 | **HF RAG endpoint** — moved to AWS per user decision | ❌ cancelled | — |
| N5b | **External audit batch** — 10 verified findings + null-safety sweep | ✅ **done 2026-09-29** (`fde0203`) — grid 352/0, suites pass | — |
| N5c | **Re-assessment (`dqf-reeval`) + Batch-6** — dual-model verification, then apply findings | ✅ **done 2026-09-29** (`667fd49`) — Gemini 12/14 CORRECT; 11 changes: GI coalesce, pregnancy negation, concerns normalization, NNT neutral 5.0, bradycardia template fix (R-13 resolved) | — |
| N6 | **Sourced adjudication backlog** — 25 N1-demoted proposals + 44 conflicts + 44 open questions + 22 unapplied prior-rescore proposals; **now also:** merge lock policy (`DEFAULT_LOCKED_FIELDS` + deletion-respecting merge), template wording review (cough/angioedema are ACEi effects in the generic AH query), lovastatin `nnt_mace_5yr` sourcing, metformin `hypoglycemia_risk` review, amlodipine bradycardia attribution (data-traced to template noise) | Needs label/PMID sourcing per cell (E1 pattern) | 1–2 wk |
| N6b | **Indication-boundary design** — any-class queries compare pain NNT vs CV NNT vs GI healing; needs target-condition field + eligibility gate before scoring | Deep redesign surfaced by re-assessment (RES-01/RES-02); design first, implement in S-arc | design 2–3 d |
| N7 | **E2 Phase 0+2** — add 3 antiplatelet drug records, wire template/scorer/`DIM_DIRECTION`, run Batch-7 triage | Design approved in N2; unblocks E2 completion | 1–2 wk |

**Validation note:** Phase V is now V1 ✅ · V1b ✅ · V1c ✅ (×2) · V2 ✅ · V4 ✅ · holdouts ✅ · **V3 instrument ✅, results ⬜** (blocked on real raters).

---

## Mid-Term (3–6 months)

### Drug Coverage Expansion

| # | Class | Drugs | Status |
|---|-------|-------|--------|
| E1 | **Anticoagulants** | warfarin, apixaban, rivaroxaban, edoxaban, dabigatran, enoxaparin | ✅ **done 2026-09-27** — 42-cell adjudication merged, profiles written |
| E2 | **Antiplatelets** | aspirin, clopidogrel, ticagrelor, prasugrel | 🟡 Phase-1 design done (N2); Phase 0 (records) + Phase 2 (wiring) + Batch-7 → N7 |
| E3 | **Antihypertensives** | lisinopril, losartan, amlodipine, metoprolol, HCTZ, chlorthalidone | ✅ records + L3/L4 + profile docs done (33 drugs, N4) |
| E4 | **Diabetes** | metformin, empagliflozin, dapagliflozin, semaglutide, tirzepatide, insulin glargine | ✅ records + L3/L4 + profile docs done (28 drugs, N4) |
| E5 | **Antidepressants** | escitalopram, sertraline, venlafaxine, bupropion, mirtazapine | ⬜ 🟡 Medium |
| E6 | **Antibiotics** | amoxicillin, doxycycline, azithromycin, ciprofloxacin, TMP-SMX | ⬜ 🟡 Medium |

Each new class = 5–8 records + L3 scorer dimensions + profile docs + validation. The E1 pipeline (evidence harvest → specs → template + 7-dim scorer → Batch-6 triage → adjudication → `merge_l3 --only` → profiles) is the repeatable playbook.

### RAG Evidence Queries

| # | Task | Status |
|---|------|--------|
| R1 | Per-class curated PubMed queries in `rag-queries/{class}/` | ⬜ — queries currently live in `extract_l3.py` templates, not per-class dirs |
| R2 | Evidence summary doc linking each score component to citations | ⬜ (profiles carry per-cell citations already) |
| R3 | Inline citation display in query tool (hover → evidence) | ⬜ — `api/query-tool.html` + `server.py` `/api/query` exist, no drill-down |

### Scoring Engine Maturation

| # | Improvement | Status |
|---|-------------|--------|
| S1 | **DDI penalty** — regimen-aware interaction penalty between ranked drugs and existing meds | 🟡 partial — `server.py` penalizes `ddi_risk` ≥ 2/3 and `regimens.json` exists (3 regimens, conditions), no full interaction matrix |
| S2 | **Renal/hepatic penalty** — granular CKD stages (currently binary) | ⬜ |
| S3 | **Age-specific efficacy** | ⬜ |
| S4 | **Pregnancy/lactation** sub-score with trimester-specific adjustments | ⬜ (per-drug `pregnancy_safety`/`lactation_safety` fields already populated) |

### Tool Usability

| # | Feature | Status |
|---|---------|--------|
| U1 | **PDF report** — patient profile → ranked list → citations | 🟡 partial — `build_pdf_fpdf*.py` cover NSAID/statin PoC only |
| U2 | **Scenario comparison** — side-by-side patient profiles | 🟡 partial — `regimens.json` supports conditions; no UI comparison |
| U3 | **Score drill-down** — click score → data + calculation | ⬜ |
| U4 | **Mobile responsive** query tool | 🟡 partial — responsive CSS present, untested |

---

## Long-Term (6–12 months)

### Personalization

| # | Feature |
|---|---------|
| P1 | **CYP genotype input** — CYP2C19, CYP2C9, CYP3A4, CYP2D6 metabolizer dosing adjustments |
| P2 | **Weight/BSA-based dosing** — enoxaparin, vancomycin, etc. |
| P3 | **Organ function integration** — real CrCl / eGFR / MELD instead of categorical normal/mild/moderate/severe |

### Full Prescription Analysis

| # | Feature |
|---|---------|
| F1 | **Multi-drug interaction scoring** — full med list → interaction matrix |
| F2 | **Additive toxicity detection** — NSAID + warfarin + PPI → cumulative GI bleed = HIGH |
| F3 | **Therapeutic duplication check** — two PPIs, ACEi + ARB |

### Pharmacoeconomic Layer

| # | Feature |
|---|---------|
| Q1 | **Cost/affordability** — pricing as a 5th scoring axis |
| Q2 | **Formulary tier display** — per-institution status in results |
| Q3 | **Cost-value view** — "best clinical" vs "best affordable" toggle |

### Clinical Integration

| # | Feature |
|---|---------|
| C1 | **FHIR R4 interface** — Patient resource in, GuidanceResponse out |
| C2 | **SMART-on-FHIR app** — embeddable widget for Epic/Cerner |
| C3 | **CDS Hooks** — trigger DQF when a drug is ordered for a matching patient |
| C4 | **Institutional formulary management** — "best value for our population" dashboard |

### Research & Publication

| # | Milestone | Status |
|---|-----------|--------|
| R1 | Submit validation paper to *JACMP* / *Applied Clinical Informatics* | ⬜ — 8 validation reports exist as source material |
| R2 | Open-source DQF on GitHub with contribution templates | 🟡 repo public at `github.com/rikirinjani/DQF`; no templates yet |
| R3 | Preprint on medRxiv with DOI | ⬜ |
| R4 | FDA SaMD 510(k)-exempt classification if pursuing EHR integration | ⬜ |

---

## Known Debt

- **`l4_schema_map.json` Risk 1** — `nnt_bp_control` false-shares a key name between Antihypertensive `{value,ci_95,dose}` and Diabetes `{a1c_reduction,unit,dose}`; needs coordinated rename + consumer update (`server.py` has 6 hardcoded L4 refs, `_add_e3_e4_drugs.py` too).
- **`docs`/`INDEX.md`** still say "2 drug classes, 9 drugs" — README-era text.
- **50 null L3 cells** — documented gaps, not blockers (no-fabrication rule).
- **46 unapplied prior-rescore proposals** (32 batch4_rescore + 14 ddi_rescore per mechanical diff 2026-09-29; 8 ddi superseded — see `rag-queries/curation/n6_worklist.json`) — values proposed but never merged; awaiting apply-or-reject → N6.
- **lovastatin `nnt_mace_5yr` missing** — ✅ crash fixed 2026-09-29 (null-safe neutral 5.0 fallback, `fde0203`/`667fd49`); the DATA is still missing → N6 sourcing.
- ✅ **`bp_reduction` absent from `DIM_DIRECTION`** — fixed 2026-09-29 (`fde0203`, R-10): bp_reduction/hmgcr_inhibition/ldl_reduction_pct = benefit.
- **merge lock policy** — `DEFAULT_LOCKED_FIELDS` is empty and list-merging re-adds expert-deleted items (re-assessment REG-02/RES-03); policy decision + implementation → N6.
- **metformin `hypoglycemia_risk` = 3** in drugs.json — clinically questionable for monotherapy; candidate for N6 sourced review.

---

## How to Read This

```
Priority: 🔴 High (next)  🟡 Medium  🟢 Nice-to-have
✅ done   🟡 partial      ⬜ not started
N  = immediate next actions
E  = drug expansion      V = validation (V3 is the last one)
R  = RAG evidence        S = scoring engine    U = usability
P  = personalization     F = full rx           Q = pharmacoeconomics
C  = clinical integration
```

> **Next logical step:** N6 (sourced adjudication backlog — worklist + source plan first), then N6b design, then N7.
