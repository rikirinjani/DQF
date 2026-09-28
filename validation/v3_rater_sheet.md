# V3 Rater Sheet — Pharmacist Ranking Template

Instructions for raters:

1. For each scenario below: read the vignette, then rank **all** candidate drugs from most (1)
   to least appropriate for that patient and the stated priority.
2. Rank every candidate — no ties, no omissions.
3. Give a confidence (1–5) and a one-line rationale per scenario.
4. Work **independently**. Do not discuss with other raters until all sheets are submitted.
5. You will not see DQF scores, L1–L4 data, or any other rater's rankings — by design.

---

## Per-scenario template (copy once per scenario)

```
Scenario: V3-S0X
Vignette: <age/sex; condition; renal/hepatic function; concomitant meds; priority note>
Candidates (presented order): <as shown on your randomized sheet>

Your ranking (1 = most appropriate):
  1.
  2.
  3.
  ...

Confidence (1-5): ___
Rationale (one line): _______________________________________________
```

---

## Data-entry format

Submit one JSON file per rater: `validation/v3_rater_R<1|2|3>.json`

```json
{
  "rater_id": "R1",
  "submitted_at": "2026-XX-XXTXX:XX:XX",
  "scenario_order_seed": 42,
  "rankings": {
    "V3-S01": ["<id>", "<id>", "<id>", "<id>", "<id>"],
    "V3-S02": ["<id>", "<id>", "<id>", "<id>"],
    "V3-S03": ["<id>", "<id>", "<id>", "<id>", "<id>"],
    "V3-S04": ["<id>", "<id>", "<id>", "<id>", "<id>", "<id>"],
    "V3-S05": ["<id>", "<id>", "<id>", "<id>", "<id>"],
    "V3-S06": ["<id>", "<id>", "<id>", "<id>", "<id>"],
    "V3-S07": ["<id>", "<id>", "<id>", "<id>", "<id>"],
    "V3-S08": ["<id>", "<id>", "<id>", "<id>", "<id>"],
    "V3-S09": ["<id>", "<id>", "<id>", "<id>", "<id>"],
    "V3-S10": ["<id>", "<id>", "<id>", "<id>"],
    "V3-S11": ["<id>", "<id>", "<id>", "<id>"],
    "V3-S12": ["<id>", "<id>", "<id>", "<id>"]
  },
  "confidence": {
    "V3-S01": 4,
    "V3-S02": 4,
    "V3-S03": 3,
    "V3-S04": 3,
    "V3-S05": 4,
    "V3-S06": 4,
    "V3-S07": 3,
    "V3-S08": 4,
    "V3-S09": 5,
    "V3-S10": 4,
    "V3-S11": 4,
    "V3-S12": 3
  },
  "rationale": {
    "V3-S01": "one line",
    "V3-S02": "one line",
    "V3-S03": "one line",
    "V3-S04": "one line",
    "V3-S05": "one line",
    "V3-S06": "one line",
    "V3-S07": "one line",
    "V3-S08": "one line",
    "V3-S09": "one line",
    "V3-S10": "one line",
    "V3-S11": "one line",
    "V3-S12": "one line"
  }
}
```

Rules (validated by `v3_agreement.py` before analysis):

- Every scenario V3-S01…V3-S12 present in `rankings`, `confidence`, `rationale`.
- Each `rankings` entry is a **permutation of that scenario's candidate ids** from
  `validation/v3-scenarios.json` (real drug ids only; same set, any order).
- `confidence` values are integers 1–5.
- Long-format CSV also accepted: rows `scenario_id,drug,rank` (one row per candidate); the
  script converts to the same structure.

Candidate counts per scenario for reference: S01 5, S02 4, S03 5, S04 6, S05 5, S06 5,
S07 5, S08 5, S09 5, S10 4, S11 4, S12 4 (57 candidate items total).
