<!-- run: run-2026-05-13-tk5 -->
## Idea Brief

**Project Type**: FEATURE
**Date**: 2026-05-13
**Pipeline**: run-2026-05-13-tk5
**Initiative**: delivery-team plugin smoke test (BACKLOG-106)

*Spoken by Gandalf the Grey.*

> A product owner is never late, nor early. They prioritize precisely when they mean to. The team has shipped five waves with no probe at its heel — today we forge the probe.

### Problem Statement
The delivery-team plugin shipped 5/5 waves of the skill-token-economy initiative without an empirical regression test that invokes the team end-to-end. W3-18 telemetry hardening emits per-dispatch token data only when a pipeline runs; nothing answers "is the team still building hello-world?" on the next plugin change. This initiative builds that probe so token-economy, model-routing, and prompt-template regressions surface locally before merge.

### Target Users
- **Plugin maintainer (developer)**: needs empirical regression detection before merging plugin changes
- **Future contributors**: need a fast local check that "the team still works" after edits

### Goals
1. End-to-end smoke run completes in < 30 min wall-clock on a developer's machine, with hard `--cost-cap 3.00` per run and concurrency-of-1 enforcement.
2. `report.json` captures ≥ 6 metric groups (`outcome.success`, `wall_clock_seconds`, `cost_usd`, `tokens.{input,output,cache_creation,cache_read}`, `model_usage` per-model, `pipeline.{stages_completed, stories_completed, dispatch_count, defects_logged}`, `skill_loads`, `git_sha`, `claude_cli_version`); `--init-baseline` writes mean+stddev per metric across a 5-sample baseline at `baselines/hello_world_spike.json`.
3. 0 GitHub Actions workflows invoke `claude` (`.github/workflows/smoke-*.yml` does not exist); local-only constraint is recorded in `delivery-team/architecture/smoke-test-architecture.md` with a pointer to the binding memory file.

### Constraints
- **LOCAL-ONLY (binding)**: `claude` CLI is not available in CI runners. Memory file `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md` binds this. Tooling that shells out to `claude` MUST NOT live in `.github/workflows/`. No bypass-with-ADR.
- **Cost + time caps**: hard `--cost-cap 3.00` per run; 30-min wall-clock timeout; concurrency-of-1 enforcement.
- **Reuse existing telemetry — do not re-invent**: `delivery-team/hooks/telemetry.py` (emits `.delivery/telemetry/skill-loads.jsonl`) read directly by aggregator with zero changes; `delivery-team/hooks/telemetry_run_summary.py` (per-pipeline summary JSON) may be invoked as fallback. Mirror `governance/skill-budgets.json` shape for baseline JSON (`last_baseline`, `last_baseline_run`, advisory vs hard); mirror `scripts/check_skill_budgets.py` + `scripts/lint_known_debt.py` exit-code conventions.
- **Producer-validator separation**: meta-test fault-injection fixtures CANNOT share author with the parser (`lib/metrics.py`). Producer ≠ validator.
- **Route through delivery-flow**: full scope (runner + metrics + baseline + regression diff + meta-tests) in one initiative; not staged across separate commits.

### Initial Scope
- **W6-1** [M] — `delivery-team/tests/smoke/run_smoke.py` + `lib/runner.py` + `lib/workspace.py` (workspace + subprocess runner; `--plugin-dir` capability-probe at startup with `HOME=<fake>` primary path, copy-into-fake-home fallback)
- **W6-2** [M] — `lib/metrics.py` (stream-json → Metrics; pure functions; testable)
- **W6-3** [S] — `lib/aggregator.py` (reads `.delivery/telemetry/skill-loads.jsonl` + state.md + run-summary JSON)
- **W6-4** [S] — `lib/report.py` (JSON + Markdown writers; output to `delivery-team/tests/smoke/artifacts/<utc-timestamp>/{report.json, summary.md, stream.jsonl}`)
- **W6-5** [M] — `lib/baseline.py` + `baselines/hello_world_spike.json` (5-sample baseline writer + regression detector: HARD-FAIL on outcome/cost/wall_clock/stories_completed/dispatch_count; ADVISORY-WARN on tokens.*/skill_loads.* outside mean ± 2·stddev)
- **W6-6** [S] — `prompts/hello_world_spike.txt` + `fixtures/delivery_config_minimal.yml` (explicit "skip personas, skip UAT" + minimal-retrospective directive)
- **W6-7** [M] — `tests/test_meta.py` + fixture workspaces (pytest meta-tests; no Claude calls; malformed-stream fault injection + baseline-comparison demo + aggregator-fixture parsing)
- **W6-8** [S] — `delivery-team/tests/smoke/README.md` + root `Makefile` `smoke` target
- **Cross-cutting** — `delivery-team/architecture/smoke-test-architecture.md` with Mermaid diagram + decision log + local-only constraint cite (pointer to memory file)

### Out of Scope (initial)
- Hardware-team / mtg-commander / other-plugin smoke tests (factor `lib/` for reuse; build delivery-team's first)
- CI workflow (banned by memory directive — no `.github/workflows/smoke-*.yml`)
- Cost-tracking dashboards beyond the per-run report (future BACKLOG)

### Success Signal
A maintainer can run `python3 delivery-team/tests/smoke/run_smoke.py` after any plugin change and get a JSON+Markdown report (under `delivery-team/tests/smoke/artifacts/<utc-timestamp>/`) diffed against a 5-sample baseline, with **HARD-FAIL** on `outcome.success=false`, `cost > hard_max`, `wall_clock > hard_max`, `stories_completed` mismatch, or `dispatch_count > hard_max`, and **ADVISORY-WARN** on `tokens.*` and `skill_loads.*` outside mean ± 2·stddev. Meta-tests (malformed-stream fault injection, baseline-comparison demo, aggregator-fixture parsing) pass without invoking Claude.

### Open Risks (PO acknowledged)
- **Prompt drift**: orchestrator may dispatch beyond hello-world. Mitigation: `hard_max` on `dispatch_count` + explicit "skip personas, skip UAT" in prompt.
- **`--plugin-dir` semantics**: primary path uses `HOME=<fake>` + `--plugin-dir <repo>/delivery-team`; fallback copies plugin into `<fake-home>/.claude/plugins/delivery-team/`. `runner.py` capability-probes at startup.
- **Stop hook blocks**: existing Stop hook enforces retro/memory completion. Prompt requests minimal retrospective; runner captures stderr to detect.
- **Variance > stddev budget**: 5-sample baseline may underestimate true variance. First month is advisory-only on `tokens.*` and `skill_loads.*`; tighten after 20+ runs.

### Stop-Rule
Defects/story > 0.4 across any 3-PR window pauses subsequent work. Current rolling rate = 0.111 (well under threshold).

— Gandalf, PO, run-2026-05-13-tk5. All we have to decide is what to build with the time that is given to us. And I decide we build the probe.
