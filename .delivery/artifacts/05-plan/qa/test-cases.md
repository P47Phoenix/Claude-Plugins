<!-- run: run-2026-05-13-tk5 | stage: 05-plan | depth: light | step: 3 | author: Legolas (QA Engineer) | sources: stories.md, prd.md, user-seed.md, smoke-test-architecture.md -->

# Test Cases — BACKLOG-106 Delivery-team plugin smoke test

> *"That bug still only counts as one."* — Legolas, sharp-eyed.

Me carve 18 test cases across three stories. Every AC traced. Every Stage-7 UAT gate mapped. Negative paths sharpened. No coverage holes.

**Tally**: 24 story ACs (S1=8, S2=8, S3=8) + 8 PRD initiative ACs (AC-01..AC-08, identical to user-seed Stage-7 UAT gates 1-8) = 32 source lines mapped to 18 TCs. Zero unmapped lines.

---

## Coverage Map — Story ACs ↔ TC traceability

| Story | AC ID | TC IDs |
|-------|-------|--------|
| S1 | AC-S1-01 | TC-S1-01 |
| S1 | AC-S1-02 | TC-S1-02, TC-S1-03 |
| S1 | AC-S1-03 | TC-S1-03 |
| S1 | AC-S1-04 | TC-S1-04 |
| S1 | AC-S1-05 | TC-S1-05 |
| S1 | AC-S1-06 | TC-S1-06 |
| S1 | AC-S1-07 | TC-S1-07 |
| S1 | AC-S1-08 | TC-S1-08 |
| S2 | AC-S2-01 | TC-S2-01, TC-S2-02 |
| S2 | AC-S2-02 | TC-S2-03 |
| S2 | AC-S2-03 | TC-S2-04, TC-S2-07 |
| S2 | AC-S2-04 | TC-S2-04, TC-S2-NN-COSTCAP |
| S2 | AC-S2-05 | TC-S2-05 |
| S2 | AC-S2-06 | TC-S2-08 |
| S2 | AC-S2-07 | TC-S2-09 |
| S2 | AC-S2-08 | TC-S2-03 |
| S3 | AC-S3-01 | TC-S3-01, TC-S3-02 |
| S3 | AC-S3-02 | TC-S3-03 |
| S3 | AC-S3-03 | TC-S3-04 |
| S3 | AC-S3-04 | TC-S3-05 |
| S3 | AC-S3-05 | TC-S3-06 |
| S3 | AC-S3-06 | TC-S3-07 |
| S3 | AC-S3-07 | TC-S3-NN-PRODUCERBLIND |
| S3 | AC-S3-08 | TC-S3-08 |

Zero unmapped ACs. PO Plan-memory-lesson-1 satisfied (round-1 enumerated all 24 by ID).

---

## Stage 7 UAT gate mapping (user-seed lines 45-52)

The user-seed initiative-level acceptance gates are the BLOCKING coverage matrix. Any gate without a TC is a coverage hole.

| Gate # | User-seed text (verbatim) | PRD AC | Verifying TC(s) | Status |
|--------|---------------------------|--------|-----------------|--------|
| **1** | `python3 ... run_smoke.py` completes on the developer's machine in < 30 min wall-clock. | AC-01 | TC-UAT-01 (live run, Stage 7) | MAPPED |
| **2** | Output: `delivery-team/tests/smoke/artifacts/<utc-timestamp>/{report.json, summary.md, stream.jsonl}` | AC-02 | TC-S1-02 | MAPPED |
| **3** | `report.json` contains `outcome.success`, `wall_clock_seconds`, `cost_usd`, `tokens.*`, `model_usage`, `pipeline.*`, `skill_loads`, `git_sha`, `claude_cli_version` | AC-03 | TC-S1-08 + TC-UAT-03 (live) | MAPPED |
| **4** | `--init-baseline` flag runs scenario 5× sequentially → writes baselines/hello_world_spike.json with mean+stddev per metric | AC-04 | TC-S2-01, TC-S2-02, TC-S2-03 | MAPPED |
| **5** | Default regression detector HARD-FAILS on outcome/cost/wall_clock/stories_completed/dispatch_count; ADVISORY-WARNS on tokens/skill_loads outside ±2σ | AC-05 | TC-S2-04, TC-S2-05, TC-S2-NN-COSTCAP | MAPPED |
| **6** | Meta-tests in `tests/test_meta.py` pass: malformed-stream + baseline-comparison + aggregator-fixture; no Claude calls; < 5 sec | AC-06 | TC-S3-01, TC-S3-02, TC-S3-03, TC-S3-04, TC-S3-05, TC-S3-08, TC-S3-NN-NONETWORK | MAPPED |
| **7** | NO `.github/workflows/smoke-*.yml` exists | AC-07 | TC-UAT-07 (BC-01 grep gate) | MAPPED |
| **8** | `delivery-team/architecture/smoke-test-architecture.md` records local-only constraint with pointer to memory file | AC-08 | TC-UAT-08 (grep for binding memory path in architecture doc) | MAPPED |

**Coverage holes**: NONE. All 8 gates mapped to ≥1 TC. Gates 1, 3, 7, 8 add TC-UAT-* cases (live-run / structural-grep gates that execute at Stage 7 against the merged artifact, not at Stage-6 unit level).

---

## Test Cases (18 + 3 UAT structural gates = 21 total)

### Test Case Table

| ID | Title | Type | Priority | Preconditions | Steps | Expected Result |
|----|-------|------|----------|---------------|-------|-----------------|
| **TC-S1-01** | `--help` exit and flag enumeration | Positive / Smoke | P0 | S1 lib + runner.py merged | `python3 delivery-team/tests/smoke/run_smoke.py --help`; capture stdout + exit code | Exit code 0; stdout contains all 5 flags: `--init-baseline`, `--cost-cap`, `--timeout`, `--baseline`, `--dry-run`. **AC**: AC-S1-01. |
| **TC-S1-02** | `--dry-run` writes 3 artifacts under timestamped dir | Positive / Functional | P0 | Fixture stream-json at `tests/smoke/fixtures/dry-run-stream.jsonl` | `python3 delivery-team/tests/smoke/run_smoke.py --dry-run`; `find delivery-team/tests/smoke/artifacts/ -newer <pre-run-timestamp>` | A single `<utc-timestamp>/` dir exists containing exactly `report.json`, `summary.md`, `stream.jsonl`; no `claude` subprocess spawned (verified via `psutil.process_iter` snapshot during run OR by inspecting that `lib/runner.py` short-circuits to fixture path when `--dry-run` is set). **AC**: AC-S1-02, **UAT Gate 2**. |
| **TC-S1-03** | HOME isolation post-run | Positive / NFR-Isolation | P0 | `~/.claude/` pre-run mtime + size snapshot on a sentinel file (e.g. `~/.claude/settings.json`) | Run `python3 delivery-team/tests/smoke/run_smoke.py --dry-run`; re-stat sentinel | Sentinel `(mtime, size)` tuple is byte-identical pre and post; `lib/workspace.py` log line confirms HOME pointed at a `tempfile.mkdtemp(prefix="smoke-")` path that is now deleted. **AC**: AC-S1-02, AC-S1-03, **NFR-Isolation**. |
| **TC-S1-04** | Capability-probe selects `--plugin-dir` vs `copy-into-home` | Positive + Negative / Branch | P1 | Mock `claude --help` output via shim on `$PATH` | (a) Shim emits help text containing `--plugin-dir` → run runner, read `report.json.plugin_load_strategy`; (b) Shim emits help text WITHOUT `--plugin-dir` → run runner, read `report.json.plugin_load_strategy` | (a) `plugin_load_strategy == "plugin-dir"`; (b) `plugin_load_strategy == "copy-into-home"` AND the temp `<tmpdir>/.claude/plugins/delivery-team/` exists during the run AND does NOT contain a nested `tests/smoke/` directory (recursion guard). **AC**: AC-S1-04. |
| **TC-S1-05** | `--timeout` kills runaway subprocess **(NEGATIVE / boundary)** | Negative / Boundary | P0 | Fixture subprocess script `tests/fixtures/sleep_long.py` that sleeps 60 s | `python3 delivery-team/tests/smoke/run_smoke.py --timeout 1 --dry-run --subprocess-fixture tests/fixtures/sleep_long.py`; wait ≤ 3 s wall-clock | `report.json` contains `outcome.success == false`, `outcome.reason == "timeout"`, `outcome.exit_code != 0`; runner returns within 2 s of timeout deadline; SIGTERM was sent (verifiable via fixture exit-trap logging). **AC**: AC-S1-05, **UAT Gate 5** (timeout half). |
| **TC-S1-06** | Malformed stream-json emits warnings, no raise **(NEGATIVE)** | Negative / Fault-injection | P0 | Fixture `tests/fixtures/malformed-stream.jsonl` with: 3 valid events, 1 event missing `usage` key, 1 line of non-JSON garbage | Import `lib.metrics.parse_stream`; pass fixture iterator; capture warnings via `warnings.catch_warnings(record=True)` | Function returns a `Metrics` dataclass; `warnings.warn` was called ≥ 2 times (one per malformed event); `Metrics.dispatch_count` reflects only the 3 valid events; **NO exception raised**. **AC**: AC-S1-06. |
| **TC-S1-07** | Aggregator with missing telemetry files **(NEGATIVE)** | Negative / Edge | P1 | Fixture workspace at `tests/fixtures/workspace_no_telemetry/` with `.delivery/state.md` only (no `skill-loads.jsonl`, no `run-summary-*.json`) | Call `lib.aggregator.aggregate(workspace_path)` | Returns merged dict with `skill_loads == []`; fallback invocation of `delivery-team/hooks/telemetry_run_summary.py` runs and produces the missing summary; no `FileNotFoundError` raised; aggregator does NOT modify either telemetry hook source file (verified via `git status` against pre-call snapshot). **AC**: AC-S1-07, **BC-02 reuse-mandate**. |
| **TC-S1-08** | `report.json` schema completeness (incl. null-emission) | Positive / Contract | P0 | Fixture stream + fixture workspace such that `claude --version` shim returns exit 1 | Run runner in `--dry-run` mode against that fixture; load resulting `report.json` and validate keys | All keys present: `schema_version`, `run_id`, `git_sha`, `claude_cli_version`, `plugin_load_strategy`, `outcome.{success,exit_code,reason}`, `wall_clock_seconds`, `cost_usd`, `tokens.{input,output,cache_creation,cache_read}`, `model_usage[]`, `pipeline.{stages_completed,stories_completed,dispatch_count,defects_logged}`, `skill_loads[]`, `advisory_warnings[]`, `hard_failures[]`. `claude_cli_version` is `null` (NOT missing, NOT empty string). **AC**: AC-S1-08, **UAT Gate 3**. |
| **TC-S2-01** | `--init-baseline` 5× sequential mean+stddev compute | Positive / Functional | P0 | Pre-computed 5 fixture reports under `tests/fixtures/baseline-inputs/report-{1..5}.json` with known token + cost values | `python3 delivery-team/tests/smoke/run_smoke.py --init-baseline --dry-run --fixture-reports tests/fixtures/baseline-inputs/`; load resulting `baselines/hello_world_spike.json` | `metrics{}` map contains entries for the 5 input metric groups; each `mean` and `stddev` matches a hand-computed reference (within 1e-6); `n_samples == 5`; `last_captured_utc` is ISO-8601 UTC; `last_captured_git_sha` matches `git rev-parse HEAD`. **AC**: AC-S2-01, **UAT Gate 4**. |
| **TC-S2-02** | `--init-baseline` concurrency-of-1 enforcement **(NEGATIVE)** | Negative / Concurrency | P0 | One `--init-baseline` invocation in flight (stub with `time.sleep(5)` lock-hold) | Launch second `--init-baseline` from a parallel shell within the sleep window | Second invocation exits non-zero within 1 s; stderr contains a clear "concurrency-of-1" message naming the lockfile path; primary invocation completes unaffected. **AC**: AC-S2-01, **BC-05**. |
| **TC-S2-03** | Baseline JSON shape matches §6 contract (≥ 11 metric rows) | Positive / Contract | P0 | Output of TC-S2-01 | `python3 -c "import json; b=json.load(open('baselines/hello_world_spike.json')); ..."` | Top-level keys present: `schema_version`, `scenario`, `n_samples`, `last_captured_utc`, `last_captured_git_sha`, `last_captured_cli_version`, `metrics`. Each `metrics[k]` has `mean`, `stddev`, `n`, `classification ∈ {"hard","advisory"}`; entries cover `wall_clock_seconds`, `cost_usd`, 4× `tokens.*`, ≥ 2× `pipeline.*`, ≥ 3× `skill_loads.*` → **≥ 11 rows total**. Hard-classified rows carry `hard_max`; advisory rows do not require it. **AC**: AC-S2-02, AC-S2-08. |
| **TC-S2-04** | Hard-fail on `outcome.success=false` | Negative / Detector | P0 | Synthetic report `tests/fixtures/report-outcome-false.json` with `outcome.success=false`; baseline fixture | `lib.baseline.compare(report, baseline)` | Returns `(exit_code=1, hard_failures=[<non-empty list naming the outcome rule>], advisory_warnings=[])`. **AC**: AC-S2-03, AC-S2-04, **UAT Gate 5**. |
| **TC-S2-05** | Advisory-warn on token drift outside ±2σ | Negative / Detector | P0 | Synthetic report with `tokens.input` = `mean + 3·stddev`; baseline fixture with non-zero stddev on `tokens.input` | `lib.baseline.compare(report, baseline)` | Returns `(exit_code=0, hard_failures=[], advisory_warnings=[<non-empty list naming tokens.input>])`; warning appended to `report.json.advisory_warnings[]`. **AC**: AC-S2-05, **UAT Gate 5**. |
| **TC-S2-06** | Regression detector with zero-stddev baseline metric **(NEGATIVE / divide-by-zero guard)** | Negative / Boundary | P0 | Baseline fixture where `tokens.cache_creation.stddev == 0.0` (e.g. all 5 baseline samples were identical); synthetic report with `tokens.cache_creation` matching baseline mean exactly | `lib.baseline.compare(report, baseline)` | Returns without raising `ZeroDivisionError`. If report value == mean → no warning. If report value != mean → advisory warning emitted using a fallback rule (e.g. exact-equality check OR `abs(delta) > 0` treated as out-of-band when stddev==0). Behavior documented in `lib/baseline.py` docstring. **AC**: AC-S2-03 (config/usage error path), defensive contract. |
| **TC-S2-07** | Missing baseline file → exit_code=2 **(NEGATIVE / `--init-baseline` UX)** | Negative / Usage | P0 | Repo state with `baselines/hello_world_spike.json` deleted | `python3 delivery-team/tests/smoke/run_smoke.py --baseline baselines/hello_world_spike.json` (NO `--init-baseline`) | Process exits with code 2; stderr message instructs the user to run `--init-baseline` first; cites the expected baseline path verbatim. Mirrors `scripts/check_skill_budgets.py` exit-2 = config/usage error convention (BC-02). **AC**: AC-S2-03. |
| **TC-S2-08** | Prompt file guardrail grep | Positive / Content | P1 | `prompts/hello_world_spike.txt` exists | `grep -E "skip personas\|skip UAT\|minimal retrospective" prompts/hello_world_spike.txt \| wc -l` | Returns ≥ 3 matches; file is plain text (no markdown markers `#`, `**`, `-` at line starts); single paragraph (one blank-line block max). **AC**: AC-S2-06. |
| **TC-S2-09** | Minimal config loads under setup-wizard schema | Positive / Contract | P0 | `fixtures/delivery_config_minimal.yml` exists | Invoke the delivery-flow setup-wizard schema-check entrypoint against the fixture (load it into the existing config-loader; check schema version) | Loads without raising; schema version == `2.7`; no optional sub-skill keys present; no analytics-dashboard keys; no fitness-review keys. **AC**: AC-S2-07. |
| **TC-S2-NN-COSTCAP** | **Cost-cap exceeded → graceful termination (SYNTHETIC INJECTION)** | Negative / Boundary / Critical | P0 | Synthetic stream-json injector fixture `tests/fixtures/inject-cost-overrun.jsonl` containing 6 events each with `usage.cost_usd: 0.55` → cumulative `$3.30` (over the $3.00 cap on event 6) | (1) Configure `lib/runner.py` to read events from the synthetic injector instead of `claude` subprocess stdout (via `--dry-run --stream-fixture`); (2) Run with `--cost-cap 3.00`; (3) Inspect `report.json` | Subprocess (or its dry-run simulation) terminates within 100 ms of the event that crosses `$3.00`; `report.json.outcome.success == false`; `report.json.outcome.reason == "cost-cap-exceeded"` (or a verbatim equivalent documented in `lib/runner.py`); `cost_usd` recorded in report is **the cumulative at termination** (≥ 3.00, ≤ 3.30); SIGTERM was issued (not SIGKILL first); `hard_failures[]` contains the cost-cap rule string. **AC**: AC-S1-05, AC-S2-04, **UAT Gate 5**, **NFR-Cost**, **BC-05**. |
| **TC-S3-01** | Meta-tests pass in < 5 s | Positive / Smoke | P0 | S3 merged; pytest installed | `python3 -m pytest delivery-team/tests/smoke/tests/ -v` | Exit code 0; output reports `3 passed`; wall-clock < 5.00 s (measured by pytest's own duration line). **AC**: AC-S3-01, **UAT Gate 6**. |
| **TC-S3-02** | Meta-tests issue **zero Claude calls** **(NEGATIVE / structural)** | Negative / Static | P0 | S3 meta-test source present | (1) `grep -rE "subprocess\.(Popen\|run\|call).*[\"']claude[\"']" delivery-team/tests/smoke/tests/`; (2) `grep -rE "^import claude\\b\|^from claude " delivery-team/tests/smoke/tests/`; (3) AT RUNTIME during `pytest`: snapshot `psutil.process_iter()` via a session-scoped fixture, assert no PID has `name() == "claude"` during the run | All three grep paths return zero matches; runtime psutil assertion passes. **AC**: AC-S3-01, **UAT Gate 6**. |
| **TC-S3-03** | Test 1 — malformed-stream fault injection **(NEGATIVE / fixture)** | Negative / Fault-injection | P0 | Fixture `tests/fixtures/malformed-stream.jsonl` shipped by S3 with: 3 valid events + 2 malformed lines (one missing `usage`, one non-JSON garbage line `not-json-at-all-{{}`) | Run `pytest delivery-team/tests/smoke/tests/test_meta.py::test_malformed_stream -v` | Test passes; assertion confirms `warnings.warn(...)` was called exactly 2 times (one per malformed line); `Metrics.dispatch_count` equals 3 (the valid count). **AC**: AC-S3-02, **UAT Gate 6**. |
| **TC-S3-04** | Test 2 — baseline-comparison demo | Positive + Negative / Detector | P0 | Two synthetic reports + one synthetic baseline shipped by S3 under `tests/fixtures/` | `pytest delivery-team/tests/smoke/tests/test_meta.py::test_baseline_comparison -v` | Report A (`cost_usd > hard_max`) → `compare()` returns `exit_code=1`, `hard_failures` non-empty. Report B (`tokens.input` outside ±2σ) → `compare()` returns `exit_code=0`, `advisory_warnings` non-empty. **AC**: AC-S3-03, **UAT Gate 6**. |
| **TC-S3-05** | Test 3 — aggregator-fixture parsing | Positive / Contract | P0 | Fixture workspace `tests/fixtures/workspace_sample/.delivery/{telemetry/skill-loads.jsonl, telemetry/run-summary-*.json, state.md}` shipped by S3 | `pytest delivery-team/tests/smoke/tests/test_meta.py::test_aggregator_parsing -v` | Aggregator output dict is byte-equal to the hand-computed expected JSON (compared via `json.dumps(d, sort_keys=True)`); `pipeline.{stages_completed,stories_completed,dispatch_count,defects_logged}` all match expected values. **AC**: AC-S3-03, **UAT Gate 6**. |
| **TC-S3-06** | README documents binding memory path + 6 required sections | Positive / Content | P1 | `delivery-team/tests/smoke/README.md` exists | (1) `grep -F "/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md" delivery-team/tests/smoke/README.md`; (2) `grep -E "(make smoke\|--init-baseline\|--cost-cap\|--timeout\|--baseline\|--dry-run)"`; (3) `grep -E "smoke-test-architecture\.md"` | (1) exactly 1 match (binding memory path appears verbatim); (2) ≥ 6 matches covering invocation + all 5 flags; (3) ≥ 1 match (architecture-doc pointer present). **AC**: AC-S3-05. |
| **TC-S3-07** | root `Makefile` `smoke` target wired with cost+time caps | Positive / Build-tool | P0 | Root `Makefile` exists (new or modified by S3) | (1) `make -n smoke` (dry-run); (2) `grep -E "^\.PHONY:.*\bsmoke\b" Makefile`; (3) `make help` | (1) Dry-run prints `python3 delivery-team/tests/smoke/run_smoke.py --cost-cap 3.00 --timeout 1800` exactly; (2) `.PHONY: smoke` declared; (3) `make help` lists `smoke` as a target with a one-line description. **AC**: AC-S3-06. |
| **TC-S3-08** | `pytest --collect-only` shows exactly 3 functions | Positive / Bound | P1 | S3 merged | `python3 -m pytest delivery-team/tests/smoke/tests/ --collect-only -q` | Output enumerates exactly 3 test functions; no `parametrize` expansion bumps the count; collection exit code 0. **AC**: AC-S3-08, **UAT Gate 6**. |
| **TC-S3-NN-PRODUCERBLIND** | Producer-validator separation (git history check) **(NEGATIVE / process)** | Negative / Process / Post-hoc | P0 | S1 + S2 + S3 commits on `main` | `git log --format='%H %an %s' delivery-team/tests/smoke/tests/ delivery-team/tests/smoke/lib/metrics.py delivery-team/tests/smoke/lib/baseline.py` | The commit(s) touching `tests/test_meta.py` + `tests/fixtures/` are authored by a DIFFERENT Stage-6 Dev dispatch (different author OR clearly-labeled `[dispatch-B]` commit-message tag) than commits touching `lib/metrics.py` and `lib/baseline.py`. Verified via the Scrum-Bag dispatch log at `.delivery/artifacts/05-plan/sm/dispatch-plan.md`. **AC**: AC-S3-07, **BC-03**. |
| **TC-S3-NN-NONETWORK** | Meta-tests run with no network **(NEGATIVE / isolation)** | Negative / Isolation | P1 | S3 merged; ability to disable loopback OR run inside `unshare --net` | (1) `unshare --net python3 -m pytest delivery-team/tests/smoke/tests/` (Linux); OR (2) wrap the test invocation in a session-scoped fixture that monkey-patches `socket.socket` to raise on any call | All 3 tests still pass; no network access attempted; combined with TC-S3-02 (import/process grep) this is the empirical "no Claude calls" assertion. **AC**: AC-S3-01, **UAT Gate 6**. |
| **TC-UAT-01** | Live `run_smoke.py` completes in < 30 min (Stage 7) | Positive / NFR-Performance | P0 | All 3 stories merged on `main`; developer machine; valid `claude` CLI on `$PATH`; baseline file present | `time python3 delivery-team/tests/smoke/run_smoke.py --cost-cap 3.00 --timeout 1800` | Exit code 0; total wall-clock < 1800 s; `report.json.outcome.success == true`; advisory-warning list may be non-empty but `hard_failures == []`. **AC**: AC-01, **UAT Gate 1**. |
| **TC-UAT-07** | NO `.github/workflows/smoke-*.yml` (BC-01) | Negative / Governance | P0 | All 3 stories merged on `main` | `find .github/workflows/ -name "smoke-*.yml" -o -name "*smoke*.yml" \| wc -l` | Returns `0`. Any non-zero result is a binding BC-01 violation and blocks UAT acceptance. **AC**: AC-07, **UAT Gate 7**, **BC-01**. |
| **TC-UAT-08** | Architecture doc cites binding memory file | Positive / Governance | P0 | `delivery-team/architecture/smoke-test-architecture.md` exists (authored Stage 4) | `grep -F "/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md" delivery-team/architecture/smoke-test-architecture.md` | Exactly 1 match; surrounding paragraph explains the LOCAL-ONLY constraint in prose. **AC**: AC-08, **UAT Gate 8**, **BC-01**. |

---

## Boundary Values

| Input | Lower Bound | Upper Bound | On-Boundary | Off-Boundary |
|-------|-------------|-------------|-------------|--------------|
| `--cost-cap` | $0.00 (impractical) | $3.00 (NFR-Cost hard) | $3.00 (cumulative at termination event) — pass | $3.01 cumulative → hard-fail (TC-S2-NN-COSTCAP) |
| `--timeout` | 1 s (test fixture) | 1800 s (30 min NFR) | 1 s → kill at 1 s (TC-S1-05) | 0 s / negative → usage error |
| `--init-baseline n_samples` | 5 (binding, BC-05 + FR-06) | 5 | exactly 5 → baseline written | < 5 → guard fires (TC-S2-09 adjacent); 6+ samples → not produced by `--init-baseline` (manual only) |
| Baseline `stddev` | 0.0 (zero variance) | unbounded | 0.0 → divide-by-zero guard fires (TC-S2-06) | negative → invalid (data error, exit 2) |
| Meta-test wall-clock | 0 s | 5.00 s (AC-S3-01) | exactly 5.00 s → boundary fail (target is strictly <) | 5.01 s → AC-S3-01 fail |
| Token deviation σ-band | mean − 2σ | mean + 2σ | exactly mean + 2σ → on-boundary, advisory-warn (canonical: warn IF strictly outside; verify chosen inequality in `lib/baseline.py`) | mean + 2.01σ → advisory-warn (TC-S2-05) |
| `report.json` field count | per §5 schema (≥ 14 top-level keys) | same | all keys present incl. `null` placeholders (TC-S1-08) | missing key → schema-validation fail |

---

## Negative Test Cases (consolidated)

| ID | Title | Invalid Input | Expected Error |
|----|-------|---------------|----------------|
| TC-S1-05 | Subprocess timeout | `--timeout 1` against a sleeping fixture | `outcome.success=false`, `outcome.reason="timeout"`, SIGTERM sent |
| TC-S1-06 | Malformed stream-json event | jsonl with missing `usage` key + non-JSON line | `warnings.warn` ≥ 2; **no raise**; dispatch_count counts only valid events |
| TC-S1-07 | Missing telemetry files | Workspace with no `skill-loads.jsonl` | `skill_loads == []`; fallback hook invoked; no `FileNotFoundError` |
| TC-S2-02 | Concurrent `--init-baseline` | 2nd invocation while 1st in flight | exit non-zero; stderr `concurrency-of-1` message |
| TC-S2-04 | `outcome.success=false` | Synthetic report A | `compare()` → exit_code=1, `hard_failures` non-empty |
| TC-S2-06 | Zero-stddev baseline metric | Baseline with `stddev=0.0` | No `ZeroDivisionError`; documented fallback behavior |
| TC-S2-07 | Missing baseline file (first run) | `baselines/hello_world_spike.json` deleted | Exit code 2; stderr instructs `--init-baseline` |
| TC-S2-NN-COSTCAP | Cost-cap exceeded via injected events | Stream of 6 events × $0.55 each = $3.30 vs `--cost-cap 3.00` | Termination at event 6; `outcome.success=false`, `outcome.reason="cost-cap-exceeded"`; `hard_failures[]` non-empty |
| TC-S3-02 | Hidden Claude call in meta-tests | grep + runtime psutil snapshot | Zero `subprocess.Popen("claude", …)`; zero `import claude`; no PID named `claude` during run |
| TC-S3-03 | Malformed-stream fixture | 2 malformed lines among 5 events | Exactly 2 warnings; dispatch_count = 3 |
| TC-S3-NN-PRODUCERBLIND | Same author for producer + validator | `git log` shows shared author across `lib/{metrics,baseline}.py` and `tests/test_meta.py` | BC-03 violation; UAT blocks |
| TC-S3-NN-NONETWORK | Meta-test attempts network | Run inside `unshare --net` | All 3 tests still pass |
| TC-UAT-07 | `smoke-*.yml` exists in `.github/workflows/` | `find` returns ≥ 1 | BC-01 violation; UAT blocks |

---

## Cost-Cap Synthetic Injection Mechanism (TC-S2-NN-COSTCAP detail)

The cost-cap test path is the single most-binding negative case in the wave. Mechanism documented here so the Stage-6 Dev dispatch authoring TC-S2-NN-COSTCAP has unambiguous contract.

1. **Fixture file**: `delivery-team/tests/smoke/tests/fixtures/inject-cost-overrun.jsonl`. 6 events, each one a single JSON line of the shape Claude Code emits with stream-json output:
   ```
   {"type":"assistant","usage":{"input_tokens":1000,"output_tokens":2000,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"cost_usd":0.55},"model":"claude-opus-4-7"}
   ```
   Cumulative `cost_usd` after each event: $0.55, $1.10, $1.65, $2.20, $2.75, **$3.30** (crosses cap on event 6).
2. **Injection point**: `lib/runner.py` accepts a hidden `--stream-fixture <path>` flag (active only under `--dry-run`). When set, `runner.read_stream()` yields lines from the fixture file instead of invoking `subprocess.Popen("claude", ...)`. The cost-cap check loop in `runner.py` reads `metrics.cost_usd` after every event and compares to the configured `--cost-cap` value.
3. **Termination behavior**: on event 6, `runner.py` MUST: (a) issue SIGTERM to the (mocked) subprocess handle, (b) write `outcome.reason = "cost-cap-exceeded"` to the in-memory report state, (c) set `outcome.success = false`, (d) append the cost-cap rule string to `hard_failures[]`, (e) emit `report.json` + `summary.md` + `stream.jsonl` (truncated at event 6) before exiting non-zero.
4. **Assertion contract** (in the meta-test or live TC):
   - `report.json.outcome.success == False`
   - `report.json.outcome.reason == "cost-cap-exceeded"`
   - `3.00 <= report.json.cost_usd <= 3.30`
   - `report.json.hard_failures` is a non-empty list containing the substring `cost`
   - Stream length ≤ 6 events (no events past the cap recorded)
   - Process exit code is non-zero (1 or higher, exact value documented in `lib/runner.py`)

---

## Coverage Notes

**Equivalence classes covered**:
- **Stream-parsing**: valid events (TC-S1-06 happy path inside the fixture), malformed missing-key, non-JSON garbage line, zero events (implicit via `--dry-run` empty fixture).
- **Subprocess lifecycle**: clean exit (TC-S1-02), timeout-killed (TC-S1-05), cost-cap-killed (TC-S2-NN-COSTCAP), capability-probe primary path + fallback (TC-S1-04).
- **Baseline detector**: happy path (TC-S2-01), hard-fail outcome (TC-S2-04), hard-fail cost (TC-S2-NN-COSTCAP), advisory token drift (TC-S2-05), zero-stddev edge (TC-S2-06), missing-baseline UX (TC-S2-07).
- **Aggregator**: present telemetry (TC-S3-05), missing telemetry with fallback (TC-S1-07).
- **Meta-tests**: pass-in-budget (TC-S3-01), no-Claude-call assertion via 3 independent paths — grep imports, grep subprocess, runtime psutil + no-network (TC-S3-02 + TC-S3-NN-NONETWORK).
- **Governance**: BC-01 grep gate (TC-UAT-07), BC-02 reuse-mandate (TC-S1-07 + TC-S3-05 implicit via reading existing hook output), BC-03 producer-validator separation (TC-S3-NN-PRODUCERBLIND), BC-05 cost+time caps (TC-S1-05 + TC-S2-NN-COSTCAP + TC-S2-02).

**What remains untested (intentionally out-of-scope)**:
- 20+ accumulated production runs to tighten 2σ → tighter band (NFR-Reproducibility, deferred to future BACKLOG per PRD §Out of Scope).
- Hardware-team / mtg-commander reuse paths (NFR-Reuse boundary preserved by `lib/` factoring; not exercised this wave).
- Cost-tracking dashboards (PRD §Out of Scope).
- Stop-hook stderr capture pathological cases (covered structurally by capability-probe + report contract; pathological exhaustion deferred).

**Known gaps & decisions**:
- TC-UAT-01 (live <30 min run) is a Stage-7 UAT gate, not a Stage-6 unit verification — by design, it requires a real `claude` CLI invocation. Stage-6 Dev DoD validates the harness mechanics; Stage-7 UAT validates the empirical claim.
- TC-S2-06 (zero-stddev guard) documents the chosen fallback behavior in `lib/baseline.py` docstring; the chosen rule (exact-equality vs `abs(delta)>0`) is a Stage-6 Dev decision but MUST be documented and tested.
- The "on-boundary mean ± 2σ" inequality convention (strict-outside vs inclusive) MUST be documented in `lib/baseline.py` and exercised in TC-S2-05; current contract is **strict-outside** triggers warn.

**Rationale for key decisions** (≤ 5 sentences):
1. **18 TCs not 13**: round-1 lesson from PO Plan-memory-lesson-1 (tk4 caught 3 unmapped ACs) — me enumerated every story AC by ID and added negative-path TCs (TC-S2-06 zero-stddev, TC-S3-NN-NONETWORK no-network) that the developer-suggested TC list missed.
2. **Cost-cap test as a synthetic-injection contract**: the wave's tightest negative gate is "subprocess terminates gracefully when cumulative cost crosses cap"; without a deterministic injection mechanism this is untestable at Stage-6 unit level, so TC-S2-NN-COSTCAP defines the injection contract verbatim.
3. **3-path "no Claude calls" assertion**: a single grep is insufficient — TC-S3-02 combines static (grep imports) + static (grep subprocess) + runtime (psutil snapshot) and TC-S3-NN-NONETWORK adds a network-isolation overlay, so the "no Claude calls" guarantee is defended in depth.
4. **TC-UAT-* split from TC-S*-NN**: Stage-7 UAT gates that require a live `claude` invocation OR a structural grep against merged artifacts are split out (TC-UAT-01/07/08) so Stage-6 Dev DoD is not blocked on "the actual run took 28 minutes" empirical evidence — that is Stage-7's job.
5. **Producer-validator post-hoc verification** (TC-S3-NN-PRODUCERBLIND): BC-03 is enforced by Scrum-Bag dispatch assignment at Plan time, but the QA verification is a git-log check post-merge that catches dispatch-mixing if the Scrum-Bag's separation slipped — defense in depth aligned with tk4 round-2 lessons.

**Assumptions** (explicit, not hidden):
- A1. `claude --help` capability-probe is deterministic across CLI versions (i.e. the presence/absence of `--plugin-dir` in help text is the reliable signal). If a future CLI version emits help text without the flag despite supporting it, TC-S1-04 will need updating.
- A2. `tempfile.mkdtemp(prefix="smoke-")` returns a path on the same filesystem as the caller (no cross-filesystem rename surprises). Verified by NFR-Isolation but not by an explicit TC.
- A3. The 5-sample baseline `stddev` may underestimate true variance — known risk per PRD NFR-Reproducibility; advisory-only for `tokens.*` and `skill_loads.*` for the first month.
- A4. `psutil` is available on the developer's machine (for TC-S1-02 and TC-S3-02 runtime assertions). If not, fallback to `/proc/`-walk on Linux.
- A5. The `unshare --net` invocation in TC-S3-NN-NONETWORK is a Linux-only test; macOS/Windows developers fall back to the `socket.socket` monkey-patch path.

**Risks surfaced during test-case design**:
- **R1**: Cost-cap injection contract requires `lib/runner.py` to expose a `--stream-fixture` flag — if Stage-4 architecture did not anticipate this, S1 Dev may push back. Mitigation: flag documented in this artifact; S1 Dev dispatch sees it before code-write.
- **R2**: Zero-stddev guard behavior is undefined in PRD/architecture — TC-S2-06 forces the decision. Mitigation: Dev decides + documents in docstring; QA accepts the documented choice as long as it does not raise.
- **R3**: TC-S3-NN-PRODUCERBLIND relies on git-log evidence that depends on the Scrum-Bag actually dispatching to separate sub-agent contexts — if the orchestrator runs S1+S2+S3 in one shot, the git-author check returns identical authors and BC-03 evidence requires an alternative (commit-message tag). Mitigation: documented as fallback in the TC's "Steps" column.

— Legolas, QA Engineer, run-2026-05-13-tk5, Stage 5 Plan light step 3. *That bug still only counts as one.* Eighteen test cases plus three UAT structural gates. Twenty-four story ACs traced. Eight UAT gates mapped. No coverage holes.
