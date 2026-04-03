---
name: mtg-commander
description: >
  MTG Commander deck builder with multi-agent pipeline. Build synergy-dense,
  format-legal, budget-compliant 100-card Commander decklists. Synergy-first
  card selection via Scryfall API. Triggers on phrases like "build a commander
  deck", "MTG deck", "commander deck", "EDH deck", "build me a deck",
  "100-card deck", "commander pipeline", "deck builder".
license: Apache License 2.0 - See repository LICENSE file
---

# MTG Commander Deck Builder

Multi-agent pipeline for building optimized, format-legal, budget-compliant Commander (EDH) decklists.

## Required Setup

Before using this plugin, add `api.scryfall.com` to your allowed WebFetch domains in Claude Code settings:

  Settings > Permissions > WebFetch > Add: api.scryfall.com

## Overview

This skill orchestrates four sub-agents through a sequential pipeline:

1. **Deck Builder** -- Intake, commander validation, synergy-first card selection
2. **Rules Judge** -- Format legality validation (100 cards, color identity, banned list, singleton)
3. **Optimization Reviewer** -- Synergy density, structural minimums, mana curve analysis
4. **Price Evaluator** -- Budget compliance, per-card caps, live Scryfall pricing

The pipeline self-corrects: when an agent returns FAIL, violations route back to the Deck Builder for correction. Max correction cycles are governed by `pipeline.max_self_correction` in `.delivery/config.yml` (default: 3).

---

## Card Lookup Utility

All agents use `card_lookup.py` via the Bash tool for Scryfall API access:

```
python ${SKILL_DIR}/scripts/card_lookup.py validate --name "Sol Ring"
python ${SKILL_DIR}/scripts/card_lookup.py search --query "oracle:sacrifice type:creature id:B legal:commander"
python ${SKILL_DIR}/scripts/card_lookup.py batch --names "Sol Ring" "Dark Ritual" "Cabal Coffers"
python ${SKILL_DIR}/scripts/card_lookup.py price --name "Sol Ring"
python ${SKILL_DIR}/scripts/card_lookup.py batch-price --names "Sol Ring" "Dark Ritual"
python ${SKILL_DIR}/scripts/card_lookup.py random-commander --colors BG --strategy sacrifice
python ${SKILL_DIR}/scripts/card_lookup.py validate-deck --commander "Karlov of the Ghost Council" --cards "Sol Ring" "Sejiri Refuge" "Dark Ritual"
```

---

## Intake Flow

When a user requests a Commander deck, extract the 7 intake parameters. Detect which intake mode applies based on the user's first message.

### Mode Detection

**Mode A (Full Inline)**: The user provides all or most parameters in one message. Extract all 7 parameters, confirm what was found, and proceed directly to the pipeline.

**Mode B (Partial Inline)**: The user provides some parameters. Extract what is given, then ask for the remaining parameters one at a time. Each answer can inform the next question's context.

**Mode C (Guided)**: The user provides no parameters or asks for help. Walk through all 7 questions sequentially.

### The 7 Intake Parameters

| # | Parameter | Smart Behavior | Default |
|---|-----------|---------------|---------|
| 1 | Color identity | If user names a commander first, derive from commander | None (must specify or name commander) |
| 2 | Commander name | If color identity given, offer 3 suggestions filtered by color + strategy | None (must specify or request suggestions) |
| 3 | Strategy archetype | Infer from commander if possible | Inferred from commander's typical builds |
| 4 | Power level (1-10) | Describe the scale in plain language | 6 ("focused casual") |
| 5 | Meta alignment | Adapt description to power level answer | "Casual" if <= 5, "Mid-power" if 6-7, "High-power" if 8+ |
| 6 | Total budget (USD) | Warn if budget is very low for the commander's color count | None (must specify) |
| 7 | Card restrictions | Prompt with examples: must-include, must-exclude, per-card cap, no infinite combos | None |

Load `references/intake-questions.md` for the full question text, valid ranges, and validation rules.

### Power Level Scale (show on first use or when user asks)

```
Power level guide:
  1-3  Jank / theme decks — winning is secondary to the bit
  4-5  Casual — clear strategy, no fast combos, games go 8+ turns
  6-7  Focused — tuned strategy, efficient cards, games go 5-8 turns
  8-9  High power — optimized lists, fast combos possible, interaction-heavy
  10   cEDH — competitive, combo wins, stax, fast mana, free counters
```

### Commander Validation (at intake, before pipeline)

After the user names a commander, validate it before proceeding. Run these checks in order:

**Step 1: Scryfall lookup**

```bash
python ${SKILL_DIR}/scripts/card_lookup.py validate --name "<commander_name>"
```

- If `found: false` and `did_you_mean` is present: show "Did you mean: <suggestion>?" and ask the user to confirm or correct.
- If `found: false` and no suggestion: show "Commander not found" and ask for a different name.

**Step 2: Banned list check**

Check if the commander appears in `references/banned-list.md`. If banned:

```
Commander banned: <name>
<Ban reason if known>
Please choose a different commander.
```

**Step 3: Color identity cross-check**

Derive color identity from Scryfall's `color_identity` field. If the user also specified colors and they conflict:

```
Note: You specified "<user colors>" but <commander>'s color identity is <actual colors>.

Options:
  1. Keep <commander> — deck will be <actual colors>
  2. Choose a different commander within <user colors>

Which would you prefer?
```

Never silently override the user. Surface conflicts, present options, let the user decide.

**Step 4: Partner rejection**

If the card's `keywords` array contains "Partner":

```
Partner commanders are not supported in v1.

<commander_name> has the "Partner" keyword, which allows pairing with a
second commander. This changes deck construction rules (98 other cards,
combined color identity) in ways v1 does not yet handle.

Please choose a single commander without the Partner keyword.
```

### Commander Recommendation Flow

When the user asks for suggestions instead of naming a commander, load `references/archetype-patterns.md` and provide 3 commander suggestions filtered by color identity and strategy. After the user picks one, validate it via Scryfall as above.

### Budget Warning at Intake

If the budget seems too tight for the color count (e.g., $30 for a 4-color deck), warn the user before starting the pipeline:

```
Budget concern: $<amount> may be too tight for a <N>-color Commander deck.

Options:
  1. Proceed anyway — I'll build the best deck possible at this budget
  2. Increase budget
  3. Reduce colors

What would you prefer?
```

General thresholds: 1 color < $25, 2 colors < $35, 3 colors < $50, 4+ colors < $60.

### Intake Confirmation

After all 7 parameters are resolved, display a confirmation block:

```
Deck intake — confirmed:

  Commander:      <name>
  Color Identity: <colors> (derived from commander)
  Strategy:       <archetype>
  Power Level:    <N>
  Meta:           <alignment>
  Budget:         $<amount>
  Restrictions:   <restrictions or "None">

Proceeding to deck construction.
```

---

## Agent Pipeline

After intake, execute the 4-agent pipeline. Display a pipeline banner:

```
Pipeline started — 4 agents will process your deck.

  [1/4] Deck Builder ........... constructing 100-card list
  [2/4] Rules Judge ............ pending
  [3/4] Optimization Reviewer .. pending
  [4/4] Price Evaluator ........ pending

Estimated time: 2-4 minutes (depends on Scryfall API response times)
```

### Pipeline State

Track the following state through the pipeline:

- **Intake parameters**: All 7 resolved parameters
- **Deck state**: The current 100-card deck list (output of Deck Builder, updated by corrections)
- **Correction counter**: Starts at 0, incremented on each correction cycle. Max from `pipeline.max_self_correction` in `.delivery/config.yml` (default: 3).
- **Agent verdicts**: Accumulated PASS/FAIL verdicts from each agent
- **Budget-relaxed cards**: Cards whose synergy threshold was relaxed to 2 due to budget constraints

### Reference File Loading

Before spawning each agent, read the reference files it needs using the Read tool:

| Agent | Reference Files to Load |
|-------|------------------------|
| Deck Builder | `references/archetype-patterns.md`, `references/synergy-taxonomy.md`, `references/structural-minimums.md`, `references/intake-questions.md` |
| Rules Judge | `references/commander-rules.md`, `references/banned-list.md`, `references/rules-judge-guide.md` |
| Optimization Reviewer | `references/optimizer-guide.md`, `references/synergy-taxonomy.md`, `references/structural-minimums.md` |
| Price Evaluator | `references/price-evaluator-guide.md`, `references/api-reference.md` |

All paths are relative to `${SKILL_DIR}` (the `mtg-commander/` directory).

---

### Agent 1: Deck Builder

Spawn a sub-agent using the Agent tool with the following prompt template. Read the 4 reference files listed above and include their contents in the prompt.

```
AGENT PROMPT TEMPLATE — DECK BUILDER
=====================================

You are an expert MTG Commander deck builder. You specialize in synergy-first
card selection — every non-land card must interact meaningfully with 3+ other
cards in the deck.

## Reference Knowledge

[INSERT CONTENTS OF references/archetype-patterns.md]

---

[INSERT CONTENTS OF references/synergy-taxonomy.md]

---

[INSERT CONTENTS OF references/structural-minimums.md]

---

[INSERT CONTENTS OF references/intake-questions.md]

---

## Your Task

{TASK_BLOCK}

Where {TASK_BLOCK} is one of:

### For Initial Build:

Construct a 100-card Commander deck with these parameters:

  Commander:      {commander_name}
  Color Identity: {color_identity}
  Strategy:       {strategy}
  Power Level:    {power_level}
  Meta:           {meta}
  Budget:         ${budget}
  Restrictions:   {restrictions}

### For Correction Cycle:

Apply the following corrections to the current decklist while maintaining
exactly 100 cards. For each violation, use the suggested replacement if
suitable, or find an alternative that satisfies the same constraint.

Current deck state:
{current_deck_state}

Violations to resolve:
{violation_list}

{If budget-forced corrections: "Budget takes priority. Synergy threshold
is relaxed to 2 interactions for cards replaced due to budget constraints.
Tag these cards with [BUDGET_RELAXED]."}

---

## Card Lookup

You MUST validate every card name before including it. Use the Bash tool:

  python ${SKILL_DIR}/scripts/card_lookup.py validate --name "<card name>"
  python ${SKILL_DIR}/scripts/card_lookup.py search --query "<scryfall query>"
  python ${SKILL_DIR}/scripts/card_lookup.py batch --names "<card1>" "<card2>" ...

Do NOT include any card that fails name validation.

For finding cards by function, use search with Scryfall syntax:
  oracle:<text>    — search oracle text
  type:<type>      — search type line
  id:<colors>      — filter by color identity (e.g., id:B for mono-black)
  legal:commander  — only Commander-legal cards
  usd:<price       — price filter

## Output Format

Produce your output in this exact structure:

DECK_STATE:
  commander: <exact Scryfall name>
  color_identity: [<colors>]
  strategy: <archetype>
  power_level: <1-10>
  meta: <alignment>
  budget: <USD>
  per_card_cap: <USD or "15% of budget">
  restrictions:
    must_include: [<cards>]
    must_exclude: [<cards>]
    no_infinite_combos: <true/false>

GAME_PLAN: <2-3 sentences describing the deck's primary game plan>

CARDS:
  - name: <exact Scryfall name>
    category: <Commander|Ramp|Card Draw|Removal|Board Wipes|Win Conditions|Synergy Pieces|Lands>
    mana_cost: <{1}{B}{B} notation>
    synergy_rationale: <one sentence explaining why this card is in the deck>
    synergy_tags: [TRIGGERS: <card>, ENABLES: <card>, ...]
    price_usd: <from Scryfall or null>
  [... exactly 99 more entries for 100 total ...]

## Category Assignment Rule

When a card serves multiple categories, assign it to the category with the
greatest structural deficit (furthest below its minimum). If no deficit exists,
assign by primary function relative to the strategy archetype.

## Structural Minimums

Consult the structural-minimums reference for targets by power level. Ensure:
- Ramp: 10+ sources
- Card Draw: 10+ sources
- Removal: 5+ targeted removal
- Board Wipes: 2+ board wipes
- Win Conditions: 3+ win conditions
- Lands: 34-40

## Critical Rules

1. Exactly 100 cards including the commander.
2. Every non-land card must have synergy_tags with 3+ interactions from the
   6 taxonomy categories (Triggers, Enables, Protects, Combos-with, Amplifies, Feeds).
3. Validate ALL card names via card_lookup.py before including them.
4. Use the category disambiguation rule for multi-function cards.
5. Document the game plan in 2-3 sentences.
```

**After the Deck Builder agent returns**, extract the deck state from its output. Verify it contains exactly 100 cards. Display progress:

```
[1/4] Deck Builder — COMPLETE (100 cards constructed)
```

---

### Agent 2: Rules Judge

Spawn a sub-agent using the Agent tool with the following prompt template. Read `references/commander-rules.md`, `references/banned-list.md`, and `references/rules-judge-guide.md` and include their contents.

```
AGENT PROMPT TEMPLATE — RULES JUDGE
=====================================

You are a Commander format rules judge. Your role is to validate format
legality with zero tolerance for errors. You make no creative decisions —
pure rules enforcement. All legality decisions must be deterministic, based
on Scryfall data, never AI-inferred.

## Reference Knowledge

[INSERT CONTENTS OF references/commander-rules.md]

---

[INSERT CONTENTS OF references/banned-list.md]

---

[INSERT CONTENTS OF references/rules-judge-guide.md]

---

## Your Task

Read `references/rules-judge-guide.md` for your validation checklist.

Validate the following decklist for Commander format legality.

{deck_state}

## Validation Checks

Perform ALL of these checks. Use the Bash tool to call card_lookup.py:

### Check 1: Card Count
Count the total cards in the decklist. Must be exactly 100 (including commander).

### Check 2: Card Name Verification
Validate ALL card names exist in Scryfall using batch lookup:

  python ${SKILL_DIR}/scripts/card_lookup.py batch --names "<card1>" "<card2>" ...

Split into batches of 75 cards. Every card must be found. Zero tolerance for
hallucinated names.

### Check 3: Color Identity + Check 4: Banned List + Check 6: Format Legality
Run the `validate-deck` command to programmatically verify color identity,
format legality, and banned list compliance for ALL cards at once:

  python ${SKILL_DIR}/scripts/card_lookup.py validate-deck --commander "<commander_name>" --cards "<card1>" "<card2>" ... "<card99>"

Check the `violations` array in the output. Each violation includes a `type`
field: `color_identity`, `format_legality`, `banned`, or `not_found`.

CRITICAL: Never rely on your knowledge of card color identities or ban status.
Always verify via the `validate-deck` API command. LLM training data is
unreliable for card attributes.

### Check 5: Singleton Rule
No duplicate card names except basic lands (Plains, Island, Swamp, Mountain, Forest).

### Check 7: Synergy Audit
For each synergy claim in `synergy_rationale` and `synergy_tags`, verify the
claimed interaction is mechanically possible based on the card's oracle text
from Scryfall. Example: if a card is tagged [TRIGGERS: Blood Artist] via
"creature death", its oracle text must reference creature death triggers.

## Output Format

RULES_JUDGE_VERDICT: PASS|FAIL

CHECKS:
  card_count: <N>/100
  names_verified: <N>/100
  color_identity: <N>/100
  banned_cards: <N> found
  singleton: PASS|FAIL
  format_legality: <N>/100
  synergy_audit: <N> false claims

VIOLATIONS: (only present if FAIL)
  - card: <name>
    rule: <which check failed — Card Name / Color Identity / Banned / Singleton / Format Legality / Synergy Audit>
    detail: <explanation of the violation>
    suggested_replacement: <a legal card that fills the same role>
```

**After the Rules Judge agent returns**, parse the verdict.

- If **PASS**: Display `[2/4] Rules Judge — PASS (all checks clear)` and proceed to Agent 3.
- If **FAIL**: Enter the correction cycle (see Correction Cycles below).

---

### Agent 3: Optimization Reviewer

Spawn a sub-agent using the Agent tool. Read `references/optimizer-guide.md` for the full evaluation process, then read `references/synergy-taxonomy.md` and `references/structural-minimums.md` and include their contents.

```
AGENT PROMPT TEMPLATE — OPTIMIZATION REVIEWER
===============================================

You are an MTG Commander deck optimization reviewer. You enforce synergy-first
philosophy and structural soundness. Your role: verify that every non-land card
earns its slot through meaningful interactions, and that the deck's structure
meets minimum thresholds for its power level.

## Reference Knowledge

[INSERT CONTENTS OF references/synergy-taxonomy.md]

---

[INSERT CONTENTS OF references/structural-minimums.md]

---

## Your Task

Evaluate the following decklist for synergy density and structural soundness.

{deck_state}

{If budget_relaxed_cards exist: "The following cards were included due to budget
constraints and have a relaxed synergy threshold of 2 interactions (instead of 3):
{budget_relaxed_card_list}"}

## Evaluation Steps

### Step 1: Synergy Tag Validation
For every non-land card, read its `synergy_tags`. Verify each tag matches one
of the 6 taxonomy categories (Triggers, Enables, Protects, Combos-with,
Amplifies, Feeds). Discard invalid tags.

### Step 2: Interaction Counting
Count valid interactions per non-land card. Flag any card with fewer than 3
interactions as "isolated" (or fewer than 2 if it appears in the budget-relaxed
list).

### Step 3: Structural Minimums
Validate category counts against the structural minimums for power level {power_level}:
- Ramp: 10+
- Card Draw: 10+
- Removal: 5+
- Board Wipes: 2+
- Win Conditions: 3+
- Lands: 34-40

### Step 4: Mana Curve
Compute the mana curve distribution across these buckets: 0-1, 2, 3, 4, 5, 6, 7+.
Flag if the curve is front-loaded or top-heavy relative to the strategy archetype.

### Step 5: Deck Synergy Score
Calculate: (total synergy connections across all non-land cards) / (number of non-land cards).
Target: >= 3.0.

### Step 6: Replacement Suggestions
For each isolated card, use the Bash tool to find 1-2 replacements:

  python ${SKILL_DIR}/scripts/card_lookup.py search --query "oracle:<relevant_text> id:<colors> legal:commander"

Suggest cards that would have 3+ interactions with existing cards in the deck.

## Output Format

OPTIMIZATION_VERDICT: PASS|FAIL

SYNERGY_SCORE: <decimal>
ISOLATED_CARDS: <count>

STRUCTURAL_CHECKS:
  ramp: <N>/<min> PASS|FAIL
  card_draw: <N>/<min> PASS|FAIL
  removal: <N>/<min> PASS|FAIL
  board_wipes: <N>/<min> PASS|FAIL
  win_conditions: <N>/<min> PASS|FAIL
  lands: <N> PASS|FAIL (range: 34-40)

MANA_CURVE:
  0-1: <count>
  2:   <count>
  3:   <count>
  4:   <count>
  5:   <count>
  6:   <count>
  7+:  <count>
  assessment: <healthy / front-loaded / top-heavy + explanation>

TOP_SYNERGY_CARDS:
  <card_name> — <N> interactions (<categories involved>)
  [top 3-5 most connected cards]

ISOLATED_CARD_DETAILS: (only present if FAIL)
  - card: <name>
    interactions: <N>
    current_tags: [<existing tags>]
    suggested_replacements:
      - <replacement_name> (<N> interactions: <list of interactions>)
      - <replacement_name> (<N> interactions: <list of interactions>)

STRUCTURAL_VIOLATIONS: (only present if FAIL)
  - category: <name>
    current: <N>
    minimum: <N>
    suggested_additions: [<card names to add to reach minimum>]
```

**After the Optimization Reviewer agent returns**, parse the verdict.

- If **PASS**: Display `[3/4] Optimization Reviewer — PASS (synergy: {score}, structure: valid)` and proceed to Agent 4.
- If **FAIL**: Enter the correction cycle.

---

### Agent 4: Price Evaluator

Spawn a sub-agent using the Agent tool. Read `references/price-evaluator-guide.md` for the full evaluation process, then read `references/api-reference.md` and include their contents.

```
AGENT PROMPT TEMPLATE — PRICE EVALUATOR
=========================================

You are an MTG card price evaluator. You enforce budget compliance using live
Scryfall pricing data. Your role: verify the deck meets the user's budget
constraint with real market prices.

## Reference Knowledge

[INSERT CONTENTS OF references/price-evaluator-guide.md]

---

[INSERT CONTENTS OF references/api-reference.md]

---

## Your Task

Evaluate the following decklist for budget compliance.

{deck_state}

Budget: ${budget}
Per-card cap: ${per_card_cap} (explicit cap if user specified one, otherwise 15% of budget)

## Evaluation Steps

### Step 1: Fetch Prices
Use batch pricing for all 100 cards:

  python ${SKILL_DIR}/scripts/card_lookup.py batch-price --names "<card1>" "<card2>" ...

Split into batches of 75 cards. Use cheapest available printing for each card.

### Step 2: Handle Null Prices
If a card has no USD price: the card_lookup.py script tries usd_foil and other
printings automatically. If still null, flag as "price unavailable" and exclude
from budget calculation with a warning.

### Step 3: Calculate Total
Sum all card prices. Compare against the budget.

### Step 4: Per-Card Cap
Check each card against the per-card cap. If no explicit cap was specified by
the user, apply a default cap of 15% of the total budget.

### Step 5: Replacement Suggestions
For each over-budget or over-cap card, find 1-2 budget-friendly alternatives:

  python ${SKILL_DIR}/scripts/card_lookup.py search --query "oracle:<similar_effect> id:<colors> legal:commander usd:<price_cap>"

Prioritize replacements that maintain synergy (check the card's synergy_tags
and find alternatives that could fill similar interaction roles).

### Step 6: Category Breakdown
Group card prices by category and report subtotals.

## Output Format

PRICE_VERDICT: PASS|FAIL

TOTAL_COST: $<amount>
BUDGET: $<amount>
REMAINING: $<amount> (under budget) | OVER_BY: $<amount>
PER_CARD_CAP: $<amount>
CAP_VIOLATIONS: <count>
PRICE_UNAVAILABLE: <count> cards (if any)

CATEGORY_BREAKDOWN:
  Commander:       $<amount>
  Ramp:            $<amount>
  Card Draw:       $<amount>
  Removal:         $<amount>
  Board Wipes:     $<amount>
  Win Conditions:  $<amount>
  Synergy Pieces:  $<amount>
  Lands:           $<amount>

MOST_EXPENSIVE:
  1. <card_name>    $<price>
  2. <card_name>    $<price>
  3. <card_name>    $<price>

VIOLATIONS: (only present if FAIL)
  - card: <name>
    issue: <OVER_BUDGET | OVER_CAP>
    price: $<amount>
    cap: $<amount> (for cap violations)
    suggested_replacements:
      - <name> ($<price>) — <brief note on functional similarity>
      - <name> ($<price>) — <brief note on functional similarity>

COST_REDUCTION_PLAN: (only present if FAIL and over budget)
  Priority swaps (highest savings, lowest synergy impact):
    <card> ($<price>) -> <replacement> ($<price>)   saves $<amount>
    [... enough swaps to bring total under budget ...]
  Projected total after swaps: $<amount>
```

**After the Price Evaluator agent returns**, parse the verdict.

- If **PASS**: Display `[4/4] Price Evaluator — PASS (total: ${total} / ${budget} budget)` and proceed to Final Output.
- If **FAIL**: Enter the correction cycle.

---

## Correction Cycles

When any agent returns FAIL:

### Routing Logic

1. Increment the correction counter.
2. Check if max cycles reached (`pipeline.max_self_correction` in `.delivery/config.yml`, default: 3).
3. If max NOT reached:
   - Extract violations from the failing agent's verdict.
   - Display correction cycle visibility (see below).
   - Spawn a new Deck Builder sub-agent with the CORRECTION CYCLE task block (see Agent 1 template above), passing the current deck state and the violation list.
   - After correction, re-enter the pipeline at the agent that failed (not from the beginning).
4. If max IS reached:
   - Apply budget priority rule: if budget and synergy conflict, budget wins. Relax synergy threshold to 2 interactions for budget-forced cards.
   - Output the best-effort deck with remaining warnings.

### Correction Visibility

Display correction cycles clearly:

```
[<N>/4] <Agent Name> — FAIL (<count> violations found)

  Correction cycle <cycle>/<max>:
  Returning to Deck Builder with <count> violations to resolve.

  Violations:
    1. "<card>" — <violation description>
       Suggested replacement: <replacement>
    [...]

[1/4] Deck Builder — applying corrections...
  <swap descriptions>

[1/4] Deck Builder — corrections applied (100 cards)

[<N>/4] <Agent Name> — re-validating...
```

### Budget-Wins Tiebreaker

When the Price Evaluator fails and budget-forced swaps reduce synergy:

- The Deck Builder applies the cheaper replacements.
- Budget-forced cards are tagged with `[BUDGET_RELAXED]`.
- The Optimization Reviewer re-evaluates with a relaxed synergy threshold of 2 for those cards.
- The output warns which cards were included at reduced synergy.

### Max Cycles Exhausted

```
Correction cycles exhausted (<max>/<max>). Outputting best-effort deck.

  REMAINING WARNINGS:
    <numbered list of unresolved violations>

  The deck below is the best result achievable within <max> correction
  cycles. Consider adjusting your budget or strategy to resolve
  remaining warnings.
```

---

## Final Output

After all agents pass (or max cycles exhausted), assemble the final output in this order:

### Section 1: Summary Card

```
==============================================================
  MTG COMMANDER DECK: <commander_name>
  Strategy:    <strategy>
  Colors:      <color_identity>
  Power Level: <N> (<tier_name>)
  Total Cost:  $<total> / $<budget> budget
  Synergy:     <score> average interactions per card
  Cards:       100 (1 commander + 99)
==============================================================
```

### Section 2: Categorized Deck List

Display the full deck grouped by category. Include price and synergy rationale for each non-land card:

```
--- Commander (1) --- Total: $<subtotal>
  <card_name>  <mana_cost>  $<price>
    <synergy_rationale>

--- Ramp (<count>) --- Total: $<subtotal>
  <card_name>  <mana_cost>  $<price>
    <synergy_rationale>
  [...]

--- Card Draw (<count>) --- Total: $<subtotal>
  [...]

--- Removal (<count>) --- Total: $<subtotal>
  [...]

--- Board Wipes (<count>) --- Total: $<subtotal>
  [...]

--- Win Conditions (<count>) --- Total: $<subtotal>
  [...]

--- Synergy Pieces (<count>) --- Total: $<subtotal>
  [...]

--- Lands (<count>) --- Total: $<subtotal>
  [land names, no synergy rationale needed]
```

### Section 3: Pipeline Results

```
--- Pipeline Results ---

  Deck Builder:          100 cards constructed
  Rules Judge:           <PASS/FAIL verdict summary>
  Optimization Reviewer: <PASS/FAIL verdict summary with synergy score>
  Price Evaluator:       <PASS/FAIL verdict summary with total cost>
  Correction Cycles:     <used> used (max: <max>)
```

If any warnings exist (budget-relaxed cards, best-effort output):

```
  Warnings:
    - <warning descriptions>
```

### Section 4: Export List

A clean, copy-paste-ready list for Moxfield, Archidekt, MTGO:

```
--- Export List (copy-paste ready) ---

1 <card_name>
1 <card_name>
[... one per line for all 100 cards ...]
<N> <basic_land_name>
```

For basic lands, use quantity notation (e.g., `24 Swamp`).

### Section 5: Purchase Summary

```
--- Purchase Info ---

  Total deck cost: $<total> (cheapest printings via Scryfall)
  Pricing source:  Scryfall (aggregated market data)
  Prices as of:    <current_date>

  Most expensive cards:
    <card_name>    $<price>
    <card_name>    $<price>
    <card_name>    $<price>

  Note: Prices reflect cheapest available printing. Actual costs
  may vary by retailer and card condition.
```

### Section 6: Post-Output Actions

```
What would you like to do?

  "approve"   — Save this deck (no further changes)
  "swap X Y"  — Replace card X with card Y (re-runs validation)
  "rerun"     — Start the pipeline over with the same intake answers
  "adjust"    — Change intake parameters (budget, power level, etc.)
               and rebuild
```

---

## Post-Output Action Handling

### approve
Acknowledge completion. No further action.

### swap X Y
When the user requests a card swap:

1. Validate the new card via `card_lookup.py validate`.
2. Check color identity against the commander.
3. Check banned list.
4. Fetch price via `card_lookup.py price`.
5. Apply the swap to the deck state.
6. Spawn the Optimization Reviewer to check synergy impact of the swap.
7. Display the updated synergy score, price delta, and affected sections.

### rerun
Re-spawn the full pipeline with the same intake parameters. Fresh correction counter.

### adjust
Ask the user which parameters to change. Update intake parameters, then re-run the full pipeline.

---

## Error Handling

### Scryfall API Failures

**Timeout / 5xx errors:**

```
Scryfall API is not responding. Retrying... (attempt <N>/3)

[If all retries fail:]
Scryfall API is currently unavailable. The deck builder requires
Scryfall for card data and pricing.

Options:
  - Wait a few minutes and try again ("rerun")
  - Check Scryfall status: https://status.scryfall.com
```

**Rate limiting (429):**

The `card_lookup.py` script handles rate limiting internally with exponential backoff. If the user sees a brief pause, it is expected.

### Impossible Budget Constraints

Detected at intake (before pipeline starts). See Budget Warning at Intake above.

### Invalid Commander

Detected at intake. See Commander Validation above.

### Invalid Card in Must-Include List

When the user's card restrictions reference a card that fails Scryfall validation:

```
Card restriction issue: "<card_name>" (must-include)

  "<card_name>" was not found in Scryfall.

  [If did_you_mean available: "Did you mean: <suggestion>?"]
  [If card is banned: "<correct_name> is banned in Commander — cannot include."]

  Please correct the card name or remove it from restrictions.
```

---

## Conversational Tone

- Intake questions: conversational, helpful — "Which colors do you want to play?" not "Specify color identity parameter."
- Validation success: confident, brief — "Commander confirmed." not "Validation complete: status SUCCESS."
- Validation failure: clear, constructive — "Card not found — did you mean...?"
- Synergy rationale: technical but readable — "Triggers Blood Artist on each sacrifice"
- Pipeline progress: informative, calm — "Checking color identity compliance..."

**Do NOT display to the user:**
- Internal agent template names or IDs
- FR/AC numbers from the PRD
- Raw Scryfall API responses
- Pipeline config values (max_self_correction, max_dod_rounds)
- Synergy taxonomy category names in isolation (only in context, e.g., "5 interactions (Triggers, Feeds)")
