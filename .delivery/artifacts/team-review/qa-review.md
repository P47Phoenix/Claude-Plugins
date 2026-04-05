# QA Review: delivery-team Plugin

**Reviewer**: Legolas (QA Engineer)
**Date**: 2026-04-04
**Scope**: Full quality review of delivery-team plugin
**Verdict**: 17 defects found. That bug still only counts as one.

---

## Summary

| Severity | Count |
|----------|-------|
| BLOCKING | 4 |
| WARNING | 9 |
| SUGGESTION | 4 |
| **Total** | **17** |

---

## BLOCKING Defects

### B-01: SKILL.md artifact paths contradict pipeline-stages.md (STALE REFERENCES)

**Files**:
- `delivery-team/skills/delivery-flow/SKILL.md` lines 549, 574, 591, 625, 644, 677, 703, 743, 763, 790-791, 832, 907
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` lines 193, 229, 258, 272, 323-324, 384-385, 456, 543

**Issue**: SKILL.md uses FLAT artifact paths (e.g., `.delivery/artifacts/01-idea-brief.md`, `.delivery/artifacts/02-prd.md`, `.delivery/artifacts/03-ux-design.md`), while pipeline-stages.md uses NAMESPACED paths (e.g., `.delivery/artifacts/01-idea/po/idea-brief.md`, `.delivery/artifacts/02-refine/po/prd.md`, `.delivery/artifacts/03-design/ux/user-flows.md`).

These are contradictory. SKILL.md and pipeline-stages.md are both authoritative references loaded during pipeline execution. An agent following SKILL.md will write artifacts to different locations than pipeline-stages.md specifies, causing downstream agents to fail when looking for artifacts at the wrong path.

The namespaced paths in pipeline-stages.md appear to be the intended format (matching the architecture document and actual pipeline runs in `.delivery/artifacts/`), making SKILL.md's flat paths the stale version.

**Specific contradictions**:
| SKILL.md (stale) | pipeline-stages.md (current) |
|-------------------|------------------------------|
| `.delivery/artifacts/01-idea-brief.md` | `.delivery/artifacts/01-idea/po/idea-brief.md` |
| `.delivery/artifacts/02-prd.md` | `.delivery/artifacts/02-refine/po/prd.md` |
| `.delivery/artifacts/03-ux-design.md` | `.delivery/artifacts/03-design/ux/user-flows.md` + 3 others |
| `.delivery/artifacts/04-architecture.md` | `.delivery/artifacts/04-architect/solution/architecture.md` |
| `.delivery/artifacts/04a-adrs/ADR-001.md` | `.delivery/artifacts/04-architect/debate-judge/decision.md` |
| `.delivery/artifacts/05-sprint-plan.md` | `.delivery/artifacts/05-plan/sm/sprint-plan.md` |
| `.delivery/artifacts/06-dev-notes.md` | `.delivery/artifacts/06-dev/developer/{story-id}.md` |
| `.delivery/artifacts/07-uat-report.md` | `.delivery/artifacts/07-uat/qa/test-plan.md` |

pipeline-stages.md entry conditions also use stale flat references (e.g., line 229: `01-idea-brief.md exists`, line 272: `02-prd.md exists`, line 543: `06-dev-notes.md exists`).

**Fix**: Update SKILL.md Stage Definitions section (lines 524-927) to use the namespaced artifact paths from pipeline-stages.md. Also update pipeline-stages.md entry conditions to use full namespaced paths.

---

### B-02: config-schema.json has wrong types for 3 keys (SCHEMA MISMATCH)

**Files**:
- `delivery-team/skills/delivery-flow/references/config-schema.json` lines 726-730, 773-780
- `delivery-team/skills/delivery-flow/references/config-schema.md` lines 89, 98

**Issue 1 -- `presentation.vocabulary_overrides`**: config-schema.md defines this as `map` type (line 89) and the YAML template shows `vocabulary_overrides: {}` (a map/object). config-schema.json defines it as `"type": "string"` with `"default": "{}"` (a string). This means JSON Schema validation will reject valid YAML configs that use an object value.

**Issue 2 -- `presentation.thresholds`**: config-schema.md defines this as `map[string, integer]` (line 98) with valid values "type-name: seconds pairs". config-schema.json defines it as `"type": "string"` with `"enum": ["type-name: seconds pairs (e.g.", "sprint-review: 120). 0 = unlimited."]` (lines 773-780). The generate-schema.py script has parsed the "Valid Values" column description as enum values instead of recognizing this as an object/map type. This is a parsing bug in the schema generator.

**Fix**: Fix `generate-schema.py` to handle `map[string, ...]` type correctly, producing `"type": "object"` with `"additionalProperties"`. Regenerate config-schema.json.

---

### B-03: enforce_pipeline_scope.py hook exists but is NOT registered in hooks.json (DEAD CODE)

**Files**:
- `delivery-team/hooks/enforce_pipeline_scope.py` (218 lines of implementation)
- `delivery-team/hooks/hooks.json` (no reference to enforce_pipeline_scope)
- `delivery-team/skills/delivery-flow/references/setup-wizard.md` (references the hook)

**Issue**: `enforce_pipeline_scope.py` is a fully implemented PreToolUse hook that warns when source code files are edited outside an active delivery pipeline. It reads `.delivery/config.yml` for scope settings. However, it is NOT registered in `hooks.json`, which means it NEVER executes.

The setup-wizard.md references installing this hook in the project's `.claude/settings.json` as a project-level hook (distinct from the plugin hooks in hooks.json). This is by design -- it should be installed per-project, not globally via the plugin. However:
1. CLAUDE.md lists "8 hooks across 5 event types" but only 7 are registered in hooks.json
2. The docs site `docs/reference/hooks.md` lists only 7 hooks
3. There is no documentation explaining this hook is project-level, not plugin-level

**Fix**: Either register it in hooks.json OR document clearly that this is a per-project hook installed by the setup wizard. Update hook count in documentation to be accurate.

---

### B-04: DoD validator prompt template contradicts context isolation rules (DESIGN CONFLICT)

**Files**:
- `delivery-team/skills/delivery-flow/SKILL.md` lines 942-962
- `delivery-team/skills/delivery-flow/SKILL.md` lines 289-295 (two-channel rule)
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` lines 122-166 (DoD Validator Dispatch Template)

**Issue**: SKILL.md's Team DoD Protocol (line 952) shows the validator prompt with artifact content INLINE:

```
Artifact:
---
[ARTIFACT CONTENT]
---
```

This directly violates the two-channel communication model defined at SKILL.md line 293: "The orchestrator NEVER reads an artifact and pastes its content into another agent's prompt."

Meanwhile, pipeline-stages.md's DoD Validator Dispatch Template (lines 122-166) correctly uses file paths:
```
--- INPUT ARTIFACTS (read these files) ---
{for each stage artifact:}
- {artifact_file_path}: {description}
```

The SKILL.md version will cause the orchestrator to read and paste artifact content, bloating agent prompts and violating isolation.

**Fix**: Update SKILL.md's DoD validator prompt template (lines 942-962) to match pipeline-stages.md's file-path-based template.

---

## WARNING Defects

### W-01: Docs site has incorrect Design stage output path

**Files**:
- `docs/user-guide/pipeline.md` line 70
- `docs/architecture/overview.md` line 51

**Issue**: Both docs files reference `.delivery/artifacts/03-design/ux/design.md` as the Design stage output. The actual outputs per pipeline-stages.md are: `03-design/ux/user-flows.md`, `03-design/ux/wireframes.md`, `03-design/ui/component-specs.md`, `03-design/ui/accessibility.md`. No file named `design.md` exists in the output specification.

**Fix**: Update docs files to list the correct output files.

---

### W-02: Docs config reference omits `pipeline.required_agent_retry_max`

**Files**:
- `docs/user-guide/config.md` (entire file)
- `delivery-team/skills/delivery-flow/references/config-schema.md` line 39

**Issue**: `pipeline.required_agent_retry_max` is defined in config-schema.md (line 39, type: integer, default: 2, range: 1-5) but is completely absent from the docs config reference at `docs/user-guide/config.md`. The YAML template in the docs also omits this key.

**Fix**: Add `pipeline.required_agent_retry_max` to the Pipeline Settings table in docs/user-guide/config.md.

---

### W-03: SKILL.md Quick Start says "3-question wizard" but also references "9+ question version"

**Files**:
- `delivery-team/skills/delivery-flow/SKILL.md` lines 116-124

**Issue**: Line 116 says the quick start is a "3-question wizard instead of the full 9+ question version." But config-schema.md references wizard questions up to Q14 (14+ questions). The "9+ question" claim is stale -- it should say "14+ question" or just "full version."

**Fix**: Update "9+ question" to "14+ question" or remove the specific number.

---

### W-04: Memory index has no stage chunks for Idea, Refine, or Architect

**Files**:
- `.delivery/memory/index.md` lines 38-43 (Stage Chunks table)

**Issue**: The Stage Chunks table lists files for Design, Plan, Development, and UAT. Stages Idea, Refine, and Architect have no stage chunk files. The memory protocol in SKILL.md (Phase 4, Step 2, line 348) says to "Read the stage-specific chunk from `memory/stages/<stage>.md`" for EVERY active stage. When the orchestrator attempts to read `memory/stages/idea.md`, `memory/stages/refine.md`, or `memory/stages/architect.md`, the files will not exist.

The protocol does handle this gracefully (proceed without lessons if no memory exists), but the index table creates a false impression that only 4 of 7 stages have lessons. After 13 runs, some lessons for Refine and Architect should have accumulated.

**Fix**: Either create stub chunk files for the missing stages, or update index.md with a note that stages with 100% pass rates have no accumulated lessons.

---

### W-05: Plan stage first-try pass rate inconsistency between index.md and stage lesson

**Files**:
- `.delivery/memory/index.md` line 14: "80% (4/5)"
- `.delivery/memory/stages/plan.md` line 9: "Plan has the lowest first-try pass rate (57%, 4/7 runs)"

**Issue**: index.md reports Plan stage at 80% (4/5) from the "last 5 runs" window, while plan.md lesson reports 57% (4/7) across "all runs." Both are technically correct (different windows), but the lesson text says "lowest first-try pass rate" without qualifying the window. If someone reads both, the numbers appear contradictory. The index.md note says "2 consecutive first-try passes with pre-loaded constraints" which explains the improvement trend.

**Fix**: Update the plan.md lesson to qualify the window: "57% (4/7 runs, all-time)" and note the improving trend.

---

### W-06: audit_agent_prompt.py does not respect `pipeline.isolation_audit` config setting

**Files**:
- `delivery-team/hooks/audit_agent_prompt.py` (entire file)
- `delivery-team/skills/delivery-flow/references/config-schema.md` line 36
- `docs/reference/hooks.md` line 72: "Controlled by pipeline.isolation_audit (off, warn, block)"

**Issue**: The docs claim the Agent Prompt Audit hook is controlled by `pipeline.isolation_audit` (off/warn/block). But the actual hook script (`audit_agent_prompt.py`) never reads `.delivery/config.yml` or checks the `isolation_audit` setting. It always runs with warn-level behavior (emits a systemMessage but never blocks). The "block" and "off" modes are documented but not implemented.

**Fix**: Either implement config reading in the hook script (read `isolation_audit` from config and adjust behavior) or remove the config key documentation as aspirational.

---

### W-07: generate_pptx.py calls sys.exit(1) inside generate_pptx() function

**Files**:
- `delivery-team/skills/presentation/scripts/generate_pptx.py` lines 344, 354, 366

**Issue**: The `generate_pptx()` function (which is documented as a reusable function with return value and Raises docstring) calls `sys.exit(1)` on three error paths instead of raising exceptions. This means:
1. The function cannot be used as a library -- calling code cannot catch errors
2. The docstring says "Raises: FileNotFoundError, json.JSONDecodeError, ValueError" but none of these are actually raised -- they are caught and converted to sys.exit(1)
3. If imported into a test harness, errors will kill the test process

**Fix**: Replace `sys.exit(1)` calls inside `generate_pptx()` with proper exception raises. Move sys.exit handling to the CLI `main()` function.

---

### W-08: validate_gdscript.py silently succeeds when Godot is not installed

**Files**:
- `delivery-team/hooks/validate_gdscript.py` line 26

**Issue**: When `godot` is not on PATH, the hook calls `exit_success()` silently. This means GDScript validation is completely bypassed with no warning. For GAME_DEV projects that specifically rely on this hook for quality enforcement, the silent bypass could allow broken scripts through the pipeline.

**Fix**: When Godot is not found, emit a warning message ("GDScript validation skipped: godot not found on PATH") instead of silently passing. This at least makes the bypass visible.

---

### W-09: Docs hooks page lists 7 hooks, CLAUDE.md says "7 hooks across 5 event types" -- both miss enforce_pipeline_scope

**Files**:
- `CLAUDE.md` line: "### delivery-team Hooks (7 hooks across 5 event types)"
- `docs/reference/hooks.md` line 4: "7 hooks across 5 event types"
- `delivery-team/hooks/enforce_pipeline_scope.py` (not documented anywhere)

**Issue**: The hook count is inconsistent with the actual codebase. There are 7 hooks in hooks.json plus enforce_pipeline_scope.py (project-level), making 8 hook scripts total. Neither CLAUDE.md nor the docs mention enforce_pipeline_scope at all.

**Fix**: Document enforce_pipeline_scope.py in both CLAUDE.md and docs/reference/hooks.md as a project-level hook installed by the setup wizard.

---

## SUGGESTION Defects

### S-01: SKILL.md has duplicate/redundant stage definitions

**Files**:
- `delivery-team/skills/delivery-flow/SKILL.md` lines 524-927 (inline stage definitions)
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (authoritative stage definitions)

**Issue**: SKILL.md contains a full second copy of all 7 stage definitions (lines 524-927) IN ADDITION to referencing `references/pipeline-stages.md` as the authoritative source (line 363: "Read the stage sub-flow from references/pipeline-stages.md"). This creates a maintenance burden where every change must be made in two places, and as B-01 shows, they have already diverged on artifact paths.

**Fix**: Consider removing the inline stage definitions from SKILL.md and relying solely on pipeline-stages.md. The SKILL.md can retain a summary table of stages with their depth/routing information without duplicating the full sub-flows.

---

### S-02: config-schema.md YAML template includes `decision_matrix_inputs.team_size: 4` as integer

**Files**:
- `delivery-team/skills/delivery-flow/references/config-schema.md` line 199

**Issue**: The YAML template shows `team_size: 4` (an integer), but the schema table (line 29) says the valid values for decision_matrix_inputs fields are "low/medium/high" (strings). The template is inconsistent with the schema definition.

**Fix**: Change template line 199 from `team_size: 4` to `team_size: medium` (or whatever string value is appropriate).

---

### S-03: No test coverage for hook scripts

**Files**:
- `delivery-team/hooks/*.py` (6 hook scripts)
- `delivery-team/hooks/lib/hook_utils.py` (shared utilities)

**Issue**: None of the hook scripts have unit tests. The hooks are critical infrastructure (config validation, pipeline enforcement, GDScript validation, empirical detection) but cannot be verified structurally. Key risks:
- `flag_empirical_validation.py` regex patterns could have false positives/negatives
- `enforce_pipeline_scope.py` YAML parsing with regex is fragile (no real YAML parser)
- `audit_agent_prompt.py` code fence counting heuristic could trigger on legitimate prompts
- `hook_utils.py` `exit_block()` writes to stderr -- untested contract with Claude Code

**Fix**: Add a `tests/` directory with unit tests for at minimum: hook_utils contract, empirical validation regex patterns, pipeline scope YAML parsing, and GDScript validation output parsing.

---

### S-04: Docs config page omits several presentation config keys

**Files**:
- `docs/user-guide/config.md` lines 142-148 (Presentation section)
- `delivery-team/skills/delivery-flow/references/config-schema.md` lines 83-99 (full presentation keys)

**Issue**: The docs Presentation section only lists 5 of the 16 presentation config keys. Missing: `save_to_artifacts`, `marp_theme`, `staleness_warning_days`, `vocabulary_overrides`, `pptx_template`, `pptx_font`, `pptx_accent_color`, `narrative.emphasis`, `narrative.cutting`, `narrative.framing`, `narrative.tension`, `thresholds`. While docs can be an abbreviated reference, omitting 11 of 16 keys means users cannot configure PPTX branding or narrative passes without reading the raw schema.

**Fix**: Add the missing presentation keys to the docs config reference, at minimum the PPTX branding keys added in v2.6 and the narrative keys from v2.4.

---

## Testability Assessment

### What CAN be tested structurally
- Config schema consistency (md vs json vs yaml template) -- automated comparison possible
- Artifact path consistency between SKILL.md and pipeline-stages.md -- grep-able
- Hook registration (hooks.json lists all hook scripts that exist)
- Memory index references (all files in the Stage Chunks and Topic Files tables exist on disk)
- Docs accuracy (stage counts, key counts, output paths match source)

### What CANNOT be tested structurally
- Whether collaboration patterns actually improve artifact quality
- Whether self-correction converges within the iteration limit
- Whether the two-channel rule is followed during live orchestration
- Whether alias personality injection works at each strength level
- Whether the SKILL_LOADED check actually improves skill loading reliability
- Whether empirical validation regex patterns have acceptable false positive/negative rates

---

## Rapid Iteration Risk Assessment (last 3 commits)

The `git diff --stat HEAD~3` shows 44 files changed with 3,490 insertions and 2,078 deletions. Key observations:

1. **Entire docs site added in one commit** (docs/*, mkdocs.yml) -- 20+ new files. High risk of copy-paste errors from source files. Confirmed: W-01 (wrong design output path), W-02 (missing config key), S-04 (incomplete presentation keys).

2. **SKILL.md modified** (+54/-54 lines) -- changes were targeted, but the inline stage definitions were NOT updated to match pipeline-stages.md, creating B-01.

3. **Config schema bumped to v2.6** -- 3 version bumps in one day (2.4, 2.5, 2.6). The schema generator did not handle the new map types correctly, creating B-02.

---

*Seventeen. Final count: seventeen defects. That bug still only counts as one.*
