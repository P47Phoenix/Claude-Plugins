<!-- run: run-2026-05-13-tk5 -->
<!-- author: Celebrimbor (Solution Architect, Stage 4 light) -->
<!-- backlog: BACKLOG-106 -->
# ADR-tk5-001 — Smoke-Test Runner Architecture

## Status

**Accepted** — 2026-05-13 (run-2026-05-13-tk5, Stage 4 light)

## Context

The delivery-team plugin shipped 5/5 waves of the skill-token-economy initiative (BACKLOG-101, BACKLOG-103, BACKLOG-104) on code review alone. Token-economy, model-routing, and prompt-template regressions could merge without an empirical signal. Telemetry exists — `delivery-team/hooks/telemetry.py` writes `.delivery/telemetry/skill-loads.jsonl` per Skill invocation, and `delivery-team/hooks/telemetry_run_summary.py` writes a per-run summary JSON on pipeline stop — but those signals only populate when a pipeline runs by hand. Nothing answers "is the team still building hello-world?" on the next plugin change.

BACKLOG-106 introduces a smoke-test runner to close that gap. Three architectural decisions need to be locked before Stage-6 implementation: how to invoke Claude (subprocess vs SDK), how to reuse existing telemetry, and where to run it (local vs CI). The constraints file (`.delivery/artifacts/02-refine/po/constraints.yml`) declares the local-only directive as binding (BC-01) and the telemetry-reuse mandate as binding (BC-02), with producer-validator separation (BC-03) carried over from past-wave precedent (validated:5).

## Decision

The smoke-test runner is built as follows:

1. **Isolated Claude Code subprocess, not SDK.** `lib/runner.py` spawns `claude` via `subprocess.Popen` with `HOME` overridden to a `tempfile.mkdtemp` directory. The subprocess loads the delivery-team plugin via `--plugin-dir <repo>/delivery-team` (primary path) with a copy-into-`<tmp>/.claude/plugins/delivery-team/` fallback selected by a capability probe (`claude --help | grep -q -- --plugin-dir`).
2. **Reuse `telemetry.py` and `telemetry_run_summary.py` outputs.** `lib/aggregator.py` reads `<workspace>/.delivery/telemetry/skill-loads.jsonl` and the newest `<workspace>/.delivery/telemetry/run-summary-*.json`, falling back to invoking `telemetry_run_summary.py` directly if no summary file exists. No schema changes to either hook are made by this initiative.
3. **5-sample baseline with mean+stddev, mirroring `governance/skill-budgets.json` shape.** `--init-baseline` runs the scenario 5× sequentially (concurrency-of-1 enforced in the runner) and writes `baselines/hello_world_spike.json` with `mean`, `stddev`, `n`, optional `hard_max`, and explicit `classification: hard | advisory` per metric. Hard-class metrics fail the run on threshold breach; advisory-class metrics warn within mean ± 2σ.
4. **Local-only invocation; no CI.** Entry points are `python3 delivery-team/tests/smoke/run_smoke.py` and the root `Makefile` `smoke` target. No `.github/workflows/smoke-*.yml` is authored. This decision is BINDING per the memory directive in §"Local-Only Constraint" below and cannot be reopened via subsequent ADR.

## Local-Only Constraint

This ADR locks in the local-only invocation model as binding. The source is the memory file at `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md` (memory: `feedback_claude_code_local_only`). The rule: the `claude` CLI is only available on the developer's machine; CI runners (GitHub Actions, etc.) have neither the binary nor the credentials. Any `.github/workflows/smoke-*.yml` would silently fail or never run, so none may be authored.

CI workflows in this repo are limited to lint/budget/metadata jobs — `workflow-injection-lint.yml`, `skill-line-budget.yml`, `fitness-review.yml`. The smoke-test runner is invoked exclusively from the developer's machine. The README (W6-8) and the permanent architecture doc (`delivery-team/architecture/smoke-test-architecture.md` §9) both point back to this memory file by full path so a future contributor cannot lose the directive's provenance.

This constraint is BINDING. No bypass-with-ADR is permitted.

## Producer-Validator Separation

Per BC-03 (binding from past waves; validated:5), the Stage-6 Dev dispatch that authors the meta-test fixtures in `delivery-team/tests/smoke/tests/test_meta.py` and `delivery-team/tests/smoke/tests/fixtures/` (W6-7) MUST be a DIFFERENT dispatch from the one that authors `delivery-team/tests/smoke/lib/metrics.py` (W6-2) and `delivery-team/tests/smoke/lib/baseline.py` (W6-5).

Rationale: the meta-tests are the validator side of a producer-validator pair. If the same dispatch writes both the parser and the fault-injection fixtures, the validator inherits the producer's blind spots — malformed-stream edge cases the producer did not consider will be absent from the fixture corpus too. The Stage-5 Plan assigns Stories 1+2 (W6-1 through W6-6) to one Dev dispatch and Story 3 (W6-7 + W6-8) to a different Dev dispatch. The validator dispatch authors fixtures from the PRD/BACKLOG contract only and MUST NOT read `lib/metrics.py` or `lib/baseline.py` source while writing fixtures.

This separation only works if it is enforced; the Scrum Bag at Stage 5 owns the dispatch assignment and Stage-7 UAT verifies the git history shows two separate Dev commits (or two separate commit authors within a squash) for the producer and validator halves.

## Consequences

**Positive**:
- Plugin maintainer gets a single-command empirical regression probe in < 30 min wall-clock per run.
- Hard caps on cost ($3/run), wall-clock (30 min), and dispatch count fail loudly on the most expensive regression classes.
- 2σ advisory band on token drift and skill-load drift surfaces silent regressions without spurious noise during the first month.
- Telemetry-hook reuse means `delivery-team/hooks/telemetry.py` and `telemetry_run_summary.py` get exercised on every smoke run — implicit integration coverage for those hooks at zero additional cost.
- Producer-validator split preserves the past-wave practice that surfaced 5 meta-test defects in earlier initiatives.
- `lib/` boundary is preserved for future reuse by `hardware-team` and `mtg-commander` smoke tests (out of scope here, but the factoring does not foreclose it).

**Negative**:
- 5 samples is a small n; the stddev underestimates true variance. Mitigated by 2σ-then-1.5σ tightening policy after 20+ production runs (NFR-Reproducibility).
- `--init-baseline` envelope is $15 (5 × $3 cap) — acknowledged budget item.
- Subprocess approach loses fidelity with any future in-process plugin-loading mechanism. Acceptable trade-off: the goal is parity with the maintainer's real CLI experience.
- Local-only means each maintainer must run the probe before merging. There is no automated pre-merge gate. Mitigation: documented in `delivery-team/tests/smoke/README.md` and the root `Makefile` `smoke` target.
- Stop hook could block the pipeline mid-run; runner captures stderr so the maintainer can see the failure. The prompt (W6-6) explicitly requests a minimal retrospective so the Stop hook has something to consume.

**Neutral**:
- The permanent architecture doc (`delivery-team/architecture/smoke-test-architecture.md`) carries the full Mermaid diagram, component map, metrics schema, baseline schema, and detector logic. This ADR carries the decision; the architecture doc carries the implementation contract. Future changes to the schemas or the detector logic update the architecture doc; only changes to the four core decisions above warrant a new ADR.

## Alternatives Considered

### (a) Claude SDK in-process invocation

**Rejected.** The Anthropic SDK does not currently expose a plugin-loading mechanism — plugins live in the `claude` CLI surface, not in the SDK. Invoking the SDK in-process would test a different code path than the one shipped to maintainers and would not exercise `--plugin-dir`, hook firing, or the Stop-hook contract. The whole point of the probe is parity with real maintainer experience; SDK invocation breaks that parity at the first step.

### (b) CI workflow invoking `claude`

**Rejected — BANNED by memory directive.** Per `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md` (memory: `feedback_claude_code_local_only`), CI runners have no `claude` binary and no credentials. A `.github/workflows/smoke-*.yml` would silently fail or never run. Rejected without further analysis — the directive is binding and predates this initiative.

### (c) Hand-run pipeline with manual telemetry diff

**Rejected.** Status quo. The whole reason this initiative exists is that hand-running and eyeballing telemetry did not catch token-economy or model-routing drift in waves 1–5. Automating the diff is the value proposition.

### (d) 10-sample baseline instead of 5

**Rejected (for now).** 10 samples doubles the baseline-capture envelope to $30 and the wall-clock to ~5 hours sequential. The PO accepted a 5-sample baseline with a 2σ-then-1.5σ tightening policy in NFR-Reproducibility. After 20 accumulated production runs, a follow-up BACKLOG can re-baseline at higher n if the variance budget proves insufficient.

### (e) Pure stream-json parser; ignore existing telemetry hooks

**Rejected — violates BC-02 (binding).** The reuse mandate requires the aggregator to consume `telemetry.py` and `telemetry_run_summary.py` outputs directly. Re-implementing telemetry parsing in the runner would create a second source of truth for skill-load and prose-token data and would silently miss the placeholder-row semantics that `telemetry.py` already handles per W3-18 / ADR-tk0e-001.

## Related

- `delivery-team/architecture/smoke-test-architecture.md` — full architecture (Mermaid, schemas, detector logic, decision log)
- `.delivery/artifacts/02-refine/po/prd.md` — PRD for BACKLOG-106
- `.delivery/backlog/BACKLOG-106-delivery-team-smoke-test.md` — initiative backlog with WI breakdown
- `.delivery/artifacts/02-refine/po/constraints.yml` — binding constraints (BC-01 through BC-05)
- `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md` — local-only memory directive
- `delivery-team/hooks/telemetry.py` — PreToolUse skill-load hook (reuse mandate target)
- `delivery-team/hooks/telemetry_run_summary.py` — per-run summary emitter (reuse mandate target)
- `governance/skill-budgets.json` — baseline JSON shape pattern
- `scripts/check_skill_budgets.py` — exit-code convention reference

---

*— Celebrimbor, Stage 4 Architect, run-2026-05-13-tk5.*
