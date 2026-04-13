# Architect DoD Review: hardware-team Plugin Re-Validation

**Reviewer**: Celebrimbor (Solution Architect)
**Date**: 2026-04-12
**Review Type**: DoD Re-Validation (Gate 6)
**Prior Blocking Findings**: FINDING-02 (missing check_pipeline_bypass.py), FINDING-03 (missing check_kicad_file.py), FINDING-07 (config_version vs schema_version mismatch)
**Verdict**: PASS -- All blocking findings resolved, no regressions

---

> "The second tempering reveals whether the alloy holds true. These corrections have been wrought with precision."

---

## 1. Prior Blocking Findings -- Resolution Verification

### FINDING-02: check_pipeline_bypass.py Missing

**Prior Status**: BLOCKING -- `hooks.json` referenced `check_pipeline_bypass.py` but file did not exist on disk.

**Current Status**: RESOLVED

- File exists at `hardware-team/hooks/check_pipeline_bypass.py` (105 lines)
- Compiles cleanly (`py_compile` passes)
- Follows hook protocol: reads JSON from stdin, emits `{"message": ...}` to stdout, exits 0
- Implements correct logic: checks `HARDWARE_ROLE_SKILLS` set (6 role skills), detects pipeline context via `agent_prompt` and `session_context` heuristics, warns when role skills invoked outside pipeline
- No `shell=True`, no `subprocess`, no `eval` -- SEC-06 compliant
- `hooks.json` PreToolUse(Skill) entry correctly references this script

### FINDING-03: check_kicad_file.py Missing

**Prior Status**: BLOCKING -- `hooks.json` referenced `check_kicad_file.py` but file did not exist on disk.

**Current Status**: RESOLVED

- File exists at `hardware-team/hooks/check_kicad_file.py` (107 lines)
- Compiles cleanly (`py_compile` passes)
- Follows hook protocol: reads JSON from stdin, emits `{"message": ...}` to stdout, exits 0
- Correctly detects KiCad file extensions (`.kicad_sch`, `.kicad_pcb`, `.kicad_pro`) and emits notification for downstream hooks (`drc_check.py`, `bom_drift.py`)
- Path safety validation (null byte check) present
- `hooks.json` PostToolUse(Write|Edit) entry correctly references this script as the first hook in the chain (before `drc_check.py` and `bom_drift.py`)

### FINDING-07: config_version vs schema_version Field Name Mismatch

**Prior Status**: BLOCKING -- `validate_session.py` looked for `config_version` instead of `schema_version`, causing false warnings on valid configs.

**Current Status**: RESOLVED

- `validate_session.py` line 81: `config.get("schema_version", "")` -- correct field name
- `validate_session.py` line 83: regex fallback also searches for `schema_version` -- correct
- `validate_session.py` line 22: `CURRENT_SCHEMA_VERSION = "1.0"` -- matches `validate_config.py` and `config-schema.md`
- No remaining references to `config_version` anywhere in the file

---

## 2. Regression Check

### All Hook Scripts Compile and Exist

| Script | Event | Exists | Compiles | Lines |
|--------|-------|--------|----------|-------|
| `validate_session.py` | SessionStart | Yes | Yes | 259 |
| `check_kicad_happy.py` | SessionStart | Yes | Yes | 167 |
| `check_pipeline_bypass.py` | PreToolUse(Skill) | Yes | Yes | 105 |
| `check_kicad_file.py` | PostToolUse(Write/Edit) | Yes | Yes | 107 |
| `drc_check.py` | PostToolUse(Write/Edit) | Yes | Yes | 199 |
| `bom_drift.py` | PostToolUse(Write/Edit) | Yes | Yes | 205 |

### hooks.json Integrity

- All 6 scripts referenced in `hooks.json` exist on disk -- zero dead references
- Three event types used (SessionStart, PreToolUse, PostToolUse) -- all valid per Claude Code hook protocol
- PostToolUse chain ordering correct: `check_kicad_file.py` (notification) -> `drc_check.py` (validation) -> `bom_drift.py` (drift detection)

### Utility Scripts Compile

| Script | Exists | Compiles |
|--------|--------|----------|
| `scripts/validate_config.py` | Yes | Yes |
| `scripts/security.py` | Yes | Yes |

### Config Field Alignment (No Regression from FINDING-07 Fix)

| Source | Field Name | Version | Aligned |
|--------|-----------|---------|---------|
| `validate_session.py` | `schema_version` | `1.0` | Yes |
| `validate_config.py` | `schema_version` | `{"1.0"}` | Yes |
| `config-schema.md` | `schema_version` | `1.0` | Yes |
| `hardware-flow/SKILL.md` | `schema_version` | `"1.0"` | Yes |

### Marketplace Registration (No Regression)

- 7 skill paths registered in `marketplace.json` match exactly 7 skill directories on disk
- No orphaned skills, no phantom skills
- Plugin description accurate

### Plugin Structure (No Regression)

- Root `SKILL.md` and `LICENSE.txt` present
- All 7 skills have `SKILL.md` files
- Reference file counts: hardware-flow (14), hw-product-owner (3), electrical-engineer (5), pcb-layout-engineer (3), manufacturing-engineer (4), compliance-engineer (4), test-engineer (4)
- `.hardware/` namespace used consistently (no `.delivery/` contamination)

---

## 3. Advisory Findings from Prior Review (Unchanged, Non-Blocking)

The following advisory findings from the prior review remain. They are naming inconsistencies that do not affect runtime behavior:

| ID | Description | Status |
|----|-------------|--------|
| FINDING-01 | Hook filename `validate_session.py` vs architecture-specified `check_hw_config.py` | Open (advisory) |
| FINDING-04 | Script filename `validate_config.py` vs architecture-specified `config_schema.py` | Open (advisory) |
| FINDING-05 | `security.py` provides `state_manager.py` functionality under a different name | Open (advisory) |
| FINDING-06 | `validate_config.py` at `scripts/` instead of `skills/hardware-flow/scripts/` | Open (advisory) |

These are acceptable deviations -- the functionality is present and correct; only the filenames differ from the architecture specification.

---

## 4. Gate Evaluation

**Gate 6 criterion**: Implementation conforms to architecture decisions [blocking]

All three prior blocking findings have been resolved:
- Hook scripts that were missing now exist, compile, and implement correct logic
- The config field name mismatch has been corrected
- No new defects introduced by the fixes
- No regressions in plugin structure, marketplace registration, or config alignment

The implementation conforms to the architecture. The forge holds true.

---

## Overall Verdict

**STATUS: DONE**

The corrections have been wrought with care. Every rivet holds. The hardware-team plugin passes Gate 6.
