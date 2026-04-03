# PRD: MTG Commander Deck Builder Plugin

**Version**: 1.1
**Date**: 2026-04-01
**Author**: Product Owner (Gandalf)
**Project Type**: GREENFIELD
**Pipeline Routing**: Idea > Refine > Design > Architect > Plan > Development > UAT

---

## 1. Purpose

This document specifies the functional and non-functional requirements for the MTG Commander Deck Builder — a new Claude Code plugin that produces format-legal, synergy-dense, structurally sound, budget-compliant Commander decklists through a multi-agent pipeline.

The core philosophy: **Synergy first. Always.** Every non-land card must interact meaningfully with 3+ other cards. Popularity is a tiebreaker, never a selection criterion. This is a deck *construction* pipeline with built-in quality gates — not a card recommendation engine.

---

## 2. Goals

| ID | Goal | Metric | Baseline | Target | Measurement |
|----|------|--------|----------|--------|-------------|
| G-01 | Produce format-legal 100-card Commander decklists | Dogfooding test cases producing fully legal decklists | 0/5 | 5/5 | Rules Judge returns PASS on all 5 test cases (Section 8) |
| G-02 | Enforce synergy-first card selection | Average synergy score across dogfooding decks | 0 | >= 3.0 | Optimization Reviewer synergy score output per deck |
| G-03 | Meet structural minimums by power level | Test case decks passing structural validation | 0/5 | 5/5 | Optimization Reviewer structural check PASS on all 5 test cases |
| G-04 | Enforce budget compliance with real pricing | Test case decks within stated budget | 0/5 | 5/5 | Price Evaluator PASS on all 5 test cases |
| G-05 | Complete pipeline in a single session | Pipeline runs completing without manual user intervention between agents | 0% | 100% (5/5 test cases) | End-to-end run logs show no user prompts between agent handoffs |
| G-06 | Ship as a valid Claude Code plugin | Plugin validator errors and warnings | N/A (new plugin) | 0 errors, 0 warnings | `plugin-validator` output on `mtg-commander/` directory |

---

## 3. Target Users

| Persona | Experience | Primary Need | Key Constraint |
|---------|-----------|--------------|----------------|
| Experienced player, new commander | Veteran (5+ years) | Build around an unfamiliar commander without 6 hours of card research | Time |
| New-to-Commander player | Intermediate (knows Magic, new to Commander) | Structurally sound 100-card list that actually functions | Knowledge gap (does not know structural requirements) |
| Budget-conscious brewer | Any level | Competitive deck within a hard budget ceiling ($50-200 range) | Budget must shape selection, not just filter |
| Returning player | Lapsed (1-3 year gap) | Current-pool deck without outdated assumptions | Currency (card pool expanded, banned list changed) |

---

## 4. Functional Requirements

### FR-01: Plugin Structure

The plugin ships as a top-level directory in the Claude-Plugins repo following established conventions.

| AC | Acceptance Criterion |
|----|---------------------|
| FR-01.1 | Plugin directory is `mtg-commander/` (kebab-case) |
| FR-01.2 | `SKILL.md` exists at root with primary skill instructions: intake orchestration, agent sequencing, output format specification |
| FR-01.3 | `LICENSE.txt` exists at plugin root |
| FR-01.4 | Plugin is registered in `.claude-plugin/marketplace.json` with unique name `mtg-commander`, display description, source path, and skill paths |
| FR-01.5 | Directory structure includes `agents/`, `references/`, and `scripts/` subdirectories |
| FR-01.6 | Plugin passes `plugin-validator` with zero errors |
| FR-01.7 | `api.scryfall.com` is documented as a required WebFetch domain in setup instructions within SKILL.md |

### FR-02: Deck Builder Agent

The Deck Builder handles user intake and produces the initial 100-card decklist.

**Intake Flow:**

| AC | Acceptance Criterion |
|----|---------------------|
| FR-02.1 | Agent presents 7 intake questions in sequence: (1) color identity, (2) commander name, (3) strategy archetype, (4) power level (1-10 scale), (5) meta alignment, (6) total budget in USD, (7) card restrictions (must-include / must-exclude) |
| FR-02.2 | User may provide all 7 answers upfront (inline) or answer interactively one at a time |
| FR-02.3 | Commander name is validated against Scryfall before proceeding — invalid names halt intake with an error message and prompt for correction |
| FR-02.3a | Commander name is validated against the Commander banned list before proceeding. A banned commander halts intake with an error message naming the ban and prompting for an alternative. |
| FR-02.4 | Color identity is derived from the validated commander card, not user input alone (user-specified colors serve as a cross-check) |

**Deck Output:**

| AC | Acceptance Criterion |
|----|---------------------|
| FR-02.5 | Output is exactly 100 cards including the commander |
| FR-02.6 | Every card is assigned to exactly one category: Commander (1), Lands (34-40), Ramp (10+), Card Draw (10+), Removal (5+), Board Wipes (2+), Win Conditions (3+), Synergy Pieces (remaining). **Disambiguation rule**: When a card serves multiple category functions, assign it to the category with the greatest structural deficit (i.e., the category furthest below its minimum). If no deficit exists, assign based on the card's primary function relative to the deck's strategy archetype. This ensures FR-04.3 structural minimums are deterministically verifiable. |
| FR-02.7 | Output format lists cards grouped by category with card name, mana cost, and a one-sentence synergy rationale for each non-land card |
| FR-02.8 | Agent documents the deck's primary game plan in 2-3 sentences before the card list |
| FR-02.9 | The Deck Builder SHOULD validate each card name against Card Finder (FR-06.7) during construction. Cards that fail name validation MUST NOT appear in the output list. This reduces hallucinated names reaching the Rules Judge and preserves correction cycles for legality and synergy issues. |
| FR-02.10 | If a user specifies a partner commander (a card with the "Partner" keyword), the intake flow informs the user that partner commanders are not supported in v1 and prompts for a single commander. |

### FR-03: Rules Judge Agent

The Rules Judge validates format legality. It makes no creative decisions — pure rules enforcement.

| AC | Acceptance Criterion |
|----|---------------------|
| FR-03.1 | Validates exactly 100 cards in the decklist (including commander) |
| FR-03.2 | Validates every card name exists in Scryfall (zero tolerance for hallucinated names) |
| FR-03.3 | Validates every card's color identity is within the commander's color identity |
| FR-03.4 | Validates no card appears on the Commander banned list |
| FR-03.5 | Validates singleton rule: no duplicate card names except basic lands |
| FR-03.6 | Validates each card's format legality status is "legal" in Commander format per Scryfall data |
| FR-03.7 | When a card interaction is claimed in synergy rationale, validates that the interaction is mechanically possible based on oracle text (e.g., a card described as "triggers on creature death" must actually have oracle text referencing creature death) |
| FR-03.8 | Outputs a structured verdict: PASS (all checks clear) or FAIL with a list of specific violations. Each violation includes the card name, the rule violated, and a suggested correction. |
| FR-03.9 | Legality decisions are deterministic — based on authoritative Scryfall data, never AI-inferred |

### FR-04: Optimization Reviewer Agent

The Optimization Reviewer enforces the synergy-first philosophy and structural soundness.

| AC | Acceptance Criterion |
|----|---------------------|
| FR-04.1 | For every non-land card, identifies and lists the other cards it interacts with. Interactions are classified using the **Synergy Interaction Taxonomy** (see below). Only interactions that match a defined category count toward the 3-card threshold. |
| FR-04.2 | Flags any non-land card that interacts with fewer than 3 other cards in the deck as "isolated" |
| FR-04.3 | Validates structural minimums: 10+ ramp sources, 10+ card draw sources, 5+ targeted removal, 2+ board wipes, 3+ win conditions |
| FR-04.4 | Validates land count is between 34 and 40 (inclusive), adjusted for power level and average mana value |
| FR-04.5 | Produces a mana curve distribution (0-1, 2, 3, 4, 5, 6, 7+) and flags if the curve is front-loaded or top-heavy relative to the strategy archetype |
| FR-04.6 | For each isolated card flagged, suggests 1-2 replacement candidates that have 3+ interactions with existing cards |
| FR-04.7 | Outputs a structured verdict: PASS (zero isolated cards, all structural minimums met) or FAIL with specific violations and replacement suggestions |
| FR-04.8 | Calculates a deck synergy score: (total synergy connections across all non-land cards) / (number of non-land cards). Reports this score in the verdict. |

**Synergy Interaction Taxonomy**

An interaction between two cards counts toward the 3-card threshold only if it falls into one of these categories:

| Category | Definition | Example | Exclusion |
|----------|-----------|---------|-----------|
| **Triggers** | Card A's effect causes Card B's triggered ability to fire | Viscera Seer sacrificing a creature triggers Blood Artist | — |
| **Enables** | Card A provides a resource or condition that Card B specifically requires | Urborg, Tomb of Yawgmoth enables Cabal Coffers | Generic mana enablement alone does NOT count (Sol Ring does not "enable" every 2+ cost card) |
| **Protects** | Card A shields Card B from removal, counters, or adverse effects | Lightning Greaves protecting a voltron commander | — |
| **Combos-with** | Cards A and B form part of a defined combo (2-4 card combination producing a win condition or overwhelming advantage) | Sanguine Bond + Exquisite Blood | — |
| **Amplifies** | Card A increases the output or effectiveness of Card B's ability by a measurable factor | Panharmonicon doubling Solemn Simulacrum's ETB | — |
| **Feeds** | Card A produces tokens, cards, or resources that Card B specifically consumes | Bitterblossom producing tokens for Skullclamp | — |

**Exclusions** (do NOT count as interactions):
- Sharing a creature type alone (two Elves do not interact unless one references the Elf type)
- Generic mana enablement (ramp enabling expensive cards is the ramp category's role, not synergy)
- Both being "good cards" in the same strategy without mechanical connection

**Design stage responsibility**: The Design stage MAY refine, extend, or restructure this taxonomy. If the taxonomy changes, it must remain deterministic and enforceable by the Optimization Reviewer. OQ-1 (structured tags vs. free text) directly affects how interactions are recorded and counted.

### FR-05: Price Evaluator Agent

The Price Evaluator enforces budget compliance using live Scryfall pricing data.

| AC | Acceptance Criterion |
|----|---------------------|
| FR-05.1 | Retrieves current USD pricing for each card via Scryfall API (using the cheapest available printing) |
| FR-05.2 | Calculates total deck cost as the sum of all 100 cards' cheapest printing prices |
| FR-05.3 | Validates total deck cost does not exceed the user-specified budget |
| FR-05.4 | If a per-card cap is specified (or defaults to 15% of total budget), flags any card exceeding the cap |
| FR-05.5 | For each over-budget or over-cap card, suggests 1-2 budget-friendly alternatives that maintain synergy (via Card Finder) |
| FR-05.6 | Outputs a structured verdict: PASS (within budget, no cap violations) or FAIL with specific violations, the current total cost, the budget ceiling, and replacement suggestions |
| FR-05.7 | Reports a price breakdown by category (lands, ramp, draw, removal, synergy pieces, etc.) |
| FR-05.8 | When Scryfall returns null USD price for a card, Card Finder uses the card's cheapest non-foil printing price. If no printing has a USD price, the card is flagged as "price unavailable" and excluded from budget calculations with a warning in the Price Evaluator verdict. |

### FR-06: Card Finder Utility

The Card Finder is a shared utility available to all agents for on-demand card lookup.

| AC | Acceptance Criterion |
|----|---------------------|
| FR-06.1 | Queries the Scryfall API search endpoint (`/cards/search`) with support for: card name, oracle text substring, color identity filter, type line filter, mana value filter, Commander format legality filter |
| FR-06.2 | Returns structured card data: name, mana cost, type line, oracle text, color identity, USD price (cheapest printing), set name |
| FR-06.3 | Supports "budget replacement" queries: given a card name and a price ceiling, returns functionally similar cards under the price ceiling |
| FR-06.4 | Implements Scryfall rate limiting: minimum 50ms delay between consecutive API requests |
| FR-06.5 | Handles Scryfall API errors gracefully: returns clear error messages for 404 (card not found), 422 (bad query), and 429 (rate limited — back off and retry) |
| FR-06.6 | Implemented as a Python script (`scripts/card_lookup.py`) using only `urllib` (no external dependencies) |
| FR-06.7 | Provides a card name validation function that returns True/False for whether a given name exactly matches a card in Scryfall |
| FR-06.8 | Supports batch card lookup via Scryfall's `/cards/collection` endpoint, accepting up to 75 card identifiers per request and returning structured data for all matched cards. Agents SHOULD use batch lookup when validating or pricing complete decklists. |
| FR-06.9 | When a search query returns zero results, Card Finder returns an empty result set with the query parameters echoed back. Consuming agents (Optimization Reviewer, Price Evaluator) must include a "no replacement found" note in their verdict for that card. |

### FR-07: Orchestration Flow

The SKILL.md orchestrates the agent pipeline from intake through final output.

| AC | Acceptance Criterion |
|----|---------------------|
| FR-07.1 | Pipeline executes agents in sequence: Deck Builder > Rules Judge > Optimization Reviewer > Price Evaluator |
| FR-07.2 | If any agent returns FAIL, the pipeline cycles back to the Deck Builder with the specific violations and replacement suggestions from the failing agent. After each correction cycle, the resulting decklist must satisfy FR-02.5 (exactly 100 cards). The Rules Judge re-validates card count on every cycle. |
| FR-07.3 | Correction cycles use the existing pipeline config mechanism (`pipeline.max_self_correction` in `.delivery/config.yml`) — no new iteration limit mechanism is introduced |
| FR-07.4 | If max correction cycles are exhausted, the pipeline outputs the best-effort decklist with a clear warning listing remaining violations. **Constraint priority rule**: When budget and synergy constraints conflict irreconcilably, budget compliance takes priority. Cards replaced solely due to budget constraints have their synergy threshold relaxed to 2 interactions (instead of 3). The output warns which cards were included with reduced synergy due to budget constraints. |
| FR-07.5 | Final output is a formatted decklist with: deck summary (commander, strategy, power level, total cost), cards grouped by category, synergy score, budget breakdown, and any remaining warnings |
| FR-07.6 | Final output includes an export-ready card list (one card name per line, no annotations) suitable for copy-paste into deck building tools |
| FR-07.7 | Each agent's verdict (PASS/FAIL + details) is preserved in the output for transparency |

---

## 5. Non-Functional Requirements

| ID | Requirement | Acceptance Criterion |
|----|------------|---------------------|
| NFR-01 | Scryfall API rate limiting | Card Finder enforces minimum 50ms delay between requests. Bulk endpoints preferred over individual lookups where possible. |
| NFR-02 | No external Python dependencies | All scripts use only Python standard library (`urllib`, `json`, `time`). No pip install required. |
| NFR-03 | Card name accuracy | Zero hallucinated card names in final output. Every card name verified against Scryfall. Rules Judge gates this with zero tolerance. |
| NFR-04 | Plugin validation | Plugin passes `plugin-validator` with zero errors and zero warnings. |
| NFR-05 | Internet required | Plugin requires internet access for Scryfall API. This is documented in setup instructions. No offline mode in v1. |
| NFR-06 | Scryfall error resilience | Card Finder retries on 429 (rate limit) with exponential backoff (max 3 retries). Returns meaningful error on persistent failure. |
| NFR-07 | Session completion | Full pipeline (intake through final output) completes within a single Claude Code session. No multi-session workflows. |

---

## 6. v1 Scope Boundary

### In Scope

- Plugin skeleton (`mtg-commander/`) with SKILL.md, agents, references, scripts, LICENSE.txt
- 4 agents: Deck Builder, Rules Judge, Optimization Reviewer, Price Evaluator
- 1 utility: Card Finder (Scryfall API client)
- 7 intake questions with validation
- Sequential pipeline with correction loops
- Scryfall API as sole external data source (card data + pricing)
- Reference files: Commander format rules, banned list, archetype patterns, structural targets, API patterns
- 5 test cases for dogfooding validation (see Section 8)

### Out of Scope (Deferred to v2+)

| Item | Rationale |
|------|-----------|
| Recommander integration | Needs API investigation. Scryfall + heuristic synergy sufficient for v1. |
| EDHREC integration | No official API. Tiebreaker-only value does not justify scraping complexity. |
| Multi-source pricing (TCGPlayer, Card Kingdom) | Scryfall pricing covers v1. Multi-source adds API key management. |
| Moxfield / Archidekt export | Export-ready text list covers v1. Platform-specific export is convenience. |
| Deck modification mode ("improve my deck") | Different intake flow required. v1 focuses on new builds. |
| Persistent card database (SQLite cache) | Scryfall API is fast enough for v1 volumes. |
| Hooks (automated validation) | Agents themselves provide validation. Hooks add CI-style value but are not needed for v1 correctness. |
| Meta-game analysis | Requires additional data sources and ongoing maintenance. |
| MCP server for Scryfall | Python script via Card Finder is sufficient for v1. MCP adds value when multiple plugins need Scryfall access. |
| Partner commanders | Requires revised intake flow (2 names), combined color identity derivation, 98-card deck structure, and structural minimum adjustments. Rejected at intake with clear message (FR-02.10). |

---

## 7. Reference Files Required

These reference documents support the agents and must be authored during the Development stage.

| File | Location | Purpose | Content |
|------|----------|---------|---------|
| Commander Rules | `references/commander-rules.md` | Rules Judge source of truth | Format rules, color identity rules, singleton rule, commander tax, combat damage, partner rules |
| Banned List | `references/banned-list.md` | Rules Judge banned card check | Current Commander banned list (sourced from mtgcommander.net). Updated manually on ban announcements. |
| Archetype Patterns | `references/archetype-patterns.md` | Deck Builder archetype knowledge | Common archetypes (aristocrats, voltron, spellslinger, tribal, combo, stax, group hug, mill, etc.) with typical card categories and synergy patterns |
| Structural Minimums | `references/structural-minimums.md` | Optimization Reviewer targets | Ramp, draw, removal, board wipe, land count targets by power level (casual 1-4, mid 5-7, high 8-9, cEDH 10) |
| Intake Questions | `references/intake-questions.md` | Deck Builder intake flow | The 7 questions with valid input ranges, default values, and validation rules |
| API Reference | `references/api-reference.md` | Card Finder implementation guide | Scryfall endpoints, query syntax, rate limits, response schemas, error codes |

---

## 8. Test Cases (Dogfooding Gate)

All 3 test cases must produce valid decklists before UAT passes. The team builds these decks before users do.

### Test Case 1: Mono-Black Graveyard

| Field | Value |
|-------|-------|
| Commander | K'rrik, Son of Yawgmoth |
| Color Identity | Black |
| Strategy | Graveyard recursion / reanimator |
| Power Level | 7 |
| Meta Alignment | Mid-power casual |
| Budget | $150 |
| Restrictions | None |

**Pass criteria**: 100 legal cards, synergy score >= 3.0, total cost <= $150, 10+ ramp, 10+ draw, zero banned cards, zero hallucinated names.

### Test Case 2: Orzhov Lifegain

| Field | Value |
|-------|-------|
| Commander | Karlov of the Ghost Council |
| Color Identity | White/Black |
| Strategy | Lifegain/drain |
| Power Level | 6 |
| Meta Alignment | Casual |
| Budget | $100 |
| Restrictions | No cards over $10 each |

**Pass criteria**: 100 legal cards, synergy score >= 3.0, total cost <= $100, no card > $10, all cards within WB color identity, 10+ ramp, 10+ draw, zero banned cards, zero hallucinated names.

### Test Case 3: Mono-Blue Mill

| Field | Value |
|-------|-------|
| Commander | Bruvac the Grandiloquent |
| Color Identity | Blue |
| Strategy | Mill / library depletion |
| Power Level | 5 |
| Meta Alignment | Casual / fun |
| Budget | $75 |
| Restrictions | No infinite combos |

**Pass criteria**: 100 legal cards, synergy score >= 3.0, total cost <= $75, all cards within U color identity, 10+ ramp, 10+ draw, no infinite combo pieces flagged, zero banned cards, zero hallucinated names.

### Test Case 4: Multi-Color Stress Test (3+ Colors)

| Field | Value |
|-------|-------|
| Commander | Korvold, Fae-Cursed King |
| Color Identity | Black/Red/Green (Jund) |
| Strategy | Sacrifice / aristocrats |
| Power Level | 8 |
| Meta Alignment | High-power |
| Budget | $200 |
| Restrictions | None |

**Pass criteria**: 100 legal cards, synergy score >= 3.0, total cost <= $200, all cards within BRG color identity (no white, no blue cards), 10+ ramp, 10+ draw, zero banned cards, zero hallucinated names. This test exercises multi-color identity validation and higher power structural targets.

### Test Case 5: Budget Stress Test (4-Color, $50)

| Field | Value |
|-------|-------|
| Commander | Atraxa, Praetors' Voice |
| Color Identity | White/Blue/Black/Green |
| Strategy | +1/+1 counters / proliferate |
| Power Level | 7 |
| Meta Alignment | Mid-power casual |
| Budget | $50 |
| Restrictions | No cards over $5 each |

**Pass criteria**: 100 legal cards, synergy score >= 3.0 (budget-relaxed threshold of >= 2.0 acceptable per FR-07.4 constraint priority rule if budget forces substitutions), total cost <= $50, no card > $5, all cards within WUBG color identity (no red cards), 10+ ramp, 10+ draw, zero banned cards, zero hallucinated names. This test exercises the correction loop and budget/synergy constraint negotiation.

---

## 9. Marketplace Registration

The plugin entry in `.claude-plugin/marketplace.json` follows the established pattern:

```json
{
  "name": "mtg-commander",
  "description": "MTG Commander deck builder with multi-agent pipeline. Synergy-first card selection, Scryfall API integration, format legality validation, structural optimization, and budget enforcement. Produces complete 100-card decklists.",
  "source": "./",
  "strict": false,
  "skills": [
    "./mtg-commander"
  ]
}
```

---

## 10. Open Questions for Design/Architect Stages

| # | Question | Relevant Stage |
|---|----------|---------------|
| OQ-1 | Should the synergy rationale be a free-text sentence or a structured tag system (e.g., `[TRIGGERS: creature death]`, `[ENABLES: ramp]`)? Structured tags enable automated synergy counting; free text is more readable. | Design |
| OQ-2 | What is the minimum acceptable synergy score for a deck to pass the Optimization Reviewer? The PRD requires 3+ interactions per card, but a deck-level threshold (e.g., average 3.5) may also be warranted. | Design |
| OQ-3 | Should the Card Finder use Scryfall's `/cards/search` (flexible query) or `/cards/named` (exact match) for name validation? Exact match is faster but less tolerant of minor input variations. | Architect |
| OQ-4 | How should the agents handle double-faced cards, split cards, and adventure cards where the card has multiple names? Scryfall returns these with `//` separators. | Architect |
| OQ-5 | ~~Should partner commanders be supported in v1?~~ **RESOLVED in v1.1**: Partner commanders are explicitly OUT of scope for v1. FR-02.10 specifies that partner commanders are rejected at intake with a clear message. Partner support (2-commander, 98-other-cards, combined color identity) is deferred to v2+. | N/A |

---

## 11. Dependencies

| Dependency | Type | Risk | Mitigation |
|-----------|------|------|-----------|
| Scryfall API | External service | Low (well-documented, stable, free) | Card Finder implements retry logic and rate limiting. No fallback in v1 — Scryfall downtime blocks deck building. |
| `api.scryfall.com` WebFetch permission | Configuration | Low | Documented in SKILL.md setup instructions. User must add to allowed domains. |
| Commander banned list currency | Data freshness | Low (changes quarterly) | Maintained as a reference file. Updated manually when bans are announced. |
| Scryfall pricing accuracy | Data quality | Medium (Scryfall aggregates, may lag market) | Acceptable for v1. Budget enforcement uses Scryfall as source of truth. |

---

## 12. PO Notes

1. **Agent architecture is proposed, not decided.** This PRD specifies WHAT each agent does (inputs, outputs, validation rules). HOW the agents are implemented (sub-agents, tool-use patterns, prompt structure) is a Design/Architect decision.

2. **The correction cycle mechanism already exists.** The delivery pipeline config has `pipeline.max_self_correction: 3` and `pipeline.max_dod_rounds: 3`. The deck builder pipeline should reference this mechanism — do not invent a new iteration limit config.

3. **Synergy scoring is the novel value proposition.** Popularity-based tools already exist (EDHREC). Our differentiation is synergy-first selection with explicit interaction mapping. If we nail nothing else, we nail this.

4. **Dogfooding is P0.** All 5 test cases must produce valid decks that the team reviews before UAT. Code review alone is not sufficient. We play with the tool before users do.

5. **Card name accuracy is the highest-risk failure mode.** AI models hallucinate Magic card names. The Rules Judge exists specifically to catch this. Zero tolerance — every name verified against Scryfall.

---

*"Even the smallest plugin can change the course of a game night — provided it knows the difference between a Sol Ring and a hallucinated one. Build the fellowship. Trust the pipeline. Synergy first. Always."*

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-01 | Initial PRD |
| 1.1 | 2026-04-01 | QA evaluation + adversarial review fixes: Goals table with baselines/targets/metrics (B3 fix). Deterministic commander in Test Case 1 (B2 fix). Category disambiguation rule in FR-02.6 (B2 fix). Synergy Interaction Taxonomy with 6 categories and explicit exclusions (Challenge 1 fix). Budget-vs-synergy constraint priority rule in FR-07.4 (Challenge 4 fix). FR-02.9 card name pre-validation, FR-02.10 partner rejection, FR-02.3a banned commander at intake, FR-05.8 null price handling, FR-06.8 batch lookup, FR-06.9 empty result handling, FR-07.2 100-card invariant during corrections. 2 additional test cases (multi-color, budget stress). OQ-5 resolved as out-of-scope. |

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/02-refine/po/prd.md
SUMMARY: PRD v1.1 — 13 findings addressed: 3 blocking, 2 must-fix, 4 recommended, 4 warnings. No regressions.
```
