# Troubleshooting Quick-Reference

> *"Even the smallest person can change the course of the future — or at least get the pipeline unstuck."* — Bilbo

When the pipeline coughs, check here first. Entries are **SYMPTOM → CAUSE → FIX**.
Keep this page short; link out to the deep references when you need the long version.

For a friendlier first-run overview, see `getting-started.md`.
For the config-key catalog, see `config-schema.md`.

---

## 1. Pipeline aborts mid-run

- **Symptom:** Stages stop advancing. A `.delivery/state.md` file remains on disk.
- **Cause:** An explicit `abort` command was issued, or an unrecoverable escalation
  fired and you (or the orchestrator) chose *Abort*.
- **Fix:** Re-invoke `delivery-team:delivery-flow`. The orchestrator detects the
  aborted state file and offers **Resume / Restart / Abandon**.

## 2. Config drift (version mismatch)

- **Symptom:** A warning at pipeline start announces a config upgrade.
- **Cause:** The schema was bumped; your `.delivery/config.yml` `config_version`
  is older than the current schema version.
- **Fix:** Defaults are auto-applied for new keys. Re-run the setup wizard
  (`"setup"`) if you want to configure the new keys interactively instead of
  accepting defaults.

## 3. Skill not loading

- **Symptom:** The agent response does not begin with `SKILL_LOADED: <name>`.
- **Cause:** The skill is not installed, or your phrase did not match its
  trigger set.
- **Fix:** Verify the plugin is registered in `.claude-plugin/marketplace.json`.
  Use a trigger phrase from the skill's description (see the plugin's SKILL.md).

## 4. Pipeline bypass warning

- **Symptom:** A PreToolUse hook warns when `developer` or `godot` is invoked
  outside `delivery-flow`.
- **Cause:** You tried to spawn an implementation skill directly, without a
  pipeline run holding its context.
- **Fix:** For real features, invoke `delivery-team:delivery-flow` first so the
  work carries requirements, design, and DoD. For one-off fixes, the warning is
  informational — acknowledge and continue.

## 5. DoD validators repeatedly fail the same criterion

- **Symptom:** Three rounds of self-correction and the same gate still says
  NOT_DONE.
- **Cause:** The agent cannot satisfy the gate — usually a cross-cutting
  conflict or an ambiguous specification.
- **Fix:** Dynamic escalation triggers automatically. Choose one of the four
  options the orchestrator offers: **Provide guidance / Override / Redirect /
  Abort** (see SKILL.md "Dynamic Escalation Protocol").

## 6. Defects — where do I track them?

- **Symptom:** "I found a defect. Where does it go?"
- **Fix:** Each defect lives at `.delivery/defects/DEFECT-NNN.md` with a
  rolled-up summary in `.delivery/defects/index.md`. See `defect-tracking.md`
  for the schema.

## 7. State file out of sync

- **Symptom:** `state.md` references stages or artifact files that do not exist
  on disk.
- **Cause:** An aborted run, a manual deletion, or a session crash mid-stage.
- **Fix:** On resume the orchestrator validates the artifact map. If validation
  fails, it offers **Restart** (archives the stale state, starts fresh).

## 8. MTG Commander runs inline (no sub-agents)

- **Symptom:** A single Agent dispatch happens, then a decklist appears with no
  Challenger output.
- **Cause:** The `mtg-commander` SKILL.md sub-agent guardrail was not honored.
- **Fix:** This is a known anti-pattern. Re-invoke and explicitly request the
  adversarial pipeline ("run the full challenger pipeline"). If it recurs,
  log a defect per issue 6.

## 9. `constraints.yml` validation fails

- **Symptom:** `validate_constraints.py` exits with code 1.
- **Cause:** Required fields are missing (usually `entities` or `invariants`),
  or the YAML itself does not parse.
- **Fix:** Walk through `constraints-quickstart.md` and compare against working
  examples in `references/fixtures/`.

## 10. "Where do I find…?"

| Looking for | Location |
|---|---|
| Memory index + chunks | `.delivery/memory/` (start at `index.md`) |
| Past run archives | `.delivery/memory/archive/` |
| Backlog items | `.delivery/backlog/BACKLOG-NNN-*.md` |
| Defects | `.delivery/defects/DEFECT-NNN.md` |
| Pipeline state | `.delivery/state.md` (only present during an in-progress run) |

---

## See Also

- `getting-started.md` — quick-start wizard, skill map, first pipeline walkthrough
- `config-schema.md` — every config key, type, default, valid values
- `defect-tracking.md` — defect schema and plugin self-improvement triggers
- `../SKILL.md` — Dynamic Escalation Protocol, Resume/Restart/Abandon state machine

> *"Not all those who wander are lost — but if your pipeline is, start here."*
