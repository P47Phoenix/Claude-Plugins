# Release Notes: Pipeline Integrity Fixes

**Version**: 2.13.0
**Date**: 2026-04-01
**Pipeline Run**: BUG_FIX run-2026-04-01-m7v3
**Author**: Bilbo (Technical Writer)
**Source Issues**: #54, IA-1 (retro r4x2), IA-4 (retro r4x2)

> "I think I'm quite ready for another documentation adventure." Three quiet defects had crept into the pipeline's rulebook -- gaps in the mortar, as Gimli might say. This release seals them all, ensuring branches stay where they ought to, confidence scores tell the honest truth, and refactoring work gets the architect's eye it deserves.

---

## Summary

Three pipeline integrity fixes bundled into a single BUG_FIX run. All changes are **markdown-only** edits to delivery-flow skill reference files. No source code, no scripts, no hooks, no new config keys. No breaking changes.

| Fix | Issue | One-liner |
|-----|-------|-----------|
| Branch strategy enforcement | #54 | Pipeline now enforces feature branch creation, commit targeting, and PR creation across Plan/Dev/UAT stages |
| Confidence score cap | IA-1 | Review board confidence capped at 4/5 when empirical validation cannot be performed |
| Refactoring sub-type routing | IA-4 | FEATURE projects involving refactoring now route through Architect (light) instead of potentially skipping it |

---

## What's Fixed

### Fix 1: Branch Strategy Enforcement (#54)

The pipeline documented a git branching strategy in `references/git-integration.md`, but the stage instructions in `SKILL.md` never referenced or enforced it. Commits could silently land on `main` even when `git.branch_strategy` was configured for feature branching.

**Now enforced across three stages:**

- **Stage 5 (Plan)**: When `git.branch_strategy` is not `none` AND `git.auto_branch` is `true`, the pipeline creates a feature branch. Failure is a blocking error.
- **Stage 6 (Development)**: All commits must target the feature branch. Committing to the base branch when `auto_branch: true` is a blocking error.
- **Stage 7 (UAT)**: When `github.create_pr` is `true`, the pipeline creates a PR from the feature branch to the base branch. PR body includes sprint goal, stories with "Closes #N" references, and UAT results.

Both `SKILL.md` (stage step instructions) and `git-integration.md` (detailed enforcement rules) were updated in lockstep.

### Fix 2: Confidence Score Cap (IA-1)

The review board could previously award 5/5 confidence even when no empirical validation was performed (e.g., markdown-only changes where no tests can run). This overstated the evidence basis for approval.

**Two new blocking criteria added to Gate 7 (UAT Acceptance):**

- Review board confidence is capped at **4/5 maximum** when empirical validation cannot be performed. A score of 5/5 requires empirical evidence (test execution, runtime verification, or observable behavior confirmation).
- When confidence is capped, the DoD must include an explicit **Empirical Validation Limitation** section documenting: (a) which criteria could not be empirically validated, (b) what prevented validation, and (c) residual risk.

The existing "Empirical-items classification" criterion remains unchanged.

### Fix 3: Refactoring Sub-Type for FEATURE Routing (IA-4)

FEATURE projects involving module decomposition, boundary changes, or architectural restructuring could previously hit the Architect-skip path if they were "contained within a single service or module." This meant refactoring work could bypass architect review entirely.

**Three changes to FEATURE detection and routing:**

- New **refactoring sub-type** added to FEATURE detection with 8 signals: "refactor", "decompose", "extract module", "split class", "restructure", "reorganize modules", "break apart", "modularize".
- Refactoring work explicitly routes to **Architect-light** (not skip).
- The existing "contained within a single service or module" skip condition now includes a qualifier: "AND does not involve module decomposition, boundary changes, or architectural restructuring."

No existing skip conditions were removed -- only narrowed.

---

## Files Modified

All files are within `delivery-team/skills/delivery-flow/`:

| File | Changes |
|------|---------|
| `SKILL.md` | Added branch creation directive (Stage 5), branch enforcement directive (Stage 6), PR creation step (Stage 7). All three reference `references/git-integration.md`. |
| `references/git-integration.md` | Added ENFORCEMENT blockquote (Stage 5), new "Stage 6 -- Branch Enforcement" subsection, PR creation directives with body template (Stage 7). |
| `references/quality-gates.md` | Added 2 blocking criteria to Gate 7: confidence cap at 4/5 without empirical validation, mandatory Empirical Validation Limitation section in DoD. |
| `references/project-types.md` | Added refactoring sub-type with 8 detection signals, added module decomposition to "Apply Light" list, narrowed "Apply Skip" single-module condition. |

**No files added. No files deleted.**

---

## Migration Notes

None required. These are purely additive changes to pipeline instruction files:

- No new config keys introduced (all referenced keys -- `git.branch_strategy`, `git.auto_branch`, `github.create_pr` -- already exist in config schema v2.3).
- No schema changes.
- No breaking changes to existing pipeline behavior for projects that do not use git integration or branching.
- Projects with `git.branch_strategy: none` are unaffected by Fix 1.
- The confidence cap (Fix 2) applies going forward to all UAT gates.
- The refactoring sub-type (Fix 3) applies going forward to FEATURE-type projects.

---

## Verification

13/13 acceptance criteria pass structural verification. Empirical validation (dogfooding via a live pipeline run exercising each fix) is a UAT gate item tracked separately.

---

## Issue Traceability

| Issue | Source | Resolution |
|-------|--------|------------|
| #54 | GitHub issue | Branch enforcement directives added to SKILL.md and git-integration.md across 3 stages |
| IA-1 | Retrospective r4x2 | Confidence cap and limitation documentation criteria added to quality-gates.md Gate 7 |
| IA-4 | Retrospective r4x2 | Refactoring sub-type and routing narrowing added to project-types.md |

> And so three quiet gaps in the pipeline's rulebook have been found and filled -- branches now stay on their proper paths, confidence scores speak only to what can be proven, and refactoring work shall not slip past the architect's watchful eye. The mortar holds. Now then, I believe elevenses is calling.
