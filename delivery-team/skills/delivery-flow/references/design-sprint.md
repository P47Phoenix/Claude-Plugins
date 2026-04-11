# Design Sprint — PO + Architect Paired Sub-Workflow

## Purpose

The Design Sprint is a paired PO + Architect sub-workflow for making decomposition decisions during Stage 4. It structures the collaboration between the PO (who owns the problem scope and constraints) and the Architect (who owns paradigm selection and structural decomposition) so that decomposition is goal-driven, not technology-driven. The sprint produces the same Stage 4 artifacts as a regular architect invocation but routes through paradigm-specific sub-skills for context isolation.

## When It Triggers

A Design Sprint triggers during **Stage 4 Architect** when the project involves decomposition work:

- New system design (GREENFIELD, GAME_DEV)
- System migration or restructure (FEATURE with `transformation-planning` signals)
- Modularization or service boundary definition (`decompose` task type)
- Any invocation where `architecture.decomposition` is configured or the task signals decomposition-heavy work

**Detection signals:** The orchestrator looks for `decompose` or `design` task types, `transformation-planning` signals, or explicit decomposition keywords in the pipeline context. If none are present, a regular architect invocation runs instead.

## Flow

1. **PO defines goal and constraints** — The PO provides the problem scope from the PRD (`.delivery/artifacts/02-refine/po/prd.md`) and project constraints (`.delivery/artifacts/02-refine/po/constraints.yml`). This frames what the decomposition must achieve and what boundaries it must respect.

2. **Architect router selects paradigm** — The architect SKILL.md detection priority chain (ADR-002) determines which paradigm to use:
   - (1) Explicit user intent in the prompt
   - (2) `architecture.decomposition` from `.delivery/config.yml`
   - (3) Decision matrix fallback based on domain characteristics

3. **Paradigm skill executes decomposition** — The router dispatches an `Agent` with the selected paradigm's `SKILL.md` and only its declared `shared_refs`. The paradigm sub-agent produces the decomposition artifacts in isolation — no cross-paradigm context bleeding.

4. **Output lands at standard artifact path** — Decomposition output writes to `.delivery/artifacts/04-architect/solution/architecture.md` and any ADRs to `.delivery/artifacts/04-architect/adrs/`. The artifact structure is identical to a regular architect invocation.

5. **Architecture Board Review (if enabled)** — If `architecture_board.enabled` is true in config, the board review runs against the decomposition output per `team-patterns.md` Pattern 3b. Personas review in parallel, judge synthesizes, self-correction loops apply.

6. **DoD validates** — Standard Stage 4 DoD validators (Architect, QA, DevOps, Security) validate the output. The decomposition must meet the same quality bar as any architecture artifact.

## Roles

| Role | Responsibility |
|------|---------------|
| **Product Owner** | Defines problem scope, goal, and constraints from PRD + constraints.yml. Owns the "what" and "why" of decomposition. Does not make structural decisions. |
| **Architect (router)** | Selects paradigm via ADR-002 priority chain. Dispatches paradigm sub-skill. Owns the "how" of decomposition routing. |
| **Paradigm skill** | Executes decomposition within its paradigm's methodology. Produces architecture artifacts. Receives only paradigm-scoped references. |

## Output Artifacts

All outputs land at the standard Stage 4 paths — no new artifact locations:

- `.delivery/artifacts/04-architect/solution/architecture.md` — primary architecture document
- `.delivery/artifacts/04-architect/adrs/ADR-*.md` — architecture decision records
- `.delivery/artifacts/04-architect/board/` — architecture board reviews (if board enabled)
- Paradigm-specific decomposition detail is embedded within `architecture.md`, not in separate files

## Invocation

The delivery-flow orchestrator triggers a Design Sprint (rather than a regular architect invocation) when **any** of these conditions hold during Stage 4:

1. The task type resolved to `decompose` or `design` with decomposition signals
2. `architecture.decomposition` is set in config (not `auto`)
3. The project type is GREENFIELD or GAME_DEV (new system implies decomposition)
4. The PRD or pipeline context contains `transformation-planning` keywords

When none of these conditions hold, the orchestrator invokes the architect skill normally — no paradigm routing, no Design Sprint. The regular architect handles `review`, `document`, `evaluate`, and all other non-decomposition task types directly.

## Backwards Compatibility

The Design Sprint is **optional** and **additive**:

- If `paradigms/` directory does not exist, the architect falls back to inline decomposition using monolithic references (current behavior preserved)
- If `architecture.decomposition` is unset or `auto` and the decision matrix is used, the result still routes through a paradigm sub-skill if one exists — otherwise falls back to inline
- Existing pipelines that do not configure decomposition continue to work unchanged
- No new config keys are introduced — `architecture.decomposition` already exists in the config schema
- The Design Sprint does not alter Stage 4 entry/exit conditions, DoD validators, or artifact contracts
