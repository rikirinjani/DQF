# Celecoxib — 4-Level Quantitative Profile

> **Role in PoC:** Selectivity dimension. COX-2 selective, distinct PK/safety profile, different metabolic pathway. Tests whether the framework can capture selectivity ratios meaningfully.

---

## L1 — Molecular Binding

### Primary Target: COX-2 (selective)

| Target | Ki (nM) | Functional Effect |
|--------|---------|-------------------|
| **COX-2** | ~5 nM | Potent anti-inflammatory |
| **COX-1** | ~500 nM | Weak inhibition — clinically insignificant at therapeutic doses |
| **COX-2 selectivity ratio** | **~30:1** | The defining feature |

Celecoxib is a **COX-2-selective inhibitor** (the first marketed coxib). The sulfonamide pharmacophore fits into the COX-2 side pocket (Val523 vs Ile523 in COX-1, creating additional space). At therapeutic doses, it inhibits COX-2 but sparing COX-1, resulting in preserved GI mucosal protection and platelet function.

### Off-Target Pharmacology

| Target | Potency | Relevance | Source |
|--------|---------|-----------|--------|
| **Carbonic anhydrase** (sulfonamide class effect) | Weak | Distinguish from other coxibs | — |
| **NF-κB** | Modulation | May contribute to anti-tumor effects | PMID:41383482 |
| **P-glycoprotein** | Substrate | Transport implications | — |
| **Akt/mTOR pathway** | Downstream inhibition | Oncology applications | PMID:41383482 |

**Key finding from RAG:** "Celecoxib in oncology: targeting the COX-2/PGE2 pathway" (PMID:41383482, Front Pharmacol 2025) — celecoxib shows anti-proliferative and anti-metastatic effects beyond COX-2 inhibition, including effects on intratumoral inflammation and immune modulation.

### Active Metabolites
- **Hydroxycelecoxib** — inactive (no COX activity)
- **Carboxycelecoxib** — inactive
- No active metabolites — purified pharmacophore

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | ~80% (oral) |
| **pKa** | 11.1 (weakly acidic) |
| **Volume of distribution** | 5–6 L/kg (**high** — extensive tissue distribution) |
| **Protein binding** | 97% (albumin) |
| **Half-life (plasma)** | **8–12 h** (longest in PoC set) |
| **Tmax** | 2-4 h (slower absorption) |
| **Metabolism** | **CYP2C9** (major) — **no conjugation pathway** |
| **Excretion** | Renal (metabolites), some biliary |
| **CYP2C9 polymorphism** | **Clinically significant** — poor metabolizers have ↑ exposure |

**PK Signature:** Completely different from ibuprofen/diclofenac. High Vd (tissue distribution), long t½ (once-daily), CYP2C9-only metabolism (no conjugation). The absence of a conjugation pathway is unusual among NSAIDs and creates a narrow metabolic dependency on CYP2C9.

**Polymorphism impact:** CYP2C9*2 and *3 variants reduce clearance 30-50%. Clinical consequence: higher risk of GI bleeding in poor metabolizers at standard doses. This is captured by L2 but invisible at L1 or L4 without population stratification.

---

## L3 — Systems Response

### COX-2 Selectivity Dynamics

| Compartment | COX-1 Sparing | Implications |
|-------------|---------------|--------------|
| **GI mucosa** | **Yes** | Preserved PGE2 → less ulceration |
| **Platelets** | **Yes** | No effect on thromboxane A2 → normal platelet aggregation |
| **Endothelium PGI2** | **Inhibited** | Suppresses vasoprotective prostacyclin → pro-thrombotic |
| **Kidney** | **Partially sparing** | Renal PGE2 still affected → potential fluid retention |

### The Coxib Paradox (L3 explains this)
COX-2 selectivity **reduces GI toxicity** (spares COX-1) but **increases CV risk** (inhibits endothelial PGI2 without affecting platelet thromboxane). This creates an imbalance:
- Healthy endothelium: PGI2 ↓ (pro-thrombotic)
- Platelets: thromboxane A2 unaffected (normal aggregation)
- Net effect: pro-thrombotic state

This is the fundamental L3 insight that no single L4 NNT/NNH score captures.

### Tissue Penetration
- **Synovial fluid:** excellent penetration (consistent with high Vd)
- **CNS:** limited (P-glycoprotein substrate)
- **Tumor tissue:** accumulates (oncology application)

### RAG Evidence
RAG query for `"celecoxib COX-2 selective cardiovascular safety"` retrieved:
- **PMID:39660078** — SCOT trial vascular/renal biomarkers in celecoxib vs traditional NSAID users (Eur Heart J Open, 2024)
- **PMID:41560736** — Imrecoxib vs celecoxib meta-analysis (Front Pharmacol 2025)
- **PMID:40028763** — Korean AS cohort: comparable CV/GI risk between celecoxib and nsNSAIDs (2025)
- **PMID:41383482** — Celecoxib in oncology — beyond COX-2 (Front Pharmacol 2025)

---

## L4 — Clinical Outcomes

### Acute Pain (≥50% pain relief over 4-6 h vs placebo)

| Dose | NNT (95% CI) | Success Rate | Source |
|------|---------------|--------------|--------|
| **Celecoxib 200 mg** | 3.0 (2.5–3.6) | ~40% | Moderate — lower than ibuprofen 400 mg |
| **Celecoxib 400 mg** | **2.5 (2.2–2.9)** | ~50% | Cochrane 2008 |
| **Celecoxib 400 mg + PPI** | 2.5 | ~50% | Standard co-prescription |

**Note:** Celecoxib's NNT is comparable to ibuprofen 400 mg (2.5) at the 400 mg dose but inferior at 200 mg. However, this single-dose acute pain data understates its value in chronic use where GI safety advantage matters.

### Safety / NNH

| Adverse Event | Risk | Notes |
|---------------|------|-------|
| **GI ulcer/bleed** | **Lower than non-selective NSAIDs** | The key advantage; NNH ~4x better than ibuprofen |
| **Cardiovascular (MACE)** | **Increased** (similar to diclofenac) | CLASS trial, PRECISION trial, SCOT trial |
| **Renal** | Similar to other NSAIDs | Fluid retention, BP increase |
| **Sulfonamide allergy** | Cross-reactivity | Contraindicated in sulfa allergy |
| **Upper GI event (annualized)** | 0.3% vs 0.8% (nsNSAID) | PRECISION trial |

### Pain Conditions Covered
- **Osteoarthritis** — primary indication (equally effective to nsNSAIDs)
- **Rheumatoid arthritis** — effective
- **Postoperative pain** — 400 mg loading dose
- **Ankylosing spondylitis** — effective (RAG: PMID:40028763)
- **Oncology** — emerging (COX-2/PGE2 in tumor microenvironment)

### RAG Evidence
- **PMID:39660078** — SCOT trial: CV event biomarkers in celecoxib users
- **PMID:41560736** — Imrecoxib vs celecoxib RCT meta-analysis (2025)
- **PMID:40028763** — Nationwide Korean AS cohort: comparable CV/GI risk (2025)

---

## Key References (with PMIDs)

| PMID | Title | Evidence Level |
|------|-------|----------------|
| 39660078 | SCOT: Vascular/Renal Biomarkers in NSAID Users | MODERATE (Eur Heart J Open) |
| 41560736 | Imrecoxib vs Celecoxib Meta-Analysis | MODERATE (Front Pharmacol) |
| 40028763 | Celecoxib vs nsNSAIDs in AS Cohort | MODERATE (Scand J Rheum) |
| 41383482 | Celecoxib in Oncology — COX-2/PGE | MODERATE (Front Pharmacol) |
| 40819363 | Novel Celecoxib Analogs — Selective COX-2 | MODERATE (Future Med Chem) |

## Framework Takeaways for Celecoxib

1. **Selectivity ratio is a derived L1 metric that propagates to all levels:** 30:1 COX-2/COX-1 selectivity explains the GI safety advantage (L4) AND the CV risk (L3 coxib paradox).
2. **CYP2C9 polymorphism is a L2 factor with L4 consequences:** The framework naturally captures pharmacogenomic stratification. Poor metabolizers have higher exposure → greater GI risk. Single-score comparators don't handle this.
3. **The coxib paradox is an L3 insight:** The framework shows why L1 selectivity → tissue-specific sparing (GI good, CV bad) → L4 outcomes (reduced GI bleeds, increased MACE). This causal chain is explicit in the 4-level design.
4. **Acute NNT understates chronic value:** In single-dose postoperative pain, celecoxib 400 mg = ibuprofen 400 mg (both NNT 2.5). In chronic OA use, celecoxib has a real safety advantage. The framework needs a time × condition dimension.
