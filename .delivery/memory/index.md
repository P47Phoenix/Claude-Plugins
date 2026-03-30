# Memory Index

**Last updated**: 2026-03-29
**Total runs**: 4

## Stage Health (from last 4 runs)

| Stage | First-Try Pass Rate | Trend | Notes |
|-------|-------------------|-------|-------|
| Idea | 75% (3/4) | +8% | Run 3: phantom ref (round 2). Run 4: pass |
| Refine | 100% (3/3) | = | Consistent. 1 run skipped (BUG_FIX) |
| Design | 33% (1/3) | -17% | Runs 1+3: round 2. Run 4: first-try (gate-patterns injection). 1 run skipped (BUG_FIX) |
| Architect | 100% (2/2) | = | Only ran in 2 of 4 runs (light depth both times) |
| Plan | 50% (2/4) | -33% | Runs 1+4: round 2 (capacity). Runs 2+3: pass |
| Development | 75% (3/4) | -8% | Run 1: stale schema.json. Runs 2-4: pass |
| UAT | 50% (2/4) | -17% | Run 1: dogfooding deferred. Run 3: DEFECT-001. Runs 2+4: pass |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
3. Read gate-patterns.md before stages with <80% pass rate — contributed to Design first-try pass → stages/design.md
4. Markdown-only edits need calibrated estimates (one tier lower than code) — Plan capacity ceiling → stages/plan.md
5. PO must check git history before bug prioritization — avoids duplicate work → topics/human-preferences.md

## Topic Files (read when relevant)

| Topic | When to Read | File |
|-------|-------------|------|
| Human preferences | Before any human checkpoint AND at pipeline start | topics/human-preferences.md |
| Team decisions | Before Architect or Plan stages | topics/team-decisions.md |
| Gate failure patterns | Before any stage with <80% pass rate (Design, Plan, UAT) | topics/gate-patterns.md |
| Defect patterns | When defects are logged | topics/defect-patterns.md |
| Project type patterns | At pipeline start (type-specific lessons) | topics/project-types.md |

## Stage Chunks (read per-stage)

| Stage | File |
|-------|------|
| Design | stages/design.md |
| Plan | stages/plan.md |
| Development | stages/development.md |
| UAT | stages/uat.md |
