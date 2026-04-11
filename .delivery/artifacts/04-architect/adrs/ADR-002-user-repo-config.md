# ADR-002: User-Repo Config File `.mtg-commander.yml`

**Status:** Accepted
**Date:** 2026-04-08
**Author:** Celebrimbor (Architect)
**Pipeline:** run-2026-04-11-e6f3

---

## Context

The adversarial review loops and enhanced price rules introduce configurable behavior: loop caps per step, per-card price goals, escalation modes, and budget source selection. These settings need to persist across pipeline runs and vary per user or per project. The question is where the config file lives.

## Decision

Config file is `.mtg-commander.yml` in the **user's working directory** (the directory where Claude Code is invoked). It is NOT in the plugin directory. It is loaded at pipeline start, after intake confirmation, before the pipeline banner.

Schema:
```yaml
version: 1
loops:
  deck_builder: 2
  rules_judge: 2
  optimizer: 2
  price_evaluator: 2
price_rules:
  max_card_price: null
  escalation: true
  budget_source: higher
escalation:
  on_loop_exhaustion: warn
```

Behavior:
- **Missing file**: all defaults, pipeline works identically to pre-config behavior.
- **Present file**: validate schema, apply overrides, use defaults for missing keys.
- **Invalid keys**: warn with key names, use defaults for those keys.
- **Parse failure**: warn with error detail, use all defaults.
- Pipeline NEVER fails due to config.

## Alternatives Considered

### (a) Config in Plugin Directory

Store config at `mtg-commander/.mtg-commander.yml` inside the plugin repo.

**Rejected because:**
- All users of the plugin share the same config. There is no per-user or per-project customization.
- Modifying the config requires modifying the plugin repo, which may be read-only (installed via plugin marketplace).
- Config would be committed to version control alongside plugin code, mixing user preferences with plugin implementation.
- Violates separation of concerns: the plugin defines behavior; the user configures it.

### (b) Config in `.delivery/config.yml`

Add mtg-commander config as a section within the delivery-flow config file.

**Rejected because:**
- Couples mtg-commander to delivery-flow. The mtg-commander plugin operates independently -- it has no delivery-flow integration (explicitly out of scope per PRD).
- `.delivery/config.yml` has its own versioned schema (currently v2.7) with its own extension protocol. Adding mtg-commander keys would require a delivery-flow schema version bump for a change that has nothing to do with delivery-flow.
- Users who use mtg-commander without delivery-flow would need to create a `.delivery/` directory structure for no reason.
- Config key namespace collision risk: both systems might define `loops`, `escalation`, etc.

### (c) Command-Line Flags Per Invocation

Pass config as inline parameters: "build a commander deck with 3 loops per step and $5 card goal."

**Rejected because:**
- No persistence. Users must re-specify every parameter on every invocation.
- Verbose intake flow. The 7 intake parameters are already substantial; adding loop caps, escalation modes, and price rules per run creates parameter overload.
- Error-prone. Users may forget to specify a critical setting and get unexpected defaults.
- Cannot be version-controlled. A `.yml` file can be committed to a project repo, shared with teammates, and tracked over time.

## Consequences

### Positive
- Per-project customization: different MTG projects (e.g., budget vs. competitive) can have different configs.
- Version-controllable: the config file can be committed alongside the project's other files.
- Zero coupling to delivery-flow or plugin internals.
- Graceful degradation: missing file = full defaults = identical behavior to pre-config pipeline. Backwards compatible by design.
- Dot-prefixed file follows convention for tool config (.eslintrc, .prettierrc, .editorconfig).

### Negative
- Users must know about the file to benefit from it. Mitigated by the config status line shown after intake (Galadriel's IA Section 3: "Create .mtg-commander.yml to customize").
- No schema validation tooling beyond the pipeline's own load-time check. If the user writes invalid YAML, they get a warning but no IDE assistance. Future: could add a JSON Schema for editor autocomplete.
- File must be in the working directory, not discoverable via parent directory traversal. If the user invokes Claude Code from a subdirectory, the config is not found. This is intentional -- explicit over implicit.

### Neutral
- The `version: 1` field enables future schema migrations. Unknown keys are warned and ignored, so v1 configs remain valid when the schema evolves.
- Config loading adds one file read operation at pipeline start. Negligible performance impact.

## Validation

- AC-2: Challenger loops configurable per step via `.mtg-commander.yml`.
- AC-3: Pipeline works correctly when file is absent.
- AC-4: Pipeline works correctly with partial overrides.
- AC-9: Invalid config warns but does not fail the pipeline.
