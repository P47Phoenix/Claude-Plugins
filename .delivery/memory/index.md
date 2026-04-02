# Memory Index

**Last updated**: 2026-04-01
**Total runs**: 6

## Stage Health (from last 5 runs)

| Stage | First-Try Pass Rate | Trend | Notes |
|-------|-------------------|-------|-------|
| Idea | 80% (4/5) | = | Run 3: phantom ref. Runs 4-6: pass |
| Refine | 100% (3/3) | = | Consistent. 2 runs skipped (BUG_FIX) |
| Design | 67% (2/3) | +17% | Runs 4+5: first-try (gate-patterns). 2 skips |
| Architect | 100% (2/2) | = | Only ran in 2 of 6 runs |
| Plan | 80% (4/5) | +20% | Run 4: round 2. Runs 2+3+5+6: pass |
| Development | 100% (5/5) | = | Perfect since run 2 |
| UAT | 80% (4/5) | +20% | Run 3: DEFECT-001. Runs 2+4+5+6: pass |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Gate-patterns memory injection yields compound returns — 2 consecutive 100% first-try DoD runs → topics/gate-patterns.md
3. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
4. Retro improvement actions are highest-value BUG_FIX candidates — triage into backlog immediately → stages/uat.md
5. Tech Writer validator in plugin repos must search installed files, not repo source → stages/uat.md

## Topic Files (read when relevant)

| Topic | When to Read | File |
|-------|-------------|------|
| Human preferences | Before any human checkpoint AND at pipeline start | topics/human-preferences.md |
| Team decisions | Before Architect or Plan stages | topics/team-decisions.md |
| Gate failure patterns | Before any stage with <80% pass rate | topics/gate-patterns.md |
| Defect patterns | When defects are logged | topics/defect-patterns.md |
| Project type patterns | At pipeline start (type-specific lessons) | topics/project-types.md |

## Stage Chunks (read per-stage)

| Stage | File |
|-------|------|
| Design | stages/design.md |
| Plan | stages/plan.md |
| Development | stages/development.md |
| UAT | stages/uat.md |
