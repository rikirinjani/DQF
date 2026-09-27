# Dabigatran — 4-Level Quantitative Profile

> **Role in PoC:** The only direct thrombin inhibitor in the set and the only prodrug. The renal extreme of the class (80-85% unchanged renal excretion) paired with the only dedicated specific antidote (idarucizumab). Demonstrates that a single drug can hold both the highest renal risk and the fullest reversal benefit.

---

## L1 — Molecular Binding

### Primary Target: Thrombin (Factor IIa)

| Target | Potency | Functional Effect |
|--------|---------|-------------------|
| **Thrombin (FIIa)** | Ki 4.5 nM, recorded as 8.35 (-log10 Ki) | Oral direct competitive thrombin inhibition; selective and reversible (PMID 17598008) |

Dabigatran is administered as the prodrug **dabigatran etexilate**; the active moiety binds thrombin directly and reversibly (PMID 17598008). Its Ki (4.5 nM) is an order of magnitude weaker than the FXa Ki values of rivaroxaban and edoxaban, but the targets differ, so the comparison is descriptive, not ordinal.

### Prodrug Feature (L2-relevant)

| Feature | Finding | Source |
|---------|---------|--------|
| **Etexilate activation** | Prodrug converted to active dabigatran | label |
| **Transporter status** | Etexilate is a P-gp substrate; dabigatran is not CYP-metabolized | label |

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 3-7% absolute (label); 5 recorded in drugs.json |
| **Half-life** | 12-14 h (PMID 19696042); label renal table: 13 h at CrCl 80 or higher, 18 h at CrCl 30-50, 27 h at CrCl 15-30 |
| **Volume of distribution** | 50-70 L (label); 60 L recorded in drugs.json |
| **Protein binding** | 35% (label) |
| **Metabolism** | Etexilate is a P-gp substrate; dabigatran not CYP-metabolized (label) |
| **Renal excretion** | 80-85% excreted unchanged (PMID 31335150) |

**PK Signature:** Lowest bioavailability (3-7%, label) and lowest protein binding (35%, label) in the class, consequences of the prodrug design. Elimination is overwhelmingly renal: 80-85% unchanged drug (PMID 31335150), with the label's renal table showing half-life more than doubling from 13 h to 27 h as CrCl falls to 15-30 mL/min. This is the physical basis for `renal_clearance_dependence` = 3 and the CrCl <30 contraindication (EU/Canada label).

---

## L3 — Systems Response

Scale: each dimension is scored 1-3; higher = more of the named quantity. `anticoagulation_efficacy` and `reversal_availability` are benefit dimensions (higher is better); the other five are risk dimensions (higher is worse). Scores are the adjudicated cells of 2026-09-27 (`rag-queries/curation/anticoagulant_adjudication.json`), already merged into `api/drugs.json`; basis text is from the adjudication record.

| Dimension | Score | Direction | Basis (adjudication) |
|-----------|-------|-----------|----------------------|
| **anticoagulation_efficacy** | 3 | benefit | R1a: auto 3 supported by 6 audit-clean strong |
| **bleeding_risk** | 3 | risk | R1a: auto 3 supported by 6 audit-clean strong |
| **renal_clearance_dependence** | 3 | risk | Override: renal excretion 80-85% unchanged (PMID 31335150); t½ 13 h to 27 h as CrCl falls (label); contraindicated CrCl <30 (label) |
| **ddi_risk** | 3 | risk | R7: filtered re-score on 3 pk/pd sentences |
| **monitoring_burden** | 1 | risk | Override: PRADAXA label, 12.2 Pharmacodynamics: "INR is relatively insensitive to the exposure to dabigatran and cannot be interpreted the same way as used for warfarin monitoring" |
| **reversal_availability** | 3 | benefit | R1a: auto 3 supported by 3 audit-clean strong |
| **gi_bleeding_risk** | 2 | risk | R2a: moderate-only evidence (2 moderate, 0 flagged strong); 3 not earned |

**L3 Signature:** Dabigatran pairs the class maximum on renal dependence with the strongest reversal story: idarucizumab is a specific antibody antidote (PMID 27789605), not a partially effective agent. The monitoring score came from the label's statement that INR cannot be used for dabigatran; the pool sentences that pushed the rules toward 2 were warfarin time-in-therapeutic-range comparisons, the comparator's metric rather than dabigatran's burden (`why_pool_differs`).

---

## L4 — Clinical Outcomes

### RE-LY vs Warfarin

| Outcome | Result | Source |
|---------|--------|--------|
| **Stroke/SE, 150 mg dose** | Superior to warfarin | PMID 22435606 |
| **Major bleeding HR** | null (not sourced; RE-LY numeric not cleanly extractable, per values draft) | drugs.json |
| **ICH** | null (not sourced) | drugs.json |

### Dosing and Contraindications

| Item | Value | Source |
|------|-------|--------|
| **Renal limit** | Contraindicated if CrCl <30 (EU/Canada) | label |
| **Valve exclusion** | Not recommended in mechanical heart valves | label |
| **Onset** | 120 min | drugs.json |

### Reversal

| Agent | Effect | Source |
|-------|--------|--------|
| **Idarucizumab** | Specific reversal agent for dabigatran | PMID 27789605 |

### Indications

- Stroke prevention in non-valvular AF
- VTE treatment/prophylaxis

(drugs.json; label)

### Special-Population Safety

| Population | Rating | Source |
|------------|--------|--------|
| **Pregnancy** | Limited data | label |
| **Lactation** | Unknown | label |
| **Hepatic** | Moderate (Child-Pugh B): no consistent change | label |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 17598008 | Thrombin Ki 4.5 nM; selective, reversible inhibition |
| PMID 19696042 | Half-life 12-14 h |
| PMID 22435606 | RE-LY: superiority at 150 mg |
| PMID 27789605 | Idarucizumab reversal |
| PMID 31335150 | Renal excretion 80-85% unchanged |
| label (DailyMed setid 9ac0a64a-8666-45f7-9d4f-40fd894f7e6d) | F 3-7%; renal half-life table; Vd 50-70 L; protein binding 35%; P-gp/CYP status; contraindications; pregnancy/lactation/hepatic |
| label_sourcing_e1.json | Verbatim PRADAXA monitoring quote |
| anticoagulant_adjudication.json | All seven L3 cells |

## Framework Takeaways for Dabigatran

1. **Renal extreme vs warfarin's hepatic clearance:** 80-85% unchanged renal excretion (PMID 31335150) against warfarin's CYP-metabolized elimination (PMID 9014207) is the widest clearance contrast in the class and drives the L3 renal column (3 vs 1).
2. **Highest risk, fullest rescue:** the same drug scores 3 on renal dependence and 3 on reversal; a single-score comparator would average away this pairing.
3. **Prodrug penalty is quantifiable:** etexilate design costs ~95% of oral bioavailability (3-7%, label) yet still supports twice-daily dosing, showing L1 form and L2 exposure trade off rather than track each other.
4. **Null honesty at L4:** the major-bleeding HR remains null because the RE-LY numeric was not cleanly extractable (values draft); the L3 bleeding cell (3) carries the comparison instead.
