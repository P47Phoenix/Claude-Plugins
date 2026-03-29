# User Guide: Deterministic Rules Engine

**Version**: 2.11.0
**Date**: 2026-03-28
**Author**: Bilbo (Technical Writer)

> *"I think I'm quite ready for another documentation adventure."*

---

## Table of Contents

1. [Overview](#1-overview)
2. [Getting Started](#2-getting-started)
3. [Preset Profiles](#3-preset-profiles)
4. [Configuring Rules in config.yml](#4-configuring-rules-in-configyml)
5. [Using Dry-Run Mode](#5-using-dry-run-mode)
6. [Reading the Audit Trail](#6-reading-the-audit-trail)
7. [Troubleshooting](#7-troubleshooting)
8. [Reference: Config Keys](#8-reference-config-keys)

---

## 1. Overview

The rules engine makes all pipeline flow-control decisions -- stage routing, DoD gate pass/fail, escalation triggers, and collaboration pattern selection -- using deterministic rules instead of AI interpretation. Given the same inputs and config, the engine produces identical results every time.

AI continues to handle all creative work: writing artifacts, conducting reviews, brainstorming, synthesizing feedback. The rules engine handles the mechanical decisions about which stages run, at what depth, whether a gate passes, and when to escalate.

### How It Works

Rules resolve through a 4-layer system, where each layer can override the previous:

```
Layer 1 (Plugin Defaults)     Built-in rules shipped with the plugin
        |
Layer 2 (Preset Profile)      solo / standard / strict
        |
Layer 3 (Per-Repo Config)     Your .delivery/config.yml overrides
        |
Layer 4 (Per-Run Override)    Session-scoped natural language overrides
```

Most users only need to pick a preset (Layer 2). Power users can add per-repo overrides (Layer 3). In strict mode, Layer 4 (per-run overrides) is disabled entirely for maximum determinism.

---

## 2. Getting Started

### If You Already Have a Project

Your existing `.delivery/config.yml` (v2.3) works unchanged. The rules engine applies the `standard` preset by default. On your next session, you will see an informational message:

```
[MIGRATION] Config v2.3 detected. Rules engine defaults apply.
Run the setup wizard to configure rules.* options (questions W-15 through W-17).
```

This message is not blocking. Your pipeline runs normally.

To silence the message and explicitly configure rules, either:

**Option A -- Run the setup wizard** (recommended). The wizard asks three new questions and writes the `rules.*` section for you.

**Option B -- Edit config.yml manually.** Add the following and bump the version:

```yaml
config_version: "2.4"

rules:
  preset: standard          # solo | standard | strict
  escalation_sensitivity: balanced  # relaxed | balanced | aggressive
```

### If You Are Starting a New Project

Run the setup wizard. After the existing questions (Q1-Q14), three new questions appear:

- **W-15: Rule Profile** -- Picks your preset (solo/standard/strict). Auto-detected from your risk tolerance answer.
- **W-16: Rule Customizations** -- Shown only if you choose "customize" or auto-detection confidence is low. Lets you override specific routing, validators, or thresholds.
- **W-17: Escalation Sensitivity** -- How quickly the pipeline intervenes when a stage struggles (relaxed/balanced/eager).

### Disabling the Rules Engine

Set one line in your config to disable the entire engine and revert to previous AI-interpreted behavior:

```yaml
rules:
  enabled: false
```

The pipeline immediately falls back to pre-rules behavior. No code changes, no git operations. This flag is checked before any rule loading occurs -- zero overhead when disabled.

---

## 3. Preset Profiles

Presets configure routing depth, validator counts, gate thresholds, and escalation behavior as a single named package. Pick the one that matches your workflow.

### solo -- For Solo Developers and Prototypes

**When to use:** You work alone or in a very small team. You value speed over ceremony. You want the pipeline to help without slowing you down.

**What it does:**
- Most stages run at `light` depth (reduced scope, not skipped)
- 1 validator per gate (instead of the full validator set)
- Lower pass thresholds (70% default)
- Warnings are non-blocking (reported but do not halt the pipeline)
- Fastest iteration -- fewer validators, lighter stages, quicker gates

**Typical config:**
```yaml
rules:
  preset: solo
  escalation_sensitivity: balanced
```

### standard -- The Default for Most Teams

**When to use:** You are on a small-to-medium team doing regular feature work. You want a balance between thoroughness and speed. This preset matches the previous SKILL.md routing baseline.

**What it does:**
- Full depth for Development and UAT; light depth for most other stages
- Full validator set per stage
- Standard pass thresholds (80% default)
- 3 collaboration patterns enabled
- Warnings are warnings (reported, reviewed, but not blocking)

**Typical config:**
```yaml
rules:
  preset: standard
  escalation_sensitivity: balanced
```

### strict -- For Regulated and Enterprise Environments

**When to use:** You work in a regulated environment (SOC2, ISO 27001, HIPAA, PCI-DSS). You need auditable gate decisions. You cannot accept AI fallback on any flow-control decision.

**What it does:**
- Full depth for most stages
- Security validator added to every gate
- Warnings promoted to blocking (must be resolved before a gate passes)
- No AI fallback on any gate decision -- if the rules engine errors, the pipeline halts
- Layer 4 (per-run overrides) is disabled entirely
- Full audit trail required for every run
- YAML type coercion warnings become hard errors

**Typical config:**
```yaml
rules:
  preset: strict
  strict_mode: true
  escalation_sensitivity: balanced
```

---

## 4. Configuring Rules in config.yml

All rule configuration lives under the `rules` key in `.delivery/config.yml`. The preset handles most settings. Override individual keys only when the preset does not match your needs.

### Minimal Configuration

Two lines are all most users need:

```yaml
rules:
  preset: solo
  escalation_sensitivity: balanced
```

### Overriding Gate Thresholds

Set per-stage pass thresholds (0-100). Higher values require a higher score to pass the gate. Only listed stages are overridden; all others use preset defaults.

```yaml
rules:
  preset: standard
  pass_threshold:
    design: 90        # We care deeply about design quality
    development: 85   # Standard bar for code
    uat: 95           # High bar for user acceptance
```

### Overriding Routing Depth

Control which stages run at `full` or `light` depth for specific project types. Only listed combinations are overridden.

```yaml
rules:
  routing_overrides:
    BUG_FIX:
      architect: light    # Bug fixes skip deep architecture review
      design: light       # Bug fixes get lightweight design pass
    SPIKE:
      uat: light          # Spikes get lightweight UAT
```

Valid project types: `GREENFIELD`, `FEATURE`, `BUG_FIX`, `GAME_DEV`, `SPIKE`, `DOCS_ONLY`.
Valid depths: `full`, `light`. Light means reduced scope -- not skipped.

### Overriding Required Validators

Replace the preset's validator list for specific stages. Unlisted stages keep preset defaults.

```yaml
rules:
  required_validators:
    development: [developer, qa, architect, security]
    uat: [qa, devops, po, security, tech-writer]
```

### Adding Custom Rules (Advanced)

For requirements that presets and overrides cannot express, define custom gate rules:

```yaml
rules:
  custom:
    - field: "artifacts.prd.sections.length"
      operator: ">="
      value: 5
      gate: "refine_dod"
      description: "PRD must have at least 5 sections"
```

Custom rules are evaluated alongside preset rules. They add to the gate criteria; they do not replace preset rules.

### Escalation Sensitivity

Controls how quickly the pipeline intervenes when a stage struggles:

| Setting | Max Iterations | Repeated Failures | Deadlock Timeout | Best For |
|---------|---------------|-------------------|------------------|----------|
| `relaxed` | 5 | 3 | 10 minutes | Exploratory work, learning |
| `balanced` | 3 | 2 | 5 minutes | Most work (default) |
| `aggressive` | 2 | 1 | 3 minutes | Time-sensitive, deadline-driven |

```yaml
rules:
  escalation_sensitivity: relaxed
```

### Strict Mode

Enable strict mode for maximum determinism and auditability:

```yaml
rules:
  strict_mode: true
```

When strict mode is on:
- Layer 4 (per-run overrides) is disabled. Only Layers 1-3 apply.
- YAML type coercion warnings become hard errors.
- If the rules engine encounters an error, the pipeline halts (no AI fallback).
- The audit trail tags each decision with its determinism category.

---

## 5. Using Dry-Run Mode

Dry-run lets you see exactly what the rules engine will decide before committing to a pipeline run. This is the primary trust-building tool -- you can verify that your config produces the routing, thresholds, and escalation behavior you expect.

### Basic Dry-Run

```bash
python delivery-team/scripts/evaluate_rules.py \
  --context .delivery/tmp/context-routing.json \
  --rules-dir delivery-team/skills/delivery-flow/references/rules/ \
  --config .delivery/config.yml \
  --dry-run
```

This outputs a human-readable summary showing:
- Resolved routing map (which stages, what depth, which layer provided each value)
- Gate thresholds per stage with source layer
- Escalation thresholds
- Determinism summary (count of fully deterministic vs hybrid vs AI-driven decisions)
- A JSON block for machine consumption

**Example output:**

```
=== DRY RUN: Rules Engine Evaluation ===
Config: .delivery/config.yml (v2.4)
Preset: solo (Layer 2)
Strict mode: off

--- Resolved Routing Map ---
Project type: FEATURE | Risk tolerance: standard

  Stage          Depth    Source
  -------        -----    ------
  1. Idea        light    Layer 2 (solo preset)
  2. Refine      light    Layer 2 (solo preset)
  3. Design      light    Layer 2 (solo preset)
  4. Architect   light    Layer 2 (solo preset)
  5. Plan        light    Layer 2 (solo preset)
  6. Development full     Layer 2 (solo preset)
  7. UAT         light    Layer 2 (solo preset)

  Active stages: 7 (5 light, 2 full)
```

Every row includes a "Source" column showing which layer provided the value. This is how you verify your overrides are taking effect.

### Compare Mode

Add `--compare` to see a side-by-side diff between your config and the defaults:

```bash
python delivery-team/scripts/evaluate_rules.py \
  --context .delivery/tmp/context-routing.json \
  --rules-dir delivery-team/skills/delivery-flow/references/rules/ \
  --config .delivery/config.yml \
  --dry-run --compare
```

This appends a comparison table showing which values differ, which layer changed them, and a plain-English summary of the impact:

```
=== COMPARISON: Rule-Based vs Default Routing ===

  Stage          Rules Engine    Default (no overrides)    Delta
  -------        ------------    ----------------------    -----
  3. Design      light (L3)      full                      CHANGED (Layer 3 override)
  7. UAT         light (L3)      full                      CHANGED (Layer 3 override)

  Summary: Your config reduces Design and UAT from full to light depth
  for FEATURE projects.
```

### CLI Actions

The CLI supports three actions:

| Action | Purpose | Example |
|--------|---------|---------|
| `route` | Evaluate stage routing for a project context | `--action route` |
| `gate` | Evaluate a DoD gate for a specific stage | `--action gate --stage design` |
| `resolve` | Show the fully resolved rule set across all 4 layers | `--action resolve` |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (or rules engine disabled via `rules.enabled: false`) |
| 1 | Argument or configuration error |
| 2 | Rule evaluation error |

---

## 6. Reading the Audit Trail

Every rule evaluation during a pipeline run is logged to `.delivery/audit/audit-<pipeline_id>.jsonl`. The audit trail serves two audiences: the developer who just ran the pipeline (quick summary) and the auditor reviewing it later (complete traceability).

### Post-Run Summary

After each pipeline run, the orchestrator displays a summary:

```
=== Pipeline Run Summary ===
Pipeline ID:  pipe-20260328-143200
Stages run:   7 (5 light, 2 full)
Preset:       solo

--- Decision Log ---
  Stage       Gate Result    Score    Determinism    Iterations
  -------     -----------    -----    -----------    ----------
  Idea        GO             85.0     (a) full       1
  Refine      GO             90.0     (b) hybrid     1
  Design      RECYCLE->GO    78.0     (b) hybrid     2
  Architect   GO             82.0     (a) full       1
  Plan        GO             88.0     (a) full       1
  Development GO             91.0     (b) hybrid     1
  UAT         GO             86.0     (b) hybrid     1

  Escalations: 0
  Overrides:   0
  Total rule evaluations: 23
```

**Reading the columns:**
- **Gate Result**: `GO` means passed. `RECYCLE->GO` means it failed once, recycled, then passed on retry.
- **Score**: Weighted score out of 100. Must meet the stage's pass threshold.
- **Determinism**: `(a) full` = all inputs were structured data, fully deterministic. `(b) hybrid` = some inputs were AI-derived (e.g., validator pass/fail judgments), but the aggregation is deterministic.
- **Iterations**: How many attempts before the gate passed.

### JSONL Audit File

Each line in the audit file is a self-contained JSON object:

```json
{
  "timestamp": "2026-03-28T14:32:01Z",
  "pipeline_id": "pipe-20260328-143200",
  "stage": "design",
  "gate_id": "design_dod",
  "rule_id": "design-threshold",
  "input_context": {
    "stage.depth": "full",
    "stage.validators.ux.passed": true,
    "stage.validators.po.passed": true,
    "stage.validators.qa.passed": false
  },
  "passed": false,
  "score": 66.7,
  "decision": "RECYCLE",
  "reason": "QA validator failed: test coverage below 80% threshold",
  "determinism_category": "b",
  "resolution_layer": 2
}
```

**Key fields for auditors:**
- `input_context` -- The exact data the rule evaluated against. Replay this through the engine to verify the result.
- `determinism_category` -- `a` (fully deterministic), `b` (hybrid: deterministic aggregation of AI-derived inputs), `c` (AI-driven, not flow-control).
- `resolution_layer` -- Which layer provided the rule (1=defaults, 2=preset, 3=config, 4=runtime).

### Filtering the Audit Trail

The JSONL format supports standard command-line filtering:

```bash
# Find all gate failures
grep '"passed":false' .delivery/audit/audit-*.jsonl

# Find all fully deterministic decisions
grep '"determinism_category":"a"' .delivery/audit/audit-*.jsonl

# Find all decisions from Layer 3 (per-repo config overrides)
grep '"resolution_layer":3' .delivery/audit/audit-*.jsonl

# Find all escalations
grep '"decision":"ESCALATE"' .delivery/audit/audit-*.jsonl
```

---

## 7. Troubleshooting

### "Config v2.3 detected" message on every session

**Cause:** Your `.delivery/config.yml` has `config_version: "2.3"` (or no version field). The rules engine works fine with defaults, but reminds you to configure it.

**Fix:** Add the `rules` section and bump the version:
```yaml
config_version: "2.4"

rules:
  preset: standard
  escalation_sensitivity: balanced
```

Or run the setup wizard to do this automatically.

### "YAML type coercion detected" warning

**Cause:** YAML silently converts certain values. Common traps:
- `yes` / `no` become booleans (`true` / `false`)
- `on` / `off` become booleans
- `3.10` becomes `3.1` (trailing zero dropped)

**Fix:** Wrap ambiguous values in quotes:
```yaml
# Wrong -- YAML interprets "yes" as boolean true
strict_mode: yes

# Correct
strict_mode: true

# Wrong -- YAML drops the trailing zero
pass_threshold:
  design: 3.10

# Correct
pass_threshold:
  design: "3.10"   # if you mean the string
  design: 3.1      # if you mean the number
```

In strict mode, coercion warnings become hard errors and halt the pipeline.

### "STRICT MODE: YAML type coercion is a hard error"

**Cause:** You have `rules.strict_mode: true` and your config contains an ambiguous YAML value.

**Fix:** The error message names the exact key, shows the raw value, and shows what YAML coerced it to. Fix the value as described above. In strict mode, there is no workaround -- ambiguous values are not allowed.

### CONFIG VALIDATION ERROR

**Cause:** A `rules.*` value is invalid (wrong type, out of range, or unrecognized option).

**Example:**
```
CONFIG VALIDATION ERROR:

  Key: rules.preset
  Value: "aggressive"
  Expected: one of [solo, standard, strict]
```

**Fix:** The error message shows the key, the invalid value, and the expected value or range. All validation errors are reported at once so you can fix them in a single edit.

### Rules engine error (default mode)

**Cause:** A rule evaluation failed (e.g., a required field is null because a validator has not run yet).

**What you see:**
```
RULES ENGINE ERROR at gate "design_dod":

  Field 'stage.validators.architect.status' is null but rule
  'arch-review-required' requires a non-null value.

  How would you like to proceed?
    1. Retry   -- Re-run the gate evaluation
    2. Skip    -- Use AI evaluation for THIS gate only (logged as user override)
    3. Abort   -- Stop the pipeline entirely
```

**Fix:** Choose an option. Option 2 (Skip) falls back to AI evaluation for that one gate and logs the override in the audit trail. This does not disable the rules engine for other gates.

### Rules engine error (strict mode)

**Cause:** Same as above, but strict mode does not offer fallback options.

**What you see:**
```
RULES ENGINE ERROR -- Pipeline halted.

  Gate:    design_dod
  Error:   Field 'stage.validators.architect.status' is null but rule
           'arch-review-required' requires a non-null value.
  Action:  Ensure the architect validator has run before the Design DoD
           gate evaluates.
  State:   .delivery/state.md updated: status=HALTED
```

**Fix:** Resolve the underlying issue (in this example, run the architect validator first), then re-run the pipeline. It resumes from the halted stage.

### "Rules engine disabled via config"

**Cause:** `rules.enabled: false` is set in your config. The rules engine is bypassed entirely and the pipeline uses AI-interpreted decisions.

**Fix:** If this is intentional, no action needed. If not, set `rules.enabled: true` (or remove the key -- it defaults to `true`).

### Pipeline routing seems wrong

**Diagnosis steps:**
1. Run `--dry-run` to see what the rules engine decides and which layer each value comes from.
2. Run `--dry-run --compare` to see how your overrides differ from the defaults.
3. Check the audit trail for the specific gate or routing decision.

**Common causes:**
- A Layer 3 override is active that you forgot about. The `--compare` output highlights all overrides.
- The wrong preset is selected. Check `rules.preset` in your config.
- A Layer 4 per-run override was applied in a previous session. Layer 4 overrides are transient and not persisted, so this only applies within a single session.

### Key conflict with pre-existing config keys

**Cause:** Your v2.3 config contains unofficial keys that conflict with the new `rules.*` namespace (e.g., a manually added `gate_threshold` key).

**What you see:**
```
[CONFLICT] config key "gate_threshold.design" conflicts with v2.4
           "rules.pass_threshold.design".
           Remove "gate_threshold.design" and use
           "rules.pass_threshold.design: 90" instead.
           Pipeline halted. Fix config and re-run.
```

**Fix:** The error names both the old key and the new key with the exact replacement. Remove the old key and use the `rules.*` equivalent.

---

## 8. Reference: Config Keys

All keys are optional. Defaults are applied from the preset when a key is absent.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `rules.enabled` | boolean | `true` | Master switch. Set `false` to disable the entire rules engine. |
| `rules.preset` | string | `"standard"` | Preset profile: `solo`, `standard`, or `strict`. |
| `rules.strict_mode` | boolean | `false` | Enable strict mode (no AI fallback, no Layer 4, coercion = error). |
| `rules.escalation_sensitivity` | string | `"balanced"` | Escalation profile: `relaxed`, `balanced`, or `aggressive`. |
| `rules.pass_threshold.<stage>` | number (0-100) | Preset default | Per-stage gate pass threshold. Higher = stricter. |
| `rules.routing_overrides.<project_type>.<stage>` | string | Preset default | Per-project-type stage depth: `full` or `light`. |
| `rules.required_validators.<stage>` | list of strings | Preset default | Validators required for a stage's DoD gate. |
| `rules.custom` | list of objects | `[]` | Custom gate rules (field, operator, value, gate, description). |

### Supported Operators for Custom Rules

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equals | `"value": "FEATURE"` |
| `!=` | Not equals | `"value": "SPIKE"` |
| `>`, `>=`, `<`, `<=` | Numeric comparison | `"value": 5` |
| `IN` | Value in list | `"value": ["python", "typescript"]` |
| `NOT IN` | Value not in list | `"value": ["DOCS_ONLY"]` |
| `MATCHES` | Regex match | `"value": "^v\\d+\\.\\d+"` |
| `IS NULL` | Field is null/missing | (no value needed) |
| `IS NOT NULL` | Field exists | (no value needed) |
