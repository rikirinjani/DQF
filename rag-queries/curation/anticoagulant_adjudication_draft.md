# Anticoagulant L3 adjudication - DRAFT for review (E1 Batch-6)

**Status: DRAFT. Nothing has been written to `api/drugs.json` (`l3_systems` is still `{}` for all 6 records).**

Inputs: `batch6_current.json` (v2 auto-scores) + `batch6_verdicts.json` (Batch-6 LLM triage, 310/313 sentences) + `classifier_audit.py` flags + sourced fields already in `api/drugs.json` / `curation/anticoagulant_values_draft.md`.

## Decision rules

**Family A - `ddi_risk` (6 cells).** Batch-3 taxonomy (`pk`/`pd`/`none`). Per `kaggle_ddi_triage.py` these labels *"feed a filtered re-score"*: keep the pk/pd sentences, drop `none`, re-run the same `_score_risk` block (**R7**). If no pk/pd sentence survives -> **null (R6)**.

**Family B - the other 36 cells** (`strong`/`moderate`/`negative`/`none`), counted after `classifier_audit` flags are removed:

| rule | condition | outcome |
|---|---|---|
| R0 | pool empty | `null` |
| R5 | every candidate is `none` | `null` (keyword false positives) |
| R1a | auto = 3 and >=1 audit-clean strong | keep 3 |
| R1b | >=2 audit-clean strong, 0 flagged, auto < 3 | raise to 3 |
| R1c | otherwise >=1 audit-clean strong | keep auto |
| R4 | all strong evidence auditor-flagged | `null` |
| R2 | moderate only (no clean strong) | cap at 2 |
| R3 | explicit `negative`, no clean strong | 1 |
| R7 | ddi: filtered pk/pd re-score | re-scored value |

**Override layer.** Where the pool is empty or contradicted, a value already sourced in `api/drugs.json` (label / PMID, per the 2026-09-25 source policy) takes precedence; every such cell cites its field. If no sourced field exists, the cell stays `null` rather than inheriting a v2 guess.

## The 42 cells

| drug | dimension | auto | pool | labels (n / clean S / flag F / mod / neg / none / pk+pd) | **proposed** | via | basis |
|---|---|---|---|---|---|---|---|
| warfarin | anticoagulation_efficacy | 3 | 3 | 12 / 5 / 0 / 2 / 0 / 5 / 0 | **3** | R1a | auto 3 supported by 5 audit-clean strong |
| warfarin | bleeding_risk | 3 | 3 | 12 / 2 / 3 / 1 / 0 / 6 / 0 | **3** | R1a | auto 3 supported by 2 audit-clean strong |
| warfarin | renal_clearance_dependence | 3 | 3 | 6 / 1 / 0 / 2 / 1 / 2 / 0 | **1** **<-CHG** | OVERRIDE | l2_pk.metabolism = CYP2C9/CYP1A2/CYP3A4 (PMID 9014207); l4.dose_reduction_criteria = "INR-titrated, no fixed dose" (label) - no renal dose adjustment exists. Urinary 92% is METABOLITES (label), not renal clearance of parent. |
| warfarin | ddi_risk | 3 | 2 | 12 / 0 / 0 / 0 / 0 / 8 / 4 | **2** **<-CHG** | R7 | filtered re-score on 4 pk/pd sentence(s) (Batch-3 precedent); auto scored the full pool = 3 |
| warfarin | monitoring_burden | 3 | 3 | 12 / 3 / 2 / 3 / 0 / 4 / 0 | **3** | R1a | auto 3 supported by 3 audit-clean strong |
| warfarin | reversal_availability | 3 | 3 | 7 / 2 / 0 / 2 / 0 / 3 / 0 | **3** | R1a | auto 3 supported by 2 audit-clean strong |
| warfarin | gi_bleeding_risk | 3 | 3 | 4 / 2 / 0 / 1 / 0 / 1 / 0 | **3** | R1a | auto 3 supported by 2 audit-clean strong |
| apixaban | anticoagulation_efficacy | 3 | 3 | 12 / 3 / 3 / 0 / 0 / 6 / 0 | **3** | R1a | auto 3 supported by 3 audit-clean strong |
| apixaban | bleeding_risk | 3 | 3 | 12 / 7 / 0 / 1 / 0 / 4 / 0 | **3** | R1a | auto 3 supported by 7 audit-clean strong |
| apixaban | renal_clearance_dependence | 3 | 3 | 6 / 1 / 0 / 1 / 0 / 4 / 0 | **2** **<-CHG** | OVERRIDE | l2_pk.renal_excretion_pct = 27 (PMID 24353445/24861792); dose reduction only at CrCl 15-30 (label). |
| apixaban | ddi_risk | 3 | 3 | 11 / 0 / 0 / 0 / 0 / 8 / 3 | **3** | R7 | filtered re-score on 3 pk/pd sentence(s) (Batch-3 precedent); auto scored the full pool = 3 |
| apixaban | monitoring_burden | 3 | 2 | 6 / 0 / 4 / 1 / 0 / 1 / 0 | **1** **<-CHG** | OVERRIDE | PMID 34662890: "requires no dose adjustment or monitoring"; PMID 31089975: "without the need for therapeutic drug monitoring". |
| apixaban | reversal_availability | 3 | 3 | 4 / 1 / 0 / 0 / 0 / 3 / 0 | **3** | R1a | auto 3 supported by 1 audit-clean strong |
| apixaban | gi_bleeding_risk | 1 | null | pool empty | **1** | OVERRIDE | L4 GI bleed HR 0.89 (0.70-1.14) vs warfarin - label ARISTOTLE table (curation draft, not yet written into drugs.json). |
| rivaroxaban | anticoagulation_efficacy | 3 | 3 | 12 / 6 / 0 / 2 / 0 / 4 / 0 | **3** | R1a | auto 3 supported by 6 audit-clean strong |
| rivaroxaban | bleeding_risk | 3 | 3 | 12 / 3 / 0 / 4 / 1 / 4 / 0 | **3** | R1a | auto 3 supported by 3 audit-clean strong |
| rivaroxaban | renal_clearance_dependence | 2 | null | 1 / 0 / 0 / 0 / 0 / 1 / 0 | **3** **<-CHG** | OVERRIDE | l2_pk.renal_excretion_pct = 66 (33% unchanged + 33% metabolites, PMID 24861792). |
| rivaroxaban | ddi_risk | 3 | 3 | 9 / 0 / 0 / 0 / 0 / 7 / 2 | **3** | R7 | filtered re-score on 2 pk/pd sentence(s) (Batch-3 precedent); auto scored the full pool = 3 |
| rivaroxaban | monitoring_burden | 3 | 2 | 9 / 0 / 0 / 5 / 0 / 4 / 0 | **1** **<-CHG** | OVERRIDE | DailyMed XARELTO label: "Monitoring for the anticoagulation effect of rivaroxaban using a clotting test (PT, INR or aPTT) or anti-factor Xa (FXa) activity is not recommended." |
| rivaroxaban | reversal_availability | 3 | 3 | 12 / 3 / 0 / 3 / 0 / 6 / 0 | **3** | R1a | auto 3 supported by 3 audit-clean strong |
| rivaroxaban | gi_bleeding_risk | 1 | null | pool empty | **3** **<-CHG** | OVERRIDE | DailyMed XARELTO label, 6 Clinical Trials Experience: GI bleeding 221 (2.0%) vs 140 (1.2%), HR 1.61 (1.30-1.99). |
| edoxaban | anticoagulation_efficacy | 3 | 3 | 12 / 4 / 0 / 1 / 0 / 7 / 0 | **3** | R1a | auto 3 supported by 4 audit-clean strong |
| edoxaban | bleeding_risk | 3 | 3 | 12 / 7 / 0 / 2 / 0 / 3 / 0 | **3** | R1a | auto 3 supported by 7 audit-clean strong |
| edoxaban | renal_clearance_dependence | 2 | null | 1 / 0 / 0 / 0 / 0 / 1 / 0 | **3** **<-CHG** | OVERRIDE | l2_pk.renal_excretion_pct = 50; dose reduction to 30 mg if CrCl 15-50 (label). |
| edoxaban | ddi_risk | 3 | 2 | 6 / 0 / 0 / 0 / 0 / 4 / 2 | **2** **<-CHG** | R7 | filtered re-score on 2 pk/pd sentence(s) (Batch-3 precedent); auto scored the full pool = 3 |
| edoxaban | monitoring_burden | 2 | null | 1 / 0 / 0 / 0 / 0 / 1 / 0 | **1** **<-CHG** | OVERRIDE | DailyMed SAVAYSA label, 12.2 Pharmacodynamics: changes in PT, INR and aPTT "are small, subject to a high degree of variability and not useful in monitoring the anticoagulant effect of edoxaban." |
| edoxaban | reversal_availability | 1 | null | pool empty | **2** **<-CHG** | OVERRIDE | l4.reversal_agent = "andexanet alfa (partial; PMID 29345686)". |
| edoxaban | gi_bleeding_risk | 2 | 2 | 1 / 1 / 0 / 0 / 0 / 0 / 0 | **2** | R1c | keep 2: 1 clean strong (+0 flagged) |
| dabigatran | anticoagulation_efficacy | 3 | 3 | 12 / 6 / 0 / 2 / 0 / 4 / 0 | **3** | R1a | auto 3 supported by 6 audit-clean strong |
| dabigatran | bleeding_risk | 3 | 3 | 12 / 6 / 0 / 2 / 2 / 2 / 0 | **3** | R1a | auto 3 supported by 6 audit-clean strong |
| dabigatran | renal_clearance_dependence | 2 | null | 1 / 0 / 0 / 0 / 0 / 1 / 0 | **3** **<-CHG** | OVERRIDE | l2_pk.renal_excretion_pct = 80-85 unchanged (PMID 31335150); t1/2 13 h -> 27 h as CrCl falls (label); contraindicated CrCl <30 (label). |
| dabigatran | ddi_risk | 3 | 3 | 9 / 0 / 0 / 0 / 0 / 6 / 3 | **3** | R7 | filtered re-score on 3 pk/pd sentence(s) (Batch-3 precedent); auto scored the full pool = 3 |
| dabigatran | monitoring_burden | 3 | 2 | 7 / 0 / 2 / 2 / 0 / 3 / 0 | **1** **<-CHG** | OVERRIDE | DailyMed PRADAXA label, 12.2 Pharmacodynamics: "INR is relatively insensitive to the exposure to dabigatran and cannot be interpreted the same way as used for warfarin monitoring." |
| dabigatran | reversal_availability | 3 | 3 | 11 / 3 / 0 / 2 / 0 / 6 / 0 | **3** | R1a | auto 3 supported by 3 audit-clean strong |
| dabigatran | gi_bleeding_risk | 2 | 2 | 5 / 0 / 0 / 2 / 1 / 2 / 0 | **2** | R2a | moderate-only (2 moderate, 0 flagged strong) - 3 not earned |
| enoxaparin | anticoagulation_efficacy | 3 | 3 | 10 / 1 / 0 / 2 / 0 / 7 / 0 | **3** | R1a | auto 3 supported by 1 audit-clean strong |
| enoxaparin | bleeding_risk | 3 | 3 | 12 / 2 / 0 / 1 / 0 / 9 / 0 | **3** | R1a | auto 3 supported by 2 audit-clean strong |
| enoxaparin | renal_clearance_dependence | 3 | 3 | 7 / 3 / 0 / 1 / 0 / 3 / 0 | **3** | R1a | auto 3 supported by 3 audit-clean strong |
| enoxaparin | ddi_risk | 2 | null | 1 / 0 / 0 / 0 / 0 / 1 / 0 | **2** | OVERRIDE | DailyMed LOVENOX label, 7 Drug Interactions: agents that enhance hemorrhage risk (anticoagulants, platelet inhibitors, NSAIDs) "should be discontinued"; if coadministration is essential, "conduct close clinical and laboratory monitoring". Label 12.3: "No pharmacokinetic interaction was observed between enoxaparin and thrombolytics". |
| enoxaparin | monitoring_burden | 3 | 3 | 12 / 6 / 0 / 3 / 0 / 3 / 0 | **3** | R1a | auto 3 supported by 6 audit-clean strong |
| enoxaparin | reversal_availability | 3 | 3 | 7 / 2 / 0 / 3 / 0 / 2 / 0 | **3** | R1a | auto 3 supported by 2 audit-clean strong |
| enoxaparin | gi_bleeding_risk | 1 | null | pool empty | **null** **<-CHG** | R0 | pool empty / unsupported and no sourced field -> null |

**14 of 42 cells would change** vs the v2 auto-score: 11 via a sourced override, 3 via the evidence rules. 2 further cell keeps its value but gains a citation.

## Every changing cell

| drug | dimension | auto -> proposed | why |
|---|---|---|---|
| warfarin | renal_clearance_dependence | 3 -> **1** | auto=3 is a keyword false positive (crcl/creatinine/dialysis matched cohort-exclusion text); the one clean strong is a single 1996 CrCl/half-life correlation, contradicted by an explicit negative in ESKD. |
| warfarin | ddi_risk | 3 -> **2** | filtered re-score on 4 pk/pd sentence(s) (Batch-3 precedent); auto scored the full pool = 3 |
| apixaban | renal_clearance_dependence | 3 -> **2** | clean strong is the dialysis RCT title (PMID 36335914) - real but dialysis-specific; 27% renal excretion = moderate, not maximal. |
| apixaban | monitoring_burden | 3 -> **1** | both sentences were LLM-labelled strong and auditor-FLAGGED: they say monitoring is NOT needed. The other two flagged strongs are warfarin-arm INR targets (comparator's burden, not apixaban's). |
| rivaroxaban | renal_clearance_dependence | 2 -> **3** | pool had 1 sentence, LLM-labelled none; label/PMID already record 66% renal. |
| rivaroxaban | monitoring_burden | 3 -> **1** | rules capped it at 2 on anti-Xa/PT assay-availability papers, which measure assay capability, not routine monitoring burden. |
| rivaroxaban | gi_bleeding_risk | 1 -> **3** | pool empty (0 drug-anchored GI sentences); label gives a significant increase vs warfarin. |
| edoxaban | renal_clearance_dependence | 2 -> **3** | pool had 1 sentence, LLM-labelled none; label already records the renal rule. |
| edoxaban | ddi_risk | 3 -> **2** | filtered re-score on 2 pk/pd sentence(s) (Batch-3 precedent); auto scored the full pool = 3 |
| edoxaban | monitoring_burden | 2 -> **1** | pool had 1 sentence, LLM-labelled none; label states monitoring is not useful. |
| edoxaban | reversal_availability | 1 -> **2** | pool empty; the record already carries a partial-reversal agent, so 1 (none) is wrong and 3 (full antidote) overstates a partial agent. |
| dabigatran | renal_clearance_dependence | 2 -> **3** | pool had 1 sentence, LLM-labelled none; label/PMID already record 80-85% renal. |
| dabigatran | monitoring_burden | 3 -> **1** | rules capped it at 2 on warfarin-TTR comparison sentences (the comparator's metric, not dabigatran's burden). |
| enoxaparin | gi_bleeding_risk | 1 -> **null** | pool empty / unsupported and no sourced field -> null |

## Sourced overrides that change a value (need your sign-off)

- **warfarin / renal_clearance_dependence**: 3 -> **1**  
  - source: l2_pk.metabolism = CYP2C9/CYP1A2/CYP3A4 (PMID 9014207); l4.dose_reduction_criteria = "INR-titrated, no fixed dose" (label) - no renal dose adjustment exists. Urinary 92% is METABOLITES (label), not renal clearance of parent.  
  - why the pool answer is wrong: auto=3 is a keyword false positive (crcl/creatinine/dialysis matched cohort-exclusion text); the one clean strong is a single 1996 CrCl/half-life correlation, contradicted by an explicit negative in ESKD.
- **apixaban / renal_clearance_dependence**: 3 -> **2**  
  - source: l2_pk.renal_excretion_pct = 27 (PMID 24353445/24861792); dose reduction only at CrCl 15-30 (label).  
  - why the pool answer is wrong: clean strong is the dialysis RCT title (PMID 36335914) - real but dialysis-specific; 27% renal excretion = moderate, not maximal.
- **apixaban / monitoring_burden**: 3 -> **1**  
  - source: PMID 34662890: "requires no dose adjustment or monitoring"; PMID 31089975: "without the need for therapeutic drug monitoring".  
  - why the pool answer is wrong: both sentences were LLM-labelled strong and auditor-FLAGGED: they say monitoring is NOT needed. The other two flagged strongs are warfarin-arm INR targets (comparator's burden, not apixaban's).
- **rivaroxaban / renal_clearance_dependence**: 2 -> **3**  
  - source: l2_pk.renal_excretion_pct = 66 (33% unchanged + 33% metabolites, PMID 24861792).  
  - why the pool answer is wrong: pool had 1 sentence, LLM-labelled none; label/PMID already record 66% renal.
- **rivaroxaban / monitoring_burden**: 3 -> **1**  
  - source: DailyMed XARELTO label: "Monitoring for the anticoagulation effect of rivaroxaban using a clotting test (PT, INR or aPTT) or anti-factor Xa (FXa) activity is not recommended."  
  - why the pool answer is wrong: rules capped it at 2 on anti-Xa/PT assay-availability papers, which measure assay capability, not routine monitoring burden.
- **rivaroxaban / gi_bleeding_risk**: 1 -> **3**  
  - source: DailyMed XARELTO label, 6 Clinical Trials Experience: GI bleeding 221 (2.0%) vs 140 (1.2%), HR 1.61 (1.30-1.99).  
  - why the pool answer is wrong: pool empty (0 drug-anchored GI sentences); label gives a significant increase vs warfarin.
- **edoxaban / renal_clearance_dependence**: 2 -> **3**  
  - source: l2_pk.renal_excretion_pct = 50; dose reduction to 30 mg if CrCl 15-50 (label).  
  - why the pool answer is wrong: pool had 1 sentence, LLM-labelled none; label already records the renal rule.
- **edoxaban / monitoring_burden**: 2 -> **1**  
  - source: DailyMed SAVAYSA label, 12.2 Pharmacodynamics: changes in PT, INR and aPTT "are small, subject to a high degree of variability and not useful in monitoring the anticoagulant effect of edoxaban."  
  - why the pool answer is wrong: pool had 1 sentence, LLM-labelled none; label states monitoring is not useful.
- **edoxaban / reversal_availability**: 1 -> **2**  
  - source: l4.reversal_agent = "andexanet alfa (partial; PMID 29345686)".  
  - why the pool answer is wrong: pool empty; the record already carries a partial-reversal agent, so 1 (none) is wrong and 3 (full antidote) overstates a partial agent.
- **dabigatran / renal_clearance_dependence**: 2 -> **3**  
  - source: l2_pk.renal_excretion_pct = 80-85 unchanged (PMID 31335150); t1/2 13 h -> 27 h as CrCl falls (label); contraindicated CrCl <30 (label).  
  - why the pool answer is wrong: pool had 1 sentence, LLM-labelled none; label/PMID already record 80-85% renal.
- **dabigatran / monitoring_burden**: 3 -> **1**  
  - source: DailyMed PRADAXA label, 12.2 Pharmacodynamics: "INR is relatively insensitive to the exposure to dabigatran and cannot be interpreted the same way as used for warfarin monitoring."  
  - why the pool answer is wrong: rules capped it at 2 on warfarin-TTR comparison sentences (the comparator's metric, not dabigatran's burden).

## Override that only attaches a citation (no value change)

- **apixaban / gi_bleeding_risk**: 1 -> **1** (unchanged) - L4 GI bleed HR 0.89 (0.70-1.14) vs warfarin - label ARISTOTLE table (curation draft, not yet written into drugs.json).
- **enoxaparin / ddi_risk**: 2 -> **2** (unchanged) - DailyMed LOVENOX label, 7 Drug Interactions: agents that enhance hemorrhage risk (anticoagulants, platelet inhibitors, NSAIDs) "should be discontinued"; if coadministration is essential, "conduct close clinical and laboratory monitoring". Label 12.3: "No pharmacokinetic interaction was observed between enoxaparin and thrombolytics".

## Label-sourcing pass (`curation/label_sourcing_e1.json`)

Run after your decision to fetch DailyMed labels instead of leaving cells null. Quotes are sliced verbatim out of the fetched SPL text.

| cell | status | value now | section | quote |
|---|---|---|---|---|
| rivaroxaban | gi_bleeding_risk | sourced | **3** | 6 Clinical Trials Experience | Gastrointestinal (GI) Gastrointestinal bleeding events included upper GI, lower GI, and rectal bleeding. 221 (2.0) 140 (1.2) 1.61 (1.30, 1.99) Fatal B |
| enoxaparin | gi_bleeding_risk | not_found | **null** |  | -Full label searched: no GI-specific bleeding rate or GI-site event count exists. Only a precaution for patients with active ulcerative/angiodysplastic |
| edoxaban | monitoring_burden | sourced | **1** | 12 Pharmacodynamics | Changes observed in PT, INR, and aPTT at the expected therapeutic dose, however, are small, subject to a high degree of variability and not useful in  |
| rivaroxaban | monitoring_burden | sourced | **1** | 5 Increased | Monitoring for the anticoagulation effect of rivaroxaban using a clotting test (PT, INR or aPTT) or anti-factor Xa (FXa) activity is not recommended.  |
| dabigatran | monitoring_burden | sourced | **1** | 12 Pharmacodynamics | INR is relatively insensitive to the exposure to dabigatran and cannot be interpreted the same way as used for warfarin monitoring. As in adults, ther |
| enoxaparin | ddi_risk | sourced | **2** | 12 Pharmacokinetics Absorption | No pharmacokinetic interaction was observed between enoxaparin and thrombolytics when administered concomitantly. 13 NONCLINICAL TOXICOLOGY 13.1 Carci |

## Cells that stay null

- **enoxaparin / gi_bleeding_risk** - label search found no GI-specific bleeding rate for enoxaparin (only a precaution for patients with active ulcerative/angiodysplastic GI disease). Pool empty too -> `null`, documented as `not_found`.

## Decisions taken (2026-09-27)

1. **All 7 originally proposed sourced overrides approved.**
2. **DDI filtered re-score (R7) approved** for the 6 ddi cells.
3. **Label fetch chosen over null** for the empty cells - done; 5/6 sourced.
4. **Source monitoring_burden then set to 1** for rivaroxaban + dabigatran - both sourced from the label and set to 1.
