# DEFECT-001 Fix: Rules Judge Color Identity Validation

**Defect**: Rules Judge relied on LLM card knowledge for color identity checks, causing Sejiri Refuge (W/U) to pass in a Karlov (W/B) deck. The LLM confused it with a W/B land.

**Root Cause**: The rules-judge-guide.md told the agent to check color identity from batch results, but the agent could skip the programmatic check and rely on its training data. No enforcement mechanism existed.

**Fix Summary**: Three-part fix to mandate programmatic Scryfall API validation.

---

## Part 1: `validate-deck` Command (card_lookup.py)

**File**: `mtg-commander/scripts/card_lookup.py`

Added new CLI command `validate-deck` that accepts a commander name and card list, then programmatically checks:
- Card existence in Scryfall (via batch lookup)
- Color identity subset validation (card identity must be subset of commander identity)
- Format legality (`legalities.commander` must be `"legal"`)
- Banned list compliance (parsed from `references/banned-list.md`)

Also added:
- `_load_banned_list()` helper that parses the banned-list.md markdown table
- `os` and `re` imports for file path resolution and table parsing

**Usage**:
```bash
python card_lookup.py validate-deck --commander "Karlov of the Ghost Council" --cards "Sol Ring" "Sejiri Refuge" "Dark Ritual" "Swamp"
```

**Output format**:
```json
{
  "commander": {"name": "...", "color_identity": ["W", "B"]},
  "total_cards": 4,
  "violations": [
    {"card": "Sejiri Refuge", "type": "color_identity", "card_identity": ["U", "W"], "commander_identity": ["B", "W"], "illegal_colors": ["U"]}
  ],
  "legal_count": 3,
  "illegal_count": 1
}
```

## Part 2: Rules Judge Guide Update

**File**: `mtg-commander/references/rules-judge-guide.md`

Changes:
- Added `validate-deck` to the Tools section with mandatory usage note
- Check 3 (Color Identity): Rewrote procedure to mandate `validate-deck` as the primary method. Added CRITICAL warning against using LLM knowledge.
- Check 4 (Banned List): Updated to reference `validate-deck` output as primary check, with `banned-list.md` as cross-reference.
- Check 6 (Format Legality): Updated to reference `validate-deck` output as primary check.
- Determinism Guarantee: Bolded the programmatic requirement for color identity, banned list, and format legality. Added DEFECT-001 root cause note.

## Part 3: SKILL.md Rules Judge Template Update

**File**: `mtg-commander/SKILL.md`

Changes:
- Added `validate-deck` usage example to the Card Lookup Utility section
- Consolidated Checks 3, 4, and 6 in the Rules Judge agent template to use `validate-deck` as a single programmatic call
- Added CRITICAL instruction: "Never rely on your knowledge of card color identities or ban status"

---

## Test Result

```
$ python card_lookup.py validate-deck --commander "Karlov of the Ghost Council" --cards "Sol Ring" "Sejiri Refuge" "Dark Ritual" "Swamp"
```

Result: Sejiri Refuge correctly flagged as color identity violation (illegal color: U). Sol Ring, Dark Ritual, and Swamp correctly passed. The defect is resolved.

---

## Files Changed

| File | Change Type |
|------|------------|
| `mtg-commander/scripts/card_lookup.py` | Added `validate-deck` command, `_load_banned_list()`, `cmd_validate_deck()` |
| `mtg-commander/references/rules-judge-guide.md` | Mandated `validate-deck` for Checks 3/4/6, added determinism notes |
| `mtg-commander/SKILL.md` | Updated Rules Judge template and Card Lookup Utility section |
