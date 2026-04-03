# US-07 Dev Notes: Price Evaluator Agent

**Developer**: Gimli
**Date**: 2026-04-01
**Story Points**: 4
**Status**: DONE

---

## What Was Built

### `mtg-commander/references/price-evaluator-guide.md`

The Price Evaluator's complete budget compliance evaluation process, forged from FR-05 (PRD), Architecture S4.5, and the companion reference (`api-reference.md`).

Contains 6 sections:

1. **Price Retrieval** -- Batch pricing via `card_lookup.py batch-price` (75-card splits), individual price lookups for replacements, and the null price fallback chain (USD > USD foil > cheapest printing > "unavailable"). Cards with no price are excluded from budget calculations, not estimated.

2. **Budget Checks** -- Total budget check (sum vs stated budget), per-card cap check (explicit cap or 15% of budget default), category subtotals across 8 categories (Commander, Ramp, Card Draw, Removal, Board Wipes, Win Conditions, Synergy Pieces, Lands), and top 5 most expensive cards identification.

3. **Replacement Suggestions** -- Search process for budget-friendly alternatives via `card_lookup.py search` with price-filtered queries. Synergy preservation requirements for replacements. Budget-wins tiebreaker rule: budget takes priority over synergy, threshold relaxes from 3 to 2 interactions for budget-forced swaps, affected cards tagged `[BUDGET_RELAXED]`. Cost reduction plan with swaps ranked by savings-to-synergy-impact ratio.

4. **Output Format** -- Structured verdict matching the SKILL.md template (PRICE_VERDICT, TOTAL_COST, BUDGET, REMAINING/OVER_BY, PER_CARD_CAP, CAP_VIOLATIONS, CATEGORY_BREAKDOWN, MOST_EXPENSIVE, VIOLATIONS, COST_REDUCTION_PLAN, UNAVAILABLE_PRICES). Verdict rules table for PASS/FAIL determination. PASS output still includes full budget utilization data.

5. **Evaluation Sequence** -- 14-step ordered checklist from deck state parsing through verdict production. No steps skipped.

6. **Edge Cases** -- Handling for: all cards price unavailable (INCONCLUSIVE verdict), no budget constraint (auto-PASS with informational pricing), commander as most expensive card (fixed slot, no replacement suggested), basic land pricing, replacement cascade.

### SKILL.md Updates

- Updated Agent 4 spawn instruction to include `references/price-evaluator-guide.md` as the first reference read
- Updated the reference loading table to list `price-evaluator-guide.md` for the Price Evaluator

---

## Acceptance Criteria Coverage

| AC | Criterion | Covered In |
|----|-----------|-----------|
| 7.1 | Retrieve current USD pricing via batch-price, cheapest printing | Section 1.1, 1.3 |
| 7.2 | Calculate total deck cost as sum of all 100 cards | Section 2.1 |
| 7.3 | Validate total cost does not exceed budget | Section 2.1 |
| 7.4 | Per-card cap: explicit or 15% default | Section 2.2 |
| 7.5 | Suggest 1-2 budget-friendly alternatives maintaining synergy | Section 3.2, 3.3 |
| 7.6 | Structured PASS/FAIL verdict with violations and replacements | Section 4 |
| 7.7 | Price breakdown by category | Section 2.3 |
| 7.8 | Null USD handling: fallback chain, flag as unavailable | Section 1.3 |
| 7.9 | Loads api-reference.md as reference context | SKILL.md update |

---

## Design Decisions

1. **14-step evaluation sequence**: Mirrors the Optimization Reviewer's approach. Explicit ordering prevents the agent from skipping steps or reordering in ways that produce incomplete verdicts. Parse first, fetch prices, check budgets, then suggest fixes.

2. **Savings-to-synergy-impact ratio for cost reduction**: Not all expensive cards are equal swap candidates. A $20 card with 5 synergy connections is a worse swap target than a $20 card with 3 connections. The guide makes this explicit rather than leaving it to the agent's judgment.

3. **Commander as fixed slot**: The commander cannot be budget-swapped -- it is the deck's identity. If the commander exceeds the per-card cap, that is a constraint the user must resolve at intake, not something the evaluator silently overrides. The guide documents this edge case explicitly.

4. **INCONCLUSIVE verdict for mass pricing failures**: Rather than forcing a PASS or FAIL when Scryfall data is unavailable, the guide adds a third verdict state. You cannot judge what you cannot measure. The SKILL.md orchestrator can retry or warn the user.

5. **No budget constraint handling**: Some users do not care about budget. The evaluator still runs and reports pricing for informational value, but auto-passes. No wasted correction cycles on a constraint that does not exist.

---

## Files Modified

| File | Change |
|------|--------|
| `mtg-commander/references/price-evaluator-guide.md` | Created (new file) |
| `mtg-commander/SKILL.md` | Updated Agent 4 spawn instruction and reference loading table |

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/developer/us-07-notes.md
SUMMARY: Created price-evaluator-guide.md with 14-step evaluation covering batch pricing, budget/cap checks, synergy-aware replacements, cost reduction plans. Updated SKILL.md.
```
