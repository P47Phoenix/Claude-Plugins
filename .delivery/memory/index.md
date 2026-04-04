# Memory Index

**Last updated**: 2026-04-03
**Total runs**: 8

## Stage Health (from last 5 runs)

| Stage | First-Try Pass Rate | Trend | Notes |
|-------|-------------------|-------|-------|
| Idea | 100% (5/5) | Stable | Perfect since run 4 |
| Refine | 100% (2/2) | Stable | Only ran in 2 of last 5 (BUG_FIX+SPIKE skipped) |
| Design | 100% (2/2) | Stable | Ran in 2 of last 5 |
| Architect | 100% (3/3) | Stable | Ran in 3 of last 5 |
| Plan | 50% (2/4) | **Declining** | 3 failures in 7 total runs — systemic weak point |
| Development | 100% (5/5) | Stable | Perfect across all run types |
| UAT | 100% (4/4) | Stable | Includes GREENFIELD with 2 in-flight defect fixes |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Gate-patterns memory injection yields compound returns — but Plan stage needs pre-loaded constraints → topics/gate-patterns.md
3. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
4. Agent validation of format-critical rules must be deterministic (API-driven), not LLM-inferred → stages/uat.md
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
