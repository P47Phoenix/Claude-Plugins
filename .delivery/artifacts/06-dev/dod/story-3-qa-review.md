# Story 3 QA Review — Challenger-Tier Model Inheritance Hook

**Validator:** Legolas (QA)  
**Date:** 2026-05-03  
**ADR:** ADR-tk1-003 §W1-5  
**Status:** DONE  

## Gate 1: AC for W1-5 Covered

**Acceptance Criteria:** Hook detects adversarial+mismatch; warns NOT blocks.

| Test | Input | Expected | Actual | Result |
|------|-------|----------|--------|--------|
| 1 | adversarial + claude-opus vs claude-haiku | warn, exit 0 | [CHALLENGER-TIER-WARN], stderr, exit 0 | PASS |
| 2 | non-adversarial prompt | silent, exit 0 | (no output), exit 0 | PASS |
| 3 | adversarial + matched model | silent, exit 0 | (no output), exit 0 | PASS |
| 4 | malformed JSON | graceful exit 0 | hook_utils handles, exit 0 | PASS |

All four scenarios covered. Warn-only policy enforced (exit 0 always).

## Gate 2: Failure-Mode Resilience

**Requirement:** Malformed input, missing model field, etc — all exit 0.

- **Missing model field:** `check_challenger_tier_inheritance()` returns `(False, "")` → no warning
- **Parsing error in regex:** try/except on line 72 logs to stderr, returns clean `(False, "")`
- **Outer guard:** main()-level try/except on line 163 wraps entire block — hook cannot crash
- **All paths:** exit_success() called on line 204 — guaranteed exit 0

Zero crash scenarios. Non-blocking throughout.

## Gate 3: Existing Audit Logic Preserved (Additive-Only)

**Requirement:** Compound-role detection, code-fence, length checks remain unchanged.

- **Compound-role (OD-10):** lines 94–147 untouched; still runs at line 192
- **Code-fence check:** lines 177–182 unchanged
- **Length check:** lines 184–189 unchanged
- **All warnings:** still collected into `warnings` list and emitted as single ISOLATION AUDIT block

No mutations. Three validation chains still functional post-implementation.

## Gate 4: Warn Output to stderr EARLY

**Requirement:** Signal blocks emitted EARLY per memory.

- **Function:** `_emit_challenger_warning()` at line 82 prints to `sys.stderr`
- **Call site:** line 166 in main() — BEFORE compound-role check (line 192)
- **GITHUB_STEP_SUMMARY:** lines 85–91 append markdown warning if env var set
- **Timing:** Challenger-tier check executes first in execution flow

Early emission confirmed. No ordering issues.

## Gate 5: GITHUB_STEP_SUMMARY Append Works

**Requirement:** Append works when env var present.

- **Detection:** `os.environ.get("GITHUB_STEP_SUMMARY")` at line 85
- **Write:** `fh.write(f"\n> **{warning_msg}**\n")` at line 89
- **Non-blocking:** OSError caught, pass clause (line 91)
- **Format:** Markdown blockquote with bold message

Append functional when env var present; graceful no-op when absent.

## Code Metrics

- **Pre-implementation:** 113 lines
- **Post-implementation:** 208 lines (+95)
- **Coverage:** All additive; no existing logic mutated
- **imports:** `sys`, `re`, `os`, `Path` all present
- **hook_utils:** imported and used correctly for exit/response signaling

## Dogfood Evidence Summary

- **4/4 tests pass** (adversarial+mismatch, non-adversarial, adversarial+matched, malformed)
- **Exit code:** always 0
- **Warning format:** consistent [CHALLENGER-TIER-WARN] prefix with ADR + policy footnote
- **hooks.json:** valid JSON, PreToolUse event registered

## Verdict

All five gates satisfied. Hook detects adversarial+mismatch model inheritance via warn-only policy (ADR-tk1-003 W1-5). Failure-mode resilience confirmed. Existing audit logic preserved and functional. Signal blocks emitted early to stderr + GITHUB_STEP_SUMMARY. Implementation is additive, non-blocking, and ready for Wave 1 deployment.

**DONE.**
