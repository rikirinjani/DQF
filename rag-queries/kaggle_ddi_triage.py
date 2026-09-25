# ============================================================
# DQF BATCH 3 — ddi_risk evidence-pool triage (paste into fresh Kaggle notebook)
# GPU T4 x2, Internet ON. No dataset needed (input from public repo).
# Classifies 401 drug-anchored ddi-candidate sentences: real interaction
# (pk/pd) vs comparison/background/none. Output feeds a filtered re-score.
# Output: ddi_verdicts.json
# ============================================================

# ---------- CELL 1: deps + input ----------
import os, sys, json, time, re, subprocess, urllib.request
print('STEP 0', flush=True)
url = ('https://raw.githubusercontent.com/rikirinjani/DQF/master/'
       'rag-queries/ddi_sentences.json')
INP = '/tmp/ddi_sentences.json'
urllib.request.urlretrieve(url, INP)
data = json.load(open(INP, encoding='utf-8'))
nsent = sum(len(v['sentences']) for v in data.values())
print(f'input OK: {len(data)} drugs, {nsent} sentences', flush=True)
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

# ---------- CELL 3: prompt + smoke ----------
PROMPT = ('You are triaging PubMed sentences about the drug {drug} for a '
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

def classify_prompt(drug, chunk):
    lines = [f'{i+1}. [{s["pmid"]}] {s["text"]}' for i, s in enumerate(chunk)]
    return PROMPT.format(drug=drug) + '\n\n' + '\n'.join(lines) + '\n\nJSON array:'

def parse_arr(txt):
    m = re.search(r'\[.*\]', txt, re.S)
    if not m:
        return None
    try:
        arr = json.loads(m.group(0))
        out = []
        for o in arr:
            n = int(o.get('n', 0)); c = str(o.get('cls', 'none')).lower()
            out.append({'n': n, 'cls': c if c in ('pk', 'pd', 'none') else 'none'})
        return out
    except Exception:
        # salvage individual pairs
        pairs = re.findall(r'"n"\s*:\s*(\d+)\s*,\s*"(?:cls|class)"\s*:\s*"(pk|pd|none)"', txt)
        return [{'n': int(a), 'cls': b} for a, b in pairs] or None

did0 = next(iter(data))
print(f"SMOKE: {did0} ({len(data[did0]['sentences'])} sent)", flush=True)
chunk0 = data[did0]['sentences'][:6]
t0 = time.time()
arr = parse_arr(gen(classify_prompt(did0, chunk0)))
print(f'secs={time.time()-t0:.1f} parsed={arr}', flush=True)

# ---------- CELL 4: full triage ----------
OUTP = '/kaggle/working/ddi_verdicts.json'
CHUNK = 8
res, t0 = {}, time.time()
n_sent = n_kept = 0
for i, (did, d) in enumerate(data.items()):
    sents = d['sentences']
    verdicts = {}
    for j in range(0, len(sents), CHUNK):
        chunk = sents[j:j+CHUNK]
        try:
            arr = parse_arr(gen(classify_prompt(did, chunk)))
        except Exception as e:
            arr = None
            print(f'  ERR {did} chunk{j}: {type(e).__name__}', flush=True)
        if not arr:
            arr = [{'n': k+1, 'cls': 'none'} for k in range(len(chunk))]
        for k, o in enumerate(arr):
            idx = o.get('n', k+1) - 1
            if 0 <= idx < len(chunk):
                s = chunk[idx]
                cls = o['cls']
                verdicts[f'{s["pmid"]}|{k+j}'] = {'pmid': s['pmid'], 'text': s['text'], 'cls': cls}
                n_sent += 1
                if cls in ('pk', 'pd'):
                    n_kept += 1
    res[did] = {'class': d['class'], 'sentences': list(verdicts.values())}
    json.dump(res, open(OUTP, 'w', encoding='utf-8'), ensure_ascii=False)
    if (i + 1) % 10 == 0:
        print(f'  [{i+1}/{len(data)}] sent={n_sent} kept(pk/pd)={n_kept} '
              f'elapsed={(time.time()-t0)/60:.1f}m', flush=True)
print(f'DONE sentences={n_sent} kept={n_kept} min={(time.time()-t0)/60:.1f}', flush=True)
print('saved ->', OUTP, flush=True)
