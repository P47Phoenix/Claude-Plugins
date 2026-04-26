# BACKLOG-47-4-7-example-skill-designation: Designate a canonical "4.7 exemplar" skill

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- Galadriel on-ramp pillar P-4 (exemplar skill for contributor reference)
- Fresh-challenger F-C-08 (scannable triage needs a "gold-standard" anchor)
- Plan WI-05 (pattern library location — ADR-005)

## Context

After the migration, 6 keystone SKILL.md files are fully reviewed and stamped `opus-4-7`. One of them should be promoted to the role of **canonical 4.7 exemplar**: the file a new contributor reads first when learning how to write a skill that is 4.7-aware. Galadriel pillar P-4 identified this as an under-appreciated on-ramp lever — teaching by concrete reference beats teaching by abstract authoring rules.

The candidates are the six keystones that got a full prose review. The decision is both *which* keystone and *how* it gets marked (a `role: 4-7-exemplar` frontmatter field? A README pointer? A link in CONTRIBUTING?).

## Proposed scope

- Review the six fully-audited keystone SKILL.md files and pick the one that best embodies 4.7 authoring principles (honest `model_awareness`, no over-pressure, clean role isolation, explicit input/output contracts, adaptive-thinking-agnostic prose).
- Extend the `model_awareness` frontmatter schema (or add a sibling field) to mark the chosen file as the exemplar. Alternative: add a `# See Also` block at the top of less-exemplary SKILL.md files pointing at it.
- Reference the exemplar from:
  - `CONTRIBUTING.md` (see BACKLOG-47-contributing-4-7-note)
  - `docs/migrations/4.6-to-4.7.md` (see BACKLOG-47-migration-guide-stub)
  - `CLAUDE.md` Key Conventions section.
- Confirm with a fresh contributor dogfood: can they author a new skill correctly using only the exemplar + CONTRIBUTING? If not, iterate.

## Out of scope for this item

- Rewriting any of the six keystone files to *be* a better exemplar. Pick the best-as-it-stands; exemplar-upgrades are follow-on work.
- Designating exemplars for other quality attributes (security, accessibility, etc.) — that's a separate discussion.
- Creating a non-skill "template" file — the value proposition is that a *real working skill* is the reference, not a placeholder.

## Success criteria

- Exactly one skill in the repo carries the "4.7 exemplar" designation.
- The designation is discoverable from CLAUDE.md and CONTRIBUTING.md.
- A fresh-contributor dogfood produces a valid 4.7-aware SKILL.md using only the exemplar + CONTRIBUTING as guidance.

## Priority & effort (rough)

- Priority: low
- T-shirt: XS (mostly a selection decision + a few pointer edits).
- Depends on: BACKLOG-47-contributing-4-7-note, BACKLOG-47-migration-guide-stub (for the link targets to exist).
