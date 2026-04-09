# Test Strategy — BACKLOG-006 transformation-planning
**Role:** Legolas (QA)
**Stage:** 05-plan
**Pipeline:** run-2026-04-09-c4d1

## Approach
Mix of **static** (file-exists, grep, schema-validate) and **empirical** (dogfood content assertions). Static runs in CI; empirical runs on dogfood artifacts and gates dogfood stories' DoD.

## Traceability Matrix

| FR/NFR/AC | Story | Test | Type | Oracle |
|---|---|---|---|---|
| FR-1 / AC-1 | US-1 | T-1.1 | static-grep | `delivery-team/skills/architect/SKILL.md` contains `transformation-planning` in task_type list |
| FR-1 | US-1 | T-1.2 | static-grep | Entry names PO + Architect ownership |
| FR-6 | US-2 | T-2.1 | file-exists | `architect/references/transformation-planning.md` |
| FR-6 | US-2 | T-2.2 | static-grep | Contains "legacy trigger" + "default ON" + "logged justification" |
| FR-7 | US-2 | T-2.3 | static-grep | Links to all four phase reference docs |
| FR-2 | US-3 | T-3.1 | file-exists | `transformation-phase-1a-behavioral.md` |
| FR-2 | US-3 | T-3.2 | static-grep | All 7 use-case fields: actor, goal, preconditions, main_flow, variations, evidence_citations, confidence |
| FR-2 | US-3 | T-3.3 | static-grep | Evidence sources: tests, UI, endpoints, commits, docs, telemetry |
| FR-7 | US-3 | T-3.4 | static-grep | MAR trio named: code archaeologist, user advocate, skeptical tester |
| FR-3 | US-4 | T-4.1 | file-exists | `transformation-phase-1b-structural.md` |
| FR-3 | US-4 | T-4.2 | static-grep | 4-element Model-First mapping: entities/state/actions/constraints |
| FR-3 | US-4 | T-4.3 | static-grep | `actions` consumes Phase 1A use cases |
| FR-4 | US-5 | T-5.1 | file-exists | `transformation-phase-2-to-be.md` |
| FR-4 | US-5 | T-5.2 | static-grep | Volatility golden rule citation requirement mentioned |
| FR-5 | US-5 | T-5.3 | file-exists | `transformation-phase-3-roadmap.md` |
| FR-5 | US-5 | T-5.4 | static-grep | All 6 step fields: scope, ordering_rationale, reversibility, risk, incremental_value, preserved_invariants |
| FR-5 / ADR-002 | US-5 | T-5.5 | static-grep | 30% threshold + <4 collapse + >7 justification escape |
| FR-2 | US-6 | T-6.1 | file-exists | `templates/as-is-use-cases.md` |
| FR-3, FR-4 | US-6 | T-6.2 | file-exists | `templates/as-is-constraints.yml` + `to-be-constraints.yml` |
| FR-3, FR-4, NFR-1 | US-6 | T-6.3 | schema-validate | Templates validate against BACKLOG-001 8-field shape |
| FR-5 | US-6 | T-6.4 | file-exists | `templates/roadmap.md` with 6-field step schema |
| FR-8 / AC-2 | US-7 | **T-7.1 (empirical)** | count | `as-is-use-cases.md` has **≥5** use-case entries |
| FR-2 | US-7 | **T-7.2 (empirical)** | grep-per-entry | Every use case has ≥1 `evidence_citations` with real repo path |
| FR-2 / AC-2 | US-7 | **T-7.3 (empirical)** | confidence-check | **≥1** entry `confidence: low` with non-empty reason |
| FR-7 | US-7 | T-7.4 | file-exists | MAR review record present |
| FR-3 / AC-3 / NFR-1 | US-8 | T-8.1 | schema-validate | `validate_constraints.py` exits 0 on `as-is-constraints.yml`; `actions` references US-7 IDs |
| FR-4 / AC-4 / NFR-1 | US-8 | T-8.2 | schema-validate | `validate_constraints.py` exits 0 on `to-be-constraints.yml`; cites volatility golden rule |
| FR-5 / AC-5 | US-8 | **T-8.3 (empirical)** | step-count + field-check | `roadmap.md` ≥3 steps, all 6 fields present |
| FR-5 / ADR-002 | US-8 | **T-8.4 (empirical)** | big-bang math | Per step: `touched/total ≤ 0.30` OR (`total<4` AND `touched≤1`) OR (`step_count>7` AND header justification) |
| NFR-3 | US-8 | **T-8.5 (empirical)** | diff-convergence | Each step names an AS-IS↔TO-BE delta present in both models |
| AC-7 / NFR-2 | US-8 | T-8.6 | config-diff | No new required keys in `.delivery/config.yml`; schema remains v2.7 compatible |
| forbidden_vocab | US-8 | **T-8.7 (empirical)** | vocab oracle | `to-be-constraints.yml` contains **zero** tokens from `forbidden_vocabulary` (case-insensitive whole-word). **AS-IS exempt.** |
| NFR-2 | US-8 | T-8.8 | backwards-compat | Existing pipelines still run; no breaking change to architect SKILL.md surface |

## Empirical vs Static Summary
- **Static:** T-1.1, T-1.2, T-2.*, T-3.*, T-4.*, T-5.*, T-6.*, T-7.4, T-8.1, T-8.2, T-8.6, T-8.8 — runnable in CI pre-dogfood.
- **Empirical:** **T-7.1, T-7.2, T-7.3, T-8.3, T-8.4, T-8.5, T-8.7** — require real dogfood output; gate the dogfood stories' DoD.

## Forbidden-Vocabulary Oracle Scope
Applies **only** to TO-BE (`to-be-constraints.yml` + any TO-BE rationale). AS-IS is exempt: legacy systems may legitimately *be* e.g. a "layered monolith" and forbidding the word would force euphemism and destroy evidence fidelity. TO-BE is design space where the ban enforces paradigm-neutral Model-First reasoning (per citations in constraints.yml: Model-First Reasoning arXiv:2512.14474).

## Risks
- **R-QA-1** Dogfood scope choices may miss thin-evidence areas → MAR review (T-7.4) forces skeptical pass.
- **R-QA-2** `validate_constraints.py` must exist and be current; if not, T-6.3/T-8.1/T-8.2 degrade to manual schema-conformance review.
