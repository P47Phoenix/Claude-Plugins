# Sprint Plan -- Issue #40: Enforcement Hook Cannot Read Config

**Type**: BUG_FIX | **Light Mode** | **Scrum Bag**: Aragorn
**Date**: 2026-03-25

---

## User Story

**As a** delivery-flow user with a configured `pipeline.scope` setting,
**I want** the enforcement hook to actually read my `.delivery/config.yml` at invocation time,
**So that** scope enforcement reflects my real configuration rather than ignoring it entirely.

### Acceptance Criteria

**AC-1: Config-driven scope evaluation**

- Given a `.delivery/config.yml` with `pipeline.scope: code-only`
- When a Write/Edit targets a `.py` file and no pipeline is active
- Then the hook returns a warning advising the user to use the delivery pipeline

**AC-2: Custom scope patterns respected**

- Given a `.delivery/config.yml` with `pipeline.scope: custom` and `scope_include` patterns defined
- When a Write/Edit targets a file matching a `scope_include` pattern
- Then the hook enforces on that file (warns if no active pipeline)

**AC-3: All-scope with exclusions**

- Given a `.delivery/config.yml` with `pipeline.scope: all`
- When a Write/Edit targets a file matching a `scope_exclude` pattern (e.g., `.delivery/`, `.git/`)
- Then the hook allows the edit without warning

**AC-4: Graceful degradation**

- Given no `.delivery/config.yml` exists, or the file is malformed
- When any Write/Edit is invoked
- Then the hook passes through silently (no enforcement, no crash)

**AC-5: Active pipeline detection**

- Given a `.delivery/state.md` file exists indicating an active pipeline
- When a Write/Edit targets an in-scope file
- Then the hook allows the edit (pipeline is running, enforcement satisfied)

**AC-6: Settings.json updated**

- Given the fix is applied
- When Claude loads `.claude/settings.json`
- Then the hook entry is type `command` pointing to `python delivery-team/hooks/enforce_pipeline_scope.py`, not a prompt hook

---

## Test Cases

| ID | Scenario | Input | Expected |
|----|----------|-------|----------|
| T1 | Code-only scope, no pipeline, source file | scope=`code-only`, target=`app.py`, no state.md | Warning returned |
| T2 | Code-only scope, no pipeline, non-source file | scope=`code-only`, target=`README.md`, no state.md | Allow (not a source file) |
| T3 | Code-only scope, active pipeline, source file | scope=`code-only`, target=`app.py`, state.md exists | Allow |
| T4 | All scope, excluded path | scope=`all`, target=`.delivery/state.md` | Allow (excluded) |
| T5 | All scope, non-excluded path, no pipeline | scope=`all`, target=`src/main.rs`, no state.md | Warning |
| T6 | Custom scope, matching include pattern | scope=`custom`, include=`["*.py"]`, target=`fix.py`, no state.md | Warning |
| T7 | Custom scope, non-matching file | scope=`custom`, include=`["*.py"]`, target=`style.css` | Allow |
| T8 | Missing config file entirely | no config.yml | Allow (pass-through) |
| T9 | Malformed YAML in config | config.yml contains `{{{broken` | Allow (pass-through, no crash) |
| T10 | Missing scope key in valid config | config.yml exists but no `pipeline.scope` key | Allow (defaults to pass-through) |

---

## Implementation Approach

### New File: `delivery-team/hooks/enforce_pipeline_scope.py`

The heart of the fix. A Python command hook that:

1. Reads hook input via `hook_utils.read_hook_input()` to get the target file path from the tool invocation
2. Reads `.delivery/config.yml` using `pathlib` + stdlib YAML parsing
3. Reads `.delivery/state.md` to detect active pipeline
4. Evaluates scope rules against the target file path:
   - `code-only`: match against known source extensions
   - `all`: allow if file matches any `scope_exclude` pattern
   - `custom`: match against `scope_include` glob patterns
5. Returns response via `hook_utils.emit_response()`

Uses `pathlib` throughout. No shell calls. No external dependencies beyond what `hook_utils.py` already establishes.

### Modified File: `.claude/settings.json`

Replace the prompt hook with a command hook:

```json
{
  "type": "command",
  "command": "python delivery-team/hooks/enforce_pipeline_scope.py",
  "timeout": 10
}
```

The matcher (`Edit|Write|NotebookEdit`) stays the same. Only the hook definition changes.

### No Other Files Touched

The config schema is unchanged. Other hooks are unchanged. This is a surgical replacement of one broken hook with one that works.

---

*A guard who cannot read the law is no guard at all. We give him eyes.*
