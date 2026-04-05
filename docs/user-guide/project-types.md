# Project Types

The delivery pipeline auto-detects your project type from your description and routes it through the appropriate stages at the right depth.

## The 6 Project Types

### GREENFIELD

A new project built from scratch with no existing codebase.

**Detection signals**: "new project", "from scratch", "brand new", "start fresh", "bootstrap"

**Stage routing**: All 7 stages at full depth with all 4 human checkpoints.

---

### FEATURE

Adding functionality to an existing system.

**Detection signals**: "add feature", "enhance", "extend", "new capability", "integrate"

**Stage routing**: All 7 stages. Architect stage runs at light depth (or skip for UI-only changes in a single module).

---

### BUG_FIX

Fixing a defect in an existing system.

**Detection signals**: "fix", "bug", "broken", "error", "crash", "regression", "not working"

**Stage routing**: Stages 2 (Refine), 3 (Design), and 4 (Architect) are skipped. Plan runs light. Idea, Dev, and UAT run at full depth.

---

### GAME_DEV

Game development projects. This is a **modifier** that combines with a base type (GREENFIELD, FEATURE, or BUG_FIX).

**Detection signals**: "game", "Godot", "Unity", "gameplay", "NPC", "HUD", "GDScript"

**Stage routing**: Same as the base type, with game-specific augmentations:

- **Design**: Game UI Designer added
- **Architect**: Game architecture roles added (Systems, Level/World, Network, Graphics)
- **Dev**: Godot skill invoked alongside Developer
- **UAT**: Playtest scenarios, performance budgets, input validation

If GAME_DEV signals are present but no base type is clear, the default base is GREENFIELD.

---

### SPIKE

Time-boxed investigation or proof of concept. Output is throwaway.

**Detection signals**: "spike", "POC", "prototype", "investigate", "feasibility", "explore"

**Stage routing**: Only Idea, Architect, and Dev stages run. No UAT. No plan.

---

### DOCS_ONLY

Documentation-only changes with no code modifications.

**Detection signals**: "documentation", "docs only", "write docs", "user guide", "runbook"

**Stage routing**: Refine, Design, and Architect are skipped. Plan runs light. Idea, Dev, and UAT run.

!!! warning "Strict classification"
    If any code changes are described alongside documentation, DOCS_ONLY is reclassified as the appropriate type with documentation as a deliverable.

---

## Detection Rules

1. **GAME_DEV is always a modifier** — never standalone. Default base is GREENFIELD.
2. **BUG_FIX takes precedence** when error/defect language is dominant.
3. **Existing codebase context defaults to FEATURE** when otherwise ambiguous.
4. **SPIKE vs FEATURE**: Concrete deliverable with production intent is FEATURE, even if "explore" is used.
5. **Conflicting signals require clarification** — the pipeline asks before assuming.

## Light-or-Skip Decision (FEATURE at Architect)

For FEATURE projects, the Architect stage uses this decision logic:

**Apply Light** if the feature involves any of:

- New API endpoints or service interfaces
- New data models or schema changes
- External integrations or third-party services
- Security-sensitive changes
- Changes touching more than 3 modules

**Apply Skip** if all of these are true:

- UI-only change (no backend modifications)
- Contained within a single module
- No new data models or schema changes
- No security implications
- No new external dependencies
