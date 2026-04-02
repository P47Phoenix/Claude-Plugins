# Memory Index

**Last updated**: 2026-04-01
**Total runs**: 7

## Stage Health (from last 5 runs)

| Stage | First-Try Pass Rate | Trend | Notes |
|-------|-------------------|-------|-------|
| Idea | 100% (5/5) | +20% | Perfect since run 4 |
| Refine | 100% (2/2) | = | Only ran in 2 of last 5 (BUG_FIX+SPIKE skipped) |
| Design | 100% (1/1) | +33% | Only ran in 1 of last 5 |
| Architect | 100% (3/3) | = | Ran in 3 of last 5 (2 light, 1 full SPIKE) |
| Plan | 100% (3/3) | +20% | Ran in 3 of last 5 (2 skipped for SPIKE) |
| Development | 100% (5/5) | = | Perfect across all run types |
| UAT | 100% (3/3) | +20% | Ran in 3 of last 5 (SPIKE skipped) |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Gate-patterns memory injection yields compound returns — 3 consecutive 100% first-try DoD runs → topics/gate-patterns.md
3. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
4. Data-driven analysis prevents over-engineering — survey actual state before proposing infrastructure → stages/development.md
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
