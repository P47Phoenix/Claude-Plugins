# Stories — BACKLOG-006 transformation-planning
**Role:** Gandalf (PO)
**Stage:** 05-plan
**Source:** PRD FR-1..FR-8, constraints.yml, ADR-001, ADR-002
**Pipeline:** run-2026-04-09-c4d1

## Capacity Declaration
- Sprint ceiling: **4 pts**; hard cap: **5 pts**
- Estimate tier: markdown (XS=1, S=2, M=3, L=4, XL=5)
- Amendments merged from Celebrimbor sequencing pass: see §Amendments
- Dogfood output path per constraints.yml: `.delivery/artifacts/dogfood/transformation-planning/` (NOT `08-transform/` — constraints.yml is authoritative)

## Stories

### US-1 — Register `transformation-planning` task_type  (XS=1)
**As** the orchestrator **I want** a dispatchable `transformation-planning` task_type in architect SKILL.md **so that** Phase 1A..3 can be invoked.
**AC-1.1** (→FR-1) `delivery-team/skills/architect/SKILL.md` task_type list includes `transformation-planning` with 1-line description + 4-phase pointer.
**AC-1.2** (→FR-1) Entry names PO as Phase 1A owner and Architect as Phase 1B/2/3 owner (ADR-001).
**Deps:** none. **Blocks:** US-2..US-6.

### US-2 — Master protocol doc `transformation-planning.md`  (S=2)
**As** an operator **I want** a single entry reference **so that** the 4-phase flow, legacy trigger, and file-handoff contract are discoverable.
**AC-2.1** (→FR-6) Documents phase sequence, ownership, file-handoff rule (write-before-read).
**AC-2.2** (→FR-6) Documents legacy trigger: Phase 1A default ON; skippable only with logged PO justification citing trusted docs.
**AC-2.3** (→FR-7) Links to the four phase reference docs (1A, 1B, 2, 3).
**Deps:** US-1.

### US-3 — Phase 1A reference `transformation-phase-1a-behavioral.md`  (M=3)
**As** the PO **I want** the Phase 1A protocol **so that** I can reconstruct use cases from evidence.
**AC-3.1** (→FR-2) Use-case schema: `actor, goal, preconditions, main_flow, variations, evidence_citations, confidence{high|medium|low}`.
**AC-3.2** (→FR-2) Enumerates evidence sources: tests, UI strings, endpoints, commits, docs, telemetry.
**AC-3.3** (→FR-7) Includes MAR persona trio (code archaeologist, user advocate, skeptical tester) + architecture-board review step.
**AC-3.4** (→FR-6) Documents legacy trigger rule.
**Deps:** US-1, US-2.

### US-4 — Phase 1B reference `transformation-phase-1b-structural.md`  (M=3)
**As** the Architect **I want** the Phase 1B protocol **so that** I can produce `as-is-constraints.yml` under Model-First.
**AC-4.1** (→FR-3) Documents 4-element Model-First mapping: entities, state, actions, constraints; `actions` MUST consume Phase 1A use cases.
**AC-4.2** (→FR-3, NFR-1) Points to BACKLOG-001 shared constraints schema.
**Deps:** US-1, US-2.

### US-5 — Phase 2 + Phase 3 reference docs  (M=3)
**As** the Architect **I want** Phase 2 and Phase 3 protocols **so that** I can build `to-be-constraints.yml` and `roadmap.md`.
**AC-5.1** (→FR-4) `transformation-phase-2-to-be.md` documents TO-BE schema (same as AS-IS) and requires citation of volatility golden rule (BACKLOG-004) when available.
**AC-5.2** (→FR-5) `transformation-phase-3-roadmap.md` documents step schema (`scope, ordering_rationale, reversibility, risk, incremental_value, preserved_invariants`).
**AC-5.3** (→FR-5) Documents 30% big-bang check per ADR-002, including the <4 subsystems collapse and >7-step justification escape.
**AC-5.4** (→FR-5, NFR-3) Requires each step to close a named AS-IS↔TO-BE delta (diffable convergence).
**Deps:** US-1, US-2.

### US-6 — Template files  (S=2)
**As** an executor **I want** starter templates **so that** artifacts are schema-conformant on first draft.
**AC-6.1** (→FR-2) `architect/references/templates/as-is-use-cases.md` with the FR-2 schema and a worked stub.
**AC-6.2** (→FR-3, FR-4) `templates/as-is-constraints.yml` and `to-be-constraints.yml` matching the BACKLOG-001 8-field constraints shape.
**AC-6.3** (→FR-5) `templates/roadmap.md` with the 6-field step schema + big-bang check header.
**Deps:** US-3, US-4, US-5.

### US-7 — Dogfood Phase 1A (Claude-Plugins)  (M=3)
**As** the team **I want** Phase 1A executed against this repo **so that** behavioral reconstruction is validated empirically.
**AC-7.1** (→FR-8, AC-2) Produces `.delivery/artifacts/dogfood/transformation-planning/as-is-use-cases.md` with **≥5** use cases.
**AC-7.2** (→FR-2) Every use case carries ≥1 `evidence_citations` pointing to real repo paths (file:line or commit hash).
**AC-7.3** (→FR-2) **≥1** use case carries `confidence=low` with a written reason.
**AC-7.4** (→FR-7) Architecture-board MAR review recorded.
**Deps:** US-2, US-3, US-6.

### US-8 — Dogfood Phases 1B + 2 + 3  (L=4)
**As** the team **I want** structural AS-IS, TO-BE, and roadmap produced against this repo **so that** the full capability is proven.
**AC-8.1** (→FR-3, AC-3) `.delivery/artifacts/dogfood/transformation-planning/as-is-constraints.yml` validates against shared schema; `actions` references US-7 use cases.
**AC-8.2** (→FR-4, AC-4) `to-be-constraints.yml` validates against shared schema; cites volatility golden rule when available.
**AC-8.3** (→FR-5, AC-5) `roadmap.md` lists **≥3** steps, each with all 6 fields, each independently shippable, none exceeding 30% subsystem-change (or <4 collapse, or logged >7 justification).
**AC-8.4** (→AC-7, NFR-2) `validate_constraints.py` exits 0 on both AS-IS and TO-BE outputs; no new required keys added to `.delivery/config.yml`.
**AC-8.5** (→NFR-3) Each roadmap step names the AS-IS↔TO-BE delta it closes (diffable convergence).
**AC-8.6** (forbidden-vocab oracle — TO-BE only) `to-be-constraints.yml` contains zero tokens from `constraints.yml.forbidden_vocabulary`; AS-IS exempt.
**Deps:** US-7, US-4, US-5, US-6.

## Totals
- Stories: **8**; Points: 1+2+3+3+3+2+3+4 = **21 pts**
- All ACs 1:1 traced to FRs / NFRs / Acceptance Criteria.
- Out-of-scope guardrails honored: no BACKLOG-005, no refactor tooling, no live migration, no hallucinated use cases.

## Amendments (merged from Celebrimbor sequencing pass — memory lesson run a1f3)
1. **Dogfood path corrected** to `.delivery/artifacts/dogfood/transformation-planning/` (matches `constraints.yml.mandatory_artifacts`; dispatch prompt's `08-transform/` was a drafting artifact and is overridden).
2. **AC-8.6 added** — forbidden-vocab oracle scoped to TO-BE only (AS-IS may legitimately contain those terms as descriptive evidence).
3. **US-2 promoted to hard prerequisite** of US-3..US-5 — master protocol doc fixes the handoff contract all phase docs depend on.
4. **US-6 held as one story, four files** — templates must land before dogfood as the write-contract between reference docs and dogfood output.
