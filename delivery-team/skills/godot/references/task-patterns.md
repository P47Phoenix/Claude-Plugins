# Common Task Patterns

Reference patterns for typical Godot 4.x feature work. The Godot skill loads this file on demand when the user request matches one of the patterns below; the sub-agent applies the pattern when scaffolding the implementation.

---

## New Game Entity (e.g., enemy, item, NPC)

References: `gdscript.md` (or `csharp-godot.md`) + `scenes-nodes.md` + `signals-architecture.md`

The sub-agent will:
1. Propose a scene hierarchy (root node type, child components)
2. Identify signals the entity should emit
3. Write the script(s) with typed variables, `@export` parameters, and `@onready` node refs
4. Wire signals in `_ready()`

---

## Player Controller

References: `gdscript.md` + `scenes-nodes.md` + `signals-architecture.md`

The sub-agent will apply the **component pattern**: separate HealthComponent, MovementComponent, InputComponent, AnimationComponent — each with its own script.

---

## UI System

References: `scenes-nodes.md` + `signals-architecture.md`

UI lives on a `CanvasLayer`. The sub-agent will connect UI nodes to EventBus signals rather than to gameplay nodes directly.

---

## State Machine

References: `signals-architecture.md` + `gdscript.md`

For simple behavior: enum-based state machine with `_enter_state` / `_exit_state` / `_process_state`.
For complex behavior: node-based state machine where each state is a child node with `enter()`, `exit()`, `update(delta)`.

---

## Autoload / Global System

References: `signals-architecture.md` + `scenes-nodes.md`

The sub-agent will keep autoloads infrastructure-only: `GameManager`, `AudioManager`, `SaveManager`, `EventBus`, `SceneLoader`. No gameplay logic in autoloads.
