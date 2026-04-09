# US-5 Developer Log

**Story:** Insert §0 "The Golden Rule" into volatility-decomposition.md
**Alias:** Gimli

## Files touched
- `delivery-team/skills/architect/references/volatility-decomposition.md` — inserted new §0 block between line 3 and the prior `## Core Principle` (original line 5). Inserted ~55 lines.

## AC coverage
- **AC-5.1:** §0 header present, rule stated explicitly as THE RULE, cited to Löwy, *Righting Software* Ch. 2, blockquoted.
- **AC-5.2:** "The Functional-Decomposition Trap" anti-pattern with worked order-processing example and a 4-row change-request table contrasting functional vs volatility cuts.

## Preservation
- No existing content altered. Phases 1–4, IDesign service tables, dependency rules all intact. Insertion is purely additive above `## Core Principle`.

## Verification
- `grep "Golden Rule"` → line 5 hit.
- `grep "Löwy"` → line 9 hit (with umlaut preserved).
- Markdown headers/tables render consistent with rest of file.

STATUS: DONE
