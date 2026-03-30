# US-03 Implementation Notes: Phantom Reference Detection and Filename Reconciliation

**Story**: US-03 (Milestone M2 -- Design Stage Hardening)
**Developer**: Gimli
**Date**: 2026-03-29

---

## Changes Made

### FR-05: Phantom Reference WARNING at Design DoD (quality-gates.md)

**File**: `delivery-team/skills/delivery-flow/references/quality-gates.md`
**Change type**: ADD -- new checklist item in Gate 3: Design Completeness
**Insertion point**: After "Design aligns with PRD requirements" (line 152), before "Accessibility considerations documented"

**Content added**: Single checklist item implementing two-tier phantom file detection:
- WARNING severity (does not block stage completion)
- `[PLANNED]` annotation grants exemption at this stage
- Retro annotation `<!-- retro k4m9 -->` present

**ACs satisfied**:
- AC-05a: WARNING finding for non-existent, non-PLANNED paths -- YES
- AC-05b: `[PLANNED]` exemption at Gate 3 -- YES
- AC-05c: Placement after "Design aligns with PRD requirements", `[warning]` tag, retro annotation -- YES

### FR-06: Filename Reconciliation Gate at Dev Entry (pipeline-stages.md)

**File**: `delivery-team/skills/delivery-flow/references/pipeline-stages.md`
**Change type**: ADD -- new entry condition in Stage 6: Development
**Insertion point**: After "At minimum: user stories with acceptance criteria must exist" (line 303), before Sub-Flow section

**Content added**: Full filename reconciliation gate with:
1. 5-step reconciliation process (extract paths, check disk, pass/fail criteria, blocking behavior, resolution guidance)
2. Checks BOTH Design (`.delivery/artifacts/03-design/`) and Architect (`.delivery/artifacts/04-architect/`) artifacts
3. Pass criteria: exists on disk OR in sprint plan task list
4. Fail criteria: `[PLANNED]` without sprint plan entry OR missing entirely
5. Blocking on any FAIL with list of non-existent references
6. Resolution guidance: create files, add to sprint plan, or remove references
7. Light Mode applicability note
8. Explicit note that `[PLANNED]` is NOT an exemption at Dev entry
9. Retro annotation `<!-- retro k4m9 -->` present

**ACs satisfied**:
- AC-06a: Checks Design + Architect artifacts, disk existence, sprint plan cross-ref, blocking behavior -- YES
- AC-06b: `[PLANNED]` explicitly NOT accepted as exemption at Dev entry -- YES
- AC-06c: 5-step process, pass/fail criteria, resolution guidance, Light Mode note, retro annotation -- YES

---

## Verification

Both edits are additive only. No existing content was removed or modified. Insertion points match the design spec exactly.
