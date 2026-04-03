# Intake Questions

Reference document for the Deck Builder agent and the SKILL.md orchestrator. Defines the 7 intake questions, valid inputs, defaults, validation rules, and intake mode detection.

---

## Intake Modes

The orchestrator detects the intake mode from the user's first message:

| Mode | Detection | Behavior |
|------|-----------|----------|
| **Mode A** (All Inline) | User provides all 7 parameters in a single message | Extract all parameters, validate, proceed to pipeline |
| **Mode B** (Partial + Sequential) | User provides some parameters in the first message | Extract provided parameters, ask remaining questions sequentially |
| **Mode C** (Fully Interactive) | User provides only a general request (e.g., "build me a commander deck") | Ask all 7 questions sequentially |

**Mode detection logic**: Count how many of the 7 parameters are identifiable in the user's first message. If 7 = Mode A. If 1-6 = Mode B. If 0 = Mode C.

---

## The 7 Questions

### Q1: Commander Selection

| Field | Value |
|-------|-------|
| Question | "Who is your commander?" |
| Input type | Card name (string) |
| Default | None (required) |
| Validation | Must be a Legendary Creature (or have "can be your commander" in rules text) per Scryfall data. Must not be on the banned list. Must not have the "Partner" keyword (v1 limitation). |
| On invalid | If card not found: show error, suggest fuzzy match if available, prompt for correction. If banned: show ban message, prompt for alternative. If partner: explain v1 limitation, prompt for single commander. |

**Note**: Commander selection is the first question because it determines color identity, which constrains all subsequent card choices. If the user provides color identity without a commander, ask for commander first -- color identity is derived from the commander, not specified independently.

### Q2: Color Identity (Derived)

| Field | Value |
|-------|-------|
| Question | "Your commander's color identity is [derived colors]. Does this match your expectation?" |
| Input type | Confirmation or correction |
| Default | Derived from commander's Scryfall `color_identity` field |
| Validation | Must match the commander's actual color identity from Scryfall data. If user says different colors, warn that commander constrains identity and confirm. |
| On mismatch | If user expected different colors, explain color identity rules and suggest they either: (a) accept the commander's actual identity, or (b) choose a different commander that matches their desired colors. |

**Processing**: Color identity is ALWAYS derived from the validated commander card data. User-specified colors serve only as a cross-check, never as the authoritative source.

### Q3: Strategy / Win Condition

| Field | Value |
|-------|-------|
| Question | "What strategy or win condition do you want? (e.g., graveyard recursion, voltron, tokens, combo, mill, lifegain, stax, spellslinger, tribal, +1/+1 counters, superfriends, group hug, aggro)" |
| Input type | Strategy archetype name (string) |
| Default | None (required, but can suggest based on commander) |
| Validation | Must map to a known archetype in `archetype-patterns.md`. Fuzzy matching allowed (e.g., "graveyard" maps to "Graveyard Recursion", "burn" maps to "Aggro / Combat Damage" or "Spellslinger"). |
| On unrecognized | Show available archetypes, ask user to select or describe further. |

**Smart behavior**: If the user names a commander known for a specific strategy, suggest that strategy as the default. Example: "K'rrik, Son of Yawgmoth is commonly built as Graveyard Recursion or Life Drain. Which would you prefer?"

### Q4: Power Level

| Field | Value |
|-------|-------|
| Question | "What power level are you targeting? (1-10 scale)" |
| Input type | Integer 1-10 |
| Default | 6 (mid-power, most common) |
| Validation | Must be an integer between 1 and 10 inclusive. |
| Tier mapping | 1-4 = Casual, 5-7 = Mid, 8-9 = High, 10 = cEDH |

**Power level guide** (shown to user on request):
| Level | Description |
|-------|------------|
| 1-2 | Jank / theme-first, minimal interaction |
| 3-4 | Precon-level, casual table |
| 5-6 | Upgraded precon, focused strategy |
| 7 | Optimized casual, strong but not oppressive |
| 8 | Tuned, fast mana, efficient threats |
| 9 | Near-cEDH, optimized win conditions and interaction |
| 10 | cEDH, maximum power and speed |

### Q5: Meta Alignment

| Field | Value |
|-------|-------|
| Question | "What's your playgroup's meta? (casual, mid-power, high-power, competitive/cEDH, mixed/unknown)" |
| Input type | String from options |
| Default | "mid-power" |
| Validation | Must map to one of: casual, mid-power, high-power, competitive, mixed. |
| Effect | Influences removal density, interaction speed, and whether hard stax/MLD is appropriate. |

**Cross-check**: If power level 8+ but meta "casual," warn the user about potential mismatch. If power level 3-4 but meta "competitive," warn similarly.

### Q6: Budget

| Field | Value |
|-------|-------|
| Question | "What's your total budget in USD? (or 'no budget')" |
| Input type | Positive number (USD) or "no budget" / "unlimited" |
| Default | "no budget" (no price constraint) |
| Validation | If specified, must be a positive number. Minimum $25 (below that, 100-card construction is not feasible). |
| Per-card cap | Optional: "No card over $X." If not specified, defaults to 15% of total budget. If budget is "no budget," no per-card cap applies. |

**Budget ranges** (for context):
| Range | Assessment |
|-------|-----------|
| $25-50 | Ultra-budget. Expect significant synergy compromises. Budget-forced relaxation (2 interactions) likely. |
| $50-100 | Budget. Achievable with careful selection. Some premium staples excluded. |
| $100-200 | Mid-range. Most strategies viable. Premium staples accessible. |
| $200-500 | Comfortable. All non-reserve-list staples accessible. |
| $500+ / no budget | No constraint. Full optimization possible. |

### Q7: Restrictions

| Field | Value |
|-------|-------|
| Question | "Any card restrictions? (must-include cards, must-exclude cards, no infinite combos, etc.)" |
| Input type | Free text (parsed for structured restrictions) |
| Default | "No restrictions" |
| Validation | Must-include cards validated against Scryfall (must exist, must be within color identity, must not be banned). |
| Parsed fields | `must_include: [card names]`, `must_exclude: [card names]`, `no_infinite_combos: true/false` |

**Examples of valid restrictions**:
- "Include Sol Ring and Phyrexian Arena"
- "No cards over $5 each"
- "No infinite combos"
- "Exclude Rhystic Study and Smothering Tithe"
- "Only creatures and lands" (unusual but valid)

---

## Validation Summary

| Question | Required | Has Default | Validated Against |
|----------|----------|-------------|-------------------|
| Q1: Commander | Yes | No | Scryfall (exists, legendary, not banned, not partner) |
| Q2: Color Identity | Derived | Yes (from commander) | Scryfall color_identity field |
| Q3: Strategy | Yes | Suggested | archetype-patterns.md |
| Q4: Power Level | No | Yes (6) | Integer 1-10 |
| Q5: Meta | No | Yes (mid-power) | Option list |
| Q6: Budget | No | Yes (no budget) | Positive number or "no budget" |
| Q7: Restrictions | No | Yes (none) | Scryfall for must-include cards |

---

## Intake Completion

Once all 7 questions are answered and validated, the orchestrator summarizes the intake parameters and confirms with the user before starting the pipeline:

```
INTAKE SUMMARY:
  Commander: K'rrik, Son of Yawgmoth
  Color Identity: B (Black)
  Strategy: Graveyard Recursion
  Power Level: 7 (Mid)
  Meta: Mid-power casual
  Budget: $150 (per-card cap: $22.50)
  Restrictions: None

Shall I proceed with deck construction?
```

On confirmation, the orchestrator spawns the Deck Builder sub-agent with the intake parameters and reference file contents.
