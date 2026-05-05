# Story 3 Implementation — Challenger-Tier Model Inheritance Hook

**Date:** 2026-05-03
**ADR:** ADR-tk1-003 §W1-5
**File modified:** `delivery-team/hooks/audit_agent_prompt.py`

## What Was Done

Extended `audit_agent_prompt.py` with `check_challenger_tier_inheritance(prompt_text)`.
Additive-only — all existing audit logic (compound-role OD-10, code-fence, length)
preserved unchanged.

## New Function

```python
def check_challenger_tier_inheritance(prompt_text: str) -> tuple[bool, str]:
```

- Detects `adversarial` / `challenger` keyword (case-insensitive regex)
- Extracts `model: <name>` / `model=<name>` occurrences from prompt body
- Extracts `primary model: <name>` / `primary_model: <name>` if present;
  falls back to first model mention as heuristic primary
- Treats last model mention as challenger model
- Returns `(True, warning_msg)` only when primary != challenger AND
  adversarial keyword present AND model field found
- Inner try/except: any parsing error logs to stderr, returns `(False, "")`

## Warning Emission

- `_emit_challenger_warning()` prints to **stderr** with `[CHALLENGER-TIER-WARN]` prefix
- If `GITHUB_STEP_SUMMARY` env var set, appends markdown warning there
- Called EARLY in `main()`, before all existing audit checks

## Policy

- Wave 1, Sprint 1: warn-only, exit 0 always
- Outer try/except in `main()` wraps the new block — hook cannot crash dispatch
- Promotion to hard-block deferred to Wave 2+ pending zero-violation telemetry

## Line Count

- Pre: 113 lines
- Post: 208 lines (+95, all additive)

## Dogfood Result

4/4 tests pass. See `.delivery/artifacts/06-dev/dogfood-evidence/story-3-challenger-hook-evidence.md`.
