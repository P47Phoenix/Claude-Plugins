# Price Evaluator Guide

Reference document for the Price Evaluator sub-agent. Defines the complete budget compliance evaluation process using live Scryfall pricing data via `card_lookup.py`.

---

## 1. Price Retrieval

### 1.1 Batch Pricing

Fetch prices for all 100 cards using `card_lookup.py batch-price`:

```bash
python ${SKILL_DIR}/scripts/card_lookup.py batch-price --names "<card1>" "<card2>" ... "<card75>"
python ${SKILL_DIR}/scripts/card_lookup.py batch-price --names "<card76>" ... "<card100>"
```

Split into batches of 75 cards maximum (Scryfall `/cards/collection` limit). The script returns each card's cheapest USD printing price.

### 1.2 Individual Price Lookup

For replacement card pricing during suggestion generation:

```bash
python ${SKILL_DIR}/scripts/card_lookup.py price --name "<card_name>"
```

### 1.3 Null Price Handling (Fallback Chain)

When a card has no USD price, the `card_lookup.py` script applies this fallback chain automatically:

1. **USD non-foil** (`prices.usd`) -- primary source
2. **USD foil** (`prices.usd_foil`) -- if non-foil is null
3. **Cheapest printing** -- searches other printings for any USD price
4. **"Price unavailable"** -- if all printings return null USD

Cards flagged as "price unavailable":
- Are **excluded** from the budget total
- Are **excluded** from per-card cap checks
- Are listed in `UNAVAILABLE_PRICES` in the verdict output
- Generate a warning in the final output

Do NOT estimate prices. Do NOT use non-USD currencies. If Scryfall has no USD price, the card is unavailable for budget purposes.

---

## 2. Budget Checks

### 2.1 Total Budget Check

Sum all card prices (excluding "price unavailable" cards). Compare against the user's stated budget:

```
total_cost = sum(price_usd for each card where price_usd is not null)
result = PASS if total_cost <= budget else FAIL
```

### 2.2 Per-Card Cap Check

Two modes:

| Mode | Cap Value | Source |
|------|-----------|--------|
| Explicit | User-specified amount (e.g., "no card over $10") | Intake parameter 7 (card restrictions) |
| Default | 15% of total budget | Applied when user specifies no per-card cap |

**Examples:**
- Budget $100, no explicit cap: default cap = $15.00
- Budget $200, explicit cap "no card over $10": cap = $10.00
- Budget $50, no explicit cap: default cap = $7.50

Check every card against the cap. Flag all violations.

### 2.3 Category Subtotals

Group all cards by their assigned category and calculate subtotals:

| Category | Cards Included |
|----------|---------------|
| Commander | The commander card |
| Ramp | Cards assigned to Ramp category |
| Card Draw | Cards assigned to Card Draw category |
| Removal | Cards assigned to Removal category |
| Board Wipes | Cards assigned to Board Wipes category |
| Win Conditions | Cards assigned to Win Conditions category |
| Synergy Pieces | Cards assigned to Synergy Pieces category |
| Lands | All lands (basic and non-basic) |

Report each category's subtotal and card count.

### 2.4 Most Expensive Cards

Identify the top 5 cards by price. These are the primary candidates for budget reduction if over budget.

---

## 3. Replacement Suggestions

### 3.1 When to Suggest Replacements

Suggest replacements when:
- **Over budget**: The total exceeds the stated budget
- **Over cap**: Individual cards exceed the per-card cap
- Both conditions can apply simultaneously

### 3.2 Finding Replacements

For each card needing replacement, search for budget-friendly alternatives:

```bash
python ${SKILL_DIR}/scripts/card_lookup.py search --query "oracle:<similar_effect> id:<commander_colors> legal:commander usd:<price_target>"
```

Where `<price_target>` is:
- For over-cap cards: the per-card cap value
- For over-budget cards: a target price that would bring the total under budget (distribute savings needed across the most expensive cards)

### 3.3 Synergy Preservation

Replacements must maintain deck function. For each suggested replacement:

1. Check that the replacement serves the same category role (ramp replaces ramp, draw replaces draw, etc.)
2. Check that the replacement's oracle text supports similar synergy interactions to the card being replaced
3. Report the replacement's synergy compatibility in the suggestion

### 3.4 Budget-Wins Tiebreaker

When budget and synergy conflict (the cheaper replacement has fewer interactions):

- **Budget takes priority.** This is a hard rule from FR-07.4.
- The synergy threshold relaxes from 3 interactions to **2 interactions** for budget-forced swaps.
- Cards swapped for budget reasons are tagged `[BUDGET_RELAXED]` in the deck state.
- The Optimization Reviewer will accept these cards at the relaxed threshold on re-evaluation.

### 3.5 Cost Reduction Plan

When over budget, produce a ranked swap plan:

1. Sort cards by price (highest first)
2. For each expensive card, find the cheapest functional replacement
3. Calculate savings per swap: `current_price - replacement_price`
4. Accumulate swaps until total projected cost is under budget
5. Report the plan with projected total after all swaps

Prioritize swaps that yield the highest savings with the lowest synergy impact. A $20 card with 3 interactions that can be replaced by a $2 card with 3 interactions is a better swap than a $15 card with 5 interactions replaced by a $3 card with 2 interactions.

---

## 4. Output Format

The Price Evaluator produces a structured verdict in this exact format:

```
PRICE_VERDICT: PASS|FAIL

TOTAL_COST: $<amount>
BUDGET: $<amount>
REMAINING: $<amount> (under budget) | OVER_BY: $<amount>
PER_CARD_CAP: $<amount>
CAP_VIOLATIONS: <count>
PRICE_UNAVAILABLE: <count> cards (if any)

CATEGORY_BREAKDOWN:
  Commander:       $<amount> (<count> cards)
  Ramp:            $<amount> (<count> cards)
  Card Draw:       $<amount> (<count> cards)
  Removal:         $<amount> (<count> cards)
  Board Wipes:     $<amount> (<count> cards)
  Win Conditions:  $<amount> (<count> cards)
  Synergy Pieces:  $<amount> (<count> cards)
  Lands:           $<amount> (<count> cards)

MOST_EXPENSIVE:
  1. <card_name>    $<price>
  2. <card_name>    $<price>
  3. <card_name>    $<price>
  4. <card_name>    $<price>
  5. <card_name>    $<price>

VIOLATIONS: (only present if FAIL)
  - card: <name>
    issue: <OVER_BUDGET | OVER_CAP>
    price: $<amount>
    cap: $<amount> (for cap violations)
    suggested_replacements:
      - <name> ($<price>) -- <brief note on functional similarity>
      - <name> ($<price>) -- <brief note on functional similarity>

COST_REDUCTION_PLAN: (only present if FAIL and over budget)
  Priority swaps (highest savings, lowest synergy impact):
    <card> ($<price>) -> <replacement> ($<price>)   saves $<amount>
    [... enough swaps to bring total under budget ...]
  Projected total after swaps: $<amount>

UNAVAILABLE_PRICES: (only present if any cards lack pricing)
  - <card_name> (excluded from budget calculation)
  [...]
```

### 4.1 Verdict Rules

| Condition | Verdict |
|-----------|---------|
| Total <= budget AND zero cap violations | **PASS** |
| Total > budget | **FAIL** (include COST_REDUCTION_PLAN) |
| Any card exceeds per-card cap | **FAIL** (include VIOLATIONS for each) |
| Both over budget and cap violations | **FAIL** (include both sections) |

### 4.2 PASS Output

On PASS, still include: TOTAL_COST, BUDGET, REMAINING, PER_CARD_CAP, CATEGORY_BREAKDOWN, MOST_EXPENSIVE. The user wants to see their budget utilization even when passing.

### 4.3 FAIL Output

On FAIL, include all PASS fields plus: VIOLATIONS, COST_REDUCTION_PLAN (if over budget), and UNAVAILABLE_PRICES (if applicable). Every violation must include at least one suggested replacement with price.

---

## 5. Evaluation Sequence

Execute these steps in order. No steps skipped.

1. **Parse deck state** -- Extract the 100-card list with categories and synergy tags from the input.
2. **Extract budget parameters** -- Get total budget and per-card cap (explicit or 15% default) from intake.
3. **Batch price fetch (cards 1-75)** -- Call `card_lookup.py batch-price` for the first 75 cards.
4. **Batch price fetch (cards 76-100)** -- Call `card_lookup.py batch-price` for the remaining cards.
5. **Handle null prices** -- Identify cards with no USD price after fallback chain. Flag as "price unavailable."
6. **Calculate total cost** -- Sum all available prices.
7. **Total budget check** -- Compare total against budget. Record PASS or FAIL.
8. **Per-card cap check** -- Compare each card's price against the cap. Record violations.
9. **Calculate category subtotals** -- Group prices by category, compute subtotals.
10. **Identify most expensive cards** -- Sort by price, take top 5.
11. **Generate replacement suggestions** -- For each violation (over-cap or over-budget contributor), search for budget-friendly alternatives.
12. **Build cost reduction plan** -- If over budget, rank swaps by savings-to-synergy-impact ratio. Accumulate until projected total is under budget.
13. **Tag budget-relaxed cards** -- If replacements reduce synergy below 3 interactions, tag with `[BUDGET_RELAXED]` and note the relaxed threshold of 2.
14. **Produce verdict** -- Assemble the complete output in the format above.

---

## 6. Edge Cases

### 6.1 All Cards Price Unavailable

If the majority of cards have no pricing data (e.g., Scryfall API issues), flag the entire evaluation as inconclusive:

```
PRICE_VERDICT: INCONCLUSIVE
REASON: <N> of 100 cards have no USD pricing data.
         Budget compliance cannot be determined.
         Retry when Scryfall pricing data is available.
```

### 6.2 Budget of $0 or "No Budget"

If the user specified no budget constraint, the Price Evaluator still runs but automatically passes:

```
PRICE_VERDICT: PASS (no budget constraint)
TOTAL_COST: $<amount>
```

Still produce CATEGORY_BREAKDOWN and MOST_EXPENSIVE for informational value.

### 6.3 Commander is the Most Expensive Card

The commander is a fixed slot -- it cannot be replaced for budget reasons. If the commander exceeds the per-card cap, flag it but do not suggest a replacement commander. Note in the violation:

```
- card: <commander_name>
  issue: OVER_CAP
  price: $<amount>
  cap: $<amount>
  note: Commander is a fixed slot. Consider increasing the per-card cap or budget.
```

### 6.4 Basic Lands Have No Price Impact

Basic lands (Plains, Island, Swamp, Mountain, Forest) are effectively free. Price them at $0.00 unless Scryfall returns a price, in which case use the Scryfall price. Most basic lands are under $0.25.

### 6.5 Replacement Cascade

If replacing an over-cap card with a budget-friendly alternative causes the replacement to also be over-cap (unlikely but possible with very tight caps), note it in the violation and suggest an even cheaper option.
