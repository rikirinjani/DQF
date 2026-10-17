#!/usr/bin/env python3
"""P2-0: unwrap nested l4_clinical NNT/A1c endpoints into typed records in api/evidence.json.

User decision D1 (approved 2026-10-17): the 77 nested endpoint records (NSAID
nnt_50_pain_relief 10, Statin nnt_mace_5yr 6, Antihypertensive nnt_bp_control 33,
Diabetes A1c stored under nnt_bp_control 28) are copied verbatim into a new top-level
`endpoints` section, every record `status: "legacy_unsourced"`. Comparator, horizon,
population and source stay null: nothing is invented. The objective-scoped `evidence`
section (5 PPI rows) is untouched, and so is api/drugs.json (D4: legacy keys stay as
aliases until Phase 3).

All validation runs before any file is written; any shape/count deviation raises.
`endpoints` is rebuilt from drugs.json on every run, so apply is idempotent. A pre-apply
backup goes to rag-queries/l3_output/_backups/ (repo convention).
Run: python rag-queries/curation/migrate_typed_evidence.py [--dry-run]
"""
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRUGS = ROOT / "api" / "drugs.json"
EVIDENCE = ROOT / "api" / "evidence.json"
PROPOSAL = Path(__file__).resolve().parent / "p2-0-typed-evidence-proposal.json"
BACKUP_DIR = ROOT / "rag-queries" / "l3_output" / "_backups"
VERSION = "1.1.0"

# class -> (source key, typed endpoint key, expected count)
SOURCES = {
    "NSAID": ("nnt_50_pain_relief", "nnt_50_pain_relief", 10),
    "Statin": ("nnt_mace_5yr", "nnt_mace_5yr", 6),
    "Antihypertensive": ("nnt_bp_control", "nnt_bp_control", 33),
    "Diabetes": ("nnt_bp_control", "a1c_reduction", 28),
}
TOTAL = 77
NNT_KEYS = {"value", "ci_95", "dose"}
A1C_KEYS = {"a1c_reduction", "unit", "dose"}
CI_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$")


def _check_value(drug_id, v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or math.isnan(v) or v <= 0:
        raise ValueError(f"{drug_id}: invalid value {v!r}")


def _uncertainty(drug_id, ci):
    if ci is None:
        return {"kind": "not_reported"}
    m = CI_RE.match(ci) if isinstance(ci, str) else None
    if not m:
        raise ValueError(f"{drug_id}: unparseable ci_95 {ci!r}")
    low, high = float(m.group(1)), float(m.group(2))
    if low > high:
        raise ValueError(f"{drug_id}: ci_95 low > high {ci!r}")
    return {"kind": "ci_95", "low": low, "high": high, "raw": ci}


def _nnt_record(drug_id, endpoint, src_key, src):
    if not isinstance(src, dict) or set(src) != NNT_KEYS:
        raise ValueError(f"{drug_id}: {src_key} shape {src!r}")
    _check_value(drug_id, src["value"])
    return {
        "endpoint": endpoint,
        "value": src["value"],
        "unit": "nnt",
        "direction": "lower_better",
        "comparator": None,
        "horizon_weeks": None,
        "population": None,
        "dose": src["dose"],
        "source": None,
        "uncertainty": _uncertainty(drug_id, src["ci_95"]),
        "derived_from": f"api/drugs.json l4_clinical.{src_key}",
        "status": "legacy_unsourced",
    }


def _a1c_record(drug_id, src_key, src):
    if not isinstance(src, dict) or set(src) != A1C_KEYS or src["unit"] != "%":
        raise ValueError(f"{drug_id}: {src_key} shape {src!r}")
    _check_value(drug_id, src["a1c_reduction"])
    return {
        "endpoint": "a1c_reduction",
        "value": src["a1c_reduction"],
        "unit": "percentage_points",
        "direction": "higher_better",
        "comparator": None,
        "horizon_weeks": None,
        "population": None,
        "dose": src["dose"],
        "source": None,
        "uncertainty": {"kind": "not_reported"},
        "derived_from": f"api/drugs.json l4_clinical.{src_key}.a1c_reduction",
        "status": "legacy_unsourced",
    }


def build_endpoints(drugs):
    """Pure: drugs.json `drugs` list -> {drug_id: {endpoint: typed record}}. Raises on any deviation."""
    endpoints, counts = {}, {c: 0 for c in SOURCES}
    for drug in drugs:
        cls = drug.get("class")
        if cls not in SOURCES:
            continue
        src_key, endpoint, _ = SOURCES[cls]
        l4 = drug.get("l4_clinical") or {}
        if src_key not in l4:
            raise ValueError(f"{drug['id']}: missing l4_clinical.{src_key}")
        if cls == "Diabetes":
            rec = _a1c_record(drug["id"], src_key, l4[src_key])
        else:
            rec = _nnt_record(drug["id"], endpoint, src_key, l4[src_key])
        endpoints.setdefault(drug["id"], {})[endpoint] = rec
        counts[cls] += 1
    for cls, (_, _, expected) in SOURCES.items():
        if counts[cls] != expected:
            raise ValueError(f"{cls}: {counts[cls]} records, expected {expected}")
    total = sum(len(v) for v in endpoints.values())
    if total != TOTAL:
        raise ValueError(f"{total} records, expected {TOTAL}")
    return endpoints


def _write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main(dry_run=False):
    drugs = json.load(open(DRUGS, encoding="utf-8"))["drugs"]
    evidence = json.load(open(EVIDENCE, encoding="utf-8"))
    endpoints = build_endpoints(drugs)
    counts = {c: 0 for c in SOURCES}
    cls_of = {d["id"]: d.get("class") for d in drugs}
    for drug_id, recs in endpoints.items():
        counts[cls_of[drug_id]] += len(recs)
    counts["total"] = sum(counts.values())
    print(" ".join(f"{k}={v}" for k, v in counts.items()))
    if dry_run:
        head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        _write_json(PROPOSAL, {"generated": date.today().isoformat(), "base_head": head,
                               "decision": "D1 approved 2026-10-17", "counts": counts,
                               "endpoints": endpoints})
        print(f"dry run; proposal written to {PROPOSAL.relative_to(ROOT).as_posix()}")
        return
    out = {"version": VERSION, "evidence": evidence["evidence"], "endpoints": endpoints}
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(EVIDENCE, BACKUP_DIR / f"evidence_{stamp}_p2_0.json")
    _write_json(EVIDENCE, out)
    print(f"written; backup evidence_{stamp}_p2_0.json")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
