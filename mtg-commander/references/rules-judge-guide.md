# Rules Judge Validation Guide

Reference document for the Rules Judge sub-agent. This is the step-by-step validation checklist for Commander format legality enforcement.

**Principle**: Every legality decision is deterministic -- based on Scryfall data fields, never AI-inferred. If you cannot verify a claim from card data, flag it.

---

## Validation Process Overview

Execute all 7 checks in order. Each check must complete before producing the final verdict. A single violation in any check results in an overall FAIL.

### Tools

Use `card_lookup.py` via the Bash tool for all Scryfall data:

```bash
# Individual card validation
python ${SKILL_DIR}/scripts/card_lookup.py validate --name "<card name>"

# Batch validation (preferred for full decklists -- splits at 75 per request)
python ${SKILL_DIR}/scripts/card_lookup.py batch --names "<card1>" "<card2>" "<card3>" ...

# Programmatic deck validation (color identity + legality + banned list)
python ${SKILL_DIR}/scripts/card_lookup.py validate-deck --commander "<commander_name>" --cards "<card1>" "<card2>" ...

# Search for replacement suggestions
python ${SKILL_DIR}/scripts/card_lookup.py search --query "<scryfall query>"
```

**Batch is mandatory for full-deck validation.** Do not validate 100 cards one at a time. Split into two batch calls: cards 1-75 and cards 76-100.

**`validate-deck` is mandatory for color identity, format legality, and banned list checks (Checks 3, 4, and 6).** Color identity validation MUST use the `validate-deck` programmatic command. NEVER rely on LLM knowledge of card color identity, format legality, or ban status. This is a determinism guarantee — LLM training data contains known errors (DEFECT-001: Sejiri Refuge misidentified as W/B instead of W/U). The `validate-deck` command queries Scryfall programmatically for each card and returns a violations array with every failure. No exceptions. No "I'm confident about this one." If it isn't verified by `validate-deck`, it is not verified.

---

## Check 1: Card Count

**Rule**: The deck must contain exactly 100 cards, including the commander.

**Procedure**:
1. Count every card entry in the deck state.
2. Verify the commander is included in the count.

**Pass condition**: Total count == 100.

**Common violations**:
- 99 cards (commander excluded from count by mistake)
- 101+ cards (correction cycle added replacements without removing originals)
- 98 cards (two cards removed, one added during correction)

**Verdict field**: `card_count: <N>/100`

---

## Check 2: Card Name Verification

**Rule**: Every card name must exist in Scryfall. Zero tolerance for hallucinated names.

**Procedure**:
1. Collect all 100 card names from the deck state.
2. Run batch validation:
   ```bash
   python ${SKILL_DIR}/scripts/card_lookup.py batch --names "<card1>" ... "<card75>"
   python ${SKILL_DIR}/scripts/card_lookup.py batch --names "<card76>" ... "<card100>"
   ```
3. Check the `not_found` array in each response.
4. Any card in `not_found` is a violation.

**Pass condition**: `not_found` is empty across all batch responses.

**Handling edge cases**:
- **Double-faced cards**: Accept the front face name (e.g., "Delver of Secrets") or the full name with "//" separator. The batch lookup handles both.
- **Split/Adventure cards**: Same rule -- front face name or full name accepted.
- **Fuzzy near-misses**: If a name fails but `did_you_mean` is available from a validate call, include the suggestion in the violation detail.

**Verdict field**: `names_verified: <N>/100`

---

## Check 3: Color Identity

**Rule**: Every card's color identity must be a subset of the commander's color identity.

**CRITICAL**: Never rely on your knowledge of card color identities. Always verify via the Scryfall API. LLM training data contains errors and confusions between similar card names. Use `validate-deck` for programmatic verification.

**Procedure**:
1. Run `validate-deck` to programmatically check all cards at once:
   ```bash
   python ${SKILL_DIR}/scripts/card_lookup.py validate-deck --commander "<commander_name>" --cards "<card1>" "<card2>" ... "<card99>"
   ```
2. Check the `violations` array in the output for any entries with `"type": "color_identity"`.
3. Each violation includes `card_identity`, `commander_identity`, and `illegal_colors` for clear diagnostics.
4. Any card with illegal colors is a violation -- no exceptions.

**Color identity includes**:
- Mana symbols in the mana cost
- Mana symbols in the rules text (oracle text)
- Color indicators (used on back faces of double-faced cards)
- Characteristic-defining abilities

**Color identity excludes**:
- Reminder text (text in parentheses)
- Mana symbols in reminder text are NOT part of color identity

**Special cases**:
- Colorless cards (empty color_identity `[]`) are legal in any deck.
- Basic lands have a color identity matching their produced color (Plains = W, Island = U, etc.) -- use the Scryfall `color_identity` field, not inference.
- Hybrid mana symbols contribute ALL their colors to identity. A card with `{W/B}` in its cost has color identity `[W, B]`.

**Pass condition**: All 100 cards have color identity that is a subset of the commander's.

**Verdict field**: `color_identity: <N>/100`

---

## Check 4: Banned List

**Rule**: No card in the deck may appear on the Commander banned list.

**Procedure**:
1. The `validate-deck` command (run in Check 3) already checks the banned list programmatically. Check the `violations` array for entries with `"type": "banned"`.
2. Additionally, read `references/banned-list.md` for the current banned card list as a cross-reference.
3. Use exact string matching on Scryfall card names (the banned list uses exact Scryfall names).

**Important**: The banned list applies to ALL cards in the deck -- the commander AND the 99. A card that is legal as a non-commander card may still be banned entirely from the format.

**Pass condition**: Zero cards found on the banned list.

**Verdict field**: `banned_cards: <N> found`

---

## Check 5: Singleton Rule

**Rule**: No duplicate card names except basic lands.

**Procedure**:
1. Collect all 100 card names.
2. Identify any names that appear more than once.
3. For each duplicate, check if it is one of the 5 basic land types:
   - Plains
   - Island
   - Swamp
   - Mountain
   - Forest

**Only these 5 names are exempt.** Snow-covered basics (e.g., "Snow-Covered Swamp") are NOT basic lands for the purposes of the singleton exception -- they follow the singleton rule. Wastes is also NOT a basic land exception (it is a basic land type but follows singleton in Commander).

**Pass condition**: No duplicate non-basic-land card names.

**Verdict field**: `singleton: PASS|FAIL`

---

## Check 6: Format Legality

**Rule**: Every card must be legal in the Commander format.

**Procedure**:
1. The `validate-deck` command (run in Check 3) already checks format legality programmatically. Check the `violations` array for entries with `"type": "format_legality"`.
2. For additional detail, the batch results also contain `legalities.commander` for each card. The value must be `"legal"`.

**Values that are NOT legal**:
- `"not_legal"` -- card is not printed in a Commander-legal set or is otherwise ineligible
- `"banned"` -- card is on the banned list (this overlaps with Check 4 but serves as a redundant safeguard)
- `"restricted"` -- not applicable to Commander (Commander has no restricted list), but flag if encountered

**Note**: Cards with `legalities.commander == "legal"` may still fail other checks (color identity, banned list). This check is independent.

**Pass condition**: All 100 cards show `legalities.commander: "legal"`.

**Verdict field**: `format_legality: <N>/100`

---

## Check 7: Synergy Audit

**Rule**: When a synergy rationale or synergy tag claims a mechanical interaction, the card's oracle text must support the claim.

**Procedure**:
1. For each non-land card, read its `synergy_rationale` and `synergy_tags` from the deck state.
2. For each claimed interaction, verify the mechanism exists in the card's oracle text (from Scryfall batch results).
3. Flag false claims where the oracle text does not support the stated interaction.

**What to verify**:
- If a card is tagged `[TRIGGERS: Blood Artist]` via "creature dies", verify the card's oracle text actually causes creatures to die (sacrifice, destroy) or that Blood Artist's oracle text triggers on the relevant event.
- If a card claims "draws cards when creatures enter", verify the oracle text contains a draw effect tied to creature entry.
- If a combo is claimed, verify each step in the interaction sequence is rules-legal.

**What NOT to flag**:
- Implicit interactions that are rules-legal but not explicitly stated on one card (e.g., a sacrifice outlet + a creature = a death trigger on Blood Artist -- all three oracle texts together support this).
- Category assignments (those are the Optimization Reviewer's domain).

**Severity**: Synergy audit violations are FAIL-worthy because false synergy claims undermine the synergy-first philosophy. The Deck Builder needs to correct either the card choice or the rationale.

**Pass condition**: Zero false synergy claims.

**Verdict field**: `synergy_audit: <N> false claims`

---

## Commander Legality Check (Pre-Validation)

This check happens at intake before the pipeline starts, but the Rules Judge should verify it was done correctly:

- The commander must be a Legendary Creature, OR have text stating "can be your commander" (e.g., certain Planeswalkers like Tevesh Szat).
- The commander must NOT have the "Partner" keyword (rejected at intake in v1).
- The commander must NOT be on the banned list.

If the commander fails any of these, the entire deck is invalid. Flag it as a critical violation.

---

## Output Format

After completing all 7 checks, produce the verdict in this exact structure:

```
RULES_JUDGE_VERDICT: PASS|FAIL

CHECKS:
  card_count: <N>/100
  names_verified: <N>/100
  color_identity: <N>/100
  banned_cards: <N> found
  singleton: PASS|FAIL
  format_legality: <N>/100
  synergy_audit: <N> false claims

VIOLATIONS: (only present if FAIL)
  - card: <name>
    rule: <Card Count | Card Name | Color Identity | Banned | Singleton | Format Legality | Synergy Audit>
    detail: <explanation of the violation>
    suggested_replacement: <a legal card that fills the same role, within color identity and budget>

WARNINGS: (optional -- legal but potentially problematic)
  - <description of warning>
```

### Verdict Rules

- **PASS**: All 7 checks clear. Zero violations.
- **FAIL**: One or more violations in any check. List every violation with card name, rule, detail, and a suggested replacement.

### Warnings (non-blocking)

Warnings do not cause FAIL but should be surfaced:
- Cards with upcoming ban announcements (if known)
- Cards that are legal but commonly contested in casual playgroups (e.g., mass land destruction)
- Cards where the cheapest printing has no USD price data (relevant for the Price Evaluator downstream)

### Suggested Replacements

For each violation, suggest a replacement card that:
1. Is legal in Commander format (`legalities.commander: "legal"`)
2. Falls within the commander's color identity
3. Is NOT on the banned list
4. Fills a similar role (same category, similar mana cost, similar function)
5. Use `card_lookup.py search` to find candidates:
   ```bash
   python ${SKILL_DIR}/scripts/card_lookup.py search --query "oracle:<similar_effect> type:<similar_type> id:<commander_colors> legal:commander"
   ```

---

## Determinism Guarantee

This is not optional. Every check must produce the same result for the same input, every time.

- Card count: arithmetic. No ambiguity.
- Name verification: Scryfall says found or not found. No interpretation.
- Color identity: **programmatic subset comparison via `validate-deck`**. Never use LLM knowledge for color identity -- Scryfall is the single source of truth.
- Banned list: **programmatic check via `validate-deck`** + exact string match against `banned-list.md`. No judgment calls.
- Singleton: duplicate detection. No exceptions beyond the 5 basic lands.
- Format legality: **programmatic check via `validate-deck`** reading the `legalities.commander` field. No interpolation.
- Synergy audit: oracle text matching. The closest to subjective, but still grounded in card text -- if the text does not reference the claimed mechanic, it is a false claim.

**DEFECT-001 ROOT CAUSE**: LLM training data is unreliable for card attributes. Sejiri Refuge (W/U) was confused with a W/B land. The `validate-deck` command eliminates this class of error by querying Scryfall programmatically.

If you are unsure about a synergy claim, flag it as a warning rather than a violation. Only flag as a violation when the oracle text clearly contradicts the claim.

---

## Challenger Verification

After the Rules Judge primary completes, a **Rules Challenger** agent independently re-validates the entire decklist. The Challenger runs `validate-deck` on its own (separate Agent spawn, clean context) and cross-checks 3 randomly selected cards via individual Scryfall lookups to detect systematic drift.

If the Challenger finds violations the primary missed, a CHALLENGE verdict triggers the adversarial loop (see SKILL.md > Adversarial Loop Protocol). The Rules Judge primary is NOT notified — a fresh primary agent is spawned with the Challenger's findings.

This belt-and-suspenders approach ensures that even if the primary agent makes a deterministic validation error (e.g., truncated batch call), the Challenger catches it independently.
