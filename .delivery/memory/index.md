# Memory Index

**Last updated**: 2026-04-01
**Total runs**: 5

## Stage Health (from last 5 runs)

| Stage | First-Try Pass Rate | Trend | Notes |
|-------|-------------------|-------|-------|
| Idea | 80% (4/5) | +5% | Run 3: phantom ref (round 2). Run 5: pass |
| Refine | 100% (4/4) | = | Consistent. 1 run skipped (BUG_FIX) |
| Design | 50% (2/4) | +17% | Runs 1+3: round 2. Runs 4+5: first-try (gate-patterns injection confirmed). 1 skip |
| Architect | 100% (2/2) | = | Only ran in 2 of 5 runs (light depth both times) |
| Plan | 60% (3/5) | +10% | Runs 1+4: round 2 (capacity). Runs 2+3+5: pass |
| Development | 100% (4/4) | +25% | Run 1: stale schema.json. Runs 2-5: pass |
| UAT | 60% (3/5) | +10% | Run 1: dogfooding deferred. Run 3: DEFECT-001. Runs 2+4+5: pass |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Gate-patterns memory injection yields compound returns — run r4x2 achieved 100% first-try DoD (6/6). Read gate-patterns.md before stages with <80% pass rate → topics/gate-patterns.md
3. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
4. Adversarial review at Plan prevents sprint overloading — two correction rounds in r4x2 produced exact-delivery plan → stages/plan.md
5. Structural-only validation should cap confidence below 5/5 — carry P1 follow-up when bash unavailable → stages/uat.md

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
