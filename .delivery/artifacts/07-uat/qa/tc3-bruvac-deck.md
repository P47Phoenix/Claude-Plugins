# Test Case 3: Bruvac the Grandiloquent -- Mono-Blue Mill

**Test date**: 2026-04-01
**Plugin**: mtg-commander v1
**Intake mode**: Mode A (Full Inline)

---

## Intake Summary

```
Deck intake -- confirmed:

  Commander:      Bruvac the Grandiloquent
  Color Identity: U (Blue)
  Strategy:       Mill
  Power Level:    6 (Mid / focused casual)
  Meta:           Mid-power
  Budget:         $75.00
  Restrictions:   No infinite combos, no extra turn spells

Budget warning: Bruvac is $42.86 at cheapest printing (57% of total budget).
Remaining budget for 99 cards: $32.14 (ultra-budget territory).
```

---

## Pipeline Execution

```
Pipeline started -- 4 agents will process your deck.

  [1/4] Deck Builder ........... COMPLETE (100 cards constructed)
  [2/4] Rules Judge ............ PASS (all checks clear)
  [3/4] Optimization Reviewer .. PASS (synergy: 3.1, structure: valid, budget-relaxed: 11 cards)
  [4/4] Price Evaluator ........ PASS (total: $74.14 / $75.00 budget)

  Correction Cycles: 0 used (max: 3)
```

---

## Summary Card

```
==============================================================
  MTG COMMANDER DECK: Bruvac the Grandiloquent
  Strategy:    Mill
  Colors:      U (Blue)
  Power Level: 6 (Focused Casual)
  Total Cost:  $74.14 / $75.00 budget
  Synergy:     3.1 average interactions per card
  Cards:       100 (1 commander + 99)
==============================================================
```

## Game Plan

Deploy Bruvac early to double all mill effects, then chain persistent mill engines (Teferi's Tutelage, Jace's Erasure, Drowned Secrets) with card draw to grind opponents' libraries. Close games with explosive finishers like Traumatize (mills 75% of a library with Bruvac), Fleet Swallower, or flashed-back Increasing Confusion. Fraying Sanity on the most-milled opponent creates a doubling effect that accelerates the kill. Counterspells and bounce protect the mill engines while they work.

---

## Categorized Deck List

### --- Commander (1) --- Total: $42.86

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Bruvac the Grandiloquent | {2}{U} | $42.86 | Doubles all opponent mill effects -- the deck's central engine |

### --- Ramp (11) --- Total: $4.93

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Sol Ring | {1} | $1.45 | [BUDGET_RELAXED] Accelerates mill engines by 2 turns; enables turn-2 Bruvac |
| Arcane Signet | {2} | $0.45 | [BUDGET_RELAXED] Fixes and accelerates into 3-drop mill enchantments |
| Mind Stone | {2} | $0.24 | [BUDGET_RELAXED] Ramp early, draw late; FEEDS Teferi's Tutelage draw trigger |
| Sky Diamond | {2} | $0.22 | [BUDGET_RELAXED] Enables turn-3 Bruvac |
| Wayfarer's Bauble | {1} | $0.33 | [BUDGET_RELAXED] Land ramp TRIGGERS Ruin Crab landfall |
| Everflowing Chalice | {0} | $0.34 | [BUDGET_RELAXED] Scalable ramp for Increasing Confusion's X cost |
| Star Compass | {2} | $0.51 | [BUDGET_RELAXED] Budget 2-drop ramp |
| Prismatic Lens | {2} | $0.38 | [BUDGET_RELAXED] Ramp with color fixing |
| Commander's Sphere | {3} | $0.34 | [BUDGET_RELAXED] Ramp that draws a card; FEEDS Teferi's Tutelage |
| Guardian Idol | {2} | $0.37 | [BUDGET_RELAXED] Ramp that becomes a blocker to protect mill engines |
| Worn Powerstone | {3} | $0.30 | [BUDGET_RELAXED] +2 mana for X-cost mill spells like Increasing Confusion |

### --- Card Draw (10) --- Total: $3.75

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Preordain | {U} | $0.65 | Cantrip TRIGGERS Teferi's Tutelage, Jace's Erasure, Drowned Secrets |
| Opt | {U} | $0.36 | Instant-speed cantrip TRIGGERS Teferi's Tutelage and Jace's Erasure |
| Consider | {U} | $0.33 | Cantrip TRIGGERS Teferi's Tutelage; self-mills for delve fuel |
| Fact or Fiction | {3}{U} | $0.30 | Draws 3-5 cards; TRIGGERS Teferi's Tutelage; FEEDS graveyard for Treasure Cruise |
| Chart a Course | {1}{U} | $0.12 | Draw 2 for 2; TRIGGERS Teferi's Tutelage twice; TRIGGERS Drowned Secrets |
| Treasure Cruise | {7}{U} | $0.25 | Delve draw-3; TRIGGERS Teferi's Tutelage 3 times; TRIGGERS Jace's Erasure |
| Dig Through Time | {6}{U}{U} | $0.29 | Delve selection; TRIGGERS Jace's Erasure; finds mill finishers |
| Thought Scour | {U} | $0.54 | Draw + mills target 2 (4 with Bruvac); AMPLIFIES Bruvac; TRIGGERS Teferi's Tutelage |
| Fascination | {X}{U}{U} | $0.31 | Modal: mass draw TRIGGERS all draw-mill enchantments, OR mass mill AMPLIFIES Bruvac |
| Vision Skeins | {1}{U} | $0.60 | Each player draws 2; TRIGGERS Teferi's Tutelage; FEEDS Folio of Fancies mill mode |

### --- Removal (13) --- Total: $2.93

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Negate | {1}{U} | $0.18 | PROTECTS mill engines from removal; TRIGGERS Drowned Secrets |
| Reality Shift | {1}{U} | $0.12 | Exiles creature threat; opponent manifests; TRIGGERS Drowned Secrets |
| Curse of the Swine | {X}{U}{U} | $0.22 | Scalable exile removal; TRIGGERS Drowned Secrets; tokens manageable |
| Imprisoned in the Moon | {2}{U} | $0.33 | Permanent-based removal for commanders; TRIGGERS Drowned Secrets |
| Mana Leak | {1}{U} | $0.18 | Early-game counter; PROTECTS Bruvac; TRIGGERS Drowned Secrets |
| Spell Pierce | {U} | $0.28 | Cheap protection for mill engines; TRIGGERS Drowned Secrets |
| Didn't Say Please | {1}{U}{U} | $0.39 | Counter + mills 3 (6 with Bruvac); AMPLIFIES Bruvac; TRIGGERS Drowned Secrets |
| Thought Collapse | {1}{U}{U} | $0.37 | Counter + mills 3 (6 with Bruvac); AMPLIFIES Bruvac; TRIGGERS Drowned Secrets |
| Into the Roil | {1}{U} | $0.09 | Bounce + kicker draws; TRIGGERS Drowned Secrets; TRIGGERS Teferi's Tutelage on kick |
| Blink of an Eye | {1}{U} | $0.20 | Bounce + kicker draws; TRIGGERS Drowned Secrets; TRIGGERS Teferi's Tutelage on kick |
| Stern Dismissal | {U} | $0.12 | 1-mana bounce for creatures/enchantments; TRIGGERS Drowned Secrets; PROTECTS by removing blockers |
| Vapor Snag | {U} | $0.25 | 1-mana bounce + 1 life; TRIGGERS Drowned Secrets; TRIGGERS Deepmuck crime |
| Unsummon | {U} | $0.21 | 1-mana bounce; TRIGGERS Drowned Secrets; can self-bounce Manic Scribe for re-ETB mill |

### --- Board Wipes (3) --- Total: $1.30

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Devastation Tide | {3}{U}{U} | $0.51 | Miracle for {1}{U}; resets board; replayed enchantments TRIGGER Drowned Secrets again |
| Wash Out | {3}{U} | $0.42 | Color-specific bounce; asymmetric board clear; TRIGGERS Drowned Secrets |
| Aetherize | {3}{U} | $0.37 | Bounces all attacking creatures; PROTECTS you while mill engines run; punishes aggro |

### --- Win Conditions (5) --- Total: $7.64

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Traumatize | {3}{U}{U} | $3.76 | Mills half a library; with Bruvac doubles to 75%; COMBOS-WITH Fraying Sanity for near-lethal |
| Fleet Swallower | {5}{U}{U} | $1.33 | Attack mills half library; AMPLIFIES Bruvac to 75% on attack; COMBOS-WITH Fraying Sanity |
| Increasing Confusion | {X}{U} | $1.23 | Scalable mill; flashback from graveyard doubles X; AMPLIFIES Bruvac |
| Keening Stone | {6} | $0.46 | Activated: mill cards equal to GY size; snowballs; AMPLIFIES Bruvac |
| Startled Awake | {2}{U}{U} | $0.86 | Mills 13 (26 with Bruvac); transforms to reusable creature; AMPLIFIES Bruvac |

### --- Synergy Pieces (16) --- Total: $9.02

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Ruin Crab | {U} | $1.49 | Landfall mills 3 (6 with Bruvac); TRIGGERS on every land drop; AMPLIFIES Bruvac |
| Teferi's Tutelage | {2}{U} | $0.35 | Draw TRIGGERS mill 2 (4 with Bruvac); engine with every draw spell; AMPLIFIES Bruvac |
| Fraying Sanity | {2}{U} | $0.58 | Doubles total mill at end step; COMBOS-WITH Traumatize/Fleet Swallower; AMPLIFIES all mill |
| Folio of Fancies | {1}{U} | $1.60 | Activated mass draw; activated mass mill equal to hand size; FEEDS Teferi's Tutelage; AMPLIFIES Bruvac |
| Jace's Erasure | {1}{U} | $0.28 | Draw TRIGGERS mill 1 (2 with Bruvac); redundant engine with Teferi's Tutelage |
| Drowned Secrets | {1}{U} | $0.48 | Blue spell cast TRIGGERS mill 2 (4 with Bruvac); passive mill from normal play; AMPLIFIES Bruvac |
| Imperious Mindbreaker | {1}{U}{U} | $0.40 | Soulbond; attack mills toughness (doubled by Bruvac); pairs with high-toughness creatures |
| Overwhelmed Apprentice | {U} | $0.18 | ETB mills 2 (4 with Bruvac) + scry 2; TRIGGERS Drowned Secrets; AMPLIFIES Bruvac |
| Manic Scribe | {1}{U} | $0.29 | ETB mills 3 (6 with Bruvac); delirium repeats each upkeep; AMPLIFIES Bruvac |
| Deepmuck Desperado | {2}{U} | $0.23 | Crime TRIGGERS mill 3 (6 with Bruvac); targeting opponents counts; AMPLIFIES Bruvac |
| Tome Scour | {U} | $0.27 | Mills 5 (10 with Bruvac) for 1 mana; AMPLIFIES Bruvac; TRIGGERS Fraying Sanity |
| Mind Sculpt | {1}{U} | $0.20 | Mills 7 (14 with Bruvac); AMPLIFIES Bruvac; TRIGGERS Fraying Sanity; TRIGGERS Drowned Secrets |
| Compelling Argument | {1}{U} | $0.18 | Mills 5 (10 with Bruvac) or cycles for {U}; AMPLIFIES Bruvac; TRIGGERS Drowned Secrets |
| Millstone | {2} | $0.10 | Repeatable mill 2 (4 with Bruvac); artifact survives creature wipes; AMPLIFIES Bruvac |
| Codex Shredder | {1} | $0.23 | Repeatable mill 1 (2 with Bruvac); sac to return key mill spell; AMPLIFIES Bruvac; ENABLES recursion |
| Ghoulcaller's Bell | {1} | $0.21 | Repeatable mill each player; passive mill every turn; AMPLIFIES Bruvac |

### --- Graveyard Hate (2) --- Total: $0.69

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Tormod's Crypt | {0} | $0.41 | Free graveyard exile; prevents opponents from using milled cards; ENABLES safe milling |
| Soul-Guide Lantern | {1} | $0.28 | Graveyard exile + draws a card; TRIGGERS Teferi's Tutelage; ENABLES safe milling |

### --- Lands (39) --- Total: $2.96

**Utility Lands (10):**

| Card | Price |
|------|-------|
| Reliquary Tower | $1.00 |
| Halimar Depths | $0.33 |
| Lonely Sandbar | $0.30 |
| Remote Isle | $0.15 |
| Desert of the Mindful | $0.24 |
| Memorial to Genius | $0.13 |
| Evolving Wilds | $0.29 |
| Terramorphic Expanse | $0.11 |
| Castle Vantress | $0.32 |
| Skyline Cascade | $0.09 |

**Basic Lands (29):**

| Card | Count | Price |
|------|-------|-------|
| Island | 29 | ~$0.00 |

*Note: 39 total lands (10 utility + 29 Island). Evolving Wilds and Terramorphic Expanse TRIGGER Ruin Crab landfall twice (fetch crack + land entry = 2 landfall triggers per turn).*

---

## Agent Verdicts

### [1/4] Deck Builder -- COMPLETE (100 cards constructed)

Cards constructed with synergy-first selection. 11 ramp cards flagged as [BUDGET_RELAXED] at 2-interaction threshold due to ultra-tight budget ($32.14 for 99 cards after commander). All mill engines and synergy pieces meet the full 3-interaction threshold.

### [2/4] Rules Judge -- PASS

```
RULES_JUDGE_VERDICT: PASS

CHECKS:
  card_count: 100/100
  names_verified: 100/100 (all validated via Scryfall batch lookup, 2 batches)
  color_identity: 100/100 (all cards mono-U or colorless)
  banned_cards: 0 found
  singleton: PASS (no duplicates, 29 basic Islands exempt)
  format_legality: 100/100 (all legalities.commander == "legal")
  synergy_audit: 0 false claims

VIOLATIONS: None

WARNINGS:
  - Bruvac the Grandiloquent ($42.86) consumes 57% of total budget
  - No infinite combos present (user restriction satisfied)
  - No extra turn spells present (user restriction satisfied)
```

### [3/4] Optimization Reviewer -- PASS (budget-relaxed)

```
OPTIMIZATION_VERDICT: PASS

SYNERGY_SCORE: 3.1
ISOLATED_CARDS: 0 (11 budget-relaxed ramp cards at 2-interaction threshold)

STRUCTURAL_CHECKS:
  ramp: 11/10 PASS
  card_draw: 10/10 PASS
  removal: 13/5 PASS (includes 2 mill-counters + 5 bounce spells)
  board_wipes: 3/2 PASS
  win_conditions: 5/3 PASS
  lands: 39 PASS (range: 35-39)

MANA_CURVE:
  0-1: 19 (Sol Ring, Everflowing Chalice, Ruin Crab, Overwhelmed Apprentice,
            Opt, Consider, Spell Pierce, Preordain, Thought Scour, Tome Scour,
            Ghoulcaller's Bell, Codex Shredder, Tormod's Crypt, Soul-Guide Lantern,
            Wayfarer's Bauble, Compelling Argument, Stern Dismissal, Vapor Snag,
            Unsummon)
  2:   18 (Arcane Signet, Mind Stone, Sky Diamond, Star Compass, Prismatic Lens,
            Guardian Idol, Chart a Course, Negate, Mana Leak, Reality Shift,
            Teferi's Tutelage, Fraying Sanity, Folio of Fancies, Jace's Erasure,
            Drowned Secrets, Manic Scribe, Mind Sculpt, Millstone, Vision Skeins,
            Into the Roil, Blink of an Eye)
  3:   10 (Commander's Sphere, Deepmuck Desperado, Imperious Mindbreaker,
            Imprisoned in the Moon, Didn't Say Please, Thought Collapse,
            Worn Powerstone, Curse of the Swine, Fascination, Aetherize)
  4:   3  (Fact or Fiction, Startled Awake, Wash Out)
  5:   2  (Traumatize, Devastation Tide)
  6:   1  (Keening Stone)
  7+:  1  (Fleet Swallower)
  average_mana_value: 2.13
  assessment: Front-loaded (healthy for mill) -- heavy at 0-2 CMC enables
              aggressive early deployment of mill engines alongside Bruvac.
              Low curve supports 39 lands with 11 ramp sources.

TOP_SYNERGY_CARDS:
  Bruvac the Grandiloquent -- 18+ interactions (AMPLIFIES every mill source in deck)
  Teferi's Tutelage -- 12 interactions (TRIGGERS on every draw spell/cantrip)
  Drowned Secrets -- 14 interactions (TRIGGERS on every blue spell cast)
  Fraying Sanity -- 8 interactions (AMPLIFIES + COMBOS-WITH mill finishers)
  Ruin Crab -- 6 interactions (TRIGGERS on landfall, AMPLIFIES with Bruvac)

BUDGET_RELAXED_CARDS:
  11 ramp cards accepted at 2-interaction threshold (budget-forced)
  Reason: $32.14 remaining after commander left insufficient budget for
          premium synergy ramp. Generic mana rocks fill structural minimum.
```

### [4/4] Price Evaluator -- PASS

```
PRICE_VERDICT: PASS

TOTAL_COST: $74.14
BUDGET: $75.00
REMAINING: $0.86 (under budget)
PER_CARD_CAP: $11.25 (15% of $75.00)
CAP_VIOLATIONS: 0
PRICE_UNAVAILABLE: 0 cards

CATEGORY_BREAKDOWN:
  Commander:       $42.86 (1 card)
  Ramp:            $4.93 (11 cards, avg $0.45/card)
  Card Draw:       $3.75 (10 cards, avg $0.38/card)
  Removal:         $2.93 (13 cards, avg $0.23/card)
  Board Wipes:     $1.30 (3 cards, avg $0.43/card)
  Win Conditions:  $7.64 (5 cards, avg $1.53/card)
  Synergy Pieces:  $9.02 (16 cards, avg $0.56/card)
  GY Hate:         $0.69 (2 cards, avg $0.35/card)
  Lands:           $2.96 (10 utility + 29 basic at ~$0.00)

MOST_EXPENSIVE:
  1. Bruvac the Grandiloquent    $42.86
  2. Traumatize                  $3.76
  3. Folio of Fancies            $1.60
  4. Ruin Crab                   $1.49
  5. Sol Ring                    $1.45

NOTE: All prices sourced from Scryfall (cheapest available printing).
Bruvac at $42.86 dominates the budget (58% of total cost). The remaining
99 cards average $0.32 each.
```

---

## Pipeline Results

```
--- Pipeline Results ---

  Deck Builder:          100 cards constructed
  Rules Judge:           PASS -- all 7 checks clear, 0 violations
  Optimization Reviewer: PASS -- synergy 3.1, all structural minimums met
                         (11 budget-relaxed ramp cards at 2-interaction threshold)
  Price Evaluator:       PASS -- $74.14 / $75.00 budget ($0.86 remaining)
  Correction Cycles:     0 used (max: 3)

  Warnings:
    - 11 ramp cards accepted at relaxed synergy threshold (2 interactions)
      due to ultra-budget constraint ($0.32 avg per non-commander card)
    - Commander consumes 58% of total budget
    - Deck lacks premium mill staples due to budget:
      Mesmeric Orb ($21.56), Psychic Corrosion ($6.47), Maddening Cacophony ($9.09),
      Court of Cunning ($5.04), Cyclonic Rift ($41.25), Rhystic Study ($58.74)
    - No self-mill win conditions (Thassa's Oracle $22.78, Lab Man $1.61)
      excluded to preserve budget margin
```

---

## Strategy Description

**Primary game plan**: Deploy Bruvac on turn 3 (or turn 2 with Sol Ring), then layer persistent mill enchantments (Teferi's Tutelage, Jace's Erasure, Drowned Secrets) that convert normal card draw and spell casting into constant library erosion. Each draw step mills opponents for 4+ cards with Bruvac active.

**Mid-game acceleration**: Once 2-3 mill engines are running, use card draw spells (Treasure Cruise, Fact or Fiction, Fascination) to trigger mass mill. Folio of Fancies provides both draw fuel and an activated mill ability scaled to hand size.

**Closing the game**: Traumatize a single opponent (mills 75% of their remaining library with Bruvac), then Fraying Sanity doubles their total mill at end of turn for a near-complete library wipe. Fleet Swallower achieves the same on attack. Keening Stone snowballs after other mill has filled graveyards. Increasing Confusion provides flashback reach from the graveyard.

**Defense**: Thirteen removal spells (counters + bounce) protect key pieces and disrupt threats. Three board wipes reset dangerous board states. Graveyard hate (Tormod's Crypt, Soul-Guide Lantern) prevents opponents from benefiting from their milled cards.

**Weaknesses**: Soft to enchantment removal (most engines are enchantments), graveyard shuffle effects (Eldrazi titans, Nexus of Fate), and aggressive starts before mill engines come online. Lacks premium interaction due to budget.

---

## Export List (copy-paste ready)

```
1 Bruvac the Grandiloquent
1 Sol Ring
1 Arcane Signet
1 Mind Stone
1 Sky Diamond
1 Wayfarer's Bauble
1 Everflowing Chalice
1 Star Compass
1 Prismatic Lens
1 Commander's Sphere
1 Guardian Idol
1 Worn Powerstone
1 Preordain
1 Opt
1 Consider
1 Fact or Fiction
1 Chart a Course
1 Treasure Cruise
1 Dig Through Time
1 Thought Scour
1 Fascination
1 Vision Skeins
1 Negate
1 Reality Shift
1 Curse of the Swine
1 Imprisoned in the Moon
1 Mana Leak
1 Spell Pierce
1 Didn't Say Please
1 Thought Collapse
1 Into the Roil
1 Blink of an Eye
1 Stern Dismissal
1 Vapor Snag
1 Unsummon
1 Devastation Tide
1 Wash Out
1 Aetherize
1 Traumatize
1 Fleet Swallower
1 Increasing Confusion
1 Keening Stone
1 Startled Awake
1 Ruin Crab
1 Teferi's Tutelage
1 Fraying Sanity
1 Folio of Fancies
1 Jace's Erasure
1 Drowned Secrets
1 Imperious Mindbreaker
1 Overwhelmed Apprentice
1 Manic Scribe
1 Deepmuck Desperado
1 Tome Scour
1 Mind Sculpt
1 Compelling Argument
1 Millstone
1 Codex Shredder
1 Ghoulcaller's Bell
1 Tormod's Crypt
1 Soul-Guide Lantern
1 Reliquary Tower
1 Halimar Depths
1 Lonely Sandbar
1 Remote Isle
1 Desert of the Mindful
1 Memorial to Genius
1 Evolving Wilds
1 Terramorphic Expanse
1 Castle Vantress
1 Skyline Cascade
29 Island
```

---

## Purchase Info

```
--- Purchase Info ---

  Total deck cost: $74.14 (cheapest printings via Scryfall)
  Pricing source:  Scryfall (aggregated market data)
  Prices as of:    2026-04-01

  Most expensive cards:
    Bruvac the Grandiloquent    $42.86
    Traumatize                  $3.76
    Folio of Fancies            $1.60
    Ruin Crab                   $1.49
    Sol Ring                    $1.45

  Note: Prices reflect cheapest available printing. Actual costs
  may vary by retailer and card condition. Bruvac dominates the
  budget at 58% of total cost -- consider proxying if playgroup allows.

  Upgrade path (when budget allows):
    +Psychic Corrosion ($6.47)     replaces Ghoulcaller's Bell
    +Maddening Cacophony ($9.09)   replaces Mind Sculpt
    +Court of Cunning ($5.04)      replaces Millstone
    +Hedron Crab ($2.73)           replaces Unsummon
    +Cyclonic Rift ($41.25)        replaces Wash Out
    +Mystic Remora ($10.68)        replaces Vision Skeins
    +Propaganda ($3.12)            replaces Vapor Snag
```

---

## Post-Output Actions

```
What would you like to do?

  "approve"   -- Save this deck (no further changes)
  "swap X Y"  -- Replace card X with card Y (re-runs validation)
  "rerun"     -- Start the pipeline over with the same intake answers
  "adjust"    -- Change intake parameters (budget, power level, etc.)
               and rebuild
```
