# US-1 + US-2 — transformation-planning task type registration & master doc

**Developer:** Gimli son of Glóin | **Run:** BACKLOG-006 | **Date:** 2026-04-08

## Scope

- **US-1:** Register new `transformation-planning` task_type in `delivery-team/skills/architect/SKILL.md`.
- **US-2:** Create master protocol doc `delivery-team/skills/architect/references/transformation-planning.md`.

## Changes

1. **`delivery-team/skills/architect/SKILL.md`** — three surgical edits:
   - Software Task Type Routing Table: added `transformation-planning` row (brownfield/legacy/AS-IS→TO-BE signals, Solution+PO ownership, loads master ref).
   - Software Task Type Instructions: added `transformation-planning` row describing the 4-phase PO+Architect sub-workflow with pointer to master doc.
   - Input Contract enum (line ~519): added `transformation-planning`.

2. **`delivery-team/skills/architect/references/transformation-planning.md`** — NEW (115 lines, under the 200 budget):
   - Purpose + when-to-use (brownfield, legacy, migration).
   - 4-phase structure table with PO+Architect ownership per phase.
   - Legacy trigger rule (Phase 1A default ON; skippable only with cited trusted docs).
   - Canonical artifact layout under `.delivery/artifacts/08-transform/`.
   - Phase 1A MAR persona trio (Code Archaeologist, User Advocate, Skeptical Tester) via BACKLOG-003 architecture-board pattern.
   - Roadmap constraints (30% threshold, <4 subsystem collapse, ≤7 steps escape valve) with ADR-002 pointer.
   - Pointers to the 4 phase-specific refs (1a-behavioral, 1b-structural, 2-to-be, 3-roadmap).
   - Shared primitives (constraints.yml schema, architecture-board pattern).
   - Quick-start JSON invocation example.
   - Non-goals enumerated.
   - ADR-001 linked for decision provenance.

## Verification

- Master doc line count: 115 (< 200 cap).
- SKILL.md edits preserve existing table formatting; three surgical insertions only.
- All cross-links resolve to real paths (ADR-001, ADR-002, architecture.md §BACKLOG-006, phase refs TBD by downstream stories).

## Out of scope (follow-on work)

- The 4 phase-specific reference docs (`transformation-phase-1a-behavioral.md`, etc.) are referenced but not created here — separate stories.
- The two new delivery-flow templates (`transformation-use-cases-template.md`, `transformation-roadmap-template.md`) — separate stories.

STATUS: DONE
