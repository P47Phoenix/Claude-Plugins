# Synergy Interaction Taxonomy

Reference document for the Optimization Reviewer and Deck Builder agents. Defines the 6 valid interaction categories, exclusion rules, scoring thresholds, and the structured tag format used throughout the pipeline.

---

## Purpose

Every non-land card in a Commander deck must interact meaningfully with 3 or more other cards. "Meaningful" is defined by this taxonomy -- only interactions matching one of the 6 categories below count toward the threshold. This is the core enforcement mechanism for synergy-first deck construction.

---

## The 6 Interaction Categories

### 1. TRIGGERS

**Definition**: Card A's effect causes Card B's triggered ability to fire.

**Tag format**: `[TRIGGERS: <target card name>]`

**Examples**:
- Viscera Seer sacrificing a creature **triggers** Blood Artist's "whenever a creature dies" ability.
- Panharmonicon entering the battlefield does not trigger anything by itself -- it amplifies triggers (see AMPLIFIES).
- Fetch lands cracking **trigger** landfall abilities (Avenger of Zendikar, Omnath).

**What counts**: One card's action (ETB, dies, cast, attack, sacrifice, etc.) directly fires another card's triggered ability (begins with "when", "whenever", or "at").

**What does NOT count**: Two cards that merely have triggered abilities but don't trigger each other.

---

### 2. ENABLES

**Definition**: Card A provides a resource or condition that Card B specifically requires to function or function optimally.

**Tag format**: `[ENABLES: <target card name>]`

**Examples**:
- Urborg, Tomb of Yawgmoth making all lands Swamps **enables** Cabal Coffers to count more lands.
- Bitterblossom producing tokens **enables** Skullclamp by providing 1-toughness creatures to equip.
- Phyrexian Altar providing colored mana from sacrificed creatures **enables** infinite loops requiring specific colors.

**What counts**: Card A creates a specific condition, resource, or state that Card B's text explicitly references or requires.

**What does NOT count**: Generic mana enablement. Sol Ring does NOT "enable" every card that costs 2+ mana. Ramp enabling expensive cards is the ramp category's structural role, not a synergy interaction. If the only connection is "A produces mana and B costs mana," it is NOT an ENABLES interaction.

---

### 3. PROTECTS

**Definition**: Card A shields Card B from removal, counters, or adverse effects, preserving Card B's presence on the battlefield.

**Tag format**: `[PROTECTS: <target card name>]`

**Examples**:
- Lightning Greaves giving shroud and haste **protects** a voltron commander from targeted removal.
- Heroic Intervention giving hexproof and indestructible **protects** your board from a wipe.
- Counterspell holding up mana **protects** a combo piece from being countered.

**What counts**: Card A's effect directly prevents Card B from being destroyed, exiled, countered, bounced, or otherwise removed.

**What does NOT count**: Being in the same deck. Having hexproof innately is not a synergy with another card -- it's the card's own ability.

---

### 4. COMBOS-WITH

**Definition**: Cards A and B form part of a defined combination (2-4 cards) that produces a win condition or overwhelming advantage that no single card achieves alone.

**Tag format**: `[COMBOS-WITH: <target card name>]`

**Examples**:
- Sanguine Bond **combos with** Exquisite Blood (infinite life drain loop).
- Kiki-Jiki, Mirror Breaker **combos with** Zealous Conscripts (infinite hasty tokens).
- Dramatic Reversal **combos with** Isochron Scepter (infinite mana with mana rocks).

**What counts**: Two or more cards that together produce an effect dramatically greater than the sum of their individual effects -- typically an infinite loop, instant win, or lockout. The combo must be mechanically defined (not just "these cards are both good").

**What does NOT count**: Two independently powerful cards. Demonic Tutor + Thassa's Oracle is not a combo -- Tutor finds anything, Oracle wins with an empty library. The combo is Oracle + Demonic Consultation (which exiles the library).

---

### 5. AMPLIFIES

**Definition**: Card A increases the output or effectiveness of Card B's ability by a measurable factor.

**Tag format**: `[AMPLIFIES: <target card name>]`

**Examples**:
- Panharmonicon doubling Solemn Simulacrum's ETB (2 lands + 2 draws instead of 1+1) **amplifies** Solemn Simulacrum.
- Doubling Season doubling token output **amplifies** any token producer.
- Torbran, Thane of Red Fell adding +2 damage **amplifies** any red damage source.

**What counts**: Card A contains a multiplier, doubler, adder, or scaling effect that measurably increases Card B's numerical output (damage, tokens, counters, triggers, etc.).

**What does NOT count**: Generic buffs that apply to everything without specific mechanical interaction. A +1/+1 anthem amplifies all creatures -- this counts for each creature, but only if the creature's strategy role benefits from the buff meaningfully (not just "bigger body").

---

### 6. FEEDS

**Definition**: Card A produces tokens, cards, resources, or permanents that Card B specifically consumes, processes, or sacrifices.

**Tag format**: `[FEEDS: <target card name>]`

**Examples**:
- Bitterblossom producing Faerie tokens **feeds** Skullclamp (which needs small creatures to equip and sacrifice).
- Smothering Tithe producing Treasure tokens **feeds** Reckless Fireweaver (artifact ETB triggers).
- Reassembling Skeleton returning from the graveyard **feeds** any sacrifice outlet repeatedly.

**What counts**: Card A's output (tokens, resources, recurrable permanents) is specifically useful to Card B's input requirements. There must be a producer-consumer relationship.

**What does NOT count**: Generic resource production consumed by generic resource usage. A land producing mana that a creature costs does not establish a FEEDS relationship.

---

## Exclusion Rules

The following do NOT count as synergy interactions under any category:

### Exclusion 1: Type-Sharing Alone

Two cards sharing a creature type (e.g., both are Elves) is NOT an interaction unless one card's text mechanically references the shared type. A lord that gives +1/+1 to all Elves DOES interact with each Elf (AMPLIFIES). Two vanilla Elves do NOT interact.

### Exclusion 2: Generic Mana Enablement

Ramp cards producing mana that other cards spend is NOT an interaction. Sol Ring does not "enable" or "feed" every card in the deck. Ramp's role is structural (meeting the ramp minimum in `structural-minimums.md`), not synergistic.

**Exception**: If a ramp card produces a specific resource that another card specifically references (e.g., Treasure tokens feeding Reckless Fireweaver's artifact ETB trigger), that IS a valid interaction under FEEDS or TRIGGERS.

### Exclusion 3: "Both Good Cards"

Two cards that are individually powerful in the same strategy but have no mechanical connection do NOT interact. Demonic Tutor and Rhystic Study are both strong in black/blue decks -- they do not interact with each other. Evaluate mechanical text, not strategic reputation.

---

## Scoring

### Per-Card Threshold

| Scenario | Minimum Interactions |
|----------|---------------------|
| Standard | 3 interactions with other cards in the deck |
| Budget-forced swap (FR-07.4) | 2 interactions allowed (with warning in verdict) |

A card "interacting with 3 other cards" means it has 3 or more valid synergy tags pointing to 3 or more distinct other cards in the deck.

### Deck Synergy Score

```
Deck Synergy Score = Total synergy connections across all non-land cards / Number of non-land cards
```

| Rating | Score | Assessment |
|--------|-------|------------|
| Excellent | >= 4.0 | Highly interconnected deck |
| Good | 3.0 - 3.9 | Meets synergy-first standard |
| Below threshold | 2.0 - 2.9 | Only acceptable under budget-forced relaxation |
| Poor | < 2.0 | FAIL -- too many isolated cards |

**Target**: >= 3.0 for all decks. Decks with budget-forced swaps may accept >= 2.0 with a warning.

---

## Tag Format Reference

Tags are embedded in the deck state's `synergy_tags` field for each card:

```
synergy_tags: [TRIGGERS: Blood Artist], [FEEDS: Skullclamp], [ENABLES: Cabal Coffers]
```

Rules:
- One tag per interaction per target card.
- Use the exact card name as it appears in the deck list.
- A card may have multiple tags pointing to the same target (e.g., both TRIGGERS and FEEDS the same card) -- each counts as a separate interaction.
- Tags are validated by the Optimization Reviewer against the taxonomy definitions above.
- The Rules Judge audits tag claims against oracle text (FR-03.7).
