# Story 65: Fix generate_pptx.py -- sys.exit() and accent_color

**Date**: 2026-04-04
**Stories**: BF-65-A, BF-65-B
**File**: `delivery-team/skills/presentation/scripts/generate_pptx.py`

---

## Changes Made

### BF-65-A: Replace sys.exit() with exceptions

Removed all 5 `sys.exit(1)` calls from `generate_pptx()` and replaced with proper exception raising:

| Error condition | Old behavior | New behavior |
|----------------|-------------|-------------|
| Invalid accent_color_hex | `sys.exit(1)` | `ValueError` raised (from `parse_hex_color()`) |
| Input file not found | `sys.exit(1)` | `raise FileNotFoundError(...)` |
| Invalid JSON | `sys.exit(1)` | `json.JSONDecodeError` propagates naturally |
| Missing/empty slides array | `sys.exit(1)` | `raise ValueError(...)` |
| Template file not found | `sys.exit(1)` | `raise FileNotFoundError(...)` |

CLI `main()` now wraps `generate_pptx()` in `try/except (FileNotFoundError, ValueError, json.JSONDecodeError)` and calls `sys.exit(1)` only at the CLI boundary.

The module-level import guard for `python-pptx` retains its `sys.exit(1)` -- that fires before the module is usable and is appropriate at import time.

### BF-65-B: Apply accent_color to slide elements

Applied `accent_color` to three element types:

1. **Title slide titles** -- `run.font.color.rgb = accent_color` added in `populate_title_slide()`
2. **Content slide titles** -- `run.font.color.rgb = accent_color` added in `populate_content_slide()`
3. **Table headers** -- `accent_color: RGBColor | None = None` parameter added to `add_table_to_slide()`; applied via `p.font.color.rgb = accent_color` in header row loop
4. **All 3 call sites** of `add_table_to_slide()` updated to pass `accent_color=accent_color`

---

## Verification

- AST scan confirms 0 `sys.exit()` calls inside `generate_pptx()` function body
- `py_compile` syntax check passes
- Docstring already accurately documents raised exceptions (was written aspirationally before this fix)
- CLI error path preserved: `main()` catches all three exception types, prints to stderr, exits 1

## AC Coverage

| AC | Status |
|----|--------|
| BF-65-A AC-1 (ValueError on bad hex) | DONE |
| BF-65-A AC-2 (FileNotFoundError on missing input) | DONE |
| BF-65-A AC-3 (JSONDecodeError on bad JSON) | DONE |
| BF-65-A AC-4 (ValueError on missing slides) | DONE |
| BF-65-A AC-5 (FileNotFoundError on missing template) | DONE |
| BF-65-A AC-6 (CLI wraps exceptions with sys.exit) | DONE |
| BF-65-A AC-7 (Docstring accurate) | DONE |
| BF-65-B AC-1 (Title slide title color) | DONE |
| BF-65-B AC-2 (Content slide title color) | DONE |
| BF-65-B AC-3 (Table header color) | DONE |
| BF-65-B AC-4 (add_table_to_slide accepts accent_color) | DONE |
