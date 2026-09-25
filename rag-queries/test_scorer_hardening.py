"""Scorer-hardening regression tests for extract_l3._score_risk.

Covers the three hardening changes (2026-09-25):
  1. Punctuation-insensitive ("compacted") keyword matching: prose such as
     "cytochrome p450 (cyp) 3a4" now matches keyword "cyp3a4"; short keywords
     (<5 compacted chars) are excluded from the fallback so they cannot match
     across fused word boundaries.
  2. Absence-of-effect phrases ("no clinically important", "no important",
     "no clinically significant", "absence of", "free of", "unaffected by")
     negate keywords within the 5-word proximity window.
  3. The previously dead ``negations=`` argument is wired into the proximity
     negation matcher; ddi pools pass "limited"/"few" (e.g. "with limited
     drug-drug interactions").

Run: python rag-queries/test_scorer_hardening.py
Exits non-zero on the first failed assertion.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "rag-queries", "extract_l3.py")

# ---- exec-load the pipeline module (same pattern as the adjudication scripts)
src = open(SRC, encoding="utf-8").read()
ns = {"__file__": SRC, "__name__": "exl3_test"}
exec(compile(src, "extract_l3.py", "exec"), ns)
score_risk = ns["_score_risk"]
_negated_keywords = ns["_negated_keywords"]
_compact_text = ns["_compact_text"]

# ---- per-class ddi scoring args, extracted from source (single source of truth)
cls_pos = [(m.start(), m.group(1)) for m in re.finditer(r'drug_class == "([^"]+)"', src)]
ddi_args = {}
for m in re.finditer(r'ddi_risk"\]\s*=\s*_score_risk\((.*?)drug_name=drug_name\)', src, re.S):
    cls = max((p, c) for p, c in cls_pos if p < m.start())[1]
    if cls in ddi_args:
        continue
    body = m.group(1)

    def lst(name):
        mm = re.search(name + r'=\[([^\]]*)\]', body)
        return [k.lower() for k in re.findall(r'"([^"]+)"', mm.group(1))] if mm else None

    ddi_args[cls] = {
        "keywords": [k.lower() for k in re.findall(
            r'"([^"]+)"', re.search(r'(?:keywords=)?\[([^\]]*)\]', body).group(1))],
        "intensifiers": lst("intensifiers"),
        "mitigators": lst("mitigators"),
        "negations": lst("negations"),
        "pk_contexts": lst("pk_contexts"),
        "adverse": lst("adverse_context_terms"),
    }


def ddi_score(sentence, drug, cls):
    a = ddi_args[cls]
    return score_risk([{"text": sentence}], a["keywords"], default=1,
                      intensifiers=a["intensifiers"], mitigators=a["mitigators"],
                      negations=a["negations"], pk_contexts=a["pk_contexts"],
                      adverse_context_terms=a["adverse"], drug_name=drug)


FAILS = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got={got} want={want}")
    if not ok:
        FAILS.append(name)


print("=== 1. compacted keyword matching (format variants) ===")
check("simvastatin 'cytochrome p450 (cyp) 3a4' -> keyword cyp3a4",
      ddi_score("potent inhibitors of cytochrome p450 (cyp) 3a4 significantly "
                "increase plasma concentrations of the active forms of "
                "simvastatin, lovastatin, and atorvastatin.", "simvastatin", "Statin"), 2)
check("hyphen variant 'cyp-3a4' also matches",
      ddi_score("clarithromycin, a potent cyp-3a4 inhibitor, increases "
                "simvastatin exposure.", "simvastatin", "Statin"), 2)
check("bcrp transporter variant matches (rosuvastatin BCRP DDI)",
      ddi_score("the increased rosuvastatin exposure and minimal change in "
                "atorvastatin exposure with co-administration of cedirogant is "
                "attributed to bcrp inhibition.", "rosuvastatin", "Statin"), 2)
check("compaction trap exists (raw 'cyp' inside a fused word)",
      "cyp" in _compact_text("legacy python"), True)
check("short keyword (<5 compacted chars) does NOT match via fallback",
      score_risk([{"text": "legacy python systems were reviewed."}],
                 ddi_args["PPI"]["keywords"], default=2), 2)

print("=== 2. absence-of-effect negation phrases ===")
check("'no clinically important drug interactions' negates (olmesartan)",
      ddi_score("olmesartan medoxomil has minimal adverse effects with no "
                "clinically important drug interactions.", "olmesartan",
                "Antihypertensive"), 1)
check("'no important drug interaction' negates",
      len(_negated_keywords("no important drug interaction was observed",
                            ["drug interaction"])), 1)
check("'unaffected by' negates (rosuvastatin CYP sentence)",
      len(_negated_keywords("rosuvastatin is unaffected by inhibition by either cyp",
                            ["cyp"])), 1)

print("=== 3. call-site negations wiring ('limited'/'few') ===")
check("'with limited drug-drug interactions' negates (pitavastatin)",
      ddi_score("pitavastatin is a newly developed statin with limited "
                "drug-drug interactions.", "pitavastatin", "Statin"), 1)
check("'fewer drug interactions' negates via substring 'few'",
      ddi_score("celecoxib is associated with fewer drug interactions than "
                "conventional nsaids.", "celecoxib", "NSAID"), 1)

print("=== 4. regression: genuine evidence still scores ===")
check("real interaction sentence still counted (losartan)",
      ddi_score("pharmacokinetic interaction among amlodipine, losartan, and "
                "chlorthalidone after a single oral administration in healthy "
                "male subjects.", "losartan", "Antihypertensive"), 2)
check("clarithromycin lovastatin exposure sentence still scores (lovastatin)",
      ddi_score("based on mechanistic/clinical studies involving clarithromycin, "
                "a strong inhibitor of cyp3a4 and hepatic statin uptake "
                "transporters, lovastatin exposure is markedly increased.",
                "lovastatin", "Statin"), 2)

print("=== 4b. Antacid ddi_risk producer (new in this change set) ===")
check("antacid chelation DDI sentence scores (aluminum hydroxide)",
      ddi_score("aluminum hydroxide antacid reduces the absorption of "
                "coadministered levothyroxine and fluoroquinolones.",
                "aluminum hydroxide", "Antacid"), 2)
check("antacid absence sentence stays low (calcium carbonate)",
      ddi_score("calcium carbonate has no clinically important drug interactions.",
                "calcium carbonate", "Antacid"), 1)

print("=== 5. module integrity ===")
# NOTE: the Antacid block gained its ddi_risk call in the same change set
# (previously legacy data with no producer); its interaction dim is also
# covered separately by "chelation_ddi" (manual/extra).
for cls in ("NSAID", "Statin", "PPI", "Antihypertensive", "Diabetes", "H2RA",
            "Antacid", "Alginate", "Mucosal Protectant"):
    check(f"ddi args extracted for {cls}", cls in ddi_args, True)
check("all ddi call sites carry the 'limited' negation",
      all("limited" in (ddi_args[c]["negations"] or []) for c in ddi_args), True)

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} -> {FAILS}")
    sys.exit(1)
print("ALL CHECKS PASSED")
