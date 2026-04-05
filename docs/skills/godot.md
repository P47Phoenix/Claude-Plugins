# Godot

**Invocation**: `delivery-team:godot`

Godot 4.x game development agent for GDScript and C# development.

## How to Trigger

- Mentions of Godot, GDScript, `.tscn`, `.gd`
- `@export`, `@onready`, `CharacterBody2D/3D`, `Area2D/3D`
- Autoloads, PackedScene, scene tree operations
- Requests to build game features in Godot

## Task Categories

| Category | Signals | Reference |
|----------|---------|-----------|
| **GDScript** | `.gd` files, `@export`, `@onready`, `match`, `await` | gdscript.md |
| **C# / Godot** | `.cs` files, `[Export]`, `[Signal]`, `.NET` | csharp-godot.md |
| **Scene / Node** | `.tscn`, node hierarchy, scene inheritance | scenes-nodes.md |
| **Signals / Events** | Signal declaration, Event Bus, autoloads, state machines | signals-architecture.md |
| **Validation** | Verify, validate, headless checking | validation.md |
| **Quality Gate** | Done, complete, pre-commit checklist | defect-prevention.md + validation.md |

Multiple categories commonly overlap — a player character task touches GDScript + scene design + signals.

## Task Types

| Type | What It Does |
|------|-------------|
| **write** | Implement GDScript or C# code with scene structure |
| **fix** | Diagnose and patch issues |
| **refactor** | Improve structure following Godot patterns |
| **review** | Audit against Godot best practices |
| **explain** | Walk through code with annotations |
| **design** | Design scene hierarchy and signal architecture |
| **validate** | Run headless validation checks |

## Clean Code Integration

The Godot skill shares the same clean code foundation as the developer skill. The clean code guide loads on every task. Custom standards configured via `tech_stack.clean_code_guide` apply to Godot tasks as well.

## Pipeline Integration

When invoked outside the delivery pipeline, a warning is displayed (same as the developer skill). Within the pipeline, the Godot skill runs alongside the developer skill during the Development stage for GAME_DEV projects.

## Example Usage

```
User: "Create a player controller with jump and dash"

Language: GDScript | Task: write
References: gdscript.md, scenes-nodes.md, signals-architecture.md

Output: CharacterBody2D script with state machine,
        scene hierarchy description, signal connections,
        and test suggestions
```
