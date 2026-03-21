# Godot Signals and Event Architecture

Signal patterns, event bus design, and state machine architecture for Godot 4.x.

## Signal Fundamentals

Signals are Godot's observer pattern. They decouple emitters from receivers — the emitting node does not need to know who (if anyone) is listening.

### Declaration (GDScript)

```gdscript
signal health_changed(new_health: int, max_health: int)
signal died
signal item_collected(item: ItemData)
```

### Declaration (C#)

```csharp
[Signal] public delegate void HealthChangedEventHandler(int newHealth, int maxHealth);
[Signal] public delegate void DiedEventHandler();
[Signal] public delegate void ItemCollectedEventHandler(ItemData item);
```

### Connection Best Practices

Connect in `_ready()`, not in the Inspector for dynamic nodes:

```gdscript
func _ready() -> void:
    health_component.health_changed.connect(_on_health_changed)
    health_component.died.connect(_on_died)
```

Use `disconnect()` or one-shot connections when signals should fire once:

```gdscript
# One-shot: automatically disconnects after first emission
some_signal.connect(_handler, CONNECT_ONE_SHOT)

# Or use await for inline one-shot handling
await animation_player.animation_finished
```

### Signal Naming Conventions

- Past tense for events that have happened: `died`, `health_changed`, `item_collected`
- Present tense for requests/commands (rare): `request_spawn`
- Include relevant payload in name: `health_changed(new_health, max_health)` not just `health_changed()`

---

## Event Bus (Global Signals Autoload)

For events between unrelated nodes (UI reacting to gameplay, audio reacting to damage), use an autoloaded Event Bus rather than wiring signals through intermediate nodes.

**`autoloads/EventBus.gd`:**

```gdscript
extends Node

signal enemy_died(enemy: Enemy, position: Vector2)
signal player_health_changed(new_health: int, max_health: int)
signal level_completed(level_id: int, time: float)
signal game_paused(is_paused: bool)
```

**Emitting (from anywhere):**

```gdscript
EventBus.enemy_died.emit(self, global_position)
```

**Listening (from anywhere):**

```gdscript
func _ready() -> void:
    EventBus.player_health_changed.connect(_on_player_health_changed)
```

**Rules for Event Bus:**
- Only use for truly global events — do not put per-entity signals here
- Keep it as a signal-only file; no state, no logic
- Document each signal with a comment explaining when it fires and who typically emits/listens

---

## State Machine Pattern

Use state machines for character behavior, game flow, and UI screens.

### Simple State Machine (GDScript)

```gdscript
enum State { IDLE, WALKING, JUMPING, ATTACKING, DEAD }

var current_state: State = State.IDLE

func _physics_process(delta: float) -> void:
    match current_state:
        State.IDLE:
            _process_idle(delta)
        State.WALKING:
            _process_walking(delta)
        State.JUMPING:
            _process_jumping(delta)
        State.ATTACKING:
            _process_attacking(delta)
        State.DEAD:
            pass  # no processing when dead

func _change_state(new_state: State) -> void:
    _exit_state(current_state)
    current_state = new_state
    _enter_state(new_state)

func _enter_state(state: State) -> void:
    match state:
        State.ATTACKING:
            animation_player.play("attack")
            attack_hitbox.monitoring = true

func _exit_state(state: State) -> void:
    match state:
        State.ATTACKING:
            attack_hitbox.monitoring = false
```

### Node-Based State Machine (for complex states)

For complex behavior with many states, use a node-based state machine where each state is a separate scene/node:

```
StateMachine (Node)
├── IdleState (Node)
├── WalkState (Node)
├── AttackState (Node)
└── DeadState (Node)
```

Each state node implements `enter()`, `exit()`, `update(delta)`, and `physics_update(delta)`. The `StateMachine` node calls these on the active state.

---

## Component Pattern

Break complex node behavior into composable components:

```
Player (CharacterBody2D)
├── HealthComponent (Node)    ← manages HP, emits health_changed, died
├── MovementComponent (Node)  ← handles movement, velocity, acceleration
├── AttackComponent (Node)    ← manages attack cooldown, hitboxes
├── AnimationComponent (Node) ← drives AnimationPlayer from state signals
└── InputComponent (Node)     ← translates input → movement/action intents
```

**HealthComponent** owns health logic; Player does not manage HP directly. Other nodes (UI, audio) connect to HealthComponent's signals — not to Player directly.

Benefits: components are reusable across entity types (enemies, destructibles), testable in isolation, and replaceable (swap out a component without touching the entity).

---

## Deferred Calls and Thread Safety

When modifying the scene tree (adding/removing nodes) inside `_physics_process`, `_process`, or signal handlers, use deferred calls:

```gdscript
# Safe: deferred until end of current frame
queue_free()                              # safe to call from callbacks
call_deferred("add_child", new_node)     # explicit defer for add_child
node.set_deferred("visible", false)      # defer property changes

# Unsafe inside physics/signal callbacks:
# get_parent().remove_child(self)  ← may cause physics engine errors
```

**Rule:** Any operation that changes scene tree structure should be deferred when called from within frame processing or physics callbacks.

---

## Autoload Architecture

Keep autoloads focused on infrastructure:

| Autoload | Responsibility |
|----------|---------------|
| `GameManager` | Scene transitions, game state (menu/playing/paused/game_over) |
| `AudioManager` | Sound effect pooling, music playback, bus management |
| `SaveManager` | Save/load game data, settings persistence |
| `EventBus` | Global signal routing |
| `SceneLoader` | Async scene loading with loading screen |

**Do not put** gameplay logic, enemy behavior, or level-specific code in autoloads.
