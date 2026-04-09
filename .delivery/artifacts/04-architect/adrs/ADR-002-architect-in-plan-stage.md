# ADR-002 — Architect Participation in Stage 5 Plan

**Status**: accepted
**Date**: 2026-04-08
**Stage**: 4 Architect (LIGHT) | **Author**: Celebrimbor (Solution Architect)
**Feature**: Paired Constraints Primitive

## Context

The gap report (`.delivery/artifacts/research/architect-examine-decomposition-gaps.md` Gap 3) confirms that `delivery-team/skills/delivery-flow/references/pipeline-stages.md:428-449` invokes PO, QA, Scrum Bag, and DevOps at Stage 5 Plan — but not the Architect. Architect artifacts are consumed as input files only; `config-schema.md:57-63` retains Architect as a passive DoD validator. This contradicts `volatility-decomposition.md:97-120` Phase 5, which assigns the Architect to implementation sequencing, interface design, and effort estimation. The PRD closes this gap via FR-6 and AC-5.

## Decision

Architect is invoked in Stage 5 Plan as an **active participant** (not a gate-owner) via a new sub-flow step with `task_type: implementation-sequencing`.

**Invocation point**: new step 2 inserted between current `pipeline-stages.md` line 430 (end of step 1 PO invocation) and current line 431 (start of QA invocation). Existing steps 2–9 renumber to 3–10.

**Task**:
- SKILL: `delivery-team:architect`
- TASK_TYPE: `implementation-sequencing`
- ROLE: `solution`
- Input artifacts: `.delivery/artifacts/02-refine/po/prd.md`, `.delivery/artifacts/02-refine/po/constraints.yml`, `.delivery/artifacts/04-architect/solution/architecture.md`, `.delivery/artifacts/04-architect/solution/constraints.yml`, `.delivery/artifacts/05-plan/po/stories.md`
- Output: `.delivery/artifacts/05-plan/architect/sequencing.md`
- Required for: FEATURE, GREENFIELD, GAME_DEV
- Waived for: BUG_FIX, DOCS_ONLY, DESIGN (Light Mode)

## Consequences

**Positive.**
- Closes Gap 3 and satisfies PRD FR-6 / AC-5.
- Stage 5 consensus now runs with an architect-authored sequencing note in hand, raising the signal quality of SM estimates and PO story ordering.
- Architect's decomposition constraints (volatility classes, invariants) flow into Plan with a named owner rather than as orphaned input files.

**Negative.**
- Architect workload per FEATURE run increases by one task. Tolerable: `implementation-sequencing` is a focused task on artifacts the Architect already authored — the cognitive burden is low.
- Plan stage duration increases by one sequential step before the parallel QA/SM/DevOps dispatch. Measured at Dev stage; expected impact is small because the Architect output is short (a sequencing note, not a full architecture document).
- Token cost: bounded by input artifact sizes already loaded elsewhere in the pipeline. Included in the PRD NFR-5 15% ceiling measurement.

## Alternatives Considered

1. **Architect as DoD reviewer only** (status quo). *Rejected*: passive post-hoc review cannot influence the sequencing decisions that Gap 3 identifies as the failure mode. 57% first-try Plan pass rate is the evidence.
2. **Architect as on-demand consult.** Invoked only when SM or PO explicitly requests. *Rejected*: the memory lesson `feedback_no_skip_stages.md` — on-demand tends toward skipped. Required steps are honored; optional steps are evaded under pressure.
3. **Full Architect presence across all Stage 5 sub-flows.** Architect participates in consensus and adversarial review as a peer. *Rejected*: token and time cost disproportionate to the gap; memory shows most Plan rework is in story decomposition and estimation, not in late-stage critique.
4. **Architect owns Stage 5.** *Rejected*: Stage 5 ownership belongs to PO and SM by pipeline convention; reassignment would reverberate through DoD validators, consensus protocol, and the config schema.

## Rationale

The chosen option is the minimum intervention that closes the gap. A single sequential step producing one short artifact is the cheapest way to place the Architect's voice inside Plan before the parallel dispatch consumes it. The waiver list (BUG_FIX, DOCS_ONLY, DESIGN) preserves Light Mode economics. The ADR is revisitable when BACKLOG-003 (architecture board) matures — at which point the board may absorb or extend this single-task touchpoint.
