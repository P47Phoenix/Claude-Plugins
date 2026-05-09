# Solution Architect — Role Manifest

The Solution Architect designs single-system or single-feature architectures, evaluates designs, produces ADRs, and selects technology for one bounded scope. The Solution role owns the broadest set of task types in the architect skill — most software design work routes here unless an explicit Enterprise / Data / Security signal redirects it.

## Reference Files Loaded

- `references/architecture-patterns.md` — architecture styles (layered, hexagonal, clean, microservices, event-driven, DDD, modular monolith)
- `references/c4-model.md` — context / container / component / code diagrams (Mermaid + PlantUML notation)
- `references/adr-template.md` — ADR template, lifecycle, examples
- `references/quality-attributes.md` — ISO 25010, ATAM, measurable scenarios, architectural tactics

Add `references/domain-discovery.md` for `design` / `decompose` task types (interview first).

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "design", "architect a solution", "system design", "how should we build" | **design** | architecture-patterns.md, c4-model.md + domain-discovery.md (interview first) |
| "review architecture", "evaluate design", "architecture assessment" | **review** | architecture-patterns.md, quality-attributes.md |
| "ADR", "architecture decision", "document decision" | **document** | adr-template.md |
| "technology evaluation", "compare technologies", "tech selection", "build vs buy" | **evaluate** | technology-evaluation.md (shared with Enterprise) |
| "decompose", "service boundaries", "bounded context", "break apart", "modularize", "volatility", "IDesign", "team topology", "event storming", "subdomain" | **decompose** | architecture-patterns.md, c4-model.md + configured decomposition reference |
| "C4", "context diagram", "container diagram", "component diagram" | **model** | c4-model.md |
| "quality attributes", "non-functional", "scalability", "performance architecture", "-ilities" | **analyze-quality** | quality-attributes.md, architecture-patterns.md |
| "integration", "API design", "event-driven", "messaging" | **integration** | architecture-patterns.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **design** | Create a complete architecture for a system or feature, including component breakdown, interactions, data flows, and C4 diagram descriptions |
| **review** | Evaluate existing architecture against quality attributes and patterns; produce findings with severity (critical / warning / suggestion) |
| **document** | Write an Architecture Decision Record capturing context, decision, consequences, and alternatives |
| **evaluate** | Compare technologies or approaches using a weighted criteria matrix with explicit scoring |
| **decompose** | Break a system into services/components with clear boundaries, data ownership, and communication patterns |
| **model** | Produce C4 diagram descriptions (text-based, Mermaid/PlantUML compatible) at the appropriate level |
| **analyze-quality** | Analyze quality attributes with measurable scenarios and recommend architectural tactics |
| **integration** | Design integration architecture: APIs, events, messaging patterns, protocol selection |

## Recommended Model

- `sonnet` for `review` (classification)
- `opus` for `design`, `decompose`, `model`, `analyze-quality`, `integration` (synthesis)
- `sonnet` for `document` (template-driven) and `evaluate` (matrix-driven)

## Cross-Role Combinations

- **+ Data Architect** — data-heavy systems (analytics, leaderboards): architecture-patterns.md + data-modeling.md
- **+ Security Architect** — secure system design: architecture-patterns.md + security-patterns.md
- **+ Enterprise Architect** — `evaluate` task spanning portfolio: architecture-patterns.md + enterprise-patterns.md
- **Full system design** — architecture-patterns.md + c4-model.md + quality-attributes.md
