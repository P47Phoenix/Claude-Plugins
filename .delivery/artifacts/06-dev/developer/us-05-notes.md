# US-05: Derived Artifact Regeneration at Dev DoD

**Story**: US-05 (Milestone M4)
**Developer**: Gimli
**Date**: 2026-03-29
**Status**: CODE_COMPLETE

> "And my code! No derived artifact drifts on my watch."

---

## Changes Made

### FR-11: pipeline-stages.md (Stage 6: Development)

**AC-11a -- Developer DoD validator update (MODIFY)**
- File: `delivery-team/skills/delivery-flow/references/pipeline-stages.md`
- Location: Stage 6 > DoD Validators > Developer validator
- Changed: Added "derived artifacts regenerated from current sources" to the validator description with `<!-- retro c8f2 -->` annotation
- Added: "Derived artifact check" sub-section specifying the "Derived Artifacts" section requirement in DoD reviews, listing: derived artifact path, source file(s), regeneration status (regenerated / not applicable)

**AC-11b -- Regenerate derived artifacts sub-flow step (ADD)**
- File: `delivery-team/skills/delivery-flow/references/pipeline-stages.md`
- Location: Stage 6 > Sub-Flow, inserted as new step 5 after step 4 (Technical Writer), before former step 5 (Commit suggestion)
- Content: 4-substep process (identify, regenerate, verify, document) with SEQUENTIAL per story tag, required marker, Light Mode applicability note, and `<!-- retro c8f2 -->` annotation
- Renumbered: Former step 5 (Commit suggestion) becomes step 6; former step 6 (Team DoD Validation) becomes step 7

### FR-12: quality-gates.md (Gate 6: Development Quality)

**AC-12a -- Derived artifact regeneration blocking criterion (ADD)**
- File: `delivery-team/skills/delivery-flow/references/quality-gates.md`
- Location: Gate 6 checklist, inserted after "Empirical validation requirements identified..." item
- Content: Blocking criterion requiring regeneration confirmation and documentation in the story's DoD review
- Tags: `[blocking]` severity, `<!-- retro c8f2 -->` annotation

**AC-12b -- Placement and annotation (VERIFIED)**
- Criterion placed immediately after the "Empirical validation requirements identified..." item (line 199 -> new line 200)
- `[blocking]` severity tag present
- `<!-- retro c8f2 -->` annotation present

---

## AC Verification Matrix

| AC ID | Description | Status | Notes |
|-------|-------------|--------|-------|
| AC-11a | Developer validator includes derived artifact regeneration + "Derived Artifacts" section requirement | DONE | Validator text updated, section format specified with path/source/status columns |
| AC-11b | New step 5 in Stage 6 sub-flow with 4 substeps, Light Mode note, retro annotation, renumbered steps | DONE | Steps renumbered: old 5->6, old 6->7; no gaps |
| AC-12a | Gate 6 blocking criterion for derived artifact regeneration | DONE | Blocking criterion added with documentation requirement |
| AC-12b | Criterion placed after "Empirical validation..." with [blocking] and retro annotation | DONE | Placement, severity, and annotation all verified |

---

## Derived Artifacts

| Derived Artifact Path | Source File(s) | Regeneration Status |
|---|---|---|
| N/A | N/A | not applicable |

No derived artifacts exist for the modified files (pipeline-stages.md and quality-gates.md are source-of-truth documents, not generated).

---

## Test Case Readiness

| TC ID | AC | Verifiable | Method |
|-------|-----|-----------|--------|
| TC-11a-1 | AC-11a | Yes | Read pipeline-stages.md Stage 6 DoD Validators, grep for "derived artifacts regenerated from current sources" |
| TC-11a-2 | AC-11a | Yes | Read Developer validator, verify "Derived Artifacts" section with columns: derived artifact path, source file(s), regeneration status |
| TC-11a-3 | AC-11a | Yes | Verify "regenerated" and "not applicable" listed as accepted statuses |
| TC-11b-1 | AC-11b | Yes | Read Stage 6 Sub-Flow step 5, verify SEQUENTIAL tag, required marker, 4 substeps |
| TC-11b-2 | AC-11b | Yes | Verify Light Mode note "Applies to all project types" |
| TC-11b-3 | AC-11b | Yes | Verify step 6 is Commit suggestion, step 7 is Team DoD Validation |
| TC-11b-4 | AC-11b | Yes | Grep for `<!-- retro c8f2 -->` in step 5 |
| TC-12a-1 | AC-12a | Yes | Read quality-gates.md Gate 6, verify derived artifact criterion exists |
| TC-12a-2 | AC-12a | Yes | Verify `[blocking]` tag on the criterion |
| TC-12b-1 | AC-12b | Yes | Verify criterion follows "Empirical validation requirements identified..." line |
| TC-12b-2 | AC-12b | Yes | Grep for `<!-- retro c8f2 -->` on the criterion line |
