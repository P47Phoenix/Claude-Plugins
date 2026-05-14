<!-- run: run-2026-05-13-tk5 -->
# PRD — Delivery-team plugin smoke test (BACKLOG-106)

*Authored by Gandalf, Product Owner, run-2026-05-13-tk5.*

> A product owner is never late, nor early. They prioritize precisely when they mean to.

## Business Value

The delivery-team plugin shipped 5/5 waves of the skill-token-economy initiative (BACKLOG-101, BACKLOG-103, BACKLOG-104) without an empirical regression test that invokes the team end-to-end. Token-economy, model-routing, and prompt-template changes merged on code review alone. W3-18 telemetry hardening (see `delivery-team/hooks/telemetry.py`) emits per-dispatch token data only when a pipeline runs — nothing answers "is the team still building hello-world?" on the next plugin change.

The next plugin change — be it a new skill, a hook adjustment, or a config-schema bump — risks silent regression in cost, dispatch breadth, or pipeline completion without a probe. This initiative forges the probe so token-economy, model-routing, and prompt-template regressions surface locally before merge.

TARGET vs CURRENT framing:
- **CURRENT**: Telemetry exists (`delivery-team/hooks/telemetry.py` writes `.delivery/telemetry/skill-loads.jsonl`; `delivery-team/hooks/telemetry_run_summary.py` writes per-run summaries) but is only populated by hand-run pipelines. No baseline. No regression detector. No pytest meta-test of the harness itself.
- **TARGET (this initiative)**: Single-command `python3 delivery-team/tests/smoke/run_smoke.py` spawns isolated Claude Code subprocess, runs hello-world pipeline, captures metrics, diffs against committed 5-sample baseline, exits 0/non-zero on hard/advisory thresholds. Meta-tests validate the harness without invoking Claude.

## User Stories

- **US-1**: As a plugin maintainer, I want to run `python3 delivery-team/tests/smoke/run_smoke.py` after any plugin change so that I get an empirical regression signal in < 30 min wall-clock.
- **US-2**: As a maintainer, I want a 5-sample baseline captured once and committed to the repo so that future runs can diff against it without re-baselining each time.
- **US-3**: As a maintainer, I want hard-fail on outcome/cost/wall-clock/dispatch regressions and advisory-warn on token drift so that signal-to-noise is high.
- **US-4**: As a contributor, I want pytest meta-tests that validate the runner WITHOUT calling Claude so that the test harness itself is testable in < 5 seconds.
- **US-5**: As a future plugin author, I want the `lib/` factored so that hardware-team and mtg-commander can reuse it later (out of scope this initiative, but boundary preserved).

## Functional Requirements

- **FR-01**: Runner spawns isolated Claude Code subprocess with `mktemp` HOME and `--plugin-dir <repo>/delivery-team` (primary path). Fallback path: copy plugin into `<fake-home>/.claude/plugins/delivery-team/`. Runner capability-probes at startup to select the path.
- **FR-02**: Metrics parser consumes stream-json output to extract `tokens.{input,output,cache_creation,cache_read}`, `model_usage` (per-model dispatch + token counts), `cost_usd`, `wall_clock_seconds`, `dispatch_count`. Pure functions; malformed events warn (do not crash).
- **FR-03**: Aggregator reads `.delivery/telemetry/skill-loads.jsonl` (emitted by `delivery-team/hooks/telemetry.py`) and the per-run summary JSON (emitted by `delivery-team/hooks/telemetry_run_summary.py`) from the subprocess workspace, plus `state.md`, and merges into a single report dict.
- **FR-04**: Report writer emits `report.json` + `summary.md` + `stream.jsonl` under `delivery-team/tests/smoke/artifacts/<utc-timestamp>/`.
- **FR-05**: Baseline detector compares current report against `baselines/hello_world_spike.json` with HARD-FAIL on `outcome.success=false`, `cost > hard_max`, `wall_clock > hard_max`, `stories_completed` mismatch, `dispatch_count > hard_max`; ADVISORY-WARN on `tokens.*` and `skill_loads.*` outside mean ± 2·stddev.
- **FR-06**: `--init-baseline` runs scenario 5× sequentially (concurrency-of-1 enforced) and writes mean+stddev per metric to `baselines/hello_world_spike.json`.
- **FR-07**: Pytest meta-tests cover malformed-stream fault injection, baseline-comparison demo, aggregator-fixture parsing. NO Claude calls. Run in < 5 sec.
- **FR-08**: `delivery-team/tests/smoke/README.md` documents local-only constraint with pointer to the binding memory file. Root `Makefile` `smoke` target invokes runner with sensible defaults.

## Acceptance Criteria

- **AC-01**: `python3 delivery-team/tests/smoke/run_smoke.py` completes on the developer's machine in < 30 min wall-clock.
- **AC-02**: Output written to `delivery-team/tests/smoke/artifacts/<utc-timestamp>/{report.json, summary.md, stream.jsonl}`.
- **AC-03**: `report.json` contains all of: `outcome.success`, `wall_clock_seconds`, `cost_usd`, `tokens.{input,output,cache_creation,cache_read}`, `model_usage` (per-model dispatches+tokens), `pipeline.{stages_completed, stories_completed, dispatch_count, defects_logged}`, `skill_loads` (from `.delivery/telemetry/skill-loads.jsonl`), `git_sha`, `claude_cli_version`.
- **AC-04**: `--init-baseline` flag runs the scenario 5× sequentially and writes `baselines/hello_world_spike.json` with mean+stddev per metric.
- **AC-05**: Default regression detector HARD-FAILS on `outcome.success=false`, `cost > hard_max`, `wall_clock > hard_max`, `stories_completed` mismatch, `dispatch_count > hard_max`; ADVISORY-WARNS on `tokens.*` and `skill_loads.*` outside mean ± 2·stddev.
- **AC-06**: Meta-tests in `tests/test_meta.py` pass for malformed-stream fault injection, baseline-comparison demo, and aggregator-fixture parsing; no Claude calls; complete in < 5 sec.
- **AC-07**: NO `.github/workflows/smoke-*.yml` exists in the repo.
- **AC-08**: `delivery-team/architecture/smoke-test-architecture.md` records the local-only constraint with a pointer to the binding memory file.

## Non-Functional Requirements

- **NFR-Performance**: < 30 min wall-clock per single run on a developer's machine.
- **NFR-Cost**: hard `--cost-cap 3.00` per single run; `--init-baseline` envelope acknowledged as 5× cap (max $15 per baseline capture).
- **NFR-Reproducibility**: 2σ regression detection band on `tokens.*` and `skill_loads.*` for the first month; tighten after 20+ accumulated production runs.
- **NFR-Reuse**: `lib/` boundary preserved so hardware-team and mtg-commander can adopt later without rework (out of scope to actually wire them up here).
- **NFR-Isolation**: subprocess uses `mktemp` HOME; no contamination of developer's real `~/.claude/`.

## Constraints (binding)

- **BC-01 LOCAL-ONLY**: per memory `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md`, NO `.github/workflows/smoke-*.yml` may be authored. CI workflows in this repo are limited to lint/budget/metadata jobs (`workflow-injection-lint.yml`, `skill-line-budget.yml`, `fitness-review.yml`). No bypass-with-ADR.
- **BC-02 Reuse mandate**: aggregator MUST read existing `delivery-team/hooks/telemetry.py` + `delivery-team/hooks/telemetry_run_summary.py` outputs directly. No re-implementation. Mirror `governance/skill-budgets.json` shape for baseline JSON (`last_baseline`, `last_baseline_run`, advisory vs hard); mirror `scripts/check_skill_budgets.py` + `scripts/lint_known_debt.py` exit-code conventions.
- **BC-03 Producer-validator separation**: meta-test fault-injection fixtures CANNOT be authored by the same Stage-6 Dev dispatch that authors `lib/metrics.py` or `lib/baseline.py`. Binding from past waves; applies to validator-style artifacts. (Memory: producer-validator separation validated:5.)
- **BC-04 Route through delivery-flow**: full scope (runner + metrics + baseline + regression diff + meta-tests) in one initiative; not staged across separate commits.
- **BC-05 Cost + time caps**: hard `--cost-cap 3.00` per run; 30-min wall-clock timeout; concurrency-of-1 enforcement on `--init-baseline`.

## Out of Scope

- Hardware-team / mtg-commander / other-plugin smoke tests. (Factor `lib/` for reuse; build delivery-team's first.)
- CI workflows. (Banned by BC-01.)
- Cost-tracking dashboards beyond per-run report. (Future BACKLOG.)
- Tightening 2σ → tighter band before 20 accumulated production runs.

## Success Metric

After merge, the maintainer runs `python3 delivery-team/tests/smoke/run_smoke.py` once and sees a green report. After running again with no plugin changes, the regression detector reports PASS (within 2σ on advisory metrics and within hard caps on outcome/cost/wall-clock/dispatch). The committed baseline (`baselines/hello_world_spike.json`) parses and contains mean+stddev for ≥ 6 metric groups: `outcome`, `wall_clock_seconds`, `cost_usd`, `tokens.*`, `model_usage`, `pipeline.*`, `skill_loads`.

## Open Questions

None blocking. All open risks acknowledged in the idea-brief have mitigations:
- Prompt drift → `hard_max` on `dispatch_count` + explicit "skip personas, skip UAT" in prompt.
- `--plugin-dir` semantics → capability-probe at startup.
- Stop hook blocks → prompt requests minimal retrospective; runner captures stderr.
- Variance > stddev budget → advisory-only first month; tighten after 20+ runs.

## Constraints file

Problem-scoped `constraints.yml` emitted alongside this PRD at `.delivery/artifacts/02-refine/po/constraints.yml`.

## Stop-rule

Defects/story > 0.4 across any 3-PR window pauses subsequent work. Current rolling rate = 0.111 (well under threshold).

— Gandalf, PO, run-2026-05-13-tk5. The probe is forged with the time that is given to us.
