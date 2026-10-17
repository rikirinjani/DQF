#!/usr/bin/env python3
"""N6b Phase 2 step P2-1: give Diabetes A1c its own l4_clinical key.

The 28 Diabetes drugs store A1c reduction under l4_clinical.nnt_bp_control
({a1c_reduction, unit "%", dose}), a BP NNT key (review RISK 1 collision). This adds
l4_clinical.a1c_efficacy = {value, unit "percentage_points", dose}, copied verbatim
from that dict, directly after nnt_bp_control. nnt_bp_control stays as a legacy alias
until Phase 3 legacy retirement (user decision D4, 2026-10-17).

Key name: a1c_efficacy, the name proposed by the 2026-07-31 L4 schema audit
(api/l4_schema_map.json). Not "a1c_reduction": every Diabetes drug already has
l3_systems.a1c_reduction, an L3 keyword score with a different meaning.

Source of truth for the values: api/evidence.json endpoints.<id>.a1c_reduction
(P2-0, d673c61); the script cross-checks it against nnt_bp_control.a1c_reduction.
All validation runs before any write; a pre-apply backup goes to
rag-queries/l3_output/_backups/. Re-running is a no-op.
Run: python rag-queries/curation/apply_a1c_efficacy.py [--dry-run]
"""
import difflib
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRUGS = ROOT / "api" / "drugs.json"
EVIDENCE = ROOT / "api" / "evidence.json"
BACKUP_DIR = ROOT / "rag-queries" / "l3_output" / "_backups"
PROPOSAL = Path(__file__).resolve().parent / "p2-1-a1c-efficacy-proposal.json"
DIFF = Path(__file__).resolve().parent / "p2-1-a1c-efficacy-dry-run.diff"
KEY = "a1c_efficacy"
EXPECTED = 28


def _dump(data):
    return json.dumps(data, indent=2, ensure_ascii=False)


def _with_key_after(l4, after, key, value):
    """Rebuild l4 with key inserted right after `after` (key order is the diff)."""
    out = {}
    for k, v in l4.items():
        if k == key:
            continue
        out[k] = v
        if k == after:
            out[key] = value
    return out


def build(drugs, endpoints):
    """Return [(drug_id, new_value)] for every Diabetes drug; raise on any mismatch."""
    rows = []
    for d in drugs:
        if d["class"] != "Diabetes":
            continue
        src = (d.get("l4_clinical") or {}).get("nnt_bp_control")
        if not isinstance(src, dict) or set(src) != {"a1c_reduction", "unit", "dose"} \
                or src["unit"] != "%":
            raise ValueError(f"{d['id']}: unexpected nnt_bp_control {src!r}")
        typed = (endpoints.get(d["id"]) or {}).get("a1c_reduction") or {}
        v = src["a1c_reduction"]
        if typed.get("value") != v or type(typed.get("value")) is not type(v) \
                or typed.get("dose") != src["dose"]:
            raise ValueError(f"{d['id']}: evidence.json endpoint {typed!r} != {src!r}")
        rows.append((d["id"], {"value": v, "unit": "percentage_points", "dose": src["dose"]}))
    if len(rows) != EXPECTED:
        raise ValueError(f"{len(rows)} Diabetes drugs, expected {EXPECTED}")
    return rows


def main(dry_run=False):
    before = open(DRUGS, encoding="utf-8").read()
    data = json.loads(before)
    if _dump(data) != before:
        raise ValueError("drugs.json does not round-trip; refusing to rewrite it")
    endpoints = json.load(open(EVIDENCE, encoding="utf-8"))["endpoints"]
    rows = build(data["drugs"], endpoints)
    by_id = {d["id"]: d for d in data["drugs"]}
    changed = 0
    for drug_id, value in rows:
        l4 = by_id[drug_id]["l4_clinical"]
        if l4.get(KEY) == value:
            continue
        if KEY in l4:
            raise ValueError(f"{drug_id}: existing {KEY} {l4[KEY]!r} differs; not overwriting")
        by_id[drug_id]["l4_clinical"] = _with_key_after(l4, "nnt_bp_control", KEY, value)
        changed += 1
    after = _dump(data)
    print(f"{changed} drugs gain l4_clinical.{KEY} ({len(rows)} Diabetes drugs checked)")
    if dry_run:
        with open(PROPOSAL, "w", encoding="utf-8") as f:
            json.dump({"status": "PROPOSED", "step": "P2-1",
                       "generated": datetime.now().date().isoformat(),
                       "key": f"l4_clinical.{KEY}", "alias_kept": "l4_clinical.nnt_bp_control",
                       "source": "api/evidence.json endpoints.<id>.a1c_reduction (P2-0, d673c61)",
                       "count": len(rows), "changes": dict(rows)},
                      f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(DIFF, "w", encoding="utf-8", newline="\n") as f:  # LF: git apply-able
            f.writelines(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                              "a/api/drugs.json", "b/api/drugs.json", n=2))
        print(f"proposal -> {PROPOSAL.name}; diff -> {DIFF.name}")
        return
    if not changed:
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DRUGS, BACKUP_DIR / f"drugs_{stamp}_p2_1.json")
    with open(DRUGS, "w", encoding="utf-8") as f:
        f.write(after)
    print(f"written; backup drugs_{stamp}_p2_1.json")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
