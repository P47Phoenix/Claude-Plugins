# Test Case 1: K'rrik Graveyard Recursion Deck

**PRD Dogfooding Protocol -- MTG Commander Deck Builder Plugin**

---

==============================================================
  MTG COMMANDER DECK: K'rrik, Son of Yawgmoth
  Strategy:    Graveyard Recursion (Aristocrats / Reanimator hybrid)
  Colors:      B (Mono-Black)
  Power Level: 6 (Focused casual)
  Total Cost:  $131.35 / $150 budget
  Synergy:     3.4 average interactions per card
  Cards:       100 (1 commander + 99)
==============================================================

## Strategy Description

K'rrik turns your life total into a mana battery -- every black mana symbol in a cost can be paid with 2 life instead, letting you vomit creatures onto the board turns ahead of schedule. The deck exploits this by running a deep suite of recursive creatures (Reassembling Skeleton, Bloodghast, Bloodsoaked Champion) that loop through sacrifice outlets (Viscera Seer, Carrion Feeder, Yahenni) to trigger death payoffs (Blood Artist, Zulaport Cutthroat, Bastion of Remembrance). K'rrik's lifelink recovers the life you spend casting spells, and the drain from aristocrats effects keeps you in the positive. When the board stalls, massive reanimation spells (Living Death, Victimize, Dread Return) reload your engine.

### Key Synergy Chains

1. **The Life Engine**: K'rrik pays life to cast black spells at discount -> lifelink recovers life -> aristocrats drain opponents -> net positive life while deploying threats
2. **The Recursion Loop**: Reassembling Skeleton / Bloodghast return from graveyard -> sacrifice to Viscera Seer / Carrion Feeder -> trigger Blood Artist / Zulaport Cutthroat -> drain all opponents each cycle
3. **The Token Factory**: Endrek Sahr makes Thrulls when you cast creatures -> sacrifice Thrulls to Sifter of Skulls / Pawn of Ulamog for Eldrazi Spawn -> sacrifice Spawn for mana -> trigger more death payoffs
4. **The Reanimation Blowout**: Self-mill via Fell Stinger / Body Launderer connive -> Living Death swaps graveyards to battlefields -> mass ETB triggers from Gray Merchant + Demon of Dark Schemes drain the table
5. **Extort Engine**: Pontiff of Blight gives all your creatures extort -> K'rrik lets you pay the {W/B} extort cost with life -> each spell drains each opponent for 1 per creature with extort

---

## Categorized Deck List

### --- Commander (1) --- Total: $0.80

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| K'rrik, Son of Yawgmoth | {4}{B/P}{B/P}{B/P} | $0.80 | Pays life instead of black mana, enabling explosive turns; lifelink recovers life spent; grows with +1/+1 counters on each black spell cast |

### --- Ramp (11) --- Total: $23.61

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Dark Ritual | {B} | $4.95 | Burst mana for explosive K'rrik turns; can be paid with life via K'rrik leaving net +2B mana |
| Soldevi Adnate | {1}{B} | $1.37 | Sacrifices black creatures or artifacts for mana equal to CMC; triggers Blood Artist on sacrifice; feeds Syr Konrad |
| Burnished Hart | {3} | $0.30 | Sacrifices for 2 Swamps; triggers death payoffs; recurable with reanimation spells for repeatable ramp |
| Bontu's Monument | {3} | $6.49 | Reduces cost of creature spells by {1}; drains each opponent 1 life and you gain 1 on each creature cast; amplifies K'rrik's creature-heavy game plan |
| Pitiless Plunderer | {3}{B} | $2.72 | Creates Treasure tokens whenever a creature you control dies; converts death triggers into mana; feeds aristocrats engine |
| Pawn of Ulamog | {1}{B}{B} | $4.09 | Creates 0/1 Eldrazi Spawn (sac for {1}) whenever a nontoken creature dies; mana from deaths; tokens feed sacrifice outlets |
| Charcoal Diamond | {2} | $0.29 | Taps for {B}; affordable mono-black ramp |
| Mind Stone | {2} | $0.24 | Taps for {1}; can sacrifice to draw a card when mana is no longer needed; triggers death-matters for artifacts going to graveyard (Syr Konrad) |
| Thought Vessel | {2} | $2.82 | Taps for {1}; no maximum hand size helps when Vilis draws many cards |
| Wayfarer's Bauble | {1} | $0.33 | Fetches a basic Swamp; early ramp that fuels Mutilate's Swamp count |
| Everflowing Chalice | {0} | $0.32 | Flexible mana rock; can be cast for 0 early or kicked later; Buried Ruin can retrieve it |

### --- Card Draw (10) --- Total: $14.31

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Midnight Reaper | {2}{B} | $0.23 | Draws a card whenever a nontoken creature you control dies; core draw engine in aristocrats; K'rrik pays life, Reaper draws cards |
| Grim Haruspex | {2}{B} | $2.60 | Draws on nontoken creature death; morph for surprise deployment; redundancy with Midnight Reaper |
| Morbid Opportunist | {2}{B} | $0.23 | Draws first time a creature dies each turn (including opponents' turns); triggers off edict effects on opponents' creatures |
| Disciple of Bolas | {3}{B} | $0.32 | Sacrifices a creature to draw cards equal to its power and gain that much life; sacrifice Grave Titan for 6 cards + 6 life |
| Fell Stinger | {1}{B}{B} | $0.34 | Exploit on ETB to draw 2 and lose 2 life; K'rrik's lifelink offsets the life loss; self-mills when exploiting |
| Skullclamp | {1} | $4.97 | Equip to 1-toughness tokens (Thrulls, Eldrazi Spawn) for instant 2-card draw + death trigger; premier draw engine |
| Village Rites | {B} | $1.57 | Sacrifice a creature to draw 2; instant speed sac outlet + card advantage; triggers death payoffs |
| Deadly Dispute | {1}{B} | $0.40 | Sacrifice artifact or creature to draw 2 + create Treasure; more efficient than Village Rites with Treasure upside |
| Night's Whisper | {1}{B} | $0.36 | Draw 2 for 2 life; K'rrik can cast for {1} + 4 life total, or just 2 mana normally |
| Phyrexian Arena | {1}{B}{B} | $3.29 | Draw an extra card each upkeep; K'rrik can cast for {1} + 4 life; sustained card advantage |

### --- Removal (6) --- Total: $3.80

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Go for the Throat | {1}{B} | $0.60 | Instant-speed creature destruction; K'rrik makes it cost {1} + 2 life |
| Tragic Slip | {B} | $0.32 | -1/-1 normally, -13/-13 with morbid; trivially enabled in a deck with constant creature deaths |
| Bone Shards | {B} | $0.23 | Destroy creature or planeswalker; additional cost to discard or sac a creature feeds graveyard/death triggers |
| Infernal Grasp | {1}{B} | $0.29 | Destroy target creature, lose 2 life; K'rrik's lifelink offsets; efficient removal |
| Feed the Swarm | {1}{B} | $0.36 | Destroys creature or enchantment; mono-black's best enchantment removal; life loss offset by K'rrik |
| Malicious Affliction | {B}{B} | $2.04 | Morbid: copy this spell; trivially destroys 2 creatures for {B}{B} (4 life via K'rrik); exceptional in aristocrats |

### --- Board Wipes (2) --- Total: $9.18

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Toxic Deluge | {2}{B} | $7.30 | Pay X life to give all creatures -X/-X; scalable, hits indestructible; K'rrik's lifelink recovers the life; best black wipe |
| Mutilate | {2}{B}{B} | $1.88 | All creatures get -1/-1 per Swamp you control; in 23+ Swamp deck, typically -6/-6 or more; K'rrik survives at high enough counters |

### --- Win Conditions (4) --- Total: $13.22

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| Gray Merchant of Asphodel | {3}{B}{B} | $2.10 | ETB drains each opponent for your devotion to black; in this devotion-heavy deck, often drains 7-12 per opponent; reanimatable for repeat triggers |
| Vilis, Broker of Blood | {5}{B}{B}{B} | $8.83 | Flying 8/8; whenever you lose life, draw that many cards; K'rrik paying life = massive card draw; {B}, pay 2 life: target creature -1/-1 draws you 2 cards |
| Demon of Dark Schemes | {4}{B}{B} | $1.91 | ETB gives all other creatures -2/-2 (partial wipe); gains energy on creature death; pays 4 energy to reanimate from any graveyard; board wipe + reanimation in one |
| Grave Titan | {4}{B}{B} | $0.38 | Creates two 2/2 Zombie tokens on ETB and attack; tokens feed sacrifice outlets; massive devotion contributor for Gary |

### --- Synergy Pieces (30) --- Total: $50.74

| Card | Mana Cost | Price | Synergy Rationale |
|------|-----------|-------|-------------------|
| **Death Trigger Payoffs** | | | |
| Blood Artist | {1}{B} | $2.19 | Drains 1 on any creature death (yours or opponents'); core aristocrats payoff; triggers on every sacrifice, board wipe, and edict |
| Zulaport Cutthroat | {1}{B} | $1.51 | Each opponent loses 1 whenever a creature you control dies; redundancy with Blood Artist |
| Syr Konrad, the Grim | {3}{B}{B} | $0.57 | Deals 1 to each opponent whenever a creature enters or leaves any graveyard; triggers on mill, reanimate, exile; unique reach |
| Ayara, First of Locthwain | {B}{B}{B} | $8.25 | Drains 1 on each black creature ETB (including tokens); can sacrifice for card draw; heavy black devotion for Gary |
| Bastion of Remembrance | {2}{B} | $0.31 | Enchantment with human token; drains on your creature death; harder to remove than creature-based payoffs |
| **Sacrifice Outlets** | | | |
| Viscera Seer | {B} | $0.41 | Free sacrifice; scry 1 on each sac; sculpts draws while triggering death payoffs |
| Carrion Feeder | {B} | $0.34 | Free sacrifice; grows with +1/+1 counters; can become a threat |
| Yahenni, Undying Partisan | {2}{B} | $0.31 | Free sacrifice; grows and gains indestructible until end of turn; survives your own board wipes |
| **Recursive Creatures** | | | |
| Reassembling Skeleton | {1}{B} | $0.18 | Returns from graveyard for {1}{B}; infinite sac fodder with enough mana; K'rrik makes return cost {1} + 2 life |
| Bloodghast | {B}{B} | $2.60 | Returns on landfall; can't block but great sacrifice fodder; haste at low life (common with K'rrik) |
| Bloodsoaked Champion | {B} | $0.34 | Returns for {1}{B} when you attack; aggressive recursive creature; feeds aristocrats engine |
| **Reanimation Creatures** | | | |
| Apprentice Necromancer | {1}{B} | $0.91 | Sacrifices to reanimate a creature for one turn; the reanimated creature dies at end step, triggering death payoffs again |
| Phyrexian Delver | {3}{B}{B} | $0.91 | ETB reanimates a creature, you lose life equal to its CMC; K'rrik's lifelink offsets; itself is reanimatable for loops |
| Whisper, Blood Liturgist | {3}{B} | $0.24 | Tap + sacrifice 2 creatures to reanimate; converts tokens into big threats; triggers 2 death triggers per activation |
| **Synergy Engine Cards** | | | |
| Body Launderer | {2}{B}{B} | $0.58 | Connive on nontoken creature death (draw + discard, fills graveyard); reanimates MV <= its power when it dies |
| Endrek Sahr, Master Breeder | {4}{B} | $1.44 | Creates X Thrull tokens when you cast a creature (X = its CMC); massive token generation for sacrifice; 1/1 tokens die to Skullclamp |
| Pontiff of Blight | {4}{B}{B} | $0.35 | Gives all creatures extort; K'rrik can pay the extort {W/B} with 2 life; each spell drains all opponents per creature |
| Butcher of Malakir | {5}{B}{B} | $0.39 | Flying 5/4; whenever a creature you control dies, opponents sacrifice a creature; stacks death triggers with forced sacrifice |
| Chainer, Dementia Master | {3}{B}{B} | $0.28 | Pay 3 life to reanimate from any graveyard as Nightmare; K'rrik makes this trivially cheap; repeatable reanimation engine |
| Enduring Tenacity | {2}{B}{B} | $5.91 | Whenever you gain life, opponents lose that much life (K'rrik's lifelink triggers this constantly); reanimates on death |
| Plaguecrafter | {2}{B} | $0.39 | Each player sacrifices a creature, planeswalker, or discards; edict that triggers your death payoffs too |
| Rankle, Master of Pranks | {2}{B}{B} | $3.52 | Flying 3/3 haste; on combat damage, choose modes: each player sacrifices/discards/draws + loses 1 life; multi-angle disruption |
| **Reanimation Spells** | | | |
| Victimize | {2}{B} | $0.62 | Sacrifice a creature to return 2 from graveyard; net +1 creature; triggers death payoff + 2 ETBs |
| Exhume | {1}{B} | $4.79 | Each player returns a creature from graveyard; 2 mana (or {1} + 2 life with K'rrik); fast reanimation |
| Dread Return | {2}{B}{B} | $0.62 | Reanimate from graveyard; flashback by sacrificing 3 creatures (triggers 3 death payoffs) |
| Living Death | {3}{B}{B} | $2.21 | All players sacrifice all creatures, then return all creatures from graveyards; in a deck that fills its graveyard, this is a one-sided board swap |
| Stitch Together | {B}{B} | $1.84 | Return creature from graveyard to hand; with threshold (7+ cards in GY), return to battlefield instead; trivially enabled in self-mill deck |
| **Recursion Enchantments** | | | |
| Phyrexian Reclamation | {B} | $2.19 | Pay {1}{B} + 2 life to return creature to hand; repeatable; K'rrik makes cost {1} + 4 life total; grindy recovery |
| Chthonian Nightmare | {1}{B} | $0.47 | Pay energy + life to reanimate creature with MV <= energy spent; self-fueling recursion engine |
| Oversold Cemetery | {1}{B} | $1.93 | If 4+ creatures in your graveyard, return one to hand each upkeep; free value in a deck that fills its graveyard naturally |

### --- Lands (36) --- Total: $15.69

| Card | Price |
|------|-------|
| Castle Locthwain | $3.77 |
| Crypt of Agadeem | $1.19 |
| Bojuka Bog | $0.95 |
| Barren Moor | $0.29 |
| Polluted Mire | $0.17 |
| Desert of the Glorified | $0.18 |
| Witch's Cottage | $0.82 |
| Mortuary Mire | $0.42 |
| Memorial to Folly | $0.31 |
| Myriad Landscape | $0.34 |
| Westvale Abbey | $3.10 |
| Hagra Mauling | $1.77 |
| Buried Ruin | $0.34 |
| Swamp x23 | ~$2.00 |

**Land synergy notes:**
- Castle Locthwain: Pay life to draw (K'rrik recovers)
- Crypt of Agadeem: Taps for {B} per black creature in graveyard (massive mana in late game)
- Bojuka Bog: Graveyard hate against opponents
- Witch's Cottage / Mortuary Mire / Memorial to Folly: Return creatures from graveyard
- Westvale Abbey: Sacrifice 5 creatures to create 9/7 flying indestructible lifelink demon
- Hagra Mauling: MDFC -- removal spell when needed, tapped land otherwise
- Barren Moor / Polluted Mire / Desert of the Glorified: Cycling lands smooth draws
- Buried Ruin: Returns Skullclamp or Mind Stone from graveyard
- Myriad Landscape: Fetches 2 Swamps for Mutilate count

---

## Pipeline Results

```
--- Pipeline Results ---

  Deck Builder:          100 cards constructed
  Rules Judge:           PASS -- all 7 checks clear
  Optimization Reviewer: PASS -- synergy score 3.4, all structural minimums met
  Price Evaluator:       PASS -- $131.35 total / $150 budget ($18.65 remaining)
  Correction Cycles:     0 used (max: 3)
```

### Rules Judge Verdict

```
RULES_JUDGE_VERDICT: PASS

CHECKS:
  card_count: 100/100
  names_verified: 100/100 (all validated via Scryfall batch lookup)
  color_identity: 100/100 (all within mono-B identity)
  banned_cards: 0 found
  singleton: PASS (no duplicates except basic Swamp)
  format_legality: 100/100 (all Commander-legal)
  synergy_audit: 0 false claims
```

### Optimization Reviewer Verdict

```
OPTIMIZATION_VERDICT: PASS

SYNERGY_SCORE: 3.4
ISOLATED_CARDS: 0

STRUCTURAL_CHECKS:
  ramp: 11/10 PASS
  card_draw: 10/10 PASS
  removal: 6/5 PASS
  board_wipes: 2/2 PASS
  win_conditions: 4/3 PASS
  lands: 36 PASS (range: 35-39 for mid-power)

MANA_CURVE:
  0-1: 14  (Viscera Seer, Carrion Feeder, Bloodsoaked Champion, Tragic Slip,
             Bone Shards, Village Rites, Dark Ritual, Wayfarer's Bauble,
             Everflowing Chalice, Skullclamp, Phyrexian Reclamation,
             Bastion of Remembrance starts at 3 but has 1-drop token, etc.)
  2:   16  (Blood Artist, Zulaport Cutthroat, Reassembling Skeleton,
             Bloodghast, Night's Whisper, Stitch Together, Exhume, etc.)
  3:   11  (Grim Haruspex, Midnight Reaper, Morbid Opportunist, Toxic Deluge,
             Phyrexian Arena, Plaguecrafter, Burnished Hart, etc.)
  4:   10  (Body Launderer, Rankle, Enduring Tenacity, Disciple of Bolas,
             Dread Return, Mutilate, Pitiless Plunderer, etc.)
  5:   7   (Gray Merchant, Syr Konrad, Endrek Sahr, Chainer, Phyrexian Delver,
             Living Death, etc.)
  6:   4   (Pontiff of Blight, Demon of Dark Schemes, Grave Titan, etc.)
  7+:  2   (Vilis Broker of Blood, Butcher of Malakir)
  average_mana_value: 2.8
  assessment: healthy -- bimodal curve (cheap enablers + expensive targets)
              appropriate for reanimator strategy

TOP_SYNERGY_CARDS:
  Reassembling Skeleton -- 8 interactions (Feeds, Triggers, Enables)
  Blood Artist -- 7 interactions (Triggers across all death effects)
  Viscera Seer -- 7 interactions (Enables sacrifice loops, Feeds death triggers)
  K'rrik, Son of Yawgmoth -- 6 interactions (Enables life-payment, Amplifies extort)
  Skullclamp -- 6 interactions (Feeds draw, Triggers death on 1-toughness tokens)
```

### Price Evaluator Verdict

```
PRICE_VERDICT: PASS

TOTAL_COST: $131.35
BUDGET: $150.00
REMAINING: $18.65 (under budget)
PER_CARD_CAP: $22.50 (15% of $150)
CAP_VIOLATIONS: 0
PRICE_UNAVAILABLE: 3 cards (Infernal Grasp, Bojuka Bog, Swamp -- estimated)

CATEGORY_BREAKDOWN:
  Commander:       $0.80  (1 card)
  Ramp:            $23.61 (11 cards)
  Card Draw:       $14.31 (10 cards)
  Removal:         $3.80  (6 cards)
  Board Wipes:     $9.18  (2 cards)
  Win Conditions:  $13.22 (4 cards)
  Synergy Pieces:  $50.74 (30 cards)
  Lands:           $15.69 (36 cards)

MOST_EXPENSIVE:
  1. Vilis, Broker of Blood     $8.83
  2. Ayara, First of Locthwain  $8.25
  3. Toxic Deluge               $7.30
  4. Bontu's Monument           $6.49
  5. Enduring Tenacity          $5.91
```

---

## Export List (copy-paste ready)

```
1 K'rrik, Son of Yawgmoth
1 Blood Artist
1 Zulaport Cutthroat
1 Syr Konrad, the Grim
1 Ayara, First of Locthwain
1 Bastion of Remembrance
1 Viscera Seer
1 Carrion Feeder
1 Yahenni, Undying Partisan
1 Reassembling Skeleton
1 Bloodghast
1 Bloodsoaked Champion
1 Apprentice Necromancer
1 Phyrexian Delver
1 Whisper, Blood Liturgist
1 Midnight Reaper
1 Grim Haruspex
1 Morbid Opportunist
1 Disciple of Bolas
1 Fell Stinger
1 Body Launderer
1 Endrek Sahr, Master Breeder
1 Pontiff of Blight
1 Butcher of Malakir
1 Chainer, Dementia Master
1 Plaguecrafter
1 Rankle, Master of Pranks
1 Enduring Tenacity
1 Pitiless Plunderer
1 Pawn of Ulamog
1 Gray Merchant of Asphodel
1 Vilis, Broker of Blood
1 Demon of Dark Schemes
1 Grave Titan
1 Soldevi Adnate
1 Burnished Hart
1 Dark Ritual
1 Charcoal Diamond
1 Mind Stone
1 Thought Vessel
1 Wayfarer's Bauble
1 Everflowing Chalice
1 Bontu's Monument
1 Skullclamp
1 Village Rites
1 Deadly Dispute
1 Night's Whisper
1 Phyrexian Arena
1 Victimize
1 Exhume
1 Dread Return
1 Living Death
1 Stitch Together
1 Phyrexian Reclamation
1 Chthonian Nightmare
1 Oversold Cemetery
1 Go for the Throat
1 Tragic Slip
1 Bone Shards
1 Infernal Grasp
1 Feed the Swarm
1 Malicious Affliction
1 Toxic Deluge
1 Mutilate
1 Castle Locthwain
1 Crypt of Agadeem
1 Bojuka Bog
1 Barren Moor
1 Polluted Mire
1 Desert of the Glorified
1 Witch's Cottage
1 Mortuary Mire
1 Memorial to Folly
1 Myriad Landscape
1 Westvale Abbey
1 Hagra Mauling
1 Buried Ruin
23 Swamp
```

---

## Purchase Info

```
  Total deck cost: $131.35 (cheapest printings via Scryfall)
  Pricing source:  Scryfall (aggregated market data)
  Prices as of:    2026-04-01

  Most expensive cards:
    Vilis, Broker of Blood     $8.83
    Ayara, First of Locthwain  $8.25
    Toxic Deluge               $7.30
    Bontu's Monument           $6.49
    Enduring Tenacity          $5.91

  Note: Prices reflect cheapest available printing. Actual costs
  may vary by retailer and card condition. 3 cards had no Scryfall
  pricing data and were estimated from known market values.
```

---

## Off-the-Beaten-Path Card Highlights

Per the user's request for cards chosen for synergy rather than generic popularity:

| Card | Why It's Here (Not Just "Good") |
|------|--------------------------------|
| **Soldevi Adnate** | Forgotten Ice Age card that sacrifices creatures for mana equal to their CMC -- turns reanimation targets into Dark Rituals while triggering death payoffs |
| **Dross Harvester** (not included, budget cut) | Gains 2 life per creature death but you lose 4 on your end step -- K'rrik loves the life gain but the tension is real |
| **Enduring Tenacity** | Newer card from Duskmourn -- whenever you gain life, opponents lose that much. K'rrik's lifelink turns every spell into a drain trigger |
| **Chthonian Nightmare** | Wilds of Eldraine enchantment that reanimates for energy + life. Self-fueling, pays for itself, and K'rrik doesn't mind the life cost |
| **Oversold Cemetery** | Odyssey bulk rare that returns a creature to hand every upkeep if you have 4+ creatures in graveyard. Free. Quiet. Devastating in grindy games |
| **Demon of Dark Schemes** | Often overlooked for splashier demons. ETB -2/-2 wipe + energy from any creature death + reanimate from ANY graveyard. Three abilities that all synergize with K'rrik |
| **Pontiff of Blight** | Gives ALL your creatures extort. K'rrik pays the extort cost with life. Each creature spell triggers 5-10 extort instances on a developed board |
| **Whisper, Blood Liturgist** | Sacrifices 2 creatures (tokens count) to reanimate. Triggers 2 death payoffs per activation. Quiet powerhouse |
| **Fell Stinger** | Exploit creature from your board to draw 2. The exploited creature triggers death payoffs. K'rrik offsets the life loss |
| **Malicious Affliction** | Morbid copies the spell. In a deck with constant creature deaths, this is a 2-for-1 removal spell for {B}{B} (4 life via K'rrik) |
| **Body Launderer** | Connive on each nontoken creature death fills your graveyard precisely. When Body Launderer dies, reanimate something with MV <= its power |
| **Strands of Night** (not included, final cut) | Enchantment from The Dark: sacrifice a Swamp + pay 2 life to reanimate. Repeatable, K'rrik-friendly costs |

---

## Test Case Metadata

```
Test Case ID:    TC-1
Plugin:          mtg-commander
Pipeline Agents: Deck Builder, Rules Judge, Optimization Reviewer, Price Evaluator
Intake Mode:     A (Full Inline)
Correction Cycles: 0
Total API Calls: ~25 Scryfall batch/validate/price calls
Cards Validated: 100/100 via Scryfall
Budget Status:   PASS ($131.35 / $150)
Structural Status: PASS (all minimums met)
Synergy Status:  PASS (3.4 avg interactions)
Legality Status: PASS (all 7 checks clear)
```
