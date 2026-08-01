#!/usr/bin/env python3
"""
DQF L3 Evidence Back-fill -- Consolidation for ALL 88 drugs (9 classes)
========================================================================

Single canonical multi-angle RAG backfill runner for every drug in
api/drugs.json. Consolidates the two parallel lane scripts (A: 45 drugs
of Antihypertensive/PPI/H2RA/Antacid/Alginate/Mucosal Protectant; B: 43
drugs of Diabetes/NSAID/Statin) into one script.

Covers all 88 drugs across 9 classes:
    Antihypertensive      33
    Diabetes              28
    NSAID                 10
    PPI                    5
    Statin                 5
    H2RA                   3
    Antacid                2
    Alginate               1
    Mucosal Protectant     1
    ------------------------
    TOTAL                 88

For each drug, issues 8 RAG queries across TWO angles:

  Angle A -- drug-anchored mechanism/efficacy  (4 queries)
  Angle B -- outcome-specific quantitative      (4 queries)

The RAG retriever embeds query concepts but NOT drug names, so every query
LEADS with the drug name (the point of the "different angles" test).

Angle C -- NCBI EUtils anchored fallback. Runs only for drugs where fewer
than 6 of the 8 RAG queries returned usable (non-empty `results`) responses:
  esearch.fcgi  ({drug}[tiab] OR {drug}[nm]) AND
                ("number needed to treat"[tiab] OR NNT[tiab] OR
                 "randomized controlled trial"[pt])
  efetch.fcgi   abstracts for top 5 PMIDs

Storage convention (raw JSON per query):
    rag-queries/l3_output/<drug>/backfill_<slug>.json
    = {"query": {...}, "result": <raw response>}
where slug = query lowercased, non-alphanumerics -> `_`, 60-char cap.

Hard rules honored:
  - 1.5 s delay between RAG calls
  - "Still loading" cold-start errors: retry up to 2 more times (5 s backoff),
    record the error response in the file if still failing
  - 30 s timeout per call; on timeout treat as failed and continue
  - FULL response text saved (no truncation)
  - No existing files overwritten: `backfill_` prefix only, new files only.
    Existing `backfill_*` files are SKIPPED (resumable). The 6 diabetes drugs
    covered by the earlier 10-drug run are detected by their existing files
    and counted as already-covered without refetching.
  - Drug list comes from api/drugs.json `class` field (9 classes), NOT
    hardcoded.

Usage:
    python backfill_all_queries.py                  # all 88 drugs (skip-if-exists)
    python backfill_all_queries.py --refresh        # refetch + overwrite all 88 (post re-index)
    python backfill_all_queries.py --dry-run        # enumerate + validate, no HTTP
    python backfill_all_queries.py --class Diabetes
    python backfill_all_queries.py --drug metformin
    python backfill_all_queries.py --eutils-only metformin
    python backfill_all_queries.py --rag-only

Refresh mode (--refresh):
    Re-fetches every RAG query even when a backfill_*.json already exists and
    OVERWRITES the canonical file in place (no _N uniquify). Intended for
    re-running after the RAG endpoint re-indexes with a raised text cap, so
    truncated snippets are replaced by full abstracts. The 6 ALREADY_COVERED
    diabetes drugs are also refetched in refresh mode. EUtils files are
    overwritten too. Counts files_refreshed in the summary.
"""

import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DRUGS_JSON = PROJECT_ROOT / "api" / "drugs.json"
OUT_BASE = SCRIPT_DIR / "l3_output"
# Neutral summary path (does not overwrite the lane-specific
# backfill_all_summary_A.json / backfill_all_summary_B.json files).
SUMMARY_PATH = SCRIPT_DIR / "backfill_all_summary.json"

RAG_ENDPOINT = "https://balade-pubmed-rag-bot.hf.space/search"
RAG_TOP_K = 3
RAG_DELAY_S = 1.5        # polite delay between RAG queries
RAG_TIMEOUT = 30         # per-call timeout; timeout == failed
RETRY_MAX = 2            # extra attempts after initial (Still loading)
RETRY_BACKOFF_S = 5.0

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
NCBI_EMAIL = "dqf-pipeline@example.com"
NCBI_TOOL = "DQFL3BackfillAll"
NCBI_RATE_LIMIT = 0.35   # no API key -> 3 req/s -> >= 0.34 s spacing
NCBI_PER_QUERY = 5       # top 5 PMIDs per drug

# All classes in scope (exact strings from api/drugs.json `class` field).
ALL_CLASSES = [
    "Antihypertensive",
    "Diabetes",
    "NSAID",
    "Statin",
    "PPI",
    "H2RA",
    "Antacid",
    "Alginate",
    "Mucosal Protectant",
]

# 6 diabetes drugs already backfilled by the earlier 10-drug run
# (backfill_queries.py). They already have 8 backfill files each; we count
# them as already-covered and do NOT refetch, regardless of slug drift
# (e.g. pramlintide A2 wording differs from the Diabetes class template).
ALREADY_COVERED = {
    "alogliptin", "exenatide", "rosiglitazone",
    "pramlintide", "saxagliptin", "vildagliptin",
}

# Class-specific outcome phrases substituted into A2 and B2, keyed by the
# exact class strings used in api/drugs.json. {drug} is replaced with the
# query drug name so every query leads with the drug name.
CLASS_QUERIES = {
    "Antihypertensive": {
        "A2": "{drug} blood pressure reduction hypertension efficacy",
        "B2": "{drug} effect size confidence interval blood pressure change",
    },
    "Diabetes": {
        "A2": "{drug} HbA1c reduction diabetes efficacy",
        "B2": "{drug} effect size confidence interval HbA1c change",
    },
    "NSAID": {
        "A2": "{drug} pain relief analgesia efficacy",
        "B2": "{drug} effect size confidence interval pain relief",
    },
    "Statin": {
        "A2": "{drug} LDL cholesterol reduction efficacy",
        "B2": "{drug} effect size confidence interval LDL reduction",
    },
    "PPI": {
        "A2": "{drug} acid suppression esophagitis healing efficacy",
        "B2": "{drug} effect size confidence interval healing rate",
    },
    "H2RA": {
        "A2": "{drug} acid suppression ulcer healing efficacy",
        "B2": "{drug} effect size confidence interval healing rate",
    },
    "Antacid": {
        "A2": "{drug} heartburn relief efficacy",
        "B2": "{drug} effect size confidence interval symptom relief",
    },
    "Alginate": {
        "A2": "{drug} reflux symptom relief efficacy",
        "B2": "{drug} effect size confidence interval symptom relief",
    },
    "Mucosal Protectant": {
        "A2": "{drug} ulcer healing mucosal protection efficacy",
        "B2": "{drug} effect size confidence interval healing rate",
    },
}

EUTILS_TERM_TMPL = ('({drug}[tiab] OR {drug}[nm]) AND '
                    '("number needed to treat"[tiab] OR NNT[tiab] OR '
                    '"randomized controlled trial"[pt])')

# Combination-product edge case: no single [nm] MeSH term exists for
# "aluminum-magnesium-hydroxide"; use the two component MeSH terms OR'd
# with the tiab form of the combination name.
EUTILS_TERM_OVERRIDES = {
    "aluminum-magnesium-hydroxide":
        '((aluminum hydroxide[nm] OR magnesium hydroxide[nm] OR '
        'aluminum-magnesium-hydroxide[tiab])) AND '
        '("number needed to treat"[tiab] OR NNT[tiab] OR '
        '"randomized controlled trial"[pt])',
}


# ---------------------------------------------------------------------------
# Drug list from api/drugs.json
# ---------------------------------------------------------------------------
def load_drugs(classes: list[str]) -> list[dict]:
    """Load drugs filtered to the given classes. Entries: id, name, class."""
    with open(DRUGS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for d in data.get("drugs", []):
        if d.get("class") in classes:
            out.append({"id": d["id"], "name": d["name"], "class": d["class"]})
    # stable order: class order, then file order
    order = {c: i for i, c in enumerate(classes)}
    out.sort(key=lambda d: (order[d["class"]], d["id"]))
    return out


def query_drug_name(d: dict) -> str:
    """Name to embed in RAG queries. Display labels (e.g. 'Al/Mg
    Hydroxide') are replaced by the substance name from the drug id."""
    n = d.get("name") or d["id"]
    if "/" in n:
        return d["id"].replace("-", " ")
    return n


# ---------------------------------------------------------------------------
# Query construction
# ---------------------------------------------------------------------------
def build_queries(drug_name: str, drug_class: str) -> list[dict]:
    """Return the 8 RAG query specs for one drug (Angles A + B)."""
    cq = CLASS_QUERIES[drug_class]
    return [
        {"angle": "A1", "dimension": "backfill_mechanism",
         "query": f"{drug_name} mechanism of action efficacy clinical trial"},
        {"angle": "A2", "dimension": "backfill_outcome",
         "query": cq["A2"].format(drug=drug_name)},
        {"angle": "A3", "dimension": "backfill_nnt",
         "query": f"{drug_name} number needed to treat NNT outcome"},
        {"angle": "A4", "dimension": "backfill_safety",
         "query": f"{drug_name} adverse effects safety profile incidence"},
        {"angle": "B1", "dimension": "backfill_rct",
         "query": f"{drug_name} randomized controlled trial efficacy outcome quantitative result"},
        {"angle": "B2", "dimension": "backfill_effect_size",
         "query": cq["B2"].format(drug=drug_name)},
        {"angle": "B3", "dimension": "backfill_comparative",
         "query": f"{drug_name} comparative effectiveness versus placebo meta-analysis"},
        {"angle": "B4", "dimension": "backfill_pk",
         "query": f"{drug_name} time to onset pharmacokinetics peak effect"},
    ]


def slugify(query: str) -> str:
    """Slug = query lowercased, non-alphanumerics -> _, 60-char cap."""
    return re.sub(r"[^a-z0-9]+", "_", query.lower())[:60]


# ---------------------------------------------------------------------------
# RAG fetch with cold-start retry
# ---------------------------------------------------------------------------
def fetch_rag(query: str) -> tuple[dict, str]:
    """Call the RAG endpoint. Returns (data, outcome).

    outcome in {"ok", "still_loading", "error_response", "timeout",
                "http_error", "parse_error"}. On still_loading, retries up
    to RETRY_MAX more times with RETRY_BACKOFF_S; the last error response
    is returned so it can be recorded in the file.
    """
    for attempt in range(RETRY_MAX + 1):
        try:
            resp = requests.get(RAG_ENDPOINT,
                                params={"q": query, "k": RAG_TOP_K},
                                timeout=RAG_TIMEOUT)
        except requests.exceptions.Timeout:
            return {"_error": f"timeout after {RAG_TIMEOUT}s"}, "timeout"
        except requests.RequestException as e:
            return {"_error": f"http error: {e}"}, "http_error"

        try:
            data = resp.json()
        except ValueError:
            return {"_error": f"non-JSON response (HTTP {resp.status_code}): {resp.text[:200]}"}, \
                "parse_error"

        if isinstance(data, dict) and data.get("error"):
            err = str(data.get("error"))
            if "Still loading" in err and attempt < RETRY_MAX:
                time.sleep(RETRY_BACKOFF_S)
                continue
            return data, "still_loading" if "Still loading" in err else "error_response"
        return data, "ok"
    return {"_error": "retries exhausted"}, "still_loading"


# ---------------------------------------------------------------------------
# NCBI EUtils (Angle C fallback; no API key -> throttled to 3 req/s)
# ---------------------------------------------------------------------------
class EUtils:
    def __init__(self):
        self._last_req = 0.0
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": f"{NCBI_TOOL}/1.0"})

    def _throttle(self):
        elapsed = time.time() - self._last_req
        if elapsed < NCBI_RATE_LIMIT:
            time.sleep(NCBI_RATE_LIMIT - elapsed)
        self._last_req = time.time()

    def _params(self, **kw) -> dict:
        base = {"tool": NCBI_TOOL, "email": NCBI_EMAIL}
        base.update(kw)
        return base

    def search_ids(self, term: str, retmax: int = NCBI_PER_QUERY) -> list[str]:
        self._throttle()
        resp = self.session.get(
            f"{NCBI_BASE}/esearch.fcgi",
            params=self._params(db="pubmed", term=term,
                                retmax=min(retmax, 50), retmode="json", sort="relevance"),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("esearchresult", {}).get("idlist", [])

    def fetch_abstracts(self, pmids: list[str]) -> list[dict]:
        if not pmids:
            return []
        self._throttle()
        resp = self.session.get(
            f"{NCBI_BASE}/efetch.fcgi",
            params=self._params(db="pubmed", id=",".join(pmids),
                                retmode="xml", rettype="abstract"),
            timeout=30,
        )
        resp.raise_for_status()
        return self._parse_xml(resp.text)

    @staticmethod
    def _parse_xml(xml_str: str) -> list[dict]:
        """Parse PubMed XML EFetch response into structured article dicts."""
        articles = []
        root = ET.fromstring(xml_str)
        for art in root.findall("PubmedArticle"):
            medline = art.find("MedlineCitation")
            if medline is None:
                continue
            art_elem = medline.find("Article")
            pmid_elem = medline.find("PMID")
            pmd = art.find("PubmedData")
            pmid = pmid_elem.text if pmid_elem is not None else ""

            title = ""
            if art_elem is not None and (t := art_elem.find("ArticleTitle")) is not None:
                title = "".join(t.itertext())

            abstract = ""
            if art_elem is not None and (ab := art_elem.find("Abstract")) is not None:
                abstract = "\n".join("".join(at.itertext()) for at in ab.findall("AbstractText"))

            authors = []
            if art_elem is not None and (al := art_elem.find("AuthorList")) is not None:
                for a in al.findall("Author")[:3]:
                    ln, fn = a.find("LastName"), a.find("ForeName")
                    if ln is not None and fn is not None:
                        authors.append(f"{ln.text} {fn.text}")

            journal = ""
            if art_elem is not None and (j := art_elem.find("Journal")) is not None:
                if (t := j.find("Title")) is not None and t.text:
                    journal = t.text

            doi = ""
            if pmd is not None and (il := pmd.find("ArticleIdList")) is not None:
                for aid in il.findall("ArticleId"):
                    if aid.get("IdType") == "doi":
                        doi = aid.text or ""

            mesh = []
            if (ml := medline.find("MeshHeadingList")) is not None:
                for m in ml.findall("MeshHeading"):
                    if (d := m.find("DescriptorName")) is not None and d.text:
                        mesh.append(d.text)

            kws = []
            if (kl := medline.find("KeywordList")) is not None:
                for kw in kl.findall("Keyword"):
                    if kw.text:
                        kws.append(kw.text)

            pub_date = ""
            if art_elem is not None and (j := art_elem.find("Journal")) is not None:
                if (ji := j.find("JournalIssue")) is not None and (pd := ji.find("PubDate")) is not None:
                    parts = []
                    for tag in ("Year", "Month", "Day"):
                        if (el := pd.find(tag)) is not None and el.text:
                            parts.append(el.text)
                    pub_date = "-".join(parts)

            articles.append({
                "pmid": pmid, "title": title, "abstract": abstract,
                "full_text": f"{title}\n\n{abstract}",
                "authors": authors, "journal": journal,
                "doi": doi, "mesh_terms": mesh, "keywords": kws,
                "pub_date": pub_date,
            })
        return articles


def run_eutils(client: EUtils, term: str) -> dict:
    """esearch + efetch for a drug-anchored PubMed query. RAG-compatible dict."""
    try:
        pmids = client.search_ids(term, retmax=NCBI_PER_QUERY)
    except requests.RequestException as e:
        return {"_error": f"esearch failed: {e}"}
    if not pmids:
        return {"results": [], "note": "no PMIDs matched the query"}
    try:
        articles = client.fetch_abstracts(pmids)
    except requests.RequestException as e:
        return {"_error": f"efetch failed: {e}"}
    if not articles:
        return {"results": [], "note": "efetch returned no articles"}
    results = []
    for i, art in enumerate(articles):
        results.append({
            "id": f"PMID:{art['pmid']}",
            "text": art["full_text"],
            "title": art["title"],
            "rerank_score": 1.0 if i == 0 else max(0.5, 1.0 - 0.05 * i),
            "metadata": {k: art[k] for k in
                         ("pmid", "journal", "authors", "pub_date", "doi",
                          "mesh_terms", "keywords")},
        })
    return {"results": results, "source": "NCBI EUtils esearch+efetch"}


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
def save_raw(drug_id: str, query_spec: dict, result: dict,
             overwrite: bool = False) -> Path:
    """Save raw response. Never overwrites unless overwrite=True (refresh
    mode): uniquifies on collision by default, or writes the canonical
    backfill_<slug>.json in place when overwriting."""
    drug_out = OUT_BASE / drug_id
    drug_out.mkdir(parents=True, exist_ok=True)
    base = f"backfill_{slugify(query_spec['query'])}"
    if overwrite:
        path = drug_out / f"{base}.json"
    else:
        path = drug_out / f"{base}.json"
        n = 1
        while path.exists():
            path = drug_out / f"{base}_{n}.json"
            n += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"query": query_spec, "result": result}, f,
                  indent=2, ensure_ascii=False)
    return path


def count_usable(data: dict) -> int:
    """Number of usable (non-empty results) in a saved response."""
    if not isinstance(data, dict):
        return 0
    res = data.get("result", data)
    if isinstance(res, dict) and isinstance(res.get("results"), list):
        return len(res["results"])
    return 0


# ---------------------------------------------------------------------------
# Dry-run: enumerate drugs per class and validate the class map (no HTTP)
# ---------------------------------------------------------------------------
def dry_run() -> int:
    """Enumerate every drug in api/drugs.json, print class -> drug count,
    validate that every drug's class exists in CLASS_QUERIES, and exit
    without issuing any HTTP requests."""
    with open(DRUGS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    drugs = data.get("drugs", [])

    counts = {c: 0 for c in ALL_CLASSES}
    missing = []   # (drug_id, class) where class not in CLASS_QUERIES
    unlisted = []  # (drug_id, class) where class not even in ALL_CLASSES
    for d in drugs:
        cls = d.get("class", "?")
        if cls in counts:
            counts[cls] += 1
        else:
            unlisted.append((d.get("id", "?"), cls))
        if cls not in CLASS_QUERIES:
            missing.append((d.get("id", "?"), cls))

    print("=" * 56)
    print("DRY-RUN: class inventory (api/drugs.json)")
    print("=" * 56)
    total = 0
    for c in ALL_CLASSES:
        has_tpl = "templates OK" if c in CLASS_QUERIES else "!! NO TEMPLATES"
        print(f"  {c:22s} {counts[c]:3d} drugs   [{has_tpl}]")
        total += counts[c]
    print("-" * 56)
    print(f"  TOTAL                {total:3d} drugs")
    if unlisted:
        print("\n  Classes not in ALL_CLASSES:")
        for did, cls in unlisted:
            print(f"    - {did} -> {cls}")
    if missing:
        print("\n  Drugs whose class is MISSING from CLASS_QUERIES:")
        for did, cls in missing:
            print(f"    - {did} -> {cls}")
    else:
        print("\n  All drugs map to a class present in CLASS_QUERIES: OK")
    print("\n  (dry-run: no HTTP requests issued, nothing written)")
    return 0 if (total == len(drugs) and not missing) else 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="DQF L3 evidence backfill (ALL 88 drugs, 9 classes)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Enumerate drugs per class and validate the class map; no HTTP")
    parser.add_argument("--refresh", action="store_true",
                        help="Refetch all queries and OVERWRITE existing backfill files "
                             "(use after the RAG endpoint re-indexes with a raised cap)")
    parser.add_argument("--class", dest="cls",
                        help=f"Run a single class: {'|'.join(ALL_CLASSES)}")
    parser.add_argument("--drug", help="Run a single drug id only")
    parser.add_argument("--rag-only", action="store_true",
                        help="Skip Angle C (EUtils) even if RAG < 6/8 OK")
    parser.add_argument("--eutils-only", metavar="DRUG",
                        help="Run only the Angle C EUtils query for a drug")
    args = parser.parse_args()

    if args.dry_run:
        return dry_run()

    classes = ALL_CLASSES
    if args.cls:
        if args.cls not in ALL_CLASSES:
            print(f"Unknown class: {args.cls} (choose {ALL_CLASSES})", file=sys.stderr)
            return 1
        classes = [args.cls]

    drugs = load_drugs(classes)
    if args.drug:
        drugs = [d for d in drugs if d["id"] == args.drug.lower()]
    if not drugs:
        print(f"Unknown drug: {args.drug}", file=sys.stderr)
        return 1

    print(f"Loaded {len(drugs)} drugs from {DRUGS_JSON} "
          f"({', '.join(classes)})", flush=True)

    summary = {
        "pipeline": "DQF L3 evidence backfill ALL (88 drugs, 9 classes)",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "rag_endpoint": RAG_ENDPOINT,
        "classes": classes,
        "drugs": {},
    }
    totals = {"drugs_total": len(drugs), "rag_queries_issued": 0, "rag_ok": 0,
              "still_loading_failed": 0, "timeout_failed": 0, "other_errors": 0,
              "eutils_runs": 0, "files_written": 0, "files_refreshed": 0,
              "files_skipped_existing": 0, "drugs_already_covered": 0}
    endpoint_errors: list[str] = []
    eutils = EUtils()

    for drug in drugs:
        drug_id, drug_class = drug["id"], drug["class"]
        drug_name = query_drug_name(drug)
        specs = build_queries(drug_name, drug_class)
        ds = {"class": drug_class, "name": drug["name"], "files_written": [],
              "rag_ok": 0, "still_loading_failed": 0, "timeout_failed": 0,
              "other_errors": 0, "eutils_run": False, "eutils_file": None,
              "files_skipped_existing": 0, "skipped_already_covered": False}
        print(f"\n=== {drug_id} [{drug_class}] ===", flush=True)

        if args.eutils_only and args.eutils_only.lower() != drug_id:
            continue

        # Pre-existing backfill files -> mark already-covered (resume path).
        # The 6 ALREADY_COVERED drugs from the earlier 10-drug run are never
        # refetched, even if a slug differs (e.g. pramlintide A2 wording).
        # In refresh mode both skip paths are disabled: everything refetches.
        if not args.eutils_only and not args.refresh:
            if drug_id in ALREADY_COVERED:
                ds["skipped_already_covered"] = True
                totals["drugs_already_covered"] += 1
                print(f"  [ALREADY-COVERED] {drug_id} from earlier run; no refetch", flush=True)
            else:
                existing_targets = 0
                for spec in specs:
                    fname = f"backfill_{slugify(spec['query'])}.json"
                    if (OUT_BASE / drug_id / fname).exists():
                        existing_targets += 1
                if existing_targets == len(specs):
                    ds["skipped_already_covered"] = True
                    totals["drugs_already_covered"] += 1

        if not args.eutils_only and not ds["skipped_already_covered"]:
            for spec in specs:
                fname = f"backfill_{slugify(spec['query'])}.json"
                existing = OUT_BASE / drug_id / fname
                if existing.exists() and not args.refresh:
                    # Resume path: existing backfill file counts if usable
                    try:
                        with open(existing, encoding="utf-8") as f:
                            prev = json.load(f)
                        if count_usable(prev) > 0:
                            ds["rag_ok"] += 1
                    except (json.JSONDecodeError, OSError):
                        pass
                    ds["files_skipped_existing"] += 1
                    totals["files_skipped_existing"] += 1
                    print(f"  [SKIP] {fname} exists", flush=True)
                    continue

                data, outcome = fetch_rag(spec["query"])
                path = save_raw(drug_id, spec, data, overwrite=args.refresh)
                ds["files_written"].append(path.name)
                totals["files_written"] += 1
                totals["rag_queries_issued"] += 1
                if args.refresh and existing.exists():
                    totals["files_refreshed"] += 1

                nres = 0
                if isinstance(data, dict) and isinstance(data.get("results"), list):
                    nres = len(data["results"])
                tag = f"OK({nres})" if (outcome == "ok") else outcome
                print(f"  [{spec['angle']}] {spec['query'][:62]:62s} -> {tag:16s} {path.name}", flush=True)

                if outcome == "ok" and nres > 0:
                    ds["rag_ok"] += 1
                    totals["rag_ok"] += 1
                elif outcome == "still_loading":
                    ds["still_loading_failed"] += 1
                    totals["still_loading_failed"] += 1
                    endpoint_errors.append(f"{drug_id}: {spec['query'][:55]} -> Still loading (error recorded in file)")
                elif outcome == "timeout":
                    ds["timeout_failed"] += 1
                    totals["timeout_failed"] += 1
                    endpoint_errors.append(f"{drug_id}: {spec['query'][:55]} -> timeout")
                else:
                    ds["other_errors"] += 1
                    totals["other_errors"] += 1
                    endpoint_errors.append(f"{drug_id}: {spec['query'][:55]} -> {outcome}")

                time.sleep(RAG_DELAY_S)

        # Also count already-covered drugs' on-disk files for accurate
        # reporting (no refetch either way).
        if ds["skipped_already_covered"]:
            for spec in specs:
                fname = f"backfill_{slugify(spec['query'])}.json"
                existing = OUT_BASE / drug_id / fname
                if existing.exists():
                    try:
                        with open(existing, encoding="utf-8") as f:
                            prev = json.load(f)
                        if count_usable(prev) > 0:
                            ds["rag_ok"] += 1
                    except (json.JSONDecodeError, OSError):
                        pass

        # Angle C: EUtils fallback (skip if --rag-only or RAG >= 6/8 OK)
        if args.eutils_only:
            run_angle_c = True
        elif args.rag_only:
            run_angle_c = False
        elif ds["skipped_already_covered"]:
            run_angle_c = False  # already covered by prior run
        else:
            run_angle_c = ds["rag_ok"] < 6
        if run_angle_c:
            ds["eutils_run"] = True
            totals["eutils_runs"] += 1
            term = EUTILS_TERM_OVERRIDES.get(drug_id, EUTILS_TERM_TMPL.format(drug=drug_id))
            eutils_result = run_eutils(eutils, term)
            drug_out = OUT_BASE / drug_id
            drug_out.mkdir(parents=True, exist_ok=True)
            efile = drug_out / f"backfill_eutils_{drug_id}.json"
            if not args.refresh:
                n = 1
                while efile.exists():
                    efile = drug_out / f"backfill_eutils_{drug_id}_{n}.json"
                    n += 1
            with open(efile, "w", encoding="utf-8") as f:
                json.dump({"query": {"query": term, "angle": "C",
                                     "dimension": "backfill_eutils", "target": None},
                           "result": eutils_result}, f, indent=2, ensure_ascii=False)
            ds["eutils_file"] = efile.name
            ds["files_written"].append(efile.name)
            totals["files_written"] += 1
            n_arts = len(eutils_result.get("results", [])) if isinstance(eutils_result, dict) else 0
            print(f"  [EUTILS] wrote {efile.name} ({n_arts} articles)", flush=True)
        else:
            print(f"  [EUTILS] not needed (RAG OK = {ds['rag_ok']}/8)", flush=True)

        summary["drugs"][drug_id] = ds

    # Write summary file
    summary["totals"] = totals
    summary["endpoint_errors"] = endpoint_errors
    summary["overwrites"] = ("refresh mode: existing backfill_* files overwritten in place"
                             if args.refresh else "none: all outputs are new backfill_* files")
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Console report
    print("\n" + "=" * 70)
    print("SUMMARY (ALL 88 drugs, 9 classes)")
    print("=" * 70)
    for drug_id, ds in summary["drugs"].items():
        nfiles = len(ds["files_written"])
        eutils_tag = ("EUtils: " + ds["eutils_file"]) if ds["eutils_run"] else "EUtils: not needed"
        cov = " [already-covered]" if ds["skipped_already_covered"] else ""
        print(f"  {drug_id:28s} {ds['class'][:12]:12s} RAG OK {ds['rag_ok']}/8 | "
              f"still-loading {ds['still_loading_failed']} | "
              f"timeouts {ds['timeout_failed']} | other {ds['other_errors']} | "
              f"files {nfiles} | {eutils_tag}{cov}")
    print("-" * 70)
    print(f"  Drugs: {totals['drugs_total']} | RAG queries issued: {totals['rag_queries_issued']} | "
          f"OK: {totals['rag_ok']} | still-loading: {totals['still_loading_failed']} | "
          f"timeouts: {totals['timeout_failed']} | other: {totals['other_errors']} | "
          f"EUtils runs: {totals['eutils_runs']} | files written: {totals['files_written']} | "
          f"files refreshed: {totals['files_refreshed']} | "
          f"files skipped (existing): {totals['files_skipped_existing']} | "
          f"drugs already covered: {totals['drugs_already_covered']}")
    if endpoint_errors:
        print("  Endpoint errors observed:")
        for e in endpoint_errors:
            print(f"    - {e}")
    print(f"  Summary file: {SUMMARY_PATH}")
    print("  Overwrites: none (all outputs are new backfill_* files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
