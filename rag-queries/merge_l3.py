#!/usr/bin/env python3
"""
merge_l3.py -- Merge extracted L3 profiles into drugs.json.

Usage:
    python merge_l3.py                          # merge all available profiles
    python merge_l3.py --dry-run                # preview without writing
    python merge_l3.py --restore                # restore backup from merge

What it does:
    1. Reads drugs.json + all l3_output/{drug_id}_l3_profile.json
    2. For each drug with a profile, patches its l3_systems field
    3. Writes updated drugs.json (with .bak backup)
"""

import json, shutil, sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DRUGS_JSON = PROJECT_DIR / "api" / "drugs.json"
L3_DIR = SCRIPT_DIR / "l3_output"
BACKUP_DIR = SCRIPT_DIR / "l3_output" / "_backups"


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_profiles() -> dict[str, dict]:
    """Return {drug_id: profile_dict} for every *_l3_profile.json found."""
    profiles = {}
    for f in sorted(L3_DIR.glob("*_l3_profile.json")):
        drug_id = f.stem.replace("_l3_profile", "")
        profiles[drug_id] = load_json(f)
    return profiles


def _safe(val) -> str:
    """Convert any value to print-safe ASCII string."""
    s = json.dumps(val, ensure_ascii=True) if not isinstance(val, str) else repr(val)
    return s

def dry_run(profiles: dict[str, dict], drugs: list[dict]):
    """Show what would be merged."""
    print(f"\n{'='*60}")
    print(f"  DRY RUN -- {len(profiles)} profiles to merge")
    print(f"{'='*60}")
    for drug_id, profile in sorted(profiles.items()):
        drug = next((d for d in drugs if d["id"] == drug_id), None)
        has = drug.get("l3_systems", {}) if drug else {}
        fields = {k: v for k, v in profile.items() if not k.startswith("_")}
        populated = {k: v for k, v in fields.items() if v is not None and v != []}
        existing = {k: v for k, v in has.items() if v is not None and v != []}

        print(f"\n  {drug_id} -- {len(populated)} fields -> merge")
        for k, v in sorted(populated.items()):
            old_val = existing.get(k, None)
            old_s = _safe(old_val) if old_val is not None else "--"
            new_s = _safe(v)
            arrow = "UPDATE" if k in existing else "  NEW "
            print(f"    {arrow} {k}: {old_s} -> {new_s}")
        evidence = profile.get("_evidence", {})
        print(f"        PMIDs: {len(evidence.get('pmids', []))} | "
              f"Sources: {evidence.get('source_count', 0)}")

    print(f"\n  Total: {len(profiles)} drugs will be updated in {DRUGS_JSON.name}")
    print(f"  {'='*60}\n")


def backup_drugs_json():
    """Create timestamped backup before modifying."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"drugs_{ts}.json"
    shutil.copy2(DRUGS_JSON, backup)
    print(f"  Backup written: {backup}")
    return backup


def merge(profiles: dict[str, dict], drugs: list[dict], write: bool = True) -> int:
    """Patch l3_systems for each matching drug. Returns count of drugs updated."""
    updated = 0
    for drug in drugs:
        drug_id = drug["id"]
        if drug_id not in profiles:
            continue

        profile = profiles[drug_id]
        # Strip metadata fields before merging into schema
        l3_data = {k: v for k, v in profile.items() if not k.startswith("_")}

        # Merge into existing l3_systems (preserve fields the pipeline doesn't touch)
        existing = drug.get("l3_systems", {})
        for k, v in l3_data.items():
            if v is None or (isinstance(v, list) and len(v) == 0):
                # Pipeline found no data -- keep expert value if it exists
                if k not in existing:
                    existing[k] = v
            elif isinstance(v, list):
                # Merge lists (e.g., off_targets): pipeline + expert, deduplicated
                expert_list = existing.get(k, [])
                if isinstance(expert_list, list):
                    # Combine, normalize case, deduplicate preserving order
                    seen = set()
                    combined = []
                    for item in expert_list + v:
                        key = item.lower().strip() if isinstance(item, str) else str(item)
                        if key not in seen:
                            seen.add(key)
                            combined.append(item)
                    existing[k] = combined
                else:
                    existing[k] = v
            else:
                # Scalar field: pipeline's evidence-based value takes priority
                existing[k] = v

        # Attach evidence trail to the drug entry (not in l3_systems schema)
        evidence = profile.get("_evidence", {})
        note = profile.get("_note", "")
        existing["_evidence"] = evidence
        existing["_note"] = note

        drug["l3_systems"] = existing
        updated += 1

    if write:
        with open(DRUGS_JSON, "w", encoding="utf-8") as f:
            json.dump({"drugs": drugs}, f, indent=2, ensure_ascii=False)
        print(f"  Updated {DRUGS_JSON} ({updated} drugs patched)")
    return updated


def restore_latest():
    """Restore the most recent backup."""
    backups = sorted(BACKUP_DIR.glob("drugs_*.json"))
    if not backups:
        print("  No backups found.")
        return
    latest = backups[-1]
    shutil.copy2(latest, DRUGS_JSON)
    print(f"  Restored {DRUGS_JSON} from {latest.name}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Merge L3 profiles into drugs.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--restore", action="store_true", help="Restore latest backup")
    args = parser.parse_args()

    if args.restore:
        restore_latest()
        return

    if not DRUGS_JSON.exists():
        print(f"  ERROR: {DRUGS_JSON} not found", file=sys.stderr)
        sys.exit(1)

    drugs = load_json(DRUGS_JSON)["drugs"]
    profiles = find_profiles()

    if not profiles:
        print("  No L3 profiles found -- run extract_l3.py first")
        return

    # Exclude metadata-only profiles (_summary.json data)
    if args.dry_run:
        dry_run(profiles, drugs)
        return

    backup_drugs_json()
    count = merge(profiles, drugs, write=True)
    print(f"  Done. {count}/{len(profiles)} profiles merged.")


if __name__ == "__main__":
    main()
