<!-- run: run-2026-05-13-tk5 | stage: 06-development | dispatch: B (validator, producer-blind) | author: Gimli the dwarf -->

# S3 Implementation Notes — Stage 6 Development, Dispatch B

> *"That module was built by dwarf-craft. It will hold."* — Gimli

## Producer-validator separation evidence

This dispatch (B) authored Story 3 **without sharing context with the
dispatch that wrote Stories 1+2** (lib/metrics.py + lib/baseline.py).
Fixtures, assertions, and the README were derived from:

- `.delivery/artifacts/05-plan/po/stories.md` (Story 3 ACs)
- `.delivery/artifacts/05-plan/qa/test-cases.md` (TC-S3-*)
- `delivery-team/architecture/smoke-test-architecture.md`
- `.delivery/artifacts/04-architect/adrs/ADR-tk5-001-smoke-test-runner-architecture.md`
- the producer module **public surface** (function names, dataclass fields,
  return shapes) — necessary to write tests, not internal implementation.

No edits made to any file under `delivery-team/tests/smoke/lib/`. Read-only
isolation honored. BC-03 satisfied.

## Files written

### Category 1 — pytest meta-tests + fixture workspace

- `delivery-team/tests/smoke/tests/__init__.py` (empty package marker)
- `delivery-team/tests/smoke/tests/conftest.py`
  - Fixtures: `smoke_root`, `repo_root`, `lib_path` (autouse sys.path
    inserter), `valid_stream_events`, `malformed_stream_event`,
    `synthetic_baseline`, `passing_report`, `hard_fail_report`,
    `advisory_warn_report`, `sample_workspace_dir`, `sample_workspace`.
  - Autouse guard: `_block_claude_subprocess` monkeypatches
    `subprocess.Popen` and `subprocess.run` to raise `AssertionError` for
    any command whose head is `claude`.
- `delivery-team/tests/smoke/tests/test_meta.py` — exactly 3 test functions:
  - `test_malformed_stream_fault_injection` — feeds 3 valid + 1 malformed
    event to `parse_stream`; asserts no raise, `warnings.warn` fired,
    `dispatch_count == 3`, `cost_usd ≈ 0.30`.
  - `test_baseline_comparison_demo` — 3 sub-assertions:
    PASS (within bands), FAIL (cost_usd > hard_max), WARN (tokens.input
    outside ±2σ). Verifies `RegressionResult.status` in each branch.
  - `test_aggregator_fixture_parsing` — calls `aggregate()` against the
    on-disk fixture workspace, asserts 4 distinct skills,
    `stages_completed=7`, `stories_completed=3`, `defects_logged=2`,
    `telemetry_rows_real=5`.
- `delivery-team/tests/smoke/tests/fixtures/sample-workspace/.delivery/telemetry/skill-loads.jsonl`
  — 5 JSON-per-line rows across 4 distinct skills (developer appears 2×).
- `delivery-team/tests/smoke/tests/fixtures/sample-workspace/.delivery/state.md`
  — `stages_completed: 7`, `defects_logged: 2`, plus a `## Stories`
  section with 3 `- [x]` checkmarks.
- `delivery-team/tests/smoke/tests/fixtures/sample-workspace/.delivery/telemetry/run-summary-fake.json`
  — `overall.rows_real: 5`, all 7 stages marked completed.

### Category 2 — README

- `delivery-team/tests/smoke/README.md` — all 10 required sections, with
  the verbatim substring `feedback_claude_code_local_only` and the full
  binding memory file path
  `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md`.

### Category 3 — Makefile

- `Makefile` (NEW at repo root, did not exist pre-S3) — three `.PHONY`
  targets: `smoke`, `smoke-baseline`, `smoke-tests`, plus a `help` target
  listing them. The `smoke` target invokes
  `python3 delivery-team/tests/smoke/run_smoke.py --cost-cap 3.00 --timeout 1800`
  per AC-S3-06.

## Pytest run output

```
$ cd delivery-team/tests/smoke && python3 -m pytest tests/ -v
============================= test session starts ==============================
platform linux -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: /var/home/meconnelly/.../delivery-team/tests/smoke
collecting ... collected 3 items

tests/test_meta.py::test_malformed_stream_fault_injection PASSED   [ 33%]
tests/test_meta.py::test_baseline_comparison_demo          PASSED   [ 66%]
tests/test_meta.py::test_aggregator_fixture_parsing        PASSED   [100%]

============================== 3 passed in 0.02s ===============================
```

Wall-clock: **0.02 s** — far inside the 5-second budget (AC-S3-01).
`--collect-only` confirms exactly 3 test functions (AC-S3-08).

## AC traceability

| AC | Evidence |
|----|----------|
| AC-S3-01 | pytest reports 3 passed in 0.02s; no `claude` spawn (autouse guard verified by test pass) |
| AC-S3-02 | `test_malformed_stream_fault_injection` — warning + dispatch_count assertion |
| AC-S3-03 | `test_baseline_comparison_demo` — 3 sub-assertions (PASS/FAIL/WARN) |
| AC-S3-04 | `test_aggregator_fixture_parsing` — fixture workspace + hand-computed expectations |
| AC-S3-05 | README has all 10 sections + memory path + `feedback_claude_code_local_only` substring |
| AC-S3-06 | root `Makefile` exists with `.PHONY: smoke smoke-baseline smoke-tests help`; `make -n smoke` prints expected command |
| AC-S3-07 | All `lib` imports are deferred to inside fixture/test bodies (grep confirmed) |
| AC-S3-08 | `pytest --collect-only -q` shows exactly 3 test functions |

## Make target dry-run check

```
$ make -n smoke
python3 delivery-team/tests/smoke/run_smoke.py --cost-cap 3.00 --timeout 1800

$ make -n smoke-baseline
python3 delivery-team/tests/smoke/run_smoke.py --init-baseline --cost-cap 3.00 --timeout 1800

$ make -n smoke-tests
cd delivery-team/tests/smoke && python3 -m pytest tests/ -v

$ make help
Available targets:
  smoke           Run the delivery-team plugin smoke test (single run, local-only).
  smoke-baseline  Run the smoke test 5x sequentially and write baseline JSON.
  smoke-tests     Run the pytest meta-tests (fast, no claude spawn).
```

## Deviations

None material. Notes:

- The `conftest.py::_block_claude_subprocess` autouse guard patches both
  `subprocess.Popen` and `subprocess.run` (the task spec mentioned Popen
  only). Patching both is strictly stronger and costs nothing — any future
  test that calls `subprocess.run(["claude", ...])` would otherwise slip
  past the Popen-only guard.
- The on-disk fixture workspace lays files at
  `tests/fixtures/sample-workspace/.delivery/...` (not under a nested
  `work/` subdir). The `sample_workspace` fixture sets
  `ws.home = sample_workspace_dir`, which makes `aggregator.aggregate()`
  read from the fallback `<home>/.delivery/` path after the primary
  `<home>/work/.delivery/` lookup misses. Both paths exercised in the
  aggregator's read logic.
- Makefile help target included even though the task spec showed only the
  three smoke targets — included because `make help` is the conventional
  discovery interface and TC-S3-08 (in the test-cases doc, not in this
  dispatch's gate list) explicitly checks for it.

## Defects found (none requiring patches)

No defects in `lib/metrics.py`, `lib/baseline.py`, or `lib/aggregator.py`
surfaced while writing meta-tests. The producer modules' contracts match
the architecture doc and the PRD AC table.

## Producer-validator audit trail

```
$ grep -n "^from lib\|^import lib" delivery-team/tests/smoke/tests/test_meta.py
(no matches — all lib imports are inside function bodies)

$ grep -n "from lib\|import lib" delivery-team/tests/smoke/tests/test_meta.py
46:    from lib.metrics import Metrics, parse_stream
90:    from lib.baseline import RegressionResult, compare
148:    from lib.aggregator import aggregate
149:    from lib.metrics import Metrics
```

All imports are inside test functions — no module-level coupling. Stage 7
git-author check will distinguish this dispatch from S1+S2's commits.

— Gimli, son of Glóin. Seventeen commits! Three tests! All pass!
And my code!
