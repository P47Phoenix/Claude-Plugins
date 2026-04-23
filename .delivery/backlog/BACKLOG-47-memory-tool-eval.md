# BACKLOG-47-memory-tool-eval: Evaluate client-side `memory` tool adoption

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- PRD REQ-07 AC-07.2 (`.delivery/artifacts/02-refine/po/prd.md` §4)
- PRD §1 Non-Goals (memory tool is NEW, not migration)
- Anthropic 4.7 release notes (F-19 — client-side `memory` tool)

## Context

Claude Opus 4.7 shipped a client-side `memory` tool that lets agents persist and retrieve structured memory across turns without re-sending it in the system prompt. This repo already has its own self-learning memory system under `.delivery/memory/` with tiered chunked retrieval, owned by the `delivery-flow` skill.

REQ-07 AC-07.2 defers the Anthropic `memory`-tool evaluation to a NEW-BACKLOG item. The scope-discipline argument is identical to `task_budget`: adoption requires SDK wiring and would non-trivially restructure the `.delivery/memory/` system, which is orthogonal to any 4.6 → 4.7 migration concern.

## Proposed scope

- Inventory the existing `.delivery/memory/` architecture (tiered chunked retrieval, topic/stage partitioning) and identify what the Anthropic `memory` tool would and would not replace.
- Compare cost/latency profiles: today's in-prompt memory injection vs. client-side `memory` tool round-trips.
- Decide between three options:
  1. **Replace** `.delivery/memory/` injection with the `memory` tool.
  2. **Hybrid** — keep high-signal chunks in the system prompt, offload long-tail retrievals to the `memory` tool.
  3. **Reject** — our self-managed system outperforms for our scale.
- If ADOPT, produce an ADR + a migration plan that preserves existing memory content (no data loss).

## Out of scope for this item

- Any changes to the current `.delivery/memory/` directory layout prior to a decision (status quo is fine).
- `task_budget` — tracked separately in BACKLOG-47-task-budget-eval.
- Cross-repo memory sharing (a separate, larger question).

## Success criteria

- Evaluation memo at `.delivery/research/memory-tool-eval.md` covering scope, options, cost/latency comparison, recommendation.
- ADR logged under `.delivery/artifacts/<impl-run>/adrs/` if ADOPT or HYBRID is chosen.
- Existing memory entries are preserved (lossless) in any migration path.
- REQ-07 AC-07.2 literal-phrase preservation still holds — this remains a NEW feature, not absorbed into migration work.

## Priority & effort (rough)

- Priority: medium
- T-shirt: L (evaluation + potential migration of a sizeable memory corpus)
- Depends on: BACKLOG-47-sdk-wiring-routing-via-claude-api (the SDK pathway must exist before the `memory` tool can be exercised).
