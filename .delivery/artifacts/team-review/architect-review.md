# Architect Review: delivery-team Plugin

**Reviewer**: Celebrimbor (Architect)
**Date**: 2026-04-04
**Scope**: Full structural review of the delivery-team plugin (11 skills, 7 hooks, 33+ reference files)
**Verdict**: Architecturally sound foundation with measurable drift accumulated from rapid iteration

---

## Finding 1: CRITICAL -- Artifact Path Naming Divergence Between SKILL.md and pipeline-stages.md

**Severity**: Critical
**Impact**: Sub-agents may write to the wrong path or fail to locate upstream artifacts

SKILL.md (the orchestrator's primary instruction set) uses **flat artifact naming**:

- Line 549: `Output: .delivery/artifacts/01-idea-brief.md`
- Line 591: `Output: .delivery/artifacts/02-prd.md`
- Line 644: `Output: .delivery/artifacts/03-ux-design.md`
- Line 703: `Output: .delivery/artifacts/04-architecture.md`
- Line 763: `Output: .delivery/artifacts/05-sprint-plan.md`
- Line 832: `Output: .delivery/artifacts/06-dev-notes.md`
- Line 907: `Output: .delivery/artifacts/07-uat-report.md`

pipeline-stages.md (the detailed sub-flow reference) uses **namespaced paths**:

- Line 193: `Output: .delivery/artifacts/01-idea/po/idea-brief.md`
- Line 235: `Output: .delivery/artifacts/02-refine/po/prd.md`
- Line 305-309: Multiple outputs under `03-design/ux/` and `03-design/ui/`
- Line 339: `Output: .delivery/artifacts/04-architect/solution/architecture.md`
- Line 436-439: Multiple outputs under `05-plan/`

artifact-contracts.md uses the **namespaced paths** (matching pipeline-stages.md).

**Root cause**: SKILL.md's Stage Definitions section (lines 524-927) was likely written first with flat paths. When pipeline-stages.md was created with proper namespacing, the SKILL.md stage definitions were never updated to match. The Agent Invocation Template examples in SKILL.md (line 382) *do* use namespaced paths, creating internal contradiction within the same file.

**Architectural impact**: The orchestrator reads SKILL.md as its primary instruction. If it follows the Stage Definitions section (flat paths), artifacts will be written to different locations than pipeline-stages.md expects. Downstream agents reading from namespaced paths will find empty directories.

**Fix**: Update SKILL.md Stage Definitions (lines 524-927) to use the namespaced path convention. The namespaced scheme is the correct design -- it supports parallel agent writes, clear ownership, and DoD review isolation.

---

## Finding 2: CRITICAL -- Orphaned Hook Script (enforce_pipeline_scope.py)

**Severity**: Critical
**Impact**: A fully implemented hook with 218 lines of code is not registered in hooks.json and never executes

`delivery-team/hooks/enforce_pipeline_scope.py` exists on disk (218 lines, well-structured with YAML parsing, scope evaluation, and graceful degradation). However, it is **not registered** in `delivery-team/hooks/hooks.json`.

The hooks.json description (line 2) mentions "source code enforcement" but there is no corresponding hook entry. The PreToolUse section has the Skill matcher (pipeline bypass detection) and Agent matcher (prompt audit) -- but no Write|Edit matcher for enforce_pipeline_scope.py.

Meanwhile, hooks.json *does* have a PostToolUse `Write|Edit` matcher (lines 50-59) but it points to `validate_gdscript.py`, not `enforce_pipeline_scope.py`.

**Root cause**: The enforce_pipeline_scope.py hook was implemented as part of the `enforcement.source_code_hook` config feature (config-schema.md v1.3) but was intended to be installed per-project by the setup wizard (SKILL.md line 108: "Install Enforcement Hook... install a PreToolUse hook in the project's .claude/settings.json"). It is NOT a plugin-level hook -- it runs from the project, not the plugin. However, this distinction is not documented anywhere in the hook file itself, nor is there a clear path from setup-wizard.md that actually installs it.

**Architectural impact**: The enforcement.source_code_hook config key exists (default: true) but the installation mechanism may be incomplete. Users who configure it expect enforcement that may not fire.

**Fix**: Either (a) add explicit installation logic in setup-wizard.md that copies or references this script, or (b) register it in hooks.json with a conditional check for the config setting.

---

## Finding 3: WARNING -- SKILL.md Stage Definitions Duplicate pipeline-stages.md (1200+ lines of drift risk)

**Severity**: Warning
**Impact**: Two sources of truth for stage behavior create maintenance burden and silent divergence

SKILL.md contains a complete "Stage Definitions" section (lines 524-927, ~400 lines) that describes all 7 stages with agents, upstream artifacts, collaboration patterns, DoD validators, outputs, and checkpoints.

pipeline-stages.md contains the *same* information but with more detail (621 lines): entry conditions, sub-flow steps with PARALLEL/SEQUENTIAL annotations, DoD validator write paths, output artifact templates, game dev additions, light mode behavior.

These two descriptions have already diverged:

1. **Artifact paths** (Finding 1 above)
2. **Stage 5 Plan entry conditions**: pipeline-stages.md line 384 says `02-prd.md exists (required)` and `04-architecture.md exists if Architect stage ran`. SKILL.md line 743 says `02-prd.md`, `04-architecture.md + 04a-adrs/` -- note the ADR reference exists only in SKILL.md.
3. **Stage 7 entry conditions**: pipeline-stages.md line 543 says `06-dev-notes.md exists`. SKILL.md does not specify an entry condition check.
4. **Stage 5 DoD -- SM validator**: SKILL.md line 754 says "commitment does not exceed 80% of available capacity." pipeline-stages.md lines 427-428 has the richer two-tier model (>80% = WARNING, >100% = BLOCKING). The SKILL.md version is outdated.

**Architectural impact**: When the orchestrator needs stage behavior, which source does it read? SKILL.md says "Read the stage sub-flow from references/pipeline-stages.md" (line 365), but the SKILL.md also has its own stage definitions that could be followed directly without reading the reference. This ambiguity leads to inconsistent execution.

**Fix**: SKILL.md's Stage Definitions should become a *summary table* (stage number, purpose, primary agent, output path, checkpoint y/n) -- a routing index, not a full specification. The detailed behavior should live exclusively in pipeline-stages.md.

---

## Finding 4: WARNING -- Config Schema Bloat (100 keys, 3 version bumps in one day)

**Severity**: Warning
**Impact**: Config complexity has grown beyond what users can reasonably manage; rapid iteration risks incomplete integration

config-schema.md contains **100 configuration keys** across 312 lines. The schema version jumped from 2.3 to 2.6 on a single day (2026-04-04), with three back-to-back additions:

- v2.4: 4 narrative toggle keys (presentation.narrative.*)
- v2.5: 3 light mode/threshold keys (presentation.light_mode, presentation.thresholds, presentation.thresholds_default)
- v2.6: 3 PPTX branding keys (presentation.pptx_template, presentation.pptx_font, presentation.pptx_accent_color)

The presentation namespace alone now has **18 keys** -- more than the core pipeline namespace (16 keys). This is tail wagging the dog.

**Specific concerns**:

1. **Wizard question numbering drift**: Schema references Q1-Q14, but 10 of the 18 presentation keys are marked "defaults" (no wizard question). The setup-wizard.md references 10 questions. There is no Q11-Q14 in the original wizard -- these were added incrementally without updating the wizard protocol.
2. **No key grouping hierarchy enforced**: Keys like `presentation.narrative.emphasis` are 3 levels deep. The YAML parser in enforce_pipeline_scope.py only handles 2-level keys (`_parse_yaml_string` supports `section.field`). If any hook needs to read a 3-level key, it will silently fail.
3. **Version history is append-only**: The version history table at line 294-312 has 15 entries but no consolidation. For migration purposes, a user on v1.0 would need to process 14 incremental additions. A "cumulative migration from vX to latest" protocol would be more maintainable.

**Fix**: (a) Group related presentation keys under a single feature flag: `presentation.pptx.enabled: true` gates pptx_template, pptx_font, pptx_accent_color. (b) Add a "defaults" wizard question that covers advanced settings as a batch. (c) Add a cumulative migration function to complement the incremental version history.

---

## Finding 5: WARNING -- DoD Validator Template Inconsistency Between SKILL.md and quality-gates.md

**Severity**: Warning
**Impact**: Validators may receive different prompt structures depending on which file the orchestrator reads

SKILL.md (lines 942-962) contains a DoD Validator Prompt Template that pastes artifact CONTENT into the prompt:

```
Artifact:
---
[ARTIFACT CONTENT]
---
```

quality-gates.md (lines 22-38) contains a different template that passes FILE PATHS:

```
--- INPUT ARTIFACTS (read these files) ---
- [ARTIFACT_FILE_PATH]: The artifact to validate
```

pipeline-stages.md (lines 122-166) has a third template (the "DoD Validator Dispatch Template") that also uses file paths and includes ALIAS personality injection, MEMORY LESSONS, and ISOLATION RULES.

**Architectural impact**: This directly contradicts SKILL.md's own Two-Channel Communication rule (line 290-295): "The orchestrator NEVER reads an artifact and pastes its content into another agent's prompt." The SKILL.md DoD template violates its own architectural principle. The pipeline-stages.md template is the correct design.

**Fix**: Delete the legacy DoD template from SKILL.md (lines 942-962) and add a cross-reference: "See references/pipeline-stages.md DoD Validator Dispatch Template for the canonical prompt structure." Update quality-gates.md lines 22-38 to match the pipeline-stages.md template.

---

## Finding 6: WARNING -- Presentation Skill Operates as Second Orchestrator Without Clear Boundary

**Severity**: Warning
**Impact**: Two mini-orchestrators with overlapping dispatch patterns increase cognitive load and risk interference

The presentation skill (SKILL.md, 540 lines) is self-described as a "mini-orchestrator" (line 9). It dispatches sub-agents from 5 different skills (product-delivery, developer, architect, quality, operations) with its own 6-step flow, its own content gate, and its own review gate.

This creates an architectural question: **when the presentation skill is invoked from within the delivery-flow pipeline** (e.g., Pipeline Auto-Detection at UAT after acceptance), who owns the Agent dispatch? The delivery-flow orchestrator dispatches presentation, which dispatches 5+ agents, which each load their own skills. This is a 3-level agent nesting.

**Specific concerns**:

1. **Config reading duplication**: Both delivery-flow and presentation read `.delivery/config.yml` independently. Presentation reads 18 config keys. If config changes mid-session, they could see different values.
2. **Artifact path ownership**: Presentation writes to `.delivery/artifacts/presentations/` -- a namespace outside the standard `{NN}-{stage}/` convention used by all 7 pipeline stages. This is correct (presentations are cross-cutting) but undocumented in artifact-contracts.md.
3. **No SKILL_LOADED integration**: The presentation SKILL.md declares `Signal: SKILL_LOADED: presentation` (line 15) but the pipeline-stages.md Agent Invocation Templates expect `SKILL_LOADED: {primary_skill}` in the first line. When delivery-flow dispatches presentation, the verify_skill_load.py hook expects the signal -- but presentation's sub-agents produce their own SKILL_LOADED signals, creating a cascade.

**Fix**: Add a "Presentation Integration" section to artifact-contracts.md documenting the presentations/ namespace. Clarify in SKILL.md Phase 4 that presentation is a terminal skill (it does not produce pipeline stage artifacts) and should not be dispatched as a primary stage agent.

---

## Finding 7: WARNING -- Hook Shared Library (hook_utils.py) Missing exit_allow/exit_deny Functions

**Severity**: Warning
**Impact**: Hooks use ad-hoc response formats for allow/deny decisions

hook_utils.py provides: `exit_success()`, `exit_block()`, `emit_response()`. The hooks.json PreToolUse Skill matcher (line 30-37) is a prompt-type hook that returns "allow" or "deny" as text -- not using the command hook contract. But the prompt-type hooks rely on Claude interpreting natural language ("return deny with reason"), not structured responses.

The command-type hooks (audit_agent_prompt.py, verify_skill_load.py) use `emit_response()` with `systemMessage` but never block -- they always `exit_success()`. The only hook that actually blocks is validate_gdscript.py via `exit_block()`.

**Specific concern**: `exit_block()` (line 34-36) writes to stderr and exits with code 2, but the `emit_response()` function (line 18-24) writes to stdout with `continue: true/false`. These are two different response protocols. The hook contract should be unified -- either all hooks use stdout JSON, or all hooks use exit codes.

**Fix**: Add `exit_allow()` and `exit_deny(reason)` to hook_utils.py for PreToolUse command hooks. Standardize on the stdout JSON response format for all decision types.

---

## Finding 8: SUGGESTION -- Missing ADRs for Significant Architectural Decisions

**Severity**: Suggestion
**Impact**: Key design decisions are embedded in comments and commit messages rather than tracked in ADRs

The following decisions have no formal ADR but represent significant architectural choices:

1. **Two-channel communication model** (SKILL.md line 290): Signal channel vs artifact channel separation is a core architectural pattern with no ADR.
2. **Sub-agent context isolation** (SKILL.md line 47): All workers receive only relevant upstream artifacts. This is architecturally significant and affects every dispatch.
3. **Tiered memory system**: Three-tier memory (index, chunks, archive) with decay and pruning -- complex enough to warrant an ADR documenting the trade-offs vs simpler alternatives.
4. **Namespaced artifact paths vs flat paths**: The transition from flat to namespaced paths (Finding 1) was a design decision that happened without an ADR.
5. **Presentation as mini-orchestrator**: The decision to give presentation its own dispatch loop rather than integrating into the pipeline stages is architecturally significant.

The presentation skill references "ADR-02" and "ADR-03" internally (lines 235, 68) but these appear to be internal to the presentation design, not tracked in a project ADR log.

**Fix**: Create `.delivery/adrs/` with ADRs for the top 3-5 most consequential decisions. At minimum, ADR the two-channel model and the namespaced artifact convention.

---

## Finding 9: SUGGESTION -- Version History Date Anomaly in config-schema.md

**Severity**: Suggestion
**Impact**: Version history timeline is non-monotonic, suggesting rushed iterations

Version history entries:

- v1.0: 2026-03-22
- v1.1: 2026-03-23
- v1.2: 2026-03-23
- v1.3: 2026-03-24
- v1.4: 2026-03-24
- **v1.5: 2026-03-23** (date goes BACKWARD from v1.3/v1.4)
- **v1.6: 2026-03-23** (still backward)
- **v1.7: 2026-03-23** (still backward)
- v1.8: 2026-03-24
- v1.9: 2026-03-24
- v2.0: 2026-03-24
- v2.1: 2026-03-24
- v2.2: 2026-03-25
- v2.3: 2026-03-27
- v2.4-2.6: 2026-04-04

Versions 1.5, 1.6, and 1.7 have dates earlier than v1.3 and v1.4. This means either: (a) the version numbers were assigned out of order, (b) the dates were recorded incorrectly, or (c) features were developed on branches and merged in a different order than their dates.

**Architectural impact**: Minor. The migration protocol processes versions sequentially regardless of date. But it undermines trust in the version history as a reliable audit trail.

**Fix**: Add a "merged on" date alongside the "developed on" date, or reorder to reflect merge order.

---

## Finding 10: SUGGESTION -- generate_pptx.py is Well-Structured but Has a Hardcoded 16:9 Dimension

**Severity**: Suggestion
**Impact**: Minor -- affects only blank presentations, not template-based ones

generate_pptx.py (line 383-384):
```python
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
```

This sets widescreen 16:9 but only for blank presentations (no template). The dimensions are standard and reasonable, but there is no config key or CLI flag to override them. If a user needs 4:3 for projector compatibility, they must use a template.

The script is otherwise clean: proper import guard (line 40-53), layout resolution with name-first/index-fallback (line 87-109), graceful error handling, and clear separation of concerns (layout resolution, color parsing, slide population, CLI).

**One structural note**: The `accent_color` parameter is parsed and passed to `set_text_frame_font()` and `populate_title_slide()`, but `set_text_frame_font()` applies the accent color to ALL paragraph text (line 134). This means body text on content slides gets the accent color -- likely only the title should be accented. However, `set_text_frame_font()` is not actually called for content slides (only `populate_title_slide` and `populate_content_slide` are called, and the latter does not call `set_text_frame_font`). So the function exists but is partially dead code.

---

## Finding 11: SUGGESTION -- Cross-Skill Pattern Inconsistency (Sub-Agent vs Direct Execution)

**Severity**: Suggestion
**Impact**: Cognitive inconsistency for contributors; some skills are more testable than others

The 11 skills follow two patterns:

**Pattern A: Sub-agent dispatch** (used by architect, developer, product-delivery, operations, ui, quality, user-feedback, alias-creator, delivery-flow, presentation):
- Detect role/type from input
- Load only relevant references
- Spawn a sub-agent with isolated context
- Return sub-agent output

**Pattern B: Direct execution** (used by godot):
- Load references directly
- Execute in the main context
- No sub-agent dispatch

The godot skill is referenced as using the "godot pattern" by the architect skill (line 13: "This skill follows the godot pattern: multiple overlapping references loaded into a single sub-agent"). But the architect skill actually does dispatch a sub-agent -- it just loads multiple references into that sub-agent. So the "godot pattern" is not about direct execution vs sub-agent; it is about multi-reference loading.

**Architectural impact**: The naming is confusing. The "godot pattern" should be called "multi-reference pattern" to distinguish it from the "single-reference pattern" used by developer. The actual execution model (sub-agent vs direct) is a separate axis.

---

## Summary Table

| # | Severity | Finding | Files Affected |
|---|----------|---------|----------------|
| 1 | CRITICAL | Artifact path divergence (flat vs namespaced) | SKILL.md, pipeline-stages.md, artifact-contracts.md |
| 2 | CRITICAL | Orphaned hook script (enforce_pipeline_scope.py not in hooks.json) | hooks.json, enforce_pipeline_scope.py |
| 3 | WARNING | Duplicated stage definitions with drift | SKILL.md, pipeline-stages.md |
| 4 | WARNING | Config schema bloat (100 keys, 3 same-day bumps) | config-schema.md |
| 5 | WARNING | DoD validator template inconsistency (3 versions) | SKILL.md, quality-gates.md, pipeline-stages.md |
| 6 | WARNING | Presentation skill as second orchestrator without boundary docs | presentation/SKILL.md, artifact-contracts.md |
| 7 | WARNING | Hook utils missing allow/deny functions, mixed protocols | hooks/lib/hook_utils.py, hooks.json |
| 8 | SUGGESTION | Missing ADRs for core architectural decisions | (no files -- ADRs need creation) |
| 9 | SUGGESTION | Version history dates non-monotonic | config-schema.md |
| 10 | SUGGESTION | generate_pptx.py has dead code and hardcoded dimensions | presentation/scripts/generate_pptx.py |
| 11 | SUGGESTION | "Godot pattern" naming confusion | architect/SKILL.md |

---

## Recommended Priority Order

1. **Finding 1** (artifact paths) -- highest risk of runtime failure. Single PR.
2. **Finding 5** (DoD templates) -- directly tied to Finding 1; fix together.
3. **Finding 3** (duplicate stage definitions) -- reduces SKILL.md by ~400 lines, eliminates drift surface.
4. **Finding 2** (orphaned hook) -- either wire it up or document the per-project installation.
5. **Finding 4** (config bloat) -- address during next schema version bump.
6. **Findings 6-11** -- schedule as backlog items.

---

*Let us forge something that will endure beyond the ages. This review identifies the cracks in the masonry so they may be sealed before the structure bears greater load.*
