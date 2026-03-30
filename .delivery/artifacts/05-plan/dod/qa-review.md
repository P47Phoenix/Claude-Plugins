# QA Engineer Review: Sprint Plan (Gate 5 -- Plan Readiness)

**Reviewer**: Legolas (QA Engineer)
**Date**: 2026-03-29
**Artifacts Reviewed**: `test-strategy.md` v1.0, `user-stories.md` v1.0
**Sprint**: Stage Health Hardening (BUG-50)
**Scope**: 5 stories, 5 milestones, 12 FRs, 26 ACs, 57 TCs
**Verdict**: DONE (with non-blocking observation)

> *"I have counted every acceptance criterion as carefully as arrows in my quiver. The count is true -- though the label on the quiver says otherwise."*

---

## Gate 5 Criteria Assessment

### [PASS] Test strategy covers critical paths [blocking]

The test strategy covers all critical paths with precision:

- **Section 6 (Risk-Based Prioritization)** identifies four Priority 1 / CRITICAL items: Gate 5 criterion replacement (the only modification of existing content), step renumbering across three sub-flows, Dev entry BLOCK runtime behavior, and regression on non-modified stages. These are the highest blast-radius items. Sound ordering.
- **Section 5 (Dogfooding Plan)** covers all 4 empirical ACs (AC-05a, AC-05b, AC-06a, AC-06b) through 13 execution steps on a real BUG_FIX pipeline. The dogfooding subject exercises shared-module review and derived artifact regeneration -- the two features most likely to fail silently.
- **Section 4 (Regression Plan)** covers non-modified stages (1, 2, 4) via diff-based zero-change verification, modified stages (3, 5, 6, 7) via additive-only checks, and cross-file consistency (step numbering, gate-to-stage alignment, contract-to-gate alignment, retro annotations).
- **Section 8 (FR Traceability)** maps all 12 FRs to stories, ACs, TCs, and dogfooding steps. Zero gaps in the matrix.

The strategy distinguishes between what can be verified by reading files and what requires a live pipeline. That distinction governs the entire execution plan. Clear-eyed.

### [PASS] Test approach referenced for each story [blocking]

Section 2 provides an explicit test approach for every story:

| Story | Approach | Rationale |
|-------|----------|-----------|
| US-01 | Structural inspection | All 5 ACs verify text insertion in `pipeline-stages.md` and `quality/SKILL.md` |
| US-02 | Structural inspection | All 4 ACs verify templates, table rows, and gate criteria in reference files |
| US-03 | Mixed (structural + empirical) | 2 structural ACs (file content) + 4 empirical ACs (runtime gate behavior) |
| US-04 | Structural inspection | All 9 ACs verify templates, validators, steps, and gate criteria |
| US-05 | Structural inspection | All 4 ACs verify validator text, step insertion, and gate criteria |

Each story subsection includes target files, rationale for the chosen approach, a per-AC inspection method table, and a regression concern callout. The approach is not just named -- it is justified and operationalized.

### [PASS] Every AC has at least one test case [blocking]

Cross-referencing user stories against test strategy coverage matrices:

- **US-01**: 5 ACs (AC-01a through AC-02b) -- all mapped in Section 3.1, 9 TCs
- **US-02**: 4 ACs (AC-03a through AC-04a) -- all mapped in Section 3.2, 10 TCs
- **US-03**: 6 ACs (AC-05a through AC-06c) -- all mapped in Section 3.3, 12 TCs
- **US-04**: 9 ACs (AC-07a through AC-10c) -- all mapped in Section 3.4, 17 TCs
- **US-05**: 4 ACs (AC-11a through AC-12b) -- all mapped in Section 3.5, 11 TCs

**Total**: 28 ACs, 59 TCs mapped. Every AC has at least one TC. Zero unmapped ACs.

**Non-blocking observation**: The test strategy header (line 7) claims "22 ACs, 45 test cases." The Section 3.6 summary repeats these figures. However, the actual coverage matrices contain 28 ACs and 59 TCs (verified by counting every row). The Section 3.4 header says "7 ACs, 14 TCs" but the table contains 9 ACs and 17 TCs. The Section 3.5 header says "4 ACs, 10 TCs" but the table contains 4 ACs and 11 TCs. **The content is complete; the summary counts are stale.** This does not block -- the matrices themselves are the source of truth and they have full coverage. The summary numbers should be corrected before implementation begins to avoid confusion during test execution.

### [PASS] Structural vs empirical classification present [blocking]

The classification is thorough and consistent across both artifacts:

**In the test strategy:**
- Section 1 (Testing Philosophy) defines the distinction: "Structural changes get structural tests. Empirical changes get pipeline runs."
- Section 2 per-story tables tag every AC with its approach (Structural or Empirical)
- Section 3 coverage matrices tag each row with its approach
- Section 3.6 summary quantifies: 22 ACs structural (100% have structural verification), 4 ACs additionally requiring empirical validation
- Empirical ACs (AC-05a, AC-05b, AC-06a, AC-06b) are cross-referenced to specific dogfooding steps (DF-3 through DF-6)

**In the user stories:**
- Every AC table includes a "Type" column with explicit "structural" or "empirical" classification
- US-03 is the only story with mixed types, and the split is clearly marked

The classification is not just present -- it drives the entire test execution order. Structural tests run first (Phases 1-4), dogfooding runs last (Phase 5), because broken markdown wastes a pipeline cycle. Sound sequencing.

---

## Non-Blocking Findings

| # | Finding | Severity | Location | Recommendation |
|---|---------|----------|----------|----------------|
| 1 | Summary counts mismatch: header says "22 ACs, 45 TCs" but matrices contain 28 ACs, 59 TCs | Observation | test-strategy.md lines 7, 195-196, Section 3.4/3.5 headers | Update summary counts to match matrix content before test execution begins |

---

## Verdict

**DONE** -- All four Gate 5 QA blocking criteria are satisfied. The test strategy covers critical paths with risk-prioritized execution, references a test approach for every story, maps every AC to at least one test case (28/28 ACs, 59 TCs), and classifies every AC as structural or empirical with the distinction driving execution order. The dogfooding plan is genuine pipeline execution, not a checkbox.

The one observation (stale summary counts) is cosmetic and non-blocking. The coverage matrices -- the actual source of truth -- are complete.

> *"Twenty-eight targets. Fifty-nine arrows. The eye does not miss what the count mislabels. The plan is ready."*
