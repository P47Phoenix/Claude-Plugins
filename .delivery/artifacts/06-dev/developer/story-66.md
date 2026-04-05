# Story BF-66-A + BF-66-B: Fix map type parsing in generate-schema.py

**Issue**: #66
**Date**: 2026-04-04
**Developer**: Gimli

---

## Changes Made

### 1. Fixed `parse_type()` in `generate-schema.py`

**File**: `delivery-team/scripts/generate-schema.py`

Added two new branches before the fallback in `parse_type()`:

- **Bare `map`**: returns `{"type": "object"}`
- **Generic `map[K, V]`**: regex extracts the value type and returns `{"type": "object", "additionalProperties": {"type": "<value_type>"}}`

The existing `map[string, string]` case is preserved as-is (no regression).

### 2. Regenerated `config-schema.json`

**File**: `delivery-team/skills/delivery-flow/references/config-schema.json`

Ran `python generate-schema.py` to regenerate. Only the two affected fields changed:

| Field | Before | After |
|-------|--------|-------|
| `presentation.vocabulary_overrides` | `"type": "string"`, default `"{}"` | `"type": "object"`, default `{}` |
| `presentation.thresholds` | `"type": "string"`, enum with parsed description text | `"type": "object"`, additionalProperties `{"type": "integer"}`, default `{}` |

No other fields were affected.

---

## Acceptance Criteria Verification

| AC | Result | Notes |
|----|--------|-------|
| AC-1: `parse_type("map")` returns `{"type": "object"}` | PASS | New `elif t == "map"` branch |
| AC-2: `parse_type("map[string, integer]")` returns object with additionalProperties integer | PASS | Regex extracts value type |
| AC-3: `parse_type("map[string, string]")` unchanged | PASS | Existing branch preserved above new code |
| AC-4: Generic `map[X, Y]` uses regex | PASS | `re.match(r"^map\[\s*\w+\s*,\s*(\w+)\s*\]$", t)` |
| AC-5: No enum on object-typed fields | PASS | `parse_valid_values()` enum logic only fires for `type == "string"` -- self-correcting |

## Test Cases Verified

| TC | Result |
|----|--------|
| TC-1: `parse_type("map")` | `{"type": "object"}` |
| TC-2: `parse_type("map[string, integer]")` | `{"type": "object", "additionalProperties": {"type": "integer"}}` |
| TC-3: `parse_type("map[string, string]")` | `{"type": "object", "additionalProperties": {"type": "string"}}` |
| TC-4: `presentation.thresholds` has no enum | Confirmed via JSON inspection |
| TC-5: `presentation.vocabulary_overrides` type is object | Confirmed via JSON inspection |
