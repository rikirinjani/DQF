# Enoxaparin — 4-Level Quantitative Profile

> **Role in PoC:** The parenteral LMWH comparator. Indirect, antithrombin-mediated factor Xa inhibition with PK measured in anti-Xa activity units rather than drug concentration. Bridges the anticoagulant class to VTE prophylaxis and ACS, and supplies the PoC's clearest null-handling case: `gi_bleeding_risk` is unsourced and stays null.

---

## L1 — Molecular Binding

### Primary Mechanism: Indirect Factor Xa Inhibition via Antithrombin III

| Target | Potency | Functional Effect |
|--------|---------|-------------------|
| **Antithrombin III (indirect)** | not sourced (indirect mechanism; no Ki applicable) | Potentiates antithrombin-mediated inhibition of factor Xa; anti-Xa to anti-IIa ratio ~3:1 (label) |

Enoxaparin is a low-molecular-weight heparin, not a small-molecule enzyme inhibitor: it acts by catalyzing antithrombin, and its potency is expressed as anti-Xa activity per mg, not as a binding constant. `l1_binding.targets` is accordingly empty in the record.

### Mechanism Position in the Class

| Feature | Finding | Source |
|---------|---------|--------|
| **Anti-Xa : anti-IIa ratio** | ~3:1 (predominantly anti-Xa) | label |
| **Direct target binding** | None (indirect, antithrombin-dependent) | label |

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | null (not sourced); values draft notes ~92% anti-Xa bioavailability after SC injection, without citation |
| **Half-life** | 4.5 h, measured as anti-Xa activity (label) |
| **Volume of distribution** | 4.3 L, anti-Xa activity distribution (label) |
| **Protein binding** | null (not sourced) |
| **Metabolism** | null (not sourced) |
| **Renal excretion** | 40% of radiolabeled dose and 8-20% of anti-Xa activity recovered in urine over 24 h (label) |

**PK Signature:** Subcutaneous administration with all PK expressed in anti-Xa units (label). The Vd of 4.3 L is the smallest in the set and the half-life (4.5 h) the shortest, supporting once- or twice-daily injection. Renal involvement is sufficient to require dose reduction to 1 mg/kg once daily when CrCl is below 30 mL/min (label), which underlies `renal_clearance_dependence` = 3. Absolute bioavailability and protein binding remain unsourced; no values are imputed here.

---

## L3 — Systems Response

Scale: each dimension is scored 1-3; higher = more of the named quantity. `anticoagulation_efficacy` and `reversal_availability` are benefit dimensions (higher is better); the other five are risk dimensions (higher is worse). Scores are the adjudicated cells of 2026-09-27 (`rag-queries/curation/anticoagulant_adjudication.json`), already merged into `api/drugs.json`; basis text is from the adjudication record.

| Dimension | Score | Direction | Basis (adjudication) |
|-----------|-------|-----------|----------------------|
| **anticoagulation_efficacy** | 3 | benefit | R1a: auto 3 supported by 1 audit-clean strong |
| **bleeding_risk** | 3 | risk | R1a: auto 3 supported by 2 audit-clean strong |
| **renal_clearance_dependence** | 3 | risk | R1a: auto 3 supported by 3 audit-clean strong |
| **ddi_risk** | 2 | risk | Override: LOVENOX label, 7 Drug Interactions: hemorrhage-enhancing agents (anticoagulants, platelet inhibitors, NSAIDs) "should be discontinued"; if coadministration is essential, "conduct close clinical and laboratory monitoring"; label 12.3: no PK interaction with thrombolytics |
| **monitoring_burden** | 3 | risk | R1a: auto 3 supported by 6 audit-clean strong |
| **reversal_availability** | 3 | benefit | R1a: auto 3 supported by 2 audit-clean strong |
| **gi_bleeding_risk** | null | risk | not sourced (no GI-specific rate in the LOVENOX label) |

**L3 Signature:** Enoxaparin shares warfarin's monitoring profile (3) from the opposite direction: an injectable whose label mandates close clinical and laboratory monitoring when co-administered with hemorrhage-risk agents (label, 7 Drug Interactions), with anti-Xa activity as the measurable. The DDI score of 2 reflects a purely pharmacodynamic interaction section plus an explicit negative for thrombolytics. GI bleeding risk is the only null in the class: the full LOVENOX label contains no GI-specific bleeding rate, only a precaution for active ulcerative or angiodysplastic disease (label_sourcing_e1.json), and the evidence pool was empty; per PoC rules, no value was substituted.

---

## L4 — Clinical Outcomes

### Vs-Warfarin Fields

| Outcome field | Value | Source |
|---------------|-------|--------|
| **stroke_se_reduction_vs_warfarin** | null (not sourced) | drugs.json |
| **major_bleeding_hr_vs_warfarin** | null (not sourced) | drugs.json |
| **ich_reduction** | null (not sourced) | drugs.json |

Enoxaparin sits outside the vs-warfarin axis: the record carries no AF non-inferiority comparison, and its indication list contains no stroke-prevention entry (drugs.json).

### Dosing

| Item | Value | Source |
|------|-------|--------|
| **VTE regimens** | Prophylaxis 30 mg q12h; treatment 1 mg/kg q12h | label (values draft) |
| **Renal dose reduction** | CrCl <30: 1 mg/kg once daily | label |
| **Onset** | null (not sourced) | drugs.json |

### Reversal

| Agent | Effect | Source |
|-------|--------|--------|
| **Protamine** | Partial reversal | label |

Note: the adjudicated `reversal_availability` cell is 3 (R1a, 2 audit-clean strong), while the label characterizes protamine reversal as partial. Both facts are recorded here as sourced; the divergence is flagged rather than reconciled by editing either value.

### Indications

- VTE prophylaxis
- VTE treatment
- Acute coronary syndrome

(drugs.json; label)

### Special-Population Safety

| Population | Rating | Source |
|------------|--------|--------|
| **Pregnancy** | Caution; mechanical valve thrombosis risk | label |
| **Lactation** | Unknown | label |
| **Hepatic** | Not studied (unknown) | label |

---

## Key References

| Source | Supports |
|--------|----------|
| label (DailyMed setid 20635579-c92d-4f6c-a332-1096d51002f2) | Anti-Xa:anti-IIa ~3:1; t½ 4.5 h; Vd 4.3 L; urinary recovery; DDI section; dose regimens; protamine; pregnancy/lactation/hepatic |
| label_sourcing_e1.json | Verbatim LOVENOX DDI quote; documented not_found result for GI bleeding |
| values draft (rag-queries/curation/anticoagulant_values_draft.md) | VTE dosing regimens; documented nulls (bioavailability, protein binding, metabolism) |
| anticoagulant_adjudication.json | All seven L3 cells including the null GI cell |

## Framework Takeaways for Enoxaparin

1. **Null is a finding, not a gap:** the label search returned no GI-specific rate (label_sourcing_e1.json), the evidence pool was empty, and the cell stayed null. This is the PoC's cleanest demonstration that unsourced means unsourced.
2. **PK in different units:** anti-Xa activity replaces concentration, so L2 comparisons with the oral agents are qualitative (4.3 L distribution, 4.5 h half-life, label) rather than numerically commensurable.
3. **Monitoring burden without INR:** enoxaparin scores 3 on monitoring like warfarin but for different reasons, injection logistics plus laboratory monitoring during interacting co-therapy (label), showing the dimension aggregates distinct burdens.
4. **Value/label tension surfaced, not smoothed:** reversal scores 3 on clean strong evidence while the label says protamine is partial; the profile records both and leaves reconciliation to the adjudication layer.
