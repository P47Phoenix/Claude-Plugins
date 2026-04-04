# Memory Index

**Last updated**: 2026-04-04
**Total runs**: 11

## Stage Health (from last 5 runs)

| Stage | First-Try Pass Rate | Trend | Notes |
|-------|-------------------|-------|-------|
| Idea | 100% (5/5) | Stable | Perfect streak continues |
| Refine | 100% (2/2) | Stable | Only ran in 2 of last 5 |
| Design | 100% (2/2) | Stable | Ran in 2 of last 5 |
| Architect | 100% (3/3) | Stable | Ran in 3 of last 5 |
| Plan | 80% (4/5) | **Improving** | 2 consecutive first-try passes with pre-loaded constraints |
| Development | 60% (3/5) | Dipped | Derived artifacts corrections in w7m3 + p5v8 |
| UAT | 100% (5/5) | Stable | 5 consecutive first-try passes |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Gate-patterns memory injection yields compound returns — but Plan stage needs pre-loaded constraints → topics/gate-patterns.md
3. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
4. Installed↔source file sync is mandatory — Dev must commit to source, validators must check installed → stages/uat.md
5. Plan stage agents need pre-loaded constraints (sprint ceiling, mandatory artifacts) → stages/plan.md

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
