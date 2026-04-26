# BACKLOG-47-contributing-4-7-note: Add 4.7-awareness note to CONTRIBUTING guidance

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- Galadriel on-ramp pillar P-2 (contributor education)
- PRD DX pillars — "scannable triage + authoring invariants"
- Fresh-challenger F-C-08 (honest labeling requires honest authoring culture)

## Context

The 4.6 → 4.7 migration establishes authoring invariants (no `budget_tokens`, no adaptive-thinking assumptions in prose, honest `model_awareness` stamping, etc.) that new contributors must honor when adding or editing skills. Today the repo has CLAUDE.md and inline skill-authoring references, but no CONTRIBUTING.md section that says "if you edit a SKILL.md, here is what you owe to 4.7 compatibility."

Galadriel pillar P-2 (contributor education) flagged this as an on-ramp deliverable — not required for the migration itself to succeed, but cheap insurance against regression by a well-meaning contributor who doesn't know the invariants.

## Proposed scope

- Add a "Claude 4.7 authoring notes" section to `CONTRIBUTING.md` (creating the file if absent) covering:
  - `model_awareness` frontmatter expectations (what the markers mean, when each is appropriate).
  - Do/don't list: don't `budget_tokens`, don't over-pressure with `CRITICAL:`/`MUST` blocks, don't assume adaptive thinking is on.
  - Pointer to the `prompt-engineer/` pattern library for authoring examples.
  - Pointer to the 4.7 migration guide (BACKLOG-47-migration-guide-stub).
- Link the section from the PR template (if one exists) or from CLAUDE.md's "Key Conventions" section.

## Out of scope for this item

- Writing the migration guide itself (that's BACKLOG-47-migration-guide-stub).
- Building the reference authoring skill (that's BACKLOG-47-4-7-example-skill-designation).
- Changing any existing skill content.

## Success criteria

- `CONTRIBUTING.md` exists and has a "Claude 4.7 authoring notes" section.
- The section is linked from CLAUDE.md (or the PR template if applicable).
- A contributor can answer "what does `model_awareness: opus-4-7` obligate me to?" without asking a maintainer.

## Priority & effort (rough)

- Priority: low
- T-shirt: XS (single docs PR)
- Depends on: BACKLOG-47-migration-guide-stub (for the link target to exist first — or both ship together).
