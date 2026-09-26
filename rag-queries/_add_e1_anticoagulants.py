#!/usr/bin/env python3
"""Batch-add E1 (Anticoagulant) drug entries to drugs.json.

Values sourced from DailyMed/openFDA regulatory labels + PubMed (PMIDs noted).
Nothing is fabricated: unsourced fields are null. See
rag-queries/curation/anticoagulant_values_draft.md for the full provenance table.

New l2_pk fields introduced: `vd_l` (absolute volume of distribution, litres) and
`protein_binding_pct` (%). Existing `vd_l_per_kg` retained where per-kg is published.
"""
import json
from pathlib import Path

DRUGS_JSON = Path(__file__).resolve().parent.parent / "api" / "drugs.json"

NEW_DRUGS = [
    {
        "id": "apixaban",
        "class": "Anticoagulant",
        "name": "Apixaban",
        "l1_binding": {
            "targets": [],
            "mechanism": "Oral, direct, highly selective factor Xa (FXa) inhibitor (PMID 24733535)",
            "selectivity": "FXa-selective; efflux transporters (P-gp/BCRP) NOT clinically relevant for disposition (PMID 42124949)"
        },
        "l2_pk": {
            "bioavailability": 50,
            "half_life_h": 12.0,
            "vd_l": 21.0,
            "vd_l_per_kg": 0.177,
            "protein_binding_pct": 87,
            "metabolism": "P-gp + strong CYP3A4 substrate; combined inhibitors require 50% dose reduction (label)",
            "renal_excretion_pct": 27,
            "special": "Absolute F ~50% (label); 66.2% and Vd 17-26 L ss in the dedicated IV/oral study (PMID 24353445). t1/2 12 h (PMID 22722590)."
        },
        "l4_clinical": {
            "stroke_se_reduction_vs_warfarin": "superior - reduced stroke/systemic embolism, less bleeding, lower mortality (ARISTOTLE, PMID 21870978)",
            "major_bleeding_hr_vs_warfarin": {"value": 0.69, "ci_95": "0.60-0.80", "source": "label (ARISTOTLE)"},
            "ich_reduction": {"value": 0.41, "ci_95": "0.30-0.57", "source": "label (ARISTOTLE)"},
            "indications": ["Stroke prevention in non-valvular AF", "VTE treatment/prophylaxis", "Post hip/knee replacement prophylaxis"],
            "dose_reduction_criteria": "2.5 mg BID if >=2 of: age >=80, weight <=60 kg, CrCl 15-30; 50% reduction with combined P-gp + strong CYP3A4 inhibitors (label)",
            "onset_min": 180,
            "reversal_agent": "andexanet alfa (reduces anti-Xa activity 92-94%; PMID 29345686)"
        },
        "pregnancy_safety": "not recommended (label)",
        "lactation_safety": "unknown - avoid (label)",
        "hepatic_safety": "severe impairment: not recommended (label)"
    },
    {
        "id": "rivaroxaban",
        "class": "Anticoagulant",
        "name": "Rivaroxaban",
        "l1_binding": {
            "targets": [{"name": "Factor Xa (FXa)", "value": 9.4, "unit": "-log10 Ki"}],
            "mechanism": "Direct factor Xa inhibitor (PMID 37207560); Ki 0.4 nmol/L (PMID 20139357)",
            "selectivity": "Selective for FXa; CYP3A4 + P-gp substrate (label)"
        },
        "l2_pk": {
            "bioavailability": 80,
            "half_life_h": 7.0,
            "vd_l": 50.0,
            "protein_binding_pct": 92,
            "metabolism": "CYP3A4 + P-gp substrate; avoid strong combined inhibitors/inducers (label)",
            "renal_excretion_pct": 66,
            "special": "F 80-100% for 10 mg (food-independent); 15/20 mg require food (PMID 23999929/23458226). t1/2 5-9 h young, 11-13 h elderly. Renal: 33% unchanged + 33% metabolites (PMID 24861792)."
        },
        "l4_clinical": {
            "stroke_se_reduction_vs_warfarin": {"value": 0.88, "ci_95": "see label", "source": "ROCKET AF (label)"},
            "major_bleeding_hr_vs_warfarin": None,
            "ich_reduction": None,
            "indications": ["Stroke prevention in non-valvular AF", "VTE treatment", "Post hip/knee replacement prophylaxis", "CAD/PAD (with aspirin)"],
            "dose_reduction_criteria": "DVT/PE: 15 mg BID x21 d then 20 mg daily with food; CAD/PAD: 2.5 mg BID + aspirin (label)",
            "onset_min": 180,
            "reversal_agent": "andexanet alfa (PMID 29345686)"
        },
        "pregnancy_safety": "caution - obstetric hemorrhage risk (label)",
        "lactation_safety": "unknown (label)",
        "hepatic_safety": "no data in severe impairment (label)"
    },
    {
        "id": "edoxaban",
        "class": "Anticoagulant",
        "name": "Edoxaban",
        "l1_binding": {
            "targets": [{"name": "Factor Xa (FXa)", "value": 9.25, "unit": "-log10 Ki"}],
            "mechanism": "Oral direct factor Xa inhibitor (PMID 25966665); Ki 0.561 nmol/L (PMID 18624979)",
            "selectivity": ">10,000-fold selectivity for FXa (PMID 18624979)"
        },
        "l2_pk": {
            "bioavailability": 62,
            "half_life_h": 12.0,
            "vd_l": 107.0,
            "protein_binding_pct": 55,
            "metabolism": "P-gp substrate; minimal CYP metabolism (label)",
            "renal_excretion_pct": 50,
            "special": "Absolute F 62% (label); relative F 67.2% (PMID 25186833). Vd 107 L (SD 19.9) (PMID 26620048). t1/2 10-14 h (label)."
        },
        "l4_clinical": {
            "stroke_se_reduction_vs_warfarin": "favorable trend HR 0.87; superior net clinical outcome (ENGAGE AF-TIMI 48, PMID 38828563)",
            "major_bleeding_hr_vs_warfarin": {"value": 0.80, "ci_95": "see label", "source": "label (ENGAGE AF-TIMI 48)"},
            "ich_reduction": None,
            "indications": ["Stroke prevention in non-valvular AF", "VTE treatment"],
            "dose_reduction_criteria": "30 mg once daily if CrCl 15-50 mL/min, or weight <=60 kg, or P-gp inhibitor (label)",
            "onset_min": 120,
            "reversal_agent": "andexanet alfa (partial; PMID 29345686)"
        },
        "pregnancy_safety": "insufficient data (label)",
        "lactation_safety": "unknown (label)",
        "hepatic_safety": "moderate/severe impairment: not recommended (label)"
    },
    {
        "id": "dabigatran",
        "class": "Anticoagulant",
        "name": "Dabigatran",
        "l1_binding": {
            "targets": [{"name": "Thrombin (FIIa)", "value": 8.35, "unit": "-log10 Ki"}],
            "mechanism": "Oral direct competitive thrombin inhibitor (prodrug dabigatran etexilate); Ki 4.5 nM (PMID 17598008)",
            "selectivity": "Selective and reversible thrombin inhibition (PMID 17598008)"
        },
        "l2_pk": {
            "bioavailability": 5,
            "half_life_h": 13.0,
            "vd_l": 60.0,
            "protein_binding_pct": 35,
            "metabolism": "Etexilate is a P-gp substrate; dabigatran not CYP-metabolized (label)",
            "renal_excretion_pct": 80,
            "special": "Absolute F 3-7% (label). t1/2 12-14 h (PMID 19696042); renal table CrCl >=80 -> 13 h, 15-30 -> 27 h (label). Renal: 80-85% unchanged (PMID 31335150)."
        },
        "l4_clinical": {
            "stroke_se_reduction_vs_warfarin": "superior - stroke/systemic embolism prevention (RE-LY 150 mg, PMID 22435606)",
            "major_bleeding_hr_vs_warfarin": None,
            "ich_reduction": None,
            "indications": ["Stroke prevention in non-valvular AF", "VTE treatment/prophylaxis"],
            "dose_reduction_criteria": "Contraindicated if CrCl <30 (EU/Canada); not recommended in mechanical heart valves (label)",
            "onset_min": 120,
            "reversal_agent": "idarucizumab (PMID 27789605)"
        },
        "pregnancy_safety": "limited data (label)",
        "lactation_safety": "unknown (label)",
        "hepatic_safety": "moderate (Child-Pugh B): no consistent change (label)"
    },
    {
        "id": "warfarin",
        "class": "Anticoagulant",
        "name": "Warfarin",
        "l1_binding": {
            "targets": [],
            "mechanism": "Vitamin K antagonist (VKOR); reduces synthesis of factors II/VII/IX/X (label)",
            "selectivity": "CYP2C9/VKORC1 genotype-dependent dose variability (label; PMID 9014207)"
        },
        "l2_pk": {
            "bioavailability": None,
            "half_life_h": 35.0,
            "vd_l_per_kg": 0.14,
            "protein_binding_pct": 99,
            "metabolism": "S-warfarin: CYP2C9; R-warfarin: CYP1A2/CYP3A4 (PMID 9014207)",
            "renal_excretion_pct": None,
            "special": "Vd 10 L/70 kg, clearance 0.2 L/h/70 kg, t1/2 ~35 h (PMID 3542339); effective t1/2 20-60 h (label). Up to 92% of dose recovered in urine as metabolites (label)."
        },
        "l4_clinical": {
            "stroke_se_reduction_vs_warfarin": "reference comparator (all DOACs compared against warfarin)",
            "major_bleeding_hr_vs_warfarin": "reference comparator",
            "ich_reduction": "reference comparator",
            "indications": ["Stroke prevention in AF", "VTE treatment/prophylaxis", "Mechanical heart valves"],
            "dose_reduction_criteria": "INR-titrated (target 2-3); no fixed dose (label)",
            "onset_min": None,
            "reversal_agent": "vitamin K + prothrombin complex concentrate (label)"
        },
        "pregnancy_safety": "contraindicated (except mechanical heart valves) (label)",
        "lactation_safety": "compatible (label)",
        "hepatic_safety": "caution - effect may be increased (label)"
    },
    {
        "id": "enoxaparin",
        "class": "Anticoagulant",
        "name": "Enoxaparin",
        "l1_binding": {
            "targets": [],
            "mechanism": "Indirect factor Xa inhibition via antithrombin III (LMWH; anti-Xa:anti-IIa ~3:1) (label)",
            "selectivity": "Predominantly anti-Xa over anti-IIa"
        },
        "l2_pk": {
            "bioavailability": None,
            "half_life_h": 4.5,
            "vd_l": 4.3,
            "protein_binding_pct": None,
            "metabolism": None,
            "renal_excretion_pct": 40,
            "special": "PK based on anti-Xa activity: t1/2 4.5 h, Vd 4.3 L (label). 40% of radiolabeled dose and 8-20% of anti-Xa activity recovered in urine in 24 h (label)."
        },
        "l4_clinical": {
            "stroke_se_reduction_vs_warfarin": None,
            "major_bleeding_hr_vs_warfarin": None,
            "ich_reduction": None,
            "indications": ["VTE prophylaxis", "VTE treatment", "Acute coronary syndrome"],
            "dose_reduction_criteria": "Adjust in severe renal impairment (CrCl <30): 1 mg/kg once daily (label)",
            "onset_min": None,
            "reversal_agent": "protamine (partial reversal; label)"
        },
        "pregnancy_safety": "caution - mechanical valve thrombosis risk (label)",
        "lactation_safety": "unknown (label)",
        "hepatic_safety": "not studied (unknown) (label)"
    }
]


def main():
    with open(DRUGS_JSON, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {d["id"] for d in data["drugs"]}
    added = 0
    for nd in NEW_DRUGS:
        if nd["id"] in existing_ids:
            print(f"  SKIP {nd['id']} - already exists")
            continue
        nd["l3_systems"] = {}   # populated later by the L3 merge (Phase 2 + fetch)
        data["drugs"].append(nd)
        added += 1
        print(f"  ADD  {nd['id']:12s} (Anticoagulant)")

    with open(DRUGS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nDone. Added {added} drugs (total now: {len(data['drugs'])})")


if __name__ == "__main__":
    main()
