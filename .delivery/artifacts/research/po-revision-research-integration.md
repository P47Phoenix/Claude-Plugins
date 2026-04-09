# PO Revision — Research Integration into Decomposition Backlog

**Date**: 2026-04-08
**Author**: Product Owner (delivery-team:product-delivery)
**Directive**: "Should include concepts from what we talked about with model first reasoning and multi agent reflexion"
**Insight**: The decomposition work (BACKLOG-003/004/005) and the research adoption work (BACKLOG-001/002) are not independent — they share primitives. Running them as separate streams duplicates effort.

## Overlap Decisions

| Overlap | Decision | Justification |
|---|---|---|
| BACKLOG-001 (Model-First `constraints.yml`) vs BACKLOG-004 (decomposition guardrails) | **LINK — run in parallel, shared schema** | The banned-token lint + golden-rule invariant in BACKLOG-004 are structurally identical to the `numeric_ceilings`/`adr_invariants` entries in BACKLOG-001's `constraints.yml`; co-developing pressure-tests the schema against two domains (Refine + Architect) before any v2.8 bump. |
| BACKLOG-002 (MAR iteration-2 persona swap) vs BACKLOG-003 (architecture board) | **MERGE — BACKLOG-003 absorbs BACKLOG-002** | BACKLOG-003's per-seat context isolation + configurable loop + Architect synthesis IS MAR's multi-persona debator + judge instantiated for architecture review; the architecture board is the higher-leverage site for MAR's only genuinely novel idea (persona-diverse reflection), so running both builds two overlapping patterns. |
| BACKLOG-004 (content fixes) vs BACKLOG-005 (paradigm-as-skill restructure) | **KEEP INDEPENDENT (with dependency)** | The existing "content-before-restructure" ordering stands — BACKLOG-005 is a structural change that must be built on correct content from BACKLOG-004; they are genuinely different concerns (content correctness vs skill topology) even though they share the same research lineage. |

## New Sequencing

**Old**: BACKLOG-001 ∥ BACKLOG-004 → BACKLOG-003 → BACKLOG-005 → BACKLOG-002
**New**: **(BACKLOG-001 ∥ BACKLOG-004 — shared constraints primitive) → BACKLOG-003 (absorbs BACKLOG-002) → BACKLOG-005**

BACKLOG-002 is removed from the queue as a standalone item; its acceptance criteria (round-2 success ↑, zero 3-peat recurrences, <25% token overhead) are now carried by BACKLOG-003's iteration-2 board loop. BACKLOG-005 continues to be FEATURE-scale and run as its own delivery-flow.

## Summary of Changes to Backlog Files

### BACKLOG-001 — Model-First `constraints.yml` spike
- Added **Research lineage** section citing Model-First paper (arXiv:2512.14474) and cross-linking to BACKLOG-004 as candidate second domain for the same mechanism.
- Noted parallel run with BACKLOG-004 as a schema-pressure-test strategy.
- Added BACKLOG-004 and this revision memo to Links.

### BACKLOG-002 — MAR cross-persona pilot
- Status changed to **MERGED into BACKLOG-003**; item preserved as a redirect stub with merge rationale.
- Historical content preserved in place for traceability per constraint.

### BACKLOG-003 — Configurable Architecture Board Review pattern
- Title updated to note absorption of BACKLOG-002.
- Added **Research lineage** section mapping MAR concepts 1:1 onto board structure (multi-persona debators = per-seat context slices; judge = Architect synthesis; Reflexion loop = `max_rounds`) and linking Model-First decomposition model as board input.
- Added 3 new acceptance criteria (items 6–8) imported from BACKLOG-002: iteration-2 persona diversity, <25% token overhead, pilot on historically round-2 runs, zero 3-peat recurrences.
- Dependencies updated: must-run-after BACKLOG-001 + BACKLOG-004 (board seats consume their output).

### BACKLOG-004 — Decomposition guidance depth
- Added **Research lineage** section: decomposition IS model construction in the Model-First sense; guardrails and golden rule are constraints that should reuse BACKLOG-001's `constraints.yml` schema; feeds BACKLOG-003's `volatility_reviewer` seat.
- Added acceptance criterion 6: guardrails expressed as structured constraint entries, not prose.
- Dependencies updated: parallel with BACKLOG-001; blocks BACKLOG-003 and BACKLOG-005.

### BACKLOG-005 — Paradigm-as-skill restructure
- Added **Research lineage** section framing the Design Sprint sub-workflow as the synthesis of Model-First (explicit decomposition model) + MAR (multi-persona board review via BACKLOG-003) applied to architecture design; paradigm-as-skill is the vehicle.
- Added acceptance criteria 6 and 7: Model-First evidence (structured model in paradigm skill) and MAR evidence (routes through BACKLOG-003 board, no bespoke review loop).
- Dependencies updated: depends on BACKLOG-001 + BACKLOG-004 + BACKLOG-003.

## Recommended Next Action

**Kick off BACKLOG-001 and BACKLOG-004 as a single paired delivery-flow FEATURE run this week** — shared `constraints.yml` schema is co-developed across Refine and Architect stages, pressure-testing the primitive against two domains in one run. Once merged, start BACKLOG-003 (which now carries the MAR pilot criteria) as a standard FEATURE run, then schedule BACKLOG-005 as its own FEATURE run per the original plan.

## Addendum — 2026-04-08 — BACKLOG-006 inserted

**New item**: BACKLOG-006 — Architect transformation planning (AS-IS → TO-BE → Roadmap). New architect `task_type: transformation-planning` implemented as a scan → AS-IS → TO-BE → roadmap → review sub-workflow producing three linked, diffable artifacts. See `.delivery/backlog/BACKLOG-006-architect-transformation-planning.md`.

**Revised sequence**:
`(BACKLOG-001 ∥ BACKLOG-004) → BACKLOG-003 → BACKLOG-006 → BACKLOG-005`

**Rationale for placement**:
1. **Third-domain validation of the constraints primitive.** BACKLOG-001 and BACKLOG-004 co-develop `constraints.yml` across Refine and Architect decomposition (two domains). BACKLOG-006 exercises the SAME schema in a third, harder domain — brownfield transformation, where both AS-IS and TO-BE emit constraint instances and the roadmap is a constraint-preserving transformation between them. This is the strongest pressure-test we have planned before any v2.8 bump.
2. **Real target for the architecture board.** BACKLOG-003's board pattern gets validated on an actual TO-BE model (not a greenfield design), with persona-diverse review of ordering, reversibility, and invariant preservation on the roadmap.
3. **Meta-circularity — BACKLOG-006 feeds BACKLOG-005.** Running BACKLOG-006 against Claude-Plugins itself produces the AS-IS model of the current architect skill topology and a roadmap toward the paradigm-as-skill end state. BACKLOG-005 should not begin without that AS-IS model; otherwise it is restructuring blind. BACKLOG-006's dogfood output literally becomes BACKLOG-005's canonical input, so BACKLOG-006 must precede BACKLOG-005.

**Meta-circularity note**: The delivery-team plugin is the system we use BACKLOG-006 to analyze, and the AS-IS → TO-BE → Roadmap it produces on itself becomes the execution plan for BACKLOG-005. This is a structural argument, not a stylistic one: without BACKLOG-006, BACKLOG-005 lacks a modeled starting point.

## Addendum 2 — 2026-04-08 — BACKLOG-006 expanded with behavioral reconstruction

BACKLOG-006 has been expanded to split AS-IS into Phase 1A (PO-led behavioral reconstruction of use cases from legacy-system evidence — tests, UI strings, endpoints, commits, docs) and Phase 1B (Architect-led structural modeling that consumes 1A's use cases as the "actions" dimension of the Model-First explicit model). Cross-skill PO+Architect collaboration is now an explicit execution requirement of BACKLOG-006, making it the **first real instance of the PO+Architect Design Sprint sub-workflow pattern** that BACKLOG-005 will later formalize. The pairing strengthens the argument for BACKLOG-005 but does not change sequencing: BACKLOG-006 → BACKLOG-005 still holds. Default rule: Phase 1A runs unless the PO explicitly asserts trusted current use case documentation exists. Acceptance criteria now require ≥5 reconstructed use cases with evidence citations, mandatory low-confidence honesty, and behavioral-structural traceability on the dogfood run.
