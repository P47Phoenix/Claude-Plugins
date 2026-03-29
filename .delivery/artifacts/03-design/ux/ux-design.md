# UX Design: Deterministic Rules Engine Integration

**Designer**: Galadriel, UX Designer
**Date**: 2026-03-28
**Status**: Complete
**PRD Version**: 2.1

---

> *"Even the smallest person can change the course of the future -- but only if the path is clear before them."*
>
> This is a CLI/config-driven product. There is no visual UI. The "user experience" lives in the config surface users edit, the wizard questions they answer, the error messages they read when something breaks, the dry-run output they study before committing, and the audit trail they present to auditors. Every word, every format choice, every default is a design decision. I have looked into the Mirror and seen each persona's path. Here is what I found.

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Setup Wizard Flow](#2-setup-wizard-flow)
3. [Config Surface](#3-config-surface)
4. [Error and Migration Experience](#4-error-and-migration-experience)
5. [Dry-Run Experience](#5-dry-run-experience)
6. [Audit Trail Experience](#6-audit-trail-experience)
7. [Per-Run Override Experience](#7-per-run-override-experience)
8. [FR Traceability Matrix](#8-fr-traceability-matrix)

---

## 1. Design Principles

These principles govern every interaction designed in this document. When in doubt, return to these.

| Principle | Rationale |
|-----------|-----------|
| **Defaults are the product for most users** | Sarah (solo dev) will never edit a rule. The preset she picks in the wizard IS her entire rules experience. If defaults are wrong, the feature fails for the majority. |
| **Progressive disclosure, not progressive overwhelm** | Show the minimum first. Reveal complexity only when the user asks for it. The wizard conditionally hides Q-Rules-2 for this exact reason. |
| **Errors are conversations, not stack traces** | Every error message must answer three questions: What happened? Why? What do I do now? |
| **The audit trail serves two audiences** | The developer who just ran the pipeline (needs a summary). The auditor reviewing it months later (needs completeness and traceability). Design for both. |
| **Determinism must be visible, not just present** | It is not enough for the engine to be deterministic. Users must be able to SEE it is deterministic -- through dry-run, through audit logs, through the `--compare` flag. Trust is built by evidence, not by assertion. |

---

## 2. Setup Wizard Flow

> *"I give you the light of Earendil, our most beloved star. May it be a light in dark places, when all other lights go out."*
>
> The wizard is the first light a new user sees. It must illuminate the path without blinding them.

### Design: FR-17 (Setup Wizard Extension), US-15

The setup wizard currently asks 14 questions (Q1-Q10 core, plus Q11-Q14 for architecture and git/GitHub). Three new questions are added after the existing Q14 (git/GitHub configuration). They follow the same established protocol: auto-detect, present, options, record.

### Q-Rules-1: Rule Profile (W-15)

**Position**: After existing wizard questions (after Q14/git-GitHub). This is a natural transition -- the user has described WHAT their project is and HOW it is managed; now they describe HOW strictly the pipeline should govern it.

**Auto-detection logic**: Map from Q5 (Timeline & Risk Tolerance) answer:

| Q5 Answer | Recommended Preset | Confidence |
|-----------|-------------------|------------|
| Prototype | solo | 90% |
| Standard | standard | 95% |
| Mission-critical | strict | 85% |
| Regulated | strict | 95% |
| Custom/Skip | standard | 60% |

**Presentation format**:

```
--- Rules Engine Profile ---

Based on your risk tolerance ({Q5 answer}), I recommend the "{preset}" profile.

  Profile summary:
    solo     -- Minimal ceremony. 1 validator per gate. Fast paths for small work.
               Best for: solo devs, prototypes, tight iteration loops.
    standard -- Balanced defaults. Full validator set. 3 collaboration patterns.
               Best for: small-to-medium teams, most feature work.
    strict   -- Full ceremony. Security validator on every gate. Warnings block.
               Full audit trail. No AI fallback on any gate decision.
               Best for: regulated environments, enterprise, mission-critical.

  Options:
    1. solo
    2. standard  <-- recommended
    3. strict
    - Custom: describe your profile needs
    - Let's discuss: talk through the options
    - Skip: use "standard"
```

**Key design decisions**:
- The recommendation is indicated with `<-- recommended`, not pre-selected. The user must actively choose. This prevents accidental acceptance of a profile that does not fit.
- Each profile gets a one-line summary AND a "Best for" line. Users match themselves to a persona description, not to abstract feature lists.
- The `<-- recommended` marker moves based on the Q5 mapping. If Q5 was "Regulated", `strict` gets the marker.

### Q-Rules-2: Rule Customizations (W-16)

**Conditional display**: This question appears ONLY if:
1. The user explicitly types "customize" or "custom" at Q-Rules-1, OR
2. The auto-detection confidence from Q5 mapping is below 80% (i.e., Q5 was "Custom" or "Skip")

**If NOT shown**: The wizard writes the preset defaults and moves to Q-Rules-3. The user never sees this question. This is the path Sarah takes -- she picks "solo" and moves on.

**If shown -- presentation format**:

```
--- Rule Customizations ---

Your base profile is "{preset}". You can override specific rules below.
Leave blank to keep the preset default. Type "help {category}" for details.

  Routing overrides (which stages run at what depth for each project type):
    Current: using {preset} routing defaults
    Override? [blank to skip / "show defaults" to see the table / "customize"]

  Validator overrides (which validators are required per stage):
    Current: using {preset} validator set
    Override? [blank to skip / "show defaults" to see the list / "customize"]

  Gate threshold overrides (pass score required per stage):
    Current: all stages at {preset_default}%
    Override? [blank to skip / "show defaults" / "customize"]

  Escalation overrides:
    (Handled in Q-Rules-3 below)
```

**Interaction pattern for "customize"**: When the user types "customize" for any category, the wizard enters a sub-interaction:

```
  Routing customization:
    For each project type, specify stage depths (full/light).
    Format: PROJECT_TYPE.STAGE = full|light
    Example: BUG_FIX.architect = light

    Enter overrides (one per line, blank line when done):
    > BUG_FIX.design = light
    > SPIKE.architect = light
    >
    Recorded 2 routing overrides.
```

**Key design decisions**:
- Sub-interactions use a simple `KEY = VALUE` format, not nested YAML. The wizard translates to YAML for config.yml.
- "show defaults" displays the current preset's values as a reference table before asking for overrides. Users override from knowledge, not from guessing.
- Each category is independent. The user can customize routing without touching validators.

### Q-Rules-3: Escalation Sensitivity (W-17)

**Position**: Always shown (not conditional). Escalation affects how aggressively the pipeline intervenes when things go wrong -- every user benefits from choosing this.

**Presentation format**:

```
--- Escalation Sensitivity ---

How quickly should the pipeline escalate when a stage struggles?

  relaxed   -- Patient. Max 5 iterations before escalation. Tolerates 3 repeated
               failures. 10-minute deadlock timeout. Best for exploratory work.
  balanced  -- Middle ground. Max 3 iterations. 2 repeated failures. 5-minute
               deadlock timeout. Good default for most work.
  eager     -- Aggressive intervention. Max 2 iterations. 1 repeated failure.
               3-minute deadlock timeout. Best for time-sensitive work.

  Options:
    1. relaxed
    2. balanced  <-- recommended
    3. eager
    - Let's discuss: talk through the trade-offs
    - Skip: use "balanced"
```

**Note on naming**: The PRD uses "relaxed/balanced/aggressive" but "aggressive" has negative connotations for a configuration option. I recommend "eager" instead -- it conveys the same behavior (quick to act) without the adversarial framing. If the team prefers the PRD terminology, replace "eager" with "aggressive" throughout. The config key value remains the PRD's term (`relaxed`/`balanced`/`aggressive`) for backward compatibility with the PRD spec; the wizard display label is the user-facing choice.

**Config output**: After all three questions, the wizard writes to `.delivery/config.yml`:

```yaml
# --- Rules Engine Configuration ---
# Profile: controls routing depth, validator count, and gate strictness
# Change preset to reconfigure all rules at once; override individual keys below
rules:
  preset: solo                    # solo | standard | strict
  escalation_sensitivity: balanced  # relaxed | balanced | aggressive (eager)
  # Uncomment to override specific rules:
  # strict_mode: false
  # pass_threshold:
  #   design: 80
  #   development: 85
  # routing_overrides:
  #   BUG_FIX:
  #     architect: light
```

**Key design decisions**:
- Commented-out override examples are included in the generated config. This teaches by example -- users see what IS possible without being overwhelmed by what they must configure.
- The comment on `preset` explains what it controls in plain language.
- If Q-Rules-2 produced overrides, those are written as uncommented YAML keys under `rules`.

---

## 3. Config Surface

> *"The world is changed. I feel it in the water. I feel it in the earth."*
>
> The config file is where users live with their rules daily, long after the wizard has run. It must be scannable, self-documenting, and forgiving.

### Design: FR-04 (DoD Gate Rules), FR-05 (Context Serialization), FR-12 (Config Schema v2.4), US-04

### Minimal Config (Sarah's Path)

A solo developer who ran the wizard and picked "solo" sees this in their config:

```yaml
config_version: "2.4"
project_type: FEATURE
tech_stack:
  languages: [python]
# ... existing keys ...

# --- Rules Engine ---
rules:
  preset: solo
  escalation_sensitivity: balanced
```

That is it. Two lines under `rules`. Everything else is handled by Layer 1 (plugin defaults) + Layer 2 (solo preset). Sarah never needs to know that 126 individual rules exist underneath.

### Fully Customized Config (Marcus's Path)

A team lead who wants per-stage control:

```yaml
config_version: "2.4"
project_type: FEATURE
# ... existing keys ...

# --- Rules Engine ---
rules:
  preset: standard
  strict_mode: false
  escalation_sensitivity: balanced

  # Gate pass thresholds (0-100). Higher = stricter.
  # Overrides the preset default for listed stages only.
  pass_threshold:
    design: 90        # We care deeply about design quality
    development: 85   # Standard bar for code
    uat: 95           # High bar for user acceptance

  # Routing overrides by project type.
  # Only listed combinations are overridden; all others use preset defaults.
  routing_overrides:
    BUG_FIX:
      architect: light    # Bug fixes skip deep architecture review
      design: light       # Bug fixes get lightweight design pass
    SPIKE:
      uat: light          # Spikes get lightweight UAT

  # Required validators per stage.
  # Replaces the preset's validator list for listed stages only.
  required_validators:
    development: [developer, qa, architect, security]  # Added security
    uat: [qa, devops, po, security, tech-writer]       # Added security

  # Custom rules (advanced -- use only if presets + overrides are insufficient)
  # custom:
  #   - field: "artifacts.prd.sections.length"
  #     operator: ">="
  #     value: 5
  #     gate: "refine_dod"
  #     description: "PRD must have at least 5 sections"
```

### Config Comment Strategy

Every `rules.*` key group gets a one-line comment explaining what it controls and how overrides work. Comments use this pattern:

```
# {What it controls} ({value range}). {Override behavior}.
```

Examples:
- `# Gate pass thresholds (0-100). Higher = stricter.`
- `# Only listed combinations are overridden; all others use preset defaults.`

This answers the two questions a user has when scanning config: "What does this do?" and "What happens to the stuff I did not list?"

### Old Key Conflict Handling

When a v2.3 config contains keys that conflict with v2.4 `rules.*` semantics (e.g., if someone had manually added unofficial `gate_threshold` keys):

```
[CONFLICT] config key "gate_threshold.design" conflicts with v2.4 "rules.pass_threshold.design".
           Remove "gate_threshold.design" and use "rules.pass_threshold.design: 90" instead.
           Pipeline halted. Fix config and re-run.
           Exit code: 1
```

The error names BOTH the old key and the new key, and tells the user the exact replacement. No guessing required.

---

## 4. Error and Migration Experience

> *"The quest stands upon the edge of a knife. Stray but a little, and it will fail."*
>
> Errors in a rules engine are not inconveniences -- they are trust-destroying events. Every error must be handled with the gravity it deserves.

### Design: FR-14 (Error Handling), FR-10 (Translation Layer), FR-12 (Config Schema v2.4), US-11, US-13

### 4.1 Rules Engine Error (Strict Mode)

When `rules.strict_mode: true` and the engine encounters an error:

**stderr output** (JSON for machine parsing):
```json
{
  "gate_id": "design_dod",
  "error_type": "rule_evaluation_error",
  "message": "Field 'stage.validators.architect.status' is null but rule 'arch-review-required' requires a non-null value",
  "timestamp": "2026-03-28T14:32:01Z",
  "resolution": "Ensure the architect validator has run before the Design DoD gate evaluates. Check .delivery/state.md for pipeline state."
}
```

**What the user sees** (orchestrator formats the stderr JSON into human-readable output):

```
RULES ENGINE ERROR -- Pipeline halted.

  Gate:    design_dod
  Error:   Field 'stage.validators.architect.status' is null but rule
           'arch-review-required' requires a non-null value.
  Action:  Ensure the architect validator has run before the Design DoD
           gate evaluates.
  State:   .delivery/state.md updated: status=HALTED,
           halt_reason=rules_engine_error

  To resume: fix the issue and re-run the pipeline. It will resume from
  the halted stage.
```

**Key design decisions**:
- stderr gets structured JSON (for CI/CD integration -- Chen's need).
- The orchestrator reformats into human-readable text with clear sections: Gate, Error, Action, State.
- "Action" always tells the user what to DO, not just what went wrong.
- "To resume" is always present -- the user should never wonder "now what?"

### 4.2 Rules Engine Error (Default Mode)

When `rules.strict_mode: false` (default) and the engine encounters an error:

```
RULES ENGINE ERROR at gate "design_dod":

  Field 'stage.validators.architect.status' is null but rule
  'arch-review-required' requires a non-null value.

  How would you like to proceed?

    1. Retry   -- Re-run the gate evaluation (useful if the error was transient)
    2. Skip    -- Use AI evaluation for THIS gate only (logged as user override)
    3. Abort   -- Stop the pipeline entirely

  Choice [1/2/3]:
```

**Key design decisions**:
- Exactly three options, numbered. No ambiguity.
- Option 2 explicitly says "THIS gate only" -- the user knows they are not disabling the rules engine globally.
- Option 2 explicitly says "logged as user override" -- the user knows this will appear in the audit trail. Priya's auditor can see it.
- No default selection. The user must actively choose. Silent fallback is the thing we are eliminating.

### 4.3 Config Migration (v2.3 to v2.4)

When a v2.3 config is detected:

```
[MIGRATION] config v2.3 -> v2.4: rules section added with default values.

  What changed:
    + rules.preset: standard        (new -- using default)
    + rules.escalation_sensitivity: balanced  (new -- using default)
    + rules.strict_mode: false      (new -- using default)

  Your existing config keys are unchanged. The new "rules" section uses
  safe defaults that match previous pipeline behavior as closely as possible.

  To customize rules: edit .delivery/config.yml and modify the "rules" section.
  To silence this warning: update config_version to "2.4".
```

**Key design decisions**:
- The migration warning lists EVERY new key and its default value. No surprises.
- "match previous pipeline behavior as closely as possible" -- this is the honest framing. We cannot promise identical behavior because the old behavior was non-deterministic. We can promise the defaults are the closest deterministic equivalent.
- The warning appears on stderr so it does not pollute stdout (important for Chen's CI/CD piping).
- The warning persists until the user bumps `config_version` to "2.4". This is intentional -- the user should acknowledge the migration.

### 4.4 YAML Type Coercion Warnings (Default Mode)

When the translation layer detects YAML type coercion in default mode:

```
[WARN] YAML type coercion detected:
  Key: rules.strict_mode
  Raw value: yes
  Interpreted as: true (boolean)

  If you meant the string "yes", wrap it in quotes: "yes"
  If you meant the boolean true, this is fine -- but consider using true
  instead of yes for clarity.
```

**Key design decisions**:
- The warning names the SPECIFIC key, shows the raw value, and shows the coerced value.
- It offers BOTH possibilities: maybe the user meant a string, maybe they meant a boolean. It does not assume.
- It suggests the fix for both cases.
- In default mode, this is a warning -- the pipeline continues with the coerced value.

### 4.5 YAML Type Coercion Error (Strict Mode)

When `rules.strict_mode: true` and coercion is detected:

```
STRICT MODE: YAML type coercion is a hard error.

  Key: rules.pass_threshold.design
  Raw value: 3.10
  Coerced to: 3.1 (YAML drops trailing zero)

  In strict mode, ambiguous YAML values are not allowed.
  Fix: use quotes for literal strings ("3.10") or verify the numeric
  value is what you intended (3.1).

  Exit code: 2
```

**stderr JSON** (for CI/CD):
```json
{
  "error_type": "yaml_coercion",
  "key": "rules.pass_threshold.design",
  "raw": "3.10",
  "coerced": "3.1",
  "message": "YAML type coercion is a hard error in strict mode. Use quotes for literal strings."
}
```

### 4.6 Schema Validation Errors

When a rule value fails type validation (regardless of mode):

```
CONFIG VALIDATION ERROR:

  Key: rules.preset
  Value: "aggressive"
  Expected: one of [solo, standard, strict]

  Key: rules.pass_threshold.design
  Value: "high"
  Expected: numeric (0-100)

  2 validation errors found. Fix .delivery/config.yml and re-run.
  Exit code: 1
```

**Key design decisions**:
- All validation errors are reported at once, not one-at-a-time. The user fixes everything in one edit cycle.
- Each error shows: the key, the invalid value, and what WAS expected.
- "Expected" uses human terms ("one of [...]", "numeric (0-100)") not JSON Schema jargon.

---

## 5. Dry-Run Experience

> *"Will you look into the Mirror? For I have the power to show things unbeforeseen."*
>
> The dry-run is the Mirror of Galadriel for this feature. It shows the user what WILL happen before it happens. It builds trust through transparency.

### Design: FR-11 (Python Evaluation Script), US-16

### 5.1 Standard Dry-Run Output

Invocation:
```bash
python evaluate_rules.py \
  --context .delivery/tmp/context-routing.json \
  --rules-dir references/rules/ \
  --config .delivery/config.yml \
  --dry-run
```

Output (stdout, human-readable with embedded JSON):
```
=== DRY RUN: Rules Engine Evaluation ===
Config: .delivery/config.yml (v2.4)
Preset: solo (Layer 2)
Strict mode: off
Timestamp: 2026-03-28T14:30:00Z

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

--- Gate Thresholds ---
  Stage          Threshold    Source
  -------        ---------    ------
  1. Idea        70           Layer 2 (solo preset)
  2. Refine      70           Layer 2 (solo preset)
  3. Design      70           Layer 2 (solo preset)
  4. Architect   70           Layer 2 (solo preset)
  5. Plan        70           Layer 2 (solo preset)
  6. Development 80           Layer 2 (solo preset)
  7. UAT         70           Layer 2 (solo preset)

--- Escalation Thresholds ---
  Max iterations:          3 (balanced)
  Repeated failure limit:  2 (balanced)
  Deadlock timeout:        5 minutes (balanced)

--- Determinism Summary ---
  Fully deterministic (a):  5 decision points
  Hybrid (b):               2 decision points (DoD aggregation, YAML parsing)
  AI-driven (c):            0 decision points (flow control only)

--- JSON Output ---
{
  "routing": { ... },
  "thresholds": { ... },
  "escalation": { ... },
  "preset": "solo",
  "resolution_layers": { ... },
  "determinism": { ... }
}
```

**Key design decisions**:
- The output has TWO sections: a human-readable summary (tables) and a machine-readable JSON block. Developers read the tables; CI/CD pipes the JSON.
- Every row shows its "Source" column -- which layer provided this value. This is the core trust mechanism. Users can see EXACTLY where every decision comes from.
- "Active stages" gives a quick count so Sarah can estimate time.
- The determinism summary explicitly counts how many decisions are fully deterministic vs hybrid vs AI-driven. This is evidence, not assertion.

### 5.2 Compare Mode Output

Invocation:
```bash
python evaluate_rules.py \
  --context .delivery/tmp/context-routing.json \
  --rules-dir references/rules/ \
  --config .delivery/config.yml \
  --dry-run --compare
```

Additional output (appended after the standard dry-run):
```
=== COMPARISON: Rule-Based vs Default Routing ===

Project type: FEATURE | Risk tolerance: standard

  Stage          Rules Engine    Default (no overrides)    Delta
  -------        ------------    ----------------------    -----
  1. Idea        light           light                     --
  2. Refine      light           light                     --
  3. Design      light (L3)      full                      CHANGED (Layer 3 override)
  4. Architect   light           light                     --
  5. Plan        light           light                     --
  6. Development full            full                      --
  7. UAT         light (L3)      full                      CHANGED (Layer 3 override)

  Overrides active: 2
  Source: Layer 3 (per-repo config)

  Summary: Your config reduces Design and UAT from full to light depth
  for FEATURE projects. This will reduce pipeline duration but skip deep
  design review and comprehensive UAT for features.
```

**Key design decisions**:
- Side-by-side comparison with a "Delta" column. Changes are marked "CHANGED" with the source layer.
- A plain-English summary at the bottom explains the IMPACT of the overrides, not just the fact of them. "This will reduce pipeline duration but skip deep design review" -- the user understands the trade-off.
- Rows with no difference show `--` in the Delta column. The eye is drawn to the changes.
- "(L3)" annotation inline shows which layer is active for changed values.

---

## 6. Audit Trail Experience

> *"The time of the Elves is over. My people are leaving these shores. But this record shall endure."*
>
> The audit trail outlives the pipeline run. It must serve the developer who just ran the pipeline AND the auditor who reviews it months later. These are fundamentally different reading experiences.

### Design: FR-06 (Audit Trail Logging), US-05

### 6.1 JSONL Audit Format

Each line in `.delivery/audit/audit-<pipeline_id>.jsonl` is a self-contained JSON object:

```json
{"timestamp":"2026-03-28T14:32:01Z","pipeline_id":"pipe-20260328-143200","stage":"design","gate_id":"design_dod","rule_id":"design-threshold","input_context":{"stage.depth":"full","stage.validators.ux.passed":true,"stage.validators.po.passed":true,"stage.validators.qa.passed":false},"passed":false,"score":66.7,"decision":"RECYCLE","reason":"QA validator failed: test coverage below 80% threshold","determinism_category":"b","resolution_layer":2}
```

**Key design decisions**:
- One JSON object per line (JSONL standard). No pretty-printing in the log file -- this is a machine format.
- `input_context` is INCLUDED in every entry. This is critical for reproducibility (Priya's requirement). An auditor can take any entry and replay it through the engine to verify the result.
- `determinism_category` is a single character (a/b/c) for compact filtering: `grep '"determinism_category":"a"' audit-*.jsonl` finds all fully deterministic decisions.
- `resolution_layer` is a number (1/2/3/4) for the same reason.

### 6.2 Post-Run Summary

After a pipeline run completes, the orchestrator displays a summary derived from the audit trail:

```
=== Pipeline Run Summary ===
Pipeline ID:  pipe-20260328-143200
Duration:     12 minutes
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

--- Determinism Breakdown ---
  Category (a) fully deterministic:  14 evaluations (61%)
  Category (b) hybrid:                9 evaluations (39%)
  Category (c) AI-driven:             0 evaluations (0%)

  Audit log: .delivery/audit/audit-pipe-20260328-143200.jsonl
```

**Key design decisions**:
- The summary fits on one screen. Developers glance at it and move on.
- "RECYCLE->GO" notation shows that Design failed once and passed on retry. The arrow tells the story.
- Determinism breakdown gives a percentage. Over time, users can see if their pipeline is becoming more or less deterministic.
- The audit log path is printed at the bottom -- one click/copy away from the full details.
- The summary itself is NOT written to the audit log. The log is the raw data; the summary is a derived view.

### 6.3 Auditor Navigation

For Priya's SOC2 audit, the auditor needs to:

1. **Find all gate decisions for a pipeline run**: `cat audit-pipe-*.jsonl | python -m json.tool` (or `jq` if available)
2. **Filter by determinism category**: `grep '"determinism_category":"a"' audit-pipe-*.jsonl`
3. **Verify a specific gate**: Extract the `input_context` from an entry, save it to a file, and re-run `evaluate_rules.py --context <file> --dry-run` to verify the same result is produced.
4. **Find all user overrides**: `grep '"resolution_layer":4' audit-pipe-*.jsonl`
5. **Find all AI fallback decisions**: `grep '"decision_source":"user_override"' audit-pipe-*.jsonl`

**Key design decisions**:
- JSONL format was chosen specifically because it is grep-friendly. Each entry is one line. Standard Unix tools work.
- No custom query tool is needed. `grep`, `jq`, and `python -m json.tool` are sufficient. This avoids adding a dependency.
- The reproducibility proof (item 3 above) uses the SAME `evaluate_rules.py` script with `--dry-run`. No separate verification tool.

---

## 7. Per-Run Override Experience

> *"Instead of a dark lord, you would have a queen -- beautiful and terrible as the dawn!"*
>
> Layer 4 overrides are powerful and dangerous. They let a user change rules mid-flight. This power must come with clear consent and full visibility.

### Design: DD2 Layer 4, US-11, FR-16

### 7.1 Invoking an Override

The user speaks in natural language during a pipeline run:

```
User: "Set the development pass threshold to 70 for this run."
```

The orchestrator interprets this as a Layer 4 override and responds:

```
PER-RUN OVERRIDE REQUESTED

  Key:     rules.pass_threshold.development
  Current: 85 (Layer 3: per-repo config)
  New:     70 (Layer 4: per-run override)

  WARNING: This override RELAXES your configured threshold.
  Your config explicitly sets development pass_threshold to 85.
  This override will lower it to 70 for this run only.

  Proceed? [y/n]:
```

### 7.2 When Layer 4 Relaxes Layer 3

The confirmation prompt appears ONLY when Layer 4 would relax (lower thresholds, remove validators, reduce depth) a Layer 3 value. If Layer 4 tightens a value (raises a threshold), no confirmation is needed -- tightening is always safe.

**Relaxation examples** (confirmation required):
- Lowering a pass threshold
- Removing a required validator
- Changing a stage from full to light depth

**Tightening examples** (no confirmation needed):
- Raising a pass threshold
- Adding a required validator
- Changing a stage from light to full depth

### 7.3 Override Applied

After confirmation:

```
Override applied for this run only.

  rules.pass_threshold.development: 85 -> 70
  Logged in audit trail with resolution_layer: 4

  This override will NOT persist to future runs.
```

### 7.4 Override Rejected

If the user declines:

```
Override cancelled. Using configured value:
  rules.pass_threshold.development: 85 (Layer 3)
```

### 7.5 Strict Mode: Layer 4 Disabled

When `rules.strict_mode: true`:

```
User: "Set the development pass threshold to 70 for this run."

PER-RUN OVERRIDES DISABLED

  Strict mode is active. Per-run overrides (Layer 4) are disabled.
  Only Layers 1-3 (plugin defaults, preset, per-repo config) apply.

  To modify rules, edit .delivery/config.yml directly.
```

### 7.6 Scope Restriction

Layer 4 cannot swap presets:

```
User: "Switch to solo preset for this run."

OVERRIDE SCOPE EXCEEDED

  Layer 4 overrides can only adjust individual keys:
    - Pass thresholds per stage
    - Individual validators (add/remove)
    - Escalation sensitivity
    - Individual routing depths

  Preset-level changes require editing .delivery/config.yml.
```

**Key design decisions**:
- The confirmation prompt shows BOTH the current value and its source layer. The user knows exactly what they are overriding and where it came from.
- The "WARNING" prefix and bold "RELAXES" language make it clear this is a potentially dangerous action.
- The override confirmation is a simple y/n, not a multi-option menu. The action is binary: do it or do not.
- "This override will NOT persist" is stated explicitly every time. There is no ambiguity about transience.
- All overrides are logged in the audit trail. An auditor can see every Layer 4 override, its before/after values, and whether it was user-confirmed.

---

## 8. FR Traceability Matrix

> *"All we have to decide is what to do with the time that is given us."*
>
> And what we must do is ensure every requirement finds its home in the design. Here is the full accounting.

| FR | Requirement | Design Element | Section |
|----|-------------|----------------|---------|
| FR-01 | BRE condition evaluator extraction | **Internal -- no user-facing design.** Extraction is a code refactoring task. Users never interact with `condition_evaluator.py` directly. | N/A |
| FR-02 | Integration adapter layer | **Internal -- no user-facing design.** The `DeliveryRulesAdapter` is invoked by the evaluation script. Users interact with the script's input/output, not the adapter. | N/A |
| FR-03 | Stage routing rules | Dry-run routing map display (Section 5.1), Compare mode delta table (Section 5.2), Audit trail routing entries (Section 6.1) | 5, 6 |
| FR-04 | DoD gate rules | Config surface for `pass_threshold` and `required_validators` (Section 3), Error messages on gate failure (Section 4.1, 4.2), Post-run summary gate results (Section 6.2) | 3, 4, 6 |
| FR-05 | Context serialization | **Internal -- no user-facing design.** Context is assembled programmatically. Users see context indirectly via `input_context` in audit trail entries (Section 6.1) and via dry-run output (Section 5.1). | 5, 6 |
| FR-06 | Audit trail logging | JSONL format design (Section 6.1), Post-run summary (Section 6.2), Auditor navigation patterns (Section 6.3) | 6 |
| FR-07 | Preset profiles | Wizard Q-Rules-1 presentation (Section 2), Config surface minimal vs full (Section 3), Dry-run "Source" column showing preset layer (Section 5.1) | 2, 3, 5 |
| FR-08 | Escalation rules | Wizard Q-Rules-3 presentation (Section 2), Dry-run escalation thresholds display (Section 5.1), Post-run summary escalation count (Section 6.2) | 2, 5, 6 |
| FR-09 | Collaboration pattern rules | **Internal routing -- minimal user-facing design.** Collaboration patterns are selected by rules and visible in dry-run output (Section 5.1, included in JSON output block) and audit trail entries. No dedicated config surface beyond existing `pipeline.collaboration_patterns` key. | 5, 6 |
| FR-10 | YAML-to-JSON translation layer | YAML type coercion warnings (Section 4.4), YAML type coercion strict-mode errors (Section 4.5), Schema validation error messages (Section 4.6) | 4 |
| FR-11 | Python evaluation script (with dry-run) | Dry-run standard output (Section 5.1), Compare mode output (Section 5.2), Error output formats (Section 4.1, 4.2) | 4, 5 |
| FR-12 | Config schema extension (v2.4) | Config surface design (Section 3), Migration experience (Section 4.3), Config comment strategy (Section 3), Old key conflict handling (Section 3) | 3, 4 |
| FR-13 | SKILL.md orchestrator updates | **Internal -- no user-facing design.** SKILL.md changes are instructions to the orchestrator (Claude), not to the user. The user experiences the RESULT of these changes through deterministic routing, rule-based gates, and audit trail entries -- all designed in Sections 5, 6. | 5, 6 |
| FR-14 | Error handling and fallback | Strict mode error format (Section 4.1), Default mode 3-option prompt (Section 4.2), Error message structure (Section 4) | 4 |
| FR-15 | Depth selection rules | Dry-run routing map with depth per stage (Section 5.1), Compare mode showing depth changes (Section 5.2), Wizard routing override interaction (Section 2, Q-Rules-2) | 2, 5 |
| FR-16 | Rule override mechanism | Per-run override flow (Section 7), Config surface Layer 3 overrides (Section 3), Dry-run "Source" column showing override layers (Section 5.1), Compare mode delta (Section 5.2) | 3, 5, 7 |
| FR-17 | Setup wizard extension | Q-Rules-1 (Section 2), Q-Rules-2 conditional flow (Section 2), Q-Rules-3 (Section 2), Config output from wizard (Section 2) | 2 |
| FR-18 | Routing Decision Specification | **Internal -- no user-facing design.** The specification is an internal reference document that defines correct routing. Users experience its effects through the dry-run routing map (Section 5.1) and compare mode (Section 5.2), which show routing based on the specification. | 5 |

### Coverage Verification

- **FRs with user-facing design**: FR-03, FR-04, FR-06, FR-07, FR-08, FR-10, FR-11, FR-12, FR-14, FR-15, FR-16, FR-17 (12 of 18)
- **FRs that are internal/no user-facing design**: FR-01, FR-02, FR-05, FR-09, FR-13, FR-18 (6 of 18)
- **FRs with zero design mapping**: 0 of 18

All 18 FRs are accounted for. No gaps.

---

## Appendix: Persona Validation

| Persona | Primary Path | Key Design Touchpoints |
|---------|-------------|----------------------|
| **Sarah** (Solo Dev) | Wizard -> solo preset -> done | Q-Rules-1 (pick solo), Q-Rules-3 (pick balanced), skip Q-Rules-2. Minimal config (2 lines). Dry-run to preview timing. |
| **Marcus** (Team Lead) | Wizard -> standard preset -> customize validators | Q-Rules-1 (standard), Q-Rules-2 (customize validators and thresholds), Q-Rules-3. Full config with per-stage overrides. Post-run summary for leadership reporting. |
| **Priya** (Enterprise Architect) | Wizard -> strict preset -> full audit | Q-Rules-1 (strict), Q-Rules-3 (balanced or eager). Strict mode enables: hard errors on coercion, no Layer 4 overrides, full audit with determinism tagging. JSONL audit for SOC2 evidence. |
| **Jake** (Game Dev) | Wizard -> solo preset -> routing overrides for GAME_DEV | Q-Rules-1 (solo), Q-Rules-2 (customize routing: GAME_DEV.design=light, GAME_DEV.architect=light). Fast iteration paths. Dry-run to verify reduced ceremony. |
| **Chen** (DevOps) | Strict mode -> JSON stderr -> CI/CD integration | Strict mode for deterministic CI/CD. JSON error output on stderr for pipeline parsing. JSONL audit for automated compliance checks. Dry-run in CI for preview without execution. |

---

*"I pass the test. I will diminish, and go into the West, and remain Galadriel."*

*This design serves the user, not the designer. Every decision here can be questioned, revised, or overturned by the team. What matters is that the Mirror showed us the path clearly -- what we do with that vision is the team's choice.*
