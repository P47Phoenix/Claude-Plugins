# Config Schema v2.4 Additions: `rules.*` Section

**Version**: 2.4
**Date**: 2026-03-28
**Author**: Gimli, Developer (delivery-team)
**Traces To**: PRD FR-12, US-12
**Status**: Ready to merge into config-schema.md

> This file documents the new `rules.*` keys to be merged into the Complete Schema table in `config-schema.md`. After merge, bump `config_version` from "2.3" to "2.4" and add the version history entry.

---

## New Schema Rows

| Key | Type | Required | Default | Valid Values | Wizard Q# | Consumed By |
|-----|------|----------|---------|-------------|-----------|-------------|
| `rules.enabled` | boolean | no | true | true, false | defaults | evaluate_rules.py (master switch: when false, all rule evaluation is bypassed and the orchestrator uses AI-driven decisions as before v2.4) |
| `rules.preset` | string | no | "standard" | solo, standard, strict | W-15 | evaluate_rules.py (Layer 2 preset selection) |
| `rules.strict_mode` | boolean | no | false | true, false | W-15 (implied by strict preset) | evaluate_rules.py (Layer 4 disable, coercion warnings become errors, no AI fallback on rule engine failure) |
| `rules.routing_overrides` | map[string, map[string, string]] | no | {} | project_type -> stage_name -> "full"/"light" | W-16 | evaluate_rules.py (Layer 3 routing overrides) |
| `rules.gate_overrides` | map[string, object] | no | {} | gate_id -> {pass_threshold: int, required_validators: [string]} | W-16 | evaluate_rules.py (Layer 3 gate overrides: per-stage pass thresholds and required validator lists) |
| `rules.escalation` | object | no | see sub-keys | see sub-keys below | W-17 | evaluate_rules.py (escalation behavior) |
| `rules.escalation.sensitivity` | string | no | "balanced" | relaxed, balanced, aggressive | W-17 | evaluate_rules.py (selects sensitivity profile from escalation-rules.json) |
| `rules.escalation.max_iterations_override` | map[string, integer] | no | {} | stage_name -> integer (1-10) | W-17 | evaluate_rules.py (per-stage max iteration override, takes precedence over sensitivity profile) |
| `rules.escalation.repeated_failure_override` | integer/null | no | null | integer (1-5) or null | W-17 | evaluate_rules.py (global repeated failure threshold override) |
| `rules.dod_overrides` | map[string, list[string]] | no | {} | stage_name -> [validator_names] | W-16 | evaluate_rules.py (Layer 3 per-stage DoD validator list overrides, replaces dod_validators.<stage> for rule evaluation) |
| `rules.limits_overrides` | map[string, integer] | no | {} | limit_name -> integer | W-16 | evaluate_rules.py (Layer 3 overrides for pipeline.max_self_correction, pipeline.max_dod_rounds, etc.) |
| `rules.custom` | list[object] | no | [] | list of {field, operator, value, gate, severity, description} | W-16 | evaluate_rules.py (user-defined custom rule conditions injected into gate evaluation) |

---

## Sub-key Details

### `rules.escalation`

| Sub-key | Type | Default | Description |
|---------|------|---------|-------------|
| `sensitivity` | string | "balanced" | Which sensitivity profile to use from escalation-rules.json. Controls max_iterations, repeated_failure_threshold, deadlock_timeout, adversarial_confidence_floor, no_progress_threshold, and decision_deadlock_threshold. |
| `max_iterations_override` | map | {} | Per-stage override for max iterations. Key is stage name (idea, refine, design, architect, plan, development, uat). Value is integer 1-10. Overrides the sensitivity profile value for that stage only. |
| `repeated_failure_override` | integer/null | null | Global override for repeated_failure_threshold. When set, overrides the sensitivity profile value across all stages. |

### `rules.gate_overrides`

Map where keys are gate IDs (e.g., `idea_dod`, `refine_dod`, `development_dod`) and values are objects with optional keys:

| Sub-key | Type | Default | Description |
|---------|------|---------|-------------|
| `pass_threshold` | integer | (from dod-gates.json) | Override the pass threshold for this gate. Range: 0-100. |
| `required_validators` | list[string] | (from dod-gates.json) | Override the required validator list. Only these validators must pass for a GO decision. |

### `rules.limits_overrides`

Map where keys are limit names and values are integers:

| Limit Name | Corresponding Pipeline Key | Default | Range |
|-----------|---------------------------|---------|-------|
| `max_self_correction` | `pipeline.max_self_correction` | 3 | 1-10 |
| `max_dod_rounds` | `pipeline.max_dod_rounds` | 3 | 1-10 |
| `delegation_retry_max` | `pipeline.delegation_retry_max` | 2 | 1-5 |

### `rules.custom`

List of custom rule objects. Each object has:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field` | string | yes | Dot-notation field path evaluated against context (e.g., `artifacts.test_coverage`) |
| `operator` | string | yes | Comparison operator: ==, !=, >, <, >=, <=, IN, NOT_IN, IS_NULL, IS_NOT_NULL, MATCHES |
| `value` | any | yes (except IS_NULL/IS_NOT_NULL) | Value to compare against |
| `gate` | string | yes | Which gate this rule applies to (e.g., `development_dod`, `uat_dod`, or `all`) |
| `severity` | string | no (default: "warning") | blocking, warning, suggestion |
| `description` | string | yes | Human-readable description of what this rule checks |

---

## Defaults by Project Type (additions)

No project-type-specific defaults for `rules.*` keys. All project types use the same defaults listed above. Project-type-specific behavior is driven by `rules.routing_overrides` and `rules.gate_overrides` when configured.

---

## Config File Template Addition

Add this section to the config template after the `presentation` section:

```yaml
rules:
  enabled: true
  preset: standard
  strict_mode: false
  routing_overrides: {}
  gate_overrides: {}
  escalation:
    sensitivity: balanced
    max_iterations_override: {}
    repeated_failure_override: null
  dod_overrides: {}
  limits_overrides: {}
  custom: []
```

---

## Version History Entry

| Version | Date | Changes |
|---------|------|---------|
| 2.4 | 2026-03-28 | Added `rules.*` section: rules.enabled (master switch), rules.preset (solo/standard/strict), rules.strict_mode, rules.routing_overrides, rules.gate_overrides, rules.escalation (sensitivity, max_iterations_override, repeated_failure_override), rules.dod_overrides, rules.limits_overrides, rules.custom (user-defined rule conditions). Supports deterministic rules engine integration (escalation-rules.json, collaboration-patterns.json, dod-gates.json). |

---

## Migration Notes (v2.3 to v2.4)

When the pipeline detects `config_version: "2.3"`:

1. Add `rules` section with all defaults listed above.
2. Write migration message to stderr: `[MIGRATION] config v2.3 -> v2.4: rules section added with default values (rules engine enabled with standard preset)`.
3. Update `config_version` to `"2.4"`.
4. If any existing keys conflict with the new `rules.*` namespace (unlikely but possible with custom keys), halt with exit code 1 and list conflicts on stderr.

No existing keys are renamed or removed. Migration is strictly additive.

---

## Wizard Questions (references only -- implementation in setup-wizard.md)

| # | Question | Maps To |
|---|----------|---------|
| W-15 | "Which rules preset fits your team?" (auto-detect from team.size + risk_tolerance; options: solo, standard, strict) | `rules.preset`, `rules.strict_mode` |
| W-16 | "Any gate or routing overrides?" (conditional, only if preset != solo; options: threshold overrides, routing overrides, custom rules, skip) | `rules.gate_overrides`, `rules.routing_overrides`, `rules.dod_overrides`, `rules.limits_overrides`, `rules.custom` |
| W-17 | "Escalation sensitivity?" (options: relaxed, balanced, aggressive; default derived from risk_tolerance) | `rules.escalation.sensitivity` |

---

## Extension Protocol Checklist

| Step | Action | Status |
|------|--------|--------|
| 1. Add to Schema | 12 new rows in Complete Schema table | Defined in this file |
| 2. Bump Version | 2.3 -> 2.4 | Required at merge time |
| 3. Add Wizard Questions | W-15, W-16, W-17 | Defined (implementation in setup-wizard.md) |
| 4. Add to Pipeline Config Table | `rules.*` consumed by evaluate_rules.py | Defined |
| 5. Add Migration Note | v2.4 version history entry | Defined in this file |
| 6. Update Consuming Skill | SKILL.md rules engine protocol | Phase 3 (US-16) |
| 6.5. Regenerate JSON Schema | Run generate-schema.py after merge | Required after merge |
