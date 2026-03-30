# QA Review: Design Specification Testability

**Reviewer**: Legolas (QA Engineer -- Risk Reviewer)
**Date**: 2026-03-29
**Artifact**: `.delivery/artifacts/03-design/ux/user-flows.md` v1.0
**Review Type**: Multi-Perspective Review Board -- Testability Assessment

---

## 1. Structural vs. Empirical Verifiability

Each design spec was assessed for whether it can be verified by reading the modified file (structural) or only by running a pipeline (empirical).

| FR | Structural (file inspection) | Empirical (pipeline run) | Notes |
|---|---|---|---|
| FR-01 | YES -- new step 5 text in pipeline-stages.md Stage 7 Sub-Flow can be verified by reading the file; DoD validator update verifiable by inspection | PARTIAL -- step renumbering correctness and sequencing behavior require pipeline execution to confirm no regression | Insertion point (after step 4) is specified precisely |
| FR-02 | YES -- new section in quality/SKILL.md verifiable by reading the file | NO | Purely additive markdown section |
| FR-03 | YES -- new table row and new template section in artifact-contracts.md verifiable by reading the file | NO | Two additions, both at specified locations |
| FR-04 | YES -- new checklist item in quality-gates.md Gate 7 verifiable by reading the file | NO | Single line addition |
| FR-05 | YES -- new checklist item in quality-gates.md Gate 3 verifiable by reading the file | YES -- the WARNING behavior (logged, surfaced, non-blocking) can only be verified by running a pipeline with a phantom reference | PRD marks this AC as "empirical" -- design correctly preserves that |
| FR-06 | YES -- new entry condition block in pipeline-stages.md verifiable by reading the file | YES -- the blocking behavior (FAIL on missing files, PASS on sprint-plan items) requires a pipeline run to confirm the gate actually fires | PRD marks this AC as "empirical" -- design correctly preserves that |
| FR-07 | YES -- capacity matrix template in project-templates.md verifiable by reading the file | NO | Template presence is structural |
| FR-08 | YES -- coverage matrix template combined with FR-07 verifiable by reading the file | NO | Combined with FR-07 |
| FR-09 | YES -- SM validator text modification and new step 4 in pipeline-stages.md Stage 5 Sub-Flow verifiable by reading the file | PARTIAL -- matrix validation enforcement requires pipeline run | Step renumbering also needs pipeline confirmation |
| FR-10 | YES -- two-tier threshold text in quality-gates.md Gate 5 and pipeline-stages.md SM validator verifiable by reading the file | PARTIAL -- threshold enforcement behavior (warning vs. blocking at different percentages) requires pipeline run | Replaces existing criterion; verify old text removed |
| FR-11 | YES -- new step 5 and Developer validator modification in pipeline-stages.md Stage 6 verifiable by reading the file | PARTIAL -- regeneration enforcement during actual Dev stage requires pipeline run | Step renumbering also needs pipeline confirmation |
| FR-12 | YES -- new checklist item in quality-gates.md Gate 6 verifiable by reading the file | NO | Single line addition |

**Summary**: All 12 FRs have a structural verification path (the markdown content can be confirmed by reading the target file). FRs 05 and 06 additionally require empirical validation per the PRD's own AC Type classification. FRs 01, 09, 10, and 11 have partial empirical concerns (step renumbering, enforcement behavior) that are lower risk but should be covered in dogfooding.

---

## 2. FR Traceability Matrix Coverage

The design's FR Traceability Matrix (lines 474-491) was compared against the PRD's 12 functional requirements.

| FR | Present in Design Matrix | Target File Matches PRD | Verified Column |
|---|---|---|---|
| FR-01 | YES | YES -- pipeline-stages.md | YES |
| FR-02 | YES | YES -- quality/SKILL.md | YES |
| FR-03 | YES | YES -- artifact-contracts.md | YES |
| FR-04 | YES | YES -- quality-gates.md | YES |
| FR-05 | YES | YES -- quality-gates.md | YES |
| FR-06 | YES | YES -- pipeline-stages.md | YES |
| FR-07 | YES | YES -- project-templates.md | YES |
| FR-08 | YES | YES -- project-templates.md | YES |
| FR-09 | YES | YES -- pipeline-stages.md | YES |
| FR-10 | YES | YES -- quality-gates.md + pipeline-stages.md | YES |
| FR-11 | YES | YES -- pipeline-stages.md | YES |
| FR-12 | YES | YES -- quality-gates.md | YES |

**Result**: All 12 FRs are covered. No gaps.

---

## 3. Open Question Resolution Testability

### OQ-1: Phantom vs. Planned files (RESOLVED in PRD v1.1)

- **Design adoption**: Two-tier model with `[PLANNED]` annotation at Design (FR-05 WARNING) and enforcement at Dev entry (FR-06 BLOCK).
- **Testability**: PARTIALLY STRUCTURAL. The text defining the two-tier model can be verified by reading quality-gates.md (Gate 3) and pipeline-stages.md (Stage 6 entry conditions). However, the behavioral claim -- that `[PLANNED]` annotations exempt files at Design but NOT at Dev entry -- requires a pipeline run to confirm enforcement.
- **Risk**: Low. The design spec is explicit about where each tier applies. The separation across two gate criteria (FR-05 and FR-06) makes the intent clear and auditable.

### OQ-2: Shared module definition (RESOLVED in PRD v1.1)

- **Design adoption**: Artifact-traceable definition -- file referenced in 2+ stage artifacts.
- **Testability**: STRUCTURAL. The definition is embedded in FR-01 (pipeline-stages.md step text) and FR-02 (quality/SKILL.md protocol section). Both can be verified by reading the files. The identification steps in FR-02 are explicit and tool-scoped (Glob/Read).
- **Risk**: None. Clear, unambiguous, inspectable.

### OQ-3: Empirical-items tracking format (DESIGN DECISION)

- **Design adoption**: Dedicated section within existing UAT test-plan artifact, not a standalone file.
- **Testability**: STRUCTURAL for the decision itself -- the template in artifact-contracts.md (FR-03) and the Gate 7 criterion (FR-04) both reference the section-within-test-plan approach. The validator criterion explicitly checks for "section present in UAT test plan."
- **Risk**: Low. The rationale is documented (4 points). The validator criterion in FR-04 is specific enough to be enforceable: "every PRD acceptance criterion classified as structural or empirical with justification."

---

## 4. Risk Findings

### R1: Step Renumbering Across Three Stages (LOW)

FRs 01, 09, and 11 each insert new sub-flow steps that require renumbering subsequent steps in Stages 5, 6, and 7. The design states "subsequent steps must be renumbered" but does not provide the renumbered step lists. This is a minor implementation risk -- the developer must get the renumbering right.

**Recommendation**: Implementation PR should include full before/after step numbers for each stage. Structural verification should confirm no duplicate or missing step numbers.

### R2: FR-10 Modifies Existing Criterion -- Old Text Must Be Removed (LOW)

FR-10 replaces the existing Gate 5 criterion "Commitment does not exceed 80% of available capacity [blocking]" with the two-tier model. The design provides both current and new text. Structural verification must confirm the old text is removed, not duplicated alongside the new text.

**Recommendation**: Verify the MODIFY change type is honored -- old text absent, new text present.

### R3: FR-09 and FR-10 Both Modify the Same SM Validator Line (LOW)

The design acknowledges this overlap and shows the combined final text. Good. No conflict.

### R4: No Structural Test for NFR-04 Token Budget at Design (INFO)

NFR-04 compliance is noted in the design with estimated token counts. The PRD explicitly defers NFR-04 validation to Dev stage DoD. This is acceptable -- just noting it is not testable at this stage.

---

## 5. Verdict

The design specification is well-structured for testability. Every FR has a clear structural verification path (read the target file, confirm the specified content exists at the specified location). The two empirically-typed ACs (FR-05, FR-06) are correctly identified and will require pipeline dogfooding per the PRD's validation approach. The FR traceability matrix covers all 12 FRs with no gaps. All three open question resolutions are testable. No blocking issues found.

---

**VERDICT**: APPROVE_WITH_NOTES
