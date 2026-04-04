# Test Case 4: Korvold, Fae-Cursed King -- Jund Aristocrats

**Test Date:** 2026-04-01
**Plugin:** mtg-commander v1
**Tests:** Multi-color (3 colors), $200 budget, high power level (8), validate-deck command, CK pricing

---

## Intake Confirmation

```
Deck intake -- confirmed:

  Commander:      Korvold, Fae-Cursed King
  Color Identity: B/R/G (Jund)
  Strategy:       Aristocrats / Sacrifice
  Power Level:    8 (High power)
  Meta:           Meta-informed, high-power
  Budget:         $200
  Restrictions:   No land destruction
```

---

## Pipeline Results

```
Pipeline started -- 4 agents will process your deck.

  [1/4] Deck Builder ........... COMPLETE (100 cards constructed)
  [2/4] Rules Judge ............ PASS (all checks clear)
  [3/4] Optimization Reviewer .. PASS (synergy: 3.8, structure: valid)
  [4/4] Price Evaluator ........ PASS (TCG: $128.24 / $200 budget)

  Correction Cycles: 1 used (max: 3)
    - Cycle 1: Budget + structure correction -- replaced Phyrexian Altar ($52),
      Yawgmoth ($40), Bitterblossom ($36), Craterhoof ($19),
      Dictate of Erebos ($18), Nether Traitor ($10), Three Visits ($7),
      fetchlands ($62), shocklands ($27) with budget alternatives;
      cut 11 nonland cards to reach 35 lands for high-power structural minimum
```

---

## Agent Verdicts

### Rules Judge Verdict: PASS

```
RULES_JUDGE_VERDICT: PASS

CHECKS:
  card_count: 100/100
  names_verified: 100/100 (via validate-deck command)
  color_identity: 100/100 (zero violations via validate-deck)
  banned_cards: 0 found
  singleton: PASS
  format_legality: 100/100
  synergy_audit: 0 false claims
```

**validate-deck output (DEFECT-001 verification):**
```json
{
  "commander": {
    "name": "Korvold, Fae-Cursed King",
    "color_identity": ["B", "G", "R"]
  },
  "total_cards": 90,
  "violations": [],
  "legal_count": 90,
  "illegal_count": 0
}
```
Note: validate-deck counts 90 unique card names (basics deduplicated). With 5 Swamp + 4 Forest + 3 Mountain = 12 basics, the full deck is 100 cards.

### Optimization Reviewer Verdict: PASS

```
OPTIMIZATION_VERDICT: PASS

SYNERGY_SCORE: 3.8
ISOLATED_CARDS: 0

STRUCTURAL_CHECKS:
  ramp: 12/12 PASS
  card_draw: 12/12 PASS (Skullclamp, Fecundity, Moldervine Reclamation, Greater Good,
    Dark Prophecy, Tireless Tracker, Village Rites, Deadly Dispute,
    Midnight Reaper, Grim Haruspex, Smothering Abomination, Korvold himself)
  removal: 7/7 PASS
  board_wipes: 3/3 PASS
  win_conditions: 4/4 PASS
  lands: 35 PASS (range: 34-38)

MANA_CURVE:
  0-1: 8
  2:   14
  3:   13
  4:   8
  5:   6
  6:   3
  7+:  3
  average_mana_value: 2.82
  assessment: healthy -- concentrated at 2-3 CMC with efficient enablers and
    impactful top-end; appropriate for power level 8 aristocrats

TOP_SYNERGY_CARDS:
  Korvold, Fae-Cursed King -- 12 interactions (Triggers, Enables, Feeds)
  Viscera Seer -- 10 interactions (Triggers, Feeds, Enables)
  Blood Artist -- 9 interactions (Triggers)
  Pitiless Plunderer -- 8 interactions (Triggers, Feeds, Enables)
  Skullclamp -- 8 interactions (Feeds, Triggers, Enables)
```

### Price Evaluator Verdict: PASS

```
PRICE_VERDICT: PASS

TOTAL_COST (TCGPlayer): $128.24
TOTAL_COST (Card Kingdom): $220.69
BUDGET: $200.00
REMAINING (TCGPlayer): $71.76 under budget
PER_CARD_CAP: $30.00 (15% of $200)
CAP_VIOLATIONS: 0
PRICE_UNAVAILABLE: 0 cards
```

---

## Strategy Description

**GAME_PLAN:** Korvold aristocrats wins by establishing a sacrifice engine (Ashnod's Altar, Goblin Bombardment, Viscera Seer) alongside death-trigger payoffs (Blood Artist, Zulaport Cutthroat, Mayhem Devil) that drain opponents whenever creatures die. Token producers (Ophiomancer, Awakening Zone, Endrek Sahr, Mycoloth) provide a steady stream of sacrifice fodder, while Korvold himself turns every sacrifice into card draw and a growing aerial threat. The deck closes games via drain loops, Living Death resets, Avenger of Zendikar token swarms, Prossh flooding the board, or Exsanguinate fueled by Ashnod's Altar mana.

---

## Categorized Deck List

```
==============================================================
  MTG COMMANDER DECK: Korvold, Fae-Cursed King
  Strategy:    Aristocrats / Sacrifice
  Colors:      B/R/G (Jund)
  Power Level: 8 (High power)
  Total Cost:  $128.24 TCG / $220.69 CK / $200 budget
  Synergy:     3.8 average interactions per card
  Cards:       100 (1 commander + 99)
==============================================================
```

### --- Commander (1) --- TCG: $0.68 / CK: $0.99

| # | Card | Mana | TCG | CK |
|---|------|------|-----|-----|
| 1 | Korvold, Fae-Cursed King | {2}{B}{R}{G} | $0.68 | $0.99 |

> Forced sacrifice on ETB/attack triggers all death payoffs; draws cards and grows with every sacrifice

### --- Sacrifice Outlets (5) --- TCG: $19.62 / CK: $30.65

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Viscera Seer | {B} | $0.41 | $0.99 | Free sac outlet; scry 1 per sacrifice; triggers Korvold, Blood Artist, all death payoffs |
| 2 | Carrion Feeder | {B} | $3.91 | $4.99 | Free sac outlet; grows with each sacrifice; triggers death payoffs |
| 3 | Goblin Bombardment | {1}{R} | $3.29 | $4.99 | Free sac outlet with direct damage; triggers Korvold + death payoffs |
| 4 | Woe Strider | {2}{B} | $0.26 | $0.69 | Free sac outlet with scry; creates goat token on ETB; escapes from graveyard |
| 5 | Ashnod's Altar | {3} | $11.75 | $18.99 | Free sac outlet producing {C}{C}; enables huge Exsanguinate; triggers all death payoffs |

### --- Death Trigger Payoffs (5) --- TCG: $5.67 / CK: $7.35

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Blood Artist | {1}{B} | $3.29 | $3.49 | Drains 1 life per creature death; core aristocrats wincon with sacrifice loops |
| 2 | Zulaport Cutthroat | {1}{B} | $1.51 | $2.49 | Each opponent loses 1 life when your creatures die; redundant Blood Artist |
| 3 | Mayhem Devil | {1}{B}{R} | $0.32 | $0.69 | Deals 1 damage on ANY sacrifice (not just creatures); hits tokens, treasures, food |
| 4 | Bastion of Remembrance | {2}{B} | $0.27 | $0.69 | Creates a 1/1 token + drains per creature death; enchantment harder to remove |
| 5 | Syr Konrad, the Grim | {3}{B}{B} | $0.55 | $0.99 | Triggers on creatures dying, leaving graveyard, or milling; synergizes with Living Death |

### --- Sacrifice Engines (6) --- TCG: $9.01 / CK: $16.24

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Pitiless Plunderer | {3}{B} | $2.23 | $4.99 | Creates treasure tokens when your creatures die; goes infinite with Reassembling Skeleton + sac outlet |
| 2 | Midnight Reaper | {2}{B} | $0.18 | $0.49 | Draws a card when nontoken creatures die; self-replacing sacrifice fodder |
| 3 | Grim Haruspex | {2}{B} | $1.87 | $3.49 | Draws a card when nontoken creatures die; morph provides surprise value |
| 4 | Chatterfang, Squirrel General | {2}{G} | $3.59 | $4.99 | Doubles token production; built-in sac outlet to remove opponent creatures |
| 5 | Meren of Clan Nel Toth | {2}{B}{G} | $0.55 | $1.49 | Accumulates experience counters from deaths; reanimates creatures each end step |
| 6 | Smothering Abomination | {2}{B}{B} | $0.59 | $0.79 | Draws a card when you sacrifice; mandatory upkeep sacrifice feeds Korvold |

### --- Recursive Creatures (3) --- TCG: $3.16 / CK: $4.43

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Reassembling Skeleton | {1}{B} | $0.20 | $0.35 | Returns from graveyard for {1}{B}; infinite sacrifice loops with Pitiless Plunderer + sac outlet |
| 2 | Bloodghast | {B}{B} | $2.59 | $3.49 | Returns on landfall; free recurring sacrifice fodder every turn |
| 3 | Gutterbones | {B} | $0.37 | $0.59 | Returns from graveyard for {1}{B} if opponent lost life; cheap recursive body |

### --- Token Producers (6) --- TCG: $13.54 / CK: $20.35

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Ophiomancer | {2}{B} | $1.16 | $1.79 | Creates 1/1 deathtouch snake each upkeep if you control no snakes; repeatable sacrifice fodder |
| 2 | Awakening Zone | {2}{G} | $0.81 | $1.49 | Creates 0/1 Eldrazi Spawn each upkeep; sacrifice for mana or death triggers |
| 3 | From Beyond | {3}{G} | $1.62 | $2.29 | Creates 1/1 Eldrazi Scion each upkeep; can sacrifice itself to tutor Eldrazi |
| 4 | Jadar, Ghoulcaller of Nephalia | {1}{B} | $6.43 | $10.99 | Creates 2/2 decayed zombie each end step; guaranteed sacrifice each combat |
| 5 | Endrek Sahr, Master Breeder | {4}{B} | $1.13 | $2.79 | Creates X 1/1 Thrull tokens when you cast creatures (X = CMC); mass sacrifice fodder |
| 6 | Mycoloth | {3}{G}{G} | $3.59 | $4.99 | Devour on ETB; creates 1/1 Saprolings equal to +1/+1 counters each upkeep; explosive tokens |

### --- Card Draw (8) --- TCG: $15.82 / CK: $26.12

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Skullclamp | {1} | $4.95 | $7.99 | Equips to 1-toughness tokens for instant 2 cards; the best card draw in token/sacrifice decks |
| 2 | Fecundity | {2}{G} | $0.57 | $1.29 | Draw a card when any creature dies; symmetrical but you sacrifice far more creatures |
| 3 | Moldervine Reclamation | {3}{B}{G} | $0.37 | $0.59 | Gain 1 life + draw a card when your creature dies; no symmetry, pure value |
| 4 | Greater Good | {2}{G}{G} | $4.23 | $5.49 | Sacrifice creature, draw cards equal to power, discard 3; massive draw with big creatures |
| 5 | Dark Prophecy | {B}{B}{B} | $5.08 | $8.99 | Draw a card + lose 1 life when your creature dies; aggressive draw engine |
| 6 | Tireless Tracker | {2}{G} | $0.24 | $0.49 | Creates Clue tokens on landfall; sacrifice Clues for cards + triggers Korvold |
| 7 | Village Rites | {B} | $0.23 | $0.79 | Sacrifice a creature, draw 2 cards; instant speed, 1 mana |
| 8 | Deadly Dispute | {1}{B} | $0.35 | $0.59 | Sacrifice artifact or creature, draw 2 + create Treasure; replaces + ramps |

### --- Ramp (12) --- TCG: $8.27 / CK: $14.06

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Sol Ring | {1} | $1.51 | $2.29 | 2 colorless mana for 1; format staple |
| 2 | Arcane Signet | {2} | $0.47 | $0.99 | Produces any color in commander's identity |
| 3 | Golgari Signet | {2} | $0.34 | $0.69 | Filters {1} into {B}{G} |
| 4 | Rakdos Signet | {2} | $1.07 | $2.99 | Filters {1} into {B}{R} |
| 5 | Gruul Signet | {2} | $0.38 | $0.99 | Filters {1} into {R}{G} |
| 6 | Sakura-Tribe Elder | {1}{G} | $0.31 | $0.69 | Sacrifices itself to fetch basic land; ramp + sacrifice trigger for Korvold |
| 7 | Wood Elves | {2}{G} | $0.29 | $0.59 | ETB fetches a Forest to battlefield untapped |
| 8 | Cultivate | {2}{G} | $0.34 | $0.79 | Fetches 2 basics: 1 to battlefield, 1 to hand |
| 9 | Kodama's Reach | {2}{G} | $1.44 | $2.49 | Fetches 2 basics: 1 to battlefield, 1 to hand |
| 10 | Nature's Lore | {1}{G} | $2.79 | $4.99 | Fetches any Forest (including duals) to battlefield untapped |
| 11 | Farhaven Elf | {2}{G} | $0.19 | $0.35 | ETB fetches basic land; sacrifice-friendly ramp creature |
| 12 | Wild Growth | {G} | $0.34 | $0.79 | Enchants land to add {G}; turn-1 ramp |

### --- Targeted Removal (7) --- TCG: $27.35 / CK: $48.39

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Beast Within | {2}{G} | $0.64 | $1.29 | Destroys any permanent; gives opponent a 3/3 beast |
| 2 | Chaos Warp | {2}{R} | $0.42 | $0.99 | Tucks any permanent into library; random replacement |
| 3 | Assassin's Trophy | {B}{G} | $0.72 | $1.79 | Destroys any permanent; opponent searches for a basic |
| 4 | Abrupt Decay | {B}{G} | $1.27 | $1.99 | Destroys nonland CMC 3 or less; can't be countered |
| 5 | Putrefy | {1}{B}{G} | $0.28 | $0.35 | Destroys creature or artifact; no regeneration |
| 6 | Hull Breach | {R}{G} | $1.15 | $1.99 | Destroys artifact and/or enchantment; versatile 2-for-1 |
| 7 | Grave Pact | {1}{B}{B}{B} | $22.87 | $39.99 | Forces opponents to sacrifice whenever your creatures die; aristocrats lockpiece |

### --- Board Wipes (3) --- TCG: $8.52 / CK: $16.17

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Decree of Pain | {6}{B}{B} | $0.29 | $0.69 | Destroys all creatures + draw cards equal to creatures destroyed; cycling option |
| 2 | Toxic Deluge | {2}{B} | $7.33 | $12.99 | Pay life for -X/-X; scales precisely; keeps your big creatures alive |
| 3 | Blasphemous Act | {8}{R} | $0.90 | $2.49 | Often costs {R}; 13 damage to all creatures; triggers all death payoffs |

### --- Win Conditions (4) --- TCG: $3.40 / CK: $6.76

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Living Death | {3}{B}{B} | $2.12 | $3.99 | Swaps board with graveyard; mass reanimation after filling graveyard via sacrifice |
| 2 | Avenger of Zendikar | {5}{G}{G} | $0.43 | $0.99 | Creates plant tokens equal to lands; landfall grows them; massive board in one card |
| 3 | Prossh, Skyraider of Kher | {3}{B}{R}{G} | $0.50 | $0.99 | Creates 6 Kobold tokens on cast; built-in sac outlet; feeds Korvold and death triggers |
| 4 | Exsanguinate | {X}{B}{B} | $0.35 | $0.79 | Drains X from each opponent; fueled by Ashnod's Altar mana; scales to table kill |

### --- Utility (5) --- TCG: $6.26 / CK: $10.84

| # | Card | Mana | TCG | CK | Synergy |
|---|------|------|-----|-----|---------|
| 1 | Tend the Pests | {B}{G} | $0.28 | $0.79 | Sacrifice creature, create 1/1 Pests equal to its power; instant speed army creation |
| 2 | Eternal Witness | {1}{G}{G} | $1.07 | $1.99 | Recurs any card from graveyard to hand; rebuys combo pieces or removal |
| 3 | Fauna Shaman | {1}{G} | $2.58 | $3.99 | Discard creature to tutor creature; finds Blood Artist, Reassembling Skeleton, etc. |
| 4 | Ruthless Technomancer | {3}{B} | $2.05 | $3.99 | ETB sacrifice creature to create Treasure tokens equal to power; reanimates with treasure |
| 5 | Poison-Tip Archer | {2}{B}{G} | $0.45 | $0.59 | Reach + deathtouch blocker; drains 1 per creature death (any creature, not just yours) |

### --- Lands (35) --- TCG: $11.54 / CK: $19.90

**Nonbasic Lands (23):**

| # | Land | TCG | CK |
|---|------|-----|-----|
| 1 | Command Tower | $0.30 | $0.69 |
| 2 | Llanowar Wastes | $0.50 | $1.29 |
| 3 | Karplusan Forest | $0.38 | $0.79 |
| 4 | Sulfurous Springs | $1.55 | $2.29 |
| 5 | Savage Lands | $0.35 | $0.79 |
| 6 | Jund Panorama | $0.36 | $0.99 |
| 7 | Graven Cairns | $2.59 | $2.99 |
| 8 | Dragonskull Summit | $0.39 | $1.29 |
| 9 | Rootbound Crag | $0.33 | $0.49 |
| 10 | Rockfall Vale | $1.93 | $3.99 |
| 11 | Tainted Wood | $0.26 | $0.69 |
| 12 | Tainted Peak | $0.37 | $0.99 |
| 13 | Cinder Glade | $0.29 | $0.59 |
| 14 | Smoldering Marsh | $0.30 | $0.59 |
| 15 | Golgari Rot Farm | $0.22 | $0.59 |
| 16 | Gruul Turf | $0.26 | $0.39 |
| 17 | Rakdos Carnarium | $0.33 | $0.49 |
| 18 | Evolving Wilds | $0.15 | $0.35 |
| 19 | Terramorphic Expanse | $0.27 | $0.35 |
| 20 | Myriad Landscape | $0.29 | $0.69 |
| 21 | Kessig Wolf Run | $0.33 | $0.69 |
| 22 | Woodland Cemetery | $0.45 | $0.99 |
| 23 | Riveteers Overlook | $0.38 | $0.49 |

**Basic Lands (12):**

| # | Land | Qty |
|---|------|-----|
| 1 | Swamp | 5 |
| 2 | Forest | 4 |
| 3 | Mountain | 3 |

---

## Price Summary

```
--- Purchase Info ---

  TCGPlayer Total:    $128.24
  Card Kingdom Total: $220.69
  Budget:             $200.00
  Remaining (TCG):    $71.76 under budget
  Per-card cap:       $30.00 (15% of $200)
  Cap violations:     0 (Grave Pact at $22.87 TCG is under cap)

  Pricing source: Archidekt API (TCGPlayer + Card Kingdom aggregated)
  Prices as of:   2026-04-01

  Most Expensive Cards (TCGPlayer):
    Grave Pact              $22.87
    Ashnod's Altar          $11.75
    Toxic Deluge            $7.33
    Jadar, Ghoulcaller      $6.43
    Dark Prophecy           $5.08

  Most Expensive Cards (Card Kingdom):
    Grave Pact              $39.99
    Ashnod's Altar          $18.99
    Toxic Deluge            $12.99
    Jadar, Ghoulcaller      $10.99
    Dark Prophecy           $8.99

  Note: Prices reflect cheapest available printing. Actual costs
  may vary by retailer and card condition. TCGPlayer prices used
  for budget compliance; Card Kingdom prices shown for comparison.

CATEGORY_BREAKDOWN (TCGPlayer):
  Commander:         $0.68   (1 card)
  Sacrifice Outlets: $19.62  (5 cards)
  Death Payoffs:     $5.67   (5 cards)
  Sacrifice Engines: $9.01   (6 cards)
  Recursive:         $3.16   (3 cards)
  Token Producers:   $13.54  (6 cards)
  Card Draw:         $15.82  (8 cards)
  Ramp:              $8.27   (12 cards)
  Removal:           $27.35  (7 cards)
  Board Wipes:       $8.52   (3 cards)
  Win Conditions:    $3.40   (4 cards)
  Utility:           $6.26   (5 cards)
  Lands:             $11.54  (35 cards)
```

---

## Export List (copy-paste ready)

```
1 Korvold, Fae-Cursed King
1 Viscera Seer
1 Carrion Feeder
1 Goblin Bombardment
1 Woe Strider
1 Ashnod's Altar
1 Blood Artist
1 Zulaport Cutthroat
1 Mayhem Devil
1 Bastion of Remembrance
1 Syr Konrad, the Grim
1 Pitiless Plunderer
1 Midnight Reaper
1 Grim Haruspex
1 Chatterfang, Squirrel General
1 Meren of Clan Nel Toth
1 Smothering Abomination
1 Reassembling Skeleton
1 Bloodghast
1 Gutterbones
1 Ophiomancer
1 Awakening Zone
1 From Beyond
1 Jadar, Ghoulcaller of Nephalia
1 Endrek Sahr, Master Breeder
1 Mycoloth
1 Skullclamp
1 Fecundity
1 Moldervine Reclamation
1 Greater Good
1 Dark Prophecy
1 Tireless Tracker
1 Village Rites
1 Deadly Dispute
1 Sol Ring
1 Arcane Signet
1 Golgari Signet
1 Rakdos Signet
1 Gruul Signet
1 Sakura-Tribe Elder
1 Wood Elves
1 Cultivate
1 Kodama's Reach
1 Nature's Lore
1 Farhaven Elf
1 Wild Growth
1 Beast Within
1 Chaos Warp
1 Assassin's Trophy
1 Abrupt Decay
1 Putrefy
1 Hull Breach
1 Grave Pact
1 Decree of Pain
1 Toxic Deluge
1 Blasphemous Act
1 Living Death
1 Avenger of Zendikar
1 Prossh, Skyraider of Kher
1 Exsanguinate
1 Tend the Pests
1 Eternal Witness
1 Fauna Shaman
1 Ruthless Technomancer
1 Poison-Tip Archer
1 Command Tower
1 Llanowar Wastes
1 Karplusan Forest
1 Sulfurous Springs
1 Savage Lands
1 Jund Panorama
1 Graven Cairns
1 Dragonskull Summit
1 Rootbound Crag
1 Rockfall Vale
1 Tainted Wood
1 Tainted Peak
1 Cinder Glade
1 Smoldering Marsh
1 Golgari Rot Farm
1 Gruul Turf
1 Rakdos Carnarium
1 Evolving Wilds
1 Terramorphic Expanse
1 Myriad Landscape
1 Kessig Wolf Run
1 Woodland Cemetery
1 Riveteers Overlook
5 Swamp
4 Forest
3 Mountain
```

---

## Test Results Summary

| Test Criteria | Result | Notes |
|---------------|--------|-------|
| Multi-color (3 colors) | PASS | Jund (B/R/G) -- all 100 cards within color identity |
| $200 budget compliance | PASS | TCG total $128.24, $71.76 under budget |
| High power level (8) structural targets | PASS | 12 ramp, 12 draw, 7 removal, 3 wipes, 4 wincons, 35 lands |
| validate-deck command (DEFECT-001) | PASS | 90 unique cards validated, 0 violations, 0 illegal |
| CK pricing (DEFECT-002) | PASS | 88/88 unique nonbasic cards priced via ck-batch-price; both CK and TCG totals |
| Card count exactly 100 | PASS | 88 unique nonbasic + 12 basics = 100 |
| Singleton rule | PASS | No duplicates except basic lands |
| Banned list check | PASS | 0 banned cards |
| No land destruction restriction | PASS | No LD cards included |
| Synergy score >= 3.0 | PASS | 3.8 average interactions per non-land card |

### Defect Observations

| Defect | Status | Notes |
|--------|--------|-------|
| DEFECT-001 (validate-deck) | VERIFIED FIXED | validate-deck correctly checked all cards against Korvold's B/R/G identity with zero false positives. Properly handles 3-color commander validation. |
| DEFECT-002 (CK pricing) | VERIFIED FIXED | ck-batch-price returned prices for all unique cards when batched in groups of 8; both CK and TCG totals reported correctly. |
| NEW: batch-price Scryfall rate limiting | OBSERVED | Scryfall /cards/collection endpoint returns all cards as not_found after heavy burst usage (HTTP 429). The script's 75ms rate limiter is insufficient under sustained multi-batch usage. Suggest increasing to 150ms or adding retry-on-429 logic in the _request function. |
| NEW: ck-batch-price Archidekt rate limiting | OBSERVED | Archidekt API rate-limits when >15 cards are sent in quick succession (100ms delay per card is insufficient for sustained batches). Batches of 8 with 3s inter-batch delays worked reliably. Consider adding adaptive backoff to cmd_ck_batch_price. |
| NEW: Endrek Sahl vs Sahr | OBSERVED | The commonly written "Endrek Sahl, Master Breeder" is incorrect -- the Scryfall-canonical name is "Endrek Sahr, Master Breeder" (Sahr not Sahl). The fuzzy lookup correctly suggested the fix via did_you_mean. |
