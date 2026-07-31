# Framework Ontology — The 4 Levels

## What This Framework Does

This framework profiles drugs across four dimensions — molecular binding, pharmacokinetics, systems response, and clinical outcomes — producing a structured, evidence-graded fingerprint. It does not produce a single score or rank. Quantification here means dimensional profiling: each level is independently populated, and the user weighs the dimensions according to their context.

## The 4 Levels

### L1 — Molecular Binding

**What it captures:** The drug's interaction with its molecular targets — primary (intended) and off-target (unintended). Reported as Ki (inhibition constant), Kd (dissociation constant), IC50 (half-maximal inhibitory concentration), or EC50 (half-maximal effective concentration).

**Data sources:** PDSP Ki database, IUPHAR/BPS Guide to Pharmacology, published SAR studies, crystallography.

**Rules:**
- List primary target(s) first with Ki/Kd values
- Off-target pharmacology follows, limited to targets with established relevance at therapeutic concentrations
- Active metabolites (prodrugs, major circulating metabolites) get their own binding profile
- Flag assay conditions where known (species, temperature, radioligand) — Ki values vary by condition
- Evidence level: typically MODERATE (single-well-executed SAR) or HIGH (multiple consistent measurements)

### L2 — Pharmacokinetics

**What it captures:** How the drug moves through the body — absorption, distribution, metabolism, excretion (ADME). Key parameters: bioavailability, volume of distribution, half-life, protein binding, metabolism pathways, clearance, food effects.

**Data sources:** DrugBank, Inxight FRDB, Lombardo et al. PK datasets, FDA clinical pharmacology reviews, published PopPK studies.

**Rules:**
- Report plasma half-life and tissue half-life separately where available (they often differ)
- Note active metabolites and their PK profiles
- Flag pharmacogenomic vulnerabilities (e.g., CYP2C9 polymorphism for celecoxib)
- Report dose-standardized values where possible
- Evidence level: typically HIGH for well-studied drugs (multiple independent measurements)

### L3 — Systems Response

**What it captures:** The biological consequence of L1 binding expressed at the tissue and pathway level — COX inhibition dynamics, downstream signaling, tissue penetration kinetics, off-target pathway engagement.

**Data sources:** Published mechanistic studies, pathway analyses, tissue distribution studies. This level has no single structured database and is primarily populated via literature mining.

**Rules:**
- Separate direct pharmacology (e.g., COX inhibition time course) from pathway consequences (e.g., PGI2 suppression)
- Document tissue-specific PK where available (e.g., synovial fluid half-life)
- Note which L1 targets have established L3 consequences vs. speculative
- Active metabolites get their own L3 profile
- Evidence level: typically MODERATE (mechanistic studies) or LOW (emerging)

### L4 — Clinical Outcomes

**What it captures:** Clinical efficacy and safety in humans — NNT (number needed to treat), NNH (number needed to harm), effect sizes, adverse event rates, and condition-specific outcomes.

**Data sources:** Cochrane systematic reviews, Oxford Pain League Table, published RCTs, FDA labeling.

**Rules:**
- Report dose-specific outcomes where available (e.g., ibuprofen 200 mg vs 400 mg NNT differ)
- Stratify by condition when evidence exists (acute pain NNT ≠ chronic pain NNT)
- Report both efficacy (NNT) and safety (NNH, adverse event rates)
- Evidence level: typically HIGH for Cochrane-backed outcomes, MODERATE for single trials

### L4 Data Schema — `l4_clinical` block

Each drug profile carries an `l4_clinical` object in `api/drugs.json`. Schema is class-specific (locked 2026-07-31; 88/88 drugs populated):

**Antihypertensive (and Diabetes share the key set, differing in `nnt_bp_control` inner shape):**

```jsonc
{
  "nnt_bp_control": {
    // Antihypertensive:
    "value": 3,          // int — NNT for BP control
    "ci_95": "2-5",      // string — 95% CI as "lo-hi"
    "dose": "2.5-20mg",  // string — dose range the NNT applies to
    // Diabetes instead uses:
    // "a1c_reduction": 1.2, "unit": "%", "dose": "1.2-1.8mg SC"
  },
  "indications": ["Hypertension", "Heart failure"], // string[]
  "success_rate": 0.53,   // float 0-1 — probability of the primary efficacy endpoint
  "onset_min": 120        // Antihypertensive: int minutes. Diabetes: string "days"|"hours"|"weeks"
}
```

Onset captures mechanism: direct antagonists (ramipril 120 min, furosemide 60 min) vs prodrugs requiring activation + CNS penetration (methyldopa 300 min) vs nuclear-receptor transcription (spironolactone 1440 min).

**Legacy class-specific shapes (pre-existing, unchanged):**

| Class | Key fields |
|-------|-----------|
| NSAID | `nnt_50_pain_relief`, `nnh_gi`, `nnh_cv`, `onset_min`, `success_rate` (+ optional `note`) |
| Statin | `nnt_mace_5yr`, `ldl_reduction_mean_pct`, `myopathy_rate_per_1000`, `rhabdo_rate_per_1000`, `success_rate_ldl_goal` |
| PPI | `ee_healing_4wk_pct`, `ee_healing_8wk_pct`, `duodenal_ulcer_healing_4wk_pct`, `gerd_symptom_nnt`, `h_pylori_eradication_pct`, `maintenance_12mo_pct`, `ddi_burden`, `pregnancy_safety` |
| H2RA | `ee_healing_8wk_pct`, `duodenal_ulcer_healing_4wk_pct`, `gerd_symptom_nnt`, `ddi_burden`, `pregnancy_safety` |
| Antacid / Alginate / Mucosal protectant | `ddi_burden`, `pregnancy_safety` (+ class-specific healing fields for alginate) |

**Conventions:**
- Quantitative endpoints are sparse in source digests; values are class-anchored pharmacology when direct evidence is absent. Original quantification carried `_evidence_level` / `_evidence_note` flags that are stripped at merge time — the ontology treats the block as evidence-graded at the field level, not the block level.
- Phantom-field adjudication (keyword hits beyond the 300-char truncation window in L3 extraction) is recorded in `rag-queries/l2b_overrides.json` under `phantom_adjudication.verdicts` (27 verdicts as of 2026-07-31).

## Causal Relationships Between Levels

The levels are not independent. L1→L3→L4 forms a causal chain:

```
L1 (binding) → L3 (tissue consequences) → L4 (clinical outcomes)
```

L2 (pharmacokinetics) modulates the translation from L1 to L3:
```
L1 → [L2: how much drug reaches target] → L3 → L4
```

This means information appears at multiple levels — e.g., COX-2 selectivity appears at L1 (binding ratio), L3 (PGI2 vs TXA2 balance), and L4 (GI sparing vs CV risk). This is intentional: it preserves the causal chain rather than deduplicating.

## Active Metabolite Ontology

When a drug acts primarily through an active metabolite (prodrug), represent both:

- **Parent drug** L1: metabolism pathway, prodrug status
- **Active metabolite** L1, L2, L3, L4: the effective molecule's profile

Example: paracetamol is profiled as parent (L1: weak COX-2) with AM404 as its active metabolite (L1: TRPV1 + Nav1.8 + CB1; L3: dual central/peripheral pathways).

Other drugs requiring this treatment: sulindac → sulindac sulfide, nabumetone → 6-MNA, codeine → morphine.

## What Quantification Means in This Framework

The framework quantifies by providing structured, comparable data across defined dimensions. It does not collapse those dimensions into a single score. The "quantification" is in the:

1. **Standardized schema** — every drug profile follows the same 4-level structure
2. **Comparable metrics** — same parameters reported for every drug (e.g., all NNTs use ≥50% pain relief over 4-6 h)
3. **Evidence grading** — every datum tagged with traceable evidence level
4. **Dimensional separation** — independent profiling of each level preserves information a single score would lose

A ranked comparison is possible — but only after the user applies context-specific weights. The framework itself remains agnostic.

## Condition and Population Dimensions

Outcomes vary by condition and population. The framework captures this by:

- Reporting NNTs per condition (acute pain ≠ chronic OA ≠ headache)
- Flagging pharmacogenomic factors (CYP2C9, HLA, etc.)
- Stratifying safety outcomes by risk population where available
- Including a "population variability" note in each L4 section

This is not a separate level — it is a qualifier applied to L4 data.
