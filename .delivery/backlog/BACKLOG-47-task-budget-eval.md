# BACKLOG-47-task-budget-eval: Evaluate `task_budget` (beta) adoption across agentic flows

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- PRD REQ-07 AC-07.1 (`.delivery/artifacts/02-refine/po/prd.md` §4)
- PRD §1 Non-Goals (task_budget is NEW, not migration)
- Anthropic 4.7 release notes (F-18 — `task_budget` beta parameter on the Messages API)

## Context

Claude Opus 4.7 introduced a `task_budget` beta parameter that lets callers cap per-request token / tool-use budgets on the Messages API. The 4.6 → 4.7 migration engagement (run-2026-04-22-4x7e) deliberately scoped this out: REQ-07 AC-07.1 requires the roadmap to carry the literal phrase "task_budget and memory tool adoption are NEW features, not migration work" and to log each as a separate NEW-BACKLOG candidate rather than fold them into migration WIs.

The motivation is scope discipline: any `task_budget` adoption requires SDK wiring (this repo has zero `anthropic.messages.create` call sites today — see ADR-004), a budget-sizing exercise, and telemetry to evaluate effectiveness. None of that is migration work.

## Proposed scope

- Investigate which agentic flows in this repo would meaningfully benefit from per-request budgets (candidates: `prd-quality-gate-flow`, `agentic-flow-builder`, `delivery-flow` adversarial loops, `mtg-commander` Challenger agents).
- Define a budget-sizing methodology: baseline current token consumption per invocation type, then choose a ceiling that preserves ≥95th-percentile success runs.
- Prototype wiring in ONE flow only (likely `prd-quality-gate-flow` since it already has deterministic gate mechanics) and measure.
- Decide adoption posture: always-on, opt-in via config, or reject.
- Coordinate with BACKLOG-47-sdk-wiring-routing-via-claude-api — `task_budget` is only reachable once the SDK adoption pathway is established.

## Out of scope for this item

- Wiring the Anthropic SDK into any flow. That is a prerequisite tracked separately (see Depends on).
- The `memory` tool — tracked separately in BACKLOG-47-memory-tool-eval.
- Budget enforcement inside the Claude Code harness itself (that is harness-team territory, not skill/plugin work).

## Success criteria

- A one-page evaluation memo produced under `.delivery/research/` covering: which flows benefit, budget sizes, prototype results.
- If ADOPT: an ADR + a wiring PR for at least one flow, with dogfood evidence of budget enforcement.
- If REJECT or DEFER: the memo explains why and what would change the calculus.
- REQ-07 AC-07.1 literal-phrase check is preserved — this item is **not** a migration lift-over.

## Priority & effort (rough)

- Priority: medium
- T-shirt: M (spike + measurement + decision memo)
- Depends on: BACKLOG-47-sdk-wiring-routing-via-claude-api (must land first); Anthropic `task_budget` beta reaching GA would elevate priority.
