# Release Plan — Architecture Board Capability (run-2026-04-08-b2c7)

**Role:** Release Manager — *Samwise Gamgee* (steady on the road)
**Change ID:** BACKLOG-003 (+ absorbed -002)

## Change Inventory

- NEW: `delivery-team/skills/delivery-flow/references/architecture-board-personas.md` (4 personas)
- MOD: `config-schema.md` — `architecture_board` block (v2.7), default `enabled: false`
- MOD: `team-patterns.md` — Architecture Board Review pattern
- MOD: `pipeline-stages.md` — Stage 4 conditional board invocation
- NEW: dogfood sample under `.delivery/artifacts/04-architect/board/`

## Release Steps

1. `git add` the modified references + new personas file
2. Conventional commit: `feat(delivery-flow): add configurable architecture board (BACKLOG-003)`
3. `git push origin main` (or branch + PR per repo convention)
4. Marketplace rsync/cache refresh (standard plugin publish path)
5. Smoke check: load `delivery-team:delivery-flow` in a fresh project — default disabled, zero behavior change

## Rollback

`git revert <sha>` — trivially safe. Default `enabled: false` means no in-flight pipelines depend on the new code path. No data migration, no config break.

## Observability

First real run with `architecture_board.enabled: true` produces:
- N reviewer artifacts in `.delivery/artifacts/04-architect/board/*-review.md`
- 1 `judge-verdict.md` with PASS / CONDITIONAL / FAIL + rationale
- Token overhead logged toward NFR-1 baseline

## GO Criteria

- [x] All QA TCs pass (test-results.md)
- [x] PO final DoD GO (po-final.md)
- [x] Backwards compat verified (default off)
- [x] Rollback documented and trivial

**Status:** GO for release. — *Sam*
