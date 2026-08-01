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

# Fix E: tokens whose content the endpoint confuses with similarly-prefixed
# drug queries (e.g. methyldopa queries returning methylphenidate/methylone/
# MDMA). A snippet is relevant only if it does NOT contain any of these
# UNLESS it also contains the drug's own name variant.
CONFUSABLE_TOKENS = {"methylphenidate", "methylone", "mdma", "methyl-dopa"}

# Fix C: lazily-built set of every drug name in drugs.json (lowercased).
# Used by the co-mention relevance rule -- a head-to-head comparison trial
# mentions the subject drug once alongside a comparator, and the comparator
# is (almost always) another drug from the framework's own list.
_OTHER_DRUG_NAMES = None  # module-level lazy cache

def _other_drug_names(current_name=""):
    """All drug names from drugs.json minus the current drug's own name.

    Same rule as extract_l3.py. Built lazily on first use and cached
    module-wide. Class words and other non-drug words never enter the set
    (it is derived from drug names only), and callers only count mentions
    of length >= 4 to avoid noise.
    """
    global _OTHER_DRUG_NAMES
    if _OTHER_DRUG_NAMES is None:
        try:
            d = json.load(open(DRUGS, encoding="utf-8"))
            _OTHER_DRUG_NAMES = {
                str(x.get("name", "")).lower() for x in d.get("drugs", []) if x.get("name")
            }
        except Exception:
            _OTHER_DRUG_NAMES = set()
    own = (current_name or "").lower()
    return {n for n in _OTHER_DRUG_NAMES if n and n != own}

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

    Same rule as extract_l3.py (_snippet_relevant): keep a snippet iff
      * a drug-name variant appears in its title, OR
      * >=2 mentions across title+text, OR
      * a single mention alongside another drug name from the framework's
        drug list (co-mention head-to-head comparison trial, e.g.
        methyldopa-vs-nifedipine RCTs which mention both drugs once).
    Confusable content (Fix E: methylphenidate/methylone/mdma/methyl-dopa)
    is relevant only if the drug's own name variant is also present.
    Returns (kept_snippets, total_snippets, kept_count).
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
                # OR a single mention co-occurring with another drug name
                # (text embeds the title in both RAG and EUtils sources, so
                # counting in text covers title mentions).
                title_match = title and any(v in title_lower for v in variants)
                count = sum(text_lower.count(v) for v in variants)
                has_confusable = any(tok in f"{title_lower}\n{text_lower}" for tok in CONFUSABLE_TOKENS)
                if has_confusable:
                    # Fix E: confusable content is relevant iff the drug's own
                    # name variant is also present ("mentioning both -> keep";
                    # "confusable only -> drop").
                    if not (title_match or count >= 1):
                        continue
                elif not title_match:
                    # Fix C: >=2 mentions, OR a single mention co-occurring
                    # with another drug name (co-mention comparison trial)
                    if count < 2 and not (
                            count >= 1 and any(
                                len(o) >= 4 and (o in title_lower or o in text_lower)
                                for o in _other_drug_names(drug_name))):
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
