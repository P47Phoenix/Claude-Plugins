# Retrospective: Clean Code Foundational Standards (FEATURE)

**Pipeline Run:** run-2026-03-27-c8f2
**Date:** 2026-03-27
**Facilitator:** Scrum Master
**Type:** FEATURE
**Stages Completed:** 7/7 (Idea, Refine, Design, Architect-Light, Plan, Dev, UAT)
**Human Checkpoints:** 2 (Refine, UAT)
**Self-Correction Rounds:** 5 total across 4 stages
**Defects:** 0 | **Failed Tests:** 0 | **CODE_COMPLETE:** 14

---

## Continue Doing

1. **PO pre-pipeline session producing structured requirements.** The PO session before pipeline start meant Idea stage needed minimal rework. This front-loading of clarity paid off across every downstream stage. Keep this pattern for all FEATURE-type work.

2. **Self-correction loops catching real issues.** Every self-correction round found legitimate gaps -- missing FR mappings, capacity declarations, stale schema, dogfooding gaps. The system worked as designed: validators caught what producers missed.

3. **Dogfooding as a UAT gate.** The 51 findings across 18 Python files would have shipped as latent debt without the dogfooding requirement. Enforcing "run the code on the codebase" before UAT sign-off is the single highest-value quality gate.

4. **Cross-role validation catching blind spots.** PO caught design gaps, SM caught plan gaps, Architect caught dev gaps. Each role found issues the producing role missed, validating the multi-perspective review model.

5. **Immediate issue creation for discovered bugs.** The alias injection bug (issue #50) and prd-quality-gate-flow refactoring items (#51-53) were filed as GitHub issues during the pipeline rather than lost in notes. This keeps the backlog honest.

---

## Start Doing

1. **Run schema/artifact generation scripts as part of dev DoD, not post-hoc.** The config-schema.json staleness was caught by Architect review, but the generate script should be in the dev checklist, not discovered during validation. **Action: Add "regenerate derived artifacts" to dev stage DoD checklist.**

2. **Include hook_utils.py and shared utility modules in review scope explicitly.** Shared modules were missed in UAT review scope -- they need to be called out as first-class review targets when the changeset touches them. **Action: Add shared-module review checkpoint to UAT stage.**

3. **Smoke-test alias/personality injection on every alias-related change.** The Gandalf bug sat undetected until PO manually tested mid-pipeline. A quick "invoke alias, check for personality markers" test should be standard. **Action: Add alias smoke-test to alias-creator skill's validation section.**

4. **Declare capacity and test coverage expectations at Plan stage start, not after SM review.** SM had to request capacity declaration and QA had to flag FR-14/FR-15 test gaps. These should be mandatory Plan stage inputs. **Action: Update Plan stage template to require capacity + coverage matrix upfront.**

---

## Stop Doing

1. **Stop treating dogfooding as optional or deferrable.** UAT round 1 failed because dogfooding was not done and docs were not applied. The team knew dogfooding was required but deferred it. Dogfooding is not a nice-to-have -- it is the UAT stage. Stop treating it as a follow-up task.

2. **Stop assuming derived artifacts are current.** The schema.json staleness was a process failure, not a code failure. Stop relying on memory to regenerate derived files. Either automate generation or add explicit checklist items.

3. **Stop scoping reviews narrowly when the changeset is broad.** hook_utils.py was missed because the review focused on the "primary" files. When a feature touches shared infrastructure, the review scope must expand to match. Stop reviewing only the files that were explicitly changed.

---

## Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| Stages completed | 7/7 | On target |
| Self-correction rounds | 5 | Acceptable for a foundational feature |
| Defects escaped to UAT | 0 | Strong |
| Dogfooding findings | 51 across 18 files | High value -- validates the gate |
| GitHub issues created | 4 | Good backlog hygiene |
| UAT rounds needed | 2 | One too many -- dogfooding skip caused it |
| Human checkpoint rejections | 0 | Clean passes |

---

## Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Add "regenerate derived artifacts" to dev stage DoD checklist | Scrum Master | 2026-04-01 |
| 2 | Add shared-module review checkpoint to UAT stage instructions | Scrum Master | 2026-04-01 |
| 3 | Add alias smoke-test to alias-creator skill validation section | Developer | 2026-04-03 |
| 4 | Update Plan stage template to require capacity + coverage matrix as mandatory inputs | Scrum Master | 2026-04-01 |
| 5 | Fix alias personality injection bug (issue #50) | Developer | 2026-04-03 |
| 6 | Triage prd-quality-gate-flow refactoring issues #51-53 | Product Owner | 2026-04-01 |

---

## Lessons for Memory System

1. **Pre-pipeline PO sessions reduce downstream churn.** When requirements are structured before Idea stage, self-correction rounds drop at early stages. Store as a recommended pattern for FEATURE-type work.

2. **Derived artifacts need explicit regeneration steps.** Any file generated from a source (schema from markdown, docs from code) will go stale silently. Pipeline must treat regeneration as a build step, not a manual memory item.

3. **Dogfooding finds categories of issues that code review cannot.** 51 findings across 18 files -- code review alone would not have caught import inconsistencies, dead code, and style drift at this volume. Dogfooding is non-negotiable for broad refactoring work.

4. **Review scope must match changeset scope.** When a feature touches shared utilities, the review checklist must explicitly enumerate shared modules. Narrow review scope on broad changesets creates systematic blind spots.

5. **Personality/behavioral features need behavioral tests.** The alias injection bug was only found by manual invocation. Features that change runtime behavior (not just structure) need a "try it" validation step in addition to code review.
