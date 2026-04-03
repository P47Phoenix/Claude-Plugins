# Dev Notes: US-05 -- Rules Judge Agent Reference File

**Story**: US-05 | **SP**: 5 | **Sprint**: 1
**FR Coverage**: FR-03 (AC 5.1 through 5.11)
**File Created**: `mtg-commander/references/rules-judge-guide.md`
**File Updated**: `mtg-commander/SKILL.md` (reference loading table + agent template)

---

## Implementation Summary

Created the Rules Judge validation guide -- the reference file the Rules Judge sub-agent reads for its step-by-step legality checklist. The file covers all 7 validation checks from FR-03, the structured verdict output format, the determinism guarantee, and replacement suggestion guidance.

Also updated the SKILL.md orchestrator in two places:
1. Reference loading table: added `references/rules-judge-guide.md` to the Rules Judge row
2. Agent 2 prompt template: added the guide as a third reference insert and added "Read `references/rules-judge-guide.md` for your validation checklist" instruction

## Structure

| Section | Content |
|---------|---------|
| Process Overview | Tool usage patterns, batch-mandatory rule |
| Check 1: Card Count | Exactly 100 including commander, common violations |
| Check 2: Card Name Verification | Batch validation, DFC/split handling, zero hallucination tolerance |
| Check 3: Color Identity | Subset comparison, hybrid mana, reminder text exclusion, colorless cards |
| Check 4: Banned List | Cross-reference against `banned-list.md`, exact string match |
| Check 5: Singleton Rule | Duplicate detection, 5 basic land exceptions only (Snow-Covered excluded) |
| Check 6: Format Legality | `legalities.commander` field check, redundant banned safeguard |
| Check 7: Synergy Audit | Oracle text verification of synergy claims, implicit interaction handling |
| Commander Legality | Pre-validation verification (legendary creature, no partner, not banned) |
| Output Format | PASS/FAIL verdict, VIOLATIONS list, WARNINGS list |
| Determinism Guarantee | Every check grounded in data, not inference |

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| 5.1 | PASS | Check 1 defines exactly-100 rule with commander included |
| 5.2 | PASS | Check 2 uses `card_lookup.py batch` with batch splitting at 75 |
| 5.3 | PASS | Check 3 validates color_identity subset with hybrid/DFC/colorless handling |
| 5.4 | PASS | Check 4 cross-references `banned-list.md` with exact name matching |
| 5.5 | PASS | Check 5 defines singleton with 5 basic land exceptions listed by name |
| 5.6 | PASS | Check 6 reads `legalities.commander` field from Scryfall data |
| 5.7 | PASS | Check 7 audits synergy claims against oracle text |
| 5.8 | PASS | Output format section defines PASS/FAIL verdict with violation structure |
| 5.9 | PASS | Determinism Guarantee section enforces data-only decisions |
| 5.10 | PASS | SKILL.md updated -- agent loads `commander-rules.md`, `banned-list.md`, and `rules-judge-guide.md` |
| 5.11 | PASS | Check 2 mandates batch validation over individual lookups |

## Design Decisions

- **Snow-Covered basics excluded from singleton exception**: The Commander rules are clear -- only the 5 named basic lands (Plains, Island, Swamp, Mountain, Forest) are exempt. Snow-Covered variants and Wastes follow singleton. This avoids a common rules misunderstanding.
- **Synergy audit severity**: False synergy claims are FAIL-worthy, not warnings. The synergy-first philosophy is the whole point of this deck builder. If a card claims interactions it does not have, the Deck Builder needs to fix it.
- **Warnings section added**: Non-blocking warnings for edge cases (upcoming bans, casual playgroup concerns, missing price data). These do not cause FAIL but surface useful information for downstream agents.
- **Commander re-verification**: The Rules Judge verifies the commander was validated correctly at intake. Belt and suspenders -- if intake missed something, the Judge catches it.

## Notes

- The guide deliberately mirrors the SKILL.md template's check ordering (1-7) for consistency.
- Replacement suggestion guidance uses `card_lookup.py search` with Scryfall query syntax, same pattern as other agents.
- The determinism guarantee section is blunt on purpose. The Rules Judge has no room for "probably legal" -- it is either data-verified or it is a violation.
