# UAT Test Plan — Orchestration Discipline Bundle

**QA**: Legolas
**Stage**: 07 — UAT
**Scope**: FEATURE bundle covering issues #73, #71, #70, #69 plus FR-16 doc parity
**Inputs reviewed**: PRD (16 FRs, 8 NFRs), stories (OD-01..OD-13), dev notes (OD-all.md, R1+R2+R3), `delivery-flow/SKILL.md`

> *"A bowstring sings true only when every strand is whole. I will pluck each strand."* — Legolas

---

## 1. Objectives

Validate that the Orchestration Discipline Bundle:

1. Removes `project_type` from active config (v2.7) while tolerating legacy v2.6 configs.
2. Forces Phase 1 detection on every pipeline invocation.
3. Honors `routing.force_type` as the only supported pin.
4. Enforces the Delegation Prime Directive in SKILL.md (anti-patterns, Step 4.5, rejected justifications).
5. Implements layered orchestrator-origin detection in `enforce_pipeline_scope.py` with documented gaps.
6. Enforces "One Role = One Sub-Agent" across `team-patterns.md`, `quality-gates.md`, and `pipeline-stages.md`.
7. Documents the Isolated Adversarial Loop (Pattern 2b) with taxonomy, three convergence rules, and pseudocode.
8. Achieves doc parity across `CLAUDE.md`, `README.md`, `delivery-team/README.md`, `marketplace.json`, `docs/**`.
9. Dogfoods the discipline: this very pipeline run shows zero orchestrator self-writes to artifact paths.

## 2. Scope

**In scope**: SKILL.md, `references/{config-schema.md,setup-wizard.md,project-types.md,team-patterns.md,quality-gates.md,pipeline-stages.md}`, `config-schema.json`, `enforce_pipeline_scope.py`, `audit_agent_prompt.py`, `CLAUDE.md`, `README.md`, `delivery-team/README.md`, `.claude-plugin/marketplace.json`, `docs/user-guide/config.md`, `docs/skills/delivery-flow.md`, `docs/contributing/index.md`.

**Out of scope** (per PRD §6 and dev notes): Bash-redirection bypass closure; centralized sub-agent dispatch wrapper; non-Architect adversarial loops; new alias themes; default value changes for `max_self_correction`.

## 3. Test Categories & Coverage Map

| # | Category | FRs covered | Stories | Test cases |
|---|----------|-------------|---------|-----------|
| 1 | Config migration (project_type removal, v2.6 to v2.7 tolerance) | FR-01, FR-02, FR-16, NFR-03 | OD-07, OD-08 | TC-01..TC-06 |
| 2 | Phase 1 always-detect | FR-03 | OD-01, OD-02 | TC-07..TC-09 |
| 3 | `routing.force_type` override | FR-02, FR-05 | OD-07, OD-11 | TC-10..TC-12 |
| 4 | Delegation enforcement (anti-patterns + Step 4.5) | FR-06, FR-07, FR-08 | OD-03, OD-05, OD-06 | TC-13..TC-18 |
| 5 | Origin detection layers (`enforce_pipeline_scope.py`) | FR-09, NFR-02, NFR-05 | OD-13 | TC-19..TC-25 |
| 6 | One-role-per-sub-agent | FR-10, FR-11, FR-12 | OD-04, OD-10, OD-12, OD-13 | TC-26..TC-31 |
| 7 | Isolated Adversarial Loop protocol | FR-13, FR-14, FR-15 | OD-12, OD-13 | TC-32..TC-37 |
| 8 | Documentation parity | FR-16, NFR-04 | OD-13 (R2 sweep) | TC-38..TC-43 |
| 9 | Dogfooding self-test | NFR-06 | (entire run) | TC-44..TC-46 |
| 10 | Shared-module SKILL.md review | cross-cutting | OD-01..OD-06 | TC-47..TC-50 |

Total: **50 test cases**.

## 4. Approach

- **Primary technique**: documentation/static review (grep, diff, structural inspection). The repo has no test runner per CLAUDE.md, so executable tests are limited to standalone Python invocations and shell harnesses.
- **Secondary**: synthetic-fixture hook execution — feed crafted JSON into `enforce_pipeline_scope.py` and `audit_agent_prompt.py` via stdin to verify Layer 1/2/3 behavior and negation handling.
- **Tertiary**: dogfood inspection — examine the actual `.delivery/artifacts/**` git history of THIS run for orchestrator-attributed writes.

## 5. Entry Criteria

- All OD-01..OD-13 stories marked complete in `06-dev/developer/OD-all.md`.
- Round 2 + Round 3 self-corrections folded in (D-01, M-01, M-04, M-05, D2-01, D2-02, SKILL.md line 1051 fix).
- Schema generator regenerated `config-schema.json` from v2.7 markdown.
- Hook files pass `python3 -m py_compile` / `ast.parse`.

## 6. Exit Criteria (DoD)

- All P0 tests pass (TC-01..TC-25, TC-32..TC-37, TC-38..TC-46).
- Zero unresolved P0/P1 defects.
- Doc-parity grep clean: no live `project_type` references outside Deprecated Keys / Version History / ADR sections.
- Wizard question count consistent at **9** across SKILL.md, setup-wizard.md, CLAUDE.md, README.md, delivery-team/README.md.
- `enforce_pipeline_scope.py` module docstring documents all three known gaps; `quality-gates.md` mirrors them.
- Delegation Meta-Gate present in `quality-gates.md`.
- Dogfood evidence: the `.delivery/artifacts/**` writes for this run carry sub-agent attribution (or, where the activation gate is still v2.6, orchestrator-attributed writes are exempted by design — documented).

## 7. Risk-Based Prioritization

| Risk | Source | Test focus |
|------|--------|------------|
| Origin detection unreliable on a new harness (R6) | PRD section 7 | TC-19..TC-25 (all three layers, plus negative env var case) |
| Architect loops never converge (R3) | PRD section 7 | TC-32..TC-37 — verify all 3 convergence rules documented + pseudocode |
| Hook over-blocks `state.md` (R1) | PRD section 7 | TC-22 allowlist exhaustive coverage |
| Doc-parity drift (R5) | PRD section 7 | TC-38..TC-43 grep sweep across the 8 listed files |
| Wizard renumbering inconsistency (history of R1/R2/R3 churn) | dev notes | TC-04, TC-05, TC-49 |
| Compound-role detector false positives on negation (M-05) | R2 fix | TC-29 negation guard |

## 8. Shared-Module Review — `SKILL.md`

`delivery-flow/SKILL.md` is the entry point referenced (directly or by convention) by every other delivery-team skill. Six structural assertions covered by TC-47..TC-50:

1. Delegation Prime Directive section is the first prose block after metadata (FR-06).
2. Step 4.5 contains the rejection clause and links to "Common Orchestrator Anti-Patterns" (FR-07).
3. Common Orchestrator Anti-Patterns section enumerates >=6 patterns with name/description/correct alternative (FR-08); dev notes claim 8 patterns — verify.
4. "One Role = One Sub-Agent" rule block sits adjacent to the Delegation Prime Directive and is referenced by name from `team-patterns.md`, `quality-gates.md`, `pipeline-stages.md` (FR-10, FR-11).
5. Phase 0 no longer mentions skipping Phase 1 from config; Phase 1 header note states "every pipeline invocation" (FR-03, OD-01, OD-02).
6. Wizard count says **9 questions** (single source of truth, line 1051 fix verified).

## 9. Defect Handling

- P0 = blocks merge. Route to dev-stage retro immediately; PR cannot ship.
- P1 = ship-blocker unless explicit waiver from PO + Architect.
- P2/P3 = log to `.delivery/defects/` and surface in retrospective; ship allowed.
- All defects must reference the failing TC ID and the specific FR/AC violated.

## 10. Schedule

UAT executes in a single pass (this is a docs/hooks bundle, no long-running test infra). Estimated effort: ~1 hour for the full 50 cases by a single QA. Re-run on each fix round.

## 11. Deliverables

- This test plan (`07-uat/qa/test-plan.md`).
- Test cases (`07-uat/qa/test-cases.md`).
- UAT execution report appended after dry run (separate file, not in this plan's scope).

---

*"The arrow flies straight only because the bow knows its tension. Fifty strands, fifty checks. None will be left untested."* — Legolas
