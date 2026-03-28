# Memory Index

**Last updated**: 2026-03-28
**Total runs**: 2

## Stage Health (from last 2 runs)

| Stage | First-Try Pass Rate | Notes |
|-------|-------------------|-------|
| Idea | 100% | Clean pass both runs |
| Refine | 100% | 1 run (FEATURE), skipped for BUG_FIX |
| Design | 50% | 1 run — PO found 5 FR traceability gaps |
| Architect | 100% | 1 run (light depth) |
| Plan | 75% | Run 1: SM capacity + QA gaps. Run 2: clean pass (light) |
| Development | 75% | Run 1: stale schema.json. Run 2: clean pass |
| UAT | 50% | Run 1: dogfooding deferred + review scope. Run 2: clean pass |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
3. Derived artifacts (schema.json) must be regenerated after source changes → stages/development.md
4. Design/Plan must trace to ALL PRD FRs — validators check FR-by-FR → topics/gate-patterns.md
5. Use plugin-dev skills when modifying plugin components → topics/human-preferences.md

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
