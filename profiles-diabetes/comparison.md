# Diabetes — Class Comparison

> The diabetes class spans 6 mechanisms: biguanide (metformin), SU/glinide secretagogues, DPP-4 inhibitors, GLP-1 receptor agonists, SGLT2 inhibitors, insulins, and a thiazolidinedione and amylin analog. L3 dimensions: a1c_reduction (benefit), weight_effect (direction-agnostic), cv_outcome_benefit (benefit), renal_benefit (benefit), gi_tolerability (benefit), ddi_risk (risk), hypoglycemia_risk (risk).

L3 scores below are the current `api/drugs.json` values (post-N1 where applied). Per-drug detail: see `<drug>.md` in this directory.

## L3 Score Matrix

| Drug | a1c_reduction | cv_outcome_benefit | ddi_risk | gi_tolerability | hypoglycemia_risk | renal_benefit | weight_effect | heart_rate_effect |
|---|---|---|---|---|---|---|---|---|
| **acarbose** | 3 | 3 | 2 | 3 | 2 | 3 | 3 | — |
| **alogliptin** | 3 | 2 | 1 | 3 | 3 | 3 | 2 | — |
| **canagliflozin** | 3 | 3 | 1 | 3 | 3 | 3 | 3 | — |
| **dapagliflozin** | 3 | 3 | 1 | 3 | 2 | 3 | 3 | — |
| **dulaglutide** | 3 | 3 | 1 | 3 | 2 | 3 | 3 | — |
| **empagliflozin** | 3 | 3 | 2 | 3 | 3 | 3 | 3 | — |
| **ertugliflozin** | 3 | 3 | 1 | 3 | 3 | 3 | 3 | — |
| **exenatide** | 3 | 3 | 1 | 3 | 3 | 2 | 3 | — |
| **gliclazide** | 3 | 2 | 2 | 3 | 3 | 3 | 2 | — |
| **glimepiride** | 3 | 3 | 1 | 3 | 3 | 2 | 3 | — |
| **glipizide** | 3 | 3 | 1 | 3 | 3 | 3 | 2 | — |
| **glyburide** | 3 | 2 | 2 | 3 | 3 | 2 | 2 | — |
| **insulin-aspart** | 3 | 1 | 1 | 3 | 2 | 1 | 2 | — |
| **insulin-degludec** | 3 | 1 | 1 | 3 | 3 | 1 | 2 | — |
| **insulin-glargine** | 3 | 1 | 1 | 3 | 3 | 1 | 3 | — |
| **insulin-lispro** | 3 | 1 | 1 | 3 | 3 | 1 | 1 | — |
| **linagliptin** | 3 | 3 | 2 | 3 | 3 | 3 | 2 | — |
| **liraglutide** | 3 | 3 | 1 | 3 | 3 | 3 | 3 | — |
| **metformin** | 3 | 3 | 2 | 3 | 3 | 3 | 2 | — |
| **pioglitazone** | 3 | 3 | 2 | 3 | 2 | 3 | 2 | — |
| **pramlintide** | 3 | 2 | 1 | 3 | 3 | 2 | 3 | — |
| **repaglinide** | 3 | 2 | 2 | 3 | 3 | 2 | 2 | — |
| **rosiglitazone** | 3 | 2 | 2 | 3 | 1 | 2 | 3 | — |
| **saxagliptin** | 3 | 3 | 3 | 3 | 2 | 3 | 2 | — |
| **semaglutide** | 3 | 3 | 1 | 3 | 2 | 3 | 3 | — |
| **sitagliptin** | 3 | 2 | 1 | 3 | 3 | 3 | 2 | — |
| **tirzepatide** | 3 | 3 | 1 | 3 | 3 | 2 | 3 | — |
| **vildagliptin** | 3 | 1 | 1 | 3 | 2 | 3 | 2 | — |

## L4 Snapshot

| Drug | Key efficacy field | Value |
|---|---|---|
| **acarbose** | a1c_reduction (stored under `nnt_bp_control`) | 0.6 |
| **alogliptin** | a1c_reduction (stored under `nnt_bp_control`) | 0.6 |
| **canagliflozin** | a1c_reduction (stored under `nnt_bp_control`) | 0.8 |
| **dapagliflozin** | a1c_reduction (stored under `nnt_bp_control`) | 0.7 |
| **dulaglutide** | a1c_reduction (stored under `nnt_bp_control`) | 1.2 |
| **empagliflozin** | a1c_reduction (stored under `nnt_bp_control`) | 0.8 |
| **ertugliflozin** | a1c_reduction (stored under `nnt_bp_control`) | 0.7 |
| **exenatide** | a1c_reduction (stored under `nnt_bp_control`) | 0.9 |
| **gliclazide** | a1c_reduction (stored under `nnt_bp_control`) | 1.1 |
| **glimepiride** | a1c_reduction (stored under `nnt_bp_control`) | 1.2 |
| **glipizide** | a1c_reduction (stored under `nnt_bp_control`) | 1.2 |
| **glyburide** | a1c_reduction (stored under `nnt_bp_control`) | 1.3 |
| **insulin-aspart** | a1c_reduction (stored under `nnt_bp_control`) | 1.3 |
| **insulin-degludec** | a1c_reduction (stored under `nnt_bp_control`) | 1.2 |
| **insulin-glargine** | a1c_reduction (stored under `nnt_bp_control`) | 1.2 |
| **insulin-lispro** | a1c_reduction (stored under `nnt_bp_control`) | 1.3 |
| **linagliptin** | a1c_reduction (stored under `nnt_bp_control`) | 0.6 |
| **liraglutide** | a1c_reduction (stored under `nnt_bp_control`) | 1.2 |
| **metformin** | a1c_reduction (stored under `nnt_bp_control`) | 1.5 |
| **pioglitazone** | a1c_reduction (stored under `nnt_bp_control`) | 0.9 |
| **pramlintide** | a1c_reduction (stored under `nnt_bp_control`) | 0.5 |
| **repaglinide** | a1c_reduction (stored under `nnt_bp_control`) | 0.9 |
| **rosiglitazone** | a1c_reduction (stored under `nnt_bp_control`) | 0.8 |
| **saxagliptin** | a1c_reduction (stored under `nnt_bp_control`) | 0.6 |
| **semaglutide** | a1c_reduction (stored under `nnt_bp_control`) | 1.5 |
| **sitagliptin** | a1c_reduction (stored under `nnt_bp_control`) | 0.6 |
| **tirzepatide** | a1c_reduction (stored under `nnt_bp_control`) | 2.1 |
| **vildagliptin** | a1c_reduction (stored under `nnt_bp_control`) | 0.6 |

