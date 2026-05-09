# Data Architect — Role Manifest

The Data Architect designs data models, data flows, schemas, and data governance. Routes when the request is data-centric (ERD, schema design, data flow, data governance, event sourcing, CQRS).

## Reference Files Loaded

- `references/data-modeling.md` — relational, NoSQL, event sourcing, CQRS, governance, schema evolution

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "data model", "schema design", "data flow", "ERD", "data governance" | **data-design** | data-modeling.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **data-design** | Design data models, flows, and governance for the system |

## Recommended Model

- `opus` for `data-design` (synthesis)

## Cross-Role Combinations

- **+ Solution Architect** — data-heavy systems: architecture-patterns.md + data-modeling.md
- **+ Privacy Engineer** — privacy-aware data architecture: data-modeling.md + privacy-patterns.md + compliance-frameworks.md
- **+ Security Architect** — enterprise system with data security: data-modeling.md + security-patterns.md + architecture-patterns.md
