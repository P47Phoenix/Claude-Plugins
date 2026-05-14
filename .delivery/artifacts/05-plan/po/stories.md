<!-- run: run-2026-05-13-tk5 -->
<!-- author: Gandalf (Product Owner, Stage 5 light, step 1) -->
<!-- backlog: BACKLOG-106 -->
<!-- decomposition: 8 WIs -> 3 stories (file-scope consolidation, validated:5) -->
# Stories — BACKLOG-106 Delivery-team plugin smoke test

> *"A product owner is never late, nor early. They consolidate stories precisely when they mean to."* — Gandalf

Me carve eight WIs into three stories by file scope. Story 1 wire pipeline. Story 2 forge baseline + prompt. Story 3 prove harness + write README. Producer-validator split binds Story 3 to different Stage-6 Dev dispatch than Stories 1+2 (BC-03, validated:5).

WI coverage check (no orphans, no duplicates):
- W6-1 -> S1, W6-2 -> S1, W6-3 -> S1, W6-4 -> S1
- W6-5 -> S2, W6-6 -> S2
- W6-7 -> S3, W6-8 -> S3

Total: 8 WIs assigned, each exactly once.

---

## Story S1 — Wire the smoke-test pipeline (Effort: L)

**WIs**: W6-1, W6-2, W6-3, W6-4
**Depends on**: (none — entry story)
**Blocks**: S2, S3

### Files

**New**:
- `delivery-team/tests/smoke/run_smoke.py`
- `delivery-team/tests/smoke/lib/__init__.py`
- `delivery-team/tests/smoke/lib/runner.py`
- `delivery-team/tests/smoke/lib/workspace.py`
- `delivery-team/tests/smoke/lib/metrics.py`
- `delivery-team/tests/smoke/lib/aggregator.py`
- `delivery-team/tests/smoke/lib/report.py`

**Modified**: (none)

### Acceptance Criteria

- **AC-S1-01**: `python3 delivery-team/tests/smoke/run_smoke.py --help` exits 0 and lists flags `--init-baseline`, `--cost-cap`, `--timeout`, `--baseline`, `--dry-run`. (covers W6-1 AC, maps to PRD AC-01.)
- **AC-S1-02**: `python3 delivery-team/tests/smoke/run_smoke.py --dry-run` writes `delivery-team/tests/smoke/artifacts/<utc-timestamp>/{report.json, summary.md, stream.jsonl}` WITHOUT spawning a `claude` subprocess (uses fixture stream-json). (covers W6-1+W6-2+W6-3+W6-4 wired-pipeline AC, maps to Per-Story Acceptance Story 1 in BACKLOG-106 and PRD AC-02.)
- **AC-S1-03**: `lib/workspace.py` creates HOME via `tempfile.mkdtemp(prefix="smoke-")` and on exit a stat-based check asserts no writes landed under the developer's real `~/.claude/`. (covers W6-1 isolation AC, maps to PRD NFR-Isolation and architecture §8 mktemp-HOME decision.)
- **AC-S1-04**: `lib/runner.py` capability-probes `claude --help | grep -q -- --plugin-dir` at startup; result written to `report.json` as `plugin_load_strategy: "plugin-dir" | "copy-into-home"`. Primary path uses `--plugin-dir <repo>/delivery-team`; fallback copies plugin tree into `<tmpdir>/.claude/plugins/delivery-team/` (skipping `tests/smoke/` to avoid recursive inclusion). (covers W6-1 capability-probe AC, maps to PRD FR-01 and architecture §4.)
- **AC-S1-05**: `lib/runner.py` enforces `--cost-cap` and `--timeout` flags; subprocess wall-clock exceeding `--timeout` is killed with SIGTERM and `outcome.success=false`, `outcome.reason="timeout"` written to report. (covers W6-1 cost+time-cap AC, maps to PRD BC-05.)
- **AC-S1-06**: `lib/metrics.py` is pure-function: `parse_stream(events: Iterable[dict]) -> Metrics` returns a dataclass with `tokens.{input,output,cache_creation,cache_read}`, `model_usage: list[ModelUsage]`, `cost_usd`, `wall_clock_seconds`, `dispatch_count`; malformed events emit a `warnings.warn(...)` call and do not raise. (covers W6-2 AC, maps to PRD FR-02 and AC-03.)
- **AC-S1-07**: `lib/aggregator.py` reads `<workspace>/.delivery/telemetry/skill-loads.jsonl`, newest `<workspace>/.delivery/telemetry/run-summary-*.json`, and `<workspace>/.delivery/state.md`; missing `skill-loads.jsonl` treated as empty list; missing `run-summary-*.json` fallback-invokes `delivery-team/hooks/telemetry_run_summary.py`. NO modifications to either telemetry hook source file. (covers W6-3 AC, maps to PRD FR-03 and BC-02 reuse mandate.)
- **AC-S1-08**: `lib/report.py` writes `report.json` containing exactly the schema in `delivery-team/architecture/smoke-test-architecture.md` §5: keys `schema_version`, `run_id`, `git_sha`, `claude_cli_version`, `plugin_load_strategy`, `outcome.{success,exit_code,reason}`, `wall_clock_seconds`, `cost_usd`, `tokens.*`, `model_usage[]`, `pipeline.{stages_completed,stories_completed,dispatch_count,defects_logged}`, `skill_loads[]`, `advisory_warnings[]`, `hard_failures[]`. Unmeasurable fields emit `null`, not omitted. (covers W6-4 AC, maps to PRD AC-03 and FR-04.)

### Test cases (QA will expand)

- **TC-S1-01**: `--help` shows all 5 flags + exits 0.
- **TC-S1-02**: `--dry-run` writes all three artifacts under timestamped dir; no `claude` process spawned (asserted via `psutil` or process-table snapshot).
- **TC-S1-03**: post-run stat check confirms `~/.claude/` unmodified after a dry-run (mtime + size invariant on a chosen sentinel file).
- **TC-S1-04**: capability-probe sets strategy correctly when `--plugin-dir` is in help text and when it is absent (mocked help output).
- **TC-S1-05**: `--timeout 1` against a sleeping fixture subprocess produces `outcome.success=false`, `outcome.reason="timeout"` within 2 sec.
- **TC-S1-06**: malformed stream-json event (missing `usage` key) produces a `warnings.warn` call and does not raise; downstream Metrics still emitted.
- **TC-S1-07**: aggregator against fixture workspace with missing `skill-loads.jsonl` returns merged dict with `skill_loads: []`.
- **TC-S1-08**: `report.json` schema validates against the §5 contract; null-emission preserved for `claude_cli_version` when `claude --version` fails.

### Constraints (per producer-validator separation)

- Story 1 authors `lib/metrics.py` (W6-2). It does NOT author the meta-tests for `lib/metrics.py` — those belong to Story 3 per BC-03 producer-validator separation.
- Story 1 Dev dispatch may also be assigned Story 2 (per BACKLOG-106 §Story Decomposition: "Stories 1+2 to one Dev dispatch").
- Story 1 does not touch `lib/baseline.py`, `baselines/`, `prompts/`, `fixtures/`, `tests/`, `README.md`, or root `Makefile` — those belong to S2 or S3.

### Out of scope (story-local)

- Baseline JSON file and regression detector (Story 2).
- Pipeline kickoff prompt + minimal config fixture (Story 2).
- Pytest meta-tests + fixture workspaces (Story 3).
- README + Makefile target (Story 3).
- `--init-baseline` 5-run loop body (Story 2 — wired into runner but loop semantics are baseline-detector responsibility).

---

## Story S2 — Forge baseline + scenario prompt (Effort: M)

**WIs**: W6-5, W6-6
**Depends on**: S1 (needs `lib/runner.py` + `lib/report.py` interfaces wired so `--init-baseline` 5-run loop can produce reports for stddev computation)
**Blocks**: S3 (meta-tests exercise `lib/baseline.py` paths)

### Files

**New**:
- `delivery-team/tests/smoke/lib/baseline.py`
- `delivery-team/tests/smoke/baselines/hello_world_spike.json`
- `delivery-team/tests/smoke/prompts/hello_world_spike.txt`
- `delivery-team/tests/smoke/fixtures/delivery_config_minimal.yml`

**Modified**: (none)

### Acceptance Criteria

- **AC-S2-01**: `python3 delivery-team/tests/smoke/run_smoke.py --init-baseline --dry-run` runs the scenario 5× sequentially (concurrency-of-1 enforced — second invocation while one is in flight raises) and writes `delivery-team/tests/smoke/baselines/hello_world_spike.json` with `mean`, `stddev`, `n` per metric. (covers W6-5 AC, maps to PRD AC-04 and FR-06.)
- **AC-S2-02**: `baselines/hello_world_spike.json` JSON shape matches `delivery-team/architecture/smoke-test-architecture.md` §6 exactly: top-level `schema_version`, `scenario`, `n_samples`, `last_captured_utc`, `last_captured_git_sha`, `last_captured_cli_version`, `metrics{}` map; each metric entry has `mean`, `stddev`, `n`, optional `hard_max`, explicit `classification: "hard" | "advisory"`. Mirrors `governance/skill-budgets.json` per BC-02. (covers W6-5 shape AC, maps to PRD FR-05 and BC-02.)
- **AC-S2-03**: `lib/baseline.py` `compare(report: dict, baseline: dict) -> CompareResult` returns `(exit_code, hard_failures: list[str], advisory_warnings: list[str])`. Exit-code mirrors `scripts/check_skill_budgets.py`: 0 = pass, 1 = hard fail, 2 = config/usage error (missing baseline file, malformed JSON). (covers W6-5 detector AC, maps to PRD AC-05 and architecture §7.)
- **AC-S2-04**: HARD-FAIL triggers exactly: `outcome.success == false` OR `cost_usd > metrics.cost_usd.hard_max` OR `wall_clock_seconds > metrics.wall_clock_seconds.hard_max` OR `pipeline.dispatch_count > metrics.pipeline.dispatch_count.hard_max` OR `pipeline.stories_completed != metrics.pipeline.stories_completed.mean` (strict equality). (covers W6-5 hard-fail AC, maps to PRD FR-05 and architecture §7.)
- **AC-S2-05**: ADVISORY-WARN triggers (exit code stays 0): `tokens.{input,output,cache_creation,cache_read}` outside `mean ± 2·stddev` OR any `skill_loads.<skill>` outside `mean ± 2·stddev`. Warnings appended to `report.json.advisory_warnings[]` and `summary.md`. (covers W6-5 advisory AC, maps to PRD FR-05 and architecture §7.)
- **AC-S2-06**: `prompts/hello_world_spike.txt` is a single-paragraph delivery-flow kickoff prompt that explicitly requests: minimal pipeline, skip personas, skip UAT beyond minimal Stop-hook retrospective, single hello-world story. Plain text, no markdown. (covers W6-6 prompt AC, maps to PRD risk-register row "Prompt drift" mitigation.)
- **AC-S2-07**: `fixtures/delivery_config_minimal.yml` is a minimal-viable `.delivery/config.yml` pinned to current config schema (v2.7 per `delivery-team/skills/delivery-flow/references/config-schema.md`); no optional sub-skills, no analytics dashboard, no fitness reviews; passes the delivery-flow setup-wizard schema check on load. (covers W6-6 fixture AC, maps to PRD FR-08 and BACKLOG-106 §W6-6.)
- **AC-S2-08**: `baselines/hello_world_spike.json` contains entries for ≥ 6 metric groups: `wall_clock_seconds`, `cost_usd`, `tokens.*` (4 entries), `pipeline.*` (≥ 2 entries), `skill_loads.*` (≥ 3 entries). Total ≥ 11 metric rows in the `metrics{}` map. (covers W6-5 baseline-coverage AC, maps to PRD Success Metric.)

### Test cases (QA will expand)

- **TC-S2-01**: `--init-baseline --dry-run` with 5 fixture reports produces a baseline JSON whose `mean` and `stddev` match a hand-computed reference for each metric.
- **TC-S2-02**: `--init-baseline` while one is already in flight raises with a clear "concurrency-of-1" error message.
- **TC-S2-03**: baseline JSON validates against `governance/skill-budgets.json`-style shape (required keys present, `classification` is one of the two literals).
- **TC-S2-04**: `compare()` against a synthetic report with `outcome.success=false` returns exit_code=1 + `hard_failures` containing the rule string.
- **TC-S2-05**: `compare()` against a synthetic report with `cost_usd` above `hard_max` returns exit_code=1.
- **TC-S2-06**: `compare()` against a synthetic report with `tokens.input` outside `mean ± 2·stddev` returns exit_code=0 + `advisory_warnings` non-empty.
- **TC-S2-07**: `compare()` with missing baseline file returns exit_code=2.
- **TC-S2-08**: prompt file passes a grep-check for the required guardrails ("skip personas", "skip UAT", "minimal retrospective").
- **TC-S2-09**: minimal config loads under the delivery-flow setup-wizard without error.

### Constraints (per producer-validator separation)

- Story 2 authors `lib/baseline.py` (W6-5). It does NOT author the meta-tests for `lib/baseline.py` — those belong to Story 3 per BC-03 producer-validator separation.
- Per BACKLOG-106 §Story Decomposition, Story 2 Dev dispatch is the SAME dispatch as Story 1 (producer side of producer-validator pair).
- Story 2 does not author meta-tests, README, or Makefile (Story 3).
- Story 2 may consume the `lib/runner.py` and `lib/report.py` interfaces produced by Story 1 but does not modify those modules' public APIs (any required API change goes back to S1 first).

### Out of scope (story-local)

- Meta-tests against `lib/baseline.py` (Story 3 — different Dev dispatch).
- README documentation of baseline format (Story 3).
- Makefile `smoke` target wiring (Story 3).
- Re-running the 5-sample baseline post-merge (Stage 7 UAT + post-merge task per BACKLOG-106 §Post-merge).
- Tightening 2σ band to 1.5σ (deferred per NFR-Reproducibility — future BACKLOG after 20+ runs).

---

## Story S3 — Prove harness + ship docs (Effort: M)

**WIs**: W6-7, W6-8
**Depends on**: S1 (meta-tests exercise `lib/metrics.py` + `lib/aggregator.py` paths), S2 (meta-tests exercise `lib/baseline.py` paths; README documents prompt + config fixture)
**Blocks**: (none — exit story)

### Files

**New**:
- `delivery-team/tests/smoke/tests/__init__.py`
- `delivery-team/tests/smoke/tests/test_meta.py`
- `delivery-team/tests/smoke/tests/fixtures/` (directory with malformed-stream `.jsonl` fixtures, baseline-comparison demo `.json` fixtures, aggregator parsing inputs — sample `skill-loads.jsonl` + `run-summary-*.json` + `state.md`)
- `delivery-team/tests/smoke/README.md`

**Modified / New-or-Edit**:
- `Makefile` (root) — NEW if absent, EDIT if present; adds `smoke` target.

### Acceptance Criteria

- **AC-S3-01**: `python3 -m pytest delivery-team/tests/smoke/tests/` passes 3 tests in < 5 sec wall-clock; zero `claude` subprocesses spawned during the run (asserted via process-table snapshot in a fixture or by inspection of the test bodies — no `subprocess.Popen("claude", ...)` allowed). (covers W6-7 AC, maps to PRD AC-06 and FR-07.)
- **AC-S3-02**: Test 1 — malformed-stream fault injection: fixture jsonl contains 3 valid events + 2 malformed (missing `usage`, malformed JSON line); `lib/metrics.py:parse_stream` emits `warnings.warn(...)` for each malformed line and returns a `Metrics` whose `dispatch_count` reflects only the valid events. Test asserts both the warning count and the dispatch count. (covers W6-7 malformed-stream AC, maps to PRD FR-02.)
- **AC-S3-03**: Test 2 — baseline-comparison demo: two synthetic reports (one tripping hard-fail via `cost_usd > hard_max`, one tripping advisory-warn via `tokens.input` outside ± 2σ) are passed to `lib/baseline.py:compare()` against a synthetic baseline fixture. Test asserts exit_code=1 + non-empty `hard_failures` on report A; exit_code=0 + non-empty `advisory_warnings` on report B. (covers W6-7 baseline-comparison AC, maps to PRD FR-05.)
- **AC-S3-04**: Test 3 — aggregator-fixture parsing: fixture workspace at `tests/fixtures/workspace_sample/.delivery/{telemetry/skill-loads.jsonl, telemetry/run-summary-*.json, state.md}` is read by `lib/aggregator.py`; merged dict contains the expected `skill_loads[]`, `pipeline.{stages_completed,stories_completed,dispatch_count,defects_logged}` values pre-computed by hand. (covers W6-7 aggregator-parsing AC, maps to PRD FR-03.)
- **AC-S3-05**: `delivery-team/tests/smoke/README.md` documents: (1) one-line invocation (`python3 delivery-team/tests/smoke/run_smoke.py` and `make smoke`), (2) the LOCAL-ONLY constraint with full path to the binding memory file `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md`, (3) flag reference (`--init-baseline`, `--cost-cap`, `--timeout`, `--baseline`, `--dry-run`), (4) baseline-capture workflow, (5) exit-code conventions, (6) pointer to `delivery-team/architecture/smoke-test-architecture.md`. (covers W6-8 README AC, maps to PRD AC-07/AC-08 and BC-01.)
- **AC-S3-06**: root `Makefile` `smoke` target exists, invokes `python3 delivery-team/tests/smoke/run_smoke.py --cost-cap 3.00 --timeout 1800`, declared `.PHONY: smoke`. If `Makefile` is new, it carries that single target plus a `help` target listing it. (covers W6-8 Makefile AC, maps to PRD FR-08 and BACKLOG-106 §W6-8.)
- **AC-S3-07**: No file authored by Story 3 imports from `delivery-team/tests/smoke/lib/metrics.py` or `delivery-team/tests/smoke/lib/baseline.py` source files at fixture-authoring time — Story 3 Dev dispatch wrote fixtures from the PRD/BACKLOG/architecture-doc contract only. (Verifiable post-hoc by git-blame split + commit-author check; covers W6-7 producer-validator AC, maps to BC-03.)
- **AC-S3-08**: `python3 -m pytest delivery-team/tests/smoke/tests/ --collect-only` shows exactly 3 test functions; no `parametrize` explosion (keeps the < 5 sec budget honest and the failure attribution clear). (covers W6-7 test-count AC, maps to PRD AC-06.)

### Test cases (QA will expand)

- **TC-S3-01**: `python3 -m pytest delivery-team/tests/smoke/tests/` exits 0 and reports `3 passed in < 5.00s`.
- **TC-S3-02**: process-table inspection during test run shows no `claude` child processes.
- **TC-S3-03**: malformed-stream fixture trips exactly 2 warnings (one per malformed line); valid-event `dispatch_count` is correct.
- **TC-S3-04**: synthetic hard-fail report yields exit_code=1; synthetic advisory-warn report yields exit_code=0 with non-empty advisory list.
- **TC-S3-05**: aggregator fixture parsing yields the hand-computed merged dict (byte-equal JSON dump).
- **TC-S3-06**: README contains the binding memory-file full path (grep check).
- **TC-S3-07**: `make smoke -n` (dry-run) prints the runner invocation without executing it.
- **TC-S3-08**: `make help` lists `smoke` as a target.
- **TC-S3-09**: post-hoc git history shows S3 commit(s) by a different author/dispatch than S1+S2 commit(s).

### Constraints (per producer-validator separation)

- **producer-validator separation (BC-03, BINDING from past waves; validated:5)**: Story 3 meta-tests and fixtures MUST be authored by a DIFFERENT Stage-6 Dev dispatch than the dispatch that authored Story 1's `lib/metrics.py` (W6-2) and Story 2's `lib/baseline.py` (W6-5). The validator Dev dispatch authors fixtures from the PRD, BACKLOG-106, and `delivery-team/architecture/smoke-test-architecture.md` contracts ONLY and MUST NOT read the source of `lib/metrics.py` or `lib/baseline.py` while writing fixtures. Stage-7 UAT verifies the git log shows two separate Dev commits (or two distinct authors within a squash) for the producer (S1+S2) and validator (S3) halves. Source: ADR-tk5-001 §"Producer-Validator Separation" + BACKLOG-106 §W6-7 + BC-03.
- The Scrum Bag at Stage 5 owns the dispatch assignment that enforces this separation; the orchestrator dispatches Story 3 to a fresh sub-agent context, not the same context that ran S1+S2.
- Story 3 does not modify `lib/metrics.py`, `lib/baseline.py`, `lib/aggregator.py`, `lib/runner.py`, `lib/workspace.py`, `lib/report.py`, `prompts/`, `fixtures/delivery_config_minimal.yml`, or `baselines/hello_world_spike.json` — those are owned by S1 and S2.

### Out of scope (story-local)

- Modifying any `lib/*.py` parser, runner, or baseline detector (S1 + S2 own those — producer side).
- Modifying the `baselines/hello_world_spike.json` capture (S2 — re-capture post-merge per BACKLOG-106 §Post-merge).
- Re-authoring the prompt or minimal config fixture (S2).
- Adding `.github/workflows/smoke-*.yml` (BANNED by BC-01 — README explicitly cites the binding memory file).
- Cost-tracking dashboards or per-run history beyond the timestamped artifacts dir (future BACKLOG per PRD Out-of-Scope).

---

## Cross-story producer-validator summary

| Story | Dev dispatch | Authors | Validator-blind? |
|-------|--------------|---------|------------------|
| S1 | Dispatch A (producer) | `run_smoke.py`, `lib/{runner,workspace,metrics,aggregator,report}.py` | n/a — producer side |
| S2 | Dispatch A (producer, same as S1) | `lib/baseline.py`, `baselines/hello_world_spike.json`, `prompts/hello_world_spike.txt`, `fixtures/delivery_config_minimal.yml` | n/a — producer side |
| S3 | Dispatch B (validator, DIFFERENT from A) | `tests/test_meta.py`, `tests/fixtures/`, `README.md`, root `Makefile` | YES — fixtures written from PRD/BACKLOG/architecture contract only; MUST NOT read S1+S2 source while authoring |

Search-grep-able phrase: **producer-validator** separation enforced at S3 per BC-03 (validated:5 from past waves).

---

## WI coverage audit (no orphans, no duplicates)

| WI | Story | File scope |
|----|-------|-----------|
| W6-1 | S1 | `run_smoke.py` + `lib/runner.py` + `lib/workspace.py` |
| W6-2 | S1 | `lib/metrics.py` |
| W6-3 | S1 | `lib/aggregator.py` |
| W6-4 | S1 | `lib/report.py` |
| W6-5 | S2 | `lib/baseline.py` + `baselines/hello_world_spike.json` |
| W6-6 | S2 | `prompts/hello_world_spike.txt` + `fixtures/delivery_config_minimal.yml` |
| W6-7 | S3 | `tests/test_meta.py` + `tests/fixtures/` |
| W6-8 | S3 | `README.md` + root `Makefile` |

Eight WIs, three stories, zero orphans, zero duplicates. Carve done.

— Gandalf, PO, run-2026-05-13-tk5. Three stories to bind the eight, in the smoke-test ground where the shadows lie.
