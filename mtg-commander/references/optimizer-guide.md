# Optimization Reviewer Evaluation Guide

Detailed evaluation process for the Optimization Reviewer sub-agent. This is the axe you swing at every decklist -- methodical, thorough, no mercy for dead weight.

**Source Requirements**: FR-04 (PRD), Architecture S4.4
**Companion References**: `synergy-taxonomy.md` (6 interaction categories), `structural-minimums.md` (category targets by power level)

---

## 1. Synergy Evaluation

The synergy-first philosophy is non-negotiable. Every non-land card must justify its slot through mechanical interactions with other cards in the deck. Reputation alone does not earn a seat at the table.

### 1.1 Count Synergy Tags

For each non-land card in the deck state:

1. Read its `synergy_tags` field.
2. Validate each tag matches one of the 6 taxonomy categories from `synergy-taxonomy.md`:
   - **TRIGGERS** -- Card A's effect causes Card B's triggered ability to fire
   - **ENABLES** -- Card A provides a resource or condition Card B specifically requires
   - **PROTECTS** -- Card A shields Card B from removal or adverse effects
   - **COMBOS-WITH** -- Cards form a defined combination producing a win condition or overwhelming advantage
   - **AMPLIFIES** -- Card A increases Card B's output by a measurable factor
   - **FEEDS** -- Card A produces tokens/resources/permanents that Card B specifically consumes
3. Discard any tag that does not match a valid category. Log discarded tags in the evaluation notes.

### 1.2 Apply Exclusion Rules

Reject interactions that violate the 3 exclusion rules from `synergy-taxonomy.md`:

| Exclusion | Rule |
|-----------|------|
| Type-Sharing Alone | Two cards sharing a creature type is NOT an interaction unless one card's text mechanically references the shared type |
| Generic Mana Enablement | Ramp producing mana that other cards spend is NOT an interaction (Sol Ring does not "enable" everything) |
| "Both Good Cards" | Two individually powerful cards with no mechanical connection do NOT interact |

**Exception**: Specific resource production consumed by a specific reference (e.g., Treasure tokens feeding Reckless Fireweaver's artifact ETB trigger) IS valid under FEEDS or TRIGGERS.

### 1.3 Flag Isolated Cards

A card is **isolated** when it has fewer than the required minimum interactions:

| Scenario | Minimum Interactions | Action |
|----------|---------------------|--------|
| Standard card | 3 interactions with distinct other cards | Flag as isolated if < 3 |
| Budget-forced swap (FR-07.4) | 2 interactions allowed | Flag as isolated if < 2; include `[BUDGET_RELAXED]` warning |

An isolated card is a replacement candidate. It does not automatically fail the deck -- but enough isolated cards will drag the synergy score below threshold.

### 1.4 Calculate Deck Synergy Score

```
Deck Synergy Score = Total valid synergy connections across all non-land cards
                     ÷ Number of non-land cards
```

| Rating | Score | Verdict |
|--------|-------|---------|
| Excellent | >= 4.0 | PASS -- Highly interconnected |
| Good | 3.0 - 3.9 | PASS -- Meets synergy-first standard |
| Below threshold | 2.0 - 2.9 | FAIL -- Only acceptable under budget-forced relaxation (FR-07.4) |
| Poor | < 2.0 | FAIL -- Too many isolated cards, deck needs significant rework |

**Target**: >= 3.0 for all decks. A score between 2.0 and 2.9 is acceptable ONLY when budget constraints forced substitutions, and only with an explicit warning in the verdict.

### 1.5 Identify Top Synergy Cards

List the 3-5 most connected cards in the deck (highest interaction count). These are the deck's backbone -- the cards that hold the strategy together. Report them in the verdict for user visibility.

---

## 2. Structural Checks

Structural minimums are hard floors. A deck that fails to meet any minimum receives a FAIL verdict, regardless of synergy score. These numbers exist because a deck without enough ramp stalls, a deck without enough draw runs dry, and a deck without enough removal loses to the first threat it cannot answer.

### 2.1 Category Minimums

Cross-reference the deck's card category counts against the targets from `structural-minimums.md` for the declared power level tier:

| Category | Casual (1-4) | Mid (5-7) | High (8-9) | cEDH (10) |
|----------|-------------|-----------|------------|-----------|
| Ramp | 10+ | 10+ | 12+ | 14+ |
| Card Draw | 10+ | 10+ | 12+ | 14+ |
| Targeted Removal | 5+ | 5+ | 7+ | 8+ |
| Board Wipes | 2+ | 2+ | 3+ | 2+ |
| Win Conditions | 3+ | 3+ | 4+ | 4+ |
| Lands | 36-40 | 35-39 | 34-38 | 28-34 |

Each card is assigned to exactly ONE category (disambiguation rule: assign to category with greatest structural deficit; if no deficit, assign by primary function relative to strategy).

For each category below minimum: report the deficit with current count vs. required count, and suggest specific cards to add using `card_lookup.py search`.

### 2.2 Mana Curve Analysis

Compute the mana curve distribution for all non-land cards across these buckets:

| Bucket | CMC Range |
|--------|-----------|
| 0-1 | Converted mana cost 0 or 1 |
| 2 | Converted mana cost 2 |
| 3 | Converted mana cost 3 |
| 4 | Converted mana cost 4 |
| 5 | Converted mana cost 5 |
| 6 | Converted mana cost 6 |
| 7+ | Converted mana cost 7 or higher |

**Curve assessment by archetype:**

| Archetype Pattern | Healthy Curve Shape | Warning Flags |
|-------------------|-------------------|---------------|
| Aggro / Voltron / Low-curve | Heavy at 1-3, light at 5+ | Top-heavy: too many 5+ CMC cards |
| Midrange / Value | Bell curve peaking at 3-4 | Front-loaded: insufficient top-end threats; Top-heavy: too slow |
| Control / Stax | Spread with interaction at 1-3, finishers at 5+ | Missing low-cost interaction |
| Combo | Low curve with combo pieces at various costs | Top-heavy: combo should be lean |
| Reanimator | Cheap enablers + expensive targets (bimodal) | All expensive with no enablers |

Calculate the **Average Mana Value (AMV)** of non-land cards. Apply adjustments from `structural-minimums.md`:

| AMV Range | Land Adjustment | Ramp Adjustment |
|-----------|----------------|-----------------|
| < 2.0 | -2 lands from recommended | No change |
| 2.0 - 2.5 | -1 land | No change |
| 2.5 - 3.5 | Baseline | Baseline |
| 3.5 - 4.0 | +1 land | +1 ramp |
| > 4.0 | +2 lands | +2 ramp |

### 2.3 Land Count Validation

Validate land count falls within the acceptable range for the power level tier (from `structural-minimums.md`). Consider the AMV adjustment above. A deck with 42 lands at power level 5 is bloated. A deck with 30 lands at power level 4 is starving.

### 2.4 Win Condition Redundancy

Verify the deck has multiple independent paths to victory. A single win condition is a single point of failure -- one Swords to Plowshares and the game plan collapses.

Check for:
- At least the minimum win condition count for the tier (3+ for casual/mid, 4+ for high/cEDH)
- Win conditions across different card types (not all creatures, not all enchantments) to resist targeted hate
- At least one win condition that does not rely on the commander (commander removal is inevitable)

### 2.5 Removal and Interaction Assessment

Validate removal is sufficient and appropriate for the declared power level:

- **Casual/Mid (1-7)**: Mix of creature and noncreature removal. At least 1 enchantment/artifact answer.
- **High (8-9)**: Instant-speed interaction preferred. Include versatile removal (Beast Within, Generous Gift, Anguished Unmaking).
- **cEDH (10)**: Maximize efficiency (0-2 CMC interaction). Counterspells for blue decks. Free spells where legal and available.

---

## 3. Replacement Suggestions

For each isolated card (below interaction threshold) or structural deficit, the Optimizer suggests specific replacements.

### 3.1 Finding Replacements for Isolated Cards

For each isolated card, search for 1-2 replacements using:

```bash
python ${SKILL_DIR}/scripts/card_lookup.py search --query "oracle:<relevant_text> id:<commander_colors> legal:commander"
```

A valid replacement must:
1. Have 3+ interactions with existing cards in the deck (evaluate against current synergy tags)
2. Fit within the deck's color identity
3. Be Commander-legal
4. Not duplicate an existing card in the deck (singleton rule)
5. Maintain or improve structural category counts

### 3.2 Filling Structural Gaps

When a category is below minimum, suggest specific cards to add:

1. Search for cards matching the deficit category and the deck's color identity
2. Prioritize cards that also contribute synergy interactions (dual-purpose fills)
3. Identify which existing cards could be swapped out (lowest synergy count in an over-filled category)

### 3.3 Budget-Aware Suggestions

When the deck is in budget-constrained mode (FR-07.4):
- Replacement suggestions should be budget-friendly alternatives
- Budget-forced cards carry a relaxed synergy threshold of 2 interactions
- Tag budget-forced cards with `[BUDGET_RELAXED]` in the verdict
- Include a warning listing which cards were accepted at reduced synergy

---

## 4. Output Format

The Optimization Reviewer produces this structured verdict:

```
OPTIMIZATION_VERDICT: PASS|FAIL

SYNERGY_SCORE: <decimal, e.g., 3.4>
ISOLATED_CARDS: <count of cards below interaction threshold>

STRUCTURAL_CHECKS:
  ramp: <N>/<min> PASS|FAIL
  card_draw: <N>/<min> PASS|FAIL
  removal: <N>/<min> PASS|FAIL
  board_wipes: <N>/<min> PASS|FAIL
  win_conditions: <N>/<min> PASS|FAIL
  lands: <N> PASS|FAIL (range: <min>-<max>)

MANA_CURVE:
  0-1: <count>
  2:   <count>
  3:   <count>
  4:   <count>
  5:   <count>
  6:   <count>
  7+:  <count>
  average_mana_value: <decimal>
  assessment: <healthy | front-loaded | top-heavy> — <explanation>

TOP_SYNERGY_CARDS:
  <card_name> — <N> interactions (<categories involved>)
  [top 3-5 most connected cards]

ISOLATED_CARD_DETAILS: (only present if isolated cards exist)
  - card: <name>
    interactions: <N>
    current_tags: [<existing tags>]
    suggested_replacements:
      - <replacement_name> (<N> interactions: <list of interactions>)
      - <replacement_name> (<N> interactions: <list of interactions>)

STRUCTURAL_VIOLATIONS: (only present if structural checks fail)
  - category: <name>
    current: <N>
    minimum: <N>
    suggested_additions: [<card names to add to reach minimum>]

BUDGET_RELAXED_CARDS: (only present if budget relaxation applied)
  - card: <name>
    interactions: <N> (threshold: 2)
    reason: budget-forced substitution
```

### Verdict Logic

- **PASS**: Zero isolated cards AND all structural minimums met AND synergy score >= 3.0
- **FAIL**: Any of the following:
  - One or more isolated cards (below interaction threshold)
  - Any structural category below minimum
  - Synergy score < 3.0 (unless budget-relaxed, in which case >= 2.0 is acceptable with warning)
  - Land count outside valid range for power level tier

---

## 5. Evaluation Sequence

Execute these steps in order. Do not skip steps.

1. **Parse deck state** -- Read all cards, their categories, synergy_tags, and metadata (power level, strategy archetype, budget constraints).
2. **Validate synergy tags** -- Check each tag against the 6 taxonomy categories. Discard invalid tags.
3. **Apply exclusion rules** -- Remove interactions that violate the 3 exclusion rules.
4. **Count interactions** -- Tally valid interactions per non-land card.
5. **Flag isolated cards** -- Mark cards below threshold (3 standard, 2 budget-relaxed).
6. **Calculate synergy score** -- Total connections / non-land card count.
7. **Identify top synergy cards** -- Find the 3-5 most connected cards.
8. **Check structural minimums** -- Compare category counts against power-level-adjusted targets.
9. **Compute mana curve** -- Distribution across CMC buckets + AMV calculation.
10. **Validate land count** -- Check against range for tier, adjusted by AMV.
11. **Assess win condition redundancy** -- Multiple paths, diverse card types.
12. **Assess removal sufficiency** -- Appropriate for power level.
13. **Generate replacement suggestions** -- For isolated cards and structural deficits.
14. **Produce verdict** -- PASS or FAIL with the structured output format above.
