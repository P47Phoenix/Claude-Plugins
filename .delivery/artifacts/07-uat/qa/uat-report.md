# UAT Report: Issues #65 + #66 (Code Fixes)

**Date**: 2026-04-04
**QA Engineer**: Legolas
**Sprint**: Bug Fix Sprint
**Type**: BUG_FIX
**Stories**: BF-65-A, BF-65-B, BF-66-A, BF-66-B

---

> *"Nineteen arrows loosed, nineteen targets struck. The wind carries no doubt today."*

---

## Summary

| Metric | Value |
|--------|-------|
| Total Test Cases | 19 |
| Passed | 19 |
| Failed | 0 |
| Overall Verdict | **PASS** |

---

## Test Results

### Issue #65: generate_pptx.py

#### Story BF-65-A: Replace sys.exit() with exceptions in generate_pptx()

##### TC-1: AST-walk generate_pptx() for sys.exit calls

**Covers**: AC-6 (TC-6 from stories)
**Verdict**: PASS

AST analysis of the `generate_pptx()` function body found **0** `sys.exit()` calls. The function raises exceptions (`ValueError`, `FileNotFoundError`, `json.JSONDecodeError`) instead of terminating the process.

##### TC-2: Grep sys.exit across full file

**Covers**: AC-6
**Verdict**: PASS

2 `sys.exit` occurrences in the entire file, both in expected locations:
- **Line 53**: Import guard (top-level, outside any function) -- correct behavior for missing dependency
- **Line 462**: Inside `main()` CLI wrapper -- correct behavior for CLI error handling

Neither is inside the `generate_pptx()` function body.

##### TC-3: main() has try/except wrapping generate_pptx() call

**Covers**: AC-6
**Verdict**: PASS

AST analysis confirms `main()` contains a `try/except` block that catches:
- `FileNotFoundError`
- `ValueError`
- `JSONDecodeError`

The except handler prints the error to stderr and calls `sys.exit(1)`.

##### TC-4: Docstring documents raised exceptions

**Covers**: AC-7
**Verdict**: PASS

The `generate_pptx()` docstring contains a `Raises:` section documenting:
- `FileNotFoundError` -- present
- `ValueError` -- present
- `json.JSONDecodeError` -- present

All three match the actual implementation.

##### TC-5: File syntax validity

**Covers**: All ACs
**Verdict**: PASS

`ast.parse()` on the full file completed without errors. Python syntax is valid.

---

#### Story BF-65-B: Apply accent_color to slide elements

##### TC-6: accent_color applied in populate_title_slide()

**Covers**: AC-1
**Verdict**: PASS

Line 149: `run.font.color.rgb = accent_color` -- title slide title runs receive the accent color.

##### TC-7: accent_color applied in populate_content_slide()

**Covers**: AC-2
**Verdict**: PASS

Line 255: `run.font.color.rgb = accent_color` -- content slide title runs receive the accent color.

##### TC-8: accent_color applied in add_table_to_slide() headers

**Covers**: AC-3
**Verdict**: PASS

Line 218: `p.font.color.rgb = accent_color` -- table header cell text receives the accent color, guarded by `if accent_color:` check (line 217).

##### TC-9: add_table_to_slide() accepts accent_color parameter

**Covers**: AC-4
**Verdict**: PASS

Line 180: Function signature includes `accent_color: RGBColor | None = None` parameter.

##### TC-10: All call sites pass accent_color

**Covers**: AC-3
**Verdict**: PASS

All 3 call sites of `add_table_to_slide()` pass the `accent_color` keyword argument:
- Line 270: `add_table_to_slide(slide, table_data, font_name, accent_color=accent_color)` (comparison layout)
- Line 277: `add_table_to_slide(slide, table_data, font_name, accent_color=accent_color)` (timeline layout)
- Line 307: `add_table_to_slide(slide, table_data, font_name, top=4.0, accent_color=accent_color)` (generic fallback)

---

### Issue #66: generate-schema.py + config-schema.json

#### Story BF-66-A: Fix map type parsing in generate-schema.py

##### TC-11: parse_type("map") returns object

**Covers**: AC-1
**Verdict**: PASS

```
parse_type("map") -> {"type": "object"}
```

Exact match with expected output.

##### TC-12: parse_type("map[string, integer]") returns object with additionalProperties

**Covers**: AC-2
**Verdict**: PASS

```
parse_type("map[string, integer]") -> {"type": "object", "additionalProperties": {"type": "integer"}}
```

Exact match with expected output.

##### TC-13: parse_type("map[string, string]") regression check

**Covers**: AC-3
**Verdict**: PASS

```
parse_type("map[string, string]") -> {"type": "object", "additionalProperties": {"type": "string"}}
```

No regression. Existing behavior preserved.

---

#### Story BF-66-B: Regenerate config-schema.json

##### TC-14: Generator runs successfully

**Covers**: AC-1
**Verdict**: PASS

`python generate-schema.py` completed without errors. Parsed 86 schema rows and wrote output.

##### TC-15: vocabulary_overrides has type "object"

**Covers**: AC-2
**Verdict**: PASS

```json
"vocabulary_overrides": {
  "type": "object",
  "default": {}
}
```

Previously was `"type": "string"` with `"default": "{}"` (string). Now correctly `"type": "object"` with `"default": {}` (object).

##### TC-16: thresholds has type "object" with additionalProperties

**Covers**: AC-3
**Verdict**: PASS

```json
"thresholds": {
  "type": "object",
  "additionalProperties": {
    "type": "integer"
  },
  "default": {}
}
```

Previously was `"type": "string"` with a bogus `"enum"` containing description fragments.

##### TC-17: thresholds has no enum field

**Covers**: AC-4
**Verdict**: PASS

No `"enum"` key present in the `thresholds` property. The old incorrect enum (`["type-name: seconds pairs (e.g.", "sprint-review: 120). 0 = unlimited."]`) has been eliminated.

##### TC-18: Idempotency check

**Covers**: AC-5
**Verdict**: PASS

Running `python generate-schema.py` twice produces identical output. No drift.

##### TC-19: Git diff scope

**Covers**: AC-5
**Verdict**: PASS

`git diff` shows changes confined to exactly two properties:
1. `vocabulary_overrides`: `"type": "string"` -> `"type": "object"`, `"default": "{}"` -> `"default": {}`
2. `thresholds`: `"type": "string"` + bogus `"enum"` -> `"type": "object"` + `"additionalProperties": {"type": "integer"}`, `"default": "{}"` -> `"default": {}`

No unexpected changes elsewhere in the schema.

---

## AC Coverage Matrix

### Story BF-65-A (sys.exit removal)

| AC | Description | TCs | Verdict |
|----|-------------|-----|---------|
| AC-6 | No sys.exit in generate_pptx(); main() catches exceptions | TC-1, TC-2, TC-3 | PASS |
| AC-7 | Docstring documents all raised exceptions | TC-4 | PASS |

### Story BF-65-B (accent_color application)

| AC | Description | TCs | Verdict |
|----|-------------|-----|---------|
| AC-1 | Title slide title receives accent_color | TC-6 | PASS |
| AC-2 | Content slide title receives accent_color | TC-7 | PASS |
| AC-3 | Table headers receive accent_color | TC-8, TC-10 | PASS |
| AC-4 | add_table_to_slide accepts accent_color param | TC-9 | PASS |

### Story BF-66-A (map type parsing)

| AC | Description | TCs | Verdict |
|----|-------------|-----|---------|
| AC-1 | parse_type("map") -> object | TC-11 | PASS |
| AC-2 | parse_type("map[K,V]") -> object + additionalProperties | TC-12 | PASS |
| AC-3 | map[string, string] regression | TC-13 | PASS |
| AC-5 | No enum on object-typed fields | TC-17 | PASS |

### Story BF-66-B (schema regeneration)

| AC | Description | TCs | Verdict |
|----|-------------|-----|---------|
| AC-1 | Generator runs without error | TC-14 | PASS |
| AC-2 | vocabulary_overrides type is object | TC-15 | PASS |
| AC-3 | thresholds type is object with integer additionalProperties | TC-16 | PASS |
| AC-4 | thresholds has no enum | TC-17 | PASS |
| AC-5 | No unexpected field changes | TC-18, TC-19 | PASS |

**19/19 test cases: PASS**
**15/15 acceptance criteria: PASS**

---

## Defects

None found.

---

## Observations

1. The `generate_pptx()` function is now safe for library use. All error paths raise exceptions rather than calling `sys.exit()`, while the CLI wrapper in `main()` properly catches and converts these to exit codes for command-line consumers.

2. The `accent_color` parameter flows cleanly through the entire slide generation pipeline: parsed once in `generate_pptx()`, passed to `populate_title_slide()` and `populate_content_slide()`, and forwarded to all `add_table_to_slide()` call sites. The table function uses a defensive `if accent_color:` guard since the parameter is optional.

3. The schema generator's `parse_type()` function now handles the full spectrum of map types: bare `map`, explicit `map[string, string]`, and generic `map[K, V]` patterns. The fix is self-correcting for `parse_valid_values()` -- once the type is `object` instead of `string`, the comma-split enum logic no longer fires on description text.

4. **Note**: These fixes exist as uncommitted working-tree changes. The HEAD commit still contains the bugs. Changes must be committed and pushed to close Issues #65 and #66.

---

## Verification Methods

| Method | Purpose |
|--------|---------|
| AST analysis (`ast.parse`, `ast.walk`) | Structural verification immune to comments/strings |
| Grep with line numbers | Content matching with location verification |
| Direct function invocation | Behavioral tests of parse_type() |
| Schema regeneration + idempotency | End-to-end integration test |
| Git diff analysis | Change scope verification |

---

## Final Verdict: **PASS**

> *"The quiver is spent, and not a single shaft went astray. These fixes stand true -- commit them and let the bugs fall."*

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/07-uat/qa/uat-report.md
SUMMARY: All 19 TCs pass, 15/15 ACs verified across 4 stories (Issues #65+#66), zero defects found.
