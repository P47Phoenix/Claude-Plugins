# Release Plan — US-9 Adversarial Challenger Agents

**Release Manager**: Sam (DevOps)
**Pipeline**: run-2026-04-11-e6f3
**Date**: 2026-04-11

## Change Inventory

| File | Change Type | Lines Changed |
|------|-------------|---------------|
| `mtg-commander/SKILL.md` | Modified (augmented) | +199 net (980 -> 1179) |
| `mtg-commander/references/rules-judge-guide.md` | Modified | Challenger integration + deterministic mandate |
| `mtg-commander/references/price-evaluator-guide.md` | Modified | CK divergence + Price Challenger integration |

## NOT Shipped (User-Side)

- `.mtg-commander.yml` — user-created config in THEIR repo, not ours. We ship defaults.

## Release Steps

1. Commit changes on feature branch (`feat/us9-adversarial-challengers`)
2. PR to `main` with conventional commit: `feat(mtg-commander): add adversarial challenger agents with sub-agent dispatch guardrail (#US-9)`
3. Merge (squash) after CI green
4. Tag: `v2.18.0` (minor — new feature, backwards compatible)
5. Update `marketplace.json` description if needed

## Rollback Plan

```bash
git revert <merge-commit-sha>
```

No schema migration. No database. No external state.
The `.mtg-commander.yml` config is optional — absence = defaults.
Revert removes challenger prompts; pipeline reverts to pre-adversarial behavior.

## Risk Assessment

- **Low**: All changes are prompt-level (SKILL.md + reference guides)
- **No runtime dependencies** added
- **Backwards compatible**: no config = existing behavior preserved
