# BACKLOG-111 - Smoke-harness metrics / live baseline

**Type**: FEATURE
**Created**: 2026-09-19
**Status**: OPEN
**Priority**: Could
**Origin**: PR #88; absorbs BACKLOG-108 S5

## Summary

Refresh smoke-harness metrics and record a live baseline on the new model set (Opus 5, Sonnet 5, Haiku 4.5), including `xhigh` behavior claims.

## Constraints

- Local-only: needs the claude CLI. Never place in `.github/workflows/` (CI runners lack it).
- Fixture edits stay separate from harness logic.

## Acceptance

- Committed baseline reflects live runs on the new set.
