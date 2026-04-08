# Project Type Detection and Routing

> **Runtime detection is mandatory (v2.7+).** Project type is a **per-run**
> routing decision. Phase 1 detection runs on **every** pipeline invocation
> against the current user request. The config file does NOT pin the project
> type — the legacy `project_type` key was removed in schema v2.7. Pinning
> the type at setup time is explicitly disallowed because it freezes routing
> across requests whose actual type may differ (the "frozen routing footgun"
> that v2.7 fixes).
>
> **Opt-in override**: If a repo genuinely needs an intentional pin (e.g., a
> docs-only repo that should never trigger code stages), set
> `routing.force_type` in `.delivery/config.yml`. Phase 1 detection still runs
> and is logged, but routing uses the pin. A banner announces the override on
> every run. This is the ONLY supported way to pin the type, and it is
> deliberately namespaced under `routing.` so it is a discoverable, intentional
> act rather than a footgun hiding at the root.
>
> See ADR-002 for the full migration rationale.

## Detection Matrix

Classify every user request into one of the following project types before pipeline execution begins. Classification drives stage routing, agent selection, and gate depth.

---

### GREENFIELD

- **Signals**: "new project", "from scratch", "greenfield", "brand new", "start fresh", "build a new", "create a new", "bootstrap", "initialize"
- **Confidence boosters**: No existing codebase mentioned, no references to current system, user describes a problem without an existing solution
- **Confidence reducers**: Mentions existing system, "add to", "extend", "modify", references current architecture or tech stack already in use

### FEATURE

- **Signals**: "add feature", "enhance", "extend", "new capability", "improvement", "add support for", "integrate", "upgrade", "enable", "allow users to"
- **Confidence boosters**: References existing system, mentions current architecture, describes adding to something that already works, names existing services or modules
- **Confidence reducers**: "from scratch", no existing context, describes a complete system rather than an addition

### BUG_FIX

- **Signals**: "fix", "bug", "defect", "broken", "regression", "error", "crash", "not working", "failing", "incorrect behavior", "unexpected result", "should but doesn't", "used to work"
- **Confidence boosters**: Error messages, stack traces, "it used to work", reproduction steps provided, specific version references, "since the last update"
- **Confidence reducers**: "new feature", "enhancement", no description of incorrect behavior

### DESIGN

- **Signals**: "design session", "design-only", "architecture proposal", "no code yet", "exploring design", "design workshop", "produce design deliverable"
- **Confidence boosters**: User explicitly says "no code", references a "design package" or "design deliverable" as the output, wants ADRs / architecture / wireframes without implementation, frames the engagement as a workshop or proposal
- **Confidence reducers**: Mentions tests, deployment, release, commits, "ship it", or any implementation verbs
- **Disambiguation from SPIKE**: SPIKE is a throwaway, time-boxed investigation whose output is a learning or recommendation that may be discarded. DESIGN is a committed design intent — the design package itself IS the deliverable and is expected to be honored by future implementation work.
- **Disambiguation from GREENFIELD**: GREENFIELD runs all the way through Plan/Dev/UAT to produce working code. DESIGN intentionally stops after Architect — no Plan, no Dev, no UAT. If the user wants the design AND the implementation in the same engagement, that is GREENFIELD (or FEATURE), not DESIGN.

### GAME_DEV

- **Signals**: "game", "Godot", "Unity", "Unreal", "gameplay", "level", "HUD", "multiplayer", "NPC", "player controller", "sprite", "tilemap", "game loop", "physics body", "collision", "scene tree", "GDScript", "C# MonoBehaviour"
- **Note**: GAME_DEV is a MODIFIER, not a standalone type. It always combines with GREENFIELD, FEATURE, or BUG_FIX.
- **Combinations**:
  - GAME_DEV+GREENFIELD: new game project from scratch
  - GAME_DEV+FEATURE: adding a new mechanic, system, or content to an existing game
  - GAME_DEV+BUG_FIX: fixing a game bug (physics glitch, rendering issue, logic error)
- **Default base**: If GAME_DEV signals are present but no base type is clear, default to GREENFIELD.

### SPIKE

- **Signals**: "spike", "POC", "proof of concept", "prototype", "investigate", "evaluate", "feasibility", "explore whether", "can we", "research", "experiment", "try out", "what if"
- **Confidence boosters**: Time-boxed language ("spend a day on", "quick test"), "just test if", "see if it's possible", no mention of production deployment
- **Confidence reducers**: Production readiness language, "deploy", "release", full feature descriptions

### DOCS_ONLY

- **Signals**: "documentation", "docs only", "write docs", "API docs", "user guide", "runbook", "README", "document the", "write a guide", "onboarding doc", "architecture decision record"
- **Confidence boosters**: No code changes mentioned, documentation-specific deliverable, "update the wiki", "write a how-to"
- **Confidence reducers**: Code changes described alongside docs, "implement and document"

---

## Disambiguation Rules

1. **GAME_DEV is always a modifier** -- never assign it as a standalone type. If no base type signal is present, default base is GREENFIELD.
2. **Conflicting signals require clarification.** When signals for both FEATURE and GREENFIELD are present at similar strength, ask the user: "Are you building something entirely new, or adding to an existing system?"
3. **Existing codebase context defaults to FEATURE.** If the user references an existing codebase but the type is otherwise unclear, default to FEATURE.
4. **BUG_FIX takes precedence** when error/defect language is the dominant signal. A request like "add error handling for the crash on login" is BUG_FIX, not FEATURE.
5. **SPIKE vs FEATURE ambiguity**: If the user describes a concrete deliverable with production intent, it is FEATURE even if they use the word "explore." SPIKE implies throwaway or time-boxed output.
6. **DOCS_ONLY is strict**: If any code changes are described, it is not DOCS_ONLY. Reclassify as the appropriate type and note that documentation is a deliverable.

---

## Stage Routing Matrix

Each cell defines the execution depth for that stage given the project type.

| Stage | GREENFIELD | FEATURE | BUG_FIX | DESIGN | GAME_DEV+ | SPIKE | DOCS_ONLY |
|-------|-----------|---------|---------|--------|-----------|-------|-----------|
| 1. Idea | full | full | full | full | full | full | full |
| 2. Refine | full | full | skip | full | full | skip | skip |
| 3. Design | full | full | skip | full | full+game | skip | skip |
| 4. Architect | full | light-or-skip | skip | full | full+game | full | skip |
| 5. Plan | full | full | light | skip | full | skip | light |
| 6. Dev | full | full | full | skip | full+game | full | full |
| 7. UAT | full | full | full | skip | full | skip | full |

---

## Stage Depth Definitions

### Full

- All agents invoked (primary + supporting roles)
- All collaboration patterns run (evaluator-optimizer, adversarial review, debate, consensus as applicable)
- Full quality gate evaluation with all criteria at all severity levels (blocking, warning, suggestion)
- Full team DoD validation with all designated validators for the stage
- Self-correction enabled with maximum 3 iterations before escalation

### Light

- Primary agent only -- no supporting agents spawned
- No adversarial review or debate patterns executed
- Simplified quality gate: evaluate blocking criteria only, skip warnings and suggestions
- Reduced DoD validators: primary role + 1 reviewer only
- Self-correction enabled with maximum 2 iterations before escalation

### Skip

- Stage does not execute at all
- Pipeline advances directly to the next non-skipped stage
- Downstream stages receive whatever upstream artifacts are available (may be fewer than in full runs)
- No gate evaluation, no DoD validation, no artifacts produced for this stage

### Full+Game

Everything in Full, plus game-specific augmentations:

- **Design stage**: Game UI Designer added as a participating agent. Evaluates HUD, menus, in-game UI, controller mapping, and game-specific UX patterns.
- **Architect stage**: Game architecture roles added as relevant to the project scope:
  - Game Systems Architect (ECS, state machines, game loop)
  - Level/World Designer (scene structure, streaming, persistence)
  - Network/Multiplayer Architect (netcode, sync, lobbies) -- only if multiplayer
  - Graphics/Rendering Specialist (shaders, particles, performance) -- only if graphically intensive
- **Dev stage**: Godot skill (or relevant engine skill) invoked alongside the Developer skill. Engine-specific patterns and best practices enforced.
- **UAT stage**: Game-specific test patterns applied:
  - Playtest scenarios (game feel, difficulty, progression)
  - Performance budgets (frame time targets, memory limits, draw call budgets)
  - Input scheme validation (keyboard, controller, touch as applicable)
  - Platform-specific checks (if targeting multiple platforms)

---

## Light-or-Skip Decision Logic (FEATURE at Architect Stage)

Apply **Light** if the feature involves ANY of the following:

- New API endpoints or service interfaces
- New data models or schema changes
- New external integrations or third-party services
- Security-sensitive changes (auth, permissions, data access)
- Changes touching more than 3 services or modules

Apply **Skip** if ALL of the following are true:

- UI-only change (no backend modifications)
- Contained within a single service or module
- No new data models or schema changes
- No security implications
- No new external dependencies
