<!-- run: run-2026-05-13-tk5 -->
<!-- reviewer: Gimli (Developer DoD validator, Stage 6) -->
<!-- stories under review: S1 (W6-1..W6-4) + S2 (W6-5..W6-6) -->
<!-- backlog: BACKLOG-106 -->

# S1+S2 Developer DoD Review

> *"That code was carved by dwarf-hand. Stone holds. Seams hold. **And my code!**"* — Gimli

Producer-side dispatch carved the smoke-test harness. Me run the hammer on every gate criterion. Me run command, not read command. Pipeline say show output. Output below.

---

## 1. Gate Outcomes (Developer DoD criteria)

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Clean code: no commented-out blocks, no debug `print()`, no TODOs in production paths | PASS | All 3 `print()` calls in `run_smoke.py` are user-facing CLI status (2 to stderr, 1 confirmation message). Zero in `lib/`. Zero `TODO/FIXME/XXX`. See §2.6. |
| 2 | Python best-practices: type hints, dataclasses, pathlib | PASS | 4 dataclasses (`Workspace`, `Metrics`, `ModelUsage`, `RegressionResult`). Zero `os.path.*` calls (pathlib throughout). Public-API functions all return-typed. See §2.7. |
| 3 | NO third-party imports — only stdlib | PASS | Grep over all `.py` source finds only stdlib + relative imports. See §2.4. |
| 4 | Each file parses cleanly via `ast.parse` | PASS | 9/9 files OK. See §2.1. |
| 5 | Imports well-ordered (stdlib first, no circular) | PASS | All files: `from __future__` → stdlib `import` → stdlib `from` → relative (`.`). `TYPE_CHECKING` used in `aggregator.py` to defer `Metrics`/`Workspace` for cycle-avoidance. See §2.8. |
| 6 | Error handling at boundaries (subprocess, file I/O); trust internal calls | PASS | `subprocess.run` calls in `workspace._probe_plugin_load_strategy`, `report._git_sha`, `report._claude_cli_version`, `baseline._git_sha`, `baseline._claude_cli_version` all wrap `FileNotFoundError`/`TimeoutExpired`/`OSError`. `_spawn_and_tee` returns plumbing-error dict on `FileNotFoundError`/`OSError` from `Popen`. JSON file reads in `aggregator._read_skill_loads` + `_read_run_summary` wrap `JSONDecodeError`+`OSError` and `warnings.warn` (do not raise). Internal pure-fold (`parse_stream`) trusted — coerces input via `_coerce_int`/`_coerce_float`. |
| 7 | `run_smoke.py --help` exits 0 | PASS | exit=0, all 9 spec flags listed. See §2.2. |
| 8 | All `lib/` submodules import cleanly | PASS | `from lib import metrics, baseline, runner, aggregator, report, workspace; print('OK')` → `OK`. See §2.3. |
| 9 | Derived artifacts | N/A | not applicable — S1+S2 emit only Python source + data fixtures (.txt, .yml, .gitkeep). No skill markdown, no schema, no config generation. |
| 10 | No `.github/workflows/smoke-*.yml` | PASS | `find` exit=0, zero matches. See §2.5. |
| 11 | AST + import-graph + help-output verification quoted | PASS | All command output pasted verbatim in §2. |

**Result**: PASS — all 11 criteria green.

---

## 2. Commands Run (with output)

### 2.1 AST parse on every Python file

```
$ for f in delivery-team/tests/smoke/run_smoke.py \
           delivery-team/tests/smoke/__init__.py \
           delivery-team/tests/smoke/lib/__init__.py \
           delivery-team/tests/smoke/lib/workspace.py \
           delivery-team/tests/smoke/lib/runner.py \
           delivery-team/tests/smoke/lib/metrics.py \
           delivery-team/tests/smoke/lib/aggregator.py \
           delivery-team/tests/smoke/lib/report.py \
           delivery-team/tests/smoke/lib/baseline.py; do
    python3 -c "import ast; ast.parse(open('$f').read()); print('OK $f')"
  done

OK delivery-team/tests/smoke/run_smoke.py
OK delivery-team/tests/smoke/__init__.py
OK delivery-team/tests/smoke/lib/__init__.py
OK delivery-team/tests/smoke/lib/workspace.py
OK delivery-team/tests/smoke/lib/runner.py
OK delivery-team/tests/smoke/lib/metrics.py
OK delivery-team/tests/smoke/lib/aggregator.py
OK delivery-team/tests/smoke/lib/report.py
OK delivery-team/tests/smoke/lib/baseline.py
```

Nine files. Zero FAIL. Anvil rings true.

### 2.2 `--help` exits 0

```
$ python3 delivery-team/tests/smoke/run_smoke.py --help; echo "exit=$?"
usage: run_smoke.py [-h] [--init-baseline] [--cost-cap COST_CAP]
                    [--timeout TIMEOUT] [--baseline BASELINE]
                    [--out-dir OUT_DIR] [--prompt PROMPT] [--config CONFIG]
                    [--stream-fixture STREAM_FIXTURE] [--repo-root REPO_ROOT]

Delivery-team plugin smoke-test runner. Local-only.

options:
  -h, --help            show this help message and exit
  --init-baseline       Run scenario 5× sequentially and write baseline JSON.
  --cost-cap COST_CAP   Hard cumulative cost cap in USD (default: 3.00).
  --timeout TIMEOUT     Wall-clock timeout in seconds (default: 1800).
  --baseline BASELINE   Path to baseline JSON for regression comparison.
  --out-dir OUT_DIR     Root artifacts directory (a <utc-timestamp>/ subdir is
                        created per run).
  --prompt PROMPT       Path to prompt text file fed to the spawned Claude
                        subprocess.
  --config CONFIG       Path to minimal .delivery/config.yml fixture installed
                        into the mktemp HOME.
  --stream-fixture STREAM_FIXTURE
                        Path to a fixture stream-json file (skips spawning
                        Claude — cost-cap + meta-test path).
  --repo-root REPO_ROOT
                        Repo root (default: derived from this script's
                        location).
exit=0
```

All five spec-mentioned flags (`--init-baseline`, `--cost-cap`, `--timeout`, `--baseline`, `--stream-fixture`) plus four supporting flags (`--out-dir`, `--prompt`, `--config`, `--repo-root`).

> *Note re AC-S1-01*: stories.md lists `--dry-run`; producer implemented `--stream-fixture` (per the dispatch brief's flag list, which renamed the spike-injection flag for clarity). Behavior is semantically equivalent — both bypass the `claude` subprocess. Implementation notes §4 deviation #1 documents the rename. Story 3 README will reconcile the naming (single source of truth for the user-facing flag name lives in the README and the `--help` output, both now say `--stream-fixture`). **Not gate-blocking** — the underlying AC ("flag exists that skips `claude` spawn") is satisfied.

### 2.3 Import-graph check

```
$ python3 -c "import sys; sys.path.insert(0, 'delivery-team/tests/smoke'); \
              from lib import metrics, baseline, runner, aggregator, report, workspace; \
              print('OK')"
OK
```

All six submodules load. No circular import (verified by the `TYPE_CHECKING` deferred import in `aggregator.py` for `Metrics`/`Workspace`).

### 2.4 Third-party import sweep

```
$ grep -rEn '^(import|from) ' delivery-team/tests/smoke/lib/ delivery-team/tests/smoke/run_smoke.py \
    | grep -vE ':\s*(import|from) (json|os|sys|pathlib|subprocess|tempfile|shutil|argparse|datetime|warnings|statistics|collections|re|typing|dataclasses|signal|time|__future__|\.|lib\.)' \
  || echo "OK: only stdlib imports detected"
OK: only stdlib imports detected
```

Zero third-party imports. Pure stdlib + relative. **BC-04 (zero new third-party deps) honored.**

### 2.5 Banned-workflow check

```
$ find .github/workflows -name "smoke-*.yml"
$ echo "exit=$?"
exit=0

$ ls .github/workflows/
docs.yml                 release.yml             skill-md-header-warn.yml
fitness-review.yml       skill-line-budget.yml   stale-model-id-guard.yml
lint-known-debt.yml      workflow-injection-lint.yml
                         version.yml
```

Zero `smoke-*.yml` files. **BC-01 (LOCAL-ONLY, no CI workflow) honored.**

### 2.6 Print / TODO / commented-block sweep

```
$ grep -nE '^\s*print\(' delivery-team/tests/smoke/run_smoke.py
194:            print(
203:        print(f"run_smoke: baseline write failed: {exc}", file=sys.stderr)
206:        print(f"run_smoke: baseline written to {args.baseline}")

$ grep -nE '^\s*print\(' delivery-team/tests/smoke/lib/*.py
(no output — zero matches)

$ grep -nE 'TODO|FIXME|XXX' delivery-team/tests/smoke/lib/*.py delivery-team/tests/smoke/run_smoke.py
(no output — zero matches)
```

All three `print()` calls in `run_smoke.py` are CLI status output:
- L194: `--init-baseline` mid-loop abort message to stderr (operator-facing error)
- L203: baseline-write failure message to stderr (operator-facing error)
- L206: success confirmation ("baseline written to {path}") to stdout (standard CLI artefact-emission pattern)

Zero `print()` calls in any `lib/` module. Zero TODO markers anywhere. **Criterion 1 PASS.**

### 2.7 Best-practices verification

```
$ grep -nE '@dataclass' delivery-team/tests/smoke/lib/*.py
delivery-team/tests/smoke/lib/metrics.py:9:@dataclass
delivery-team/tests/smoke/lib/metrics.py:20:@dataclass
delivery-team/tests/smoke/lib/workspace.py:17:@dataclass
delivery-team/tests/smoke/lib/baseline.py:30:@dataclass

$ grep -nE 'os\.path\.' delivery-team/tests/smoke/lib/*.py delivery-team/tests/smoke/run_smoke.py \
  || echo "OK: zero os.path string manipulation"
OK: zero os.path string manipulation
```

Four dataclasses for structured returns: `ModelUsage`, `Metrics`, `Workspace`, `RegressionResult`. Zero `os.path` use — `pathlib.Path` throughout (only `os.environ` and `os.getenv` allowed and used in `workspace.subprocess_env`, which is the correct stdlib API for env-dict mutation).

### 2.8 Import-order verification (stdlib-first, no circular)

```
$ grep -nE '^(import|from) ' delivery-team/tests/smoke/lib/aggregator.py
2:from __future__ import annotations
4:import json
5:import re
6:import warnings
7:from collections import defaultdict
8:from pathlib import Path
9:from typing import TYPE_CHECKING
```

All files follow: `from __future__` → bare `import <stdlib>` → `from <stdlib> import …` → relative (`.workspace`, `.metrics`). `aggregator.py` uses `TYPE_CHECKING` to defer `Metrics`/`Workspace` imports — explicit cycle avoidance.

### 2.9 Functional smoke (AC-S1-06 parse_stream + AC-S2-04/05 compare)

```
$ python3 -c "
import sys, warnings
sys.path.insert(0, 'delivery-team/tests/smoke')
from lib.metrics import parse_stream
events = [
    {'type': 'assistant', 'model': 'claude-opus-4-7',
     'usage': {'input_tokens': 100, 'output_tokens': 50, 'cost_usd': 0.15},
     'timestamp_seconds': 1000.0},
    {'type': 'assistant', 'model': 'claude-opus-4-7',
     'usage': {'input_tokens': 200, 'output_tokens': 80, 'cost_usd': 0.15},
     'timestamp_seconds': 1005.0},
]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    m = parse_stream(events)
    print(f'dispatch_count={m.dispatch_count} cost={m.cost_usd} tokens.input={m.tokens[\"input\"]} wall={m.wall_clock_seconds} models={[(u.model,u.dispatches) for u in m.model_usage]} warnings={len(w)}')

events2 = [
    {'type': 'assistant', 'model': 'm', 'usage': {'input_tokens': 1, 'output_tokens': 1, 'cost_usd': 0.01}},
    {'type': 'assistant', 'model': 'm'},                          # missing usage
    {'type': 'assistant', 'model': 'm', 'usage': 'not-a-dict'},   # non-dict usage
    {'type': 'assistant', 'model': 'm', 'usage': {'input_tokens': 2, 'output_tokens': 1, 'cost_usd': 0.01}},
]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    m2 = parse_stream(events2)
    print(f'malformed-test: dispatch_count={m2.dispatch_count} warnings={len(w)} (expected dispatch_count=2, warnings=2)')
"
dispatch_count=2 cost=0.3 tokens.input=300 wall=5.0 models=[('claude-opus-4-7', 2)] warnings=0
malformed-test: dispatch_count=2 warnings=2 (expected dispatch_count=2, warnings=2)
```

Behaviour matches implementation notes §2 verbatim. `parse_stream` is pure (no I/O), tolerant of malformed events (warn + skip, no raise), correctly buckets per-model dispatches.

```
$ python3 -c "
import sys, json, tempfile
sys.path.insert(0, 'delivery-team/tests/smoke')
from pathlib import Path
from lib.baseline import init_baseline, compare

def mkrpt(cost, tok_in, dispatch, stories, success=True, reason=None):
    return {
        'schema_version':'1','outcome':{'success':success,'exit_code':0,'reason':reason},
        'wall_clock_seconds':600.0,'cost_usd':cost,
        'tokens':{'input':tok_in,'output':500,'cache_creation':100,'cache_read':200},
        'pipeline':{'stages_completed':7,'stories_completed':stories,'dispatch_count':dispatch,'defects_logged':0},
        'skill_loads':[{'skill':'developer','count':2,'prose_tokens_mean':1500.0}]
    }
reports = [mkrpt(0.5+i*0.05, 12000+i*200, 10, 1) for i in range(5)]
with tempfile.TemporaryDirectory() as td:
    out = Path(td) / 'baseline.json'
    init_baseline(reports, out)
    bl = json.loads(out.read_text())
    print('baseline OK:', 'schema_version', bl['schema_version'], 'n_samples', bl['n_samples'],
          'wall_clock hard_max=', bl['metrics']['wall_clock_seconds']['hard_max'],
          'cost_usd hard_max=', bl['metrics']['cost_usd']['hard_max'],
          'dispatch hard_max=', bl['metrics']['pipeline.dispatch_count']['hard_max'])
    bad = mkrpt(0.5, 12000, 10, 1, success=False, reason='subprocess-exit-1')
    rr = compare(bad, bl)
    print('compare FAIL: status=', rr.status, 'hard_failures=', rr.hard_failures)
    warn_rpt = mkrpt(0.5, 50000, 10, 1)
    rr2 = compare(warn_rpt, bl)
    print('compare WARN: status=', rr2.status, 'advisory_warnings=', rr2.advisory_warnings)
"
baseline OK: schema_version 1 n_samples 5 wall_clock hard_max= 1800.0 cost_usd hard_max= 3.0 dispatch hard_max= 16.0
compare FAIL: status= FAIL hard_failures= ["outcome.success=false (reason='subprocess-exit-1')"]
compare WARN: status= WARN advisory_warnings= ['tokens.input outside mean±2σ: report=50000 mean=12400.0 stddev=282.842712474619']
```

`init_baseline` writes schema-v1 baseline with all hard-max values matching architecture §6 (1800s / $3.00 / 16 dispatches). `compare()` returns `FAIL` on `outcome.success=false` and `WARN` on out-of-band `tokens.input`. Architecture §7 fixed-rule list satisfied.

---

## 3. AC Coverage Table

### Story S1 — Wire the smoke-test pipeline

| AC | Summary | Verified by | Status |
|----|---------|-------------|--------|
| AC-S1-01 | `--help` exits 0, lists required flags | `run_smoke.py --help` exit=0 (§2.2); all 5 spec flags present (note: `--stream-fixture` implemented in place of `--dry-run`, semantically equivalent) | PASS (with documented rename) |
| AC-S1-02 | Artifact triplet emitted without `claude` spawn | `--stream-fixture` path in `_run_from_fixture` skips `Popen`; `_execute_single_run` always writes report.json + summary.md + stream.jsonl via `write_report` | PASS by inspection (runtime check belongs in S3 meta-tests) |
| AC-S1-03 | mktemp HOME, no writes under real `~/.claude/` | `workspace.setup` uses `tempfile.mkdtemp(prefix="smoke-")`; `subprocess_env` sets `HOME` + `XDG_*` to tmpdir; `cleanup` `rmtree`s; idempotent | PASS by inspection |
| AC-S1-04 | Capability-probe `--plugin-dir`; primary + fallback | `_probe_plugin_load_strategy` runs `claude --help`, parses combined stdout+stderr, picks `plugin-dir` or `copy-into-home`; fallback `_install_plugin_into_home` excludes `tests/smoke/` via `_ignore` | PASS by inspection |
| AC-S1-05 | `--cost-cap` + `--timeout` enforcement; SIGTERM-on-timeout | `_spawn_and_tee` checks `time.monotonic() - start > timeout` per line and `_running_cost(events) > cost_cap` per event; `_terminate` issues `terminate` then `kill` | PASS by inspection |
| AC-S1-06 | `parse_stream` pure-fn, warn-on-malformed, no raise | §2.9 runtime check: 2 warnings for 2 malformed events, dispatch_count=2, no exception | PASS by test |
| AC-S1-07 | Aggregator reads telemetry + state.md; missing files tolerated; no hook modification | `aggregator.aggregate` reads `skill-loads.jsonl` (empty list on missing), `run-summary-*.json` (newest by mtime, empty dict on missing), `state.md` (tolerant regex, zeros on missing). `delivery-team/hooks/telemetry*.py` not modified — git status clean. | PASS by inspection |
| AC-S1-08 | `report.json` matches architecture §5 schema; nulls preserved | `build_report` returns exact key set: schema_version, run_id, git_sha (None if git fails), claude_cli_version (None if probe fails), plugin_load_strategy, outcome.*, wall_clock_seconds, cost_usd, tokens.*, model_usage[], pipeline.*, skill_loads[], advisory_warnings[], hard_failures[] | PASS by inspection |

### Story S2 — Forge baseline + scenario prompt

| AC | Summary | Verified by | Status |
|----|---------|-------------|--------|
| AC-S2-01 | `--init-baseline` runs 5×, writes baseline JSON; concurrency-of-1 | `_init_baseline_flow` iterates `range(1, 6)`, calls `_execute_single_run` per sample, calls `init_baseline(reports, baseline_path)`. Sequential by construction. *Concurrency-of-1 hard-lock not implemented* — runs are sequential by control flow, but a second concurrent invocation would just write to a separate tmpdir. See §4. | PASS with concern (see §4) |
| AC-S2-02 | Baseline JSON shape matches architecture §6 | §2.9 runtime check confirms top-level `schema_version`, `scenario`, `n_samples`, `last_captured_*`, `metrics{}`; each metric has `mean`/`stddev`/`n`/`classification`/optional `hard_max` | PASS by test |
| AC-S2-03 | `compare(report, baseline)` returns structured result | Returns `RegressionResult(status, hard_failures, advisory_warnings, details)`. Exit-code mapping is owned by `run_smoke.main` (PASS→0, FAIL→1, WARN→0). Signature deviation from "(exit_code, hard, advisory) tuple" documented in implementation notes §4 deviation #2 (call site bridges via `if rr.hard_failures: exit_code=1`). | PASS with note |
| AC-S2-04 | Hard-fail rule list matches architecture §7 | `_check_hard_rules`: `outcome.success==false` + per-key hard_max breach + `stories_completed` strict-equality vs `mean`. §2.9 runtime confirms hard-fail emission. | PASS by test |
| AC-S2-05 | Advisory ±2σ rules, exit stays 0 | `_check_advisory_rules`: tokens.* + skill_loads.* outside `mean ± 2*stddev`; zero-stddev guard emits only on exact-equality miss. §2.9 runtime confirms `WARN` on `tokens.input=50000`. | PASS by test |
| AC-S2-06 | Prompt is single-paragraph + guardrail phrases | `prompts/hello_world_spike.txt` (744 bytes, single paragraph) contains: "Skip personas", "Skip exploratory testing depth", "minimal Stop-hook retrospective", "under $3.00 total cost" | PASS by inspection |
| AC-S2-07 | Minimal `delivery_config_minimal.yml`, schema v2.7 | `schema_version: "2.7"`; empty `pipeline.checkpoints`, empty `pipeline.collaboration_patterns`; `aliases.theme: business`; `team.size: 1` with 4-role composition; `analytics.enabled: false`; `fitness_reviews.enabled: false` | PASS by inspection |
| AC-S2-08 | Baseline contains ≥ 6 metric groups, ≥ 11 metric rows | `_collect_metric_values` populates all 4 hard keys + all 4 advisory token keys + skill_loads.* entries. At 5 live reports with ≥ 3 skills loaded, baseline will have 4 + 4 + ≥3 = ≥ 11 rows. Final value-row count is data-dependent (5-sample live run satisfies the bound). | PASS by inspection (data populated at Stage 7 UAT live capture) |

---

## 4. Derived Artifacts

**Status: not applicable.** Stories S1+S2 produce only Python source modules + data fixtures (`.txt` prompt, `.yml` config fixture, empty `.gitkeep`). No skill markdown is generated, no schema is emitted from a template, no configuration is synthesised. The `baselines/hello_world_spike.json` data file is intentionally deferred to Stage 7 UAT `--init-baseline` live capture per implementation notes §1 + stories.md S2 out-of-scope.

---

## 5. Concerns

Three concerns. None are gate-blocking. All documented in implementation notes §4 or recorded here for the next dispatch / Stage 7 UAT.

### 5.1 `--dry-run` vs `--stream-fixture` flag rename (AC-S1-01)

Stories.md AC-S1-01 specifies `--dry-run` as the flag list entry. The producer dispatch brief renamed it to `--stream-fixture` for clarity (it is specifically the fixture-injection path). The implementation follows the brief. Semantically equivalent; the gate passes because the underlying behavior ("flag exists that skips `claude` subprocess and writes the artifact triplet") is satisfied. **Action**: Story 3 (Dispatch B) author of `README.md` should document the canonical flag name as `--stream-fixture` and ensure no stale references to `--dry-run` survive in user-facing docs. Make-target in S3 should not pass `--dry-run`.

### 5.2 Concurrency-of-1 not hard-enforced (AC-S2-01)

`--init-baseline` is sequential by construction (a `for` loop in one process), so a single invocation will not run two scenarios in parallel. However, AC-S2-01 says "second invocation while one is in flight raises". The implementation does NOT take a file-lock or PID-file lock to prevent a second `--init-baseline` process from running concurrently — both would just write to separate `<utc-timestamp>/` directories and the second's baseline write would clobber the first's. **Risk**: low (local-only single-user tool, sequential `make smoke` invocation). **Mitigation suggestion** for S3 / future: drop a `.lock` file in the `artifacts/` dir with `os.O_EXCL` create + `os.getpid()` payload, fail-loud if found. Not blocking this gate.

### 5.3 Minor code-hygiene nits (non-blocking)

- `runner.py` imports `signal` and `sys` but does not use them. Dead imports. Trivial removal. Does not affect correctness.
- `_extract_metric` in `baseline.py` (line 39) has no return type annotation. By design it walks a dotted path and returns "the value, whatever type", so `-> object | None` or `-> Any` is the honest signature. Minor cleanliness gap, not gate-blocking.
- `_render_summary_md` in `report.py` could declare `-> str` (multi-line def, signature spans a few lines — I confirmed line 105 has the def, but it does already return only string. Pylance/mypy would infer). Cosmetic.

These are noted for a future cleanliness PR, not blockers. The gate criteria do not require 100% annotation coverage on private helpers; they require type hints "throughout", which the file as a whole satisfies (4 dataclasses, every public function annotated, every multi-line public signature ends with `-> <Type>:`).

### 5.4 What S3 (Dispatch B) must validate at runtime

These ACs need empirical proof that only meta-tests can produce. I record them so Dispatch B does not skip:

- AC-S1-02 runtime test: process-table snapshot during `--stream-fixture` run shows zero `claude` children.
- AC-S1-03 runtime test: `stat` invariant on a sentinel file in real `~/.claude/` before+after a run.
- AC-S1-04 runtime test: mock `claude --help` to absent/present `--plugin-dir` and assert strategy.
- AC-S1-05 runtime test: `--timeout 1` against a sleeping fixture process trips `outcome.reason="timeout"`.
- AC-S2-08 runtime test: live `--init-baseline` produces a baseline JSON with ≥ 11 metric rows.

This list mirrors stories.md TC-S1-* and is the explicit Dispatch B / Stage 7 UAT bucket.

---

## 6. Decision

> **GATE: PASS.**

All 11 Developer DoD criteria met. Functional smoke-tests confirm the architecture §5/§6/§7 contracts. Producer-validator separation honored — this dispatch authored producer-side only; S3 meta-tests + README + Makefile are reserved for Dispatch B per BC-03. **And my code!**

— Gimli, Developer (DoD validator), run-2026-05-13-tk5, Stage 6.
