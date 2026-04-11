# Release Plan — paradigm-as-skill extraction (run d5e2)

**Role:** Sam (DevOps / Release Manager) | 2026-04-10

## Change Inventory

### New Files
- `delivery-team/skills/architect/paradigms/volatility/SKILL.md`
- `delivery-team/skills/architect/paradigms/volatility/references/volatility-decomposition.md`
- `delivery-team/skills/architect/paradigms/volatility/references/domain-discovery-volatility.md`
- `delivery-team/skills/architect/paradigms/ddd/SKILL.md`
- `delivery-team/skills/architect/paradigms/ddd/references/strategic-ddd.md`
- `delivery-team/skills/delivery-flow/references/design-sprint.md`

### Edited Files
- `delivery-team/skills/architect/SKILL.md` (Paradigm Router added; paradigm_id routing)

### Redirect Stubs (moved-content pointers)
- `delivery-team/skills/architect/references/volatility-decomposition.md`
- `delivery-team/skills/architect/references/strategic-ddd.md`

## Release Steps

1. All 15 TCs green (verified this run).
2. Commit on feature branch: `feat(architect): extract paradigms to sub-skills with context-isolated routing`.
3. PR with diff review on architect SKILL.md router + paradigm SKILL.md files.
4. Merge to main. No version bump (additive sub-skill extraction, no schema change).
5. Cache sync: no action needed (paradigm sub-skills are file-based, no generated artifacts).

## Rollback

`git revert` merge commit + restore original `volatility-decomposition.md` and `strategic-ddd.md` from pre-redirect content. Zero persisted state; no config migration. RTO: <2 minutes.

## Risk

**Low.** Additive restructure. Default routing falls back to monolithic architect skill. Paradigm sub-skills are opt-in via router dispatch. ADR-001 compliance verified (not registered in marketplace.json).
