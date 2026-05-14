# BACKLOG-106 — Delivery-team plugin smoke test

**Type**: FEATURE
**Pipeline**: run-2026-05-13-tk5
**Created**: 2026-05-13
**Status**: IN PROGRESS
**PO**: Gandalf
**Stop-rule baseline**: defects/story = 0.111 (well under 0.4 threshold)

## Summary

The delivery-team plugin shipped 5/5 waves of the skill-token-economy initiative (BACKLOG-101, BACKLOG-103, BACKLOG-104) without an empirical regression test that invokes the team end-to-end. W3-18 telemetry hardening (`delivery-team/hooks/telemetry.py`) emits per-dispatch token data only when a pipeline runs — there is no probe that answers "is the team still building hello-world?" on the next plugin change. Token-economy, model-routing, and prompt-template regressions could merge on code review alone.

This initiative builds that probe. `python3 delivery-team/tests/smoke/run_smoke.py` spawns an isolated Claude Code subprocess (mktemp HOME + `--plugin-dir` with copy-into-fake-home fallback), runs a tiny hello-world delivery-flow pipeline, captures metrics from stream-json + existing telemetry hooks, and diffs against a committed 5-sample baseline. Hard-fail on outcome/cost/wall-clock/dispatch regressions; advisory-warn on token drift. Pytest meta-tests validate the harness itself without invoking Claude (< 5 sec). Local-only — no `.github/workflows/smoke-*.yml` per binding memory directive.

## Work Items (8 WIs)

| WI | Surface | Effort | Story |
|----|---------|--------|-------|
| W6-1 | `delivery-team/tests/smoke/run_smoke.py` + `lib/runner.py` + `lib/workspace.py` | M | Story 1 |
| W6-2 | `delivery-team/tests/smoke/lib/metrics.py` | M | Story 1 |
| W6-3 | `delivery-team/tests/smoke/lib/aggregator.py` | S | Story 1 |
| W6-4 | `delivery-team/tests/smoke/lib/report.py` | S | Story 1 |
| W6-5 | `delivery-team/tests/smoke/lib/baseline.py` + `baselines/hello_world_spike.json` | M | Story 2 |
| W6-6 | `delivery-team/tests/smoke/prompts/hello_world_spike.txt` + `fixtures/delivery_config_minimal.yml` | S | Story 2 |
| W6-7 | `delivery-team/tests/smoke/tests/test_meta.py` + fixture workspaces | M | Story 3 |
| W6-8 | `delivery-team/tests/smoke/README.md` + root `Makefile` `smoke` target | S | Story 3 |

### W6-1 — workspace + subprocess runner (M)

**Files**:
- `delivery-team/tests/smoke/run_smoke.py` (CLI entrypoint)
- `delivery-team/tests/smoke/lib/runner.py` (subprocess management)
- `delivery-team/tests/smoke/lib/workspace.py` (mktemp HOME + plugin install)

**Acceptance**: spawns isolated Claude Code subprocess with HOME override; tees stream-json to artifacts; respects `--cost-cap`, `--timeout`, `--init-baseline` flags; capability-probes `--plugin-dir` at startup with `HOME=<fake>` primary path, copy-into-fake-home fallback. Subprocess uses `mktemp` HOME so no contamination of developer's real `~/.claude/`.

### W6-2 — metrics parser (M)

**Files**: `delivery-team/tests/smoke/lib/metrics.py`

**Acceptance**: pure functions parse stream-json events into a `Metrics` dataclass; malformed events warn (do not crash); 100% unit-testable without Claude. Extracts `tokens.{input,output,cache_creation,cache_read}`, `model_usage` per-model, `cost_usd`, `wall_clock_seconds`, `dispatch_count`.

### W6-3 — workspace aggregator (S)

**Files**: `delivery-team/tests/smoke/lib/aggregator.py`

**Acceptance**: reads `.delivery/telemetry/skill-loads.jsonl` (emitted by existing `delivery-team/hooks/telemetry.py`, zero changes) + `state.md` + per-run summary JSON (emitted by existing `delivery-team/hooks/telemetry_run_summary.py`, invoked as fallback if direct read fails) from the subprocess workspace; merges into a single report dict. Reuse mandate per BC-02 — no re-implementation of telemetry hooks.

### W6-4 — report writers (S)

**Files**: `delivery-team/tests/smoke/lib/report.py`

**Acceptance**: writes `report.json` + `summary.md` + `stream.jsonl` to `delivery-team/tests/smoke/artifacts/<utc-timestamp>/`. `report.json` contains all fields per AC-03 (PRD): `outcome.success`, `wall_clock_seconds`, `cost_usd`, `tokens.*`, `model_usage`, `pipeline.{stages_completed, stories_completed, dispatch_count, defects_logged}`, `skill_loads`, `git_sha`, `claude_cli_version`.

### W6-5 — baseline + regression detector (M)

**Files**:
- `delivery-team/tests/smoke/lib/baseline.py`
- `delivery-team/tests/smoke/baselines/hello_world_spike.json`

**Acceptance**: `--init-baseline` runs scenario 5× sequentially (concurrency-of-1 enforced); mean+stddev computed per metric; baseline JSON shape mirrors `governance/skill-budgets.json` (`last_baseline`, `last_baseline_run`, advisory vs hard sections). Exit-code conventions mirror `scripts/check_skill_budgets.py` + `scripts/lint_known_debt.py`. Hard-fail/advisory-warn thresholds per FR-05 / PRD AC-05.

### W6-6 — prompt + fixtures + minimal config (S)

**Files**:
- `delivery-team/tests/smoke/prompts/hello_world_spike.txt`
- `delivery-team/tests/smoke/fixtures/delivery_config_minimal.yml`

**Acceptance**: prompt explicitly requests minimal pipeline (skip personas, skip UAT, skip retro tail beyond minimal retrospective required by Stop hook); config is minimal-viable for delivery-flow boot (no optional sub-skills, no analytics dashboard, no fitness reviews). Pinned to current delivery-flow config schema (currently v2.7 per `delivery-team/skills/delivery-flow/references/config-schema.md`).

### W6-7 — meta-tests (M)

**Files**:
- `delivery-team/tests/smoke/tests/test_meta.py`
- `delivery-team/tests/smoke/tests/fixtures/` (fixture workspaces — malformed stream, baseline-comparison demo, aggregator parsing inputs)

**Acceptance**: pytest passes 3 tests in < 5 sec; covers malformed-stream fault injection (parser warns, does not crash), baseline-comparison demo (synthetic inputs trip hard-fail and advisory-warn paths deterministically), aggregator-fixture parsing (fixture jsonl + state.md inputs yield expected merged dict). NO Claude calls.

**Producer-validator note (BC-03, binding)**: must be authored by a different Stage-6 Dev dispatch than the one that authors `lib/metrics.py` (W6-2) and `lib/baseline.py` (W6-5). Past-wave precedent: producer-validator separation validated:5.

### W6-8 — README + Makefile target (S)

**Files**:
- `delivery-team/tests/smoke/README.md`
- root `Makefile` (add `smoke` target; create file if it does not exist)

**Acceptance**: README documents local-only constraint with pointer to binding memory file (`/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md`); `make smoke` invokes `python3 delivery-team/tests/smoke/run_smoke.py` with sensible defaults (`--cost-cap 3.00`, `--timeout 1800`).

## Cross-cutting

- `delivery-team/architecture/smoke-test-architecture.md` — Mermaid diagram (runner → workspace → subprocess → telemetry hooks → aggregator → baseline → report flow) + decision log + local-only constraint cite with pointer to binding memory file. Stage-4 Architect artifact, not a Stage-6 Dev WI.

## File Surface Inventory

Complete file list this initiative touches or creates. Architect uses this for batching math at Stage 4; Dev uses it for change-set scoping at Stage 6.

| Path | Status | WI | Notes |
|------|--------|----|----|
| `delivery-team/tests/smoke/run_smoke.py` | NEW | W6-1 | CLI entrypoint |
| `delivery-team/tests/smoke/lib/__init__.py` | NEW | W6-1 | package marker |
| `delivery-team/tests/smoke/lib/runner.py` | NEW | W6-1 | subprocess wrapper |
| `delivery-team/tests/smoke/lib/workspace.py` | NEW | W6-1 | mktemp HOME + plugin install |
| `delivery-team/tests/smoke/lib/metrics.py` | NEW | W6-2 | stream-json parser |
| `delivery-team/tests/smoke/lib/aggregator.py` | NEW | W6-3 | telemetry hook output reader |
| `delivery-team/tests/smoke/lib/report.py` | NEW | W6-4 | JSON + Markdown writers |
| `delivery-team/tests/smoke/lib/baseline.py` | NEW | W6-5 | regression detector |
| `delivery-team/tests/smoke/baselines/hello_world_spike.json` | NEW | W6-5 | committed 5-sample baseline |
| `delivery-team/tests/smoke/prompts/hello_world_spike.txt` | NEW | W6-6 | pipeline kickoff prompt |
| `delivery-team/tests/smoke/fixtures/delivery_config_minimal.yml` | NEW | W6-6 | minimal `.delivery/config.yml` |
| `delivery-team/tests/smoke/tests/__init__.py` | NEW | W6-7 | package marker |
| `delivery-team/tests/smoke/tests/test_meta.py` | NEW | W6-7 | pytest meta-tests |
| `delivery-team/tests/smoke/tests/fixtures/*.jsonl` | NEW | W6-7 | malformed-stream + parsing fixtures |
| `delivery-team/tests/smoke/tests/fixtures/baseline_*.json` | NEW | W6-7 | baseline-comparison demo inputs |
| `delivery-team/tests/smoke/README.md` | NEW | W6-8 | local-only docs |
| `Makefile` | NEW or EDIT | W6-8 | add `smoke` target |
| `delivery-team/architecture/smoke-test-architecture.md` | NEW | cross-cutting | Architect Stage 4 |

Total: 14 new files + 1 new-or-edit (`Makefile`) + 1 architect artifact = ~16 surfaces. Matches the WI-count math (8 WIs, multi-file WIs counted explicitly).

## Telemetry Contract (reuse-mandate detail)

Aggregator (W6-3) reads from the subprocess workspace, NOT the developer's real `~/.delivery/`. Contract surface:

- **Input A**: `<workspace>/.delivery/telemetry/skill-loads.jsonl` — line-delimited JSON, one record per skill load. Schema owned by `delivery-team/hooks/telemetry.py`. Aggregator MUST tolerate missing file (treat as empty list).
- **Input B**: `<workspace>/.delivery/telemetry/run-summary-*.json` — per-run summary written by `delivery-team/hooks/telemetry_run_summary.py` on Stop. Aggregator picks the newest. Missing file → invoke the hook as fallback (BC-02 explicitly permits this).
- **Input C**: `<workspace>/.delivery/state.md` — current pipeline state. Aggregator parses minimally (stage count, stories completed, defects logged) — does not re-parse the full state machine.
- **Output**: single dict merged with stream-json `Metrics` (from W6-2), passed to report writer (W6-4).

No schema changes to `delivery-team/hooks/telemetry.py` or `telemetry_run_summary.py` permitted by this initiative. If a contract gap is found, file a follow-up BACKLOG — do not patch inline.

## Per-Story Acceptance (Stage 5 hint)

- **Story 1 acceptance**: `python3 delivery-team/tests/smoke/run_smoke.py --dry-run` writes a placeholder report to `delivery-team/tests/smoke/artifacts/<utc-timestamp>/report.json` WITHOUT invoking Claude (uses fixture stream-json). Demonstrates the full pipe is wired before paying for a real run.
- **Story 2 acceptance**: `python3 delivery-team/tests/smoke/run_smoke.py --init-baseline --dry-run` writes a 5-sample baseline from fixture inputs. Baseline JSON validates against `governance/skill-budgets.json` shape pattern.
- **Story 3 acceptance**: `pytest delivery-team/tests/smoke/tests/` passes in < 5 sec with 3 tests; `make smoke --dry-run` invokes runner; README links to binding memory file.

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| Prompt drift (orchestrator over-dispatches) | M | M | hard_max on dispatch_count + explicit "skip personas, skip UAT" in prompt | Dev (W6-6) |
| `--plugin-dir` flag semantics change in Claude CLI | L | M | capability-probe at startup with fallback path | Dev (W6-1) |
| Stop hook blocks pipeline mid-run | M | M | prompt requests minimal retrospective; runner captures stderr to detect | Dev (W6-1, W6-6) |
| 5-sample stddev underestimates true variance | M | L | advisory-only on tokens/skill_loads first month | PO |
| Subprocess HOME leaks to real `~/.claude/` | L | H | mktemp HOME + explicit env scrub in runner; meta-test asserts | Dev (W6-1) + Validator (W6-7) |
| Producer-validator separation violated | L | M | Stage-5 Plan assigns Story 3 to different Dev dispatch | Scrum Bag |

## Dependencies

- **External**: `claude` CLI installed locally with stream-json support; `python3` ≥ 3.10; `pytest` available (use `python3 -m pytest`).
- **Internal**: `delivery-team/hooks/telemetry.py` + `delivery-team/hooks/telemetry_run_summary.py` MUST exist and behave per their current contract. If either is missing or schema-changed before merge, this initiative pauses until contracts re-stabilize.
- **Sequencing**: Story 1 (runner/metrics/aggregator/report) lands before Story 2 (baseline can be tested against fixture reports). Story 3 (meta-tests + README) can land in parallel with Story 2 since meta-tests use fixtures, not live runs.

## Story Decomposition (target for Stage 5 Plan)

Memory lesson applied: story consolidation by file scope validated:5. Collapse 8 WIs into 3 stories at Stage 5.

- **Story 1 (Effort L)** — W6-1 + W6-2 + W6-3 + W6-4: runner + metrics + aggregator + report. One wired vertical: subprocess in, artifacts out. Files all under `delivery-team/tests/smoke/{run_smoke.py,lib/}`.
- **Story 2 (Effort M)** — W6-5 + W6-6: baseline + prompt/fixtures. Files under `delivery-team/tests/smoke/{baselines/,prompts/,fixtures/,lib/baseline.py}`. Producer half of producer-validator pair.
- **Story 3 (Effort M)** — W6-7 + W6-8: meta-tests + README/Makefile. Files under `delivery-team/tests/smoke/{tests/,README.md}` + root `Makefile`. Validator half of producer-validator pair (BC-03) — Story 3 Dev dispatch MUST be different agent than Stories 1+2.

File-count math discipline (architect-batching lesson): 8 WIs across ~14 file surfaces. Story 1 = 6 files (run_smoke.py + lib/{runner,workspace,metrics,aggregator,report}.py). Story 2 = 4 files (lib/baseline.py + baselines/hello_world_spike.json + prompts/hello_world_spike.txt + fixtures/delivery_config_minimal.yml). Story 3 = 4+ files (tests/test_meta.py + tests/fixtures/* + README.md + Makefile). Totals add up.

## Constraints

- **BC-01 LOCAL-ONLY**: NO `.github/workflows/smoke-*.yml`. CI workflows in this repo limited to lint/budget/metadata jobs. Source: `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md`. No bypass-with-ADR.
- **BC-02 Reuse mandate**: aggregator reads `delivery-team/hooks/telemetry.py` + `delivery-team/hooks/telemetry_run_summary.py` outputs directly. Mirror `governance/skill-budgets.json` shape + `scripts/check_skill_budgets.py` exit-code conventions.
- **BC-03 Producer-validator separation**: meta-test fixtures (W6-7) authored by separate Stage-6 Dev dispatch than `lib/metrics.py` (W6-2) and `lib/baseline.py` (W6-5). Validated:5 from past waves.
- **BC-04 Single-initiative**: full scope in one delivery-flow run; not staged across commits.
- **BC-05 Cost + time caps**: hard `--cost-cap 3.00` per run; 30-min wall-clock timeout; concurrency-of-1 on `--init-baseline`.

## Out of Scope

- Hardware-team / mtg-commander / other-plugin smoke tests. Factor `lib/` for reuse; build delivery-team's first.
- CI workflows. Banned by BC-01.
- Cost-tracking dashboards beyond per-run report. Future BACKLOG.
- Tightening 2σ band before 20+ accumulated production runs.

## Stop-rule

Defects/story > 0.4 across any 3-PR window pauses subsequent work. Current rolling rate = 0.111 (well under threshold). If this initiative pushes the rolling rate above 0.4, pause and triage before next plugin change.

## Downstream Stage Handoff Notes

For Stage-3 Design, Stage-4 Architect, Stage-5 Plan, and Stage-6 Dev consumers of this BACKLOG file.

- **Stage 3 (Design)**: paradigm decomposition is NOT required. The runner shape is procedural-imperative (subprocess + parsers + writers); no design-sprint paradigm exploration needed. Recommend skipping the design-sprint sub-skill and writing a minimal design note ratifying the runner-as-orchestrator pattern already implicit in the user-seed.
- **Stage 4 (Architect)**: produce `delivery-team/architecture/smoke-test-architecture.md` with one Mermaid sequence diagram (runner → workspace → claude subprocess → telemetry hooks → aggregator → baseline → report) and one decision log. Cite the binding memory file. No multi-persona architecture-board review needed — this is a single-paradigm Python tool, not a system architecture decision.
- **Stage 5 (Plan)**: collapse 8 WIs → 3 stories per the decomposition above. Assign Stories 1+2 to one Dev dispatch (producer side) and Story 3 to a separate Dev dispatch (validator side) to honor BC-03. Use story-level acceptance from this BACKLOG, not WI-level — WI-level is for Architect file-count math only.
- **Stage 6 (Dev)**: implement against the file inventory above. Each story = one PR-equivalent commit. Validator Dev MUST NOT read the producer Dev's `lib/metrics.py` or `lib/baseline.py` source while authoring fixtures — write fixtures from the PRD/BACKLOG contract only. (Producer-validator separation only works if the validator stays blind to producer internals.)
- **Stage 7 (UAT)**: maintainer runs `python3 delivery-team/tests/smoke/run_smoke.py` once on their machine; observes green report; commits the baseline if not already committed. UAT signs off when AC-01 through AC-08 are all met.

## Post-merge

Squash-rebase + ff-merge + push origin/main (no PR per Wave-N pattern; 6 prior waves precedent from BACKLOG-100..BACKLOG-104). After merge:

1. Run `python3 delivery-team/tests/smoke/run_smoke.py` once to confirm green report.
2. Commit `baselines/hello_world_spike.json` if it does not yet exist (post-baseline-capture commit allowed as a follow-up to the merge commit).
3. Update `CHANGELOG.md` with a BACKLOG-106 entry.
4. Add a note to `governance/fitness-review.md` if the smoke-test cadence (run-after-each-plugin-change) should appear in the quarterly fitness review schedule.
5. After 20 accumulated production runs, file a follow-up BACKLOG to tighten advisory bands from 2σ to 1.5σ.
