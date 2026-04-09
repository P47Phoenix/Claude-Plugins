# US-1 — architecture_board Config Block Docs

**Dev:** Gimli (developer)
**Status:** DONE
**Date:** 2026-04-08

## Change

Added new `## architecture_board Config Block` section to
`delivery-team/skills/delivery-flow/references/config-schema.md`, placed
between the main schema table and "Defaults by Project Type".

## Contents

- Field table: 6 keys (enabled, reviewers, max_iterations, convergence,
  judge, cross_persona_iteration2) with types, required flags, defaults,
  valid values, consuming skill (delivery-flow).
- YAML example block copied verbatim from ADR-001.
- Backwards-compat note: block fully optional, absent = Stage 4 unchanged
  (NFR-2, AC-9). Cross-link to ADR-001.
- Distinguishes Pattern 3b (configurable) from fixed Pattern 3.

## Not Done (per instructions)

- `config_version` NOT bumped (explicit ask).
- No Version History row added.
- No wizard question, no schema.json regen, no SKILL.md table edit.

## Acceptance

- Field shape matches ADR-001 exactly (7 fields shown in ADR; documented 6
  configurable + enabled flag = 6 table rows, matching ADR example block).
- Defaults match ADR-001: enabled=false, max_iterations=2,
  convergence=all-done, judge=chief-architect, cross_persona_iteration2=true.
- Backwards-compat note present.
