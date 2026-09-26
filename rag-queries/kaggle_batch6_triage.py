# ============================================================
# DQF BATCH 6 — Anticoagulant (E1) evidence-pool strength triage
# (paste into a fresh Kaggle notebook; GPU T4 x2, Internet ON, no dataset)
#
# Covers the 6 Anticoagulant drugs x 7 new dimensions: 42 groups,
# 313 sentences. Small run (~10-20 min) -> detached launch still works:
#   Save Version -> Save & Run All (Commit)      (browser/machine can be off)
# or:  kaggle kernels push                        (fully headless)
# The run RESUMES: output is saved after every group, so a stopped session
# can be re-run and continues instead of restarting.
#
# Labels:
#   ddi_risk                       -> pk / pd / none            (Batch-3 taxonomy)
#   every other dimension          -> strong / moderate / negative / none
#     strong   = direct evidence IN <drug> of a clinically meaningful effect
#                on the dimension: quantified magnitude (%/absolute change),
#                significant trial result vs control/placebo, established
#                efficacy, dose-response
#     moderate = real evidence about <drug> and this dimension but indirect,
#                mechanistic, qualitative, animal/in-vitro, or unquantified
#     negative = explicit NO effect / absence of the effect for <drug>
#     none     = not about this dimension for <drug>: other endpoints, effects
#                of OTHER drugs, comparisons without own quantified effect,
#                background/disease info, methods, guidelines
#
# Output: /kaggle/working/batch6_verdicts.json
# ============================================================

# ---------- CELL 1: deps + input ----------
import os, sys, json, time, re, subprocess, urllib.request
print('STEP 0', flush=True)
url = ('https://raw.githubusercontent.com/rikirinjani/DQF/master/'
       'rag-queries/batch6_sentences.json')
INP = '/tmp/batch6_sentences.json'
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
                              dim=g['dim'], desc=g.get('desc') or g['dim'])
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

# smoke: one ddi group + one non-ddi group
for gid in [k for k in data if data[k]['dim'] == 'ddi_risk'][:1] + \
           [k for k in data if data[k]['dim'] != 'ddi_risk'][:1]:
    g = data[gid]
    t0 = time.time()
    arr = parse_arr(gen(classify_prompt(gid, g, g['sentences'][:5])))
    print(f'SMOKE {gid}: secs={time.time()-t0:.1f} parsed={arr}', flush=True)

# ---------- CELL 4: full triage (RESUMABLE) ----------
OUTP = '/kaggle/working/batch6_verdicts.json'
CHUNK = 8
res, t0 = {}, time.time()
if os.path.exists(OUTP):
    try:
        res = json.load(open(OUTP, encoding='utf-8'))
        print(f'RESUME: {len(res)}/{len(data)} groups already done', flush=True)
    except Exception as e:
        print(f'RESUME: unreadable partial ({type(e).__name__}) — fresh start', flush=True)
        res = {}
n_sent = n_keep = 0
for i, (gid, g) in enumerate(data.items()):
    if gid in res:
        continue
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
                    n_keep += 1
    res[gid] = {'drug': g['drug'], 'dim': g['dim'], 'class': g.get('class'),
                'desc': g.get('desc'), 'sentences': list(verdicts.values())}
    json.dump(res, open(OUTP, 'w', encoding='utf-8'), ensure_ascii=False)
    if (i + 1) % 20 == 0:
        print(f'  [{i+1}/{len(data)}] sent={n_sent} keep(pk/pd/strong)={n_keep} '
              f'elapsed={(time.time()-t0)/60:.1f}m', flush=True)
print(f'DONE groups={len(res)} sentences={n_sent} kept={n_keep} min={(time.time()-t0)/60:.1f}', flush=True)
print('saved ->', OUTP, flush=True)
