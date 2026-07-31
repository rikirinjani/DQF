#!/usr/bin/env python3
"""Show PPI L3 data from drugs.json."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

p = r"C:\Users\think\Project_v2\drug-quantification-framework\api\drugs.json"
with open(p, encoding="utf-8") as f:
    data = json.load(f)

ppis = [d for d in data["drugs"] if d.get("class") == "PPI"]
for d in ppis:
    l3 = d.get("l3_systems", {})
    ev = l3.get("_evidence", {})
    targets = [t["name"] for t in d.get("l1_binding", {}).get("targets", [])]
    print(f'\n## {d["name"]} ({d["id"]})')
    print(f'  cdi_risk={l3.get("cdi_risk")} ddi_risk={l3.get("ddi_risk")} '
          f'tolerance={l3.get("tolerance")}')
    print(f'  PMIDs={len(ev.get("pmids",[]))} sources={ev.get("source_count")}')
    print(f'  L1 targets: {targets}')
