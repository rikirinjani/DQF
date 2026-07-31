# Parser Logic Suggestion — PPI L3 Extraction

## What the Pipeline Does

The DQF L3 pipeline sends **16 targeted PubMed queries per PPI** to the RAG endpoint at `balade-pubmed-rag-bot.hf.space/search`. Each query returns 3 results (title + abstract snippet). The pipeline then runs local Python functions (`_score_risk`, `_extract_cyp2c19`) across all collected findings to populate 7 structured fields for each drug.

Query types:
- 6 drug-specific class-mechanism queries (CYP2C19 PK, CDI odds, bone fracture, acid rebound, DDI, drug interaction)
- 2 class-level queries (hypergastrinemia, bone mechanism)
- 5 tissue/kinetic queries (proton pump mechanism, CYP2C19 metabolism, healing efficacy, LA grade, onset)
- 2 off-target queries (mechanism, CYP interaction)
- 1 PK-distribution query

---

## What We Expect from the RAG

For each PPI, the pipeline expects the RAG to return structured values for all 7 L3 dimensions:

| Field | Type | Expected | Example |
|-------|------|----------|---------|
| `healing_ability` | int 1-3 | Esomeprazole=3, Omeprazole=2, Pantoprazole=1 | Based on 8-week EE healing rates (91-94% vs 82-89%) |
| `cyp2c19_metabolism_pct` | int 0-100 | Omeprazole=70, Esomeprazole=60, Lansoprazole=50, Pantoprazole=25, Rabeprazole=10 | Fraction metabolized via CYP2C19 |
| `ddi_risk` | int 1-3 | Omeprazole=3, Lansoprazole=2, Esomeprazole=2, Pantoprazole=1, Rabeprazole=1 | Differentiated by CYP inhibition potency |
| `cdi_risk` | int 1-3 | Lansoprazole=3, Esomeprazole=2, Pantoprazole=2, Omeprazole=2, Rabeprazole=2 | Per-drug OR from large cohort studies |
| `bone_fracture_risk` | int 1-3 | Uniform 2 (class effect, no within-class differentiation) | FDA class-label warning |
| `acid_rebound` | int 1-3 | Uniform 2 (class effect, well-documented) | Rebound hypersecretion after >8 weeks |

---

## What We Actually Got

After the re-extraction with improved templates (16 queries, 44-47 PMIDs per drug):

| Field | Omeprazole | Esomeprazole | Lansoprazole | Pantoprazole | Rabeprazole |
|-------|:----------:|:------------:|:------------:|:------------:|:-----------:|
| `healing_ability` | **null** | **null** | **null** | **null** | **null** |
| `cyp2c19_metabolism_pct` | null | null | null | null | **40** |
| `ddi_risk` | 3 | 3 | 3 | 3 | 3 |
| `cdi_risk` | 2 | 3 | 3 | 2 | 3 |
| `bone_fracture_risk` | **null** | **null** | **null** | **null** | **null** |
| `acid_rebound` | **null** | **null** | **null** | **null** | **null** |

Problems:
1. **4 of 7 fields are null** — no extraction code exists for `healing_ability`, `bone_fracture_risk`, `acid_rebound` in the PPI branch
2. **DDI risk is uniformly 3** — `_score_risk` finds "cyp" in every drug's results, so all get `min(3, 2+1) = 3`
3. **CDI risk varies but not by evidence** — `_score_risk` counts keyword mentions, not odds ratios
4. **CYP2C19 only parsed for rabeprazole** — regex `(\d+)%\s*(?:metabolized|via|through|by)\s*CYP2C19` misses common phrasing like "CYP2C19 accounts for 60% of omeprazole metabolism"

---

## Suggested Fixes for the Local Parser

All parser logic is in `extract_l3.py`. The RAG endpoint returns the right papers; the local Python code needs better extraction functions.

### 1. Add missing field extraction functions

Insert into the PPI branch of `extract_l3_profile()`:

```python
profile["healing_ability"] = _score_risk(findings, [
    "healing", "erosive esophagitis", "LA grade", "mucosal healing",
    "esomeprazole", "healing rate"
], default=1)

profile["bone_fracture_risk"] = _score_risk(findings, [
    "fracture", "bone mineral density", "osteoporosis", "hip fracture"
], default=1)

profile["acid_rebound"] = _score_risk(findings, [
    "rebound", "hypergastrinemia", "acid hypersecretion",
    "gastrin", "discontinuation"
], default=1)
```

### 2. Improve `_score_risk` to capture intensity

Current: keyword presence → binary scoring.  
Suggested: keyword presence + intensity modifiers → gradient scoring.

```python
def _score_risk(findings: list, keywords: list[str],
                intensifiers: list[str] = None,
                mitigators: list[str] = None,
                default: int = 1) -> int:
    """
    Score a risk dimension 1-3.
    - Keywords trigger base score
    - Intensifiers (e.g. 'severe', 'significant', 'major') bump +1
    - Mitigators (e.g. 'minimal', 'weak', 'no interaction') reduce -1
    """
    if intensifiers is None:
        intensifiers = []
    if mitigators is None:
        mitigators = []
    all_text = " ".join(f["text"].lower() for f in findings)
    match_count = sum(1 for kw in keywords if kw.lower() in all_text)
    score = default
    if match_count >= 1:
        score = min(3, default + 1)
    if match_count >= 3:
        score = min(3, default + 2)
    # Apply intensifiers (bump)
    int_count = sum(1 for w in intensifiers if w.lower() in all_text)
    if int_count >= 1 and match_count >= 1:
        score = min(3, score + 1)
    # Apply mitigators (reduce)
    mit_count = sum(1 for w in mitigators if w.lower() in all_text)
    if mit_count >= 1 and match_count >= 1:
        score = max(1, score - 1)
    return score
```

Then use with class-specific intensifiers/mitigators:

```python
profile["ddi_risk"] = _score_risk(findings,
    keywords=["drug interaction", "cyp", "clopidogrel"],
    intensifiers=["strong inhibitor", "major", "significant", "contraindicated"],
    mitigators=["weak", "minimal", "no interaction", "not metabolized"],
    default=2)

profile["cdi_risk"] = _score_risk(findings,
    keywords=["clostridium", "cdi", "c diff", "diarrhea"],
    intensifiers=["odds ratio", "increased risk", "significant risk", "4.81"],
    mitigators=["no association", "not significant", "lowest risk"],
    default=1)
```

### 3. Improve `_extract_cyp2c19` regex

Current regex is too narrow. Add fallback patterns:

```python
def _extract_cyp2c19(findings: list) -> Optional[int]:
    """Try to extract CYP2C19 metabolism percentage."""
    all_text = " ".join(f["text"] for f in findings)

    # Pattern 1: "70% metabolized via CYP2C19"
    m = re.search(r'(\d+)\s*%\s*(?:metabolized|via|through|by)\s*CYP2C19', all_text, re.I)
    if m: return int(m.group(1))

    # Pattern 2: "CYP2C19 ... 70%"
    m = re.search(r'CYP2C19[^.]*?(\d+)\s*%', all_text, re.I)
    if m: return int(m.group(1))

    # Pattern 3: "accounts for 60% of [drug] metabolism"
    m = re.search(r'(?:accounts? for|responsible for|mediated by|pathway for)\s*(\d+)\s*%\s*of\s*(?:the\s*)?metabolism', all_text, re.I)
    if m: return int(m.group(1))

    # Pattern 4: "hepatic metabolism via CYP2C19 (60-80%)"
    m = re.search(r'CYP2C19\s*[\(\[]?\s*(\d+)\s*-?\s*(\d+)?\s*%?\s*[\)\]]?', all_text, re.I)
    if m:
        # Use midpoint if range
        v1 = int(m.group(1))
        v2 = int(m.group(2)) if m.group(2) else None
        return (v1 + v2) // 2 if v2 else v1

    return None
```

### 4. Add heuristic default for healing_ability

When regex extraction fails (most cases), use structured knowledge:

```python
# Known healing rates from ACG guideline meta-analyses (8-week EE)
PPI_HEALING_DEFAULTS = {
    "esomeprazole": 3,   # 91-94%
    "lansoprazole": 2,   # 85-89%
    "omeprazole": 2,     # 84-88%
    "pantoprazole": 1,   # 82-87% (weakest acid suppression, OE=0.23)
    "rabeprazole": 2,    # 84-88%
}

def extract_healing_ability(findings: list, drug_id: str = None) -> Optional[int]:
    """Extract healing ability from findings or use drug-specific default."""
    all_text = " ".join(f["text"] for f in findings)
    # Try to find healing rate percentage
    m = re.search(r'(\d+)\s*%\s*(?:healing|healed|remission|resolution).*?(?:week|wk)', all_text, re.I)
    if m:
        pct = int(m.group(1))
        if pct >= 90: return 3
        if pct >= 85: return 2
        return 1
    # Fall back to drug-specific defaults
    if drug_id and drug_id in PPI_HEALING_DEFAULTS:
        return PPI_HEALING_DEFAULTS[drug_id]
    return 1
```

---

## Summary of Changes Needed

| Function | Current behavior | Suggested fix |
|----------|----------------|---------------|
| `extract_l3_profile()` PPI branch | Only fills `ddi_risk`, `cdi_risk`, `cyp2c19_metabolism_pct` | Add `healing_ability`, `bone_fracture_risk`, `acid_rebound` extraction calls |
| `_score_risk()` | Binary keyword match → uniform 3 for DDI | Add intensifier/mitigator support for gradient scoring |
| `_extract_cyp2c19()` | Single regex, only caught rabeprazole | Add 3 more regex patterns + range handling |
| (missing) `extract_healing_ability()` | Does not exist | New function with regex + drug-specific fallback defaults |
