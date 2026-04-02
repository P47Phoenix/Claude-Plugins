# Dev Notes: Pipeline Integrity Fixes (US-01)

**Developer**: Gimli
**Date**: 2026-04-01
**Status**: DONE
**Story**: US-01 — Enforce Pipeline Integrity Rules for Branch Strategy, Confidence Scoring, and Architect Routing
**Sprint Plan**: BUG_FIX (Light Plan), 2 SP
**Source Issues**: #54, IA-1 (retro r4x2), IA-4 (retro r4x2)

> "The foundation was sound, but the mortar had gaps. Now it holds. And my code!"

---

## 1. Summary of Changes Per File

### File 1: `delivery-flow/SKILL.md`
Three surgical additions to stage definitions, no existing content altered:

| Location | Change | AC |
|----------|--------|----|
| Stage 5 (Plan), before Light mode | Added **Branch creation** directive: when `git.branch_strategy` is not `none` AND `git.auto_branch` is `true`, create feature branch per `references/git-integration.md`. Blocking error on failure. | AC-1.1 |
| Stage 6 (Development), before Execution | Added **Branch enforcement** directive: all commits MUST target feature branch, not base branch. References `references/git-integration.md`. Missing branch when `auto_branch: true` is blocking error. | AC-1.2 |
| Stage 7 (UAT), before Post-acceptance | Added **PR creation** step: when `github.create_pr` is `true`, create PR from feature branch to base branch. Body includes sprint goal, stories with "Closes #N", UAT results. References `references/git-integration.md`. | AC-1.3 |

### File 2: `delivery-flow/references/git-integration.md`
Three additions to the Pipeline Integration Points section:

| Location | Change | AC |
|----------|--------|----|
| Stage 5, after skip-branch paragraph | Added **ENFORCEMENT** blockquote: branch creation is MANDATORY when conditions met. Failure is blocking error. Pipeline MUST NOT proceed without branch in state. | AC-1.4 |
| New subsection before Commit Suggestions | Added **Stage 6 (Development) -- Branch Enforcement** subsection: commits must target feature branch, missing branch when `auto_branch: true` is blocking error with escalation. | AC-1.5 |
| New subsection before Working Tree Validation | Added **Stage 7 (UAT) -- PR Creation** subsection: full PR workflow with body template (sprint goal, stories with "Closes #N", UAT results), state recording. | AC-1.6 |

### File 3: `delivery-flow/references/quality-gates.md`
Two new blocking criteria added to Gate 7 (UAT Acceptance), inserted after the existing Empirical-items classification criterion:

| Criterion | AC |
|-----------|----|
| **Confidence cap**: review board confidence capped at 4/5 maximum when empirical validation cannot be performed. 5/5 requires empirical evidence. | AC-2.1 |
| **Empirical Validation Limitation documentation**: DoD must include explicit section documenting (a) unvalidated criteria, (b) what prevented validation, (c) residual risk. | AC-2.2 |

The existing Empirical-items classification criterion was preserved unchanged (AC-2.3).

### File 4: `delivery-flow/references/project-types.md`
Three changes to FEATURE detection and routing:

| Location | Change | AC |
|----------|--------|----|
| FEATURE detection section | Added **Sub-type -- refactoring** with 8 detection signals: "refactor", "decompose", "extract module", "split class", "restructure", "reorganize modules", "break apart", "modularize". | AC-3.1 |
| Light-or-Skip "Apply Light" list | Added bullet: "Module decomposition, boundary changes, or architectural restructuring (refactoring sub-type)". | AC-3.2 |
| Light-or-Skip "Apply Skip" list | Narrowed "Contained within a single service or module" with qualifier: "AND does not involve module decomposition, boundary changes, or architectural restructuring." | AC-3.3 |

All existing non-refactoring FEATURE detection signals and routing logic remain unchanged. No Skip conditions removed -- only narrowed (AC-3.4).

---

## 2. Per-AC Verification

| AC | Status | Evidence |
|----|--------|----------|
| AC-1.1 | PASS | SKILL.md Stage 5 contains branch creation directive referencing `references/git-integration.md` by name. |
| AC-1.2 | PASS | SKILL.md Stage 6 contains branch enforcement directive referencing `references/git-integration.md` by name. |
| AC-1.3 | PASS | SKILL.md Stage 7 contains PR creation step referencing `references/git-integration.md` by name. |
| AC-1.4 | PASS | git-integration.md Stage 5 contains ENFORCEMENT blockquote: MANDATORY branch creation, blocking error on failure. |
| AC-1.5 | PASS | git-integration.md contains "Stage 6 (Development) -- Branch Enforcement" subsection with blocking error for missing branch. |
| AC-1.6 | PASS | git-integration.md contains "Stage 7 (UAT) -- PR Creation" subsection with PR body template including sprint goal, "Closes #N", UAT results. |
| AC-2.1 | PASS | quality-gates.md Gate 7 contains blocking criterion capping confidence at 4/5 without empirical validation. |
| AC-2.2 | PASS | quality-gates.md Gate 7 contains blocking criterion requiring "Empirical Validation Limitation" section in DoD. |
| AC-2.3 | PASS | Existing "Empirical-items classification" criterion remains unchanged at its original position. |
| AC-3.1 | PASS | project-types.md FEATURE section contains "refactoring" sub-type with all 8 specified signals. |
| AC-3.2 | PASS | project-types.md "Apply Light" list includes module decomposition/boundary changes/restructuring bullet. |
| AC-3.3 | PASS | project-types.md "Apply Skip" single-module condition includes "AND does not involve..." qualifier. |
| AC-3.4 | PASS | All existing non-refactoring FEATURE signals and routing unchanged. No Skip conditions removed. |

**Result**: 13/13 ACs pass structural verification.

---

## 3. Deviations from Story

None. All changes are exactly as specified in the acceptance criteria. No new files created. No config keys added. No existing content removed or modified.

---

## 4. Verification Status

| Type | Coverage | Notes |
|------|----------|-------|
| **Structural** | 13/13 ACs | All criteria verified by reading modified files and confirming text changes exist at correct locations. |
| **Empirical** | 0/13 ACs | These are markdown instruction files -- empirical validation means running a pipeline session that exercises each fix (TC-5 dogfooding). This is a UAT gate item per IA-1 and per memory lesson `feedback_dogfooding.md`. |

### Derived Artifacts Check
- `config-schema.json` exists in the delivery-flow references directory.
- No config schema changes were made (all config keys already existed in v2.3).
- No derived artifact regeneration required.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/developer/dev-notes.md
SUMMARY: US-01 implemented: 13/13 ACs pass structural verification across 4 files (SKILL.md, git-integration, quality-gates, project-types)
```
