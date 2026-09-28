# Batch-5 Rescore Draft (N1) — proposal only, not applied

> Generated 2026-09-27 from `batch5_verdicts.json` (413 groups / 2573 sentences / 905 kept). **Decision 2026-09-28 (user-approved): 11 vetted changes applied to drugs.json — see `batch5_rescore_adjudication.json`; 25 questionable proposals demoted to open questions; 44 conflicts + 44 open questions untouched.**

## Rule

- `clean` (non-ddi): any strong -> 3, elif any moderate -> 2, else 1
- `clean` (ddi): `_score_risk` on the pk/pd-filtered sentences (R7 style)
- `kw`: `_score_risk` over the full pool — independent keyword signal
- **raise**: clean > current AND support >= 2 (1 supporting sentence -> open question)
- **drop**: clean < current AND kw < current (ddi with pk/pd present -> open question)
- **fill**: current is null AND support >= 2
- **locked**: 6 anticoagulants (excluded), 54 batch4_rescore cells, 62 ddi_rescore cells -> disagreements routed to conflicts

## Stats

- groups scanned: 413 (anticoagulant groups excluded: 0, locked groups: 116)
- **proposals: 36** (17 raises, 19 drops, 0 fills)
- holds (clean == current): 192
- open questions: 44
- conflicts with prior adjudication: 44

## Proposals (36)

| drug | dim | current | clean | kw | support | labels | new | rule | basis |
|---|---|---|---|---|---|---|---|---|---|
| sodium-alginate | raft_strength | 3 | 2 | 1 | 6 | moderate:6, none:1 | 2 | N-drop | [moderate] sodium alginate is a biocompatible, natural polymer with ph-sensitive gel-forming ability. (PMID PMID:17451926) |
| sodium-alginate | reflux_suppression | 3 | 2 | 1 | 1 | moderate:1, none:2 | 2 | N-drop | [moderate] the aims of the present study were to compare effects of sodium alginate and the antacid m (PMID PMID:16977507) |
| bisoprolol | renal_protection | 2 | 3 | 2 | 2 | moderate:2, none:2, strong:2 | 3 | N-raise | [strong] mean bisoprolol clearance (10.2 l/h) was 30 % lower than in healthy individuals and correl (PMID PMID:26996442) |
| clonidine | metabolic_effect | 2 | 3 | 2 | 2 | moderate:1, none:1, strong:2 | 3 | N-raise | [strong] however, when the clonidine was withdrawn, the glucose intolerance subsided. (PMID PMID:6279379) |
| diltiazem | electrolyte_risk | 2 | 3 | 2 | 2 | moderate:1, none:7, strong:2 | 3 | N-raise | [strong] the distribution of epidural fibrosis density, percentage of fibrosis, and distribution of (PMID PMID:31747760) |
| diltiazem | renal_protection | 2 | 3 | 2 | 3 | moderate:2, negative:1, none:4, strong:3 | 3 | N-raise | [strong] to determine if an intravenous infusion of diltiazem improves renal function through chang (PMID PMID:36354148) |
| felodipine | metabolic_effect | 2 | 3 | 2 | 3 | negative:1, none:1, strong:3 | 3 | N-raise | [strong] in response to acute felodipine administration, the significant diuresis and natriuresis o (PMID PMID:1693722) |
| furosemide | electrolyte_risk | 2 | 3 | 3 | 5 | moderate:2, none:2, strong:5 | 3 | N-raise | [strong] urinary spot sodium and urine output were measured at baseline, 2, and 6 h after 40 mg iv  (PMID PMID:41569687) |
| hydrochlorothiazide | renal_protection | 2 | 3 | 2 | 2 | moderate:2, negative:1, none:2, strong:2 | 3 | N-raise | [strong] hydrochlorothiazide and prevention of kidney-stone recurrence. (PMID PMID:36856614) |
| losartan | electrolyte_risk | 1 | 3 | 1 | 2 | none:3, strong:2 | 3 | N-raise | [strong] a double-blind, randomized study evaluating losartan potassium monotherapy or in combinati (PMID PMID:18328120) |
| nebivolol | metabolic_effect | 3 | 2 | 2 | 2 | moderate:2, none:3 | 2 | N-drop | [moderate] nebivolol is a beta-1 receptor blocker used to treat hypertension, heart failure, erectile (PMID PMID:37849071) |
| alogliptin | gi_tolerability | 3 | 2 | 2 | 1 | moderate:1, none:1 | 2 | N-drop | [moderate] other adverse events were reported in 1 subject each: dizziness (alogliptin 100 mg), synco (PMID PMID:18405789) |
| ertugliflozin | gi_tolerability | 3 | 1 | 2 | 0 | none:1 | 1 | N-drop | [none] as metformin is administered with meals because of its gastrointestinal side effects, the  (PMID PMID:30427588) |
| exenatide | cv_outcome_benefit | 2 | 3 | 2 | 2 | moderate:2, none:1, strong:2 | 3 | N-raise | [strong] long-term changes in cardiovascular risk markers during administration of exenatide twice  (PMID PMID:26338040) |
| gliclazide | weight_effect | 2 | 3 | None | 2 | moderate:1, none:3, strong:2 | 3 | N-raise | [strong] gliclazide lowered hba1c more than other oral insulinotropic agents, with a weighted mean  (PMID PMID:26361859) |
| glipizide | weight_effect | 2 | 3 | None | 2 | none:4, strong:2 | 3 | N-raise | [strong] sitagliptin and glipizide added to metformin provided similar degrees of glycemic efficacy (PMID PMID:21477878) |
| glyburide | gi_tolerability | 3 | 1 | 2 | 0 | none:1 | 1 | N-drop | [none] rosiglitazone was associated with more weight gain and edema than either metformin or glyb (PMID PMID:17145742) |
| insulin-glargine | cv_outcome_benefit | 2 | 1 | 1 | 0 | none:1 | 1 | N-drop | [none] we investigated cardiovascular outcomes by treatment group in participants randomly assign (PMID PMID:38344820) |
| insulin-glargine | renal_benefit | 2 | 1 | 1 | 0 | none:1 | 1 | N-drop | [none] analysis of patient characteristics and safety of insulin glargine u300 use in 21 359 pati (PMID PMID:39972199) |
| insulin-lispro | hypoglycemia_risk | 3 | 1 | 1 | 0 | none:1 | 1 | N-drop | [none] obese patients with t2dm treated with insulin lispro were able to achieve the same level o (PMID PMID:24325997) |
| liraglutide | hypoglycemia_risk | 3 | 1 | 2 | 0 | none:1 | 1 | N-drop | [none] the common adverse reactions of liraglutide are hypoglycemia and gastrointestinal reaction (PMID PMID:38357515) |
| liraglutide | weight_effect | 2 | 3 | None | 3 | moderate:5, none:4, strong:3 | 3 | N-raise | [strong] the mean hba1c and weight reductions were 12.3 mmol/mol (1.13%; p<0.001) and 3.8 kg (p<0.0 (PMID PMID:29527308) |
| pramlintide | cv_outcome_benefit | 2 | 3 | 2 | 4 | moderate:1, none:2, strong:4 | 3 | N-raise | [strong] cardiovascular safety of pramlintide was assessed using accepted regulatory medical defini (PMID PMID:28702246) |
| repaglinide | cv_outcome_benefit | 2 | 3 | 2 | 2 | none:2, strong:2 | 3 | N-raise | [strong] the study suggests that prolonged use of pioglitazone, repaglinide and alogliptin may sign (PMID PMID:41267359) |
| repaglinide | gi_tolerability | 3 | 1 | 2 | 0 | none:1 | 1 | N-drop | [none] repaglinide is considered a safe drug; adverse events are mild to moderate which includes  (PMID PMID:20387361) |
| saxagliptin | gi_tolerability | 3 | 1 | 1 | 0 | none:1 | 1 | N-drop | [none] adverse events and events of special interest (gastrointestinal adverse events, infections (PMID PMID:24376173) |
| sitagliptin | gi_tolerability | 3 | 1 | 2 | 0 | none:1 | 1 | N-drop | [none] incidence rates of specific adverse events were also generally similar between the two gro (PMID PMID:20412573) |
| tirzepatide | gi_tolerability | 3 | 2 | 2 | 1 | moderate:1, none:1 | 2 | N-drop | [moderate] while gastrointestinal adverse effects are common, hyponatremia induced by tirzepatide is  (PMID PMID:41179268) |
| vildagliptin | weight_effect | 2 | 3 | None | 3 | moderate:3, none:5, strong:3 | 3 | N-raise | [strong] weight was statistically significantly negatively associated with exenatide (wmd = -1.10,  (PMID PMID:20616619) |
| sucralfate | barrier_protection | 3 | 1 | 2 | 0 | none:1 | 1 | N-drop | [none] sucralfate, widely known as a mucoprotective agent for gastroduodenal ulcers, has recently (PMID PMID:40872708) |
| ibuprofen | gi_risk | 3 | 1 | 2 | 0 | none:1 | 1 | N-drop | [none] case-control studies of upper gi bleeding found odds ratios of the association with ibupro (PMID PMID:8953831) |
| meloxicam | gi_risk | 3 | 2 | 2 | 1 | moderate:1, negative:1, none:2 | 2 | N-drop | [moderate] it was concluded that unlike nonselective nsaids, meloxicam's blockade of txa2 formation ( (PMID PMID:12162470) |
| meloxicam | renal_risk | 2 | 3 | 2 | 2 | moderate:3, negative:2, none:1, strong:2 | 3 | N-raise | [strong] neither hepatic insufficiency nor moderate renal dysfunction have any relevant effects on  (PMID PMID:8630630) |
| piroxicam | renal_risk | 2 | 3 | 2 | 2 | moderate:4, none:4, strong:2 | 3 | N-raise | [strong] renal effects of ibuprofen, piroxicam, and sulindac in patients with asymptomatic renal fa (PMID PMID:2183665) |
| pitavastatin | myopathy_risk | 3 | 1 | 2 | 0 | none:1 | 1 | N-drop | [none] similarly, pitavastatin has better myopathy profile when compared to other statins. (PMID PMID:28952474) |
| rosuvastatin | myopathy_risk | 3 | 2 | 2 | 1 | moderate:1, none:1 | 2 | N-drop | [moderate] recently, a group of genes and molecular pathways has been described to participate in sta (PMID PMID:36613689) |

## Conflicts with prior adjudication (44)

| drug | dim | current | clean | kw | support | labels |
|---|---|---|---|---|---|---|
| aluminum-magnesium-hydroxide | neutralization_capacity | 2 | 3 | 1 | 1 | moderate:1, none:1, strong:1 |
| calcium-carbonate | renal_toxicity_risk | 1 | 3 | 1 | 2 | moderate:1, none:1, strong:2 |
| amlodipine | renal_protection | 2 | 1 | 2 | 0 | none:1 |
| atenolol | ddi_risk | 2 | 1 | 2 | 0 | none:2 |
| atenolol | renal_protection | 2 | 3 | 2 | 3 | moderate:1, none:1, strong:3 |
| candesartan | electrolyte_risk | 2 | 1 | 2 | 0 | none:1 |
| captopril | ddi_risk | 3 | 2 | 3 | 2 | none:7, pd:2 |
| chlorthalidone | ddi_risk | 1 | 3 | 3 | 1 | none:6, pd:1 |
| chlorthalidone | renal_protection | 2 | 3 | 2 | 2 | moderate:1, none:1, strong:2 |
| clonidine | renal_protection | 2 | 3 | 2 | 6 | none:4, strong:6 |
| diltiazem | ddi_risk | 3 | 2 | 3 | 4 | none:6, pd:3, pk:1 |
| felodipine | ddi_risk | 3 | 2 | 2 | 2 | none:6, pd:1, pk:1 |
| hydrochlorothiazide | ddi_risk | 2 | 3 | 3 | 2 | none:9, pd:1, pk:1 |
| hydrochlorothiazide | metabolic_effect | 2 | 3 | 3 | 3 | moderate:1, none:1, strong:3 |
| indapamide | renal_protection | 2 | 3 | 2 | 1 | none:1, strong:1 |
| irbesartan | ddi_risk | 2 | 1 | 2 | 1 | none:4, pk:1 |
| lisinopril | ddi_risk | 1 | 2 | 3 | 1 | none:9, pd:1 |
| losartan | renal_protection | 2 | 3 | 2 | 2 | moderate:2, none:1, strong:2 |
| metoprolol | ddi_risk | 3 | 2 | 3 | 5 | none:7, pd:2, pk:3 |
| metoprolol | metabolic_effect | 2 | 3 | 3 | 1 | moderate:3, none:4, strong:1 |
| olmesartan | ddi_risk | 1 | 2 | 3 | 1 | none:10, pd:1 |
| valsartan | ddi_risk | 1 | 2 | 2 | 1 | none:7, pd:1 |
| acarbose | ddi_risk | 2 | 1 | 1 | 5 | none:7, pd:4, pk:1 |
| alogliptin | cv_outcome_benefit | 2 | 3 | 2 | 1 | moderate:1, none:2, strong:1 |
| alogliptin | weight_effect | 2 | 3 | None | 5 | moderate:1, none:1, strong:5 |
| gliclazide | cv_outcome_benefit | 2 | 3 | 2 | 2 | moderate:1, none:1, strong:2 |
| gliclazide | ddi_risk | 2 | 1 | 2 | 1 | none:5, pk:1 |
| glimepiride | renal_benefit | 2 | 3 | 2 | 1 | none:1, strong:1 |
| glyburide | cv_outcome_benefit | 2 | 3 | 2 | 1 | none:1, strong:1 |
| glyburide | ddi_risk | 2 | 1 | 2 | 1 | none:2, pk:1 |
| linagliptin | weight_effect | 2 | 1 | None | 0 | none:1 |
| repaglinide | renal_benefit | 2 | 3 | 2 | 2 | none:1, strong:2 |
| rosiglitazone | cv_outcome_benefit | 2 | 3 | 2 | 2 | moderate:5, none:1, strong:2 |
| rosiglitazone | ddi_risk | 2 | 1 | 1 | 3 | none:6, pd:1, pk:2 |
| tirzepatide | renal_benefit | 2 | 3 | 2 | 1 | moderate:1, none:3, strong:1 |
| ranitidine | ddi_risk | 3 | 2 | 2 | 2 | none:2, pd:2 |
| aspirin | cv_risk | 2 | 3 | 2 | 3 | moderate:5, none:2, strong:3 |
| indomethacin | ddi_risk | 2 | 1 | 2 | 3 | none:2, pd:3 |
| piroxicam | ddi_risk | 1 | 2 | 2 | 2 | none:8, pd:1, pk:1 |
| esomeprazole | acid_rebound | 2 | 3 | 2 | 1 | none:4, strong:1 |
| esomeprazole | ddi_risk | 3 | 2 | 2 | 4 | none:2, pk:4 |
| lansoprazole | ddi_risk | 3 | 2 | 2 | 5 | none:5, pd:1, pk:4 |
| pantoprazole | ddi_risk | 2 | 1 | 1 | 1 | none:5, pk:1 |
| simvastatin | ddi_risk | 2 | 1 | 2 | 0 | none:1 |

## Open questions (44)

| drug | dim | current | clean | kw | support | labels |
|---|---|---|---|---|---|---|
| amlodipine | electrolyte_risk | 2 | 3 | 2 | 1 | moderate:1, none:1, strong:1 |
| amlodipine | metabolic_effect | 2 | 1 | 2 | 0 | none:2 |
| atenolol | electrolyte_risk | 2 | 1 | 2 | 0 | none:1 |
| carvedilol | metabolic_effect | 3 | 2 | 3 | 1 | moderate:1, negative:1, none:2 |
| chlorthalidone | bp_reduction | 3 | 2 | 3 | 2 | moderate:2, none:6 |
| chlorthalidone | metabolic_effect | 2 | 1 | 2 | 0 | none:1 |
| hydralazine | bp_reduction | 3 | 2 | 3 | 3 | moderate:3, negative:1, none:8 |
| hydralazine | electrolyte_risk | 2 | 1 | 2 | 0 | none:3 |
| hydralazine | renal_protection | 2 | 3 | 2 | 1 | negative:1, none:2, strong:1 |
| metoprolol | electrolyte_risk | 1 | 3 | 1 | 1 | none:2, strong:1 |
| olmesartan | metabolic_effect | 3 | 2 | 3 | 2 | moderate:2, negative:1, none:1 |
| olmesartan | renal_protection | 3 | 2 | 3 | 4 | moderate:4, none:3 |
| propranolol | electrolyte_risk | 3 | 1 | 3 | 0 | none:1 |
| telmisartan | electrolyte_risk | 2 | 3 | 2 | 1 | none:1, strong:1 |
| telmisartan | renal_protection | 3 | 2 | 3 | 4 | moderate:4, none:1 |
| terazosin | electrolyte_risk | 3 | 2 | 3 | 1 | moderate:1, none:1 |
| valsartan | electrolyte_risk | 1 | 3 | 1 | 1 | moderate:1, none:2, strong:1 |
| verapamil | metabolic_effect | 3 | 2 | 3 | 2 | moderate:2, none:9 |
| acarbose | hypoglycemia_risk | 2 | 1 | 2 | 0 | none:1 |
| dulaglutide | renal_benefit | 3 | 2 | 3 | 7 | moderate:7, none:3 |
| exenatide | renal_benefit | 2 | 3 | 2 | 1 | moderate:1, none:2, strong:1 |
| glyburide | renal_benefit | 2 | 3 | 2 | 1 | none:2, strong:1 |
| glyburide | weight_effect | 2 | 3 | None | 1 | none:2, strong:1 |
| insulin-aspart | weight_effect | 2 | 3 | None | 1 | none:1, strong:1 |
| insulin-degludec | weight_effect | 2 | 3 | None | 1 | none:1, strong:1 |
| linagliptin | cv_outcome_benefit | 3 | 2 | 3 | 1 | moderate:1, none:5 |
| linagliptin | gi_tolerability | 3 | 1 | 3 | 0 | none:1 |
| metformin | weight_effect | 2 | 3 | None | 1 | moderate:1, none:1, strong:1 |
| pioglitazone | weight_effect | 2 | 3 | None | 1 | none:1, strong:1 |
| rosiglitazone | renal_benefit | 2 | 3 | 2 | 1 | moderate:1, strong:1 |
| saxagliptin | weight_effect | 2 | 3 | None | 1 | moderate:2, negative:2, none:1, strong:1 |
| sitagliptin | hypoglycemia_risk | 3 | 1 | 3 | 0 | none:1 |
| vildagliptin | hypoglycemia_risk | 2 | 3 | 1 | 1 | moderate:1, none:1, strong:1 |
| aspirin | renal_risk | 2 | 3 | 2 | 1 | moderate:4, negative:2, none:3, strong:1 |
| diclofenac | cv_risk | 2 | 1 | 2 | 0 | none:1 |
| diclofenac | renal_risk | 2 | 1 | 2 | 0 | none:1 |
| ibuprofen | cv_risk | 2 | 3 | 2 | 1 | none:1, strong:1 |
| naproxen | cv_risk | 2 | 3 | 2 | 1 | moderate:5, negative:1, none:5, strong:1 |
| paracetamol | renal_risk | 2 | 1 | 2 | 0 | none:1 |
| piroxicam | cv_risk | 2 | 1 | 2 | 0 | none:1 |
| lansoprazole | cdi_risk | 2 | 1 | 2 | 0 | none:1 |
| pantoprazole | acid_rebound | 2 | 1 | 2 | 0 | none:1 |
| pantoprazole | cdi_risk | 3 | 2 | 3 | 1 | moderate:1, none:2 |
| rabeprazole | acid_rebound | 2 | 1 | 2 | 0 | none:1 |

## By class (proposals)

| class | raises | drops | fills |
|---|---|---|---|
| Alginate | 0 | 2 | 0 |
| Antihypertensive | 8 | 1 | 0 |
| Diabetes | 7 | 11 | 0 |
| Mucosal Protectant | 0 | 1 | 0 |
| NSAID | 2 | 2 | 0 |
| Statin | 0 | 2 | 0 |

Holds omitted (192 cells where Batch-5 confirms the current value).

## Decision (2026-09-28, user-approved)

- **Applied (11)**: furosemide|electrolyte_risk 2→3, losartan|electrolyte_risk 1→3, diltiazem|renal_protection 2→3, hydrochlorothiazide|renal_protection 2→3, clonidine|metabolic_effect 2→3, exenatide|cv_outcome_benefit 2→3, liraglutide|weight_effect 2→3, piroxicam|renal_risk 2→3, insulin-glargine|cv_outcome_benefit 2→1, insulin-glargine|renal_benefit 2→1, meloxicam|gi_risk 3→2
- **Demoted to open questions (25)**: proposals whose basis sentence was misattributed (wrong drug/construct), irrelevant, or a single none-labeled sentence — incl. ibuprofen|gi_risk 3→1 (contradicts its own GI-bleeding basis), sucralfate|barrier_protection 3→1 (basis affirms mucoprotection), liraglutide|hypoglycemia_risk 3→1 (basis lists hypoglycemia as common)
- Full audit trail: `batch5_rescore_adjudication.json`
