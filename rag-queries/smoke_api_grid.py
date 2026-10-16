#!/usr/bin/env python3
"""352-query legacy API grid (no-crash + hard-gate invariants).

Recovered from the portable grid in Kaggle kernel
rikirinjani/dqf-n6b-slice-verify-cpu (the original lived only in a Temp dir).

11 class filters x age{30,70} x renal{normal,severe} x pregnancy{no,3rd tri}
x lactation{no,yes} x hepatic{normal,severe} = 352 legacy queries.

Per query, beyond "does not raise", asserts the N6b Phase 1 invariants:
  - no drug is both ranked and excluded/unranked
  - every candidate has exactly one disposition (results/excluded/eligible_unranked)
  - every excluded row carries at least one failed hard rule
Run: python rag-queries/smoke_api_grid.py
"""
import asyncio
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "api"))

import server
from server import QueryRequest

CLASSES = ["any", "NSAID", "Statin", "PPI", "H2RA", "Antacid", "Alginate",
           "Mucosal Protectant", "Anticoagulant", "Antihypertensive", "Diabetes"]


def _check(res, cls):
    ranked = [r["id"] for r in res["results"]]
    excluded = [r["id"] for r in res["excluded"]]
    unranked = [r["id"] for r in res["eligible_unranked"]]
    if set(ranked) & (set(excluded) | set(unranked)):
        return "drug both ranked and gated"
    expected = len(server.drugs) if cls == "any" else sum(
        d["class"] == cls for d in server.drugs)
    if len(ranked) + len(excluded) + len(unranked) != expected:
        return f"disposition count {len(ranked)}+{len(excluded)}+{len(unranked)} != {expected}"
    for row in res["excluded"]:
        if not any(r.get("state") == "failed" for r in row["reasons"]):
            return f"{row['id']} excluded without a failed rule"
    return None


def main():
    fails, n = [], 0
    for cls, age, renal, preg, lac, hep in itertools.product(
            CLASSES, [30, 70], ["normal", "severe"], ["not_pregnant", "third_trimester"],
            ["no", "yes"], ["normal", "severe"]):
        req = QueryRequest(age=age, renal_function=renal, cv_risk="moderate", gi_risk="high",
                           pain_type="inflammatory", drug_class=cls, prioritize="balanced",
                           pregnancy_status=preg, lactation=lac, hepatic_function=hep)
        label = f"{cls} age{age} {renal} {preg} lact{lac} hep{hep}"
        try:
            res = asyncio.run(server.query_drugs(req))
            n += 1
        except Exception as e:
            fails.append(f"{label}: {e!r}")
            continue
        err = _check(res, cls)
        if err:
            fails.append(f"{label}: {err}")
    print(f"queries run: {n}, failures: {len(fails)}")
    if fails:
        print("first:", fails[0])
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
