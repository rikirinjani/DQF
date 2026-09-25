"""Post-hoc auditor for LLM evidence triage verdicts (classifier upgrade gate).

Purpose
-------
Batch 4 showed Mistral-7B (4-bit) over-emits ``strong`` for sentences that are
quantified-looking but wrong for the dimension: wrong dimension (migraine
sentence for metabolic_effect), wrong direction (benefit sentences for cv_risk,
"ameliorates renal failure" for renal_toxicity_risk), or absence-as-effect
("weight neutral", "no sign of rebound"). The both-signal adjudication rule
could not catch these because the cell-level judge saw the same sentences.

This auditor sits between triage output and adjudication and flags suspect
``strong`` labels *before* they can drive a score raise. It is deliberately
rule-based and explainable -- every flag carries a reason code.

Rules (a sentence labeled ``strong`` is suspect if any fires)
------------------------------------------------------------
  R1 ABSENCE    direction-agnostic dimension ("weight_effect"): the sentence
                states the absence of an effect ("no evidence", "without",
                "neutral", ...) -- not positive evidence.
  R2 DIRECTION  dimension has a known direction: benefit dimensions need a
                benefit term (renal dims need renal-benefit phrasing, not bare
                BP efficacy), risk dimensions need a harm term.
  R3 FIT        sentence contains none of the dimension's scoring keywords
                (salt-name masked) -- it is about something else.
  R4 PK-MECH    sentence is a pharmacokinetic/mechanistic statement while the
                dimension is not a PK/interaction dimension.

Usage
-----
  python rag-queries/classifier_audit.py --selftest
  python rag-queries/classifier_audit.py path/to/batchN_verdicts.json [--strict]

Output: JSON report on stdout; exit 1 with --strict when any group is suspect.
"""
import argparse
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT = os.path.join(ROOT, "rag-queries", "extract_l3.py")
FIXTURES = os.path.join(ROOT, "rag-queries", "fixtures", "classifier_artifacts.json")

# Dimension direction: benefit (higher = better), risk (higher = worse),
# None = direction-agnostic (an effect in either direction counts).
DIM_DIRECTION = {
    # benefit
    "renal_protection": "benefit", "cv_outcome_benefit": "benefit",
    "renal_benefit": "benefit", "neutralization_capacity": "benefit",
    "barrier_protection": "benefit", "healing_ability": "benefit",
    "ulcer_healing": "benefit", "reflux_suppression": "benefit",
    "raft_strength": "benefit", "a1c_reduction": "benefit",
    "gi_tolerability": "benefit",
    # risk
    "renal_risk": "risk", "cv_risk": "risk", "electrolyte_risk": "risk",
    "hypoglycemia_risk": "risk", "cdi_risk": "risk", "bone_fracture_risk": "risk",
    "renal_toxicity_risk": "risk", "gi_risk": "risk", "ddi_risk": "risk",
    "chelation_ddi": "risk", "myopathy_risk": "risk", "aluminum_exposure": "risk",
    "milk_alkali_risk": "risk", "acid_rebound": "risk",
    # direction-agnostic
    "weight_effect": None, "metabolic_effect": None, "heart_rate_effect": None,
}

ABSENCE_TERMS = [
    "no significant", "no increase", "no evidence", "no association",
    "not associated", "not related", "not increased", "not elevated",
    "not affected", "no benefit", "no effect", "no protection",
    "no clinically important", "no important", "no clinically significant",
    "absence of", "free of", "unaffected by", "no sign", "no adverse",
    "no deterioration", "no difference", "no change", "no improvement",
    "without", "unlikely", "weight neutral", "weight-neutral",
    "inconclusive", "remains unclear", "remain unclear", "did not",
    "does not", "do not", "no causality",
]

BENEFIT_TERMS = [
    "benefit", "protect", "renoprotect", "protective", "improve", "improved",
    "superior", "effective", "efficacious", "efficacy", "slow progression",
    "slow the progression", "delay", "attenuat", "ameliorat", "preserv",
    "prevent", "reduc", "lower risk",
]

# Positive-effect terms for direction-agnostic dims ("weight_effect"): an
# absence phrase plus one of these is real effect evidence, e.g.
# "... accompanied by weight loss and no increase in hypoglycemia".
EFFECT_TERMS = [
    "loss", "gain", "reduction", "reduc", "increase", "decrease", "change",
    "higher", "lower", "improve", "elevat", "bmi",
]

# Benefit dimensions where the generic list is too loose: BP efficacy "effective"
# is not renal protection, so renal dims require renal-benefit phrasing.
# (Batch-4 artifact: the CLICK trial sentence was labeled strong for
# chlorthalidone renal_protection purely on the word "effective".)
DIM_BENEFIT_TERMS = {
    "renal_protection": ["renoprotect", "nephroprotect", "protect the kidney",
                         "slow progression", "slow the progression", "delay the progression",
                         "ameliorat", "albuminuria", "proteinuria", "egfr"],
    "renal_benefit": ["renoprotect", "nephroprotect", "protect the kidney",
                      "slow progression", "slow the progression", "delay the progression",
                      "albuminuria", "proteinuria", "egfr"],
}

HARM_TERMS = [
    "risk", "increased", "increase", "adverse", "harm", "toxic", "failure",
    "insufficiency", "impair", "reduced the", "decrease", "decreased",
    "suppress", "inhibit", "hypokalem", "hyperkalem", "hyponatrem",
    "serum potassium", "serum sodium", "lower", "elevated", "high risk",
]

PK_TERMS = [
    "pharmacokinetic", "pharmacokinetics", "clearance", "half-life",
    "bioavailability", "cmax", "auc", "rate constant", "plasma concentration",
]


def _load_module():
    ns = {"__file__": EXTRACT, "__name__": "audit_dim_kw"}
    exec(compile(open(EXTRACT, encoding="utf-8").read(), "extract_l3.py", "exec"), ns)
    return ns


def load_dim_keywords():
    """Extract per-(class, dim) scoring keywords from extract_l3.py source."""
    src = open(EXTRACT, encoding="utf-8").read()
    cls_pos = [(m.start(), m.group(1)) for m in re.finditer(r'drug_class == "([^"]+)"', src)]
    kwmap = {}
    for m in re.finditer(r'profile\["(\w+)"\]\s*=\s*_score_risk\((.*?)drug_name=drug_name\)',
                         src, re.S):
        cls = max((p, c) for p, c in cls_pos if p < m.start())[1]
        kwm = re.search(r'(?:keywords=)?\[([^\]]*)\]', m.group(2))
        if kwm:
            kwmap.setdefault((cls, m.group(1)),
                             [k.lower() for k in re.findall(r'"([^"]+)"', kwm.group(1))])
    return kwmap


def audit_sentence(text, dim, cls, kwmap, salt_re):
    """Return a list of reason codes for one ``strong`` sentence."""
    s = text.lower()
    reasons = []
    direction = DIM_DIRECTION.get(dim)
    has_absence = any(t in s for t in ABSENCE_TERMS)

    # R1/R2 direction. For direction-agnostic dimensions an absence phrase is
    # the tell ("weight neutral", "without weight gain"). For directed
    # dimensions the sentence must carry evidence in the dimension's own
    # direction; an absence phrase alone therefore also fails here (this
    # subsumes R1 and avoids false-flagging sentences like "naproxen reduced
    # GFR ... while no significant change occurred with sulindac", where the
    # negation belongs to the comparator arm).
    if direction is None:
        if has_absence and not any(t in s for t in EFFECT_TERMS):
            reasons.append("R1_ABSENCE")
    elif direction == "benefit":
        terms = DIM_BENEFIT_TERMS.get(dim, BENEFIT_TERMS)
        if not any(t in s for t in terms):
            reasons.append("R2_DIRECTION_NO_BENEFIT")
    else:  # risk
        if not any(t in s for t in HARM_TERMS):
            reasons.append("R2_DIRECTION_NO_HARM")

    kws = kwmap.get((cls, dim))
    if kws:
        probe = salt_re.sub(" ", s) if salt_re else s
        if not any(k in probe for k in kws):
            reasons.append("R3_FIT_NO_DIM_KEYWORD")

    if dim not in ("ddi_risk", "chelation_ddi") and any(t in s for t in PK_TERMS):
        reasons.append("R4_PK_MECHANISTIC")

    return reasons


def audit_group(group, kwmap, salt_re):
    flagged = []
    for sent in group.get("sentences", []):
        if sent.get("cls") != "strong":
            continue
        reasons = audit_sentence(sent["text"], group["dim"], group.get("class"),
                                 kwmap, salt_re)
        if reasons:
            flagged.append({"pmid": sent.get("pmid"), "reasons": reasons,
                            "text": sent["text"][:160]})
    return {"drug": group.get("drug"), "dim": group.get("dim"),
            "suspect": bool(flagged), "flagged_strong": flagged}


def _selftest():
    ns = _load_module()
    kwmap = load_dim_keywords()
    salt_re = ns["SALT_NAME_RE"]
    fx = json.load(open(FIXTURES, encoding="utf-8"))

    # group artifacts by (drug, dim) -> expect the CELL to be flagged
    cells = {}
    for a in fx["artifacts"]:
        g = cells.setdefault((a["drug"], a["dim"], a["class"]), [])
        g.append({"pmid": None, "text": a["text"], "cls": "strong"})
    fails = []
    print("=== artifact cells (expect suspect) ===")
    for (drug, dim, cls), sents in cells.items():
        r = audit_group({"drug": drug, "dim": dim, "class": cls, "sentences": sents},
                        kwmap, salt_re)
        print(f"  [{'PASS' if r['suspect'] else 'FAIL'}] {drug:26s} {dim:24s} "
              f"({len(r['flagged_strong'])}/{len(sents)} strong flagged)")
        if not r["suspect"]:
            fails.append((drug, dim))

    print("=== controls (expect clean per-sentence) ===")
    for c in fx["controls"]:
        reasons = audit_sentence(c["text"], c["dim"], c["class"], kwmap, salt_re)
        ok = not reasons
        print(f"  [{'PASS' if ok else 'FAIL'}] {c['drug']:26s} {c['dim']:24s} {reasons or ''}")
        if not ok:
            fails.append((c["drug"], c["dim"], "control flagged"))

    print()
    if fails:
        print(f"SELFTEST FAILED: {fails}")
        return 1
    print(f"SELFTEST PASSED ({len(cells)} artifact cells flagged, "
          f"{len(fx['controls'])} controls clean)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Audit LLM triage verdicts for suspect strong labels")
    ap.add_argument("verdicts", nargs="?", help="batchN_verdicts.json")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any group is suspect")
    ap.add_argument("--selftest", action="store_true", help="run fixture self-test")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())
    if not args.verdicts:
        ap.error("provide a verdicts json or --selftest")

    ns = _load_module()
    kwmap = load_dim_keywords()
    salt_re = ns["SALT_NAME_RE"]
    ver = json.load(open(args.verdicts, encoding="utf-8"))

    report, n_suspect = [], 0
    for gid, g in ver.items():
        r = audit_group(g, kwmap, salt_re)
        report.append(r)
        if r["suspect"]:
            n_suspect += 1
    print(json.dumps({"groups": len(report), "suspect_groups": n_suspect,
                      "report": report}, indent=1, ensure_ascii=False))
    print(f"\n{n_suspect}/{len(report)} groups have suspect strong labels", file=sys.stderr)
    sys.exit(1 if (args.strict and n_suspect) else 0)


if __name__ == "__main__":
    main()
