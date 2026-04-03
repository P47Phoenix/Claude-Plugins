# Structural Minimums by Power Level

Reference document for the Optimization Reviewer agent. Defines minimum card counts per category, adjusted by power level tier and average mana value. These are hard floors -- a deck that fails to meet any minimum receives a FAIL verdict.

---

## Power Level Tiers

| Tier | Power Level | Description |
|------|------------|-------------|
| Casual | 1-4 | Precon-level or below. Fun-first, theme-heavy, lower interaction. |
| Mid | 5-7 | Upgraded precon to focused. Clear strategy, reasonable interaction. |
| High | 8-9 | Optimized. Fast mana, efficient interaction, focused win conditions. |
| cEDH | 10 | Competitive. Maximum efficiency, fastest wins, heaviest interaction. |

---

## Category Minimums

### Ramp

Sources that accelerate mana production beyond one land per turn.

| Tier | Minimum | Notes |
|------|---------|-------|
| Casual (1-4) | 10 | Includes mana rocks, mana dorks, land ramp spells |
| Mid (5-7) | 10 | Favor 2-CMC ramp (signets, talismans, Nature's Lore) |
| High (8-9) | 12 | Include fast mana (Sol Ring, Mana Vault, Chrome Mox) |
| cEDH (10) | 14 | Maximize fast mana, rituals, and 0-1 CMC acceleration |

**What counts as ramp**: Mana rocks, mana dorks, land ramp spells (Cultivate, Kodama's Reach), cost reducers, rituals. Does NOT count: lands themselves, cards that produce mana only conditionally, or cards whose primary function is something else with incidental mana (use disambiguation rule).

### Card Draw

Sources that provide card advantage -- drawing extra cards, impulse draw, or recurring card selection.

| Tier | Minimum | Notes |
|------|---------|-------|
| Casual (1-4) | 10 | Includes one-shot draw, enchantment-based draw engines |
| Mid (5-7) | 10 | Favor repeatable draw engines over one-shots |
| High (8-9) | 12 | Include efficient cantrips and engines |
| cEDH (10) | 14 | Maximize card velocity -- Necropotence, Ad Nauseam, etc. |

**What counts as card draw**: Draw spells, draw engines (Phyrexian Arena, Rhystic Study), cantrips (Brainstorm, Ponder), impulse draw (exile top, play this turn), tutors that find specific cards. Does NOT count: looting alone (draw + discard is card parity, not advantage, unless graveyard-matters), scry without draw.

### Targeted Removal

Spells or abilities that remove specific threats from the board.

| Tier | Minimum | Notes |
|------|---------|-------|
| Casual (1-4) | 5 | Covers creatures and some noncreature threats |
| Mid (5-7) | 5 | Include versatile removal (Beast Within, Generous Gift) |
| High (8-9) | 7 | Include counterspells for blue decks; instant-speed preferred |
| cEDH (10) | 8 | Maximize efficiency -- 0-2 CMC interaction (Swords, Path, Swan Song) |

**What counts as removal**: Destroy/exile target permanent, counterspells, bounce (temporary removal), -X/-X effects, fight effects. Does NOT count: board wipes (separate category), combat damage, forced sacrifice without targeting.

### Board Wipes

Effects that clear multiple permanents simultaneously.

| Tier | Minimum | Notes |
|------|---------|-------|
| Casual (1-4) | 2 | At least one creature wipe |
| Mid (5-7) | 2 | Include one that hits noncreature permanents |
| High (8-9) | 3 | Consider asymmetric wipes (Cyclonic Rift, Toxic Deluge) |
| cEDH (10) | 2 | Fewer needed -- games end before wipes matter; include compact ones |

**What counts as a board wipe**: Destroy/exile/bounce all creatures, all nonland permanents, or all permanents of a type. Partial wipes that hit 3+ targets conditionally count (e.g., Blasphemous Act). Does NOT count: targeted removal (even if it can hit multiple targets one at a time).

### Win Conditions

Cards that directly enable winning the game or represent the deck's primary path to victory.

| Tier | Minimum | Notes |
|------|---------|-------|
| Casual (1-4) | 3 | Clear win conditions, even if slow |
| Mid (5-7) | 3 | Redundant win conditions preferred |
| High (8-9) | 4 | Include compact combos or overwhelming finishers |
| cEDH (10) | 4 | Compact 2-3 card combos with tutor access |

**What counts as a win condition**: Cards that directly win the game (Thassa's Oracle, Craterhoof Behemoth), combo pieces that form a game-ending loop, or commanders that serve as the primary win condition (voltron commanders, combo commanders). Does NOT count: "good cards" that generate value but don't close the game.

### Lands

| Tier | Minimum | Maximum | Recommended | Notes |
|------|---------|---------|-------------|-------|
| Casual (1-4) | 36 | 40 | 37-38 | Higher land count compensates for fewer ramp sources |
| Mid (5-7) | 35 | 39 | 36-37 | Standard range |
| High (8-9) | 34 | 38 | 35-36 | Lower curve = fewer lands needed |
| cEDH (10) | 28 | 34 | 30-32 | Very low curves + heavy fast mana = fewer lands |

---

## Mana Value Adjustments

The above minimums assume an average mana value (AMV) between 2.5 and 3.5 for non-land cards. Adjust as follows:

| AMV Range | Land Adjustment | Ramp Adjustment |
|-----------|----------------|-----------------|
| < 2.0 | -2 lands from recommended | No change |
| 2.0 - 2.5 | -1 land from recommended | No change |
| 2.5 - 3.5 | No adjustment (baseline) | No adjustment |
| 3.5 - 4.0 | +1 land from recommended | +1 ramp |
| > 4.0 | +2 lands from recommended | +2 ramp |

---

## Category Summary Table

Quick reference for the Optimization Reviewer's structural validation.

| Category | Casual (1-4) | Mid (5-7) | High (8-9) | cEDH (10) |
|----------|-------------|-----------|------------|-----------|
| Ramp | 10+ | 10+ | 12+ | 14+ |
| Card Draw | 10+ | 10+ | 12+ | 14+ |
| Removal | 5+ | 5+ | 7+ | 8+ |
| Board Wipes | 2+ | 2+ | 3+ | 2+ |
| Win Conditions | 3+ | 3+ | 4+ | 4+ |
| Lands | 36-40 | 35-39 | 34-38 | 28-34 |

---

## Disambiguation Rule

When a card serves multiple category functions (e.g., Solemn Simulacrum is both ramp and card draw), assign it to the category with the **greatest structural deficit** -- the category furthest below its minimum. If no deficit exists, assign based on the card's primary function relative to the deck's strategy archetype.

This ensures structural minimums are deterministically verifiable. A card can only count toward ONE category.

---

## Validation Logic

The Optimization Reviewer checks:

1. Count cards per category.
2. Compare against the minimums for the deck's power level tier.
3. Apply mana value adjustments if AMV falls outside 2.5-3.5.
4. FAIL if any category is below its adjusted minimum.
5. FAIL if land count is outside the valid range for the tier.
6. Report each deficit with current count vs. minimum.
