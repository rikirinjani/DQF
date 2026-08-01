#!/usr/bin/env python3
"""
L3 Systems Response -- Repeatable Extraction Pipeline
=====================================================

Automates the hardest level of the Drug Quantification Framework:
given a drug + its L1 targets, runs targeted PubMed RAG queries and
extracts structured L3 systems-response data.

Usage:
    # Single drug by ID from drugs.json
    python extract_l3.py --drug ibuprofen

    # Single drug with custom targets
    python extract_l3.py --drug warfarin --class Anticoagulant --targets "VKORC1,CYP2C9,Factor II,Factor VII,Factor IX,Factor X"

    # Batch: all drugs in a class
    python extract_l3.py --class NSAID

    # All drugs in drugs.json
    python extract_l3.py --all

    # Dry-run (show queries, don't fetch)
    python extract_l3.py --drug ibuprofen --dry-run

    # Output directory
    python extract_l3.py --drug ibuprofen --out-dir l3_output

    # Skip fetch, re-parse existing RAG results
    python extract_l3.py --drug ibuprofen --reparse

Output:
    l3_output/{drug_id}/  -- raw RAG JSONs + structured L3 profile

Response schema (live endpoint):
    results[] = {id, text, score, doi, journal, year, rerank_score, evidence};
    title is the first line of text; text is hard-capped at 512 chars
    server-side (index-baked), so prefer EUtils path for full abstracts.
"""

import json, os, sys, time, re, xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
import requests


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DRUGS_JSON = PROJECT_DIR / "api" / "drugs.json"
TEMPLATES_JSON = SCRIPT_DIR / "l3_query_templates.json"
RAW_DIR = SCRIPT_DIR / "raw"
DEFAULT_OUT_DIR = SCRIPT_DIR / "l3_output"

RAG_ENDPOINT = "https://balade-pubmed-rag-bot.hf.space/search"
RAG_TOP_K = 3
RAG_DELAY_S = 1.5  # polite delay between queries

# Tokens whose content the endpoint confuses with similarly-prefixed drug
# queries (e.g. methyldopa queries returning methylphenidate/methylone/MDMA).
# A snippet is relevant only if it does NOT contain any of these UNLESS it
# also contains the drug's own name variant (Fix E).
CONFUSABLE_TOKENS = {"methylphenidate", "methylone", "mdma", "methyl-dopa"}

# NCBI EUtils constants
NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
NCBI_API_KEY = os.environ.get("NCBI_API_KEY", "")
NCBI_EMAIL = os.environ.get("NCBI_EMAIL", "dqf-pipeline@example.com")
NCBI_TOOL = "DQFL3Pipeline"
NCBI_RATE_LIMIT = 0.12  # ~8 req/s with key (cushion below 10/s limit)
NCBI_PER_QUERY = 5  # max articles per PubMed query


# ---------------------------------------------------------------------------
# NCBI EUtils Fallback -- PubMedClient
# ---------------------------------------------------------------------------
class PubMedClient:
    """NCBI EUtils client for PubMed search + abstract retrieval."""

    def __init__(self, api_key: str = NCBI_API_KEY, email: str = NCBI_EMAIL,
                 tool: str = NCBI_TOOL, rate_limit: float = NCBI_RATE_LIMIT):
        self.api_key = api_key
        self.email = email
        self.tool = tool
        self.rate_limit = rate_limit
        self._last_req = 0.0
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": f"{tool}/1.0"})

    def _throttle(self):
        elapsed = time.time() - self._last_req
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_req = time.time()

    def _params(self, **kw) -> dict:
        base = {"tool": self.tool, "email": self.email}
        if self.api_key:
            base["api_key"] = self.api_key
        base.update(kw)
        return base

    def search_ids(self, query: str, max_results: int = NCBI_PER_QUERY) -> list[str]:
        """ESearch: query -> list of PMIDs."""
        self._throttle()
        resp = self._session.get(
            f"{NCBI_BASE}/esearch.fcgi",
            params=self._params(db="pubmed", term=query,
                                retmax=min(max_results, 50), retmode="json", sort="relevance"),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("esearchresult", {}).get("idlist", [])

    def fetch_abstracts(self, pmids: list[str]) -> list[dict]:
        """EFetch: PMIDs -> structured article dicts with abstracts."""
        if not pmids:
            return []
        self._throttle()
        resp = self._session.get(
            f"{NCBI_BASE}/efetch.fcgi",
            params=self._params(db="pubmed", id=",".join(pmids),
                                retmode="xml", rettype="abstract"),
            timeout=30,
        )
        resp.raise_for_status()
        return self._parse_xml(resp.text)

    def search(self, query: str, max_results: int = NCBI_PER_QUERY) -> list[dict]:
        """ESearch + EFetch combined."""
        pmids = self.search_ids(query, max_results=max_results)
        return self.fetch_abstracts(pmids)

    def _parse_xml(self, xml_str: str) -> list[dict]:
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

            # Title
            title = ""
            if art_elem is not None and (t := art_elem.find("ArticleTitle")) is not None:
                title = "".join(t.itertext())

            # Abstract
            abstract = ""
            sections = []
            if art_elem is not None and (ab := art_elem.find("Abstract")) is not None:
                for at in ab.findall("AbstractText"):
                    sections.append("".join(at.itertext()))
            abstract = "\n".join(sections)

            # Authors (first 3)
            authors = []
            if art_elem is not None and (al := art_elem.find("AuthorList")) is not None:
                for a in al.findall("Author")[:3]:
                    ln = a.find("LastName")
                    fn = a.find("ForeName")
                    if ln is not None and fn is not None:
                        authors.append(f"{ln.text} {fn.text}")

            # Journal
            journal = ""
            if art_elem is not None and (j := art_elem.find("Journal")) is not None:
                if (t := j.find("Title")) is not None and t.text:
                    journal = t.text

            # DOI
            doi = ""
            if pmd is not None and (il := pmd.find("ArticleIdList")) is not None:
                for aid in il.findall("ArticleId"):
                    if aid.get("IdType") == "doi":
                        doi = aid.text or ""

            # MeSH
            mesh = []
            if (ml := medline.find("MeshHeadingList")) is not None:
                for m in ml.findall("MeshHeading"):
                    if (d := m.find("DescriptorName")) is not None and d.text:
                        mesh.append(d.text)

            # Keywords
            kws = []
            if (kl := medline.find("KeywordList")) is not None:
                for kw in kl.findall("Keyword"):
                    if kw.text:
                        kws.append(kw.text)

            # Pub date
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


def _build_pubmed_query(drug_name: str, query: str) -> str:
    """Build a drug-anchored PubMed query string for NCBI EUtils.

    The anchor forces the drug name into [tiab]/[nm]. Concept terms from the
    template query are OR'd with [tiab] tags (drug name itself and common
    filler words dropped) so the query returns results -- the previous
    implicit AND of 6+ unquoted terms returned 0 for most template queries.
    """
    anchor = f'({drug_name}[tiab] OR {drug_name}[nm])'
    filler = {
        "mechanism", "effect", "risk", "role", "action", "therapy",
        "treatment", "outcome", "benefit", "consequence", "efficacy",
    }
    drug_lower = drug_name.lower()
    concepts = [
        tok for tok in query.lower().split()
        if tok != drug_lower and tok not in filler
    ]
    if concepts:
        concept_side = " OR ".join(f"{tok}[tiab]" for tok in concepts)
    else:
        # No concept terms left -- fall back to raw query minus the drug name
        raw = " ".join(tok for tok in query.split() if tok.lower() != drug_lower)
        if not raw:
            return anchor
        concept_side = raw
    return f"{anchor} AND ({concept_side})"


def pubmed_fallback(query: str, drug_name: str, client: PubMedClient,
                    max_results: int = NCBI_PER_QUERY) -> Optional[dict]:
    """
    Query NCBI EUtils and return results in the same format as the RAG endpoint.
    Translation layer: PubMedClient -> RAG-compatible dict.
    """
    # Build a PubMed-optimized query: drug + concept, restricted to title/abstract
    pubmed_q = _build_pubmed_query(drug_name, query)
    try:
        articles = client.search(pubmed_q, max_results=max_results)
    except requests.RequestException as e:
        print(f"  [PUBMED-FAIL] NCBI EUtils error: {e}", file=sys.stderr)
        return None

    if not articles:
        return None

    results = []
    for art in articles:
        results.append({
            "id": f"PMID:{art['pmid']}",
            "text": art["full_text"],
            "title": art["title"],
            "rerank_score": 1.0 if results else 0.95,  # monotonic decreasing
            "metadata": {
                "pmid": art["pmid"],
                "journal": art["journal"],
                "authors": art["authors"],
                "pub_date": art["pub_date"],
                "doi": art["doi"],
                "mesh_terms": art["mesh_terms"],
            }
        })

    return {"results": results}
def load_drugs() -> dict:
    with open(DRUGS_JSON, encoding="utf-8") as f:
        return json.load(f)


def load_templates() -> dict:
    with open(TEMPLATES_JSON, encoding="utf-8") as f:
        return json.load(f)


def get_drug(drug_id: str) -> Optional[dict]:
    """Find a drug by its 'id' field in drugs.json."""
    data = load_drugs()
    for d in data["drugs"]:
        if d["id"] == drug_id.lower().strip():
            return d
    return None


def get_drugs_by_class(class_name: str) -> list[dict]:
    """Return all drugs matching a given class."""
    data = load_drugs()
    return [d for d in data["drugs"] if d["class"].lower() == class_name.lower().strip()]


# ---------------------------------------------------------------------------
# Query construction
# ---------------------------------------------------------------------------
def build_l3_queries(drug: dict, templates: dict) -> list[dict]:
    """
    Build a list of query specs for this drug.
    Each spec: { "query": str, "dimension": str, "target": str|None }
    """
    drug_name = drug["name"]
    drug_class = drug["class"]
    class_templates = templates.get("classes", {}).get(drug_class, {})

    queries = []

    # 1. Class mechanism queries (always run)
    for q_template in class_templates.get("class_mechanism_queries", []):
        q = q_template.replace("{drug}", drug_name)
        queries.append({
            "query": q,
            "dimension": "class_mechanism",
            "target": None
        })

    # 2. Tissue-specific queries
    for q_template in class_templates.get("tissue_queries", []):
        q = q_template.replace("{drug}", drug_name)
        queries.append({
            "query": q,
            "dimension": "tissue_kinetics",
            "target": None
        })

    # 3. Off-target queries per L1 target
    l1 = drug.get("l1_binding", {})
    targets = l1.get("targets", [])
    off_target_templates = class_templates.get("off_target_queries", [])
    for target in targets:
        tname = target["name"]
        for q_template in off_target_templates:
            q = q_template.replace("{drug}", drug_name).replace("{target}", tname)
            queries.append({
                "query": q,
                "dimension": "off_target",
                "target": tname
            })

    # 4. PK-tissue disconnect query if half-life is notable
    pk = drug.get("l2_pk", {})
    hl = pk.get("half_life_h", 0)
    special = pk.get("special", "")
    if hl < 3 or "synovial" in special.lower() or "tissue" in special.lower() or "enterohepatic" in special.lower():
        queries.append({
            "query": f"{drug_name} tissue concentration half-life distribution pharmacokinetics",
            "dimension": "tissue_kinetics",
            "target": None
        })

    return queries


# ---------------------------------------------------------------------------
# RAG fetch
# ---------------------------------------------------------------------------
def fetch_rag(query: str, top_k: int = RAG_TOP_K,
              retries: int = 2, backoff_s: float = 5.0) -> Optional[dict]:
    """Call the PubMed RAG endpoint. Returns parsed JSON or None.

    The endpoint answers HTTP 200 with {"error": "Still loading"} while a
    cold model spins up. Retry up to `retries` more times with `backoff_s`
    seconds between attempts; if the error persists, return None (callers
    already fall back to NCBI EUtils).
    """
    for attempt in range(retries + 1):
        try:
            resp = requests.get(
                RAG_ENDPOINT,
                params={"q": query, "k": top_k},
                timeout=30
            )
            resp.raise_for_status()
            parsed = resp.json()
        except requests.RequestException as e:
            print(f"  [WARN] RAG fetch failed for '{query[:60]}': {e}", file=sys.stderr)
            return None
        # HTTP 200 but the backend is still warming up -> retry with backoff
        if isinstance(parsed, dict) and isinstance(parsed.get("error"), str) \
                and "loading" in parsed["error"].lower():
            print(f"  [WARN] RAG still loading for '{query[:60]}' "
                  f"(attempt {attempt + 1}/{retries + 1}, backoff {backoff_s}s): "
                  f"{parsed['error']}", file=sys.stderr)
            if attempt < retries:
                time.sleep(backoff_s)
                continue
            return None
        return parsed
    return None


def save_raw(drug_id: str, query_spec: dict, result: dict, out_dir: Path, source: str = "rag"):
    """Save raw RAG JSON response to disk.

    `source` records provenance per record ("rag" or "eutils") so evidence
    pools can be audited unambiguously (canonical-store minimal step).
    """
    slug = re.sub(r'[^a-z0-9]+', '_', query_spec["query"].lower())[:60]
    drug_out = out_dir / drug_id
    drug_out.mkdir(parents=True, exist_ok=True)
    path = drug_out / f"{slug}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "query": query_spec,
            "source": source,
            "result": result
        }, f, indent=2, ensure_ascii=False)
    return path


# ---------------------------------------------------------------------------
# Extraction -- RAG results -> structured L3 data
# ---------------------------------------------------------------------------
# Lazily-built set of every drug name in drugs.json (lowercased). Used by the
# co-mention relevance rule: a head-to-head comparison trial mentions the
# subject drug once alongside a comparator, and the comparator is (almost
# always) another drug from the framework's own list.
_OTHER_DRUG_NAMES = None  # module-level lazy cache (Fix C)


def _get_other_drug_names(current_drug_name: str) -> set:
    """All drug names from load_drugs(), minus the current drug's own name.

    Built lazily on first use and cached module-wide. Class words and other
    non-drug words never enter the set (it is derived from drug names only),
    and callers only count mentions of length >= 4 to avoid noise.
    """
    global _OTHER_DRUG_NAMES
    if _OTHER_DRUG_NAMES is None:
        try:
            data = load_drugs()
            _OTHER_DRUG_NAMES = {
                str(d.get("name", "")).lower()
                for d in data.get("drugs", []) if d.get("name")
            }
        except Exception:
            _OTHER_DRUG_NAMES = set()
    own = (current_drug_name or "").lower()
    return {n for n in _OTHER_DRUG_NAMES if n and n != own}


def _snippet_relevant(drug: dict, text: str, title: str = "") -> bool:
    """Relevance gate: is this snippet really about the drug? (Fix C + Fix E)

    Keep iff:
      1. a drug-name variant appears in the TITLE (authoritative), OR
      2. a drug-name variant appears >=1 in title+text AND at least one
         OTHER drug name (len >= 4, from the full drug list) co-occurs in
         title+text -- a head-to-head comparison trial, OR
      3. a drug-name variant appears >=2 across title+text (current rule).
    Otherwise drop.

    Confusable-token filter (Fix E): a snippet is relevant only if it does
    NOT contain any CONFUSABLE_TOKENS (methylphenidate/methylone/mdma/
    methyl-dopa) UNLESS it also contains the drug's own name variant --
    e.g. a methyldopa query returning methylphenidate content is dropped
    unless methyldopa itself is also mentioned.
    """
    text_lower = text.lower()
    title_lower = (title or "").lower()
    drug_name_lower = (drug.get("name") or "").lower()
    drug_id_lower = (drug.get("id") or "").lower()
    drug_name_tokens = drug_name_lower.split()
    first_token = drug_name_tokens[0] if drug_name_tokens else ""
    # Accept the first token of the name (e.g. "hydrochlorothiazide") when
    # the name has multiple tokens.
    accept_first_token = len(drug_name_tokens) > 1

    def _variant_count(hay_lower: str) -> int:
        c = 0
        if drug_name_lower:
            c += hay_lower.count(drug_name_lower)
        if drug_id_lower and drug_id_lower != drug_name_lower:
            c += hay_lower.count(drug_id_lower)
        if accept_first_token and first_token and first_token != drug_name_lower:
            c += hay_lower.count(first_token)
        return c

    title_count = _variant_count(title_lower)
    total_count = title_count + _variant_count(text_lower)

    # Fix E: confusable content decides relevance on its own -- a snippet
    # containing a confusable token (methylphenidate/methylone/mdma/
    # methyl-dopa) is relevant iff the drug's own name variant is also
    # present: "methyldopa snippet mentioning methylphenidate but NOT
    # methyldopa -> drop; mentioning both -> keep".
    combined = f"{title_lower}\n{text_lower}"
    if any(tok in combined for tok in CONFUSABLE_TOKENS):
        return total_count >= 1

    # Fix C: keep iff drug variant in TITLE, OR (>=1 mention AND another
    # drug name co-occurs -- head-to-head comparison trial), OR >=2 mentions.
    if title_count >= 1:
        return True
    if total_count >= 1:
        for other in _get_other_drug_names(drug_name_lower):
            if len(other) >= 4 and (other in title_lower or other in text_lower):
                return True
    return total_count >= 2


def extract_l3_profile(drug: dict, raw_files: list[Path], templates: dict) -> dict:
    """
    Parse all raw RAG results for a drug and build a structured L3 profile.
    Returns a dict matching the drugs.json l3_systems schema.
    """
    drug_class = drug["class"]
    class_templates = templates.get("classes", {}).get(drug_class, {})
    l3_schema = class_templates.get("l3_fields", {}).copy()

    # Collect all extracted PMIDs + snippets
    all_pmids = set()
    findings = []  # list of {"pmid": str, "finding": str, "dimension": str}

    # Drug-name relevance gate: the RAG endpoint embeds query concepts only
    # (it ignores drug names), so off-drug papers must be filtered BEFORE
    # scoring. Track pool relevance for evidence + threshold fallback.
    total_snippets = 0
    relevant_snippets = 0
    dup_pmids_skipped = 0  # Fix B: PMIDs re-returned across query files

    for rf in raw_files:
        try:
            with open(rf, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            continue

        # Handle two formats:
        #   New format: {"query": {...}, "result": {"results": [...]}}
        #   Legacy format (from original PoC): {"results": [...]}
        if "results" in data and isinstance(data["results"], list):
            # Legacy format -- no query metadata
            query_spec = {"dimension": "legacy", "target": None}
            query_text = rf.stem.replace("_", " ").replace("-", " ")
            results_list = data["results"]
        elif "result" in data:
            query_spec = data.get("query", {})
            query_text = query_spec.get("query", rf.stem)
            result = data["result"]
            results_list = result.get("results", []) if isinstance(result, dict) else []
        else:
            continue

        dimension = query_spec.get("dimension", "unknown")

        for r in results_list:
            pmid = r.get("id", "").replace("PMID:", "")
            text = r.get("text", "")
            if pmid:
                total_snippets += 1
                # Relevance gate (shared _snippet_relevant): keep a snippet
                # only if the drug is clearly the SUBJECT, not a passing
                # mention -- title match, OR single mention alongside a
                # comparator drug (co-mention comparison trial), OR >=2
                # mentions. Confusable content (Fix E) is filtered inside.
                if not _snippet_relevant(drug, text, r.get("title") or ""):
                    continue
                relevant_snippets += 1
                if pmid in all_pmids:
                    # Fix B: the endpoint re-returns the same paper across
                    # query angles -- count it toward stats but do NOT append
                    # a duplicate finding (evidence payload must stay unique).
                    dup_pmids_skipped += 1
                    continue
                all_pmids.add(pmid)
                findings.append({
                    "pmid": pmid,
                    "text": text,  # Fix A: full text, no [:300] truncation
                    "dimension": dimension,
                    "score": r.get("rerank_score", 0)
                })

    # Build structured profile
    profile = l3_schema.copy()

    # Fill in the fields that apply to this class
    if drug_class == "NSAID":
        profile["off_targets"] = _extract_off_targets(findings, drug)
        profile["gi_risk"] = _score_risk(findings, ["gastric", "bleeding", "mucosal", "gi_risk"], default=2)
        profile["cv_risk"] = _score_risk(findings, ["cardiovascular", "thrombosis", "mace", "cv_risk"], default=1)
        profile["renal_risk"] = _score_risk(findings, ["renal", "kidney", "prostaglandin"], default=1)
        profile["ddi_risk"] = _score_risk(findings, ["drug interaction", "cyp", "warfarin"], default=1)

    elif drug_class == "Statin":
        profile["myopathy_risk"] = _score_risk(findings, ["myopathy", "muscle", "rhabdomyolysis"], default=2)
        profile["ddi_risk"] = _score_risk(findings, ["drug interaction", "cyp3a4", "oatp"], default=1)
        profile["pleiotropic_effects"] = _extract_pleiotropic(findings)

    elif drug_class == "PPI":
        drug_id = drug.get("id")
        drug_name = drug.get("name", "")
        profile["healing_ability"] = extract_healing_ability(findings, drug_id=drug_id)
        # CYP2C19: try regex on RAG snippets, then full-text NCBI fetch, then known defaults
        cyp_val = _extract_cyp2c19(findings, drug_id=drug_id)
        if cyp_val is None:
            cyp_val = _fetch_cyp2c19_fulltext(drug_name)
        profile["cyp2c19_metabolism_pct"] = cyp_val
        profile["ddi_risk"] = _score_risk(findings,
            keywords=["drug interaction", "cyp", "clopidogrel"],
            intensifiers=["strong inhibitor", "major", "significant", "contraindicated"],
            mitigators=["weak", "minimal", "no interaction", "not metabolized"],
            default=2)
        profile["cdi_risk"] = _score_risk(findings,
            keywords=["clostridium", "cdi", "c diff", "diarrhea"],
            intensifiers=["odds ratio", "increased risk", "significant risk", "4.81"],
            mitigators=["no association", "not significant", "lowest"],
            default=1)
        profile["bone_fracture_risk"] = _score_risk(findings,
            keywords=["fracture", "bone mineral density", "osteoporosis", "hip fracture", "bone"],
            default=1)
        profile["acid_rebound"] = _score_risk(findings,
            keywords=["rebound", "hypergastrinemia", "acid hypersecretion", "gastrin"],
            intensifiers=["significant", "marked", "clinically relevant"],
            default=1)

    elif drug_class == "Antihypertensive":
        profile["bp_reduction"] = _score_risk(findings,
            keywords=["bp reduction", "blood pressure", "antihypertensive", "systolic", "diastolic"],
            intensifiers=["superior", "greater reduction", "most effective", "first-line"],
            mitigators=["modest", "mild", "minimal reduction", "no better than"],
            default=2)
        profile["renal_protection"] = _score_risk(findings,
            keywords=["renal", "nephropathy", "kidney", "proteinuria", "albuminuria", "creatinine"],
            intensifiers=["significant", "protective", "renoprotective", "delay", "slow progression"],
            mitigators=["no benefit", "no protection", "no effect"],
            default=1)
        profile["metabolic_effect"] = _score_risk(findings,
            keywords=["glucose", "lipid", "uric acid", "metabolic", "diabetes", "insulin", "potassium", "sodium"],
            intensifiers=["neutral", "favorable", "beneficial", "improved"],
            mitigators=["unfavorable", "hyperglycemia", "hyperuricemia", "hypokalemia", "dyslipidemia"],
            default=2)
        profile["electrolyte_risk"] = _score_risk(findings,
            keywords=["hyperkalemia", "hypokalemia", "hyponatremia", "electrolyte", "potassium", "sodium"],
            intensifiers=["severe", "significant", "life-threatening", "hospitalization"],
            mitigators=["no significant", "mild", "transient", "well-tolerated"],
            default=1)
        profile["ddi_risk"] = _score_risk(findings,
            keywords=["drug interaction", "interaction", "NSAID", "diuretic", "ACE inhibitor", "ARB"],
            intensifiers=["contraindicated", "significant", "major", "caution"],
            mitigators=["no interaction", "safe", "well-tolerated", "minimal"],
            default=1)
        profile["heart_rate_effect"] = _check_heart_rate(findings)

    elif drug_class == "Diabetes":
        profile["a1c_reduction"] = _score_risk(findings,
            keywords=["a1c", "glycemic", "hemoglobin a1c", "glucose", "glycemic control", "hyperglycemia"],
            intensifiers=["superior", "greater reduction", "most effective", "significant reduction", "1.5%"],
            mitigators=["modest", "mild reduction", "inferior", "no better than"],
            default=2)
        profile["weight_effect"] = _score_weight_effect(findings)
        profile["cv_outcome_benefit"] = _score_risk(findings,
            keywords=["cardiovascular", "mace", "mortality", "heart failure", "cv death", "myocardial infarction", "stroke"],
            intensifiers=["significant reduction", "benefit", "protective", "reduced risk", "superior", "-14%", "-26%", "-38%"],
            mitigators=["no benefit", "no difference", "neutral", "non-inferior", "no effect"],
            default=1)
        profile["renal_benefit"] = _score_risk(findings,
            keywords=["renal", "kidney", "nephropathy", "egfr", "albuminuria", "proteinuria", "ckd", "creatinine"],
            intensifiers=["significant", "protective", "slow progression", "renoprotective", "reduced"],
            mitigators=["no benefit", "no effect", "no difference", "no protection"],
            default=1)
        profile["gi_tolerability"] = _score_risk(findings,
            keywords=["nausea", "vomiting", "diarrhea", "gi", "gastrointestinal", "abdominal", "dyspepsia"],
            intensifiers=["severe", "intolerable", "discontinuation", "high rate", "frequent"],
            mitigators=["well-tolerated", "mild", "transient", "low rate", "no significant"],
            default=2)
        profile["ddi_risk"] = _score_risk(findings,
            keywords=["drug interaction", "interaction", "renal clearance", "tubular secretion", "contrast"],
            intensifiers=["significant", "contraindicated", "caution", "major"],
            mitigators=["no interaction", "no significant", "safe", "well-tolerated"],
            default=1)
        profile["hypoglycemia_risk"] = _score_risk(findings,
            keywords=["hypoglycemia", "low blood glucose", "severe hypoglycemia", "glucose <70", "hypoglycemic"],
            intensifiers=["high risk", "frequent", "severe", "significant", "increased"],
            mitigators=["low risk", "minimal", "no increased", "rare", "no significant"],
            default=2)

    elif drug_class == "H2RA":
        profile["ddi_risk"] = _score_risk(findings, ["cyp", "drug interaction", "theophylline"], default=1)
        profile["tolerance"] = _check_tolerance(findings)
        profile["cns_penetration"] = _check_cns(findings)
        profile["off_targets"] = _extract_off_targets(findings, drug)

    pool_relevance_pct = round(100 * relevant_snippets / total_snippets, 1) if total_snippets else 0.0
    profile["_evidence"] = {
        "pmids": sorted(all_pmids),
        "source_count": len(raw_files),
        "finding_count": len(findings),
        "dup_pmids_skipped": dup_pmids_skipped,
        "pool_relevance_pct": pool_relevance_pct,
        "filtered_off_drug": total_snippets - relevant_snippets,
        "relevance_gate": "pass" if pool_relevance_pct >= 30 else "flag",
    }
    profile["_note"] = "Auto-extracted by L3 pipeline. Review before merging into drugs.json."

    return profile


def _extract_off_targets(findings: list, drug: dict) -> list:
    """Identify off-targets mentioned in RAG results beyond the drug's primary targets."""
    known_targets = {t["name"].lower() for t in drug.get("l1_binding", {}).get("targets", [])}
    known_kw = {"cox-1", "cox-2", "cox", "hmgcr", "h+/k+-atpase", "h2 receptor"}
    # Generic words that appear in text but aren't target names
    stop_words = {"ion", "cation", "transient", "putative", "novel", "target", "site", "mediated",
                  "current", "function", "cell", "human", "potent", "key", "direct", "type",
                  "alternative", "multiple", "specific", "partial", "full", "acid"}

    off_targets = set()
    for f in findings:
        text_lower = f["text"].lower()
        # Look for target-like patterns: "{name} receptor", "{name} channel", etc.
        targets_found = re.findall(r'(\w[\w/-]+)\s+(receptor|channel|antagonist|agonist)', text_lower)
        for name, _ in targets_found:
            name = name.strip().lower()
            if (name not in known_targets and name not in known_kw
                    and len(name) > 3 and name not in stop_words):
                off_targets.add(name.title())

    return sorted(off_targets)[:6]  # cap at 6


def _score_risk(findings: list, keywords: list[str], default: int = 1,
                intensifiers: list[str] = None,
                mitigators: list[str] = None) -> int:
    """Score a risk dimension 1-3 based on keyword density + intensity modifiers.

    Keywords trigger base score. Intensifiers (e.g. 'severe', 'major') bump +1.
    Mitigators (e.g. 'minimal', 'weak') reduce -1.
    """
    if intensifiers is None:
        intensifiers = []
    if mitigators is None:
        mitigators = []
    score = default
    all_text = " ".join(f["text"].lower() for f in findings)
    match_count = sum(1 for kw in keywords if kw.lower() in all_text)
    if match_count >= 3:
        score = min(3, default + 2)
    elif match_count >= 1:
        score = min(3, default + 1)
    # Apply intensifiers (bump if keywords also matched)
    if match_count >= 1:
        int_count = sum(1 for w in intensifiers if w.lower() in all_text)
        if int_count >= 1:
            score = min(3, score + 1)
        # Apply mitigators (reduce)
        mit_count = sum(1 for w in mitigators if w.lower() in all_text)
        if mit_count >= 1:
            score = max(1, score - 1)
    return score


def _extract_cyp2c19(findings: list, drug_id: str = None, drug_name: str = None) -> Optional[int]:
    """Try to extract CYP2C19 metabolism percentage from RAG findings.

    Tries multiple regex patterns in order of specificity. Falls back to
    known drug-specific defaults for PPIs (well-established PK constants).

    Regex handles:
      - "70% metabolized via CYP2C19"
      - "CYP2C19 accounts for 60% of metabolism"
      - "hepatic metabolism via CYP2C19 (60-80%)"
    """
    # Known defaults: well-established PK constants from FDA labeling + clinical literature
    # These are stable reference values, not evidence-extracted.
    PPI_CYP2C19_DEFAULTS = {
        "omeprazole": 70,    # primary CYP2C19 substrate, ~70% metabolized via CYP2C19
        "esomeprazole": 60,  # S-isomer, less CYP2C19-dependent than omeprazole
        "lansoprazole": 50,  # metabolized by both CYP2C19 (~50%) and CYP3A4 (~50%)
        "pantoprazole": 25,  # CYP2C19 + CYP3A4 + cytosolic sulfotransferase escape
        "rabeprazole": 10,   # primarily non-enzymatic thioether reduction; CYP minor
    }

    all_text = " ".join(f["text"] for f in findings)

    # Pattern 1: "70% metabolized via CYP2C19"
    m = re.search(r'(\d+)\s*%\s*(?:metabolized|via|through|by)\s*CYP2C19', all_text, re.I)
    if m:
        return int(m.group(1))

    # Pattern 2: "CYP2C19 ... 70%"
    m = re.search(r'CYP2C19[^.]*?(\d+)\s*%', all_text, re.I)
    if m:
        return int(m.group(1))

    # Pattern 3: "accounts for 60% of [drug] metabolism"
    m = re.search(r'(?:accounts? for|responsible for|mediated by|pathway for)\s*(\d+)\s*%\s*of\s*(?:the\s*)?metabolism', all_text, re.I)
    if m:
        return int(m.group(1))

    # Pattern 4: "CYP2C19 (60-80%)" or "CYP2C19: 60-80%"
    m = re.search(r'CYP2C19\s*[\(\:\s]+(\d+)\s*-?\s*(\d+)?\s*%', all_text, re.I)
    if m:
        v1 = int(m.group(1))
        v2 = int(m.group(2)) if m.group(2) else None
        return (v1 + v2) // 2 if v2 else v1

    # Fallback: known defaults per drug (well-established PK constants)
    if drug_id and drug_id.lower() in PPI_CYP2C19_DEFAULTS:
        return PPI_CYP2C19_DEFAULTS[drug_id.lower()]

    return None


def _fetch_cyp2c19_fulltext(drug_name: str) -> Optional[int]:
    """Secondary pass: fetch full PubMed abstracts for CYP2C19 metabolism.

    Called when regex on RAG snippets returns None. Uses NCBI EUtils with
    module-level API key. Full abstracts are typically long enough to
    contain the metabolism fraction (mid-abstract PK section).
    """
    if not drug_name:
        return None

    # Build NCBI search query
    query = f'({drug_name}[tiab] OR {drug_name}[nm]) AND (CYP2C19[tiab] AND (metabolism OR pharmacokinetics OR fraction))'
    params = {
        "db": "pubmed", "term": query, "retmax": "3",
        "retmode": "json", "sort": "relevance",
        "tool": NCBI_TOOL, "email": NCBI_EMAIL,
    }
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY

    try:
        # ESearch
        time.sleep(NCBI_RATE_LIMIT)
        resp = requests.get(f"{NCBI_BASE}/esearch.fcgi", params=params, timeout=30)
        resp.raise_for_status()
        ids = resp.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return None

        # EFetch full abstracts
        time.sleep(NCBI_RATE_LIMIT)
        fetch_params = {
            "db": "pubmed", "id": ",".join(ids[:2]),
            "retmode": "xml", "rettype": "abstract",
            "tool": NCBI_TOOL, "email": NCBI_EMAIL,
        }
        if NCBI_API_KEY:
            fetch_params["api_key"] = NCBI_API_KEY
        resp2 = requests.get(f"{NCBI_BASE}/efetch.fcgi", params=fetch_params, timeout=30)
        resp2.raise_for_status()

        # Parse XML for full text
        root = ET.fromstring(resp2.text)
        full_text = ""
        for art in root.findall("PubmedArticle"):
            medline = art.find("MedlineCitation")
            if medline is None:
                continue
            art_elem = medline.find("Article")
            title = ""
            if art_elem is not None and (t := art_elem.find("ArticleTitle")) is not None:
                title = "".join(t.itertext())
            abstract = ""
            if art_elem is not None and (ab := art_elem.find("Abstract")) is not None:
                sections = ["".join(at.itertext()) for at in ab.findall("AbstractText")]
                abstract = "\n".join(sections)
            full_text += f"{title}\n\n{abstract}\n\n"

        if not full_text:
            return None

        # Build a pseudo-findings list and re-run regex
        findings = [{"text": full_text}]
        return _extract_cyp2c19(findings)

    except (requests.RequestException, json.JSONDecodeError, ET.ParseError):
        return None


def extract_healing_ability(findings: list, drug_id: str = None) -> Optional[int]:
    """Extract healing ability (1-3) from RAG findings.

    Attempts to find healing rate percentages in evidence. Falls back to
    known drug-specific defaults from ACG/AGA guideline meta-analyses
    (8-week erosive esophagitis healing rates).
    """
    PPI_HEALING_DEFAULTS = {
        "esomeprazole": 3,   # 91-94% (most potent acid suppression)
        "lansoprazole": 2,   # 85-89%
        "omeprazole": 2,     # 84-88%
        "pantoprazole": 1,   # 82-87% (weakest acid suppression, OE=0.23)
        "rabeprazole": 2,    # 84-88%
    }

    all_text = " ".join(f["text"] for f in findings)

    # Pattern 1: "90% healing" or "healing rate 88%"
    m = re.search(r'(\d+)\s*%\s*(?:healing|healed|remission|resolution)', all_text, re.I)
    if m:
        pct = int(m.group(1))
        if pct >= 90:
            return 3
        if pct >= 84:
            return 2
        return 1

    # Pattern 2: "healing ... 90%" or "healing rate of 90%"
    m = re.search(r'(?:healing|healed)\s*(?:efficacy|rate)?\s*(?:is|of|:|\s)\s*(\d+)\s*%', all_text, re.I)
    if m:
        pct = int(m.group(1))
        if pct >= 90:
            return 3
        if pct >= 84:
            return 2
        return 1

    # Fallback: known defaults per drug
    if drug_id and drug_id.lower() in PPI_HEALING_DEFAULTS:
        return PPI_HEALING_DEFAULTS[drug_id.lower()]

    return None


def _check_tolerance(findings: list) -> bool:
    """Check for tolerance/tachyphylaxis evidence."""
    all_text = " ".join(f["text"].lower() for f in findings)
    return "tolerance" in all_text or "tachyphylaxis" in all_text


def _check_cns(findings: list) -> bool:
    """Check for CNS penetration evidence."""
    all_text = " ".join(f["text"].lower() for f in findings)
    return "cns" in all_text or "central nervous" in all_text or "blood-brain" in all_text


def _check_heart_rate(findings: list) -> str:
    """Determine heart rate effect from evidence: bradycardia, tachycardia, or none."""
    all_text = " ".join(f["text"].lower() for f in findings)
    brady_kw = ["bradycardia", "heart rate reduction", "negative chronotropic", "slow heart", "decreased heart rate"]
    tachy_kw = ["tachycardia", "reflex tachycardia", "increased heart rate", "palpitations", "heart rate increase"]
    for kw in brady_kw:
        if kw in all_text:
            return "bradycardia"
    for kw in tachy_kw:
        if kw in all_text:
            return "tachycardia"
    return "none"


def _score_weight_effect(findings: list) -> int:
    """Score weight effect: 1=weight gain, 2=neutral, 3=weight loss.
    Uses keyword matching across all evidence text."""
    all_text = " ".join(f["text"].lower() for f in findings)
    loss_kw = ["weight loss", "weight reduction", "decreased weight", "weight decrease",
               "lost weight", "reduced weight", "body weight reduction"]
    gain_kw = ["weight gain", "weight increase", "increased weight", "weight gain",
               "body weight increase", "edema"]
    has_loss = any(kw in all_text for kw in loss_kw)
    has_gain = any(kw in all_text for kw in gain_kw)
    if has_loss and not has_gain:
        return 3
    if has_gain and not has_loss:
        return 1
    # Both mentioned or neither → neutral
    return 2


def _extract_pleiotropic(findings: list) -> list:
    """Extract pleiotropic effect mentions for statins."""
    effects = set()
    keywords = ["endothelial", "anti-inflammatory", "antioxidant", "plaque", "smooth muscle",
                "vascular", "thrombosis", "immunomodulatory"]
    all_text = " ".join(f["text"].lower() for f in findings)
    for kw in keywords:
        if kw in all_text:
            effects.add(kw.title())
    return sorted(effects)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def write_profile(drug_id: str, profile: dict, out_dir: Path):
    """Write the structured L3 profile to disk."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{drug_id}_l3_profile.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    print(f"  Wrote L3 profile: {path}")
    return path


def write_summary(all_profiles: dict, out_dir: Path):
    """Write a summary report comparing all extracted L3 profiles."""
    summary = {
        "pipeline": "L3 Systems Response Extractor v1.0",
        "source": str(DRUGS_JSON),
        "drugs": {}
    }
    for drug_id, profile in all_profiles.items():
        evidence = profile.pop("_evidence", {})
        note = profile.pop("_note", "")
        summary["drugs"][drug_id] = {
            "pmids": evidence.get("pmids", []),
            "pmid_count": len(evidence.get("pmids", [])),
            "source_count": evidence.get("source_count", 0),
            "fields_populated": sum(1 for v in profile.values() if v is not None and v != []),
            "note": note
        }
        # Restore evidence
        profile["_evidence"] = evidence
        profile["_note"] = note

    path = out_dir / "_summary.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"  Wrote summary: {path}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run_pipeline(drug: dict, templates: dict, out_dir: Path,
                 dry_run: bool = False, reparse: bool = False,
                 pubmed_client: Optional[PubMedClient] = None,
                 pubmed_only: bool = False):
    """Run the full L3 extraction pipeline for one drug."""
    drug_id = drug["id"]
    drug_name = drug["name"]
    drug_class = drug["class"]
    print(f"\n{'='*60}")
    print(f"  L3 Pipeline: {drug_name} ({drug_id}) -- {drug_class}")
    print(f"{'='*60}")

    # Build queries
    queries = build_l3_queries(drug, templates)
    print(f"  Queries generated: {len(queries)}")
    for i, q in enumerate(queries):
        print(f"    {i+1:2d}. [{q['dimension']:20s}] {q['query'][:80]}")

    if dry_run:
        print("  [DRY RUN -- no fetch, no write]")
        return None

    # Fetch
    raw_files = []
    if reparse:
        # Load existing raw files -- check both new (l3_output/{drug}/) and legacy (raw/) locations
        search_dirs = [out_dir / drug_id, RAW_DIR]
        for d in search_dirs:
            if not d.exists():
                continue
            if d == RAW_DIR:
                drug_name_lower = drug.get("name", drug_id).lower().replace(" ", "-")
                found = sorted(d.glob(f"{drug_id}*.json")) + sorted(d.glob(f"{drug_name_lower}*.json"))
                seen = set()
                unique = []
                for f in found:
                    if f.name not in seen:
                        seen.add(f.name)
                        unique.append(f)
                found = unique
            else:
                found = sorted(d.glob("*.json"))
            raw_files.extend(found)
        if raw_files:
            print(f"  Reparsing {len(raw_files)} existing raw files...")
        else:
            print(f"  No existing raw files for {drug_id}")
    else:
        print(f"  Fetching {len(queries)} RAG queries...")
        for i, qs in enumerate(queries):
            print(f"    [{i+1}/{len(queries)}] {qs['query'][:70]}...", end=" ", flush=True)
            result = None
            result_source = "rag"
            if not pubmed_only:
                result = fetch_rag(qs["query"])
            if result is None and pubmed_client is not None:
                # Fallback to NCBI EUtils
                result = pubmed_fallback(qs["query"], drug_name, pubmed_client)
                if result:
                    result_source = "eutils"
                    print(f"PubMed OK ({len(result.get('results',[]))} res)")
                else:
                    print("PUBMED-FAIL")
            elif result:
                n = len(result.get("results", []))
                print(f"RAG OK ({n} results)")
            else:
                print("FAIL")

            if result:
                path = save_raw(drug_id, qs, result, out_dir, source=result_source)
                raw_files.append(path)
            if i < len(queries) - 1:
                time.sleep(RAG_DELAY_S)

    # Extract
    if raw_files:
        profile = extract_l3_profile(drug, raw_files, templates)

        # Threshold-triggered EUtils refetch: the RAG endpoint embeds query
        # concepts only, so a low pool_relevance_pct means the pool is mostly
        # off-drug papers. Re-query PubMed directly, anchored on the drug name.
        pool_relevance_pct = profile.get("_evidence", {}).get("pool_relevance_pct", 0)
        if pool_relevance_pct < 30:
            if pubmed_client is None:
                pubmed_client = PubMedClient(api_key=NCBI_API_KEY, email=NCBI_EMAIL)
            if pubmed_client is not None:
                print(f"  [RELEVANCE] pool at {pool_relevance_pct}% < 30% \u2014 refetching via NCBI EUtils")
                eutils_files = []
                for i, qs in enumerate(queries):
                    result = pubmed_fallback(qs["query"], drug_name, pubmed_client)
                    if result:
                        path = save_raw(drug_id, qs, result, out_dir, source="eutils")
                        eutils_files.append(path)
                    if i < len(queries) - 1:
                        time.sleep(RAG_DELAY_S)
                if eutils_files:
                    profile = extract_l3_profile(drug, eutils_files, templates)
                    profile["_evidence"]["source"] = "pubmed_eutils_refetch"
                else:
                    print("  [RELEVANCE] EUtils refetch returned no results -- keeping original profile")

        write_profile(drug_id, profile, out_dir)
        return profile
    else:
        print(f"  No data to extract for {drug_id}")
        return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="L3 Systems Response Extraction Pipeline")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--drug", help="Drug ID (e.g., ibuprofen)")
    group.add_argument("--class", dest="drug_class", help="Drug class (e.g., NSAID, Statin)")
    group.add_argument("--all", action="store_true", help="Run for all drugs in drugs.json")
    parser.add_argument("--targets", help="Comma-separated L1 target names (for custom drugs not in drugs.json)")
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR, type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Show queries without fetching")
    parser.add_argument("--reparse", action="store_true", help="Skip fetch, re-parse existing raw files")
    parser.add_argument("--pubmed-only", action="store_true",
                        help="Use NCBI EUtils only (skip RAG endpoint entirely). "
                             "Set NCBI_API_KEY and NCBI_EMAIL env vars for best rate limits.")
    parser.add_argument("--eutils-first", action="store_true",
                        help="First-class EUtils mode (drug-anchored, full abstracts). "
                             "Alias for --pubmed-only.")
    args = parser.parse_args()

    # --eutils-first is an alias for --pubmed-only: skip the RAG endpoint
    # entirely per-query and go straight to the NCBI EUtils fallback. Alias at
    # the args level so the pipeline logic is not duplicated.
    if args.eutils_first:
        args.pubmed_only = True

    templates = load_templates()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # Prepare PubMed Client if pubmed-only or fallback may be needed
    pubmed_client = None
    if args.pubmed_only or not args.reparse:
        if NCBI_API_KEY:
            pubmed_client = PubMedClient(api_key=NCBI_API_KEY, email=NCBI_EMAIL)
            if args.pubmed_only:
                print(f"  [INFO] Using NCBI EUtils fallback (key set, {NCBI_EMAIL})")
        else:
            if args.pubmed_only:
                print("  [WARN] --pubmed-only set but no NCBI_API_KEY env var. "
                      "Rate limited to 3 req/s. Set NCBI_API_KEY for 10 req/s.")
                pubmed_client = PubMedClient(api_key="", email=NCBI_EMAIL)

    if args.drug:
        drugs = [get_drug(args.drug)]
        if not drugs[0]:
            # Custom drug not in drugs.json
            drug = {"id": args.drug, "name": args.drug.capitalize(), "class": "NSAID"}
            if args.targets:
                drug["l1_binding"] = {
                    "targets": [{"name": t.strip()} for t in args.targets.split(",")]
                }
            drugs = [drug]
            # Try to infer class
            templates_list = load_templates()
            print("  [INFO] Drug not in drugs.json -- using custom targets. Specify --class if not NSAID.")
    elif args.drug_class:
        drugs = get_drugs_by_class(args.drug_class)
        if not drugs:
            print(f"  No drugs found for class '{args.drug_class}'")
            return
        print(f"  Found {len(drugs)} drugs in class '{args.drug_class}'")
        # Skip drugs that already have a profile
        existing_count = 0
        filtered = []
        for d in drugs:
            profile_path = args.out_dir / f"{d['id']}_l3_profile.json"
            if profile_path.exists():
                existing_count += 1
            else:
                filtered.append(d)
        if existing_count:
            print(f"  Skipping {existing_count} drugs with existing profiles (re-run with --force to override)")
        drugs = filtered
    elif args.all:
        data = load_drugs()
        drugs = data["drugs"]
        print(f"  Found {len(drugs)} total drugs")
        # Skip drugs that already have a profile
        existing_count = 0
        filtered = []
        for d in drugs:
            profile_path = args.out_dir / f"{d['id']}_l3_profile.json"
            if profile_path.exists():
                existing_count += 1
            else:
                filtered.append(d)
        if existing_count:
            print(f"  Skipping {existing_count} drugs with existing profiles (use --force to override)")
        drugs = filtered

    all_profiles = {}
    failed = []
    for drug in drugs:
        try:
            profile = run_pipeline(drug, templates, args.out_dir,
                                   args.dry_run, args.reparse, pubmed_client,
                                   args.pubmed_only)
            if profile:
                all_profiles[drug["id"]] = profile
        except Exception as e:
            print(f"  [ERROR] Pipeline failed for {drug.get('id', '?')}: {e}", file=sys.stderr)
            failed.append(drug.get("id", "?"))

    if all_profiles:
        write_summary(all_profiles, args.out_dir)

    if failed:
        print(f"\n  FAILED: {len(failed)} drugs -- {', '.join(failed)}", file=sys.stderr)
    print(f"\n  Done. Profiles in: {args.out_dir}")


if __name__ == "__main__":
    main()
