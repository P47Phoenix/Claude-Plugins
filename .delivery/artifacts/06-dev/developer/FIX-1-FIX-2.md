# FIX-1 + FIX-2 — DEFECT-003 Resolution

**Run**: run-2026-04-11-g8h5
**Alias**: Gimli (developer)
**Defect**: DEFECT-003 (wizard/schema drift v2.6 → v2.7)

## Files Touched

1. `delivery-team/skills/delivery-flow/SKILL.md`
   - Lines 145–152 (Quick-Start Mode): dropped the "What are you building?" question, renumbered 3 → 2, added the "Project type is detected per run in Phase 1" note referencing `routing.force_type`.
   - Lines 96–107 (Phase 0 Version check): appended the v2.6 → v2.7 migration rule. In-memory strip of `project_type`, announce the migration, recommend re-running `setup` to persist (no silent auto-write).

2. `.delivery/defects/DEFECT-003.md`
   - Appended `Status: CLOSED — fixed in run-2026-04-11-g8h5` under the Status section (convention matches DEFECT-001/002).

## Verification

Grep for the removed question in SKILL.md:

```
$ grep -n "What are you building" delivery-team/skills/delivery-flow/SKILL.md
(no matches)
```

Quick-Start Mode now reads:

```
### Quick-Start Mode
If the user says "quick start", ... run a 2-question wizard ...
1. **What language/framework?** -- auto-detect from codebase, user confirms
2. **How strict?** -- Prototype (minimal) / Standard (balanced) / Strict (full)
> Note: Project type is detected per run in Phase 1, not configured. Use `routing.force_type` if you want to pin it.
```

## Out of Scope (Deliberate)

- `setup-wizard.md` already correctly documents the v2.7 removal (Q1 gone, 9 questions down from 10) — no changes needed.
- `.delivery/config.yml` already manually migrated to v2.7 in a prior session.
