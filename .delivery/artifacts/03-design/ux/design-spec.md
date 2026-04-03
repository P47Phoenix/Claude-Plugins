# UX Design Specification: MTG Commander Deck Builder Plugin

**Version**: 1.0
**Date**: 2026-04-01
**Designer**: Galadriel (UX Designer)
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Project Type**: GREENFIELD
**Scope**: Conversational UX for CLI-based multi-agent deck building pipeline

---

> *"Instead of a dark UI, you would have a design beautiful and terrible as the dawn. A conversational flow, as clear as starlight upon still water, guiding the user from a single wish — 'build me a deck' — to one hundred cards in perfect fellowship."*

---

## 1. Intake Flow (FR-02)

The intake flow is the user's first contact with the plugin. It must feel like a conversation with a knowledgeable deck builder, not a form. Seven questions, but the user should never feel interrogated.

### 1.1 Smart Extraction: Meet the User Where They Are

The plugin accepts input in three modes. The system detects which mode applies based on the user's first message.

**Mode A: Full Inline** — User provides all or most parameters in natural language.

```
User: Build me a mono-black graveyard deck with K'rrik, Son of Yawgmoth
      as commander. Power level 7, mid-power casual meta, $150 budget.
      No specific card restrictions.
```

The system extracts all 7 parameters, confirms what it found, and asks only about gaps:

```
Deck intake — extracted from your request:

  Commander:     K'rrik, Son of Yawgmoth
  Color Identity: Black (derived from commander)
  Strategy:      Graveyard recursion / reanimator
  Power Level:   7
  Meta:          Mid-power casual
  Budget:        $150
  Restrictions:  None

Validating commander against Scryfall...
Commander confirmed: K'rrik, Son of Yawgmoth (Black) — legal in Commander.

All 7 parameters resolved. Proceeding to deck construction.
```

**Mode B: Partial Inline** — User provides some parameters. The system fills what it can and asks for the rest sequentially.

```
User: Build me a mono-black deck under $100.
```

```
Deck intake — extracted from your request:

  Color Identity: Black
  Budget:        $100

I need a few more details to build your deck.

  Commander: Which commander would you like? (I can suggest options
             if you tell me your preferred strategy.)
```

After the user answers each question, the next unanswered question is presented. Questions are never bundled — one at a time, so each answer can inform the next question's context.

**Mode C: Guided** — User provides no parameters or asks for help.

```
User: Build me a Commander deck.
```

```
Let's build your deck. I'll walk you through 7 questions.

  1/7 — Color Identity
  Which colors do you want to play?
  Options: White (W), Blue (U), Black (B), Red (R), Green (G),
           or any combination. You can also name a commander and
           I'll derive the colors.
```

### 1.2 Question Sequence and Smart Defaults

The 7 questions are presented in this order. Each question has a smart default or contextual adaptation based on prior answers.

| # | Question | Smart Behavior | Default |
|---|----------|---------------|---------|
| 1 | Color identity | If user names a commander first, skip this — derive from commander | None (must specify or name commander) |
| 2 | Commander name | If color identity given, offer 3 suggestions filtered by color + strategy (if known) | None (must specify or request suggestions) |
| 3 | Strategy archetype | Infer from commander if possible (e.g., K'rrik suggests life-pay / graveyard) | Inferred from commander's typical builds |
| 4 | Power level (1-10) | Describe the scale in plain language | 6 ("focused casual — your deck has a clear plan but isn't trying to win on turn 3") |
| 5 | Meta alignment | Adapt description to power level answer | "Casual" if power <= 5, "Mid-power" if 6-7, "High-power" if 8+ |
| 6 | Total budget (USD) | Warn if budget is very low for the commander (e.g., $30 for a 4-color deck) | None (must specify) |
| 7 | Card restrictions | Prompt with examples: must-include, must-exclude, per-card cap, no infinite combos | None |

**Question 4 — Power Level Scale** (shown on first use or when user asks "what does power level mean?"):

```
Power level guide:
  1-3  Jank / theme decks — winning is secondary to the bit
  4-5  Casual — clear strategy, no fast combos, games go 8+ turns
  6-7  Focused — tuned strategy, efficient cards, games go 5-8 turns
  8-9  High power — optimized lists, fast combos possible, interaction-heavy
  10   cEDH — competitive, combo wins, stax, fast mana, free counters

Pick a number, or describe your playgroup and I'll suggest one.
```

### 1.3 Commander Recommendation Flow

When the user asks for commander suggestions instead of naming one:

```
User: I want to play blue-black but I'm not sure which commander.
      I like graveyard strategies.
```

```
Here are 3 commanders for UB Graveyard strategies:

  1. Lazav, the Multifarious — Self-mill, clone from graveyard.
     Voltron-adjacent, rewards a dense graveyard.
  2. The Scarab God — Reanimator with zombie tribal upside.
     Value-oriented, strong in longer games.
  3. Satoru Umezawa — Ninjutsu from hand, not graveyard per se,
     but synergizes with ETB/graveyard recursion shells.

Pick a number, name a different commander, or say "more" for
additional options.
```

Recommendations come from the archetype patterns reference file, not from Scryfall search. Scryfall validates the chosen commander after selection.

### 1.4 Validation at Intake

Three validations occur during intake, each with a distinct user-facing behavior:

**A. Commander Name Validation** (Scryfall lookup):

```
Validating commander against Scryfall...
Commander confirmed: Karlov of the Ghost Council (White/Black) — legal in Commander.
```

On failure:

```
Commander not found: "Karloz of the Ghost Council"

Did you mean: Karlov of the Ghost Council?
Enter the correct name or type "yes" to use the suggestion.
```

**B. Banned Commander Check**:

```
Commander banned: Golos, Tireless Pilgrim

Golos was banned in Commander (September 2021) due to its ability
to bypass color identity in deck building while providing generic
value regardless of strategy.

Please choose a different commander.
```

**C. Color Identity Cross-Check**:

When the user specifies both colors and a commander, and they conflict:

```
Note: You specified "mono-black" but Teysa Karlov's color identity
is White/Black (Orzhov).

Options:
  1. Keep Teysa Karlov — deck will be White/Black (Orzhov)
  2. Choose a different commander within mono-black

Which would you prefer?
```

The system never silently overrides the user. Conflicts are surfaced, options presented, user decides.

### 1.5 Partner Commander Rejection (FR-02.10)

```
Partner commanders are not supported in v1.

Thrasios, Triton Hero has the "Partner" keyword, which allows
pairing with a second commander. This changes deck construction
rules (98 other cards, combined color identity) in ways v1
does not yet handle.

Please choose a single commander without the Partner keyword.
```

---

## 2. Pipeline Visibility

The pipeline runs 4 agents in sequence. The user must know what is happening, how long it takes, and when they can intervene. Silence breeds anxiety; visibility breeds trust.

### 2.1 Pipeline Banner

After intake completes, the pipeline begins with a banner:

```
Pipeline started — 4 agents will process your deck.

  [1/4] Deck Builder ........... constructing 100-card list
  [2/4] Rules Judge ............ pending
  [3/4] Optimization Reviewer .. pending
  [4/4] Price Evaluator ........ pending

Estimated time: 2-4 minutes (depends on Scryfall API response times)
```

### 2.2 Agent Progress Indicators

Each agent displays a start banner, sub-step progress, and a completion banner.

**Deck Builder progress**:

```
[1/4] Deck Builder — constructing initial decklist...
  Resolving commander identity...
  Loading archetype patterns for: graveyard recursion
  Selecting ramp package (10+ sources)...
  Selecting card draw package (10+ sources)...
  Selecting removal suite...
  Selecting synergy pieces...
  Filling land base (34-40 lands)...
  Validating card names against Scryfall (batch lookup)...
  Documenting synergy rationale...

[1/4] Deck Builder — COMPLETE (100 cards constructed)
```

**Rules Judge progress**:

```
[2/4] Rules Judge — validating format legality...
  Checking card count (100)...
  Validating card names via Scryfall (batch)...
  Checking color identity compliance...
  Checking Commander banned list...
  Checking singleton rule...
  Validating format legality status...
  Auditing synergy claims...

[2/4] Rules Judge — PASS (all checks clear)
```

Or on failure:

```
[2/4] Rules Judge — FAIL (3 violations found)
  See correction cycle below.
```

**Optimization Reviewer progress**:

```
[3/4] Optimization Reviewer — evaluating synergy and structure...
  Mapping synergy interactions (6 categories)...
  Calculating per-card interaction counts...
  Checking structural minimums...
  Analyzing mana curve distribution...
  Computing deck synergy score...

[3/4] Optimization Reviewer — PASS (synergy score: 3.4, structure: valid)
```

**Price Evaluator progress**:

```
[4/4] Price Evaluator — checking budget compliance...
  Fetching prices via Scryfall (batch lookup)...
  Calculating total deck cost...
  Checking per-card price cap...
  Generating price breakdown by category...

[4/4] Price Evaluator — PASS (total: $127.43 / $150.00 budget)
```

### 2.3 User Intervention Points

The pipeline runs autonomously. The user does NOT intervene between agents. This is by design (G-05: complete pipeline in a single session without manual user intervention between agent handoffs).

**The user can intervene at exactly two points:**

1. **During intake** — the user is actively answering questions. Full control.
2. **After final output** — the user reviews the completed deck. They can approve, request changes, or re-run.

**During pipeline execution**, the user sees progress indicators but cannot modify the run. If they type during execution, the system queues their input for after completion.

### 2.4 Correction Cycle Visibility

When an agent returns FAIL, the user sees the cycle clearly:

```
[2/4] Rules Judge — FAIL (2 violations found)

  Correction cycle 1/3:
  Returning to Deck Builder with 2 violations to resolve.

  Violations:
    1. "Demonic Consultation" — Banned in Commander
       Suggested replacement: Diabolic Intent
    2. "Blak Lotus" — Card not found in Scryfall (possible typo)
       Suggested replacement: Dark Ritual

[1/4] Deck Builder — applying corrections...
  Replacing Demonic Consultation with Diabolic Intent...
  Replacing Blak Lotus with Dark Ritual...
  Verifying 100-card count maintained...

[1/4] Deck Builder — corrections applied (100 cards)

[2/4] Rules Judge — re-validating...

[2/4] Rules Judge — PASS (all checks clear)
```

The cycle counter (`1/3`) tells the user how many correction rounds remain before the pipeline outputs a best-effort result.

---

## 3. Agent Output Formats

Each agent produces structured output. The formats are designed for scannability — the user should be able to assess the deck in under 60 seconds.

### 3.1 Deck Builder Output

The Deck Builder outputs the initial decklist grouped by category, with synergy rationale for every non-land card.

```
DECK: K'rrik, Son of Yawgmoth — Graveyard Recursion
Power Level: 7 | Meta: Mid-power casual | Budget: $150

Game Plan:
  This deck leverages K'rrik's Phyrexian mana ability to cheat on
  mana costs, filling the graveyard through sacrifice and self-mill,
  then recurring threats with reanimation spells. The win condition
  is draining opponents through aristocrats triggers or assembling
  a critical mass of reanimated threats.

--- Commander (1) ---
  K'rrik, Son of Yawgmoth          {4}{B/P}{B/P}{B/P}
    Your commander. Enables life-as-mana for all black costs.

--- Ramp (12) ---
  Sol Ring                          {1}
    Accelerates into K'rrik on turn 2.
  Dark Ritual                       {B}
    Turn 1 K'rrik enabler; feeds Phyrexian mana sequences.
  Cabal Coffers                     LAND
    Generates massive black mana for reanimation spells.
  [... 9 more cards ...]

--- Card Draw (11) ---
  [cards with synergy rationale...]

--- Removal (7) ---
  [cards with synergy rationale...]

--- Board Wipes (3) ---
  [cards with synergy rationale...]

--- Win Conditions (4) ---
  [cards with synergy rationale...]

--- Synergy Pieces (28) ---
  [cards with synergy rationale...]

--- Lands (34) ---
  [land names, no rationale needed]

Total: 100 cards
```

### 3.2 Rules Judge Output

**On PASS**:

```
RULES JUDGE VERDICT: PASS

  Card count:        100/100
  Names verified:    100/100 (all found in Scryfall)
  Color identity:    100/100 within Black
  Banned cards:      0 found
  Singleton:         PASS (no illegal duplicates)
  Format legality:   100/100 legal in Commander
  Synergy claims:    Audited (0 false claims detected)
```

**On FAIL**:

```
RULES JUDGE VERDICT: FAIL — 3 violations

  Card count:        100/100
  Names verified:    98/100
  Color identity:    99/100
  Banned cards:      1 found
  Singleton:         PASS
  Format legality:   99/100

  VIOLATIONS:

  1. CARD NOT FOUND: "Blak Lotus"
     Rule: FR-03.2 — Every card name must exist in Scryfall
     Likely issue: Typo (did you mean "Black Lotus"?)
     Note: Black Lotus is banned — see violation #3 if corrected
     Suggested replacement: Dark Ritual

  2. COLOR IDENTITY: Cyclonic Rift (Blue)
     Rule: FR-03.3 — All cards must be within commander's color identity
     Commander identity: Black only
     Suggested replacement: Damnation

  3. BANNED: Demonic Consultation
     Rule: FR-03.4 — Card appears on Commander banned list
     Suggested replacement: Diabolic Intent
```

### 3.3 Optimization Reviewer Output

**On PASS**:

```
OPTIMIZATION REVIEWER VERDICT: PASS

  Synergy Score: 3.4 (target: >= 3.0)
  Isolated Cards: 0

  Structural Minimums:
    Ramp:        12/10  PASS
    Card Draw:   11/10  PASS
    Removal:      7/5   PASS
    Board Wipes:  3/2   PASS
    Win Conditions: 4/3 PASS
    Lands:       34     PASS (range: 34-40)

  Mana Curve:
    0-1: ████████ 12
    2:   ██████████████ 18
    3:   ████████████ 15
    4:   ████████ 10
    5:   ████ 5
    6:   ███ 3
    7+:  ██ 3
    Curve assessment: Healthy — front-loaded, appropriate for
    power 7 with K'rrik's cost reduction.

  Top Synergy Connections:
    Blood Artist        — 8 interactions (Triggers, Feeds)
    Viscera Seer        — 7 interactions (Enables, Feeds)
    Gray Merchant        — 6 interactions (Triggers, Amplifies)
```

**On FAIL** (isolated cards found):

```
OPTIMIZATION REVIEWER VERDICT: FAIL — 2 isolated cards

  Synergy Score: 2.7 (target: >= 3.0)
  Isolated Cards: 2

  ISOLATED CARDS (fewer than 3 interactions):

  1. Phyrexian Arena — 2 interactions
     Interacts with: K'rrik (Enables: life payment), Vilis (Triggers: life loss)
     Missing: No Feeds, Amplifies, or Combos-with connections
     Suggested replacements:
       - Necropotence (5 interactions: K'rrik, Vilis, Bolas's Citadel,
         Peer into the Abyss, Skirge Familiar)
       - Sign in Blood (4 interactions: K'rrik, Vilis, Magus of the Will,
         Sanguine Bond)

  2. Burnished Hart — 1 interaction
     Interacts with: Nim Deathmantle (Triggers: creature death)
     Suggested replacements:
       - Soldevi Adnate (4 interactions: K'rrik, Reassembling Skeleton,
         Nim Deathmantle, Pitiless Plunderer)
       - Wayfarer's Bauble (3 interactions: K'rrik, Crucible of Worlds,
         Rings of Brighthearth)
```

### 3.4 Price Evaluator Output

**On PASS**:

```
PRICE EVALUATOR VERDICT: PASS

  Total Cost:   $127.43 / $150.00 budget
  Remaining:    $22.57 under budget
  Per-Card Cap: $22.50 (15% of $150) — no violations

  Price Breakdown by Category:
    Commander:      $12.99
    Ramp:           $18.74
    Card Draw:      $14.22
    Removal:         $9.87
    Board Wipes:     $8.45
    Win Conditions: $11.33
    Synergy Pieces: $38.91
    Lands:          $12.92

  Most Expensive Cards:
    1. K'rrik, Son of Yawgmoth    $12.99
    2. Bolas's Citadel             $8.47
    3. Necropotence                $7.22
```

**On FAIL**:

```
PRICE EVALUATOR VERDICT: FAIL — over budget

  Total Cost:   $183.27 / $150.00 budget
  Over by:      $33.27

  Per-Card Cap: $22.50 (15% of $150)
  Cap Violations: 1

  BUDGET VIOLATIONS:

  1. OVER CAP: Vampiric Tutor — $34.99 (cap: $22.50)
     Budget-friendly alternatives:
       - Diabolic Tutor ($0.25) — same effect, 4 mana instead of 1
       - Beseech the Mirror ($3.49) — bargain cost, flexible tutor

  COST REDUCTION SUGGESTIONS (to bring total under $150):

  Priority replacements (highest savings, lowest synergy impact):
    Vampiric Tutor ($34.99) -> Diabolic Tutor ($0.25)     saves $34.74
    Cabal Coffers ($18.99) -> Cabal Stronghold ($1.49)     saves $17.50

  With these 2 swaps: new total = $130.78 (under budget)
```

---

## 4. Correction Cycle UX

When agents find problems, the pipeline self-corrects. The user must understand what happened, what changed, and why.

### 4.1 Rules Judge Correction

The user sees violations, corrections, and re-validation as a continuous narrative:

```
[2/4] Rules Judge — FAIL (2 violations)
  Correction cycle 1/3 — returning to Deck Builder

  Violations passed to Deck Builder:
    1. "Primeval Titan" — Banned in Commander
    2. "Selvala, Heart of Wilds" — Color identity Green (deck is mono-black)

[1/4] Deck Builder — applying corrections...
  Swapping Primeval Titan -> Burnished Hart (ramp, mono-black legal)
  Swapping Selvala -> Erebos, God of the Dead (card draw, mono-black)
  Card count verified: 100/100

[2/4] Rules Judge — re-validating...
[2/4] Rules Judge — PASS
```

### 4.2 Budget-Wins Tiebreaker UX

When the Price Evaluator fails and budget-forced swaps reduce synergy, the user sees the tradeoff explicitly:

```
[4/4] Price Evaluator — FAIL (over budget by $47.82)
  Correction cycle 1/3 — returning to Deck Builder

  Budget-priority swaps (synergy may decrease):
    Vampiric Tutor ($34.99) -> Diabolic Tutor ($0.25)
      Synergy impact: 5 interactions -> 3 interactions
      Note: Budget constraint forced this swap. Synergy threshold
      relaxed from 3 to 2 for this card.

    Cabal Coffers ($18.99) -> Cabal Stronghold ($1.49)
      Synergy impact: 4 interactions -> 2 interactions
      Note: Budget constraint forced this swap. Synergy threshold
      relaxed from 3 to 2 for this card.

  New total: $131.46 / $150.00 budget

[3/4] Optimization Reviewer — re-evaluating synergy...
  Synergy score: 3.1 (was 3.4 — 2 cards at reduced threshold)
  Budget-relaxed cards: Diabolic Tutor (2), Cabal Stronghold (2)
[3/4] Optimization Reviewer — PASS (budget-relaxed threshold applied)

[4/4] Price Evaluator — re-validating...
[4/4] Price Evaluator — PASS ($131.46 / $150.00)
```

### 4.3 Max Cycles Exhausted

When all correction cycles are used and violations remain:

```
Correction cycles exhausted (3/3). Outputting best-effort deck.

  REMAINING WARNINGS:
    1. Synergy: Burnished Hart has 1 interaction (threshold: 3,
       budget-relaxed threshold: 2). No budget-compliant replacement
       with 2+ interactions was found.
    2. Budget: Total cost is $152.18 ($2.18 over $150 budget).
       All high-cost cards have been replaced with cheapest alternatives.

  The deck below is the best result achievable within 3 correction
  cycles. Consider adjusting your budget or strategy to resolve
  remaining warnings.
```

---

## 5. Final Output

The final output is the culmination of the pipeline. It must be comprehensive enough to use immediately and scannable enough to evaluate in under 2 minutes.

### 5.1 Summary Card

The deck opens with a summary card — the "at a glance" view:

```
==============================================================
  MTG COMMANDER DECK: K'rrik, Son of Yawgmoth
  Strategy:    Graveyard Recursion / Reanimator
  Colors:      Black
  Power Level: 7 (Focused)
  Total Cost:  $127.43 / $150.00 budget
  Synergy:     3.4 average interactions per card
  Cards:       100 (1 commander + 99)
==============================================================
```

### 5.2 Complete Deck Presentation

After the summary card, the full categorized deck list with synergy notes (same format as Section 3.1, but now with pricing for each card):

```
--- Commander (1) --- Total: $12.99
  K'rrik, Son of Yawgmoth  {4}{B/P}{B/P}{B/P}  $12.99
    Your commander. Enables life-as-mana for all black costs.

--- Ramp (12) --- Total: $18.74
  Sol Ring               {1}        $2.49
    Accelerates into K'rrik on turn 2.
  Dark Ritual            {B}        $1.29
    Turn 1 K'rrik enabler; feeds Phyrexian mana sequences.
  [... continued ...]

[... all categories ...]
```

### 5.3 Agent Verdicts (Transparency Section)

After the deck list, a condensed view of all agent verdicts:

```
--- Pipeline Results ---

  Deck Builder:          100 cards constructed
  Rules Judge:           PASS (all checks clear)
  Optimization Reviewer: PASS (synergy: 3.4, structure: valid)
  Price Evaluator:       PASS ($127.43 / $150.00)
  Correction Cycles:     0 used (max: 3)
```

If any warnings exist (budget-relaxed cards, best-effort output), they appear here:

```
  Warnings:
    - 2 cards included at reduced synergy threshold (budget priority):
      Diabolic Tutor (2 interactions), Cabal Stronghold (2 interactions)
```

### 5.4 Export-Ready Card List

A clean, copy-paste-ready list for deck building tools (Moxfield, Archidekt, MTGO, etc.):

```
--- Export List (copy-paste ready) ---

1 K'rrik, Son of Yawgmoth
1 Sol Ring
1 Dark Ritual
1 Cabal Coffers
1 Wayfarer's Bauble
1 Arcane Signet
[... all 100 cards, one per line ...]
1 Swamp
1 Swamp
1 Swamp
[... basic lands with quantity ...]
```

For basic lands, the export format uses quantity notation:

```
24 Swamp
```

### 5.5 Purchase Summary

A compact section linking the user to pricing sources:

```
--- Purchase Info ---

  Total deck cost: $127.43 (cheapest printings via Scryfall)
  Pricing source:  Scryfall (aggregated market data)
  Prices as of:    2026-04-01

  Most expensive cards:
    K'rrik, Son of Yawgmoth    $12.99
    Bolas's Citadel             $8.47
    Necropotence                $7.22

  Note: Prices reflect cheapest available printing. Actual costs
  may vary by retailer and card condition. Search for cards on
  your preferred retailer to purchase.
```

### 5.6 Post-Output User Actions

After the final output, the user can:

```
What would you like to do?

  "approve"   — Save this deck (no further changes)
  "swap X Y"  — Replace card X with card Y (re-runs validation)
  "rerun"     — Start the pipeline over with the same intake answers
  "adjust"    — Change intake parameters (budget, power level, etc.)
               and rebuild
```

**"swap" flow**: The user names a card to remove and a card to add. The system validates the new card (Scryfall lookup, color identity, banned list, price) and re-runs the Optimization Reviewer to check synergy impact:

```
User: swap Burnished Hart with Soldevi Adnate

Validating Soldevi Adnate...
  Scryfall: Found
  Color identity: Black — within commander identity
  Banned: No
  Price: $0.35

Swap applied. Re-checking synergy...
  Soldevi Adnate: 4 interactions (was Burnished Hart: 1 interaction)
  Deck synergy score: 3.5 (was 3.4)
  New total cost: $127.08 (was $127.43)

Swap complete. Updated deck reflects this change.
```

---

## 6. Error Handling

Errors must be informative, never cryptic. The user should always know what went wrong, whether they can fix it, and what to try next.

### 6.1 Scryfall API Failures

**Timeout / 5xx errors**:

```
Scryfall API is not responding (timeout after 10 seconds).
Retrying... (attempt 2/3)

[If all retries fail:]
Scryfall API is currently unavailable. The deck builder requires
Scryfall for card data and pricing.

Options:
  - Wait a few minutes and try again ("rerun")
  - Check Scryfall status: https://status.scryfall.com
```

**Rate limiting (429)**:

```
Scryfall rate limit reached. Backing off for 2 seconds...
Resuming card lookups...
```

This is informational only. The user does not need to act. The Card Finder handles retry automatically. The message appears so the user understands a brief pause.

### 6.2 Impossible Budget Constraints

When the budget is too low to build a functional deck:

```
Budget concern: $30 may be too tight for a 4-color Commander deck.

A 4-color mana base alone typically costs $15-40 (even with all
budget lands). This leaves $0-15 for 60+ non-land cards.

Options:
  1. Proceed anyway — I'll build the best deck possible at $30,
     but synergy scores may be low and the mana base will be
     all basics + budget taplands.
  2. Increase budget — $50-75 opens significantly more options
     for 4-color builds.
  3. Reduce colors — mono-color and 2-color decks work well
     at $30 budgets.

What would you prefer?
```

This warning fires during intake (before pipeline execution), not after the Price Evaluator fails. Prevention is better than correction.

### 6.3 No Valid Commander

When the user requests a strategy or color combination with no matching commander suggestions:

```
I couldn't find a commander matching "5-color mill" in my
archetype patterns.

This could mean:
  - The strategy doesn't have well-established commanders in
    these colors
  - The strategy exists but under a different name

Try:
  - Name a specific commander you have in mind
  - Broaden the color identity (e.g., "blue mill" or "blue-black mill")
  - Describe the play pattern you want ("I want to put cards from
    opponents' libraries into their graveyards")
```

### 6.4 Invalid Card in Must-Include List

When the user's card restrictions reference a card that does not exist or is illegal:

```
Card restriction issue: "Blak Lotus" (must-include)

  "Blak Lotus" was not found in Scryfall.

  Did you mean:
    - Black Lotus (banned in Commander — cannot include)
    - Gilded Lotus (legal, {5} artifact, produces 3 mana)

  Please correct the card name or remove it from restrictions.
```

---

## 7. Conversational Tone and Personality

The plugin speaks in a knowledgeable but approachable voice. It is an experienced deck builder sitting across the table from you at the LGS, not a search engine.

### 7.1 Tone Guidelines

| Situation | Tone | Example |
|-----------|------|---------|
| Intake questions | Conversational, helpful | "Which colors do you want to play?" not "Specify color identity parameter." |
| Validation success | Confident, brief | "Commander confirmed." not "Validation complete: status SUCCESS." |
| Validation failure | Clear, constructive | "Card not found — did you mean...?" not "ERROR: Card lookup returned null." |
| Synergy rationale | Technical but readable | "Triggers Blood Artist on each sacrifice" not "Synergy: triggers" |
| Budget concerns | Honest, option-giving | "This budget is tight for 4 colors. Here are your options..." |
| Pipeline progress | Informative, calm | "Checking color identity compliance..." not "EXECUTING RULE FR-03.3..." |

### 7.2 What NOT to Display

- Internal agent names (the user sees "Deck Builder" not "Agent 1" or "deck-builder.md")
- FR/AC numbers from the PRD (those are internal)
- Raw Scryfall API responses
- Pipeline config values (max_self_correction, max_dod_rounds)
- Internal synergy taxonomy category names in isolation (show them only in context: "5 interactions (Triggers, Feeds)")

---

## 8. Accessibility and Scannability

### 8.1 Visual Hierarchy in CLI

The design uses ASCII-safe formatting for maximum terminal compatibility:

| Element | Format | Purpose |
|---------|--------|---------|
| Section headers | `--- Category (count) ---` | Separates deck categories |
| Summary card | `===` border | Highlights the at-a-glance view |
| Progress steps | `[n/4]` prefix | Shows pipeline position |
| Verdicts | `PASS` / `FAIL` in caps | Instant scan for status |
| Mana costs | `{1}{B}{B}` notation | Standard MTG shorthand |
| Price | Right-aligned `$X.XX` | Quick cost scanning |
| Correction cycles | `Correction cycle n/3` | Shows remaining attempts |
| Warnings | `REMAINING WARNINGS:` block | Grouped at end, not scattered |

### 8.2 Information Density

Each output section answers one question:

| Section | Question It Answers |
|---------|-------------------|
| Summary card | "What is this deck?" |
| Categorized list | "What's in it and why?" |
| Pipeline results | "Did it pass all checks?" |
| Export list | "How do I build this on Moxfield?" |
| Purchase info | "How much does it cost?" |

The user reads top-to-bottom and gets progressively more detail. Summary first, specifics second, export last.

---

*"The quest stands upon the edge of a knife. Stray but a little — a hallucinated card name, a color identity violation, a budget transgression — and it will fail, to the ruin of game night. But hope remains, while the pipeline is true. Go now, and build with the light of Earendil upon your mana base."*

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/03-design/ux/design-spec.md
SUMMARY: UX design spec for MTG Commander deck builder: smart intake (3 modes), pipeline visibility with agent progress, structured output formats, correction cycle UX, error handling, post-output actions.
```
