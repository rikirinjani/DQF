# Second Drug Class — Scoping and Implementation

> **R1's question (v3):** "The framework is demonstrated on one class (NSAIDs). How do we know it generalizes?" Tier 2 (holdout validation) tests within-class generalizability. A second drug class tests cross-class generalizability — and whether the 4-level ontology genuinely works outside analgesia.

## Why a Second Class Matters

The PoC chose NSAIDs because the class has:
- Well-understood L1 (COX-1/2 is a simple target)
- Well-characterized L2 (PK parameters in multiple databases)
- Rich L3 (tissue-level COX dynamics → downstream effects)
- Abundant L4 (Cochrane NNT league tables, decades of RCTs)

None of these are guaranteed for another class. A second class validates that the ontology is class-agnostic, not analgesia-specific.

## Candidate Classes

### 1. Statins (HMG-CoA Reductase Inhibitors) — Recommended

| Dimension | NSAIDs | Statins |
|-----------|--------|---------|
| L1 target | COX-1/2 + off-targets (P2X3, TRPV1, etc.) | HMG-CoA reductase + off-targets (pleiotropic effects, e.g., eNOS upregulation, anti-inflammatory) |
| L2 data | Abundant PK (multiple databases) | Abundant PK (well-studied class) |
| L3 | Tissue-level COX dynamics | Mevalonate pathway suppression, endothelial function, plaque stabilization |
| L4 endpoint | NNT for pain relief | LDL reduction, major adverse cardiac events (MACE), NNT for CV event prevention |
| Class size | PoC uses 4 of ~20 | Atorvastatin, rosuvastatin, simvastatin, pravastatin, pitavastatin, lovastatin (6 major) |

**Why statins:**
- Most studied drug class in history — data density exceeds NSAIDs
- L1 off-target pharmacology exists (pleiotropy: atorvastatin's eNOS, rosuvastatin's anti-inflammatory independent of LDL) — tests the off-target profiling pipeline
- L4 endpoint is different (MACE reduction instead of NNT) — tests whether the ontology adapts
- Clinical utility is real: comparing statins by potency vs tolerability vs drug-drug interaction risk is a genuine clinical problem
- PK differences matter: simvastatin vs atorvastatin vs rosuvastatin have very different CYP metabolism, half-lives, and food effects

**Risks:**
- L3 is harder to populate — statin pleiotropy is less well-characterized mechanistically than NSAID tissue COX dynamics
- L4 data is trial-specific and population-dependent (primary vs secondary prevention NNTs differ)

### 2. SSRIs (Selective Serotonin Reuptake Inhibitors) — Research-Focused

| Dimension | NSAIDs | SSRIs |
|-----------|--------|-------|
| L1 target | COX-1/2 | SERT (primary) + off-targets (NET, H1, 5-HT2C, sigma-1, etc.) |
| L2 data | Abundant | Abundant |
| L3 | Tissue-level pathway activation | Neurotransmitter reuptake → downstream signaling → neuroplasticity (complex) |
| L4 endpoint | NNT for pain relief | NNT for depression remission, NNH for side effects (sexual dysfunction, weight gain, insomnia) |
| Class size | ~20 | ~8-10 major |

**Why it's interesting but harder:**
- L1 off-target profiles are clinically decisive (fluoxetine's 5-HT2C vs sertraline's DAT vs paroxetine's NET → different side effect profiles)
- L3 is much harder — the causal chain from SERT occupancy → mood improvement is poorly understood, involves weeks of adaptation, and no simple endpoint like "COX inhibition time course" exists
- L4 has delayed onset (2-6 weeks vs NSAID's 30 min), making attribution harder
- The framework would demonstrate real comparative value (SSRI selection is a genuine clinical problem) but requires significantly more L3 work

### 3. Antibiotics (Fluoroquinolones) — Structural Challenge

| Dimension | NSAIDs | Fluoroquinolones |
|-----------|--------|------------------|
| L1 target | Human COX-1/2 + off-targets | Bacterial DNA gyrase + topoisomerase IV |
| L2 data | Abundant | Abundant |
| L3 | Human tissue response | Bacterial cell death → resistance selection → microbiome disruption → human immune response |
| L4 endpoint | NNT for pain relief | MIC, clinical cure rate, resistance emergence rate |
| Class size | ~20 | ~5-6 major |

**Why it's relevant:**
- The endpoint substitution (MIC for NNT) is the hardest test of the ontology's generalizability
- L3 involves both pathogen and host — dual-level systems biology
- Clinically useful: comparing fluoroquinolones by spectrum vs PK vs tissue penetration vs tendon toxicity is a real problem

**Risks:**
- L1 target is bacterial, not human — the framework would need to handle dual pharmacology (human off-target effects + bacterial targets)
- L4 data is infection-site-specific (urinary vs respiratory vs skin MICs differ)
- This is more work than statins or SSRIs

## Recommendation

**Start with statins.** They are the highest-confidence second class:
- Most familiar data structure (PK databases, Cochrane meta-analyses, well-documented L1 profiles)
- Best available L4 endpoint data (CTT meta-analyses have NNT per mmol LDL reduction per year)
- Known off-target pharmacology (pleiotropy) tests the L1 pipeline without being as messy as SSRIs
- The class is clinically relevant — comparative statin selection is a real prescribing decision

SSRIs would be more informative for the framework's robustness but require 2-3× the effort for L3 alone. Antibiotics would be the strongest generalizability proof but require adapting the ontology for bacterial targets.

## Implementation Plan (Statins)

### Phase 1 — Data Assembly (~10-14 days)

| Step | Effort | Deliverable |
|------|--------|-------------|
| Select 4-5 statins for PoC | 0.5 d | Drug list (atorvastatin, rosuvastatin, simvastatin, pravastatin, pitavastatin) |
| L1 — RAG queries for off-target pharmacology | 2 d | Per-drug off-target profile (Cochrane Handbook, pleiotropy reviews, PDSP) |
| L2 — Extract PK from structured sources | 1 d | Half-life, Vd, protein binding, metabolism (CYP3A4 vs CYP2C9 vs renal), food effects |
| L3 — RAG queries for mechanistic effects | 3 d | Mevalonate pathway suppression, eNOS, anti-inflammatory, plaque composition effects |
| L4 — Extract CTT/FDA outcome data | 2 d | MACE reduction per drug per dose, NNT per mmol LDL per year, myopathy/rhabdomyolysis rates, diabetes risk |
| Cross-drug comparison | 1 d | Comparison table: 4 levels, 5 statins |

### Phase 2 — Build & Validate (~5-7 days)

| Step | Effort | Deliverable |
|------|--------|-------------|
| Write 5 statin profiles | 3 d | `profiles/atorvastatin.md`, `profiles/rosuvastatin.md`, etc. |
| Build statin comparison table | 1 d | `comparison-statins.md` |
| Run Tier 2 holdout on statins | 1 d | Leave-one-statin-out cross-validation |
| Integrate into PDF | 2 d | Section 10 (or parallel PoC document) |

### Phase 3 — Write-Up (~3 days)

| Step | Effort | Deliverable |
|------|--------|-------------|
| Generalizability section revision | 1 d | Updated Limitations section |
| Methods section: level-specific adaptations | 1 d | Documentation of statin-specific L1-L4 mappings |
| Cross-class comparison discussion | 1 d | What NSAID PoC teaches us + what statin PoC confirms/changes |

### Total Effort: ~18-24 work days

## Level-Specific Adaptations for Statins

### L1
- Primary target: HMG-CoA reductase (IC50 per statin: rosuvastatin ~5 nM, pitavastatin ~10 nM, atorvastatin ~8 nM, simvastatin acid ~11 nM, pravastatin ~40 nM)
- Off-target tests: eNOS upregulation (atorvastatin, rosuvastatin), anti-inflammatory independent of LDL (rosuvastatin), bone effects (simvastatin), cognitive effects (all)
- Drug-drug interaction risk: CYP3A4 (atorvastatin, simvastatin) vs CYP2C9 (rosuvastatin, pitavastatin) vs renal (pravastatin)
- Pharmacogenomics: SLCO1B1 polymorphism (simvastatin myopathy risk), ABCG2 (rosuvastatin exposure)

### L2
- Standard PK: bioavailability, t½, Vd, protein binding, metabolism
- Special: food effect (atorvastatin with grapefruit), time to steady state, lipophilicity (affects tissue penetration)

### L3
- Mevalonate pathway suppression kinetics
- Pleiotropic effects: endothelial function (eNOS, NO bioavailability), anti-inflammatory (CRP reduction), plaque stabilization, thrombotic modulation
- Time course: LDL reduction days-weeks, pleiotropic effects may have different time courses
- Tissue selectivity: hepatic vs extrahepatic (pravastatin is hepatoselective; others penetrate extrahepatic tissues)

### L4
- Primary: MACE reduction per mg/dL LDL reduction per year (CTT meta-analysis)
- Per-statin: atorvastatin 80 mg, rosuvastatin 20 mg, simvastatin 40 mg as standard comparator doses
- Safety: myopathy (simvastatin 80 mg withdrawn), rhabdomyolysis, diabetes incidence (statin class effect, dose-dependent), hepatotoxicity
- Drug-specific: pravastatin — no known drug interactions (renal clearance); simvastatin — highest myopathy risk; rosuvastatin — highest potency, lowest required dose

## Relationship to Existing NSAID PoC

The statin PoC should be a **parallel document**, not an extension of the existing PDF. It provides independent evidence for generalizability. The methods section for both can share the framework ontology document, with class-specific adaptations noted as appendices.

A cross-class synthesis section would then discuss:
- Which levels transfer cleanly (L2, L4)
- Which require class-specific adaptation (L1 target ontology, L3 mechanistic pathways)
- Where the ontology breaks (if anywhere)

## Open Questions

1. **Dose standardization** — Statins have very different potencies (rosuvastatin 5 mg = simvastatin 40 mg). The framework needs a dose-equivalence mechanism or per-dose reporting. This is technically interesting — it reproduces the NSAID dose problem (ibuprofen 200 vs 400 mg) in a more extreme form.

2. **Endpoint heterogeneity** — NNT for pain relief is a single, simple endpoint. Statin L4 involves composite cardiovascular endpoints (MACE), individual endpoints (MI, stroke, revascularization), and safety endpoints (myopathy, diabetes). Which L4 metrics to report is a framework-design question.

3. **Pleiotropic attribution** — Statins have LDL-independent effects (anti-inflammatory, endothelial). Are these L1 off-target (eNOS upregulation) → L3 consequences, or L4 observations with unclear mechanism? How the framework handles this sets precedent for future classes.
