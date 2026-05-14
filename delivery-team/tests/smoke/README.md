# Delivery-team plugin smoke-test runner

## What this is

A local-only smoke-test harness that exercises the `delivery-team` plugin
end-to-end by spawning a real `claude` Code subprocess against a synthetic
hello-world spike prompt, captures the full stream-json output, aggregates
delivery-pipeline telemetry from the isolated workspace, and emits a
structured `report.json` + `summary.md` + `stream.jsonl` per run. A baseline
of 5 sequential captures is stored under `baselines/` and used by the
regression detector to flag hard (cost / outcome / dispatch_count drift)
and advisory (token / skill-load drift) regressions on subsequent runs.

## Local-only notice

**This harness is intentionally NOT wired into CI.** It must NEVER be
invoked from `.github/workflows/`. The binding rationale is captured in
the user-feedback memory file:

    /home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md

The substring `feedback_claude_code_local_only` is the grep handle that
Stage 7 gate #6 and `BC-01` use to confirm both this README and the
architecture document cite the constraint. Claude Code is a developer-local
tool — CI runners do not have the `claude` binary or credentials, so any
workflow that shells out to `claude` would silently fail or never run. Do
not "fix" this by adding a workflow; the omission is the design.

## Prerequisites

- `claude` CLI installed and on `$PATH` (run `claude --version` to confirm).
- Python 3.10 or newer (the harness uses `from __future__ import annotations`
  and `Literal` types; no third-party runtime deps).
- `pytest` installed for the meta-tests (`pip install pytest` — pytest is the
  only test-time dependency).
- Clean git working tree recommended (the runner records `git rev-parse
  --short HEAD` into `report.json`).

## Quick start

Preferred:

    make smoke

Direct invocation (equivalent):

    python3 delivery-team/tests/smoke/run_smoke.py

Both forms write artifacts under
`delivery-team/tests/smoke/artifacts/<utc-timestamp>/`.

## Flags

Inherited from `run_smoke.py --help`:

| Flag | Default | Purpose |
|------|---------|---------|
| `--init-baseline` | off | Run the scenario 5× sequentially, then write baseline JSON from the captured reports. |
| `--cost-cap` | `3.00` | Hard cumulative cost cap in USD; subprocess terminates if cumulative `cost_usd` would exceed this. |
| `--timeout` | `1800` | Wall-clock timeout in seconds; the subprocess is killed with SIGTERM when this is exceeded. |
| `--baseline` | `baselines/hello_world_spike.json` | Path to baseline JSON for regression comparison; missing file = compare step is skipped. |
| `--out-dir` | `artifacts/` | Root artifacts directory; a `<utc-timestamp>/` subdir is created per run. |
| `--prompt` | `prompts/hello_world_spike.txt` | Path to the prompt text file fed to the spawned Claude subprocess. |
| `--config` | `fixtures/delivery_config_minimal.yml` | Minimal `.delivery/config.yml` installed into the mktemp HOME. |
| `--stream-fixture` | unset | Path to a fixture stream-json file (skips spawning Claude; used by meta-tests and cost-cap injection). |
| `--repo-root` | derived | Repo root; defaults to the parent of `delivery-team/`. |

## Baseline workflow

Initial capture (run from repo root; expect 5 sequential `claude` invocations):

    make smoke-baseline
    # or:
    python3 delivery-team/tests/smoke/run_smoke.py --init-baseline

The runner executes the scenario 5× sequentially (concurrency-of-1
enforced), folds each run's `report.json` into per-metric `mean` + `stddev`
+ `n`, and writes `baselines/hello_world_spike.json` per the schema in
`delivery-team/architecture/smoke-test-architecture.md` §6.

Subsequent `make smoke` runs read that baseline file and feed each new
`report.json` through `lib/baseline.py::compare()`. Hard-classified
metrics (`wall_clock_seconds`, `cost_usd`, `pipeline.dispatch_count`,
`pipeline.stories_completed`) drive HARD-FAIL exit; advisory-classified
metrics (`tokens.*`, `skill_loads.*`) drive ADVISORY-WARN entries
appended to the report but do not change exit code.

## Reading the report

Each run writes three artifacts under
`artifacts/<utc-timestamp>/`:

- **`report.json`** — schema-v1 structured report (see architecture §5).
  Top-level keys: `schema_version`, `run_id`, `git_sha`,
  `claude_cli_version`, `plugin_load_strategy`, `outcome.*`,
  `wall_clock_seconds`, `cost_usd`, `tokens.*`, `model_usage[]`,
  `pipeline.*`, `skill_loads[]`, `advisory_warnings[]`,
  `hard_failures[]`. Unmeasurable fields emit `null` (not omitted).
- **`summary.md`** — human-readable rendering of `report.json`, with a
  PASS/FAIL banner, the metric table, and the skill-loads / advisory /
  hard-failure sections inline.
- **`stream.jsonl`** — verbatim stream-json output captured from the
  spawned Claude subprocess; one JSON object per line.

Exit codes:

| Code | Meaning |
|------|---------|
| 0    | Pass (advisory warnings allowed). |
| 1    | Hard-fail (outcome.success=false OR regression hard-rule violated). |
| 2    | Cost-cap exceeded mid-stream. |
| 3    | Wall-clock timeout. |
| 4    | Plumbing failure (missing input, write failure, etc.). |

## Running the meta-tests

The smoke harness ships with three pytest meta-tests that exercise
`lib/metrics.py`, `lib/baseline.py`, and `lib/aggregator.py` without ever
invoking Claude:

    cd delivery-team/tests/smoke && python3 -m pytest tests/ -v

Or via `make`:

    make smoke-tests

Expected output: `3 passed in < 5.00s`. The conftest installs an autouse
guard that monkey-patches `subprocess.Popen` and `subprocess.run` to
raise `AssertionError` if any test attempts to spawn a `claude` process.

## What it does NOT do

- It does NOT add anything under `.github/workflows/` — see the
  Local-only notice above and the binding memory file
  `feedback_claude_code_local_only.md`.
- It does NOT maintain cost-tracking dashboards or per-run history beyond
  the timestamped `artifacts/<utc-timestamp>/` directories.
- It does NOT modify `~/.claude/` on the developer's machine. The runner
  isolates the spawned subprocess inside a `tempfile.mkdtemp(prefix="smoke-")`
  HOME that is scrubbed on exit.
- It does NOT tighten the 2σ advisory band; that decision is deferred to
  a future BACKLOG item once 20+ runs of baseline data exist.

## Cost notice

A single `make smoke` run typically costs **$1 – $2** in Claude API spend
and finishes in 5 – 15 minutes wall-clock. The default `--cost-cap 3.00`
caps any single run at **$3.00**; the subprocess is killed (SIGTERM) the
moment cumulative `cost_usd` would exceed that bound. A baseline capture
(`make smoke-baseline`) runs the scenario 5× sequentially, so budget
**$5 – $10** and 30 – 75 minutes of wall-clock for it. Re-capture the
baseline whenever the plugin's skill graph changes materially — the
purpose is to detect drift, and drift-after-redesign is expected.

## Architecture pointer

Full design rationale, schemas, and the producer-validator separation
contract are in:

    delivery-team/architecture/smoke-test-architecture.md

ADR linkage:

    .delivery/artifacts/04-architect/adrs/ADR-tk5-001-smoke-test-runner-architecture.md
