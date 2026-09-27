# DQF Roadmap — Clinical Tool

> *Pharmacist-built, evidence-grounded, patient-personalized drug ranking.*
> **Last refreshed 2026-09-27** (was stale since 2026-07-26 — old copy still described the 9-drug PoC and listed finished work as pending).

---

## Current State (verified 2026-09-27)

| Metric | Value |
|--------|-------|
| Drugs | **95** across **10 classes** — Antihypertensive 33, Diabetes 28, NSAID 10, Statin 6, Anticoagulant 6, PPI 5, H2RA 3, Antacid 2, Alginate 1, Mucosal Protectant 1 |
| L3 coverage | 95/95 drugs; 798 numeric cells, 50 documented nulls (NSAID 24, Statin 20, H2RA 5, Anticoagulant 1) |
| L4 coverage | 95/95, class-specific schema locked in `api/l4_schema_map.json` |
| Profile docs | 56 — `profiles/` (NSAID), `profiles-statins/`, `profiles-gi/`, `profiles-anticoagulants/` |
| Validation | 8 reports in `validation/` (V1, V1b, V1c×2, V2, V4, + 2 leave-one-out holdouts) |
| Scorer tests | 46 checks passing — `python rag-queries/test_scorer_hardening.py` (22) + `test_anticoagulant_scorer.py` (24) |
| LLM triage | Batches 1–6 run; **Batch 5 full corpus landed 2026-09-27** (413 groups / 2573 sentences / 905 kept) |
| Latest commit | `dc55a32` on `master`, pushed |

---

## Immediate — Next

| # | Task | Why | Est. |
|---|------|-----|------|
| N1 | **Consume `rag-queries/batch5_verdicts.json`** — rescore/adjudicate the non-anticoagulant evidence pools (`batch4_rescore.json` is the recipe precedent) | 905 kept sentences are sitting unused; this is the payoff of the ~92 min GPU run | 1–2 d |
| N2 | **E2 — Antiplatelets**: clopidogrel, ticagrelor, prasugrel (aspirin already present, classed NSAID) | Next 🔴 High class; same pipeline as E1 is proven end-to-end | 1–2 wk |
| N3 | **Inter-rater reliability (V3)** — 2–3 pharmacists rank patient scenarios independently, compare agreement with DQF | The one Phase-V task never started (V1/V1b/V1c/V2/V4 all done) | 2 wk |
| N4 | **Profile docs for Antihypertensive + Diabetes** | 61 drugs have JSON records but no `profiles-*` docs — the only classes without them | 1 wk |
| N5 | **HF RAG endpoint** `balade-pubmed-rag-bot.hf.space` still 503 → keep `extract_l3.py --eutils-first` (3 req/s, no `NCBI_API_KEY`); fix or replace the Space | Fetch throughput bottleneck for every future class | as needed |

**Validation note:** Phase V is now V1 ✅ · V1b ✅ · V1c ✅ (×2) · V2 ✅ · V4 ✅ · holdouts ✅ · **V3 ⬜**.

---

## Mid-Term (3–6 months)

### Drug Coverage Expansion

| # | Class | Drugs | Status |
|---|-------|-------|--------|
| E1 | **Anticoagulants** | warfarin, apixaban, rivaroxaban, edoxaban, dabigatran, enoxaparin | ✅ **done 2026-09-27** — 42-cell adjudication merged, profiles written |
| E2 | **Antiplatelets** | aspirin, clopidogrel, ticagrelor, prasugrel | 🔴 **next** (aspirin only) |
| E3 | **Antihypertensives** | lisinopril, losartan, amlodipine, metoprolol, HCTZ, chlorthalidone | 🟡 records + L3/L4 done (33 drugs, 0 nulls); profile docs missing → N4 |
| E4 | **Diabetes** | metformin, empagliflozin, dapagliflozin, semaglutide, tirzepatide, insulin glargine | 🟡 records + L3/L4 done (28 drugs, 0 nulls); profile docs missing → N4 |
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

> **Next logical step:** N1 — consume the Batch-5 verdicts, then start E2 antiplatelets.
