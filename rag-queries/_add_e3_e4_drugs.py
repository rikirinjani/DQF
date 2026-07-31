#!/usr/bin/env python3
"""Batch-add E3 (Antihypertensive) and E4 (Diabetes) drug entries to drugs.json."""
import json, sys
from pathlib import Path

DRUGS_JSON = Path(__file__).resolve().parent.parent / "api" / "drugs.json"

# ── Drug entry data ──────────────────────────────────────────────────
NEW_DRUGS = [
    # ── E3: Antihypertensives ──
    {
        "id": "lisinopril",
        "class": "Antihypertensive",
        "name": "Lisinopril",
        "l1_binding": {
            "targets": [{"name": "ACE", "value": 8.5, "unit": "-log10 IC50"}],
            "mechanism": "Competitive ACE inhibitor, blocks AngI → AngII conversion",
            "selectivity": "ACE > ACE2 (no bradykinin breakdown)"
        },
        "l2_pk": {
            "bioavailability": 25,
            "half_life_h": 12.0,
            "vd_l_per_kg": 0.2,
            "metabolism": "Not metabolized (renal elimination unchanged)",
            "renal_excretion_pct": 100,
            "special": "Long ACE-binding half-life permits once-daily dosing despite short serum t½"
        },
        "l4_clinical": {
            "nnt_bp_control": {"value": 3, "ci_95": "2-5", "dose": "10-40mg"},
            "indications": ["Hypertension", "Heart failure", "Post-MI", "Diabetic nephropathy"],
            "success_rate": 0.55,
            "onset_min": 60
        },
        "pregnancy_safety": "D",
        "lactation_safety": "safe",
        "hepatic_safety": "safe"
    },
    {
        "id": "losartan",
        "class": "Antihypertensive",
        "name": "Losartan",
        "l1_binding": {
            "targets": [{"name": "AT1 receptor", "value": 8.8, "unit": "-log10 Ki"}],
            "mechanism": "Selective AT1 receptor antagonist; active metabolite E-3174 more potent",
            "selectivity": "AT1 >>> AT2"
        },
        "l2_pk": {
            "bioavailability": 33,
            "half_life_h": 2.0,
            "vd_l_per_kg": 0.4,
            "metabolism": "CYP2C9, CYP3A4 (prodrug → E-3174 active metabolite, t½ 6-9h)",
            "renal_excretion_pct": 60,
            "special": "Active metabolite E-3174 has 10-40x greater AT1 affinity"
        },
        "l4_clinical": {
            "nnt_bp_control": {"value": 4, "ci_95": "3-6", "dose": "50-100mg"},
            "indications": ["Hypertension", "Diabetic nephropathy", "Stroke prevention (LIFE)"],
            "success_rate": 0.52,
            "onset_min": 120
        },
        "pregnancy_safety": "D",
        "lactation_safety": "safe",
        "hepatic_safety": "caution"
    },
    {
        "id": "amlodipine",
        "class": "Antihypertensive",
        "name": "Amlodipine",
        "l1_binding": {
            "targets": [{"name": "L-type calcium channel", "value": 9.2, "unit": "-log10 IC50"}],
            "mechanism": "Dihydropyridine CCB, blocks L-type Ca channels in vascular smooth muscle",
            "selectivity": "Vascular >>> cardiac (no significant negative inotropy)"
        },
        "l2_pk": {
            "bioavailability": 74,
            "half_life_h": 40.0,
            "vd_l_per_kg": 21.0,
            "metabolism": "CYP3A4 (extensive hepatic)",
            "renal_excretion_pct": 10,
            "special": "Very long t½ permits once-daily dosing; slow onset avoids reflex tachycardia"
        },
        "l4_clinical": {
            "nnt_bp_control": {"value": 3, "ci_95": "2-5", "dose": "5-10mg"},
            "indications": ["Hypertension", "Stable angina", "Vasospastic angina"],
            "success_rate": 0.60,
            "onset_min": 360
        },
        "pregnancy_safety": "C",
        "lactation_safety": "safe",
        "hepatic_safety": "caution"
    },
    {
        "id": "metoprolol",
        "class": "Antihypertensive",
        "name": "Metoprolol",
        "l1_binding": {
            "targets": [{"name": "β1-adrenergic receptor", "value": 8.7, "unit": "-log10 Ki"}],
            "mechanism": "Selective β1 blocker; reduces CO, HR, and renin release",
            "selectivity": "β1 >> β2 (dose-dependent loss of selectivity at high doses)"
        },
        "l2_pk": {
            "bioavailability": 50,
            "half_life_h": 4.0,
            "vd_l_per_kg": 4.0,
            "metabolism": "CYP2D6 (polymorphic; poor metabolizers have 3-5x higher concentrations)",
            "renal_excretion_pct": 5,
            "special": "CYP2D6 PM phenotype mimics supratherapeutic dosing"
        },
        "l4_clinical": {
            "nnt_bp_control": {"value": 4, "ci_95": "3-7", "dose": "50-200mg"},
            "indications": ["Hypertension", "Angina", "Post-MI", "Heart failure (succinate)"],
            "success_rate": 0.50,
            "onset_min": 120
        },
        "pregnancy_safety": "C/D",
        "lactation_safety": "safe",
        "hepatic_safety": "caution"
    },
    {
        "id": "hydrochlorothiazide",
        "class": "Antihypertensive",
        "name": "Hydrochlorothiazide",
        "l1_binding": {
            "targets": [{"name": "NCC", "value": 7.2, "unit": "-log10 IC50"}],
            "mechanism": "Thiazide diuretic; inhibits Na-Cl cotransporter in distal convoluted tubule",
            "selectivity": "NCC > CA (weak carbonic anhydrase inhibition)"
        },
        "l2_pk": {
            "bioavailability": 70,
            "half_life_h": 10.0,
            "vd_l_per_kg": 3.0,
            "metabolism": "Not metabolized (eliminated unchanged in urine)",
            "renal_excretion_pct": 95,
            "special": "Duration longer than t½ suggests prolonged tissue binding to RBC CA"
        },
        "l4_clinical": {
            "nnt_bp_control": {"value": 3, "ci_95": "2-5", "dose": "12.5-50mg"},
            "indications": ["Hypertension", "Edema", "Nephrogenic DI"],
            "success_rate": 0.48,
            "onset_min": 120
        },
        "pregnancy_safety": "B",
        "lactation_safety": "safe",
        "hepatic_safety": "safe"
    },
    {
        "id": "chlorthalidone",
        "class": "Antihypertensive",
        "name": "Chlorthalidone",
        "l1_binding": {
            "targets": [{"name": "NCC", "value": 7.5, "unit": "-log10 IC50"}],
            "mechanism": "Thiazide-like diuretic; inhibits Na-Cl cotransporter, longer-acting than HCTZ",
            "selectivity": "NCC (does NOT inhibit CA)"
        },
        "l2_pk": {
            "bioavailability": 65,
            "half_life_h": 50.0,
            "vd_l_per_kg": 4.0,
            "metabolism": "Not metabolized (eliminated unchanged in urine)",
            "renal_excretion_pct": 50,
            "special": "Very long t½ due to extensive RBC partitioning; superior to HCTZ in ALLHAT trial"
        },
        "l4_clinical": {
            "nnt_bp_control": {"value": 3, "ci_95": "2-4", "dose": "12.5-25mg"},
            "indications": ["Hypertension", "Edema"],
            "success_rate": 0.52,
            "onset_min": 180
        },
        "pregnancy_safety": "B",
        "lactation_safety": "safe",
        "hepatic_safety": "safe"
    },
    # ── E4: Diabetes Drugs ──
    {
        "id": "metformin",
        "class": "Diabetes",
        "name": "Metformin",
        "l1_binding": {
            "targets": [{"name": "AMPK", "value": 5.8, "unit": "-log10 Ki"}, {"name": "mitochondrial complex I", "value": 4.2, "unit": "-log10 IC50"}],
            "mechanism": "AMPK activation via mitochondrial complex I inhibition; decreases hepatic gluconeogenesis",
            "selectivity": "Broad pleiotropic"
        },
        "l2_pk": {
            "bioavailability": 55,
            "half_life_h": 6.0,
            "vd_l_per_kg": 1.0,
            "metabolism": "Not metabolized (eliminated unchanged in urine)",
            "renal_excretion_pct": 90,
            "special": "Contraindicated if eGFR <30; lactic acidosis risk with renal impairment"
        },
        "l4_clinical": {
            "nnt_bp_control": {"a1c_reduction": 1.5, "unit": "%", "dose": "2000mg"},
            "indications": ["T2DM", "Prediabetes", "PCOS", "GDM"],
            "success_rate": 0.65,
            "onset_min": "days"
        },
        "pregnancy_safety": "B",
        "lactation_safety": "safe",
        "hepatic_safety": "caution"
    },
    {
        "id": "empagliflozin",
        "class": "Diabetes",
        "name": "Empagliflozin",
        "l1_binding": {
            "targets": [{"name": "SGLT2", "value": 8.3, "unit": "-log10 IC50"}],
            "mechanism": "SGLT2 inhibitor; blocks renal glucose reabsorption → glycosuria",
            "selectivity": "SGLT2 >>> SGLT1 (>2500x)"
        },
        "l2_pk": {
            "bioavailability": 78,
            "half_life_h": 12.0,
            "vd_l_per_kg": 1.6,
            "metabolism": "UGT2B7, UGT1A9 (glucuronidation)",
            "renal_excretion_pct": 55,
            "special": "EMPA-REG OUTCOME showed 14% CV mortality reduction"
        },
        "l4_clinical": {
            "nnt_bp_control": {"a1c_reduction": 0.8, "unit": "%", "dose": "10-25mg"},
            "indications": ["T2DM", "Heart failure (EMPEROR-Reduced)", "CKD (EMPA-KIDNEY)"],
            "success_rate": 0.60,
            "onset_min": "days"
        },
        "pregnancy_safety": "C",
        "lactation_safety": "unknown",
        "hepatic_safety": "safe"
    },
    {
        "id": "dapagliflozin",
        "class": "Diabetes",
        "name": "Dapagliflozin",
        "l1_binding": {
            "targets": [{"name": "SGLT2", "value": 8.0, "unit": "-log10 IC50"}],
            "mechanism": "SGLT2 inhibitor; glycosuria, modest diuretic effect",
            "selectivity": "SGLT2 >> SGLT1"
        },
        "l2_pk": {
            "bioavailability": 78,
            "half_life_h": 12.0,
            "vd_l_per_kg": 1.5,
            "metabolism": "UGT1A9 (glucuronidation to inactive metabolite)",
            "renal_excretion_pct": 75,
            "special": "DAPA-HF showed 26% CV death/HF hospitalization reduction irrespective of diabetes status"
        },
        "l4_clinical": {
            "nnt_bp_control": {"a1c_reduction": 0.7, "unit": "%", "dose": "5-10mg"},
            "indications": ["T2DM", "Heart failure (DAPA-HF)", "CKD (DAPA-CKD)"],
            "success_rate": 0.58,
            "onset_min": "days"
        },
        "pregnancy_safety": "C",
        "lactation_safety": "unknown",
        "hepatic_safety": "safe"
    },
    {
        "id": "semaglutide",
        "class": "Diabetes",
        "name": "Semaglutide",
        "l1_binding": {
            "targets": [{"name": "GLP-1 receptor", "value": 9.5, "unit": "-log10 EC50"}],
            "mechanism": "GLP-1 receptor agonist; glucose-dependent insulin secretion, delayed gastric emptying, satiety",
            "selectivity": "GLP-1R >>> glucagon receptor"
        },
        "l2_pk": {
            "bioavailability": 89,
            "half_life_h": 168.0,
            "vd_l_per_kg": 8.0,
            "metabolism": "Proteolysis (peptide backbone degraded to amino acids)",
            "renal_excretion_pct": 3,
            "special": "Once-weekly dosing; SUSTAIN-6 showed 26% CV risk reduction"
        },
        "l4_clinical": {
            "nnt_bp_control": {"a1c_reduction": 1.5, "unit": "%", "dose": "0.5-2.0mg SC"},
            "indications": ["T2DM", "Obesity (2.4mg SC)", "CV risk reduction"],
            "success_rate": 0.70,
            "onset_min": "days"
        },
        "pregnancy_safety": "C",
        "lactation_safety": "unknown",
        "hepatic_safety": "safe"
    },
    {
        "id": "tirzepatide",
        "class": "Diabetes",
        "name": "Tirzepatide",
        "l1_binding": {
            "targets": [{"name": "GIP receptor", "value": 10.3, "unit": "-log10 EC50"}, {"name": "GLP-1 receptor", "value": 9.0, "unit": "-log10 EC50"}],
            "mechanism": "Dual GIP/GLP-1 receptor agonist; superior glycemic control + weight loss vs GLP-1 monotherapy",
            "selectivity": "GIPR ~ GLP-1R (balanced dual agonist)"
        },
        "l2_pk": {
            "bioavailability": 80,
            "half_life_h": 120.0,
            "vd_l_per_kg": 10.0,
            "metabolism": "Proteolysis (amino acid catabolism)",
            "renal_excretion_pct": 3,
            "special": "SURPASS trials: 1.5-2.1% A1c reduction; SURMOUNT-1: 15-21% body weight loss"
        },
        "l4_clinical": {
            "nnt_bp_control": {"a1c_reduction": 2.1, "unit": "%", "dose": "5-15mg SC"},
            "indications": ["T2DM", "Obesity (SURMOUNT)"],
            "success_rate": 0.75,
            "onset_min": "days"
        },
        "pregnancy_safety": "C",
        "lactation_safety": "unknown",
        "hepatic_safety": "safe"
    },
    {
        "id": "insulin-glargine",
        "class": "Diabetes",
        "name": "Insulin Glargine",
        "l1_binding": {
            "targets": [{"name": "insulin receptor", "value": 9.0, "unit": "-log10 Ki"}],
            "mechanism": "Long-acting basal insulin analog; forms microprecipitate at injection site for sustained release",
            "selectivity": "IR >> IGF-1R"
        },
        "l2_pk": {
            "bioavailability": "SC only",
            "half_life_h": 24.0,
            "vd_l_per_kg": 0.2,
            "metabolism": "Proteolysis (metabolites M1 and M2 retain some activity)",
            "renal_excretion_pct": 0,
            "special": "Flat PK profile with no pronounced peak; once-daily basal coverage"
        },
        "l4_clinical": {
            "nnt_bp_control": {"a1c_reduction": 1.2, "unit": "%", "dose": "0.2-0.6 U/kg"},
            "indications": ["T1DM", "T2DM (advanced)"],
            "success_rate": 0.65,
            "onset_min": "hours"
        },
        "pregnancy_safety": "B",
        "lactation_safety": "safe",
        "hepatic_safety": "safe"
    }
]


def main():
    with open(DRUGS_JSON, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {d["id"] for d in data["drugs"]}
    added = 0
    for nd in NEW_DRUGS:
        if nd["id"] in existing_ids:
            print(f"  SKIP {nd['id']} — already exists")
            continue
        data["drugs"].append(nd)
        added += 1
        print(f"  ADD  {nd['id']:25s} ({nd['class']})")

    with open(DRUGS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Added {added} drugs (total now: {len(data['drugs'])})")


if __name__ == "__main__":
    main()
