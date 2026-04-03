# Adversarial Challenge: MTG Commander Deck Builder Plugin PRD

**Challenger**: Adversarial Reviewer
**Date**: 2026-04-01
**PRD Version**: 1.0
**Overall Confidence**: 3/5 (Proceed with targeted fixes -- two challenges require PRD revision)

---

## Challenge 1: "Every card synergizes with 3+ other cards" Is Not Testable As Specified

**Confidence: 2/5 -- Serious concern**

The PRD's core differentiator is synergy-first selection: "Every non-land card interacts meaningfully with 3+ other cards in the deck" (G-02, FR-04.1, FR-04.2). The Optimization Reviewer is tasked with validating this. The PRD also introduces a synergy score metric (FR-04.8).

**The fundamental problem**: "interacts meaningfully" is undefined. The PRD does not specify what constitutes a meaningful interaction versus a weak or coincidental one. Consider:

- Does sharing a creature type count? If Elvish Mystic and Llanowar Elves are both Elves, do they "interact" with each other? They share a type but have zero mechanical synergy.
- Does "all creatures benefit from Coat of Arms" count as an interaction between every creature and Coat of Arms, AND between every creature pair? If yes, a single anthem effect could inflate synergy counts for every creature in the deck, making the 3+ threshold trivially easy to meet.
- Does a ramp spell "interact with" every card that costs 4+ mana? Technically Sol Ring enables casting everything -- does it get 60+ synergy connections?

The Rules Judge validates interaction claims against oracle text (FR-03.7), but only checks whether a *claimed* interaction is mechanically possible -- it does not define when an interaction *should* be claimed. The Deck Builder decides what to claim, the Judge checks if the claim is plausible, and the Optimizer counts claims. This means synergy scoring is driven by how aggressively the Deck Builder writes rationale text, not by objective deck quality.

**What this means practically**: Two runs of the same commander with the same card pool could produce different synergy scores based solely on how the AI phrases its rationale. "Interacts meaningfully" needs a taxonomy or it becomes a rubber stamp.

**What must change**: The PRD must either:
1. Define interaction categories with inclusion/exclusion rules (e.g., "shared creature type alone does not constitute interaction; a card that references the type by name does"), OR
2. Defer synergy scoring to a structured tag system (OQ-1 leans this way but is left open) and make the Design stage responsible for the taxonomy before Development begins, OR
3. Acknowledge that synergy validation in v1 is heuristic and AI-judged, remove the hard "3+ interactions" gate, and make synergy score advisory rather than blocking.

Option 2 is the strongest path -- it preserves the aspiration while routing the hard problem to Design where it belongs. But the PRD cannot ship to Design with "interacts meaningfully" unresolved, because Design will inherit the ambiguity and pass it to Development unchanged.

**Verdict**: MUST FIX. The core value proposition has no testable definition.

---

## Challenge 2: Card Hallucination Mitigation Is Correctly Placed But Has a Cost Blindspot

**Confidence: 4/5 -- Minor concern**

The PRD correctly identifies card hallucination as the highest-risk failure mode (PO Note 5) and places the Rules Judge immediately after the Deck Builder to catch it (FR-03.2). Every card name is validated against Scryfall with zero tolerance. This is the right architecture.

**The concern is the correction cycle cost.** If the Deck Builder hallucinate 10 card names in a 100-card list (plausible -- AI models are notoriously bad at exact Magic card names), the Rules Judge returns FAIL with 10 violations, and the Deck Builder must correct all 10. But the replacement cards must ALSO be validated, which means a second Rules Judge pass. If 3 of the 10 replacements are also hallucinated, that is a third cycle. The PRD references `pipeline.max_self_correction: 3` (FR-07.3), which means the pipeline could exhaust all correction cycles on card name accuracy alone before the Optimizer or Price Evaluator ever run.

A better architecture would have the Deck Builder call Card Finder (FR-06.7) to validate card names *during initial construction*, not after. FR-06.7 provides exactly this: "a card name validation function that returns True/False for whether a given name exactly matches a card in Scryfall." If the Deck Builder validates each card as it selects it, the Rules Judge receives a list with zero (or near-zero) hallucinated names, and correction cycles are preserved for actual legality and synergy issues.

**However**, FR-07.1 already allows the Deck Builder to use Card Finder -- it is a "shared utility available to all agents." The PRD does not *prohibit* pre-validation; it simply does not *require* it. This is a Design/Architect decision about agent composition, not a PRD gap.

**Recommendation**: Add one sentence to FR-02 acceptance criteria: "FR-02.9: The Deck Builder SHOULD validate each card name against Card Finder (FR-06.7) during construction. Cards that fail validation MUST NOT appear in the output list." This converts pre-validation from an implementation choice to a documented expectation without over-specifying the architecture.

**Verdict**: Not blocking. The architecture handles hallucination; the optimization is a should-have.

---

## Challenge 3: Scryfall API Rate Limits Make 100-Card Pricing Fragile

**Confidence: 3/5 -- Moderate concern**

The PRD specifies "minimum 50ms delay between consecutive API requests" (FR-06.4, NFR-01). Scryfall's actual documentation states 50-100ms between requests, or approximately 10 requests per second. The idea brief correctly states 10 requests/second.

**The math for a full pipeline run:**

1. **Deck Builder**: Commander validation = 1 request. Card name validation during build (if FR-02.9 is adopted) = up to 99 requests. That is ~5-10 seconds.
2. **Rules Judge**: Validate 100 card names = 100 requests = ~5-10 seconds. Validate legality = potentially 100 more if legality status is not included in the name lookup response. That is 10-20 seconds.
3. **Price Evaluator**: Price lookup for 100 cards = 100 requests = ~5-10 seconds.
4. **Correction cycles**: Each correction cycle that touches N cards adds N requests per agent that re-validates.

**Best case (no corrections)**: ~200-300 API calls, 10-30 seconds of API wait time alone. **Worst case (3 correction cycles with significant churn)**: ~800-1200 API calls, 40-120 seconds of API wait time. This is within Scryfall's tolerance for a single session but is not negligible for user experience.

**The real concern**: The PRD says "bulk endpoints preferred over individual lookups where possible" (NFR-01) but does not specify which agents should use bulk endpoints. Scryfall's `/cards/collection` endpoint accepts up to 75 card identifiers per request. A 100-card deck could be fully validated and priced in 2 bulk requests instead of 100 individual ones. This is a 50x reduction in API calls.

**What is missing**: FR-06 (Card Finder) specifies the `/cards/search` endpoint (FR-06.1) but never mentions `/cards/collection` or `/cards/named` for exact lookups. The Card Finder's interface is designed around individual card searches, not batch operations. This means even if bulk is "preferred," the utility does not support it.

**Recommendation**: Add an acceptance criterion to FR-06: "FR-06.8: Card Finder supports batch card lookup via Scryfall's `/cards/collection` endpoint, accepting up to 75 card identifiers per request and returning structured data for all matched cards. Agents SHOULD use batch lookup when validating or pricing complete decklists." This is architecturally important enough to specify at the PRD level.

**Verdict**: Not blocking for v1 correctness, but the PRD should acknowledge the performance characteristic and add batch support to the Card Finder spec.

---

## Challenge 4: The Orchestration Sequence Has a Logical Flaw in Budget Correction

**Confidence: 2/5 -- Serious concern**

The pipeline is: Deck Builder > Rules Judge > Optimization Reviewer > Price Evaluator (FR-07.1). When any agent returns FAIL, the pipeline cycles back to the Deck Builder (FR-07.2).

**The flaw**: When the Price Evaluator busts the budget, the Deck Builder must replace expensive cards with cheaper alternatives. But the replacements must then pass the Rules Judge (legality) AND the Optimization Reviewer (synergy) again. This means a budget fix can create a synergy failure, which creates a correction cycle, which changes cards, which may re-bust the budget. The correction loop is:

```
Budget fail -> Builder replaces cards -> Judge re-validates -> Optimizer re-validates 
-> Optimizer fails (replacement has <3 synergy) -> Builder replaces again 
-> Judge re-validates -> Optimizer passes -> Pricer re-validates 
-> Pricer fails (new replacement is expensive) -> ...
```

With `max_self_correction: 3`, this oscillation between budget and synergy constraints can exhaust all cycles without convergence. The problem is structural: budget and synergy are competing constraints, and the pipeline has no mechanism to negotiate between them.

**Real-world example**: A $75 Mono-Blue Mill deck (Test Case 3). Rhystic Study is a premier draw spell with 10+ synergy connections. It costs ~$40. Removing it for budget reasons removes a major synergy hub, which causes multiple other cards to drop below the 3-interaction threshold. Replacing those cards changes the deck substantially, potentially re-introducing budget problems.

**What must change**: The PRD needs to specify what happens when budget and synergy constraints conflict irreconcilably. Options:
1. **Budget wins**: If a card must be cut for budget, the synergy threshold is relaxed for its replacement (e.g., 2 interactions instead of 3). This needs explicit specification.
2. **Optimizer suggests budget-aware replacements**: FR-04.6 says the Optimizer suggests replacements, but does not require them to be budget-aware. The Optimizer and Price Evaluator should share context.
3. **Combined pass**: The Optimizer and Price Evaluator run together or the Optimizer is aware of the budget constraint. This is an architecture change.
4. **Graceful degradation**: If budget and synergy conflict after max cycles, the output includes a warning explaining the tradeoff. FR-07.4 partially covers this ("best-effort decklist with a clear warning") but does not acknowledge the budget/synergy tension specifically.

At minimum, FR-07.4 should explicitly state: "When budget and synergy constraints conflict irreconcilably, budget compliance takes priority. The output warns which cards were included with fewer than 3 synergy connections due to budget constraints." This gives the pipeline a deterministic resolution rule.

**Verdict**: MUST FIX. The correction loop can oscillate without convergence. The PRD needs a priority rule for competing constraints.

---

## Challenge 5: Three Test Cases Are Insufficient for a GREENFIELD Plugin

**Confidence: 3/5 -- Moderate concern**

The PRD specifies 3 test cases (Section 8): Mono-Black Graveyard ($150), Orzhov Lifegain ($100 with $10/card cap), and Mono-Blue Mill ($75, no infinite combos). These cover:

- 1 mono-color, 1 two-color, 1 mono-color (no 3+ color test)
- 3 different budget tiers
- 1 per-card cap scenario
- 1 card restriction scenario (no infinite combos)
- 0 partner commander scenarios (OQ-5 asks if partners are in scope -- if yes, no test)
- 0 high-power (8-10) scenarios
- 0 edge cases for color identity (e.g., hybrid mana, Phyrexian mana, colorless commander)

**The critical gap is multi-color.** A 3+ color commander (e.g., Korvold, Meren, Atraxa) exercises color identity validation far more rigorously than mono or two-color. With mono-black, every black card is legal. With 4-color, the Rules Judge must correctly identify which combinations of 4 colors are within identity and reject the fifth. This is where color identity bugs hide.

**Secondary gap**: No test case exercises the correction loop. All 3 test cases are designed to *pass* cleanly. There is no test case that intentionally triggers a Rules Judge failure (e.g., a commander with a commonly confused color identity) or a Price Evaluator failure (e.g., a $50 budget that forces significant compromises). The dogfooding tests the happy path but not the correction machinery.

**Recommendation**: Add two test cases:
1. **Multi-color stress test**: A 3+ color commander (e.g., Korvold, Fae-Cursed King -- Jund/BRG) at power 8 with a $200 budget. Exercises multi-color identity validation and higher power structural targets.
2. **Budget stress test**: A popular commander (e.g., Atraxa, Praetors' Voice -- WUBG) at power 7 with a $50 budget. This WILL trigger budget correction cycles because 4-color mana bases are expensive. Tests the correction loop and budget/synergy negotiation.

**Verdict**: Not blocking, but 3 tests leave significant coverage gaps. Adding 2 targeted cases would substantially increase confidence.

---

## Challenge 6: Open Question OQ-5 (Partner Commanders) Must Be Resolved Before Design

**Confidence: 4/5 -- Low risk if resolved**

OQ-5 asks whether partner commanders are supported in v1. The PRD leaves this to Design. However, partner support has PRD-level implications:

- **FR-02.1** (intake questions): Question 2 is "commander name" (singular). Partners require two names and combined color identity derivation. The intake flow changes.
- **FR-02.5**: "exactly 100 cards including the commander" -- with partners, it is 100 cards including TWO commanders (98 other cards). The count rule changes.
- **FR-02.4**: Color identity is "derived from the validated commander card" -- with partners, it is the union of both commanders' color identities.
- **FR-03.1**: Validates "exactly 100 cards (including commander)" -- same count ambiguity.
- **Structural minimums**: Partners decks sometimes have different structural needs (e.g., partner pairs that provide card advantage may need fewer draw sources).

If partners are IN scope, at least 5 acceptance criteria need revision. If partners are OUT of scope, the PRD should state this explicitly so that the Rules Judge can reject partner commanders with a clear error message rather than silently mishandling them.

**Recommendation**: Resolve OQ-5 in the PRD as OUT of scope for v1, with an explicit acceptance criterion: "FR-02.10: If a user specifies a partner commander, the intake flow informs the user that partner commanders are not supported in v1 and prompts for a single commander." This is a 2-minute PRD change that prevents an ambiguous failure mode.

**Verdict**: Not blocking if resolved as out-of-scope. Blocking if left ambiguous.

---

## Summary Table

| # | Challenge | Confidence | Verdict |
|---|-----------|-----------|---------|
| 1 | Synergy scoring is untestable as specified | 2/5 | **MUST FIX** -- "interacts meaningfully" needs a taxonomy or must be routed to Design explicitly |
| 2 | Card hallucination correction cost | 4/5 | Proceed -- add pre-validation recommendation to FR-02 |
| 3 | Scryfall API rate limits and batch support | 3/5 | Proceed -- add batch endpoint to Card Finder spec |
| 4 | Budget/synergy correction oscillation | 2/5 | **MUST FIX** -- needs priority rule for competing constraints |
| 5 | Three test cases insufficient | 3/5 | Proceed -- add 2 targeted test cases (multi-color, budget stress) |
| 6 | Partner commanders unresolved | 4/5 | Proceed -- resolve as out-of-scope with explicit rejection |

---

## Blocking Assessment

**Two challenges scored <= 2 and require PRD revision before proceeding to Design:**

1. **Challenge 1 (confidence 2/5)**: The synergy-first philosophy -- the PRD's stated core differentiator -- has no testable definition. "Interacts meaningfully" is subjective and AI-variable. The 3+ interaction threshold is gameable through overly broad interaction claims (type-sharing, mana-enablement). Without an interaction taxonomy or explicit routing to Design for taxonomy creation, the Optimization Reviewer cannot enforce the gate deterministically. Fix: either define interaction categories in the PRD or add an explicit precondition that Design must produce an interaction taxonomy before Development begins.

2. **Challenge 4 (confidence 2/5)**: The correction loop can oscillate between budget and synergy constraints without convergence. The pipeline has no priority rule for when these constraints conflict. With `max_self_correction: 3`, oscillation exhausts cycles and produces a "best-effort" deck that may violate both constraints. Fix: add a constraint priority rule to FR-07 (recommended: budget wins, synergy threshold relaxes for budget-forced replacements) and specify this in FR-07.4's graceful degradation clause.

**Three additional challenges require minor PRD amendments (not blocking but should be addressed before Plan):**

- **Challenge 2**: Add FR-02.9 recommending pre-validation of card names via Card Finder during construction.
- **Challenge 3**: Add FR-06.8 specifying batch card lookup via Scryfall's `/cards/collection` endpoint.
- **Challenge 5**: Add 2 test cases: multi-color stress test and budget stress test.
- **Challenge 6**: Resolve OQ-5 as out-of-scope with explicit partner rejection in FR-02.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/02-refine/challenger/challenge.md
CONFIDENCE: 3/5
ESCALATION: Not required (overall confidence > 2). Two MUST FIX items (Challenge 1, Challenge 4) require PRD revision before Design. Four minor amendments recommended.
SUMMARY: 6 challenges raised against MTG Commander Deck Builder PRD. Synergy scoring lacks a testable definition (the core value proposition is ambiguous). Budget/synergy correction loop can oscillate without convergence. Card hallucination mitigation is architecturally sound but should pre-validate. Scryfall API performance needs batch endpoint support. Test coverage gaps in multi-color and correction-loop scenarios. Partner commander scope must be resolved explicitly.
```
