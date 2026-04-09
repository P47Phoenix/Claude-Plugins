# US-7 — Architect-in-Plan integration (ADR-002)

**Story**: Wire Architect into Stage 5 Plan per ADR-002.
**Developer alias**: Gimli
**Status**: DONE

## Acceptance Criteria
- AC-7.1 — New invocation step at Plan step 2, `task_type: implementation-sequencing` — MET
- AC-7.2 — Output `.delivery/artifacts/05-plan/architect/sequencing.md` declared — MET
- AC-7.3 — Architect listed as participant (not owner) of Stage 5 — MET (step 2 note: "participates as an active contributor (not gate-owner); PO retains Stage 5 ownership"; Output Artifacts annotated "Architect as participant per ADR-002")

## File touched
`delivery-team/skills/delivery-flow/references/pipeline-stages.md`

## Line range modified
Stage 5 Plan Sub-Flow: lines ~427–464 (step list) and Output Artifacts / Light Mode at ~480–491. Primary insertion at line 431 (new step 2). Renumbered original steps 2→3 through 9→10.

## Step count
- Before: 9 steps in Stage 5 Sub-Flow
- After: 10 steps in Stage 5 Sub-Flow (delta +1)

## Waiver wiring
- Step 2 header flags: required for FEATURE, GREENFIELD, GAME_DEV; WAIVED for BUG_FIX, DOCS_ONLY, DESIGN
- Light Mode block explicitly lists the step as WAIVED

## Verification
- `grep implementation-sequencing` → 2 hits (step header + SKILL line)
- `grep 05-plan/architect/sequencing.md` → 2 hits (Output line in step 2 + Output Artifacts section)
- Numbering: steps 1..10 contiguous, no gaps, no duplicates
- Existing step content preserved verbatim; only renumber prefixes and "after step N" back-references updated
