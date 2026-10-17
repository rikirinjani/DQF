#!/usr/bin/env python3
"""Apply user-approved label-sourced safety fields to api/drugs.json.

Source of truth: rag-queries/curation/label_sourcing_safety_fields.json (evidence
commit 277962a). Approved 2026-10-17 in full, including the statin pregnancy
downgrade (X -> 'avoid ...' -> D).

Only proposals with a non-null value are written; null proposals (label silent /
not in DailyMed) leave the stored value untouched, and so do stored values that are
already label-sourced narratives ending in "(label)" (only warfarin, from E1). A pre-apply backup goes to
rag-queries/l3_output/_backups/ (repo convention), written the same way as merge_l3.
Run: python rag-queries/curation/apply_label_safety.py [--dry-run]
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRUGS = ROOT / "api" / "drugs.json"
EVIDENCE = Path(__file__).resolve().parent / "label_sourcing_safety_fields.json"
BACKUP_DIR = ROOT / "rag-queries" / "l3_output" / "_backups"
FIELDS = ("pregnancy_safety", "lactation_safety", "hepatic_safety")


def main(dry_run=False):
    data = json.load(open(DRUGS, encoding="utf-8"))
    ev = json.load(open(EVIDENCE, encoding="utf-8"))
    by_id = {d["id"]: d for d in data["drugs"]}
    changes = []
    for drug_id, row in ev["proposals"].items():
        drug = by_id[drug_id]
        for field in FIELDS:
            new = row[field]["proposed"]
            if new is None or drug.get(field) == new:
                continue
            cur = drug.get(field)
            if isinstance(cur, str) and cur.endswith("(label)"):
                # earlier label-sourced adjudication (E1/N6) is kept: it is at
                # least as specific (e.g. warfarin "except mechanical heart valves")
                print(f"KEEP {drug_id:16s} {field:17s} {cur!r} (proposed {new!r})")
                continue
            changes.append((drug_id, field, drug.get(field), new))
            drug[field] = new
    for c in changes:
        print(f"{c[0]:16s} {c[1]:17s} {c[2]!r} -> {c[3]!r}")
    print(f"{len(changes)} cell changes across {len({c[0] for c in changes})} drugs")
    if dry_run:
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DRUGS, BACKUP_DIR / f"drugs_{stamp}_label_safety.json")
    with open(DRUGS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"written; backup drugs_{stamp}_label_safety.json")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
