# User Stories: Batched BUG_FIX #65 + #66

**Sprint**: Bug Fix Sprint
**Type**: BUG_FIX
**Date**: 2026-04-04

---

## Story 1: Replace sys.exit() with exceptions in generate_pptx()

**ID**: BF-65-A
**Priority**: High
**Estimate**: S (code-tier, ~45 min)
**References**: Issue #65

### Story

As a developer importing generate_pptx as a library, I need the `generate_pptx()` function to raise exceptions on error instead of calling `sys.exit()`, so that I can catch and handle errors without my process being terminated.

### Acceptance Criteria

| # | Criterion | Type | Verification |
|---|-----------|------|-------------|
| AC-1 | `generate_pptx()` raises `ValueError` when `accent_color_hex` is invalid | Behavioral | Call with invalid hex, assert ValueError raised |
| AC-2 | `generate_pptx()` raises `FileNotFoundError` when input file does not exist | Behavioral | Call with nonexistent path, assert FileNotFoundError raised |
| AC-3 | `generate_pptx()` re-raises `json.JSONDecodeError` when input JSON is malformed | Behavioral | Call with bad JSON file, assert JSONDecodeError raised |
| AC-4 | `generate_pptx()` raises `ValueError` when slides array is missing or empty | Behavioral | Call with `{"slides": []}`, assert ValueError raised |
| AC-5 | `generate_pptx()` raises `FileNotFoundError` when template file does not exist | Behavioral | Call with nonexistent template, assert FileNotFoundError raised |
| AC-6 | CLI `main()` catches all three exception types and calls `sys.exit(1)` with printed error | Behavioral | Run CLI with bad input, assert exit code 1 and stderr output |
| AC-7 | Function docstring accurately documents raised exceptions | Structural | Read docstring, verify it matches implementation |

### Test Cases

| TC | Covers AC | Test | Expected |
|----|-----------|------|----------|
| TC-1 | AC-1 | `generate_pptx("x.json", "out.pptx", accent_color_hex="ZZZZZZ")` | `ValueError` raised |
| TC-2 | AC-2 | `generate_pptx("/nonexistent.json", "out.pptx")` | `FileNotFoundError` raised |
| TC-3 | AC-3 | Create file with `{bad json`, call `generate_pptx()` | `json.JSONDecodeError` raised |
| TC-4 | AC-4 | Create file with `{"slides": []}`, call `generate_pptx()` | `ValueError` raised |
| TC-5 | AC-5 | `generate_pptx("valid.json", "out.pptx", template_path="/nope.pptx")` | `FileNotFoundError` raised |
| TC-6 | AC-6 | `grep -c 'sys.exit' generate_pptx.py` inside `generate_pptx()` body | 0 matches |

### Technical Notes

- 5 `sys.exit(1)` calls to convert: accent color parse, input file missing, JSON decode, slides validation, template missing.
- For JSON decode: remove the try/except and let `json.JSONDecodeError` propagate naturally, OR catch and re-raise with context.
- `main()` wraps the call in `try/except (FileNotFoundError, ValueError, json.JSONDecodeError)`.

---

## Story 2: Apply accent_color to slide elements

**ID**: BF-65-B
**Priority**: Medium
**Estimate**: S (code-tier, ~30 min)
**References**: Issue #65

### Story

As a presentation author specifying a brand accent color, I need the accent_color to be visually applied to slide titles and table headers, so that my presentations reflect the configured branding.

### Acceptance Criteria

| # | Criterion | Type | Verification |
|---|-----------|------|-------------|
| AC-1 | Title slide title runs have `font.color.rgb` set to `accent_color` | Behavioral | Generate PPTX with custom color, inspect title slide title font color |
| AC-2 | Content slide title runs have `font.color.rgb` set to `accent_color` | Behavioral | Generate PPTX with custom color, inspect content slide title font color |
| AC-3 | Table header cell text has `font.color.rgb` set to `accent_color` | Behavioral | Generate PPTX with table data and custom color, inspect header font color |
| AC-4 | `add_table_to_slide()` accepts an `accent_color` parameter | Structural | Function signature includes `accent_color: RGBColor | None = None` |

### Test Cases

| TC | Covers AC | Test | Expected |
|----|-----------|------|----------|
| TC-1 | AC-1 | Generate PPTX with `accent_color="#ff0000"`, read title slide title run font color | `RGBColor(0xFF, 0x00, 0x00)` |
| TC-2 | AC-2 | Generate PPTX with `accent_color="#ff0000"`, read content slide title run font color | `RGBColor(0xFF, 0x00, 0x00)` |
| TC-3 | AC-3 | Generate PPTX with table data and `accent_color="#ff0000"`, read header cell font color | `RGBColor(0xFF, 0x00, 0x00)` |

### Technical Notes

- `populate_title_slide()`: add `run.font.color.rgb = accent_color` at line 148 (where `font.name` is set).
- `populate_content_slide()`: add `run.font.color.rgb = accent_color` at line 250 (where title `font.name` is set).
- `add_table_to_slide()`: add `accent_color` parameter; apply `p.font.color.rgb = accent_color` in header row loop (line 213 area).
- Update all 4 call sites of `add_table_to_slide()` to pass `accent_color`.

---

## Story 3: Fix map type parsing in generate-schema.py

**ID**: BF-66-A
**Priority**: High
**Estimate**: S (code-tier, ~30 min)
**References**: Issue #66

### Story

As a config schema maintainer, I need `generate-schema.py` to correctly parse bare `map` and `map[K, V]` types from config-schema.md, so that the generated JSON schema represents map-typed fields as objects instead of strings.

### Acceptance Criteria

| # | Criterion | Type | Verification |
|---|-----------|------|-------------|
| AC-1 | `parse_type("map")` returns `{"type": "object"}` | Behavioral | Unit assertion |
| AC-2 | `parse_type("map[string, integer]")` returns `{"type": "object", "additionalProperties": {"type": "integer"}}` | Behavioral | Unit assertion |
| AC-3 | `parse_type("map[string, string]")` continues to return `{"type": "object", "additionalProperties": {"type": "string"}}` | Behavioral | No regression |
| AC-4 | Generic `map[X, Y]` pattern extracts value type using regex | Structural | Code review |
| AC-5 | `parse_valid_values()` does not add enum when type is `object` | Behavioral | Verify vocabulary_overrides and thresholds have no enum in output |

### Test Cases

| TC | Covers AC | Test | Expected |
|----|-----------|------|----------|
| TC-1 | AC-1 | `parse_type("map")` | `{"type": "object"}` |
| TC-2 | AC-2 | `parse_type("map[string, integer]")` | `{"type": "object", "additionalProperties": {"type": "integer"}}` |
| TC-3 | AC-3 | `parse_type("map[string, string]")` | `{"type": "object", "additionalProperties": {"type": "string"}}` |
| TC-4 | AC-5 | Regenerate schema, check `presentation.thresholds` | No `enum` key present |
| TC-5 | AC-5 | Regenerate schema, check `presentation.vocabulary_overrides` | Type is `object`, not `string` |

### Technical Notes

- Add two cases to `parse_type()` before the fallback:
  - `elif t == "map":` -> `return {"type": "object"}`
  - `elif` regex match for `map[K, V]` -> extract value type, return object with additionalProperties
- The existing `map[string, string]` case can be kept or folded into the generic regex.
- In `parse_valid_values()`, the description text for thresholds is currently parsed as enum because the type is `string`. Once type becomes `object`, the comma-split enum logic only fires for `type == "string"`, so the fix is self-correcting.

---

## Story 4: Regenerate config-schema.json

**ID**: BF-66-B
**Priority**: High
**Estimate**: XS (code-tier, ~15 min)
**References**: Issue #66
**Blocked by**: BF-66-A

### Story

As a pipeline maintainer, I need config-schema.json regenerated from the fixed parser, so that the schema artifact matches the source of truth in config-schema.md.

### Acceptance Criteria

| # | Criterion | Type | Verification |
|---|-----------|------|-------------|
| AC-1 | `config-schema.json` regenerated by running `python generate-schema.py` | Process | Script runs without error |
| AC-2 | `presentation.vocabulary_overrides` has `"type": "object"` | Structural | JSON inspection |
| AC-3 | `presentation.thresholds` has `"type": "object"` with `"additionalProperties": {"type": "integer"}` | Structural | JSON inspection |
| AC-4 | `presentation.thresholds` has no `"enum"` field | Structural | JSON inspection |
| AC-5 | No other fields changed unexpectedly | Structural | Git diff review |

### Test Cases

| TC | Covers AC | Test | Expected |
|----|-----------|------|----------|
| TC-1 | AC-2 | `jq '.properties.presentation.properties.vocabulary_overrides.type' config-schema.json` | `"object"` |
| TC-2 | AC-3 | `jq '.properties.presentation.properties.thresholds.additionalProperties.type' config-schema.json` | `"integer"` |
| TC-3 | AC-4 | `jq '.properties.presentation.properties.thresholds.enum' config-schema.json` | `null` |
| TC-4 | AC-5 | `git diff config-schema.json` -- only vocabulary_overrides and thresholds sections changed | Confirmed |
