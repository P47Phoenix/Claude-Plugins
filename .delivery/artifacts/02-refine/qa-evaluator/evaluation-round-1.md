# Gate 2 Evaluation: MTG Commander Deck Builder Plugin

**Evaluator**: Legolas, QA Engineer
**Date**: 2026-04-01
**PRD Version**: 1.0
**Round**: 1

---

## BLOCKING Criteria

### B1: All requirements are testable

**Verdict: PASS**

All 7 FRs (FR-01 through FR-07) and 7 NFRs (NFR-01 through NFR-07) have explicit, verifiable acceptance criteria. Each AC maps to a concrete verification method:

- **FR-01** (Plugin Structure): File existence checks (`ls mtg-commander/SKILL.md`, `ls mtg-commander/LICENSE.txt`), JSON key lookup in `marketplace.json`, `plugin-validator` execution with zero-error exit code.
- **FR-02** (Deck Builder): Count intake questions presented (7), verify Scryfall API call on commander name input, count output cards (exactly 100), verify category assignments sum to 100, verify synergy rationale present for each non-land card.
- **FR-03** (Rules Judge): Every AC is a deterministic check against Scryfall API data -- card existence, color identity subset, banned list membership, singleton rule, format legality. Verdict output is structured (PASS/FAIL). All verifiable programmatically.
- **FR-04** (Optimization Reviewer): Numeric thresholds (10+ ramp, 10+ draw, 5+ removal, 2+ board wipes, 3+ win conditions, 34-40 lands). Synergy interaction count per card. Synergy score formula defined. All measurable.
- **FR-05** (Price Evaluator): USD values from Scryfall, arithmetic sum, comparison against budget ceiling, per-card cap calculation (15% of total). All numeric and verifiable.
- **FR-06** (Card Finder): API endpoint verification, response schema validation, rate limit timing measurement, error code handling (404, 422, 429). File existence check for `scripts/card_lookup.py`. Import check for `urllib` only.
- **FR-07** (Orchestration): Agent execution sequence observable in output. Correction cycle count against `pipeline.max_self_correction`. Final output format verification (sections present, export-ready list format).

Every AC can have a test written for it. No criterion relies on subjective judgment alone.

---

### B2: Acceptance criteria are specific and measurable (no "either...or")

**Verdict: NOT PASS -- 2 blocking issues found**

I scanned all 44 acceptance criteria across FR-01 through FR-07 and 7 NFRs for branching language, ambiguity, and unmeasurable phrasing.

**Blocking Issue 1: FR-02.1 -- Test Case 1 commander is "either...or"**

The PRD's AC FR-02.1 itself is clean, but Test Case 1 in Section 8 specifies:

> Commander: Sheoldred, the Apocalypse (or K'rrik, Son of Yawgmoth -- builder's choice based on archetype fit)

This is an "either...or" in the test specification. A test case must have a single, deterministic expected input. "Builder's choice" means the test is not repeatable -- different runs may use different commanders, producing fundamentally different decklists with different color identities, synergy patterns, and price profiles. The pass criteria cannot be consistently evaluated.

**Fix required**: Pick one commander. If both are valuable test scenarios, split into two test cases (3a and 3b) or make one the primary and the other an optional stretch test.

**Blocking Issue 2: FR-02.6 -- category assignment has overlapping definitions**

FR-02.6 states: "Every card is assigned to exactly one category." The categories include Ramp (10+), Card Draw (10+), and Synergy Pieces (remaining). Many Commander staples serve dual roles -- e.g., Solemn Simulacrum is both ramp and card draw; Phyrexian Arena is card draw but also a synergy piece in lifegain decks. The PRD does not define how dual-purpose cards are categorized.

This matters because the structural minimums in FR-04.3 count cards per category. If a dual-purpose card is placed in "Synergy Pieces," the ramp or draw count may fall below the 10-card minimum, triggering a false FAIL. If placed in "Ramp," the card draw count suffers. The assignment rule is untestable without a disambiguation criterion.

**Fix required**: Add a prioritization rule for dual-purpose cards. For example: "When a card serves multiple category functions, it is assigned to the category with the fewest cards above its structural minimum. Ties are broken by primary function (the function most relevant to the deck's strategy archetype)."

---

### B3: Success metrics have baselines and targets

**Verdict: NOT PASS -- no baselines or metrics table**

The PRD has a Goals table (Section 2) with 6 goals (G-01 through G-06). Each goal has a "Success Measure" column. However:

1. **No baselines.** This is a GREENFIELD plugin -- there is no existing system to measure against. The PRD should still define baselines, even if they are "0" or "N/A (new capability)." Without explicit baselines, there is no way to demonstrate improvement or validate that the plugin delivers new value versus the null state.

2. **No numeric targets in goals.** The success measures are restatements of the requirements, not independently measurable metrics. For example:
   - G-02: "Every non-land card interacts meaningfully with 3+ other cards" -- this is the requirement itself (FR-04.2), not a success metric with a target. A proper metric would be: "Baseline: 0 decks built. Target: 3/3 dogfooding test cases produce decks with synergy score >= 3.0."
   - G-05: "User provides intake answers, receives finished decklist. No manual intermediate steps." -- this is a feature description, not a metric. A proper metric would be: "Baseline: N/A. Target: 100% of pipeline runs complete without user intervention between agents."

3. **No measurement methodology.** The goals do not specify HOW each success measure is verified. The test cases in Section 8 partially fill this gap, but they are not linked to the goals table.

**Fix required**: Add a proper metrics table with columns: Goal ID, Metric, Baseline, Target, Measurement Method. The 3 dogfooding test cases provide excellent raw material -- link them to goals explicitly.

---

### B4: Edge cases identified

**Verdict: WARNING -- significant gaps**

The PRD identifies risks in Section 11 (Dependencies) but does not have a dedicated edge cases or risks section for functional behavior. The Open Questions (Section 10) surface 5 good design-level questions but are positioned as deferred, not as identified edge cases.

**Missing edge cases I would test:**

1. **Commander with partner/companion/background ability**: OQ-5 asks whether partner commanders are supported, but the PRD does not define behavior when a user inputs a partner commander. Does the pipeline reject it? Silently treat it as a solo commander? This is a runtime edge case, not just a design question. If a user inputs "Thrasios, Triton Hero" (a partner commander), the Deck Builder must handle it -- reject with a clear message or support it. Neither behavior is specified.

2. **Scryfall API returns no price data**: FR-05.1 assumes Scryfall always has USD pricing. Some cards (especially new releases, promos, or digital-only printings) have null price fields in Scryfall. The Price Evaluator has no AC for handling cards with missing price data. Does it skip the card? Use $0? Fail the evaluation? This directly impacts budget calculations.

3. **Commander is on the banned list**: The Rules Judge (FR-03.4) checks for banned cards, but the intake flow (FR-02.3) only validates that the commander name exists in Scryfall. A user could input a banned commander (e.g., Golos, Tireless Pilgrim). The Deck Builder would build an entire 100-card list before the Rules Judge catches the illegal commander. This wastes a full pipeline cycle. The intake should validate ban status upfront.

4. **Budget too low for any viable deck**: What happens when a user specifies a $10 budget? The Price Evaluator will FAIL, suggest replacements, and the Deck Builder will attempt corrections -- but basic lands and the commander alone may exceed $10 for some commanders. No AC defines a minimum viable budget or a "budget infeasible" early exit.

5. **Card Finder returns no results**: FR-06.3 supports "budget replacement" queries. What if no functionally similar card exists under the price ceiling? FR-06 has no AC for empty result sets. The Price Evaluator (FR-05.5) and Optimization Reviewer (FR-04.6) both depend on Card Finder suggestions. If Card Finder returns nothing, these agents have no defined fallback behavior.

6. **Scryfall API down (extended outage)**: NFR-05 acknowledges internet is required and Section 11 notes "Scryfall downtime blocks deck building." But no AC defines user-facing behavior -- does the pipeline hang? Timeout? Display an error? The Card Finder (FR-06.5) handles individual request errors but not "API unreachable" as a distinct state.

7. **100-card count after correction cycles**: FR-07.2 cycles back to the Deck Builder when an agent fails. If the Rules Judge flags 5 illegal cards for removal, the Deck Builder must replace them while maintaining exactly 100 cards. No AC explicitly requires that replacement operations preserve the 100-card count invariant during corrections (FR-02.5 only governs initial output).

8. **Duplicate basic lands and singleton rule interaction**: FR-03.5 states "no duplicate card names except basic lands." Commander decks commonly run snow-covered basics (Snow-Covered Island, etc.) and Wastes. Are these considered "basic lands" for the singleton exception? The Scryfall type line distinguishes "Basic Snow Land" from "Basic Land." The boundary of the exception is undefined.

**Recommendation**: Edge cases 2, 3, 5, and 7 should be addressed before Plan stage -- they represent runtime failures with no defined behavior. Edge cases 1, 4, 6, and 8 can be addressed during Design/Architect.

---

## BLOCKING Summary

| # | Criterion | Verdict |
|---|-----------|---------|
| B1 | All requirements are testable | **PASS** |
| B2 | Acceptance criteria are specific and measurable | **NOT PASS** -- 2 issues (either/or in test case, dual-purpose card categorization undefined) |
| B3 | Success metrics have baselines and targets | **NOT PASS** -- no baselines, no numeric targets, no measurement methodology |

## WARNING Summary

| # | Criterion | Verdict |
|---|-----------|---------|
| W1 | Edge cases identified | **WARNING** -- 8 functional edge cases not covered; 4 should be addressed before Plan |

---

## Detailed Findings

### Finding 1: Test Case 1 uses "either...or" commander selection [BLOCKING]

**Severity**: Blocking
**Location**: Section 8, Test Case 1
**Issue**: "Sheoldred, the Apocalypse (or K'rrik, Son of Yawgmoth -- builder's choice based on archetype fit)" introduces non-deterministic test input. These are different commanders with different oracle text, different synergy profiles, and different price points. A test case must have fixed inputs to be repeatable.
**Fix**: Choose one commander for Test Case 1. If both are valuable, create Test Case 1a (Sheoldred) and Test Case 1b (K'rrik).

### Finding 2: Dual-purpose card categorization rule missing [BLOCKING]

**Severity**: Blocking
**Location**: FR-02.6, FR-04.3
**Issue**: FR-02.6 requires every card in exactly one category. FR-04.3 validates structural minimums by category count. Many Commander staples serve dual roles (e.g., Solemn Simulacrum = ramp + draw, Swords to Plowshares = removal + lifegain synergy). Without a categorization disambiguation rule, the Deck Builder's assignment is arbitrary, and the Optimization Reviewer's count validation is unreliable.
**Fix**: Add a categorization priority rule to FR-02.6 or FR-04.3. Suggested: "Dual-purpose cards are assigned to the category with the greatest structural deficit. If no deficit exists, the card is assigned based on its primary function relative to the deck's strategy archetype."

### Finding 3: Success metrics lack baselines and targets [BLOCKING]

**Severity**: Blocking
**Location**: Section 2, Goals table
**Issue**: The Goals table has 6 rows with "Success Measure" descriptions, but no Baseline column, no numeric Target column, and no Measurement Method column. Success measures are restatements of requirements, not independently verifiable metrics. Example: G-02's measure is the same as FR-04.2's requirement text.
**Fix**: Add a proper metrics table. Suggested format:

| Goal | Metric | Baseline | Target | Measurement |
|------|--------|----------|--------|-------------|
| G-01 | Legal decklists produced by dogfooding test cases | 0/3 | 3/3 | Rules Judge PASS on all 3 test cases |
| G-02 | Avg synergy score across test case decks | 0 | >= 3.0 | Optimization Reviewer synergy score output |
| G-04 | Test case decks within budget | 0/3 | 3/3 | Price Evaluator PASS on all 3 test cases |
| G-05 | Pipeline runs completing without manual intervention | 0% | 100% (3/3 test cases) | End-to-end run logs |
| G-06 | Plugin validator errors | N/A | 0 errors, 0 warnings | `plugin-validator` output |

### Finding 4: Missing price data handling [WARNING]

**Severity**: Warning
**Location**: FR-05.1, FR-06.2
**Issue**: Scryfall returns null USD prices for some cards (new releases, promos, digital-only). FR-05.1 assumes price data always exists. No AC defines behavior when a card has no price.
**Fix**: Add an AC to FR-05 or FR-06: "When Scryfall returns null USD price for a card, Card Finder uses the card's cheapest non-foil printing price. If no printing has a USD price, the card is flagged as 'price unavailable' and excluded from budget calculations with a warning in the verdict."

### Finding 5: Banned commander not caught at intake [WARNING]

**Severity**: Warning
**Location**: FR-02.3, FR-03.4
**Issue**: Intake validates commander name existence (FR-02.3) but not ban status. A banned commander passes intake, and the Deck Builder constructs a full 100-card list before the Rules Judge catches the illegal commander in FR-03.4. This wastes an entire pipeline cycle.
**Fix**: Add FR-02.3a: "Commander name is validated against the Commander banned list before proceeding. A banned commander halts intake with an error message naming the ban and prompting for an alternative."

### Finding 6: Empty Card Finder results undefined [WARNING]

**Severity**: Warning
**Location**: FR-06.3, FR-04.6, FR-05.5
**Issue**: FR-04.6 and FR-05.5 both instruct agents to "suggest 1-2 replacement candidates" using Card Finder. FR-06 has no AC for when Card Finder returns zero results for a replacement query.
**Fix**: Add FR-06.8: "When a search query returns zero results, Card Finder returns an empty result set with the query parameters echoed back. Consuming agents (Optimization Reviewer, Price Evaluator) must include a 'no replacement found' note in their verdict for that card."

### Finding 7: 100-card invariant during correction cycles [WARNING]

**Severity**: Warning
**Location**: FR-07.2, FR-02.5
**Issue**: FR-02.5 requires exactly 100 cards in the initial output. FR-07.2 sends violations back to the Deck Builder for correction. No AC requires that the corrected decklist also has exactly 100 cards. If the Deck Builder removes flagged cards without adding replacements, the count breaks.
**Fix**: Add to FR-07.2: "After each correction cycle, the resulting decklist must satisfy FR-02.5 (exactly 100 cards). The Rules Judge re-validates card count on every cycle."

### Finding 8: Synergy score threshold undefined [OBSERVATION]

**Severity**: Observation (non-blocking)
**Location**: FR-04.8, Section 8 test cases
**Issue**: FR-04.8 defines the synergy score formula but sets no minimum threshold for PASS. The test cases in Section 8 require "synergy score > 3.0" but this threshold appears nowhere in FR-04. OQ-2 asks about this but defers it. The test cases assume a threshold that the FR does not mandate -- the Optimization Reviewer has no AC telling it to fail a deck with synergy score 2.9.
**Recommendation**: This is correctly deferred to Design (OQ-2), but the test cases should not assume an answer. Either remove the synergy score threshold from test case pass criteria, or add an AC to FR-04.7 that references the threshold.

---

## Verdict

**STATUS: NOT_DONE**

The PRD fails 2 of 3 blocking criteria. It has strong testable requirements (B1 PASS) and well-structured acceptance criteria overall, but two specific AC issues block passage:

1. **B2 fails** due to an "either...or" in Test Case 1 and undefined dual-purpose card categorization rules that make structural minimum validation non-deterministic.
2. **B3 fails** due to missing baselines, numeric targets, and measurement methodology in the Goals table. The success measures restate requirements rather than defining independently verifiable metrics.

Additionally, 8 edge cases are unaddressed (WARNING), with 4 representing runtime failures that have no defined behavior (price data gaps, banned commander at intake, empty Card Finder results, 100-card invariant during corrections).

The bones of this PRD are excellent. The functional requirements are thorough, the agent boundaries are clean, the test cases are well-chosen, and the scope boundary is disciplined. The fixes needed are additive (add a metrics table, add disambiguation rules, add edge case ACs) -- nothing needs to be redesigned.

The bow is drawn but the aim needs adjusting. Three targeted fixes unblock this gate.

```
STATUS: NOT_DONE
ARTIFACT: .delivery/artifacts/02-refine/qa-evaluator/evaluation-round-1.md
SUMMARY: Gate 2 FAIL. B1 PASS (all requirements testable). B2 NOT PASS (either/or in Test Case 1 commander, dual-purpose card categorization undefined). B3 NOT PASS (no baselines, no numeric targets, success measures restate requirements). 8 edge case warnings (price data gaps, banned commander at intake, empty Card Finder results, 100-card invariant during corrections, partner commanders, minimum budget, API outage, snow basics). 3 targeted fixes unblock.
```
