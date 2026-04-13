# Config Schema Reference

Single source of truth for `.hardware/config.yml` format. The setup wizard, pipeline, and all skills reference this file for config keys, types, defaults, and valid values.

## Current Version: 1.0

`.hardware/config.yml` is a pure YAML file. No frontmatter delimiters (`---`). The file is created by the `hw-setup` wizard or manually by the user.

When adding new config keys, bump the version and add a migration note. Follow the Extension Protocol at the end of this document.

## Complete Schema

| Key | Type | Required | Default | Valid Values | Wizard Q# | Consumed By |
|-----|------|----------|---------|-------------|-----------|-------------|
| `schema_version` | string | yes | "1.0" | semver string | auto | hardware-flow (migration check), validate_config.py |
| `project_name` | string | yes | (none) | non-empty string | Q1 | hardware-flow (pipeline identity) |
| `target_fab` | enum | no | jlcpcb | jlcpcb, pcbway, custom | Q2 | DFM gate (fab-specific rules), manufacturing-engineer (ordering package) |
| `custom_fab_name` | string | no | "" | non-empty string (only when target_fab: custom) | Q2 | manufacturing-engineer (custom fab identification) |
| `compliance_regions` | list[string] | no | [] | each item: fcc, ce, ul, rohs, reach, none | Q3 | compliance-engineer (region checklists), Compliance gate |
| `bom_budget` | number/null | no | null | positive number or null (null = no limit) | Q4 | BOM gate (cost threshold) |
| `second_source_required` | boolean | no | false | true/false | Q4 | BOM gate (single-source blocking) |
| `production_volume` | enum | no | prototype | prototype, small-batch, production | Q5 | pipeline (stage depth adaptation), DFM gate |
| `board_layers` | integer | no | 2 | 1, 2, 4, 6, 8 | Q6 | pcb-layout-engineer (stackup constraints), DFM gate (layer compatibility) |
| `dependencies.kicad_happy_version` | string | no | ">=1.2.0" | semver range string | Q7 | SessionStart hook (version compatibility check) |
| `rework.max_rework_iterations` | integer | no | 3 | positive integer >= 1 | Q8 | hardware-flow (per-path rework termination) |
| `rework.max_total_reworks` | integer | no | 10 | positive integer >= 1 | Q9 | hardware-flow (pipeline-wide rework termination) |
| `gate_strictness` | enum | no | standard | strict, standard, relaxed | Full mode | all gates (finding severity threshold) |
| `pipeline.staleness_warning_days` | integer | no | 7 | positive integer >= 1 | defaults | SessionStart hook (paused pipeline warning) |
| `pipeline.staleness_critical_days` | integer | no | 30 | positive integer >= 1, must be > staleness_warning_days | defaults | SessionStart hook (critical staleness warning) |
| `review.schematic_review_passes` | integer | no | 2 | integer 1-5 | Full mode | electrical-engineer (parallel reviewer count) |
| `review.design_review_board` | boolean | no | true | true/false | Full mode | hardware-flow (multi-role Design Review Board) |
| `memory.entries_limit` | integer | no | 100 | positive integer >= 10 | defaults | hardware-flow (memory retrieval cap) |

## Example Config (v1.0)

```yaml
# .hardware/config.yml -- Schema v1.0
schema_version: "1.0"

# Project identity
project_name: "sensor-board-v2"

# Fabrication target
target_fab: jlcpcb           # Enum: jlcpcb | pcbway | custom
custom_fab_name: ""          # Only used when target_fab: custom

# Compliance regions
compliance_regions:           # List of: fcc | ce | ul | rohs | reach | none
  - fcc
  - ce

# BOM constraints
bom_budget: 12.50            # USD per unit. null = no limit
second_source_required: false # If true, BOM Gate blocks single-source components

# Production volume
production_volume: small-batch  # Enum: prototype | small-batch | production

# Board complexity
board_layers: 4              # Integer: 1, 2, 4, 6, 8

# Dependencies
dependencies:
  kicad_happy_version: ">=1.2.0"  # Minimum compatible kicad-happy version

# Rework limits
rework:
  max_rework_iterations: 3   # Per individual rework path
  max_total_reworks: 10       # Across all paths in a pipeline run

# Gate strictness
# strict: critical, major, AND minor findings all block the gate
# standard: critical and major findings block; minor findings pass (logged)
# relaxed: only critical findings block; major findings pass (logged as warning)
gate_strictness: standard    # Enum: strict | standard | relaxed

# Staleness detection
pipeline:
  staleness_warning_days: 7           # Days paused before warning
  staleness_critical_days: 30         # Days paused before critical warning

# Review configuration
review:
  schematic_review_passes: 2  # Number of parallel reviewer passes (1-5)
  design_review_board: true   # Enable multi-role Design Review Board at key transitions

# Memory configuration
memory:
  entries_limit: 100          # Max memory entries for retrieval
```

## Field Validation Rules

| Field | Required | Type | Default | Validation |
|---|---|---|---|---|
| `schema_version` | Yes | string | "1.0" | Must match known schema versions |
| `project_name` | Yes | string | (none) | Non-empty string, max 100 chars |
| `target_fab` | No | enum | jlcpcb | One of: jlcpcb, pcbway, custom |
| `custom_fab_name` | No | string | "" | Non-empty when target_fab is custom; ignored otherwise |
| `compliance_regions` | No | list | [] | Each item one of: fcc, ce, ul, rohs, reach, none |
| `bom_budget` | No | number/null | null | Positive number or null |
| `second_source_required` | No | boolean | false | true/false |
| `production_volume` | No | enum | prototype | One of: prototype, small-batch, production |
| `board_layers` | No | integer | 2 | One of: 1, 2, 4, 6, 8 |
| `dependencies.kicad_happy_version` | No | string | ">=1.2.0" | Semver range string |
| `rework.max_rework_iterations` | No | integer | 3 | Positive integer >= 1 |
| `rework.max_total_reworks` | No | integer | 10 | Positive integer >= 1 |
| `gate_strictness` | No | enum | standard | One of: strict, standard, relaxed |
| `pipeline.staleness_warning_days` | No | integer | 7 | Positive integer >= 1 |
| `pipeline.staleness_critical_days` | No | integer | 30 | Positive integer >= 1, must be > staleness_warning_days |
| `review.schematic_review_passes` | No | integer | 2 | Integer 1-5 |
| `review.design_review_board` | No | boolean | true | true/false |
| `memory.entries_limit` | No | integer | 100 | Positive integer >= 10 |

## Config-Driven Stage Depth

The config influences pipeline behavior based on project type and settings. In Phase 1, the pipeline structure (all 8 stages) does not change, but gate behavior adapts.

| Config Value | Effect on Pipeline |
|---|---|
| `target_fab: jlcpcb` | DFM gate uses JLCPCB-specific rules; manufacturing-engineer invokes kicad-happy:jlcpcb |
| `target_fab: pcbway` | DFM gate uses PCBWay rules; manufacturing-engineer invokes kicad-happy:pcbway |
| `compliance_regions: [fcc, ce]` | Compliance gate produces checklists for both FCC and CE; both must pass |
| `compliance_regions: []` or `[none]` | Compliance gate runs minimal checks only |
| `bom_budget: 12.50` | BOM gate compares total cost against $12.50; over-budget triggers NOT_DONE |
| `bom_budget: null` | BOM gate skips cost threshold check |
| `board_layers: 4` | Layout stage knows stackup constraints; DFM gate validates 4-layer compatibility |
| `production_volume: prototype` | Relaxed gate thresholds appropriate for prototype quantities |
| `production_volume: production` | Full rigor; all compliance and manufacturing checks enforced |
| `gate_strictness: strict` | Critical, major, and minor findings all block gates |
| `gate_strictness: relaxed` | Only critical findings block gates |
| `rework.max_rework_iterations: 3` | Each individual rework path terminates after 3 iterations |
| `rework.max_total_reworks: 10` | Pipeline-wide rework cap; escalates to human when hit |

## Forward Compatibility Protocol

Following delivery-flow's extension protocol:

1. **Missing keys use defaults** -- a v1.0 config loaded by a v1.1 schema plugin uses defaults for new keys. Never fail on absent keys.
2. **Unknown keys are ignored** -- a v1.1 config loaded by a v1.0 schema plugin ignores keys it does not recognize. Never fail on extra keys.
3. **`schema_version` enables migration guidance** -- when old config meets new schema, the SessionStart hook announces: "Config uses schema vX.Y. Current schema is vA.B. New settings applied with defaults: [list]."
4. **Invalid values warn and use defaults** -- never fail the pipeline due to config errors. Invalid `target_fab: "invalid"` warns and uses `jlcpcb`.

## Extension Protocol (for Future Schema Versions)

When adding new config keys in future versions:

1. Add the key to the schema with a sensible default
2. Increment schema_version (minor for additive, major for breaking)
3. Update this document with the new key documentation
4. Update `validate_config.py` to validate the new key
5. Ensure all code paths handle the key being absent (default fallback)

## Security

All YAML parsing MUST use `yaml.safe_load()` (never `yaml.load()` or `yaml.FullLoader`). This prevents YAML deserialization attacks. See architecture Section 14.1.
