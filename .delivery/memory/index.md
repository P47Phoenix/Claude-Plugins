# Memory Index

**Last updated**: 2026-03-29
**Total runs**: 3

## Stage Health (from last 3 runs)

| Stage | First-Try Pass Rate | Notes |
|-------|-------------------|-------|
| Idea | 67% | Run 3: Architect found phantom ref (round 2 pass) |
| Refine | 100% | Run 3: clean after adversarial fixes applied pre-DoD |
| Design | 50% | Run 2: FR traceability gaps. Run 3: filename + positioning errors |
| Architect | 100% | Run 3: light depth, clean pass |
| Plan | 83% | Run 1: SM capacity + QA gaps. Run 2+3: clean |
| Development | 83% | Run 1: stale schema.json. Run 2+3: clean (CODE_COMPLETE) |
| UAT | 67% | Run 1: dogfooding deferred. Run 3: DEFECT-001 filename mismatch |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
3. Verify file references in idea briefs/architecture docs — Architect catches phantom refs → topics/gate-patterns.md
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
