# BACKLOG-47-sdk-wiring-routing-via-claude-api: Anthropic SDK adoption pathway via `claude-api` skill

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- ADR-004 — Prompt-Caching Adoption Scope: Out-of-Engagement (`.delivery/artifacts/04-architect/adrs/ADR-004-4-7-prompt-caching-scope.md`)
- PRD Open Question 8 (`.delivery/artifacts/02-refine/po/prd.md` §8)
- CLAUDE.md — "ambient `claude-api` skill" convention for Anthropic SDK work

## Context

This repo has zero Anthropic SDK imports today (PRD §3.1 confirms, ADR-004 relies on that fact to defer prompt-caching adoption). PRD Open Question 8 records the PO's guidance that *if* any plugin later wires the Anthropic SDK directly — the near-term candidates are `prd-quality-gate-flow` and `agentic-flow-builder`, which run deterministic agentic flows — that work must route through the ambient `claude-api` skill per CLAUDE.md convention.

ADR-004 locks three features behind this pathway: prompt caching, `cache_control` usage, and (by downstream dependency) `task_budget` and `memory` tool adoption. Establishing the pathway is therefore a prerequisite to unlocking three other backlog items (prompt-caching, task_budget, memory tool).

This item is the meta-decision: *does* any plugin wire the SDK, and if so, what is the shared pattern for call-site hygiene (caching strategy comments, model ID sourcing, error handling)?

## Proposed scope

- Identify plugins whose value would measurably increase with direct SDK access (`prd-quality-gate-flow` and `agentic-flow-builder` are the leading candidates; evaluate others).
- Produce a reference implementation in one plugin that shows: (a) `claude-api` skill invocation pattern, (b) mandatory per-call-site caching-strategy comment (per ADR-004 Galadriel P-6), (c) model ID resolution through a shared config rather than hardcoded strings (per ADR-002 model-ID reference strategy).
- Publish a "SDK wiring checklist" under `delivery-flow/references/` or `prompt-engineer/references/` so future plugins follow the same pattern.
- Update CLAUDE.md if new invariants emerge.

## Out of scope for this item

- Prompt-caching adoption itself (ADR-004 will be revisited once pathway exists).
- `task_budget` and `memory` tool (tracked separately).
- Migrating `mtg-commander`, `research-agent`, or other non-deterministic flows that are better served by Claude Code's harness-driven tool calls.

## Success criteria

- At least one plugin successfully uses the Anthropic SDK through the `claude-api` skill in a dogfood run, with call-site caching-strategy comments present and reviewable.
- The SDK wiring checklist reference is in the repo and linked from CLAUDE.md.
- All call sites use centralised model ID resolution (no hardcoded `claude-opus-4-7` strings in plugin code).
- Downstream backlog items (BACKLOG-47-task-budget-eval, BACKLOG-47-memory-tool-eval, any future prompt-caching ADR) can cite this pathway as "available."

## Priority & effort (rough)

- Priority: medium (enabling work — low user-facing value on its own, but three other backlog items depend on it).
- T-shirt: M
- Depends on: nothing repo-side; indirectly depends on Anthropic SDK stability.
