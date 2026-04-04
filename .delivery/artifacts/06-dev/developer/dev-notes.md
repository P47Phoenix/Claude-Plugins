# Dev Notes: BUG-58 -- Add Agent Invocation Templates with ALIAS Blocks

**Story**: BUG-58
**Date**: 2026-04-04
**Developer**: Gimli (Developer)
**Status**: CODE_COMPLETE

> "That template was built by dwarf-craft. It will hold."

---

## What Was Done

Added three Agent Invocation Templates to `pipeline-stages.md` in a new "Agent Invocation Templates" section inserted between the Dispatch Annotations and Stage 1 definitions.

### Templates Added

1. **Primary Agent Dispatch Template** -- for main stage workers (PO, Architect, Developer, etc.)
2. **Supporting Agent Dispatch Template** -- for supplementary workers (Data Analyst, DevOps, Tech Writer, etc.)
3. **DoD Validator Dispatch Template** -- for end-of-stage DoD validators dispatched in parallel

All three templates include the `--- ALIAS ---` block with the placeholder `{alias_personality_block OR "No alias active."}`, matching the existing pattern in `team-patterns.md`.

### Personality Strength Protocol

The section header includes a blockquote documenting the personality_strength protocol from SKILL.md Phase 4 Step 4, with all three levels:
- **light**: character + personality only
- **moderate**: adds style + one example
- **full**: adds catchphrase + two examples + "stay in character" instruction

### Omission Rules

Documented that the ALIAS block is omitted entirely when:
- Theme is `business` (no personality injection by design)
- Agent's role has no entry in the active theme (partial theme coverage)

### Consistency with team-patterns.md

The templates mirror the structural pattern used in `team-patterns.md` collaboration templates (Evaluator, Challenger, Reviewer, Debate PRO/CON/JUDGE, Consensus R1/R2/R3). All templates share:
- `AGENT INVOCATION TEMPLATE` header
- SKILL / TASK_TYPE / ROLE fields
- SKILL_LOADED confirmation line
- `--- TASK ---`, `--- INPUT ARTIFACTS ---`, `--- MEMORY LESSONS ---`, `--- ALIAS ---`, `--- OUTPUT ---`, `--- ISOLATION RULES ---` sections
- Signal block at the end

### Differences Between Dispatch Types

| Field | Primary | Supporting | DoD Validator |
|-------|---------|------------|---------------|
| STATUS values | DONE, NOT_DONE, CODE_COMPLETE | DONE, NOT_DONE | DONE, NOT_DONE |
| TASK_TYPE | stage-specific | stage-specific | `dod-validation` |
| Output path | stage/role/artifact.md | stage/role/artifact.md | stage/dod/role-review.md |
| Task description | stage-specific work | stage-specific work | DoD criteria evaluation |

## File Modified

- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` -- added ~120 lines in new "Agent Invocation Templates" section

## Derived Artifacts

- No derived artifacts require regeneration. `pipeline-stages.md` is a source reference document consumed directly by the orchestrator at runtime.

## Acceptance Criteria Verification

| AC | Status | Evidence |
|----|--------|----------|
| AC-1: Primary agent template has ALIAS block | PASS | Template contains `--- ALIAS ---` section |
| AC-2: Supporting agent template has ALIAS block | PASS | Template contains `--- ALIAS ---` section |
| AC-3: DoD validator template has ALIAS block | PASS | Template contains `--- ALIAS ---` section |
| AC-4: Templates reference personality_strength protocol | PASS | Blockquote documents light/moderate/full levels with reference to SKILL.md Phase 4 Step 4 |
| AC-5: Dogfooding | DEFERRED | To be validated during UAT with live LOTR theme pipeline run |

## Known Scope Limitation

AC-5 (dogfooding validation) cannot be verified by structural inspection alone. It requires a live pipeline run with an active alias theme to confirm agents actually receive and display the personality. This is deferred to UAT (TC-5).
