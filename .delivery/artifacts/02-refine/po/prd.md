# PRD — Architect Transformation Planning Capability

**Pipeline:** run-2026-04-09-c4d1
**Date:** 2026-04-09
**Source:** BACKLOG-006-architect-transformation-planning.md
**Owner:** PO (Gandalf) + Architect (paired)
**Stage:** 02-refine

## Problem
Per BACKLOG-006, the Architect skill is effectively greenfield-only: its task_types (`design`, `decompose`, `model`, etc. at `architect/SKILL.md:519`) assume PRD → architecture, and the closest brownfield-adjacent capability (`audit-preparation`) is compliance-focused. Real-world architecture work is dominated by brownfield migrations of legacy systems whose original authors and intent are gone. Worse, structural analysis alone is blind: one can map modules and coupling without knowing what the system is *for*. Phase 1A behavioral reconstruction — use cases reverse-engineered from code, tests, UI, docs, and history — is missing entirely. No capability today produces a linked, diffable AS-IS → TO-BE → Roadmap artifact set.

## Users / Actors
- **PO** — Phase 1A owner; reconstructs use cases from codebase evidence.
- **Architect** — Phase 1B / Phase 2 / Phase 3 owner; builds structural AS-IS, TO-BE model, roadmap.
- **Downstream engineers** — consume the roadmap as an execution plan; each step is independently shippable work.
- **Orchestrator (delivery-flow)** — dispatches the sub-workflow and enforces phase ordering / handoffs.

## Functional Requirements
- **FR-1** — Register new architect `task_type: transformation-planning` in `delivery-team/skills/architect/SKILL.md`.
- **FR-2 — Phase 1A Behavioral Reconstruction (PO-led):** reads codebase evidence (tests, UI strings, endpoints, commits, docs, telemetry if any) and produces `as-is-use-cases.md`. Each use case carries: `actor`, `goal`, `preconditions`, `main_flow`, `variations`, `evidence_citations`, `confidence` (high/medium/low). A dogfood run must yield ≥5 use cases; ≥1 MUST carry `confidence=low` with a written reason.
- **FR-3 — Phase 1B Structural Reconstruction (Architect-led):** Model-First AS-IS with four elements — `entities` (current modules/services), `state` (volatility/coupling), `actions` (the Phase 1A use cases), `constraints` (implicit rules the code follows today). Emitted as `as-is-constraints.yml` conforming to the shared BACKLOG-001 schema.
- **FR-4 — Phase 2 TO-BE (Architect-led):** explicit TO-BE model expressed as `to-be-constraints.yml` in the same schema. Must cite the volatility golden rule (BACKLOG-004) when available.
- **FR-5 — Phase 3 Roadmap (Architect-led):** ordered iterative steps bridging AS-IS → TO-BE. Each step names: `scope`, `ordering_rationale`, `reversibility`, `risk`, `incremental_value`, `preserved_invariants`. ≥3 steps. Each step independently shippable (no step depends on a future step for value). "No big-bang" check: no single step changes more than 30% of subsystems.
- **FR-6 — Legacy trigger rule:** documented in architect references. Phase 1A default ON. Skippable ONLY when the PO explicitly asserts trusted current use-case documentation exists and is cited in the invocation; skipping is logged with justification.
- **FR-7 — Reference docs:** four reference documents under `architect/references/` covering Phase 1A (behavioral), Phase 1B (structural), Phase 2 (TO-BE), Phase 3 (roadmap). Phase 1A reference includes a MAR-style persona trio — code archaeologist, user advocate, skeptical tester — for use-case review.
- **FR-8 — Dogfood:** first invocation runs against Claude-Plugins itself, producing all three linked artifacts committed to `.delivery/artifacts/`.

## Non-Functional Requirements
- **NFR-1** — AS-IS and TO-BE artifacts conform to the shared `constraints.yml` schema from BACKLOG-001 (cross-backlog consistency).
- **NFR-2** — No new required config keys in `.delivery/config.yml`; backwards compatible with schema v2.7.
- **NFR-3** — Roadmap steps are diffable against AS-IS and TO-BE models (measurable convergence — each step closes a named delta).

## Acceptance Criteria
1. `transformation-planning` appears in the architect SKILL.md task_type list and is dispatchable.
2. A dogfood run against Claude-Plugins produces `as-is-use-cases.md` with ≥5 entries, each with evidence citations, ≥1 carrying `confidence=low`.
3. `as-is-constraints.yml` validates against the shared schema and references 1A use cases in its `actions` field.
4. `to-be-constraints.yml` validates against the shared schema and cites the volatility golden rule.
5. `roadmap.md` lists ≥3 ordered steps, each with all six required fields, each independently shippable, none exceeding the 30% subsystem-change ceiling.
6. All four reference docs exist under `architect/references/`.
7. `validate_constraints.py` exits 0 on both AS-IS and TO-BE outputs.

## Out of Scope
- BACKLOG-005 paradigm-as-skill restructure.
- Automated refactor tooling.
- Live migration execution — this capability produces *plans*, not automation of the plans.
- Behavioral reconstruction beyond cited evidence; no hallucinated use cases.

## Success Metrics
- Dogfood run produces real use cases with real evidence citations (not stubs).
- Roadmap ≥3 independently-shippable steps named against real Claude-Plugins subsystems.
- All three linked artifacts committed and diffable; validator exits 0.

## Risks + Mitigations
- **R-1 Hallucinated use cases** — Mitigation: `evidence_citations` required field; `confidence` forced; ≥1 low-confidence mandate prevents false certainty.
- **R-2 Scope creep into BACKLOG-005** — Mitigation: explicit anti-scope in FR and Out of Scope sections; paradigm-as-skill restructure stays on -005.
- **R-3 AS-IS → TO-BE gap too wide to be roadmap-able** — Mitigation: 30% subsystem ceiling forces incremental decomposition; if the gap cannot be closed in ≥3 shippable steps, the TO-BE is wrong and returns to Phase 2.
- **R-4 PO + Architect coordination overhead** — Mitigation: file-based handoff (1A artifact → 1B consumer), not live co-execution; orchestrator sequences the phases.
