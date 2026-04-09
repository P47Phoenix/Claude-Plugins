# Release Plan — transformation-planning (run c4d1)

**Role:** Sam (DevOps / Release Manager) | 2026-04-08

## Change Inventory

- `delivery-team/skills/architect/references/transformation-planning.md` (new, orchestrator ref)
- `delivery-team/skills/architect/references/transformation-phase-1a-behavioral.md` (new)
- `delivery-team/skills/architect/references/transformation-phase-1b-structural.md` (new)
- `delivery-team/skills/architect/references/transformation-phase-2-to-be.md` (new)
- `delivery-team/skills/architect/references/transformation-phase-3-roadmap.md` (new)
- `delivery-team/skills/architect/SKILL.md` (3 transformation-planning references added; additive routing)
- `.delivery/artifacts/08-transform/{as-is-constraints.yml, as-is-use-cases.md, to-be-constraints.yml, roadmap.md}` (dogfood outputs)

## Release Steps

1. Run `python3 delivery-team/skills/delivery-flow/scripts/validate_constraints.py` on all 3 constraints files (pre-merge gate) — currently PASS.
2. Commit on feature branch; conventional commit `feat(architect): add transformation-planning task_type`.
3. Open PR; require architect SKILL.md diff review + ref-docs spot check.
4. Merge to main; no version bump (additive reference files, no schema change).
5. Announce in release notes; link BACKLOG-006 for Step 5 (real orchestrator wiring).

## Rollback

`git revert` the merge commit. Zero persisted state; no config schema change; no migration required. RTO: <2 minutes.

## Observability

- Monitor pipeline runs for Architect stage dispatching `transformation_planning` task_type (grep memory logs).
- Track whether 08-transform artifacts are produced on brownfield engagements.
- Alert: none required (additive, no new runtime path in orchestrator yet — Step 5 deferred).

## Risk

**Low.** Purely additive; validators green; dogfooded on this repo.
