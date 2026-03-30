# Architect Review: Design Specification — Stage Health Hardening

**Reviewer**: Celebrimbor (Solution Architect)
**Review Type**: Multi-Perspective Review Board — Technical Implementability
**Date**: 2026-03-29
**Artifact**: `.delivery/artifacts/03-design/ux/user-flows.md`

---

## Verdict: APPROVE_WITH_NOTES

---

## File Path Verification

All five target files verified on disk via Read tool:

| Target File | Exists | Verified |
|---|---|---|
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | YES | Content read, 440 lines |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | YES | Content read, 234 lines |
| `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | YES | Content read, 189 lines |
| `delivery-team/skills/delivery-flow/references/project-templates.md` | YES | Content read, 152 lines |
| `delivery-team/skills/quality/SKILL.md` | YES | Content read, 367 lines |

---

## Insertion Point Verification

### FR-01: Shared-module review in UAT sub-flow

- **Claimed**: Insert after current step 4 (Exploratory testing sessions) and before step 5 (Invoke Supporting Agents) in Stage 7.
- **Actual (line 382-388)**: Step 4 is "Exploratory testing sessions". Step 5 is "Invoke Supporting Agents" (line 388).
- **CORRECT**. Insertion point is accurate. Renumbering from step 5 onward is correctly specified (5 becomes 6, through 10 becoming 11).

- **DoD Validator update**: Design says to append to "QA Engineer" validator description. The current text at line 405 reads: `- QA Engineer [required]: all tests pass, no critical defects`. The proposed new text adds `, shared-module review complete (if shared modules were modified)`.
- **CORRECT**. Additive change, no conflict.

### FR-02: Shared-module review in quality/SKILL.md

- **Claimed**: Insert after "Empirical Validation and CODE_COMPLETE Status" section (after line 311) and before "Sub-Agent Interface" section.
- **Actual**: Line 311 is the end of the CODE_COMPLETE pipeline behavior paragraph. Line 312 is `---`. Line 314 is `## Sub-Agent Interface`.
- **CORRECT**. The insertion point between line 311 and the `---` separator at line 312 is accurate. The new section slots cleanly between the two existing sections.

### FR-03: Empirical-items tracking in artifact-contracts.md

- **Claimed Addition 1**: Add row to Stage 6 to Stage 7 output sections table after "CODE_COMPLETE Items" row.
- **Actual (line 137)**: The table has CODE_COMPLETE Items as its first row. The new "Empirical Items Classification" row would follow it.
- **CORRECT**.

- **Claimed Addition 2**: Add new section after "Contract Summary Matrix" section (end of file).
- **Actual**: The file ends at line 189 with the last row of the Contract Summary Matrix table. No content follows.
- **CORRECT**. Clean end-of-file append.

### FR-04: Empirical-items classification in Gate 7

- **Claimed**: Insert after line 207 ("All pending empirical validations from Stage 6 included as mandatory UAT test cases [blocking]").
- **Actual (line 207)**: Confirmed — line 207 reads exactly `- [ ] All pending empirical validations from Stage 6 included as mandatory UAT test cases [blocking]`.
- **CORRECT**.

### FR-05: Phantom reference WARNING in Gate 3

- **Claimed**: Insert after line 153 ("Design aligns with PRD requirements...").
- **Actual (line 152)**: Line 152 reads `- [ ] Design aligns with PRD requirements (every user story has a corresponding design element) [blocking]`. Line 153 is `- [ ] Accessibility considerations documented...` which is a [warning] item.
- **NOTE (N-01)**: The design says "after line 153" but the text it quotes ("Design aligns with PRD requirements...") is actually at **line 152**, not 153. Line 153 is the Accessibility criterion. The intent is clear — insert after the last [blocking] item in Gate 3 and before the [warning] items — but the line number is off by one. The implementer should insert after line 152 (the "Design aligns..." criterion), not after line 153.

### FR-06: Filename reconciliation gate at Dev entry

- **Claimed**: After line 302 ("At minimum: user stories with acceptance criteria must exist").
- **Actual (line 303)**: Line 303 reads `- At minimum: user stories with acceptance criteria must exist`.
- **NOTE (N-02)**: The design references line 302, but the actual text is at **line 303**. Off by one. The intent is unambiguous — add a new entry condition bullet after the existing entry conditions in Stage 6. No functional impact.

### FR-09: Matrix validation step in Plan sub-flow

- **Claimed**: Modify SM validator at line 273.
- **Actual (line 273)**: Confirmed — `- Scrum Bag [required]: process is sound, capacity realistic`.
- **CORRECT**.

- **Claimed**: Insert new step 4 in Stage 5 sub-flow after step 3 (Invoke Supporting Agents) and before step 4 (Consensus Protocol).
- **Actual (line 262)**: Step 4 is "Consensus Protocol". Step 3 is "Invoke Supporting Agents" (line 249).
- **CORRECT**. Renumbering (current 4 becomes 5, etc.) is correctly specified.

### FR-10: Layered sprint capacity threshold

- **Claimed**: Modify line 180 ("Commitment does not exceed 80% of available capacity [blocking]").
- **Actual (line 180)**: Confirmed — exact match.
- **CORRECT**.

### FR-11: Derived artifact regeneration in Dev stage

- **Claimed**: Modify Developer validator at line 329.
- **Actual (line 328-329)**: Line 328 reads `- Developer [required]: code is clean, follows language best practices`. Line 329 reads `  - Writes to: ...`.
- **NOTE (N-03)**: The design references line 329 but the text it quotes starts at **line 328**. Off by one. No functional impact — the MODIFY is against the correct text string, not just the line number.

- **Claimed**: Insert new step 5 in Stage 6 sub-flow after step 4 (Technical Writer) and before step 5 (Commit suggestion).
- **Actual (line 320)**: Step 4 is "Invoke Technical Writer". Step 5 is "Commit suggestion" (line 324).
- **CORRECT**. Renumbering correctly specified (current 5 becomes 6, 6 becomes 7).

### FR-12: Derived artifact regeneration in Gate 6

- **Claimed**: Insert after line 198 ("Empirical validation requirements identified...").
- **Actual (line 198)**: Confirmed — exact match.
- **CORRECT**.

---

## Change Type Assessment

| FR | Change Type | Appropriate | Notes |
|---|---|---|---|
| FR-01 | ADD | YES | New sub-flow step + DoD validator amendment |
| FR-02 | ADD | YES | New section in SKILL.md, purely additive |
| FR-03 | ADD | YES | Table row + end-of-file section |
| FR-04 | ADD | YES | New checklist item in existing gate |
| FR-05 | ADD | YES | New checklist item in existing gate |
| FR-06 | ADD | YES | New entry condition, additive |
| FR-07 | ADD | YES | New section at end of file |
| FR-08 | ADD | YES | Combined with FR-07, appropriate |
| FR-09 | MODIFY + ADD | YES | Validator text expansion + new sub-flow step |
| FR-10 | MODIFY | YES | Replaces simple threshold with two-tier model |
| FR-11 | MODIFY + ADD | YES | Validator text expansion + new sub-flow step |
| FR-12 | ADD | YES | New checklist item in existing gate |

All change types are appropriate. No DELETE operations are proposed. MODIFY operations correctly quote the existing text to be replaced.

---

## Integration Analysis

### Pipeline Flow Integrity

The changes integrate cleanly with the existing pipeline flow. The ordering of new steps is well-reasoned:

1. **Stage 5 (Plan)**: Matrix validation (FR-09) runs after SM produces the sprint plan and before consensus. This ensures consensus participants see validated data. Sound sequencing.

2. **Stage 6 (Development)**: Derived artifact regeneration (FR-11) runs per-story after Technical Writer and before commit suggestion. This ensures commits include fresh derived artifacts. Sound sequencing.

3. **Stage 7 (UAT)**: Shared-module review (FR-01) runs after exploratory testing and before the review board. This ensures shared-module findings inform the review board's go/no-go decision. Sound sequencing.

### Conflict Analysis

No conflicts detected between the 12 FRs. The overlapping modifications to the same files are complementary:

- **pipeline-stages.md** receives changes to Stages 5, 6, and 7 — different sections, no overlap.
- **quality-gates.md** receives changes to Gates 3, 5, 6, and 7 — different sections, no overlap.
- **FR-09 and FR-10** both modify the SM validator in pipeline-stages.md — the design explicitly accounts for this by composing FR-10 as an extension of FR-09's text, not an independent MODIFY. This avoids a merge conflict.

### Renumbering Cascade

Three sub-flows require step renumbering (Stages 5, 6, 7). The design correctly identifies all affected steps in each. An implementer must be careful to apply renumbering consistently, including any cross-references to step numbers in other documents (none were identified, but the implementer should verify).

---

## Findings

### Notes (non-blocking)

| ID | FR | Finding | Impact |
|---|---|---|---|
| N-01 | FR-05 | Line reference says "line 153" but the quoted text "Design aligns with PRD requirements..." is at line 152. Line 153 is the Accessibility criterion. | Implementer must use the quoted text, not the line number, to locate the insertion point. Low risk — the quoted text is unambiguous. |
| N-02 | FR-06 | Line reference says "line 302" but the quoted text "At minimum: user stories with acceptance criteria must exist" is at line 303. | Same as N-01. Use text, not line number. |
| N-03 | FR-11 | Line reference says "line 329" but the quoted text starts at line 328. | Same as N-01. Use text, not line number. |
| N-04 | FR-03 | The artifact-contracts.md Addition 1 says to add after the "CODE_COMPLETE Items" row, but the Contract Summary Matrix at the end of the file does not include an "Empirical Items Classification" row. Consider whether the summary matrix also needs updating for the 6-to-7 transition. | Minor completeness gap. The summary matrix row for 6-to-7 currently reads "CODE_COMPLETE Items (1+)". If empirical items classification becomes required, the summary matrix should reflect this. |
| N-05 | FR-01 | The design specifies adding to the Stage 7 DoD Validators section, but the proposed text replaces the full QA Engineer line. The current line (line 405) reads `- QA Engineer [required]: all tests pass, no critical defects`. The proposed replacement text is `- QA Engineer [required]: all tests pass, no critical defects, shared-module review complete (if shared modules were modified)`. This is a MODIFY, not an APPEND, despite the design labeling it as "append to the QA Engineer validator description." The distinction matters for implementation clarity. | Implementer should treat this as a MODIFY on the QA validator line, not an APPEND to the DoD Validators section. |

### Strengths

1. **Exhaustive traceability**: Every FR maps to a specific target file, specific insertion point, and specific content block. The FR Traceability Matrix and Change Summary by File are exemplary.
2. **Conflict awareness**: The FR-09/FR-10 composed MODIFY demonstrates awareness of multi-FR interaction.
3. **Light Mode consistency**: Every FR explicitly addresses Light Mode behavior, including the deliberate WAIVE for capacity/coverage matrices (FR-07/08).
4. **NFR compliance table**: Token budget estimation and backward compatibility notes demonstrate architectural discipline.
5. **OQ resolutions are well-reasoned**: The decision to embed empirical-items tracking within the test plan (OQ-3) rather than creating a standalone file reduces artifact namespace pollution.

---

## Summary

The design specification is implementable as written. All target files exist, all insertion points map to real content, all change types are appropriate, and no conflicts exist between the 12 FRs. The five notes above are minor line-number inaccuracies (N-01 through N-03) and two completeness observations (N-04, N-05) — none require rework before implementation proceeds, provided the implementer uses the quoted text strings rather than line numbers to locate insertion points.

---

STATUS: APPROVE_WITH_NOTES
ARTIFACT: .delivery/artifacts/03-design/review-board/architect-review.md
SUMMARY: All insertion points verified, 5 minor notes (3 off-by-one line refs, 1 summary matrix gap, 1 change-type label). Implementable as-is.
