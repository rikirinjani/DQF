# Rivaroxaban — 4-Level Quantitative Profile

> **Role in PoC:** Oral direct factor Xa inhibitor with the highest bioavailability in the class and once-daily AF dosing. The one DOAC whose label shows a significant GI bleeding increase vs warfarin. Broadest indication set (AF, VTE, surgical prophylaxis, CAD/PAD).

---

## L1 — Molecular Binding

### Primary Target: Factor Xa

| Target | Potency | Functional Effect |
|--------|---------|-------------------|
| **Factor Xa (FXa)** | Ki 0.4 nmol/L, recorded as 9.4 (-log10 Ki) | Direct FXa inhibition (PMID 37207560; PMID 20139357) |

Rivaroxaban is one of only three drugs in this class with a sourced small-molecule potency value (PMID 20139357). Its affinity is the highest recorded in the set, though only edoxaban shares the same target, so Ki comparison across the class is meaningful for exactly one pair.

### Interaction-relevant Binding Features

| Feature | Finding | Source |
|---------|---------|--------|
| **CYP3A4 + P-gp substrate** | Avoid combined strong inhibitors/inducers | label |
| **Selectivity** | FXa-selective | label |

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | 80-100% for 10 mg, food-independent; 15/20 mg require food (PMID 23999929; 23458226); 80 recorded in drugs.json |
| **Half-life** | 5-9 h in young adults, 11-13 h in elderly (PMID 23999929); 7 h recorded in drugs.json |
| **Volume of distribution** | 50 L (label) |
| **Protein binding** | 92% (label) |
| **Metabolism** | CYP3A4 + P-gp substrate; avoid strong combined inhibitors/inducers (label) |
| **Renal excretion** | 66% (33% unchanged + 33% metabolites) (PMID 24861792) |

**PK Signature:** The food effect is dose-dependent: 10 mg absorbs fully without food, while 15/20 mg doses require food to reach adequate exposure (PMID 23999929; 23458226), a unique administration constraint in this set. Elimination splits evenly between renal routes (33% unchanged drug plus 33% metabolites, PMID 24861792), making rivaroxaban substantially renally dependent. Half-life nearly doubles in elderly patients (11-13 h vs 5-9 h, PMID 23999929).

---

## L3 — Systems Response

Scale: each dimension is scored 1-3; higher = more of the named quantity. `anticoagulation_efficacy` and `reversal_availability` are benefit dimensions (higher is better); the other five are risk dimensions (higher is worse). Scores are the adjudicated cells of 2026-09-27 (`rag-queries/curation/anticoagulant_adjudication.json`), already merged into `api/drugs.json`; basis text is from the adjudication record.

| Dimension | Score | Direction | Basis (adjudication) |
|-----------|-------|-----------|----------------------|
| **anticoagulation_efficacy** | 3 | benefit | R1a: auto 3 supported by 6 audit-clean strong |
| **bleeding_risk** | 3 | risk | R1a: auto 3 supported by 3 audit-clean strong |
| **renal_clearance_dependence** | 3 | risk | Override: renal excretion 66%, 33% unchanged + 33% metabolites (PMID 24861792) |
| **ddi_risk** | 3 | risk | R7: filtered re-score on 2 pk/pd sentences |
| **monitoring_burden** | 1 | risk | Override: XARELTO label states clotting-test (PT, INR, aPTT) or anti-FXa monitoring "is not recommended" |
| **reversal_availability** | 3 | benefit | R1a: auto 3 supported by 3 audit-clean strong |
| **gi_bleeding_risk** | 3 | risk | Override: XARELTO label, 6 Clinical Trials Experience: GI bleeding 221 (2.0%) vs 140 (1.2%), HR 1.61 (1.30-1.99) |

**L3 Signature:** Rivaroxaban is the GI extreme of the class. The evidence pool for GI bleeding was empty, but the label carries a quantified, significant increase vs warfarin (HR 1.61), so the cell was raised from the auto-score of 1 to 3 (adjudication override). Monitoring was set to 1 because the label explicitly recommends against routine monitoring; the pool sentences that pushed the rules toward 2 measured assay availability, not clinical monitoring burden (`why_pool_differs`).

---

## L4 — Clinical Outcomes

### Pivotal Results

| Outcome | Result | Source |
|---------|--------|--------|
| **Stroke/SE vs warfarin (ROCKET AF)** | HR 0.88 | label |
| **VTE, EINSTEIN-DVT** | HR 0.68 | label |
| **CAD/PAD, COMPASS (MACE)** | HR 0.76 | label |
| **Major bleeding HR vs warfarin** | null (not sourced; no clean label extraction) | drugs.json |
| **GI bleeding vs warfarin** | 221 (2.0%) vs 140 (1.2%), HR 1.61 (1.30-1.99) | label, 6 Clinical Trials Experience |
| **Fatal bleeding vs warfarin** | 27 (0.2%) vs 55 (0.5%), HR 0.50 (0.31-0.79) | label, via label_sourcing_e1.json |
| **ICH vs warfarin** | 24 (0.2%) vs 42 (0.4%), HR 0.58 (0.35-0.96) | label, via label_sourcing_e1.json |

### Dosing

| Item | Value | Source |
|------|-------|--------|
| **DVT/PE** | 15 mg BID for 21 days, then 20 mg daily with food | label |
| **CAD/PAD** | 2.5 mg BID with aspirin | label |
| **Onset** | 180 min | drugs.json |

### Reversal

| Agent | Effect | Source |
|-------|--------|--------|
| **Andexanet alfa** | Reversal agent for anti-Xa inhibition | PMID 29345686 |

### Indications

- Stroke prevention in non-valvular AF
- VTE treatment
- Post hip/knee replacement prophylaxis
- CAD/PAD (with aspirin)

(drugs.json; label)

### Special-Population Safety

| Population | Rating | Source |
|------------|--------|--------|
| **Pregnancy** | Caution; obstetric hemorrhage risk | label |
| **Lactation** | Unknown | label |
| **Hepatic** | No data in severe impairment | label |

---

## Key References

| Source | Supports |
|--------|----------|
| PMID 20139357 | FXa Ki 0.4 nmol/L |
| PMID 23999929; PMID 23458226 | Bioavailability and food requirements; half-life by age |
| PMID 24861792 | Renal excretion 66% (33% unchanged + 33% metabolites) |
| PMID 37207560 | Direct FXa inhibitor mechanism |
| PMID 29345686 | Andexanet alfa reversal |
| label (DailyMed setid 10db92f9-2300-4a80-836b-673e1ae91610) | Vd 50 L; protein binding 92%; ROCKET AF HR 0.88; GI/fatal/ICH bleeding table; dose regimens; monitoring not recommended; pregnancy/lactation/hepatic |
| label_sourcing_e1.json | Verbatim label quotes for GI bleeding, fatal bleeding, ICH, monitoring |
| anticoagulant_adjudication.json | All seven L3 cells |

## Framework Takeaways for Rivaroxaban

1. **Labeled GI signal cuts both ways:** rivaroxaban raises GI bleeding vs warfarin (HR 1.61) while lowering fatal bleeding (HR 0.50) and ICH (HR 0.58). The L3 `gi_bleeding_risk` = 3 captures the first; the latter two live at L4 because no dimension encodes them.
2. **Empty pool, sourced answer:** the GI evidence pool had zero drug-anchored sentences, yet the label quantified the risk. The adjudication override layer exists precisely for this case.
3. **Administration as PK:** the 15/20 mg food requirement (PMID 23999929) is a dose-dependent bioavailability constraint none of the other five drugs has.
4. **Dual-elimination renal dependence:** 66% renal involvement (PMID 24861792) scores 3 alongside drugs eliminated mostly unchanged, because metabolite clearance is still renal.
