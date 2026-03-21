# C# in Godot Best Practices

Version baseline: Godot 4.x with .NET 8 / C# 12

## Style & Formatting

- Follow Microsoft C# conventions adapted for Godot naming: `PascalCase` for public members, `_camelCase` for private fields
- Godot node properties and methods are `PascalCase` (matching C++ source): `GetNode<T>()`, `AddChild()`, `ProcessMode`
- Use `snake_case` for signal names to match GDScript convention (Godot signals are defined in C++ as snake_case): `health_changed`
- Enable nullable reference types: `<Nullable>enable</Nullable>` in `.csproj`
- Use `partial class` for all Node-derived classes — required for Godot source generators

## Godot-Specific C# Idioms

- Always mark Node subclasses as `partial` — the Godot source generator requires it:
  ```csharp
  public partial class Player : CharacterBody2D { }
  ```
- Use `[Export]` attribute for Inspector-editable properties:
  ```csharp
  [Export] public float Speed { get; set; } = 200.0f;
  ```
- Use `GetNode<T>("NodePath")` or `[Export]` node references; avoid string `GetNode("path")` without type parameter
- Use `[Signal]` attribute to declare typed signals:
  ```csharp
  [Signal] public delegate void HealthChangedEventHandler(int newHealth, int maxHealth);
  ```
- Emit signals with `EmitSignal(SignalName.HealthChanged, newHealth, maxHealth)`
- Connect signals: `someNode.HealthChanged += OnHealthChanged;`
- Use `GD.Print()` for debug output; `GD.PushError()` and `GD.PushWarning()` for structured errors
- Use `GodotObject.IsInstanceValid(node)` to check node validity before use
- Call `QueueFree()` to safely remove nodes — never `Free()` during the current frame's processing

## Node Lifecycle

- Override `_Ready()` (not constructors) for initialization — constructors run before the node is in the scene tree
- Use `GetNode<T>()` in `_Ready()` — nodes are not available before `_Ready()`
- Use `CallDeferred(nameof(SomeMethod))` or `Callable.From(SomeMethod).CallDeferred()` to defer scene tree modifications
- Override `_Process(double delta)` and `_PhysicsProcess(double delta)` — note `double` not `float` in Godot 4 C#
- Use `SetProcess(false)` / `SetPhysicsProcess(false)` to disable per-frame callbacks when not needed

## Error Handling and Null Safety

- Enable nullable reference types and treat all `GetNode<T>()` results as potentially null until validated
- Use `GetNodeOrNull<T>("path")` when a node may not exist — returns null instead of throwing
- Validate assumptions with `Debug.Assert()` — stripped in release builds
- Catch `Exception` at system boundaries (file I/O, networking) — do not catch inside gameplay logic
- Use `GD.PushError()` for non-fatal errors that should appear in the debugger without crashing

## Performance

- Cache `GetNode<T>()` results in fields initialized in `_Ready()` — do not call in `_Process()`
- Use `[Export]` for node references that vary per instance; cache them in `_Ready()`
- Prefer `_PhysicsProcess` for physics; `_Process` for rendering/input — do not mix concerns
- Use C# arrays and `List<T>` over Godot's `Array` and `Dictionary` types for pure C# logic (faster, type-safe)
- Use Godot's `Array<T>` and `Dictionary<K,V>` when interoperating with GDScript or Godot APIs
- Pool frequently spawned objects; use `PackedScene.Instantiate<T>()` for type-safe instantiation

## Interoperability with GDScript

- C# and GDScript can call each other through the Godot API — signals, exported properties, and `Call()` work across languages
- Use `[Export]` properties and signals for the GDScript/C# boundary — these are the stable interop surface
- Avoid passing C# generic types across the boundary — use Godot-compatible types (`Variant`, `Array`, `Dictionary`)
- When calling GDScript methods from C#: `node.Call("method_name", args)` — prefer typed C# code on the C# side

## Testing

- Use `GUT` addon for both GDScript and C# (via GdUnit4 for C# projects)
- Separate pure C# business logic from Node subclasses — test logic without scene tree
- Use MSTest or NUnit for pure C# library code; use Godot-aware test frameworks for Node tests
- Run tests headlessly: `godot --headless --run-tests`

## Anti-Patterns to Avoid

- **Non-partial Node classes:** will not compile with Godot source generators
- **`Free()` during processing:** use `QueueFree()` instead — `Free()` during frame processing causes crashes
- **String-typed `GetNode("path")`:** use typed `GetNode<T>("path")` for compile-time safety
- **Constructor-based initialization:** use `_Ready()` — scene tree is not available in constructors
- **Ignoring nullable warnings:** null node references cause `NullReferenceException` at runtime
- **`float` for `_Process` delta:** Godot 4 passes `double` — using `float` silently truncates precision

## Tooling

| Tool | Purpose |
|------|---------|
| `dotnet build` | Compile and catch type errors |
| `dotnet format` | Code formatting |
| GdUnit4 / GUT | Godot C# testing |
| Godot debugger | Runtime analysis |
| Rider / VS with Godot plugin | IDE integration with scene inspection |
