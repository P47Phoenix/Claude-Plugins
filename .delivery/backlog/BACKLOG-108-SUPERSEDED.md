# BACKLOG-108 - Supersede and retarget record

**Status**: SUPERSEDED
**Date**: 2026-09-19
**Applies to**: `BACKLOG-108-opus-4-8-migration.md` (untracked in main checkout; not edited here)
**Owner of original file**: apply the header block below there.

Retired IDs are quoted in a blockquote so the stale-model-id guard (which exempts `>` lines) stays green.

> Status: SUPERSEDED by run "model literals refresh" (PR #88 branch), 2026-09-19.
> Retarget: heavy claude-opus-4-8 -> claude-opus-5; mid claude-sonnet-4-6 -> claude-sonnet-5;
> light claude-haiku-4-5-20251001 unchanged; claude-fable-5-1 allowlisted, not adopted.
> Carried forward: positive-allowlist guard, no dual-allow window, '#'/'>' provenance exemption,
> atomic ship, static-grep-only CI, fixture edits separate from harness logic,
> family-alias exemption for prd-quality-gate-flow.
> Split out: S3 (prose sweep + stamps) -> BACKLOG-109; S5 (metrics/xhigh/live baseline) -> BACKLOG-111.
> cache-prefix re-freeze: dropped (drift is pre-existing) -> BACKLOG-110.
> Memory topic opus-4-8-migration.md Section 1 lineup table: superseded; record new lineup as a new topic.

## Retarget summary

Opus 4.8 target retargeted to Opus 5 (`claude-opus-5`). Sonnet tier moves to `claude-sonnet-5`. Haiku unchanged.

## Follow-ups

- BACKLOG-109 model_awareness stamp + prose audit
- BACKLOG-110 cache-prefix-hash drift
- BACKLOG-111 smoke-harness live baseline
- BACKLOG-112 Fable adoption (conditional)
