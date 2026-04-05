# Idea Brief: Batched BUG_FIX -- generate_pptx.py + config-schema.json (#65, #66)

**Date**: 2026-04-04
**Author**: Product Owner
**Type**: BUG_FIX
**Priority**: High

---

## Problem Statement

Two defects have been discovered that compromise library usability and schema correctness. A shadow lies upon these tools -- small in appearance, but troublesome in consequence. Better to mend them together while the forge is hot.

### Issue #65 -- generate_pptx.py library defects

The `generate_pptx()` function in `delivery-team/skills/presentation/scripts/generate_pptx.py` has two problems:

1. **sys.exit() inside library function**: Five `sys.exit(1)` calls live inside `generate_pptx()` instead of raising exceptions. Any caller importing this function as a library will have their process terminated on error -- an unacceptable contract for a public API. The function's own docstring promises `FileNotFoundError`, `json.JSONDecodeError`, and `ValueError`, but delivers `SystemExit` instead.

2. **accent_color is dead code**: The `accent_color_hex` parameter is accepted, parsed into an `RGBColor`, and threaded through to `populate_title_slide()` and `populate_content_slide()` -- but neither function applies it to the title font runs. `add_table_to_slide()` does not receive it at all. The color is passed to `set_text_frame_font()` which does apply it, but that helper is never called for titles or table headers.

### Issue #66 -- config-schema.json type errors

The generated `config-schema.json` contains two type errors in the `presentation` section:

1. **`presentation.vocabulary_overrides`**: Typed as `"type": "string"` with `"default": "{}"`. The source of truth (`config-schema.md`) declares this as `map` -- it should be `{"type": "object"}`.

2. **`presentation.thresholds`**: Typed as `"type": "string"` with an `"enum"` containing description text fragments (`"type-name: seconds pairs (e.g."`, `"sprint-review: 120). 0 = unlimited."`). The source of truth declares this as `map[string, integer]` -- it should be `{"type": "object", "additionalProperties": {"type": "integer"}}`.

**Root cause**: `delivery-team/scripts/generate-schema.py` `parse_type()` handles `map[string, string]` but not bare `map` or `map[string, integer]`. Unrecognized types fall through to the default case which returns `{"type": "string"}`. Then `parse_valid_values()` treats the description text as comma-separated enum candidates.

---

## Scope

| # | File | Changes |
|---|------|---------|
| 1 | `delivery-team/skills/presentation/scripts/generate_pptx.py` | Replace 5x sys.exit() with exceptions; apply accent_color to titles and table headers |
| 2 | `delivery-team/scripts/generate-schema.py` | Add bare `map` and `map[K, V]` regex to parse_type() |
| 3 | `delivery-team/skills/delivery-flow/references/config-schema.json` | Regenerate from fixed parser |

## Out of Scope

- No changes to config-schema.md (it is already correct -- it is the source of truth)
- No new features
- No CLI behavior changes (main() preserves exit codes)

---

## Value

- `generate_pptx()` becomes safely importable as a library function
- accent_color actually brands presentations as advertised
- Config validation correctly accepts map-typed fields and rejects invalid values
- Schema artifact matches its source of truth

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Exception types differ from what callers expect | Low | Match the types already documented in the docstring |
| accent_color applied inconsistently | Low | Audit every populate/add function for font-setting patterns |
| Schema regeneration introduces unintended drift | Low | Diff-review full JSON output before committing |

## Success Criteria

1. Zero `sys.exit()` calls inside `generate_pptx()` function body
2. CLI `main()` catches exceptions and calls `sys.exit(1)` -- behavior preserved
3. accent_color applied to title slide title, content slide title, and table header fonts
4. `config-schema.json` `vocabulary_overrides` typed as `object`
5. `config-schema.json` `thresholds` typed as `object` with `additionalProperties: {type: integer}`, no enum
6. Regenerated schema matches config-schema.md v2.6
