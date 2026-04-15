# Sprint Plan — Defect Sweep (BUG_FIX, LIGHT)

**Artifact**: Sprint Plan (Aragorn / Scrum Bag)
**Mode**: LIGHT (BUG_FIX — no stories file)
**Pipeline**: delivery-flow
**Date**: 2026-04-14

> "A sweep, then. Four fixes, one sprint. No wizardry, no kings — just clean cuts."

## Fix List

| ID | Fix | Owner | AC | Estimate |
|----|-----|-------|-----|----------|
| FIX-1 | Remove project_type question from Quick-Start Mode | Gimli (developer) | `delivery-team/skills/delivery-flow/SKILL.md:142` no longer asks "What are you building?"; `references/getting-started.md:15` section removed or rewritten; Quick-Start question list drops to 2 questions (or adds an optional `force_type` pin); no `project_type` token remains in the Quick-Start flow | S |
| FIX-2 | v2.6 → v2.7 migration contract on config load | Gimli (developer) | SKILL.md (or `references/setup-wizard.md`) documents: on load, if `config_version` is `"2.6"` or missing → strip top-level `project_type`, bump `config_version` to `"2.7"`, emit migration announcement; in-repo `.delivery/config.yml` already v2.7, so this is forward-guard documentation (no runtime migration script required this sweep) | S |
| FIX-3 | `check_dod_constraints.py --skip-declarations` flag | Gimli (developer) | New CLI flag `--skip-declarations`; when set, `check_forbidden_vocab` excludes lines inside the artifact's own `forbidden_vocabulary:` YAML block (header + indented list items) before regex scan; running the script against its own constraints file with the flag returns exit 0; fixture added covering both flag-on and flag-off modes | S |
| FIX-4 | CI workflow injection regression guard | Gimli (developer) | New job or workflow lints `.github/workflows/*.yml`; multiline-greps each `run:` block for `${{ github.event.*`, `${{ github.head_ref`, `${{ github.pull_request.*`; fails CI if any hit; passes on current tree (DEFECT-004 version.yml already fixed); `docs.yml` audited in passing | S |

## Dependencies

None between fixes. All four are independent edits; execute in parallel or any order within a single sprint.

## Sprint Shape

- **Sprint count**: 1
- **Total estimate**: 4 × S
- **Parallelism**: full (no ordering constraints)

## Light-Mode Definition of Done

Per BUG_FIX light routing, DoD validators reduce to:

- **Developer (Gimli)**: implements, self-reviews, passes lints, confirms AC per fix.
- **QA (Legolas)**: smoke-verifies each fix — re-reads wizard text, runs `check_dod_constraints.py --skip-declarations` against the constraints file, triggers the CI lint against a synthetic bad workflow to prove it fails.

Skipped in light mode: adversarial review, consensus debate, architecture board, review board.

## Non-Goals (restating Idea-brief anti-scope)

- No schema changes past v2.7.
- No wizard UX redesign.
- No new features.
- No edits to architecture-board, constraints primitive, MTG plugin, or other v2.7-current behavior.
- No re-edit of `.github/workflows/version.yml` (primary DEFECT-004 fix already landed).

## Architect Check

Architect not convened (BUG_FIX skips Architect stage). Each fix is bounded by an existing defect report with an explicit proposed fix — no architectural ambiguity per `feedback_architect_examine_first`.

## Ready to Execute

Gimli may pick any FIX-N first. Suggested order by lowest friction: FIX-1 → FIX-4 → FIX-3 → FIX-2. No blockers.

> "One sprint. Fly, you fools — but fly in a straight line."
