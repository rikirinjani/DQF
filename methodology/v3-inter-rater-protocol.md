# V3 Inter-Rater Reliability Protocol — Pharmacist Ranking vs DQF (Tier 3)

> **Rationale:** V1 tested guideline concordance (PPI); the Tier-2 holdout
> (`methodology/validation-protocol.md`) tests generalizability without experts. V3 is the
> Tier-3-style test the protocol anticipated: licensed pharmacists independently rank
> de-identified patient scenarios, and agreement is measured two ways — between raters
> (inter-rater reliability) and between raters and DQF (rater-vs-engine). This quantifies
> whether DQF rankings are consistent with expert judgment, beyond internal consistency.
>
> **Status: INSTRUMENT READY — RESULTS PENDING.** No rater data has been collected; every
> agreement number is absent until real raters submit `v3_rater_R*.json` files. Nothing in
> this protocol or in `v3-scenarios.json` fabricates rater results.

## Design

| Element | Specification |
|---|---|
| Raters | 2–3 licensed pharmacists (R1, R2, R3). Eligibility: active license, ≥2 years clinical practice, no role in building DQF |
| Scenarios | The 12 in `validation/v3-scenarios.json` (V3-S01…S12; 57 candidate items across PPI, NSAID, Statin, Antihypertensive, Anticoagulant) |
| Task | For each scenario, rank **all** candidate drugs from most (1) to least appropriate for the vignette + priority note |
| Output | Ranked list (permutation of candidates), confidence 1–5, one-line rationale per scenario |

### Blinding and anchoring controls

1. Raters see **only** the vignette and candidate drug names — no DQF scores, no L1–L4 data,
   no other rater's rankings.
2. **Scenario order** is randomized per rater (seeded permutation, seed recorded) to prevent
   order/learning effects.
3. **Candidate order within each scenario** is presented in a per-rater randomized order to
   prevent position anchoring; the presented order is recorded so the submitted ranking can be
   distinguished from it.
4. Raters work **independently**; no discussion until all rankings are submitted.
5. DQF rankings are frozen in `v3-scenarios.json` before recruitment and not recomputed until
   analysis (any recompute is logged in the file's `reverification` field).

## Metrics (with justification)

| Metric | When | Why |
|---|---|---|
| **Weighted κ (quadratic)** — primary | 2 raters; per scenario on ordinal rank positions, averaged across scenarios | Corrects for chance agreement and weights large rank displacements more heavily than small ones — the clinically meaningful error scale |
| **Kendall's W** (tie-corrected) | >2 raters; per scenario, averaged | Standard concordance coefficient for k ≥ 3 raters on the same items |
| **Spearman ρ** — secondary | All rater pairs + rater-vs-DQF; per scenario on midranks, averaged | Familiar bounded effect size; midrank handling makes it tie-robust |
| **Top-1 agreement** | Rater vs DQF | The clinically actionable question: does the expert's first choice match the engine's? |
| **Top-3 Jaccard** | Rater vs DQF | Partial-overlap tolerance for classes where several options are genuinely close |

Ties in DQF overall scores are handled with **midranks** (average position), precomputed in
`v3-scenarios.json` (`ranks_midrank`) and used by `v3_agreement.py`.

### Precision reasoning for 12 scenarios

With n = 12 scenarios and expected mean ρ ≈ 0.6–0.8, the 95% CI on the mean (Fisher z
approximation) is roughly ±0.15–0.20 — sufficient to separate "good agreement" (≥ 0.6) from
"poor" (< 0.4). Detecting ρ = 0.6 against a 0.3 null at 80% power requires ~10–12 scenarios;
12 is the minimum defensible panel size. 15 scenarios would tighten the CI to ~±0.12 — a
reasonable extension if recruitment allows, not a requirement.

## Timeline

| Step | Effort |
|---|---|
| Recruitment + consent | 1–2 weeks elapsed |
| Ranking (12 scenarios × 2–3 min) | ~30–45 min per rater |
| Analysis (`v3_agreement.py` + write-up) | ~1 h after all submissions |
| **Total** | ~2–3 weeks elapsed, ~3 h effort |

## Analysis plan

1. Collect `validation/v3_rater_R{1,2,3}.json` (JSON primary; long-format CSV accepted —
   `scenario_id,drug,rank` rows).
2. `python validation/v3_agreement.py --raters <files...>` computes per-scenario and
   aggregated metrics (table above), rater-vs-rater and rater-vs-DQF.
3. **Disagreement documentation** (below) for every rater-vs-DQF ρ < 0.4 or top-1 mismatch.
4. Results written to `validation/V3-inter-rater-results.md` + QMS verification record
   **only when real rater data exists**.

### How DQF rankings per scenario are generated

The exact `QueryRequest` (`scenario.query`) is run through `POST /api/query`
(`api/server.py`, `query_drugs`); where the endpoint raises (lovastatin `KeyError` L115 —
missing `nnt_mace_5yr`; warfarin `TypeError` L292 — null `renal_excretion_pct`), the scoring
functions are invoked directly on the scenario's candidates, replicating the scoring loop
(server.py L694–730): `_compute_efficacy` (L85), `_compute_safety` (L160), `_compute_pk`
(L280), `_compute_mechanism` (L361); overall = `WEIGHTS[prioritize]` weighted sum, rounded to
1 decimal; sorted descending (stable sort → ties keep `api/drugs.json` order). Both paths were
cross-checked equal on 7/12 scenarios before use; all 12 rankings were re-verified against
post-N1 `drugs.json` on 2026-09-28 (11/12 byte-identical; V3-S04 refreshed — meloxicam
`gi_risk` 3→2 moved it rank 6→5).

### How rater-vs-DQF disagreements get documented

Per disagreement, one record in the results file:

```
Scenario: V3-S0X | Drug: <id>
  Rater rank: <n> | DQF rank: <m> (overall <score>)
  Rater rationale (verbatim): <...>
  DQF basis: efficacy <e>, safety <s>, pk <p>, mechanism <mm>
  Classification: engine gap | rater preference | data issue
  Disposition: <feeds L3/L4 adjudication backlog | no action>
```

Classification guide: **engine gap** = DQF missed a consideration the vignette makes salient
(missing dim, stale value); **rater preference** = defensible judgment call within the same
evidence; **data issue** = wrong/null underlying data (feeds the no-fabrication backlog).

## Success criteria

| Metric | Acceptable | Good |
|---|---|---|
| Inter-rater mean weighted κ (2 raters) | ≥ 0.4 | ≥ 0.6 |
| Inter-rater Kendall's W (3 raters) | ≥ 0.5 | ≥ 0.7 |
| Rater-vs-DQF mean Spearman ρ | ≥ 0.4 | ≥ 0.6 |
| Top-1 agreement vs DQF | ≥ 50% | ≥ 70% |
| Disagreement documentation | 100% of top-1 mismatches | + every rationale classified |

## Deliverables

| File | Status |
|---|---|
| `validation/v3-scenarios.json` | Done — instrument (12 scenarios, DQF rankings frozen, reverified post-N1) |
| `validation/v3_rater_sheet.md` | Done — per-rater template + data-entry format |
| `validation/v3_agreement.py` | Done — analysis script (pure Python, no deps; self-test with loudly-labelled SYNTHETIC input) |
| `validation/V3-inter-rater-results.md` | **Blocked pending real raters** — never fabricated |

## Relationship to Tier 1 and Tier 2

Tier 1 (literature-anchor) is circular for DQF — the framework was built from Cochrane-sourced
data. Tier 2 (holdout, `methodology/validation-protocol.md`) tests prediction, not fit. V3
complements both: it tests **agreement with independent expert judgment** — the one axis
neither Tier 1 nor Tier 2 touches. If inter-rater agreement itself is poor (κ < 0.4), the
scenarios are too ambiguous and the rater-vs-DQF comparison is uninterpretable — check
inter-rater first, always.
