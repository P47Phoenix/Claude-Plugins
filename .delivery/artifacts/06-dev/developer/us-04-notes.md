# US-04 Implementation Notes: Plan Stage Capacity and Coverage Guardrails

**Story**: US-04 (Milestone M3)
**Developer**: Gimli
**Date**: 2026-03-29
**Status**: CODE_COMPLETE

---

## Changes Made

### FR-07 + FR-08: Capacity and Coverage Matrix Templates (AC-07a, AC-07b, AC-08a, AC-08b)

**File**: `delivery-team/skills/delivery-flow/references/project-templates.md`

- Added new "Sprint Plan Mandatory Sections" section at end of file with `<!-- retros c8f2, k4m9 -->` annotation
- Added Capacity Matrix Template with columns: Team Member, Role, Available Hours, Allocated Hours, Utilization %
- Capacity template includes a **Total** summary row and Utilization notes field
- Added Coverage Matrix Template with columns: PRD FR-ID, FR Description (summary), Planned Task(s), Story ID(s), Status
- Coverage template includes **Unmapped FRs** annotation area
- Both templates include `<!-- retro c8f2 -->` inline annotations
- Both templates include Light Mode waiver: "WAIVED" for BUG_FIX and DOCS_ONLY

### FR-09: Matrix Validation Step + Scrum Bag Validator Update (AC-09a, AC-09b)

**File**: `delivery-team/skills/delivery-flow/references/pipeline-stages.md`

- **Scrum Bag validator** (DoD Validators section): Extended description to include "capacity matrix present with utilization calculated, coverage matrix present with all PRD FRs mapped to at least one task. Capacity threshold enforcement: >80% utilization emits WARNING requiring acknowledgment; >100% utilization is BLOCKING" with `<!-- retros c8f2, k4m9 -->`
- **New step 4 "Matrix validation"**: Inserted after step 3 (Invoke Supporting Agents) with [SEQUENTIAL after step 3] [required] tags. Validates capacity matrix presence/completeness and coverage matrix with unmapped FR = BLOCKING. Light Mode waiver explicit. `<!-- retros c8f2, k4m9 -->` annotation included.
- **Renumbered steps**: Previous steps 4-8 became steps 5-9 (Consensus Protocol, Adversarial Review, Team DoD Validation, Git branch creation, Human Checkpoint 3). Sequential numbering verified with no gaps.

### FR-10: Two-Tier Capacity Threshold in Gate 5 (AC-10a, AC-10b, AC-10c)

**File**: `delivery-team/skills/delivery-flow/references/quality-gates.md`

- **Replaced** old criterion "Commitment does not exceed 80% of available capacity [blocking]" with the two-tier model:
  - >80% and <=100%: WARNING with acknowledgment requirement
  - >100%: BLOCKING with reduction or PO sign-off requirement
  - Light Mode applicability: "Applies to all project types"
- Added `<!-- retros c8f2, k4m9 -->` annotation
- Old criterion fully removed -- no duplication

---

## Verification Checklist

| AC | Verified | Notes |
|----|----------|-------|
| AC-07a | YES | Capacity matrix template has all 5 required columns + Total row |
| AC-07b | YES | "Sprint Plan Mandatory Sections" at end of file, retro annotation, Light Mode waiver |
| AC-08a | YES | Coverage matrix template has all 5 required columns + Unmapped FRs area |
| AC-08b | YES | Same section as capacity, retro annotation, Light Mode waiver |
| AC-09a | YES | Scrum Bag validator includes matrix + threshold language |
| AC-09b | YES | Step 4 inserted with SEQUENTIAL tag, required marker, BLOCKING for unmapped FR, Light Mode waiver |
| AC-10a | YES | >80% WARNING tier with acknowledgment in Gate 5 |
| AC-10b | YES | >100% BLOCKING tier with reduction/PO sign-off in Gate 5 |
| AC-10c | YES | Old "80% blocking" replaced (not duplicated), Light Mode note present |

---

## Empirical Items

All acceptance criteria for US-04 are **structural** -- verifiable by reading the modified files and checking content/placement. No runtime validation required.

---

## Files Modified

1. `delivery-team/skills/delivery-flow/references/project-templates.md` -- Sprint Plan Mandatory Sections (FR-07, FR-08)
2. `delivery-team/skills/delivery-flow/references/pipeline-stages.md` -- Stage 5 Sub-Flow step 4 + Scrum Bag validator (FR-09, FR-10)
3. `delivery-team/skills/delivery-flow/references/quality-gates.md` -- Gate 5 two-tier capacity threshold (FR-10)
