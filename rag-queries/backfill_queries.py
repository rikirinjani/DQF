#!/usr/bin/env python3
"""
DQF L3 Evidence Back-fill -- Multi-angle RAG queries for 10 priority drugs
==========================================================================

Task 1 of a DQF evidence back-fill. For each of 10 priority drugs (worst
relevance from profile audit), issues 8 RAG queries across TWO angles:

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
  - FULL response text saved (no 300-char truncation)
  - No existing files overwritten: `backfill_` prefix only, new files only.
    Existing `backfill_*` files are SKIPPED (resumable).
  - `requests` (or `urllib` fallback for EUtils only -- requests is present)

Usage:
    python backfill_queries.py
    python backfill_queries.py --drug alogliptin
    python backfill_queries.py --eutils-only alogliptin
    python backfill_queries.py --rag-only
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
OUT_BASE = SCRIPT_DIR / "l3_output"

RAG_ENDPOINT = "https://balade-pubmed-rag-bot.hf.space/search"
RAG_TOP_K = 3
RAG_DELAY_S = 1.5        # polite delay between RAG queries
RAG_TIMEOUT = 30         # per-call timeout; timeout == failed
RETRY_MAX = 2            # extra attempts after initial (Still loading)
RETRY_BACKOFF_S = 5.0

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
NCBI_EMAIL = "dqf-pipeline@example.com"
NCBI_TOOL = "DQFL3Backfill"
NCBI_RATE_LIMIT = 0.35   # no API key -> 3 req/s -> >= 0.34 s spacing
NCBI_PER_QUERY = 5       # top 5 PMIDs per drug

# (drug_id, drug_name_for_query, kind)
DRUGS = [
    ("alogliptin", "Alogliptin", "diabetes"),
    ("trandolapril", "Trandolapril", "ah"),
    ("methyldopa", "Methyldopa", "ah"),
    ("exenatide", "Exenatide", "diabetes"),
    ("rosiglitazone", "Rosiglitazone", "diabetes"),
    ("pramlintide", "Pramlintide", "pramlintide"),
    ("terazosin", "Terazosin", "ah"),
    ("saxagliptin", "Saxagliptin", "diabetes"),
    ("furosemide", "Furosemide", "furosemide"),
    ("vildagliptin", "Vildagliptin", "diabetes"),
]

# Angle A2 / B2 drug-appropriate outcome terms
A2_OUTCOME = {
    "ah": "blood pressure reduction hypertension efficacy",
    "diabetes": "HbA1c reduction diabetes efficacy",
    "pramlintide": "postprandial glucose reduction diabetes",
    "furosemide": "diuresis heart failure edema efficacy",
}
B2_OUTCOME = {
    "ah": "blood pressure change",
    "diabetes": "HbA1c change",
    "pramlintide": "HbA1c change",
    "furosemide": "congestion weight change",
}

EUTILS_TERM_TMPL = ('({drug}[tiab] OR {drug}[nm]) AND '
                    '("number needed to treat"[tiab] OR NNT[tiab] OR '
                    '"randomized controlled trial"[pt])')


# ---------------------------------------------------------------------------
# Query construction
# ---------------------------------------------------------------------------
def build_queries(drug_name: str, kind: str) -> list[dict]:
    """Return the 8 RAG query specs for one drug (Angles A + B)."""
    return [
        {"angle": "A1", "dimension": "backfill_mechanism",
         "query": f"{drug_name} mechanism of action efficacy clinical trial"},
        {"angle": "A2", "dimension": "backfill_outcome",
         "query": f"{drug_name} {A2_OUTCOME[kind]}"},
        {"angle": "A3", "dimension": "backfill_nnt",
         "query": f"{drug_name} number needed to treat NNT outcome"},
        {"angle": "A4", "dimension": "backfill_safety",
         "query": f"{drug_name} adverse effects safety profile incidence"},
        {"angle": "B1", "dimension": "backfill_rct",
         "query": f"{drug_name} randomized controlled trial efficacy outcome quantitative result"},
        {"angle": "B2", "dimension": "backfill_effect_size",
         "query": f"{drug_name} effect size confidence interval {B2_OUTCOME[kind]}"},
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
def save_raw(drug_id: str, query_spec: dict, result: dict) -> Path:
    """Save raw response. Never overwrites: uniquifies on collision."""
    drug_out = OUT_BASE / drug_id
    drug_out.mkdir(parents=True, exist_ok=True)
    base = f"backfill_{slugify(query_spec['query'])}"
    path = drug_out / f"{base}.json"
    n = 1
    while path.exists():
        path = drug_out / f"{base}_{n}.json"
        n += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"query": query_spec, "result": result}, f,
                  indent=2, ensure_ascii=False)
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="DQF L3 evidence backfill")
    parser.add_argument("--drug", help="Run a single drug id only")
    parser.add_argument("--rag-only", action="store_true",
                        help="Skip Angle C (EUtils) even if RAG < 6/8 OK")
    parser.add_argument("--eutils-only", metavar="DRUG",
                        help="Run only the Angle C EUtils query for a drug")
    args = parser.parse_args()

    drugs = DRUGS
    if args.drug:
        drugs = [d for d in DRUGS if d[0] == args.drug.lower()]
    if not drugs:
        print(f"Unknown drug: {args.drug}", file=sys.stderr)
        return 1

    summary = {
        "pipeline": "DQF L3 evidence backfill (Task 1)",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "rag_endpoint": RAG_ENDPOINT,
        "drugs": {},
    }
    totals = {"rag_queries_issued": 0, "rag_ok": 0, "still_loading_failed": 0,
              "timeout_failed": 0, "other_errors": 0, "eutils_runs": 0}
    endpoint_errors: list[str] = []
    eutils = EUtils()

    for drug_id, drug_name, kind in drugs:
        ds = {"kind": kind, "files_written": [], "rag_ok": 0,
              "still_loading_failed": 0, "timeout_failed": 0,
              "other_errors": 0, "eutils_run": False, "eutils_file": None}
        print(f"\n=== {drug_id} ===", flush=True)

        if args.eutils_only and args.eutils_only.lower() != drug_id:
            continue

        if not args.eutils_only:
            for spec in build_queries(drug_name, kind):
                fname = f"backfill_{slugify(spec['query'])}.json"
                existing = OUT_BASE / drug_id / fname
                if existing.exists():
                    # Resume path: existing backfill file counts if usable
                    try:
                        with open(existing, encoding="utf-8") as f:
                            prev = json.load(f)
                        prev_res = prev.get("result", {})
                        prev_n = len(prev_res.get("results", [])) if isinstance(prev_res, dict) else 0
                        if prev_n > 0:
                            ds["rag_ok"] += 1
                    except (json.JSONDecodeError, OSError):
                        pass
                    print(f"  [SKIP] {fname} exists", flush=True)
                    continue

                data, outcome = fetch_rag(spec["query"])
                path = save_raw(drug_id, spec, data)
                ds["files_written"].append(path.name)
                totals["rag_queries_issued"] += 1

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

        # Angle C: EUtils fallback (skip if --rag-only or RAG >= 6/8 OK)
        if args.eutils_only:
            ds["rag_ok"] = ds["rag_ok"]  # untouched
            run_angle_c = True
        elif args.rag_only:
            run_angle_c = False
        else:
            run_angle_c = ds["rag_ok"] < 6
        if run_angle_c:
            ds["eutils_run"] = True
            totals["eutils_runs"] += 1
            term = EUTILS_TERM_TMPL.format(drug=drug_id)
            eutils_result = run_eutils(eutils, term)
            drug_out = OUT_BASE / drug_id
            drug_out.mkdir(parents=True, exist_ok=True)
            efile = drug_out / f"backfill_eutils_{drug_id}.json"
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
            n_arts = len(eutils_result.get("results", [])) if isinstance(eutils_result, dict) else 0
            print(f"  [EUTILS] wrote {efile.name} ({n_arts} articles)", flush=True)
        else:
            print(f"  [EUTILS] not needed (RAG OK = {ds['rag_ok']}/8)", flush=True)

        summary["drugs"][drug_id] = ds

    # Write summary file
    summary["totals"] = totals
    summary["endpoint_errors"] = endpoint_errors
    summary["overwrites"] = "none: all outputs are new backfill_* files"
    summary_path = SCRIPT_DIR / "backfill_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Console report
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for drug_id, ds in summary["drugs"].items():
        nfiles = len(ds["files_written"])
        eutils_tag = ("EUtils: " + ds["eutils_file"]) if ds["eutils_run"] else "EUtils: not needed"
        print(f"  {drug_id:14s} RAG OK {ds['rag_ok']}/8 | still-loading {ds['still_loading_failed']} | "
              f"timeouts {ds['timeout_failed']} | other {ds['other_errors']} | files {nfiles} | {eutils_tag}")
    print("-" * 70)
    print(f"  RAG queries issued: {totals['rag_queries_issued']} | OK: {totals['rag_ok']} | "
          f"still-loading: {totals['still_loading_failed']} | timeouts: {totals['timeout_failed']} | "
          f"other: {totals['other_errors']} | EUtils runs: {totals['eutils_runs']}")
    if endpoint_errors:
        print("  Endpoint errors observed:")
        for e in endpoint_errors:
            print(f"    - {e}")
    print(f"  Summary file: {summary_path}")
    print("  Overwrites: none (all outputs are new backfill_* files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
