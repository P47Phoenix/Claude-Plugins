# UAT Test Plan — Paired Constraints Primitive

**Stage**: 7 UAT | **Role**: QA Engineer (Legolas) | **Date**: 2026-04-08
**Pipeline**: run-2026-04-08-a1f3 | **Feature**: `constraints.yml` primitive

> *"One does not simply ship without measuring."*

Note: co-located with `test-plan.md` (different feature bundle — Orchestration Discipline). This plan scopes only the Paired Constraints Primitive feature.

## Scope

All 24 test cases are already authored in Stage 5 strategy. This UAT executes them empirically; no new TCs.

Source of truth: `.delivery/artifacts/05-plan/qa/test-strategy.md`

## Execution Environment

- Working dir: `/var/home/meconnelly/Documents/GitHub/Claude-Plugins`
- Tooling: `python3` 3.14.3, PyYAML 6.0.2, `grep`
- Target scripts: `delivery-team/skills/delivery-flow/scripts/validate_constraints.py`, `check_dod_constraints.py`
- Fixtures: `delivery-team/skills/delivery-flow/references/fixtures/`
- Templates: `delivery-team/skills/delivery-flow/references/templates/`
- Dogfood artifact: `.delivery/artifacts/02-refine/po/constraints.yml`

## Execution Strategy

1. Re-run Stage 6 qa-sweep empirical checks as regression baseline.
2. Execute net-new TCs not covered in Stage 6 (forward-compat, refine template, dogfood schema validation, DoD clean-case with correct script arg order).
3. Mark longitudinal NFRs (NFR-1, NFR-5) as **empirically deferred** per Stage 5 strategy §4.
4. Verify Stage 6 fixture-mismatch deferral status.
5. Produce verdict: GO / CONDITIONAL / NO-GO.

## Deliverable

- `.delivery/artifacts/07-uat/qa/test-results.md` — full pass/fail table, deferrals, known issues, verdict.
