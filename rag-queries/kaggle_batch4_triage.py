# ============================================================
# DQF BATCH 4 — evidence-pool strength triage (paste into fresh Kaggle notebook)
# GPU T4 x2, Internet ON. No dataset needed (input from public repo).
# 54 groups = 49 non-ddi (drug,dim) cells flagged "still_diluted" in Batch 2
# + 5 ddi pools missed by Batch-3 harvest (celecoxib/atorvastatin/rosuvastatin/
#   simvastatin/tirzepatide). 300 sentences.
# Non-ddi labels: strong / moderate / negative / none
#   strong   = direct evidence IN <drug> of clinically meaningful effect on the
#              dimension: magnitude (%/absolute change), significant trial
#              outcome vs control, established efficacy, dose-response
#   moderate = real evidence about <drug> and this dimension but indirect,
#              mechanistic, qualitative, animal/in-vitro, or unquantified
#   negative = explicit NO effect / absence of the effect for <drug>
#   none     = unrelated to the dimension, other drugs' effects, comparisons
#              without own-effect magnitude, background/disease info
# ddi labels: pk / pd / none (Batch-3 taxonomy)
# Output: batch4_verdicts.json
# ============================================================

# ---------- CELL 1: deps + input ----------
import os, sys, json, time, re, subprocess, urllib.request
print('STEP 0', flush=True)
url = ('https://raw.githubusercontent.com/rikirinjani/DQF/master/'
       'rag-queries/batch4_sentences.json')
INP = '/tmp/batch4_sentences.json'
urllib.request.urlretrieve(url, INP)
data = json.load(open(INP, encoding='utf-8'))
nsent = sum(len(v['sentences']) for v in data.values())
print(f'input OK: {len(data)} groups, {nsent} sentences', flush=True)
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q',
    'transformers', 'accelerate', 'bitsandbytes', 'sentencepiece'])
print('DEPS DONE', flush=True)
import torch
assert torch.cuda.is_available(), 'NO GPU - enable accelerator (GPU T4 x2)'
print('GPU:', torch.cuda.get_device_name(0), '| count:', torch.cuda.device_count(), flush=True)

# ---------- CELL 2: model ----------
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
MODEL = 'mistralai/Mistral-7B-Instruct-v0.3'
tok = AutoTokenizer.from_pretrained(MODEL)
tok.pad_token = tok.eos_token
mdl = AutoModelForCausalLM.from_pretrained(
    MODEL, quantization_config=BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type='nf4',
        bnb_4bit_compute_dtype=torch.float16), device_map='auto')
print('MODEL READY', flush=True)

def gen(prompt, max_new=500):
    ids = tok(prompt, return_tensors='pt').to(mdl.device)
    with torch.no_grad():
        out = mdl.generate(**ids, max_new_tokens=max_new, do_sample=False,
                           pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids['input_ids'].shape[1]:], skip_special_tokens=True)

# ---------- CELL 3: prompts + smoke ----------
DIM_DESC = {
 'weight_effect': 'effect on body weight (weight loss or gain, appetite, BMI)',
 'renal_protection': 'kidney protection (slowing CKD progression, reducing proteinuria/albuminuria, renoprotection)',
 'cv_outcome_benefit': 'cardiovascular outcome benefit (reduced MACE, mortality, heart-failure hospitalization, MI, stroke)',
 'metabolic_effect': 'metabolic effects (glucose, lipids, uric acid, insulin sensitivity)',
 'renal_benefit': 'kidney benefit (eGFR, albuminuria, nephropathy outcomes)',
 'electrolyte_risk': 'electrolyte disturbances (hyperkalemia, hypokalemia, hyponatremia)',
 'cv_risk': 'cardiovascular risk or adverse cardiovascular effects',
 'renal_risk': 'kidney toxicity or adverse renal effects (AKI, rising creatinine)',
 'hypoglycemia_risk': 'hypoglycemia (low blood glucose) risk',
 'cdi_risk': 'Clostridioides difficile infection risk',
 'acid_rebound': 'rebound acid hypersecretion after stopping the drug',
 'bone_fracture_risk': 'bone fracture risk',
 'neutralization_capacity': 'capacity to neutralize gastric acid',
 'renal_toxicity_risk': 'renal accumulation / toxicity risk',
 'ddi_risk': 'drug-drug interaction potential',
}

PROMPT_DDI = ('You are triaging PubMed sentences about the drug {drug} for a '
 'drug-drug interaction (DDI) evidence pool. For each numbered sentence, '
 'classify whether it describes a REAL drug-drug interaction involving '
 '{drug}:\n'
 '- "pk" = pharmacokinetic interaction (CYP/enzyme/transporter mediated change '
 'in plasma levels, AUC, exposure, or clearance when drugs are co-administered)\n'
 '- "pd" = pharmacodynamic interaction (combined or altered clinical effect when '
 'drugs are co-administered)\n'
 '- "none" = efficacy or safety COMPARISON versus another drug ("more effective '
 'than X", "better tolerated than Y"), mere mention of another drug, treatment '
 'guidelines combining drugs, background, or anything without a real '
 'co-administration interaction.\n'
 'Return STRICT JSON array only, one object per sentence in order: '
 '[{{"n":1,"cls":"none"}},{{"n":2,"cls":"pk"}},...]')

PROMPT_DIM = ('You are grading PubMed sentences about the drug {drug} (class: '
 '{cls}) for the evidence pool of the dimension "{dim}" = {desc}.\n'
 'For each numbered sentence classify the STRENGTH of evidence that {drug} '
 'has a real effect on this dimension:\n'
 '- "strong" = direct evidence in {drug} of a clinically meaningful effect: '
 'quantified magnitude (% or absolute change), significant trial result versus '
 'control/placebo, established efficacy or outcome benefit, dose-response\n'
 '- "moderate" = real evidence that {drug} affects this dimension but indirect, '
 'mechanistic, qualitative, animal/in-vitro, or without quantification\n'
 '- "negative" = explicit evidence of NO effect / no difference / absence of '
 'the effect for {drug} on this dimension\n'
 '- "none" = not about this dimension for {drug}: other endpoints, effects of '
 'OTHER drugs, comparisons like "better tolerated than X" or "similar to Y" '
 'without own quantified effect, background disease info, methods, guidelines\n'
 'Return STRICT JSON array only, one object per sentence in order: '
 '[{{"n":1,"cls":"none"}},{{"n":2,"cls":"strong"}},...]')

def classify_prompt(gid, g, chunk):
    lines = [f'{i+1}. [{s["pmid"]}] {s["text"]}' for i, s in enumerate(chunk)]
    if g['dim'] == 'ddi_risk':
        p = PROMPT_DDI.format(drug=g['name'])
    else:
        p = PROMPT_DIM.format(drug=g['name'], cls=g.get('class') or 'unknown',
                              dim=g['dim'], desc=DIM_DESC.get(g['dim'], g['dim']))
    return p + '\n\n' + '\n'.join(lines) + '\n\nJSON array:'

VALID = ('pk', 'pd', 'none', 'strong', 'moderate', 'negative')

def parse_arr(txt):
    m = re.search(r'\[.*\]', txt, re.S)
    if not m:
        return None
    try:
        arr = json.loads(m.group(0))
        out = []
        for o in arr:
            n = int(o.get('n', 0)); c = str(o.get('cls', 'none')).lower()
            out.append({'n': n, 'cls': c if c in VALID else 'none'})
        return out
    except Exception:
        pairs = re.findall(
            r'"n"\s*:\s*(\d+)\s*,\s*"(?:cls|class)"\s*:\s*"(\w+)"', txt)
        return [{'n': int(a), 'cls': (b if b in VALID else 'none')}
                for a, b in pairs] or None

# smoke: one ddi group + one dim group
for gid in [k for k in data if data[k]['dim'] == 'ddi_risk'][:1] + \
           [k for k in data if data[k]['dim'] != 'ddi_risk'][:1]:
    g = data[gid]
    chunk0 = g['sentences'][:5]
    t0 = time.time()
    arr = parse_arr(gen(classify_prompt(gid, g, chunk0)))
    print(f'SMOKE {gid}: secs={time.time()-t0:.1f} parsed={arr}', flush=True)

# ---------- CELL 4: full triage ----------
OUTP = '/kaggle/working/batch4_verdicts.json'
CHUNK = 8
res, t0 = {}, time.time()
n_sent = n_strong = 0
for i, (gid, g) in enumerate(data.items()):
    sents = g['sentences']
    verdicts = {}
    for j in range(0, len(sents), CHUNK):
        chunk = sents[j:j+CHUNK]
        try:
            arr = parse_arr(gen(classify_prompt(gid, g, chunk)))
        except Exception as e:
            arr = None
            print(f'  ERR {gid} chunk{j}: {type(e).__name__}', flush=True)
        if not arr:
            arr = [{'n': k+1, 'cls': 'none'} for k in range(len(chunk))]
        for k, o in enumerate(arr):
            idx = o.get('n', k+1) - 1
            if 0 <= idx < len(chunk):
                s = chunk[idx]
                cls = o['cls']
                verdicts[f'{s["pmid"]}|{k+j}'] = {'pmid': s['pmid'], 'text': s['text'], 'cls': cls}
                n_sent += 1
                if cls in ('pk', 'pd', 'strong'):
                    n_strong += 1
    res[gid] = {'drug': g['drug'], 'dim': g['dim'], 'class': g.get('class'),
                'sentences': list(verdicts.values())}
    json.dump(res, open(OUTP, 'w', encoding='utf-8'), ensure_ascii=False)
    if (i + 1) % 10 == 0:
        print(f'  [{i+1}/{len(data)}] sent={n_sent} keep(pk/pd/strong)={n_strong} '
              f'elapsed={(time.time()-t0)/60:.1f}m', flush=True)
print(f'DONE groups={len(res)} sentences={n_sent} kept={n_strong} min={(time.time()-t0)/60:.1f}', flush=True)
print('saved ->', OUTP, flush=True)
