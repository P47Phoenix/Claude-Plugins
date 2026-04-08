# DS-01..DS-07 Implementation Notes

By yer leave — Gimli son of Glóin, with axe sharpened. Job's done. Here's the tally, blunt and true.

## DS-01 — config-schema.md
- Bumped `Current Version` from 2.7 to 2.8.
- Added DESIGN to `routing.force_type` valid values enum.
- Added DESIGN column to "Defaults by Project Type" table (checkpoints `[refine, architect]`, personas `[]`, all 6 collab patterns).
- Bumped `config_version` in template YAML to "2.8".
- Added v2.8 row to Version History describing DESIGN addition.

## DS-02 — delivery-flow/SKILL.md
- Added DESIGN row to Phase 1 detection signal table between BUG_FIX and GAME_DEV.
- Added DESIGN column to Phase 3 Stage Routing Matrix: Idea/Refine/Design/Architect = full, Plan/Dev/UAT = skip.

## DS-03 — references/project-types.md
- Added full DESIGN section (signals, confidence boosters/reducers, SPIKE and GREENFIELD disambiguation) inserted before GAME_DEV.
- Added DESIGN column to the Stage Routing Matrix in this file (mirrors SKILL.md).

## DS-04 — references/pipeline-stages.md
- Added "DESIGN: Runs full depth for DESIGN" callouts under Stage 1, 2, 3 headings.
- Stage 4 callout notes it is the terminal stage for DESIGN.
- Added "DESIGN: Skipped for DESIGN" callouts under Stages 5, 6, 7.

## DS-05 — references/setup-wizard.md
- Added detected project-type hint paragraph beneath the scan matrix calling out DESIGN as a possible detected type.
- Added DESIGN row to Q6 checkpoint defaults: `[refine, architect]`.
- Updated `routing.force_type` valid-values list (line ~562) to include DESIGN.

## DS-06 — CLAUDE.md, README.md, marketplace.json
- CLAUDE.md: added DESIGN to the auto-detect project type list with terminating-after-Architect note.
- README.md: expanded delivery-flow row to enumerate the project types including DESIGN and its terminal-after-Architect behavior.
- marketplace.json: bumped metadata.version from 2.18.0 to 2.19.0 (new capability).

## DS-07 — delivery-team/README.md
- Updated setup wizard bullet: schema bumped to v2.8 and project-type list now includes DESIGN with the design-only terminating note.

## Verification notes
- All edits are additive — no existing rows/sections were removed.
- Routing matrices in SKILL.md, project-types.md, and config-schema.md are consistent: DESIGN runs Idea/Refine/Design/Architect at full depth and skips Plan/Dev/UAT.
- Schema version, template version, and delivery-team README schema reference all moved to 2.8 in lockstep.
- Reminder: per config-schema.md Step 6.5, run `python delivery-team/scripts/generate-schema.py` to regenerate `config-schema.json` from the updated markdown table. Not executed in this dev pass — flag for ops/CI.

— Gimli
