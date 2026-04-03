# DEFECT-001: Rules Judge missed color identity violation

**Pipeline**: run-2026-04-02-k3r9
**Test Case**: TC-2 (Karlov Orzhov Lifegain)
**Severity**: Critical (format legality)
**Category**: Agent validation gap

## Description
Sejiri Refuge (color identity: W/U) was included in a W/B (Orzhov) deck. The Rules Judge agent reported PASS on color identity check despite this card containing Blue mana — outside the commander's color identity.

## Evidence
- `card_lookup.py validate --name "Sejiri Refuge"` returns `color_identity: ['U', 'W']`
- Commander (Karlov) has `color_identity: ['W', 'B']`
- Blue is not in the commander's color identity → illegal card

## Root Cause
The Rules Judge agent prompt relies on the LLM to check color identity rather than using deterministic Scryfall API validation. The agent should batch-validate all cards via `card_lookup.py` and programmatically compare each card's `color_identity` array against the commander's.

## Fix
1. Rules Judge guide (`references/rules-judge-guide.md`) should mandate batch API validation for color identity — not LLM card knowledge
2. Consider adding a `validate-deck` command to `card_lookup.py` that takes a commander name + card list and returns all violations programmatically

## Impact
Any deck could contain color identity violations that the Rules Judge misses. This undermines the core format legality guarantee.
