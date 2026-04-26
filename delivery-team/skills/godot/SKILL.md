---
name: godot
description: Godot 4.x game development agent. Use this skill when working on Godot projects — writing GDScript or C#, designing scenes and node hierarchies, implementing signals and event bus patterns, state machines, component architecture, or project structure. Triggers on mentions of Godot, GDScript, .tscn, .gd, @export, @onready, CharacterBody2D/3D, Area2D/3D, autoloads, PackedScene, or requests to build game features in Godot. Targets Godot 4.x / GDScript 2.0.
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7-frontmatter-only
last_audited: 2026-04-22
pattern_library_version: 4-7-1
---

# Godot 4.x Development Agent

## Design Principle: Reference-Scoped Sub-Agents

Godot development spans multiple overlapping concerns (scripting, scene architecture, signals, C# interop). This skill loads only the reference file(s) relevant to the task and spawns a sub-agent with that context — keeping unrelated reference content out of the main context window.

---

## Pipeline Context Check

Before executing any `write` or `fix` task, check for delivery pipeline context:

1. Check if `.delivery/config.yml` exists in the current working directory.
2. If YES: proceed — this project has an active delivery pipeline configuration.
3. If NO: announce a warning before proceeding:

> WARNING: No delivery pipeline config found. This implementation is not going through the delivery-flow pipeline. QA evaluator-optimizer loop, DoD validation, defect prevention checklist, and headless validation will NOT run automatically. Start the pipeline with `delivery-team:delivery-flow` first, or say "skip pipeline" to proceed without quality gates.

This check does NOT block implementation — it warns. Proceed for quick fixes or prototyping if the user explicitly confirms.

---

## Phase 1: Task Classification

Classify the request into one or more categories before proceeding:

| Category | Signals | Reference |
|---|---|---|
| **GDScript** | `.gd` files, GDScript syntax, `@export`, `@onready`, `match`, `await` | `references/gdscript.md` |
| **C# / Godot** | `.cs` files, `[Export]`, `[Signal]`, `partial class`, `.NET`, Rider | `references/csharp-godot.md` |
| **Scene / Node design** | `.tscn`, node hierarchy, scene inheritance, `CharacterBody2D`, `Area2D`, `StaticBody` | `references/scenes-nodes.md` |
| **Signals / Events / State** | Signal declaration, Event Bus, autoloads, state machines, component pattern | `references/signals-architecture.md` |
| **Validation** | verify, validate, check, test, headless, errors | `references/validation.md` |
| **Quality Gate** | done, complete, finish, checklist, pre-commit | `references/defect-prevention.md` + `references/validation.md` |

**Multiple categories are common** — a task about a player character likely touches GDScript + scene design + signals. Include all relevant reference files in the sub-agent prompt.

**Declare before every task:**

> `Language: [GDScript | C#] | Task: [write / fix / refactor / review / explain / design / validate] | References: [list of reference files used] | Clean Code: [default | <custom-path>]`

---

## Phase 2: Sub-Agent Invocation

**For every implementation task, follow these steps exactly:**

1. Classify the task (Phase 1)
2. Read **only** the relevant reference file(s) listed above — do not read all four unless the task genuinely spans all areas
3. Read the clean code guide:
   - If `.delivery/config.yml` exists and `tech_stack.clean_code_guide` is set to a non-empty value, read that file instead of the default
   - Otherwise, read `delivery-team/skills/developer/references/clean-code.md` (shared with the developer skill — do NOT copy this file into the Godot skill directory)
4. Spawn a sub-agent using the `Agent` tool with the prompt template below
5. Return the sub-agent's output directly to the user

The sub-agent has access to: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep` — it can work directly in the Godot project files.

### Sub-Agent Prompt Template

```
You are an expert Godot 4.x game developer. Apply these best practices to everything you produce:

---
[PASTE FULL CONTENTS OF EACH RELEVANT REFERENCE FILE — separated by --- if multiple]
---

## Clean Code Standards

[PASTE FULL CONTENTS OF clean code guide HERE — either delivery-team/skills/developer/references/clean-code.md (default) or custom guide from tech_stack.clean_code_guide config]

---

## Task

[TASK TYPE]: [DESCRIBE WHAT THE USER WANTS]

## Language

[GDScript | C#]

## Context

[Include any of the following that are relevant:]
- Existing .gd or .cs scripts to modify
- Scene file paths (.tscn)
- Project structure or autoload configuration
- Godot engine version (4.x, specify if known)
- Constraints (performance targets, existing API, multiplayer requirements)

## Output Requirements

Produce:
1. Complete, working GDScript or C# code — no placeholder stubs unless requested
2. Scene structure description if new nodes are needed (what nodes, what hierarchy)
3. Signal connection instructions if signals are involved
4. Inline comments on non-obvious logic only
5. A brief explanation of key architecture decisions (3–5 sentences)
6. How to test / verify the behavior in the Godot editor

### Verification Status

- **Verified by tests**: [GdUnit tests written and described]
- **Verified by inspection**: [code structure, signal wiring, node hierarchy, file paths]
- **Requires runtime validation**: [scene rendering, input handling, physics, animation, TileMap display, camera behavior, audio playback]
- **Verification gaps**: [any criteria not verifiable without running the Godot editor]

Scene rendering, input handling, TileMap display, physics interactions, animation playback, camera behavior, and audio playback ALWAYS require runtime validation. Never mark these as verified by inspection.

Follow the official GDScript style guide and all conventions in the reference material.
```

### Task Type Instructions for Sub-Agent

| Task Type | What the sub-agent does |
|---|---|
| **write** | Implement from scratch following all conventions in the references |
| **fix** | Identify root cause, patch it, explain what was wrong |
| **refactor** | Improve structure/idioms without changing behavior; cite which patterns were applied |
| **review** | Audit against the reference material; produce findings with severity (critical / warning / suggestion) |
| **explain** | Annotate and walk through the code; reference Godot patterns where applicable |
| **design** | Propose scene hierarchy, node types, signal flow, and component breakdown before writing code |
| **validate** | Run headless validation, parse output, report errors with file:line references and fix suggestions |
| **quality-gate** | Run defect-prevention checklist against modified files; report pass/fail per item with file:line evidence for failures |

---

## Reference Files

| File | Content |
|---|---|
| `references/gdscript.md` | GDScript 2.0 style, idioms, typing, signals, performance, anti-patterns |
| `references/csharp-godot.md` | C# 12 / .NET 8 in Godot 4.x: partial classes, [Export], [Signal], QueueFree, nullable safety |
| `references/scenes-nodes.md` | Scene self-containment, node type selection, hierarchy conventions, scene inheritance, Resource-based data |
| `references/signals-architecture.md` | Signal patterns, Event Bus autoload, state machines (enum and node-based), component pattern, deferred calls |
| `references/validation.md` | Headless validation, common agent-missed bugs, AC classification (structural vs empirical), pre-write checklist |
| `references/defect-prevention.md` | Pre-completion checklist, defect patterns, detection commands, defect metrics |

---

## Common Task Patterns

### New Game Entity (e.g., enemy, item, NPC)

References: `gdscript.md` (or `csharp-godot.md`) + `scenes-nodes.md` + `signals-architecture.md`

The sub-agent will:
1. Propose a scene hierarchy (root node type, child components)
2. Identify signals the entity should emit
3. Write the script(s) with typed variables, `@export` parameters, and `@onready` node refs
4. Wire signals in `_ready()`

### Player Controller

References: `gdscript.md` + `scenes-nodes.md` + `signals-architecture.md`

The sub-agent will apply the **component pattern**: separate HealthComponent, MovementComponent, InputComponent, AnimationComponent — each with its own script.

### UI System

References: `scenes-nodes.md` + `signals-architecture.md`

UI lives on a `CanvasLayer`. The sub-agent will connect UI nodes to EventBus signals rather than to gameplay nodes directly.

### State Machine

References: `signals-architecture.md` + `gdscript.md`

For simple behavior: enum-based state machine with `_enter_state` / `_exit_state` / `_process_state`.
For complex behavior: node-based state machine where each state is a child node with `enter()`, `exit()`, `update(delta)`.

### Autoload / Global System

References: `signals-architecture.md` + `scenes-nodes.md`

The sub-agent will keep autoloads infrastructure-only: `GameManager`, `AudioManager`, `SaveManager`, `EventBus`, `SceneLoader`. No gameplay logic in autoloads.

---

## Architecture Guardrails

The sub-agent must enforce these in every output:

- **No hardcoded absolute paths** — use `@export` node references or `@onready`
- **No `get_parent()` for data** — use signals or exported references
- **No business logic in autoloads** — autoloads are infrastructure only
- **`queue_free()` not `free()`** — never call `free()` during frame processing
- **Deferred tree modifications** — use `call_deferred()` / `set_deferred()` inside `_physics_process` and signal handlers
- **Self-contained scenes** — scenes must work regardless of where they are placed in the tree
- **Type everything** — all variables, parameters, and return types must be typed in GDScript
- **No @onready access before tree entry** — never call methods that use @onready variables on a node that hasn't been added to the scene tree yet. Use `call_deferred()` or add the node first, then configure.
- **Never use `:=` type inference** — always use explicit types (`var x: int = 5`). The `:=` operator causes silent failures in the editor that headless validation doesn't catch.
- **Run GdUnit4 tests when available** — if `addons/gdUnit4/` exists in the project and test files exist in `res://tests/`, run `godot --headless -s addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests` after implementation.
- **Array sizes must match enum sizes** — every array indexed by an enum must have the same number of elements. Validate at runtime or in tests.
- **Validate after implementation** — if `godot` is available on PATH, run `godot --headless --path <project> --quit` after every `write` or `fix` task on `.gd` or `.tscn` files and report any new errors. If `godot` is not available, note that headless validation was skipped and recommend manual validation
- **Run defect prevention checklist** — before marking any story as complete, run through `references/defect-prevention.md` checklist items relevant to the story's changes

---

## User Commands

| Command | Action |
|---|---|
| `gdscript` | Use GDScript for this task |
| `csharp` | Use C# for this task |
| `design` | Produce scene/architecture design before writing code |
| `review` | Switch task type to code review |
| `explain` | Annotate and explain existing code |
| `refactor` | Improve structure without changing behavior |
| `accept` | Finalize — write any pending files to disk |

---

## Cross-Skill References

| File | Owner Skill | Purpose |
|------|-------------|---------|
| `delivery-team/skills/developer/references/clean-code.md` | developer | Foundational clean code standards. Loaded on every godot task unless overridden by `tech_stack.clean_code_guide` in `.delivery/config.yml`. |

> Path stability: these paths are contracts. Renaming the owner skill's directory is a breaking change.

---

## Godot Version Note

All output targets **Godot 4.x** with **GDScript 2.0** or **.NET 8 / C# 12**. Godot 3.x syntax (`onready`, `export`, `yield`, `OS.get_ticks_msec()`) is not used. If the user specifies a Godot 3.x project, ask to confirm before proceeding — the reference material does not cover Godot 3.x patterns.
