# US-06 Dev Notes: Optimization Reviewer Agent

**Developer**: Gimli
**Date**: 2026-04-01
**Story Points**: 5
**Status**: DONE

---

## What Was Built

### `mtg-commander/references/optimizer-guide.md`

The Optimization Reviewer's complete evaluation process, forged from the requirements in FR-04 (PRD), Architecture S4.4, and the companion references (`synergy-taxonomy.md`, `structural-minimums.md`).

Contains 5 sections:

1. **Synergy Evaluation** -- Tag validation against 6 taxonomy categories, exclusion rule enforcement, isolated card flagging (< 3 interactions standard, < 2 budget-relaxed), deck synergy score calculation (target >= 3.0), top synergy card identification.

2. **Structural Checks** -- Category minimum validation by power level tier (ramp, draw, removal, wipes, win conditions, lands), mana curve analysis with archetype-specific assessment, AMV-based adjustments, win condition redundancy checks, removal sufficiency assessment.

3. **Replacement Suggestions** -- Search process for isolated card replacements and structural gap fills via `card_lookup.py search`. Budget-aware suggestion logic for FR-07.4 scenarios.

4. **Output Format** -- Structured verdict matching the SKILL.md template (OPTIMIZATION_VERDICT, SYNERGY_SCORE, STRUCTURAL_CHECKS, MANA_CURVE, TOP_SYNERGY_CARDS, ISOLATED_CARD_DETAILS, STRUCTURAL_VIOLATIONS, BUDGET_RELAXED_CARDS). Includes `average_mana_value` in mana curve output.

5. **Evaluation Sequence** -- 14-step ordered checklist from deck state parsing through verdict production. No steps skipped.

### SKILL.md Updates

- Updated Agent 3 spawn instruction to include `references/optimizer-guide.md` as the first reference read
- Updated the reference loading table to list `optimizer-guide.md` for the Optimization Reviewer

---

## Acceptance Criteria Coverage

| AC | Criterion | Covered In |
|----|-----------|-----------|
| 6.1 | Identify interactions using 6 taxonomy categories | Section 1.1, 1.2 |
| 6.2 | Flag cards with < 3 interactions as isolated | Section 1.3 |
| 6.3 | Validate structural minimums (ramp 10+, draw 10+, removal 5+, wipes 2+, wins 3+) | Section 2.1 |
| 6.4 | Validate land count 34-40 with adjustments | Section 2.3, 2.2 (AMV table) |
| 6.5 | Mana curve distribution (0-1, 2, 3, 4, 5, 6, 7+) with archetype assessment | Section 2.2 |
| 6.6 | Suggest 1-2 replacements for isolated cards via card_lookup.py search | Section 3.1 |
| 6.7 | Structured PASS/FAIL verdict with violations and replacements | Section 4 |
| 6.8 | Deck synergy score calculation, target >= 3.0 | Section 1.4 |
| 6.9 | Loads synergy-taxonomy.md and structural-minimums.md | SKILL.md update + Section header |
| 6.10 | Budget-forced relaxation to 2 interactions with warning | Sections 1.3, 3.3, 4 |

---

## Design Decisions

1. **14-step evaluation sequence**: Ordered explicitly to prevent shortcuts. Parse first, validate tags, apply exclusions, count, flag, score, check structure, suggest. No parallelism in evaluation -- each step depends on the prior.

2. **Archetype-aware curve assessment**: Added a table mapping archetype patterns (aggro, midrange, control, combo, reanimator) to expected curve shapes. A top-heavy aggro deck is a problem; a top-heavy reanimator deck is the plan. The SKILL.md template had "flag relative to strategy archetype" but no specifics -- this guide provides them.

3. **Win condition diversity check**: Added beyond the simple count minimum. Checking for diverse card types and at least one non-commander win condition. Commander removal is inevitable -- you need backup.

4. **AMV in output format**: Added `average_mana_value` to the MANA_CURVE section of the verdict output. The SKILL.md template did not include it, but the structural-minimums reference requires it for adjustment calculations. The Optimizer needs to show its work.

---

## Files Modified

| File | Change |
|------|--------|
| `mtg-commander/references/optimizer-guide.md` | Created (new file) |
| `mtg-commander/SKILL.md` | Updated Agent 3 spawn instruction and reference loading table |

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/developer/us-06-notes.md
SUMMARY: Created optimizer-guide.md with 14-step evaluation process covering synergy counting, structural checks, mana curve, replacements. Updated SKILL.md references.
```
