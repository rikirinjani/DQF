# Pravastatin — 4-Level Quantitative Profile

> **Role in PoC:** Hydrophilic, non-CYP, natural origin. Non-prodrug, renally cleared, sulfation metabolism (CYP-independent). Tests whether the framework captures the "simplest pharmacokinetic profile" dimension — the class baseline for safety comparisons.

---

## L1 — Molecular Binding

### Primary Target: HMG-CoA Reductase (HMGCR)

| Target | Ki (nM) | Functional Effect |
|--------|---------|-------------------|
| **HMGCR** | ~1.5 nM | Competitive, reversible inhibition |
| **Additional OH group** (6'-OH) | Structural feature | Contributes to hydrophilicity |

Pravastatin is a **hydrophilic statin** derived from natural fungal metabolites (from *Penicillium citrinum* — the original statin discovery pathway). Unlike simvastatin (derived from lovastatin), pravastatin is administered as the **active hydroxy acid** — not a prodrug. It is the most polar (hydrophilic) statin along with rosuvastatin.

The 6'-OH group makes pravastatin more hydrophilic than the other natural statins. This structural feature is the L1 determinant of its entire safety profile: limited passive diffusion, no CYP metabolism, and active renal excretion.

### Off-Target Pharmacology (L3-relevant)

| Target | Potency | Relevance |
|--------|---------|-----------|
| **OATP1B1** | Substrate | Hepatic uptake (dominates distribution) |
| **OATP1B3** | Substrate | Mild backup |
| **BCRP** | Substrate | Intestinal efflux, biliary |
| **MRP2** | Substrate | Biliary excretion |
| **Sulfation (SULT)** | **Primary clearance** | Unique — cytosolic sulfotransferase, not CYP |
| **CYP3A4** | **No significant metabolism** | Unique — no CYP involvement |
| **Antioxidant (direct radical scavenging)** | Moderate | May contribute to vascular effects |

### Active Metabolites
- **3α-Isopravastatin** — minor, weakly active
- **Pravastatin is not a prodrug** — administered as active form
- Unlike simvastatin (lactone prodrug), no hydrolysis step required
- No clinically significant metabolites

### Unique L1 Feature: Sulfation Clearance
Pravastatin is cleared by **sulfation** (SULT2A1, SULT1E1) — a conjugation pathway completely independent of CYP450. This is unique among all drugs, not just statins. The sulfation pathway has:
- No genetic variants relevant to drug exposure
- No clinically significant drug interactions at this enzyme
- No substrate overlap with CYP3A4/CYP2C9 inhibitors

This L1 structural feature (hydroxyl group amenable to sulfation) propagates to L2 (no CYP DDI) and L4 (safest DDI profile).

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | ~18% (oral) |
| **Volume of distribution** | ~35 L (low — confined to plasma, hydrophilic) |
| **Protein binding** | **~50%** (lowest among all statins) |
| **Half-life (plasma)** | **~1.5–2 h** (shortest among statins) |
| **Tmax** | 1–1.5 h |
| **Metabolism** | **Sulfation** (SULT) — no CYP involvement |
| **Excretion** | **Renal (~60%)**, biliary (~40%) |
| **Food effect** | ↓ Cmax ~30%, no significant AUC change |
| **Hepatic selectivity** | **Very high** (OATP1B1-dependent, minimal passive diffusion) |

**PK Signature:** Pravastatin has the **shortest half-life** (1.5-2 h) — but this does not correlate with inferior LDL outcomes because hepatic residence time matters more than plasma t½. The lowest protein binding (50% vs 95-99% for other statins) and low Vd (confined to plasma space) reflect its hydrophilicity.

**Zero CYP interaction:** No known clinically significant CYP3A4, CYP2C9, or CYP2C8 interaction. This is the defining PK advantage. Pravastatin is the **safest statin in polypharmacy** — the one recommended when DDI is a concern.

### Polymorphism Impact
- **SLCO1B1** affects pravastatin (↓ OATP1B1 → ↑ plasma exposure) but less than atorvastatin
- No clinically actionable polymorphism requiring dose adjustment
- Renal impairment → ↑ exposure (proportional to eGFR decline)

---

## L3 — Systems Response

### LDL Reduction Dynamics

| Dose | Mean LDL Reduction | 95% CI | Notes |
|------|-------------------|--------|-------|
| **10 mg** | ~20% | ±3% | Starting dose |
| **20 mg** | ~24% | ±3% | Standard dose |
| **40 mg** | ~30% | ±3% | Maximum dose |
| **80 mg** | ~34% | ±3% | Less commonly used |

Pravastatin is the **least potent LDL-lowering statin** — maximum 30-34% reduction vs 55% for atorvastatin 80 mg. However, this does not mean 50% less MACE reduction — CTT per-mmol-LDL relationships are consistent regardless of statin.

### Pleiotropic Mechanisms (L3-specific)

| Mechanism | Effect | Evidence Level | Notes |
|-----------|--------|----------------|-------|
| **eNOS upregulation** | ↑ NO | Weak-moderate | Weaker than lipophilic statins |
| **hsCRP reduction** | ~15-20% | Modest | Lower than atorvastatin/rosuvastatin |
| **Antioxidant (direct)** | Free radical scavenging | Unique among statins | May compensate for weaker eNOS |
| **Plaque stabilization** | ↓ MMP, ↑ collagen (IVUS) | Weak | Less IVUS data than lipophilic statins |
| **Anti-inflammatory** | ↓ IL-6 | Modest | Weaker than atorvastatin |
| **Immunomodulation** | Minimal | Evidence poor | Low passive diffusion limits extrahepatic effect |

### The Hydrophilicity Trade-off (L3)
Pravastatin's hydrophilic nature is a **double-edged sword** captured by the framework:
- **Advantage:** Minimal extrahepatic effects → lower myopathy risk, minimal DDI
- **Disadvantage:** Fewer pleiotropic effects (weaker eNOS, anti-inflammatory) → less LDL-independent benefit
- The net effect: pravastatin reduces MACE proportionally to LDL reduction, with less additional benefit

### Tissue Penetration
- **Liver** — high (OATP1B1-mediated uptake — the only route since passive diffusion is minimal)
- **Muscle** — minimal (hydrophilic, no passive diffusion)
- **Vascular wall** — limited
- **CNS** — negligible
- **Breast milk** — detectable (minimal risk data)

### RAG Evidence
Expected retrieval:
- CARE, LIPID, WOSCOPS — landmark pravastatin trials
- PROVE-IT — pravastatin vs atorvastatin
- PLAC-I — pravastatin and atherosclerosis progression
- REGRESS — pravastatin regression in CAD

---

## L4 — Clinical Outcomes

### MACE Reduction (per 1 mmol/L LDL reduction)

| Outcome | Relative Risk Reduction | Notes |
|---------|------------------------|-------|
| **Major coronary events** | ~22% per mmol/L (CTT consistent) | Confirmed across 3 landmark RCTs |
| **Total mortality** | ~22% per mmol/L (CTT) | CARE, LIPID individual results consistent |
| **Coronary revascularization** | ~23% per mmol/L | CTT consistent |

Pravastatin's MACE reduction is **indistinguishable from atorvastatin per unit LDL reduction** — despite weaker pleiotropic effects. This supports the LDL-centric model: pleiotropy adds little to per-mmol-LDL benefit.

### Landmark Trials

| Trial | Population | Dose | Key Outcome | Absolute Risk Reduction |
|-------|-----------|------|-------------|------------------------|
| **WOSCOPS** (1995) | Primary prevention, hypercholesterolemia (n=6,595) | 40 mg vs placebo | ↓ non-fatal MI + CHD death 31% | 2.4% (5 y) |
| **CARE** (1996) | Post-MI, "normal" LDL (n=4,159) | 40 mg vs placebo | ↓ fatal CHD + non-fatal MI 24% | 2.9% (5 y) |
| **LIPID** (1998) | Unstable angina + prior MI (n=9,014) | 40 mg vs placebo | ↓ CHD mortality **24%**, total mortality **22%** | 3.1% (6 y) |
| **PROVE-IT** (2004) | ACS, intensive vs moderate (n=4,162) | 40 mg vs atorvastatin 80 mg | Atorvastatin superior (16% RRR) | Moderate-intensity vs intensive |

### The WOSCOPS Legacy
WOSCOPS was the **first primary prevention statin trial** to show benefit in men with elevated cholesterol but no prior CVD. It established that primary prevention with statins reduces events. This is analogous to 4S (secondary prevention landmark) but in the primary prevention space.

### The PROVE-IT Comparison (Pravastatin vs Atorvastatin)
The direct comparison (PROVE-IT TIMI 22) showed atorvastatin 80 mg is superior to pravastatin 40 mg in ACS — but the difference is fully explained by the difference in achieved LDL (62 vs 95 mg/dL). This is the **framework's best evidence** that per-mmol-LDL relationships are drug-independent within the statin class, supporting the LDL-centric model.

### Safety Profile

| Adverse Event | Risk | Notes |
|---------------|------|-------|
| **Myopathy** | **Lowest among all statins** | 0.02-0.05% — hydrophilic, no passive muscle diffusion |
| **Rhabdomyolysis** | <0.01% | Extremely rare |
| **Transaminase elevation** | <0.5% | Lowest among statins |
| **New-onset diabetes** | ~7% relative risk | Consistent with class (slightly lower estimates) |
| **Drug interactions** | **None clinically significant** | No CYP metabolism — safest in polypharmacy |
| **Renal** | Safe with dose adjustment | Renally cleared |

### The Safest Statin
Pravastatin is widely considered the **safest statin** based on:
- Lowest myopathy risk (no muscle diffusion)
- No CYP interactions
- Shortest half-life (rapid clearance if toxicity)
- Lowest protein binding (50%) → rapid dialysis clearance

### Condition Spectrum
- **Primary prevention (men, hypercholesterolemia)** — WOSCOPS
- **Post-MI, normal LDL** — CARE (established benefit even with "normal" cholesterol)
- **Stable CHD, broad range** — LIPID (largest pravastatin trial)
- **Unstable angina** — LIPID subgroup
- **ACS (as moderate-intensity comparator)** — PROVE-IT

### RAG Evidence
Expected retrieval:
- WOSCOPS — primary prevention
- CARE — post-MI with normal LDL
- LIPID — broad CHD population
- PROVE-IT — direct atorvastatin comparison
- PLAC-I, REGRESS — atherosclerosis imaging

---

## Key References (with PMIDs)

| PMID | Title | Evidence Level |
|------|-------|----------------|
| 7675295 | **WOSCOPS**: Pravastatin in Primary Prevention (NEJM, 1995) | **HIGH** (landmark RCT, n=6,595) |
| 8591860 | **CARE**: Pravastatin Post-MI with Normal LDL (NEJM, 1996) | **HIGH** (landmark RCT, n=4,159) |
| 9768350 | **LIPID**: Pravastatin in CHD Population (NEJM, 1998) | **HIGH** (landmark RCT, n=9,014) |
| 15047687 | **PROVE-IT**: Pravastatin vs Atorvastatin in ACS (NEJM, 2004) | HIGH (RCT, n=4,162) |
| CTT 2010 | Efficacy of Intensive LDL-C Lowering (Lancet) | HIGH (meta-analysis) |
| CTT 2012 | Effects by Baseline LDL (Lancet) | HIGH (meta-analysis) |
| 7804365 | PLAC-I: Pravastatin & Atherosclerosis (Am J Cardiol, 1995) | MODERATE (IVUS) |
| 9034419 | REGRESS: Pravastatin in CAD (Circulation, 1996) | MODERATE (IVUS) |

## Framework Takeaways for Pravastatin

1. **Strongest evidence for the LDL-centric model:** Pravastatin produces per-mmol MACE reduction identical to more pleiotropic statins, supporting the framework's L4-level finding that pleiotropic effects contribute little beyond LDL reduction.

2. **Safest DDI profile is an L1→L2→L4 chain:**
   - L1: Hydroxy group → sulfation pathway (no CYP)
   - L2: SULT metabolism, renal excretion, no CYP interaction
   - L4: Safest choice in polypharmacy (transplant, HIV, elderly)

3. **Shortest t½ ≠ least effective:** Plasma t½ of 1.5-2 h yet once-daily dosing achieves equivalent per-mmol-LDL MACE reduction. L3 hepatic residence time is the relevant PK parameter, not plasma t½. This is exactly the kind of PK-L4 disconnect the framework is designed to capture.

4. **The PROVE-IT comparison (pravastatin vs atorvastatin) is the class's strongest internal comparator** — controlling for drug identity shows LDL reduction alone explains outcome difference. This supports the framework's claim that single-score drug comparators add no information beyond LDL reduction for statins.

5. **Cross-class parallel:** Pravastatin ↔ ibuprofen. Both are the "safest, most-studied" reference of their class. Pravastatin is the oldest statin with the longest safety record; ibuprofen is the reference NSAID. Both have the lowest risk profile within their class.
