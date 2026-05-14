<!-- run: run-2026-05-13-tk5 -->
# User-Input Seed — run-2026-05-13-tk5

This is the user's pipeline-kickoff brief as provided to the orchestrator. It serves as the upstream "raw idea" for Stage 1 Idea.

## Title
Delivery-team plugin smoke test (hello-world; metrics-capturing; local-only)

## Context

The delivery-team plugin shipped 5/5 waves of the skill-token-economy initiative. None of the token-economy, model-routing, or prompt-template changes were gated by an empirical regression test that actually invokes the team end-to-end. The W3-18 telemetry hardening produces per-dispatch token data — but only when a pipeline runs. There is no scheduled "is the team still building hello-world?" probe.

This initiative builds that probe: a smoke test that spawns its own Claude Code instance, invokes the delivery-flow pipeline against a tiny hello-world brief, and captures runtime metrics (model usage, token usage, duration, dispatch counts, pipeline signals). Metrics get diffed against a stored baseline so regressions surface on the next plugin change.

## Hard PO directives (binding)

- **Local-only**. Claude Code is local-developer-only. Tooling that shells out to `claude` MUST NOT live in `.github/workflows/`. Memory file: `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md` (saved Step 0, indexed in MEMORY.md).
- **Route through delivery-flow**. No bypass-with-ADR.
- **Full scope**: runner + metrics + baseline + regression diff + meta-tests in one initiative; not staged across separate commits.

## Work scope (8 WIs)

| WI | Surface | Effort |
|----|---------|--------|
| W6-1 | `delivery-team/tests/smoke/run_smoke.py` + `lib/runner.py` + `lib/workspace.py` (workspace + subprocess runner) | M |
| W6-2 | `lib/metrics.py` (stream-json → Metrics; pure functions; testable) | M |
| W6-3 | `lib/aggregator.py` (reads `.delivery/telemetry/skill-loads.jsonl` + state.md + run-summary JSON) | S |
| W6-4 | `lib/report.py` (JSON + Markdown writers) | S |
| W6-5 | `lib/baseline.py` + `baselines/hello_world_spike.json` (baseline + regression detector) | M |
| W6-6 | `prompts/hello_world_spike.txt` + `fixtures/delivery_config_minimal.yml` | S |
| W6-7 | `tests/test_meta.py` + fixture workspaces (pytest meta-tests; no Claude calls) | M |
| W6-8 | `delivery-team/tests/smoke/README.md` + root `Makefile` `smoke` target | S |

Cross-cutting: `delivery-team/architecture/smoke-test-architecture.md` with Mermaid diagram + decision log + local-only constraint cite.

## Existing utilities to reuse (no re-invention)

- `delivery-team/hooks/telemetry.py` — emits `.delivery/telemetry/skill-loads.jsonl`; aggregator reads it directly (zero changes).
- `delivery-team/hooks/telemetry_run_summary.py` — per-pipeline summary JSON; aggregator may invoke as fallback.
- `governance/skill-budgets.json` shape pattern for baseline JSON (`last_baseline`, `last_baseline_run`, advisory vs hard).
- `scripts/check_skill_budgets.py` + `scripts/lint_known_debt.py` patterns for exit-code conventions.

## Acceptance criteria (initiative-level)

1. `python3 delivery-team/tests/smoke/run_smoke.py` completes on the developer's machine in < 30 min wall-clock.
2. Output: `delivery-team/tests/smoke/artifacts/<utc-timestamp>/{report.json, summary.md, stream.jsonl}`.
3. `report.json` contains: `outcome.success`, `wall_clock_seconds`, `cost_usd`, `tokens.{input,output,cache_creation,cache_read}`, `model_usage` (per-model dispatches+tokens), `pipeline.{stages_completed, stories_completed, dispatch_count, defects_logged}`, `skill_loads` (from telemetry.jsonl), `git_sha`, `claude_cli_version`.
4. `--init-baseline` flag runs scenario 5× sequentially → writes `baselines/hello_world_spike.json` with mean+stddev per metric.
5. Default regression detector: HARD-FAIL on `outcome.success=false`, `cost > hard_max`, `wall_clock > hard_max`, `stories_completed` mismatch, `dispatch_count > hard_max`. ADVISORY-WARN on `tokens.*` and `skill_loads.*` outside mean ± 2·stddev.
6. Meta-tests in `tests/test_meta.py` pass: malformed-stream fault injection, baseline-comparison demo, aggregator-fixture parsing.
7. NO `.github/workflows/smoke-*.yml` exists.
8. `delivery-team/architecture/smoke-test-architecture.md` records local-only constraint with pointer to memory file.

## Out of scope

- Hardware-team / mtg-commander / other-plugin smoke tests (factor `lib/` for reuse; build only delivery-team's first).
- CI workflow (banned by memory directive).
- Cost-tracking dashboards beyond per-run report (future BACKLOG).

## Open risks (PO has acknowledged)

- **Prompt drift**: orchestrator may dispatch more than hello-world spike requires. Mitigation: `hard_max` on `dispatch_count` + explicit "skip personas, skip UAT" in prompt.
- **Cost overrun**: hard `--cost-cap 3.00` + 30-min wall-clock timeout + concurrency-of-1 enforcement.
- **`--plugin-dir` semantics**: primary path uses `HOME=<fake>` + `--plugin-dir <repo>/delivery-team`. Fallback: copy plugin into `<fake-home>/.claude/plugins/delivery-team/`. runner.py capability-probes at startup.
- **Stop hook blocks**: existing Stop hook enforces retro/memory completion. Prompt explicitly requests minimal retrospective; runner captures stderr to detect.
- **Variance > stddev budget**: 5-sample baseline may underestimate true variance. First month is advisory-only on `tokens.*` and `skill_loads.*`; tighten after 20+ runs.

## Stop-rule

Defects/story > 0.4 across any 3-PR window pauses subsequent work. Current rolling rate = 0.111 (well under threshold).
