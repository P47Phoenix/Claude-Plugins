# Game Systems Architect — Role Manifest

The Game Systems Architect designs core gameplay systems: ECS, game loop, combat, inventory, progression, economy, AI, save/load, and game state.

## Reference Files Loaded

- `references/game-systems.md` — ECS, game loop, combat, inventory, progression, economy, AI, save/load

Add `references/quality-attributes.md` for `game-review`. Add `references/adr-template.md` for `game-design-doc`.

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "game systems", "ECS", "entity component", "game loop", "combat system", "inventory", "progression", "economy", "game state", "save system", "AI architecture", "behavior tree" | **game-systems** | game-systems.md |
| "review" + game context | **game-review** | game-systems.md + quality-attributes.md |
| "document decision" + game context | **game-design-doc** | game-systems.md + adr-template.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **game-systems** | Design core gameplay system architecture: entity models, state management, system interactions, data flow between systems |
| **game-review** | Evaluate existing game architecture against performance budgets, scalability, and maintainability; produce findings with severity |
| **game-design-doc** | Write an architecture decision record for a game system decision, including performance implications and platform considerations |

## Recommended Model

- `opus` for `game-systems`, `game-design-doc` (synthesis)
- `sonnet` for `game-review` (classification)

## Cross-Role Combinations

- **+ Solution Architect** — game with cloud backend: game-systems.md + architecture-patterns.md
- **+ Data Architect** — data-heavy game (analytics, leaderboards): game-systems.md + data-modeling.md
