#!/usr/bin/env python3
"""Classify DailyMed label excerpts into PROPOSED pregnancy/lactation/hepatic safety values.

Input: label_safety.json from Kaggle kernel rikirinjani/dqf-label-safety-sourcing-cpu.
Output: rag-queries/curation/label_sourcing_safety_fields.json (PROPOSED ONLY).

Value vocabulary is the one server.py / eligibility.py already consume:
  pregnancy  -> narrative "(label)" strings; _norm_preg maps 'contraindicated'->X,
                'avoid'->D, anything else->C
  lactation  -> prefix 'avoid' | 'caution' | 'safe' (_norm_lact reads the prefix)
  hepatic    -> 'contraindicated' (hard gate) | 'caution' | 'safe' | narrative (penalty 1)
Every proposal carries the deciding label sentence verbatim. Rules are ordered;
the first match wins.
Run: python rag-queries/curation/classify_label_safety.py <label_safety.json>
"""
import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "label_sourcing_safety_fields.json"


def sentences(rec, *kinds):
    out = []
    for k in kinds:
        for sec in rec.get("sections", {}).get(k, []):
            for s in re.split(r"(?<=[.;])\s+", sec["text"]):
                s = s.strip()
                if 10 < len(s) < 600:
                    out.append((k, s))
    return out


def first(sents, pattern, exclude=None):
    rx = re.compile(pattern, re.I)
    ex = re.compile(exclude, re.I) if exclude else None
    for k, s in sents:
        m = rx.search(s)
        if m and not (ex and ex.search(s)):
            if len(s) > 300:
                s = "..." + s[max(0, m.start() - 120):m.end() + 160] + "..."
            return k, s
    return None


def classify_pregnancy(rec):
    contra = sentences(rec, "contraindications")
    hit = first(contra, r"pregnan", r"not contraindicated|discontinuation of lipid")
    if hit:
        return "contraindicated in pregnancy (label)", "P1 pregnancy listed in contraindications", hit
    allp = sentences(rec, "boxed_warning", "pregnancy")
    if not rec.get("sections", {}).get("pregnancy"):
        allp += sentences(rec, "pregnancy_any")
    hit = first(allp, r"warning: fetal toxicity|(^|\d\s)fetal toxicity|"
                      r"when pregnancy is detected,? discontinue|discontinue .{0,60} as soon as possible")
    if hit:
        return ("avoid - fetal toxicity; discontinue when pregnancy is detected (label)",
                "P2 fetal-toxicity boxed warning / discontinue-on-detection", hit)
    hit = first(allp, r"not recommended during the second and third trimesters|"
                      r"avoid .{0,30}in pregnant women|should not be used during pregnancy|"
                      r"not recommended (during|in) pregnancy", r"unless")
    if hit:
        return ("avoid - not recommended in pregnancy or in 2nd/3rd trimester (label)",
                "P2b explicit not-recommended / avoid in pregnancy", hit)
    hit = first(allp, r"discontinue .{0,40}when pregnancy is recognized|may cause fetal harm|"
                      r"can cause fetal harm")
    if hit:
        return ("avoid - may cause fetal harm; discontinue when pregnancy is recognized (label)",
                "P3 fetal harm statement", hit)
    hit = first(allp, r"insufficient|limited|no (adequate|available) (and well-controlled )?"
                      r"(studies|data)|not been established|unknown")
    if hit:
        return "insufficient human data (label)", "P4 limited/no human data", hit
    hit = first(allp, r"pregnancy category ([ABCDX])\b")
    if hit:
        letter = re.search(r"pregnancy category ([ABCDX])\b", hit[1], re.I).group(1).upper()
        return letter, "P4c explicit pregnancy category letter (pre-PLLR label)", hit
    if allp:
        preg_only = [x for x in allp if re.search(r"pregnan", x[1], re.I)] or allp
        return "use if clearly needed (label)", "P5 pregnancy section present, no restriction", preg_only[0]
    return None, "P0 no pregnancy text extracted", None


def classify_lactation(rec):
    contra = sentences(rec, "contraindications")
    hit = first(contra, r"\blactation\b|nursing|breast", r"not contraindicated")
    if hit:
        return "avoid - lactation listed in contraindications (label)", "L0a contraindicated", hit
    sents = sentences(rec, "lactation") or sentences(rec, "lactation_any")
    hit = first(sents, r"breastfeeding is not recommended|not recommended .{0,40}(breast|nursing)|"
                       r"do not use .{0,40}nursing|should not breastfeed|"
                       r"advise .{0,40}not to breastfeed|lactation\b.{0,20}contraindicat")
    if hit:
        return "avoid - breastfeeding not recommended (label)", "L1 not recommended", hit
    hit = first(sents, r"decision should be made whether to discontinue nursing")
    if hit:
        return ("caution - discontinue nursing or the drug (label)",
                "L2 discontinue-nursing-or-drug decision", hit)
    hit = first(sents, r"compatible with breastfeeding|developmental and health benefits of "
                       r"breastfeeding should be considered")
    if hit and not first(sents, r"not known|no (information|data)|unknown"):
        return "caution - benefit/risk statement only (label)", "L3 benefit/risk only", hit
    hit = first(sents, r"not present in human milk|not detected in (human |breast )?milk")
    if hit:
        return ("caution - not detected in human milk (limited data) (label)",
                "L3b not detected in milk", hit)
    hit = first(sents, r"not known|no (information|data|available data)|unknown")
    if hit:
        return "caution - unknown excretion/infant effect (label)", "L4 unknown", hit
    hit = first(sents, r"excreted in (human )?(breast )?milk|appears in (human |breast )?milk|"
                       r"transferred (through|into) (human |breast )?milk|present in (human )?milk")
    if hit:
        return "caution - excreted in human milk (label)", "L4b excreted in milk", hit
    if sents:
        return "caution - see label (label)", "L5 lactation text, no rule matched", sents[0]
    return None, "L0 no lactation text extracted", None


def classify_hepatic(rec):
    contra = sentences(rec, "contraindications")
    hit = first(contra, r"hepatic|\bliver\b|transaminase|cirrhosis", r"not contraindicated")
    if hit:
        return "contraindicated", "H1 hepatic condition listed in contraindications", hit
    sents = [(k, s) for k, s in sentences(rec, "hepatic") + sentences(rec, "hepatic_any")
             if re.search(r"hepat|\bliver\b|child-pugh|cirrho", s, re.I)]
    hit = first(sents, r"not recommended|should not be used|avoid use", r"monitor")
    if hit:
        return "severe impairment: not recommended (label)", "H2 not recommended", hit
    raw = sents + sentences(rec, "hepatic")
    hit = first(raw, r"no (initial )?dos(e|age) adjustment|no adjustment|not clinically (meaningful|significant)|"
                       r"no clinically (relevant|meaningful|significant)|"
                       r"not considered (to be )?clinically (relevant|meaningful|significant)")
    caution = first(sents, r"reduce (the )?(dose|dosage)|dose reduction|reduced (dose|dosage)|"
                           r"lower (the )?(starting )?(dose|dosage)|caution|monitor|increase[sd]? .{0,30}(exposure|levels|"
                           r"concentration|bioavailability)|titrat|adjust|slowed|prolonged|"
                           r"hepatic failure|hepatotox|jaundice|hepatic injury|cautious|potentiat|"
                           r"hypoglycemi|conservative", r"no (initial )?(dose|dosage) adjustment|no adjustment")
    if hit and not caution:
        return "safe", "H3 no dose adjustment", hit
    if caution:
        return "caution", "H4 dose reduction / monitoring / increased exposure", caution
    if hit:
        return "safe", "H3 no dose adjustment", hit
    hit = first(sents, r"no clinical experience|not (been )?studied|no pharmacokinetic study")
    if hit:
        return ("not studied in (severe) hepatic impairment (label)",
                "H5a not studied / no clinical experience", hit)
    if sents:
        return "not studied (unknown) (label)", "H5 hepatic text, no rule matched", sents[0]
    return None, "H0 no hepatic text extracted", None


STATINS_PLLR = ["atorvastatin", "rosuvastatin", "simvastatin", "pravastatin", "pitavastatin"]

REVIEW_FLAGS = {
    "statin_pregnancy_downgrade": {
        "drugs": STATINS_PLLR,
        "note": "Current labels no longer list pregnancy as a contraindication (8.1: 'Discontinue "
                "... when pregnancy is recognized'; FDA 2021 statin class labeling change). Proposed "
                "value normalizes to D, so these 5 drugs would LEAVE the pregnancy_x hard gate "
                "(still -6 safety penalty).",
    },
    "lovastatin_label_lag": {
        "drugs": ["lovastatin"],
        "note": "Every lovastatin label on DailyMed (10 checked, 2026) is old-format and still "
                "lists 'Pregnancy and lactation' under CONTRAINDICATIONS -> X, inconsistent with the "
                "other 5 statins. Proposed per label as found.",
    },
    "stale_label": {
        "drugs": ["rosiglitazone", "glyburide"],
        "note": "Only label available: AVANDIA 2010-01-19 (rosiglitazone); glyburide single-entity "
                "label chosen is Teva 2015 old-format (newer generics share the same text).",
    },
    "pre_pllr_category_letter": {
        "drugs": ["glipizide", "glyburide"],
        "note": "Label states a letter category (C / B); proposed verbatim as the letter.",
    },
    "not_in_dailymed": {
        "drugs": ["vildagliptin", "gliclazide"],
        "note": "Not US-approved; no DailyMed SPL. Fields stay null; needs EMA SmPC sourcing round.",
    },
    "hepatic_label_silent": {
        "drugs": ["atenolol", "terazosin", "clonidine", "hydralazine"],
        "note": "No hepatic impairment guidance found in label text; hepatic_safety stays null.",
    },
    "ace_inhibitor_hepatic_basis": {
        "drugs": ["enalapril", "ramipril", "perindopril", "captopril"],
        "note": "hepatic 'caution' rests on the class idiosyncratic hepatic-failure warning "
                "(discontinue if jaundice), not on impairment dosing (ramipril also cites raised "
                "exposure).",
    },
    "new_hepatic_hard_gate": {
        "drugs": ["lovastatin", "carvedilol", "nebivolol", "methyldopa", "acarbose",
                  "rosuvastatin", "pravastatin"],
        "note": "rosuvastatin/pravastatin: current labels list acute liver failure / decompensated "
                "cirrhosis (stored values were caution/safe). Label contraindication is specific (active liver disease / severe impairment / "
                "cirrhosis) but the current hepatic_contraindicated rule fires on ANY non-normal "
                "hepatic_function, including mild - see the open hepatic-rule policy item.",
    },
}


def gate_impact(proposals):
    """Which drugs enter/leave the two hard gates if the proposals are applied."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "api"))
    import eligibility
    drugs = {d["id"]: d for d in json.load(open(
        Path(__file__).resolve().parents[2] / "api" / "drugs.json", encoding="utf-8"))["drugs"]}
    out = {"pregnancy_x": {"enter": [], "leave": []},
           "hepatic_contraindicated": {"enter": [], "leave": []}}
    for drug_id, row in proposals.items():
        cur = drugs[drug_id]
        new_p = row["pregnancy_safety"]["proposed"]
        if new_p is not None:
            was = eligibility._norm_preg(cur.get("pregnancy_safety")) == "X"
            now = eligibility._norm_preg(new_p) == "X"
            if now != was:
                out["pregnancy_x"]["enter" if now else "leave"].append(drug_id)
        new_h = row["hepatic_safety"]["proposed"]
        if new_h is not None:
            was = cur.get("hepatic_safety") == "contraindicated"
            now = new_h == "contraindicated"
            if now != was:
                out["hepatic_contraindicated"]["enter" if now else "leave"].append(drug_id)
    return out


def main(src):
    data = json.load(open(src, encoding="utf-8"))["drugs"]
    proposals, sources, gaps = {}, {}, []
    for drug_id, rec in data.items():
        if "setid" not in rec:
            gaps.append({"id": drug_id, "reason": rec.get("status", "not found")})
            continue
        sources[drug_id] = {"setid": rec["setid"], "title": rec["title"][:160],
                            "effective": rec.get("effective")}
        row = {}
        for field, fn in (("pregnancy_safety", classify_pregnancy),
                          ("lactation_safety", classify_lactation),
                          ("hepatic_safety", classify_hepatic)):
            value, rule, hit = fn(rec)
            row[field] = {"proposed": value, "rule": rule,
                          "quote": hit[1] if hit else None,
                          "section": hit[0] if hit else None}
        proposals[drug_id] = row
    OUT.write_text(json.dumps({
        "generated_by": "rag-queries/curation/classify_label_safety.py",
        "kernel": "rikirinjani/dqf-label-safety-sourcing-cpu (v3 + v4 re-pick for glyburide, rosiglitazone, lovastatin)",
        "status": "PROPOSED ONLY - no drugs.json changes until user approval",
        "approval_gate": "Evidence file for user review (N6 pattern). Apply only after explicit "
                         "APPROVED; statin pregnancy downgrade is a separate yes/no.",
        "method": "Kaggle CPU kernel fetches DailyMed v2 SPL (Rx, single-entity, best section "
                  "coverage among up to 8-10 candidates) -> section + whole-document sentence "
                  "sweep -> ordered rules in this script; every value carries its deciding quote",
        "review_flags": REVIEW_FLAGS,
        "gate_impact": gate_impact(proposals),
        "sources": sources, "gaps": gaps, "proposals": proposals,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT} ({len(proposals)} drugs, {len(gaps)} gaps)")


if __name__ == "__main__":
    main(sys.argv[1])
