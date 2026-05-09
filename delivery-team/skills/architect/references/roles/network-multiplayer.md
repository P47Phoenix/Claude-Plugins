# Network/Multiplayer Architect — Role Manifest

The Network/Multiplayer Architect designs netcode: client-server topology, rollback, state synchronization, lag compensation, matchmaking, and anti-cheat.

## Reference Files Loaded

- `references/network-multiplayer.md` — client-server, rollback, state sync, lag compensation, matchmaking, anti-cheat

Add `references/quality-attributes.md` for `game-review`. Add `references/adr-template.md` for `game-design-doc`.

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "netcode", "multiplayer", "rollback", "lag compensation", "matchmaking", "client-server", "P2P", "state sync", "lobby", "dedicated server" | **netcode** | network-multiplayer.md |
| "review" + multiplayer context | **game-review** | network-multiplayer.md + quality-attributes.md |
| "document decision" + multiplayer context | **game-design-doc** | network-multiplayer.md + adr-template.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **netcode** | Design network architecture: synchronization model, prediction/reconciliation strategy, bandwidth management, session flow |
| **game-review** | Evaluate existing game architecture against performance budgets, scalability, and maintainability; produce findings with severity |
| **game-design-doc** | Write an architecture decision record for a game system decision, including performance implications and platform considerations |

## Recommended Model

- `opus` for `netcode`, `game-design-doc` (synthesis)
- `sonnet` for `game-review` (classification)

## Cross-Role Combinations

- **+ Security Architect** — multiplayer with security / anti-cheat: network-multiplayer.md + security-patterns.md
