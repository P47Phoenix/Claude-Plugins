# ADR-001: Paradigm Skills as Internal Sub-Skills

**Status:** Proposed
**Date:** 2026-04-10
**Deciders:** Celebrimbor (Architect), Galadriel (UX, non-binding recommendation), Gandalf (PO)
**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)
**Traced to:** FR-1, FR-2, FR-3; Galadriel Q1

---

## Context

The architect skill must be restructured so that decomposition paradigms (volatility, DDD, and future paradigms) live in their own SKILL.md files with isolated references. The question is how these paradigm skills relate to the plugin ecosystem: are they registered as top-level skills in `plugin.json`, or are they internal sub-skills discovered only by the architect's router?

The delivery-flow orchestrator currently invokes `architect` as a single skill. Changing this contract would ripple into orchestrator SKILL.md, pipeline stage definitions, and every config that references architect task types. Galadriel's Stage 3 design recommended internal registration; this ADR formalises the decision.

---

## Decision

Paradigm skills are **internal sub-skills** of the architect skill. They are:

- Discovered by the architect SKILL.md router via the `paradigms/` directory convention
- NOT registered in `plugin.json`
- NOT directly invocable by the orchestrator or other skills
- Loaded by the architect spawning an `Agent` with the paradigm SKILL.md

The architect skill remains the sole entry point for all architecture tasks, including decomposition.

---

## Consequences

### What becomes easier

- **Adding new paradigms** requires only a new `paradigms/<name>/` directory with SKILL.md and references. No `plugin.json` edits, no orchestrator changes, no delivery-flow updates.
- **Context isolation** improves without ecosystem complexity -- paradigm sub-agents load only their own references plus declared shared refs.
- **Backwards compatibility** is automatic -- the orchestrator's `architect` invocation is unchanged. Existing pipelines work without modification.
- **Removal or refactoring** of a paradigm is a local change within `architect/paradigms/` with no external contracts to honour.

### What becomes harder

- **Direct paradigm invocation** is not possible -- a user cannot say "load the volatility skill" from the top level. They must invoke architect, which routes internally. This is intentional: paradigms are implementation details, not user-facing capabilities.
- **Paradigm discoverability** requires reading the architect SKILL.md or config documentation. Paradigms do not appear in the marketplace skill list. Acceptable because paradigm selection is a config value (`architecture.decomposition`), not a skill invocation.

---

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **(a) Registered in plugin.json** (full top-level skills) | Direct invocation; visible in marketplace | Creates public API surface; orchestrator must learn per-paradigm skill names; breaking change to delivery-flow; paradigm refactoring becomes a public contract change | Ecosystem complexity disproportionate to the benefit; violates orchestrator delegation invariant |
| **(b) Inline sections in monolithic SKILL.md** (status quo) | No migration; no new files | Context isolation violation; monolith grows with each paradigm; 29 refs loaded regardless of task; violates the PRD success criteria | The problem we are solving |
| **(c) Separate standalone plugins per paradigm** | Maximum isolation; independent versioning | Extreme fragmentation; each paradigm needs its own marketplace entry, LICENSE, hooks; shared references duplicated across plugins; maintenance cost scales linearly with paradigm count | Over-engineering; paradigms share too much infrastructure (output contracts, domain discovery, shared refs) to justify full plugin separation |

---

## References

- Galadriel, Information Architecture (Stage 3): Q1 non-binding recommendation
- `as-is-constraints.yml`: invariant "Context isolation: sub-agents receive only role-scoped references"
- `constraints.yml` (Refine): invariant "Paradigm sub-skill loads ONLY its own references"
- PRD FR-3: architect SKILL.md paradigm router
