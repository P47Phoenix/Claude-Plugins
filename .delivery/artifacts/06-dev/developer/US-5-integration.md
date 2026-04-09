# US-5: Stage 4 Orchestrator Integration for Architecture Board

**Developer:** Gimli
**Status:** DONE

## File Modified
`delivery-team/skills/delivery-flow/references/pipeline-stages.md`

## Change
Inserted new conditional sub-step **6.5 Architecture Board Review** in the
Stage 4: Architect section, placed after step 6 (Isolated Adversarial Loop)
and before step 7 (Team DoD Validation).

- Line range inserted: ~393–402 (new step 6.5 block)
- Verification: `grep "architecture_board.enabled" pipeline-stages.md` → 1 match (line 394)

## Behavior
- Gated by `architecture_board.enabled` in `.delivery/config.yml`
- Dispatches N reviewer personas from `architecture_board.reviewers` in parallel
- Judge runs sequentially after reviewers, verdict feeds DoD
- Iteration cap: `architecture_board.max_iterations`
- Round-2 persona rotation (MAR cross-persona routing)
- References `team-patterns.md` §Architecture Board Review (Configurable)

## No Conflict With Stage 5
Edit is scoped to Stage 4 (lines ~334–402). Stage 5 Architect-in-Plan
insertion at line ~431 is untouched.
