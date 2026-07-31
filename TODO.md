# DQF Roadmap — Clinical Tool

> *Pharmacist-built, evidence-grounded, patient-personalized drug ranking.*

---

## Immediate — Validation (Phase V)

**Goal:** Prove DQF scores match real-world prescribing guidance before expanding.

| # | Task | Why | Est. |
|---|------|-----|------|
| V1 | **Guideline concordance study** — Pick a class (PPIs first: ACG/AGA/ASGE guidelines). Rank drugs by DQF vs guideline algorithm. Report: "DQF ranks esomeprazole #1 for EE healing; ACG guideline recommends PPI BID → matches." | Establishes credibility. A validation table is publishable. | 1–2 wk |
| V2 | **Formulary tier comparison** — Compare DQF scores against common institutional formulary tiers (DoD, VA, large health systems). "Pantoprazole scores 7.7 → preferred on >80% of formularies." | Tool must reflect real-world access, not just ideal pharmacology. | 1 wk |
| V3 | **Inter-rater reliability** — Have 2–3 pharmacists rank a set of patient scenarios independently; compare agreement with DQF. | Humans vs algorithm consistency check. | 2 wk |
| V4 | **Edge-case audit** — Test scenarios where DQF might disagree with clinical consensus (pregnancy, CKD, polypharmacy). Document what the tool gets right/wrong. | Honest failure mode catalog. | 1 wk |

**Output:** `validation/` directory with per-class validation reports + a `validation/comparison_paper.md`.

---

## Mid-Term (3–6 months)

### Drug Coverage Expansion

| # | Class | Drugs | Priority |
|---|-------|-------|----------|
| E1 | **Anticoagulants** | warfarin, apixaban, rivaroxaban, edoxaban, dabigatran, enoxaparin | 🔴 High |
| E2 | **Antiplatelets** | aspirin, clopidogrel, ticagrelor, prasugrel | 🔴 High |
| E3 | **Antihypertensives** | lisinopril, losartan, amlodipine, metoprolol, HCTZ, chlorthalidone | 🔴 High |
| E4 | **Diabetes** | metformin, empagliflozin, dapagliflozin, semaglutide, tirzepatide, insulin glargine | 🔴 High |
| E5 | **Antidepressants** | escitalopram, sertraline, venlafaxine, bupropion, mirtazapine | 🟡 Medium |
| E6 | **Antibiotics** | amoxicillin, doxycycline, azithromycin, ciprofloxacin, TMP-SMX | 🟡 Medium |

Each class = 5–8 profiles + JSON entries + scoring engine branches + RAG queries + validation.

### RAG Evidence Queries (Phase 4 — Async with E1–E6)

| # | Task |
|---|------|
| R1 | Per class: 5–10 curated PubMed queries in `rag-queries/{class}/` |
| R2 | Evidence summary document linking each score component to trial citations |
| R3 | Inline citation display in the query tool (hover over score → see evidence) |

### Scoring Engine Maturation

| # | Improvement |
|---|-------------|
| S1 | **DDI penalty** — If patient query includes current meds, apply interaction penalty between ranked drugs and existing regimen |
| S2 | **Renal/hepatic penalty** — Granular CKD stage adjustments (currently binary normal/impaired) |
| S3 | **Age-specific efficacy** — Some drugs work better or worse in elderly (e.g., anticholinergics) |
| S4 | **Pregnancy/lactation** — Dedicated safety sub-score with trimester-specific adjustments |

### Tool Usability

| # | Feature |
|---|---------|
| U1 | **PDF report** — Downloadable clinical summary (patient profile → ranked list → evidence citations) |
| U2 | **Scenario comparison** — Side-by-side rankings for two different patient profiles |
| U3 | **Score drill-down** — Click any score → see the actual data and calculation behind it |
| U4 | **Mobile responsive** — The UI works well on phone for bedside/rounding use |

---

## Long-Term (6–12 months)

### Personalization

| # | Feature |
|---|---------|
| P1 | **CYP genotype input** — Dosing adjustments for CYP2C19, CYP2C9, CYP3A4, CYP2D6 metabolizer status |
| P2 | **Weight/BSA-based dosing** — For drugs where weight matters (enoxaparin, vancomycin) |
| P3 | **Organ function integration** — Real CrCl / eGFR / MELD score input instead of categorical "normal/mild/moderate/severe" |

### Full Prescription Analysis

| # | Feature |
|---|---------|
| F1 | **Multi-drug interaction scoring** — Input entire medication list → scored interaction matrix |
| F2 | **Additive toxicity detection** — "Patient on NSAID + warfarin + PPI → cumulative GI bleed risk = HIGH" |
| F3 | **Therapeutic duplication check** — "Two PPIs prescribed" or "ACEi + ARB combination" |

### Pharmacoeconomic Layer

| # | Feature |
|---|---------|
| Q1 | **Cost/affordability** — Drug pricing data as a 5th scoring axis |
| Q2 | **Formulary tier display** — Per-institution formulary status in results |
| Q3 | **Cost-value view** — "Best clinical choice" vs "best affordable choice" toggle |

### Clinical Integration

| # | Feature |
|---|---------|
| C1 | **FHIR R4 interface** — Accept Patient resource, produce GuidanceResponse |
| C2 | **SMART-on-FHIR app** — Embeddable widget for Epic/Cerner |
| C3 | **CDS Hooks** — Trigger DQF when a new drug is ordered for a patient with matching conditions |
| C4 | **Institutional formulary management** — "Which PPI gives best value for our population?" dashboard |

### Research & Publication

| # | Milestone |
|---|----------|
| R1 | Submit validation paper to *JACMP* or *Applied Clinical Informatics* |
| R2 | Open-source DQF on GitHub with contribution templates for new drug classes |
| R3 | Preprint on medRxiv with DOI |
| R4 | FDA SaMD 510(k) exempt classification if pursuing EHR integration |

---

## How to Read This

```
Priority: 🔴 High (next)  🟡 Medium  🟢 Nice-to-have
Phase V = Validation (immediate, ⬆ priority over everything)
Phase E = Expansion
Phase R = RAG evidence
Phase S = Scoring
Phase U = Usability
Phase P = Personalization
Phase F = Full rx analysis
Phase Q = Pharmacoeconomic
Phase C = Clinical integration
```

> **Next logical step:** V1 — validate PPI ranking against ACG/AGA guidelines. Want to start there?
