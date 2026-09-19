# BACKLOG-112 - Fable adoption (conditional)

**Type**: SPIKE
**Created**: 2026-09-19
**Status**: PARKED (conditional)
**Priority**: Won't (until measured need)
**Origin**: PR #88 PRD decisions Q4, Q5

## Summary

`claude-fable-5-1` is allowlisted by the guard but adopted in no role. Adopt only if a role shows measured need beyond Opus 5.

## Preconditions

- Cost: 2x Opus 5 ($10/$50 vs $5/$25 per MTok).
- Code paths for forced `tool_choice` 400, always-on thinking, `refusal` handling, fallback.
- Acknowledge no ZDR, no Priority Tier, 30-day retention.

## Acceptance

- Adoption PR edits sites only; guard already permits the ID.
