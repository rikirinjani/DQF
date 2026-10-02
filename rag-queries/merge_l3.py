#!/usr/bin/env python3
"""
merge_l3.py -- Merge extracted L3 profiles into drugs.json.

Usage:
    python merge_l3.py                          # merge all available profiles
    python merge_l3.py --dry-run                # preview without writing
    python merge_l3.py --restore                # restore backup from merge
    python merge_l3.py --unlock ddi_risk,renal_risk   # unlock specific fields for this run
    python merge_l3.py --unlock-all             # pre-N6.5 behavior: no locks

What it does:
    1. Reads drugs.json + all l3_output/{drug_id}_l3_profile.json
    2. For each drug with a profile, patches its l3_systems field
    3. Writes updated drugs.json (with .bak backup)

Lock semantics (N6.5): fields in DEFAULT_LOCKED_FIELDS are human-adjudicated
and are never overwritten by a pipeline re-run while a non-empty expert value
exists -- scalars AND lists (locked lists are kept verbatim; the pipeline
never appends to them, so expert deletions survive). Rescore flows that must
update a locked field pass an explicit --unlock / --unlock-all.
"""

import json, os, shutil, sys
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

def dry_run(profiles: dict[str, dict], drugs: list[dict], locked: set[str] | None = None):
    """Show what would be merged."""
    locked = DEFAULT_LOCKED_FIELDS if locked is None else locked
    print(f"\n{'='*60}")
    print(f"  DRY RUN -- {len(profiles)} profiles to merge")
    print(f"  Locked fields ({len(locked)}): {', '.join(sorted(locked))}")
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
            lock_note = ""
            if k in locked and k in has:
                cur = has.get(k)
                keep = (len(cur) > 0) if isinstance(cur, list) else (cur is not None)
                if keep:
                    lock_note = "  [LOCKED - expert value kept]"
                    arrow = " KEEP "
            print(f"    {arrow} {k}: {old_s} -> {new_s}{lock_note}")
        evidence = profile.get("_evidence", {})
        print(f"        PMIDs: {len(evidence.get('pmids', []))} | "
              f"Sources: {evidence.get('source_count', 0)}")

    print(f"\n  Total: {len(profiles)} drugs will be updated in {DRUGS_JSON.name}")
    print(f"  {'='*60}\n")


def backup_drugs_json():
    """Create timestamped backup before modifying (collision-safe)."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"drugs_{ts}.json"
    n = 1
    while backup.exists():  # same-second collisions get a suffix
        backup = BACKUP_DIR / f"drugs_{ts}_{n}.json"
        n += 1
    shutil.copy2(DRUGS_JSON, backup)
    print(f"  Backup written: {backup}")
    return backup


# Fields whose current values were set by human adjudication and must NOT be
# silently overwritten by a pipeline re-run. N6.5 Option B (approved): the
# re-assessment candidate set (6 high-stakes risk dims) UNION every l3 dim
# actually adjudicated in N6.1-N6.4, so the lock list matches what humans
# really curated. nnt_mace_5yr is l4_clinical (merge only patches l3_systems)
# and is intentionally absent. Unlock per run via --unlock/--unlock-all.
DEFAULT_LOCKED_FIELDS: set[str] = {
    # worklist candidate (re-assessment REG-02/RES-03)
    "gi_risk", "cv_risk", "ddi_risk", "renal_risk", "bleeding_risk", "gi_bleeding_risk",
    # N6.1-6.4 adjudicated dims (changes, keeps-with-basis, batch-3 vetting)
    "acid_rebound", "barrier_protection", "bone_fracture_risk", "bp_reduction",
    "cdi_risk", "cv_outcome_benefit", "electrolyte_risk", "gi_tolerability",
    "heart_rate_effect", "hypoglycemia_risk", "metabolic_effect", "myopathy_risk",
    "neutralization_capacity", "raft_strength", "reflux_suppression", "renal_benefit",
    "renal_protection", "renal_toxicity_risk", "weight_effect",
}


def merge(profiles: dict[str, dict], drugs: list[dict], write: bool = True,
          locked_fields: set[str] | None = None) -> int:
    """Patch l3_systems for each matching drug. Returns count of drugs updated.

    locked_fields: dims whose CURRENT drugs.json values are human-adjudicated;
    a pipeline re-run never overwrites them (a None/empty pipeline value still
    leaves the expert value untouched, as before). Locked LISTS are kept
    verbatim -- the pipeline never appends to them, so expert deletions
    survive. None (default) = DEFAULT_LOCKED_FIELDS; pass an explicit set to
    override (use set() for full pipeline behavior).
    """
    locked = DEFAULT_LOCKED_FIELDS if locked_fields is None else set(locked_fields)
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
            # Locked (human-adjudicated) dims: the expert value wins VERBATIM,
            # for scalars and lists alike. This check runs before type handling
            # so locked lists are kept as-is -- the pipeline never appends to
            # them (deletion-respecting: items an expert removed stay removed).
            # An absent expert value (None or an empty list) is no expert value
            # at all, so the pipeline still fills it.
            if k in locked and k in existing:
                cur = existing[k]
                if isinstance(cur, list):
                    if len(cur) > 0:
                        continue
                elif cur is not None:
                    continue
            if v is None or (isinstance(v, list) and len(v) == 0):
                # Pipeline found no data -- keep expert value if it exists
                if k not in existing:
                    existing[k] = v
            elif isinstance(v, list):
                # Merge lists (e.g., off_targets): pipeline + expert, deduplicated
                # (unlocked fields only -- locked lists returned above)
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
                # (locked dims with an expert value returned above)
                existing[k] = v

        # Attach evidence trail to the drug entry (not in l3_systems schema)
        evidence = profile.get("_evidence", {})
        note = profile.get("_note", "")
        existing["_evidence"] = evidence
        existing["_note"] = note

        drug["l3_systems"] = existing
        updated += 1

    if write:
        # Atomic write: dump to a sibling temp file, then os.replace — a crash
        # mid-write can no longer leave a truncated drugs.json behind.
        tmp = DRUGS_JSON.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"drugs": drugs}, f, indent=2, ensure_ascii=False)
        os.replace(tmp, DRUGS_JSON)
        print(f"  Updated {DRUGS_JSON} ({updated} drugs patched, atomic write)")
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
    parser.add_argument("--only", metavar="ID[,ID...]",
                        help="Limit the merge to these drug ids. Profiles for drugs "
                             "outside this list are ignored -- use it whenever a merge "
                             "must not touch the rest of drugs.json. Without it the "
                             "merge is repo-wide and will overwrite values that were "
                             "later adjudicated by hand (the profile files keep their "
                             "original auto-score, so a re-merge reverts them).")
    parser.add_argument("--unlock", metavar="FIELD[,FIELD...]",
                        help="Remove these fields from the default lock set for this run "
                             "(explicit unlock for pipeline rescore flows).")
    parser.add_argument("--unlock-all", action="store_true",
                        help="Disable locking entirely (pre-N6.5 behavior).")
    args = parser.parse_args()

    if args.restore:
        restore_latest()
        return

    locked = set() if args.unlock_all else set(DEFAULT_LOCKED_FIELDS)
    if args.unlock:
        locked -= {f.strip() for f in args.unlock.split(",") if f.strip()}

    if not DRUGS_JSON.exists():
        print(f"  ERROR: {DRUGS_JSON} not found", file=sys.stderr)
        sys.exit(1)

    drugs = load_json(DRUGS_JSON)["drugs"]
    profiles = find_profiles()

    if not profiles:
        print("  No L3 profiles found -- run extract_l3.py first")
        return

    if args.only:
        wanted = {i.strip() for i in args.only.split(",") if i.strip()}
        unknown = wanted - set(profiles)
        if unknown:
            print(f"  ERROR: no profile for {sorted(unknown)}", file=sys.stderr)
            sys.exit(1)
        profiles = {k: v for k, v in profiles.items() if k in wanted}
        print(f"  --only: limiting merge to {sorted(profiles)}")

    # Exclude metadata-only profiles (_summary.json data)
    if args.dry_run:
        dry_run(profiles, drugs, locked)
        return

    backup_drugs_json()
    count = merge(profiles, drugs, write=True, locked_fields=locked)
    print(f"  Done. {count}/{len(profiles)} profiles merged "
          f"({len(locked)} fields locked).")


if __name__ == "__main__":
    main()
