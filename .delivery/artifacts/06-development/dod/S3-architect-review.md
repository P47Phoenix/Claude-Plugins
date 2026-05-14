<!-- run: run-2026-05-13-tk5 -->
<!-- stage: 06-development -->
<!-- story: S3 — meta-tests + README + Makefile -->
<!-- reviewer: Celebrimbor (Solution Architect, DoD validation) -->
<!-- adr: ADR-tk5-001 -->
# S3 — Architect DoD Review

> *"Let us forge something that will endure beyond the ages."* — Celebrimbor

## Verdict

**STATUS: DONE**

S3 conforms to ADR-tk5-001 producer-validator separation and the
architecture intent recorded in
`delivery-team/architecture/smoke-test-architecture.md`. All five
architect gate criteria pass. No re-work required.

## Gate Results

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Producer-validator separation: tests do NOT modify/wrap `lib/*.py` | PASS | See §1 |
| 2 | Fixture workspace matches arch doc §Workspace strategy | PASS | See §2 |
| 3 | README documents local-only + cites memory file by full path (grep) | PASS | See §3 |
| 4 | Makefile target invocation matches runner CLI surface (no drift) | PASS | See §4 |
| 5 | No re-implementation of `lib/*` logic in tests | PASS | See §5 |

## 1. Producer-Validator Separation

Me Celebrimbor inspect imports + patches. Validator side never wrap
producer side.

- `tests/test_meta.py` imports `lib.metrics.parse_stream`,
  `lib.metrics.Metrics`, `lib.baseline.compare`,
  `lib.baseline.RegressionResult`, `lib.aggregator.aggregate` —
  black-box calls only, no decorator-wrapping, no subclassing.
- `tests/conftest.py` `monkeypatch.setattr` calls patch ONLY
  `subprocess.Popen` and `subprocess.run` to block accidental Claude
  spawn (an isolation guard, not a producer wrap). Grep:
  `monkeypatch.setattr.*lib\.` → 0 hits.
- No top-level redefinitions of `parse_stream`, `compare`, `aggregate`,
  `Metrics`, or `RegressionResult` in either test file. Grep:
  `^def parse_stream|^def compare|^def aggregate|^class Metrics|^class RegressionResult`
  → 0 hits.
- The `sample_workspace` fixture constructs a real `lib.workspace.Workspace`
  dataclass and assigns post-init attributes (`home`, `workdir`,
  `_setup_done`) to bypass `setup()`'s `mktemp` — this is fixture-data
  preparation for the aggregator, not a wrap of the producer's logic.

The validator dispatch authored fixtures + assertions from the
architecture doc §5–§6 contract and from BACKLOG-106 contract values
(`hard_max=3.00`, `±2σ band`, alphabetical skill-load ordering,
state.md `[x]` story checkbox semantics). Numeric invariants in
`test_meta.py` (e.g. `cost_usd == 0.30 = 0.10+0.15+0.05`, prose mean
`(800+900)/2 = 850`) are derived from the fixtures themselves, not
copied from producer source.

Note (not a defect): the architectural producer-validator commit-history
verification per ADR §"Producer-Validator Separation" is delegated to
Stage-7 UAT (Scrum Bag). At Stage-6 DoD the producer + validator
working-tree contents are intact and uncontaminated; that is the
in-stage gate.

## 2. Fixture Workspace Shape

Architecture doc §2 (Mermaid) and §5 require the aggregator to read:

- `<workspace>/.delivery/telemetry/skill-loads.jsonl`
- `<workspace>/.delivery/telemetry/run-summary-*.json` (newest)
- `<workspace>/.delivery/state.md`

Fixture tree at
`delivery-team/tests/smoke/tests/fixtures/sample-workspace/`:

```
.delivery/state.md
.delivery/telemetry/run-summary-fake.json
.delivery/telemetry/skill-loads.jsonl
```

All three present at the exact relative paths the production aggregator
walks. Content shape matches the contract:

- `skill-loads.jsonl` — 5 rows (one JSON per line), keys
  `skill | prose_tokens | timestamp_seconds` — matches
  `telemetry.py` per W3-18.
- `run-summary-fake.json` — top-level `schema_version`, `overall`,
  `stages` — matches `telemetry_run_summary.py` shape.
- `state.md` — flat key-value lines (`stages_completed: 7`,
  `defects_logged: 2`) + `## Stories` checklist with three `[x]` items —
  matches the aggregator's minimal-parser contract in arch doc §10 OQ-2.

## 3. README Local-Only Citation (Grep)

Per architecture §9 and ADR §"Local-Only Constraint", the README MUST
point back to the memory file by full path.

Grep on `delivery-team/tests/smoke/README.md`:

| Line | Match |
|------|-------|
| 20 | `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md` |
| 22 | substring handle `feedback_claude_code_local_only` |
| 135 | secondary citation in "What it does NOT do" |

Full memory path appears verbatim at line 20 in a fenced reference
block. The §"Local-only notice" prose explicitly bans
`.github/workflows/` and quotes the binding rationale. PASS.

## 4. Makefile vs Runner CLI Surface

Runner argparse (from `run_smoke.py:_build_parser`) declares
`--init-baseline`, `--cost-cap` (default 3.00), `--timeout` (default
1800), `--baseline`, `--out-dir`, `--prompt`, `--config`,
`--stream-fixture`, `--repo-root`.

Makefile invocations:

| Target | Command | Flags used | Drift? |
|---|---|---|---|
| `smoke` | `python3 delivery-team/tests/smoke/run_smoke.py --cost-cap 3.00 --timeout 1800` | `--cost-cap`, `--timeout` | None |
| `smoke-baseline` | `python3 .../run_smoke.py --init-baseline --cost-cap 3.00 --timeout 1800` | `--init-baseline`, `--cost-cap`, `--timeout` | None |
| `smoke-tests` | `cd .../smoke && python3 -m pytest tests/ -v` | (pytest) | N/A — meta-tests, no claude spawn |

Every flag the Makefile passes exists on the parser with matching value
shape (float / int). README §"Flags" table matches the parser exactly.
No drift across Makefile ↔ README ↔ runner.

## 5. No Re-implementation of `lib/*` Logic

Tests call into producer modules, never duplicate their logic:

- `parse_stream` aggregation: tests assert on `metrics.cost_usd`,
  `metrics.tokens['input']`, `metrics.dispatch_count` after invoking
  the real `parse_stream` — no second parser anywhere.
- `compare` regression decision: tests construct three fixture dicts
  (PASS / FAIL / WARN) and dispatch them through the real `compare()`,
  asserting on `RegressionResult.status` and the
  `hard_failures` / `advisory_warnings` lists. No re-implementation of
  the ±2σ math or hard-rule branching.
- `aggregate` workspace reading: tests instantiate a real `Workspace`,
  call real `aggregate(ws, Metrics())`, assert on the returned dict.
  No second JSONL reader, no second `state.md` parser. The
  alphabetical-ordering invariant is asserted as a property of the
  returned list, not recomputed.

Zero duplication of producer code paths. Tests are pure consumers of
the `lib/*` public surface.

## Architect Observations (informational; non-blocking)

- The autouse `_block_claude_subprocess` guard is a good belt-and-braces
  defense against future regressions where someone "helpfully" adds a
  shell-out. Consistent with arch doc §9.
- `pytest --collect-only` returns exactly 3 test functions
  (AC-S3-08 satisfied) — verified by direct collect.
- Test 2 (`test_baseline_comparison_demo`) packs 3 sub-assertions
  inside one test function. This is intentional per the test docstring
  and AC-S3-03; the validator chose function-grouping over
  `@pytest.mark.parametrize` to keep the collect count at 3.
  Architecturally fine.
- The README "What it does NOT do" section explicitly forbids future
  CI workflows — defensive and consistent with the binding directive.

## Decision

S3 is **accepted** by the Architect role. The producer-validator
separation contract from ADR-tk5-001 is intact in the working tree,
the fixture workspace mirrors the production layout, README documents
the local-only constraint with full memory-file path, Makefile targets
match the runner CLI without drift, and no `lib/*` logic is duplicated
in the validator dispatch.

Ring forged. No flaw.

---

*— Celebrimbor, Solution Architect, run-2026-05-13-tk5, Stage 6 DoD.*
