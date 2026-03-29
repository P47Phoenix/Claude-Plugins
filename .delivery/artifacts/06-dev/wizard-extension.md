# Setup Wizard Extension: Rule Configuration Questions

**Author**: Gimli (Developer)
**Date**: 2026-03-28
**Traces To**: US-15 (stories.md), FR-17, UX Design Section 2
**Target File**: `delivery-team/skills/delivery-flow/references/setup-wizard.md`
**Position**: After existing Q14 (git/GitHub configuration)

> "Seventeen commits!" -- but first, three questions.

---

## Integration Notes

These three questions are appended after the existing wizard questions (currently Q1-Q14). They follow the same established protocol: auto-detect, present, options, record. The numbering below uses W-15/W-16/W-17 as working identifiers; final question numbers will be Q15/Q16/Q17 when merged into setup-wizard.md.

**Config version requirement**: These questions require config schema v2.4 (see US-12). The `rules` section they produce is new -- it does not conflict with any existing config keys.

---

### W-15: Rule Profile (single-select)

**Auto-detect**: Map from Q5 (Timeline & Risk Tolerance) answer:

| Q5 Answer | Recommended Preset | Confidence |
|-----------|-------------------|------------|
| Prototype | solo | 90% |
| Standard | standard | 95% |
| Mission-critical | strict | 85% |
| Regulated | strict | 95% |
| Custom/Skip | standard | 60% |

**Present**: "Based on your risk tolerance ({Q5 answer}), I recommend the "{preset}" profile."

**Options**:

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
- The `<-- recommended` marker moves based on the Q5 mapping. If Q5 was "Regulated", `strict` gets the marker.
- The recommendation is indicated with `<-- recommended`, not pre-selected. The user must actively choose.
- Each profile gets a one-line summary AND a "Best for" line so users match themselves to a persona, not abstract feature lists.

**Config key**: `rules.preset`

**Valid values**: `solo`, `standard`, `strict`

**Default if skipped**: `standard`

**Influences**: Stage routing depth, validator count per gate, gate pass thresholds, collaboration pattern selection, and whether AI fallback is permitted on gate decisions. The preset acts as a base layer -- all rule defaults cascade from this choice.

---

### W-16: Rule Customizations (conditional, multi-part)

**Conditional display**: This question appears ONLY if:
1. The user explicitly types "customize" or "custom" at W-15, OR
2. The auto-detection confidence from Q5 mapping is below 80% (i.e., Q5 was "Custom" or "Skip")

**If NOT shown**: The wizard writes the preset defaults and moves to W-17. The user never sees this question. This is the fast path -- user picks a profile and moves on.

**Present**: "Your base profile is "{preset}". You can override specific rules below."

**Options**:

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
    (Handled in W-17 below)
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

**Interaction pattern for "show defaults"**: Displays the current preset's values as a reference table before asking for overrides. Users override from knowledge, not from guessing.

**Key design decisions**:
- Sub-interactions use a simple `KEY = VALUE` format, not nested YAML. The wizard translates to YAML for config.yml.
- Each category is independent. The user can customize routing without touching validators.
- "Accept all" (blank through all categories) is equivalent to not showing this question at all -- same config output.

**Config keys**:
- `rules.routing_overrides` -- Stage depth overrides per project type (map of PROJECT_TYPE.STAGE to full/light)
- `rules.gate_overrides` -- Gate pass threshold overrides per stage (map of stage to percentage)
- `rules.dod_overrides` -- Validator set overrides per stage (map of stage to validator list)
- `rules.escalation` -- Deferred to W-17

**Default if skipped/not shown**: No override keys written. The preset defaults apply.

**Influences**: Overrides take precedence over the preset base layer (Layer 3 in the 4-layer resolution: defaults -> preset -> config overrides -> runtime overrides). Only explicitly set overrides are written; absent keys fall through to the preset.

---

### W-17: Escalation Sensitivity (single-select)

**Conditional display**: Always shown (not conditional). Escalation affects how aggressively the pipeline intervenes when things go wrong -- every user benefits from choosing this.

**Auto-detect**: Derive from Q5 (risk tolerance). Prototype maps to relaxed, standard to balanced, mission-critical/regulated to eager.

**Present**: "How quickly should the pipeline escalate when a stage struggles?"

**Options**:

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

**Threshold mapping**:

| Setting | `max_iterations` | `repeated_failure_tolerance` | `deadlock_timeout_minutes` |
|---------|------------------|------------------------------|----------------------------|
| relaxed | 5 | 3 | 10 |
| balanced | 3 | 2 | 5 |
| eager | 2 | 1 | 3 |

**Naming note**: The user-facing label is "eager" (positive connotation -- quick to act). The config value stored is `aggressive` for backward compatibility with the PRD spec. The display-to-config mapping is: relaxed->relaxed, balanced->balanced, eager->aggressive.

**Config keys**:
- `rules.escalation_sensitivity` -- The selected level: `relaxed`, `balanced`, or `aggressive`
- `rules.escalation.max_iterations` -- Derived from the threshold mapping above
- `rules.escalation.repeated_failure_tolerance` -- Derived from the threshold mapping above
- `rules.escalation.deadlock_timeout_minutes` -- Derived from the threshold mapping above

**Valid values for `escalation_sensitivity`**: `relaxed`, `balanced`, `aggressive`

**Default if skipped**: `balanced`

**Influences**: How many self-correction iterations a stage gets before the pipeline escalates (pauses for human input or switches collaboration pattern). Higher patience means more autonomous recovery attempts; lower patience means faster human intervention.

---

## Config Output

After all three questions, the wizard writes the following to `.delivery/config.yml` under the `rules` section:

### Minimal output (solo profile, no customization, balanced escalation):

```yaml
# --- Rules Engine Configuration ---
# Profile: controls routing depth, validator count, and gate strictness
# Change preset to reconfigure all rules at once; override individual keys below
rules:
  preset: solo                    # solo | standard | strict
  escalation_sensitivity: balanced  # relaxed | balanced | aggressive
```

Only two keys. No override keys written. This is the fast path for solo developers.

### Full output (standard profile, with customizations, eager escalation):

```yaml
# --- Rules Engine Configuration ---
# Profile: controls routing depth, validator count, and gate strictness
# Change preset to reconfigure all rules at once; override individual keys below
rules:
  preset: standard                # solo | standard | strict
  escalation_sensitivity: aggressive  # relaxed | balanced | aggressive
  routing_overrides:
    BUG_FIX:
      design: light
      architect: light
    SPIKE:
      architect: light
  gate_overrides:
    design: 75
    development: 90
  dod_overrides:
    idea: [po]
    refine: [po, qa]
  escalation:
    max_iterations: 2
    repeated_failure_tolerance: 1
    deadlock_timeout_minutes: 3
```

### Default output (no customization, commented examples):

```yaml
# --- Rules Engine Configuration ---
# Profile: controls routing depth, validator count, and gate strictness
# Change preset to reconfigure all rules at once; override individual keys below
rules:
  preset: standard                # solo | standard | strict
  escalation_sensitivity: balanced  # relaxed | balanced | aggressive
  # Uncomment to override specific rules:
  # routing_overrides:
  #   BUG_FIX:
  #     architect: light
  # gate_overrides:
  #   design: 80
  #   development: 85
  # dod_overrides:
  #   idea: [po]
  # escalation:
  #   max_iterations: 4
  #   repeated_failure_tolerance: 2
  #   deadlock_timeout_minutes: 7
```

Commented-out override examples teach by example -- users see what IS possible without being overwhelmed by what they must configure.

---

## Test Cases

| # | Test | Input | Expected |
|---|------|-------|----------|
| T1 | Q5=Prototype auto-maps to solo | Q5 answer="Prototype" | W-15 recommends solo (90% confidence) |
| T2 | Q5=Standard auto-maps to standard | Q5 answer="Standard" | W-15 recommends standard (95% confidence) |
| T3 | Q5=Mission-critical auto-maps to strict | Q5 answer="Mission-critical" | W-15 recommends strict (85% confidence) |
| T4 | Q5=Custom triggers W-16 | Q5 answer="Custom" | Confidence 60%, below 80% threshold, W-16 shown |
| T5 | W-16 skipped by default | User selects "standard" at W-15 (95% confidence) | W-16 not displayed, wizard proceeds to W-17 |
| T6 | W-16 shown on "customize" | User types "custom" at W-15 | W-16 displayed with all 3 categories |
| T7 | Minimal config for solo | Solo profile, balanced escalation, no customization | Config has exactly `rules.preset: solo` and `rules.escalation_sensitivity: balanced` |
| T8 | Custom rules written | User provides routing overrides in W-16 | `rules.routing_overrides` key present in config |
| T9 | Escalation thresholds for eager | User selects "eager" at W-17 | Config has `escalation_sensitivity: aggressive`, thresholds: max_iterations=2, repeated_failure_tolerance=1, deadlock_timeout_minutes=3 |
| T10 | Escalation thresholds for relaxed | User selects "relaxed" at W-17 | Thresholds: max_iterations=5, repeated_failure_tolerance=3, deadlock_timeout_minutes=10 |
| T11 | Skip at W-15 defaults to standard | User skips W-15 | `rules.preset: standard` |
| T12 | Skip at W-17 defaults to balanced | User skips W-17 | `rules.escalation_sensitivity: balanced` |

---

## Merge Instructions

To integrate into `setup-wizard.md`:

1. Insert the three questions after the current last question (Q14 / git-GitHub configuration)
2. Renumber as Q15, Q16, Q17 (or maintain whatever numbering scheme is current at merge time)
3. Update the wizard overview to say "17 questions" instead of "14 questions" (or current count)
4. Update the "Four Phases" description if needed -- no new phases are added; these questions fit in the existing "Present & Ask" phase
5. Add the `rules` section to the Config File Format example in setup-wizard.md
6. Update config-schema.md to v2.4 with the new `rules.*` keys (see US-12)
