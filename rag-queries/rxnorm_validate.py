#!/usr/bin/env python3
"""Validate the framework's drug names against RxNorm (RxNav REST API).

For each drug in api/drugs.json:
  1. resolve rxcui by name;
  2. pull all-related concepts and find the ingredient (IN) vs precise
     ingredient (PIN) -- RxNorm models a salt/ester as PIN `form_of` IN;
  3. flag salt-form names (PIN != IN) and report the modifier.

Output: a JSON report + a console table. Read-only, rate-limited, cached.

Usage:
    python rxnorm_validate.py [--limit N] [--out rxnorm_report.json]
"""
import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRUGS_JSON = ROOT / "api" / "drugs.json"
BASE = "https://rxnav.nlm.nih.gov/REST"
RATE_S = 0.25  # polite ~4 req/s


def _get(path: str, **params):
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception:
            if attempt == 2:
                return None
            time.sleep(1.0 * (attempt + 1))
    return None


def rxcui_for(name: str):
    d = _get("rxcui.json", name=name)
    ids = (d or {}).get("idGroup", {}).get("rxnormId") or []
    return ids[0] if ids else None


def ingredients(rxcui: str):
    """Return (IN names, PIN names) via allrelated."""
    d = _get(f"rxcui/{rxcui}/allrelated.json")
    if not d:
        return [], []
    ins, pins = [], []
    for grp in d.get("allRelatedGroup", {}).get("conceptGroup", []):
        tty = grp.get("tty")
        for c in grp.get("conceptProperties", []) or []:
            if tty == "IN":
                ins.append(c.get("name"))
            elif tty == "PIN":
                pins.append(c.get("name"))
    return ins, pins


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="rxnorm_report.json")
    args = ap.parse_args()

    drugs = json.load(open(DRUGS_JSON, encoding="utf-8"))["drugs"]
    if args.limit:
        drugs = drugs[: args.limit]

    report, salt_count, unresolved = [], 0, 0
    for i, d in enumerate(drugs, 1):
        name = d.get("name") or d["id"]
        rx = rxcui_for(name)
        time.sleep(RATE_S)
        if not rx:
            unresolved += 1
            report.append({"id": d["id"], "name": name, "rxcui": None,
                           "salt_form": None, "in": [], "pin": [],
                           "note": "unresolved"})
            print(f"  [{i:>3}/{len(drugs)}] {d['id']:<26} UNRESOLVED")
            continue
        ins, pins = ingredients(rx)
        time.sleep(RATE_S)
        # salt form when the resolved ingredient set has a PIN distinct from IN
        salt = bool(pins) and (not ins or any(p not in ins for p in pins) or pins != ins)
        if salt:
            salt_count += 1
        report.append({"id": d["id"], "name": name, "rxcui": rx,
                       "salt_form": salt, "in": sorted(set(ins)),
                       "pin": sorted(set(pins))})
        tag = "SALT" if salt else "    "
        print(f"  [{i:>3}/{len(drugs)}] {d['id']:<26} {tag} "
              f"IN={sorted(set(ins))[:2]} PIN={sorted(set(pins))[:2]}")

    out = Path(args.out)
    json.dump({"drugs": report, "salt_form_count": salt_count,
               "unresolved": unresolved, "total": len(drugs)},
              open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\nDONE total={len(drugs)} salt_form={salt_count} "
          f"unresolved={unresolved} -> {out}")


if __name__ == "__main__":
    main()
