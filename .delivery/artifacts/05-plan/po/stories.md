# Stories — Paired Constraints Primitive (`constraints.yml`)

**Stage**: 5 (Plan) | **Role**: Product Owner (Gandalf)
**Pipeline ID**: run-2026-04-08-a1f3
**Date**: 2026-04-08
**Inputs**: PRD FR-1..FR-8, `architecture.md`, ADR-001/002/003, `.delivery/memory/stages/plan.md`

> *"The burden is named. Now we measure it in stones we can carry — no more, no less."*

---

## Capacity Declaration

| Field | Value |
|---|---|
| Team size | 1 |
| Velocity baseline | 5 pts / sprint |
| Ceiling (80% target) | 4 pts / sprint |
| Hard cap (100%) | 5 pts / sprint (never exceed) |
| Work class | Markdown + Schema + Content → estimates one tier lower (memory: run-h3k7) |
| Sprints proposed | **4** |
| Total committed | **17 pts** |

Honesty note: three sprints was a hope; four is the truth. No story exceeds 3 pts; if Sprint Planning re-estimates any higher, split before commit.

> *"A wizard commits precisely when he means to — and no story point later."*

---

## User Stories

### US-1 — `constraints.yml` JSON schema + validator
- **Role**: Orchestrator / DoD validators
- **Goal**: load and rule-check any `constraints.yml` against a canonical schema
- **Value**: deterministic gate decisions; zero AI variance on structure
- **Acceptance Criteria**:
  - AC-1.1 JSON Schema defines exactly 8 top-level fields (`entities`, `state_variables`, `actions`, `numeric_ceilings`, `mandatory_artifacts`, `invariants`, `forbidden_vocabulary`, `citations`) ⇒ **PRD FR-1, AC-1**
  - AC-1.2 `entities` and `invariants` required; remainder optional ⇒ **PRD FR-1**
  - AC-1.3 Validator exits non-zero on missing required fields ⇒ **PRD FR-1 invariant check**
  - AC-1.4 Schema is forward-compatible: additional top-level fields in a future `constraints.yml` are ignored rather than rejected by the validator ⇒ **PRD FR-1 extensibility**
- **Estimate**: 3 pts
- **Depends on**: none
- **DoD**: schema under `delivery-team/skills/delivery-flow/references/`; validator headless; red/green fixtures pass

### US-2 — `constraints-model-guide.md` authoring canon
- **Role**: PO/Architect sub-agents
- **Goal**: one guide explaining every field + required/optional markers
- **Value**: consistent authorship across Refine and Architect
- **Acceptance Criteria**:
  - AC-2.1 Guide documents all 8 fields with type + required/optional + example ⇒ **PRD FR-1, AC-1**
  - AC-2.2 Guide cross-links Löwy golden rule for `citations` ⇒ **PRD FR-3, AC-4**
- **Estimate**: 2 pts
- **Depends on**: US-1
- **DoD**: guide under `delivery-flow/references/`; linked from PRD dependency list

### US-3 — Refine-stage PO constraints template + invocation
- **Role**: PO sub-agent at Refine
- **Goal**: emit `constraints.yml` with problem-scoped content as part of Refine
- **Acceptance Criteria**:
  - AC-3.1 Template instantiates all 8 fields with Refine-scoped guidance ⇒ **PRD FR-2**
  - AC-3.2 `pipeline-stages.md` Refine invocation updated to require `constraints.yml` artifact ⇒ **PRD FR-2**
  - AC-3.3 Sample emission passes US-1 validator ⇒ **PRD FR-2 invariant check**
- **Estimate**: 2 pts
- **Depends on**: US-1, US-2
- **DoD**: template + invocation update shipped; sample validated

### US-4 — Architect-stage decomposition template + invocation
- **Role**: Architect sub-agent
- **Goal**: emit `constraints.yml` with volatility/DDD-scoped content
- **Acceptance Criteria**:
  - AC-4.1 Template instantiates 8 fields with Architect-scoped content ⇒ **PRD FR-3**
  - AC-4.2 `forbidden_vocabulary` pre-populated with enumerated list (`lambda, ecr, sqs, ec2, s3, dynamodb, kafka, python, node, typescript, golang`) ⇒ **PRD FR-3, NFR-2, AC-3**
  - AC-4.3 `citations` requires Löwy reference when volatility strategy selected ⇒ **PRD FR-3, AC-4**
- **Estimate**: 2 pts
- **Depends on**: US-1, US-2
- **DoD**: template + invocation update shipped; sample emission validated; token list locked

### US-5 — `volatility-decomposition.md` §0 Golden Rule insertion
- **Role**: Architect reader
- **Goal**: see Löwy's rule stated as a rule at the top of the reference
- **Acceptance Criteria**:
  - AC-5.1 New §0 "The Golden Rule" — Löwy, *Righting Software* Ch. 2, verbatim ⇒ **PRD FR-4, AC-4**
  - AC-5.2 Functional-decomposition-trap anti-pattern with worked example ⇒ **PRD FR-4 (Gap 1)**
- **Estimate**: 1 pt
- **Depends on**: none
- **DoD**: edit landed; no prose regressions

### US-6 — `strategic-ddd.md` Decomposition Hygiene sidebar
- **Role**: Architect reader (DDD path)
- **Goal**: equivalent "no implementation nouns" guardrail across DDD phases
- **Acceptance Criteria**:
  - AC-6.1 Sidebar threaded into Phases 1–4 prohibiting cloud services/runtimes/languages ⇒ **PRD FR-5 (Gap 2 DDD parity)**
  - AC-6.2 Bounded-context integrity rules added ⇒ **PRD FR-5**
- **Estimate**: 1 pt
- **Depends on**: none
- **DoD**: sidebar present in all four phases

### US-7 — Architect-in-Plan integration (`pipeline-stages.md`)
- **Role**: Orchestrator
- **Goal**: invoke Architect in Stage 5 Plan per ADR-002
- **Acceptance Criteria**:
  - AC-7.1 New invocation step between Plan steps 1 and 3, `task_type: implementation-sequencing` ⇒ **PRD FR-6, ADR-002**
  - AC-7.2 Output `.delivery/artifacts/05-plan/architect/sequencing.md` declared ⇒ **PRD FR-6, AC-5**
  - AC-7.3 Architect listed as participant (not owner) of Stage 5 ⇒ **PRD FR-6 (Gap 3)**
- **Estimate**: 2 pts
- **Depends on**: US-1
- **DoD**: `pipeline-stages.md` updated; dry-run orchestrator loads new step

### US-8 — DoD validator deterministic constraint checks
- **Role**: DoD validators (Plan + Architect)
- **Goal**: at least one rule-based check against `constraints.yml` per gate
- **Acceptance Criteria**:
  - AC-8.1 Forbidden-vocabulary grep blocks DoD on match ⇒ **PRD FR-7, AC-3, NFR-2**
  - AC-8.2 Mandatory-artifact presence check ⇒ **PRD FR-7**
  - AC-8.3 Numeric-ceiling compliance check ⇒ **PRD FR-7**
  - AC-8.4 Missing Löwy citation on volatility artifact fails DoD ⇒ **PRD FR-7, AC-4**
- **Estimate**: 3 pts
- **Depends on**: US-1, US-4
- **DoD**: validator integrated into `dod_validators` path; red/green fixtures; no new required `config.yml` key (NFR-4)

### US-9 — Dogfood: emit this PRD's own `constraints.yml`
- **Role**: Exhibit A
- **Goal**: ship `.delivery/artifacts/02-refine/po/constraints.yml` that passes all checks in UAT
- **Acceptance Criteria**:
  - AC-9.1 File exists at exact path ⇒ **PRD FR-8, AC-7**
  - AC-9.2 Passes US-1 schema validator ⇒ **PRD FR-8**
  - AC-9.3 Passes US-8 deterministic DoD checks during UAT ⇒ **PRD FR-8, AC-7 (P0 dogfood)**
  - AC-9.4 Dogfood run includes explicit installed-cache refresh step (source → cache sync) before validation, preventing stale-cache masking of source edits ⇒ **PRD FR-8, memory hot lesson #4**
- **Estimate**: 1 pt
- **Depends on**: US-1, US-2, US-3, US-8
- **DoD**: file committed; UAT run green; memory lesson "no DoD before dogfood" honored

---

## Sprint Allocation

| Sprint | Stories | Points | % of 5-pt cap |
|---|---|---|---|
| **S1 — Foundations** | US-1 (3), US-5 (1) | **4** | 80% target ✅ |
| **S2 — Guides & Templates** | US-2 (2), US-6 (1), US-4 (2) | **5** | 100% hard cap ⚠ |
| **S3 — Integration** | US-3 (2), US-7 (2) | **4** | 80% target ✅ |
| **S4 — Validators & Dogfood** | US-8 (3), US-9 (1) | **4** | 80% target ✅ |

**Total: 17 pts / 4 sprints.** S2 rides the hard cap — watch it. If S1 slips, pull US-6 from S2 into S3 (trivially re-orderable — no dependency).

---

## Cross-Cutting Risks (emergent from breakdown)

- **CR-1** US-8 relies on US-4's enumerated token list — lock the list in US-4 DoD or US-8 re-opens.
- **CR-2** US-9 cannot begin until US-1/2/3/8 are green; schedule last in S4.
- **CR-3** US-3 and US-7 both edit `pipeline-stages.md` — coordinate across S3 to avoid merge collisions.
- **CR-4** NFR-5 token delta (≤15%) is a post-land measurement — Data Analyst owns it at UAT, not per-sprint.

---

## Out of Scope Reminder

No BACKLOG-003, BACKLOG-005, BACKLOG-006. No `config.yml` v2.7→v2.8 bump (PRD §6 — earned only after the primitive survives both domains).

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/po/stories.md
SUMMARY: Nine stories, 17 pts across 4 sprints (honest recalibration from 3). All ACs traced 1:1 to PRD FR-1..FR-8. No sprint over 5-pt hard cap. patched round 2 — +AC-1.4 +AC-9.4
