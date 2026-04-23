# BACKLOG-47-overpressure-audit: Keystone SKILL.md audit for `CRITICAL:/MUST/NEVER/ALWAYS` over-pressure patterns

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- PRD REQ-06 AC-06.1/AC-06.2 (`.delivery/artifacts/02-refine/po/prd.md` §4)
- PRD §3 finding F-28 — "strong-language pattern risk on 4.7"
- DX-M5 pressure audit (deferred by Architect this engagement)

## Context

PRD REQ-06 offered the Architect a COULD-level task: optionally audit keystone SKILL.md files for over-pressed imperative language (`CRITICAL:`, `MUST`, `You MUST`, `NEVER`, `ALWAYS` block styles — PRD F-28) and judge whether the pattern over-pressures Opus 4.7, which responds differently than 4.6 to imperative pressure density.

AC-06.1 permitted inclusion at Architect discretion; AC-06.2 said that **if deferred**, it must be logged as a NEW-BACKLOG item. The Architect deferred DX-M5 this engagement (see transformation-plan DX milestones), so this file is the AC-06.2 deliverable.

The audit is a grep across the six keystone files (PRD Section 3.7) producing a count table plus an Architect judgement ("over-pressed / acceptable"). No line-by-line edits are proposed by the audit itself; remediation would be a follow-on WI only if the judgement is "over-pressed."

## Proposed scope

- Grep the six keystone files for the target patterns:
  - `CRITICAL:` (case-sensitive block marker)
  - `\bMUST\b` as an imperative (not inside prose like "must contain")
  - `You MUST`, `You must`
  - `\bNEVER\b`, `\bALWAYS\b` as imperative block markers
- Produce a count table: file × pattern × raw count.
- Produce a qualitative Architect judgement per file: "over-pressed" | "acceptable" | "under-pressed."
- If any file is judged over-pressed, open a targeted remediation WI (separate from this audit).
- If all files are acceptable, the audit artifact itself is the entire deliverable — no edits.

## Out of scope for this item

- Non-keystone SKILL.md files (they get the same pattern treatment in BACKLOG-47-frontmatter-only-prose-skim as part of the prose-skim pass).
- Prose edits themselves (those are remediation WIs, spawned only if needed).
- Other F-25 landmines (inferred instructions, 4.6-era adaptive-thinking assumptions) — scope is strictly F-28.

## Success criteria

- Audit artifact at `.delivery/artifacts/<impl-run>/audits/overpressure-audit.md` with count table + per-file judgement.
- If "over-pressed" on any file: a remediation WI exists and is linked from the audit.
- If all "acceptable": a one-line entry is added to `delivery-flow/references/` pattern library documenting "over-pressure not observed — keep imperative density at current levels."
- REQ-06 AC-06.2 is satisfied (logged as NEW-BACKLOG).

## Priority & effort (rough)

- Priority: low (COULD-level from the PRD; deferred for a reason).
- T-shirt: XS (grep + judgement; optional remediation scales with findings).
- Depends on: nothing.
