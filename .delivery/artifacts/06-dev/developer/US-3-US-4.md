# US-3 + US-4 — Transformation Phase 1A & 1B reference docs

*By Gimli son of Glóin, dwarven developer.*

## Scope
- US-3: FR-2 + FR-7 — Phase 1A behavioral reconstruction reference (PO-led).
- US-4: FR-3 + FR-7 — Phase 1B structural reconstruction reference (Architect-led).

## Deliverables
- `delivery-team/skills/architect/references/transformation-phase-1a-behavioral.md` (119 lines, cap 220)
- `delivery-team/skills/architect/references/transformation-phase-1b-structural.md` (70 lines, cap 180)

## Key design points
- Phase 1A schema matches architecture.md §5 verbatim; ≥1 low-confidence entry forced as honesty function.
- MAR trio (Code Archaeologist, User Advocate, Skeptical Tester) reuses BACKLOG-003 architecture-board pattern — no new collaboration pattern.
- Legacy trigger rule: default RUN; skip only on PO-cited trusted docs < 6 months old, logged.
- Phase 1B consumes 1A on disk (two-channel rule); blocks if 1A missing.
- Model-First mapping table: actors→entities, flows→actions, preconditions→state_variables, implicit rules→invariants, modules→entities, coupling→state.
- Observed (not desired) volatility classification; desired-state is Phase 2 contamination.

## Anti-patterns called out
- Hallucinated use cases, high-confidence floor, scope drift into TO-BE, orphan actions, module-diagram-only AS-IS.

Aye — two rings forged, each ringing its own note.
