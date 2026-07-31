# Statin PoC — Cross-Comparison Table (5 Drugs)

> **Role in PoC:** Tests whether the framework's 4-level design captures meaningful drug-to-drug distinctions within the statin class — or whether statins are functionally interchangeable. Also evaluates whether cross-class generalizability holds (framework designed for NSAIDs works for statins).

---

## L1 — Molecular Binding Comparison

| Property | Atorvastatin | Rosuvastatin | Simvastatin | Pravastatin | Pitavastatin |
|----------|-------------|--------------|-------------|-------------|--------------|
| **HMGCR Ki (nM)** | ~1.5 | **~0.1** | ~0.2 (active acid) | ~1.5 | ~0.5 |
| **Active form** | Acid (direct) | Acid (direct) | Lactone → acid (prodrug) | Acid (direct) | Acid (direct) |
| **Active metabolites** | **Yes** (ortho/para-OH) | None | Minor (6'-OH) | Minor (weak) | None |
| **Lipophilicity** | Lipophilic (logP ~6) | **Hydrophilic** (logP ~0.5) | Lipophilic (logP ~4.7) | **Hydrophilic** | **Intermediate** |
| **Key structural feature** | Fluorophenyl (synthetic) | **Methanesulfonamide** | **Lactone ring** (prodrug) | 6'-OH (natural origin) | **Cyclopropyl** (quinolone) |
| **Unique off-target** | OATP1B1 (substrate) | BCRP (substrate) | CYP3A4 (high affinity) | **Sulfation** (not CYP) | **UGT** (not CYP) |

### Key Differentiation
1. **Most potent:** Rosuvastatin (Ki 0.1 nM) > pitavastatin (0.5) > simvastatin acid (0.2) > atorvastatin ≈ pravastatin (1.5)
2. **Prodrug status:** Only simvastatin is a prodrug — requires in vivo hydrolysis
3. **Active metabolites:** Only atorvastatin has clinically significant active metabolites (equipotent, prolong effect)
4. **Metabolic pathway uniqueness:** Pravastatin (sulfation) and pitavastatin (glucuronidation) are CYP-independent; simvastatin and atorvastatin (CYP3A4-dependent)

---

## L2 — Pharmacokinetic Comparison

| Parameter | Atorvastatin | Rosuvastatin | Simvastatin | Pravastatin | Pitavastatin |
|-----------|-------------|--------------|-------------|-------------|--------------|
| **Bioavailability** | 12-14% | ~20% | **<5%** | ~18% | **~60%** |
| **Vd (L)** | ~380 | ~134 | Very large | ~35 | ~200 |
| **Protein binding** | 98% | 88% | 95-98% | **~50%** | **~99%** |
| **Half-life (plasma)** | ~14 h | **~19 h** | ~2-3 h | ~1.5-2 h | ~12 h |
| **Functional t½** | **20-30 h** (metabolites) | ~19 h | ~2-3 h | ~1.5-2 h | ~12 h |
| **Tmax** | 1-2 h | 3-5 h | 1.5-2.5 h | 1-1.5 h | **~1 h** |
| **Major metabolism** | **CYP3A4** | CYP2C9 (minor) | **CYP3A4** | **Sulfation** | **Glucuronidation** |
| **Renal excretion** | <2% | **~90%** | ~13% | **~60%** | <5% |
| **Key polymorphism** | **SLCO1B1** (↑ exposure 2-3×) | **BCRP** (↑ 1.6-2×) | SLCO1B1 | SLCO1B1 (modest) | — |
| **Hepatic selectivity** | Moderate (passive + active) | **Very high** (OATP only) | Moderate | **Very high** (OATP only) | High (OATP + passive) |

### Key Differentiation
1. **Longest functional t½:** Atorvastatin (20-30 h via metabolites) > rosuvastatin (19 h) > pitavastatin (12 h) > simvastatin ≈ pravastatin (2 h)
2. **Highest bioavailability:** Pitavastatin (60%) — others 5-20%
3. **Most CYP-dependent:** Simvastatin and atorvastatin (CYP3A4 → high DDI)
4. **Least CYP-dependent:** Pravastatin (sulfation), pitavastatin (UGT), rosuvastatin (≤10% CYP)
5. **Lowest protein binding:** Pravastatin (50%) — may matter in hypoalbuminemia

---

## L3 — Systems Response Comparison

| Property | Atorvastatin | Rosuvastatin | Simvastatin | Pravastatin | Pitavastatin |
|----------|-------------|--------------|-------------|-------------|--------------|
| **Max LDL reduction** | ~55% (80 mg) | **~55% (40 mg)** | ~42% (80 mg⁺) | ~34% (80 mg) | ~44% (4 mg) |
| **Dose-response rule** | ~6% per doubling | ~7% per doubling | ~6% per doubling | ~4% per doubling | ~6% per doubling |
| **Pleiotropic strength** | **Strong** | **Strong** | Moderate | **Weak** | Moderate |
| **eNOS upregulation** | Well-documented | Well-documented | Moderate | Weak | Moderate |
| **hsCRP reduction** | ~37% (80 mg) | **~37% (20 mg)** | ~20-30% | ~15-20% | ~30-35% |
| **Plaque regression** | Yes (REVERSAL, SATURN) | **Yes (ASTEROID)** | Limited IVUS data | Limited IVUS data | Yes (Japan-ACS) |
| **Myopathy risk (mechanism)** | Passive diffusion + SLCO1B1 | **Minimal** (hydrophilic) | Passive diffusion + lactone | **Minimal** (hydrophilic) | Moderate |
| **Extrahepatic distribution** | High | **Very low** | High | **Very low** | Moderate |

### Key Differentiation
1. **Pleiotropic gradient:** Atorvastatin ≈ rosuvastatin > pitavastatin > simvastatin > pravastatin
2. **LDL-per-mg efficiency:** Rosuvastatin >> pitavastatin > atorvastatin > simvastatin > pravastatin
3. **Plaque regression evidence strongest for:** Rosuvastatin (ASTEROID) and atorvastatin (SATURN)
4. **Hydrophilicity pleiotropy trade-off:** Pravastatin and rosuvastatin have minimal extrahepatic effects, which reduces both pleiotropic benefits AND myopathy risk

---

## L4 — Clinical Outcomes Comparison

| Property | Atorvastatin | Rosuvastatin | Simvastatin | Pravastatin | Pitavastatin |
|----------|-------------|--------------|-------------|-------------|--------------|
| **MACE/1 mmol LDL** | ~22% RRR | ~22% RRR | ~22% RRR | ~22% RRR | ~22% RRR (assumed) |
| **Landmark trial(s)** | TNT, CARDS, ASCOT-LLA, PROVE-IT | **JUPITER** | **4S** (first mortality) | WOSCOPS, CARE, LIPID | LIVES (observational) |
| **Total mortality benefit** | Yes (meta-analysis) | Yes (JUPITER) | **Yes (4S)** | Yes (CARE, LIPID) | Not established |
| **Primary prevention** | Yes (ASCOT-LLA, CARDS) | **Yes (JUPITER)** | Limited alone | **Yes (WOSCOPS)** | Limited data |
| **ACS benefit** | **Yes (PROVE-IT)** | Limited data | Limited data | Moderate (weak) | Limited data |
| **Plaque regression (IVUS)** | Yes | **Yes** | No RCT data | No RCT data | Yes (Japan-ACS) |
| **Myopathy risk (clinical)** | 0.5-1% (real-world) | **~0.1%** | 0.02-0.05% (std) | **~0.02%** | ~0.3% |
| **DDI risk** | **High** (CYP3A4) | Low (CYP2C9 minor) | **Very high** (CYP3A4) | **None** | **None** |
| **New-onset diabetes** | Moderate | Moderate | Moderate | Low | **Lowest** |
| **Renal dose adjustment** | No | **Yes** (90% renal) | No | **Yes** (60% renal) | No |

### Key Differentiation
1. **MACE reduction per LDL:** Virtually identical across all five statins (~22% per 1 mmol/L) — the CTT meta-analysis finding
2. **Landmark trial differences reflect era/timing, not drug superiority:** 4S (simvastatin, first mortality), WOSCOPS (pravastatin, first primary prevention), JUPITER (rosuvastatin, first CRP-based), TNT (atorvastatin, first high-vs-standard)
3. **Safety gradient:** Pravastatin (safest) > rosuvastatin ≈ pitavastatin > atorvastatin > simvastatin (most DDI/myopathy)
4. **PROVE-IT comparison** showed atorvastatin 80 mg > pravastatin 40 mg — but this is entirely explained by achieved LDL (62 vs 95 mg/dL)

---

## Framework-Specific Findings (Statin Class)

### Cross-Class Generalizability Verified (from NSAID PoC)
The following framework features transfer cleanly to the statin class:

| Framework Feature | NSAID Example | Statin Example | Generalizable? |
|------------------|--------------|----------------|----------------|
| **L1 selectivity ratio** | COX-2/COX-1 (celecoxib) | HMGCR Ki range (0.1-1.5 nM) | **Yes** — potency gradient captured |
| **L2 PK polymorphism** | CYP2C9 (celecoxib) | SLCO1B1 (atorvastatin), BCRP (rosuvastatin) | **Yes** — stronger statin evidence |
| **L3 pleiotropy** | ASIC1a (ibuprofen) | eNOS/CRP (all statins, varying strength) | **Yes** — but attenuated (statin pleiotropy is class effect, not drug-specific) |
| **L3 mechanistic paradox** | Coxib paradox (GI good, CV bad) | **Hydrophilicity trade-off** (low myopathy, low pleiotropy) | **Yes** — different mechanism, same framework structure |
| **L4 clinical trial age** | CLASS (celecoxib, 2000) | 4S (simvastatin, 1994) vs JUPITER (rosuvastatin, 2008) | **Yes** — trial era and intensity matter |
| **Prodrug status** | — | Simvastatin (lactone) | **Yes** — framework captures active species distinction |
| **Active metabolites** | — | Atorvastatin (ortho/para-OH) | **Yes** — metabolites prolong effect |

### New Framework Features Revealed by Statins (Not Present in NSAIDs)

| New Feature | Description | Statin Example | Framework Handling |
|-------------|-------------|----------------|-------------------|
| **Class-level per-unit outcome** | ~22% RRR per 1 mmol/L LDL reduction is identical across drugs | All 5 statins | L4 consistency check — framework shows class vs drug-specific signal separation |
| **Era-dependent landmark trials** | 4S (1994) vs JUPITER (2008) — different standards of care | Simvastatin vs rosuvastatin | L4 requires trial context; framework needs trial-year annotation |
| **Dose-dependent drug identity** | Atorvastatin 10 mg ≠ 80 mg (TNT showed 22% RRR between them) | Atorvastatin | Framework handles dose as parameter — NSAIDs had narrower therapeutic ranges |
| **Metabolic pathway as DDI predictor** | CYP3A4 vs non-CYP predicts interaction burden | Simvastatin vs pravastatin | L1→L2→L4 chain well-captured |
| **Active metabolite prolongation** | Functional t½ ≠ plasma t½ | Atorvastatin (parent 14 h, functional 20-30 h) | L2 parent t½ is misleading without L1 metabolite context |
| **Lipophilicity continuum** | logP range 0.5 (rosuvastatin) to 6 (atorvastatin) | All 5 statins span the gradient | L1 lipophilicity → L2 (Vd, CYP metabolism) → L3 (tissue penetration) → L4 (myopathy, DDI) |

### Framework Limitations Observed

| Limitation | Description | Impact |
|-----------|-------------|--------|
| **Per-mmol-LDL RRR is constant** | Framework works hard to differentiate statins, but L4 outcome is near-identical when normalized for LDL reduction | Weakens framework's argument that drug-specific scoring adds value for statins |
| **Pleiotropy appears to contribute little to L4 outcomes** | Pravastatin produces same per-mmol-LDL MACE reduction as more pleiotropic statins | Suggests statin pleiotropy may be a L3 theoretical feature without L4 consequence |
| **Trial-era confounding** | Simvastatin 4S (1994) vs rosuvastatin JUPITER (2008) — different background therapy | L4 comparisons must be era-adjusted |
| **Dose dependency is underdeveloped** | Atorvastatin 10 mg vs 80 mg is a bigger difference than atorvastatin 10 mg vs pravastatin 40 mg | Framework needs a "dose-response dimension" within each profile |

---

## Summary: Framework Value for Statins vs NSAIDs

| Dimension | NSAID Class | Statin Class | Verdict |
|-----------|-------------|--------------|---------|
| **Drug differentiation** | **High** (COX selectivity, off-target, PK, safety) | **Low-moderate** (per-mmol-LDL outcome is constant) | Framework adds more value for NSAIDs |
| **Safety signal diversity** | **High** (GI vs CV trade-off) | **Low** (myopathy risk gradient, but all are safe) | Framework differentiates safety better for NSAIDs |
| **DDI profile** | Moderate | **Strong** (CYP-dependent vs independent) | Framework handles well for both |
| **PK-polymorphism link** | Moderate (CYP2C9 for celecoxib) | **Strong** (SLCO1B1, BCRP) | Statins provide better pharmacogenomic evidence |
| **Pleiotropy authenticity** | **Strong** (ASIC1a for ibuprofen is drug-specific) | Weak (most pleiotropy is class effect) | Framework's L3 is more valuable for NSAIDs |
| **Framework generalizability** | — | — | **Confirmed** — framework works for both classes, but differentiation power varies |

### Bottom Line
The 4-level framework **generalizes to the statin class** — all four levels produce meaningful data for each drug. However, the framework's **differentiation power is lower for statins** than NSAIDs because:
1. The per-mmol-LDL outcome is class-constant (unlike NSAID NNT range: 2.1-3.6)
2. Statin pleiotropy is primarily a class effect, not drug-specific
3. Safety profiles differ in degree (myopathy 0.02-1%) but not qualitatively (no GI vs CV trade-off)

This is **not a framework failure** — it's an honest finding that aligns with clinical reality: cardiologists treat statins as largely interchangeable, while rheumatologists distinguish NSAIDs carefully. The framework faithfully reflects this difference.

### Cross-Class Parallels (NSAID ↔ Statin)

| NSAID | Statin Counterpart | Parallel |
|-------|-------------------|----------|
| **Ibuprofen** | **Pravastatin** | Safest, most-studied reference — baseline comparator |
| **Diclofenac** | **Atorvastatin** | Market-dominant, moderate safety, well-studied |
| **Celecoxib** | **Rosuvastatin** | Target-selective, best-tolerated, best evidence of differentiated benefit |
| **Paracetamol** | **Pitavastatin** | Fewest interactions, metabolic uniqueness, modest efficacy |
| *(gap)* | **Simvastatin** *(no NSAID counterpart)* | Prodrug — historical landmark but clinically surpassed |
