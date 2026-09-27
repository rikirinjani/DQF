# Anticoagulant PoC — Cross-Comparison Table (6 Drugs)

> **Role in PoC:** Tests whether the 4-level framework separates four mechanisms (vitamin K antagonist, three direct factor Xa inhibitors, one direct thrombin inhibitor, one LMWH) on a shared grid, and whether the adjudicated 7-dimension L3 layer adds signal where the vs-warfarin L4 fields are null or saturated.

---

## L1 — Molecular Binding Comparison

| Property | Warfarin | Apixaban | Rivaroxaban | Edoxaban | Dabigatran | Enoxaparin |
|----------|----------|----------|-------------|----------|------------|------------|
| **Primary target** | VKOR (label) | Factor Xa (PMID 24733535) | Factor Xa (PMID 37207560) | Factor Xa (PMID 25966665) | Thrombin, FIIa (PMID 17598008) | Antithrombin III, indirect (label) |
| **Potency (Ki)** | not sourced | not sourced | 0.4 nmol/L (PMID 20139357) | 0.561 nmol/L (PMID 18624979) | 4.5 nM (PMID 17598008) | not sourced (indirect) |
| **Prodrug** | No | No | No | No | Yes, etexilate (label) | No |
| **Selectivity statement** | CYP2C9/VKORC1 genotype-dependent dosing (label; PMID 9014207) | Highly selective FXa (PMID 24733535) | FXa-selective (label) | >10,000-fold for FXa (PMID 18624979) | Selective, reversible thrombin (PMID 17598008) | anti-Xa : anti-IIa ~3:1 (label) |
| **Interaction liability at the target level** | CYP2C9/1A2/3A4 oxidation (PMID 9014207) | P-gp/BCRP not clinically relevant (PMID 42124949); combined P-gp + strong CYP3A4 rule (label) | CYP3A4 + P-gp substrate (label) | P-gp substrate, minimal CYP (label) | Etexilate P-gp substrate, not CYP-metabolized (label) | not sourced |

### Key Differentiation
1. **Three points of attack:** factor synthesis (warfarin at VKOR), factor Xa (apixaban, rivaroxaban, edoxaban directly; enoxaparin indirectly via antithrombin), and thrombin (dabigatran). One class, three mechanistic levels.
2. **Potency is sourced for only 3 of 6:** rivaroxaban (0.4 nmol/L) and edoxaban (0.561 nmol/L) share a target, so their Ki values are comparable; dabigatran's 4.5 nM is against thrombin and not rank-orderable against the FXa pair.
3. **Only dabigatran is a prodrug** (etexilate, label), which explains its 3-7% bioavailability at L2.
4. **Only warfarin has pharmacogenomic dosing** (CYP2C9/VKORC1, PMID 9014207).
5. **Enoxaparin has no molecular potency at all:** antithrombin-mediated activity measured as anti-Xa units (label).

---

## L2 — Pharmacokinetic Comparison

| Parameter | Warfarin | Apixaban | Rivaroxaban | Edoxaban | Dabigatran | Enoxaparin |
|-----------|----------|----------|-------------|----------|------------|------------|
| **Route** | Oral | Oral | Oral | Oral | Oral | Subcutaneous |
| **Bioavailability** | null (not sourced) | ~50% (label) | 80-100% at 10 mg (PMID 23999929) | 62% (label) | 3-7% (label) | null (not sourced) |
| **Half-life** | 20-60 h effective (label) | 12 h (PMID 22722590) | 5-9 h young, 11-13 h elderly (PMID 23999929) | 10-14 h (label) | 12-14 h, rising to 27 h at CrCl 15-30 (PMID 19696042; label) | 4.5 h, anti-Xa units (label) |
| **Volume of distribution** | 0.14 L/kg (PMID 3542339) | 21 L (PMID 24353445) | 50 L (label) | 107 L (PMID 26620048) | 50-70 L (label) | 4.3 L (label) |
| **Protein binding** | 99% (label) | 87% (label) | 92% (label) | 55% (label) | 35% (label) | null (not sourced) |
| **Renal excretion** | null as parent; 92% as metabolites (label) | 27% (PMID 24861792) | 66% (PMID 24861792) | 50% (PMID 24861792) | 80-85% unchanged (PMID 31335150) | 8-20% anti-Xa activity, 40% radioactivity in 24 h urine (label) |
| **Renal dose rule** | None; INR-titrated (label) | 2.5 mg BID rule includes CrCl 15-30 (label) | None recorded in drugs.json | 30 mg if CrCl 15-50 (label) | Contraindicated CrCl <30, EU/Canada (label) | 1 mg/kg once daily if CrCl <30 (label) |
| **Food requirement** | not sourced | not sourced | 15/20 mg require food (PMID 23999929; 23458226) | not sourced | not sourced | not applicable |

### Key Differentiation
1. **Renal elimination spans the class:** dabigatran 80-85% unchanged (PMID 31335150) at one end, warfarin hepatically cleared with only metabolites in urine (label) at the other. This gradient is the physical basis of the L3 renal column (3/3/3/2/1/3).
2. **Warfarin's effective half-life (20-60 h, label) is several times the DOAC range (4.5-14 h):** the pharmacokinetic reason warfarin needs slow titration and loading strategy while every DOAC is fixed-dose.
3. **Bioavailability extremes:** rivaroxaban 80-100% at 10 mg (PMID 23999929) vs dabigatran 3-7% (label), a prodrug penalty of roughly twenty-fold.
4. **Protein binding spans 99% (warfarin) to 35% (dabigatran),** with enoxaparin unsourced.
5. **Enoxaparin is quantified differently:** anti-Xa activity units, subcutaneous route, smallest Vd (4.3 L, label); its L2 rows are not numerically commensurable with the oral drugs.

---

## L3 — Systems Response Comparison

Scale: each dimension is scored 1-3; higher = more of the named quantity. `anticoagulation_efficacy` and `reversal_availability` are benefit dimensions (higher is better); `bleeding_risk`, `renal_clearance_dependence`, `ddi_risk`, `monitoring_burden`, and `gi_bleeding_risk` are risk dimensions (higher is worse). Scores are the adjudicated 2026-09-27 cells, merged into `api/drugs.json`.

| Dimension | Warfarin | Apixaban | Rivaroxaban | Edoxaban | Dabigatran | Enoxaparin |
|-----------|----------|----------|-------------|----------|------------|------------|
| **anticoagulation_efficacy** (benefit) | 3 | 3 | 3 | 3 | 3 | 3 |
| **bleeding_risk** (risk) | 3 | 3 | 3 | 3 | 3 | 3 |
| **renal_clearance_dependence** (risk) | 1 | 2 | 3 | 3 | 3 | 3 |
| **ddi_risk** (risk) | 2 | 3 | 3 | 2 | 3 | 2 |
| **monitoring_burden** (risk) | 3 | 1 | 1 | 1 | 1 | 3 |
| **reversal_availability** (benefit) | 3 | 3 | 3 | 2 | 3 | 3 |
| **gi_bleeding_risk** (risk) | 3 | 1 | 3 | 2 | 2 | null |

### Key Differentiation
1. **Two dimensions are saturated:** efficacy and overall bleeding are 3 for all six drugs. As with the statin class, the framework's separating power concentrates in the remaining five dimensions.
2. **Renal column splits the class:** warfarin 1 (hepatic, PMID 9014207) vs dabigatran/rivaroxaban/edoxaban/enoxaparin 3; apixaban 2 on 27% renal excretion (PMID 24861792), the only intermediate.
3. **Monitoring splits 3/1:** warfarin (INR titration) and enoxaparin (injection plus laboratory monitoring per label) vs all four DOACs whose labels state monitoring is not recommended or not useful (XARELTO, SAVAYSA, PRADAXA quotes in label_sourcing_e1.json).
4. **Reversal:** edoxaban 2 is the only non-3 (partial andexanet, PMID 29345686). Dabigatran's 3 rests on a specific antibody antidote (idarucizumab, PMID 27789605); enoxaparin's 3 was kept on 2 audit-clean strong sentences even though the label calls protamine partial, a recorded value/label tension.
5. **GI bleeding anchors the extremes in labels:** rivaroxaban 3 (HR 1.61 vs warfarin, label) against apixaban 1 (HR 0.89, label); enoxaparin null (no GI-specific rate in the LOVENOX label).

---

## L4 — Clinical Outcomes Comparison

| Property | Warfarin | Apixaban | Rivaroxaban | Edoxaban | Dabigatran | Enoxaparin |
|----------|----------|----------|-------------|----------|------------|------------|
| **Pivotal AF trial** | Reference arm | ARISTOTLE (PMID 21870978) | ROCKET AF (label) | ENGAGE AF-TIMI 48 (PMID 38828563) | RE-LY (PMID 22435606) | none in record (no AF indication) |
| **Stroke/SE vs warfarin** | Reference | Superior (PMID 21870978) | HR 0.88 (label) | Favorable trend, HR 0.87 (PMID 38828563) | Superior at 150 mg (PMID 22435606) | null (not sourced) |
| **Major bleeding HR** | Reference | 0.69 (0.60-0.80) (label) | null (not sourced) | 0.80 (label) | null (not sourced) | null (not sourced) |
| **ICH** | Reference | HR 0.41 (0.30-0.57) (label) | HR 0.58 (0.35-0.96) (label) | null (not sourced) | null (not sourced) | null (not sourced) |
| **GI bleeding** | Reference | HR 0.89 (0.70-1.14) (label) | HR 1.61 (1.30-1.99) (label) | null (not sourced) | null (not sourced) | null (not sourced) |
| **Reversal agent** | Vitamin K + PCC (label) | Andexanet alfa, 92-94% anti-Xa reduction (PMID 29345686) | Andexanet alfa (PMID 29345686) | Andexanet alfa, partial (PMID 29345686) | Idarucizumab (PMID 27789605) | Protamine, partial (label) |
| **Onset (min)** | null (not sourced) | 180 (drugs.json) | 180 (drugs.json) | 120 (drugs.json) | 120 (drugs.json) | null (not sourced) |
| **Distinct indication** | Mechanical heart valves (drugs.json; label) | Post hip/knee prophylaxis (drugs.json) | CAD/PAD with aspirin (label) | Shared AF/VTE only (drugs.json) | Shared AF/VTE only (drugs.json) | ACS; VTE prophylaxis (drugs.json; label) |

### Key Differentiation
1. **Apixaban is the only triple win vs warfarin:** superior stroke prevention, less major bleeding (HR 0.69), and lower mortality in ARISTOTLE (PMID 21870978). Each other DOAC concedes one axis or lacks a sourced HR for it.
2. **Rivaroxaban is the only labeled GI increase (HR 1.61); apixaban runs the other way (HR 0.89):** same dimension, opposite directions, both from labels. Rivaroxaban simultaneously lowers fatal bleeding (HR 0.50) and ICH (HR 0.58), so its bleeding profile is site-dependent, not uniformly worse.
3. **Two major-bleeding HRs are null** (rivaroxaban, dabigatran; not cleanly extractable per values draft), and the L3 adjudicated cells carry those columns instead.
4. **Reversal pharmacology splits three ways:** idarucizumab (specific antibody, dabigatran) vs andexanet alfa (FXa decoy for the anti-Xa DOACs, partial for edoxaban in this record) vs vitamin K + PCC (warfarin) vs protamine (partial, enoxaparin).
5. **Enoxaparin sits outside the vs-warfarin axis entirely:** parenteral, indicated for VTE prophylaxis/treatment and ACS, with all three vs-warfarin L4 fields null.
6. **Onset is sourced only for the DOACs (120-180 min, drugs.json);** warfarin and enoxaparin remain null.

---

## Framework-Specific Findings (Anticoagulant Class)

| Feature | Observation | Evidence |
|---------|-------------|----------|
| **Saturated benefit/risk cells** | Efficacy and bleeding are 3 for all six drugs; differentiation lives in 5 of 7 dimensions | anticoagulant_adjudication.json |
| **Direction-typed dimensions** | 2 benefit and 5 risk dimensions declared up front, so the artifact gate worked from day one | phase2-anticoagulant-design.md |
| **Null honesty** | One L3 cell (enoxaparin GI), one L2 field (warfarin F), and two L4 HRs (rivaroxaban, dabigatran major bleeding) stay null with documented searches | label_sourcing_e1.json; values draft |
| **Cross-level causal chain** | Dabigatran L2 80-85% renal (PMID 31335150) → L3 renal 3 → L4 CrCl <30 contraindication (label) | drugs.json; adjudication |
| **Comparator asymmetry** | Warfarin defines the L4 axis but carries no HRs of its own; its profile is completed by the other five drugs | drugs.json |
| **Adjudication value added** | 14 of 42 L3 cells changed vs the v2 auto-score, 11 via sourced overrides (e.g. warfarin renal 3→1, rivaroxaban GI 1→3) | anticoagulant_adjudication_draft.md |

### Framework Limitations Observed

| Limitation | Impact |
|------------|--------|
| **Efficacy/bleeding saturation** | The two most clinically salient dimensions do not separate the class at L3; per-drug distinction must come from L4 HRs or the remaining five L3 cells |
| **Missing L4 HRs** | With rivaroxaban and dabigatran major-bleeding HRs null, cross-drug bleeding comparisons lean on label fragments and L3 cells |
| **Monitoring is a process dimension** | It separates warfarin/enoxaparin (3) from DOACs (1) without describing any clinical outcome difference; consumers must not read it as efficacy or harm |
| **Reversal value/label tension** | Enoxaparin scores 3 while its label characterizes protamine as partial; the framework records both rather than resolving the conflict |

---

## Summary: Framework Value for Anticoagulants vs Statins

| Dimension | Statin Class | Anticoagulant Class | Verdict |
|-----------|--------------|---------------------|---------|
| **Drug differentiation at L3** | Low-moderate (5 identical per-mmol-LDL outcomes) | Moderate (5 of 7 dimensions split the class) | Framework differentiates anticoagulants better |
| **Safety signal diversity** | Low (degree, not kind) | Moderate (GI, renal, monitoring, reversal axes differ in kind) | Anticoagulants exercise more dimensions |
| **L4 completeness** | High (CTT class estimate) | Partial (nulls for 2 major-bleeding HRs, all enoxaparin comparisons) | Statin L4 was more complete |
| **Null handling** | Rare | Systematic (documented searches, no substitution) | Anticoagulant PoC stress-tested this and held |
| **Comparator structure** | None (class vs placebo baseline) | Single shared comparator (warfarin) | Simplifies cross-drug L4 reading |

### Bottom Line
The 4-level framework generalizes to the anticoagulant class and differentiates it better than the statin class. Efficacy and overall bleeding saturate at 3, echoing the statin finding, but renal dependence, monitoring burden, reversal, GI risk, and DDI risk each split the six drugs into distinct groups, and several splits (rivaroxaban vs apixaban GI, warfarin vs dabigatran clearance, idarucizumab vs andexanet vs protamine) are anchored in labels and PMIDs rather than inference. The L4 layer is comparator-shaped and partially null, so the adjudicated L3 cells do most of the separating work, which is the intended division of labor between the levels.
