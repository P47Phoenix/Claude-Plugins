# Godot Scene and Node Architecture

Godot 4.x scene and node design patterns for maintainable, scalable game projects.

## Core Principle: Scenes as Building Blocks

Every scene should be **self-contained** — it must function correctly regardless of where in the scene tree it is placed. Scenes are the primary unit of composition in Godot; treat them like classes in OOP.

- A `Player.tscn` scene should not assume it has a parent named "World" or a sibling named "Camera"
- Reference external nodes through `@export` properties set in the Inspector, not hardcoded paths
- Each scene owns its own logic; parent scenes orchestrate child scenes through signals and exported properties

## Node Type Selection Guide

| Purpose | Node to Use |
|---------|-------------|
| 2D characters, enemies | `CharacterBody2D` |
| 2D static environment | `StaticBody2D` |
| 2D triggers, areas | `Area2D` |
| 3D characters, enemies | `CharacterBody3D` |
| 3D static environment | `StaticBody3D` |
| 3D triggers, areas | `Area3D` |
| UI root layer | `CanvasLayer` |
| UI containers | `VBoxContainer`, `HBoxContainer`, `GridContainer` |
| Game manager (global) | Autoload (Project → Autoload) |
| Render-to-texture | `SubViewport` |
| Spawner logic | `Node` with script (or `MultiMeshInstance2D/3D` for large counts) |

## Scene Hierarchy Conventions

```
World.tscn
├── TileMap          ← environment
├── Enemies          ← Node, parent for runtime-spawned enemies
├── Player.tscn      ← self-contained player scene
├── UI.tscn          ← self-contained UI scene (on CanvasLayer)
└── GameCamera       ← camera that follows player via exported reference
```

- Group spawned runtime nodes under a dedicated parent (`Enemies`, `Bullets`, `Pickups`)
- Keep the root of each scene a single node that represents the scene's purpose
- Use `CanvasLayer` for all UI — ensures UI ignores camera transforms

## Scene Inheritance

Use scene inheritance (right-click → "New Inherited Scene") for variants of the same base:

```
Enemy.tscn (base)
├── Goblin.tscn (inherits Enemy.tscn, overrides speed and sprite)
├── Orc.tscn (inherits Enemy.tscn, overrides health and attack)
└── Boss.tscn (inherits Enemy.tscn, adds additional nodes)
```

Prefer inheritance for variants that share the same node structure. Use composition (separate scenes embedded as children) for reusable behaviors that differ between unrelated types.

## Communication Between Nodes (Priority Order)

1. **Signals (preferred):** child notifies parent/world of events without knowing who listens
2. **Exported node references:** parent passes a reference to a sibling node via `@export`
3. **Autoload singletons:** global events that have no natural owner (game state, audio, save system)
4. **Direct `get_parent()` calls:** only when the relationship is architecturally guaranteed and stable
5. **Absolute node paths:** avoid — fragile, breaks on scene restructuring

## Groups

Use groups for one-to-many relationships without tight coupling:

```gdscript
# Add nodes to a group in _ready() or via the Inspector
add_to_group("enemies")

# Broadcast to all enemies from anywhere in the tree
get_tree().call_group("enemies", "stun", 2.0)

# Check membership
if node.is_in_group("enemies"):
    pass
```

Good uses: pause systems, global broadcasts, collectibles, checkpoints.
Bad use: as a replacement for signals in one-to-one relationships.

## Resource-Based Data

Use `Resource` subclasses for authored game data:

```gdscript
class_name WeaponData extends Resource

@export var name: String
@export var damage: int
@export var fire_rate: float
@export var projectile_scene: PackedScene
```

- Create `.tres` files in the editor; assign to `@export var weapon: WeaponData` on entities
- Resources are shared by reference — change a resource instance and all users see the change
- Use `resource.duplicate()` for per-instance copies when mutation is needed (e.g., per-player stats)

## Dynamic Scene Loading

```gdscript
# Preload (compile-time, small scenes)
const BulletScene: PackedScene = preload("res://scenes/bullet.tscn")

# Load (runtime, large scenes — use ResourceLoader for async)
var level_scene: PackedScene = load("res://levels/level_02.tscn")

# Async loading (large scenes, no freeze)
ResourceLoader.load_threaded_request("res://levels/level_02.tscn")
var level_scene = ResourceLoader.load_threaded_get("res://levels/level_02.tscn")
```

Use `preload` for small, always-needed scenes; use `ResourceLoader.load_threaded_request` for large scenes (levels, cutscenes) to avoid frame hitches.

## Anti-Patterns to Avoid

- **Hardcoded absolute paths:** `get_node("/root/World/Player")` breaks on scene restructure
- **God scenes:** one massive scene with hundreds of nodes — split into composable sub-scenes
- **Logic in scene tree structure:** don't use node position in tree as a data source
- **Directly accessing parent's internals:** use signals or exported references instead
- **Using a Node when a Resource would do:** game data (stats, items) belongs in Resources, not Nodes
