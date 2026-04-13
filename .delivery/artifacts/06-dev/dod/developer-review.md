# Stage 6 Developer DoD Re-Validation: hardware-team Plugin

**Reviewer:** Gimli (Developer)
**Date:** 2026-04-12
**Scope:** Re-validate fixes for F-001, F-002, config field mismatch, CompE minimum_model_tier

> "I have returned to these corridors with hammer in hand. Let us see if the cracks have been sealed, or if the mountain still groans."

---

## Prior Findings Re-Validation

### F-001 [WAS BLOCKING] Missing `check_pipeline_bypass.py`

**Status: RESOLVED**

- File exists at `hooks/check_pipeline_bypass.py` (3,606 bytes, 104 lines)
- Compiles cleanly via `py_compile` -- no syntax errors
- Matches `hooks.json` reference: `PreToolUse` -> `Skill` matcher -> `check_pipeline_bypass.py`
- Defines `HARDWARE_ROLE_SKILLS` set with all 6 hardware role skills (hw-product-owner, electrical-engineer, pcb-layout-engineer, manufacturing-engineer, compliance-engineer, test-engineer)
- Reads hook input from stdin via `json.loads()` per Claude Code hook protocol
- Non-blocking: emits warning JSON but always exits 0
- Security: no `shell=True`, no `os.system`, all input via `json.loads()`, SEC-06 compliant

No regressions. The corridor is sealed.

---

### F-002 [WAS BLOCKING] Missing `check_kicad_file.py`

**Status: RESOLVED**

- File exists at `hooks/check_kicad_file.py` (3,064 bytes, 106 lines)
- Compiles cleanly via `py_compile` -- no syntax errors
- Matches `hooks.json` reference: `PostToolUse` -> `Write|Edit` matcher -> `check_kicad_file.py`
- Detects `.kicad_sch`, `.kicad_pcb`, `.kicad_pro` extensions correctly
- Reads hook input from stdin via `json.loads()` per Claude Code hook protocol
- Non-blocking: emits notification JSON but always exits 0
- Security: null-byte path validation, no `shell=True`, SEC-06 compliant

No regressions. The second corridor holds.

---

### Config field mismatch -- schema_version alignment

**Status: RESOLVED**

Both validation touchpoints use `schema_version` consistently:

| File | Line | Value | Correct |
|------|------|-------|---------|
| `hooks/validate_session.py` | 22 | `CURRENT_SCHEMA_VERSION = "1.0"` | YES |
| `hooks/validate_session.py` | 81 | Searches for `schema_version` key in YAML | YES |
| `scripts/validate_config.py` | 113 | `KNOWN_SCHEMA_VERSIONS = {"1.0"}` | YES |
| `scripts/validate_config.py` | 191 | Validates `schema_version` against known set | YES |

No field name mismatches. No `config_version` or other variants found anywhere.

---

### CompE missing `minimum_model_tier`

**Status: RESOLVED**

- `skills/compliance-engineer/SKILL.md` frontmatter line 5: `minimum_model_tier: Sonnet`
- Role Identity table line 20: `Model Tier | Sonnet (structured cross-referencing)`
- Frontmatter and body are consistent

---

## Regression Check

### hooks.json Full Integrity

Every command in `hooks.json` references an existing, compilable script:

| Hook Event | Matcher | Script | Exists | Compiles | Exit Behavior |
|------------|---------|--------|--------|----------|---------------|
| SessionStart | `*` | `validate_session.py` | YES | YES | Always 0 |
| SessionStart | `*` | `check_kicad_happy.py` | YES | YES | Always 0 |
| PreToolUse | `Skill` | `check_pipeline_bypass.py` | YES | YES | Always 0 |
| PostToolUse | `Write\|Edit` | `check_kicad_file.py` | YES | YES | Always 0 |
| PostToolUse | `Write\|Edit` | `drc_check.py` | YES | YES | Always 0 |
| PostToolUse | `Write\|Edit` | `bom_drift.py` | YES | YES | Always 0 |

All 6 scripts use `${CLAUDE_PLUGIN_ROOT}` path prefix -- correct for hook protocol.
All 6 scripts use `{"message": ...}` JSON output protocol -- correct.

### Cross-Script Consistency

- All 6 hooks follow the same stdin-JSON-in / stdout-JSON-out pattern
- All 6 hooks are non-blocking (exit 0 regardless of findings)
- All 6 hooks have SEC-06 compliant docstrings and no `shell=True`
- `validate_session.py` and `validate_config.py` agree on schema version `1.0`
- `check_kicad_file.py` and `drc_check.py` both extract file paths the same way (consistent `_extract_file_path` pattern)
- `drc_check.py` and `bom_drift.py` both handle `.kicad_sch` -- no conflict (DRC checks schematic rules, BOM drift checks component references)

### No New Issues Introduced

- No orphan script files (all scripts in `hooks/` are referenced by `hooks.json`)
- No orphan `hooks.json` entries (all entries point to existing scripts)
- `marketplace.json` registration unchanged and correct (7 skill paths)
- Plugin-level `SKILL.md` unchanged and correct

---

## Prior Non-Blocking Findings (Unchanged)

These were not in scope for this re-validation but remain for tracking:

| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| F-003 | Warning | `rework-paths.md` vs `rework-loops.md` name mismatch | Open |
| F-004 | Warning | `gate-framework.md` decomposed into separate files | Open |
| F-005 | Warning | Missing `state_manager.py` script | Open |
| F-006 | Warning | `validate_config.py` location mismatch vs architecture | Open |
| F-007 | Warning | Test fixture directory has specs only, no KiCad files | Open |

These are non-blocking and do not affect the gate decision.

---

## Verdict

> "The cracks are filled, the beams reinforced. Both corridors that threatened cave-ins now hold firm as the pillars of Khazad-dum. The forge is sound. And my axe approves."

**STATUS: DONE**

All four targeted fixes verified. No regressions. The two formerly-blocking issues (F-001, F-002) are fully resolved. Config field alignment is correct. CompE frontmatter is complete. All 6 hook scripts compile, follow protocol, and are correctly wired in hooks.json.
