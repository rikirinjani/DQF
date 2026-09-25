# ============================================================
# DQF LLM-judge batch — MANUAL version (paste into a fresh Kaggle notebook)
# Run cell by cell. Needs: GPU T4 x2 (Settings → Accelerator), Internet ON.
# No dataset attach needed (downloads input from the public repo).
# Expect: ~5 min model load, then ~1-3h judging. Output: judge_output.json
# ============================================================

# ---------- CELL 1: deps + input ----------
import os, sys, json, time, re, subprocess, urllib.request
print('STEP 0: deps + input check', flush=True)
INP = '/kaggle/input/dqf-l3-judge-input/judge_input.json'
if not os.path.exists(INP):
    print('dataset mount missing; fallback: GitHub raw', flush=True)
    url = ('https://raw.githubusercontent.com/rikirinjani/DQF/master/'
           'rag-queries/judge_input.json')
    INP = '/tmp/judge_input.json'
    urllib.request.urlretrieve(url, INP)
    print('fallback download OK', flush=True)
data_check = json.load(open(INP, encoding='utf-8'))
print(f'input OK: {len(data_check)} drugs', flush=True)
del data_check
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q',
    'transformers', 'accelerate', 'bitsandbytes', 'sentencepiece'])
print('DEPS DONE', flush=True)
import torch
assert torch.cuda.is_available(), 'NO GPU - enable accelerator (GPU T4 x2) and re-run'
print('GPU:', torch.cuda.get_device_name(0),
      '| VRAM GB:', round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1),
      '| count:', torch.cuda.device_count(), flush=True)

# ---------- CELL 2: model ----------
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
MODEL = 'mistralai/Mistral-7B-Instruct-v0.3'  # Apache-2.0, ungated
print('STEP 1: load model', flush=True)
tok = AutoTokenizer.from_pretrained(MODEL)
tok.pad_token = tok.eos_token
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
                         bnb_4bit_compute_dtype=torch.float16)
mdl = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=bnb,
                                           device_map='auto')
print('MODEL READY', flush=True)

def gen(prompt, max_new=220):
    ids = tok(prompt, return_tensors='pt').to(mdl.device)
    with torch.no_grad():
        out = mdl.generate(**ids, max_new_tokens=max_new, do_sample=False,
                           pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids['input_ids'].shape[1]:], skip_special_tokens=True)

# ---------- CELL 3: judge helpers + SMOKE TEST (2 dims, ~30s) ----------
SYS = ('You are a clinical-pharmacology evidence judge. '
 'Score how strongly the evidence sentences support an effect of the drug '
 'on the given dimension. Rules: (1) count ONLY sentences about THIS drug; '
 'ignore effects attributed to other named drugs; (2) IGNORE sodium/potassium '
 'mentions that are part of ANOTHER drug\u2019s salt name (e.g. divalproex '
 'sodium, warfarin sodium, sodium valproate, losartan potassium, sodium '
 'bicarbonate vehicle); serum/urinary sodium and electrolyte disturbances ARE '
 'valid; (3) negated or no-effect statements do not support; general background '
 'does not support. Return STRICT JSON only: '
 '{"score": 1|2|3, "n_supporting": <int>, "pmids": [<ids>], "rationale": "<1 sentence>"} '
 'where 1=no/weak evidence, 2=moderate, 3=strong.')

def judge_prompt(drug, dim, current, ev):
    lines = [f"[{e['pmid']}] {e['text']}" for e in ev]
    return (f"{SYS}\nDrug: {drug}\nDimension: {dim}\n"
            f"Current keyword score: {current}\nEvidence:\n"
            + "\n".join(lines) + "\nJSON:")

def parse_json(txt):
    m = re.search(r'\{[^{}]*"score"[^{}]*\}', txt, re.S)
    if not m:
        return None
    try:
        o = json.loads(m.group(0))
        s = int(o.get('score', 0))
        return o if s in (1, 2, 3) else None
    except Exception:
        return None

# smoke test on first drug/first dim with evidence
data = json.load(open(INP, encoding='utf-8'))
did0 = next(iter(data))
d0 = data[did0]
dim0 = next(d for d, ev in d0['evidence'].items() if ev)
print(f'SMOKE: {did0}/{dim0} ...', flush=True)
t0 = time.time()
txt0 = gen(judge_prompt(d0.get('name', did0), dim0, d0['current'].get(dim0), d0['evidence'][dim0]))
print(f'smoke secs={time.time()-t0:.1f}', flush=True)
print('parsed:', parse_json(txt0))
print('raw tail:', txt0[-200:])

# ---------- CELL 4: full batch (saves incrementally) ----------
OUTP = '/kaggle/working/judge_output.json'
print(f'STEP 2: judge {len(data)} drugs', flush=True)
res, t0 = {}, time.time()
n_calls = n_ok = n_agree = 0
for i, (did, d) in enumerate(data.items()):
    rdrug = {'drug': did}
    for dim, ev in d['evidence'].items():
        if not ev:
            continue
        n_calls += 1
        cur = d['current'].get(dim)
        try:
            txt = gen(judge_prompt(d.get('name', did), dim, cur, ev))
            o = parse_json(txt)
        except Exception as e:
            o, txt = {'score': None, 'error': type(e).__name__}, ''
        if o and o.get('score'):
            n_ok += 1
            if cur == o['score']:
                n_agree += 1
        else:
            o = {'score': None, 'raw': txt[:300]}
        rdrug[dim] = o
    res[did] = rdrug
    json.dump(res, open(OUTP, 'w', encoding='utf-8'), ensure_ascii=False)
    if (i + 1) % 5 == 0:
        print(f'  [{i+1}/{len(data)}] ok={n_ok}/{n_calls} agree={n_agree} '
              f'elapsed={(time.time()-t0)/60:.1f}m', flush=True)
print(f'DONE calls={n_calls} ok={n_ok} agree={n_agree}/{n_ok} '
      f'total_min={(time.time()-t0)/60:.1f}', flush=True)
print('saved ->', OUTP, flush=True)
