# Dev Notes: US-04 -- SKILL.md Orchestrator + Deck Builder Agent

**Story**: US-04 | **SP**: 8 | **Sprint**: 1
**FR Coverage**: FR-02 (Intake + Deck Builder), FR-07 (Orchestration)
**File Written**: `mtg-commander/SKILL.md` (complete overwrite of placeholder)

---

## Implementation Summary

Built the complete SKILL.md orchestrator implementing all 19 acceptance criteria from US-04. The file is the "brain of the pipeline" -- it handles intake, commander validation, agent sequencing, correction routing, output assembly, and post-output actions.

## Structure

| Section | Lines (approx) | Purpose |
|---------|----------------|---------|
| Frontmatter + Setup | 1-30 | Skill metadata, WebFetch domain requirement |
| Card Lookup Utility | 31-45 | Shared `card_lookup.py` invocation patterns |
| Intake Flow | 46-200 | Mode A/B/C detection, 7 questions, commander validation, partner rejection, budget warnings |
| Agent Pipeline | 201-280 | Pipeline banner, state tracking, reference loading table |
| Agent 1: Deck Builder | 281-400 | Full prompt template with deck state format, synergy tags, structural minimums, card lookup instructions |
| Agent 2: Rules Judge | 401-480 | Prompt template with 7 validation checks, structured verdict format |
| Agent 3: Optimization Reviewer | 481-570 | Prompt template with synergy scoring, structural checks, mana curve, replacement suggestions |
| Agent 4: Price Evaluator | 571-660 | Prompt template with batch pricing, cap logic, category breakdown, cost reduction plan |
| Correction Cycles | 661-730 | Routing logic, visibility format, budget-wins tiebreaker, max cycle exhaustion |
| Final Output | 731-850 | 6 output sections: summary card, categorized list, pipeline results, export list, purchase summary, post-output actions |
| Post-Output Actions | 851-890 | approve/swap/rerun/adjust handling |
| Error Handling | 891-940 | Scryfall failures, budget warnings, invalid commander, invalid restrictions |
| Conversational Tone | 941-960 | Tone guidelines and display restrictions |

## Acceptance Criteria Verification

### Intake (FR-02)

| AC | Status | Evidence |
|----|--------|----------|
| 4.1 | PASS | 7 intake parameters table with smart behavior and defaults |
| 4.2 | PASS | Mode A/B/C detection section with clear heuristics |
| 4.3 | PASS | Commander validation Step 1: Scryfall lookup via `card_lookup.py validate` |
| 4.4 | PASS | Commander validation Step 2: banned list check against `references/banned-list.md` |
| 4.5 | PASS | Commander validation Step 3: color identity derived from Scryfall `color_identity` field, user colors are cross-check |
| 4.6 | PASS | Commander validation Step 4: partner rejection with clear user-facing message |

### Deck Builder Agent Template (FR-02)

| AC | Status | Evidence |
|----|--------|----------|
| 4.7 | PASS | Agent spawned via Agent tool; prompt includes contents of archetype-patterns.md, synergy-taxonomy.md, structural-minimums.md, intake-questions.md |
| 4.8 | PASS | Output format requires exactly 100 cards; critical rule #1 |
| 4.9 | PASS | Category disambiguation rule in prompt: assign to category with greatest structural deficit |
| 4.10 | PASS | Output format includes name, category, mana_cost, synergy_rationale, synergy_tags per card |
| 4.11 | PASS | GAME_PLAN field in output format: 2-3 sentences |
| 4.12 | PASS | Card lookup section: "validate EVERY card name", "Do NOT include any card that fails" |

### Orchestration (FR-07)

| AC | Status | Evidence |
|----|--------|----------|
| 4.13 | PASS | Pipeline sequences: Deck Builder > Rules Judge > Optimization Reviewer > Price Evaluator |
| 4.14 | PASS | Correction cycle routing: violations + replacements back to Deck Builder, 100-card invariant enforced |
| 4.15 | PASS | Correction limit from `pipeline.max_self_correction` in `.delivery/config.yml` (default 3). No new config. |
| 4.16 | PASS | Max cycles exhausted section: best-effort output with warnings, budget priority, synergy relaxed to 2 |
| 4.17 | PASS | Final output Section 1-3: summary card, categorized list with prices, synergy score, budget breakdown, warnings |
| 4.18 | PASS | Final output Section 4: export-ready card list, one name per line, quantity notation for basic lands |
| 4.19 | PASS | Final output Section 3: pipeline results with each agent's verdict preserved |

## Design Decisions

1. **Agent prompts are templates, not executable code.** The `{TASK_BLOCK}`, `{deck_state}`, `{violation_list}` placeholders are filled by the orchestrator at spawn time. This follows the delivery-team pattern.

2. **Correction re-entry at failing agent, not pipeline start.** Per architecture Section 6.2. Avoids redundant re-validation of already-passed stages.

3. **Global correction counter, not per-agent.** One counter for the entire pipeline run (architecture Section 6.2). Rules Judge using 1 cycle + Price Evaluator using 2 cycles = 3 total (max).

4. **Deck state flows through conversation context, not disk.** Per architecture Section 6.4. The ~100-card structured state is well within context window. No file persistence in v1.

5. **Reference files loaded selectively per agent.** Each sub-agent gets only the reference files it needs (see Reference File Loading table). This keeps agent context focused.

6. **Budget warning at intake, not after Price Evaluator fails.** Per UX design Section 6.2: "Prevention is better than correction." Threshold heuristics by color count included.

## Dependencies Consumed

- US-01: Plugin skeleton (directory structure, marketplace registration)
- US-02: `scripts/card_lookup.py` (6 CLI commands referenced in all agent templates)
- US-03: All 7 reference files referenced by path in agent templates

## Known Constraints

- Agent prompt templates reference `${SKILL_DIR}` for script paths -- Claude Code resolves this at runtime.
- The orchestrator must Read reference files before passing their contents to sub-agents. This is explicit in the Reference File Loading section.
- The structured deck state format (YAML-like text, not JSON) is per architecture ADR-003 -- more reliably produced by Claude than strict JSON.
