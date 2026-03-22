# Godot Validation and Runtime Verification

Patterns for validating Godot projects beyond static code inspection. Covers headless validation, common agent-missed bugs, and integration with MCP tools.

## Headless Validation Commands

### Full project validation
```
godot --headless --path <project_dir> --quit 2>&1
```
Loads the project, initializes all autoloads, instantiates the main scene, runs one frame, and quits. Reports all ERRORs and WARNINGs encountered during initialization.

**What it catches:**
- Missing autoload scripts
- Broken scene node paths (parent path vanished)
- @onready null reference errors
- Missing resources (textures, scenes, scripts)
- Signal connection failures
- GDScript runtime errors during _ready()

### Per-script parse validation
```
godot --headless --check-only --script <script_path> 2>&1
```
Parse-validates a single .gd file without loading the full project. Fast (~1s). Requires Godot 4.2+. For earlier 4.x versions, use full project validation instead.

**What it catches:**
- Syntax errors
- Type errors (when using typed GDScript)
- Missing class references

**What it does NOT catch:**
- Runtime errors (null refs, missing nodes)
- Scene composition issues
- Signal wiring problems

## Common Agent-Missed Bugs

These are bugs that pass code review but fail at runtime. Agents should check for these patterns explicitly.

### 1. @onready null references when called before tree entry

**Pattern:** Factory creates a node, calls a method that accesses @onready vars, then adds the node to the tree.

```gdscript
# BAD — @onready vars are null until _ready() runs
var unit = unit_scene.instantiate()
unit.initialize(data)  # This calls @onready vars internally
add_child(unit)  # @onready resolves HERE, too late

# GOOD — defer setup until after tree entry
var unit = unit_scene.instantiate()
add_child(unit)  # @onready resolves now
unit.initialize(data)  # Safe to access @onready vars
```

**Detection:** Search for `.instantiate()` followed by method calls before `add_child()`. If the called method accesses `$ChildNode` or @onready vars, it will fail.

### 2. Scene node path breakage when instancing

**Pattern:** A .tscn file uses `parent="RootName/ChildName/..."` paths. When instanced into another scene, these paths can break if the instanced root name changes.

```
# BAD — combat_panel.tscn uses full path from root name
[node name="VBox" type="VBoxContainer" parent="CombatPanelLayer/CombatPanel"]

# When instanced into game_map.tscn as a different name, paths break
```

**Detection:** In .tscn files, check that `parent=` paths are relative to the scene's own root, not including the root name itself. For child nodes, parent should be `"."` (direct child of root), `"ChildName"` (grandchild), etc.

### 3. TileSet/TileMapLayer programmatic setup

**Pattern:** Creating TileSet programmatically with `TileSetAtlasSource`. Common issues:
- Forgetting to call `create_tile()` for each atlas position
- Texture format incompatibility
- Atlas source not added to TileSet before assigning to TileMapLayer

**Detection:** When a script creates a TileSet programmatically, verify the chain: create Image → create ImageTexture → create TileSetAtlasSource → set texture → create_tile() for each position → add_source() to TileSet → assign to TileMapLayer.

### 4. Camera2D not set as current

**Pattern:** Camera2D exists in scene but `make_current()` or `enabled = true` is never called.

**Detection:** If a scene has a Camera2D node, check that either:
- The .tscn sets `current = true` on the Camera2D
- The script calls `make_current()` in `_ready()`
- The script sets `enabled = true`

### 5. project.godot comment corruption

**Pattern:** Godot's editor reformatter can merge GDScript-style comments (`# Comment\n`) with the next line when saving project.godot.

```
# Before Godot editor save:
# Camera controls
camera_up={...}

# After Godot editor save:
#Cameracontrolscamera_up={...}  # BROKEN — camera_up action no longer exists
```

**Detection:** After Godot opens and saves the project, re-read project.godot and check that all expected input actions exist as uncommented keys.

## Pre-Write Checklist

Before marking a Godot story as complete, verify:

- [ ] `godot --headless --path <project> --quit` produces zero ERROR lines
- [ ] All new .gd files pass `--check-only` validation
- [ ] No `@onready` vars accessed before the node enters the scene tree
- [ ] All .tscn `parent=` paths use relative paths (not including root node name)
- [ ] Camera2D nodes call `make_current()` or have `current = true`
- [ ] New autoloads are properly registered (uncommented) in project.godot
- [ ] EventBus signals are declared before being emitted or connected

## Acceptance Criteria Classification

### Structural (verifiable by code inspection)
- File exists at expected path
- Class has required properties/methods
- Function signature matches spec
- Constants have correct values
- Signal declared on EventBus

### Empirical (requires runtime validation)
- Scene renders correctly (tiles visible, sprites colored)
- Click interaction works (selection, movement, attack)
- Animation plays (tween, sprite change)
- UI panel shows/hides correctly
- Sound plays
- Camera follows/pans correctly
- Units appear at correct positions
- Health bar updates visually

When a story has empirical acceptance criteria and no validation tool was used, mark the story as **"code-complete, pending validation"** rather than **"done"**.

## MCP Integration (GodotIQ)

When GodotIQ MCP server is available (`pip install godotiq`), these additional static analysis tools can be used without Godot running:

- **Code validation**: convention checking, anti-pattern detection
- **Dependency graphs**: trace which scripts depend on which
- **Signal flow**: map signal connections across the project
- **Scene analysis**: parse .tscn files for node structure issues

Configure in `.mcp.json`:
```json
{
  "mcpServers": {
    "godotiq": {
      "command": "python3",
      "args": ["-m", "godotiq"],
      "env": { "GODOTIQ_PROJECT_ROOT": "<path_to_godot_project>" }
    }
  }
}
```
