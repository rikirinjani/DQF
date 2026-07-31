"""Build L2b semantic-review digests: per drug, per field, the heuristic score
+ the evidence snippets matching that field's keywords (from FIELD_SCHEMA).
Writes one JSON per drug to a temp digest dir."""
import json, glob, os, pathlib, re

OUT = r"C:\Users\think\Project_v2\drug-quantification-framework\rag-queries\l3_output"
DRUGS = r"C:\Users\think\Project_v2\drug-quantification-framework\api\drugs.json"
DIGEST_DIR = r"C:\Users\think\AppData\Local\Temp\opencode\l2b_digests"

FIELD_SCHEMA = {
    "Antihypertensive": [
        ("bp_reduction", ["bp reduction","blood pressure","antihypertensive","systolic","diastolic"], 2),
        ("renal_protection", ["renal","nephropathy","kidney","proteinuria","albuminuria","creatinine"], 1),
        ("metabolic_effect", ["glucose","lipid","uric acid","metabolic","diabetes","insulin","potassium","sodium"], 2),
        ("electrolyte_risk", ["hyperkalemia","hypokalemia","hyponatremia","electrolyte","potassium","sodium"], 1),
        ("ddi_risk", ["drug interaction","interaction","NSAID","diuretic","ACE inhibitor","ARB"], 1),
    ],
    "Diabetes": [
        ("a1c_reduction", ["a1c","glycemic","hemoglobin a1c","glucose","glycemic control","hyperglycemia"], 2),
        ("weight_effect", ["weight","weight loss","weight gain","body weight","obesity","bmi"], 1),
        ("cv_outcome_benefit", ["cardiovascular","mace","mortality","heart failure","cv death","myocardial infarction","stroke"], 1),
        ("renal_benefit", ["renal","kidney","nephropathy","egfr","albuminuria","proteinuria","ckd","creatinine"], 1),
        ("gi_tolerability", ["nausea","vomiting","diarrhea","gi","gastrointestinal","abdominal","dyspepsia"], 2),
        ("ddi_risk", ["drug interaction","interaction","renal clearance","tubular secretion","contrast"], 1),
        ("hypoglycemia_risk", ["hypoglycemia","low blood glucose","severe hypoglycemia","glucose <70","hypoglycemic"], 2),
    ],
}
HEART_KW = ["heart rate","bradycardia","tachycardia","heart rate effect"]

def _name_variants(drug_id, name):
    """Drug-name variants to search for (mirrors extract_l3.py relevance gate)."""
    base = (name or drug_id).lower()
    variants = {base, drug_id.lower()}
    base2 = re.sub(r"[^a-z]", "", base)
    variants.add(base2)
    variants.add(base.split()[0])
    return {v for v in variants if len(v) >= 5}

def load_pool(drug_id, drug_name=""):
    """Load the retrieval pool, applying the drug-relevance gate.

    Same rule as extract_l3.py: keep a snippet iff a drug-name variant
    appears in its title, OR >=2 mentions across title+text. This drops
    off-drug papers (passing mentions) while preserving legitimate
    co-mention comparison trials (e.g. methyldopa-vs-nifedipine RCTs,
    which mention both drugs in title+abstract). Returns
    (kept_snippets, total_snippets, kept_count).
    """
    d = os.path.join(OUT, drug_id)
    snips = []
    total = 0
    if not os.path.isdir(d):
        return snips, total, 0
    variants = _name_variants(drug_id, drug_name)
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            j = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        res = j.get("result", {}).get("results", []) if "result" in j else j.get("results", [])
        for r in res:
            t = r.get("text", "")
            pid = str(r.get("id", "")).replace("PMID:", "")
            if t and pid:
                total += 1
                text_lower = t.lower()
                title = r.get("title") or ""
                title_lower = title.lower()
                # Title match is authoritative; otherwise require >=2 mentions
                # across title+text (text embeds the title in both RAG and
                # EUtils sources, so counting in text covers title mentions).
                if title and any(v in title_lower for v in variants):
                    pass  # keep
                else:
                    count = sum(text_lower.count(v) for v in variants)
                    if count < 2:
                        continue
                snips.append({"pmid": pid, "text": t, "title": title, "score": r.get("rerank_score", 0)})
    return snips, total, len(snips)

def main():
    pathlib.Path(DIGEST_DIR).mkdir(parents=True, exist_ok=True)
    d = json.load(open(DRUGS, encoding="utf-8"))
    count = 0
    for x in d["drugs"]:
        cls = x["class"]
        if cls not in FIELD_SCHEMA:
            continue
        lid = x["id"]
        l3 = x.get("l3_systems", {})
        pool, pool_total, pool_kept = load_pool(lid, x.get("name", ""))
        digest = {
            "drug_id": lid, "name": x.get("name"), "class": cls,
            "pool_size": pool_total, "pool_kept": pool_kept,
            "filtered_off_drug": pool_total - pool_kept,
            "pool_relevance_pct": round(100.0 * pool_kept / pool_total, 1) if pool_total else 0.0,
            "profile_pool_relevance_pct": (l3.get("_evidence", {}) or {}).get("pool_relevance_pct"),
            "fields": {},
        }
        for fname, kws, default in FIELD_SCHEMA[cls]:
            matched = [s for s in pool if any(k in s["text"].lower() for k in kws)]
            digest["fields"][fname] = {
                "heuristic": l3.get(fname), "default": default,
                "evidence": matched[:8],  # cap per field
            }
        if cls == "Antihypertensive":
            hk = [s for s in pool if any(k in s["text"].lower() for k in HEART_KW)]
            digest["fields"]["heart_rate_effect"] = {
                "heuristic": l3.get("heart_rate_effect"), "default": "none",
                "evidence": hk[:8],
            }
        # also keep fields present in profile but not in schema (e.g. l3 extras)
        for k, v in l3.items():
            if k.startswith("_") or k in digest["fields"]:
                continue
            digest["fields"][k] = {"heuristic": v, "default": None, "evidence": []}
        fp = os.path.join(DIGEST_DIR, lid + ".json")
        json.dump(digest, open(fp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        count += 1
    print(f"Wrote {count} digests to {DIGEST_DIR}")

if __name__ == "__main__":
    main()
