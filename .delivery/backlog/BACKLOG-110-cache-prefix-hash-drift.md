# BACKLOG-110 - cache-prefix-hash drift

**Type**: CHORE
**Created**: 2026-09-19
**Status**: OPEN
**Priority**: Could
**Origin**: PR #88 (pre-existing drift, PRD s7; dropped from BACKLOG-108 re-freeze)

## Summary

`governance/cache-prefix-hash.txt` is stale. Recorded hash `43067c9e...` does not match the sha256 of `delivery-team/skills/delivery-flow/SKILL.md`, currently `0a7aa92f...`. No CI job reads the file.

## Scope

- Reconcile the file with `delivery-flow/SKILL.md`.
- Decide whether a CI check should read it; if not, consider deleting the file.

## Acceptance

- Hash matches SKILL.md, or file removed with rationale recorded.
