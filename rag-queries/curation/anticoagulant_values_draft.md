# Anticoagulant records — extracted values (draft for review)

Every value below carries its source. `—` = not yet sourced (must stay `null` until found; no fabrication).
Extraction method: NCBI E-utilities XML efetch over targeted PK-review / pivotal-trial queries.
(openFDA label API is unreachable from this environment — DNS blocked; LanceDB full text available for OA papers.)

## L1 — target / mechanism

| Drug | Target+potency | Mechanism | Source |
|---|---|---|---|
| apixaban | — (Ki not yet sourced) | oral, direct, highly selective FXa inhibitor | PMID 24733535 |
| rivaroxaban | — | direct inhibitor of activated factor X (FXa) | PMID 37207560 |
| edoxaban | — | oral direct factor Xa inhibitor | PMID 25966665 |
| dabigatran | — | oral direct competitive thrombin inhibitor | PMID 19696042, 37207560 |
| warfarin | — | vitamin K antagonist (VKOR) | (to source) |
| enoxaparin | — | indirect, antithrombin-mediated FXa inhibition (LMWH) | (to source) |

## L2 — PK

| Drug | Bioavailability (%) | half_life_h | Vd | renal_excretion_pct | Source |
|---|---|---|---|---|---|
| apixaban | 66.2 | 12 | 17–26 L ss (`vd_l`) | ~27 (25 per cross-class review) | 24353445; 22722590; 24861792 |
| rivaroxaban | 80–100 (10 mg, food-independent; 15/20 mg need food) | 5–9 (young), 11–13 (elderly) | — | 66 (33 unchanged + 33 metabolites) | 23999929; 23458226; 24861792 |
| edoxaban | 67.2 (relative) | — | — | 33 | 25186833; 24861792 |
| dabigatran | — | 12–14 | — | 80–85 unchanged | 19696042; 31335150 |
| warfarin | — | ~35 | 10 L/70 kg → 0.14 (`vd_l_per_kg`) | hepatic metabolism dominant (negligible renal) | 3542339 |
| enoxaparin | — | — | — | renal | (to source) |

Cross-class renal-elimination source (single PMID): **24861792** — dabigatran ≥80%, rivaroxaban 66%, edoxaban 33%, apixaban 25%.

## L4 — clinical (7-field set)

| Drug | stroke/SE vs warfarin | major bleeding vs warfarin | ICH reduction | reversal_agent | Source |
|---|---|---|---|---|---|
| apixaban | superior (ARISTOTLE) | less bleeding (warfarin HR 1.85 vs apixaban, observational) | — | andexanet alfa (↓anti-Xa 92–94%) | 21870978; 39110427; 29345686 |
| rivaroxaban | (ROCKET-AF — to source) | — | — | andexanet alfa | 29345686 |
| edoxaban | superior net clinical outcome (ENGAGE AF) | dose-reduction benefit in ≥80 y | — | andexanet alfa (partial) | 38828563; 38985461 |
| dabigatran | superior stroke/SE prevention (RE-LY, 150 mg) | — | — | idarucizumab | 22435606 |
| warfarin | reference comparator | reference comparator | reference comparator | vitamin K + PCC | (to source) |
| enoxaparin | (VTE focus — to source) | — | n/a | protamine | (to source) |

## Still to source (must remain null until found)

- **Protein binding** — all 6 (except enoxaparin low). Class review 24861792 is a candidate source.
- **Vd** — rivaroxaban, edoxaban, dabigatran, enoxaparin (`vd_l`).
- **L1 potency (Ki/IC50)** — all 6.
- **Exact ARISTOTLE / ROCKET-AF / RE-LY HRs** — qualitative statements found; numeric HRs need a source (PMID 21870978 abstract is truncated in PubMed).
- **Metabolism strings** — CYP3A4/P-gp per drug (note: efflux transporters NOT clinically relevant for apixaban, PMID 42124949; relevant for rivaroxaban).
- **Dose-reduction criteria** — CrCl/age/weight thresholds per drug.
- **Safety** — pregnancy / lactation / hepatic for most.
- **Enoxaparin PK** — anti-Xa-based; needs its own retrieval approach.

## Notes / findings

- The abstract-level relevance harvest (226 PMIDs, committed) is **context-rich but value-poor**; targeted PK-review queries + XML efetch are what surfaced the numbers.
- Three retrieval routes now known: NCBI targeted queries (primary), LanceDB vector search (precise paper discovery, rag-service venv), openFDA labels (**blocked — DNS**).
