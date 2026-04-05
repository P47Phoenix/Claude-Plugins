# Sprint Plan: Batched BUG_FIX #65 + #66

**Sprint Goal**: Fix library defects in generate_pptx.py and type-parsing defects in generate-schema.py, then regenerate config-schema.json to restore correctness.
**Type**: BUG_FIX
**Velocity Ceiling**: 80%
**Sprint Capacity**: 4 stories, all S/XS code-tier
**Total Estimate**: ~2 hours

---

## Story Sequence

| Order | Story ID | Title | Size | Estimate | Dependencies | Assignee |
|-------|----------|-------|------|----------|-------------|----------|
| 1 | BF-65-A | Replace sys.exit() with exceptions in generate_pptx() | S | 45 min | None | Developer |
| 2 | BF-65-B | Apply accent_color to slide elements | S | 30 min | None | Developer |
| 3 | BF-66-A | Fix map type parsing in generate-schema.py | S | 30 min | None | Developer |
| 4 | BF-66-B | Regenerate config-schema.json | XS | 15 min | BF-66-A | Developer |

**Parallelizable**: BF-65-A, BF-65-B, and BF-66-A are independent. BF-66-B is blocked by BF-66-A.

---

## Implementation Plan

### Phase 1 -- Parallel Fixes (BF-65-A + BF-65-B + BF-66-A)

#### Track A: generate_pptx.py (BF-65-A + BF-65-B)

**File**: `delivery-team/skills/presentation/scripts/generate_pptx.py`

**BF-65-A Tasks** -- Replace sys.exit() with exceptions:

1. **Accent color parse error** (line 345): Replace `sys.exit(1)` with `raise ValueError(...)`. Remove the try/except wrapper since `parse_hex_color()` already raises `ValueError`.

2. **Input file not found** (line 351): Replace `sys.exit(1)` with `raise FileNotFoundError(f"Input file not found: {input_path}")`.

3. **JSON decode error** (line 358): Remove the try/except block; let `json.JSONDecodeError` propagate naturally from `json.load()`. Or re-raise with added context.

4. **Missing slides array** (line 365): Replace `sys.exit(1)` with `raise ValueError('JSON must contain a non-empty "slides" array.')`.

5. **Template file not found** (line 374): Replace `sys.exit(1)` with `raise FileNotFoundError(f"Template file not found: {template_path}")`.

6. **Update main()**: Wrap `generate_pptx()` call in:
   ```python
   try:
       slide_count = generate_pptx(...)
   except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
       print(f"Error: {e}", file=sys.stderr)
       sys.exit(1)
   ```

**BF-65-B Tasks** -- Apply accent_color:

1. **populate_title_slide()** (line 148): After `run.font.name = font_name`, add `run.font.color.rgb = accent_color`.

2. **populate_content_slide()** (line 250): After `run.font.name = font_name`, add `run.font.color.rgb = accent_color`.

3. **add_table_to_slide()**: Add `accent_color: RGBColor | None = None` parameter. In header row loop (line 213 area), add `p.font.color.rgb = accent_color` when accent_color is not None.

4. **Update call sites**: All 4 calls to `add_table_to_slide()` (lines 265, 272, 302, and the timeline call) need `accent_color=accent_color` added. This requires threading `accent_color` through `populate_content_slide()` which already receives it.

#### Track B: generate-schema.py (BF-66-A)

**File**: `delivery-team/scripts/generate-schema.py`

1. **Add bare `map` case** to `parse_type()` (after the `map[string, string]` case at line 84):
   ```python
   elif t == "map":
       return {"type": "object"}
   ```

2. **Add generic `map[K, V]` regex** (before the fallback):
   ```python
   map_match = re.match(r"^map\[(\w+),\s*(\w+)\]$", t)
   if map_match:
       value_type = map_match.group(2)
       return {"type": "object", "additionalProperties": {"type": value_type}}
   ```

3. **Verify self-correction**: Once `vocabulary_overrides` gets type `object`, `parse_valid_values()` will not attempt to parse its Valid Values as enum (the enum logic only fires for `type == "string"`). Same for `thresholds`.

---

### Phase 2 -- Regenerate (BF-66-B)

**Blocked by**: BF-66-A complete.

1. Run `python delivery-team/scripts/generate-schema.py`.
2. Diff-review the regenerated `config-schema.json`:
   - `vocabulary_overrides`: `"type": "string"` -> `"type": "object"`, `"default": "{}"` -> `"default": {}`
   - `thresholds`: `"type": "string"` + `"enum"` -> `"type": "object"` + `"additionalProperties": {"type": "integer"}`, `"default": "{}"` -> `"default": {}`
3. Verify no other fields changed unexpectedly.

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| map[K,V] regex too greedy or too narrow | Low | Medium | Anchor regex, test with all 3 map variants from config-schema.md |
| Accent color applied to wrong elements | Low | Low | Trace all font-setting code paths before modifying |
| Schema regeneration drifts other fields | Low | Medium | Full git diff review before commit |
| main() exception handling misses a type | Low | Low | Catch broad (FileNotFoundError, ValueError, json.JSONDecodeError) which covers all 5 cases |

---

## Branch Strategy

- Branch: `fix/65-66-pptx-schema-bugs`
- Conventional commits:
  - `fix: replace sys.exit with exceptions in generate_pptx (#65)`
  - `fix: apply accent_color to slide titles and table headers (#65)`
  - `fix: handle bare map and map[K,V] types in generate-schema (#66)`
  - `chore: regenerate config-schema.json (#66)`
- Single PR batching both issues

---

## Definition of Done

- [ ] Zero `sys.exit()` calls inside `generate_pptx()` function body
- [ ] CLI `main()` catches exceptions and exits with code 1 (behavior preserved)
- [ ] accent_color applied to: title slide title, content slide title, table header fonts
- [ ] `parse_type()` handles `map`, `map[string, string]`, `map[string, integer]`
- [ ] `config-schema.json` `vocabulary_overrides` typed as `object`
- [ ] `config-schema.json` `thresholds` typed as `object` with `additionalProperties: {type: integer}`, no enum
- [ ] Git diff of config-schema.json shows only expected changes
- [ ] All acceptance criteria pass across 4 stories (7 + 4 + 5 + 5 = 21 ACs)
- [ ] PR reviewed and merged
