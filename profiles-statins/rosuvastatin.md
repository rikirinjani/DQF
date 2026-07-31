# Rosuvastatin — 4-Level Quantitative Profile

> **Role in PoC:** High-potency hydrophilic reference. Most potent HMGCR inhibitor, OATP1B1-dependent hepatic uptake, minimal CYP metabolism. Tests whether the framework captures the potency vs pleiotropy trade-off.

---

## L1 — Molecular Binding

### Primary Target: HMG-CoA Reductase (HMGCR)

| Target | Ki (nM) | Functional Effect |
|--------|---------|-------------------|
| **HMGCR** | **~0.1 nM** (most potent statin) | Competitive reversible inhibition |
| **Additional H-bond interactions** | Unique sulfonyl moiety | Additional polar contacts in active site → ↑ binding affinity |

Rosuvastatin is the **most potent statin** at the molecular level (Ki ~0.1 nM vs atorvastatin ~1.5 nM). The crystal structure shows the unique sulfonyl group (methanesulfonamide moiety) forms additional hydrogen bonds with the HMGCR active site, contributing to the ~15× higher binding affinity. It is **hydrophilic** (logP ~0.5) — the most hydrophilic statin — which directs hepatic uptake via active transport (OATP1B1) rather than passive diffusion.

### Off-Target Pharmacology (L3-relevant)

| Target | Potency | Relevance |
|--------|---------|-----------|
| **OATP1B1** | High-affinity substrate | Hepatic selectivity — the dominant uptake mechanism |
| **OATP1B3** | Substrate | Backup hepatic uptake |
| **BCRP** (ABCG2) | Substrate | Intestinal efflux, biliary secretion |
| **CYP2C9** | Minor substrate | <10% metabolism — minimal DDI |
| **NF-κB** | Inhibition (indirect) | Pleiotropic anti-inflammatory effect |
| **NADPH oxidase** | Downregulation | Antioxidant (class effect but weaker COX-independent) |

### Active Metabolites
- **None** — rosuvastatin is the only statin with no active metabolites
- <10% is metabolized (mostly via CYP2C9)
- ~90% excreted unchanged (renal + biliary)
- This is the **simplest metabolic profile** among all statins

### Key Structural Difference vs Lipophilic Statins
Rosuvastatin's hydrophilicity (methanesulfonamide group) is the structural feature that drives its entire PK/L3/L4 profile:
- Requires active transport for hepatic entry → hepatoselective
- Limited passive diffusion into extrahepatic tissues → lower myopathy risk
- No CYP metabolism → minimal drug interactions
- These features are **L1-determined but propagate to all levels**

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | ~20% (oral) |
| **Volume of distribution** | ~134 L (moderate — limited by hydrophilicity) |
| **Protein binding** | 88% (moderate — lowest among statins) |
| **Half-life (plasma)** | **~19 h** (longest of all statins) |
| **Tmax** | 3–5 h (slow absorption) |
| **Metabolism** | **CYP2C9** (minor, <10%), mostly unchanged |
| **Excretion** | Renal (~90% unchanged), biliary (~10%) |
| **Food effect** | ↓ Cmax ~20%, no significant AUC change |
| **Hepatic selectivity** | **Very high** (OATP1B1-dependent uptake, low passive diffusion) |

**PK Signature:** Rosuvastatin is the outlier. Longest t½ (19 h), no active metabolites, minimal CYP metabolism, and near-complete renal excretion of unchanged drug. The t½ is truly functional — not artefactually prolonged by active metabolites as with atorvastatin. The long t½ allows flexible once-daily or even every-other-day dosing in some regimens.

**Polymorphism impact:** BCRP (ABCG2) c.421C>A (rs2231142) is the major polymorphism affecting rosuvastatin exposure (↑ AUC ~1.6-2×). SLCO1B1 affects rosuvastatin less than atorvastatin. BCRP polymorphism frequency: ~30% in East Asians → explains clinical observation of higher rosuvastatin exposure in Asian populations.

---

## L3 — Systems Response

### LDL Reduction Dynamics

| Dose | Mean LDL Reduction | 95% CI | Notes |
|------|-------------------|--------|-------|
| **5 mg** | ~42% | ±3% | Starting dose (some regions) |
| **10 mg** | ~46% | ±3% | Common starting dose |
| **20 mg** | ~52% | ±3% | Standard dose |
| **40 mg** | ~55% | ±3% | Maximum dose (JUPITER dose) |

Rosuvastatin produces the **greatest LDL reduction per mg** of any statin. The 40 mg dose achieves ~55% LDL reduction — comparable to atorvastatin 80 mg — at half the nominal dose. This potency is traceable to L1 (highest HMGCR affinity) + L2 (longest t½, hepatoselective uptake).

### Pleiotropic Mechanisms (L3-specific)

| Mechanism | Effect | Evidence | Notes |
|-----------|--------|----------|-------|
| **eNOS upregulation** | ↑ NO bioavailability | Strong in vitro data | Class effect |
| **hsCRP reduction** | **~37% reduction** at 20 mg | **JUPITER trial** — the defining pleiotropic evidence | Independent of LDL |
| **Plaque regression** | **Statistically significant regression** | ASTEROID (IVUS), SATURN, ORION | Rosuvastatin 40 mg showed regression in ASTEROID |
| **Antioxidant** | ↓ Lipid peroxidation, ↓ ROS | In vitro, ex vivo | Consistent with class |
| **Anti-inflammatory** | ↓ IL-6, ↓ TNFα, ↓ MCP-1 | Clinical biomarkers | Independent pathway |
| **Thrombosis** | ↓ PAI-1, ↓ Factor VII | Modest effect | Less studied than lipophilic statins |

### The JUPITER Finding (L3→L4 connection)
JUPITER (2008) enrolled individuals with LDL <130 mg/dL but hsCRP ≥2 mg/L — normal lipids + elevated inflammation. Rosuvastatin 20 mg reduced:
- LDL by 50%
- hsCRP by 37%
- **Primary MACE endpoint by 44%** (HR 0.56, p<0.00001)

The benefit magnitude exceeds what LDL reduction alone would predict — the **L3 finding** (anti-inflammatory effect in normolipidemic population) maps directly to the **L4 outcome** (MACE reduction in primary prevention with normal lipids). This is the strongest evidence in the statin class for LDL-independent benefit.

### Tissue Penetration
- **Liver** — very high (OATP1B1-mediated uptake)
- **Vascular wall** — limited passive diffusion (hydrophilic)
- **Muscle** — minimal passive diffusion → lower myopathy risk
- **CNS** — negligible (hydrophilic + BCRP efflux)

### RAG Evidence
Expected data:
- JUPITER trial primary results (NEJM 2008) — L3→L4 anti-inflammatory signal
- ASTEROID trial — plaque regression by IVUS
- JUPITER subgroup analyses (elderly, diabetes, metabolic syndrome)

---

## L4 — Clinical Outcomes

### MACE Reduction (per 1 mmol/L LDL reduction)

| Outcome | Relative Risk Reduction | Absolute Risk Reduction | NNT (5 years, JUPITER population) |
|---------|------------------------|------------------------|-----------------------------------|
| **Major CV events** | ~22% per mmol/L (consistent with CTT) | ~1.6% | ~63 |
| **MI** | ~54% (JUPITER primary) | ~0.5% | ~200 |
| **Stroke** | ~48% (JUPITER) | ~0.3% | ~333 |
| **Revascularization** | ~46% (JUPITER) | ~0.6% | ~167 |
| **All-cause mortality** | ~20% (JUPITER, p=0.02) | ~0.3% | ~333 |

*Note: The JUPITER RRR values appear larger than CTT meta-analysis averages because the JUPITER population had lower baseline LDL but elevated CRP. The per-mmol-LDL reduction is consistent with CTT.*

### Landmark Trials

| Trial | Population | Dose | Key Outcome | Absolute Risk Reduction |
|-------|-----------|------|-------------|------------------------|
| **JUPITER** | Primary prevention, LDL<130, CRP≥2 (n=17,802) | 20 mg vs placebo | ↓ MACE 44% (HR 0.56) | 1.2% over 1.9 y |
| **ASTEROID** | CAD, aggressive target (n=507) | 40 mg | **Plaque regression** by IVUS | — |
| **METEOR** | Low-risk, subclinical atherosclerosis (n=984) | 40 mg | ↓ CIMT progression | Early atherosclerosis |
| **CORONA** | Systolic HF (n=5,011) | 10 mg vs placebo | ↓ CV hospitalizations 8%, no mortality benefit | — |
| **HOPE-3** | Intermediate risk (n=12,705) | 10 mg vs placebo | ↓ CV events 24% | 0.7% |

### Safety Profile

| Adverse Event | Risk | Notes |
|---------------|------|-------|
| **Myopathy** | **Lower than lipophilic statins** | Hydrophilicity limits muscle penetration |
| **Rhabdomyolysis** | <0.02% | Very rare; BCRP polymorphism increases risk |
| **Proteinuria (dipstick)** | Up to 12% at 40 mg | Transient tubular proteinuria — not renal injury |
| **New-onset diabetes** | ~9% relative risk per mmol/L | Consistent with class effect (dose-dependent) |
| **Drug interactions** | **Minimal** | No CYP3A4; CYP2C9 interactions rare (<10% metabolism) |
| **Renal impairment** | ↑ exposure (90% renal excretion) | Dose adjustment needed for eGFR <30 |

### Condition Spectrum
- **Primary prevention (normal lipids, elevated CRP)** — JUPITER: unique population, landmark trial
- **Stable CAD** — ASTEROID (plaque regression), SATURN (comparison vs atorvastatin)
- **Intermediate-risk primary prevention** — HOPE-3
- **Heart failure** — CORONA (neutral for mortality, reduced hospitalizations)
- **Subclinical atherosclerosis** — METEOR (CIMT progression slowed)

### RAG Evidence
Expected retrieval:
- JUPITER trial primary (NEJM 2008) + meta-analyses
- ASTEROID plaque regression (JAMA 2006)
- HOPE-3 primary prevention (NEJM 2016)
- BCRP polymorphism and rosuvastatin exposure

---

## Key References (with PMIDs)

| PMID | Title | Evidence Level |
|------|-------|----------------|
| 18997196 | JUPITER: Rosuvastatin in Primary Prevention (NEJM 2008) | HIGH (RCT, n=17,802) |
| 17008640 | ASTEROID: Plaque Regression with Rosuvastatin (JAMA 2006) | MODERATE (IVUS, n=507) |
| 21757642 | METEOR: CIMT with Rosuvastatin (J Am Coll Cardiol) | MODERATE (imaging) |
| 17984165 | CORONA: Rosuvastatin in Heart Failure (NEJM 2007) | HIGH (RCT, n=5,011) |
| 27275479 | HOPE-3: Rosuvastatin in Intermediate Risk (NEJM 2016) | HIGH (RCT, n=12,705) |
| CTT 2010 | Efficacy of More Intensive LDL-C Lowering (Lancet) | HIGH (meta-analysis) |
| CTT 2012 | Effects by Baseline LDL (Lancet) | HIGH (meta-analysis) |
| 26286635 | ASTEROID 5-Year Follow-up | MODERATE (observational) |

## Framework Takeaways for Rosuvastatin

1. **Potency at L1 does not linearly predict L4 outcome:** Rosuvastatin has 15× higher HMGCR affinity than atorvastatin (Ki 0.1 vs 1.5 nM) but similar per-mmol LDL reduction. However, its longer t½ and hepatoselectivity mean lower mg doses achieve comparable effect — a L1→L2→L4 chain.

2. **The JUPITER trial is a three-level story:**
   - L3 (anti-inflammatory pleiotropic mechanism in normal-lipid, high-CRP population)
   - L4 (44% MACE reduction exceeds LDL-only prediction)
   - The framework makes this causal chain explicit

3. **Hydrophilicity (L1 structural feature) propagates across all levels:**
   - L2: OATP1B1-dependent uptake, long t½, renal excretion
   - L3: Hepatoselectivity → minimal pleiotropy in extrahepatic tissues
   - L4: Lower myopathy risk, minimal drug interactions

4. **Cross-class parallel:** Rosuvastatin vs celecoxib. Both are the "target-selective" member of their class (rosuvastatin = hepatoselective, celecoxib = COX-2 selective). Both achieve their selectivity through structural features that reduce off-target effects at the cost of lost pleiotropy. Both demonstrate the framework's ability to handle selectivity ratios.
