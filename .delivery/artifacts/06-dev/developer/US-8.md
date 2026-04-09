# US-8 — DoD validator deterministic constraint checks

**Author:** Gimli (developer alias) · **Status:** CODE_COMPLETE

## Deliverables

- `delivery-team/skills/delivery-flow/scripts/check_dod_constraints.py`
  stdlib-only Python 3, PyYAML-with-fallback loader (mirrors US-1).
- `delivery-team/skills/delivery-flow/references/fixtures/constraints-dod-sample.yml`
  Uses ADR-003 enumerated forbidden-vocabulary subset + Löwy citation.
- `delivery-team/skills/delivery-flow/references/fixtures/dod-artifact-clean.md`
- `delivery-team/skills/delivery-flow/references/fixtures/dod-artifact-contaminated.md`

## Checks implemented

| # | Check                     | Severity | AC    |
|---|---------------------------|----------|-------|
| 1 | Forbidden-vocab grep      | FAIL     | 8.1   |
| 2 | Mandatory artifact exists | FAIL     | 8.2   |
| 3 | Numeric ceilings summary  | INFO     | 8.3   |
| 4 | Löwy citation shape       | WARN     | 8.4   |

Check 1 uses a compiled `re` alternation with `(?<![A-Za-z0-9_])...(?![...])`
anchors for case-insensitive whole-word match; longer tokens sorted first so
`AWS Lambda` wins over `Lambda` when both present. Check 3 is informational —
hard ceiling enforcement needs structured artifact parsing (out of MVP scope,
commented in code). Check 4 warns when Löwy / "Righting Software" entry is
absent or missing chapter/page on volatility artifacts.

## Test results

Green (clean fixture):
```
[1] PASS no forbidden tokens  [2] PASS artifacts present
[3] max_bearers=1             [4] OK Löwy citation
DoD: PASS  (exit 0)
```

Red (contaminated fixture):
```
[1] FAIL 5 matches: AWS Lambda:7, DynamoDB:8, Lambda:15, Python:15, DynamoDB:16
[2] PASS  [3] info  [4] OK
DoD: FAIL  (exit 1)
```

All four ACs exercised. Exit codes match spec (0 green, 1 red). Script is
stdlib-only and honors US-1's PyYAML fallback.
