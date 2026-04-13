---
name: hardware-flow
description: Pipeline orchestrator that coordinates the hardware delivery team through 8 stages (Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release) with sub-agent dispatch, validation gates, rework loops, human-execution stages, kicad-happy integration, state persistence, and self-learning memory. Triggers on phrases like "hardware pipeline", "run hardware", "hardware flow", "hw-setup", "start hardware project", "concept to production", "PCB pipeline", "hardware delivery", "resume hardware pipeline".
license: Apache License 2.0 - See repository LICENSE file
---

# Hardware Flow -- Pipeline Orchestrator

## Design Principle: Hardware Team Delivery with Validation Gates and Physical-World Integration

This skill is the ORCHESTRATOR. It coordinates the hardware delivery team through a
structured 8-stage pipeline but NEVER produces domain artifacts directly. All domain
work -- requirements, schematics, layout reviews, DFM reports, compliance packages,
test procedures -- is delegated to worker skills that operate as sub-agents with
isolated context.

> **Disclaimer -- AI Scope Limitations**: This pipeline coordinates AI-assisted design
> review and documentation. It does NOT replace physical testing, lab measurements,
> certified compliance testing, or professional engineering sign-off. Human-execution
> stages (Prototype, Pilot Run, Production Release) require physical work that AI
> cannot perform. All compliance outputs are pre-compliance assessments only -- formal
> certification requires accredited test labs.

### Core Principles

1. **Delegation, not execution (Prime Directive).** The orchestrator manages flow,
   routing, and validation. Worker skills (hw-product-owner, electrical-engineer,
   pcb-layout-engineer, manufacturing-engineer, compliance-engineer, test-engineer)
   produce ALL domain artifacts. Workers are invoked as sub-agents using the Agent tool.

   **The orchestrator NEVER writes domain content.** This is non-negotiable.
   Explicit anti-patterns (any of these is a Prime Directive violation):
   - Writing a requirements doc, schematic review, DFM report, compliance analysis,
     or test procedure with Write or Edit because "it's simple"
   - Drafting a short artifact inline and saving it to skip an Agent dispatch
   - Writing a compound prompt that asks one sub-agent to act as multiple roles
     (see "One Role = One Sub-Agent" below)
   - Collapsing two review passes into one by pasting prior findings into
     the next reviewer's prompt
   - Forwarding artifact content (not paths) between sub-agents through the
     orchestrator

   The orchestrator's ONLY write paths are `.hardware/state.md`,
   `.hardware/state.tmp.md`, `.hardware/config.yml`, `.hardware/memory/**`, and
   `stage-summary.md` files under each stage namespace. Everything else is
   produced by a dispatched sub-agent.

2. **Multi-perspective validation.** Every artifact is validated by MULTIPLE roles
   (Team Definition of Done) before a stage gate passes. No single perspective gates
   quality -- the team decides collectively.

3. **Self-correction with bounds.** When validation fails, the pipeline corrects itself
   by routing feedback to the responsible agent. Every correction loop has a counter
   (max 3 iterations) to prevent infinite cycles.

4. **Dynamic escalation.** Escalation to the human can happen at ANY point -- not just
   at scheduled checkpoints. Low confidence, repeated failures, deadlocks, and
   cross-cutting conflicts all trigger escalation immediately.

5. **Learning from every run.** The pipeline writes memory files after every execution
   (including aborts). Past lessons are loaded at the start of each run and passed to
   agents as context, so the pipeline improves over time.

6. **Human-physical integration.** Three stages (Prototype, Pilot Run, Production
   Release) involve physical work that AI cannot perform. The pipeline prepares
   documentation, pauses for human action, then validates results on resumption.

7. **Context isolation.** Worker sub-agents receive ONLY the upstream artifacts and
   lessons relevant to their task. The orchestrator selects the relevant subset --
   agents do not see the full pipeline state.

8. **kicad-happy consumption, not reimplementation.** Hardware roles invoke kicad-happy
   skills for component sourcing, fabrication validation, analysis, and documentation.
   The orchestrator does NOT invoke kicad-happy directly -- role skills own that decision.

---

## Phase 0: Setup Wizard

Before the pipeline executes, check for project configuration:

### State Detection (Resume Check)

Before checking config, check for an existing pipeline state:

1. **Check for `.hardware/state.md`** in the current working directory.
2. **If state exists with `status: in_progress` or `status: paused`**:
   - Read the YAML frontmatter to load pipeline state.
   - Announce: `> Existing pipeline found: [pipeline_id], started [date], last completed Stage [N] ([name]). Currently at Stage [N+1].`
   - **Validate**: verify all artifact files in the `artifacts` map exist on disk. If any are missing, announce which and offer: Restart from that stage / Abandon.
   - **Semantic validation**: current_stage in range 1-8, not in stages_completed, no gaps in completed+skipped.
   - **Config divergence check**: compute SHA-256 of current `.hardware/config.yml` and compare against `config_hash` in state. If different, warn: "Config has changed since this pipeline started. Resume uses the original config snapshot. Choose Restart to apply new config."
   - Offer the user: **Resume** / **Restart** / **Abandon**
   - Resume: load config from snapshot file, skip completed stages, start at current_stage.
   - Restart: archive state file to `.hardware/archived/state-<timestamp>.md` (cap at 5, delete oldest), start fresh.
   - Abandon: delete state file, no pipeline runs.
3. **If state exists with `status: paused_dispatch_error`**:
   - Announce: `> Pipeline paused due to dispatch error at Stage [N]. Error: [error_type].`
   - Offer: **Retry** / **Restart** / **Abandon**
4. **If state exists with `status: aborted`**:
   - Announce: `> Aborted pipeline found from [date], stopped at Stage [N]. Artifacts from stages [list] are preserved.`
   - Offer: Resume / Restart / Abandon.
5. **If state exists with `status: completed`**: ignore (previous run finished normally).
6. **If no state file exists**: proceed to config check (normal flow).

### Config Check

1. **Check for `.hardware/config.yml`** in the current working directory.
2. **If config exists and is valid**:
   - Read the YAML configuration to load all project settings.
   - **Version check**: Compare `schema_version` to the current schema version (v1.0).
     If the config uses an older schema, apply defaults for missing keys and announce:
     `> Config upgraded from v[old] to v[current]. New settings applied with defaults: [list]`
   - Announce: `> Config loaded from .hardware/config.yml (v[version])`
   - Apply settings: target_fab, compliance_regions, bom_budget, production_volume,
     board_layers, rework limits, gate_strictness, review config.
   - For any key missing from the config, use the default from `references/config-schema.md`.
   - Proceed to Phase 1.

3. **If config exists but has invalid fields**:
   - Warn per-field with expected type/values. Use defaults for invalid fields.
   - Never fail the pipeline due to config errors.

4. **If no config exists**:
   - **STOP. Do NOT proceed to Phase 1.** The setup wizard MUST run before the pipeline can execute.
   - Run the setup wizard. Reference `references/setup-wizard.md` for the full protocol.
   - The wizard asks 9 questions sequentially:
     - Q1: Project name
     - Q2: Target fabrication house (jlcpcb / pcbway / other)
     - Q3: Target compliance regions (FCC, CE, UL, none)
     - Q4: BOM budget target (USD per unit, or no limit)
     - Q5: Production volume target (prototype / small-batch / production)
     - Q6: Board layer count (1 / 2 / 4 / 6 / 8+)
     - Q7: Minimum kicad-happy version (default: >=1.2.0)
     - Q8: Rework iteration limit per path (default: 3)
     - Q9: Total rework limit per pipeline run (default: 10)
   - Generate `.hardware/config.yml` with schema_version: "1.0"
   - Create directory structure: `.hardware/`, `.hardware/memory/`, `.hardware/artifacts/`
   - Validate config against schema
   - After the wizard completes, `.hardware/config.yml` MUST exist before proceeding.

5. **User can re-run the wizard at any time** with the `hw-setup` command.

### Quick-Start Mode

If the user says "quick start", "quick setup", or "just get started", run a 3-question wizard:

1. **What is your project name?**
2. **Target fab house?** (jlcpcb / pcbway / other)
3. **How strict?** Hobby (minimal gates) / Standard (balanced) / Production (full)

All other settings use smart defaults from `references/config-schema.md` based on the
strictness level. Generate `.hardware/config.yml` and proceed.

---

## Phase 1: Pre-Flight Checks

After config is loaded, perform pre-flight validation before pipeline execution.

1. **kicad-happy availability**: Check that kicad-happy skills are available.
   - All 11 available: proceed silently.
   - Partial: warn about missing skills. Pipeline may degrade at affected stages.
   - None: BLOCK pipeline start. kicad-happy is required.

2. **Project type detection**: Determine project type from config and user context.

   | Type | Key Signals | Stage Routing |
   |------|-------------|---------------|
   | Hobby / 1-Layer Prototype | `production_volume: prototype`, `board_layers: 1-2`, no compliance | DFM minimal, Compliance skip, Pilot Run skip, Prod Release skip |
   | Small-Batch (10-1000) | `production_volume: small-batch` | Full pipeline, Pilot Run optional |
   | Production (1000+) / Certified | `production_volume: production`, compliance regions set | Full pipeline + extended yield analysis |

3. **Memory load**: Check for `.hardware/memory/index.md` and load hot lessons.

4. **Announce pipeline start**:
   ```
   HARDWARE PIPELINE: [project_name]
   Config: .hardware/config.yml (v[schema_version])
   Fab: [target_fab] | Regions: [compliance_regions] | Budget: $[bom_budget]
   kicad-happy: [N]/11 skills available
   Memory: [N] lessons loaded

   Stages: Concept > Schematic > Layout > Prototype >
           DFM/DFA > Compliance > Pilot Run > Production Release
   [Skipped: stages that will be skipped based on project type]
   ```

---

## Phase 2: Memory Retrieval

Memory uses a **tiered chunked system** -- read only what's needed, never everything.
See `references/memory-protocol.md` for the full architecture.

### At Pipeline Start (this phase)

1. Check if `.hardware/memory/index.md` exists in the current working directory.
2. If yes, read **only** `memory/index.md` (the routing index, ~50 lines max).
   This tells you:
   - **Stage health**: which stages have low first-try pass rates (flag for extra attention)
   - **Hot lessons**: top 5 most impactful lessons (inject into ALL agent prompts)
   - **Topic pointers**: which chunk files to read and when
3. Do NOT read stage chunks yet -- those are loaded per-stage in Phase 3 (Step 2).
4. If no memory directory exists, proceed without lessons. The first run establishes
   the baseline.

### What Gets Injected Into Every Agent Prompt

```
Lessons from past runs on this project (apply these):
- [Hot Lesson 1 -- from index.md]
- [Hot Lesson 2 -- from index.md]

For each injected lesson, report its disposition in your output:
  MEMORY_APPLIED: <MEM-ID> -- <how the lesson influenced a decision>
  MEMORY_NOTED: <MEM-ID> -- <reason it was acknowledged but not applicable>
```

---

## Phase 3: Pipeline Execution Protocol

> **SELF-RECOVERY**: If you find yourself idle after agents have returned results,
> re-read `.hardware/state.md` to determine `current_stage` and immediately resume
> the pipeline protocol at the appropriate step. Do not wait for user input.

### One Role = One Sub-Agent (Prime Directive Corollary)

Every reviewer, validator, or evaluator role is dispatched as a **separate** Agent
tool call. One role = one sub-agent invocation. Never collapse multiple roles into a
single compound prompt.

- A review board of 4 reviewers = 4 Agent calls (dispatched in parallel).
- A DoD with 3 validators = 3 Agent calls (dispatched in parallel).
- A rework assessment = separate Agent call with rework context.

Violations (to avoid):
- "You are EE Reviewer. Also act as MfgE Reviewer." (compound multi-role prompt)
- Listing several `ROLE:` declarations in one Agent prompt.
- Asking a single sub-agent to produce both the artifact AND review it.
- Pasting prior-reviewer findings into a new reviewer's prompt to "save a call".

### Two-Channel Communication

The orchestrator uses two communication channels:

- **Signal channel**: STATUS, file paths, summaries (<200 chars) -- flows through orchestrator for routing decisions.
- **Artifact channel**: file contents -- NEVER flows through orchestrator. Sub-agents write files to disk. Downstream agents read files by path. The orchestrator passes paths, not content.

**The rule**: If information is longer than 200 characters, it belongs in a file. The orchestrator passes the file path. The downstream agent reads the file. The orchestrator NEVER reads an artifact and pastes its content into another agent's prompt.

### For Each Active Stage, Execute This Protocol

#### Step 1: Announce

Output a stage header with the stage number, name, execution mode, and purpose.

```
## Stage [N]: [NAME] [[AI-execution | Human-execution]]
Purpose: [one-line description of what this stage produces]
Roles: [primary role(s)]
kicad-happy skills: [list if applicable, else "none"]
```

#### Step 2: Load Stage Memory

Read the **stage-specific chunk** from `.hardware/memory/lessons-<stage>.md` (e.g.,
`lessons-schematic.md` for the Schematic stage). This file contains lessons specific
to this stage (~100 lines max).

Additionally, load relevant **cross-cutting chunks** based on context:
- If this stage has a **human checkpoint** --> also read `lessons-general.md`
- If this stage's **first-try pass rate is <80%** (from index.md) --> also read `lessons-rework.md`

**Total reads per stage: 1-2 chunk files, never more.**

Combine the stage lessons + hot lessons (from Phase 2) into the agent prompt context.

#### Step 3: Load Stage Definition

Read the stage sub-flow from `references/pipeline-stages.md`. This defines the
specific agents to invoke, their task types, and the sub-flow sequence.

#### Step 4: Invoke Primary Agent

Construct the prompt using the Agent Invocation Template. The template requires:

- **SKILL**: the hardware-team role skill to invoke (e.g., `hardware-team:electrical-engineer`)
- **TASK_TYPE**: from the stage definition (e.g., `review`, `analyze`, `prepare`)
- **ROLE**: the specific role within the skill
- **INPUT ARTIFACTS**: file paths to upstream artifacts -- NOT content. The sub-agent reads artifacts from disk.
- **MEMORY LESSONS**: hot lessons from index.md + stage lessons loaded in Step 2
- **OUTPUT**: the namespaced output path (e.g., `.hardware/artifacts/02-schematic/schematic-review.md`)

The sub-agent writes its artifact to the output path and responds with a signal block:
```
STATUS: {DONE | NOT_DONE | CODE_COMPLETE}
ARTIFACT: {output_file_path}
SUMMARY: {one sentence, max 200 characters}
```

After the agent responds, verify the signal:
1. Check for `SKILL_LOADED: {expected_skill_name}` in the first line.
2. If present: extract STATUS, ARTIFACT, SUMMARY from the signal block.
3. If absent: retry once with the same prompt. If second attempt fails, escalate to user.

#### Step 4.5: Delegation Self-Check

Before using Write or Edit on any file in `.hardware/artifacts/`: STOP.
Ask: "Am I writing domain content (a requirements doc, review, analysis, report,
test procedure, or compliance package)?"

- If YES: do NOT write. Construct an Agent Invocation Template and delegate to the
  appropriate skill. The sub-agent writes the artifact.
- If NO (writing stage-summary.md, state.md, or routing metadata): proceed.

**Rejected justifications.** The following are NOT valid reasons to bypass delegation:

- "but it's simple" / "but it's just a short doc"
- "but I already know the answer from kicad-happy output"
- "but the sub-agent would just produce the same thing"
- "but it's faster if I do it"
- "but no sub-agent exists for this artifact type" -- escalate to the user

#### Step 5: Invoke Supporting Agents

If the stage runs at full depth, invoke additional worker sub-agents for supplementary
work. Each supporting agent receives its own Agent Invocation Template with file paths
to upstream artifacts.

When supporting agents are independent, dispatch them in PARALLEL using multiple Agent
tool calls in a single message.

When a required supporting agent fails, retry up to 2 times. When an optional supporting
agent fails, log the gap and proceed.

#### Step 6: Run Design Review Board (where applicable)

At key transitions (post-Schematic, post-Layout), the Design Review Board activates:
independent parallel reviews from EE, PCB Layout, MfgE, and CompE. Findings are
aggregated and deduplicated. See `references/gate-framework.md` for the full protocol.

#### Step 7: Team DoD Validation

Run the Team Definition of Done protocol for this stage.

Spawn ALL validators in parallel using multiple Agent tool calls. Each validator receives ONLY:
- The artifact file path (validator reads it from disk)
- Its role-specific gate criteria (from `references/quality-gates.md`)

No validator sees another validator's output. Each writes to its own namespaced path
(e.g., `.hardware/artifacts/{NN}-{stage}/dod/{role}-review.md`).

Collect signals from all validators before evaluating:
- ALL validators must return STATUS: DONE for the stage to complete
- If any vote NOT_DONE, trigger self-correction: pass the artifact file path + all
  NOT_DONE findings file paths to the primary agent for revision
- Max 3 DoD validation rounds per stage (configurable via config)
- If still NOT_DONE after 3 rounds, trigger dynamic escalation

**CONTINUATION DIRECTIVE**: After collecting all validator signals, IMMEDIATELY proceed
to evaluate results and advance to Step 8. Do not wait for user input.

#### Step 8: Verify Artifact and Update State

1. Verify the artifact file exists on disk by checking the ARTIFACT path from the signal block.
   If missing, retry the primary agent once.

2. Write `stage-summary.md` to `.hardware/artifacts/{NN}-{stage}/stage-summary.md`.
   This is routing metadata, not domain content.

3. Update pipeline state in `.hardware/state.md` using atomic write (write to `state.tmp.md`,
   then rename to `state.md`):
   - Update `current_stage` to the NEXT stage number
   - Add the just-completed stage to `stages_completed`
   - Add the artifact file path to the `artifacts` map
   - Update `last_updated` timestamp
   - Record gate results

#### Step 9: Check for Human Checkpoint (Human-Execution Stages)

For human-execution stages (Prototype, Pilot Run, Production Release), follow the
three-phase pattern:

**Phase A: GATE-IN (AI generates preparation artifacts)**
- Sub-agent produces: ordering packages, test procedures, checklists
- Artifacts saved to `.hardware/artifacts/<stage-name>/`
- Output presented to user with structured action items

**Phase B: HUMAN-ACTION (pipeline pauses)**
- Pipeline state transitions to: `PAUSED_AWAITING_HUMAN`
- User receives: preparation artifacts + numbered action items
- User performs physical work (ordering, assembly, testing)
- User confirms: `"<stage> complete"` or `"<stage> failed: <description>"`

**Phase C: GATE-OUT (AI evaluates completion)**
- On "complete": gate evaluates, pipeline advances
- On "failed: <description>": rework triggered (see Rework Loops)

#### Step 10: Advance

Move to the next active stage in the routing matrix.

**STATE ANCHOR**: "Entering Stage [N+1]: [NAME]. Previous stage [N] complete. CONTINUING pipeline protocol from Step 1."

Then IMMEDIATELY execute Step 1 of the next stage. Do not stop between stages.

---

## Stage Definitions

> **Authoritative source**: `references/pipeline-stages.md` is the single source of truth
> for stage sub-flows, agent invocation details, artifact output paths (namespaced), and
> DoD Validator Dispatch Templates. The summaries below provide routing and orchestration
> context only. When executing a stage, ALWAYS load the full definition from
> `references/pipeline-stages.md`.

### Stage 1: Concept

**Execution mode**: AI-execution
**Purpose**: Capture hardware requirements, constraints, regulatory landscape, initial BOM budget.
**Primary agent**: HW Product Owner (hw-product-owner skill)
**Upstream artifacts**: none (first stage)
**kicad-happy skills**: none
**DoD validators**: HW Product Owner, Electrical Engineer
**Human checkpoint**: none
**Max self-correction**: 2 iterations
**Output**:
  - `.hardware/artifacts/01-concept/requirements.md`
  - `.hardware/artifacts/01-concept/constraints.md`
  - `.hardware/artifacts/01-concept/regulatory-scan.md`
  - `.hardware/artifacts/01-concept/bom-budget.md`

---

### Stage 2: Schematic

**Execution mode**: AI-execution
**Purpose**: Schematic design review, component selection, SPICE simulation, firmware interface docs.
**Primary agent**: Electrical Engineer (electrical-engineer skill)
**Supporting**: HW Product Owner (trade-off decisions)
**Upstream artifacts**: `.hardware/artifacts/01-concept/*`
**kicad-happy skills**: kicad, spice, digikey, mouser, lcsc, element14
**Gate**: Schematic Review Gate (multi-reviewer iterative pattern)
  - Multiple reviewers with forced-find prompting
  - 7 categories: power integrity, signal integrity, component derating, pull-ups/pull-downs, decoupling, voltage level compatibility, thermal
  - Deduplication across reviewers
  - Number of review passes: configurable via `review.schematic_review_passes` (default: 2)
**DoD validators**: Electrical Engineer, HW Product Owner, PCB Layout Engineer
**Design Review Board**: Yes (post-Schematic)
**Human checkpoint**: none
**Max self-correction**: 3 iterations
**Output**:
  - `.hardware/artifacts/02-schematic/schematic-review.md`
  - `.hardware/artifacts/02-schematic/component-rationale.md`
  - `.hardware/artifacts/02-schematic/simulation-results.md`
  - `.hardware/artifacts/02-schematic/firmware-interface.md`

---

### Stage 3: Layout

**Execution mode**: AI-execution
**Purpose**: PCB layout review, routing analysis, DRC validation.
**Primary agent**: PCB Layout Engineer (pcb-layout-engineer skill)
**Upstream artifacts**: `.hardware/artifacts/02-schematic/*`
**kicad-happy skills**: kicad
**Gate**: DRC Gate
  - Consumes kicad-happy:kicad for DRC parsing
  - Fab-specific rules based on `target_fab` config
**DoD validators**: PCB Layout Engineer, Electrical Engineer, Manufacturing Engineer
**Design Review Board**: Yes (post-Layout)
**Human checkpoint**: none
**Max self-correction**: 3 iterations
**Output**:
  - `.hardware/artifacts/03-layout/layout-review.md`
  - `.hardware/artifacts/03-layout/routing-analysis.md`
  - `.hardware/artifacts/03-layout/drc-results.md`

---

### Stage 4: Prototype

**Execution mode**: Human-execution (gate-in / human-action / gate-out)
**Purpose**: Generate ordering package, test procedures; human orders, assembles, and tests prototype.
**Primary agent**: Test Engineer (test-engineer skill)
**Supporting**: Electrical Engineer (bring-up support)
**Upstream artifacts**: `.hardware/artifacts/02-schematic/*`, `.hardware/artifacts/03-layout/*`
**kicad-happy skills**: jlcpcb or pcbway (ordering package)
**Gate**: Human Confirmation Gate
**DoD validators**: Test Engineer, Electrical Engineer
**Human checkpoint**: YES -- pipeline PAUSES for human physical work
**Max self-correction**: N/A (human-driven)
**Output**:
  - `.hardware/artifacts/04-prototype/ordering-package.md`
  - `.hardware/artifacts/04-prototype/test-procedure.md`
  - `.hardware/artifacts/04-prototype/test-fixture-requirements.md`

---

### Stage 5: DFM/DFA

**Execution mode**: AI-execution
**Purpose**: Design for Manufacturing and Design for Assembly review, yield assessment, BOM validation.
**Primary agent**: Manufacturing Engineer (manufacturing-engineer skill)
**Upstream artifacts**: `.hardware/artifacts/03-layout/*`, `.hardware/artifacts/04-prototype/*` (if available)
**kicad-happy skills**: jlcpcb or pcbway, bom
**Gate**: DFM Gate + BOM Gate (evaluated together)
  - DFM: fab-specific rules (trace/space, via, mask, clearance)
  - BOM: cost vs budget, availability, lifecycle, second-source
**DoD validators**: Manufacturing Engineer, PCB Layout Engineer, HW Product Owner
**Human checkpoint**: none
**Max self-correction**: 3 iterations
**Output**:
  - `.hardware/artifacts/05-dfm-dfa/dfm-report.md`
  - `.hardware/artifacts/05-dfm-dfa/dfa-report.md`
  - `.hardware/artifacts/05-dfm-dfa/yield-assessment.md`
  - `.hardware/artifacts/05-dfm-dfa/bom-validation.md`

**Routing note**: For `production_volume: prototype` projects, DFM runs at minimal depth
(basic DRC only, no extended yield analysis).

---

### Stage 6: Compliance

**Execution mode**: AI-execution
**Purpose**: EMC pre-compliance analysis, safety assessment, environmental compliance, regulatory documentation.
**Primary agent**: Compliance Engineer (compliance-engineer skill)
**Upstream artifacts**: `.hardware/artifacts/02-schematic/*`, `.hardware/artifacts/03-layout/*`, `.hardware/artifacts/05-dfm-dfa/*`
**kicad-happy skills**: emc, kidoc
**Gate**: Compliance Gate
  - Per-region checklist based on `compliance_regions` config
  - Evidence-linked requirements
**DoD validators**: Compliance Engineer, Electrical Engineer, Manufacturing Engineer
**Human checkpoint**: none
**Max self-correction**: 3 iterations
**Output**:
  - `.hardware/artifacts/06-compliance/emc-report.md`
  - `.hardware/artifacts/06-compliance/safety-analysis.md`
  - `.hardware/artifacts/06-compliance/environmental-checklist.md`
  - `.hardware/artifacts/06-compliance/compliance-package.md`

**Routing note**: Skipped for `production_volume: prototype` projects with no compliance
regions configured. This pipeline produces pre-compliance assessments only -- formal
certification requires accredited test labs and is outside AI scope.

---

### Stage 7: Pilot Run

**Execution mode**: Human-execution (gate-in / human-action / gate-out)
**Purpose**: Manufacturing transfer package, production test procedures, yield targets; human runs pilot batch.
**Primary agent**: Manufacturing Engineer (manufacturing-engineer skill)
**Supporting**: Test Engineer (production test procedures)
**Upstream artifacts**: `.hardware/artifacts/05-dfm-dfa/*`, `.hardware/artifacts/06-compliance/*`
**kicad-happy skills**: kidoc, bom
**Gate**: Human Confirmation Gate
**DoD validators**: Manufacturing Engineer, Test Engineer
**Human checkpoint**: YES -- pipeline PAUSES for human physical work
**Max self-correction**: N/A (human-driven)
**Output**:
  - `.hardware/artifacts/07-pilot-run/manufacturing-transfer.md`
  - `.hardware/artifacts/07-pilot-run/production-test-procedure.md`
  - `.hardware/artifacts/07-pilot-run/yield-targets.md`

**Routing note**: Skipped for `production_volume: prototype`. Optional for small-batch.

---

### Stage 8: Production Release

**Execution mode**: Human-execution (gate-in / human-action / gate-out)
**Purpose**: Final production checklist, final BOM, compliance package, release documentation; human initiates production.
**Primary agent**: Manufacturing Engineer (manufacturing-engineer skill)
**Upstream artifacts**: all prior artifacts
**kicad-happy skills**: kidoc, bom
**Gate**: Final Gate (all artifacts complete, all gates passed)
**DoD validators**: Manufacturing Engineer, HW Product Owner, Compliance Engineer, Test Engineer
**Human checkpoint**: YES -- pipeline PAUSES for human physical work
**Max self-correction**: N/A (human-driven)
**Output**:
  - `.hardware/artifacts/08-production-release/production-checklist.md`
  - `.hardware/artifacts/08-production-release/final-bom.md`
  - `.hardware/artifacts/08-production-release/compliance-package.md`
  - `.hardware/artifacts/08-production-release/release-documentation.md`

**Routing note**: Skipped for `production_volume: prototype`. Minimal for small-batch
(BOM + ordering docs only).

---

## Stage Routing Matrix

Based on the detected project type, determine which stages execute and at what depth.

| Stage | Hobby / Prototype | Small-Batch (10-1000) | Production (1000+) / Certified |
|-------|-------------------|----------------------|-------------------------------|
| 1. Concept | Full | Full | Full |
| 2. Schematic | Full | Full | Full |
| 3. Layout | Full | Full | Full |
| 4. Prototype | Full | Full | Full |
| 5. DFM/DFA | Minimal (basic DRC only) | Full | Full + extended yield analysis |
| 6. Compliance | Skip (no regulatory) | Standard (FCC/CE as configured) | Full (all configured regions + safety) |
| 7. Pilot Run | Skip | Optional | Full |
| 8. Production Release | Skip | Minimal (BOM + ordering docs) | Full (manufacturing transfer package) |

### Depth Definitions

- **Full**: All agents invoked, all gates evaluated, full DoD validation, max 3
  self-correction iterations.
- **Minimal**: Primary agent only, blocking criteria only, reduced DoD (primary + 1
  reviewer), max 2 self-correction iterations.
- **Standard**: Full gate evaluation for configured regions. No extended analysis.
- **Optional**: User prompted whether to execute. If skipped, no gate penalty.
- **Skip**: Stage does not execute. Pipeline advances to the next active stage.
  Downstream stages receive whatever upstream artifacts are available.

**CRITICAL**: Minimal and Skip are DIFFERENT. Minimal stages execute with reduced
ceremony. Skip stages do not execute at all. Never conflate them. If the routing
matrix says "minimal" for a stage, that stage MUST run and MUST produce an artifact.

---

## Rework Loops

The pipeline is a Directed Acyclic Graph (DAG) with controlled backward edges. Rework
does NOT create cycles -- it is a bounded backward jump with re-validation of all
downstream gates.

### Defined Rework Paths

| Rework Path | Trigger Examples |
|---|---|
| Prototype --> Schematic | Fundamental circuit error discovered during bring-up |
| Prototype --> Layout | Routing or thermal issue revealed by prototype |
| DFM/DFA --> Layout | DFM violation requires layout change |
| DFM/DFA --> Schematic | Component unavailable at target fab, needs substitution |
| Compliance --> Schematic | EMC failure requires filtering/shielding component redesign |
| Compliance --> Layout | EMC failure requiring layout-specific changes (ground plane, trace rerouting) |
| Pilot Run --> DFM/DFA | Assembly yield issue requires DFM adjustment |
| Pilot Run --> Schematic | Circuit-level issue revealed by production conditions |

### Termination Conditions

| Condition | Default | Config Key | Behavior |
|---|---|---|---|
| `max_rework_iterations` | 3 | `rework.max_rework_iterations` | Per individual rework path. When path X-->Y triggers for the (N+1)th time, pipeline PAUSES and escalates to human. |
| `max_total_reworks` | 10 | `rework.max_total_reworks` | Across ALL paths in a single pipeline run. When total exceeds limit, pipeline PAUSES and escalates to human. |

Escalation message includes: (a) which limit was hit (per-path or total), (b) rework
count per path, (c) cumulative rework history, (d) recommendation for human intervention.
User options: `continue` (one more iteration), `abort` (stop pipeline, save state),
`override limit N` (raise the limit).

### Rework Execution Semantics

1. Pipeline sets `current_stage` to target stage
2. Target stage sub-agent receives: original artifacts + rework reason + specific issue description
3. Target stage re-executes (full stage, not just gate)
4. Target stage gate re-evaluates
5. ALL downstream gates between target and source are re-validated (gate re-evaluation, not full stage re-execution)
6. Rework event logged to `.hardware/state.md` with: timestamp, source stage, target stage, trigger reason, resolution, iteration count, total rework count

When rework triggers from a human-execution stage:
1. Human checkpoint is INVALIDATED (status: PENDING --> INVALIDATED)
2. Existing preparation artifacts are ARCHIVED (moved to `archived/run-N/`, never deleted)
3. Rework path determined using the rework path table above
4. Target stage re-executes with failure description as additional context

---

## Sub-Agent Dispatch Failure Handling

A dispatch failure is distinct from a gate failure. A gate failure means the stage
executed but produced unsatisfactory results. A dispatch failure means the stage could
not execute at all.

**Protocol:**

1. **Detect**: The orchestrator wraps every Agent tool dispatch in error detection.
2. **Retry once**: The orchestrator retries the dispatch exactly once with the same prompt.
3. **If retry fails -- PAUSE**: The pipeline transitions to `PAUSED_DISPATCH_ERROR` with:
   - `dispatch_error.stage`: The stage number that failed
   - `dispatch_error.role`: The role skill being dispatched
   - `dispatch_error.error_type`: One of `TIMEOUT`, `CONTEXT_OVERFLOW`, `MODEL_ERROR`, `UNKNOWN`
   - `dispatch_error.error_detail`: The raw error message
   - `dispatch_error.retry_attempted`: true
   - `dispatch_error.timestamp`: ISO 8601
4. **User options**: Retry / Skip (non-critical stages only) / Abort

---

## kicad-happy Integration

Hardware roles invoke kicad-happy skills internally via the Skill tool using the
`kicad-happy:<skill>` syntax. The orchestrator does NOT invoke kicad-happy directly.

### Role-to-kicad-happy Mapping

| Hardware Role | kicad-happy Skills Consumed | Usage Context |
|---|---|---|
| Electrical Engineer | `kicad`, `spice`, `digikey`, `mouser`, `lcsc`, `element14` | Schematic analysis, simulation, component sourcing |
| PCB Layout Engineer | `kicad` | PCB analysis, DRC parsing, layout review |
| Manufacturing Engineer | `jlcpcb`, `pcbway`, `bom`, `kidoc` | DFM rules, BOM management, manufacturing documentation |
| Compliance Engineer | `emc`, `kidoc` | EMC pre-compliance analysis, regulatory documentation |
| Test Engineer | `kicad` (optional) | Test point locations, connector pinouts, debug interfaces |
| HW Product Owner | (none directly) | Uses role outputs for trade-off decisions |

### Error Handling: kicad-happy Not Available

When a sub-agent attempts to invoke a kicad-happy skill that is not installed:

1. Sub-agent reports: `SKILL_UNAVAILABLE: kicad-happy:<skill>`
2. Orchestrator logs the error in pipeline state
3. Pipeline does NOT crash -- it degrades gracefully
4. Gate evaluates based on available data

### Reimplementation Guard

A capability is reimplemented if a hardware-team role performs an action that would
produce the same output as invoking a kicad-happy skill, without invoking that skill.

**IS reimplementation** (prohibited):
- Parsing `.kicad_sch` files to extract BOM data instead of invoking `kicad-happy:kicad`
- Querying DigiKey API directly instead of invoking `kicad-happy:digikey`
- Implementing EMC rule checks from scratch instead of invoking `kicad-happy:emc`

**IS NOT reimplementation** (permitted):
- Domain knowledge in SKILL.md that guides when/how to invoke kicad-happy
- Interpreting kicad-happy output and making engineering judgments
- Combining outputs from multiple kicad-happy skills into a unified report

### Output Contract Validation

Each role sub-agent validates kicad-happy output structure before processing.
See `references/kicad-integration.md` for the full contract specification.

If validation fails, the sub-agent reports `CONTRACT_MISMATCH` and continues with
degraded capability (same as SKILL_UNAVAILABLE).

---

## Team Definition of Done Protocol

DoD validation is the final checkpoint before a stage advances. It runs AFTER all
stage work has completed. DoD is NON-NEGOTIABLE -- no stage advances without ALL
validators saying DONE (unless the human overrides via escalation).

### Execution Steps

1. **Identify validators.** Each stage has named validators defined in the stage
   definitions above and detailed in `references/quality-gates.md`.

2. **Spawn validator sub-agents.** The validator reads the artifact from the file
   path -- the orchestrator NEVER pastes artifact content into validator prompts.

3. **Evaluate votes.** ALL validators must return DONE for the stage to complete.

4. **Self-correction on NOT_DONE.** If any validator returns NOT_DONE:
   - Aggregate ALL findings from all validators.
   - Re-invoke the primary agent with: original context + current artifact path +
     feedback file paths.
   - The primary agent must address every finding without regressing on passing criteria.
   - Re-run ALL validators (not just the ones that failed -- revisions can introduce
     regressions).

5. **Track iteration count.** Maximum 3 DoD validation rounds per stage.

6. **Escalate on exhaustion.** After 3 rounds with unresolved findings, trigger
   dynamic escalation with all attempts shown.

### Gate Strictness (from config)

| Level | Blocking Criteria | Pass-Through |
|-------|------------------|--------------|
| `strict` | Critical, Major, AND Minor findings | None |
| `standard` | Critical and Major findings | Minor findings (logged) |
| `relaxed` | Critical findings only | Major (logged as warning), Minor (logged) |

---

## Dynamic Escalation Protocol

Escalation is not limited to scheduled human checkpoints. The orchestrator monitors
for escalation conditions continuously.

### Escalation Triggers

| Trigger | Condition |
|---------|-----------|
| Repeated DoD failure | Same criterion fails across 3 consecutive validation cycles |
| Decision deadlock | Two roles produce contradictory findings that cannot be reconciled |
| Rework limit hit | Per-path or total rework limit exceeded |
| Dispatch failure | Sub-agent dispatch fails after retry |
| No correction progress | Self-correction produces no meaningful change |

### Escalation Format

```
## Escalation: [Stage Name] -- [Brief Issue Description]

**Issue**: [What went wrong, 1-2 sentences]
**Attempts**: [What was tried and how many iterations]
**Current state**: [What passes, what still fails]
**Findings**: [Aggregated feedback from most recent cycle]

**Options**:
1. **Provide guidance**: [What input would unblock progress]
2. **Override**: Proceed despite the issue (risk: [specific risk])
3. **Redirect**: Try a different approach
4. **Abort**: Halt pipeline, preserve all artifacts
```

---

## State Management

### State File (.hardware/state.md)

Pipeline state is persisted as a Markdown file with YAML frontmatter. The orchestrator
reads and writes this file to track pipeline progress, gate results, rework history,
and artifact registry.

See architecture Section 7.1 for the complete state file schema including:
- `pipeline_id`, `status`, `started`, `last_updated`, `current_stage`
- `stages_completed`, `stages_skipped`
- `config_hash` (SHA-256 for divergence detection)
- `config_snapshot_file` (full config preserved at start)
- `artifacts` registry (path -> stage metadata)
- `gates` results (ordered by execution)
- `rework_history` (per-path counts and events)
- `checkpoints` (human-execution stage status)

### State Operations

| Operation | When | What |
|---|---|---|
| **Create** | Pipeline start | Initialize with pipeline_id, config_hash, status=in_progress |
| **Update (stage complete)** | Stage completion | Add stage to stages_completed, register artifacts, record gate results |
| **Update (rework)** | Rework triggered | Add rework event, update current_stage |
| **Pause** | Human-execution stage | Set status=paused, save checkpoint entry |
| **Resume** | Session restart | Load state, validate artifacts exist, continue from current_stage |
| **Complete** | All stages done | Set status=completed |
| **Abort** | User aborts or escalation | Set status=aborted, preserve all artifacts |

### Staleness Detection

When a pipeline is paused, the SessionStart hook performs staleness detection:

- **Always**: Display paused status with age.
- **Warning threshold** (default 7 days, config: `pipeline.staleness_warning_days`):
  Warn that config or project files may have drifted.
- **Critical threshold** (default 30 days, config: `pipeline.staleness_critical_days`):
  Strongly recommend Restart over Resume.

---

## Memory and Self-Learning

After pipeline completion (or abort), the orchestrator captures lessons learned.

### Memory Architecture

```
.hardware/memory/
+-- index.md                     # Memory index: entry IDs, tags, relevance scores
+-- lessons-concept.md           # Lessons from Concept stages
+-- lessons-schematic.md         # Lessons from Schematic stages
+-- lessons-layout.md            # Lessons from Layout stages
+-- lessons-prototype.md         # Lessons from Prototype stages
+-- lessons-dfm.md               # Lessons from DFM/DFA stages
+-- lessons-compliance.md        # Lessons from Compliance stages
+-- lessons-rework.md            # Cross-cutting rework pattern lessons
+-- lessons-general.md           # General project and process lessons
+-- lessons-archived.md          # Archived low-relevance entries
```

### Memory Tiering

| Tier | Criteria | Injection Point |
|---|---|---|
| **Always inject** | Lessons tagged with current stage AND same project | Sub-agent prompt (mandatory) |
| **Inject if relevant** | Lessons tagged with current stage from other projects, top 5 by relevance | Sub-agent prompt (if context allows) |
| **Available on request** | All other lessons | Sub-agent reads via Read tool if needed |

### Post-Pipeline Protocol

1. **Capture lessons.** Review pipeline execution: gates that failed, rework paths
   triggered, human escalations, findings from review gates.
2. **Write lessons to stage-specific files.** Each lesson to `lessons-<stage>.md`.
   Cross-cutting patterns go to `lessons-rework.md`.
3. **Update index.** Recalculate stage health stats, update hot lessons (top 5 by
   validation count), update topic pointers.
4. **Deduplicate.** When adding to a chunk:
   - Similar lesson exists: increment validated count, update last run.
   - Contradicts existing: note contradiction, remove after 3 consecutive contradictions.
   - Chunk exceeds 100 lines: prune least-validated, oldest entries.
5. **Archive.** Entries with relevance < 0.1 after 10+ runs move to `lessons-archived.md`.
6. **Memory influence tracking.** Update relevance scores based on MEMORY_APPLIED /
   MEMORY_NOTED signals from sub-agents.

---

## User Commands

| Command | Action |
|---------|--------|
| `hw-setup` | Run setup wizard to create/update `.hardware/config.yml` |
| `start` / "Run the hardware pipeline" | Start pipeline from Stage 1 |
| `status` | Show current pipeline state (stage, gates passed, rework count) |
| `resume` / "Resume hardware pipeline" | Resume a paused or in-progress pipeline |
| `skip` | Skip the current stage (only for non-critical stages; records in state) |
| `back [stage]` | Manually trigger rework to a specific stage |
| `approve` / "[stage] complete" | Approve a human-execution stage checkpoint |
| `abort` | Abort the pipeline, preserve all artifacts and write memory |
| `override` | Override a gate failure (records decision and risk in state) |
| `quick start` | Run abbreviated 3-question setup wizard |

---

## Guardrails

These guardrails prevent runaway execution and ensure predictable behavior:

- **Max self-correction iterations per stage**: 3 (or stage-specific override).
  Every correction loop has a counter. When exhausted, escalate.
- **Max DoD validation rounds per stage**: 3. After 3 rounds with unresolved
  findings, escalate.
- **No infinite loops.** Every loop has a bounded counter. The orchestrator tracks
  iteration counts and halts at limits.
- **Max rework iterations per path**: 3 (configurable). Per-path rework counter.
- **Max total reworks per run**: 10 (configurable). Global rework counter.
- **Write before advancing.** Artifacts are written to `.hardware/artifacts/` before
  the pipeline advances. Ensures artifacts survive aborts.
- **Context isolation.** Worker skills receive only upstream artifacts relevant to
  their task.
- **No skipping DoD.** Every active stage must pass team DoD validation before
  advancing. No bypass except human override.
- **Minimal stages MUST execute.** Minimal means reduced depth, not skip. Every
  stage marked "minimal" MUST produce an artifact and pass its DoD gate.
- **Preserve on abort.** If aborted, all artifacts are preserved. Memory file is
  written even for aborted runs.
- **State persistence after every stage.** Pipeline state written to
  `.hardware/state.md` after every stage gate using atomic write.
- **No stalling between steps or stages.** After every agent return, validator
  completion, or checkpoint approval, immediately proceed to the next step.
- **Orchestrator does not produce domain artifacts.** Apply the delegation
  self-check (Step 4.5) before any Write/Edit to `.hardware/artifacts/`.
- **One Role = One Sub-Agent.** Never combine multiple roles in a single Agent dispatch.
- **kicad-happy consumption, not reimplementation.** Never replicate kicad-happy
  functionality. Invoke the skill.

---

## Common Orchestrator Anti-Patterns

These patterns have caused real Prime Directive violations. Recognize them and
correct course immediately.

1. **"But it's simple" self-writing.** Drafting a short review or report inline.
   Even a one-paragraph artifact MUST be produced by a dispatched sub-agent.

2. **Compound multi-role prompts.** One Agent call asking the sub-agent to
   "act as EE reviewer, then also as MfgE reviewer". One role = one sub-agent.

3. **Collapsed review loops.** Running ONE reviewer and treating a single
   zero-finding pass as "converged". The iterative review requires either
   two consecutive clean loops or class-saturation.

4. **Pasting findings forward.** Reading a reviewer's findings and pasting
   content into the next reviewer's prompt. Pass file PATHS only.

5. **Skipping a "minimal" stage as if it were "skip".** Minimal means reduced
   depth. It MUST run and produce an artifact.

6. **Writing artifacts to satisfy a gate.** When a validator says the report
   needs a section, the orchestrator adds it inline. Wrong -- dispatch the
   primary agent with the feedback file path.

7. **Fusing validator with producer.** One Agent call that both produces the
   artifact and validates it. Validators are ALWAYS separate dispatches.

---

## Cross-Stage Artifact Flow

Each stage receives upstream artifacts from prior stages. The orchestrator selects
the relevant subset for each sub-agent (context isolation).

| Stage | Receives From Upstream |
|-------|------------------------|
| 1. Concept | (none -- first stage) |
| 2. Schematic | Concept artifacts |
| 3. Layout | Schematic artifacts |
| 4. Prototype | Schematic + Layout artifacts |
| 5. DFM/DFA | Layout + Prototype artifacts (if available) |
| 6. Compliance | Schematic + Layout + DFM/DFA artifacts |
| 7. Pilot Run | DFM/DFA + Compliance artifacts |
| 8. Production Release | All prior artifacts |

Exact artifact file paths for each stage are defined in `references/pipeline-stages.md`.

---

## References

These reference files provide detailed specifications. Load on demand via Read tool.

| File | Purpose |
|------|---------|
| `references/pipeline-stages.md` | 8-stage definitions with gates, agent invocation templates, artifact paths |
| `references/quality-gates.md` | Gate criteria, DoD validator dispatch templates, severity definitions |
| `references/config-schema.md` | Config schema v1.0 specification, validation rules, extension protocol |
| `references/rework-paths.md` | Rework DAG definition, path table, termination logic |
| `references/gate-framework.md` | Gate validation patterns, Design Review Board protocol |
| `references/memory-protocol.md` | Self-learning memory protocol, tiering, entry format, cleanup |
| `references/kicad-integration.md` | kicad-happy dispatch patterns, output contracts, error taxonomy |
| `references/setup-wizard.md` | hw-setup wizard flow, questions, defaults |
