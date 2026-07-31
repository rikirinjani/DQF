import json, glob, os
dig = r"C:\Users\think\AppData\Local\Temp\opencode\l2b_digests"
other_drugs = ["clonidine","hydrochlorothiazide","chlorthalidone","labetalol","nifedipine","metoprolol","atenolol","uridine","rosmarinic","hydroxychloroquine"]
for fp in sorted(glob.glob(os.path.join(dig, "*.json"))):
    j = json.load(open(fp, encoding="utf-8"))
    tot = 0; fields_hit = []
    for fn, f in j.get("fields", {}).items():
        ev = f.get("evidence") or []
        hit = [s for s in ev if any(d in s["text"].lower() for d in other_drugs)]
        if hit:
            tot += len(hit); fields_hit.append(f"{fn}:{len(hit)}")
    if tot:
        print(f"{j['drug_id']:16s} pool_rel={j.get('pool_relevance_pct')}%  cross-drug evidence={tot}  [{', '.join(fields_hit)}]")
