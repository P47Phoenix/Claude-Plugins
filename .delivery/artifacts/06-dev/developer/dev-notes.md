# Dev Notes: MTG Commander Deck Builder Plugin (GREENFIELD)

**Developer**: Gimli
**Date**: 2026-04-02
**Status**: CODE_COMPLETE
**Stories**: US-01 through US-07 (7 implemented, US-08 dogfooding pending)
**Sprint Plan**: v2.0 (4 sprints, 42 SP total)

> "Seventeen files forged. One plugin to build them all."

---

## Implementation Summary

| Sprint | Stories | SP | Status |
|--------|---------|:--:|--------|
| S1 | US-01 (scaffold), US-02 (Scryfall client) | 10 | DONE |
| S2 | US-03 (references), US-04 (orchestrator) | 13 | DONE |
| S3 | US-05 (Rules Judge), US-06 (Optimizer) | 10 | DONE |
| S4 | US-07 (Price Evaluator) | 4 | DONE |
| S4 | US-08 (dogfooding) | 5 | PENDING (empirical) |

## Files Created (13 total)

| File | Lines | Purpose |
|------|------:|---------|
| `SKILL.md` | ~400 | Orchestrator + 4 agent templates |
| `LICENSE.txt` | 201 | Apache 2.0 |
| `scripts/card_lookup.py` | 481 | Scryfall API client (6 commands, stdlib only) |
| `references/commander-rules.md` | ~80 | Format rules + color identity |
| `references/banned-list.md` | ~60 | 44 banned cards (live-fetched) |
| `references/archetype-patterns.md` | ~300 | 13 strategy archetypes |
| `references/structural-minimums.md` | ~150 | Category targets by power tier |
| `references/synergy-taxonomy.md` | ~120 | 6 interaction categories |
| `references/intake-questions.md` | ~100 | 7 intake questions with modes |
| `references/api-reference.md` | ~100 | Scryfall API + CLI reference |
| `references/rules-judge-guide.md` | ~200 | 7 legality checks |
| `references/optimizer-guide.md` | ~250 | 14-step synergy + structural eval |
| `references/price-evaluator-guide.md` | ~280 | Budget enforcement + replacements |

## Smoke Test Results

| Test | Result |
|------|--------|
| `card_lookup.py validate --name "Sol Ring"` | PASS — returns full card data |
| `card_lookup.py price --name "Sol Ring"` | PASS — returns $1.43 (cheapest printing) |
| `card_lookup.py validate --name "K'rrik, Son of Yawgmoth"` | PASS — commander legal, color_identity: [B] |
| `card_lookup.py batch --names "Sol Ring" "Dark Ritual"` | PASS — returns data array |
| `card_lookup.py search "o:draw c:b t:creature"` | PASS — returns search results |

## Empirical Validations Pending (US-08)

| Test Case | What Needs Validating |
|-----------|----------------------|
| TC-1 | K'rrik Mono-B Graveyard, $150 budget |
| TC-2 | Karlov Orzhov Lifegain, $100 + $10/card cap |
| TC-3 | Bruvac Mono-U Mill, $75 + no infinite combos |
| TC-4 | Korvold Jund Multi-color, $200 |
| TC-5 | Atraxa 4-color Budget Stress, $50 |

These require the full skill to be installed and invoked end-to-end.
