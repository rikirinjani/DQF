#!/usr/bin/env python3
"""
Generate comprehensive Antihypertensive + Diabetes drug entries for drugs.json.
Defines all major drugs with L1 targets and basic L2 PK.

Usage:
    python _expand_e3_e4_full.py           # dry-run: show what would be added
    python _expand_e3_e4_full.py --apply   # actually modify drugs.json
"""
import json, sys, copy
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DRUGS_JSON = SCRIPT_DIR.parent / "api" / "drugs.json"

# ============================================================
# ANTIHYPERTENSIVE DRUG DEFINITIONS
# ============================================================

def make_target(name, value=8.0, unit="-log10 Ki"):
    return {"name": name, "value": value, "unit": unit}

ANTIHYPERTENSIVES = [
    # --- ACE inhibitors (target: ACE / kininase II) ---
    {
        "id": "enalapril",
        "class": "Antihypertensive", "name": "Enalapril",
        "l1_binding": {"targets": [make_target("ACE", 9.0)], "mechanism": "ACE inhibitor prodrug; blocks AngI→AngII conversion", "selectivity": "ACE > ACE2"},
        "l2_pk": {"bioavailability": 60, "half_life_h": 11.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic esterase → enalaprilat", "renal_excretion_pct": 90, "special": "Active metabolite enalaprilat; prolonged terminal t½ ~35h"}
    },
    {
        "id": "ramipril",
        "class": "Antihypertensive", "name": "Ramipril",
        "l1_binding": {"targets": [make_target("ACE", 8.8)], "mechanism": "ACE inhibitor prodrug", "selectivity": "ACE > ACE2"},
        "l2_pk": {"bioavailability": 55, "half_life_h": 13.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic → ramiprilat", "renal_excretion_pct": 85, "special": "Active metabolite ramiprilat; tissue ACE binding"}
    },
    {
        "id": "perindopril",
        "class": "Antihypertensive", "name": "Perindopril",
        "l1_binding": {"targets": [make_target("ACE", 8.5)], "mechanism": "ACE inhibitor prodrug", "selectivity": "ACE > ACE2"},
        "l2_pk": {"bioavailability": 35, "half_life_h": 17.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic → perindoprilat", "renal_excretion_pct": 75, "special": "Highest tissue ACE penetration among ACEi"}
    },
    {
        "id": "captopril",
        "class": "Antihypertensive", "name": "Captopril",
        "l1_binding": {"targets": [make_target("ACE", 8.2)], "mechanism": "Direct ACE inhibitor (not prodrug); contains sulfhydryl group", "selectivity": "ACE > ACE2"},
        "l2_pk": {"bioavailability": 65, "half_life_h": 2.0, "vd_l_per_kg": 0.2, "metabolism": "Partial hepatic oxidation", "renal_excretion_pct": 95, "special": "SH group confers free-radical scavenging; short t½ requires BID/TID"}
    },
    {
        "id": "trandolapril",
        "class": "Antihypertensive", "name": "Trandolapril",
        "l1_binding": {"targets": [make_target("ACE", 9.2)], "mechanism": "ACE inhibitor prodrug", "selectivity": "ACE > ACE2"},
        "l2_pk": {"bioavailability": 40, "half_life_h": 24.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic → trandolaprilat", "renal_excretion_pct": 70, "special": "Longest t½; once-daily dosing with 24h BP coverage"}
    },

    # --- ARBs (target: AT1 receptor) ---
    {
        "id": "valsartan",
        "class": "Antihypertensive", "name": "Valsartan",
        "l1_binding": {"targets": [make_target("AT1 receptor", 8.5)], "mechanism": "Competitive AT1 receptor antagonist", "selectivity": "AT1 > AT2 (>20,000-fold)"},
        "l2_pk": {"bioavailability": 25, "half_life_h": 6.0, "vd_l_per_kg": 0.4, "metabolism": "Not metabolized (<20%)", "renal_excretion_pct": 30, "special": "Biliary excretion (70%); food reduces AUC 40%"}
    },
    {
        "id": "candesartan",
        "class": "Antihypertensive", "name": "Candesartan",
        "l1_binding": {"targets": [make_target("AT1 receptor", 9.0)], "mechanism": "AT1 receptor antagonist (insurmountable); prodrug candesartan cilexetil", "selectivity": "AT1 > AT2 (>10,000-fold)"},
        "l2_pk": {"bioavailability": 42, "half_life_h": 9.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic esterase → active candesartan", "renal_excretion_pct": 60, "special": "Insurmountable AT1 blockade; tight receptor binding"}
    },
    {
        "id": "irbesartan",
        "class": "Antihypertensive", "name": "Irbesartan",
        "l1_binding": {"targets": [make_target("AT1 receptor", 9.2)], "mechanism": "Competitive AT1 receptor antagonist", "selectivity": "AT1 > AT2 (>10,000-fold)"},
        "l2_pk": {"bioavailability": 70, "half_life_h": 15.0, "vd_l_per_kg": 0.3, "metabolism": "Hepatic CYP2C9 glucuronidation", "renal_excretion_pct": 20, "special": "Highest bioavailability among ARBs"}
    },
    {
        "id": "olmesartan",
        "class": "Antihypertensive", "name": "Olmesartan",
        "l1_binding": {"targets": [make_target("AT1 receptor", 8.8)], "mechanism": "AT1 receptor antagonist; prodrug olmesartan medoxomil", "selectivity": "AT1 > AT2 (>12,500-fold)"},
        "l2_pk": {"bioavailability": 28, "half_life_h": 13.0, "vd_l_per_kg": 0.2, "metabolism": "Intestinal esterase → olmesartan", "renal_excretion_pct": 50, "special": "Enterohepatic recirculation"}
    },
    {
        "id": "telmisartan",
        "class": "Antihypertensive", "name": "Telmisartan",
        "l1_binding": {"targets": [make_target("AT1 receptor", 9.5)], "mechanism": "AT1 receptor antagonist; PPARgamma partial agonist", "selectivity": "AT1 > AT2 (>3,000-fold); PPARgamma moderate"},
        "l2_pk": {"bioavailability": 45, "half_life_h": 24.0, "vd_l_per_kg": 0.5, "metabolism": "Hepatic glucuronidation", "renal_excretion_pct": 5, "special": "Longest t½ (24h); PPARgamma partial agonism adds metabolic benefit; biliary elimination ~95%"}
    },

    # --- CCBs (target: L-type calcium channel) ---
    {
        "id": "nifedipine",
        "class": "Antihypertensive", "name": "Nifedipine",
        "l1_binding": {"targets": [make_target("L-type calcium channel", 8.5)], "mechanism": "Dihydropyridine CCB; blocks L-type Ca²⁺ channel (Cav1.2)", "selectivity": "Vascular > cardiac"},
        "l2_pk": {"bioavailability": 60, "half_life_h": 2.0, "vd_l_per_kg": 0.8, "metabolism": "Hepatic CYP3A4", "renal_excretion_pct": 80, "special": "Extended-release formulations used; reflex tachycardia with immediate-release"}
    },
    {
        "id": "felodipine",
        "class": "Antihypertensive", "name": "Felodipine",
        "l1_binding": {"targets": [make_target("L-type calcium channel", 8.8)], "mechanism": "Dihydropyridine CCB; L-type Cav1.2 blocker", "selectivity": "Vascular-selective > cardiac"},
        "l2_pk": {"bioavailability": 15, "half_life_h": 25.0, "vd_l_per_kg": 4.0, "metabolism": "Hepatic CYP3A4", "renal_excretion_pct": 70, "special": "High vascular selectivity; grapefruit juice interaction (CYP3A4)"}
    },
    {
        "id": "diltiazem",
        "class": "Antihypertensive", "name": "Diltiazem",
        "l1_binding": {"targets": [make_target("L-type calcium channel", 7.8)], "mechanism": "Non-dihydropyridine CCB; benzothiazepine class", "selectivity": "Cardiac > vascular (rate-limiting)"},
        "l2_pk": {"bioavailability": 40, "half_life_h": 5.0, "vd_l_per_kg": 3.0, "metabolism": "Hepatic CYP3A4 (desacetyl metabolite active)", "renal_excretion_pct": 65, "special": "Negative chronotrope; AV nodal blockade; contraindicated with HFrEF"}
    },
    {
        "id": "verapamil",
        "class": "Antihypertensive", "name": "Verapamil",
        "l1_binding": {"targets": [make_target("L-type calcium channel", 8.2)], "mechanism": "Non-dihydropyridine CCB; phenylalkylamine class", "selectivity": "Cardiac > vascular (rate-limiting)"},
        "l2_pk": {"bioavailability": 22, "half_life_h": 6.0, "vd_l_per_kg": 4.0, "metabolism": "Hepatic CYP3A4 (norverapamil active)", "renal_excretion_pct": 70, "special": "Strong CYP3A4 inhibitor; constipation side effect; negative inotrope"}
    },

    # --- Beta blockers ---
    {
        "id": "atenolol",
        "class": "Antihypertensive", "name": "Atenolol",
        "l1_binding": {"targets": [make_target("beta1-adrenergic receptor", 7.5)], "mechanism": "Cardioselective beta1 antagonist", "selectivity": "beta1 > beta2 (~5-fold)"},
        "l2_pk": {"bioavailability": 50, "half_life_h": 7.0, "vd_l_per_kg": 0.2, "metabolism": "Minimal hepatic (hydrophilic)", "renal_excretion_pct": 90, "special": "Hydrophilic; renal clearance; low CNS penetration"}
    },
    {
        "id": "bisoprolol",
        "class": "Antihypertensive", "name": "Bisoprolol",
        "l1_binding": {"targets": [make_target("beta1-adrenergic receptor", 8.2)], "mechanism": "Cardioselective beta1 antagonist", "selectivity": "beta1 > beta2 (~14-fold, highest)"},
        "l2_pk": {"bioavailability": 90, "half_life_h": 11.0, "vd_l_per_kg": 3.0, "metabolism": "Hepatic CYP2D6 (50%) + renal clearance (50%)", "renal_excretion_pct": 50, "special": "Highest cardioselectivity; balanced clearance; once-daily"}
    },
    {
        "id": "carvedilol",
        "class": "Antihypertensive", "name": "Carvedilol",
        "l1_binding": {"targets": [make_target("beta1-adrenergic receptor", 8.5), make_target("beta2-adrenergic receptor", 8.0), make_target("alpha1-adrenergic receptor", 7.5)], "mechanism": "Non-selective beta + alpha1 antagonist; antioxidant", "selectivity": "Non-selective"},
        "l2_pk": {"bioavailability": 25, "half_life_h": 7.0, "vd_l_per_kg": 1.5, "metabolism": "Hepatic CYP2D6/CYP2C9 (glucuronidation)", "renal_excretion_pct": 15, "special": "Added mortality benefit in HFrEF; vasodilation via alpha1 block; antioxidant properties"}
    },
    {
        "id": "propranolol",
        "class": "Antihypertensive", "name": "Propranolol",
        "l1_binding": {"targets": [make_target("beta1-adrenergic receptor", 8.2), make_target("beta2-adrenergic receptor", 8.0)], "mechanism": "Non-selective beta antagonist", "selectivity": "Non-selective (beta1 = beta2)"},
        "l2_pk": {"bioavailability": 25, "half_life_h": 4.0, "vd_l_per_kg": 4.0, "metabolism": "Hepatic CYP2D6/CYP1A2 (high first-pass)", "renal_excretion_pct": 5, "special": "Lipophilic; CNS penetration; migraine + tremor indications"}
    },
    {
        "id": "nebivolol",
        "class": "Antihypertensive", "name": "Nebivolol",
        "l1_binding": {"targets": [make_target("beta1-adrenergic receptor", 8.8)], "mechanism": "Highly cardioselective beta1 antagonist; NO-mediated vasodilation", "selectivity": "beta1 > beta2 (~50-fold, highest selectivity)"},
        "l2_pk": {"bioavailability": 85, "half_life_h": 12.0, "vd_l_per_kg": 10.0, "metabolism": "Hepatic CYP2D6 (extensive polymorphic metabolism)", "renal_excretion_pct": 40, "special": "NO-mediated vasodilation (unlike other betaBs); L-arginine/NO pathway"}
    },

    # --- Diuretics ---
    {
        "id": "furosemide",
        "class": "Antihypertensive", "name": "Furosemide",
        "l1_binding": {"targets": [make_target("NKCC2", 6.8)], "mechanism": "Loop diuretic; blocks Na⁺-K⁺-2Cl⁻ cotransporter in TALH", "selectivity": "NKCC2 > NKCC1"},
        "l2_pk": {"bioavailability": 60, "half_life_h": 2.0, "vd_l_per_kg": 0.15, "metabolism": "Minimal hepatic glucuronidation", "renal_excretion_pct": 65, "special": "Short t½; natriuretic effect outlasts serum levels; ototoxic at high doses"}
    },
    {
        "id": "spironolactone",
        "class": "Antihypertensive", "name": "Spironolactone",
        "l1_binding": {"targets": [make_target("mineralocorticoid receptor", 8.2)], "mechanism": "Competitive MR antagonist; potassium-sparing diuretic", "selectivity": "MR > AR,PR,GR (weak antiandrogen)"},
        "l2_pk": {"bioavailability": 70, "half_life_h": 1.5, "vd_l_per_kg": 0.9, "metabolism": "Hepatic (active metabolites: 7alpha-thiomethylspironolactone, canrenone)", "renal_excretion_pct": 30, "special": "Active metabolites carry longer t½ (canrenone ~16h); gynecomastia risk; hyperkalemia"}
    },
    {
        "id": "indapamide",
        "class": "Antihypertensive", "name": "Indapamide",
        "l1_binding": {"targets": [make_target("NCC", 6.5)], "mechanism": "Thiazide-like diuretic; blocks Na⁺-Cl⁻ cotransporter in DCT", "selectivity": "NCC-selective"},
        "l2_pk": {"bioavailability": 95, "half_life_h": 17.0, "vd_l_per_kg": 25.0, "metabolism": "Hepatic (extensive)", "renal_excretion_pct": 60, "special": "Lipophilic; high Vd; extrarenal vasodilatory effect; longer t½ than HCTZ"}
    },

    # --- Alpha blockers ---
    {
        "id": "doxazosin",
        "class": "Antihypertensive", "name": "Doxazosin",
        "l1_binding": {"targets": [make_target("alpha1-adrenergic receptor", 8.5)], "mechanism": "Selective alpha1 antagonist; vasodilation via alpha1b subtype blockade", "selectivity": "alpha1 > alpha2 (~100-fold)"},
        "l2_pk": {"bioavailability": 65, "half_life_h": 22.0, "vd_l_per_kg": 1.0, "metabolism": "Hepatic CYP3A4 (O-demethylation)", "renal_excretion_pct": 65, "special": "Long t½ (22h); first-dose syncope risk; ALSO used for BPH"}
    },
    {
        "id": "terazosin",
        "class": "Antihypertensive", "name": "Terazosin",
        "l1_binding": {"targets": [make_target("alpha1-adrenergic receptor", 8.0)], "mechanism": "Selective alpha1 antagonist", "selectivity": "alpha1 > alpha2"},
        "l2_pk": {"bioavailability": 90, "half_life_h": 12.0, "vd_l_per_kg": 0.8, "metabolism": "Minimal hepatic", "renal_excretion_pct": 40, "special": "Also BPH indication; first-dose syncope; no longer first-line for HTN (ALLHAT)"}
    },

    # --- Central/Other ---
    {
        "id": "clonidine",
        "class": "Antihypertensive", "name": "Clonidine",
        "l1_binding": {"targets": [make_target("alpha2-adrenergic receptor", 7.5)], "mechanism": "Central alpha2 agonist; reduces sympathetic outflow from medulla", "selectivity": "alpha2 > alpha1 (~200:1)"},
        "l2_pk": {"bioavailability": 90, "half_life_h": 12.0, "vd_l_per_kg": 2.0, "metabolism": "Hepatic (50%)", "renal_excretion_pct": 50, "special": "Rebound hypertension on abrupt cessation; transdermal patch available; sedation common"}
    },
    {
        "id": "hydralazine",
        "class": "Antihypertensive", "name": "Hydralazine",
        "l1_binding": {"targets": [make_target("smooth muscle NO pathway", 5.5)], "mechanism": "Direct vasodilator; NO-mediated cGMP activation", "selectivity": "Arteriolar > venous"},
        "l2_pk": {"bioavailability": 35, "half_life_h": 3.0, "vd_l_per_kg": 1.5, "metabolism": "Hepatic N-acetylation (polymorphic: slow/fast acetylators)", "renal_excretion_pct": 15, "special": "Reflex tachycardia; drug-induced lupus (slow acetylators); typically combo with BB + diuretic"}
    },
    {
        "id": "methyldopa",
        "class": "Antihypertensive", "name": "Methyldopa",
        "l1_binding": {"targets": [make_target("alpha2-adrenergic receptor", 6.5)], "mechanism": "Central alpha2 agonist; converted to alpha-methylnorepinephrine; stimulates central alpha2 receptors reducing SNS outflow", "selectivity": "alpha2 > alpha1, central (prodrug)"},
        "l2_pk": {"bioavailability": 45, "half_life_h": 2.0, "vd_l_per_kg": 0.4, "metabolism": "Hepatic O-methylation + renal elimination of metabolites", "renal_excretion_pct": 70, "special": "Preferred for pregnancy-induced hypertension (safety record); positive Coombs test ~20%; sedating"}
    },
]

# ============================================================
# DIABETES DRUG DEFINITIONS
# ============================================================

DIABETES = [
    # --- SGLT2 inhibitors ---
    {
        "id": "canagliflozin",
        "class": "Diabetes", "name": "Canagliflozin",
        "l1_binding": {"targets": [make_target("SGLT2", 8.0)], "mechanism": "SGLT2 inhibitor; blocks renal glucose reabsorption in proximal tubule", "selectivity": "SGLT2 > SGLT1 (~250-fold)"},
        "l2_pk": {"bioavailability": 65, "half_life_h": 13.0, "vd_l_per_kg": 1.0, "metabolism": "Hepatic O-glucuronidation (UGT1A9, UGT2B4)", "renal_excretion_pct": 30, "special": "Weak SGLT1 inhibition in gut; CREDENCE trial renal benefit; amputation signal (CANVAS)"}
    },
    {
        "id": "ertugliflozin",
        "class": "Diabetes", "name": "Ertugliflozin",
        "l1_binding": {"targets": [make_target("SGLT2", 8.2)], "mechanism": "SGLT2 inhibitor", "selectivity": "SGLT2 > SGLT1 (>2,000-fold)"},
        "l2_pk": {"bioavailability": 70, "half_life_h": 16.0, "vd_l_per_kg": 0.9, "metabolism": "Hepatic O-glucuronidation (UGT1A9, UGT2B7)", "renal_excretion_pct": 50, "special": "High SGLT2 selectivity; VERTIS CV trial; no significant SGLT1 activity"}
    },

    # --- GLP-1 RAs ---
    {
        "id": "liraglutide",
        "class": "Diabetes", "name": "Liraglutide",
        "l1_binding": {"targets": [make_target("GLP-1 receptor", 8.5)], "mechanism": "GLP-1 receptor agonist (97% sequence homology to human GLP-1)", "selectivity": "GLP-1R selective"},
        "l2_pk": {"bioavailability": 55, "half_life_h": 13.0, "vd_l_per_kg": 0.05, "metabolism": "Proteolytic degradation (DPP-4 resistant via fatty acid)", "renal_excretion_pct": 5, "special": "Once-daily SC; LEADER trial CV benefit; 4.3% weight loss; also approved for obesity"}
    },
    {
        "id": "dulaglutide",
        "class": "Diabetes", "name": "Dulaglutide",
        "l1_binding": {"targets": [make_target("GLP-1 receptor", 8.0)], "mechanism": "GLP-1 receptor agonist (Fc-fusion protein, once-weekly)", "selectivity": "GLP-1R selective"},
        "l2_pk": {"bioavailability": 50, "half_life_h": 120.0, "vd_l_per_kg": 0.1, "metabolism": "Proteolytic degradation", "renal_excretion_pct": 1, "special": "Once-weekly SC; REWIND trial CV benefit; Fc fusion extends t½ to 5 days; 3-4lb weight loss"}
    },
    {
        "id": "exenatide",
        "class": "Diabetes", "name": "Exenatide",
        "l1_binding": {"targets": [make_target("GLP-1 receptor", 8.0)], "mechanism": "GLP-1 receptor agonist (synthetic exendin-4 from Gila monster)", "selectivity": "GLP-1R selective"},
        "l2_pk": {"bioavailability": 65, "half_life_h": 2.5, "vd_l_per_kg": 0.1, "metabolism": "Renal proteolysis + glomerular filtration", "renal_excretion_pct": 90, "special": "First GLP-1 RA; BID for immediate-release, once-weekly for ER; EXSCEL CV neutral; nausea common"}
    },

    # --- DPP-4 inhibitors ---
    {
        "id": "sitagliptin",
        "class": "Diabetes", "name": "Sitagliptin",
        "l1_binding": {"targets": [make_target("DPP-4", 8.5)], "mechanism": "DPP-4 inhibitor; increases endogenous GLP-1 and GIP half-life", "selectivity": "DPP-4 > DPP-8/9 (>2,600-fold)"},
        "l2_pk": {"bioavailability": 87, "half_life_h": 12.0, "vd_l_per_kg": 1.5, "metabolism": "Minimal hepatic (<20%)", "renal_excretion_pct": 85, "special": "First DPP-4i; renal dose adjustment needed; TECOS CV safety; weight-neutral"}
    },
    {
        "id": "saxagliptin",
        "class": "Diabetes", "name": "Saxagliptin",
        "l1_binding": {"targets": [make_target("DPP-4", 8.0)], "mechanism": "DPP-4 inhibitor", "selectivity": "DPP-4 > DPP-8/9 (>10-fold)"},
        "l2_pk": {"bioavailability": 67, "half_life_h": 2.5, "vd_l_per_kg": 0.5, "metabolism": "Hepatic CYP3A4/CYP3A5 → active metabolite (5-hydroxy saxagliptin)", "renal_excretion_pct": 75, "special": "Active metabolite (half potency, same t½); SAVOR-TIMI 53 HF hospitalization signal; renal dose adjustment"}
    },
    {
        "id": "linagliptin",
        "class": "Diabetes", "name": "Linagliptin",
        "l1_binding": {"targets": [make_target("DPP-4", 9.0)], "mechanism": "DPP-4 inhibitor", "selectivity": "DPP-4 > DPP-8/9 (>10,000-fold)"},
        "l2_pk": {"bioavailability": 30, "half_life_h": 12.0, "vd_l_per_kg": 10.0, "metabolism": "Minimal (unchanged parent ~90%)", "renal_excretion_pct": 5, "special": "No renal dose adjustment (biliary excretion); highest DPP-4 binding affinity; CARMELINA CV safety"}
    },
    {
        "id": "alogliptin",
        "class": "Diabetes", "name": "Alogliptin",
        "l1_binding": {"targets": [make_target("DPP-4", 8.8)], "mechanism": "DPP-4 inhibitor", "selectivity": "DPP-4 > DPP-8/9 (>10,000-fold)"},
        "l2_pk": {"bioavailability": 70, "half_life_h": 21.0, "vd_l_per_kg": 0.8, "metabolism": "Minimal hepatic (<10%)", "renal_excretion_pct": 75, "special": "Longest t½ among gliptins; renal dose adjustment; EXAMINE CV safety"}
    },
    {
        "id": "vildagliptin",
        "class": "Diabetes", "name": "Vildagliptin",
        "l1_binding": {"targets": [make_target("DPP-4", 8.2)], "mechanism": "DPP-4 inhibitor (cyanopyrrolidine class)", "selectivity": "DPP-4 > DPP-8/9"},
        "l2_pk": {"bioavailability": 85, "half_life_h": 2.5, "vd_l_per_kg": 0.7, "metabolism": "Hepatic hydrolysis (cyano group → inactive metabolite)", "renal_excretion_pct": 85, "special": "BID dosing (short t½); liver enzyme monitoring required; not available in US"}
    },

    # --- TZDs ---
    {
        "id": "pioglitazone",
        "class": "Diabetes", "name": "Pioglitazone",
        "l1_binding": {"targets": [make_target("PPARgamma", 7.5)], "mechanism": "PPARgamma agonist; increases insulin sensitivity in adipose, muscle, liver", "selectivity": "PPARgamma > PPARalpha (weak partial agonist)"},
        "l2_pk": {"bioavailability": 83, "half_life_h": 8.0, "vd_l_per_kg": 0.3, "metabolism": "Hepatic CYP2C8, CYP3A4 (active metabolites)", "renal_excretion_pct": 20, "special": "PROactive trial CV benefit?; weight gain (2-4kg); edema; bladder cancer concern; no renal dose adjustment"}
    },
    {
        "id": "rosiglitazone",
        "class": "Diabetes", "name": "Rosiglitazone",
        "l1_binding": {"targets": [make_target("PPARgamma", 8.2)], "mechanism": "PPARgamma agonist (high potency)", "selectivity": "PPARgamma-selective"},
        "l2_pk": {"bioavailability": 99, "half_life_h": 4.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic CYP2C8 (N-demethylation + hydroxylation)", "renal_excretion_pct": 25, "special": "RECORD trial; controversially associated with MI risk; restricted access in many markets; withdrawn in EU"}
    },

    # --- Sulfonylureas ---
    {
        "id": "glipizide",
        "class": "Diabetes", "name": "Glipizide",
        "l1_binding": {"targets": [make_target("SUR1", 7.2)], "mechanism": "SU receptor (SUR1) on beta-cell K_ATP channel; stimulates insulin secretion", "selectivity": "SUR1 > SUR2"},
        "l2_pk": {"bioavailability": 95, "half_life_h": 3.5, "vd_l_per_kg": 0.2, "metabolism": "Hepatic CYP2C9 (hydroxylation → inactive metabolites)", "renal_excretion_pct": 80, "special": "Short t½; meal-time dosing; hypoglycemia risk (dose-dependent); weight gain 2-3kg"}
    },
    {
        "id": "glimepiride",
        "class": "Diabetes", "name": "Glimepiride",
        "l1_binding": {"targets": [make_target("SUR1", 7.8)], "mechanism": "SU receptor (SUR1) on beta-cell K_ATP channel; insulin secretagogue", "selectivity": "SUR1 > SUR2A > SUR2B"},
        "l2_pk": {"bioavailability": 100, "half_life_h": 9.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic CYP2C9 (oxidation → M1 metabolite active)", "renal_excretion_pct": 60, "special": "Once-daily; M1 metabolite has ~1/3 potency; extra-pancreatic effects?; lower hypoglycemia risk than glyburide"}
    },
    {
        "id": "glyburide",
        "class": "Diabetes", "name": "Glyburide",
        "l1_binding": {"targets": [make_target("SUR1", 8.0)], "mechanism": "SU receptor (SUR1) on beta-cell K_ATP channel; potent insulin secretagogue", "selectivity": "SUR1-selective"},
        "l2_pk": {"bioavailability": 90, "half_life_h": 10.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic CYP2C9 (hydroxylation → inactive metabolites)", "renal_excretion_pct": 50, "special": "Highest hypoglycemia risk among SUs (long t½ + active hepatic metabolites); contraindicated in renal impairment; ADOPT trial fastest monotherapy failure"}
    },
    {
        "id": "gliclazide",
        "class": "Diabetes", "name": "Gliclazide",
        "l1_binding": {"targets": [make_target("SUR1", 7.0)], "mechanism": "SU receptor (SUR1) on beta-cell K_ATP channel; insulin secretagogue; antioxidant", "selectivity": "SUR1 > SUR2 (less vascular binding)"},
        "l2_pk": {"bioavailability": 80, "half_life_h": 12.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic CYP2C9 (multiple metabolites)", "renal_excretion_pct": 70, "special": "Modified-release (MR) formulation; ADVANCE trial microvascular benefit; antioxidant properties; preferred SU in some guidelines"}
    },

    # --- Insulins ---
    {
        "id": "insulin-aspart",
        "class": "Diabetes", "name": "Insulin Aspart",
        "l1_binding": {"targets": [make_target("insulin receptor", 8.5)], "mechanism": "Rapid-acting insulin analog; AspB28 substitution reduces hexamer formation → faster absorption", "selectivity": "IR > IGF-1R"},
        "l2_pk": {"bioavailability": 80, "half_life_h": 1.0, "vd_l_per_kg": 0.2, "metabolism": "Proteolytic degradation in liver, kidney, muscle", "renal_excretion_pct": 30, "special": "Onset 5-15min; duration 3-5h; faster than regular insulin; also available as faster aspart"}
    },
    {
        "id": "insulin-lispro",
        "class": "Diabetes", "name": "Insulin Lispro",
        "l1_binding": {"targets": [make_target("insulin receptor", 8.5)], "mechanism": "Rapid-acting insulin analog; LysB28ProB29 → reduced dimerization", "selectivity": "IR > IGF-1R"},
        "l2_pk": {"bioavailability": 80, "half_life_h": 1.0, "vd_l_per_kg": 0.2, "metabolism": "Proteolytic degradation", "renal_excretion_pct": 30, "special": "First rapid-acting analog (1996); onset 5-15min; duration 4-6h; mealtime flexibility"}
    },
    {
        "id": "insulin-degludec",
        "class": "Diabetes", "name": "Insulin Degludec",
        "l1_binding": {"targets": [make_target("insulin receptor", 8.0)], "mechanism": "Ultra-long basal insulin analog; multihexamer depot formation after SC injection; slow monomer release", "selectivity": "IR > IGF-1R"},
        "l2_pk": {"bioavailability": 70, "half_life_h": 25.0, "vd_l_per_kg": 0.5, "metabolism": "Proteolytic degradation → inactive metabolites", "renal_excretion_pct": 5, "special": "Ultra-long t½ (~25h); flat PK profile; duration >42h; flexible dosing (8-40h window); lower hypoglycemia vs glargine"}
    },

    # --- Others ---
    {
        "id": "acarbose",
        "class": "Diabetes", "name": "Acarbose",
        "l1_binding": {"targets": [make_target("alpha-glucosidase", 6.5)], "mechanism": "alpha-glucosidase inhibitor; delays carbohydrate digestion in small intestine", "selectivity": "Intestinal alpha-glucosidases > pancreatic alpha-amylase"},
        "l2_pk": {"bioavailability": 2, "half_life_h": 2.0, "vd_l_per_kg": 0.1, "metabolism": "Intestinal metabolism by gut bacteria", "renal_excretion_pct": 50, "special": "Minimal systemic absorption (<2%); works locally in gut; flatulence common; postprandial glucose reduction"}
    },
    {
        "id": "repaglinide",
        "class": "Diabetes", "name": "Repaglinide",
        "l1_binding": {"targets": [make_target("SUR1", 7.5)], "mechanism": "Meglitinide; closes beta-cell K_ATP channel at different binding site than SU; rapid insulin secretion", "selectivity": "SUR1-selective"},
        "l2_pk": {"bioavailability": 56, "half_life_h": 1.0, "vd_l_per_kg": 0.2, "metabolism": "Hepatic CYP2C8, CYP3A4 (glucuronidation)", "renal_excretion_pct": 10, "special": "Ultra-short t½ (1h); mealtime dosing (prandial glucose regulator); gemfibrozil interaction (CYP2C8)"}
    },
    {
        "id": "pramlintide",
        "class": "Diabetes", "name": "Pramlintide",
        "l1_binding": {"targets": [make_target("amylin receptor", 7.0)], "mechanism": "Synthetic amylin analog; slows gastric emptying + suppresses glucagon", "selectivity": "AmylinR (calcitonin receptor + RAMP)"},
        "l2_pk": {"bioavailability": 40, "half_life_h": 0.5, "vd_l_per_kg": 0.1, "metabolism": "Renal proteolysis", "renal_excretion_pct": 40, "special": "Only non-GLP-1 injectable; requires TID dosing; nausea common; weight loss; adjunct to mealtime insulin"}
    },
]

def make_drug_entry(d, existing_ids):
    """Create a full drugs.json entry from a drug definition dict."""
    entry = {
        "id": d["id"],
        "class": d["class"],
        "name": d["name"],
        "l1_binding": d.get("l1_binding", {}),
        "l2_pk": d.get("l2_pk", {}),
        "l3_systems": {},
        "l4_clinical": {}
    }
    return entry

def main():
    import shutil
    apply = "--apply" in sys.argv

    # Load current drugs.json
    with open(DRUGS_JSON) as f:
        data = json.load(f)
    existing_ids = {d["id"] for d in data["drugs"]}

    all_new = []
    all_new += ANTIHYPERTENSIVES
    all_new += DIABETES

    to_add = [d for d in all_new if d["id"] not in existing_ids]
    already_have = [d["id"] for d in all_new if d["id"] in existing_ids]

    print(f"=== E3+E4 Comprehensive Expansion ===\n")
    print(f"Existing drugs.json: {len(data['drugs'])} drugs")
    print(f"Definitions: {len(ANTIHYPERTENSIVES)} antihypertensives + {len(DIABETES)} diabetes = {len(all_new)}")
    print(f"Already in drugs.json: {len(already_have)} ({', '.join(already_have)})")
    print(f"New to add: {len(to_add)}\n")

    if not to_add:
        print("Nothing to add.")
        return

    # Group by class
    from collections import Counter
    class_counts = Counter(d["class"] for d in to_add)
    for cls, cnt in class_counts.items():
        print(f"  {cls}: {cnt} new drugs")

    # Dry-run: show the drugs
    print("\n--- New Drug Entries ---")
    for d in to_add:
        targets = [t["name"] for t in d.get("l1_binding", {}).get("targets", [])]
        pk = d.get("l2_pk", {})
        hl = pk.get("half_life_h", "?")
        print(("  %-25s class=%-20s targets=%-40s t1/2=%sh" % (d['id'], d['class'], ', '.join(targets), hl)))

    if not apply:
        print(f"\n{'='*60}")
        print(f"DRY RUN — pass --apply to actually modify drugs.json")
        print(f"{'='*60}")
        return

    # APPLY: add new entries to drugs.json
    for d in to_add:
        entry = make_drug_entry(d, existing_ids)
        data["drugs"].append(entry)
        existing_ids.add(d["id"])

    # Write backup
    backup_dir = Path(__file__).resolve().parent / "l3_output" / "_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"drugs_{ts}.json"
    shutil.copy2(DRUGS_JSON, backup_path)
    print(f"\nBackup: {backup_path}")

    with open(DRUGS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated:  {DRUGS_JSON}")
    print(f"Now has:  {len(data['drugs'])} drugs")

    print(f"\n=== Done ===")

if __name__ == "__main__":
    main()
