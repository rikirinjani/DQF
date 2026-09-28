# Antihypertensive — Class Comparison

> The antihypertensive class spans 8 mechanisms: ACE inhibitors, ARBs, dihydropyridine and non-dihydropyridine CCBs, thiazide/thiazide-like and loop diuretics, beta-blockers, alpha-blockers, and central alpha-2 agonists. L3 dimensions: bp_reduction (benefit), renal_protection (benefit), metabolic_effect (direction-agnostic), electrolyte_risk (risk), ddi_risk (risk), heart_rate_effect (direction-agnostic string).

L3 scores below are the current `api/drugs.json` values (post-N1 where applied). Per-drug detail: see `<drug>.md` in this directory.

## L3 Score Matrix

| Drug | bp_reduction | ddi_risk | electrolyte_risk | metabolic_effect | renal_protection | heart_rate_effect |
|---|---|---|---|---|---|---|
| **amlodipine** | 3 | 2 | 2 | 2 | 2 | bradycardia |
| **atenolol** | 3 | 2 | 2 | 3 | 2 | bradycardia |
| **bisoprolol** | 3 | 2 | 1 | 1 | 2 | bradycardia |
| **candesartan** | 3 | 2 | 2 | 3 | 3 | none |
| **captopril** | 3 | 3 | 3 | 3 | 3 | none |
| **carvedilol** | 3 | 3 | 1 | 3 | 2 | bradycardia |
| **chlorthalidone** | 3 | 1 | 3 | 2 | 2 | none |
| **clonidine** | 3 | 2 | 1 | 3 | 2 | bradycardia |
| **diltiazem** | 3 | 3 | 2 | 3 | 3 | bradycardia |
| **doxazosin** | 3 | 1 | 1 | 2 | 3 | none |
| **enalapril** | 3 | 2 | 3 | 3 | 3 | bradycardia |
| **felodipine** | 3 | 3 | 3 | 2 | 3 | tachycardia |
| **furosemide** | 3 | 2 | 3 | 3 | 3 | tachycardia |
| **hydralazine** | 3 | 2 | 2 | 2 | 2 | tachycardia |
| **hydrochlorothiazide** | 3 | 2 | 3 | 2 | 3 | none |
| **indapamide** | 3 | 2 | 3 | 3 | 2 | none |
| **irbesartan** | 3 | 2 | 1 | 3 | 3 | none |
| **lisinopril** | 3 | 1 | 1 | 1 | 3 | none |
| **losartan** | 3 | 2 | 3 | 3 | 2 | none |
| **methyldopa** | 3 | 1 | 1 | 1 | 2 | none |
| **metoprolol** | 3 | 3 | 1 | 2 | 2 | bradycardia |
| **nebivolol** | 3 | 3 | 2 | 3 | 1 | bradycardia |
| **nifedipine** | 3 | 3 | 3 | 3 | 3 | tachycardia |
| **olmesartan** | 3 | 1 | 1 | 3 | 3 | none |
| **perindopril** | 3 | 3 | 3 | 3 | 3 | none |
| **propranolol** | 3 | 1 | 3 | 2 | 1 | bradycardia |
| **ramipril** | 3 | 2 | 1 | 3 | 3 | tachycardia |
| **spironolactone** | 3 | 2 | 3 | 3 | 3 | none |
| **telmisartan** | 3 | 2 | 2 | 3 | 3 | none |
| **terazosin** | 3 | 3 | 3 | 3 | 1 | none |
| **trandolapril** | 3 | 1 | 3 | 3 | 3 | none |
| **valsartan** | 3 | 1 | 1 | 3 | 3 | none |
| **verapamil** | 3 | 2 | 1 | 3 | 3 | bradycardia |

## L4 Snapshot

| Drug | Key efficacy field | Value |
|---|---|---|
| **amlodipine** | nnt_bp_control | 3 |
| **atenolol** | nnt_bp_control | 4 |
| **bisoprolol** | nnt_bp_control | 4 |
| **candesartan** | nnt_bp_control | 4 |
| **captopril** | nnt_bp_control | 3 |
| **carvedilol** | nnt_bp_control | 4 |
| **chlorthalidone** | nnt_bp_control | 3 |
| **clonidine** | nnt_bp_control | 4 |
| **diltiazem** | nnt_bp_control | 3 |
| **doxazosin** | nnt_bp_control | 4 |
| **enalapril** | nnt_bp_control | 3 |
| **felodipine** | nnt_bp_control | 3 |
| **furosemide** | nnt_bp_control | 5 |
| **hydralazine** | nnt_bp_control | 5 |
| **hydrochlorothiazide** | nnt_bp_control | 3 |
| **indapamide** | nnt_bp_control | 3 |
| **irbesartan** | nnt_bp_control | 4 |
| **lisinopril** | nnt_bp_control | 3 |
| **losartan** | nnt_bp_control | 4 |
| **methyldopa** | nnt_bp_control | 4 |
| **metoprolol** | nnt_bp_control | 4 |
| **nebivolol** | nnt_bp_control | 4 |
| **nifedipine** | nnt_bp_control | 3 |
| **olmesartan** | nnt_bp_control | 4 |
| **perindopril** | nnt_bp_control | 3 |
| **propranolol** | nnt_bp_control | 4 |
| **ramipril** | nnt_bp_control | 3 |
| **spironolactone** | nnt_bp_control | 3 |
| **telmisartan** | nnt_bp_control | 4 |
| **terazosin** | nnt_bp_control | 4 |
| **trandolapril** | nnt_bp_control | 3 |
| **valsartan** | nnt_bp_control | 4 |
| **verapamil** | nnt_bp_control | 3 |

