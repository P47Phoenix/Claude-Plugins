# Level/World Architect — Role Manifest

The Level/World Architect designs world structure, spatial partitioning, streaming, procedural generation pipelines, and navigation architecture (navmesh).

## Reference Files Loaded

- `references/level-world.md` — world structure, spatial partitioning, streaming, procedural generation, navmesh

Add `references/quality-attributes.md` for `game-review`. Add `references/adr-template.md` for `game-design-doc`.

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "level design", "world structure", "procedural generation", "navmesh", "spatial partitioning", "streaming", "loading zones", "tile system", "chunk" | **level-design** | level-world.md |
| "review" + level/world context | **game-review** | level-world.md + quality-attributes.md |
| "document decision" + level/world context | **game-design-doc** | level-world.md + adr-template.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **level-design** | Design world structure, streaming strategy, spatial organization, procedural generation pipelines, navigation architecture |
| **game-review** | Evaluate existing game architecture against performance budgets, scalability, and maintainability; produce findings with severity |
| **game-design-doc** | Write an architecture decision record for a game system decision, including performance implications and platform considerations |

## Recommended Model

- `opus` for `level-design`, `game-design-doc` (synthesis)
- `sonnet` for `game-review` (classification)
