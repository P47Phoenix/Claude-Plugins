# Architecture: MTG Commander Deck Builder Plugin

**Version**: 1.0
**Date**: 2026-04-01
**Architect**: Celebrimbor (Solution Architect)
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**UX Spec**: `.delivery/artifacts/03-design/ux/design-spec.md` v1.0
**Project Type**: GREENFIELD

---

> *"Let us forge something that will endure beyond the ages. A pipeline of four agents, each a ring of power unto itself, yet bound together in one orchestrator to rule them all -- and in the synergy, bind them."*

---

## 1. Architecture Overview

The MTG Commander Deck Builder is a **single-skill Claude Code plugin** that orchestrates four domain-specialized sub-agents via the `Agent` tool. This follows the established delivery-team pattern: one SKILL.md as orchestrator, sub-agents spawned with isolated context from reference files, no persistent agent definitions.

### Core Architecture Decision

The user's design proposes 4 agents + 1 utility. This maps to the Claude Code plugin model as:

| User Design | Plugin Implementation | Rationale |
|------------|----------------------|-----------|
| Deck Builder (Agent 1) | Sub-agent via `Agent` tool | Spawned by SKILL.md with archetype + intake references |
| Rules Judge (Agent 2) | Sub-agent via `Agent` tool | Spawned with commander-rules + banned-list references |
| Optimization Reviewer (Agent 3) | Sub-agent via `Agent` tool | Spawned with synergy-taxonomy + structural-minimums references |
| Price Evaluator (Agent 4) | Sub-agent via `Agent` tool | Spawned with api-reference; invokes card_lookup.py for pricing |
| Card Finder (Utility) | Python script (`scripts/card_lookup.py`) | Invoked via `Bash` tool by any agent that needs Scryfall data |

**There are no agent definition files.** The existing plugin architecture (delivery-team, architect, developer, godot) uses the `Agent` tool with inline prompt templates in SKILL.md. Agent "definitions" are prompt templates that include the relevant reference file contents. See [ADR-001](../adrs/ADR-001.md) for the full decision record.

---

## 2. Plugin Directory Structure

```
mtg-commander/
├── SKILL.md                           # Orchestrator: intake, agent sequencing, output formatting
├── LICENSE.txt                        # Apache 2.0
├── references/
│   ├── commander-rules.md             # Format rules, color identity, singleton, commander tax
│   ├── banned-list.md                 # Current Commander banned list (manually maintained)
│   ├── archetype-patterns.md          # Strategy archetypes with synergy patterns, commander suggestions
│   ├── structural-minimums.md         # Ramp/draw/removal/land targets by power level tier
│   ├── synergy-taxonomy.md            # The 6 interaction categories + exclusion rules
│   ├── intake-questions.md            # 7 intake questions with validation rules, defaults, smart behaviors
│   └── api-reference.md              # Scryfall API endpoints, query syntax, rate limits, error codes
└── scripts/
    └── card_lookup.py                 # Card Finder utility: Scryfall API client (stdlib only)
```

### What Is NOT in the Directory

| Omitted Item | Why |
|-------------|-----|
| `agents/` directory | Claude Code plugins do not use agent definition files. Sub-agents are spawned via the `Agent` tool with prompt templates in SKILL.md. See ADR-001. |
| `skills/` directory | This plugin has one skill (the orchestrator). Sub-skills add value when a plugin has multiple independently-invocable capabilities. The 4 agents are pipeline stages, not independent skills. |
| `.mcp.json` | MCP server deferred to v2. Python script via Bash tool is sufficient. See ADR-002. |
| `hooks/` directory | Hooks deferred to v2 per PRD scope boundary. Agent validation is sufficient for v1. |
| `plugin.json` | This repo does not use plugin.json. Plugin registration is via `.claude-plugin/marketplace.json`. |

### Marketplace Registration

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

This entry is appended to the `plugins` array in `.claude-plugin/marketplace.json`.

---

## 3. SKILL.md Orchestrator Design

The SKILL.md follows the **delivery-flow pattern**: it is an orchestrator that delegates all domain work to sub-agents. It never produces deck content directly.

### 3.1 SKILL.md Frontmatter

```yaml
---
name: mtg-commander
description: >
  MTG Commander deck builder with multi-agent pipeline. Build synergy-dense,
  format-legal, budget-compliant 100-card Commander decklists. Synergy-first
  card selection via Scryfall API. Triggers on phrases like "build a commander
  deck", "MTG deck", "commander deck", "EDH deck", "build me a deck",
  "100-card deck", "commander pipeline", "deck builder".
license: Apache License 2.0 - See repository LICENSE file
---
```

### 3.2 Orchestrator Responsibilities

The SKILL.md handles:

1. **Intake extraction** -- Detects Mode A/B/C from the user's first message (per UX spec Section 1.1). Extracts parameters, identifies gaps, asks sequentially.
2. **Commander validation** -- Invokes `card_lookup.py` via Bash to validate the commander name against Scryfall before proceeding.
3. **Agent sequencing** -- Spawns the 4 sub-agents in order: Deck Builder > Rules Judge > Optimization Reviewer > Price Evaluator.
4. **Correction routing** -- When an agent returns FAIL, routes violations back to the Deck Builder sub-agent with correction instructions. Tracks cycle count (max from pipeline config, default 3).
5. **Output formatting** -- Assembles the final output: summary card, categorized deck list, agent verdicts, export list, purchase summary (per UX spec Section 5).
6. **Post-output actions** -- Handles approve/swap/rerun/adjust commands.

### 3.3 What the Orchestrator Does NOT Do

- Does not select cards (Deck Builder's job)
- Does not validate legality (Rules Judge's job)
- Does not evaluate synergy (Optimization Reviewer's job)
- Does not check prices (Price Evaluator's job)
- Does not call Scryfall directly (card_lookup.py's job, except for commander validation at intake)

---

## 4. Sub-Agent Definitions

Each sub-agent is spawned using the `Agent` tool with a prompt template. The template includes: role instructions, relevant reference file contents (read via `Read` tool before spawning), the deck state (shared artifact), and tool access declarations.

### 4.1 Shared Artifact: The Deck State

The deck state is a structured text artifact passed between agents. It is NOT persisted to disk -- it flows through the orchestrator as agent output/input.

**Deck State Format:**

```
DECK_STATE:
  commander: <name>
  color_identity: [<colors>]
  strategy: <archetype>
  power_level: <1-10>
  meta: <alignment>
  budget: <USD amount>
  per_card_cap: <USD amount or "15% of budget">
  restrictions:
    must_include: [<card names>]
    must_exclude: [<card names>]
    no_infinite_combos: <true/false>

CARDS:
  - name: <exact Scryfall name>
    category: <Commander|Ramp|Card Draw|Removal|Board Wipes|Win Conditions|Synergy Pieces|Lands>
    mana_cost: <{1}{B}{B} notation>
    synergy_rationale: <one sentence>
    synergy_tags: [<TRIGGERS:target>, <ENABLES:target>, ...]
    price_usd: <cheapest printing price or null>
  [... 99 more entries ...]

GAME_PLAN: <2-3 sentence description>
```

**Why structured text, not JSON:** The agents are Claude sub-agents that produce natural language output. Structured text with clear delimiters is more reliably produced and parsed by the model than strict JSON. The format uses YAML-like notation for readability but does not require a YAML parser -- the orchestrator pattern-matches on the structure.

**Synergy tags** use the structured tag format (e.g., `[TRIGGERS: Blood Artist]`, `[ENABLES: Cabal Coffers]`). This resolves OQ-1 from the PRD: structured tags enable automated counting by the Optimization Reviewer while remaining human-readable. Tags are drawn from the 6 taxonomy categories defined in `references/synergy-taxonomy.md`.

### 4.2 Deck Builder Sub-Agent

**Spawned by:** SKILL.md orchestrator (Phase 1, or during correction cycles)
**References loaded:** `archetype-patterns.md`, `intake-questions.md`, `synergy-taxonomy.md`, `structural-minimums.md`
**Tools available:** `Bash` (to invoke `card_lookup.py`)
**Input:** Intake parameters (initial run) or intake parameters + violation list (correction cycle)
**Output:** Complete deck state with 100 cards, synergy tags, game plan

**Prompt template structure:**

```
You are an expert MTG Commander deck builder. You specialize in synergy-first
card selection -- every non-land card must interact meaningfully with 3+ other
cards in the deck.

---
[CONTENTS OF archetype-patterns.md]
---
[CONTENTS OF synergy-taxonomy.md]
---
[CONTENTS OF structural-minimums.md]
---
[CONTENTS OF intake-questions.md]
---

## Task

[INITIAL BUILD or CORRECTION CYCLE with violations]

## Card Lookup

You have access to the Card Finder utility. To look up cards, use the Bash tool:

  python /path/to/mtg-commander/scripts/card_lookup.py search --query "oracle:sacrifice type:creature id:B legal:commander"
  python /path/to/mtg-commander/scripts/card_lookup.py validate --name "Blood Artist"
  python /path/to/mtg-commander/scripts/card_lookup.py batch --names "Sol Ring" "Dark Ritual" "Cabal Coffers"

Validate EVERY card name before including it in the deck. Do not include any
card that fails name validation (FR-02.9).

## Output

Produce the deck state in the format specified above. Exactly 100 cards.
Every non-land card must have synergy_tags listing specific interactions
with other cards in the deck.
```

### 4.3 Rules Judge Sub-Agent

**Spawned by:** SKILL.md orchestrator (Phase 2)
**References loaded:** `commander-rules.md`, `banned-list.md`
**Tools available:** `Bash` (to invoke `card_lookup.py`)
**Input:** Complete deck state from Deck Builder
**Output:** Structured verdict (PASS or FAIL with violations)

**Key behaviors:**
- Validates card names via batch lookup (`card_lookup.py batch`)
- Checks color identity by comparing each card's Scryfall color_identity against the commander's
- Checks banned list against `banned-list.md` reference
- Validates singleton rule (no duplicates except basic lands)
- Audits synergy claims by cross-referencing oracle text from Scryfall
- All checks are deterministic -- based on Scryfall data, never AI-inferred (FR-03.9)

**Verdict format:**

```
RULES_JUDGE_VERDICT: PASS|FAIL

CHECKS:
  card_count: 100/100
  names_verified: 100/100
  color_identity: 100/100
  banned_cards: 0
  singleton: PASS
  format_legality: 100/100
  synergy_audit: 0 false claims

VIOLATIONS: (only if FAIL)
  - card: <name>
    rule: <which rule violated>
    detail: <explanation>
    suggested_replacement: <card name>
```

### 4.4 Optimization Reviewer Sub-Agent

**Spawned by:** SKILL.md orchestrator (Phase 3)
**References loaded:** `synergy-taxonomy.md`, `structural-minimums.md`
**Tools available:** `Bash` (to invoke `card_lookup.py` for replacement suggestions)
**Input:** Complete deck state (post-Rules Judge pass)
**Output:** Structured verdict with synergy score, structural check, mana curve, isolated card list

**Key behaviors:**
- Reads synergy_tags from deck state and validates each against the taxonomy
- Counts interactions per non-land card; flags any with < 3 (or < 2 if budget-relaxed per FR-07.4)
- Validates structural minimums from `structural-minimums.md` based on power level
- Computes mana curve distribution
- Calculates deck synergy score: total interactions / non-land card count
- For isolated cards, uses `card_lookup.py search` to find replacements with 3+ interactions

### 4.5 Price Evaluator Sub-Agent

**Spawned by:** SKILL.md orchestrator (Phase 4)
**References loaded:** `api-reference.md`
**Tools available:** `Bash` (to invoke `card_lookup.py`)
**Input:** Complete deck state (post-Optimization Reviewer pass)
**Output:** Structured verdict with total cost, per-card prices, cap violations, category breakdown

**Key behaviors:**
- Uses `card_lookup.py batch-price` to fetch prices for all 100 cards
- Selects cheapest printing for each card (FR-05.1)
- Handles null prices per FR-05.8 (try cheapest non-foil printing, flag as "price unavailable" if none)
- Computes total cost, validates against budget
- Applies per-card cap (explicit or 15% of budget default)
- For over-budget/over-cap cards, uses `card_lookup.py` to find budget-friendly alternatives

---

## 5. Scryfall API Integration (Card Finder)

### 5.1 Script Design: `scripts/card_lookup.py`

A single Python script with CLI interface, using only standard library (`urllib.request`, `json`, `time`, `sys`, `argparse`).

**CLI Commands:**

| Command | Purpose | Scryfall Endpoint | Example |
|---------|---------|------------------|---------|
| `validate` | Check if a card name exists | `/cards/named?exact=<name>` | `card_lookup.py validate --name "Sol Ring"` |
| `search` | Find cards matching criteria | `/cards/search?q=<query>` | `card_lookup.py search --query "oracle:sacrifice type:creature id:B legal:commander"` |
| `batch` | Look up multiple cards at once | `/cards/collection` (POST) | `card_lookup.py batch --names "Sol Ring" "Dark Ritual"` |
| `price` | Get cheapest printing price | `/cards/search?q=!"<name>"&unique=prints&order=usd` | `card_lookup.py price --name "Sol Ring"` |
| `batch-price` | Get prices for many cards | `/cards/collection` (POST) | `card_lookup.py batch-price --names "Sol Ring" "Dark Ritual"` |
| `random-commander` | Find commanders by criteria | `/cards/search?q=is:commander id:<colors>` | `card_lookup.py random-commander --colors BG --strategy sacrifice` |

### 5.2 Design Decision: `validate` Uses `/cards/named?exact=`

This resolves **OQ-3** from the PRD. For name validation, we use Scryfall's `/cards/named` endpoint with the `exact` parameter:

- **Exact match is the correct semantic.** Name validation asks "does this exact card exist?" -- not "find cards similar to this name." Fuzzy matching would mask hallucinated names (e.g., "Demonic Consultancy" fuzzy-matches to "Demonic Consultation" but is a different card).
- **Faster.** Single card lookup, no pagination.
- **Fallback for typos.** If exact match fails, the script falls back to `/cards/named?fuzzy=<name>` and returns the suggestion with a "did you mean?" message. This gives the agent a correction path without silently accepting wrong names.

See [ADR-004](../adrs/ADR-004.md) for the full decision record.

### 5.3 Design Decision: Double-Faced / Split / Adventure Cards

This resolves **OQ-4** from the PRD.

Scryfall returns multi-faced cards with `//` separators (e.g., `"Delver of Secrets // Insectile Aberration"`). The Card Finder handles these as follows:

1. **Validation:** Accept either the full name (`"Delver of Secrets // Insectile Aberration"`) or the front face name alone (`"Delver of Secrets"`). Scryfall's `/cards/named?exact=` accepts both.
2. **Color identity:** Use the combined color identity of all faces (Scryfall provides this in the top-level `color_identity` field).
3. **Oracle text:** For synergy auditing, combine oracle text from all faces. Scryfall provides `card_faces[].oracle_text` for multi-faced cards.
4. **Pricing:** Use the card's price (Scryfall prices the physical card, not individual faces).
5. **Display:** In the deck list output, use the front face name only (e.g., "Delver of Secrets") for readability.

### 5.4 Rate Limiting Implementation

```python
import time

class RateLimiter:
    """Enforce minimum delay between Scryfall API requests."""

    def __init__(self, min_delay_ms=75):
        # 75ms default (Scryfall asks for 50-100ms; 75ms is safe middle)
        self.min_delay = min_delay_ms / 1000.0
        self.last_request_time = 0

    def wait(self):
        elapsed = time.monotonic() - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.monotonic()
```

### 5.5 Error Handling

| Scryfall Response | Card Finder Behavior |
|------------------|---------------------|
| 200 OK | Return parsed card data |
| 404 Not Found | Return `{"found": false, "query": "<original query>"}` |
| 422 Bad Request | Return error with query echoed back for debugging |
| 429 Rate Limited | Exponential backoff: wait 1s, 2s, 4s. Max 3 retries. Then return error. |
| 5xx Server Error | Retry once after 2s. Then return error with suggestion to check status.scryfall.com |
| Timeout (10s) | Retry once. Then return error. |
| Null USD price | Try `prices.usd_foil`. If null, try other printings via search. If all null, flag as "price unavailable". |

### 5.6 Card Data Model

The Card Finder returns a normalized subset of Scryfall's full response:

```python
{
    "name": "Blood Artist",              # Canonical name
    "mana_cost": "{1}{B}",               # Mana cost string
    "cmc": 2.0,                          # Converted mana cost
    "type_line": "Creature - Vampire",   # Type line
    "oracle_text": "Whenever Blood Artist or another creature dies, ...",
    "color_identity": ["B"],             # Color identity array
    "colors": ["B"],                     # Card colors
    "legalities": {"commander": "legal"},# Format legality map
    "price_usd": "1.49",                # Cheapest USD price (string or null)
    "set_name": "Avacyn Restored",       # Set of cheapest printing
    "scryfall_uri": "https://...",       # Link for reference
    "card_faces": null,                  # Non-null for double-faced cards
    "keywords": ["Partner", ...],        # Keywords (for partner detection)
    "found": true                        # Whether the card was found
}
```

### 5.7 Batch Endpoint Usage

The `/cards/collection` endpoint accepts up to 75 card identifiers per request. For a 100-card deck:

1. Split into 2 requests: cards 1-75, cards 76-100
2. Use `{"identifiers": [{"name": "Sol Ring"}, {"name": "Dark Ritual"}, ...]}` format
3. Response includes `data` (found cards) and `not_found` (missing identifiers)
4. Rate limit applies between the 2 requests (75ms delay)

This is the preferred method for validating or pricing complete decklists (FR-06.8). Individual lookups are reserved for replacement searches and commander validation.

---

## 6. Orchestration Flow

### 6.1 Pipeline Sequence

```
User Message
     |
     v
[SKILL.md: Intake Extraction]
     | Detect Mode A/B/C
     | Extract parameters
     | Validate commander (card_lookup.py validate)
     | Check banned list (reference)
     | Check partner keyword (reject if present)
     | Resolve all 7 parameters
     |
     v
[SKILL.md: Spawn Deck Builder Sub-Agent]
     | Read: archetype-patterns.md, synergy-taxonomy.md,
     |       structural-minimums.md, intake-questions.md
     | Pass: intake parameters
     | Agent produces: deck state (100 cards)
     |
     v
[SKILL.md: Spawn Rules Judge Sub-Agent]
     | Read: commander-rules.md, banned-list.md
     | Pass: deck state
     | Agent produces: verdict (PASS/FAIL)
     |
     +--[FAIL]--> Correction Router (see 6.2)
     |
     v  [PASS]
[SKILL.md: Spawn Optimization Reviewer Sub-Agent]
     | Read: synergy-taxonomy.md, structural-minimums.md
     | Pass: deck state
     | Agent produces: verdict with synergy score
     |
     +--[FAIL]--> Correction Router (see 6.2)
     |
     v  [PASS]
[SKILL.md: Spawn Price Evaluator Sub-Agent]
     | Read: api-reference.md
     | Pass: deck state + budget parameters
     | Agent produces: verdict with pricing
     |
     +--[FAIL]--> Correction Router (see 6.2)
     |
     v  [PASS]
[SKILL.md: Format Final Output]
     | Summary card
     | Categorized deck list with prices
     | Agent verdicts
     | Export list
     | Purchase summary
     | Post-output actions prompt
     |
     v
User Reviews Deck
```

### 6.2 Correction Cycle Implementation

When any agent returns FAIL:

1. **SKILL.md increments the correction counter** for the current cycle.
2. **SKILL.md extracts violations** from the failing agent's verdict.
3. **SKILL.md spawns a new Deck Builder sub-agent** with:
   - The current deck state
   - The violation list with suggested replacements
   - Instruction to apply corrections while maintaining exactly 100 cards
   - All original references (archetype-patterns, synergy-taxonomy, structural-minimums)
4. **The corrected deck state flows back** through the pipeline from the failing agent's position (not from the beginning).
5. **If correction counter reaches max** (from pipeline config `pipeline.max_self_correction`, default 3):
   - Apply budget priority rule (FR-07.4): relax synergy threshold to 2 for budget-forced swaps
   - Output best-effort deck with remaining warnings

**Correction re-entry point:** After correction, the pipeline re-enters at the agent that failed, not at the beginning. If the Rules Judge failed and corrections were applied, the corrected deck goes back to the Rules Judge, then proceeds to Optimization Reviewer and Price Evaluator. This avoids redundant re-validation of already-passed stages.

**Correction cycle counter scope:** One counter for the entire pipeline run, not per-agent. If the Rules Judge uses 1 cycle and the Price Evaluator uses 2, the total is 3 (max reached). This matches the existing pipeline config mechanism (FR-07.3).

### 6.3 Post-Output Actions

After final output, the orchestrator handles four commands:

| Command | Behavior |
|---------|----------|
| `approve` | Acknowledge completion. No further action. |
| `swap X Y` | Validate card Y via card_lookup.py. Check color identity, banned status, price. Re-run Optimization Reviewer for synergy impact. Update deck state and re-display affected sections. |
| `rerun` | Re-spawn the full pipeline with the same intake parameters. Fresh correction counter. |
| `adjust` | Prompt the user for which parameters to change. Then re-run pipeline with updated parameters. |

### 6.4 State Management

**No disk persistence in v1.** The deck state lives entirely in the conversation context, passed between sub-agents as text. This is sufficient because:

- The pipeline completes in a single session (G-05, NFR-07)
- The deck state (~100 cards with metadata) is well within Claude's context window
- No cross-session resume is needed for v1

**v2 consideration:** If deck modification mode is added, persisting deck state to a file would enable cross-session editing. The structured deck state format is designed to be file-compatible if needed.

---

## 7. Reference File Architecture

### 7.1 Reference Loading Strategy

Following the three-level context loading pattern:

1. **Metadata** (always loaded) -- marketplace.json entry tells Claude what the plugin does
2. **SKILL.md** (loaded when skill triggers) -- orchestrator instructions, intake logic, agent templates
3. **References** (loaded on demand) -- each sub-agent gets only the references it needs

| Reference File | Loaded By | Sub-Agent(s) That Use It |
|---------------|-----------|--------------------------|
| `commander-rules.md` | Orchestrator (before Rules Judge spawn) | Rules Judge |
| `banned-list.md` | Orchestrator (at intake + before Rules Judge spawn) | Rules Judge, Orchestrator (intake validation) |
| `archetype-patterns.md` | Orchestrator (before Deck Builder spawn) | Deck Builder |
| `structural-minimums.md` | Orchestrator (before Deck Builder + Opt Reviewer spawn) | Deck Builder, Optimization Reviewer |
| `synergy-taxonomy.md` | Orchestrator (before Deck Builder + Opt Reviewer spawn) | Deck Builder, Optimization Reviewer |
| `intake-questions.md` | Orchestrator (before Deck Builder spawn) | Deck Builder |
| `api-reference.md` | Orchestrator (before Price Evaluator spawn) | Price Evaluator |

### 7.2 Reference File Scope and Content

**`commander-rules.md`** -- The Rules Judge's source of truth.
- Commander format rules (100-card singleton, color identity, commander tax, command zone)
- Color identity derivation rules (mana cost + rules text + color indicators)
- Singleton exception: basic lands
- Commander damage rule (21 combat damage)
- Format-specific timing rules relevant to synergy auditing

**`banned-list.md`** -- A flat list of banned card names with ban dates.
- Sourced from mtgcommander.net
- Updated manually when bans are announced (quarterly)
- Format: one card name per line, with ban date

**`archetype-patterns.md`** -- The Deck Builder's strategy knowledge.
- Common archetypes: aristocrats, voltron, spellslinger, tribal, combo, stax, group hug, mill, reanimator, tokens, enchantress, equipment, superfriends, landfall, counters/proliferate, wheels, chaos, clone
- Per archetype: typical card categories, core synergy patterns, key card types, commander suggestions by color
- Power level adjustments (what changes at casual vs. mid vs. high vs. cEDH)

**`structural-minimums.md`** -- Targets by power level tier.
- 4 tiers: Casual (1-4), Mid (5-7), High (8-9), cEDH (10)
- Per tier: ramp count, draw count, removal count, board wipe count, land count range, win condition count
- Special adjustments for archetypes (e.g., spellslinger runs more draw, voltron runs more protection)
- Mana curve target shapes per tier

**`synergy-taxonomy.md`** -- The interaction classification system.
- 6 categories: Triggers, Enables, Protects, Combos-with, Amplifies, Feeds
- Per category: definition, examples, edge cases
- Explicit exclusion rules (shared creature type alone, generic mana enablement, "both good cards")
- Tag format specification: `[CATEGORY: target_card_name]`
- Scoring rules: how to count, how to compute deck synergy score

**`intake-questions.md`** -- The 7 questions with smart behavior rules.
- Question text, valid input ranges, defaults, smart derivation rules
- Mode A/B/C detection heuristics
- Commander suggestion logic (by color + strategy)
- Budget warning thresholds by color count
- Power level scale descriptions

**`api-reference.md`** -- Scryfall API integration guide.
- Endpoint documentation for `/cards/named`, `/cards/search`, `/cards/collection`
- Scryfall search syntax (oracle text, type, color identity, format legality)
- Rate limiting rules (50-100ms between requests)
- Response schema (relevant fields only)
- Error codes and handling
- Batch request format and limits (75 per request)

---

## 8. WebFetch Permission

The plugin requires `api.scryfall.com` added to the allowed WebFetch domains. This is documented in SKILL.md's setup instructions section.

**Note:** The `card_lookup.py` script uses `urllib.request` (via `Bash` tool), not `WebFetch`. However, Claude may also need to make direct web requests to Scryfall during intake (commander validation) or for ad-hoc lookups. Adding `api.scryfall.com` to WebFetch covers both paths.

The SKILL.md setup section will include:

```
## Setup

Before using this plugin, add `api.scryfall.com` to your allowed WebFetch
domains in Claude Code settings:

  Settings > Permissions > WebFetch > Add: api.scryfall.com
```

---

## 9. Open Question Resolutions

| # | Question | Resolution | Rationale |
|---|----------|-----------|-----------|
| OQ-1 | Structured tags vs. free text for synergy rationale? | **Both.** Structured tags (`[TRIGGERS: Blood Artist]`) for machine-countable interactions + one-sentence free-text rationale for human readability. | Tags enable the Optimization Reviewer to deterministically count interactions. Free text gives the user understanding. The UX spec shows both in the output. See ADR-003. |
| OQ-3 | `/cards/search` vs. `/cards/named` for name validation? | **`/cards/named?exact=` with fuzzy fallback.** | Exact match is the correct semantic for validation. Fuzzy fallback provides "did you mean?" corrections without silently accepting wrong names. See ADR-004. |
| OQ-4 | How to handle double-faced / split / adventure cards? | **Accept front face name or full name. Use combined color identity and oracle text.** | Scryfall handles both name forms. Combined identity/text ensures correct legality and synergy checking. See Section 5.3. |

---

## 10. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Card name hallucination despite pre-validation | Medium | High (core failure mode) | FR-02.9 pre-validation + Rules Judge batch validation + `card_lookup.py validate` at every stage. Three-layer defense. |
| Scryfall API downtime | Low | High (blocks entire pipeline) | Retry logic with backoff. Clear error message with status page link. No offline fallback in v1. |
| Sub-agent context window overflow | Low | Medium (agent cannot process full deck) | Deck state is ~100 entries x ~5 lines = ~500 lines. Well within window. Reference files are loaded selectively. |
| Synergy tags hallucinated by Deck Builder | Medium | Medium (false synergy claims) | Rules Judge audits synergy claims against oracle text. Optimization Reviewer validates tags against taxonomy categories. |
| Budget-synergy conflict causing infinite correction loops | Medium | Medium (exhausts cycles without resolution) | Correction counter is global (not per-agent). Budget priority rule (FR-07.4) relaxes synergy threshold. Best-effort output with warnings. |
| Scryfall price data lag vs. actual market prices | Low | Low (acceptable in v1) | Documented as a known limitation. Scryfall is source of truth for v1. |

---

## 11. Assumptions

1. **Scryfall API remains free and stable.** No API key required. Rate limits stay at 10 req/s.
2. **Claude's Agent tool supports the sub-agent pattern.** Each sub-agent can invoke Bash (for card_lookup.py) and Read (for reference files).
3. **100-card deck state fits comfortably in context.** Estimated at ~15-20K tokens with synergy tags and rationale.
4. **The Commander banned list changes infrequently.** Manual updates to `banned-list.md` are acceptable for v1.
5. **Users have internet access.** No offline mode.

---

## 12. Architecture Diagrams

### 12.1 Component Diagram (C4 Level 2)

```
+------------------------------------------------------------------+
|                     mtg-commander Plugin                          |
|                                                                   |
|  +------------------------------------------------------------+  |
|  |                    SKILL.md (Orchestrator)                  |  |
|  |  - Intake extraction (Mode A/B/C)                          |  |
|  |  - Commander validation                                     |  |
|  |  - Agent sequencing (4 stages)                              |  |
|  |  - Correction routing (max N cycles)                        |  |
|  |  - Output formatting                                        |  |
|  |  - Post-output actions                                      |  |
|  +-----+--------+--------+--------+---------------------------+  |
|        |        |        |        |                               |
|        v        v        v        v                               |
|  +---------+ +-------+ +-------+ +-------+                       |
|  |  Deck   | | Rules | | Opt.  | | Price |   (Sub-agents via     |
|  | Builder | | Judge | | Rev.  | | Eval. |    Agent tool)        |
|  +---------+ +-------+ +-------+ +-------+                       |
|        |        |        |        |                               |
|        +--------+--------+--------+                               |
|                 |                                                  |
|                 v                                                  |
|  +------------------------------------------------------------+  |
|  |           scripts/card_lookup.py (Card Finder)              |  |
|  |  - validate, search, batch, price, batch-price              |  |
|  |  - Rate limiting (75ms between requests)                    |  |
|  |  - Error handling (retry, backoff)                          |  |
|  +------------------------------+-----------------------------+  |
|                                 |                                 |
+------------------------------------------------------------------+
                                  |
                                  v
                        +------------------+
                        |  Scryfall API    |
                        |  api.scryfall.com|
                        +------------------+
```

### 12.2 Sequence Diagram (Happy Path)

```
User        SKILL.md       DeckBuilder   RulesJudge   OptReviewer  PriceEval   card_lookup.py  Scryfall
 |              |               |             |             |           |             |            |
 |--"build me"->|               |             |             |           |             |            |
 |              |--validate cmd------------------------------------------------>|            |
 |              |               |             |             |           |             |---req--->|
 |              |               |             |             |           |             |<--200----|
 |              |<--------------confirmed--------------------------------------------------------|
 |<--confirm----|               |             |             |           |             |            |
 |              |               |             |             |           |             |            |
 |              |--Agent(build)->|             |             |           |             |            |
 |              |               |--batch validate----------------------------------->|            |
 |              |               |             |             |           |             |---POST-->|
 |              |               |             |             |           |             |<--200----|
 |              |<-deck state---|             |             |           |             |            |
 |              |               |             |             |           |             |            |
 |              |--Agent(judge)------>|             |             |           |             |
 |              |               |             |--batch------------------------------->|            |
 |              |               |             |             |           |             |---POST-->|
 |              |               |             |             |           |             |<--200----|
 |              |<------PASS----------|             |             |           |             |
 |              |               |             |             |           |             |            |
 |              |--Agent(opt)----------->|             |           |             |            |
 |              |<---------PASS--------------|             |           |             |            |
 |              |               |             |             |           |             |            |
 |              |--Agent(price)----------------------------->|             |            |
 |              |               |             |             |           |--batch----->|            |
 |              |               |             |             |           |             |---POST-->|
 |              |               |             |             |           |             |<--200----|
 |              |<---------------------PASS-----------------|             |            |
 |              |               |             |             |           |             |            |
 |<-final deck--|               |             |             |           |             |            |
```

---

## 13. ADR Index

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](../adrs/ADR-001.md) | Single Skill with Agent Sub-Agents vs. Multi-Skill Plugin | Accepted |
| [ADR-002](../adrs/ADR-002.md) | Scryfall API Client -- Python Script vs. MCP Server | Accepted |
| [ADR-003](../adrs/ADR-003.md) | Synergy Representation -- Structured Tags + Free Text Hybrid | Accepted |
| [ADR-004](../adrs/ADR-004.md) | Card Name Validation -- Exact Match with Fuzzy Fallback | Accepted |

---

## 14. Next Steps

1. **Plan stage**: Break this architecture into user stories and sprint tasks
2. **Dev stage**: Implement in order: card_lookup.py first (enables all agents), then reference files, then SKILL.md with agent templates, then integration testing with 5 test cases
3. **UAT stage**: Dogfooding gate -- all 5 test cases must produce valid, synergy-dense, budget-compliant decklists

---

*"The work is laid out upon the anvil. Four agents, one orchestrator, seven references, one script. Each piece precisely fitted. The pipeline shall hold because each ring knows its purpose and none oversteps its bound. Let us forge."*

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/04-architect/solution/architecture.md
SUMMARY: Architecture mapped to Claude Code plugin conventions: single SKILL.md orchestrator, 4 sub-agents via Agent tool, card_lookup.py script, 7 refs. 4 ADRs.
```
