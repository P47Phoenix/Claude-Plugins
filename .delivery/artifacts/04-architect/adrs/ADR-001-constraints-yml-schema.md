# ADR-001 — `constraints.yml` Schema

**Status**: accepted
**Date**: 2026-04-08
**Stage**: 4 Architect (LIGHT) | **Author**: Celebrimbor (Solution Architect)
**Feature**: Paired Constraints Primitive

## Context

The PRD (FR-1) requires a single primitive carrying stage-committed constraints from Refine and Architect into Plan, Dev, and DoD gates. The primitive must be mechanically checkable by the Business Rules Engine, human-glanceable at checkpoints, and small enough to resist bloat (PRD R-1). A format and shape must be chosen and locked so that templates, validators, and the `constraints-model-guide.md` may bind to it.

## Decision

`constraints.yml` is a single YAML document with **eight top-level fields**. `entities` and `invariants` are required; the remaining six are optional. New fields may be added only as optional; removals require a major schema bump.

| Field | Type | Required | Shape |
|---|---|---|---|
| `entities` | list-of-strings | yes | `[string]` |
| `invariants` | list-of-strings | yes | `[string]` |
| `forbidden_vocabulary` | list-of-strings | no | `[string]` |
| `numeric_ceilings` | map (string→number) | no | `{string: number}` |
| `state_variables` | list-of-strings | no | `[string]` |
| `actions` | list-of-strings | no | `[string]` |
| `mandatory_artifacts` | list-of-strings (paths) | no | `[string]` |
| `citations` | list-of-objects | no | `[{work, chapter, page}]` |

Canonical author order and full examples live in `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`.

## Consequences

**Positive.**
- Rule-checkable end-to-end — every field has at least one deterministic consumer, satisfying the PRD R-1 rejection criterion.
- Small surface area (8 fields) resists scope creep.
- YAML is already the config language of `.delivery/config.yml`; no new parser dependency.
- Structured `citations` enable mechanical Löwy-rule enforcement (PRD AC-4).

**Negative.**
- Schema lock-in: downstream validators bind to exact key names; renaming requires a coordinated migration.
- YAML's permissiveness (implicit typing, indent sensitivity) invites author errors; mitigated by templates and parse-error reporting in the validator.
- Structured citations cost three keys per entry versus a free-form string.

## Alternatives Considered

1. **JSON.** More rigid, better tooling in some ecosystems. *Rejected*: less human-friendly for hand-authoring at checkpoint time; quoting overhead hurts glance-ability; inconsistent with existing `.delivery/config.yml` YAML idiom.
2. **TOML.** Excellent for flat key-value, poor for nested lists-of-objects (citations). *Rejected*: shape mismatch.
3. **Single nested block inside `.delivery/config.yml`.** *Rejected*: violates stage artifact isolation — config is global, `constraints.yml` must live alongside the stage's other artifacts for per-run versioning and sibling DoD walks.
4. **Markdown with YAML frontmatter.** *Rejected*: the user has previously flagged markdown-with-frontmatter as incorrect for config-shaped files (memory: `feedback_config_format.md`). Pure YAML honors that standard.

## Rationale

YAML wins on three axes simultaneously: ecosystem fit (existing config file is YAML), author ergonomics (human-glance at checkpoint), and parser ubiquity (PyYAML in the existing BRE stack). The 8-field shape is the smallest set where each field has a named consumer in the PRD — anything fewer drops a required check; anything more violates R-1.
