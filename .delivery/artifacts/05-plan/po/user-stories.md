# User Stories: MTG Commander Deck Builder Plugin

**Version**: 1.0
**Date**: 2026-04-01
**Author**: Product Owner (Gandalf)
**Project Type**: GREENFIELD
**Pipeline**: Idea > Refine > Design > Architect > Plan > Development > UAT
**PRD Reference**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Architecture Reference**: `.delivery/artifacts/04-architect/solution/architecture.md` v1.0

> *"Do not be too eager to deal out stories in point estimation. Even the wisest PO cannot see all dependency chains. But I can see eight of them, and that shall be enough."*

---

## Capacity Declaration

| Metric | Value |
|--------|-------|
| Sprint capacity | 8 stories |
| Total story points | 42 |
| Python script stories | Code-level estimates (higher tier) |
| Markdown/reference stories | One tier lower estimates |
| Sprint count | 1 (single sprint delivery) |
| Max correction cycles | Per `pipeline.max_self_correction` in config |

---

## Story Map

| ID | Story | Priority | Source | Points | Dependencies | Type |
|----|-------|----------|--------|--------|-------------|------|
| US-01 | Plugin scaffold | P0 | FR-01 | 2 | None | Markdown + config |
| US-02 | Scryfall API client script | P0 | FR-06 | 8 | US-01 | Python script |
| US-03 | Reference files | P0 | PRD S7, Architecture S2 | 5 | US-01 | Markdown (7 files) |
| US-04 | SKILL.md orchestrator + Deck Builder agent | P0 | FR-02, FR-07 | 8 | US-01, US-02, US-03 |  Markdown (prompt engineering) |
| US-05 | Rules Judge agent | P0 | FR-03 | 5 | US-04 | Markdown (prompt engineering) |
| US-06 | Optimization Reviewer agent | P0 | FR-04 | 5 | US-04 | Markdown (prompt engineering) |
| US-07 | Price Evaluator agent | P0 | FR-05 | 4 | US-04 | Markdown (prompt engineering) |
| US-08 | Dogfooding validation | P0 | PRD S8, G-01 through G-06 | 5 | US-01 through US-07 | End-to-end testing |
| | **Total** | | | **42** | | |

### Dependency Graph

```
US-01 (scaffold)
  ├── US-02 (card_lookup.py)
  ├── US-03 (references)
  │
  └──┬── US-04 (SKILL.md + Deck Builder)
     │     ├── US-05 (Rules Judge)
     │     ├── US-06 (Optimization Reviewer)
     │     └── US-07 (Price Evaluator)
     │
     └──── US-08 (dogfooding) ← depends on ALL above
```

---

## US-01: Plugin Scaffold

**As a** plugin developer,
**I want** the `mtg-commander/` directory structure, LICENSE, and marketplace registration created,
**So that** subsequent stories have a valid plugin skeleton to build upon.

**Story Points**: 2 (markdown-only, no logic)

### Acceptance Criteria

| AC | Criterion | Source |
|----|-----------|--------|
| 1.1 | Directory `mtg-commander/` exists at repo root (kebab-case) | FR-01.1 |
| 1.2 | `mtg-commander/SKILL.md` exists (stub with frontmatter only -- content in US-04) | FR-01.2 |
| 1.3 | `mtg-commander/LICENSE.txt` exists with Apache 2.0 text | FR-01.3 |
| 1.4 | Plugin registered in `.claude-plugin/marketplace.json` with name `mtg-commander`, description, source `"./"`, skills `["./mtg-commander"]` | FR-01.4 |
| 1.5 | Subdirectories `references/` and `scripts/` exist under `mtg-commander/` | FR-01.5 |
| 1.6 | No `agents/`, `skills/`, `hooks/`, `plugin.json`, or `.mcp.json` created (per architecture ADR-001, v1 scope) | Architecture S2 |
| 1.7 | `api.scryfall.com` documented as required WebFetch domain in SKILL.md stub | FR-01.7 |

### Test Cases

| # | Test | Expected Result |
|---|------|----------------|
| T1.1 | `ls mtg-commander/` | Shows `SKILL.md`, `LICENSE.txt`, `references/`, `scripts/` |
| T1.2 | `cat .claude-plugin/marketplace.json \| python -m json.tool` | Valid JSON, contains entry with `"name": "mtg-commander"` |
| T1.3 | `cat mtg-commander/SKILL.md` | Contains frontmatter with name, description, license fields; mentions `api.scryfall.com` |
| T1.4 | `ls mtg-commander/agents/ 2>&1` | Directory does not exist (expected) |

### Dependencies

None. This is the foundation story.

---

## US-02: Scryfall API Client Script (Card Finder)

**As an** agent in the deck builder pipeline,
**I want** a Python script (`scripts/card_lookup.py`) that queries the Scryfall API for card data,
**So that** I can validate card names, search for cards, fetch prices, and perform batch lookups without external dependencies.

**Story Points**: 8 (Python script with 6 CLI commands, rate limiting, error handling, batch splitting)

### Acceptance Criteria

| AC | Criterion | Source |
|----|-----------|--------|
| 2.1 | Script located at `mtg-commander/scripts/card_lookup.py` | FR-06.6 |
| 2.2 | Uses only Python standard library (`urllib`, `json`, `time`, `sys`, `argparse`) -- zero pip dependencies | FR-06.6, NFR-02 |
| 2.3 | `validate` command: queries `/cards/named?exact=<name>`, returns `{"found": true/false, ...}`. Falls back to fuzzy match with "did you mean?" on exact miss. | FR-06.7, Architecture S5.2 |
| 2.4 | `search` command: queries `/cards/search?q=<query>` with support for oracle text, color identity, type line, mana value, Commander legality filters | FR-06.1 |
| 2.5 | `batch` command: queries `/cards/collection` (POST) with up to 75 identifiers per request. Splits 100-card decks into 2 requests (1-75, 76-100). Returns `data` (found) and `not_found` arrays. | FR-06.8, Architecture S5.7 |
| 2.6 | `price` command: fetches cheapest USD printing price. Handles null USD by trying `usd_foil`, then other printings. Flags "price unavailable" if all null. | FR-05.1, FR-05.8 |
| 2.7 | `batch-price` command: batch pricing for full decklists via `/cards/collection` | Architecture S5.1 |
| 2.8 | `random-commander` command: searches `/cards/search?q=is:commander id:<colors>` for commander suggestions | Architecture S5.1 |
| 2.9 | Rate limiting: minimum 75ms delay between consecutive API requests (Scryfall asks 50-100ms; 75ms safe middle) | FR-06.4, Architecture S5.4 |
| 2.10 | Error handling: 404 returns `{"found": false}`, 422 returns query echo, 429 retries with exponential backoff (1s, 2s, 4s, max 3 retries), 5xx retries once after 2s, timeout at 10s with one retry | FR-06.5, NFR-06, Architecture S5.5 |
| 2.11 | Returns normalized card data model: name, mana_cost, cmc, type_line, oracle_text, color_identity, legalities, price_usd, set_name, keywords, found | FR-06.2, Architecture S5.6 |
| 2.12 | When search returns zero results, returns `{"results": [], "query": "<original query>"}` | FR-06.9 |
| 2.13 | Handles double-faced/split/adventure cards: accepts front face name or full `//`-separated name, combines oracle text from all faces, uses combined color identity | Architecture S5.3 |
| 2.14 | Script outputs JSON to stdout for machine parsing by agents | Architecture S5.1 |

### Test Cases

| # | Test | Expected Result |
|---|------|----------------|
| T2.1 | `python card_lookup.py validate --name "Sol Ring"` | `{"found": true, "name": "Sol Ring", ...}` |
| T2.2 | `python card_lookup.py validate --name "Totally Fake Card Name"` | `{"found": false, ...}` |
| T2.3 | `python card_lookup.py validate --name "Sol Rign"` | Fuzzy match returns `{"found": false, "did_you_mean": "Sol Ring"}` |
| T2.4 | `python card_lookup.py search --query "oracle:sacrifice type:creature id:B legal:commander"` | JSON array of matching cards with required fields |
| T2.5 | `python card_lookup.py batch --names "Sol Ring" "Dark Ritual" "Totally Fake"` | `data` contains Sol Ring and Dark Ritual; `not_found` contains "Totally Fake" |
| T2.6 | `python card_lookup.py price --name "Sol Ring"` | Returns `{"name": "Sol Ring", "price_usd": "<some number>", ...}` |
| T2.7 | `python card_lookup.py search --query "name:xyznotacard"` | Returns `{"results": [], "query": "name:xyznotacard"}` |
| T2.8 | `python card_lookup.py validate --name "Delver of Secrets"` | Returns found=true (front face of DFC accepted) |
| T2.9 | Run 5 rapid successive commands | Rate limiter enforces >= 75ms gaps (no 429 errors) |

### Dependencies

- **US-01**: Plugin directory must exist

---

## US-03: Reference Files

**As the** deck builder pipeline,
**I want** 7 reference files containing MTG domain knowledge,
**So that** each sub-agent loads only the context it needs to perform its role accurately.

**Story Points**: 5 (7 markdown files with domain-specific content -- one tier lower than code, but significant research and accuracy required)

### Acceptance Criteria

| AC | Criterion | Source |
|----|-----------|--------|
| 3.1 | `references/commander-rules.md` covers: format rules, color identity rules (including hybrid mana), singleton rule, commander tax, combat damage, command zone, partner rules (for rejection message per FR-02.10), mulligan rules | PRD S7 |
| 3.2 | `references/banned-list.md` contains the current Commander banned list sourced from mtgcommander.net. Each entry is the exact Scryfall card name. | PRD S7 |
| 3.3 | `references/archetype-patterns.md` covers at minimum: aristocrats, voltron, spellslinger, tribal, combo, stax, group hug, mill, reanimator, +1/+1 counters, lifegain/drain, superfriends, tokens. Each archetype includes: typical category distribution, key synergy patterns, commander suggestions. | PRD S7 |
| 3.4 | `references/structural-minimums.md` defines category targets by power level tier: casual (1-4), mid (5-7), high (8-9), cEDH (10). Covers: ramp (10+), card draw (10+), removal (5+), board wipes (2+), lands (34-40), win conditions (3+). Adjustments for average mana value noted. | PRD S7, FR-04.3, FR-04.4 |
| 3.5 | `references/synergy-taxonomy.md` defines the 6 interaction categories (Triggers, Enables, Protects, Combos-with, Amplifies, Feeds) with definitions, examples, and the 3 exclusion rules. Uses structured tag format: `[CATEGORY: target_card]` | PRD FR-04.1, Architecture S4.1 |
| 3.6 | `references/intake-questions.md` defines the 7 questions with: question text, valid input ranges, default values, validation rules, Mode A/B/C detection logic (per UX spec) | PRD S7, FR-02.1 |
| 3.7 | `references/api-reference.md` covers: Scryfall endpoints used (`/cards/named`, `/cards/search`, `/cards/collection`), query syntax (Scryfall search syntax), rate limit policy, response schemas, error codes, and the card data model | PRD S7, Architecture S5 |

### Test Cases

| # | Test | Expected Result |
|---|------|----------------|
| T3.1 | `ls mtg-commander/references/` | Shows all 7 `.md` files |
| T3.2 | `grep -l "banned" mtg-commander/references/banned-list.md` | File exists and contains banned card entries |
| T3.3 | Banned list contains "Lutri, the Spellchaser" | Current banned card present (validates currency) |
| T3.4 | `grep -c "TRIGGERS\|ENABLES\|PROTECTS\|COMBOS-WITH\|AMPLIFIES\|FEEDS" mtg-commander/references/synergy-taxonomy.md` | All 6 categories defined |
| T3.5 | Structural minimums file defines targets for power levels 1-4, 5-7, 8-9, 10 | Four tiers present with numeric targets |
| T3.6 | Archetype patterns file covers at least 10 archetypes | 10+ archetype headings present |
| T3.7 | API reference file documents `/cards/named`, `/cards/search`, `/cards/collection` endpoints | All 3 endpoints documented |

### Dependencies

- **US-01**: `references/` directory must exist

---

## US-04: SKILL.md Orchestrator + Deck Builder Agent

**As a** user who wants to build a Commander deck,
**I want** a SKILL.md that handles intake, validates my commander, sequences the 4 agents, manages correction cycles, and formats the final output,
**So that** I get a complete, validated, optimized, budget-compliant decklist in a single session.

**Story Points**: 8 (complex orchestrator with intake modes, agent prompt templates, correction routing, output assembly -- prompt engineering at its densest)

### Acceptance Criteria

#### Intake (FR-02)

| AC | Criterion | Source |
|----|-----------|--------|
| 4.1 | Presents 7 intake questions: color identity, commander name, strategy archetype, power level (1-10), meta alignment, budget (USD), card restrictions | FR-02.1 |
| 4.2 | Supports Mode A (all inline), Mode B (partial + sequential), Mode C (fully interactive) | FR-02.2, Architecture S3.2 |
| 4.3 | Commander name validated against Scryfall via `card_lookup.py validate` before proceeding. Invalid name halts intake with error and prompts for correction. | FR-02.3 |
| 4.4 | Commander validated against banned list before proceeding. Banned commander halts with ban explanation and prompts for alternative. | FR-02.3a |
| 4.5 | Color identity derived from validated commander card data (Scryfall `color_identity` field), not from user input alone. User-specified colors serve as cross-check. | FR-02.4 |
| 4.6 | If user specifies a partner commander (keyword "Partner" in card data), intake rejects with message that partners are not supported in v1 and prompts for single commander. | FR-02.10 |

#### Deck Builder Agent Template (FR-02)

| AC | Criterion | Source |
|----|-----------|--------|
| 4.7 | Deck Builder sub-agent spawned via `Agent` tool with prompt template including contents of `archetype-patterns.md`, `synergy-taxonomy.md`, `structural-minimums.md`, `intake-questions.md` | Architecture S4.2 |
| 4.8 | Output is exactly 100 cards including commander | FR-02.5 |
| 4.9 | Every card assigned to exactly one category using disambiguation rule: assign to category with greatest structural deficit; if no deficit, assign by primary function relative to strategy | FR-02.6 |
| 4.10 | Output lists cards grouped by category with card name, mana cost, synergy rationale, and synergy tags per card | FR-02.7, Architecture S4.1 |
| 4.11 | Game plan documented in 2-3 sentences before card list | FR-02.8 |
| 4.12 | Every card name validated via `card_lookup.py` during construction. Cards failing validation excluded from output. | FR-02.9 |

#### Orchestration (FR-07)

| AC | Criterion | Source |
|----|-----------|--------|
| 4.13 | Pipeline sequences agents: Deck Builder > Rules Judge > Optimization Reviewer > Price Evaluator | FR-07.1 |
| 4.14 | On FAIL from any agent, routes violations + replacement suggestions back to Deck Builder for correction. Deck must remain exactly 100 cards after each correction. | FR-07.2 |
| 4.15 | Correction cycle limit from `pipeline.max_self_correction` in `.delivery/config.yml` (default 3). No new config mechanism introduced. | FR-07.3 |
| 4.16 | If max cycles exhausted, outputs best-effort decklist with warning listing remaining violations. Budget takes priority over synergy in irreconcilable conflicts. Budget-forced cards have synergy threshold relaxed to 2 interactions. | FR-07.4 |
| 4.17 | Final output includes: deck summary (commander, strategy, power level, total cost), cards by category, synergy score, budget breakdown, remaining warnings | FR-07.5 |
| 4.18 | Final output includes export-ready card list (one name per line, no annotations) for copy-paste to deck tools | FR-07.6 |
| 4.19 | Each agent's verdict (PASS/FAIL + details) preserved in output for transparency | FR-07.7 |

### Test Cases

| # | Test | Expected Result |
|---|------|----------------|
| T4.1 | Invoke skill with "Build me a K'rrik, Son of Yawgmoth commander deck, mono-black, graveyard recursion, power 7, mid-power casual, $150, no restrictions" (Mode A) | All 7 parameters extracted, no follow-up questions, pipeline starts |
| T4.2 | Invoke skill with "Build a commander deck" (Mode C) | Asks intake questions sequentially |
| T4.3 | Provide invalid commander name "Gandalf the Grey" | Intake halts with "card not found" error, prompts for correction |
| T4.4 | Provide "Lutri, the Spellchaser" as commander | Intake halts with banned commander message |
| T4.5 | Provide partner commander (e.g., "Thrasios, Triton Hero") | Intake rejects with "partners not supported in v1" message |
| T4.6 | Final output card count | Exactly 100 cards |
| T4.7 | Final output contains export block | One card name per line, no annotations |

### Dependencies

- **US-01**: Plugin skeleton
- **US-02**: `card_lookup.py` for commander validation and agent card lookups
- **US-03**: Reference files loaded into agent prompt templates

---

## US-05: Rules Judge Agent

**As the** orchestrator pipeline,
**I want** a Rules Judge sub-agent that validates format legality of the decklist using Scryfall data,
**So that** every output deck is provably legal with zero hallucinated card names.

**Story Points**: 5 (prompt template with 7 validation checks, structured verdict output, deterministic rules enforcement)

### Acceptance Criteria

| AC | Criterion | Source |
|----|-----------|--------|
| 5.1 | Validates exactly 100 cards in decklist (including commander) | FR-03.1 |
| 5.2 | Validates every card name exists in Scryfall via `card_lookup.py batch`. Zero tolerance for hallucinated names. | FR-03.2 |
| 5.3 | Validates every card's color identity is within commander's color identity (using Scryfall `color_identity` field) | FR-03.3 |
| 5.4 | Validates no card appears on Commander banned list (cross-referenced against `banned-list.md`) | FR-03.4 |
| 5.5 | Validates singleton rule: no duplicate card names except cards with names matching the 5 basic land types (Plains, Island, Swamp, Mountain, Forest) | FR-03.5 |
| 5.6 | Validates each card's format legality is "legal" in Commander format per Scryfall `legalities.commander` field | FR-03.6 |
| 5.7 | Audits synergy claims: when a synergy rationale references a mechanical interaction, validates that the oracle text supports the claim | FR-03.7 |
| 5.8 | Outputs structured verdict: PASS (all checks clear) or FAIL with list of violations. Each violation includes card name, rule violated, and suggested correction. | FR-03.8 |
| 5.9 | All legality decisions are deterministic -- based on Scryfall data, never AI-inferred | FR-03.9 |
| 5.10 | Agent prompt template loads `commander-rules.md` and `banned-list.md` as reference context | Architecture S4.3 |
| 5.11 | Agent uses `card_lookup.py batch` for name verification (preferred over individual lookups for full decklists) | FR-06.8, Architecture S4.3 |

### Test Cases

| # | Test | Expected Result |
|---|------|----------------|
| T5.1 | Submit a valid 100-card mono-black deck | Verdict: PASS, all checks show passing counts |
| T5.2 | Submit deck with 99 cards | Verdict: FAIL, violation: "card_count: 99/100" |
| T5.3 | Submit deck with a hallucinated card name "Shadowmaw Devourer" | Verdict: FAIL, violation: name not found in Scryfall |
| T5.4 | Submit mono-black deck containing "Swords to Plowshares" (white card) | Verdict: FAIL, violation: color identity {W} outside commander's {B} |
| T5.5 | Submit deck containing a banned card | Verdict: FAIL, violation: card on banned list |
| T5.6 | Submit deck with 2x "Lightning Bolt" | Verdict: FAIL, violation: singleton rule (non-basic land duplicate) |
| T5.7 | Submit deck with false synergy claim (e.g., "Blood Artist triggers on enchantment death") | Verdict: FAIL, violation: synergy audit -- oracle text does not reference enchantments |

### Dependencies

- **US-04**: Orchestrator spawns this agent and passes deck state

---

## US-06: Optimization Reviewer Agent

**As the** orchestrator pipeline,
**I want** an Optimization Reviewer sub-agent that enforces synergy-first philosophy and structural soundness,
**So that** every deck has meaningful card interactions and meets category minimums for its power level.

**Story Points**: 5 (prompt template with synergy counting, structural validation, mana curve analysis, replacement suggestions)

### Acceptance Criteria

| AC | Criterion | Source |
|----|-----------|--------|
| 6.1 | For every non-land card, identifies and lists interacting cards using synergy tags. Only interactions matching the 6 taxonomy categories (Triggers, Enables, Protects, Combos-with, Amplifies, Feeds) count toward threshold. | FR-04.1 |
| 6.2 | Flags any non-land card interacting with fewer than 3 other cards as "isolated" | FR-04.2 |
| 6.3 | Validates structural minimums: 10+ ramp, 10+ card draw, 5+ targeted removal, 2+ board wipes, 3+ win conditions | FR-04.3 |
| 6.4 | Validates land count between 34 and 40 (inclusive), with adjustment guidance for power level and average mana value | FR-04.4 |
| 6.5 | Produces mana curve distribution (0-1, 2, 3, 4, 5, 6, 7+) and flags front-loaded or top-heavy curves relative to strategy archetype | FR-04.5 |
| 6.6 | For each isolated card, suggests 1-2 replacements with 3+ interactions to existing cards (found via `card_lookup.py search`) | FR-04.6 |
| 6.7 | Outputs structured verdict: PASS (zero isolated cards, all minimums met) or FAIL with specific violations and replacement suggestions | FR-04.7 |
| 6.8 | Calculates deck synergy score: (total synergy connections across all non-land cards) / (number of non-land cards). Reports in verdict. Target: >= 3.0 | FR-04.8, G-02 |
| 6.9 | Agent prompt template loads `synergy-taxonomy.md` and `structural-minimums.md` as reference context | Architecture S4.4 |
| 6.10 | When budget constraints force substitutions (per FR-07.4), synergy threshold is relaxed to 2 interactions for affected cards with warning in verdict | FR-07.4 |

### Test Cases

| # | Test | Expected Result |
|---|------|----------------|
| T6.1 | Submit well-constructed deck with all cards having 3+ interactions | Verdict: PASS, synergy score >= 3.0 |
| T6.2 | Submit deck with a card having zero synergy tags | Verdict: FAIL, card flagged as isolated, replacements suggested |
| T6.3 | Submit deck with only 8 ramp sources | Verdict: FAIL, structural violation: "ramp: 8/10 (minimum 10)" |
| T6.4 | Submit deck with 42 lands | Verdict: FAIL, structural violation: "lands: 42 (max 40)" |
| T6.5 | Submit deck and verify mana curve output | Distribution across 0-1, 2, 3, 4, 5, 6, 7+ buckets present |
| T6.6 | Submit deck with synergy score 2.5 | Verdict: FAIL, synergy score below 3.0 threshold |

### Dependencies

- **US-04**: Orchestrator spawns this agent and passes deck state after Rules Judge PASS

---

## US-07: Price Evaluator Agent

**As the** orchestrator pipeline,
**I want** a Price Evaluator sub-agent that enforces budget compliance using live Scryfall pricing,
**So that** every deck respects the user's stated budget with real market prices, not estimates.

**Story Points**: 4 (prompt template with batch pricing integration, cap logic, budget alternatives -- simpler rules than US-05/06 but depends on live API data)

### Acceptance Criteria

| AC | Criterion | Source |
|----|-----------|--------|
| 7.1 | Retrieves current USD pricing for each card via `card_lookup.py batch-price`, using cheapest available printing | FR-05.1 |
| 7.2 | Calculates total deck cost as sum of all 100 cards' cheapest printing prices | FR-05.2 |
| 7.3 | Validates total cost does not exceed user-specified budget | FR-05.3 |
| 7.4 | Applies per-card cap: explicit cap if specified, otherwise defaults to 15% of total budget. Flags any card exceeding cap. | FR-05.4 |
| 7.5 | For over-budget or over-cap cards, suggests 1-2 budget-friendly alternatives that maintain synergy (via `card_lookup.py search`) | FR-05.5 |
| 7.6 | Outputs structured verdict: PASS (within budget, no cap violations) or FAIL with violations, current total, budget ceiling, and replacement suggestions | FR-05.6 |
| 7.7 | Reports price breakdown by category (Lands, Ramp, Card Draw, Removal, Board Wipes, Win Conditions, Synergy Pieces) | FR-05.7 |
| 7.8 | When Scryfall returns null USD price: tries cheapest non-foil printing. If no printing has USD price, flags as "price unavailable" and excludes from budget calculation with warning. | FR-05.8 |
| 7.9 | Agent prompt template loads `api-reference.md` as reference context | Architecture S4.5 |

### Test Cases

| # | Test | Expected Result |
|---|------|----------------|
| T7.1 | Submit 100-card deck with $150 budget where total is under $150 | Verdict: PASS, total cost < $150 |
| T7.2 | Submit deck with $100 budget where total is $127 | Verdict: FAIL, total $127 exceeds $100 budget, specific expensive cards identified |
| T7.3 | Submit deck with "no card over $10" restriction and deck contains a $15 card | Verdict: FAIL, card exceeds per-card cap, 1-2 alternatives suggested |
| T7.4 | Submit deck with no explicit per-card cap and $100 budget; deck contains a $20 card | Verdict: FAIL, card exceeds 15% default cap ($15), alternatives suggested |
| T7.5 | Verify output includes category price breakdown | Breakdown shows cost per category |
| T7.6 | Submit deck where a card has null pricing across all printings | Card flagged as "price unavailable", excluded from total with warning |

### Dependencies

- **US-04**: Orchestrator spawns this agent and passes deck state after Optimization Reviewer PASS

---

## US-08: Dogfooding Validation

**As the** delivery team,
**I want** all 5 test cases from PRD Section 8 run end-to-end through the completed pipeline,
**So that** we validate the plugin works before users ever touch it. Code review alone is not sufficient.

**Story Points**: 5 (end-to-end testing across all components -- not code, but requires full pipeline execution and result analysis)

### Acceptance Criteria

| AC | Criterion | Source |
|----|-----------|--------|
| 8.1 | **Test Case 1 (Mono-Black Graveyard)**: K'rrik, Son of Yawgmoth. Budget $150. Power 7. Pipeline produces 100 legal cards, synergy score >= 3.0, total cost <= $150, 10+ ramp, 10+ draw, zero banned, zero hallucinated names. | PRD S8 TC1, G-01 |
| 8.2 | **Test Case 2 (Orzhov Lifegain)**: Karlov of the Ghost Council. Budget $100, no card > $10. Power 6. Pipeline produces 100 legal cards, synergy >= 3.0, total <= $100, no card > $10, all WB identity, 10+ ramp, 10+ draw, zero banned. | PRD S8 TC2, G-01 |
| 8.3 | **Test Case 3 (Mono-Blue Mill)**: Bruvac the Grandiloquent. Budget $75. Power 5. No infinite combos. Pipeline produces 100 legal cards, synergy >= 3.0, total <= $75, all U identity, 10+ ramp, 10+ draw, no infinite combos flagged, zero banned. | PRD S8 TC3, G-01 |
| 8.4 | **Test Case 4 (Jund Sacrifice)**: Korvold, Fae-Cursed King. Budget $200. Power 8. Pipeline produces 100 legal cards, synergy >= 3.0, total <= $200, all BRG identity (no W, no U), 10+ ramp, 10+ draw, zero banned. Multi-color identity stress test. | PRD S8 TC4, G-01 |
| 8.5 | **Test Case 5 (4-Color Budget Stress)**: Atraxa, Praetors' Voice. Budget $50, no card > $5. Power 7. Pipeline produces 100 legal cards, synergy >= 3.0 (>= 2.0 acceptable if budget forces per FR-07.4), total <= $50, no card > $5, all WUBG identity (no R), 10+ ramp, 10+ draw, zero banned. Budget/synergy constraint negotiation test. | PRD S8 TC5, G-01 |
| 8.6 | Plugin passes `plugin-validator` with zero errors and zero warnings | G-06, FR-01.6, NFR-04 |
| 8.7 | All 5 runs complete within single sessions (no manual intervention between agents) | G-05, NFR-07 |
| 8.8 | Each test case run log preserved as evidence in `.delivery/artifacts/06-dev/developer/` | Dogfooding evidence |

### Test Cases

| # | Test | Expected Result |
|---|------|----------------|
| T8.1 | Run TC1: K'rrik graveyard | All pass criteria met (see AC 8.1) |
| T8.2 | Run TC2: Karlov lifegain | All pass criteria met (see AC 8.2) |
| T8.3 | Run TC3: Bruvac mill | All pass criteria met (see AC 8.3) |
| T8.4 | Run TC4: Korvold sacrifice | All pass criteria met (see AC 8.4) |
| T8.5 | Run TC5: Atraxa budget stress | All pass criteria met (see AC 8.5) |
| T8.6 | Run `plugin-validator` on `mtg-commander/` | Zero errors, zero warnings |
| T8.7 | Review run logs for manual intervention | Zero user prompts between agent handoffs |

### Dependencies

- **US-01 through US-07**: All stories must be complete. Dogfooding validates the integrated whole.

---

## Sprint Summary

| Metric | Value |
|--------|-------|
| Total stories | 8 |
| Total story points | 42 |
| Total acceptance criteria | 72 |
| Total test cases | 46 |
| Python script stories | 1 (US-02: 8 points) |
| Prompt engineering stories | 4 (US-04: 8, US-05: 5, US-06: 5, US-07: 4) |
| Markdown-only stories | 2 (US-01: 2, US-03: 5) |
| Dogfooding stories | 1 (US-08: 5) |
| Critical path | US-01 > US-02 + US-03 (parallel) > US-04 > US-05 + US-06 + US-07 (parallel) > US-08 |

---

## Estimation Rationale

| Story | Points | Rationale |
|-------|--------|-----------|
| US-01 | 2 | Pure scaffolding -- directory, LICENSE, marketplace entry, stub. No logic. |
| US-02 | 8 | Full Python script: 6 CLI commands, HTTP client, rate limiter, retry logic, batch splitting, error handling, JSON output. Highest code complexity in the project. |
| US-03 | 5 | 7 reference files requiring MTG domain accuracy. One tier lower than script code, but research-heavy and accuracy-critical (wrong banned list = wrong output). |
| US-04 | 8 | Most complex prompt template: 3 intake modes, commander validation, agent sequencing, correction routing, output assembly, export formatting. The brain of the pipeline. |
| US-05 | 5 | 7 deterministic validation checks, structured verdict, synergy audit. Complex rules but well-defined. |
| US-06 | 5 | Synergy counting across 60+ non-land cards, structural validation, mana curve analysis, replacement search. Analytically dense. |
| US-07 | 4 | Simpler rules than US-05/06 (price comparison + cap logic) but depends on live API data and null-price edge cases. |
| US-08 | 5 | 5 full pipeline runs, result analysis, evidence capture. Not code, but time-intensive and verdict-dependent. |

---

*"I have mapped the fellowship's journey. Eight stories. Forty-two points. Each card in these decks shall earn its place through synergy, not through the lazy counsel of popularity engines. The pipeline is the way. Trust it."*

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/po/user-stories.md
SUMMARY: 8 user stories, 42 points, 72 ACs, 46 test cases. Dependency-ordered: scaffold > script + refs > orchestrator > 3 agents > dogfooding.
```
