# ADR-002 — Model-ID Reference Strategy: Central Alias with Provenance Comments

**Status:** Accepted
**Date:** 2026-04-20
**Architect:** Celebrimbor
**Engagement:** Opus 4.6 → 4.7 Transformation Plan
**Related:** PRD REQ-01 (AC-01.1..5), PRD §3.1 / §3.1.1, Open Questions 2 / 3
**Supersedes:** none
**Superseded-by:** none

---

## Context

Three hard-coded dated Claude model IDs live in `agentic-flow-builder/scripts/agent_registry.py` (MID-01 line 148, MID-02 line 172, MID-03 line 187). Seven family-alias strings live in `prd-quality-gate-flow/stage_definitions.py` (MID-04, seven lines). Zero model IDs appear in any SKILL.md file. Zero Anthropic SDK imports exist anywhere in either plugin (PRD §3.1.1 confirmed against the live repo).

This means the ~10 strings are **registry metadata / routing labels**, not API call targets. No runtime API call in this repo dispatches against any of these strings today. Downstream consumers copying this repo into SDK-calling code inherit the strings as-is — that is the foot-gun.

Two concrete options for post-sweep state:

- **Option A — Direct strings, inline-annotated.** Each occurrence carries a comment citing the canonical source (PRD F-01/F-03/F-04) and the retirement-or-current status.
- **Option B — Central alias module.** One `models.py` per plugin (or repo-wide) exports named constants; all occurrences reference the constant.
- **Option C — Config-driven.** A YAML/JSON config names the IDs; Python modules read it at import time.

## Decision

Adopt **Option A (direct strings with provenance comments)** for this migration, with a **provisional commitment to Option B** if/when SDK wiring is ever added.

Rationale:

1. **Option C (config-driven)** violates the explicit PRD non-goal of "no architecture rewrite / no new schema." It would introduce a runtime dependency on a new config surface for what is currently ~10 strings — disproportionate cost for this engagement's scope.
2. **Option B (central alias module)** is architecturally cleaner but introduces two new Python modules where none are needed today (because nothing calls the API). CLAUDE.md §Key Conventions directs us to route SDK integration through the ambient `claude-api` skill when it happens (Open Question 8) — therefore if/when SDK wiring lands, that work can introduce the alias module as part of its scope, not ours.
3. **Option A** is the minimal-change path that closes the drift-hygiene gap identified in PRD REQ-01 without pre-building abstractions for a caller that does not yet exist.

### Canonical shape (Option A pattern)

For `agentic-flow-builder/scripts/agent_registry.py`:

```python
# Canonical Opus model ID as of 2026-04-20 (PRD F-01, F-03).
# Historical reference: "claude-opus-4-20250514" (retires 2026-06-15 per F-04).
# If this registry is ever wired to anthropic.messages.create, route through the
# claude-api skill per CLAUDE.md convention (PRD Open Question 8).
"config": {"model": "claude-opus-4-7"},
```

For `prd-quality-gate-flow/stage_definitions.py`'s family aliases (`"claude-sonnet"`, `"claude-haiku"`): these are **internal routing labels**, not model IDs. PRD Open Question 3 and UV-01 flag them as "cosmetic until proven otherwise." The sweep either (a) leaves them untouched with a comment marking them as internal labels, or (b) — only if `flow_orchestrator.py` structural AS-IS proves they are never lifted into SDK calls — replaces them with fully-qualified IDs from the canonical set.

## Consequences

- **Positive:** Minimal-change; no new modules, no config-schema churn; preserves PRD Constraint 2 (no architecture rewrite) and Constraint 5 (schema v2.7 frozen).
- **Positive:** Provenance comments make the stale-ID foot-gun visible to marketplace consumers at read-time. A user forking `agent_registry.py` sees the comment before they inherit the stale ID.
- **Positive:** Leaves the door open for Option B when SDK wiring actually happens, with ownership clearly routed through the `claude-api` skill.
- **Negative:** 10 future edits (one per line) instead of one central edit. Acceptable given the surface is small and review cost is low.
- **Negative:** Provenance comments drift over time unless refreshed. Accepted; the `last_audited` convention (ADR-006) provides the signal for when comments need re-reading.

## Alternatives Considered

- **Option B (central alias module):** Rejected for this engagement; will be re-evaluated when SDK wiring is added.
- **Option C (config-driven):** Rejected on scope grounds (violates PRD Constraint 2) and on cost/benefit grounds (runtime config load for ~10 strings is over-engineered).
- **Option D (remove the strings entirely):** Rejected — they are registry metadata that `agent_registry.py` uses at its own abstraction layer, even without SDK calls. Removing them would break the registry's internal contract.

## Implementation Notes

- Canonical IDs for the canonical family (PRD F-01, F-03): `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` (Haiku 4.5's dated ID is still advertised).
- MID-02's `claude-haiku-4-20250514` is a suspected legacy typo — AC-01.3 requires a discovery task before substitution. Likely target: `claude-haiku-4-5-20251001` or `"claude-haiku"` alias, depending on intent.
- The sweep preserves historical commits in `.delivery/` (PRD Constraint 4 — `.delivery/` is not in sweep scope).
- M-01 regex is the post-sweep regression guard; M-02 (widened per challenger loop2 Finding #1) is the re-entry sentinel.

---

*"Name the thing truly, or leave an honest note of where it came from. The Rings that were unmade left no ledger; let us not repeat that mistake with mere strings."*

— Celebrimbor
