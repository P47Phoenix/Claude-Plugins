# g8h5 Docs Delta — Tech Writer Log

**Alias:** Bilbo Baggins
**Commit reflected:** 3aee2f9
**Scope:** surgical user-facing doc updates for 4 shipped changes.

## Changes reflected

1. Quick-Start Mode is now 2 questions (project_type question removed in v2.7).
2. v2.6 → v2.7 config migration rule (orchestrator strips `project_type` + bumps version).
3. `check_dod_constraints.py --skip-declarations` flag for self-comparison.
4. `.github/workflows/workflow-injection-lint.yml` regression guard (DEFECT-004).

## Files touched

| File | Edit summary | Lines added (approx) |
|------|--------------|----------------------|
| `delivery-team/skills/delivery-flow/references/troubleshooting.md` | Added entries #10 (v2.6→v2.7 migration) and #11 (self-compare false positives); renumbered "Where do I find" to #12 | +22 |
| `delivery-team/skills/delivery-flow/references/constraints-quickstart.md` | Added "Self-checking?" note under §6 Validate it | +6 |
| `CLAUDE.md` | Added "CI regression guards" mini-section after Hooks table | +3 |
| `README.md` | Added "Defect sweep" bullet to What's New | +1 |
| `delivery-team/skills/delivery-flow/references/getting-started.md` | "3 Questions" → "2 Questions" in header, body, walkthrough, defaults section; removed "What are you building?" Q1; noted v2.7 detection-per-run | ~-20 / +5 net |

## Verification greps

| Check | Path | Expected | Actual |
|-------|------|----------|--------|
| `skip-declarations` | constraints-quickstart.md | ≥1 | **1** |
| `v2\.6.*v2\.7\|migration\|Migrated config` | troubleshooting.md | ≥1 | **2** |
| `workflow-injection-lint\|--skip-declarations\|defect sweep` | README.md | ≥1 | **1** |
| `2 Questions\|2-question` | getting-started.md | ≥1 | **2** |
| `workflow-injection-lint` | CLAUDE.md | ≥1 | **1** |

All checks pass. Existing content preserved; no structural rewrites.

> *"Short cuts make long delays, but a short doc-diff makes a short PR."* — Bilbo
