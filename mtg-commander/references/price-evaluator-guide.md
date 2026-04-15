# Price Evaluator Guide

Reference document for the Price Evaluator sub-agent. Defines the complete budget compliance evaluation process using live Scryfall pricing data via `card_lookup.py`.

> To author the `.mtg-commander.yml` knobs this guide references (soft goal, escalation, budget_source), see [`config-walkthrough.md`](config-walkthrough.md).

---

## 1. Price Retrieval

### 1.1 Batch Pricing (TCGPlayer via Scryfall)

Fetch TCGPlayer prices for all 100 cards using `card_lookup.py batch-price`:

```bash
python ${SKILL_DIR}/scripts/card_lookup.py batch-price --names "<card1>" "<card2>" ... "<card75>"
python ${SKILL_DIR}/scripts/card_lookup.py batch-price --names "<card76>" ... "<card100>"
```

Split into batches of 75 cards maximum (Scryfall `/cards/collection` limit). The script returns each card's cheapest USD printing price.

### 1.1b Batch Pricing (Card Kingdom via Archidekt)

After TCGPlayer pricing, fetch Card Kingdom prices for the same cards:

```bash
python ${SKILL_DIR}/scripts/card_lookup.py ck-batch-price --names "<card1>" "<card2>" ... "<card100>"
```

No batch size limit (individual Archidekt API calls with 100ms delay between each). Returns both CK and TCG prices per card, plus Card Kingdom purchase links.

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

Sum all card prices (excluding "price unavailable" cards). Calculate BOTH vendor totals. The budget check uses the HIGHER of the two totals (conservative approach):

```
total_tcg = sum(price_usd for each card where price_usd is not null)
total_ck  = sum(price_ck for each card where price_ck is not null)
total_cost = max(total_tcg, total_ck)
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

TOTAL_COST: TCGPlayer: $<amount> | Card Kingdom: $<amount>
BUDGET_CHECK_PRICE: $<amount> (higher of TCG/CK — conservative)
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

PRICING_NOTE:
  TCGPlayer prices via Scryfall API. Card Kingdom prices via Archidekt API.
  Prices as of <current_date>. Budget check uses the higher vendor total.
  Verify final prices at your preferred vendor before purchasing.
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
5. **Card Kingdom price fetch** -- Call `card_lookup.py ck-batch-price` for all 100 cards. Merge CK prices into the card data.
6. **Handle null prices** -- Identify cards with no USD price after fallback chain. Flag as "price unavailable."
7. **Calculate total cost** -- Sum TCGPlayer total and Card Kingdom total separately.
8. **Total budget check** -- Compare the HIGHER of TCG/CK totals against budget. Record PASS or FAIL.
9. **Per-card cap check** -- Compare each card's price (higher of TCG/CK) against the cap. Record violations.
10. **Calculate category subtotals** -- Group prices by category, compute subtotals.
11. **Identify most expensive cards** -- Sort by price (higher of TCG/CK), take top 5.
12. **Generate replacement suggestions** -- For each violation (over-cap or over-budget contributor), search for budget-friendly alternatives.
13. **Build cost reduction plan** -- If over budget, rank swaps by savings-to-synergy-impact ratio. Accumulate until projected total is under budget.
14. **Tag budget-relaxed cards** -- If replacements reduce synergy below 3 interactions, tag with `[BUDGET_RELAXED]` and note the relaxed threshold of 2.
15. **Produce verdict** -- Assemble the complete output in the format above.

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

---

## 7. Per-Card Price Goal (Soft Goal)

When `.mtg-commander.yml` sets `price_rules.max_card_price` to a non-null value, the Price Evaluator applies a soft per-card goal in addition to the hard 15% cap.

### 7.1 Evaluation

After completing all budget checks (Section 5 steps 1-15), scan every card against the soft goal. The price used depends on `price_rules.budget_source`:
- `higher` — use the higher of TCG/CK price per card (default)
- `tcgplayer` — use TCGPlayer price only
- `cardkingdom` — use Card Kingdom price only

### 7.2 Substitution-First Logic

For each card exceeding the soft goal:
1. Search for a replacement that is (a) under the goal, (b) synergy-preserving (same category role, >= 3 interactions or >= 2 for BUDGET_RELAXED), and (c) format-legal within the commander's color identity.
2. If a valid substitute is found, suggest the swap in the verdict output.
3. If no valid substitute exists, the card is flagged for escalation.

### 7.3 Escalation (when `price_rules.escalation: true`)

Unsubstitutable over-goal cards are grouped into a BLOCKING escalation prompt. The pipeline halts until the user responds. See SKILL.md > Agent 4 > Step 5b for the full escalation message format and user options (accept/raise/force-swap).

### 7.4 Silent Mode (when `price_rules.escalation: false`)

Auto-substitute via budget-wins logic. If no substitute exists, include the card silently with a metadata tag `[OVER_GOAL: $<price>/$<goal>]`. No user prompt. No pipeline halt.

---

## 8. Card Kingdom Divergence Check (DEFECT-002 Fix)

The Price Evaluator fetches both TCGPlayer and Card Kingdom prices. After pricing is complete, apply divergence checks to detect single-vendor pricing blind spots.

### 8.1 Per-Card Divergence

For each card, compare TCG and CK prices. If divergence exceeds 30%:

```
divergence = abs(tcg_price - ck_price) / min(tcg_price, ck_price)
if divergence > 0.30: flag card
```

Flagged cards are listed in the verdict output:

```
CK_DIVERGENCE_FLAGS:
  - card: <name>
    tcg_price: $<amount>
    ck_price: $<amount>
    divergence: <percentage>%
    note: <brief explanation, e.g., "CK has this card in stock at premium" or "TCG has low-grade copies">
```

### 8.2 Total Divergence Escalation

If the total CK cost diverges more than 20% from the total TCG cost:

```
total_divergence = abs(total_tcg - total_ck) / min(total_tcg, total_ck)
if total_divergence > 0.20: escalate to user
```

Escalation message:

```
VENDOR PRICE DIVERGENCE — user decision required

Total deck cost varies significantly between vendors:
  TCGPlayer:    $<tcg_total>
  Card Kingdom: $<ck_total>
  Divergence:   <percentage>%

Which vendor would you like to optimize for?
  (a) TCGPlayer — optimize swaps against TCG prices
  (b) Card Kingdom — optimize swaps against CK prices
  (c) Keep current (higher of two) — conservative approach, no change
```

The user's choice updates `budget_source` for the remainder of this pipeline run (does not persist to config file).

### 8.3 `budget_source` Config Key

The `price_rules.budget_source` key in `.mtg-commander.yml` controls which vendor total is used for the budget check:
- `higher` (default) — `max(total_tcg, total_ck)` — most conservative
- `tcgplayer` — use TCGPlayer total only
- `cardkingdom` — use Card Kingdom total only

This key also determines which per-card price is used for the soft goal check and per-card cap check.

---

## 9. Challenger Verification

After the Price Evaluator primary completes, a **Price Challenger** agent independently re-verifies pricing. The Challenger fetches Card Kingdom prices via `ck-batch-price` in a separate Agent spawn (clean context) and:

1. Flags per-card divergence > 30% between TCG and CK prices
2. Flags total cost divergence > 20% between vendors
3. Checks per-card price goal violations if `price_rules.max_card_price` is set
4. Attempts substitution suggestions for flagged cards before escalating

If the Challenger finds pricing issues the primary missed (e.g., stale TCG prices, miscalculated totals), a CHALLENGE verdict triggers the adversarial loop (see SKILL.md > Adversarial Loop Protocol). A fresh Price Evaluator primary is spawned with the Challenger's findings.

This independent verification ensures single-vendor blind spots are caught even if the primary agent's CK fetch was incomplete or contained calculation errors.
