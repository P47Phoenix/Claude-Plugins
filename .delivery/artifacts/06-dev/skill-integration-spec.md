# SKILL.md Integration Specification: Rules Engine

**Version**: 1.0
**Date**: 2026-03-28
**Author**: Gimli (Developer)
**Status**: Implementation-Ready
**Traces To**: US-16 (SKILL.md Orchestrator Integration), US-17 (Setup Wizard Extension), US-18 (Dry-Run Preview), Architecture v1.0 Section 2.4

> *"And my code! You have my code."*

This document specifies the exact changes needed to wire the deterministic rules engine into `delivery-team/skills/delivery-flow/SKILL.md`. It does NOT contain the edits themselves -- those must be applied using `plugin-dev:skill-development`. Each change area includes the target location, what to add/replace, and the exact Bash invocation templates the orchestrator will use.

---

## Conventions Used in This Document

- `SCRIPTS_DIR` = `delivery-team/scripts/` (relative to plugin root)
- `RULES_DIR` = `delivery-team/skills/delivery-flow/references/rules/` (relative to plugin root)
- `$PLUGIN_ROOT` = the absolute path to the delivery-team plugin directory (resolved at runtime via `${CLAUDE_PLUGIN_ROOT}`)
- All `evaluate_rules.py` invocations use the Bash tool
- All context files are written to `.delivery/tmp/` (orchestrator creates this directory if missing)
- Pipeline ID format: `pipe_YYYYMMDD_HHMMSS` (set during Phase 0, reused throughout)

---

## Change Area 1: Phase 0 -- Rules Validation on Config Load

### Location in SKILL.md

Insert a new subsection after the existing "Config Settings Applied to Pipeline" table (currently around line 148) and before Phase 1. Title it: **"Rules Engine Initialization"**.

### What to Add

After the config is loaded and settings are applied, the orchestrator must validate that the rules engine is operational before the pipeline proceeds. This is a pre-flight check, not a routing decision.

#### Step 0a: Feature Flag Check

Read the `rules.enabled` key from the loaded config. Three cases:

| Config State | Action |
|-------------|--------|
| `rules.enabled: true` (or key absent -- default is enabled) | Proceed to Step 0b |
| `rules.enabled: false` | Log: `> Rules engine bypassed (rules.enabled: false). Pipeline will use prose-based routing.` Skip all rules engine invocations for this run. Set internal flag `RULES_ACTIVE = false`. |
| `rules` section missing entirely | Treat as enabled with defaults. Proceed to Step 0b. |

When `RULES_ACTIVE` is false, all subsequent rules engine invocations in Phases 3, 4, and post-pipeline are skipped. The pipeline falls back to the existing prose-based Stage Routing Matrix and AI-judged DoD gates. This is the backward-compatibility path.

#### Step 0b: Dry-Run Validation

If `RULES_ACTIVE` is true, validate that the rules resolve correctly before the pipeline starts:

1. Write a minimal context JSON to `.delivery/tmp/validation-context.json`:

```json
{
  "project": {
    "type": "<detected_or_configured_project_type>",
    "risk_tolerance": "<from_config_or_default_standard>"
  },
  "config": {
    "preset": "<from_config_or_default_standard>",
    "strict_mode": "<from_config_or_default_false>"
  }
}
```

2. Invoke the rules engine in dry-run mode:

```bash
python "$PLUGIN_ROOT/scripts/evaluate_rules.py" \
  --action resolve \
  --context .delivery/tmp/validation-context.json \
  --rules-dir "$PLUGIN_ROOT/skills/delivery-flow/references/rules/" \
  --preset "<preset_from_config>" \
  --dry-run
```

3. Parse the result:

| Exit Code | Action |
|-----------|--------|
| 0 | Rules validated. Log: `> Rules engine validated (preset: <preset>, <N> rules resolved).` Proceed. |
| 1 | Argument/config error. Log the error from stderr. If `rules.strict_mode: true`: HALT pipeline, present error to user. If strict_mode is false: warn and fall back to prose-based routing (`RULES_ACTIVE = false`). |
| 2 | Rule evaluation error. Same handling as exit code 1. |

4. If dry-run succeeds, extract and cache the resolved routing map from stdout for use in Phase 3. This avoids a redundant invocation.

#### Config Overrides Extraction

The orchestrator must extract the `rules` section from `.delivery/config.yml` and write it as JSON to `.delivery/tmp/config-overrides.json` for the CLI script (which cannot parse YAML directly). This file is reused across all rules engine invocations in the run.

```
Read .delivery/config.yml
Extract the "rules:" section as a Python dict
Write as JSON to .delivery/tmp/config-overrides.json
```

This extraction happens once during Phase 0 config load, not per-invocation.

---

## Change Area 2: Phase 3 -- Stage Routing via Rules Engine

### Location in SKILL.md

Replace the existing **"Phase 3: Stage Routing"** section (currently lines ~236-259), specifically the Stage Routing Matrix table and the Depth Definitions. The section header and introductory text remain.

### What to Replace

Remove the hardcoded Stage Routing Matrix table (the `| Stage | GREENFIELD | FEATURE | ...` table) and the three Depth Definitions bullet points (Full, Light, Skip).

### What to Add

#### Rules-Based Stage Routing Protocol

When `RULES_ACTIVE` is true, stage routing is determined by the rules engine, not the prose matrix.

**Step 3a: Assemble Routing Context**

Write the routing context to `.delivery/tmp/routing-context.json`:

```json
{
  "project": {
    "type": "<PROJECT_TYPE>",
    "risk_tolerance": "<low|standard|high>",
    "tech_stack": "<from_config>",
    "has_existing_codebase": true,
    "languages": ["python"],
    "frameworks": []
  },
  "config": {
    "preset": "<solo|standard|strict>",
    "strict_mode": false,
    "pipeline": {
      "checkpoints": { ... },
      "collaboration_patterns": { ... },
      "max_self_correction": 3
    }
  },
  "run": {
    "pipeline_id": "<pipe_YYYYMMDD_HHMMSS>",
    "is_resume": false,
    "stages_completed": []
  }
}
```

**Step 3b: Invoke Rules Engine**

If the Phase 0 dry-run already resolved routing and the context has not changed (no resume with different completed stages), use the cached result from Step 0b. Otherwise invoke:

```bash
python "$PLUGIN_ROOT/scripts/evaluate_rules.py" \
  --action route \
  --context .delivery/tmp/routing-context.json \
  --rules-dir "$PLUGIN_ROOT/skills/delivery-flow/references/rules/" \
  --preset "<preset>" \
  --config-overrides .delivery/tmp/config-overrides.json
```

**Step 3c: Parse Routing Decision**

The stdout JSON contains:

```json
{
  "decision_type": "routing",
  "routing": {
    "idea": "full|light",
    "refine": "full|light",
    "design": "full|light",
    "architect": "full|light",
    "plan": "full|light",
    "development": "full|light",
    "uat": "full|light"
  },
  "collaboration_patterns": {
    "<stage>": ["<pattern1>", "<pattern2>"]
  },
  "preset": "<active_preset>",
  "resolution_layers": {
    "<stage>": 1|2|3|4
  },
  "determinism_category": "a|b"
}
```

Extract and store:
- `routing` -- the depth map. Use this instead of the hardcoded matrix for all subsequent stage execution.
- `collaboration_patterns` -- use these instead of the patterns defined in the stage definition. If a stage has no entry, no collaboration patterns run for that stage.
- `resolution_layers` -- log this in the stage summary for traceability.

**Step 3d: Announce Routing**

Announce the routing decision the same way as today, but sourced from the rules engine:

```
> Project Type: <TYPE> | Preset: <preset> | Stages: <list with depths> | Checkpoints: <N>
> Routing source: rules engine (determinism: <category>, layers: <summary>)
```

#### Depth Definitions (Unchanged Semantics)

The depth definitions (Full, Light) retain their existing semantics. The rules engine determines WHICH depth applies per stage; the definitions of what Full and Light MEAN are unchanged:

- **Full**: All agents invoked, all collaboration patterns from the routing decision run, full quality gate, full team DoD validation, max self-correction iterations from config.
- **Light**: Primary agent only, blocking criteria only, reduced DoD (primary + 1 reviewer), reduced max iterations. No adversarial review or debate unless the routing decision explicitly includes them.

**Important**: "Light" means reduced depth, NOT skipped. Light stages MUST execute. The rules engine will never return "skip" -- stages that the old matrix marked as "skip" will be routed as "light" with minimal scope by the rules engine.

#### Fallback (RULES_ACTIVE = false)

When `RULES_ACTIVE` is false, the existing Stage Routing Matrix table (preserved in `references/legacy-routing-matrix.md`) and Depth Definitions apply unchanged. This is the backward-compatibility path for users who set `rules.enabled: false`.

Move the current Stage Routing Matrix table content to `references/legacy-routing-matrix.md` so it remains accessible but does not clutter the primary SKILL.md flow.

---

## Change Area 3: Phase 4 -- Pipeline Execution Changes

### Location in SKILL.md

Modify three steps within Phase 4 (currently lines ~300-453): Step 4 (Invoke Primary Agent), Step 6 (Run Collaboration Patterns), and Step 7 (Team DoD Validation).

### Step 4 Changes: Rules-Resolved Validators and Patterns

**Current behavior**: Step 4 constructs the Agent Invocation Template using agent roles and task types from the stage definition in `references/pipeline-stages.md`.

**New behavior**: When `RULES_ACTIVE` is true, the orchestrator augments the stage definition with rules-resolved data:

1. The **validators** for this stage come from the routing decision's gate rules (resolved during Phase 3 or from the gate rule definitions). Read the required validators for this stage from the resolved rules:

```bash
python "$PLUGIN_ROOT/scripts/evaluate_rules.py" \
  --action resolve \
  --context .delivery/tmp/routing-context.json \
  --rules-dir "$PLUGIN_ROOT/skills/delivery-flow/references/rules/" \
  --preset "<preset>" \
  --config-overrides .delivery/tmp/config-overrides.json \
  --dry-run
```

From the resolved output, extract `gates.<stage>_dod.required_validators` to know which validator roles must be invoked for this stage's DoD.

2. The **collaboration patterns** for this stage come from `collaboration_patterns.<stage>` in the routing decision (already cached from Phase 3).

3. Pass these to the Agent Invocation Template as before, but sourced from rules rather than hardcoded stage definitions.

**Fallback**: When `RULES_ACTIVE` is false, use the stage definitions from `references/pipeline-stages.md` unchanged.

### Step 6 Changes: Collaboration Patterns from Routing Decision

**Current behavior**: Step 6 runs collaboration patterns "designated for this stage" per the stage definition.

**New behavior**: When `RULES_ACTIVE` is true, run ONLY the patterns listed in `collaboration_patterns.<stage>` from the Phase 3 routing decision. The execution order remains the same (Evaluator-Optimizer, Adversarial Review, Debate, Review Board, Consensus). If the routing decision lists no patterns for a stage, skip Step 6 entirely for that stage.

### Step 7 Changes: Rules-Based DoD Gate Evaluation

**Current behavior**: Step 7 collects validator signals and uses AI judgment ("ALL validators must return STATUS: DONE") to determine pass/fail.

**New behavior**: When `RULES_ACTIVE` is true, after collecting all validator signals, invoke the rules engine for the gate decision instead of applying AI judgment.

**Step 7a: Assemble Gate Context**

After all validators have returned their signals, write gate context to `.delivery/tmp/gate-<stage>.json`:

```json
{
  "stage": {
    "name": "<stage_name>",
    "depth": "<full|light>",
    "iteration": 1,
    "max_iterations": 3,
    "validators": {
      "<role>": {
        "status": "DONE|NOT_DONE",
        "findings_path": ".delivery/artifacts/<NN>-<stage>/dod/<role>-review.md",
        "has_blocking_findings": false,
        "finding_count": 0
      }
    },
    "artifacts": {
      "primary": ".delivery/artifacts/<NN>-<stage>/<namespace>/<artifact>.md",
      "supporting": []
    }
  },
  "project": { "type": "<TYPE>", "risk_tolerance": "<level>" },
  "config": { "preset": "<preset>", "strict_mode": false },
  "run": {
    "pipeline_id": "<id>",
    "dod_round": 1,
    "correction_count": 0
  }
}
```

**Step 7b: Invoke Gate Evaluation**

```bash
python "$PLUGIN_ROOT/scripts/evaluate_rules.py" \
  --action gate \
  --context .delivery/tmp/gate-<stage>.json \
  --rules-dir "$PLUGIN_ROOT/skills/delivery-flow/references/rules/" \
  --preset "<preset>" \
  --config-overrides .delivery/tmp/config-overrides.json \
  --pipeline-id "<pipeline_id>"
```

**Step 7c: Parse Gate Decision**

The stdout JSON contains:

```json
{
  "decision_type": "gate",
  "gate_id": "<stage>_dod",
  "decision": "GO|RECYCLE|HOLD|ESCALATE|HALTED",
  "overall_score": 87.5,
  "passed": true,
  "pass_threshold": 80,
  "rule_results": [ ... ],
  "reason": "...",
  "recommendations": [],
  "determinism_category": "a|b"
}
```

Act on the decision:

| Decision | Action |
|----------|--------|
| `GO` | Stage passes. Proceed to Step 8 (Verify Artifact). |
| `RECYCLE` | Stage fails. Route feedback to primary agent for revision (existing self-correction loop). Increment `dod_round` in context. Re-evaluate after revision. |
| `HOLD` | Marginal pass. Log recommendations. Present to user: "Gate scored <score>/<threshold>. Recommendations: <list>. Proceed or revise?" |
| `ESCALATE` | Trigger dynamic escalation to user with full rule_results and reason. |
| `HALTED` | Fatal rule evaluation error in strict mode. Pipeline halts. Present error to user. |

**Step 7d: Self-Correction with Gate Re-evaluation**

When the decision is `RECYCLE`:
1. Pass NOT_DONE findings to the primary agent (existing self-correction protocol).
2. After agent revision, re-collect validator signals.
3. Re-invoke the gate evaluation (Step 7b) with updated context (incremented `dod_round`).
4. Max iterations from config (`pipeline.max_dod_rounds`, default 3).
5. If max iterations reached and still RECYCLE: escalate to user.

**Fallback**: When `RULES_ACTIVE` is false, use the existing protocol (ALL validators must return STATUS: DONE).

---

## Change Area 4: Error Handling Protocol

### Location in SKILL.md

Add a new section after Phase 4 and before the Retrospective section. Title it: **"Rules Engine Error Handling"**.

### What to Add

#### Error Categories

| Exit Code | Category | Description |
|-----------|----------|-------------|
| 0 | Success | Decision JSON on stdout. Proceed normally. |
| 1 | Config/Argument Error | Missing files, invalid arguments, malformed JSON. Error JSON on stderr. |
| 2 | Rule Evaluation Error | Condition evaluation failure, type validation failure, missing required fields. Error JSON on stderr. |

#### Error Handling by Mode

**Strict Mode** (`rules.strict_mode: true`):

Any non-zero exit code from `evaluate_rules.py` HALTS the pipeline immediately. The orchestrator:
1. Reads the error JSON from stderr.
2. Logs: `> PIPELINE HALTED: Rules engine error at <decision_point>. Error: <message>`
3. Presents the full error to the user.
4. Does NOT fall back to prose-based routing. In strict mode, a rules failure is a pipeline failure.

**Default Mode** (`rules.strict_mode: false` or absent):

Any non-zero exit code triggers a 3-option prompt to the user:

```
> Rules engine error at <decision_point>: <error_message>
>
> Options:
> 1. **Retry** -- Re-invoke the rules engine (useful if the error was transient or context was malformed)
> 2. **Fallback** -- Use prose-based routing/AI-judged gate for this decision point only (rules engine continues for subsequent decisions)
> 3. **Halt** -- Stop the pipeline and investigate
```

After each fallback, log: `> FALLBACK: <decision_point> used prose-based evaluation. Reason: <error_message>`. Include this in the audit trail (Change Area 5) and in the retrospective.

#### Timeout Handling

If `evaluate_rules.py` does not produce output within 30 seconds (configurable via `rules.timeout_seconds` in config), treat it as exit code 2 with message "Evaluation timed out after <N> seconds". Apply the same strict/default mode handling.

---

## Change Area 5: Audit Trail Integration

### Location in SKILL.md

Add a subsection within the existing Phase 4 Step 7 area (after the gate evaluation) AND in the post-pipeline section (Retrospective). Two insertion points.

### What to Add

#### Insertion 1: Per-Invocation Audit (within Phase 4 flow)

The `evaluate_rules.py` script automatically appends audit entries to `.delivery/audit/audit-<pipeline_id>.jsonl` on every non-dry-run invocation. The orchestrator does not need to write audit entries itself. However, it must:

1. Ensure `.delivery/audit/` directory exists before the first rules invocation (create in Phase 0 if missing).
2. Pass `--pipeline-id <pipeline_id>` to every non-dry-run invocation so the script can name the audit file correctly.
3. After each invocation, note the audit status in the stage summary: "Rules evaluation logged to audit trail (decision: <decision>, determinism: <category>)."

When `RULES_ACTIVE` is false and a fallback decision is made (Change Area 4), the orchestrator writes a manual audit entry:

```json
{
  "timestamp": "<ISO8601>",
  "pipeline_id": "<id>",
  "stage": "<stage>",
  "decision_type": "<routing|gate|escalation>",
  "decision": "FALLBACK",
  "reason": "Rules engine bypassed: <reason>",
  "determinism_category": "c",
  "resolution_layer": 0
}
```

Write this entry by appending to `.delivery/audit/audit-<pipeline_id>.jsonl` via the Bash tool:

```bash
echo '<json_line>' >> .delivery/audit/audit-<pipeline_id>.jsonl
```

#### Insertion 2: Retrospective Audit Summary (post-pipeline)

In the existing Retrospective section, after the pipeline completes (or aborts), add:

1. Invoke the audit summary command:

```bash
python "$PLUGIN_ROOT/scripts/evaluate_rules.py" \
  --audit-summary .delivery/audit/audit-<pipeline_id>.jsonl
```

2. Include the summary output in the retrospective under a new heading: **"Rules Engine Audit Summary"**. The summary includes:
   - Total evaluations
   - Breakdown by decision type (routing, gate, escalation)
   - Determinism category distribution (a/b/c counts)
   - Decision distribution (GO/RECYCLE/HOLD/ESCALATE/FALLBACK counts)
   - Pass rate
   - Layer usage (how many decisions came from each resolution layer)
   - Any fallback events with reasons

3. If any category "c" decisions exist (fallback), flag them: `> WARNING: <N> decisions used AI fallback instead of rules engine. See audit log for details.`

---

## Change Area 6: Dry-Run User Command

### Location in SKILL.md

Add to the existing "User Commands" section (or create one if it does not exist, near the end of SKILL.md alongside `setup`, `status`, and other user-facing commands).

### What to Add

#### `dry-run` Command

When the user says "dry-run", "preview rules", "show routing", or "what would the rules decide":

1. Assemble the routing context from the current config (same as Phase 3 Step 3a).
2. Invoke:

```bash
python "$PLUGIN_ROOT/scripts/evaluate_rules.py" \
  --action resolve \
  --context .delivery/tmp/routing-context.json \
  --rules-dir "$PLUGIN_ROOT/skills/delivery-flow/references/rules/" \
  --preset "<preset>" \
  --config-overrides .delivery/tmp/config-overrides.json \
  --dry-run
```

3. Present the output to the user in a readable format:

```
> Dry-Run Preview (preset: <preset>)
>
> Stage Routing:
>   Idea:         <depth> (layer <N>)
>   Refine:       <depth> (layer <N>)
>   Design:       <depth> (layer <N>)
>   Architect:    <depth> (layer <N>)
>   Plan:         <depth> (layer <N>)
>   Development:  <depth> (layer <N>)
>   UAT:          <depth> (layer <N>)
>
> Collaboration Patterns:
>   <stage>: <pattern1>, <pattern2>
>
> Gate Thresholds:
>   <stage>: <threshold>
>
> Determinism: <category>
> Active stages: <count>
```

4. If the user adds "compare" or says "compare with defaults":

```bash
python "$PLUGIN_ROOT/scripts/evaluate_rules.py" \
  --action resolve \
  --context .delivery/tmp/routing-context.json \
  --rules-dir "$PLUGIN_ROOT/skills/delivery-flow/references/rules/" \
  --preset "<preset>" \
  --config-overrides .delivery/tmp/config-overrides.json \
  --dry-run \
  --compare
```

Present the comparison output showing default vs. overridden values, highlighting differences.

---

## Summary of SKILL.md Edit Points

| # | Phase | Section | Action | Lines (approx.) |
|---|-------|---------|--------|-----------------|
| 1 | Phase 0 | After "Config Settings Applied to Pipeline" | INSERT new "Rules Engine Initialization" subsection | ~148 |
| 2 | Phase 3 | "Stage Routing Matrix" table + "Depth Definitions" | REPLACE with rules-based routing protocol | ~240-259 |
| 3 | Phase 4, Step 4 | "Invoke Primary Agent" | AUGMENT with rules-resolved validators/patterns | ~325 |
| 4 | Phase 4, Step 6 | "Run Collaboration Patterns" | AUGMENT with routing-decision-sourced patterns | ~375 |
| 5 | Phase 4, Step 7 | "Team DoD Validation" | REPLACE AI-judged gate with rules-based gate invocation | ~389-414 |
| 6 | New section | After Phase 4, before Retrospective | INSERT "Rules Engine Error Handling" | New |
| 7 | Retrospective | Post-pipeline section | INSERT audit summary invocation | Existing retro section |
| 8 | User Commands | End of SKILL.md | INSERT `dry-run` command | End |

## Implementation Notes

1. All Bash invocations must use `$PLUGIN_ROOT` (resolved from `${CLAUDE_PLUGIN_ROOT}`) so the paths work regardless of where the plugin is installed.
2. The `.delivery/tmp/` directory is ephemeral per-run. The orchestrator creates it in Phase 0 and can clean it up in the retrospective.
3. Context JSON files are the orchestrator's responsibility to assemble. The rules engine reads them but never writes them.
4. The `--pipeline-id` flag must be passed to all non-dry-run invocations for audit trail file naming.
5. When `RULES_ACTIVE` is false, every rules-related step in this spec is skipped. The pipeline behaves exactly as it does today. This is the zero-regression guarantee.
6. The `references/legacy-routing-matrix.md` file preserves the current prose-based routing table for fallback use and for users who disable the rules engine.

## Acceptance Criteria Traceability

| US | AC | Covered By |
|----|-----|-----------|
| US-16 AC-1 | Routing via rules engine | Change Area 2 (Phase 3 protocol) |
| US-16 AC-2 | DoD gate via rules engine | Change Area 3 (Step 7) |
| US-16 AC-3 | Escalation via rules engine | Change Area 3 (Step 7c ESCALATE decision) |
| US-16 AC-4 | No inline flow-control decisions | Change Areas 2+3 replace all inline decisions |
| US-16 AC-5 | Error handling protocol | Change Area 4 |
| US-17 | Setup wizard extension | Not in this spec (separate wizard-extension.md) |
| US-18 AC-1 | Dry-run preview | Change Area 6 |
| US-18 AC-2 | Faithful preview | Change Area 1 Step 0b (same engine, same rules) |
| US-18 AC-3 | Compare mode | Change Area 6 (compare flag) |
| US-15 AC-1 | Audit entries written | Change Area 5 (per-invocation audit) |
| US-15 AC-4 | Audit summary | Change Area 5 (retrospective integration) |
| US-15 AC-5 | Dry-run no audit write | Change Areas 1 and 6 (--dry-run flag) |
