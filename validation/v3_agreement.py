#!/usr/bin/env python3
"""
v3_agreement.py -- Inter-rater reliability analysis for V3 (pharmacist ranking vs DQF).

Reads rater files (JSON primary; long-format CSV accepted) + validation/v3-scenarios.json,
computes agreement metrics, prints a report.

Metrics:
    - Weighted kappa (quadratic weights), per scenario per rater pair, on ordinal rank
      positions; averaged across scenarios. Primary for 2 raters.
    - Kendall's W (tie-corrected), per scenario, for >=3 raters; averaged.
    - Spearman rho (midrank-based), per scenario: rater pairs + rater-vs-DQF; averaged.
    - Top-1 agreement and top-3 Jaccard, rater vs DQF.

Usage:
    python validation/v3_agreement.py --raters validation/v3_rater_R1.json [more files...]
    python validation/v3_agreement.py --raters a.json --scenarios path/to/v3-scenarios.json
    python validation/v3_agreement.py --selftest        # SYNTHETIC sample, proves it runs
    python validation/v3_agreement.py --help

NO rater data exists yet. Any agreement numbers this script prints come from the files you
pass in. The --selftest input is loudly labelled SYNTHETIC and must never be presented as
real results.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SCENARIOS = SCRIPT_DIR / "v3-scenarios.json"


# ---------------------------------------------------------------------------
# Rank helpers
# ---------------------------------------------------------------------------

def midranks(ranking):
    """ranking: list of ids, best first -> {id: midrank}. Ties share average position.

    Ties are detected by an explicit ties list when available; here we accept a parallel
    optional argument `ties` (list of id-lists) from v3-scenarios.json. Without it, equal
    positions cannot be inferred from a submitted permutation (raters submit strict orders),
    so ranks are 1..n.
    """
    n = len(ranking)
    return {rid: float(i + 1) for i, rid in enumerate(ranking)}


def midranks_with_ties(ranking, ties):
    """ranking: list of ids best first; ties: list of id-lists sharing a DQF overall score.
    Returns {id: midrank}."""
    ranks = {rid: float(i + 1) for i, rid in enumerate(ranking)}
    for group in ties or []:
        pos = [ranks[g] for g in group if g in ranks]
        if len(pos) > 1:
            mid = sum(pos) / len(pos)
            for g in group:
                if g in ranks:
                    ranks[g] = mid
    return ranks


def _pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return float("nan")
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / (sxx * syy) ** 0.5


def spearman(ranks_a, ranks_b, ids):
    """Spearman rho on midranks over the shared id list."""
    xs = [ranks_a[i] for i in ids]
    ys = [ranks_b[i] for i in ids]
    return _pearson(xs, ys)


def weighted_kappa(ranks_a, ranks_b, ids):
    """Quadratic-weighted kappa between two raters' ordinal rank positions.

    Categories are the rank positions 1..n for this scenario's candidate set. Weights
    w_ij = (i - j)^2 / (n - 1)^2. kappa = 1 - sum(w*O) / sum(w*E).
    """
    n = len(ids)
    if n < 2:
        return float("nan")
    denom = (n - 1) ** 2
    # Build the confusion matrix over items: O_ij = count(items where rater A gives
    # rank i and rater B gives rank j) / n
    conf = {}
    obs = exp = 0.0
    for a in ids:
        i = int(round(ranks_a[a]))
        j = int(round(ranks_b[a]))
        conf[(i, j)] = conf.get((i, j), 0) + 1
    total = len(ids)
    row_marg = {}
    col_marg = {}
    for (i, j), c in conf.items():
        row_marg[i] = row_marg.get(i, 0) + c
        col_marg[j] = col_marg.get(j, 0) + c
    for (i, j), c in conf.items():
        w = ((i - j) ** 2) / denom
        obs += w * (c / total)
    for i in row_marg:
        for j in col_marg:
            w = ((i - j) ** 2) / denom
            exp += w * (row_marg[i] / total) * (col_marg[j] / total)
    if exp == 0:
        return float("nan")
    return 1.0 - obs / exp


def kendalls_w(rank_dicts, ids):
    """Tie-corrected Kendall's W for k raters (rank_dicts: list of {id: rank}) on ids."""
    k = len(rank_dicts)
    n = len(ids)
    if k < 2 or n < 2:
        return float("nan")
    # Rank sums per item
    rank_sums = {i: sum(rd[i] for rd in rank_dicts) for i in ids}
    mean_rs = sum(rank_sums.values()) / n
    S = sum((rs - mean_rs) ** 2 for rs in rank_sums.values())
    # Tie correction: for each rater, for each tied group of size t, T_j = t^3 - t
    tie_term = 0.0
    for rd in rank_dicts:
        vals = {}
        for i in ids:
            vals.setdefault(rd[i], 0)
            vals[rd[i]] += 1
        for t in vals.values():
            if t > 1:
                tie_term += t ** 3 - t
    denom = k ** 2 * (n ** 3 - n) - k * tie_term
    if denom == 0:
        return float("nan")
    return (12 * S) / denom


def top1_and_top3(ranks_a, ranks_b, ids):
    """Top-1 agreement (bool) and top-3 Jaccard between two rankings (midrank dicts).

    Top-1 counts as a match if the rater's top-1 drug sits in the other ranking's top
    group, ties included (midrank == min) -- a tied top-1 is not a mismatch.
    """
    order_a = sorted(ids, key=lambda i: ranks_a[i])
    order_b = sorted(ids, key=lambda i: ranks_b[i])
    a_top = order_a[0]
    min_b = min(ranks_b[i] for i in ids)
    top1 = ranks_b[a_top] == min_b
    set_a, set_b = set(order_a[:3]), set(order_b[:3])
    jac = len(set_a & set_b) / len(set_a | set_b) if (set_a | set_b) else float("nan")
    return top1, jac


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_rater_json(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return {
        "rater_id": d.get("rater_id", Path(path).stem),
        "rankings": d["rankings"],
        "confidence": d.get("confidence", {}),
        "rationale": d.get("rationale", {}),
    }


def load_rater_csv(path):
    """Long-format CSV: scenario_id,drug,rank (one row per candidate)."""
    rankings = {}
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sid, drug, rank = row["scenario_id"], row["drug"], int(row["rank"])
            rankings.setdefault(sid, {})[drug] = rank
    # convert {sid: {drug: rank}} -> {sid: [drug by rank]}
    out = {}
    for sid, dr in rankings.items():
        out[sid] = [d for d, _ in sorted(dr.items(), key=lambda kv: kv[1])]
    return {"rater_id": Path(path).stem, "rankings": out, "confidence": {}, "rationale": {}}


def load_rater(path):
    p = Path(path)
    if p.suffix.lower() == ".csv":
        return load_rater_csv(p)
    return load_rater_json(p)


def validate_rater(rater, scenarios):
    """Check: all scenarios present; each ranking is a permutation of the candidates."""
    errs = []
    for sid, sc in scenarios.items():
        if sid not in rater["rankings"]:
            errs.append(f"{rater['rater_id']}: missing scenario {sid}")
            continue
        got = list(rater["rankings"][sid])
        want = list(sc["candidates"])
        if sorted(got) != sorted(want):
            errs.append(f"{rater['rater_id']} {sid}: ranking is not a permutation of candidates "
                        f"(got {sorted(got)}, want {sorted(want)})")
        conf = rater["confidence"].get(sid)
        if conf is not None and not (isinstance(conf, int) and 1 <= conf <= 5):
            errs.append(f"{rater['rater_id']} {sid}: confidence {conf!r} not an int in 1-5")
    return errs


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(raters, scenarios):
    """raters: list of rater dicts; scenarios: {sid: scenario dict}. Returns report dict."""
    rater_by_id = {r["rater_id"]: r for r in raters}
    per_sc = {}
    agg = {
        "weighted_kappa_pairs": [],
        "spearman_pairs": [],
        "spearman_vs_dqf": [],
        "kendalls_w": [],
        "top1_vs_dqf": [],
        "top3_jaccard_vs_dqf": [],
    }
    disagreements = []

    for sid, sc in sorted(scenarios.items()):
        dqf = sc["dqf"]
        dqf_ranks = midranks_with_ties(dqf["ranking"], dqf.get("ties", []))
        ids = list(sc["candidates"])
        entry = {"n_candidates": len(ids)}

        r_ranks = {}
        for r in raters:
            if sid in r["rankings"]:
                r_ranks[r["rater_id"]] = midranks(list(r["rankings"][sid]))

        # rater pairs
        rater_ids = sorted(r_ranks)
        kappas, rhos = [], []
        for a_i in range(len(rater_ids)):
            for b_i in range(a_i + 1, len(rater_ids)):
                a, b = rater_ids[a_i], rater_ids[b_i]
                k = weighted_kappa(r_ranks[a], r_ranks[b], ids)
                s = spearman(r_ranks[a], r_ranks[b], ids)
                kappas.append(k)
                rhos.append(s)
                agg["weighted_kappa_pairs"].append(k)
                agg["spearman_pairs"].append(s)
        if len(rater_ids) >= 3:
            w = kendalls_w([r_ranks[r] for r in rater_ids], ids)
            agg["kendalls_w"].append(w)
            entry["kendalls_w"] = w

        # rater vs DQF
        for r in rater_ids:
            s = spearman(r_ranks[r], dqf_ranks, ids)
            t1, j3 = top1_and_top3(r_ranks[r], dqf_ranks, ids)
            agg["spearman_vs_dqf"].append(s)
            agg["top1_vs_dqf"].append(t1)
            agg["top3_jaccard_vs_dqf"].append(j3)
            entry.setdefault("vs_dqf", {})[r] = {"spearman": s, "top1": t1, "top3_jaccard": j3}
            if (s == s and s < 0.4) or not t1:
                disagreements.append({
                    "scenario": sid, "rater": r, "spearman_vs_dqf": s, "top1_match": t1,
                    "rater_ranking": list(sorted(ids, key=lambda i: r_ranks[r][i])),
                    "dqf_ranking": list(dqf["ranking"]),
                    "rater_rationale": rater_by_id[r]["rationale"].get(sid, ""),
                })

        if kappas:
            entry["weighted_kappa_mean"] = sum(kappas) / len(kappas)
        if rhos:
            entry["spearman_mean"] = sum(rhos) / len(rhos)
        per_sc[sid] = entry

    def mean(xs):
        xs = [x for x in xs if x == x]
        return sum(xs) / len(xs) if xs else float("nan")

    summary = {
        "n_raters": len(raters),
        "n_scenarios": len(scenarios),
        "mean_weighted_kappa_rater_pairs": mean(agg["weighted_kappa_pairs"]),
        "mean_spearman_rater_pairs": mean(agg["spearman_pairs"]),
        "mean_spearman_vs_dqf": mean(agg["spearman_vs_dqf"]),
        "mean_kendalls_w": mean(agg["kendalls_w"]),
        "top1_agreement_vs_dqf": mean([1.0 if t else 0.0 for t in agg["top1_vs_dqf"]]),
        "mean_top3_jaccard_vs_dqf": mean(agg["top3_jaccard_vs_dqf"]),
        "n_disagreements_flagged": len(disagreements),
    }
    return {"summary": summary, "per_scenario": per_sc, "disagreements": disagreements}


def print_report(report, raters):
    s = report["summary"]
    print("=" * 64)
    print("  V3 inter-rater agreement report")
    print("=" * 64)
    print(f"  raters: {s['n_raters']}  |  scenarios: {s['n_scenarios']}")
    print()
    print("  Summary metrics")
    print(f"    weighted kappa (rater pairs, mean): {s['mean_weighted_kappa_rater_pairs']:.3f}")
    print(f"    Spearman rho   (rater pairs, mean): {s['mean_spearman_rater_pairs']:.3f}")
    print(f"    Spearman rho   (vs DQF, mean):      {s['mean_spearman_vs_dqf']:.3f}")
    if s["mean_kendalls_w"] == s["mean_kendalls_w"]:
        print(f"    Kendall's W    (>=3 raters, mean):  {s['mean_kendalls_w']:.3f}")
    print(f"    top-1 agreement vs DQF:             {s['top1_agreement_vs_dqf']:.1%}")
    print(f"    top-3 Jaccard  vs DQF (mean):       {s['mean_top3_jaccard_vs_dqf']:.3f}")
    print(f"    disagreements flagged:              {s['n_disagreements_flagged']}")
    print()
    print("  Per scenario")
    for sid, e in sorted(report["per_scenario"].items()):
        bits = [f"n={e['n_candidates']}"]
        if "weighted_kappa_mean" in e:
            bits.append(f"kappa={e['weighted_kappa_mean']:.2f}")
        if "spearman_mean" in e:
            bits.append(f"rho={e['spearman_mean']:.2f}")
        if "kendalls_w" in e:
            bits.append(f"W={e['kendalls_w']:.2f}")
        for r, v in sorted(e.get("vs_dqf", {}).items()):
            bits.append(f"{r}:rho={v['spearman']:.2f},top1={'Y' if v['top1'] else 'N'}")
        print(f"    {sid}: " + "  ".join(bits))
    if report["disagreements"]:
        print()
        print("  Disagreements flagged (rho < 0.4 or top-1 mismatch) -- document each:")
        for d in report["disagreements"]:
            print(f"    {d['scenario']} rater {d['rater']}: top1={'match' if d['top1_match'] else 'MISMATCH'}"
                  f"  rho={d['spearman_vs_dqf']:.2f}")
            print(f"      rater: {d['rater_ranking']}")
            print(f"      DQF:   {d['dqf_ranking']}")
            if d["rater_rationale"]:
                print(f"      rationale: {d['rater_rationale']}")
    print()
    print("  Success criteria (protocol): inter-rater kappa >= 0.4 (good >= 0.6);")
    print("  rater-vs-DQF rho >= 0.4 (good >= 0.6); top-1 >= 50% (good >= 70%).")
    print("=" * 64)


# ---------------------------------------------------------------------------
# Self-test (SYNTHETIC -- never present as results)
# ---------------------------------------------------------------------------

def selftest():
    print("!" * 64)
    print("!!  SELFTEST -- SYNTHETIC INPUT, NOT REAL RESULTS                  !!")
    print("!!  All numbers below come from fabricated rankings used only      !!")
    print("!!  to prove this script runs. Never cite them as findings.        !!")
    print("!" * 64)
    scenarios = {
        "SYN-S1": {
            "candidates": ["a", "b", "c", "d"],
            "dqf": {"ranking": ["a", "b", "c", "d"], "ties": []},
        },
        "SYN-S2": {
            "candidates": ["a", "b", "c"],
            "dqf": {"ranking": ["b", "a", "c"], "ties": [["a", "b"]]},
        },
    }
    raters = [
        {"rater_id": "SYN-R1", "rankings": {"SYN-S1": ["a", "b", "c", "d"], "SYN-S2": ["b", "a", "c"]},
         "confidence": {"SYN-S1": 4, "SYN-S2": 3}, "rationale": {"SYN-S1": "synthetic", "SYN-S2": "synthetic"}},
        {"rater_id": "SYN-R2", "rankings": {"SYN-S1": ["a", "c", "b", "d"], "SYN-S2": ["a", "b", "c"]},
         "confidence": {"SYN-S1": 3, "SYN-S2": 4}, "rationale": {"SYN-S1": "synthetic", "SYN-S2": "synthetic"}},
        {"rater_id": "SYN-R3", "rankings": {"SYN-S1": ["b", "a", "d", "c"], "SYN-S2": ["c", "b", "a"]},
         "confidence": {"SYN-S1": 2, "SYN-S2": 2}, "rationale": {"SYN-S1": "synthetic", "SYN-S2": "synthetic"}},
    ]
    # validation must pass on the synthetic input
    for r in raters:
        errs = validate_rater(r, scenarios)
        assert not errs, f"selftest validation failed: {errs}"
    report = analyze(raters, scenarios)
    print_report(report, raters)
    # sanity assertions on known synthetic structure
    assert report["summary"]["n_raters"] == 3
    assert report["summary"]["n_scenarios"] == 2
    assert report["summary"]["mean_kendalls_w"] == report["summary"]["mean_kendalls_w"]
    print("SELFTEST PASSED: metrics computed, validation gate works, report prints.")


def main():
    ap = argparse.ArgumentParser(
        description="V3 inter-rater agreement analysis (pharmacist ranking vs DQF). "
                    "Pass real rater files with --raters; --selftest runs a SYNTHETIC check.")
    ap.add_argument("--raters", nargs="+", metavar="FILE",
                    help="rater files: v3_rater_R*.json (or long-format CSV scenario_id,drug,rank)")
    ap.add_argument("--scenarios", metavar="FILE", default=str(DEFAULT_SCENARIOS),
                    help=f"scenarios file (default: {DEFAULT_SCENARIOS})")
    ap.add_argument("--selftest", action="store_true",
                    help="run the SYNTHETIC self-test (proves the script runs; not results)")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    if not args.raters:
        ap.print_help()
        print("\nERROR: no rater files given. No rater data exists yet -- collect")
        print("v3_rater_R*.json per methodology/v3-inter-rater-protocol.md, or run --selftest.")
        sys.exit(1)

    scen_path = Path(args.scenarios)
    if not scen_path.exists():
        print(f"ERROR: scenarios file not found: {scen_path}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(scen_path.read_text(encoding="utf-8"))
    scenarios = {sc["id"]: sc for sc in data["scenarios"]}

    raters = [load_rater(p) for p in args.raters]
    all_errs = []
    for r in raters:
        all_errs.extend(validate_rater(r, scenarios))
    if all_errs:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in all_errs:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)

    report = analyze(raters, scenarios)
    print_report(report, raters)


if __name__ == "__main__":
    main()
