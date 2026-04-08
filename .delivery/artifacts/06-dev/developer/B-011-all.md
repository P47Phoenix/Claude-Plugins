# Developer Notes -- B-011-A, B-011-B, B-011-C

**Developer**: Gimli
**Date**: 2026-04-05
**Pipeline**: run-2026-04-05-3d92
**Target file**: `delivery-team/skills/delivery-flow/references/setup-wizard.md`

---

## Implementation Summary

All three stories implemented as a single pass -- additions only to `setup-wizard.md`. No existing content modified or deleted. Three new sections inserted between "Project-Level Hook Installation" (ends at original line 338) and "Config File Format" (original line 342).

### Sections Added

1. **Stale Hook Migration** (B-011-A) -- Lines 342-406 in updated file
   - History callout referencing commit `0ef5070`
   - When migration runs (wizard execution, before hook installation)
   - Scan targets (both settings files, independent handling)
   - Detection criteria (type=prompt + matcher includes Edit/Write/NotebookEdit)
   - Removal behavior (remove stale, preserve command, clean empty arrays)
   - Logging format (file path, matcher removed, reason)
   - Edge cases table (6 scenarios: missing file, no stale hooks, coexisting hooks, non-conflicting prompt hooks, single-file stale, multiple stale)

2. **Post-Install Hook Validation** (B-011-B) -- Lines 408-483 in updated file
   - When validation runs (after installation, every wizard execution)
   - Expected hooks table with all 8 hooks (7 from hooks.json + 1 project-level)
   - Note that hook 8 conditional on `enforcement.source_code_hook` config
   - Validation process (5-step: locate, verify type, verify command, verify timeout, check source)
   - Duplicate detection logic (same event type + matcher, different hook type)
   - Cleanup behavior for anything migration missed
   - Validation summary table with Status column (PASS/FAIL/MISSING/CLEANED)
   - Completion announcements for success and failure cases

3. **Conflict Detection Logic** (B-011-C) -- Lines 485-513 in updated file
   - Flow diagram showing migration -> installation -> validation sequence
   - Conflict identification definition
   - Precedence rule (command over prompt) with rationale
   - Reference back to commit `0ef5070` for historical context

### Acceptance Criteria Cross-Check

#### B-011-A (Stale Hook Migration Logic)
- [x] Trigger conditions documented (config upgrade or fresh setup)
- [x] Scan targets: `.claude/settings.local.json` AND `.claude/settings.json`
- [x] Detection: `type: "prompt"` AND matcher includes Edit/Write/NotebookEdit
- [x] Removal behavior documented
- [x] Logging: file path, matcher removed, reason
- [x] Edge case: settings file doesn't exist (skip gracefully)
- [x] Edge case: no stale hooks ("No stale hooks detected")
- [x] Edge case: non-conflicting prompt hooks preserved (e.g., Bash matcher)
- [x] Edge case: command hook already present alongside stale prompt hook
- [x] Both files scanned independently

#### B-011-B (Post-Install Hook Validation)
- [x] Runs AFTER hook installation
- [x] Expected hooks table with all 8 hooks
- [x] Columns: Hook Name, Event Type, Matcher, Hook Type, Command/Prompt, Timeout, Source
- [x] Validation checks: type, command, matcher, timeout
- [x] Duplicate detection: same matcher, different type
- [x] Cleanup: remove stale prompt hooks superseded by command
- [x] Summary table with Status column (PASS/FAIL/CLEANED/MISSING)
- [x] Missing hooks reported with expected config
- [x] All-PASS success announcement
- [x] Non-PreToolUse hooks validated (SessionStart, Stop, PostToolUse, SubagentStop all in table)

#### B-011-C (Documentation Update)
- [x] Migration note referencing commit `0ef5070`
- [x] Conflict detection logic documented clearly
- [x] Expected hooks table accurate against hooks.json
- [x] Existing wizard content (Q1-Q12, config format, directory initialization) UNCHANGED
- [x] Sections placed after "Project-Level Hook Installation" and before "Config File Format"
- [x] Same markdown style as rest of document

### Verification

- Existing sections Q1-Q12: untouched (lines 1-308 unchanged)
- Project-Level Hook Installation section: untouched (lines 309-338 unchanged)
- Config File Format section: untouched (starts at line 515 in updated file)
- Directory Initialization section: untouched
- Pipeline Integration section: untouched
- Re-Running the Wizard section: untouched

### Hooks Table Accuracy

Verified against `delivery-team/hooks/hooks.json`:
1. SessionStart / * / command / check_config.py / 5 -- MATCH
2. Stop / * / prompt / retrospective enforcement / 15 -- MATCH
3. PreToolUse / Skill / prompt / pipeline bypass detection / 15 -- MATCH
4. PreToolUse / Agent / command / audit_agent_prompt.py / 10 -- MATCH
5. PostToolUse / Write|Edit / command / validate_gdscript.py / 15 -- MATCH
6. PostToolUse / Agent / command / verify_skill_load.py / 10 -- MATCH
7. SubagentStop / developer|godot / command / flag_empirical_validation.py / 30 -- MATCH
8. PreToolUse / Edit|Write|NotebookEdit / command / enforce_pipeline_scope.py / 5 -- from project settings (task spec)

No discrepancies found.
