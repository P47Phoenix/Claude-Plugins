# Hooks Reference

The delivery-team plugin installs 7 hooks across 5 event types. Hooks run automatically to enforce pipeline discipline, validate artifacts, and maintain quality.

## Hook Summary

| # | Hook | Event Type | Purpose |
|---|------|-----------|---------|
| 1 | Config Check | SessionStart | Validate `.delivery/config.yml` exists and is current |
| 2 | Retrospective Enforcement | Stop | Block session end if pipeline work occurred without retrospective |
| 3 | Pipeline Bypass Detection | PreToolUse (Skill) | Warn when developer/godot/quality invoked outside delivery-flow |
| 4 | Agent Prompt Audit | PreToolUse (Agent) | Audit agent prompts for context isolation compliance |
| 5 | GDScript Validation | PostToolUse (Write/Edit) | Parse-validate `.gd` files via `godot --headless --check-only` |
| 6 | Skill Load Verification | PostToolUse (Agent) | Verify SKILL_LOADED signal in agent responses |
| 7 | Empirical Validation | SubagentStop (developer/godot) | Detect runtime-only acceptance criteria |

---

## Hook Details

### 1. Config Check (SessionStart)

**Event**: `SessionStart`
**Matcher**: `*` (all sessions)
**Type**: Command (`check_config.py`)
**Timeout**: 5 seconds

Runs at the start of every session. Validates that `.delivery/config.yml` exists and checks its schema version against the current version. Reports warnings if the config is missing, stale, or outdated.

---

### 2. Retrospective Enforcement (Stop)

**Event**: `Stop`
**Matcher**: `*` (all sessions)
**Type**: Prompt
**Timeout**: 15 seconds

Checks if the session involved delivery-flow pipeline work. If pipeline work occurred, verifies that:

1. A retrospective was run
2. Memory file was written to `.delivery/memory/`
3. Defect review was completed (if defects were found)

If the post-pipeline protocol was not completed, the hook blocks the session end with a reason.

**Configuration**: Controlled by `enforcement.retro_frequency` and `enforcement.retro_skip_allowed` in config.

---

### 3. Pipeline Bypass Detection (PreToolUse - Skill)

**Event**: `PreToolUse`
**Matcher**: `Skill`
**Type**: Prompt
**Timeout**: 15 seconds

Detects when implementation skills (`delivery-team:developer`, `delivery-team:godot`, `delivery-team:quality`) are invoked for implementation work outside an active delivery pipeline. If no `.delivery/config.yml` exists, the hook denies the invocation with a message directing the user to start the pipeline first or explicitly skip.

Non-implementation skills (delivery-flow, product-delivery, architect, ui, operations, user-feedback) are always allowed.

---

### 4. Agent Prompt Audit (PreToolUse - Agent)

**Event**: `PreToolUse`
**Matcher**: `Agent`
**Type**: Command (`audit_agent_prompt.py`)
**Timeout**: 10 seconds

Audits agent prompts before they execute. Checks for context isolation compliance — ensures agent prompts do not leak context from other agents or contain information outside their isolated scope.

**Configuration**: Controlled by `pipeline.isolation_audit` (off, warn, block).

---

### 5. GDScript Validation (PostToolUse - Write/Edit)

**Event**: `PostToolUse`
**Matcher**: `Write|Edit`
**Type**: Command (`validate_gdscript.py`)
**Timeout**: 15 seconds

After any file is written or edited, checks if the file has a `.gd` extension. If so, runs `godot --headless --check-only` to parse-validate the GDScript syntax. Reports errors if the script has syntax issues.

Only activates for `.gd` files — other file types are ignored.

---

### 6. Skill Load Verification (PostToolUse - Agent)

**Event**: `PostToolUse`
**Matcher**: `Agent`
**Type**: Command (`verify_skill_load.py`)
**Timeout**: 10 seconds

After an agent sub-agent completes, verifies that the response begins with the `SKILL_LOADED: <skill-name>` signal. This confirms the skill was actually activated rather than the agent proceeding without loading its SKILL.md.

**Configuration**: Controlled by `pipeline.verify_skill_loading` (default: true).

---

### 7. Empirical Validation (SubagentStop)

**Event**: `SubagentStop`
**Matcher**: `developer|godot`
**Type**: Command (`flag_empirical_validation.py`)
**Timeout**: 30 seconds

When a developer or godot sub-agent completes, scans the agent's output for acceptance criteria that require runtime validation (visual output, user interaction, API responses, database queries). Flags these criteria as requiring manual or runtime verification rather than code inspection alone.

This prevents acceptance criteria from being incorrectly marked as "verified by inspection" when they require the application to be running.
