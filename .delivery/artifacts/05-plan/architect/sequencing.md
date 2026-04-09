# Sequencing — BACKLOG-006 transformation-planning
**Role:** Celebrimbor (Architect)
**Stage:** 05-plan
**Pipeline:** run-2026-04-09-c4d1

## Story ↔ Architecture Mapping

| Story | Architecture Element | ADR |
|---|---|---|
| US-1 | `architect/SKILL.md` task_type registry surface | ADR-001 |
| US-2 | Master protocol doc (new reference root) | ADR-001 |
| US-3 | Phase 1A reference — PO-led behavioral craft | ADR-001 |
| US-4 | Phase 1B reference — Architect-led Model-First structural | ADR-001, BACKLOG-001 schema |
| US-5 | Phase 2 + 3 references — TO-BE + roadmap mechanics | ADR-001, **ADR-002 (30% threshold)** |
| US-6 | Templates — schema-conformant scaffolds | BACKLOG-001 schema |
| US-7 | Dogfood Phase 1A artifact | FR-8 empirical proof |
| US-8 | Dogfood Phases 1B+2+3 artifacts | FR-8 empirical proof |

## Volatility Sequencing Check (Model-First)
Authoring order matches stability order:
1. **Stable first:** US-1 + US-2 (task_type name + protocol contract) — invariants.
2. **Schema-stable:** US-3..US-5 (phase docs) — schemas frozen by PRD/ADRs.
3. **Consumer scaffolding:** US-6 templates — stable once phase docs ship.
4. **Volatile last:** US-7, US-8 dogfood — evidence-driven, highest content volatility, ride on stable upstream.
No sequencing inversion. PO↔Architect handoff (US-7→US-8) is file-based per ADR-001.

## Interface Contracts
- `transformation-planning.md` (US-2) ← read by US-3/4/5 phase docs (link contract).
- Phase 1A doc (US-3) → schema consumed by `templates/as-is-use-cases.md` (US-6) → consumed by dogfood US-7.
- Phase 1B doc (US-4) → `actions` field MUST reference US-7 output (cross-phase file contract, auditable).
- Phase 3 doc (US-5) → 30% math contract from ADR-002 → enforced empirically by T-8.4 on US-8 output.
- Templates (US-6) are the **only** write-contract between reference docs and dogfood output; schema drift caught there.

## Coordination Overhead Estimate
- PO↔Architect handoffs: **2** (optional US-2 co-authoring; US-7→US-8 file handoff).
- MAR touchpoints: **1** (US-7 Phase 1A architecture-board review).
- Cross-story drift risk: **low** — schemas pre-frozen in ADRs + constraints.yml.
- Overhead: ~0.5 pt absorbed into existing estimates; no separate coordination story.

## Amendments Proposed → MERGED INTO stories.md / sprint-plan.md THIS DISPATCH
1. **Dogfood path** corrected to `.delivery/artifacts/dogfood/transformation-planning/` (per `constraints.yml.mandatory_artifacts`, overriding dispatch prompt's `08-transform/`). → Merged into US-7/US-8 ACs + stories.md §Amendments.
2. **Forbidden-vocab oracle scope** pinned to TO-BE only (AS-IS exempt for evidence fidelity). → Merged into US-8 AC-8.6 + test-strategy T-8.7.
3. **US-2 as hard prerequisite** of US-3..US-5. → Merged into stories.md deps and sprint-plan P1→P2 order.
4. **Sprint P4 hard-cap (5 pts)** with written justification logged in sprint-plan.md.

No round-2 correction needed — amendments fused in-dispatch per instruction.
