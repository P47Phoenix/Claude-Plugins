# Story 3 Dogfood Evidence — Challenger-Tier Hook

**Date:** 2026-05-03
**File:** `delivery-team/hooks/audit_agent_prompt.py`
**ADR:** ADR-tk1-003 §W1-5

## Pre-flight

- `test -f delivery-team/hooks/audit_agent_prompt.py` → EXISTS
- Pre-flight `wc -l`: **113 lines**
- `grep -n "PreToolUse" delivery-team/hooks/hooks.json` → line 28 confirmed
- hooks.json `python3 -c "import json; json.load(...)"` → valid JSON

## Tests

### Test 1 — adversarial-challenger with MISMATCHED model

**Input prompt (synthetic):**
```
You are a Challenger. primary model: claude-opus-4-5  model: claude-haiku-3-7  Critique the following plan.
```

**Result:**
- exit_code: `0`
- stderr: `[CHALLENGER-TIER-WARN] ADR-tk1-003 W1-5: adversarial/challenger dispatch
  detected with model mismatch — primary='claude-opus-4-5', challenger='claude-haiku-3-7'.
  Sprint 1 policy: warn-only. Promote to hard-block after zero-violation telemetry period (Wave 2+).`
- **PASS** — warning emitted, no block

### Test 2 — non-adversarial prompt

**Input prompt (synthetic):**
```
You are a software engineer. Write unit tests for the authentication module.
```

**Result:**
- exit_code: `0`
- stderr: (empty)
- **PASS** — no spurious warning

### Test 3 — adversarial-challenger with MATCHING model

**Input prompt (synthetic):**
```
You are an adversarial reviewer. primary model: claude-sonnet-4-6  model: claude-sonnet-4-6  Challenge the design.
```

**Result:**
- exit_code: `0`
- stderr: (empty)
- **PASS** — matching model, no warning

### Test 4 — malformed JSON input

**Input:** `NOT_VALID_JSON{{{`

**Result:**
- exit_code: `0`
- stderr: (empty — hook_utils handles graceful exit)
- **PASS** — graceful failure, no block

## hooks.json validation

```
python3 -c "import json; json.load(open('delivery-team/hooks/hooks.json'))"
```
→ `hooks.json: valid JSON`

## Post-flight

- Post-flight `wc -l`: **208 lines** (pre: 113, delta: +95)
- All existing compound-role and content-leakage logic preserved (additive-only)
