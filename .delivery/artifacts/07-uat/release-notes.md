# Release Notes: Deterministic Rules Engine Integration

**Version**: 2.11.0
**Release Date**: 2026-03-28
**Config Schema**: v2.3 -> v2.4

---

## What's New

### Deterministic Rules Engine for the Delivery Pipeline

The delivery-flow pipeline now evaluates all flow-control decisions -- stage routing, DoD gates, escalation triggers, and collaboration pattern selection -- through a deterministic rules engine. Given the same structured inputs and config, the engine produces identical results every time.

Previously, routing and gate decisions were made by AI interpretation of prose instructions. This produced non-deterministic behavior: identical project signals could yield different routing across runs. The rules engine eliminates that variance for all flow-control decisions while keeping AI where it belongs -- creative work like artifact production, code review, and feedback synthesis.

**Key capabilities:**

- **Deterministic stage routing.** A 126-cell routing matrix (6 project types x 7 stages x 3 risk tolerances) determines stage depth. Same inputs always produce the same routing map.

- **Rule-based DoD gate evaluation.** 55 gate criteria across 7 stages, evaluated with weighted scoring against configurable pass thresholds. Every gate returns a structured result with pass/fail, score, rule-by-rule breakdown, and reason.

- **Preset profiles.** Three built-in profiles cover common workflows:
  - **solo** -- Minimal ceremony. Fewer validators, lower thresholds, faster iteration. Best for solo developers, prototypes, and tight loops.
  - **standard** -- Balanced defaults matching the previous SKILL.md routing baseline. Best for small-to-medium teams and most feature work.
  - **strict** -- Full ceremony. Security validator on every gate. Warnings become blocking. No AI fallback on gate decisions. Full audit trail required. Best for regulated environments and enterprise use.

- **4-layer rule resolution.** Rules resolve bottom-up: plugin defaults (Layer 1) -> preset profile (Layer 2) -> per-repo config overrides (Layer 3) -> per-run overrides (Layer 4). Each layer can override the previous. In strict mode, Layer 4 (per-run) is disabled entirely.

- **Full audit trail.** Every rule evaluation is logged to `.delivery/audit/audit-<pipeline_id>.jsonl` with timestamp, gate ID, rule ID, input context, pass/fail, score, reason, determinism category (a/b/c), and resolution layer. Sufficient for compliance audits (SOC2, ISO 27001).

- **Dry-run mode.** Run `python evaluate_rules.py --dry-run` to see exactly what the rules engine will decide before committing to a pipeline run. Includes a `--compare` flag that shows side-by-side differences between your config overrides and the default routing.

- **Escalation rules.** Six escalation triggers with three sensitivity profiles (relaxed, balanced, eager). Deterministic threshold-based intervention when stages struggle -- max iterations, repeated failures, and deadlock timeouts.

- **Setup wizard extension.** Three new wizard questions (W-15: Rule Profile, W-16: Rule Customizations, W-17: Escalation Sensitivity) guide initial configuration with auto-detection from existing project settings.

---

## Config Migration: v2.3 to v2.4

### No Action Required

Existing v2.3 configs work unchanged with the v2.4 codebase. The rules engine applies sensible defaults for every `rules.*` key when those keys are absent:

| Key | Default |
|-----|---------|
| `rules.enabled` | `true` |
| `rules.preset` | `standard` |
| `rules.strict_mode` | `false` |
| `rules.escalation_sensitivity` | `balanced` |
| `rules.pass_threshold` | Preset defaults |
| `rules.routing_overrides` | Preset defaults |
| `rules.required_validators` | Preset defaults |
| `rules.custom` | None |

The pipeline will display an informational message on session start: "Config v2.3 detected. Rules engine defaults apply. Run the setup wizard to configure rules.* options (questions W-15 through W-17)." This message is not blocking.

### Minimal Manual Migration

To silence the migration notice and explicitly opt into the rules engine defaults, add to `.delivery/config.yml`:

```yaml
config_version: "2.4"

rules:
  preset: standard
  escalation_sensitivity: balanced
```

Or run the setup wizard, which appends the `rules.*` section and bumps the version automatically.

---

## Feature Flag: `rules.enabled`

A master kill switch is available. Set `rules.enabled: false` in `.delivery/config.yml` to disable the entire rules engine with zero overhead. The pipeline immediately falls back to the previous AI-interpreted routing behavior. No git revert, no branch switching -- one line.

```yaml
rules:
  enabled: false
```

When disabled, the CLI exits immediately with a passthrough response and the orchestrator uses pre-rules-engine behavior for all decisions. This flag is checked before any rule loading or evaluation occurs.

---

## Breaking Changes

None. This release is fully backward-compatible:

- v2.3 configs work unchanged with v2.4 codebase
- The `standard` preset defaults match the previous SKILL.md routing baseline as closely as possible
- The `rules.enabled: false` flag provides instant rollback to pre-rules behavior
- All new Python scripts use stdlib only -- no new dependencies, no pip install, no build step

---

## New Files

### Scripts (delivery-team/scripts/)

| File | Purpose |
|------|---------|
| `condition_evaluator.py` | Standalone condition evaluation engine (AND/OR/NOT, comparisons, regex) |
| `delivery_rules_adapter.py` | 4-layer rule resolution, routing and gate evaluation |
| `yaml_to_rules.py` | YAML-to-JSON translation with type coercion detection |
| `evaluate_rules.py` | CLI entry point with route, gate, and resolve actions |

### Rule Specifications (delivery-team/skills/delivery-flow/references/rules/)

| File | Purpose |
|------|---------|
| `stage-routing.json` | 126-cell routing decision matrix |
| `dod-gates.json` | 55 gate criteria across 7 stages |
| `escalation-rules.json` | 6 triggers, 3 sensitivity profiles |
| `collaboration-patterns.json` | Per-stage pattern selection rules |
| `presets/solo.json` | Solo/prototype preset profile |
| `presets/standard.json` | Default balanced preset profile |
| `presets/strict.json` | Enterprise/compliance preset profile |

---

## Known Limitations

| Item | Description | Status |
|------|-------------|--------|
| SKILL.md integration pending | The rules engine scripts and specifications are complete. Integration into the SKILL.md orchestrator (Phase 3) is specified but not yet applied. Full pipeline dogfooding requires this integration. | Tracked for Phase 3 PR |
| Wizard extension not yet merged | Setup wizard questions W-15/W-16/W-17 are designed and specified but not yet merged into setup-wizard.md. | Tracked for Phase 3 PR |
| Config schema v2.4 merge pending | The 12 new `rules.*` config keys are specified in `config-schema-v2.4-additions.md` but not yet merged into `config-schema.md`. | Tracked for Phase 3 PR |
| YAML parsing is hybrid | The orchestrator (AI) reads the YAML file and passes structured data to the translation layer. This step is non-deterministic. In strict mode, the translation layer promotes coercion warnings to hard errors to mitigate this. | By design -- see Determinism Boundary in PRD Section 5 |
| [#50](https://github.com/P47Phoenix/Claude-Plugins/issues/50) | Alias injection bug in alias-creator | Open, pre-existing, out of scope |

---

## Rollback Procedure

Three rollback levels are available, from fastest to most thorough:

| Level | Action | When to Use |
|-------|--------|-------------|
| **1 -- Config flag** | Set `rules.enabled: false` | Wrong routing, gates too strict/lenient, engine crashes |
| **2 -- Revert SKILL.md** | `git checkout <pre-phase-3> -- delivery-team/skills/delivery-flow/SKILL.md` | Orchestrator loop or context assembly issues |
| **3 -- Full revert** | `git revert` the phase merge commits | Fundamental design flaw discovered |

Level 1 takes seconds and requires no git changes. Level 2 and 3 take minutes.

---

## Documentation Updates Required

| File | Change | Priority |
|------|--------|----------|
| `CLAUDE.md` | Update config schema version note from v2.3 to v2.4 | P0 |
| `config-schema.md` | Merge `config-schema-v2.4-additions.md` (12 new keys) | P0 |
| `setup-wizard.md` | Merge `wizard-extension.md` (W-15, W-16, W-17) | P0 |
| `delivery-team/README.md` | Add rules engine to delivery-flow skill description | P1 |
| `marketplace.json` | Version bump at merge time | P1 |
