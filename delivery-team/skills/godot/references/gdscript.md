# GDScript Best Practices

Version baseline: GDScript 2.0 (Godot 4.x)

## Style & Formatting

- Follow the official GDScript style guide enforced by Godot's built-in formatter
- Use `snake_case` for variables, functions, signals, and file names; `PascalCase` for classes and node names; `ALL_CAPS` for constants and enums
- Annotate all exported variables and function parameters with type hints: `@export var speed: float = 200.0`
- Use static typing throughout — enable "Unsafe Line" warnings in project settings
- One class per file; file name matches the class name in `snake_case`
- Order script sections: `class_name` → `extends` → docstring → signals → enums → constants → `@export` vars → public vars → private vars (`_prefix`) → `@onready` vars → built-in overrides (`_ready`, `_process`) → public methods → private methods

## Idioms & Patterns

- Use `class_name` to register custom types globally — avoids `preload()` chains
- Use `@onready` for node references rather than assigning in `_ready()`:
  ```gdscript
  @onready var health_bar: ProgressBar = $UI/HealthBar
  ```
- Use `@export` for values designers should tune in the Inspector; use typed exports: `@export var damage: int`
- Prefer signals over direct function calls for loose coupling between nodes:
  ```gdscript
  signal health_changed(new_health: int, max_health: int)
  ```
- Use `await` for one-shot signal waiting and coroutines:
  ```gdscript
  await get_tree().create_timer(1.0).timeout
  ```
- Use `Resource` subclasses for data that should be authored in the editor (stats, item definitions)
- Use `Callable` and `Signal` types for typed signal connections
- Prefer `match` over long `if/elif` chains for state and type dispatch
- Use `StringName` (`&"name"`) for frequently compared strings (signal names, group names, input actions)

## Error Handling

- Use `assert(condition, "message")` to validate assumptions in development — stripped in release builds
- Check node existence before use: `if is_instance_valid(node):`
- Use `push_error("message")` for non-fatal errors that should be visible in the debugger
- Use `push_warning("message")` for non-fatal configuration issues
- Avoid crashing the game on missing nodes — fail gracefully with a logged error
- Use `Engine.is_editor_hint()` to guard editor-only code in tool scripts

## Testing (GDScript)

- Use `GUT` (Godot Unit Test) addon for unit and integration testing
- Test game logic (state machines, damage calculations, spawn rules) independently from scenes where possible
- Keep game logic in plain GDScript classes (not Nodes) when it does not need scene tree access — easier to unit test
- Use Godot's built-in debugger, profiler, and visual debugger for runtime analysis
- Use `@tool` annotation to run script logic in the editor for validation

## Performance

- Cache node references in `@onready` — avoid repeated `$Path/To/Node` lookups in `_process()`
- Use `_physics_process()` for physics-dependent logic; `_process()` for visuals and input — do not mix
- Prefer `process_mode = PROCESS_MODE_DISABLED` over `set_process(false)` for entire subtrees
- Use object pooling for frequently spawned/despawned objects (bullets, particles, enemies)
- Profile with Godot's built-in profiler before optimizing; target 60fps stable over micro-optimization
- Avoid `get_node()` in loops — resolve once and cache
- Use `PackedScene.instantiate()` for spawning; preload scenes at startup
- Avoid large dictionaries with string keys in hot paths — use typed arrays or Resources

## Signals and Architecture

- Emit signals instead of calling parent methods directly — allows any node to react without coupling
- Connect signals in `_ready()` using typed connection syntax:
  ```gdscript
  enemy.died.connect(_on_enemy_died)
  ```
- Use `call_deferred()` when modifying the scene tree from within a physics/process callback
- Prefer the **Event Bus** pattern (autoload singleton) for global events across unrelated nodes
- Use **Autoloads** for true global state (game manager, audio manager, save system); keep them minimal

## Scene and Node Organization

- Keep scenes self-contained — a scene should work independently of where it is placed
- Use scene inheritance for variants of the same base (enemy types, weapon variants)
- Use `SubViewport` for render-to-texture, splitscreen, and UI with 3D elements
- Group related nodes under a descriptive parent node; name nodes by role not type (`HealthDisplay` not `Label`)
- Use `CanvasLayer` for UI to separate it from game camera transforms

## Anti-Patterns to Avoid

- **Tight coupling via `get_parent()` or absolute paths:** use signals or exported node references
- **Business logic in `_process()` every frame:** use state machines, timers, or signals
- **Strings for node paths everywhere:** use `@onready` typed references
- **Not typing variables:** loses autocomplete, refactoring support, and runtime safety
- **Overloading autoloads with game logic:** autoloads are for infrastructure, not gameplay
- **Direct scene tree manipulation from deep child nodes:** bubble up via signals

## Tooling

| Tool | Purpose |
|------|---------|
| Godot editor formatter | `GDScript → Format File` |
| GUT addon | Unit and integration testing |
| Godot debugger + profiler | Performance and runtime analysis |
| `push_error` / `push_warning` | Structured error reporting |
| `@tool` scripts | Editor-time validation and tools |
