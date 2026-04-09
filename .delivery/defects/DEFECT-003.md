# DEFECT-003: Setup wizard quick-start still asks removed project_type question; v2.6 configs not migrated to v2.7

**Pipeline**: setup quick-start run, 2026-04-08
**Severity**: Major (schema drift — plugin/wizard out of sync with documented v2.7 schema)
**Category**: Wizard/schema drift (systemic plugin defect)

## Description
The delivery-flow setup wizard's Quick-Start Mode still asks "What are you building?" as question 1 and prompts the user to choose a project type (FEATURE / GREENFIELD / BUG_FIX / etc.). This question was removed in schema v2.7: project type is now detected per run in Phase 1 of the pipeline, and `routing.force_type` is the opt-in override for intentional pinning.

Additionally, the repo's existing `.delivery/config.yml` is still on `config_version: "2.6"` and carries the legacy `project_type: FEATURE` key. There is no v2.6 → v2.7 upgrade path that strips `project_type` from loaded configs and bumps the version, so users who ran setup before v2.7 remain pinned to stale config shapes.

## Evidence
- CLAUDE.md "Key Conventions" and delivery-flow bullet list document that v2.7 removed `project_type` and that Phase 1 detection runs on every invocation (`routing.force_type` = opt-in override).
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/config.yml` lines 1–2:
  - `config_version: "2.6"`
  - `project_type: FEATURE`
- `delivery-team/skills/delivery-flow/SKILL.md` "Quick-Start Mode" section still lists "What are you building? — auto-detect project type from the answer" as question 1.
- Possibly also present in `delivery-team/skills/delivery-flow/references/setup-wizard.md` and/or `references/getting-started.md`.
- Reproduced by user on 2026-04-08 during a `setup` quick-start run — wizard asked the removed question.

## Reproduction
1. In a repo with or without an existing `.delivery/config.yml`, invoke the delivery-flow setup wizard in quick-start mode.
2. Observe question 1: "What are you building?" prompting for project type.
3. Expected (per v2.7): no project-type question; optional prompt to set `routing.force_type` for intentional pinning.
4. Separately: open `.delivery/config.yml` and observe `config_version: "2.6"` with `project_type: FEATURE` still present, despite the documented v2.7 schema removal.

## Root Cause
Two linked gaps in the v2.7 rollout:
1. **Wizard content drift**: The Quick-Start question list in `delivery-flow/SKILL.md` (and possibly `references/setup-wizard.md` / `references/getting-started.md`) was not updated when the schema removed `project_type`. The wizard still produces v2.6-shaped configs.
2. **Missing migration**: No v2.6 → v2.7 upgrade path exists. Loaded configs with `config_version: "2.6"` and/or a `project_type` key are not normalized — the key is not stripped and the version is not bumped. Users on pre-v2.7 configs silently keep a stale pin.

## Affected Files
- `delivery-team/skills/delivery-flow/SKILL.md` (Quick-Start Mode section — question 1)
- `delivery-team/skills/delivery-flow/references/setup-wizard.md` (likely)
- `delivery-team/skills/delivery-flow/references/getting-started.md` (likely)
- `delivery-team/skills/delivery-flow/references/config-schema.md` (migration path documentation)
- Any setup-wizard implementation script (if present) under `delivery-team/skills/delivery-flow/scripts/`
- `.delivery/config.yml` in this repo (example of the unmigrated artifact)

## Proposed Fix
1. **Wizard**: Remove the "What are you building?" project-type question from Quick-Start Mode in `SKILL.md` and any mirrored references. Optionally add a follow-up prompt: "Do you want to pin a project type (advanced, rarely needed)? If so, set `routing.force_type`." Default: unset, let Phase 1 detect.
2. **Migration**: Add a v2.6 → v2.7 upgrade step to the config loader / setup wizard that:
   - Detects `config_version: "2.6"` (or missing).
   - Strips the top-level `project_type` key if present.
   - Bumps `config_version` to `"2.7"`.
   - Logs the migration action.
3. **Schema doc**: Ensure `references/config-schema.md` documents the v2.6 → v2.7 migration step explicitly.
4. **Regression guard**: Add a config-validation test that fails if a v2.7 config contains a top-level `project_type` key.
5. **Dogfood**: Run setup quick-start against this repo post-fix to confirm `.delivery/config.yml` migrates cleanly to v2.7.

## Classification
**Systemic plugin defect** — wizard/schema drift between documented v2.7 schema and actual wizard content + missing migration path. Warrants a plugin self-improvement PR to the `delivery-flow` skill. This is not a per-run content defect; it affects every user who runs `setup` or who has a pre-v2.7 config on disk.

## Status
**Open** — logged by PO on 2026-04-08. Assigned to delivery-flow plugin maintainers for self-improvement PR. Underlying wizard code intentionally not modified in this ticket (logging only).
