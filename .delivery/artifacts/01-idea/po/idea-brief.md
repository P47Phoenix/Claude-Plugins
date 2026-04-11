# Idea Brief: Paradigm-as-Skill Restructure (BACKLOG-005, Roadmap Steps 2+3)

**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)
**PO:** Gandalf
**Date:** 2026-04-10

## The Burden

The architect skill is a monolith. It holds volatility decomposition, DDD strategic design, event storming, functional decomposition, 11 architect roles, transformation-planning, and 27 reference files in a single SKILL.md + references directory. When the orchestrator loads the architect for a volatility decomposition, the entire skill loads -- including DDD, event-storming, game architecture, compliance, and privacy references that have no bearing on the task. This violates context isolation: a volatility architect does not need DDD references in its prompt window.

The roadmap (Phase 3, Celebrimbor) already charted the path. Steps 2+3 are the work.

## The Vision

Paradigm-as-skill. Each decomposition paradigm becomes its own sub-skill under `delivery-team/skills/architect/paradigms/`, with its own SKILL.md and references directory. The architect SKILL.md becomes a router that detects the paradigm from config or task context and delegates to the appropriate paradigm skill. A PO+Architect Design Sprint sub-workflow documents the collaboration loop: PO defines what, Architect routes to paradigm, paradigm skill produces decomposition.

## Scope IN (Roadmap Steps 2+3)

- Extract `volatility-decomposition.md` + related refs into `architect/paradigms/volatility/` with its own SKILL.md
- Extract `strategic-ddd.md` + related refs into `architect/paradigms/ddd/` with its own SKILL.md
- Add paradigm routing logic to architect SKILL.md (detect from `architecture.decomposition` config or task context)
- Create Design Sprint sub-workflow reference in delivery-flow
- Preserve original references as redirect stubs (avoid breaking installed caches)
- Dogfood: run a volatility decomposition through the new structure
- Verify all AS-IS invariants still hold post-restructure

## Scope OUT

- Functional decomposition, event-storming (no existing deep reference to extract -- roadmap defers these)
- Game architecture paradigms (stable, LOW volatility per AS-IS)
- Rewriting transformation-planning references (just shipped in STEP-01)
- Any restructure outside roadmap Steps 2+3
- New paradigm content (reorganize only, do not author new guidance)
- Changes to delivery-flow SKILL.md orchestrator protocol (routing is architect-internal)

## The Stakes

- Roadmap STEP-02 acceptance: volatility paradigm skill exists, independently loadable, context isolation measurable
- Roadmap STEP-03 acceptance: DDD paradigm skill exists, registry proven for multi-paradigm selection
- Architect SKILL.md references paradigm sub-skills instead of monolithic refs
- Paradigm-specific agent loads ONLY its own refs (prompt token count measurable)
- All 7 AS-IS invariants from `as-is-constraints.yml` preserved
- Subsystem change under 20% per roadmap step (STEP-02: 11%, STEP-03: 16%)

## Anti-Scope

- No new paradigm content -- reorganize existing content only
- No deletion of source refs until installed cache validates (keep as redirects)
- No new config keys introduced
- No changes to delivery-flow orchestrator protocol
