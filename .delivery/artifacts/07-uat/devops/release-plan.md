# Release Plan — Documentation Harmonization

**DevOps**: Sam | **Stage**: 7 UAT | **Date**: 2026-04-14 | **Run**: run-2026-04-11-f7g4

## Change Inventory

**New docs (5)**:
- `mtg-commander/README.md`
- `mtg-commander/.mtg-commander.yml.example`
- `mtg-commander/references/config-walkthrough.md`
- `delivery-team/skills/delivery-flow/references/constraints-quickstart.md`
- `delivery-team/skills/delivery-flow/references/troubleshooting.md`

**Updated docs (5+)**:
- `CLAUDE.md` (mtg-commander + paradigms/ + transformation-planning + constraints.yml surfaced)
- `README.md` (root — What's new + mtg-commander surfacing)
- `.claude-plugin/marketplace.json` (6 plugins registered)
- `delivery-team/skills/architect/references/volatility-decomposition.md` (redirect stub -> `../paradigms/`)
- `delivery-team/skills/architect/references/strategic-ddd.md` (redirect stub -> `../paradigms/`)

## Release Steps

1. Stage modified + new files via `git add -p` (selective, no secret leakage).
2. Commit: `docs: harmonize mtg-commander + constraints + troubleshooting references`.
3. Push to `main` (docs-only).
4. Verify GitHub renders landing pages (root + mtg-commander dir).
5. Announce in retrospective + memory index bump.

## Risk

**Minimal** — docs-only. No code paths or plugin manifests restructured beyond registry entry count (verified 6). No hooks, skills, scripts altered.

## Rollback

`git revert <commit-sha>` — single atomic commit restores prior state. No downstream consumers to notify.

## Sign-off

DevOps: APPROVED for release.
