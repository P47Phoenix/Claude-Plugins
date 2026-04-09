# UAT Test Results — Paired Constraints Primitive

**Stage**: 7 UAT | **Role**: QA Engineer (Legolas) | **Date**: 2026-04-08
**Pipeline**: run-2026-04-08-a1f3 | **Feature**: `constraints.yml`

> *"They're taking the bugs to Isengard!"*
> *(Not on my watch.)*

## Environment

| Item | Value |
|---|---|
| Python | 3.14.3 |
| PyYAML | 6.0.2 (present) |
| CWD | `/var/home/meconnelly/Documents/GitHub/Claude-Plugins` |
| Validator script | `delivery-team/skills/delivery-flow/scripts/validate_constraints.py` |
| DoD checker | `delivery-team/skills/delivery-flow/scripts/check_dod_constraints.py` |

## Test Case Results

Commands abbreviated: `V=validate_constraints.py`, `D=check_dod_constraints.py`, `F=…/fixtures`, `T=…/templates`.

| ID | Description | Command | Expected | Actual | P/F |
|---|---|---|---|---|---|
| TC-FR1-1 | Schema has 8 fields | `yaml.safe_load(T/constraints-architect.yml)` | 8 keys: actions, citations, entities, forbidden_vocabulary, invariants, mandatory_artifacts, numeric_ceilings, state_variables | 8 keys, exact match | PASS |
| TC-FR1-2 | Validator green on valid fixture | `python3 V F/constraints-valid.yml` | exit 0 | exit 0, "ok: … is valid" | PASS |
| TC-FR1-2b | Validator red on missing-entities fixture | `python3 V F/constraints-invalid-missing-entities.yml` | exit 1 | exit 1, "missing required field: entities" | PASS |
| TC-FR1-3 | Forward-compat fixture (unknown field) passes | `python3 V F/constraints-forward-compat.yml` | exit 0 | exit 0 | PASS |
| TC-FR2-1 | Refine template loadable with 8 fields | `yaml.safe_load(T/constraints-refine.yml)` | 8 keys | 8 keys | PASS |
| TC-FR3-1 | Architect template has populated `forbidden_vocabulary` | inspect template | field present, non-empty | present and populated | PASS |
| TC-FR4-1 | "Golden Rule" + "Löwy" in volatility-decomposition.md | `grep -c` | ≥1 each | 1 / 1 | PASS |
| TC-FR5-1 | "Decomposition Hygiene" in strategic-ddd.md (Phases 1–4) | `grep -c` | ≥1 | 4 matches | PASS |
| TC-FR6-1 | "implementation-sequencing" in pipeline-stages.md Stage 5 | `grep -c` | ≥1 | 3 matches (lines 432/433/491) | PASS |
| TC-FR7-1 | `check_dod_constraints.py` exists and runs | `--help` | usage printed | `usage: check_dod_constraints.py <constraints.yml> <artifact_to_check>` | PASS |
| TC-FR7-2a | Clean fixture passes DoD check | `python3 D F/constraints-dod-sample.yml F/dod-artifact-clean.md` | exit 0 | exit 0, all 4 checks pass | PASS |
| TC-FR7-2b | Contaminated fixture fails DoD check | `python3 D F/constraints-dod-sample.yml F/dod-artifact-contaminated.md` | exit 1 | exit 1, 5 forbidden-token hits reported w/ line #s | PASS |
| TC-FR8-1 | Dogfood `constraints.yml` exists at canonical path | `ls .delivery/artifacts/02-refine/po/constraints.yml` | present | 2850 bytes, Apr 8 20:04 | PASS |
| TC-FR8-2 | Dogfood validates against schema | `python3 V .delivery/artifacts/02-refine/po/constraints.yml` | exit 0 | exit 0 | PASS |

**Score: 14/14 executable TCs PASS.**

## Empirically Deferred

| ID | Reason |
|---|---|
| TC-NFR1-1 (NFR-1) | Plan first-try ≥80% target requires 5-run rolling window post-release. Cannot be measured until 5 future real pipeline runs complete and record into `.delivery/memory/stages/plan.md`. Deferred per Stage 5 strategy §4. |
| TC-NFR5-1 (NFR-5) | Refine token delta ≤15% requires longitudinal comparison across future runs. Deferred. |
| TC-NFR2-1 | Forbidden-vocab oracle against new decomposition artifacts — no new decomposition artifact produced in this run (feature is infra/primitive, not a feature that exercises Architect stage). Deferred to first post-release decomposition run. |
| TC-NFR3-1 | Backwards-compat legacy-no-constraints run — mental-model check: script is opt-in; absence of `constraints.yml` results in `experimental.constraints_model: false` code path and no gate fires. Not empirically runnable in this UAT window; design-validated. |

## Known Issues

1. **Stage 6 fixture-data mismatch (RESOLVED in UAT).** Stage 6 qa-sweep reported check 6a deferred because an earlier invocation pattern parsed the artifact as YAML. With the correct argument order (`<constraints.yml> <artifact>`), the clean fixture now passes cleanly (all 4 sub-checks green). Root cause was test-invocation error, not code defect. Stage 6's "fixture-author follow-up" recommendation is downgraded to NO-ACTION.
2. **Rolling-window metrics unmeasurable in single-run UAT.** Documented above as deferred; not blocking.

## Verdict

**GO.**

All 14 empirically-executable test cases PASS. The single Stage 6 deferral is now resolved under correct invocation. Remaining deferred items (NFR-1, NFR-2, NFR-3, NFR-5) are all longitudinal or require future decomposition runs — standard post-release measurement, not blockers.

Schema, validator, DoD checker, reference documentation, dogfood exhibit, and forward-compat all verified. The arrow flies true.

---

*"A red sun rises. Bugs have been shed this morning." — Legolas*

STATUS: DONE
ARTIFACT: .delivery/artifacts/07-uat/qa/test-results.md
SUMMARY: 14/14 PASS, 4 longitudinal TCs deferred, Stage 6 fixture deferral resolved. Verdict: GO.
