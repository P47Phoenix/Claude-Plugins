# State Management Reference

**Status**: COMPLETE (US-105)
**Version**: 1.0
**Architecture Reference**: Section 7.1, 7.2, 7.3, 7.4, 7.5, 3.4.1

This file is the authoritative source for pipeline state persistence, atomic write protocol, resume logic, corruption handling, and staleness detection for PAUSED_AWAITING_HUMAN states.

---

## 1. State File Format

Pipeline state is persisted at `.hardware/state.md` as a Markdown file with YAML frontmatter.

> **Trade-off (F-03):** Markdown-with-YAML-frontmatter is less parse-robust than pure YAML. Chosen to mirror delivery-flow's established convention. The `state_manager.py` script MUST use a robust frontmatter parser (Python `yaml.safe_load()` with explicit `---` delimiter detection, NOT regex-based splitting).

> **Security invariant (SEC-01):** All YAML parsing MUST use `yaml.safe_load()` -- never `yaml.load()` or `yaml.FullLoader`.

### 1.1 State File Schema

```yaml
---
pipeline_id: "run-2026-04-12-hw01"
status: in_progress           # Enum: in_progress | paused | paused_dispatch_error | completed | aborted
started: "2026-04-12T10:30:00Z"
last_updated: "2026-04-12T14:22:00Z"
current_stage: 3              # 1-8
stages_completed: [1, 2]
stages_skipped: []

# Config change detection (hash-based, F-10 resolution)
config_hash: "sha256:a1b2c3d4e5f6..."
config_snapshot_file: ".hardware/config-snapshot-run-2026-04-12-hw01.yml"

# Artifact registry (path -> stage metadata)
artifacts:
  ".hardware/artifacts/01-concept/requirements.md":
    stage: 1
    role: hw-product-owner
    timestamp: "2026-04-12T11:00:00Z"

# Gate results (ordered by execution)
gates:
  - stage: 1
    gate: concept-gate
    result: DONE
    timestamp: "2026-04-12T11:00:00Z"
    validators:
      - id: requirements-completeness
        result: DONE

# Rework history
rework_history:
  total_reworks: 0
  paths: {}

# Human checkpoints (for human-execution stages)
checkpoints: []

# Tamper detection (advisory, SEC-05)
_integrity_hash: "sha256:..."
---

# Pipeline State: <project-name>

This file tracks the state of the hardware pipeline run `<pipeline_id>`.
Do not edit manually -- managed by the hardware-flow orchestrator.
```

### 1.2 Required Fields

These fields MUST be present for a valid state file:

| Field | Type | Description |
|-------|------|-------------|
| `pipeline_id` | string | Unique run identifier, format: `run-YYYY-MM-DD-<suffix>` |
| `status` | enum | One of: `in_progress`, `paused`, `paused_dispatch_error`, `completed`, `aborted` |
| `started` | ISO 8601 | Pipeline start timestamp |
| `last_updated` | ISO 8601 | Most recent state write timestamp |
| `current_stage` | int (1-8) | Stage currently executing or next to execute |
| `stages_completed` | list[int] | Completed stage numbers |
| `config_hash` | string | SHA-256 of `.hardware/config.yml` at pipeline start |

### 1.3 Integrity Hash (SEC-05)

The `_integrity_hash` field is a SHA-256 computed over the serialized `stages_completed` and `gates` arrays. This is advisory tamper detection -- the pipeline warns but does not block on mismatch.

```
WARNING: State file appears to have been manually edited.
Gate results may not reflect actual pipeline execution.
Continue anyway? [Y/n]
```

---

## 2. Atomic Write Protocol

State writes MUST be atomic to prevent corruption from interrupted writes (session crash, Ctrl-C, power loss).

### 2.1 Write Sequence

```
1. Serialize full state to YAML frontmatter + Markdown body
2. Compute _integrity_hash over stages_completed + gates
3. Write to temporary file: .hardware/state.md.tmp
4. Flush and fsync the temporary file
5. Rename .hardware/state.md.tmp -> .hardware/state.md (atomic on POSIX; near-atomic on Windows NTFS)
6. Update last_updated timestamp in the in-memory state
```

### 2.2 Implementation Notes

- **temp file location**: Same directory as target (`.hardware/`) to ensure same-filesystem rename
- **Python implementation**: Use `os.replace()` for the rename step (cross-platform atomic rename)
- **Encoding**: UTF-8, no BOM
- **Newlines**: LF (Unix-style) for cross-platform consistency

### 2.3 Write Failure Recovery

If the rename fails (permissions, disk full):
1. Log `HW-STA-004: State write failed: <error>`
2. Retry once after 1-second delay
3. If retry fails: pipeline PAUSES with `paused_dispatch_error` status using the last successfully written state
4. The `.tmp` file is cleaned up on next successful write or pipeline start

---

## 3. State Operations

| Operation | Trigger | Actions |
|-----------|---------|---------|
| **Create** | Pipeline start | Initialize with sanitized `pipeline_id`, `config_hash` (SHA-256), `status=in_progress`. Save config copy to `.hardware/config-snapshot-<pipeline_id>.yml` via `safe_join()`. |
| **Update (stage)** | Stage completion | Add stage to `stages_completed`, append gate results, register artifacts, update `last_updated` |
| **Update (rework)** | Rework triggered | Add rework event to `rework_history`, update `current_stage` to rework target |
| **Pause** | Human-execution stage | Set `status=paused`, save checkpoint entry with `status: pending` |
| **Resume** | Session restart | Load state, validate artifacts, continue from `current_stage` |
| **Complete** | All stages done | Set `status=completed`, final `last_updated` timestamp |
| **Abort** | User aborts or unresolved escalation | Set `status=aborted`, preserve all artifacts |

---

## 4. Resume Logic

### 4.1 Resume Protocol

1. **Detect state**: Check for `.hardware/state.md` at session start or on "resume hardware pipeline" command
2. **Parse and validate**:
   - a. Attempt YAML frontmatter parse (first non-empty line MUST be `---`)
   - b. If parse fails: trigger corruption handling (Section 5)
   - c. If required fields missing: trigger incomplete state handling (Section 5)
   - d. Validate via `state_manager.validate_state(path) -> (valid: bool, errors: list)`
3. **Check resumable status**: Only `in_progress` or `paused` states are resumable
4. **Artifact integrity**: Verify all files in the artifact registry exist on disk
   - If artifacts missing: announce which, offer **Restart from that stage** / **Abandon**
5. **Config drift detection**: Compute SHA-256 of current `.hardware/config.yml`, compare to `config_hash`
   - If mismatch: warn "Config has changed since this pipeline started. Resume uses the original config snapshot. Choose Restart to apply new config."
6. **Present options**: **Resume** / **Restart** / **Abandon**
7. **On Resume**: Load config from snapshot file, skip completed stages, start at `current_stage`
8. **On Restart**: Archive state file to `.hardware/archived/`, start fresh with current config
9. **On Abandon**: Delete state file, no pipeline runs

### 4.2 Completed/Aborted State Handling

If `status` is `completed` or `aborted`:
- Display: "Previous pipeline run <pipeline_id> is <status>. Start a new pipeline? [Y/n]"
- On Yes: Archive old state, initialize new run
- On No: No action

---

## 5. State Corruption and Parse Failure Handling

### 5.1 YAML Parse Failure

When `.hardware/state.md` exists but YAML frontmatter cannot be parsed:

```
STATE_FILE_CORRUPTED: .hardware/state.md -- YAML parse error: <error details>
```

**User options:**
- **Restart**: Archive corrupted file to `.hardware/archived/corrupted-<timestamp>.md`, start fresh pipeline with current config
- **Manual Fix**: Display the parse error and the first 20 lines of the file so the user can fix the syntax error, then retry parse

### 5.2 Missing Required Fields

When YAML parses successfully but required fields are absent:

```
STATE_FILE_INCOMPLETE: Missing required fields: [pipeline_id, current_stage]
```

**User options:** Same as parse failure (Restart / Manual Fix)

### 5.3 Validation Function

```python
def validate_state(path: str) -> tuple[bool, list[str]]:
    """Validate state file integrity.

    Returns:
        (True, []) if valid
        (False, [error_messages]) if invalid
    """
    errors = []
    # 1. Check file exists
    # 2. Parse YAML frontmatter (safe_load)
    # 3. Check required fields present
    # 4. Check status is valid enum value
    # 5. Check current_stage is 1-8
    # 6. Check stages_completed is list of ints
    # 7. Verify _integrity_hash if present (advisory)
    return (len(errors) == 0, errors)
```

---

## 6. Staleness Detection for PAUSED_AWAITING_HUMAN

When the pipeline is in `paused` or `paused_dispatch_error` status, the SessionStart hook performs staleness detection on every session start.

### 6.1 Detection Protocol

1. Read `.hardware/state.md` and parse `last_updated` timestamp
2. Compute elapsed time since `last_updated`
3. Always display paused status regardless of age:

```
PIPELINE PAUSED at Stage 4 (Prototype) -- awaiting human action.
Paused since: 2026-04-10T14:22:00Z (2 days ago).
```

### 6.2 Staleness Thresholds

| Elapsed Time | Severity | Message |
|-------------|----------|---------|
| < 7 days | Info | Standard paused status display (no extra warning) |
| 7-29 days | Warning | `STALE PIPELINE: Paused for <N> days. Hardware context may have changed. Review state before resuming.` |
| 30+ days | Critical | `CRITICALLY STALE PIPELINE: Paused for <N> days. Component availability, pricing, and compliance requirements may have changed significantly. Strongly recommend Restart over Resume.` |

### 6.3 Staleness Actions

At any staleness level, the user is presented with: **Resume** / **Restart** / **Abandon**

The staleness warning is advisory -- the user can always choose Resume regardless of elapsed time.

---

## 7. Path Sanitization (SEC-01)

All file paths constructed from user-controlled or config-derived values MUST be sanitized.

### 7.1 Sanitization Rules

1. **Whitelist validation**: Path components MUST match `^[a-zA-Z0-9._-]+$`. Reject `/`, `\`, `..`, null bytes.
2. **Canonicalization check**: Resolve to absolute path, verify it starts with `.hardware/` (resolved).
3. **Apply everywhere**: Config snapshots, archived artifacts, artifact registry paths, rework archive paths.

### 7.2 API (state_manager.py)

```python
import os
import re

SAFE_PATH_COMPONENT = re.compile(r'^[a-zA-Z0-9._-]+$')

def sanitize_path_component(value: str) -> str:
    """Validate a single path component against the whitelist.
    Raises ValueError if the value contains unsafe characters."""
    if not SAFE_PATH_COMPONENT.match(value):
        raise ValueError(
            f"Unsafe path component: '{value}'. "
            f"Only alphanumerics, dots, hyphens, and underscores are permitted."
        )
    return value

def safe_join(base_dir: str, *components: str) -> str:
    """Join path components with sandbox validation.
    Raises ValueError if the resolved path escapes base_dir."""
    for c in components:
        sanitize_path_component(c)
    candidate = os.path.join(base_dir, *components)
    resolved = os.path.realpath(candidate)
    base_resolved = os.path.realpath(base_dir)
    if not resolved.startswith(base_resolved + os.sep) and resolved != base_resolved:
        raise ValueError(
            f"Path traversal detected: '{candidate}' resolves to '{resolved}' "
            f"which is outside sandbox '{base_resolved}'."
        )
    return candidate
```

All path construction MUST use `safe_join()` rather than raw string interpolation or `os.path.join()`.

---

## 8. Artifact Directory Structure

```
.hardware/
+-- config.yml                          # Project configuration
+-- state.md                            # Pipeline state (this file's subject)
+-- config-snapshot-<pipeline_id>.yml   # Config frozen at pipeline start
+-- memory/                             # Self-learning memory (see memory-protocol.md)
+-- archived/                           # Archived state files from previous runs
|   +-- corrupted-<timestamp>.md        # Corrupted state files preserved for debugging
+-- artifacts/                          # Pipeline artifacts organized by stage
    +-- 01-concept/
    +-- 02-schematic/
    +-- 03-layout/
    +-- 04-prototype/
    |   +-- archived/run-N/             # Rework iteration archives (never deleted)
    +-- 05-dfm-dfa/
    +-- 06-compliance/
    +-- 07-pilot-run/
    +-- 08-production-release/
```
