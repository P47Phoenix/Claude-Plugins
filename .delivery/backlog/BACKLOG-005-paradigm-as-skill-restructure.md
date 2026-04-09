# BACKLOG-005: Paradigm-as-skill restructure + PO/Architect Design Sprint sub-workflow

**Status**: Open (FEATURE-scale — likely warrants its own delivery-flow run)
**Priority**: P2 (structural; high leverage but depends on BACKLOG-004 correctness fixes landing first)
**Size**: L (multi-skill restructure + new sub-workflow + pilot)
**Created**: 2026-04-08
**Owner**: PO → Architect (structural option selection) → delivery-flow (sub-workflow wiring)

## Source
- **PO ask (verbatim, 2026-04-08)**: "Each one of these paradigms might be its own skill with many markdown files depending on the review or design step we are doing. Could even be its own workflow with the PO and architecture team working together to come up with a design."
- **Architect examination (in progress)**: `.delivery/artifacts/research/architect-examine-decomposition-gaps.md` *(placeholder — link when written)*

## Problem Statement
> "Each one of these paradigms might be its own skill with many markdown files depending on the review or design step we are doing. Could even be its own workflow with the PO and architecture team working together to come up with a design." — PO

Today the Architect skill bundles all decomposition paradigms (volatility, DDD, functional, event-storming, etc.) into a single skill with 4 strategies. This causes:
1. **Shallow per-paradigm guidance** — no paradigm gets the staged, step-by-step treatment it deserves
2. **No design-sprint workflow** — there is no structured PO+Architect collaboration loop for picking and applying a decomposition paradigm
3. **Hard to extend** — adding a new paradigm means bloating the Architect skill further

## Proposed Direction (high level — Architect is examining structural options)
- **Architect skill becomes a router**: detects which paradigm is appropriate and delegates to a paradigm skill
- **Each paradigm as its own skill** under `delivery-team/skills/` (or a paradigm sub-namespace) with staged markdown files (one file per design step: intake, identify axes, candidate decomposition, critique, finalize)
- **Pilot with volatility** (highest PO pain point from BACKLOG-004)
- **New Design Sprint sub-workflow**: PO + Architect (+ paradigm skill) collaborate in a defined loop — intake → paradigm selection → staged decomposition → board review (BACKLOG-003) → handoff to Plan
- Defer concrete skill boundaries, file inventory, and workflow stages to Architect examination output
- **This item is FEATURE-scale** and should be executed as its own delivery-flow run, not as a single PR

## Research lineage
- **Model-First + MAR synthesis applied to architecture**: the PO+Architect Design Sprint sub-workflow is the synthesis of both research papers applied to architecture design. Specifically:
  1. **Model-First** → Design Sprint builds an explicit decomposition **model** first (entities = subsystems, state = volatility classification, actions = interactions, constraints = golden rule + BACKLOG-004 guardrails expressed as `constraints.yml`-shaped entries from BACKLOG-001/004).
  2. **MAR** → Design Sprint routes model iterations through the BACKLOG-003 architecture board (multi-persona reviewers + Architect judge), with iteration-2 preserving persona diversity per MAR's novelty.
  3. **Paradigm-as-skill** is the vehicle that makes the model-first + multi-persona-reflection workflow tractable per paradigm (volatility gets its own staged model template; DDD gets its own).
- **Consumes (does not reinvent)**: BACKLOG-001's constraints primitive, BACKLOG-004's guardrails/golden rule, BACKLOG-003's board pattern. The Design Sprint sub-workflow is orchestration over three primitives, not new primitive invention.

## Success Criteria (concrete)
1. Architect skill acts as a router: examining the Architect skill's entry logic shows paradigm detection and delegation (not inline paradigm logic)
2. **Volatility paradigm skill exists** as a separate skill with staged markdown files (minimum: intake, axes, candidates, critique, finalize)
3. **Dogfood run**: one real pipeline uses the new volatility paradigm skill end-to-end and produces a decomposition artifact that (a) passes BACKLOG-004 guardrails and (b) cites the golden rule
4. **Design Sprint sub-workflow** is documented and executable — a config flag or skill invocation routes Design+Architect stages through the PO/Architect collaborative loop
5. Adding a second paradigm (e.g., DDD) later requires only a new skill, not changes to the router or workflow
6. **Model-First evidence**: the volatility paradigm skill's staged markdown includes a "model" step that emits structured entities/state/actions/constraints (reusing BACKLOG-001 schema where applicable), not prose-only guidance
7. **MAR evidence**: the Design Sprint loop routes decomposition iterations through the BACKLOG-003 architecture board with declared per-seat personas and a judge synthesis step — no bespoke review loop is invented

## Size & Complexity
- **L — FEATURE-scale.** Multi-skill restructure + new sub-workflow + pilot. This item should be **kicked off as its own FEATURE (or SPIKE-then-FEATURE) delivery-flow run** once BACKLOG-004 has landed and BACKLOG-003 is at least designed.

## Dependencies
- **Depends on BACKLOG-001 + BACKLOG-004** — shared `constraints.yml`-shaped primitive must exist; content corrections must land first so the paradigm skill is built on correct guidance
- **Depends on BACKLOG-003** — Design Sprint sub-workflow consumes the architecture board pattern (which also carries the MAR persona-swap behavior absorbed from BACKLOG-002); do not reinvent review
- **Depends on Architect examination** — structural option selection (how many skills, boundaries, sub-workflow shape) is the Architect's call

## Links
- Architect examination: `.delivery/artifacts/research/architect-examine-decomposition-gaps.md` *(placeholder)*
- Current Architect skill: `delivery-team/skills/architect/` (11 roles, 4 decomposition strategies)
- Related: BACKLOG-003 (board review), BACKLOG-004 (guidance depth)
