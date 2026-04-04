# Memory Index

**Last updated**: 2026-04-03
**Total runs**: 8

## Stage Health (from last 5 runs)

| Stage | First-Try Pass Rate | Trend | Notes |
|-------|-------------------|-------|-------|
| Idea | 100% (5/5) | = | Perfect streak continues |
| Refine | 100% (3/3) | = | GREENFIELD run added (2 skipped: BUG_FIX, SPIKE) |
| Design | 100% (2/2) | = | GREENFIELD run added |
| Architect | 100% (4/4) | = | GREENFIELD full + 2 light + SPIKE full |
| Plan | 80% (4/5) | -20% | GREENFIELD Plan took 2 rounds (SM ceiling + QA stale test strategy) |
| Development | 100% (5/5) | = | Perfect across all run types |
| UAT | 100% (4/4) | = | GREENFIELD passed with 2 defects found+fixed |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. LLM card/domain knowledge is unreliable — programmatic API validation is mandatory for correctness gates → stages/uat.md
3. Single-source pricing creates false confidence — dual-vendor pricing exposes real budget gaps → stages/uat.md
4. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
5. GREENFIELD plugins need fresh test strategies — stale files from previous pipelines cause false DoD failures → stages/plan.md

## Topic Files (read when relevant)

| Topic | When to Read | File |
|-------|-------------|------|
| Human preferences | Before any human checkpoint AND at pipeline start | topics/human-preferences.md |
| Team decisions | Before Architect or Plan stages | topics/team-decisions.md |
| Gate failure patterns | Before any stage with <80% pass rate (Plan) | topics/gate-patterns.md |
| Defect patterns | When defects are logged | topics/defect-patterns.md |
| Project type patterns | At pipeline start (type-specific lessons) | topics/project-types.md |

## Stage Chunks (read per-stage)

| Stage | File |
|-------|------|
| Design | stages/design.md |
| Plan | stages/plan.md |
| Development | stages/development.md |
| UAT | stages/uat.md |
