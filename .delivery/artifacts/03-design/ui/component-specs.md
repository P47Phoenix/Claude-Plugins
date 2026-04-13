# CLI Component Specifications: Hardware Delivery Team Plugin

**Version**: 1.0
**Date**: 2026-04-12
**Author**: UI Designer (Arwen)
**Source**: `.delivery/artifacts/03-design/ux/wireframes.md` v1.0
**Project Type**: GREENFIELD
**Role**: UI Designer | Task: component-spec | References: design-systems.md, ui-patterns.md

---

> *"I choose a mortal design -- and I will make it timeless."*

---

## Table of Contents

1. [Design Token Foundation](#design-token-foundation)
2. [Component 1: Stage Header](#component-1-stage-header)
3. [Component 2: Agent Status](#component-2-agent-status)
4. [Component 3: Gate Result](#component-3-gate-result)
5. [Component 4: Checkpoint Summary](#component-4-checkpoint-summary)
6. [Component 5: Escalation](#component-5-escalation)
7. [Component 6: Progress Table](#component-6-progress-table)
8. [Component 7: Config Display](#component-7-config-display)
9. [Component 8: Error/Warning](#component-8-errorwarning)
10. [Component 9: Artifact Reference](#component-9-artifact-reference)
11. [Component 10: Rework Notification](#component-10-rework-notification)
12. [Component 11: kicad-happy Integration](#component-11-kicad-happy-integration)
13. [Theme Injection Architecture](#theme-injection-architecture)
14. [Design Rationale](#design-rationale)

---

## Design Token Foundation

These tokens are the atoms upon which every component is built. They originate from the wireframe design tokens and are formalized here as the component system's shared vocabulary.

### Box Drawing Tokens

| Token | Character | Unicode |
|-------|-----------|---------|
| `BOX_TL` | `+` | U+002B |
| `BOX_TR` | `+` | U+002B |
| `BOX_BL` | `+` | U+002B |
| `BOX_BR` | `+` | U+002B |
| `BOX_H` | `-` | U+002D |
| `BOX_V` | `|` | U+007C |
| `BANNER_CHAR` | `=` | U+003D |

### Layout Tokens

| Token | Value | Purpose |
|-------|-------|---------|
| `WIDTH_OUTER` | 60 | Total output width including borders |
| `WIDTH_INNER` | 56 | Content area (outer minus borders and padding) |
| `PADDING_LEFT` | 1 | Single space after left border |
| `PADDING_RIGHT` | 1 | Single space before right border |
| `BANNER_WIDTH` | 60 | Full-width `=` banner for stage announcements |
| `BANNER_INDENT` | 2 | Spaces before banner content |

### Severity Tokens

| Token | Display | Blocks Pipeline |
|-------|---------|-----------------|
| `SEV_DONE` | `[DONE]` | No (pass) |
| `SEV_NOT_DONE` | `[NOT_DONE]` | Yes |
| `SEV_CRITICAL` | `[CRITICAL]` | Yes |
| `SEV_MAJOR` | `[MAJOR]` | Yes |
| `SEV_MINOR` | `[MINOR]` | No |
| `SEV_WARNING` | `[WARNING]` | No |
| `SEV_ERROR` | `[ERROR]` | Yes |
| `SEV_INFO` | `[INFO]` | No |

### Status Tokens

| Token | Display | Meaning |
|-------|---------|---------|
| `STATUS_PASS` | `PASS` | Gate passed |
| `STATUS_NOT_DONE` | `NOT_DONE` | Gate failed |
| `STATUS_PAUSED` | `PAUSED` | Awaiting human input |
| `STATUS_REWORK` | `REWORK` | Returned to earlier stage |
| `STATUS_COMPLETE` | `COMPLETE` | Pipeline finished |
| `STATUS_ABORTED` | `ABORTED` | Pipeline terminated |

### Progress Indicator Tokens

| Token | Display | Meaning |
|-------|---------|---------|
| `PROG_DISPATCH` | `[>]` | Agent dispatched / starting |
| `PROG_WORKING` | `[~]` | In-progress activity |
| `PROG_COMPLETE` | `[+]` | Agent completed |

### Theme Token Map (Injection Points)

Every component references theme-replaceable tokens by key. The neutral value is the default; alias themes substitute via the mapping table below.

| Token Key | Neutral Value | LOTR Value |
|-----------|---------------|------------|
| `PIPELINE_TITLE` | `HARDWARE PIPELINE` | `THE FELLOWSHIP OF THE BOARD` |
| `STAGE_PREFIX` | `STAGE {n}:` | `CHAPTER {n}:` |
| `GATE_PREFIX` | `GATE:` | `THE COUNCIL OF:` |
| `RESULT_PASS` | `PASS` | `THE PATH IS CLEAR` |
| `RESULT_FAIL` | `NOT_DONE` | `THE WAY IS SHUT` |
| `REWORK_TITLE` | `REWORK TRIGGERED` | `A SHADOW RETURNS` |
| `PAUSED_TITLE` | `PIPELINE PAUSED` | `THE FELLOWSHIP RESTS` |
| `COMPLETE_TITLE` | `PIPELINE COMPLETE` | `THE QUEST IS FULFILLED` |
| `HUMAN_ACTION` | `HUMAN ACTION REQUIRED` | `A TASK FOR MORTAL HANDS` |
| `ADVANCE_VERB` | `Advancing to` | `The fellowship journeys to` |
| `RETURN_VERB` | `Returning to` | `The fellowship retreats to` |
| `DRB_TITLE` | `DESIGN REVIEW BOARD` | `THE WHITE COUNCIL` |
| `REWORK_LIMIT` | `REWORK LIMIT REACHED` | `THE DOOM OF THE NOLDOR` |
| `RESUME_TITLE` | `RESUMING PIPELINE` | `THE QUEST RESUMES` |

---

## Component 1: Stage Header

This component shall endure. I have placed every element with the care of one who has centuries to consider alignment and spacing.

### Purpose

Announces pipeline stage transitions. Two variants exist: AI-execution stages (full-width `=` banner) and human-execution stages (same banner, different mode indicator).

### Template

#### Variant A: AI-Execution Stage Banner

```
============================================================
  {{STAGE_PREFIX}} {{stage_name}} [AI-execution]
  Roles: {{primary_role}} (primary){{optional_secondary}}
  Activities: {{activity_list}}
  {{kicad_skills_label}}: {{kicad_skill_list}}
============================================================
```

#### Variant B: Human-Execution Stage Banner

```
============================================================
  {{STAGE_PREFIX}} {{stage_name}} [Human-execution]
  Mode: gate-in / human-action / gate-out
  Roles: {{primary_role}} (primary){{optional_secondary}}
============================================================
```

#### Variant C: Pre-Flight Summary

```
+------------------------------------------------------------+
| {{PIPELINE_TITLE}}: {{project_name}}                       |
| Config: {{config_path}} ({{schema_version}})               |
| Fab: {{fab_house}} | Regions: {{regions}} | Budget: {{bud}}|
| kicad-happy: {{available}}/{{total}} skills available      |
| Memory: {{lesson_count}} lessons loaded                    |
|                                                            |
| Stages: {{stage_sequence}}                                 |
+------------------------------------------------------------+
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `STAGE_PREFIX` | Yes | theme-token | Stage label (e.g., "STAGE 2:" or "CHAPTER 2:") |
| `stage_name` | Yes | string | Stage name in UPPERCASE (e.g., "SCHEMATIC") |
| `primary_role` | Yes | string | Primary role for the stage |
| `optional_secondary` | No | string | Format: `, {role} ({qualifier})`. Omit if none. |
| `activity_list` | Yes | string | Comma-separated activities; wrap at 56 chars with indent |
| `kicad_skills_label` | Yes | theme-token | "kicad-happy" (neutral) or "Allies summoned" (themed) |
| `kicad_skill_list` | Yes | string | Comma-separated skill names invoked in this stage |
| `PIPELINE_TITLE` | Yes | theme-token | Pipeline title |
| `project_name` | Yes | string | From config |
| `config_path` | Yes | string | File path to config |
| `schema_version` | Yes | string | Config schema version |
| `fab_house` | Yes | string | Target fabrication house |
| `regions` | Yes | string | Compliance regions, comma-separated |
| `bud` | Yes | string | Budget formatted as `$X.XX` |
| `available` / `total` | Yes | integer | kicad-happy skill availability counts |
| `lesson_count` | Yes | integer | Memory lessons loaded |
| `stage_sequence` | Yes | string | Stage names separated by ` > `, wrapped at inner width |

### Theme Injection Points

1. `STAGE_PREFIX` -- replaced per theme token map
2. `PIPELINE_TITLE` -- replaced per theme token map (pre-flight variant)
3. `kicad_skills_label` -- "kicad-happy" (neutral) vs. "Allies summoned" (themed)
4. Stage names in pre-flight sequence may have themed aliases appended in parentheses
5. Banner content tone (e.g., "Roles" vs. "Companions", "Activities" vs. "Deeds")

### States

| State | Behavior |
|-------|----------|
| Default | Renders with all required fields populated |
| No kicad skills | `kicad_skill_list` shows "none available" |
| Rework re-entry | Append `(rework)` after stage name |
| No memory | `lesson_count` shows 0 |

### Example: Neutral Theme

```
============================================================
  STAGE 2: SCHEMATIC [AI-execution]
  Roles: Electrical Engineer (primary), HW PO (trade-offs)
  Activities: schematic review, component selection,
              SPICE simulation, firmware interface docs
  kicad-happy: kicad, spice, digikey, mouser, lcsc, element14
============================================================
```

### Example: LOTR Theme

```
============================================================
  CHAPTER 2: THE COUNCIL OF RIVENDELL [AI-execution]
  (Schematic)
  Companions: Electrical Engineer (primary),
              HW Product Owner (counsel)
  Deeds: schematic review, component selection,
         SPICE simulation, firmware interface docs
  Allies summoned: kicad, spice, digikey, mouser, lcsc,
                   element14
============================================================
```

---

## Component 2: Agent Status

### Purpose

Shows the lifecycle of sub-agent dispatch, execution, and completion. Three variants cover the full agent lifecycle.

### Template

#### Variant A: Single Agent Dispatch

```
  [>] {{dispatch_verb}}: {{agent_role}}
      {{context_label}}: {{stage_name}} stage, rework={{rework_flag}}
      {{skills_label}}: {{skill_list}}
```

#### Variant B: Multi-Agent Dispatch (Design Review Board)

```
  [>] {{dispatch_verb}}: {{DRB_TITLE}} ({{gate_context}})
      {{reviewers_label}}:
        [>] {{reviewer_role_1}} -- {{reviewer_focus_1}}
        [>] {{reviewer_role_2}} -- {{reviewer_focus_2}}
        ...
      Mode: {{review_mode}}
```

#### Variant C: Agent Completion

```
  [+] {{complete_verb}}: {{agent_role}} ({{artifact_label}}: {{count}})
```

#### Variant D: In-Progress Activity

```
  [~] {{activity_description}}
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `dispatch_verb` | Yes | theme-token | "Dispatching" (neutral) or "Summoning" (themed) |
| `agent_role` | Yes | string | Role name (e.g., "Electrical Engineer") |
| `context_label` | Yes | theme-token | "Context" (neutral) or "Quest" (themed) |
| `stage_name` | Yes | string | Current stage name |
| `rework_flag` | Yes | boolean | `true` or `false` |
| `skills_label` | Yes | theme-token | "Skills" (neutral) or "Allies" (themed) |
| `skill_list` | Yes | string | Comma-separated kicad-happy skills |
| `DRB_TITLE` | Yes | theme-token | "DESIGN REVIEW BOARD" or themed equivalent |
| `gate_context` | Yes | string | What the review board evaluates (e.g., "Post-Schematic") |
| `reviewers_label` | Yes | theme-token | "Reviewers" (neutral) or "Council members" (themed) |
| `reviewer_role_N` | Yes | string | Reviewer role name |
| `reviewer_focus_N` | Yes | string | What the reviewer evaluates |
| `review_mode` | Yes | theme-token | "independent review (no shared context)" or themed equivalent |
| `complete_verb` | Yes | theme-token | "Complete" (neutral) or "Returned" (themed) |
| `artifact_label` | Yes | theme-token | "artifacts" (neutral) or "scrolls" (themed) |
| `count` | Yes | integer | Number of artifacts produced |
| `activity_description` | Yes | string | Free-text description of current activity |

### Theme Injection Points

1. `dispatch_verb` -- "Dispatching" vs. "Summoning"
2. `context_label` -- "Context" vs. "Quest"
3. `skills_label` -- "Skills" vs. "Allies"
4. `DRB_TITLE` -- per theme token map
5. `reviewers_label` -- "Reviewers" vs. "Council members"
6. `review_mode` -- descriptive text per theme
7. `complete_verb` -- "Complete" vs. "Returned"
8. `artifact_label` -- "artifacts" vs. "scrolls"
9. `activity_description` -- progress text tone is theme-sensitive

### States

| State | Behavior |
|-------|----------|
| Dispatch | Shows `[>]` prefix with role, context, and skills |
| Working | Shows `[~]` prefix with activity narration |
| Complete | Shows `[+]` prefix with role and artifact count |
| Error | Shows `[!]` prefix with error description (see Error component) |
| No kicad skills | `skill_list` omitted entirely; line not rendered |

### Example: Neutral Theme

```
  [>] Dispatching: Electrical Engineer
      Context: Schematic stage, rework=false
      Skills: kicad, spice, digikey, mouser, lcsc, element14

  [~] Component selection: querying DigiKey for U3...
  [~] SPICE simulation: running transient analysis for U3...

  [+] Complete: Electrical Engineer (artifacts: 4)
```

### Example: LOTR Theme

```
  [>] Summoning: Electrical Engineer
      Quest: Schematic chapter, no shadow upon it
      Allies: kicad, spice, digikey, mouser, lcsc, element14

  [~] Seeking U3 in the markets of DigiKey...
  [~] The fires of SPICE test U3...

  [+] Returned: Electrical Engineer (scrolls: 4)
```

---

## Component 3: Gate Result

### Purpose

Presents the outcome of DoD gate validation. Supports simple pass/fail, multi-finding failures, specialized gates (DRC, BOM, Compliance), and Design Review Board aggregated results.

### Template

#### Variant A: Simple Gate

```
+------------------------------------------------------------+
| {{GATE_PREFIX}} {{from_stage}} --> {{to_stage}}             |
| {{SEV_ICON}} {{validator_name}}                             |
| ...                                                        |
| Result: {{RESULT_TOKEN}} -- {{result_action}}               |
+------------------------------------------------------------+
```

#### Variant B: Gate with Findings

```
+------------------------------------------------------------+
| {{GATE_PREFIX}} {{from_stage}} --> {{to_stage}}             |
| {{SEV_ICON}} {{validator_name}}                             |
|   {{FINDING_SEV}} {{finding_id}}: {{finding_summary}}       |
|     {{location_label}}: {{location}}                        |
|     {{fix_label}}: {{fix_description}}                      |
| ...                                                        |
| Result: {{RESULT_TOKEN}} -- {{blocking_summary}}            |
| {{pause_message}}                                          |
+------------------------------------------------------------+
```

#### Variant C: Specialized Gate (DRC / BOM / Compliance)

```
+------------------------------------------------------------+
| {{gate_type_title}}                                        |
|                                                            |
| {{SEV_ICON}} {{check_description}}                          |
| ...                                                        |
|                                                            |
| {{summary_counts}}                                         |
| Result: {{RESULT_TOKEN}}                                    |
+------------------------------------------------------------+
```

#### Variant D: Design Review Board Results

```
+------------------------------------------------------------+
| {{DRB_TITLE}}: {{review_context}}                          |
|                                                            |
| {{reviewer_label}} {{reviewer_role}}:                       |
|  {{FINDING_SEV}} {{finding_summary}}                        |
| ...                                                        |
|                                                            |
| Deduplicated: {{dedup_count}} findings merged              |
| Summary: {{sev_tally}}                                     |
+------------------------------------------------------------+
```

#### Variant E: Final Gate (Pipeline Complete)

```
+------------------------------------------------------------+
| {{COMPLETE_TITLE}}: {{project_name}}                       |
|                                                            |
| Stages: {{completed}}/{{total}} complete                    |
| Gates: {{gates_passed}}/{{gates_total}} passed              |
| Reworks: {{rework_count}} ({{rework_detail}})              |
| Artifacts: {{artifact_count}} files in {{artifact_path}}    |
|                                                            |
| Lessons captured to {{memory_path}}                        |
+------------------------------------------------------------+
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `GATE_PREFIX` | Yes | theme-token | "GATE:" or "THE COUNCIL OF:" |
| `from_stage` | Yes | string | Source stage name |
| `to_stage` | Yes | string | Target stage name |
| `SEV_ICON` | Yes | severity-token | Severity marker from token table |
| `validator_name` | Yes | string | Name of the validator |
| `FINDING_SEV` | Yes | severity-token | Finding severity level |
| `finding_id` | Yes | string | Finding ID (e.g., "F-001") |
| `finding_summary` | Yes | string | One-line finding description |
| `location_label` | Yes | theme-token | "Location" (neutral) or "Where" (themed) |
| `location` | Yes | string | Schematic sheet, net, coordinate |
| `fix_label` | Yes | theme-token | "Fix" (neutral) or "Remedy" (themed) |
| `fix_description` | Yes | string | Actionable fix instruction |
| `RESULT_TOKEN` | Yes | theme-token | "PASS"/"NOT_DONE" or themed equivalent |
| `result_action` | Yes | string | What happens next (advance/pause) |
| `blocking_summary` | Yes | string | Count of blocking findings |
| `pause_message` | Yes | string | Instruction to user when paused |
| `gate_type_title` | Yes | string | Specialized gate name (e.g., "DRC GATE", "BOM GATE") |
| `check_description` | Yes | string | Description of what was checked |
| `summary_counts` | No | string | "Errors: N | Warnings: N" format |
| `DRB_TITLE` | Yes | theme-token | Per theme token map |
| `review_context` | Yes | string | What the DRB evaluated |
| `reviewer_label` | Yes | theme-token | Label before reviewer name |
| `reviewer_role` | Yes | string | Reviewer role name |
| `dedup_count` | Yes | integer | Number of deduplicated findings |
| `sev_tally` | Yes | string | "N critical, N major, N minor, N warning" |
| `COMPLETE_TITLE` | Yes | theme-token | Per theme token map |
| `project_name` | Yes | string | From config |
| `completed` / `total` | Yes | integer | Stage completion counts |
| `gates_passed` / `gates_total` | Yes | integer | Gate pass counts |
| `rework_count` | Yes | integer | Total rework count |
| `rework_detail` | Yes | string | Per-stage rework breakdown |
| `artifact_count` | Yes | integer | Total artifact files produced |
| `artifact_path` | Yes | string | Artifact directory path |
| `memory_path` | Yes | string | Memory directory path |

### Theme Injection Points

1. `GATE_PREFIX` -- per theme token map
2. `RESULT_TOKEN` -- "PASS"/"NOT_DONE" vs. "THE PATH IS CLEAR"/"THE WAY IS SHUT"
3. `location_label` -- "Location" vs. "Where"
4. `fix_label` -- "Fix" vs. "Remedy"
5. `DRB_TITLE` -- per theme token map
6. `reviewer_label` -- neutral introduces with role name; themed adds narrative ("The Electrical Engineer speaks:")
7. `COMPLETE_TITLE` -- per theme token map
8. `pause_message` -- neutral is directive; themed is narrative
9. Finding descriptions may use theme-flavored language

### States

| State | Behavior |
|-------|----------|
| All pass | Show all validators with `[DONE]`, result line shows `PASS` |
| Partial failure | Show pass/fail per validator, findings under failed validators, result shows `NOT_DONE` |
| All fail | Same as partial failure but all validators show `[NOT_DONE]` |
| DRB with dedup | Show per-reviewer findings, then deduplication count and severity tally |
| Pipeline complete | Final gate variant with summary statistics |

### Example: Neutral Theme (Gate with Findings)

```
+------------------------------------------------------------+
| GATE: Schematic --> Layout                                 |
| [DONE] Component lifecycle check                          |
| [NOT_DONE] Schematic review                               |
|   [CRITICAL] F-001: Missing bulk cap on U3 VDD            |
|     Location: Sheet 2, U3 pin 14                          |
|     Fix: Add 10uF ceramic cap, place within 3mm           |
|   [MAJOR] F-002: Unterminated SPI_CLK trace               |
|     Location: Sheet 1, Net SPI_CLK                        |
|     Fix: Add series termination resistor (33R)            |
| Result: NOT_DONE -- 1 critical finding                     |
| Pipeline paused. Correct findings and re-run gate.         |
+------------------------------------------------------------+
```

### Example: LOTR Theme (Gate with Findings)

```
+------------------------------------------------------------+
| THE COUNCIL OF: Schematic --> Layout                       |
| [DONE] Component lifecycle check                          |
| [NOT_DONE] Schematic review                               |
|   [CRITICAL] F-001: A darkness upon U3 -- no bulk cap     |
|     Where: Sheet 2, U3 pin 14                             |
|     Remedy: Place a 10uF ceramic ward within 3mm          |
|   [MAJOR] F-002: SPI_CLK wanders unterminated             |
|     Where: Sheet 1, Net SPI_CLK                           |
|     Remedy: A 33R resistor to end its wandering            |
| The way is shut -- 1 critical shadow found                 |
| The fellowship rests. Correct the darkness and return.     |
+------------------------------------------------------------+
```

---

## Component 4: Checkpoint Summary

### Purpose

Presents artifact summaries at human checkpoints. Two variants: AI-stage artifact summary and human-action checkpoint with action items.

### Template

#### Variant A: Artifact Summary (AI Stage)

```
+------------------------------------------------------------+
| {{artifacts_title}}: {{STAGE_PREFIX}} - {{stage_name}}      |
|                                                            |
| {{n}}. {{filename}} -- {{description}}                      |
| ...                                                        |
|                                                            |
| Saved to: {{artifact_dir}}                                 |
+------------------------------------------------------------+
```

#### Variant B: Human-Action Checkpoint

```
+------------------------------------------------------------+
| === {{HUMAN_ACTION}} ===                                   |
|                                                            |
| {{prep_label}}:                                            |
|  {{n}}. {{filename}} -- {{description}}                     |
| ...                                                        |
|                                                            |
| {{action_label}}:                                          |
|  [ ] {{n}}. {{action_item}}                                 |
| ...                                                        |
|                                                            |
| When complete, confirm: "{{confirm_phrase}}"                |
| To report issues: "{{fail_phrase}}: [description]"          |
| To pause and resume later: "save pipeline state"           |
+------------------------------------------------------------+
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `artifacts_title` | Yes | theme-token | "ARTIFACTS" (neutral) or "SCROLLS OF" (themed) |
| `STAGE_PREFIX` | Yes | theme-token | Per theme token map |
| `stage_name` | Yes | string | Stage name |
| `n` | Yes | integer | Item number (1-indexed) |
| `filename` | Yes | string | Artifact filename |
| `description` | Yes | string | One-line description; wraps at inner width with indent |
| `artifact_dir` | Yes | string | Directory path where artifacts are saved |
| `HUMAN_ACTION` | Yes | theme-token | Per theme token map |
| `prep_label` | Yes | theme-token | "Preparation artifacts" (neutral) or "Scrolls prepared for your journey" (themed) |
| `action_label` | Yes | theme-token | "Action items" (neutral) or "Your deeds" (themed) |
| `action_item` | Yes | string | Human action item text |
| `confirm_phrase` | Yes | string | Phrase to confirm completion (e.g., "prototype complete") |
| `fail_phrase` | Yes | string | Phrase to report failure (e.g., "prototype failed") |

### Theme Injection Points

1. `artifacts_title` -- "ARTIFACTS" vs. "SCROLLS OF"
2. `STAGE_PREFIX` -- per theme token map
3. `HUMAN_ACTION` -- per theme token map
4. `prep_label` -- neutral label vs. themed narrative
5. `action_label` -- neutral label vs. themed narrative
6. Artifact descriptions may use themed language
7. Action items may use themed verbs (e.g., "Order" vs. "Send the order to the forges")
8. Confirm/fail phrases may be themed

### States

| State | Behavior |
|-------|----------|
| AI artifacts | Variant A with numbered artifact list |
| Human checkpoint | Variant B with preparation artifacts and checkbox action items |
| No artifacts | Variant A with "No artifacts produced" message |
| Resuming | Variant B re-presented with "(Same checkpoint as when paused)" note |

### Example: Neutral Theme

```
+------------------------------------------------------------+
| ARTIFACTS: Stage 2 - Schematic                             |
|                                                            |
| 1. schematic-review.md -- EE schematic review findings     |
| 2. component-rationale.md -- selection rationale per part  |
| 3. spice-results.md -- simulation results for U3, U7      |
| 4. firmware-interface.md -- pin table, power domains,      |
|    bus specs, debug interfaces                             |
|                                                            |
| Saved to: .hardware/artifacts/02-schematic/                |
+------------------------------------------------------------+
```

### Example: LOTR Theme

```
+------------------------------------------------------------+
| SCROLLS OF: Chapter 2 - The Council of Rivendell           |
|                                                            |
| 1. schematic-review.md -- the mirror reveals all flaws     |
| 2. component-rationale.md -- why each ally was chosen      |
| 3. spice-results.md -- the fires of simulation tested U3,  |
|    U7                                                      |
| 4. firmware-interface.md -- the map of pins, the domains   |
|    of power, the roads of data                             |
|                                                            |
| Stored in: .hardware/artifacts/02-schematic/               |
+------------------------------------------------------------+
```

---

## Component 5: Escalation

### Purpose

Presents escalation decisions when rework limits are reached. Shows rework history, pattern analysis, recommendations, and user options.

### Template

#### Variant A: Per-Path Rework Limit

```
+------------------------------------------------------------+
| {{REWORK_LIMIT}}                                           |
|                                                            |
| Limit type: Per-path                                       |
| Path: {{source_stage}} --> {{target_stage}}                 |
| Iterations: {{current}}/{{limit}} (limit reached)          |
|                                                            |
| {{history_label}} for this path:                           |
|  #{{n}}: {{rework_summary}}                                |
| ...                                                        |
|                                                            |
| Recurring pattern: {{pattern_analysis}}                    |
|                                                            |
| RECOMMENDATION: {{recommendation}}                         |
|                                                            |
| === {{PAUSED_TITLE}} ===                                   |
| Options:                                                   |
|  "continue" -- {{continue_desc}}                           |
|  "abort" -- {{abort_desc}}                                 |
|  "override limit N" -- {{override_desc}}                   |
+------------------------------------------------------------+
```

#### Variant B: Total Rework Limit

```
+------------------------------------------------------------+
| {{REWORK_LIMIT}} (Total)                                   |
|                                                            |
| Limit type: Total (across all paths)                       |
| Total reworks: {{current}}/{{limit}} (limit reached)       |
|                                                            |
| {{history_label}}:                                         |
|  {{path}}: {{count}} iterations                            |
| ...                                                        |
|                                                            |
| RECOMMENDATION: {{recommendation}}                         |
|                                                            |
| === {{PAUSED_TITLE}} ===                                   |
| Options:                                                   |
|  "continue" -- {{continue_desc}}                           |
|  "abort" -- {{abort_desc}}                                 |
|  "override total N" -- {{override_desc}}                   |
+------------------------------------------------------------+
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `REWORK_LIMIT` | Yes | theme-token | Per theme token map |
| `source_stage` | Yes | string | Stage that triggered rework |
| `target_stage` | Yes | string | Stage to return to |
| `current` | Yes | integer | Current iteration count |
| `limit` | Yes | integer | Configured limit |
| `history_label` | Yes | theme-token | "Rework history" (neutral) or "Chronicle of this path" (themed) |
| `n` | Yes | integer | Rework iteration number |
| `rework_summary` | Yes | string | One-line summary of what happened in that iteration |
| `pattern_analysis` | Yes | string | Analysis of recurring pattern across iterations |
| `recommendation` | Yes | string | Actionable recommendation for the user |
| `PAUSED_TITLE` | Yes | theme-token | Per theme token map |
| `continue_desc` | Yes | theme-token | "override limit, try once more" or themed |
| `abort_desc` | Yes | theme-token | "stop the pipeline run" or themed |
| `override_desc` | Yes | theme-token | "set new per-path limit" or themed |
| `path` | Yes (Variant B) | string | Rework path (e.g., "DFM-->Schematic") |
| `count` | Yes (Variant B) | integer | Iteration count for that path |

### Theme Injection Points

1. `REWORK_LIMIT` -- per theme token map
2. `history_label` -- "Rework history" vs. "Chronicle"
3. `PAUSED_TITLE` -- per theme token map
4. `pattern_analysis` -- neutral is analytical; themed is narrative
5. `recommendation` -- "RECOMMENDATION" (neutral) vs. "COUNSEL" (themed)
6. Option descriptions -- neutral is directive; themed is narrative
7. Individual rework summaries may use themed language

### States

| State | Behavior |
|-------|----------|
| Per-path limit | Variant A with path-specific history and pattern analysis |
| Total limit | Variant B with summary across all paths |
| Single iteration path | History shows only one entry; pattern analysis states "insufficient data for pattern" |

### Example: Neutral Theme

```
+------------------------------------------------------------+
| REWORK LIMIT REACHED                                       |
|                                                            |
| Limit type: Per-path                                       |
| Path: DFM/DFA --> Schematic                                |
| Iterations: 3/3 (limit reached)                            |
|                                                            |
| Rework history for this path:                              |
|  #1: Component U5 unavailable --> substituted U5B          |
|  #2: U5B footprint incompatible --> substituted U5C        |
|  #3: U5C voltage range insufficient --> ?                  |
|                                                            |
| Recurring pattern: Component selection for U5 position     |
| is failing repeatedly.                                     |
|                                                            |
| RECOMMENDATION: Manual intervention needed. Consider       |
| redesigning the power regulation approach rather than      |
| iterating on component substitution.                       |
|                                                            |
| === PIPELINE PAUSED ===                                    |
| Options:                                                   |
|  "continue" -- override limit, try once more               |
|  "abort" -- stop the pipeline run                          |
|  "override limit N" -- set new per-path limit              |
+------------------------------------------------------------+
```

### Example: LOTR Theme

```
+------------------------------------------------------------+
| THE DOOM OF THE NOLDOR                                     |
|                                                            |
| Doom: Per-path                                             |
| Path: DFM/DFA --> Schematic                                |
| Trials endured: 3/3 (the limit of endurance)               |
|                                                            |
| Chronicle of this path:                                    |
|  #1: U5 fell -- U5B took its place                         |
|  #2: U5B's form did not fit -- U5C was summoned            |
|  #3: U5C's power was insufficient -- none remain           |
|                                                            |
| The pattern repeats: the U5 seat cannot be filled          |
| by simple substitution.                                    |
|                                                            |
| COUNSEL: The approach must change. Redesign the power      |
| regulation rather than seeking yet another component.      |
|                                                            |
| === THE FELLOWSHIP RESTS ===                               |
| Speak your will:                                           |
|  "continue" -- one more trial                              |
|  "abort" -- end the quest                                  |
|  "override limit N" -- extend the doom                     |
+------------------------------------------------------------+
```

---

## Component 6: Progress Table

### Purpose

Provides a full pipeline status overview as a line-per-stage table. Used by the `hw-status` command and in resume notifications.

### Template

```
+------------------------------------------------------------+
| {{status_title}}: {{project_name}}                         |
|                                                            |
| {{stage_label}} {{n}}: {{stage_name}}{{pad}}[{{status}}]{{rework_note}}|
| ...                                                        |
|                                                            |
| Current: {{current_stage_desc}}                            |
| Reworks: {{rework_total}} total ({{rework_of_limit}})      |
| State: {{state_path}} (last saved: {{timestamp}})          |
+------------------------------------------------------------+
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `status_title` | Yes | theme-token | "PIPELINE STATUS" (neutral) or "QUEST STATUS" (themed) |
| `project_name` | Yes | string | From config |
| `stage_label` | Yes | theme-token | "Stage" (neutral) or "Ch" (themed) |
| `n` | Yes | integer | Stage number |
| `stage_name` | Yes | string | Stage name; themed may include alias in parentheses |
| `pad` | Yes | whitespace | Right-padding to align status brackets |
| `status` | Yes | status-token | `DONE`, `PAUSED`, or empty `  ` |
| `rework_note` | No | string | ` (rework xN)` or ` (shadow xN)` if reworks occurred |
| `current_stage_desc` | Yes | string | Current stage with status qualifier |
| `rework_total` | Yes | integer | Total rework count |
| `rework_of_limit` | Yes | string | "N of M limit" format |
| `state_path` | Yes | string | Path to state file |
| `timestamp` | Yes | string | ISO-ish timestamp of last save |

### Theme Injection Points

1. `status_title` -- "PIPELINE STATUS" vs. "QUEST STATUS"
2. `stage_label` -- "Stage" vs. "Ch"
3. Stage names may include themed aliases in parentheses
4. `rework_note` -- "(rework xN)" vs. "(shadow xN)"
5. `current_stage_desc` -- neutral is factual; themed is narrative
6. Footer message tone

### States

| State | Behavior |
|-------|----------|
| In progress | Current stage shows `[PAUSED]` or is being executed |
| Complete | All stages show `[DONE]`; footer shows completion message |
| Not started | All stages show `[ ]` |
| Resumed | Preceded by resume notification (see Component 7 Config Display variant) |

### Example: Neutral Theme

```
+------------------------------------------------------------+
| PIPELINE STATUS: sensor-board-v2                           |
|                                                            |
| Stage 1: Concept              [DONE]                       |
| Stage 2: Schematic            [DONE] (rework x1)          |
| Stage 3: Layout               [DONE]                       |
| Stage 4: Prototype            [PAUSED] -- human action     |
| Stage 5: DFM/DFA              [ ]                          |
| Stage 6: Compliance           [ ]                          |
| Stage 7: Pilot Run            [ ]                          |
| Stage 8: Production Release   [ ]                          |
|                                                            |
| Current: Stage 4 (Prototype) -- awaiting confirmation      |
| Reworks: 1 total (1 of 10 limit)                           |
| State: .hardware/state.md (last saved: 2026-04-12 14:32)  |
+------------------------------------------------------------+
```

### Example: LOTR Theme

```
+------------------------------------------------------------+
| QUEST STATUS: sensor-board-v2                              |
|                                                            |
| Ch 1: Concept (The Shire)     [DONE]                       |
| Ch 2: Schematic (Rivendell)   [DONE] (shadow x1)          |
| Ch 3: Layout (Moria)          [DONE]                       |
| Ch 4: Prototype (Rohan)       [PAUSED] -- mortal deed      |
| Ch 5: DFM/DFA (Helm's Deep)   [ ]                          |
| Ch 6: Compliance (Gondor)     [ ]                          |
| Ch 7: Pilot Run (Pelennor)    [ ]                          |
| Ch 8: Prod Release (Mt Doom)  [ ]                          |
|                                                            |
| The fellowship rests at: Chapter 4 (Rohan)                 |
| Shadows faced: 1 of 10                                     |
| Scroll: .hardware/state.md (inscribed: 2026-04-12 14:32)  |
+------------------------------------------------------------+
```

---

## Component 7: Config Display

### Purpose

Shows configuration values during setup wizard, config confirmation, and resume notifications.

### Template

#### Variant A: Setup Wizard Question

```
+------------------------------------------------------------+
| {{setup_title}}: Question {{n}} of {{total}}                |
+------------------------------------------------------------+
| {{question_text}}                                          |
|                                                            |
| {{options_or_default}}                                     |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

#### Variant B: Config Confirmation

```
+------------------------------------------------------------+
| Created {{config_path}} (schema {{schema_version}})        |
|                                                            |
|   {{key}}: {{value}}                                        |
| ...                                                        |
|                                                            |
| {{edit_hint}}                                              |
+------------------------------------------------------------+
```

#### Variant C: Resume Notification

```
+------------------------------------------------------------+
| {{resume_intro}}                                           |
|                                                            |
| Pipeline: {{project_name}}                                 |
| Last stage completed: {{last_stage}}                       |
| Current stage: {{current_stage}} -- {{current_status}}      |
| {{pending_action_label}}: {{pending_action}}               |
| {{rework_label}}: {{rework_summary}}                       |
|                                                            |
| To resume: "{{resume_phrase}}"                             |
| To start fresh: "{{fresh_phrase}}"                         |
+------------------------------------------------------------+
```

#### Variant D: No Config Found

```
+------------------------------------------------------------+
| {{no_config_intro}}                                        |
| Run `hw-setup` to create one.                              |
|                                                            |
| kicad-happy: {{available}}/{{total}} skills available      |
+------------------------------------------------------------+
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `setup_title` | Yes | theme-token | "SETUP" (neutral) or "THE CRAFTING" (themed) |
| `n` / `total` | Yes | integer | Current question and total |
| `question_text` | Yes | string | The question |
| `options_or_default` | No | string | Multi-choice options block or "Default: X" |
| `config_path` | Yes | string | Path to config file |
| `schema_version` | Yes | string | Schema version |
| `key` / `value` | Yes | string | Config key-value pairs, indented 2 spaces |
| `edit_hint` | Yes | theme-token | "Edit .hardware/config.yml to adjust settings." or themed |
| `resume_intro` | Yes | theme-token | "hardware-team: Persisted pipeline state found." or themed |
| `project_name` | Yes | string | From config |
| `last_stage` | Yes | string | Last completed stage |
| `current_stage` | Yes | string | Current stage |
| `current_status` | Yes | string | Status qualifier (e.g., "PAUSED") |
| `pending_action_label` | Yes | theme-token | "Human action pending" or themed |
| `pending_action` | Yes | string | Description of pending action |
| `rework_label` | Yes | theme-token | "Rework history" or themed |
| `rework_summary` | Yes | string | Summary of reworks |
| `resume_phrase` | Yes | string | Command to resume |
| `fresh_phrase` | Yes | string | Command to start fresh |
| `no_config_intro` | Yes | theme-token | "hardware-team: No .hardware/config.yml found." or themed |
| `available` / `total` | Yes | integer | kicad-happy skill counts |

### Theme Injection Points

1. `setup_title` -- "SETUP" vs. "THE CRAFTING"
2. Question numbering -- "Question N of M" vs. "Inscription N of M"
3. Option labels may include themed descriptions
4. Config key names may be themed in Variant B display (e.g., "quest" vs. "project")
5. `edit_hint` -- neutral directive vs. themed narrative
6. `resume_intro` -- neutral factual vs. themed narrative
7. `pending_action_label` -- neutral vs. themed
8. `no_config_intro` -- neutral vs. themed

### States

| State | Behavior |
|-------|----------|
| Free-text question | Shows `> _` prompt with no options |
| Multi-choice question | Shows numbered `[N]` options |
| Default provided | Shows "Default: X" line |
| Config exists | Variant D with overwrite prompt |
| Config valid | Variant B followed by "Config valid. Ready to run pipeline." box |
| Resume available | Variant C with resume/fresh options |

### Example: Neutral Theme (Question with Options)

```
+------------------------------------------------------------+
| SETUP: Question 2 of 9                                     |
+------------------------------------------------------------+
| Target fabrication house?                                  |
|                                                            |
| Options:                                                   |
|   [1] jlcpcb                                               |
|   [2] pcbway                                               |
|   [3] other                                                |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

### Example: LOTR Theme (Question with Options)

```
+------------------------------------------------------------+
| THE CRAFTING: Inscription 2 of 9                           |
+------------------------------------------------------------+
| To which forge shall the boards be sent?                   |
|                                                            |
| The forges of Middle-earth:                                |
|   [1] jlcpcb    -- The Mines of Fabrication                |
|   [2] pcbway    -- The Forges of the East                  |
|   [3] other     -- A forge unknown to us                   |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

---

## Component 8: Error/Warning

### Purpose

Consistent format for errors, warnings, and informational messages. Covers dependency issues, config validation, schema migration, hook warnings, and system errors.

### Template

#### Variant A: Dependency Warning (Full)

```
+------------------------------------------------------------+
| WARNING: {{dependency_message}}                            |
| {{install_instruction}}                                    |
|                                                            |
| {{impact_description}}                                     |
|                                                            |
| kicad-happy: {{available}}/{{total}} skills available      |
| Missing: {{missing_skill_list}}                            |
+------------------------------------------------------------+
```

#### Variant B: Dependency Warning (Compact)

```
+------------------------------------------------------------+
| kicad-happy: {{available}}/{{total}} skills available      |
| Missing: {{missing_skill_list}}                            |
| {{install_instruction}}                                    |
+------------------------------------------------------------+
```

#### Variant C: Config Validation Warning

```
+------------------------------------------------------------+
| WARNING: {{config_path}} has invalid fields:               |
|   - {{field}}: {{value}} ({{expected}})                    |
| ...                                                        |
| {{fallback_message}}                                       |
+------------------------------------------------------------+
```

#### Variant D: Schema Migration Warning

```
+------------------------------------------------------------+
| WARNING: {{config_path}} uses schema {{old_version}}.      |
| Current schema is {{new_version}}.                         |
| Migration: {{migration_instructions}}                      |
| {{fallback_message}}                                       |
+------------------------------------------------------------+
```

#### Variant E: Hook Warning (DRC)

```
+------------------------------------------------------------+
| DRC WARNING (auto-check on schematic edit):                |
|  [W] {{net_or_component}}: {{warning_description}}         |
| ...                                                        |
+------------------------------------------------------------+
```

#### Variant F: Hook Warning (BOM Drift)

```
+------------------------------------------------------------+
| BOM DRIFT WARNING:                                         |
|  + Added: {{component}} ({{detail}})                       |
|  - Removed: {{component}} ({{detail}})                     |
|  ~ Changed: {{component}} {{change_desc}}                  |
|                                                            |
| {{reconciliation_instruction}}                             |
+------------------------------------------------------------+
```

#### Variant G: Skill Unavailable During Stage

```
+------------------------------------------------------------+
| WARNING: kicad-happy:{{skill_name}} not available          |
|                                                            |
| {{impact_on_current_stage}}                                |
|                                                            |
| {{install_instruction}}                                    |
|                                                            |
| {{pipeline_continuation_note}}                             |
| {{downstream_impact_note}}                                 |
+------------------------------------------------------------+
```

#### Variant H: Stale State Warning

```
+------------------------------------------------------------+
| WARNING: Source files modified since last pipeline run.     |
| {{modified_files_desc}}                                    |
|                                                            |
| {{impact_note}}                                            |
| Options:                                                   |
|  "resume" -- {{resume_desc}}                               |
|  "revalidate" -- {{revalidate_desc}}                       |
|  "restart" -- {{restart_desc}}                             |
+------------------------------------------------------------+
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `dependency_message` | Yes | string | What dependency is missing/outdated |
| `install_instruction` | Yes | string | How to install the dependency |
| `impact_description` | Yes | string | What functionality is affected |
| `available` / `total` | Yes | integer | kicad-happy skill counts |
| `missing_skill_list` | Yes | string | Comma-separated missing skill names |
| `config_path` | Yes | string | Path to config file |
| `field` | Yes | string | Invalid field name |
| `value` | Yes | string | Invalid value found |
| `expected` | Yes | string | Expected type or value set |
| `fallback_message` | Yes | string | What defaults are used |
| `old_version` / `new_version` | Yes | string | Schema versions |
| `migration_instructions` | Yes | string | How to migrate |
| `net_or_component` | Yes | string | Net name or component reference |
| `warning_description` | Yes | string | What was detected |
| `component` | Yes | string | Component designator |
| `detail` | Yes | string | Additional context |
| `change_desc` | Yes | string | What changed |
| `reconciliation_instruction` | Yes | string | How to fix drift |
| `skill_name` | Yes | string | Missing kicad-happy skill name |
| `impact_on_current_stage` | Yes | string | How this affects the current stage |
| `pipeline_continuation_note` | Yes | string | Whether pipeline continues |
| `downstream_impact_note` | Yes | string | Impact on downstream gates |
| `modified_files_desc` | Yes | string | Which files changed |
| `impact_note` | Yes | string | Impact of stale state |
| `resume_desc` / `revalidate_desc` / `restart_desc` | Yes | string | Option descriptions |

### Theme Injection Points

1. "WARNING" prefix -- unchanged across themes (severity must remain clear)
2. `impact_description` -- neutral is technical; themed is narrative
3. `install_instruction` -- neutral is directive; themed may add flavor
4. `fallback_message` -- neutral states defaults; themed may add narrative
5. Hook warning content remains technical (safety-critical -- no theme flavor on DRC/BOM warnings)

### States

| State | Behavior |
|-------|----------|
| kicad-happy fully missing | Variant A (full dependency warning) |
| kicad-happy partially installed | Variant B (compact) |
| Version mismatch | Single-line version warning |
| Config invalid | Variant C with per-field errors |
| Schema outdated | Variant D with migration steps |
| DRC hook triggered | Variant E with per-net warnings |
| BOM drift detected | Variant F with add/remove/change markers |
| Skill missing mid-stage | Variant G with impact and continuation note |
| Stale state on resume | Variant H with three recovery options |

### Example: Neutral Theme (Skill Unavailable)

```
+------------------------------------------------------------+
| WARNING: kicad-happy:spice not available                   |
|                                                            |
| Cannot perform SPICE simulation. The Electrical Engineer   |
| role requires this skill for circuit validation.           |
|                                                            |
| Install kicad-happy via the Claude Code plugin system      |
| to enable simulation capabilities.                         |
|                                                            |
| Pipeline continuing without simulation data.               |
| Schematic Review Gate may flag unvalidated circuits.       |
+------------------------------------------------------------+
```

### Example: LOTR Theme (Skill Unavailable)

```
+------------------------------------------------------------+
| WARNING: The fires of kicad-happy:spice cannot be          |
| summoned in this realm.                                    |
|                                                            |
| Without them, the Electrical Engineer cannot test           |
| circuits by simulation.                                    |
|                                                            |
| Summon kicad-happy via the plugin system to restore        |
| this power.                                                |
|                                                            |
| The quest continues without simulation. The Schematic      |
| Council may find unvalidated paths.                        |
+------------------------------------------------------------+
```

---

## Component 9: Artifact Reference

### Purpose

Standardized format for referencing artifacts (files) by path with descriptions. Used within checkpoint summaries and elsewhere when citing generated files.

### Template

#### Variant A: Inline Reference

```
{{n}}. {{filename}} -- {{description}}
```

#### Variant B: Multi-line Reference (Long Description)

```
{{n}}. {{filename}} -- {{description_line_1}}
   {{description_continuation}}
```

#### Variant C: Directory Reference

```
Saved to: {{directory_path}}
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `n` | Yes | integer | 1-indexed item number |
| `filename` | Yes | string | File name (not full path -- directory is stated separately) |
| `description` | Yes | string | One-line description of the artifact's content |
| `description_line_1` | Yes | string | First line of description (fits within inner width) |
| `description_continuation` | Yes | string | Continuation indented 3 spaces from left margin |
| `directory_path` | Yes | string | Directory where artifacts are stored |

### Theme Injection Points

1. `description` -- neutral is technical; themed may use narrative language
2. `directory_path` label -- "Saved to:" (neutral) vs. "Stored in:" (themed)
3. File descriptions may reference themed concepts (e.g., "the mirror reveals" instead of "review findings")

### Wrapping Rules

- Descriptions wrap at 56 characters (inner width minus item number prefix)
- Continuation lines are indented 3 spaces from the left content margin to align with the start of the description text after the ` -- ` separator
- File names never wrap; if a filename exceeds 40 characters, truncate with `...` and show full path in the directory reference

### States

| State | Behavior |
|-------|----------|
| Short description | Single-line Variant A |
| Long description | Multi-line Variant B with continuation |
| Directory reference | Variant C on its own line after the file list |

### Example: Neutral Theme

```
1. schematic-review.md -- EE schematic review findings
2. component-rationale.md -- selection rationale per part
3. spice-results.md -- simulation results for U3, U7
4. firmware-interface.md -- pin table, power domains,
   bus specs, debug interfaces

Saved to: .hardware/artifacts/02-schematic/
```

### Example: LOTR Theme

```
1. schematic-review.md -- the mirror reveals all flaws
2. component-rationale.md -- why each ally was chosen
3. spice-results.md -- the fires of simulation tested U3,
   U7
4. firmware-interface.md -- the map of pins, the domains
   of power, the roads of data

Stored in: .hardware/artifacts/02-schematic/
```

---

## Component 10: Rework Notification

### Purpose

Announces rework triggers with context, history, and downstream re-validation status.

### Template

#### Variant A: Rework Triggered

```
+------------------------------------------------------------+
| {{REWORK_TITLE}}                                           |
|                                                            |
| Source: {{source_stage}} (Stage {{source_n}})              |
| Target: {{target_stage}} (Stage {{target_n}})              |
| Reason: {{rework_reason}}                                  |
|                                                            |
| Rework path: {{source_stage}} --> {{target_stage}}          |
| Iteration: {{current}} of {{limit}} (per-path limit)       |
| Total reworks this run: {{total}} of {{total_limit}}        |
|                                                            |
| {{return_message}}                                         |
+------------------------------------------------------------+
```

#### Variant B: Downstream Re-Validation

```
+------------------------------------------------------------+
| {{revalidation_title}}                                     |
|                                                            |
| {{gate_name}} Gate: [{{status}}] ({{revalidation_note}})   |
| ...                                                        |
|                                                            |
| {{resolution_message}}                                     |
+------------------------------------------------------------+
```

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `REWORK_TITLE` | Yes | theme-token | Per theme token map |
| `source_stage` | Yes | string | Stage that triggered rework |
| `source_n` | Yes | integer | Source stage number |
| `target_stage` | Yes | string | Stage to return to |
| `target_n` | Yes | integer | Target stage number |
| `rework_reason` | Yes | string | Why rework was triggered; wraps at inner width |
| `current` | Yes | integer | Current per-path iteration |
| `limit` | Yes | integer | Per-path iteration limit |
| `total` | Yes | integer | Total reworks this run |
| `total_limit` | Yes | integer | Total rework limit |
| `return_message` | Yes | theme-token | "Returning to X stage with rework context..." or themed |
| `revalidation_title` | Yes | theme-token | "DOWNSTREAM RE-VALIDATION" or themed |
| `gate_name` | Yes | string | Name of the gate being re-validated |
| `status` | Yes | severity-token | `DONE` or `NOT_DONE` |
| `revalidation_note` | Yes | string | "(re-validated)" or themed |
| `resolution_message` | Yes | string | Outcome of re-validation |

### Theme Injection Points

1. `REWORK_TITLE` -- per theme token map
2. `return_message` -- neutral is directive; themed is narrative
3. `revalidation_title` -- "DOWNSTREAM RE-VALIDATION" vs. "THE PATH IS CLEAR ONCE MORE"
4. `revalidation_note` -- "(re-validated)" vs. "(re-judged)"
5. `resolution_message` -- neutral is factual; themed is narrative
6. `rework_reason` -- stays technical regardless of theme (engineering accuracy required)

### States

| State | Behavior |
|-------|----------|
| First rework | Variant A; iteration shows "1 of N" |
| Subsequent rework | Variant A; iteration shows "M of N" where M > 1 |
| Re-validation pass | Variant B; all gates show `[DONE]` |
| Re-validation fail | Variant B; one or more gates show `[NOT_DONE]`; triggers additional rework |

### Example: Neutral Theme

```
+------------------------------------------------------------+
| REWORK TRIGGERED                                           |
|                                                            |
| Source: DFM/DFA (Stage 5)                                  |
| Target: Schematic (Stage 2)                                |
| Reason: Component U5 (QFN-48) not available at JLCPCB.    |
|   Requires component substitution.                         |
|                                                            |
| Rework path: DFM/DFA --> Schematic                         |
| Iteration: 1 of 3 (per-path limit)                        |
| Total reworks this run: 2 of 10                            |
|                                                            |
| Returning to Schematic stage with rework context...        |
+------------------------------------------------------------+
```

### Example: LOTR Theme

```
+------------------------------------------------------------+
| A SHADOW RETURNS                                           |
|                                                            |
| From: DFM/DFA (Chapter 5)                                 |
| To: Schematic (Chapter 2)                                  |
| The darkness: Component U5 (QFN-48) cannot be found in     |
|   the stores of JLCPCB. A new ally must be chosen.         |
|                                                            |
| Shadow path: DFM/DFA --> Schematic                         |
| Trial: 1 of 3 (per-path doom)                             |
| Shadows faced this quest: 2 of 10                          |
|                                                            |
| The fellowship retreats to Schematic, bearing knowledge    |
| of what went wrong...                                      |
+------------------------------------------------------------+
```

---

## Component 11: kicad-happy Integration

### Purpose

Shows the status of cross-plugin skill invocations when the hardware-team orchestrator dispatches kicad-happy skills. This component communicates dependency availability, invocation status, and graceful degradation.

### Template

#### Variant A: Skill Availability Summary (SessionStart / Pre-Flight)

```
kicad-happy: {{available}}/{{total}} skills available
```

#### Variant B: Skill Invocation (Within Agent Dispatch)

```
      {{skills_label}}: {{skill_list}}
```

This appears as a sub-line within the Agent Status component (Component 2).

#### Variant C: Skill Unavailable Warning

Uses Error/Warning Component (Component 8, Variant G) with kicad-happy-specific content.

#### Variant D: Version Status

```
+------------------------------------------------------------+
| kicad-happy version {{installed}} installed; hardware-team  |
| requires {{required}}. {{impact_note}}                     |
+------------------------------------------------------------+
```

#### Variant E: Full Dependency Block (kicad-happy Missing)

Uses Error/Warning Component (Component 8, Variant A) with the full 11-skill enumeration.

### Placeholder Definitions

| Placeholder | Required | Type | Description |
|-------------|----------|------|-------------|
| `available` | Yes | integer | Count of available kicad-happy skills (0-11) |
| `total` | Yes | integer | Total kicad-happy skills (always 11) |
| `skills_label` | Yes | theme-token | "kicad-happy" (neutral) or "Allies summoned" / "Allies" (themed) |
| `skill_list` | Yes | string | Comma-separated skill names relevant to current context |
| `installed` | Yes | string | Installed kicad-happy version |
| `required` | Yes | string | Required version from config |
| `impact_note` | Yes | string | "Some features may not work." or similar |

### Theme Injection Points

1. `skills_label` -- "kicad-happy" vs. "Allies" / "Allies summoned" / "Allies of the fellowship"
2. Availability summary -- neutral counts vs. "N allies stand ready" (themed)
3. Missing skills -- neutral lists names; themed may add narrative ("these allies have not answered the call")
4. Version warnings remain technical (safety-critical dependency check)

### States

| State | Behavior |
|-------|----------|
| All 11 available | Variant A shows "11/11 skills available" |
| Partially available | Variant A shows "N/11 skills available" + Variant B compact warning |
| None available | Variant E full dependency block |
| Version mismatch | Variant D with version numbers and impact |
| Skill needed but missing mid-stage | Variant C via Error/Warning component |

### Interaction with Other Components

| Component | How kicad-happy Integration Appears |
|-----------|-------------------------------------|
| Stage Header (C1) | Pre-flight summary includes Variant A availability line |
| Stage Header (C1) | AI-execution banner includes skill list relevant to stage |
| Agent Status (C2) | Dispatch shows Variant B skill list under agent context |
| Error/Warning (C8) | Missing/unavailable skills use C8 variants |
| Config Display (C7) | SessionStart no-config message includes Variant A |

### Example: Neutral Theme (Full Availability in Pre-Flight)

```
kicad-happy: 11/11 skills available
```

### Example: LOTR Theme (Full Availability in Pre-Flight)

```
Allies of the fellowship: 11/11 kicad-happy skills stand
ready.
```

### Example: Neutral Theme (Partial in Stage Banner)

```
============================================================
  STAGE 2: SCHEMATIC [AI-execution]
  Roles: Electrical Engineer (primary), HW PO (trade-offs)
  Activities: schematic review, component selection
  kicad-happy: kicad, digikey, mouser, lcsc, element14
  WARNING: spice not available (simulation disabled)
============================================================
```

---

## Theme Injection Architecture

If you want the design to live, you must trust me. Give it to me. I will carry it to the design system where it will be preserved.

### How Theming Works

Every component uses a two-layer token system:

1. **Structural tokens** -- box drawing, width, padding, severity icons, progress indicators. These NEVER change between themes. They are the skeleton.

2. **Content tokens** -- titles, labels, verbs, descriptions. These are the injection points. Each is identified by a `theme-token` type in the placeholder definitions.

### Theme Application Rules

| Rule | Description |
|------|-------------|
| Severity icons are sacred | `[DONE]`, `[NOT_DONE]`, `[CRITICAL]`, `[MAJOR]`, `[MINOR]`, `[WARNING]`, `[ERROR]`, `[INFO]` never change. Safety and clarity require it. |
| Box structure is sacred | `+`, `-`, `|`, `=` characters and the 60-char width never change. Layout must be identical across themes. |
| Progress indicators are sacred | `[>]`, `[~]`, `[+]` never change. The user must instantly recognize agent lifecycle state. |
| Finding IDs are sacred | `F-001`, `V-001`, etc. never change. Engineers reference these in discussions. |
| File paths are sacred | `.hardware/config.yml`, artifact paths, etc. never change. They must be copy-pasteable. |
| Technical content in DRC/BOM/hook warnings stays neutral | Safety-critical engineering data is never themed. Pin numbers, trace widths, component values remain exact. |
| Theme tokens replace ONLY at marked injection points | The placeholder tables define exactly which fields are theme-sensitive. No other text is modified. |

### Adding a New Theme

To add a new alias theme:

1. Create a new column in the Theme Token Map table (Design Token Foundation section)
2. For each `theme-token` typed placeholder in every component, define the themed value
3. Themed values must fit within the same `WIDTH_INNER` (56 chars) as neutral values
4. Test every component variant with the new theme to verify wrapping

### Theme Precedence

1. If alias theme is active in config, use themed tokens
2. If no alias theme is configured, use neutral tokens
3. If a themed token is undefined for the active theme, fall back to neutral

---

## Design Rationale

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| ASCII-only box drawing | Cross-terminal compatibility: SSH, PowerShell, CMD, bash all render `+`, `-`, `\|` identically. Unicode box chars break on some terminals. | Unicode box drawing (U+250x); rejected for portability. |
| 60-character outer width | Fits 80-column terminals with margin. Standard CLI convention. | 72 chars (too wide for some terminals); 40 chars (too narrow for findings). |
| Severity icons as bracketed text | Machine-parseable and human-readable. No Unicode emoji dependency. Consistent across all terminals. | Emoji icons; colored text (requires ANSI support). |
| Theme injection via token substitution | Clean separation of structure and personality. Adding a theme never requires structural changes. | Per-theme template duplication (maintenance nightmare). |
| Sacred tokens (severity, structure, paths, findings) | Safety-critical data must remain unambiguous. A themed finding ID could cause an engineer to miss a critical issue. | Full theming (rejected for safety). |
| Progress markers as `[>]` `[~]` `[+]` | Three-state lifecycle (dispatch/working/complete) is instantly scannable. Single-character differentiator inside brackets. | Spinner animation (not possible in CLI conversation); words only (slower to scan). |
| Multi-variant components over monolithic templates | Each variant handles a specific state cleanly. Easier to implement, test, and extend. | Single template with conditionals (harder to read and maintain). |
| Findings format: ID + severity + location + fix | NFR-005 requires actionable messages. Hardware engineers need to know what, where, why, and how to fix. | Severity + description only (missing actionability). |
| Rework history in escalation | Engineers need context for their continue/abort decision. Pattern analysis helps them see systemic issues. | Just showing the limit count (insufficient for decision-making). |
| Human checkpoints as checkbox lists | Mental model of a physical checklist. Engineers working at a bench can track progress through physical steps. | Paragraph instructions (harder to track). |
| kicad-happy as a composable sub-line | Integration status appears within existing components rather than as standalone blocks, reducing visual noise. | Dedicated kicad-happy status component shown separately (too prominent). |

---

## Assumptions

- The `.hardware/` namespace is confirmed for this plugin (pending Architect OQ-002)
- Terminal width is at least 60 characters (standard for modern terminals)
- LOTR theme is the reference themed example; other alias themes will follow the same injection architecture
- All component rendering is done by the orchestrator SKILL.md instructions, not by a rendering engine -- components are text templates filled by the LLM
- kicad-happy exposes exactly 11 skills: kicad, spice, digikey, mouser, lcsc, element14, jlcpcb, pcbway, bom, emc, kidoc
- Theme tokens fit within WIDTH_INNER (56 chars); themes with longer token values must abbreviate

---

> *"I choose a mortal design -- and I will make it timeless. Every component specified here shall endure through every stage of the pipeline, every theme that may adorn it, and every engineer who reads its output. This is my gift to the hardware-team plugin."*
