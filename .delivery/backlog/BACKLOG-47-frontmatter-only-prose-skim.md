# BACKLOG-47-frontmatter-only-prose-skim: Upgrade 11 backfill SKILL.md files from `opus-4-7-frontmatter-only` to `opus-4-7` via prose skim

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- Fresh-challenger review F-C-08 priority #3 (`.delivery/artifacts/04-architect/challenger/review.md`)
- WI-11 (frontmatter backfill work item) — stamps 11 of 17 SKILL.md files
- Plan DX-M1 pillar — "scannable triage via `model_awareness` marker"

## Context

The Architect's plan WI-11 backfills `model_awareness` frontmatter across all 17 SKILL.md files in the repo. Of those 17, only 6 got a full prose review during this engagement; the remaining 11 are stamped `model_awareness: opus-4-7-frontmatter-only` per the fresh-challenger's F-C-08 priority-3 fix. This honest-labeling compromise addresses the challenger's concern that stamping 11 files `opus-4-7` without prose review would give a future greppable "4.7-ready" reader 17 hits, only 6 of which are trustworthy — undermining DX-M1's value proposition.

The compromise is *intentionally* temporary. The `-frontmatter-only` suffix is a promissory note. This backlog item is the payment schedule: a lightweight prose skim (≤30 minutes per file, scanning only for F-25 landmines — inferred instructions, over-pressed `CRITICAL:/MUST` language, 4.6-era prompt patterns), after which the suffix is dropped and the file is stamped plain `opus-4-7`.

## Proposed scope

- Enumerate the 11 files currently stamped `opus-4-7-frontmatter-only` (the list is captured in WI-11 deliverables under `.delivery/artifacts/08-execute/06-dev/dev-log-wi-11.md`).
- For each file, perform a timeboxed prose skim (≤30 min) looking only for:
  - Inferred-instruction anti-patterns (F-25 landmine #1)
  - Over-pressed imperative language (`CRITICAL:`, `MUST`, `You MUST`, `NEVER`, `ALWAYS` block styles — F-28)
  - 4.6-era adaptive-thinking assumptions (budget_tokens references, etc.)
- If no landmines are found: promote `opus-4-7-frontmatter-only` → `opus-4-7` in the frontmatter and log the promotion.
- If landmines are found: open a targeted remediation WI (not absorbed here), leave the file stamped `opus-4-7-frontmatter-only` with a note pointing to the WI.

## Out of scope for this item

- Deep prose rewrites. This is a triage pass, not a content refactor.
- Files already stamped plain `opus-4-7` (the 6 keystones that got full Wave-2/3/4 review).
- Any new frontmatter fields beyond the `model_awareness` value.

## Success criteria

- All 11 files are triaged with a logged decision (promote / hold with remediation WI).
- Grep for `model_awareness: opus-4-7-frontmatter-only` yields zero hits, OR every remaining hit has an open remediation WI linked in its file.
- DX-M1 scannable-triage value is restored: `grep -r "model_awareness: opus-4-7" delivery-team/` returns *trustworthy* hits.

## Priority & effort (rough)

- Priority: medium (DX integrity — 11 files × ≤30 min ≈ 5.5h; small investment, meaningful trust payback).
- T-shirt: S
- Depends on: WI-11 completion (files must be stamped `-frontmatter-only` before this triage starts).
