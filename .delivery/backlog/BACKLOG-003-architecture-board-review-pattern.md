# BACKLOG-003: Configurable Architecture Board Review pattern (absorbs BACKLOG-002 MAR pilot)

**Status**: Open
**Priority**: P2 (directly extends existing Review Board pattern; unblocks richer decomposition review in BACKLOG-004/005; now also carries MAR pilot)
**Size**: M (new collaboration pattern + config schema + reference doc + pilot run)
**Created**: 2026-04-08
**Revised**: 2026-04-08 — absorbed BACKLOG-002 (MAR iteration-2 persona swap)
**Owner**: PO → Architect (pattern design) → delivery-flow (orchestrator wiring) → Quality (MAR measurement)

## Source
- **PO ask (verbatim, 2026-04-08)**: "Would like an architecture board review. Each review has its own context and perspective. This would be a configurable agentic loop as well."
- **Architect examination (in progress)**: `.delivery/artifacts/research/architect-examine-decomposition-gaps.md` *(placeholder — link when written)*
- **Related existing pattern**: `delivery-team/skills/delivery-flow/` Review Board (current implementation is generic; this specializes it for architecture with per-reviewer context isolation)

## Problem Statement
> "Would like an architecture board review. Each review has its own context and perspective. This would be a configurable agentic loop as well." — PO

Today's Review Board pattern runs reviewers with shared context and a single persona lens. Architecture review needs:
1. **Per-reviewer context isolation** — each board member sees only the slice relevant to their perspective (e.g., security sees threat surface, data sees storage/flow, cost sees infra footprint) so their critique is not diluted by out-of-lane concerns.
2. **Distinct perspective/persona per seat** — configurable N reviewers with declared viewpoints.
3. **Configurable agentic loop** — number of rounds, convergence criteria, and whether the board re-reviews after Architect revision is driven by `.delivery/config.yml`, not hardcoded.

## Proposed Direction (high level — Architect is examining concrete options)
- New collaboration pattern `architecture_board` as a specialization of Review Board
- Board roster declared in `.delivery/config.yml` under `collaboration.architecture_board.seats[]` — each seat has `{name, perspective, context_slice, alias_theme?}`
- Orchestrator spawns one sub-agent per seat with ONLY that seat's context slice (extends existing agent prompt audit hook)
- Agentic loop config: `max_rounds`, `convergence: all_approve | majority | architect_decides`
- Output: one review artifact per seat under `.delivery/artifacts/architecture/board-review/<seat>.md` plus a synthesis by the Architect
- Defer concrete schema/seat catalog to Architect examination output

## Research lineage
- **Multi-Agent Reflexion — MAR (arXiv:2512.20845)**: the architecture board IS MAR instantiated for architecture review. MAR's "multi-persona debator + judge" with distinct reflection personas maps 1:1 onto per-seat context isolation + Architect synthesis. Per-seat `perspective` declarations are MAR personas; the Architect's synthesis step is the MAR judge; `max_rounds` is the Reflexion loop depth.
- **Absorbs BACKLOG-002**: rather than pilot an iteration-2 persona swap on generic self-correction, apply MAR's novelty at its highest-leverage site — architecture review — where persona diversity is load-bearing. The board's iteration-2 re-review (after Architect revision) IS the cross-persona reflection pass.
- **Model-First Reasoning (arXiv:2512.14474)**: board reviewers consume the decomposition **model** (entities, volatility classification, constraints from BACKLOG-001/004) as input context slices. The board reviews a model, not prose — deterministic per-seat rule checks become possible.
- **Pairs with BACKLOG-004**: the volatility golden-rule and implementation-noun guardrails are exactly the rule-checkable invariants a `volatility_reviewer` seat would enforce (see architect examination Option C schema).

## Success Criteria (concrete)
1. A pipeline run configured with N=4 architecture board seats (e.g., Solution, Security, Data, Cost) produces **4 independent review artifacts**, each citing only its seat's context slice
2. Config schema v2.8 (or v2.7.x) documents `collaboration.architecture_board` and passes validation toolchain
3. Agent prompt audit hook verifies context isolation — no seat's prompt contains another seat's slice
4. At least one real delivery-flow run (dogfood) uses the pattern during Architect stage and the PO can point to the synthesis artifact
5. Number of rounds is driven by config, not code — flipping `max_rounds: 1 → 2` in config changes behavior without code edit
6. **(from BACKLOG-002 / MAR pilot)** Iteration-2 of the board loop routes through **different** persona context slices than iteration-1 (persona diversity preserved across rounds); zero 3-peat recurrences of the same defect class in `topics/defect-patterns.md` over the pilot window
7. **(from BACKLOG-002 / MAR)** Token cost of iteration-2 re-review <25% over iteration-1 baseline per run
8. **(from BACKLOG-002 / MAR)** Pilot includes at least one run that historically hit round-2 self-correction during Architect stage; recurrence class ("installed-vs-source sync", "stale derived artifacts") resolved or explicitly documented as out-of-scope

## Size & Complexity
- **M** (new pattern + schema bump + reference doc + orchestrator wiring + dogfood run)
- Reuses existing Review Board scaffolding and agent prompt audit hook

## Dependencies
- **Must-run-after BACKLOG-001 + BACKLOG-004** — board seats consume the constraints/decomposition model they produce; building the board before those models exist means reviewing prose
- **Absorbs BACKLOG-002** — no separate MAR pilot; MAR acceptance criteria are folded in above
- Naturally pairs with BACKLOG-005 (paradigm-as-skill) — board review becomes more valuable once paradigm skills exist to be reviewed
- Should land **before** BACKLOG-005 pilot so the paradigm skill pilot can be reviewed by the board

## Links
- Architect examination: `.delivery/artifacts/research/architect-examine-decomposition-gaps.md` *(placeholder)*
- Current Review Board reference: `delivery-team/skills/delivery-flow/references/` (collaboration patterns)
- Agent prompt audit hook: `delivery-team/hooks/` (context isolation enforcement)
