# Ibuprofen — 4-Level Quantitative Profile

> **Role in PoC:** Baseline reference. The most-studied NSAID, excellent data density across all levels.

---

## L1 — Molecular Binding

### Primary Target: COX-1 / COX-2

| Target | Ki (nM) | Functional Effect |
|--------|---------|-------------------|
| **COX-1** | ~10 nM | Reversible (competitive) |
| **COX-2** | ~200 nM (approx 20× selectivity for COX-1) | Anti-inflammatory |

Ibuprofen is a **non-selective, competitive, reversible** COX inhibitor with modest preference for COX-1. Structurally a propionic acid derivative (S-enantiomer active). The 2-arylpropionate class binds in the COX channel, blocking arachidonic acid access.

### Off-Target Pharmacology (L3-relevant)

| Target | Potency | Relevance |
|--------|---------|-----------|
| **ASIC1a** (acid-sensing ion channel) | Allosteric inhibition | Novel analgesic mechanism — molecular basis elucidated (PMID:28949138) |
| **TRPV1** | Direct inhibition (IC50 ~6 μM) | Conjugated ibuprofen-serotonin shows TRPV1 antagonism; reduces TRPV1 expression in TMJ inflammation models |
| **PPARγ** | Weak agonist (μM range) | May contribute to metabolic effects |
| **OAT1/OAT3** (transporters) | Concentration-dependent inhibition | Drug interaction mechanism (PMID:41338520) |

**Key finding from RAG:** "Molecular Basis for Allosteric Inhibition of Acid-Sensing Ion Channel 1a by Ibuprofen" (PMID:28949138) — ibuprofen inhibits ASIC1a through an allosteric mechanism, independent of COX inhibition. This is an L3 off-target mechanism that likely contributes to analgesic efficacy but is invisible to a single-score comparator.

### Active Metabolites
- **S-ibuprofen** — the active enantiomer (R-ibuprofen undergoes unidirectional chiral inversion to S-ibuprofen *in vivo*, unique among NSAIDs)
- No major active metabolites — largely excreted as glucuronide conjugates

---

## L2 — Pharmacokinetics

| Parameter | Value |
|-----------|-------|
| **Bioavailability** | ~100% (oral), also available IV |
| **pKa** | 4.9 |
| **Volume of distribution** | 0.1 L/kg (very low — confined to plasma due to high protein binding) |
| **Protein binding** | 99% (albumin) |
| **Half-life (plasma)** | 1.8–2.0 h |
| **Half-life (synovial fluid)** | ~4–5 h (longer persistence at effect site) |
| **Tmax** | 1-2 h (oral); 27 min absorption half-life (Morse PopPK, 2023) |
| **Clearance** | 3.79 L/h/70 kg (Morse et al. PopPK) |
| **Metabolism** | Hepatic: CYP2C9 (minor), glucuronidation (major), oxidation |
| **Excretion** | Renal (metabolites) |
| **Food effect** | Absorption delay (1.6× T½ ABS in fed state), minimal effect on extent |

**PK Signature:** Ultra-short plasma half-life but longer synovial fluid residence. High protein binding confines Vd. The 100% bioavailability and rapid absorption make it the fastest-acting oral NSAID.

*Sources: Morse et al. (2023) Population PK, Inxight FRDB. RAG query: PMID:41338520 (ibuprofen OAT interaction). Deranged Physiology, Ibuprofen Pharmacokinetics, derangedphysiology.com. Access date: July 2026.*

---

## L3 — Systems Response

### COX Inhibition Dynamics

| Compartment | Duration | Notes |
|-------------|----------|-------|
| **Plasma COX inhibition** | 4-6 h | Matches t½ ± dosing interval |
| **Synovial fluid COX inhibition** | 8-12 h | Slower equilibration in/out of joint space |
| **Platelet COX-1 (thromboxane)** | ~2 h | Reversible — platelet function returns by next dose (unlike aspirin) |

### Downstream Pathway Effects
- ↓ PGE2, PGI2, PGF2α, thromboxane A2
- ↓ Leukocyte migration into inflammatory sites
- ↓ Fever response (hypothalamic COX-2)
- **No effect on** lipoxygenase pathway (unlike some NSAIDs)
- ASIC1a inhibition → reduced acidosis-induced pain (independent of prostaglandin pathway)

### Tissue Penetration
- **Synovial fluid:** plasma ratio ~0.5 (penetrates well despite high protein binding)
- **CNS:** minimal (poor BBB penetration)
- **Inflamed tissue:** concentrates due to increased permeability + acidic pH trapping

### RAG Evidence
RAG query for `"ibuprofen ASIC TRPV1 ion channel off-target mechanism"` retrieved:
- **PMID:28949138** — Molecular basis of ASIC1a allosteric inhibition by ibuprofen (J Med Chem 2017). Moderate evidence.

---

## L4 — Clinical Outcomes

### Acute Pain (≥50% pain relief over 4-6 h vs placebo)

| Dose | NNT (95% CI) | Success Rate | Source |
|------|---------------|--------------|--------|
| **Ibuprofen 200 mg** | **2.7 (2.5–3.0)** | 46% | Cochrane 2009, Moore 2015 overview |
| **Ibuprofen 400 mg** | **2.5 (2.4–2.6)** | 54% | Cochrane (72 studies, 9,186 participants) |
| **Ibuprofen 600 mg** | ~2.4 | ~58% | Limited data |
| **Ibuprofen fast-acting 200 mg** | **2.1 (1.9–2.4)** | 57% | Cochrane OTC overview (7 studies) |
| **Ibuprofen fast-acting 400 mg** | **2.1 (1.9–2.3)** | 65% | Cochrane OTC overview (13 studies) |
| **Ibuprofen 200 mg + caffeine 100 mg** | **2.1 (1.9–3.1)** | 59% | Cochrane OTC overview |

**Context:** NNT 2.5 is considered **excellent** (among the best of all analgesics). For comparison: paracetamol 1000 mg NNT 3.6, morphine 10 mg IM NNT ~2.9.

### Safety / NNH

| Adverse Event | NNH (vs placebo) | Notes |
|---------------|------------------|-------|
| **Any adverse event** | Not significant | Similar to placebo in single-dose studies |
| **GI bleeding (chronic use)** | ~1 in 1000 patient-years | Dose-dependent, lower risk than naproxen/piroxicam |
| **Cardiovascular (chronic use, high dose)** | Increased at ≥2400 mg/day | Lower risk than diclofenac, comparable to naproxen |

### Pain Conditions Covered (Cochrane evidence)
- **Postoperative dental pain** — primary evidence base (most studies)
- **Dysmenorrhea** — NNT ~3.2
- **Osteoarthritis** — effective, dose-dependent
- **Headache/migraine** — effective (separate Cochrane reviews)
- **Acute back pain** — effective (PMID:41197604, ibuprofen 400 mg vs ketorolac IM)

### RAG Evidence
RAG query for `"ibuprofen NNT 200mg 400mg analgesic Oxford league"` retrieved:
- **PMID:39677212** — IV ibuprofen vs ketorolac meta-analysis (Cureus 2024)
- **PMID:38180091** — Cochrane review: ibuprofen for acute postoperative pain in children (2024)
- **PMID:38653785** — Combination study: paracetamol + ibuprofen + codeine (2024)

---

## Key References (with PMIDs)

| PMID | Title | Evidence Level |
|------|-------|----------------|
| 19821340 | Single Dose Oral Ibuprofen for Acute Postoperative Pain (Cochrane 2009) | HIGH |
| 26544675 | Non-prescription OTC Oral Analgesics for Acute Pain (Cochrane Overview 2015) | HIGH |
| 28949138 | Molecular Basis for Allosteric Inhibition of ASIC1a by Ibuprofen | MODERATE (J Med Chem) |
| 39677212 | IV Ibuprofen vs IV Ketorolac Meta-Analysis | MODERATE (Cureus) |
| 38180091 | Ibuprofen Postoperative Pain Children (Cochrane) | HIGH (Cochrane) |
| 41338520 | Ibuprofen-Flucloxacillin PK Interaction | MODERATE (Int J Antimicrob) |
| 38653785 | Paracetamol/Ibuprofen/Codeine Combination | MODERATE (Eur J Clin Pharm) |
| 41197604 | Oral Ibuprofen vs IM Ketorolac Back Pain | MODERATE (J Pharm Pract) |

## Framework Takeaways for Ibuprofen

1. **Impossible to score:** Is ibuprofen "better" than diclofenac? NNT says yes (2.5 vs 2.7). GI safety says yes. But CV safety? Same ballpark. Off-target analgesia via ASIC1a? Only ibuprofen has it. PK? Shorter t½ limits compliance.
2. **L3 matters:** The ASIC1a off-target effect is invisible to a single COX-focused assay — only a multi-target screen like this framework captures it.
3. **PK-L4 disconnect:** Plasma t½ ~2 h but NNT measured over 4-6 h shows effect persists — explained by L3 (synovial fluid residence, irreversible? COX inhibition time course).
