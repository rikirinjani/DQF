# Cross-Drug Comparison — 4 Levels

> **Why single-score doesn't work:** Every drug wins on at least one dimension. Every drug loses on at least one. No meaningful single number exists.

---

## L1 — Molecular Binding: Side-by-Side

| Target | Ibuprofen | Diclofenac | Celecoxib | Paracetamol |
|--------|-----------|------------|-----------|-------------|
| **COX-1** | ✅ ~10 nM | ✅ ~5 nM | ❌ ~500 nM | ❌ >100 μM |
| **COX-2** | ~200 nM | ✅ ~5 nM | ✅ ~5 nM | ~5 μM (weak) |
| **COX-2 selectivity** | ~0.05 (COX-1 preferring) | ~1 (non-selective) | **~30:1 (selective)** | ~0.05 (negligible) |
| **P2X3** | ❌ | ✅ IC50 76 μM | ❌ | ❌ |
| **TRPV1** | ✅ ~6 μM (inhibition) | ✅ ~19 μM (inhibition) | ❌ | ✅ ~1 μM (AM404 agonist) |
| **ASIC1a** | ✅ Allosteric | ❌ | ❌ | ❌ |
| **Nav1.8/1.7** | ❌ | ❌ | ❌ | ✅ nM (AM404) |
| **CB1** | ❌ | ❌ | ❌ | ✅ Indirect (AM404) |
| **PPARγ** | ✅ Weak | ❌ | ❌ | ❌ |

**Interpretation:** No drug has the same binding profile as any other. Diclofenac has unique P2X3 activity. Ibuprofen has unique ASIC1a activity. Paracetamol has a completely different mechanism via AM404. Celecoxib has the selectivity dimension. The L1 fingerprints are **orthogonal**.

---

## L2 — Pharmacokinetics: Side-by-Side

| Parameter | Ibuprofen | Diclofenac | Celecoxib | Paracetamol |
|-----------|-----------|------------|-----------|-------------|
| **Bioavailability** | **100%** | 65% | 80% | 80% |
| **Vd (L/kg)** | **0.1** | 1.4 | **5-6** | 0.9 |
| **Protein binding** | 99% | 99% | 97% | **20%** |
| **Half-life (plasma)** | 1.8 h | 1.2 h | **8-12 h** | 2.0 h |
| **Half-life (synovial)** | 4-5 h | **8-12 h** | ~12 h | N/A (no COX effect) |
| **Metabolism** | Glucuronidation + CYP2C9 | CYP2C9 + **biliary 30%** | **CYP2C9 only** | Glucuronidation + sulfation |
| **Active metabolite** | No | Minor | No | **AM404 (key)** |
| **Dosing** | QID-TID | BID | **QD-BID** | QID |
| **Renal clearance** | Yes (metabolites) | Biliary + renal | Renal (inactive) | Renal (metabolites) |

**Interpretation:**
- Ibuprofen: Ultra-fast absorption, ultra-short t½, smallest Vd — fastest onset, shortest duration
- Diclofenac: Highest oral bioavailability first-pass → enterohepatic recirculation creates "longer than t½" effect
- Celecoxib: Largest Vd, longest t½, only CYP2C9-dependent — pharmacogenomic vulnerability
- Paracetamol: Lowest protein binding (only 20%), unique FAAH metabolism for AM404 production, NAPQI toxicity pathway

**Key insight:** Diclofenac has the shortest plasma t½ (1.2 h) but BID dosing works — because tissue t½ >> plasma t½. Paracetamol has a longer plasma t½ (2 h) but QID dosing — because it lacks COX-mediated duration amplification.

---

## L3 — Systems Response: Side-by-Side

| Response | Ibuprofen | Diclofenac | Celecoxib | Paracetamol |
|----------|-----------|------------|-----------|-------------|
| **COX inhibition** | Reversible, moderate | **Reversible, potent** | Reversible, COX-2 only | Negligible in vivo |
| **Anti-inflammatory** | Yes | **Potent** | Yes | **No** |
| **GI prostaglandins** | ↓↓↓ | ↓↓↓ | **↓ (spared)** | Normal |
| **Platelet function** | **↓ (temporary)** | ↓ (temporary) | Normal | Normal |
| **Endothelial PGI2** | ↓ | ↓ | **↓↓** | Normal |
| **Synovial duration** | Moderate | **Long** | Long | N/A |
| **Off-target analgesia** | ASIC1a | **P2X3** | Minimal | **TRPV1 + Nav1.8 + CB1** |
| **Coxib paradox** | N/A | N/A | ✅ Present | N/A |
| **Therapeutic window issue** | No | No | No | **Yes (glutathione)** |

**Interpretation:**
- Diclofenac: Most potent COX inhibition, longest tissue duration, unique P2X3 pathway
- Celecoxib: The coxib paradox — GI-sparing but CV-harmful — is a L3 emergent property
- Paracetamol: No anti-inflammatory effect, but 3 distinct analgesic pathways (central TRPV1/CB1, peripheral Nav block). Completely different L3 landscape.

---

## L4 — Clinical Outcomes: Side-by-Side

| Outcome | Ibuprofen 400 mg | Diclofenac 50 mg | Celecoxib 400 mg | Paracetamol 1000 mg |
|---------|-----------------|-----------------|------------------|---------------------|
| **NNT (acute pain)** | **2.5** ✅ | 2.7 | 2.5 | 3.6 ❌ |
| **Success rate** | 54% | 55% | 50% | 46% |
| **Duration (h)** | 4-6 | 6-8 | 6-8 | 4 |
| **GI bleed risk** | Moderate | **Highest** | Lowest ✅ | **None** ✅ |
| **CV risk** | Moderate (dose-dep) | **Highest** ✅ | High | **None** ✅ |
| **Hepatotoxicity** | No | Rare | No | **Yes** ❌ |
| **Renal risk** | Yes | Yes | Yes | Minimal ✅ |
| **Antipyretic** | ✅ | ✅ | ✅ | ✅ (potent) |
| **Anti-inflammatory** | ✅ | ✅ | ✅ | ❌ |

### The "Which Is Best?" Problem

| Patient Scenario | Best Choice | Why (from framework) | Source |
|-----------------|-------------|---------------------|--------|
| **Young, healthy, acute dental pain** | Ibuprofen 400 mg | Best NNT, fast onset, short duration | Cochrane 2009 [PMID:19821340] |
| **Elderly OA + CV risk** | Paracetamol first-line | No CV risk — even though NNT is worse | Mallet 2023 [PMID:37016715] |
| **Elderly OA + GI risk** | Celecoxib + PPI | COX-2 selectivity spares GI | SCOT trial [PMID:39660078] |
| **Severe acute pain, need injection** | Diclofenac IM | Potent COX inhibition, P2X3 adds analgesia | [PMID:39763427] |
| **Patient on warfarin** | Paracetamol | No platelet effect, no GI bleed risk | [PMID:37016715] |
| **Renal colic** | Diclofenac | IM formulation, P2X3 in ureteric pain | [PMID:39763427] |
| **Post-op multimodal** | Paracetamol + ibuprofen | Different mechanisms → synergy | Moore 2015 [PMID:26544675] |

---

## Framework Summary: What the 4 Levels Reveal

### Things a single score CANNOT capture:

1. **Diclofenac vs ibuprofen for acute pain**
   - Same NNT ballpark (2.5 vs 2.7)
   - BUT: diclofenac has P2X3 activity (unique), enterohepatic recirculation (unique), higher CV risk (important for chronic use)
   - A single score can't tell you which to choose for which patient

2. **Celecoxib's paradox**
   - NNT 2.5 — same as ibuprofen
   - Safer for GI (L4) — driven by COX-2 selectivity (L1) → GI COX-1 sparing (L3)
   - Higher CV risk (L4) — driven by COX-2 selectivity (L1) → PGI2 suppression (L3)
   - The mechanism of both advantage and disadvantage is the SAME molecular feature

3. **Paracetamol's incommensurability**
   - NNT 3.6 — looks "worse" than ibuprofen's 2.5
   - But completely different mechanism, zero GI/CV toxicity, different indications
    - Comparing paracetamol to NSAIDs on a single score collapses mechanism, safety, and pharmacokinetics into one dimension — but paracetamol and ibuprofen don't share a mechanism, don't share a risk profile, and the right choice depends on whether your patient is bleeding, has heart disease, or just needs a tooth pulled

4. **Ibuprofen's hidden feature**
   - Best NNT among the set (2.5 for 400 mg)
   - Also has ASIC1a activity — no other PoC drug has this
   - This L3 feature is invisible at L4

### What the Framework Does Well

| Capability | Example |
|------------|---------|
| **Captures different mechanisms** | Paracetamol's AM404 vs diclofenac's P2X3 vs ibuprofen's ASIC1a |
| **Traces L1→L3→L4 causality** | COX-2 selectivity (L1) → PGI2/platelet imbalance (L3) → CV events (L4) |
| **Handles PK/L3 disconnect** | Diclofenac's 1.2 h t½ → 8-12 h synovial duration |
| **Stratifies by patient** | Same drug, different patient → different profile relevance |
| **Accommodates prodrugs** | Paracetamol→AM404, sulindac, nabumetone |
| **Evidence-graded** | Every data point has PMID, evidence level, confidence |

### What Needs Work

| Gap | Priority |
|-----|----------|
| **L3 systematic compilation** — currently literature-mined per drug | High |
| **Pain-condition-specific L4** — acute vs chronic vs headache NNTs differ | High |
| **Dose standardization** — comparison across doses (e.g., ibuprofen 200 vs 400 mg) | Medium |
| **Active metabolite ontology** — how to represent AM404 as the effective agent | Medium |
| **Population variability** — age, genetics (CYP2C9), comorbidities | Low (v2) |
