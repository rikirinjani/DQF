#!/usr/bin/env python3
"""P2-0 typed evidence tests — mechanical unwrap of nested NNT/A1c endpoints.

Covers the D1 (2026-10-17) contract for api/evidence.json `endpoints`:
  - 77 records, per class NSAID 10 / Statin 6 / Antihypertensive 33 / Diabetes 28
  - values and doses verbatim from drugs.json, same JSON number type
  - exact field set and order; every record legacy_unsourced, nothing invented
  - Diabetes A1c moved off the nnt_bp_control key; units/direction per endpoint
  - CI strings parsed, missing CI recorded as not_reported
  - objective-scoped `evidence` (5 PPI rows) and drugs.json untouched (D4)
  - scoped path ignores `endpoints`; migration builder reproduces the stored section
Run: python rag-queries/test_typed_evidence.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))
sys.path.insert(0, str(ROOT / "rag-queries" / "curation"))

DRUGS = json.load(open(ROOT / "api" / "drugs.json", encoding="utf-8"))["drugs"]
EVIDENCE = json.load(open(ROOT / "api" / "evidence.json", encoding="utf-8"))
ENDPOINTS = EVIDENCE["endpoints"]
BY_ID = {d["id"]: d for d in DRUGS}

# class -> (source key, typed endpoint key, expected count)
SOURCES = {
    "NSAID": ("nnt_50_pain_relief", "nnt_50_pain_relief", 10),
    "Statin": ("nnt_mace_5yr", "nnt_mace_5yr", 6),
    "Antihypertensive": ("nnt_bp_control", "nnt_bp_control", 33),
    "Diabetes": ("nnt_bp_control", "a1c_reduction", 28),
}
FIELDS = ["endpoint", "value", "unit", "direction", "comparator", "horizon_weeks",
          "population", "dose", "source", "uncertainty", "derived_from", "status"]
PPI_VALUES = {"omeprazole": 85, "esomeprazole": 90, "pantoprazole": 89,
              "lansoprazole": 86, "rabeprazole": 84}
PPI_FIELDS = ["value", "unit", "comparator", "horizon_weeks", "population", "dose",
              "source", "uncertainty"]
CI_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$")


def _records():
    for drug_id, recs in ENDPOINTS.items():
        for endpoint, rec in recs.items():
            yield drug_id, endpoint, rec


def _source(drug_id):
    cls = BY_ID[drug_id]["class"]
    return cls, BY_ID[drug_id]["l4_clinical"][SOURCES[cls][0]]


def test_endpoint_counts():
    counts = {c: 0 for c in SOURCES}
    for drug_id, _, _ in _records():
        counts[BY_ID[drug_id]["class"]] += 1
    assert sum(counts.values()) == 77, counts
    assert counts == {c: n for c, (_, _, n) in SOURCES.items()}, counts


def test_values_equal_legacy_source():
    for drug_id, endpoint, rec in _records():
        cls, src = _source(drug_id)
        assert endpoint == SOURCES[cls][1], (drug_id, endpoint)
        legacy = src["a1c_reduction"] if cls == "Diabetes" else src["value"]
        assert rec["value"] == legacy, (drug_id, rec["value"], legacy)
        assert type(rec["value"]) is type(legacy), (drug_id, type(rec["value"]), type(legacy))
        assert rec["dose"] == src["dose"], (drug_id, rec["dose"], src["dose"])


def test_record_schema_exact():
    for drug_id, _, rec in _records():
        assert list(rec.keys()) == FIELDS, (drug_id, list(rec.keys()))


def test_all_legacy_unsourced():
    for drug_id, _, rec in _records():
        assert rec["status"] == "legacy_unsourced", drug_id
        for field in ("source", "comparator", "horizon_weeks", "population"):
            assert rec[field] is None, (drug_id, field, rec[field])


def test_units_and_direction():
    for drug_id, endpoint, rec in _records():
        if BY_ID[drug_id]["class"] == "Diabetes":
            assert endpoint == "a1c_reduction" and rec["endpoint"] == "a1c_reduction", drug_id
            assert rec["unit"] == "percentage_points", drug_id
            assert rec["direction"] == "higher_better", drug_id
        else:
            assert rec["unit"] == "nnt", drug_id
            assert rec["direction"] == "lower_better", drug_id
    for drug_id, recs in ENDPOINTS.items():
        if BY_ID[drug_id]["class"] == "Diabetes":
            assert "nnt_bp_control" not in recs, drug_id


def test_uncertainty_parsed():
    for drug_id, _, rec in _records():
        cls, src = _source(drug_id)
        unc = rec["uncertainty"]
        if cls == "Diabetes":
            assert unc == {"kind": "not_reported"}, (drug_id, unc)
            continue
        if src["ci_95"] is None:
            assert unc == {"kind": "not_reported"}, (drug_id, unc)
            continue
        assert unc["kind"] == "ci_95", (drug_id, unc)
        assert unc["raw"] == src["ci_95"], (drug_id, unc)
        assert unc["low"] <= unc["high"], (drug_id, unc)
        m = CI_RE.match(unc["raw"])
        assert m, (drug_id, unc)
        assert unc["low"] == float(m.group(1)) and unc["high"] == float(m.group(2)), (drug_id, unc)
        assert type(unc["low"]) is float and type(unc["high"]) is float, (drug_id, unc)
    assert ENDPOINTS["lovastatin"]["nnt_mace_5yr"]["uncertainty"] == {"kind": "not_reported"}


def test_objective_evidence_untouched():
    ev = EVIDENCE["evidence"]
    assert set(ev) == set(PPI_VALUES), sorted(ev)
    for drug_id, value in PPI_VALUES.items():
        assert list(ev[drug_id]) == ["erosive_esophagitis_healing"], (drug_id, list(ev[drug_id]))
        rec = ev[drug_id]["erosive_esophagitis_healing"]
        assert list(rec.keys()) == PPI_FIELDS, (drug_id, list(rec.keys()))
        assert rec["value"] == value, (drug_id, rec["value"])


def test_drugs_json_not_modified():
    diabetes = [d for d in DRUGS if d["class"] == "Diabetes"]
    assert len(diabetes) == 28, len(diabetes)
    for d in diabetes:
        assert "a1c_reduction" in d["l4_clinical"]["nnt_bp_control"], d["id"]
        assert "a1c_reduction" not in d["l4_clinical"], d["id"]


def test_scoped_path_unaffected():
    import eligibility
    ev = eligibility.evidence_for("omeprazole", "erosive_esophagitis_healing")
    assert ev == EVIDENCE["evidence"]["omeprazole"]["erosive_esophagitis_healing"], ev
    for objective in ("erosive_esophagitis_healing", "nnt_50_pain_relief"):
        assert eligibility.evidence_for("ibuprofen", objective) is None, objective


def test_migration_idempotent():
    from migrate_typed_evidence import build_endpoints
    assert build_endpoints(DRUGS) == ENDPOINTS


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
        except Exception as e:
            failed += 1
            print(f"  ERROR {t.__name__}: {e!r}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
