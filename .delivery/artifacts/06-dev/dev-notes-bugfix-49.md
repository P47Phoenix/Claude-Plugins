# Dev Notes: Bug Fix #49 — Pipeline Stalling at Phase 4/5

## Summary

Injected 5 continuation directives into `delivery-team/skills/delivery-flow/SKILL.md` to eliminate pipeline stalls at Phase 4 (DoD validation) and Phase 5 (stage transitions). Total addition: ~270 tokens against a 500-token budget. No existing content was modified.

## Changes

| # | Location | AC | What |
|---|----------|-----|------|
| 1 | Line 277 | AC-5 | Self-recovery directive at Phase 4 top — instructs the model to auto-resume if it detects it has paused without completing DoD validation |
| 2 | Line 409 | AC-1 | Continuation directive after DoD validator collection — prevents the model from stopping after gathering validator results instead of acting on them |
| 3 | Line 446 | AC-3 | Continuation directive after checkpoint approval — ensures the model proceeds to the next stage after human approval rather than waiting |
| 4 | Line 452 | AC-2 | State anchor at stage transitions — explicitly names the next stage and required action to prevent context loss during handoff |
| 5 | Lines 1095-1098 | AC-4 | No-stalling guardrail — top-level instruction that prohibits pausing between stages unless blocked by a human checkpoint |

## Approach

- **Directive injection only** — no restructuring, no removals, no behavioral changes to existing logic
- **Token-minimal** — each directive is a single sentence or short block, well under budget
- **Targeted at observed failure modes** — each insertion addresses a specific stall pattern from issue #49 reports

## Outstanding Items

| Item | Status | Notes |
|------|--------|-------|
| TC-1 through TC-3, TC-5 | CODE_COMPLETE | Covered by directive placement; verifiable by inspection |
| TC-4 (full pipeline run without stalls) | PENDING | Requires runtime validation — run a full pipeline end-to-end |
| TC-6 (dogfooding) | PENDING | Team must use the patched SKILL.md in a real delivery session |

## File Modified

- `delivery-team/skills/delivery-flow/SKILL.md`
