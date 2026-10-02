#!/usr/bin/env python3
"""Tests for merge_l3 lock semantics (N6.5).

Covers: default lock (scalar + list + deletion-respecting + empty-fill),
explicit set() override, unlocked list combine, DEFAULT set contents.
Run: python rag-queries/test_merge_lock.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import merge_l3


def _mk(expert: dict) -> dict:
    return {"id": "d1", "l3_systems": dict(expert)}


def _run(expert: dict, incoming: dict, locked=None) -> dict:
    drug = _mk(expert)
    merge_l3.merge({"d1": dict(incoming)}, [drug], write=False, locked_fields=locked)
    return drug["l3_systems"]


def test_default_lock_scalar():
    out = _run({"ddi_risk": 2}, {"ddi_risk": 3})          # locked_fields=None
    assert out["ddi_risk"] == 2, f"expert scalar must win, got {out['ddi_risk']}"


def test_default_lock_list_deletion_respecting():
    # expert DELETED items from the list; pipeline still carries them -> they
    # must NOT be re-added (the pre-N6.5 bug appended expert + incoming).
    out = _run({"off_targets": ["A"]}, {"off_targets": ["A", "B"]})   # off_targets unlocked
    assert out["off_targets"] == ["A", "B"], out
    out = _run({"pleiotropic_effects": ["x"]}, {"pleiotropic_effects": ["x", "y"]})
    # pleiotropic_effects is unlocked too -> combine; use a locked list field
    # via explicit locked set to prove list-lock semantics:
    out = _run({"gi_risk": ["kept"]}, {"gi_risk": ["kept", "readded"]},
               locked={"gi_risk"})
    assert out["gi_risk"] == ["kept"], f"locked list kept verbatim, got {out['gi_risk']}"


def test_locked_empty_value_still_filled():
    out = _run({"ddi_risk": None}, {"ddi_risk": 3})
    assert out["ddi_risk"] == 3, "None expert value must be filled by pipeline"
    out = _run({"gi_risk": []}, {"gi_risk": ["x"]}, locked={"gi_risk"})
    assert out["gi_risk"] == ["x"], "empty expert list must be filled by pipeline"
    out = _run({}, {"ddi_risk": 2})
    assert out["ddi_risk"] == 2, "absent expert value must be filled by pipeline"


def test_explicit_empty_set_disables_lock():
    out = _run({"ddi_risk": 2}, {"ddi_risk": 3}, locked=set())
    assert out["ddi_risk"] == 3, "explicit set() = pre-N6.5 pipeline behavior"


def test_unlock_subset():
    # default would lock ddi_risk; unlocking it lets the pipeline win, while
    # renal_risk stays locked
    out = _run({"ddi_risk": 2, "renal_risk": 1},
               {"ddi_risk": 3, "renal_risk": 3},
               locked=merge_l3.DEFAULT_LOCKED_FIELDS - {"ddi_risk"})
    assert out["ddi_risk"] == 3, f"unlocked field must update, got {out['ddi_risk']}"
    assert out["renal_risk"] == 1, f"still-locked field must hold, got {out['renal_risk']}"


def test_unlocked_list_combines_dedup():
    out = _run({"off_targets": ["A"]}, {"off_targets": ["a", "B"]}, locked=set())
    assert out["off_targets"] == ["A", "B"], out


def test_default_set_contents():
    d = merge_l3.DEFAULT_LOCKED_FIELDS
    cand = {"gi_risk", "cv_risk", "ddi_risk", "renal_risk", "bleeding_risk", "gi_bleeding_risk"}
    assert cand <= d, f"worklist candidates missing: {cand - d}"
    assert len(d) == 25, f"expected 25 locked fields, got {len(d)}: {sorted(d)}"
    assert "nnt_mace_5yr" not in d, "nnt_mace_5yr is l4_clinical, must not be in lock set"


def test_default_lock_unrelated_fields_untouched():
    out = _run({"bp_reduction": 1}, {"bp_reduction": 3})   # bp_reduction IS locked (N6-adjudicated)
    assert out["bp_reduction"] == 1, out
    out = _run({"lipophilicity": 1}, {"lipophilicity": 2})  # unlocked dim
    assert out["lipophilicity"] == 2, out


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
