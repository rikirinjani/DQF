# ============================================================
# DQF LLM-judge BATCH 2 — adversarial re-judge (paste into a fresh Kaggle notebook)
# GPU T4 x2, Internet ON. No dataset attach needed (downloads v2 input from repo).
# Re-judges 140 cells: every ddi_risk + every run-1 disagreement, with a FIXED
# ddi_risk definition and both prior scores shown, max_new=400 (no truncation).
# Output: judge_output_v2.json
# ============================================================

# ---------- CELL 1: deps + input ----------
import os, sys, json, time, re, subprocess, urllib.request
print('STEP 0', flush=True)
url = ('https://raw.githubusercontent.com/rikirinjani/DQF/master/'
       'rag-queries/judge_input_v2.json')
INP = '/tmp/judge_input_v2.json'
urllib.request.urlretrieve(url, INP)
data = json.load(open(INP, encoding='utf-8'))
ncells = sum(len([k for k in v if k not in ('name', 'class')]) for v in data.values())
print(f'input OK: {len(data)} drugs, {ncells} cells', flush=True)
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

def gen(prompt, max_new=400):
    ids = tok(prompt, return_tensors='pt').to(mdl.device)
    with torch.no_grad():
        out = mdl.generate(**ids, max_new_tokens=max_new, do_sample=False,
                           pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids['input_ids'].shape[1]:], skip_special_tokens=True)

# ---------- CELL 3: prompts + smoke test ----------
BASE = ('You are a clinical-pharmacology evidence judge. Decide the best-supported '
 'score for how strongly the evidence shows an effect of THIS drug on the given '
 'dimension. Rules: (1) count ONLY sentences about THIS drug; (2) IGNORE sodium/'
 'potassium that is part of ANOTHER drug\u2019s salt name (divalproex sodium, '
 'losartan potassium, sodium bicarbonate vehicle) - but serum/urinary sodium and '
 'electrolyte disturbances DO count; (3) negated or no-effect statements do NOT '
 'support; (4) mechanistic background alone does NOT support. '
 'Return STRICT JSON only: {"score": 1|2|3, "n_supporting": <int>, "pmids": [ids], '
 '"rationale": "<1 sentence>"}. 1=no/weak, 2=moderate, 3=strong.')

DDI = ('SPECIAL DEFINITION for ddi_risk: judge whether the evidence shows a real '
 'DRUG-DRUG INTERACTION - a pharmacokinetic interaction (CYP/enzyme/transporter '
 'mediated change in plasma levels/exposure) or a clinically significant '
 'pharmacodynamic interaction when CO-ADMINISTERED. CRITICAL: comparisons of '
 'clinical EFFICACY or SAFETY against another drug ("more effective than '
 'piroxicam", "better tolerated than ACE inhibitors", "superior to placebo") are '
 'NOT interactions. Merely naming another drug is NOT an interaction.')

def judge_prompt(drug, dim, kw, llm1, ev):
    extra = DDI if dim == 'ddi_risk' else ''
    lines = [f"[{e['pmid']}] {e['text']}" for e in ev]
    return (f"{BASE}\n{extra}\nDrug: {drug}\nDimension: {dim}\n"
            f"Prior keyword score: {kw} | Prior LLM score: {llm1}\n"
            f"Evidence:\n" + "\n".join(lines) + "\nJSON:")

def parse(txt):
    m = re.search(r'"score"\s*:\s*([123])', txt)
    if not m:
        return None
    s = int(m.group(1))
    pm = re.search(r'"n_supporting"\s*:\s*(\d+)', txt)
    pmids = re.findall(r'\d{6,9}', txt.split('"pmids"')[-1][:200]) if '"pmids"' in txt else []
    rat = re.search(r'"rationale"\s*:\s*"([^"]{0,300})', txt)
    return {"score": s, "n_supporting": int(pm.group(1)) if pm else None,
            "pmids": pmids[:8], "rationale": rat.group(1) if rat else ""}

did0 = next(iter(data))
dim0 = next(k for k in data[did0] if k not in ('name', 'class'))
c0 = data[did0][dim0]
print(f'SMOKE: {did0}/{dim0} ({len(c0["evidence"])} sent)', flush=True)
t0 = time.time()
txt0 = gen(judge_prompt(data[did0].get('name', did0), dim0, c0['keyword_score'], c0['llm1_score'], c0['evidence']))
print(f'secs={time.time()-t0:.1f} parsed={parse(txt0)}', flush=True)
print('raw tail:', txt0[-160:], flush=True)

# ---------- CELL 4: full re-judge ----------
OUTP = '/kaggle/working/judge_output_v2.json'
res, t0 = {}, time.time()
n = ok = 0
for i, (did, d) in enumerate(data.items()):
    rd = {'drug': did}
    for dim, c in d.items():
        if dim in ('name', 'class') or not c.get('evidence'):
            continue
        n += 1
        try:
            o = parse(gen(judge_prompt(d.get('name', did), dim, c['keyword_score'], c['llm1_score'], c['evidence'])))
        except Exception as e:
            o = {'score': None, 'error': type(e).__name__}
        if o and o.get('score'):
            ok += 1
        rd[dim] = o or {'score': None}
    res[did] = rd
    json.dump(res, open(OUTP, 'w', encoding='utf-8'), ensure_ascii=False)
    if (i + 1) % 10 == 0:
        print(f'  [{i+1}/{len(data)}] ok={ok}/{n} elapsed={(time.time()-t0)/60:.1f}m', flush=True)
print(f'DONE cells={n} ok={ok} min={(time.time()-t0)/60:.1f}', flush=True)
print('saved ->', OUTP, flush=True)
