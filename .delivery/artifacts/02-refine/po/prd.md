# PRD: Paradigm-as-Skill Restructure (BACKLOG-005, Roadmap Steps 2+3)

**Pipeline:** run-2026-04-10-d5e2 (FEATURE XL)
**PO:** Gandalf
**Date:** 2026-04-10
**Traced to:** `.delivery/artifacts/08-transform/roadmap.md` STEP-02, STEP-03

---

## Problem Statement

The architect skill bundles all decomposition paradigms into a single 615-line SKILL.md with 27 reference files. When the orchestrator loads the architect for a volatility decomposition, the entire skill loads -- including DDD, event-storming, game architecture, compliance, and privacy references. This wastes context tokens, violates the "context isolation: sub-agents receive only role-scoped references" invariant at the paradigm level, and makes paradigm extension require modifying a monolith.

## Success Criteria (from Roadmap)

- **STEP-02**: Volatility paradigm skill exists as a separate skill; independently loadable; context isolation measurable by prompt token count delta.
- **STEP-03**: DDD paradigm skill exists; paradigm registry proven for multi-paradigm selection; adding a third paradigm requires only a new skill, not router changes.
- Subsystem change per step stays under 20% (roadmap ceiling is 30%; our target is tighter).
- All 7 AS-IS invariants preserved.

---

## Functional Requirements

### FR-1: Volatility Paradigm Skill (STEP-02)

Create `delivery-team/skills/architect/paradigms/volatility/` containing:
- `SKILL.md` -- paradigm-specific instructions for volatility-based decomposition (IDesign/Lowy method). Content extracted from existing `references/volatility-decomposition.md` plus the section-0 golden rule.
- `references/volatility-decomposition.md` -- the full reference, moved from `architect/references/`.
- `references/domain-discovery-volatility.md` -- volatility-specific interview questions extracted from `domain-discovery.md`.

The paradigm skill SKILL.md must declare its scope, loading trigger, and output contract compatible with the architect output contract.

### FR-2: DDD Paradigm Skill (STEP-03)

Create `delivery-team/skills/architect/paradigms/ddd/` containing:
- `SKILL.md` -- paradigm-specific instructions for strategic DDD decomposition (subdomain classification, bounded context discovery, context mapping). Content extracted from existing `references/strategic-ddd.md`.
- `references/strategic-ddd.md` -- the full reference, moved from `architect/references/`.
- `references/domain-discovery-ddd.md` -- DDD-specific interview questions extracted from `domain-discovery.md`.

### FR-3: Architect SKILL.md Paradigm Router

Update `delivery-team/skills/architect/SKILL.md` to act as a paradigm router:
1. Detect paradigm from `.delivery/config.yml` field `architecture.decomposition` (existing config key -- no new keys).
2. If `decomposition: volatility` -- delegate to `paradigms/volatility/SKILL.md`.
3. If `decomposition: ddd` -- delegate to `paradigms/ddd/SKILL.md`.
4. If `decomposition: auto` or unset -- use existing decision matrix logic to select paradigm, then delegate.
5. Non-decomposition task types (design, review, document, evaluate, etc.) continue to route through existing architect logic unchanged.
6. The decomposition strategy routing table in SKILL.md updates to point at paradigm sub-skills for `volatility` and `ddd` entries.

### FR-4: Design Sprint Sub-Workflow Reference

Create `delivery-team/skills/delivery-flow/references/design-sprint.md` documenting:
- The PO+Architect Design Sprint sub-workflow pattern.
- Flow: PO defines the problem scope and constraints --> Architect detects paradigm --> paradigm skill produces decomposition --> architecture board review (if configured) --> handoff to Plan stage.
- When it triggers: Design and Architect stages of delivery-flow when project type involves decomposition.
- Integration points with existing pipeline stages.

### FR-5: Redirect Stubs for Original References

Replace original `architect/references/volatility-decomposition.md` and `architect/references/strategic-ddd.md` with redirect stubs:
- Each stub contains a single line: "This content has moved to `paradigms/<paradigm>/references/<filename>`. Load the paradigm skill directly."
- Purpose: avoid breaking installed caches that reference the original paths. Stubs remain until the next cache refresh cycle.

### FR-6: Dogfood Validation

Run a volatility decomposition through the new paradigm skill structure:
- Invoke the architect skill with `decomposition: volatility` config.
- Verify the paradigm skill loads in isolation (only volatility references in prompt).
- Verify the decomposition output conforms to the architect output contract.
- Document token count: paradigm skill prompt vs. monolithic architect prompt.

### FR-7: AS-IS Invariant Verification

After restructure, verify all 7 invariants from `as-is-constraints.yml` still hold:
1. Two-channel communication preserved (orchestrator signals separate from domain artifacts).
2. Context isolation preserved (paradigm sub-agents receive only paradigm-scoped references).
3. DoD validation multi-validator pattern unchanged.
4. Orchestrator does not produce domain artifacts itself.
5. Self-correction loops capped at 3 rounds.
6. Retrospective mandatory at Stop.
7. Light stages reduce depth but never skip.

---

## Non-Functional Requirements

- **No new config keys**: `architecture.decomposition` already exists (values: auto, volatility, ddd, team-topology, event-storming, business-capability). No schema version bump needed.
- **Backwards compatibility**: Existing pipelines that do not reference paradigm sub-skills continue to work. The architect SKILL.md falls back to existing inline logic if paradigm sub-skill directory does not exist.
- **Context isolation measurable**: Paradigm skill prompt must be measurably smaller than full architect prompt. Target: paradigm skill loads fewer than 5 reference files vs. the monolithic 27.
- **Subsystem change ceiling**: STEP-02 touches 2 subsystems (11% of 19). STEP-03 touches 3 subsystems (16% of 19). Both under the 20% target and well under the 30% roadmap ceiling.
- **Independently shippable**: STEP-02 ships without STEP-03. If only volatility lands, the system is strictly better. DDD extraction is additive.

---

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Broken paradigm selection blocks Architect stage | High | Low | Registry defaults to existing inline logic until new skill proves over 3 runs |
| Cross-paradigm contamination (volatility language in DDD refs) | Medium | Medium | Forbidden-vocabulary check per paradigm skill at DoD |
| Installed cache references stale paths | Low | Medium | Redirect stubs preserve old paths; removal deferred to cache refresh |

---

## Out of Scope

- Functional decomposition, event-storming paradigm extraction (no deep reference exists yet)
- Game architecture paradigm restructuring
- New paradigm authoring (reorganize only)
- Delivery-flow orchestrator protocol changes
- Config schema version bump
