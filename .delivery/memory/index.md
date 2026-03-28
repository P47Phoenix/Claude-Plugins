# Memory Index

**Last updated**: 2026-03-27
**Total runs**: 1

## Stage Health (from last 1 run)

| Stage | First-Try Pass Rate | Notes |
|-------|-------------------|-------|
| Idea | 100% | Clean pass |
| Refine | 100% | Clean pass |
| Design | 50% | PO found 5 FR traceability gaps |
| Architect | 100% | Clean pass (light depth) |
| Plan | 50% | SM: capacity missing, QA: FR-14/15 test gaps |
| Development | 50% | Architect: stale config-schema.json |
| UAT | 33% | PO: dogfooding deferred, QA: review scope narrow |

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
