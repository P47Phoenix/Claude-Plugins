# Sprint Plan: Pipeline Integrity Fixes

**Version**: 1.0
**Author**: Aragorn (Scrum Master)
**Date**: 2026-04-01
**Status**: Committed
**Pipeline**: BUG_FIX (Light Plan)
**Issues**: #54, IA-1 (retro r4x2), IA-4 (retro r4x2)
**Input**: User Stories v1.0 (Gandalf/PO), Idea Brief v1.0

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."*

---

## 1. Sprint Goal

Enforce pipeline integrity by closing three rule gaps -- branch strategy enforcement (#54), confidence scoring honesty (IA-1), and architect routing for refactoring (IA-4) -- across four existing markdown files with zero behavioral regression.

---

## 2. Capacity

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Velocity baseline | 8 SP / sprint | Solo contributor, markdown-only edits (one tier below code baseline per lessons learned) |
| 80% ceiling | 6 SP | 8 x 0.80 = 6.4, rounded to 6 SP |
| Sprint 1 commitment | 2 SP | 33% of ceiling -- well within safe range for a single well-scoped story |

---

## 3. Story Assignment

| Story | Title | SP | Assigned To | Sprint |
|-------|-------|----|-------------|--------|
| US-01 | Enforce Pipeline Integrity Rules for Branch Strategy, Confidence Scoring, and Architect Routing | 2 | Developer (Gimli) | Sprint 1 |

---

## 4. Execution Order

The story bundles three AC groups across four files. Gimli should execute in this order:

1. **AC Group 1 (Branch Strategy Enforcement)** -- Start here. Edits span `SKILL.md` (3 stage sub-flows) and `git-integration.md` (3 pipeline integration subsections). This is the largest group and the P1 priority from issue #54. Get the heaviest lifting done first.
2. **AC Group 2 (Confidence Cap)** -- Next. Two new criteria added to Gate 7 in `quality-gates.md`. Contained to a single file, single section. Clean and quick.
3. **AC Group 3 (Refactoring Sub-Type)** -- Last. Four acceptance criteria in `project-types.md`. Requires careful narrowing of existing conditions without breaking non-refactoring routing. Do this with fresh eyes after the simpler edits.

---

## 5. Risk

**Main risk**: AC Group 3 inadvertently changes existing FEATURE routing for non-refactoring projects -- mitigated by AC-3.4's explicit constraint that existing Skip conditions are narrowed (not removed), and TC-4 Step 4 verifies no unintended changes.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/sm/sprint-plan.md
SUMMARY: Light sprint plan — 1 story (US-01, 2 SP), 1 sprint, assigned to Gimli, AC groups ordered by priority and complexity
```
