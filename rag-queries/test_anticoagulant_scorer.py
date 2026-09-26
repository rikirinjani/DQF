"""Anticoagulant (E1) scorer tests — Phase 2 verification.

Checks the 7 new dims added to extract_l3._score_risk, the salt vocabulary
(dabigatran etexilate / edoxaban tosylate), the pk_contexts guard, and that
build_l3_queries emits the anticoagulant probes.

Run: python rag-queries/test_anticoagulant_scorer.py
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "rag-queries", "extract_l3.py")

src = open(SRC, encoding="utf-8").read()
ns = {"__file__": SRC, "__name__": "ac_test"}
exec(compile(src, "extract_l3.py", "exec"), ns)
score_risk = ns["_score_risk"]
SALT_NAME_RE = ns["SALT_NAME_RE"]
build_l3_queries = ns["build_l3_queries"]

DIMS = ["anticoagulation_efficacy", "bleeding_risk", "renal_clearance_dependence",
        "ddi_risk", "monitoring_burden", "reversal_availability", "gi_bleeding_risk"]

# extract the Anticoagulant block's per-dim args from source
blk = re.search(r'elif drug_class == "Anticoagulant":(.*?)\n    pool_relevance_pct', src, re.S).group(1)
ARGS = {}
for m in re.finditer(r'profile\["(\w+)"\]\s*=\s*_score_risk\((.*?)drug_name=drug_name\)', blk, re.S):
    dim, body = m.group(1), m.group(2)

    def lst(name):
        mm = re.search(name + r'=\[([^\]]*)\]', body)
        return [k.lower() for k in re.findall(r'"([^"]+)"', mm.group(1))] if mm else None

    ARGS[dim] = {
        "keywords": [k.lower() for k in re.findall(
            r'"([^"]+)"', re.search(r'(?:keywords=)?\[([^\]]*)\]', body).group(1))],
        "intensifiers": lst("intensifiers"), "mitigators": lst("mitigators"),
        "negations": lst("negations"), "pk_contexts": lst("pk_contexts"),
        "adverse": lst("adverse_context_terms")}

FAILS = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got={got} want={want}")
    if not ok:
        FAILS.append(name)


def score(dim, text, drug):
    a = ARGS[dim]
    return score_risk([{"text": text}], a["keywords"], default=1,
                      intensifiers=a["intensifiers"], mitigators=a["mitigators"],
                      negations=a["negations"], pk_contexts=a["pk_contexts"],
                      adverse_context_terms=a["adverse"], drug_name=drug)


print("=== 1. all 7 dims present with args ===")
for d in DIMS:
    check(f"args extracted for {d}", d in ARGS, True)

print("=== 2. dim behaviour ===")
check("warfarin INR monitoring sentence -> monitoring_burden >= 2",
      score("monitoring_burden",
            "warfarin requires frequent INR monitoring and dose titration to keep "
            "patients in the therapeutic range.", "warfarin") >= 2, True)
check("apixaban 'no routine monitoring' -> monitoring_burden == 1",
      score("monitoring_burden",
            "due to its predictable pharmacokinetics, apixaban requires no routine "
            "coagulation monitoring.", "apixaban"), 1)
check("dabigatran '80% renal' -> renal_clearance_dependence >= 2",
      score("renal_clearance_dependence",
            "approximately 80% of a dabigatran dose is excreted unchanged by the "
            "kidneys, so severe renal impairment causes accumulation.", "dabigatran") >= 2, True)
check("rivaroxaban combined P-gp + strong CYP3A4 -> ddi_risk >= 2",
      score("ddi_risk",
            "avoid concomitant use of rivaroxaban with combined P-glycoprotein and "
            "strong CYP3A4 inhibitors.", "rivaroxaban") >= 2, True)
check("andexanet alfa reversal -> reversal_availability >= 2",
      score("reversal_availability",
            "andexanet alfa is a specific approved antidote that reverses the "
            "anticoagulant effect of apixaban.", "apixaban") >= 2, True)
check("dabigatran major bleeding trial -> bleeding_risk >= 2",
      score("bleeding_risk",
            "major bleeding occurred significantly less often with apixaban than "
            "warfarin in the randomized trial.", "apixaban") >= 2, True)
check("warfarin ICH sentence -> bleeding_risk >= 2",
      score("bleeding_risk",
            "intracranial hemorrhage is the most feared severe bleeding "
            "complication of warfarin therapy.", "warfarin") >= 2, True)

print("=== 3. pk_contexts guard on efficacy ===")
check("pure PK sentence -> anticoagulation_efficacy == 1",
      score("anticoagulation_efficacy",
            "the pharmacokinetic half-life and clearance of apixaban are "
            "predictable.", "apixaban"), 1)

print("=== 4. salt vocabulary ===")
check("'dabigatran etexilate' matches salt masker",
      bool(SALT_NAME_RE.search("dabigatran etexilate")), True)
check("'edoxaban tosylate' matches salt masker",
      bool(SALT_NAME_RE.search("edoxaban tosylate")), True)
check("'warfarin sodium' matches salt masker",
      bool(SALT_NAME_RE.search("warfarin sodium")), True)

print("=== 5. build_l3_queries emits anticoagulant probes ===")
templates = json.load(open(os.path.join(ROOT, "rag-queries", "l3_query_templates.json"),
                           encoding="utf-8"))
drug = {"id": "apixaban", "class": "Anticoagulant", "name": "Apixaban"}
qs = build_l3_queries(drug, templates)
dims_q = {q.get("dimension") for q in qs}
check("queries returned", len(qs) > 0, True)
check("template has all 7 l3_fields",
      set(templates["classes"]["Anticoagulant"]["l3_fields"]) == set(DIMS), True)
check("class_mechanism probe present",
      any(q.get("dimension") == "class_mechanism" for q in qs), True)

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} -> {FAILS}")
    sys.exit(1)
print("ALL ANTICOAGULANT SCORER CHECKS PASSED")
