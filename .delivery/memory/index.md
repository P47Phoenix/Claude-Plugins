# Memory Index

**Last updated**: 2026-04-11
**Total runs**: 23

## Stage Health (from last 5 runs)

| Stage | First-Try Pass Rate | Trend | Notes |
|-------|-------------------|-------|-------|
| Idea | 100% (5/5) | Stable | Perfect streak continues |
| Refine | 100% (2/2) | Stable | Only ran in 2 of last 5 |
| Design | 100% (2/2) | Stable | Ran in 2 of last 5 |
| Architect | 100% (3/3) | Stable | Ran in 3 of last 5 |
| Plan | 60% (3/5) | **Regressed** | run-a1f3 needed 3 DoD rounds (stale SM artifact, amendments not propagated); meta-irony — the very feature being built |
| Development | 80% (4/5) | **Improving** | Clean first-try in 3d92; derived artifacts lesson applied proactively |
| UAT | 100% (5/5) | Stable | 5 consecutive first-try passes |

## Hot Lessons (top 5 by impact)

1. ALL work routes through delivery-flow pipeline — never implement directly → topics/human-preferences.md
2. Gate-patterns memory injection yields compound returns — but Plan stage needs pre-loaded constraints → topics/gate-patterns.md
3. Dogfooding is a P0 UAT gate, not a follow-up — execute before DoD submission → stages/uat.md
4. Installed↔source file sync is mandatory — Dev must commit to source, validators must check installed → stages/uat.md
5. Propagate amendments to authoritative artifacts, not just referencing ones → topics/gate-patterns.md / stages/plan.md
6. Dogfood the capability on its own architecture in the same build that introduces it — validates end-to-end AND catches gaps the primary authors miss. Second instance 2026-04-08-b2c7. → stages/development.md

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
