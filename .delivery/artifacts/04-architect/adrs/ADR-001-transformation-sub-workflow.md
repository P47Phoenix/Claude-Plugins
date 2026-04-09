# ADR-001: transformation-planning is a 4-phase sub-workflow with PO+Architect pairing

**Status:** Accepted
**Date:** 2026-04-08
**Deciders:** Celebrimbor (Architect), Gandalf (PO)
**Related:** PRD `.delivery/artifacts/02-refine/po/prd.md`, BACKLOG-006, BACKLOG-001 (shared constraints schema), BACKLOG-003 (architecture-board pattern)

## Context

The Architect skill has no brownfield transformation capability. Legacy systems require both behavioral (what does it do for users?) and structural (what are the modules?) reconstruction before any TO-BE model or roadmap can be forged. Behavioral work is a PO discipline — evidence mining from tests, UI strings, docs, commits. Structural work is an Architect discipline — entities, state, constraints. A single-owner task conflates two very different craft traditions, and a purely structural pass is blind to user intent. We must also ensure each phase hands off cleanly and auditably, without assuming in-memory continuity between agents.

## Decision

`transformation-planning` is a 4-phase sub-workflow:

1. **Phase 1A (PO-led)** — Behavioral AS-IS → `as-is-use-cases.md`
2. **Phase 1B (Architect-led)** — Structural AS-IS → `as-is-constraints.yml` (consumes 1A use cases as `actions`)
3. **Phase 2 (Architect-led)** — TO-BE model → `to-be-constraints.yml`
4. **Phase 3 (Architect-led)** — Roadmap → `roadmap.md`

Each phase writes its artifact to disk before the next phase reads it (two-channel, file-based handoff). Phase 1A reviewed by the BACKLOG-003 architecture-board pattern using a new MAR persona trio (code archaeologist, user advocate, skeptical tester). Legacy trigger: Phase 1A defaults ON; skippable only with logged PO justification citing trusted existing use-case docs.

## Consequences

**Easier:**
- Clear ownership: PO owns behavioral craft; Architect owns structural craft.
- Auditable handoff: every phase artifact is on disk and diffable.
- Cross-artifact traceability: use cases → actions → TO-BE deltas → roadmap steps.
- Reuses existing architecture-board pattern; no new collaboration machinery.

**Harder:**
- PO+Architect coordination overhead (mitigated by file-based, not live, handoff).
- Four artifacts instead of one; more surface to keep consistent.
- Legacy trigger discipline required to avoid skipping Phase 1A on brownfield work.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|---|---|---|---|
| **Single monolithic architect task** | Simplest dispatch; one owner | Conflates behavioral and structural craft; no PO involvement; no evidence discipline for use cases | Structural-only pass is blind to user intent — a core PRD grievance |
| **Two-phase (structural + TO-BE), no Phase 1A behavioral** | Less coordination; fewer artifacts | Use cases hallucinated or skipped entirely; downstream roadmap cannot cite preserved invariants meaningfully | Violates FR-2 and the PRD's central complaint about behavioral blindness |
| **Fully automated refactoring tool** | Zero human coordination | Produces plans only per out-of-scope; live migration explicitly excluded; tool cannot reconstruct intent from evidence | Out of scope per PRD; capability produces *plans*, not automation |
| **Three-phase (merge 1A+1B into one PO+Architect co-session)** | One fewer handoff | Live co-execution violates file-handoff discipline; muddies ownership; harder to audit | Violates two-channel rule; coordination cost without auditability gain |

## Rationale

The 4-phase shape is the minimum that honors two craft traditions (behavioral and structural) while keeping handoffs file-based and auditable. Phase 1A must be PO-led because evidence mining from UI strings, tests, and commits is a product discipline, not an architectural one. Phases 1B–3 must be Architect-led because they operate on the shared BACKLOG-001 constraints schema and demand structural reasoning. Reusing the BACKLOG-003 architecture-board pattern for Phase 1A review costs nothing new and establishes the pattern as a reusable board-of-review primitive — its second instantiation proves the pattern generalizes beyond its original home.
