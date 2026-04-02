# User Stories: Pipeline Integrity Fixes

**Version**: 1.0
**Date**: 2026-04-01
**Author**: Product Owner (Gandalf)
**Source Issues**: #54, IA-1 (retro r4x2), IA-4 (retro r4x2)
**Pipeline**: BUG_FIX (Light Plan)

> "The pipeline that governs our craft must itself be governed with equal rigor."

---

## US-01: Enforce Pipeline Integrity Rules for Branch Strategy, Confidence Scoring, and Architect Routing

### Story Statement

**As a** delivery pipeline user,
**I want** the pipeline to enforce its documented rules for branch isolation, confidence scoring limits, and architect involvement in refactoring,
**So that** commits never silently land on the default branch when feature branching is configured, confidence scores honestly reflect evidence quality, and structural refactoring decisions receive appropriate architect review.

### Priority: P1

### Acceptance Criteria

#### AC Group 1: Branch Strategy Enforcement (#54)

**File: `delivery-team/skills/delivery-flow/SKILL.md`** (stage step instructions)

- **AC-1.1**: Stage 5 (Plan) sub-flow contains a step (Step 8 or equivalent) that, when `git.branch_strategy` is set to a branching strategy (not `none`) AND `git.auto_branch` is `true`, directs the orchestrator to create a feature branch per the rules in `references/git-integration.md`. The step must explicitly reference `references/git-integration.md` by name.
- **AC-1.2**: Stage 6 (Development) sub-flow contains a directive (within the commit suggestion step or as a new step) stating: "All commits during Development MUST target the feature branch created at Plan. Do NOT commit directly to the base branch (`main` or `develop`)." The directive must reference `references/git-integration.md` by name.
- **AC-1.3**: Stage 7 (UAT) sub-flow contains a step (at Step 8 or equivalent) that, when `github.create_pr` is `true`, directs the orchestrator to create a pull request from the feature branch to the base branch. The step must reference `references/git-integration.md` by name.

**File: `delivery-team/skills/delivery-flow/references/git-integration.md`**

- **AC-1.4**: The "Pipeline Integration Points" section for Stage 5 includes an enforcement note stating that branch creation is MANDATORY (not optional) when `git.auto_branch: true` and `git.branch_strategy` is not `none`. Failure to create the branch is a blocking error that halts the pipeline.
- **AC-1.5**: A new "Stage 6 (Development) -- Branch Enforcement" subsection exists within "Pipeline Integration Points" stating that all commits must target the feature branch (not the base branch). If no feature branch exists in `.delivery/state.md` and `git.auto_branch` was `true`, this is a blocking error indicating Plan did not execute correctly.
- **AC-1.6**: The "Stage 7 (UAT)" subsection within "Pipeline Integration Points" includes PR creation directives: when `github.create_pr` is `true`, create a PR from the feature branch to the base branch. The PR body must include the sprint goal, stories implemented with "Closes #N" references, and UAT test results.

#### AC Group 2: Confidence Cap for Structural-Only Validation (IA-1)

**File: `delivery-team/skills/delivery-flow/references/quality-gates.md`**

- **AC-2.1**: Gate 7 (UAT Acceptance) contains a new criterion (blocking severity) stating: "When empirical validation cannot be performed (e.g., bash unavailable, no runtime environment, no test framework accessible), review board confidence scores are capped at a maximum of 4/5. A score of 5/5 requires empirical evidence (test execution, runtime verification, or observable behavior confirmation)."
- **AC-2.2**: Gate 7 contains a second new criterion (blocking severity) stating: "When confidence is capped due to inability to perform empirical validation, the DoD artifact must include an explicit 'Empirical Validation Limitation' section documenting: (a) which acceptance criteria could not be empirically validated, (b) what prevented empirical validation, and (c) the residual risk of shipping without empirical evidence."
- **AC-2.3**: The existing "Empirical-items classification" criterion in Gate 7 remains unchanged. The new confidence cap criteria supplement (not replace) it.

#### AC Group 3: Refactoring Sub-Type for FEATURE Routing (IA-4)

**File: `delivery-team/skills/delivery-flow/references/project-types.md`**

- **AC-3.1**: The FEATURE detection section includes "refactoring" as a recognized sub-type with signals: "refactor", "decompose", "extract module", "split class", "restructure", "reorganize modules", "break apart", "modularize".
- **AC-3.2**: The "Light-or-Skip Decision Logic (FEATURE at Architect Stage)" section's "Apply Light" list includes a new bullet: "Module decomposition, boundary changes, or architectural restructuring (refactoring sub-type)" -- making these changes route to Architect-light instead of potentially hitting Architect-skip.
- **AC-3.3**: The "Apply Skip" list's existing condition "Contained within a single service or module" includes a qualifying clause: "AND does not involve module decomposition, boundary changes, or architectural restructuring."
- **AC-3.4**: Existing FEATURE detection signals and routing for non-refactoring FEATURE projects remain unchanged. No existing Skip conditions are removed -- only narrowed by the refactoring qualifier.

---

### Test Cases

All test cases follow a dogfooding approach: verify by reading the modified files and confirming the specific text changes exist and are correctly placed.

#### TC-1: Branch Enforcement in SKILL.md (covers AC-1.1, AC-1.2, AC-1.3)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read `SKILL.md` Stage 5 (Plan) sub-flow | A step exists that directs feature branch creation when `git.auto_branch: true` and `git.branch_strategy` is not `none`. Step references `references/git-integration.md` by name. |
| 2 | Read `SKILL.md` Stage 6 (Development) sub-flow | A directive exists stating commits MUST target the feature branch, not the base branch. References `references/git-integration.md` by name. |
| 3 | Read `SKILL.md` Stage 7 (UAT) sub-flow | A step exists directing PR creation from the feature branch to the base branch when `github.create_pr: true`. References `references/git-integration.md` by name. |

#### TC-2: Branch Enforcement in git-integration.md (covers AC-1.4, AC-1.5, AC-1.6)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read `git-integration.md` Stage 5 section | Contains enforcement note: branch creation is MANDATORY when `git.auto_branch: true` and strategy is not `none`. States failure to create is a blocking error. |
| 2 | Read `git-integration.md` for Stage 6 subsection | A "Stage 6 (Development) -- Branch Enforcement" subsection exists. States all commits must target feature branch. States missing feature branch when `git.auto_branch` was `true` is a blocking error. |
| 3 | Read `git-integration.md` Stage 7 subsection | PR creation directives present: create PR from feature branch to base branch, body includes sprint goal, stories with "Closes #N", and UAT results. |

#### TC-3: Confidence Cap in quality-gates.md (covers AC-2.1, AC-2.2, AC-2.3)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read `quality-gates.md` Gate 7 criteria list | A blocking criterion exists capping review board confidence at 4/5 maximum when empirical validation cannot be performed. States 5/5 requires empirical evidence. |
| 2 | Read `quality-gates.md` Gate 7 criteria list | A blocking criterion exists requiring an "Empirical Validation Limitation" section in the DoD when confidence is capped, documenting: unvalidated criteria, what prevented validation, and residual risk. |
| 3 | Read `quality-gates.md` Gate 7 criteria list | The existing "Empirical-items classification" criterion is still present and unmodified. |

#### TC-4: Refactoring Sub-Type in project-types.md (covers AC-3.1, AC-3.2, AC-3.3, AC-3.4)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read `project-types.md` FEATURE detection section | "refactoring" sub-type listed with signals including "refactor", "decompose", "extract module", "restructure". |
| 2 | Read `project-types.md` Light-or-Skip "Apply Light" list | Contains a bullet for module decomposition, boundary changes, or architectural restructuring. |
| 3 | Read `project-types.md` Light-or-Skip "Apply Skip" condition for "Contained within a single service or module" | Condition now includes qualifier: "AND does not involve module decomposition, boundary changes, or architectural restructuring." |
| 4 | Read `project-types.md` full FEATURE section | All existing non-refactoring detection signals and routing logic are unchanged. No Skip conditions removed -- only narrowed. |

#### TC-5: Dogfooding Integration Test

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run this BUG_FIX pipeline with `git.branch_strategy: feature-branch` and `git.auto_branch: true` configured | Plan stage creates a feature branch. Dev stage commits to the feature branch (not `main`/`master`). UAT stage creates a PR from the feature branch. |
| 2 | Observe UAT review board confidence scoring | If bash is unavailable during UAT, confidence is capped at 4/5 and the DoD documents the empirical validation limitation. |

---

### Estimate

**2 story points** (1 sprint, single story)

Calibration rationale: All changes are markdown-only edits to instruction/reference files. No source code, no scripts, no hooks. Per lessons learned, markdown-only changes estimate one tier lower than code changes. The changes are well-scoped (specific sections in 4 known files) with clear before/after states.

---

### Files to Modify

| File | Change Summary |
|------|---------------|
| `delivery-team/skills/delivery-flow/SKILL.md` | Add branch enforcement directives at Plan (Step 8), Dev (commit step), UAT (Step 8). Cross-reference `git-integration.md`. |
| `delivery-team/skills/delivery-flow/references/git-integration.md` | Add enforcement notes to Stage 5, new Stage 6 branch enforcement subsection, PR creation directives to Stage 7. |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | Add 2 new blocking criteria to Gate 7: confidence cap at 4/5 without empirical validation, and mandatory limitation documentation in DoD. |
| `delivery-team/skills/delivery-flow/references/project-types.md` | Add refactoring sub-type to FEATURE detection, add module decomposition to "Apply Light" list, narrow "Apply Skip" single-module condition with refactoring qualifier. |

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/po/user-stories.md
SUMMARY: Single BUG_FIX story (US-01, 2 SP) covering #54 branch enforcement, IA-1 confidence cap, IA-4 refactoring sub-type — 4 AC groups, 5 test cases
```
