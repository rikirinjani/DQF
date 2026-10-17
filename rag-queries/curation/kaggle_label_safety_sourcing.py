# NOTE: repo copy of the Kaggle kernel as last pushed (v4: re-pick for glyburide,
# rosiglitazone, lovastatin with all candidates kept). v3 ran the same code over all 56
# drugs with KNOWN = setids from earlier label_sourcing_*.json files. Merged raw output:
# rag-queries/curation/label_safety_raw.json
# DQF safety-field label sourcing (pregnancy / lactation / hepatic) via DailyMed v2 SPL.
# Scope: 50 drugs with null safety fields + re-check of the 6 currently hard-gated
# drugs (5 statins + warfarin; FDA 2021 statin pregnancy-contraindication removal).
# Output: /kaggle/working/label_safety.json (key sentences + section excerpts per drug).
import json, re, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

KNOWN = {}
DRUGS = [["glyburide", "Glyburide"], ["rosiglitazone", "Rosiglitazone"], ["lovastatin", "Lovastatin"]]
BASE = "https://dailymed.nlm.nih.gov/dailymed/services/v2"
NS = {"v": "urn:hl7-org:v3"}
RX_CODE = "34391-3"  # HUMAN PRESCRIPTION DRUG LABEL

LOINC = {
    "34066-1": "boxed_warning", "34070-3": "contraindications",
    "42228-7": "pregnancy", "34077-8": "pregnancy", "77290-5": "lactation",
    "34080-2": "lactation",
}
TITLE_RULES = [
    (re.compile(r"boxed|warning:\s*fetal", re.I), "boxed_warning"),
    (re.compile(r"contraindication", re.I), "contraindications"),
    (re.compile(r"pregnan|fetal toxicity|teratogen", re.I), "pregnancy"),
    (re.compile(r"lactation|nursing", re.I), "lactation"),
    (re.compile(r"hepat|liver", re.I), "hepatic"),
]
ANY_HEP = re.compile(r"hepatic impairment|hepatic insufficiency|hepatic dysfunction|"
                     r"child-pugh|liver disease|cirrhosis|impaired hepatic|impaired liver", re.I)
ANY_PREG = re.compile(r"pregnan", re.I)
ANY_LACT = re.compile(r"nursing mothers|breast milk|human milk|breastfe|lactation", re.I)
KEY = re.compile(r"contraindicat|discontinue|not recommended|avoid|should not|fetal|fetus|"
                 r"teratogen|embryo|breast|milk|hepatic|liver|child-pugh|pregnan", re.I)


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "dqf-label-sourcing/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            err = e
            time.sleep(2 * (i + 1))
    raise err


def text_of(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def parse(setid):
    root = ET.fromstring(get(f"{BASE}/spls/{setid}.xml"))
    code = root.find("v:code", NS)
    rx = code is not None and code.get("code") == RX_CODE
    title_el = root.find("v:title", NS)
    eff = root.find("v:effectiveTime", NS)
    out = {}
    for sec in root.iter(f"{{{NS['v']}}}section"):
        c = sec.find("v:code", NS)
        t = sec.find("v:title", NS)
        title = text_of(t) if t is not None else ""
        kind = LOINC.get(c.get("code") if c is not None else "")
        if not kind:
            for rx_, k in TITLE_RULES:
                if rx_.search(title):
                    kind = k
                    break
        if not kind:
            continue
        txt = text_of(sec)
        out.setdefault(kind, []).append({"title": title, "text": txt[:2500]})
    # whole-document sweep: old-format labels bury these in untitled paragraphs
    body = text_of(root)
    for kind, rx_ in (("hepatic_any", ANY_HEP), ("pregnancy_any", ANY_PREG),
                      ("lactation_any", ANY_LACT)):
        hits = []
        for s in re.split(r"(?<=[.;])\s+", body):
            if rx_.search(s) and 15 < len(s) < 600 and s not in hits:
                hits.append(s)
        if hits:
            out[kind] = [{"title": "(document sweep)", "text": " ".join(hits[:15])}]
    return {"rx": rx, "title": text_of(title_el) if title_el is not None else "",
            "effective": eff.get("value") if eff is not None else None, "sections": out}


def candidates(name):
    q = urllib.parse.quote(name)
    j = json.loads(get(f"{BASE}/spls.json?drug_name={q}&pagesize=50"))
    return [(d["setid"], d.get("title", "")) for d in j.get("data", [])]


def single_entity(title, name):
    t = title.upper()
    rest = t.replace(name.upper(), "")
    return (" AND " not in rest and "/" not in t and "KIT" not in t
            and not re.search(re.escape(name.upper()) + r"\s*-\s*[A-Z]", t))


def key_sentences(sections):
    res = {}
    for kind, lst in sections.items():
        sents = []
        for s in lst:
            for sent in re.split(r"(?<=[.;])\s+", s["text"]):
                if KEY.search(sent) and 15 < len(sent) < 500 and sent not in sents:
                    sents.append(sent)
        res[kind] = sents[:12]
    return res


results = {}
for drug_id, name in DRUGS:
    rec = {"name": name, "tried": []}
    order = []
    if drug_id in KNOWN:
        order.append((KNOWN[drug_id], "known"))
    try:
        order += candidates(name)
    except Exception as e:
        rec["search_error"] = repr(e)
    best = (0, None, None, None)
    for setid, title in order[:16]:
        if title != "known" and title and not single_entity(title, name):
            continue
        try:
            p = parse(setid)
        except Exception as e:
            rec["tried"].append({"setid": setid, "error": repr(e)})
            continue
        rec["tried"].append({"setid": setid, "title": p["title"][:120], "rx": p["rx"]})
        if not p["rx"]:
            continue
        score = sum(k in p["sections"] for k in ("pregnancy", "lactation", "hepatic",
                                                  "contraindications"))
        if score == 0:
            continue
        rec.setdefault("all", []).append({"setid": setid, "title": title, "score": score,
                                          "effective": p["effective"],
                                          "key_sentences": key_sentences(p["sections"])})
        if score > best[0]:
            best = (score, setid, title, p)
        if len(rec["tried"]) >= 10:
            break
    if best[1]:
        score, setid, title, p = best
        rec.update({"score": score,"setid": setid, "title": (title if title != "known" else "") or p["title"][:160], "effective": p["effective"],
                    "key_sentences": key_sentences(p["sections"]),
                    "sections": p["sections"]})
    if "setid" not in rec:
        rec["status"] = "not_found_in_dailymed"
    results[drug_id] = rec
    print(drug_id, rec.get("setid", "NOT FOUND"), rec.get("title", "")[:70], flush=True)
    time.sleep(0.5)

with open("/kaggle/working/label_safety.json", "w", encoding="utf-8") as f:
    json.dump({"generated": time.strftime("%Y-%m-%d"), "n": len(results), "drugs": results},
              f, ensure_ascii=False, indent=1)
print("found:", sum("setid" in r for r in results.values()), "/", len(results))
