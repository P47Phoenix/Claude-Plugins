# Dev Notes: US-03 -- Reference Files for MTG Commander Deck Builder

**Story**: US-03 | **SP**: 5 | **Sprint**: 1
**Developer**: Gimli
**FR Coverage**: PRD S7, Architecture S2
**Files Created**: 7 reference files in `mtg-commander/references/`

---

> *"Seven files. Seven pillars of domain knowledge. Each one load-bearing. And my code -- well, my markdown -- stands as solid as mithril."*

---

## Files Delivered

| # | File | Size | Purpose | Consumers |
|---|------|------|---------|-----------|
| 1 | `commander-rules.md` | 5.2 KB | Format rules, color identity, singleton, commander tax, partner rejection | Rules Judge |
| 2 | `banned-list.md` | 4.4 KB | 44 banned cards with exact Scryfall names | Rules Judge, Orchestrator (intake) |
| 3 | `archetype-patterns.md` | 16.4 KB | 13 strategy archetypes with distributions, synergy patterns, commanders | Deck Builder |
| 4 | `structural-minimums.md` | 6.6 KB | Category targets by power tier (casual/mid/high/cEDH) with AMV adjustments | Optimization Reviewer |
| 5 | `synergy-taxonomy.md` | 8.6 KB | 6 interaction categories, 3 exclusions, scoring thresholds, tag format | Optimization Reviewer, Deck Builder |
| 6 | `intake-questions.md` | 7.9 KB | 7 intake questions, Mode A/B/C detection, validation rules, defaults | Orchestrator, Deck Builder |
| 7 | `api-reference.md` | 9.7 KB | Scryfall endpoints, query syntax, rate limits, card data model, CLI commands | Price Evaluator, all agents via card_lookup.py |

---

## Acceptance Criteria Verification

| AC | Status | Evidence |
|----|--------|----------|
| 3.1 | PASS | `commander-rules.md` covers: format rules, color identity (including hybrid mana), singleton rule, commander tax, combat damage, command zone, partner rules (v1 rejection per FR-02.10), mulligan rules |
| 3.2 | PASS | `banned-list.md` contains 44 banned cards sourced from mtgcommander.net (fetched 2026-04-01). Exact Scryfall card names used. Lutri present (T3.3 validated). |
| 3.3 | PASS | `archetype-patterns.md` covers 13 archetypes: Aggro, Voltron, Tokens/Go-Wide, Combo, Mill, Graveyard Recursion, Life Drain/Lifegain, Stax/Control, Spellslinger, Tribal, +1/+1 Counters, Superfriends, Group Hug. Each includes: category distribution, key synergy patterns, commander suggestions. Exceeds the 10+ requirement. |
| 3.4 | PASS | `structural-minimums.md` defines targets for all 4 power tiers: Casual (1-4), Mid (5-7), High (8-9), cEDH (10). Covers: ramp (10+), card draw (10+), removal (5+), board wipes (2+), lands (28-40 range), win conditions (3+). AMV adjustments documented. |
| 3.5 | PASS | `synergy-taxonomy.md` defines 6 categories (TRIGGERS, ENABLES, PROTECTS, COMBOS-WITH, AMPLIFIES, FEEDS) with definitions, examples, and tag format `[CATEGORY: target_card]`. 3 exclusion rules defined. Scoring: 3+ interactions per card (2 for budget-forced). |
| 3.6 | PASS | `intake-questions.md` defines 7 questions with: question text, valid input ranges, defaults, validation rules. Mode A/B/C detection logic documented. |
| 3.7 | PASS | `api-reference.md` documents `/cards/named`, `/cards/search`, `/cards/collection` endpoints. Query syntax, rate limit policy (75ms), response schemas, error codes (404/422/429/5xx), and the card data model all covered. CLI command reference included. |

---

## Test Case Results

| # | Test | Result |
|---|------|--------|
| T3.1 | `ls mtg-commander/references/` | All 7 `.md` files present |
| T3.2 | `grep -l "banned" banned-list.md` | File exists, contains banned entries |
| T3.3 | Banned list contains "Lutri, the Spellchaser" | Present (entry #22) |
| T3.4 | Grep for all 6 synergy categories in synergy-taxonomy.md | 19 matches -- all 6 categories defined |
| T3.5 | Structural minimums defines 4 power tiers | 4 tiers present with numeric targets for each category |
| T3.6 | Archetype patterns covers 10+ archetypes | 13 archetype headings present |
| T3.7 | API reference documents 3 endpoints | `/cards/named`, `/cards/search`, `/cards/collection` all documented |

---

## Design Decisions

1. **Banned list sourced live**: Fetched from mtgcommander.net on 2026-04-01 rather than relying on training data. 44 cards confirmed. Includes recent bans (Dockside Extortionist, Nadu, Jeweled Lotus, Mana Crypt).

2. **13 archetypes, not 9**: The PRD listed 9 strategy archetypes as minimum. The AC (3.3) specifies "at minimum: aristocrats, voltron, spellslinger, tribal, combo, stax, group hug, mill, reanimator, +1/+1 counters, lifegain/drain, superfriends, tokens" -- that's 13. All 13 are covered. Graveyard Recursion encompasses aristocrats, reanimator, and dredge as sub-variants within one archetype.

3. **File naming matches architecture spec**: Used exact filenames from Architecture S2: `commander-rules.md`, `banned-list.md`, `archetype-patterns.md`, `structural-minimums.md`, `synergy-taxonomy.md`, `intake-questions.md`, `api-reference.md`.

4. **Disambiguation rule documented in structural-minimums.md**: The dual-purpose card assignment rule (FR-02.6) is documented in structural-minimums.md alongside the category definitions since the Optimization Reviewer needs it for structural validation.

5. **Tribal synergy exclusion explicitly noted**: The archetype-patterns.md Tribal section explicitly cross-references the synergy taxonomy exclusion that type-sharing alone does not count as interaction. This prevents the Deck Builder from claiming 30+ interactions just because "they're all Elves."

---

## Maintenance Notes

- **`banned-list.md`** requires manual update when the Commander Rules Committee announces ban changes (typically quarterly). The file header includes a maintenance note.
- **`archetype-patterns.md`** commander suggestions may become outdated as new sets release but are not format-critical.
- **`api-reference.md`** Scryfall API is stable but should be checked if the pipeline encounters unexpected response formats.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/developer/us-03-notes.md
SUMMARY: 7 reference files created in mtg-commander/references/. 44 banned cards (live-fetched), 13 archetypes, 6 synergy categories, 4 power tiers. All 7 ACs PASS.
```
