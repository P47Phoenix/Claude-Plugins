# ADR-004 — Prompt-Caching Adoption Scope: Out-of-Engagement (Latent Until SDK Wiring)

**Status:** Accepted
**Date:** 2026-04-20
**Architect:** Celebrimbor
**Engagement:** Opus 4.6 → 4.7 Transformation Plan
**Related:** PRD F-16, F-17, F-20; Galadriel DX pillar P-6; Open Question 8; REQ-07
**Supersedes:** none
**Superseded-by:** none

---

## Context

Prompt-caching specs on Opus 4.7 are unchanged from 4.6 (F-16): 4096-token minimum cacheable prompt, 4 cache_control breakpoints max, 20-block lookback window, 5-minute default TTL with 1-hour opt-in, identical pricing ($6.25 / MTok for 5-min cache writes, $10 / MTok for 1-hour, $0.50 / MTok hits). Switching between adaptive and enabled/disabled thinking modes breaks message-level cache breakpoints (F-17).

PRD §3.1 confirms zero Anthropic SDK imports in this repo. No `cache_control`, no `anthropic.messages.create` call sites. Prompt caching is a runtime concept driven by the SDK caller; it has no surface in SKILL.md prose because Claude Code (the harness running these skills) owns caching behaviour, not the skill author.

Galadriel Pattern P-6 explicitly flags this as a **latent** pillar: "Currently N/A (no SDK call sites exist). If introduced: grep for `anthropic.messages.create` and confirm every call site has a neighbouring comment naming its caching strategy."

## Decision

**Prompt-caching adoption is OUT OF SCOPE for this engagement.** No SKILL.md edits, no pattern-library entries, no CI guard. The topic is deferred to the ambient `claude-api` skill via the SDK-adoption pathway (PRD Open Question 8).

Specifically:

- **No SKILL.md gains prompt-caching guidance.** Caching is a transport-layer concern; it does not belong in skill instruction bodies under Galadriel P-3 (fail-soft) or P-6 (latent until SDK wiring).
- **No cache_control examples are added to the `prompt-engineer/` pattern library.** The pattern library is for model-facing prompt authoring, not SDK API surface.
- **A single sentence is added to the Wave 4 NEW-BACKLOG registration (REQ-07)** noting that any future SDK wiring must route through `claude-api` skill AND must carry a "caching strategy" comment at each call site — which operationalises Galadriel P-6 for whoever picks up the backlog.

## Consequences

- **Positive:** Zero migration-time cost for a concern that has no current surface. Engagement stays inside its "plan-only, no new features" boundary (PRD Non-Goals + Constraint 1).
- **Positive:** Galadriel P-6 is preserved as a *future observable* — when SDK wiring lands, the `claude-api` skill activation triggers the caching-strategy audit.
- **Positive:** PRD F-20 (pricing unchanged) means no cost-narrative edits are required in any skill doc, consistent with "no change" as the 4.7 migration answer for this topic.
- **Negative:** If a contributor ever adds `anthropic.messages.create` to this repo without routing through `claude-api`, they will inherit no caching guidance. Mitigation: the P-6 CI guard (grep for SDK imports with no neighbouring caching comment) is logged as a new-backlog candidate; ADR-006's `last_audited` convention provides the file-level signal.
- **Negative:** F-17's "switching thinking modes breaks cache breakpoints" guidance is documented nowhere in this repo. Acceptable: no repo code switches thinking modes, and if it ever does, that change will land with the SDK wiring and can absorb the guidance at that time.

## Alternatives Considered

- **Document caching semantics in `prompt-engineer/SKILL.md`.** Rejected: conflates prompt authoring (a model-facing skill) with SDK usage (a transport concern). `prompt-engineer/` targets authors who write prompts, not engineers who integrate the API. Galadriel P-3 / P-6 separation preserved.
- **Pre-emptively add a `cache-control-patterns.md` reference doc.** Rejected: zero call sites → documentation for hypothetical consumers. Violates the "don't write patterns without a caller" principle implicit in the pattern-library design (ADR-005).
- **Add cache-control patterns to the Galadriel pattern library under a "Future: SDK-era" heading.** Rejected on the same "no caller" basis. The `claude-api` skill already owns SDK patterns per CLAUDE.md; duplicating here would fragment ownership.

## Implementation Notes

- The Wave 4 REQ-07 new-backlog registration includes a line: *"Future SDK wiring: every `anthropic.messages.create` call site must carry a caching-strategy comment naming which breakpoints are used and why (Galadriel P-6). Route implementation through the `claude-api` skill per CLAUDE.md."*
- If a future backlog item adopts `task_budget` (F-18) or the memory tool (F-19), the same backlog item picks up caching-strategy audit as a neighbouring requirement — the three are naturally co-resident at the SDK layer.
- This ADR will be revisited if/when Open Question 8's "SDK adoption pathway" is exercised.

---

*"A forge uses heat in ways its patrons do not see. We do not describe the bellows to a buyer of rings. The caching is the harness's breath, not the ring's song."*

— Celebrimbor
