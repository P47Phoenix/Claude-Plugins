# transformation-planning — Master Protocol

> *"A forge worth keeping is one whose hammer has already struck a second ring."*
> — Celebrimbor

## Purpose

`transformation-planning` is the Architect task type for **brownfield / legacy transformation**. It produces a linked, diffable AS-IS → TO-BE → Roadmap artifact set so that modernization is planned on evidence, not vibes. It is the answer to the PRD's central grievance: *the Architect skill was greenfield-only, and structural analysis without behavioral reconstruction is blind.*

## When to use

Select this task type when **any** of the following apply:

- The system already exists and its original intent is lost, partial, or unwritten.
- A migration, re-platforming, or modernization effort is being scoped.
- Legacy code must be understood before a TO-BE architecture can be proposed.
- Request signals include: "brownfield", "legacy", "AS-IS", "TO-BE", "migration plan", "modernization roadmap", "reconstruct use cases".

Do **not** use for pure greenfield work — use `design` instead. Do not use for automated refactoring — this task produces **plans**, not automation (out of scope per PRD).

## Ownership — PO + Architect pairing

This is the only Architect task type with **shared ownership**. Behavioral reconstruction is a product discipline; structural reconstruction is an architectural discipline. Conflating them produces either vibes-based use cases or user-blind structural models.

| Phase | Name | Owner | Output |
|---|---|---|---|
| **1A** | Behavioral AS-IS | **Product Owner** | `as-is-use-cases.md` |
| **1B** | Structural AS-IS | **Architect** (Solution) | `as-is-constraints.yml` |
| **2**  | TO-BE model | **Architect** (Solution) | `to-be-constraints.yml` |
| **3**  | Roadmap | **Architect** (Solution) | `roadmap.md` |

Phases are sequenced by the orchestrator. Each phase **writes its artifact to disk before the next phase reads it** (two-channel, file-based handoff — no in-memory co-execution). Phase 1B consumes Phase 1A use cases as `actions` in the shared BACKLOG-001 `constraints.yml` schema.

See ADR-001 (`.delivery/artifacts/04-architect/adrs/ADR-001-transformation-sub-workflow.md`) for the decision record and rejected alternatives.

## Legacy trigger rule (Phase 1A default ON)

Phase 1A runs **by default** on every `transformation-planning` invocation. It is skippable **only** when the PO explicitly asserts that trusted existing use-case documentation exists and cites it in the invocation. Skipping is logged with written justification in the Phase 1B artifact header.

Rationale: a structural-only pass reproduces the very blindness this task type exists to eliminate.

## Output artifact layout

Canonical location (inside a delivery-flow pipeline run):

```
.delivery/artifacts/08-transform/
├── as-is-use-cases.md         # Phase 1A — PO-led behavioral reconstruction
├── as-is-constraints.yml      # Phase 1B — Architect-led structural AS-IS
├── to-be-constraints.yml      # Phase 2  — TO-BE model (shared schema)
└── roadmap.md                 # Phase 3  — ordered AS-IS → TO-BE steps
```

`08-transform` sits after UAT in the pipeline sequence. Outside a pipeline run (standalone architect invocation), use `transform/` at repo root.

## Phase 1A review — MAR persona trio

Phase 1A is reviewed using the **architecture-board** pattern (BACKLOG-003 — this is the pattern's second instantiation; no new collaboration machinery is introduced). The review board consists of three personas:

- **Code Archaeologist** — evidence-bound; skeptical of confident claims lacking citations.
- **User Advocate** — what would an end user actually care about?
- **Skeptical Tester** — can we write a test for this use case?

Each reviewed use case must carry `evidence_citations` (file path + what the file shows) and a `confidence` level (high/medium/low). **At least one `confidence=low` use case is forced per run** to defeat confidence-level gaming.

## Roadmap constraints (Phase 3)

- **No-big-bang threshold:** each roadmap step touches at most **30%** of subsystems in the AS-IS model (`subsystems_touched / total_subsystems_in_as_is_model`).
- **Edge case (< 4 subsystems):** threshold collapses to *"at most 1 subsystem per step."*
- **Escape valve:** up to 7 steps allowed; >7 requires written justification in the roadmap header.
- **Independently shippable:** every step must be reversible and deliver incremental value.

See ADR-002 (`.delivery/artifacts/04-architect/adrs/ADR-002-big-bang-threshold.md`) for the threshold derivation.

## Phase-specific reference docs

Load these on demand depending on the active phase:

| Phase | Reference file |
|---|---|
| 1A | `transformation-phase-1a-behavioral.md` — evidence sources, use-case template, confidence rules, MAR persona trio details |
| 1B | `transformation-phase-1b-structural.md` — Model-First mapping (use cases→actions, modules→entities, coupling→state, rules→constraints) |
| 2  | `transformation-phase-2-to-be.md` — TO-BE construction on the shared constraints.yml schema |
| 3  | `transformation-phase-3-roadmap.md` — roadmap template, no-big-bang check, independently-shippable rule |

## Shared primitives

- **Constraints schema** (both AS-IS and TO-BE use it) — BACKLOG-001, documented in the delivery-flow `constraints.yml` schema reference.
- **Architecture-board review pattern** — BACKLOG-003; reused for Phase 1A review with the MAR persona trio above.
- **Input/Output contracts** — standard Architect sub-agent contracts (see SKILL.md §Sub-Agent Interface).

## Quick-start invocation

```json
{
  "task_type": "transformation-planning",
  "role": "solution",
  "context": {
    "system": "LegacyOrderSvc",
    "existing_architecture": "Monolithic Rails app, ~85k LoC, no original PRD",
    "constraints": ["must preserve current invoice numbering", "no downtime migration"],
    "prd_reference": ".delivery/artifacts/02-refine/po/prd.md"
  },
  "input": "Plan the modernization of LegacyOrderSvc onto an event-driven architecture. We have tests and UI strings but no use-case docs."
}
```

Expected result: the 4 artifacts listed above under `.delivery/artifacts/08-transform/`, cross-linked, with Phase 1A reviewed by the MAR persona trio and Phase 3 passing the 30% big-bang check.

## Non-goals

- No live migration execution.
- No automated refactoring.
- No paradigm-as-skill restructure (BACKLOG-005).
- No new collaboration pattern (reuses BACKLOG-003 architecture-board).
