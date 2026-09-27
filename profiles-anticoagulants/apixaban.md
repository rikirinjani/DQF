# Apixaban — 4-Level Quantitative Profile

> **Role in PoC:** Oral direct factor Xa inhibitor. The only DOAC in this set that beat warfarin on stroke, major bleeding, and mortality simultaneously in its pivotal trial (ARISTOTLE). Lowest renal-dependence and lowest GI-bleeding scores among the DOACs.

---

## L1 — Molecular Binding

### Primary Target: Factor Xa

| Target | Potency | Functional Effect |
|--------|---------|-------------------|
| **Factor Xa (FXa)** | not sourced (no Ki in the label or the curated pool) | Oral, direct, highly selective FXa inhibition (PMID 24733535) |

Apixaban's `l1_binding.targets` list is empty and the values draft lists its L1 potency under "Still null". The mechanism is sourced (PMID 24733535), but no binding constant was retrievable, so no potency number appears in this profile.

### Transporters (L2-relevant)

| Transporter | Finding | Source |
|-------------|---------|--------|
| **P-gp / BCRP** | Efflux transporters not clinically relevant for apixaban disposition | PMID 42124949 |

Despite P-gp substrate status, the disposition evidence does not support a transporter-driven interaction claim (PMID 42124949). The labeled interaction rule is combined P-gp plus strong CYP3A4 inhibition (label).

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | ~50% absolute (label); 66.2% in the dedicated IV/oral study (PMID 24353445) |
| **Half-life** | 12 h (PMID 22722590; label) |
| **Volume of distribution** | 21 L, with 17-26 L at steady state (PMID 24353445); 0.177 L/kg (label) |
| **Protein binding** | 87% (label) |
| **Metabolism / transport** | P-gp + strong CYP3A4 substrate; combined inhibitors require 50% dose reduction (label) |
| **Renal excretion** | ~27% (PMID 24353445; 24861792) |

**PK Signature:** Moderate oral bioavailability, dual elimination (27% renal plus CYP3A4/P-gp pathways), and a 12 h half-life supporting twice-daily dosing. Apixaban has the lowest renal excretion fraction of the four DOACs with sourced values, which is the physical basis for `renal_clearance_dependence` = 2 rather than 3 (adjudication: the 27% figure is moderate; the dialysis RCT, PMID 36335914, is real but dialysis-specific).

---

## L3 — Systems Response

Scale: each dimension is scored 1-3; higher = more of the named quantity. `anticoagulation_efficacy` and `reversal_availability` are benefit dimensions (higher is better); the other five are risk dimensions (higher is worse). Scores are the adjudicated cells of 2026-09-27 (`rag-queries/curation/anticoagulant_adjudication.json`), already merged into `api/drugs.json`; basis text is from the adjudication record.

| Dimension | Score | Direction | Basis (adjudication) |
|-----------|-------|-----------|----------------------|
| **anticoagulation_efficacy** | 3 | benefit | R1a: auto 3 supported by 3 audit-clean strong |
| **bleeding_risk** | 3 | risk | R1a: auto 3 supported by 7 audit-clean strong |
| **renal_clearance_dependence** | 2 | risk | Override: renal excretion 27% (PMID 24353445/24861792); dose reduction only at CrCl 15-30 (label) |
| **ddi_risk** | 3 | risk | R7: filtered re-score on 3 pk/pd sentences |
| **monitoring_burden** | 1 | risk | Override: "requires no dose adjustment or monitoring" (PMID 34662890); "without the need for therapeutic drug monitoring" (PMID 31089975) |
| **reversal_availability** | 3 | benefit | R1a: auto 3 supported by 1 audit-clean strong |
| **gi_bleeding_risk** | 1 | risk | Override: GI bleed HR 0.89 (0.70-1.14) vs warfarin, ARISTOTLE label table |

**L3 Signature:** Apixaban holds the class-low GI score (1) on a labeled non-significant decrease vs warfarin (HR 0.89), the mirror image of rivaroxaban's labeled increase. The monitoring pool contained sentences LLM-labelled strong that were auditor-flagged negatives: they state monitoring is not needed, and the remaining flagged strongs were warfarin-arm INR targets, the comparator's burden rather than apixaban's (adjudication record, `why_pool_differs`).

---

## L4 — Clinical Outcomes

### ARISTOTLE vs Warfarin

| Outcome | Result | Source |
|---------|--------|--------|
| **Stroke / systemic embolism** | Superior; with less bleeding and lower mortality | PMID 21870978 |
| **Major bleeding** | HR 0.69 (0.60-0.80) | label (ARISTOTLE) |
| **Intracranial hemorrhage** | HR 0.41 (0.30-0.57) | label |
| **GI bleeding** | HR 0.89 (0.70-1.14) | label |

### Dosing

| Item | Value | Source |
|------|-------|--------|
| **Standard dose reduction** | 2.5 mg BID if at least 2 of: age 80 or older, weight 60 kg or less, CrCl 15-30 mL/min | label |
| **Interaction dose reduction** | 50% reduction with combined P-gp + strong CYP3A4 inhibitors | label |
| **Onset** | 180 min | drugs.json |

### Reversal

| Agent | Effect | Source |
|-------|--------|--------|
| **Andexanet alfa** | Reduces anti-Xa activity 92-94% | PMID 29345686 |

### Indications

- Stroke prevention in non-valvular AF
- VTE treatment/prophylaxis
- Post hip/knee replacement prophylaxis

(drugs.json; label)

### Special-Population Safety

| Population | Rating | Source |
|------------|--------|--------|
| **Pregnancy** | Not recommended | label |
| **Lactation** | Unknown; avoid | label |
| **Hepatic** | Severe impairment: not recommended | label |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 21870978 | ARISTOTLE: superiority vs warfarin on stroke/SE, bleeding, mortality |
| PMID 24353445 | Dedicated IV/oral PK study: F 66.2%, Vd 17-26 L |
| PMID 24861792 | Renal excretion ~27% (cross-class review) |
| PMID 22722590 | Half-life 12 h |
| PMID 29345686 | Andexanet alfa reversal, 92-94% anti-Xa reduction |
| PMID 34662890; PMID 31089975 | No monitoring required (monitoring_burden = 1) |
| label (DailyMed setid 41a133ef-e461-48ad-8221-b735bdd0ec25) | F ~50%; protein binding 87%; dose-reduction rules; ARISTOTLE HR tables; pregnancy/lactation/hepatic |
| anticoagulant_adjudication.json | All seven L3 cells |

## Framework Takeaways for Apixaban

1. **Only triple win vs warfarin:** superior stroke prevention with less bleeding and lower mortality (ARISTOTLE, PMID 21870978); the other DOACs each concede at least one axis or lack a sourced HR.
2. **GI dimension, two directions:** apixaban HR 0.89 (label) vs rivaroxaban HR 1.61 (label) anchors the class extremes of `gi_bleeding_risk` (1 vs 3) with the same evidence type.
3. **Flagged-negative evidence handled correctly:** the monitoring cell's apparent "strong" sentences were statements that monitoring is not needed; adjudication scored the dimension 1 accordingly.
4. **Renal gradient position:** 27% renal excretion (PMID 24861792) places apixaban between warfarin (hepatic) and the 50-85% renal DOACs, scored 2.
