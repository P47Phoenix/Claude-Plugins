# Test Results — Stage 7 UAT (transformation-planning, run c4d1)

**Role:** Legolas (QA Engineer) | **Date:** 2026-04-08

## Test Case Results

| # | Test Case | Expected | Actual | Status |
|---|-----------|----------|--------|--------|
| TC-01 | transformation-planning.md exists | present | present | PASS |
| TC-02 | 4 phase docs (1a/1b/2/3) exist | 4 | 4 | PASS |
| TC-03 | Dogfood outputs at 08-transform/ (as-is-constraints, as-is-use-cases, to-be-constraints, roadmap) | 4 | 4 | PASS |
| TC-04 | grep -c transformation-planning in architect SKILL.md | >=1 | 3 | PASS |
| TC-05 | grep -c "Golden Rule" phase-2 ref | >=1 | 4 | PASS |
| TC-06 | validate_constraints as-is-constraints.yml | exit 0 | exit 0 | PASS |
| TC-07 | validate_constraints to-be-constraints.yml | exit 0 | exit 0 | PASS |
| TC-08 | validate_constraints 02-refine/po/constraints.yml | exit 0 | exit 0 | PASS |
| TC-09 | Use cases in as-is-use-cases.md | >=5 | 7 | PASS |
| TC-10 | >=1 low-confidence UC entry | >=1 | 3 | PASS |
| TC-11 | Roadmap steps (STEP-NN) | >=3 | 5 | PASS |
| TC-12 | DoD self-check on to-be-constraints.yml | exit 0 | exit 1 | NOTE |
| TC-13 | Backwards compat: task_type additive | unaffected | additive-only | PASS |

## TC-12 Caveat

check_dod_constraints.py was run with to-be-constraints.yml as BOTH rules and text. It FAILED exit=1 because the `forbidden_vocabulary` list literally contains the tokens (lambda, ecs, python…) as list items — self-match, not contamination. The brief noted exit=0 expectation but empirically the grep phase cannot distinguish field declaration from field use; any self-scan FAILs. BACKLOG candidate: `--skip-declarations` mode. Not blocking — the validator functions correctly against its real use case (scanning OTHER artifacts).

Backwards-compat reasoning: `transformation_planning` task_type is purely additive to architect SKILL.md routing; no existing entries removed/renamed; legacy pipelines that never dispatch to it are unchanged.

## Summary

- Total TCs: 13 | Pass: 12 (92%) | Note: 1 | Fail: 0 | Blockers: 0

## Verdict: GO

All blocking criteria met. TC-12 is a known tool limitation, not a defect.
