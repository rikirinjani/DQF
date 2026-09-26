# Anticoagulant records — extracted values (COMPLETE draft for review)

Sources: **PMID** (PubMed/XLM) and **label** (DailyMed SPL, setid listed). `null` = not yet sourced — no fabrication.
Extraction routes: NCBI targeted PK-review/pivotal-trial queries (XML efetch) + DailyMed label API.

> **Correction (2026-09-25):** an earlier revision of this file claimed openFDA was
> "DNS-blocked". That was wrong — it was a wrong hostname. openFDA's API is
> **`api.fda.gov`** (verified: HTTP 200 label for apixaban), not `api.open.fda.gov`
> (a non-existent domain that returns NXDOMAIN from every resolver, which produced the
> `getaddrinfo` failure). No network block existed. NCR-2026-09-25-DQF-OPENFDA filed.

**Source-policy note:** protein binding / Vd / t½ / dose criteria / safety are taken from the
regulatory label (authoritative), which is a mild extension of the PMID-only convention —
flagged for your sign-off.

---

## apixaban — label setid 41a133ef-e461-48ad-8221-b735bdd0ec25 (ELIQUIS)

| Field | Value | Source |
|---|---|---|
| L1 target/potency | null | — |
| L1 mechanism | oral, direct, highly selective FXa inhibitor | PMID 24733535 |
| L2 bioavailability | 66.2 | PMID 24353445 |
| L2 half_life_h | 12 | PMID 22722590; label |
| L2 vd | 21 L (`vd_l`); 177 mL/kg = 0.177 (`vd_l_per_kg`) | label; PMID 34291105 |
| L2 protein_binding_pct | 87 | label |
| L2 metabolism | combined P-gp + strong CYP3A4 substrate | label |
| L2 renal_excretion_pct | ~27 (25 in cross-class review) | PMID 24353445; 24861792 |
| L4 stroke/SE vs warfarin | superior | PMID 21870978 (ARISTOTLE) |
| L4 major bleeding HR | 0.69 (0.60–0.80) | label ARISTOTLE table |
| L4 ICH HR | 0.41 (0.30–0.57) | label |
| L4 GI bleed HR | 0.89 (0.70–1.14) | label |
| L4 reversal_agent | andexanet alfa (↓anti-Xa 92–94%) | PMID 29345686 |
| L4 dose_reduction | 50% reduction with combined P-gp + strong CYP3A4 inhibitors | label |
| pregnancy | not recommended | label |
| hepatic | severe → not recommended | label |

## rivaroxaban — label setid 10db92f9-2300-4a80-836b-673e1ae91610 (XARELTO)

| Field | Value | Source |
|---|---|---|
| L1 target/potency | Ki 0.4 nmol/L (FXa) | PMID 20139357 |
| L1 mechanism | direct FXa inhibitor | PMID 37207560 |
| L2 bioavailability | 80–100 (10 mg, food-independent; 15/20 mg need food) | PMID 23999929; 23458226 |
| L2 half_life_h | 5–9 (young) / 11–13 (elderly) | PMID 23999929 |
| L2 vd | 50 L | label |
| L2 protein_binding_pct | 92 | label |
| L2 metabolism | combined P-gp + strong CYP3A substrate; avoid inducers/inhibitors | label |
| L2 renal_excretion_pct | 66 (33 unchanged + 33 metabolites) | PMID 24861792 |
| L4 stroke/SE HR | 0.88 (ROCKET AF) | label |
| L4 VTE (EINSTEIN-DVT) HR | 0.68 | label |
| L4 CAD/PAD (COMPASS) HR | 0.76 (MACE) | label |
| L4 reversal_agent | andexanet alfa | PMID 29345686 |
| L4 dose_reduction | 15 mg BID ×21 d → 20 mg daily (DVT/PE, with food); 2.5 mg BID + aspirin (CAD/PAD) | label |
| pregnancy | caution (obstetric hemorrhage) | label |
| hepatic | no data in severe impairment | label |

## edoxaban — label setid e77d3400-56ad-11e3-949a-0800200c9a66 (SAVAYSA)

| Field | Value | Source |
|---|---|---|
| L1 target/potency | null | — |
| L1 mechanism | oral direct FXa inhibitor | PMID 25966665 |
| L2 bioavailability | 67.2 (relative) | PMID 25186833 |
| L2 half_life_h | 10–14 | label |
| L2 vd | 107 L (SD 19.9) | label; PMID 26620048 |
| L2 protein_binding_pct | 55 | label |
| L2 metabolism | P-gp substrate; CYP3A4 minor | label |
| L2 renal_excretion_pct | ~50 of total clearance (33 of dose per cross-class review) | PMID 26620048; 24861792 |
| L4 major bleeding HR | 0.80 | label (ENGAGE AF-TIMI 48) |
| L4 CRNM bleeding HR | 0.81 | label |
| L4 stroke/SE | favorable trend HR 0.87 | label |
| L4 reversal_agent | andexanet alfa (partial) | PMID 29345686 |
| L4 dose_reduction | →30 mg if CrCl 15–50, or ≤60 kg, or P-gp inhibitor | label |
| pregnancy | insufficient data | label |
| hepatic | moderate/severe → not recommended | label |

## dabigatran — label setid 9ac0a64a-8666-45f7-9d4f-40fd894f7e6d (PRADAXA)

| Field | Value | Source |
|---|---|---|
| L1 target/potency | null | — |
| L1 mechanism | oral direct competitive thrombin inhibitor (prodrug etexilate) | PMID 19696042 |
| L2 bioavailability | null | — |
| L2 half_life_h | 12–14; label renal table 13 (normal) → 18 (CrCl 30–50) → 27 (CrCl 15–30) | PMID 19696042; label |
| L2 vd | 50–70 L | label |
| L2 protein_binding_pct | 35 | label |
| L2 metabolism | P-gp substrate (etexilate); not CYP-metabolized | label |
| L2 renal_excretion_pct | 80–85 unchanged | PMID 31335150 |
| L4 stroke/SE vs warfarin | superior (RE-LY 150 mg) | PMID 22435606 |
| L4 major bleeding HR | null | — |
| L4 reversal_agent | idarucizumab | PMID 27789605 |
| L4 dose_reduction / renal limit | contraindicated CrCl <30 (EU/Canada); avoid in mechanical valves | label |
| pregnancy | limited data | label |
| hepatic | Child-Pugh B → no consistent change | label |

## warfarin — label setid 654ca5d2-d4c1-48f8-90c4-130a21162bb0

| Field | Value | Source |
|---|---|---|
| L1 target/potency | null | — |
| L1 mechanism | vitamin K antagonist (VKOR; CYP2C9/VKORC1-dependent) | label; PMID 9014207 |
| L2 bioavailability | null (high, ~100) | — |
| L2 half_life_h | ~35 (single-dose ref); effective 20–60 | PMID 3542339; label |
| L2 vd_l_per_kg | 0.14 | PMID 3542339; label |
| L2 protein_binding_pct | 99 (albumin) | label |
| L2 metabolism | S-warfarin CYP2C9; R-warfarin CYP1A2/CYP3A4 | PMID 9014207 |
| L2 renal_excretion_pct | up to 92% of dose recovered in urine (as metabolites) | label |
| L4 vs warfarin | reference comparator (other drugs compared to it) | — |
| L4 monitoring | INR 2–3; TTR 44% in RENAL-AF | PMID 37952132 |
| L4 reversal_agent | vitamin K + prothrombin complex concentrate | label |
| pregnancy | contraindicated (except mechanical valve) | label |
| hepatic | caution (effect may be increased) | label |

## enoxaparin — label setid 20635579-c92d-4f6c-a332-1096d51002f2

| Field | Value | Source |
|---|---|---|
| L1 target/potency | null (indirect) | — |
| L1 mechanism | indirect FXa inhibition via antithrombin (LMWH) | label |
| L2 bioavailability | null (SC ~92 anti-Xa) | — |
| L2 half_life_h | 4.5 (anti-Xa activity) | label |
| L2 vd | 4.3 L (anti-Xa activity distribution) | label |
| L2 protein_binding_pct | null (negligible) | — |
| L2 metabolism | null (minimal; depolymerization) | — |
| L2 renal_excretion_pct | 40 (radioactivity) / 8–20 (anti-Xa) in urine | label |
| L4 VTE | prophylaxis/treatment (30 mg q12h; 1 mg/kg q12h) | label |
| L4 reversal_agent | protamine (partial) | label |
| pregnancy | caution — mechanical valve thrombosis risk | label |
| hepatic | not studied (unknown) | label |

---

## Source-policy — APPROVED

**User approved labels (DailyMed / openFDA) as sources alongside PMIDs (2026-09-25).**
L2 PK fields are recorded label-primary (regulatory authority) with PMID cross-references in `special`.

## Update — nulls closed via openFDA (2026-09-25)

openFDA (`api.fda.gov`) used to close the remaining gaps:

| Item | Value | Source |
|---|---|---|
| apixaban absolute F | 50% | label (PMID 24353445 study: 66.2%) |
| edoxaban absolute F | 62% | label |
| dabigatran absolute F | 3–7% | label |
| enoxaparin PK | t½ 4.5 h, Vd 4.3 L, 40%/8–20% urine | label |
| edoxaban Ki | 0.561 nmol/L | PMID 18624979 |
| dabigatran Ki | 4.5 nM | PMID 17598008 |
| rivaroxaban Ki | 0.4 nmol/L | PMID 20139357 |

### Still null (documented, no source found — no fabrication)

- **L1 potency**: apixaban, warfarin, enoxaparin (rivaroxaban/edoxaban/dabigatran ✓)
- **dabigatran major-bleeding HR** (RE-LY numeric) · **apixaban stroke/SE HR** (0.79 — label table not cleanly extractable)
- **warfarin bioavailability** (not stated in label) · **apixaban ICH/other HRs** partially

## Records built

`rag-queries/_add_e1_anticoagulants.py` adds all 6 records (verified: drugs.json 89 → 95;
existing records unchanged; `l3_systems` seeded for the later merge). New `l2_pk` fields:
`vd_l` (absolute L) and `protein_binding_pct`.
