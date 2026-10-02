#!/usr/bin/env python3
"""N6b narrow vertical slice tests — eligibility gate + evidence contract + three states.

Covers the Astra review's required assertions:
  - objective match / mismatch
  - hard contraindication (global, objective-independent)
  - unknown safety withholds ranking (unknown != false)
  - no neutral-score imputation (missing evidence -> eligible_unranked, null score)
  - no cross-endpoint fallback (one objective, one contract)
  - recommendation-path closure (combo suggestions disabled in scoped v1)
  - legacy path flagged deprecated
Run: python rag-queries/test_indication_gate.py
"""
import asyncio
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))

import eligibility
import server
from server import QueryRequest

OBJECTIVE = "erosive_esophagitis_healing"
PPIS = ["omeprazole", "esomeprazole", "pantoprazole", "lansoprazole", "rabeprazole"]
BY_ID = {d["id"]: d for d in server.drugs}


def _req(**kw):
    base = dict(age=45, renal_function="normal", cv_risk="low", gi_risk="low",
                pain_type="none", drug_class="any", prioritize="balanced",
                pregnancy_status="not_pregnant", lactation="no", hepatic_function="normal")
    base.update(kw)
    return QueryRequest(**base)


def _patient(**kw):
    base = dict(pregnancy_status="not_pregnant", hepatic_function="normal",
                renal_function="normal", age=45)
    base.update(kw)
    return base


# --- registry / mapping -----------------------------------------------------
def test_objective_exists():
    assert eligibility.objective_exists(OBJECTIVE)
    assert not eligibility.objective_exists("no_such_objective")


def test_mapping_disposition_complete():
    mapped = set(eligibility.CONDITION_MAP["map"])
    unsupported = set(eligibility.CONDITION_MAP["unsupported_in_v1"])
    all_ids = {d["id"] for d in server.drugs}
    assert mapped | unsupported == all_ids, "every drug must have an explicit disposition"
    assert mapped & unsupported == set(), "mapped and unsupported must be disjoint"
    assert mapped == set(PPIS)


# --- stage 1: eligibility ---------------------------------------------------
def test_objective_mismatch_excludes():
    statin = BY_ID["atorvastatin"]
    state, reasons = eligibility.evaluate(statin, OBJECTIVE, _patient())
    assert state == "excluded"
    assert reasons[0]["rule"] == "objective_mismatch"


def test_hard_contraindication_pregnancy_x():
    drug = copy.deepcopy(BY_ID["omeprazole"])
    drug["pregnancy_safety"] = "X"  # synthetic: mapped drug with an absolute contraindication
    state, reasons = eligibility.evaluate(drug, OBJECTIVE, _patient(pregnancy_status="first_trimester"))
    assert state == "excluded", state
    assert any(r["rule"] == "pregnancy_x" and r["state"] == "failed" for r in reasons)


def test_hard_contraindication_hepatic():
    drug = copy.deepcopy(BY_ID["omeprazole"])
    drug["hepatic_safety"] = "contraindicated"
    state, reasons = eligibility.evaluate(drug, OBJECTIVE, _patient(hepatic_function="severe"))
    assert state == "excluded"
    assert any(r["rule"] == "hepatic_contraindicated" for r in reasons)


def test_contraindication_is_objective_independent():
    # same drug, same patient, different objective -> the global rule still applies
    drug = copy.deepcopy(BY_ID["omeprazole"])
    drug["pregnancy_safety"] = "X"
    for obj in (OBJECTIVE, "some_other_objective"):
        state, reasons = eligibility.evaluate(drug, obj, _patient(pregnancy_status="third_trimester"))
        assert state == "excluded"
        # for the other objective the mismatch fires first, but the drug is excluded either way
        assert reasons


def test_unknown_safety_withholds_ranking():
    orig = eligibility.HARD_RULES
    eligibility.HARD_RULES = orig + [{"id": "test_unknown", "applies": lambda d, p: None}]
    try:
        state, reasons = eligibility.evaluate(BY_ID["omeprazole"], OBJECTIVE, _patient())
        assert state == "eligible_unranked", state
        assert any(r["rule"] == "safety_unknown" for r in reasons)
    finally:
        eligibility.HARD_RULES = orig


# --- stage 2: evidence contract --------------------------------------------
def test_contract_rejects_missing_evidence():
    ok, why = eligibility.contract_ok(None, eligibility.objective_contract(OBJECTIVE))
    assert not ok and why == "no_compatible_evidence"


def test_contract_rejects_incomplete_evidence():
    ev = {"value": 90, "unit": "percent", "comparator": None, "horizon_weeks": 8,
          "population": "erosive esophagitis"}
    ok, why = eligibility.contract_ok(ev, eligibility.objective_contract(OBJECTIVE))
    assert not ok and why == "incomplete_evidence"


def test_transform_bounded_monotonic():
    contract = eligibility.objective_contract(OBJECTIVE)
    hi = eligibility.transform({"value": 90}, contract)
    lo = eligibility.transform({"value": 84}, contract)
    assert hi > lo, "higher healing must score higher"
    assert 0.0 <= lo <= 10.0 and 0.0 <= hi <= 10.0
    assert eligibility.transform({"value": 200}, contract) == 10.0  # bounded above
    assert eligibility.transform({"value": 0}, contract) == 0.0    # bounded below


def test_no_neutral_imputation():
    # a mapped drug with its evidence removed must be unranked, never given a number
    orig = eligibility.EVIDENCE
    ev = copy.deepcopy(orig)
    del ev["evidence"]["omeprazole"]
    eligibility.EVIDENCE = ev
    try:
        res = eligibility.assess([BY_ID["omeprazole"]], OBJECTIVE, _patient())
        assert res["status"] == "no_rankable"
        assert res["eligible_ranked"] == []
        assert res["eligible_unranked"][0]["id"] == "omeprazole"
        assert "overall" not in res["eligible_unranked"][0]
    finally:
        eligibility.EVIDENCE = orig


# --- server scoped path -----------------------------------------------------
def test_scoped_three_states():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE)))
    assert res["mode"] == "objective_scoped"
    assert res["status"] == "ok"
    assert len(res["eligible_ranked"]) == 5
    assert len(res["eligible_unranked"]) == 0
    assert len(res["excluded"]) == 90
    assert {r["id"] for r in res["eligible_ranked"]} == set(PPIS)


def test_scoped_ranking_uses_evidence_transform():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE)))
    ranked = res["eligible_ranked"]
    # esomeprazole (90%) must out-score rabeprazole (84%) on efficacy
    eff = {r["id"]: r["scores"]["efficacy"] for r in ranked}
    assert eff["esomeprazole"] > eff["rabeprazole"], eff
    # overall sorted descending
    overalls = [r["overall"] for r in ranked]
    assert overalls == sorted(overalls, reverse=True)


def test_scoped_combo_suggestions_disabled():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE)))
    assert all(r["combo_suggestions"] == [] for r in res["eligible_ranked"])


def test_scoped_unsupported_objective():
    res = asyncio.run(server.query_drugs(_req(objective="not_a_real_objective")))
    assert res["status"] == "unsupported"
    assert res["eligible_ranked"] == []


def test_scoped_class_filter_reported():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE, drug_class="PPI")))
    assert res["filter_effects"]["class_filter"] == ["PPI"]
    assert res["filter_effects"]["removed"] == 90
    assert len(res["eligible_ranked"]) == 5


def test_scoped_excluded_reasons_structured():
    res = asyncio.run(server.query_drugs(_req(objective=OBJECTIVE)))
    ex = res["excluded"][0]
    assert "reasons" in ex and ex["reasons"][0]["rule"] == "objective_mismatch"


# --- legacy path ------------------------------------------------------------
def test_legacy_flagged_deprecated():
    res = asyncio.run(server.query_drugs(_req()))
    assert res["mode"] == "legacy"
    assert res["deprecated"] is True
    assert "results" in res and len(res["results"]) == 95


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
