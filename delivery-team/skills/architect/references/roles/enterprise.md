# Enterprise Architect — Role Manifest

The Enterprise Architect operates at portfolio / cross-system scope. Capability mapping, technology radar, governance alignment, and TOGAF-subset artifacts are the domain. Enterprise routes when scope crosses system boundaries or when strategic alignment / portfolio decisions are needed.

## Reference Files Loaded

- `references/enterprise-patterns.md` — TOGAF subset, capability mapping, technology radar, portfolio management
- `references/technology-evaluation.md` — weighted criteria matrix, build vs buy, PoC design, migration cost (shared with Solution)

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "capability map", "technology portfolio", "technology radar", "TOGAF", "strategic alignment", "governance" | **strategic** | enterprise-patterns.md |
| "technology evaluation", "compare technologies", "tech selection", "build vs buy" (portfolio scope) | **evaluate** | technology-evaluation.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **strategic** | Create enterprise-level artifacts: capability maps, technology radar entries, portfolio assessments |
| **evaluate** | Compare technologies or approaches using a weighted criteria matrix with explicit scoring (portfolio scope) |

## Recommended Model

- `opus` for `strategic` (synthesis)
- `sonnet` for `evaluate` (matrix-driven)

## Routing Note

`evaluate` task type is shared with Solution Architect. Enterprise scope is selected when the technology choice spans multiple systems or affects organizational strategy; Solution scope when the choice is bounded to a single system.
