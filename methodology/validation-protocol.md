# Validation Protocol — Holdout Generalizability Test (Tier 2)

> **Rationale:** The PoC covers 4 NSAID-class drugs. R2's review (v3) asked whether DQF generalizes or is hand-tuned to this specific set. A formal holdout test answers this without requiring external experts or clinical vignettes.

## Design

Leave-one-drug-out cross-validation within the existing 4-drug NSAID class. For each round, one drug is the **holdout** — the framework is populated from the other three — and the predicted profile is compared against the known profile (from literature).

### Rounds

| Round | Holdout | Training Set | Tests |
|-------|---------|-------------|-------|
| A | Ibuprofen | Diclofenac, Celecoxib, Paracetamol | Predict L1 off-target profile, L3 systems features, L4 clinical performance |
| B | Diclofenac | Ibuprofen, Celecoxib, Paracetamol | Same |
| C | Celecoxib | Ibuprofen, Diclofenac, Paracetamol | Same |
| D | Paracetamol | Ibuprofen, Diclofenac, Celecoxib | Same |

Each round answers: **did the training set produce a profile that matches the known literature for the holdout?** If yes, the framework generalizes within the class. If no, the framework overfits to the training set.

## What Gets Predicted Per Level

### L1 — Molecular Binding

**Predicted targets:** Which off-target proteins appear in ≥2 of the 3 training drugs at relevant Ki.

**Prediction:** The holdout drug will have some subset of these shared targets.

**Known limitation:** This tests whether NSAIDs share off-target pharmacology. If the holdout has unique targets (e.g., diclofenac's P2X3) that no training drug has, the prediction correctly misses them — and this is informative. A "miss" on a unique target is not a framework failure.

**Scoring:** For each predicted target, does the holdout have activity? Yes/No/Unknown.

### L3 — Systems Response

**Predicted features:** Tissue-level consequences shared by training drugs (e.g., synovial residence time extension, GI prostaglandin suppression).

**Prediction:** The holdout will have comparable tissue-level effects where it shares L1 targets.

**Scoring:** Qualitative comparison — does the holdout's L3 profile follow the training set pattern? Divergences (e.g., paracetamol's absent anti-inflammatory effect) are explainable by L1 differences.

### L4 — Clinical Outcomes

**Predicted NNT range:** From the training-set NNTs (range 2.5–3.6 for acute pain), can the holdout's NNT be bounded?

**Prediction:** Holdout NNT falls within or near the training-set range.

**Scoring:** Is holdout NNT within ±1 NNT unit of the training-set geometric mean? Flag outliers.

## Expected Results

| Holdout | Expected Prediction | Framework Verdict |
|---------|-------------------|-------------------|
| Ibuprofen | Well-predicted. All features shared with at least 2 training drugs. ASIC1a may be missed (unique). | **Generalizes** — typical NSAID with one unique feature. |
| Diclofenac | Mixed. Shared COX features well-predicted. P2X3 (unique), biliary PK, and synovial duration may be missed. | **Generalizes with gaps** — unique features are *informative misses*. |
| Celecoxib | COX-2 selectivity is partially shared (diclofenac has moderate selectivity). Predicted CV/GI profile may deviate. | **Generalizes** — selectivity gradient captured from training set. |
| Paracetamol | **Fails deliberately.** Paracetamol is not an NSAID — different mechanism, different L4 profile. This holdout tests whether the framework identifies incommensurability. | **Expected failure** — confirms framework can detect class outliers. |

## Success Criteria

| Criterion | Acceptable | Good |
|-----------|------------|------|
| L1 shared targets recall | ≥60% of shared targets found in holdout | ≥80% |
| L1 unique targets flagged as "training-set-specific" | ≥1 unique target per holdout correctly identified | All unique targets noted |
| L3 profile consistency | Qualitative match for shared targets | Divergences explained by L1 differences |
| L4 NTT bounding | Holdout NTT within ±1 of training mean | Holdout NNT within training range |

## Effort

- **Data extraction:** ~1-2 h per round (assemble training set → read holdout literature → compare)
- **Analysis:** ~1 h after all 4 rounds
- **Total: ~6-10 h** — no RAG queries needed (all data already exists in profiles)

## Deliverable

A table or matrix showing for each holdout:

```
Holdout: Ibuprofen
  L1 shared targets predicted: COX-1, COX-2, TRPV1, PPARγ  →  Found: COX-1✓, COX-2✓, TRPV1✓, PPARγ✓
  L1 unique targets missed: ASIC1a → Correct miss (unique to ibuprofen)
  L3 profile: ↓↓↓GI prostaglandins, ↓platelet, moderate synovial duration → Match ✓
  L4 NNT predicted: 2.5-3.0 → Actual: 2.5 ✓
  Verdict: GENERALIZES
```

## Relationship to Tier 1 (Literature-Anchor)

Tier 1 would be faster but weaker: it would ask whether DQF rankings match Cochrane findings. That's circular — we built DQF from Cochrane data. Tier 2's holdout design breaks the circularity by testing prediction, not fit.

## Relationship to Tier 3 (Expert Panel)

Tier 3 would be stronger but expensive: give 3-5 clinical pharmacologists de-identified vignettes, compare rankings against DQF via weighted κ. Not needed until Tier 2 results are known. If Tier 2 fails dramatically, Tier 3 is moot.
