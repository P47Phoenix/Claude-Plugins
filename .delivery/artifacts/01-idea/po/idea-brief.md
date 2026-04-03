## Idea Brief — GREENFIELD: MTG Commander Deck Builder Plugin

**Project Type**: GREENFIELD
**Date**: 2026-04-01
**Pipeline Routing**: GREENFIELD (Idea → Refine → Design → Architect → Plan → Dev → UAT)

---

### 1. Problem Statement

Building a Commander deck is a 100-card optimization problem wrapped in a creative expression problem. The format demands exactly 100 cards (singleton, except basic lands), all within a commander's color identity, with no banned cards — and that is merely the legality floor. A *good* deck requires every card to interact meaningfully with multiple other cards, sufficient mana acceleration, card advantage engines, and structural balance across the mana curve.

Today's tools fail this in predictable ways:

- **EDHREC and similar popularity aggregators** solve the wrong problem. They surface the most *popular* cards, not the most *synergistic* cards for a specific commander and strategy. A card that appears in 80% of decks is not necessarily correct for *your* deck's game plan. Popularity-driven selection produces generically strong but strategically unfocused lists — decks that do everything adequately and nothing exceptionally.
- **Manual deck building** requires deep format knowledge, extensive card pool familiarity (30,000+ legal cards), and iterative playtesting to identify synergy gaps. A skilled player spends 4-8 hours building a tuned list. A newer player may never achieve structural soundness without guidance.
- **Existing AI-assisted tools** lack format-specific validation. They hallucinate card names, ignore color identity restrictions, suggest banned cards, and cannot verify that card interactions actually work within Magic's rules framework. There is no rules judge in the loop.
- **Budget awareness is an afterthought**. Most tools suggest optimal cards regardless of cost. A player with a $100 budget does not benefit from being told to run Mana Crypt ($180). Budget must be a constraint that shapes the entire build, not a filter applied after the fact.

The core philosophy this plugin must embody: **Synergy first. Always.** Every card in a deck must interact meaningfully with 3 or more other cards. Popularity is a tiebreaker, never a selection criterion.

---

### 2. Vision

A multi-agent Claude Code plugin where specialized agents collaborate to produce Commander decks that are format-legal, synergy-dense, structurally sound, and budget-compliant — in a single pipeline run.

The user invokes the plugin, answers 7 intake questions (or provides them upfront), and receives a complete 100-card decklist that has been:

1. **Built** by a Deck Builder agent who understands Commander archetypes and synergy-first card selection
2. **Judged** by a Rules Judge agent who verifies format legality, color identity compliance, card interaction accuracy, and timing correctness
3. **Optimized** by a Reviewer agent who flags isolated cards (fewer than 3 synergy connections), checks structural minimums (ramp, draw, removal, lands), and evaluates mana curve distribution
4. **Priced** by a Price Evaluator agent who enforces total budget, per-card caps, and identifies cheapest printings

Each agent has a clear responsibility boundary. The pipeline is sequential with feedback loops — if the Rules Judge finds illegal cards or the Optimizer flags synergy failures, the deck cycles back to the Builder for correction. The output is a deck that satisfies all four agents simultaneously.

This is not a card recommendation engine. It is a deck *construction* pipeline with built-in quality gates.

---

### 3. Agent Architecture

The spec defines 4 primary agents and 1 utility sub-agent. Here is how they map to the Claude Code plugin architecture:

#### Plugin Component Mapping

| Spec Agent | Plugin Component | Rationale |
|------------|-----------------|-----------|
| **Deck Builder (Agent 1)** | Skill with agent sub-agent | Intake specialist + initial architect. Handles the 7 intake questions and produces the initial 100-card list with category assignments. This is the pipeline entry point. |
| **Rules Judge (Agent 2)** | Agent sub-agent | Stateless validation pass. Checks format legality, color identity, banned list, card interaction accuracy, and timing rules. References official rules sources. No creative decisions — pure rules enforcement. |
| **Optimization Reviewer (Agent 3)** | Agent sub-agent | Synergy-first evaluation. Flags cards with fewer than 3 interactions. Checks structural minimums (10+ ramp, 10+ draw, removal suite, land count). Evaluates mana curve. Suggests replacements. |
| **Price Evaluator (Agent 4)** | Agent sub-agent + MCP integration | Budget enforcement. Needs live pricing data from Scryfall API. Checks total budget, per-card caps, identifies cheapest printings across sets. |
| **Card Finder (Utility)** | Shared utility (script or MCP tool) | On-demand card lookup available to all agents. Priority chain: Recommander → Scryfall API → MTG JSON → EDHREC (tiebreaker only). |

#### Plugin Directory Structure (Proposed)

```
mtg-commander/
├── SKILL.md                    # Primary skill: intake, orchestration, output format
├── LICENSE.txt
├── agents/
│   ├── deck-builder.md         # Agent 1: intake + initial build
│   ├── rules-judge.md          # Agent 2: legality validation
│   ├── optimization-reviewer.md # Agent 3: synergy + structure checks
│   └── price-evaluator.md      # Agent 4: budget enforcement
├── references/
│   ├── commander-rules.md      # Format rules, banned list, color identity rules
│   ├── archetype-patterns.md   # Known archetypes, synergy patterns, category templates
│   ├── structural-minimums.md  # Ramp/draw/removal/land targets by power level
│   ├── intake-questions.md     # The 7 intake questions with validation
│   └── api-reference.md        # Scryfall API patterns, rate limits, endpoints
├── scripts/
│   └── card_lookup.py          # Card Finder utility (Scryfall API client)
└── .mcp.json                   # MCP server config for Scryfall (if MCP approach chosen)
```

#### Pipeline Flow

```
User Input → Deck Builder (intake + build)
                 ↓
           Rules Judge (validate)
                 ↓ (fail → cycle back to Builder with corrections)
           Optimization Reviewer (synergy + structure)
                 ↓ (fail → cycle back to Builder with replacements)
           Price Evaluator (budget check)
                 ↓ (fail → cycle back to Builder with budget swaps)
           Output: Final 100-card decklist
```

The Card Finder is invoked on-demand by any agent that needs to look up card data, find alternatives, or verify card text.

---

### 4. External Dependencies

| Resource | Purpose | Access Model | Risk |
|----------|---------|-------------|------|
| **Scryfall API** | Card data, oracle text, legality, pricing, set printings | Free, public REST API. 50-100ms/request rate limit. | Low — well-documented, stable, community-standard. This is the primary data source. |
| **Recommander** | Synergy-based card recommendations | API/tool (needs investigation in Refine) | Medium — availability and API stability need verification. Fallback to Scryfall + heuristic synergy if unavailable. |
| **MTG JSON** | Bulk card data for offline reference | Free JSON downloads | Low — static data, versioned releases. Good fallback for card text when API is unavailable. |
| **EDHREC** | Popularity data (tiebreaker only) | Web scraping or API (if available) | Medium — no official API. Used only as tiebreaker, never as primary signal. Can be omitted in v1 without impact. |
| **Commander Banned List** | Format legality enforcement | mtgcommander.net (static page) | Low — changes infrequently (quarterly announcements). Can be maintained as a reference file with periodic updates. |
| **TCGPlayer / Card Kingdom** | Alternative pricing sources | APIs with varying access models | High — may require API keys, have rate limits, or terms restrictions. Scryfall pricing is sufficient for v1. |

**v1 dependency decision**: Scryfall API alone covers card data, oracle text, legality, and pricing. It is the minimum viable external dependency. Recommander adds significant synergy value but needs investigation. EDHREC, TCGPlayer, Card Kingdom, Moxfield, and Archidekt are all deferred to v2.

---

### 5. Target Users

| Persona | Experience Level | Primary Need | Key Constraint |
|---------|-----------------|-------------|----------------|
| **Experienced player, new commander** | Veteran (5+ years) | Wants to build around a specific commander they have not played before. Knows the format but not the card pool for that strategy. | Time — does not want to spend 6 hours on card research for a new archetype. |
| **New-to-Commander player** | Intermediate (knows Magic, new to Commander) | Needs a structurally sound 100-card list that actually works. Does not know the format's structural requirements. | Knowledge gap — does not know they need 10+ ramp sources or what a good mana curve looks like. |
| **Budget-conscious brewer** | Any level | Wants a competitive deck within a hard budget ceiling. Needs budget to shape selection, not just filter after the fact. | Budget — the $50-200 range where card choices are constrained and substitution quality matters. |
| **Returning player** | Lapsed (1-3 year gap) | Wants to build a deck with current card pool. May have outdated assumptions about what is legal or strong. | Currency — card pool has expanded significantly, banned list has changed, power level has shifted. |

---

### 6. Goals

1. **Produce format-legal 100-card Commander decklists** — Every output passes Rules Judge validation: exactly 100 cards including Commander, all within color identity, no banned cards, singleton compliance, valid card names (no hallucinations).
2. **Enforce synergy-first card selection** — Every non-land card in the deck interacts meaningfully with 3 or more other cards. The Optimization Reviewer gates this. Popularity is never a primary selection criterion.
3. **Meet structural minimums by power level** — 10+ ramp sources, 10+ card draw sources, appropriate removal suite, and land count calibrated to curve. These targets may flex with power level (a cEDH deck has different needs than a power-6 casual deck).
4. **Enforce budget compliance with real pricing** — Total deck cost and per-card caps enforced using Scryfall's pricing data. Cheapest printings identified. Budget shapes selection, not just filters it.
5. **Complete the pipeline in a single session** — User provides intake answers, receives a finished decklist. No "come back tomorrow" or manual intermediate steps. The pipeline handles corrections internally.
6. **Ship as a valid Claude Code plugin** — Registered in `marketplace.json`, follows plugin conventions (SKILL.md + agents + references + optional scripts/MCP), installable by any Claude Code user.

---

### 7. v1 Scope vs Future

#### v1 — This Pipeline Run

| Deliverable | Details |
|-------------|---------|
| **Plugin skeleton** | `mtg-commander/` directory with SKILL.md, agents/, references/, scripts/, LICENSE.txt. Registered in marketplace.json. |
| **Deck Builder agent** | 7 intake questions (color identity, commander, strategy archetype, power level 1-10, meta alignment, total budget, card restrictions). Produces categorized 100-card list. |
| **Rules Judge agent** | Format legality validation: color identity, banned list, singleton, card name verification via Scryfall. |
| **Optimization Reviewer agent** | Synergy audit (3+ interactions per card), structural minimum checks (ramp, draw, removal, lands), mana curve analysis. |
| **Price Evaluator agent** | Scryfall-based pricing. Total budget enforcement, per-card cap, cheapest printing identification. |
| **Card Finder utility** | Scryfall API client script. Card lookup, search, pricing, legality checks. |
| **Commander reference files** | Format rules, banned list, archetype patterns, structural targets, intake question definitions. |
| **3 test cases** | Mono-Black Graveyard, Orzhov Lifegain, Mono-Blue Mill — validated end-to-end through the full pipeline. |

#### Deferred to v2

| Item | Reason |
|------|--------|
| **Recommander integration** | Needs API investigation and fallback strategy. Scryfall + heuristic synergy is sufficient for v1. |
| **EDHREC integration** | No official API. Tiebreaker-only use case does not justify scraping complexity in v1. |
| **Multi-source pricing** (TCGPlayer, Card Kingdom) | Scryfall pricing covers v1 needs. Multi-source adds API key management and rate limit complexity. |
| **Moxfield / Archidekt export** | Output format standardization (MTGO, Arena, CSV) covers v1. Platform-specific export is a convenience feature. |
| **Deck modification mode** ("improve my existing deck") | Requires a different intake flow (paste existing list, identify weaknesses). v1 focuses on new builds. |
| **Persistent card database** (SQLite cache) | Scryfall API is fast enough for v1 volumes. Caching becomes valuable at scale or for offline use. |
| **Hooks** (validation on deck output) | The agents themselves provide validation. Hooks add value for automated CI-style checks but are not needed for v1 correctness. |
| **Meta-game analysis** | Tracking local or online meta trends to adjust recommendations. Requires data sources and ongoing maintenance. |

---

### 8. Constraints

- **Scryfall API rate limits**. Scryfall allows 10 requests/second for well-behaved clients. The Card Finder utility must respect this. Bulk endpoints should be preferred over individual card lookups where possible.
- **Card name accuracy is non-negotiable**. The number one failure mode of AI-assisted deck building is hallucinated card names. Every card name in the output must be verified against Scryfall. The Rules Judge agent gates this explicitly.
- **No local card database in v1**. The plugin does not bundle or maintain a local card database. All card data comes from Scryfall API at runtime. This keeps the plugin lightweight but requires internet access.
- **Plugin conventions**. Must follow the Claude-Plugins repo patterns: kebab-case directory, SKILL.md as primary skill file, marketplace.json registration, three-level context loading.
- **WebFetch permissions**. The plugin needs `api.scryfall.com` added to allowed WebFetch domains in settings. This must be documented in the plugin's setup instructions.
- **No AI-inferred legality decisions**. Format legality (banned list, color identity, singleton rule) must be checked against authoritative sources, not inferred by the model. This mirrors the Business Rules Engine philosophy: gate decisions are deterministic, not AI-variable.
- **Pipeline compliance**. This work routes through delivery-flow. All stages execute — GREENFIELD means no stages are skipped or lightened.
- **Dogfooding gate**. All 3 test cases must produce valid, synergy-dense, budget-compliant decklists before UAT passes. The team plays with the tool before the users do.

---

*Not all those who wander through 30,000 legal cards are lost — but most of them could use a wizard with a plan, a judge with a rulebook, a reviewer with sharp eyes, and an accountant who knows the price of power. This plugin assembles that fellowship. Synergy first. Always.*

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/01-idea/po/idea-brief.md
SUMMARY: GREENFIELD idea brief for MTG Commander Deck Builder plugin. 4 agents + Card Finder utility, Scryfall API, synergy-first philosophy. v1 scope defined, 6 items deferred to v2.
```
