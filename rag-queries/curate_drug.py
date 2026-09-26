"""curate_drug.py — PMID-provenanced evidence fetcher for DQF drug curation.

For each curation field (L1 target, L2 PK, L4 outcome, safety) it runs a PubMed
search and pulls the top abstracts, so every value entered into a drug record
can cite a real source. No fabrication: if nothing relevant is returned, the
field stays null.

NCBI E-utilities only (no extra deps beyond `requests`); works when the HF RAG
endpoint is down. For PMC full text, use the rag-service
`query_lancedb_fulltext.py` (LanceDB on S3) instead.

Usage:
  python rag-queries/curate_drug.py apixaban
  python rag-queries/curate_drug.py warfarin --specs rag-queries/curation/specs-anticoagulant.json

Output: rag-queries/curation/{drug}_evidence.json
  {"drug": ..., "generated": ..., "fields": {label: {query, pmids, snippets:[{pmid, text}]}}}

Stdin/stdout are UTF-8; NCBI requests are throttled below the 3 req/s guideline.
"""
import argparse
import datetime as _dt
import json
import os
import re
import sys
import time

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = "DQFCuration"
EMAIL = os.environ.get("NCBI_EMAIL", "dqf-pipeline@example.com")
API_KEY = os.environ.get("NCBI_API_KEY", "")
REQ_INTERVAL = 0.2 if API_KEY else 0.4   # 10/s with key, 3/s without
RETMAX = 5

# Default curation field -> PubMed query templates. {drug} is substituted.
DEFAULT_SPECS = {
    "L1_target_potency": "{drug} target inhibition potency IC50 Ki mechanism",
    "L1_selectivity": "{drug} selectivity off-target pharmacology",
    "L2_pk_basic": "{drug} pharmacokinetics half-life bioavailability volume of distribution",
    "L2_metabolism_excretion": "{drug} metabolism CYP renal excretion clearance",
    "L4_efficacy": "{drug} efficacy randomized controlled trial clinical outcome",
    "L4_safety": "{drug} adverse events bleeding risk safety",
    "safety_pregnancy": "{drug} pregnancy safety teratogenicity",
    "safety_hepatic": "{drug} hepatic impairment pharmacokinetics dose adjustment",
}

_last = 0.0


def _throttle():
    global _last
    w = REQ_INTERVAL - (time.time() - _last)
    if w > 0:
        time.sleep(w)
    _last = time.time()


def _get(path, params):
    _throttle()
    p = {"tool": TOOL, "email": EMAIL, "retmode": "json"}
    if API_KEY:
        p["api_key"] = API_KEY
    p.update(params)
    r = requests.get(f"{EUTILS}/{path}", params=p, timeout=30)
    r.raise_for_status()
    return r


def esearch(query, retmax=RETMAX):
    r = _get("esearch.fcgi", {"db": "pubmed", "term": query,
                              "retmax": retmax, "sort": "relevance"})
    return r.json().get("esearchresult", {}).get("idlist", [])


def efetch_abstracts(pmids):
    if not pmids:
        return []
    _throttle()
    p = {"db": "pubmed", "id": ",".join(pmids), "rettype": "abstract",
         "retmode": "text", "tool": TOOL, "email": EMAIL}
    if API_KEY:
        p["api_key"] = API_KEY
    r = requests.get(f"{EUTILS}/efetch.fcgi", params=p, timeout=60)
    r.raise_for_status()
    text = r.text
    # Split per PMID record: records start with "PMID: <n>"
    parts = re.split(r"(?=^PMID:\s*\d+)", text, flags=re.M)
    out = []
    for part in parts:
        m = re.match(r"^PMID:\s*(\d+)", part)
        if m:
            out.append({"pmid": m.group(1), "text": part.strip()})
    return out


def run(drug, specs):
    fields = {}
    for label, tmpl in specs.items():
        query = tmpl.replace("{drug}", drug)
        try:
            pmids = esearch(query)
            snippets = efetch_abstracts(pmids)
        except Exception as e:
            print(f"  ! {label}: {type(e).__name__}: {str(e)[:80]}", file=sys.stderr)
            fields[label] = {"query": query, "error": f"{type(e).__name__}", "pmids": [], "snippets": []}
            continue
        fields[label] = {"query": query, "pmids": pmids, "snippets": snippets}
        print(f"  {label:24s} -> {len(pmids)} pmids, {len(snippets)} abstracts")
    return {"drug": drug,
            "generated": _dt.datetime.now().isoformat(timespec="seconds"),
            "source": "NCBI E-utilities (esearch+efetch)",
            "fields": fields}


def main():
    ap = argparse.ArgumentParser(description="PMID-provenanced evidence fetcher for DQF curation")
    ap.add_argument("drug")
    ap.add_argument("--specs", help="JSON file {label: query-template} to override defaults")
    ap.add_argument("--out", help="output path (default rag-queries/curation/{drug}_evidence.json)")
    args = ap.parse_args()

    specs = DEFAULT_SPECS
    if args.specs:
        specs = json.load(open(args.specs, encoding="utf-8"))
    out = args.out or os.path.join(ROOT, "rag-queries", "curation", f"{args.drug}_evidence.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    print(f"curating {args.drug}: {len(specs)} fields")
    data = run(args.drug, specs)
    json.dump(data, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    n = sum(len(f["pmids"]) for f in data["fields"].values())
    print(f"\n{n} PMIDs total -> {out}")


if __name__ == "__main__":
    main()
