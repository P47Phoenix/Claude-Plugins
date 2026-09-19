# BACKLOG-109 - model_awareness stamp + prose audit

**Type**: CHORE / AUDIT
**Created**: 2026-09-19
**Status**: OPEN
**Priority**: Should
**Origin**: PR #88 "model literals refresh" (out of scope there, PRD decision Q1)

## Summary

25 SKILL.md files carry a `model_awareness` stamp (26 stamp lines; one file has two). Earlier drafts said 34; the actual count is 25 SKILL.md files. Stamps still assert the prior-generation audit.

A stamp asserts a full prose audit against a model. Bulk-bumping without the audit is dishonest, so PR #88 left stamps untouched.

## Scope

- Audit the 25 SKILL.md files and their `pattern_library_version` / `last_audited` fields.
- Audit prose naming the prior Opus generation, F-08, and `xhigh` behavior claims (`delivery-flow/SKILL.md`, `orchestrator-doctrine.md`, `prompt-engineer/SKILL.md`) against doc-verified Opus 5 / Sonnet 5 behavior.
- Bump stamps only together with the audit.
- Absorbs BACKLOG-108 S3.

## Acceptance

- Every stamp either bumped with audit evidence or left with a recorded reason.
- `scripts/check_skill_budgets.py` still exits 0.
