# ============================================================
# DQF verification gate on Kaggle CPU (reusable).
#
# Push: copy this file into a kernel dir as dqf-gate-verify-cpu.py, set EXPECTED_HEAD
# to the pushed commit, `kaggle kernels push -p <dir>`; pull results with
# `kaggle kernels output rikirinjani/dqf-gate-verify-cpu -p <dir>`.
#
# Steps: clone @ EXPECTED_HEAD -> deps -> 4 suites -> 352-query grid (with gate
# invariants) -> scoped smoke -> hard-gate membership snapshot.
# Output: /kaggle/working/gate_results.json
# ============================================================
import json
import os
import subprocess
import sys

REPO = "https://github.com/rikirinjani/DQF.git"
EXPECTED_HEAD = "__HEAD__"
# Optional: base64 of a `git diff` against EXPECTED_HEAD, applied after the clone so
# uncommitted work can be verified before the user approves a commit/push.
PATCH_B64 = "__PATCH__"
REPO_DIR = "/tmp/dqf-repo"
RESULTS = {"expected_head": EXPECTED_HEAD}

subprocess.run(["git", "clone", "--depth", "1", REPO, REPO_DIR], check=True, timeout=300)
head = subprocess.run(["git", "-C", REPO_DIR, "rev-parse", "--short=7", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
RESULTS["head"] = head
print("HEAD:", head, "| expected:", EXPECTED_HEAD, flush=True)
assert head == EXPECTED_HEAD[:7], f"HEAD mismatch: {head} != {EXPECTED_HEAD}"
if PATCH_B64 and PATCH_B64 != "__PATCH__":
    import base64
    import hashlib
    patch = base64.b64decode(PATCH_B64)
    RESULTS["patch_sha256"] = hashlib.sha256(patch).hexdigest()
    subprocess.run(["git", "-C", REPO_DIR, "apply", "--whitespace=nowarn", "-"],
                   input=patch, check=True)
    print("applied patch", RESULTS["patch_sha256"][:12], flush=True)

subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                "fastapi", "uvicorn", "pydantic", "requests"], check=True)

SUITES = [
    "rag-queries/test_indication_gate.py",
    "rag-queries/test_scorer_hardening.py",
    "rag-queries/test_anticoagulant_scorer.py",
    "rag-queries/test_merge_lock.py",
    "rag-queries/test_typed_evidence.py",
    "rag-queries/smoke_api_grid.py",
]
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
ok = True
for t in SUITES:
    r = subprocess.run([sys.executable, t], cwd=REPO_DIR, capture_output=True, text=True, env=env)
    lines = (r.stdout or "").strip().splitlines()
    fails = [l for l in lines if l.strip().startswith(("FAIL", "ERROR"))]
    RESULTS[t] = {"rc": r.returncode, "tail": lines[-1] if lines else "",
                  "fails": fails[:10], "stderr": (r.stderr or "")[-600:] if r.returncode else ""}
    ok &= r.returncode == 0
    print(f"{t}: rc={r.returncode} | {RESULTS[t]['tail']}", flush=True)

SNAP = r'''
import asyncio, json, sys
sys.path.insert(0, "api")
import server, eligibility
from server import QueryRequest
base = dict(age=45, renal_function="normal", cv_risk="low", gi_risk="low", pain_type="none",
            drug_class="any", prioritize="balanced", pregnancy_status="not_pregnant",
            lactation="no", hepatic_function="normal")
out = {}
r = asyncio.run(server.query_drugs(QueryRequest(**base, objective="erosive_esophagitis_healing")))
out["scoped"] = {"status": r["status"], "ranked": [x["id"] for x in r["eligible_ranked"]],
                 "unranked": len(r["eligible_unranked"]), "excluded": len(r["excluded"])}
for name, kw in (("pregnant", {"pregnancy_status": "third_trimester"}),
                 ("hepatic_moderate", {"hepatic_function": "moderate"}),
                 ("hepatic_severe", {"hepatic_function": "severe"})):
    r = asyncio.run(server.query_drugs(QueryRequest(**dict(base, **kw))))
    out[name] = {"results": len(r["results"]), "excluded": sorted(x["id"] for x in r["excluded"])}
r = asyncio.run(server.query_drugs(QueryRequest(**dict(base, age=70, pain_type="inflammatory"))))
out["legacy_status"] = r.get("status")
out["legacy_summary"] = r["summary"]
out["legacy_top3"] = [x["id"] for x in r["results"][:3]]
nulls = {f: sorted(d["id"] for d in server.drugs if d.get(f) is None)
         for f in ("pregnancy_safety", "lactation_safety", "hepatic_safety")}
out["null_safety_fields"] = nulls
print(json.dumps(out))
'''
r = subprocess.run([sys.executable, "-c", SNAP], cwd=REPO_DIR, capture_output=True, text=True,
                   env=env)
try:
    RESULTS["snapshot"] = json.loads(r.stdout.strip().splitlines()[-1])
except Exception:
    RESULTS["snapshot"] = {"error": (r.stderr or r.stdout)[-800:]}
    ok = False
print(json.dumps(RESULTS["snapshot"], indent=1), flush=True)

RESULTS["verdict"] = "PASS" if ok else "FAIL"
with open("/kaggle/working/gate_results.json", "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, indent=1)
print("VERDICT:", RESULTS["verdict"], flush=True)
