# PO Framing — Design Sprint & Decomposition Refinement

**Date**: 2026-04-08
**Author**: Product Owner (delivery-team:product-delivery)
**Source ask**: PO raw ask, 2026-04-08 — "We need to better refine a design sprint and how architecture patterns are applied and reviewed" (full verbatim in each backlog item's Source section)
**Paired work**: Architect is examining current state and proposing structural options in parallel at `.delivery/artifacts/research/architect-examine-decomposition-gaps.md` *(placeholder — not yet written at time of this memo)*

## Thread Breakdown

The PO ask contains **three distinct threads**. They are related but must not be bundled — they differ in size, risk, and prerequisite ordering.

### Thread A — Configurable Architecture Board Review pattern → BACKLOG-003
Per-reviewer context isolation, distinct perspective per seat, config-driven agentic loop. Extends the existing Review Board pattern rather than replacing it. **Size: M**.

### Thread B — Decomposition guidance depth → BACKLOG-004
Three linked defects in one thread:
1. Volatility golden rule missing from reference docs
2. Implementation-detail contamination (Lambda/ECR/SQS/language names) in Architect output — PO suspects parallel defect in DDD
3. Architect absent from Plan stage

Content fixes + a rule-based guardrail lint + Plan-stage participation. **Size: S–M**. This is the thread with the clearest, most measurable failure mode today.

### Thread C — Paradigm-as-skill restructure + Design Sprint sub-workflow → BACKLOG-005
Architect skill becomes a router; each decomposition paradigm becomes its own skill with staged markdown files; new PO+Architect Design Sprint sub-workflow. **Size: L — FEATURE-scale**. Flagged on the backlog item itself as warranting its own delivery-flow run.

## Backlog Items Created

| ID | Title | Priority | Size |
|----|-------|----------|------|
| BACKLOG-003 | Configurable Architecture Board Review pattern | P2 | M |
| BACKLOG-004 | Decomposition guidance depth (golden rule, guardrails, Architect in Plan) | P1 | S–M |
| BACKLOG-005 | Paradigm-as-skill restructure + Design Sprint sub-workflow | P2 | L (FEATURE) |

Each backlog item cites the PO ask verbatim, leaves a placeholder link to the Architect examination file, and states concrete measurable success criteria (zero-contamination token check, N independent review artifacts, paradigm skill pilot run, etc.).

## Sequencing Rationale (vs existing backlog)

Existing backlog:
- **BACKLOG-001** — Model-First `constraints.yml` spike (P1, M) — QA's highest quality lift
- **BACKLOG-002** — MAR iteration-2 persona swap (P3, S) — narrow pilot

Recommended sequence:

1. **BACKLOG-001 (P1) — keep in flight.** Already the team's top quality lever per QA. No conflict with the new items.
2. **BACKLOG-004 (P1) — start in parallel with BACKLOG-001.** This is the most observable, most measurable defect from the PO ask (implementation-detail contamination is happening *today* in Architect output). It is S–M sized, has a deterministic rule-based guardrail as its acceptance check, and does **not** require structural restructuring. Fast win that also de-risks BACKLOG-005.
3. **BACKLOG-003 (P2) — next.** Land after BACKLOG-004 content corrections are in, because the board review gains leverage when reviewing improved decomposition output. Can start design work in parallel if capacity allows.
4. **BACKLOG-005 (P2, FEATURE) — last, and run as its own delivery-flow.** Depends on BACKLOG-004 (correct content) and pairs with BACKLOG-003 (board review consumed by Design Sprint). Do **not** start before Architect examination selects a structural option and before BACKLOG-004 lands.
5. **BACKLOG-002 (P3) — unchanged.** Lowest priority, narrow pilot, no conflict.

**Why BACKLOG-004 at P1 alongside BACKLOG-001:** BACKLOG-001 is a research-driven quality lift; BACKLOG-004 is a remediation of an active observable defect. They hit different parts of the pipeline (Refine vs Architect) and different owners' primary attention, so parallel execution is realistic.

**Why BACKLOG-005 is not P1 despite being the PO's most ambitious ask:** restructure-before-correct is a classic anti-pattern. We should fix the content first (BACKLOG-004), then restructure around correct content (BACKLOG-005). Shipping the restructure on top of today's contaminated guidance would bake the defect into the new skill boundaries.

## Avoiding Duplication with Architect's Work

The Architect is examining current state and proposing concrete structural options in parallel. This memo and the three backlog items intentionally:
- State **direction only**, not concrete file inventories, skill boundaries, or lint token lists
- Leave placeholder links to `.delivery/artifacts/research/architect-examine-decomposition-gaps.md`
- Defer all structural decisions (how many paradigm skills, board seat catalog, Design Sprint stage shape, DDD scope confirmation) to Architect examination output

When the Architect file lands, each backlog item's "Proposed Direction" section should be updated with the selected option and the placeholder link replaced with a real link.

## Recommended Next Action

**Wait for Architect examination → convene a 30-minute team review (PO + Architect + Quality + one dev) to pick the structural option for BACKLOG-005 and confirm DDD scope for BACKLOG-004 → kick off BACKLOG-004 immediately as a standard FEATURE delivery-flow run, and schedule BACKLOG-005 as its own FEATURE run to start once BACKLOG-004 merges.**
