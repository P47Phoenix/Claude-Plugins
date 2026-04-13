# Technical Architecture: hardware-team Plugin

**Role:** Solution Architect (Celebrimbor) | **Task:** design | **References:** architecture-patterns.md, c4-model.md, adr-template.md
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12
**Version:** 1.4 (revised per security review -- SEC-01 through SEC-06)

---

> "Let us forge something that will endure beyond the ages. Three services for the frontend layer under the sky. Seven for the data stores in their halls of stone. Eight stages for hardware projects doomed to iterate. One architecture to rule them all."

---

## Prior Art Analysis

### Step 1: Summary of Existing Specifications

The PRD (v1.1) and UX User Flows (v1.1) provide comprehensive specifications for a hardware delivery pipeline plugin. The following has been decided:

- **Plugin purpose**: An orchestration layer over kicad-happy skills for structured hardware development
- **Pipeline stages**: 8 stages (Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release)
- **Roles**: 6 Phase 1 roles (HW PO, EE, PCB Layout, MfgE, CompE, TestE)
- **kicad-happy integration**: Cross-plugin skill invocation via Skill tool (verified working)
- **Config namespace**: `.hardware/` (separate from `.delivery/`)
- **Rework termination**: max_rework_iterations=3 per path, max_total_reworks=10 per run
- **5 validation gates**: Schematic Review, DRC, BOM, DFM, Compliance
- **Human-execution stages**: gate-in/human-action/gate-out pattern for physical stages
- **Context loading**: Three-level pattern (metadata, SKILL.md, references)

### Step 2: Classification

| Spec Element | Classification | Rationale |
|---|---|---|
| 8-stage pipeline | Decision Already Made | PRD FR-002 specifies all 8 stages with execution mode classification |
| 6 Phase 1 roles | Decision Already Made | PRD Epic 2 specifies exact roles and their skill paths |
| `.hardware/` namespace | Decision Already Made | PRD Assumption 10 and OQ-002 confirm separation from `.delivery/` |
| Cross-plugin skill invocation | Decision Already Made | PRD verified working (C1, C10) |
| Rework termination limits | Decision Already Made | PRD C8 resolution specifies exact defaults |
| Config schema fields | Decision Already Made | PRD Story 1.4 specifies exact fields |
| Gate validation pattern | Decision Already Made | PRD mirrors delivery-flow Team DoD |
| Model tier requirements | Open Question | OQ-003 asks for per-role minimum tiers |
| Plugin internal structure | Open Question | Exact directory layout and skill decomposition |
| Iterative review agent configuration | Open Question | Number of passes, convergence criteria |
| State file format | Open Question | Exact schema for `.hardware/state.md` |
| Memory tier structure | Open Question | Exact memory file layout and retrieval strategy |

### Step 3: Building on Existing Design

This architecture builds on the PRD and UX flow specifications, filling the open questions while respecting all decisions already made.

---

## 1. Plugin Structure

> "This design must be forged with care. The Rings were beautiful and powerful, but a flaw in their making brought ruin. We shall not repeat that error in our architecture."

### 1.1 Directory Layout

```
hardware-team/                          # Top-level plugin directory
├── SKILL.md                            # Plugin entrypoint (Level 2 context)
├── LICENSE.txt                         # Apache 2.0
├── hooks/                              # Event-driven automation
│   ├── hooks.json                      # Hook definitions
│   ├── check_hw_config.py              # SessionStart: config validation
│   ├── check_kicad_happy.py            # SessionStart: kicad-happy availability
│   ├── check_pipeline_bypass.py        # PreToolUse: pipeline bypass detection (F-04)
│   └── check_kicad_file.py             # PostToolUse: KiCad file notification (F-06)
├── scripts/                            # Shared Python utilities
│   ├── config_schema.py                # Config validation logic
│   └── state_manager.py                # Pipeline state read/write
├── skills/                             # Sub-skills (one per role + orchestrator)
│   ├── hardware-flow/                  # Pipeline orchestrator
│   │   ├── SKILL.md                    # Orchestrator instructions
│   │   ├── references/                 # Orchestrator-specific references
│   │   │   ├── pipeline-stages.md      # 8-stage definitions with gates
│   │   │   ├── config-schema.md        # Config schema v1.0 specification
│   │   │   ├── rework-paths.md         # Rework DAG definition + termination
│   │   │   ├── gate-framework.md       # Gate validation patterns
│   │   │   ├── memory-protocol.md      # Self-learning memory protocol
│   │   │   ├── kicad-integration.md    # kicad-happy dispatch patterns
│   │   │   └── setup-wizard.md         # hw-setup wizard flow
│   │   └── scripts/                    # Orchestrator scripts
│   │       └── validate_config.py      # Config schema validation
│   ├── hw-product-owner/               # Hardware Product Owner role
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── hw-requirements.md      # HW requirements capture patterns
│   │       ├── feasibility-analysis.md # Feasibility frameworks
│   │       └── make-vs-buy.md          # Make-vs-buy decision framework
│   ├── electrical-engineer/            # Electrical Engineer role
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── schematic-review.md     # Schematic review checklist (7 categories)
│   │       ├── component-selection.md  # Component selection criteria
│   │       ├── simulation-guide.md     # SPICE simulation methodology
│   │       ├── power-analysis.md       # Power tree analysis patterns
│   │       └── firmware-interface.md   # Firmware interface doc template
│   ├── pcb-layout-engineer/            # PCB Layout Engineer role
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── layout-guidelines.md    # PCB layout best practices
│   │       ├── routing-rules.md        # Routing guidelines + impedance control
│   │       └── stackup-design.md       # Stackup design patterns
│   ├── manufacturing-engineer/         # Manufacturing Engineer role
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── dfm-rules.md           # DFM rule framework
│   │       ├── dfa-guidelines.md      # DFA guidelines
│   │       ├── panelization.md        # Panel design patterns
│   │       └── test-point-coverage.md # Test point requirements
│   ├── compliance-engineer/            # Compliance Engineer role
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── emc-design-rules.md    # EMC design rules
│   │       ├── safety-standards.md    # IEC 62368-1, IEC 60950
│   │       ├── environmental.md       # RoHS, REACH, WEEE
│   │       └── market-requirements.md # FCC Part 15, CE RED, UL
│   └── test-engineer/                  # Test Engineer role
│       ├── SKILL.md
│       └── references/
│           ├── test-strategy.md       # Test strategy frameworks
│           ├── fixture-design.md      # Test fixture design patterns
│           ├── production-test.md     # Production test methodology
│           └── validation-planning.md # Validation planning
└── references/                         # Plugin-level references
    ├── test-fixtures/                  # Reference KiCad project (Story 4.0)
    │   ├── MANIFEST.md                # Seeded defect manifest
    │   ├── reference.kicad_sch        # Schematic with 10 seeded defects
    │   ├── reference.kicad_pcb        # PCB with DFM violations
    │   ├── reference-bom.csv          # BOM with known issues
    │   └── reference-pricing.json     # Static pricing data (offline testable)
    └── prerequisites.md               # kicad-happy installation guide
```

### 1.2 Design Rationale

This structure mirrors the delivery-team plugin's proven layout:

- **Top-level SKILL.md**: Plugin entrypoint for Claude Code harness discovery
- **skills/**: One sub-directory per role + the orchestrator (hardware-flow)
- **hooks/**: Event-driven automation scripts with hooks.json
- **references/**: Plugin-level shared resources (test fixtures, prerequisites)
- **Each skill has its own references/**: Context isolation -- a skill loads only its own references

See **ADR-001** for the full decision record on plugin structure.

---

## 2. Skill Decomposition

> "Eight stages for the hardware projects doomed to iterate. Six roles to guide them. Eleven kicad-happy skills to bind them."

### 2.1 Skill Inventory

| Skill | Path | Type | Purpose |
|-------|------|------|---------|
| hardware-flow | `skills/hardware-flow/` | New (orchestrator) | Pipeline orchestrator -- coordinates all roles through 8 stages |
| hw-product-owner | `skills/hw-product-owner/` | New (role) | Requirements, constraints, feasibility, BOM budgeting |
| electrical-engineer | `skills/electrical-engineer/` | New (role) | Schematic design, component selection, simulation, firmware interface docs |
| pcb-layout-engineer | `skills/pcb-layout-engineer/` | New (role) | Physical layout, routing, stackup, DRC |
| manufacturing-engineer | `skills/manufacturing-engineer/` | New (role) | DFM/DFA review, yield, production transfer |
| compliance-engineer | `skills/compliance-engineer/` | New (role) | EMC, safety, environmental, regulatory documentation |
| test-engineer | `skills/test-engineer/` | New (role) | Test strategy, fixture design, validation planning |

> **Path convention note (F-08):** The "Path" column above shows paths relative to the plugin root (`hardware-team/`). The marketplace.json registration in Section 4 uses paths relative to the repository root (e.g., `./hardware-team/skills/hardware-flow`). Both refer to the same directory.

### 2.2 kicad-happy Skills Consumed (Cross-Plugin)

These are NOT duplicated in hardware-team. They are invoked via the Skill tool.

| kicad-happy Skill | Consuming hardware-team Role(s) | Stage(s) |
|---|---|---|
| `kicad-happy:kicad` | EE, PCB Layout | Schematic, Layout, DRC Gate |
| `kicad-happy:spice` | EE | Schematic |
| `kicad-happy:digikey` | EE | Schematic (component selection) |
| `kicad-happy:mouser` | EE | Schematic (component selection) |
| `kicad-happy:lcsc` | EE | Schematic (component selection) |
| `kicad-happy:element14` | EE | Schematic (component selection) |
| `kicad-happy:jlcpcb` | MfgE | DFM/DFA, Prototype |
| `kicad-happy:pcbway` | MfgE | DFM/DFA, Prototype |
| `kicad-happy:bom` | MfgE | DFM/DFA, Production Release |
| `kicad-happy:emc` | CompE | Compliance |
| `kicad-happy:kidoc` | CompE, MfgE | Compliance, Production Release |

### 2.3 Skill Invocation Pattern

Every role skill is invoked as a sub-agent via the Agent tool. The orchestrator (hardware-flow) NEVER produces domain artifacts directly -- this is the Prime Directive, mirrored from delivery-flow.

```
hardware-flow (orchestrator)
  |
  +-- Agent tool --> hw-product-owner skill
  |     |
  |     +-- (produces requirements, constraints, BOM budget)
  |
  +-- Agent tool --> electrical-engineer skill
  |     |
  |     +-- Skill tool --> kicad-happy:kicad (schematic analysis)
  |     +-- Skill tool --> kicad-happy:spice (simulation)
  |     +-- Skill tool --> kicad-happy:digikey (component search)
  |     +-- (produces schematic review, component rationale, simulation results,
  |          firmware interface docs)
  |
  +-- Agent tool --> pcb-layout-engineer skill
  |     |
  |     +-- Skill tool --> kicad-happy:kicad (PCB analysis, DRC)
  |     +-- (produces layout review, routing analysis, DRC results)
  |
  ... (similar for all roles)
```

**Key principle**: Hardware-team role skills invoke kicad-happy skills internally. The orchestrator does NOT invoke kicad-happy directly. This preserves role context isolation -- the EE skill knows when and why to invoke `kicad-happy:spice`; the orchestrator does not.

---

## 3. Pipeline Orchestrator Architecture

> "One architecture to rule them all, one pipeline to find them, one gate to bring them all, and in the review board bind them."

### 3.1 Eight-Stage Pipeline

| # | Stage | Execution Mode | Primary Role(s) | Gate(s) | kicad-happy Skills |
|---|-------|---------------|-----------------|---------|-------------------|
| 1 | Concept | AI-execution | HW PO | Requirements Completeness, Feasibility | None |
| 2 | Schematic | AI-execution | EE (primary), HW PO (trade-offs) | Schematic Review Gate (multi-reviewer) | kicad, spice, digikey, mouser, lcsc, element14 |
| 3 | Layout | AI-execution | PCB Layout (primary) | DRC Gate | kicad |
| 4 | Prototype | Human-execution | TestE (primary), EE (support) | Human Confirmation Gate | jlcpcb/pcbway (ordering package) |
| 5 | DFM/DFA | AI-execution | MfgE (primary) | DFM Gate + BOM Gate | jlcpcb/pcbway, bom |
| 6 | Compliance | AI-execution | CompE (primary) | Compliance Gate | emc, kidoc |
| 7 | Pilot Run | Human-execution | MfgE (primary), TestE (support) | Human Confirmation Gate | kidoc, bom |
| 8 | Production Release | Human-execution | MfgE (primary) | Final Gate (all artifacts complete) | kidoc, bom |

### 3.1.1 Sub-Agent Dispatch Failure Handling (C2 Resolution)

A sub-agent dispatch failure is distinct from a gate failure. A gate failure means the stage executed but produced unsatisfactory results. A dispatch failure means the stage could not execute at all -- the Agent tool call itself failed (timeout, context overflow, model error, or unexpected exception).

**Protocol:**

1. **Detect**: The orchestrator wraps every Agent tool dispatch in error detection. If the Agent tool returns an error rather than stage output, the orchestrator classifies it as a dispatch failure.
2. **Retry once**: The orchestrator retries the dispatch exactly once. The retry uses the same prompt and context. This handles transient errors (network hiccups, model overload).
3. **If retry fails -- PAUSE**: The pipeline transitions to `PAUSED_DISPATCH_ERROR` with the following recorded in `state.md`:
   - `dispatch_error.stage`: The stage number that failed
   - `dispatch_error.role`: The role skill being dispatched
   - `dispatch_error.error_type`: One of `TIMEOUT`, `CONTEXT_OVERFLOW`, `MODEL_ERROR`, `UNKNOWN`
   - `dispatch_error.error_detail`: The raw error message from the Agent tool
   - `dispatch_error.retry_attempted`: true
   - `dispatch_error.timestamp`: ISO 8601
4. **User options**: The orchestrator presents:
   - **Retry**: Attempt dispatch again (resets retry counter)
   - **Skip**: Mark stage as skipped (only for non-critical stages where gate is informational)
   - **Abort**: Save pipeline state and stop
5. **Logging**: Every dispatch failure (including the successful retry) is logged in a `dispatch_errors` array in `state.md` for post-run analysis.

**Error type classification:**

| Error Signal | Classification | Notes |
|---|---|---|
| Agent tool timeout (no response within platform limit) | `TIMEOUT` | May indicate excessive context or model overload |
| Agent response indicates context window exceeded | `CONTEXT_OVERFLOW` | Reduce Level 3 reference loading; consider splitting the stage |
| Agent tool returns model error (rate limit, internal error) | `MODEL_ERROR` | Typically transient; retry is appropriate |
| Any other Agent tool error | `UNKNOWN` | Logged for diagnosis |

### 3.2 Stage Routing Matrix by Project Type

Project type is detected at pipeline start. Phase 1 reads static config values; Phase 2 adds dynamic adaptation per FR-021.

| Stage | Hobby / 1-Layer Prototype | Small-Batch (10-1000) | Production (1000+) / Certified |
|-------|--------------------------|----------------------|-------------------------------|
| 1. Concept | Full | Full | Full |
| 2. Schematic | Full | Full | Full |
| 3. Layout | Full | Full | Full |
| 4. Prototype | Full | Full | Full |
| 5. DFM/DFA | Minimal (basic DRC only) | Full | Full + extended yield analysis |
| 6. Compliance | Skip (no regulatory) | Standard (FCC/CE as configured) | Full (all configured regions + safety) |
| 7. Pilot Run | Skip | Optional | Full |
| 8. Production Release | Skip | Minimal (BOM + ordering docs) | Full (manufacturing transfer package) |

**Phase 1 behavior**: All 8 stages execute at full depth regardless of project type. The routing matrix is informational guidance documented in `pipeline-stages.md`. Dynamic stage depth adaptation (skip/minimize) is Phase 2 scope per FR-021 and C7 resolution.

### 3.3 Rework Loops

The pipeline is a Directed Acyclic Graph (DAG) with controlled backward edges. Rework does NOT create cycles -- it is a bounded backward jump with re-validation of all downstream gates.

#### Defined Rework Paths

```
                    +-----------+
                    |           |
    +--------+  +--v--+  +-----v-+  +---------+  +-------+  +----------+  +---------+  +----------+
    |Concept |-→|Schem.|-→|Layout |-→|Prototype|-→|DFM/DFA|-→|Compliance|-→|Pilot Run|-→|Prod. Rel.|
    +--------+  +--^--+  +---^---+  +---------+  +---^---+  +--+--^----+  +---------+  +----------+
                   |       |  |                       |         |  |           |
                   |       |  +----- Prototype -------+         |  |           |
                   |       +-------- DFM/DFA ---------+         |  |           |
                   |       +-------- Compliance (layout) -------+  |           |
                   +----------DFM/DFA-+                            |           |
                   +----------Compliance (schematic)-+             |           |
                                                                   |           |
                                                   Pilot Run------+           |
                   +----------Pilot Run (schematic)---+                       |
```

> **Note (F-05):** The rework path table below is the authoritative source for rework routing. The ASCII diagram above is a visual aid; consult the table for precise path definitions.

| Rework Path | Trigger Examples |
|---|---|
| Prototype --> Schematic | Fundamental circuit error discovered during bring-up |
| Prototype --> Layout | Routing or thermal issue revealed by prototype |
| DFM/DFA --> Layout | DFM violation requires layout change |
| DFM/DFA --> Schematic | Component unavailable at target fab, needs substitution |
| Compliance --> Schematic | EMC failure requires filtering/shielding component redesign (new filter caps, shielding ICs) |
| Compliance --> Layout | EMC failure requiring layout-specific changes (ground plane modifications, trace rerouting for emission reduction, shielding zone additions) that do NOT require schematic changes |
| Pilot Run --> DFM/DFA | Assembly yield issue requires DFM adjustment |
| Pilot Run --> Schematic | Pilot run testing reveals circuit-level issue requiring component change or circuit modification (e.g., thermal behavior under production soldering differs from prototype, production testing reveals circuit behavior masked by bench supplies, yield analysis reveals component tolerance issue requiring redesign) |

#### Termination Conditions

| Condition | Default | Config Key | Behavior |
|---|---|---|---|
| `max_rework_iterations` | 3 | `rework.max_rework_iterations` | Per individual rework path. When path X-->Y triggers for the (N+1)th time, pipeline PAUSES and escalates to human. |
| `max_total_reworks` | 10 | `rework.max_total_reworks` | Across ALL paths in a single pipeline run. When total exceeds limit, pipeline PAUSES and escalates to human. |

Escalation message includes: (a) which limit was hit (per-path or total), (b) rework count per path, (c) cumulative rework history, (d) recommendation for human intervention. User options: `continue` (one more iteration), `abort` (stop pipeline, save state), `override limit N` (raise the limit).

#### Rework Execution Semantics

1. Pipeline sets `current_stage` to target stage
2. Target stage sub-agent receives: original artifacts + rework reason + specific issue description from source stage
3. Target stage re-executes (full stage, not just gate)
4. Target stage gate re-evaluates
5. ALL downstream gates between target and source are re-validated (gate re-evaluation against updated artifacts, not full stage re-execution)
6. Rework event logged to `.hardware/state.md` with: timestamp, source stage, target stage, trigger reason, resolution, iteration count for that path, total rework count

### 3.4 Human-Execution Stage Orchestration

> "The greatest works require both the craftsman's design and the smith's hand upon the anvil. Some stages must be wrought in the physical world."

Human-execution stages (Prototype, Pilot Run, Production Release) follow a three-phase pattern:

```
Phase 1: GATE-IN (AI generates preparation artifacts)
  |
  +-- Sub-agent produces: ordering packages, test procedures, checklists
  +-- Artifacts saved to .hardware/artifacts/<stage-name>/
  +-- Output presented to user with structured action items
  |
Phase 2: HUMAN-ACTION (pipeline pauses)
  |
  +-- Pipeline state transitions to: PAUSED_AWAITING_HUMAN
  +-- User receives: preparation artifacts + numbered action items
  +-- User performs physical work (ordering, assembly, testing)
  +-- User confirms: "<stage> complete" or "<stage> failed: <description>"
  +-- User can save: "save pipeline state" for cross-session resume
  |
Phase 3: GATE-OUT (AI evaluates completion)
  |
  +-- On "complete": gate evaluates, pipeline advances
  +-- On "failed: <description>": rework triggered (see rework paths)
  +-- On "save pipeline state": state persisted for resume
```

When rework triggers from a human-execution stage:
1. Human checkpoint is INVALIDATED (state: PENDING --> INVALIDATED)
2. Existing preparation artifacts are ARCHIVED (moved to `archived/run-N/`, never deleted)
3. Rework path determined using the standard rework path table
4. Target stage re-executes with failure description as additional context

### 3.4.1 Staleness Detection for Paused Pipelines (C4 Resolution)

When a pipeline is in `PAUSED_AWAITING_HUMAN` or `PAUSED_DISPATCH_ERROR` state, the SessionStart hook (`check_hw_config.py`) performs staleness detection:

**Protocol:**

1. **On every session start**, the hook checks for `.hardware/state.md` and reads the `last_updated` timestamp.
2. **Always display paused status** regardless of age:
   ```
   PIPELINE PAUSED at Stage 4 (Prototype) -- awaiting human action.
   Paused since: 2026-04-10T14:22:00Z (2 days ago).
   Resume with "resume hardware pipeline".
   ```
3. **Staleness warning threshold** (configurable, default 7 days):
   - Config key: `pipeline.staleness_warning_days` (integer, default 7)
   - If `now - last_updated > staleness_warning_days`:
     ```
     WARNING: Pipeline has been paused for 12 days at Stage 4 (Prototype).
     Config or project files may have drifted since the pipeline was paused.
     Options: Resume (uses original config snapshot) | Restart (applies current config) | Abandon
     ```
4. **Critical staleness threshold** (configurable, default 30 days):
   - Config key: `pipeline.staleness_critical_days` (integer, default 30)
   - If `now - last_updated > staleness_critical_days`:
     ```
     CRITICAL: Pipeline has been paused for 45 days. It is strongly recommended
     to Restart rather than Resume, as project context has likely changed significantly.
     ```

**Config schema additions** (v1.0 additive -- missing keys use defaults per Section 6.3):

| Field | Required | Type | Default | Validation |
|---|---|---|---|---|
| `pipeline.staleness_warning_days` | No | integer | 7 | Positive integer >= 1 |
| `pipeline.staleness_critical_days` | No | integer | 30 | Positive integer >= 1, must be > staleness_warning_days |

See **ADR-004** for the full decision record on this pattern.

---

## 4. Three-Level Context Loading

> "Not all knowledge should be carried at once. Load what is needed, when it is needed, and no more. This is the wisdom of the context window."

### Level 1: Metadata (Always Loaded)

The `marketplace.json` entry for hardware-team is loaded by the Claude Code harness whenever the plugin is installed. This is minimal metadata -- plugin name, description, and skill paths.

```json
{
  "name": "hardware-team",
  "description": "Hardware delivery team with 8-stage pipeline orchestrator for structured hardware product development. Coordinates 6 hardware roles (HW Product Owner, Electrical Engineer, PCB Layout Engineer, Manufacturing Engineer, Compliance Engineer, Test Engineer) through concept-to-production pipeline. Consumes kicad-happy skills for component sourcing, fabrication, analysis, and documentation.",
  "source": "./",
  "strict": false,
  "skills": [
    "./hardware-team/skills/hardware-flow",
    "./hardware-team/skills/hw-product-owner",
    "./hardware-team/skills/electrical-engineer",
    "./hardware-team/skills/pcb-layout-engineer",
    "./hardware-team/skills/manufacturing-engineer",
    "./hardware-team/skills/compliance-engineer",
    "./hardware-team/skills/test-engineer"
  ]
}
```

**Context cost**: ~200 tokens. Always present in the system prompt skill listing.

### Level 2: SKILL.md (Loaded When Skill Triggers)

Each skill's SKILL.md is loaded when the skill is invoked (by user trigger phrase or by the orchestrator via Agent tool). The SKILL.md contains:

- YAML frontmatter: name, description, license, minimum model tier
- Role description and responsibilities
- Reference file list (what to load on demand)
- Task type routing (what the role does in each stage)
- kicad-happy skills consumed (which skills to invoke and when)
- Output contracts (what artifacts the role produces)
- Anti-patterns (what the role must NOT do -- especially reimplementation guards)

**Context cost**: 500-2000 tokens per SKILL.md.

### Level 3: References (Loaded On Demand)

Reference files are loaded ONLY when the skill needs them for a specific task. The SKILL.md declares which references exist; the sub-agent reads them via the Read tool when the task requires that knowledge.

**Context cost**: 1000-5000 tokens per reference file, loaded only when needed.

### 4.1 Reference Availability Check (C5 Resolution)

When a sub-agent needs to load a Level 3 reference file, it follows this protocol before reading:

1. **Check existence**: Use the Glob tool to verify the reference file exists at the expected path before reading it.
2. **If missing**: The sub-agent includes `REFERENCE_MISSING: <path>` in its output and continues with degraded capability. The sub-agent documents what knowledge it lacked and how this may affect the quality of its output.
3. **If present but unreadable** (Read tool returns an error): The sub-agent includes `REFERENCE_CORRUPTED: <path>` in its output and continues with degraded capability.
4. **Orchestrator logging**: The orchestrator records any `REFERENCE_MISSING` or `REFERENCE_CORRUPTED` signals in the gate results for that stage.
5. **Gate impact**: A missing reference does NOT automatically fail a gate. The gate evaluates based on the quality of the output produced. However, the finding is logged for visibility.

This parallels the `SKILL_UNAVAILABLE` pattern already defined in Section 5.3 for kicad-happy skills.

**Sub-agent prompt template addition:**
```
Before reading any reference file listed in your SKILL.md, verify it exists
using Glob. If a reference file is missing, report REFERENCE_MISSING: <path>
in your output, note what knowledge is unavailable, and proceed with your
best judgment. Do NOT fail the stage due to a missing reference.
```

### Context Loading Flow

```
User: "Run the hardware pipeline"
  |
  1. Claude Code harness has Level 1 (marketplace.json) -- recognizes hardware-team
  2. Skill trigger loads Level 2 (hardware-flow/SKILL.md) -- orchestrator instructions
  3. Orchestrator dispatches Stage 1 sub-agent:
     a. Sub-agent prompt includes hw-product-owner/SKILL.md (Level 2 for role)
     b. Sub-agent reads hw-requirements.md (Level 3) when it needs requirements patterns
     c. Sub-agent does NOT read electrical-engineer references (context isolation)
  4. Orchestrator dispatches Stage 2 sub-agent:
     a. Sub-agent prompt includes electrical-engineer/SKILL.md (Level 2 for role)
     b. Sub-agent reads schematic-review.md (Level 3) for review checklist
     c. Sub-agent invokes kicad-happy:kicad via Skill tool (cross-plugin Level 2+3)
     d. Sub-agent does NOT read manufacturing-engineer references
```

---

## 5. kicad-happy Integration Architecture

> "The kicad-happy skills are rings of power forged by another hand. We do not remake them. We wield them."

### 5.1 Cross-Plugin Skill Invocation

**Mechanism**: The Skill tool supports cross-plugin invocation using the `<plugin>:<skill>` syntax. This has been verified working -- `kicad-happy:kicad` loads from `C:\Users\micha\.claude\plugins\cache\kicad-happy\kicad-happy\1.2.0\`.

**Invocation pattern within a hardware-team sub-agent**:

The sub-agent's SKILL.md documents which kicad-happy skills it may invoke and under what conditions. When the sub-agent determines it needs a kicad-happy capability, it uses the Skill tool:

```
# Inside an electrical-engineer sub-agent during Schematic stage:
# 1. Sub-agent reads its SKILL.md (already loaded)
# 2. SKILL.md says: "For schematic analysis, invoke kicad-happy:kicad"
# 3. Sub-agent calls: Skill("kicad-happy:kicad")
# 4. kicad-happy:kicad SKILL.md loads into the sub-agent's context
# 5. Sub-agent uses the loaded skill's capabilities
```

The orchestrator does NOT invoke kicad-happy directly -- role skills own the decision of when and how to use kicad-happy capabilities.

#### Cross-Plugin Trust Boundary (SEC-04 Resolution)

> "We wield rings forged by another hand. We trust the smith who made them -- but we name that trust explicitly, so that no future bearer is deceived about the source of the metal's power."

**Trust assumption**: hardware-team trusts that the Claude Code plugin harness ensures plugin authenticity and integrity. Plugin cache tampering (e.g., a malicious plugin placed at `~/.claude/plugins/cache/kicad-happy/`) is outside this plugin's threat model and is the platform's responsibility. hardware-team validates the *structure* of kicad-happy output (Section 5.5, output contract validation) but does not validate the *authenticity* of the kicad-happy plugin itself.

**Implication**: If the Claude Code harness is compromised or if a user manually places a malicious plugin in the cache directory, hardware-team's contract validation would catch structural mismatches but would NOT detect semantically malicious data (e.g., a manipulated BOM with inflated prices directing orders to a specific supplier). This is an accepted platform-level risk, not a plugin-level risk.

### 5.2 Role-to-kicad-happy Mapping

| Hardware Role | kicad-happy Skills Consumed | Usage Context |
|---|---|---|
| Electrical Engineer | `kicad`, `spice`, `digikey`, `mouser`, `lcsc`, `element14` | Schematic analysis, simulation, component sourcing |
| PCB Layout Engineer | `kicad` | PCB analysis, DRC parsing, layout review |
| Manufacturing Engineer | `jlcpcb`, `pcbway`, `bom`, `kidoc` | DFM rules, BOM management, manufacturing documentation |
| Compliance Engineer | `emc`, `kidoc` | EMC pre-compliance analysis, regulatory documentation |
| Test Engineer | `kicad` (optional) | Reads test point locations, connector pinouts, and debug interfaces from PCB design. Falls back to artifact-based planning if kicad-happy:kicad unavailable. |
| HW Product Owner | (none directly) | Uses role outputs for trade-off decisions, not kicad-happy directly |

### 5.3 Error Handling: kicad-happy Not Installed

When a hardware-team sub-agent attempts to invoke a kicad-happy skill that is not installed:

1. **Skill tool returns an error** (skill not found in plugin cache)
2. **Sub-agent catches the error** and reports to the orchestrator via its output:
   ```
   SKILL_UNAVAILABLE: kicad-happy:digikey
   Required for: component sourcing during Schematic stage
   Install: Install kicad-happy via Claude Code plugin system
   Impact: Cannot perform automated component search. Manual component data required.
   ```
3. **Orchestrator logs the error** in pipeline state and presents to user
4. **Pipeline does NOT crash** -- it degrades gracefully. The sub-agent documents what it could not do and why. The gate may still evaluate based on available data.

**Pre-flight check (SessionStart hook)**: The `check_kicad_happy.py` hook runs at session start and reports skill availability before the pipeline begins. This gives the user early warning to install missing skills.

### 5.4 Reimplementation Guard (NFR-003)

A capability is reimplemented if a hardware-team role performs an action that would produce the same output as invoking a kicad-happy skill, without invoking that skill.

**IS reimplementation** (prohibited):
- Parsing `.kicad_sch` files to extract BOM data instead of invoking `kicad-happy:kicad`
- Querying DigiKey API directly instead of invoking `kicad-happy:digikey`
- Implementing EMC rule checks from scratch instead of invoking `kicad-happy:emc`

**IS NOT reimplementation** (permitted):
- SKILL.md containing domain knowledge that guides when/how to invoke a kicad-happy skill
- Interpreting kicad-happy output and making engineering judgments about it
- Combining outputs from multiple kicad-happy skills into a unified report
- A review checklist item (e.g., "check capacitor derating") that triggers a kicad-happy invocation

Each role's SKILL.md includes an explicit "kicad-happy Consumption" section listing which skills it invokes and the anti-pattern of performing that work itself.

### 5.5 kicad-happy Output Contract Validation (F-01 Resolution)

> "A ring forged by another hand must be tested before it is worn. Trust, but verify the shape of the metal."

The kicad-happy dependency is a one-way door (ADR-002). Silent interface drift between kicad-happy versions could introduce data corruption that is extremely difficult to diagnose. To guard against this, hardware-team defines explicit output contracts for every consumed kicad-happy skill and validates them at runtime.

#### 5.5.1 Contract Specification

The reference file `kicad-integration.md` (in `skills/hardware-flow/references/`) defines the expected output structure for each consumed kicad-happy skill. Each contract includes a `contract_version` and `kicad_happy_target_version` to enable version tracking and mismatch diagnosis (F-12 resolution). Each contract specifies:

| kicad-happy Skill | Contract Version | Target kicad-happy Version | Expected Output Fields | Types | Consuming Role(s) |
|---|---|---|---|---|---|
| `kicad-happy:kicad` (schematic analysis) | 1.0 | >=1.2.x | `findings[]` (each: `id`, `severity`, `category`, `component`, `net`, `description`), `summary.total_findings`, `summary.by_severity{}` | findings: array of objects; severity: enum(critical/major/minor/info); category: string | EE, PCB Layout |
| `kicad-happy:kicad` (PCB/DRC analysis) | 1.0 | >=1.2.x | `drc_results[]` (each: `rule_id`, `severity`, `location`, `description`), `board_stats{}` | drc_results: array of objects; severity: enum | PCB Layout |
| `kicad-happy:spice` | 1.0 | >=1.2.x | `simulations[]` (each: `subcircuit`, `type`, `result`, `pass`), `summary.pass_count`, `summary.fail_count` | simulations: array of objects; pass: boolean | EE |
| `kicad-happy:digikey` / `mouser` / `lcsc` / `element14` | 1.0 | >=1.2.x | `parts[]` (each: `mpn`, `description`, `price`, `stock`, `datasheet_url`), `query` | parts: array of objects; price: number or null | EE |
| `kicad-happy:jlcpcb` / `pcbway` | 1.0 | >=1.2.x | `dfm_rules[]` (each: `rule_id`, `parameter`, `min_value`, `board_value`, `pass`), `assembly_constraints{}` | dfm_rules: array of objects; pass: boolean | MfgE |
| `kicad-happy:bom` | 1.0 | >=1.2.x | `bom_entries[]` (each: `ref`, `mpn`, `quantity`, `unit_price`, `sources[]`), `total_cost`, `single_source_items[]` | bom_entries: array of objects; total_cost: number | MfgE |
| `kicad-happy:emc` | 1.0 | >=1.2.x | `checks[]` (each: `rule_id`, `category`, `severity`, `description`, `location`), `risk_score`, `summary{}` | checks: array of objects; risk_score: number | CompE |
| `kicad-happy:kidoc` | 1.0 | >=1.2.x | `document{}` (fields: `title`, `sections[]`, `format`), `generation_status` | document: object; generation_status: enum(success/partial/failed) | CompE, MfgE |

#### 5.5.2 Runtime Contract Assertion

Each role sub-agent validates the output from a kicad-happy skill invocation before processing it. The validation is embedded in the sub-agent's SKILL.md as a mandatory post-invocation step:

```
After invoking any kicad-happy skill, validate the output structure before processing:
1. Check that the expected top-level fields are present (per kicad-integration.md contract)
2. Check that array fields are arrays (not null, not strings)
3. Check that each array element contains the required sub-fields
4. If validation passes: proceed with processing
5. If validation fails: report HW-KCH-004: CONTRACT_MISMATCH with:
   - Which skill was invoked
   - The contract version and target kicad-happy version from kicad-integration.md
   - The installed kicad-happy version (if known from SessionStart hook)
   - Which fields are missing or have unexpected types
   - The raw output (first 500 characters) for diagnostic context
   Do NOT process malformed data. Report the mismatch and continue
   the stage with degraded capability (same as SKILL_UNAVAILABLE).
```

#### 5.5.3 Error Taxonomy Addition

| Code | Error Condition | Detecting Component | Severity | Response Behavior |
|---|---|---|---|---|
| `HW-KCH-004` | kicad-happy output contract mismatch | Sub-agent (post-invocation) | Major | `CONTRACT_MISMATCH` signal. Sub-agent does NOT process malformed data. Gate evaluates on available data. Logged in gate results for diagnosis. |

This transforms silent data corruption into a detectable, actionable error. The contract specification also serves as documentation for kicad-happy maintainers about which output structures hardware-team depends on.

#### 5.5.4 Contract Update Procedure (F-12 Resolution)

When kicad-happy releases a new version:

1. Run the test fixture (Story 4.0) against the new kicad-happy version
2. If HW-KCH-004 fires for any contract: the new version has introduced a breaking change
3. Update `kicad-integration.md` contracts to match the new output structure
4. Increment the `contract_version` for each updated contract
5. Update `kicad_happy_target_version` to the new version range
6. Document the change in the architecture changelog

This is a documentation-level maintenance loop -- no code changes are required unless field semantics change (not just structure).

See **ADR-002** for the full decision record on integration pattern.

---

## 6. Config Schema (.hardware/config.yml)

### 6.1 Schema Definition (v1.0)

```yaml
# .hardware/config.yml -- Schema v1.0
schema_version: "1.0"

# Project identity
project_name: "sensor-board-v2"

# Fabrication target
target_fab: jlcpcb           # Enum: jlcpcb | pcbway | custom
custom_fab_name: ""          # Only used when target_fab: custom

# Compliance regions
compliance_regions:           # List of: fcc | ce | ul | rohs | reach | none
  - fcc
  - ce

# BOM constraints
bom_budget: 12.50            # USD per unit. null = no limit
second_source_required: false # If true, BOM Gate blocks single-source components

# Production volume
production_volume: small-batch  # Enum: prototype | small-batch | production

# Board complexity
board_layers: 4              # Integer: 1, 2, 4, 6, 8

# Dependencies
dependencies:
  kicad_happy_version: ">=1.2.0"  # Minimum compatible kicad-happy version

# Rework limits
rework:
  max_rework_iterations: 3   # Per individual rework path
  max_total_reworks: 10       # Across all paths in a pipeline run

# Gate strictness (F-13: behavioral specification in Section 10.1)
# strict: critical, major, AND minor findings all block the gate
# standard: critical and major findings block; minor findings pass (logged)
# relaxed: only critical findings block; major findings pass (logged as warning)
gate_strictness: standard    # Enum: strict | standard | relaxed

# Review configuration
review:
  schematic_review_passes: 2  # Number of parallel reviewer passes (1-5)
  design_review_board: true   # Enable multi-role Design Review Board at key transitions
```

### 6.2 Schema Validation Rules

| Field | Required | Type | Default | Validation |
|---|---|---|---|---|
| `schema_version` | Yes | string | "1.0" | Must match known schema versions |
| `project_name` | Yes | string | (none) | Non-empty string |
| `target_fab` | No | enum | jlcpcb | One of: jlcpcb, pcbway, custom |
| `compliance_regions` | No | list | [] | Each item: fcc, ce, ul, rohs, reach, none |
| `bom_budget` | No | number/null | null | Positive number or null |
| `second_source_required` | No | boolean | false | true/false |
| `production_volume` | No | enum | prototype | One of: prototype, small-batch, production |
| `board_layers` | No | integer | 2 | One of: 1, 2, 4, 6, 8 |
| `dependencies.kicad_happy_version` | No | string | ">=1.2.0" | Semver range string |
| `rework.max_rework_iterations` | No | integer | 3 | Positive integer >= 1 |
| `rework.max_total_reworks` | No | integer | 10 | Positive integer >= 1 |
| `gate_strictness` | No | enum | standard | One of: strict, standard, relaxed |
| `review.schematic_review_passes` | No | integer | 2 | Integer 1-5 |
| `review.design_review_board` | No | boolean | true | true/false |

### 6.3 Forward Compatibility Protocol

Following delivery-flow's extension protocol:

1. **Missing keys use defaults** -- a v1.0 config loaded by a v1.1 schema plugin uses defaults for new keys. Never fail on absent keys.
2. **Unknown keys are ignored** -- a v1.1 config loaded by a v1.0 schema plugin ignores keys it does not recognize. Never fail on extra keys.
3. **`schema_version` enables migration guidance** -- when old config meets new schema, the SessionStart hook announces: "Config uses schema vX.Y. Current schema is vA.B. New settings applied with defaults: [list]."
4. **Invalid values warn and use defaults** -- never fail the pipeline due to config errors. Invalid `target_fab: "invalid"` warns and uses `jlcpcb`.

### 6.4 Extension Protocol (for Future Schema Versions)

When adding new config keys in future versions:

1. Add the key to the schema with a sensible default
2. Increment schema_version (minor for additive, major for breaking)
3. Update `config-schema.md` with the new key documentation
4. Update `validate_config.py` to validate the new key
5. Ensure all code paths handle the key being absent (default fallback)

---

## 7. State Management

### 7.1 State File (.hardware/state.md)

Pipeline state is persisted as a Markdown file with YAML frontmatter, matching the delivery-flow pattern.

> **Known trade-off (F-03):** Markdown-with-YAML-frontmatter is less parse-robust than pure YAML for machine-managed state data. The YAML frontmatter delimiter (`---`) must be the first line; any accidental text before it breaks parsing, and the Markdown body below the frontmatter serves no machine purpose. This format was chosen to mirror delivery-flow's established convention and maintain ecosystem consistency. The `state_manager.py` script MUST use a robust frontmatter parser (Python `yaml` module with explicit `---` delimiter detection, NOT regex-based splitting) and validate that the first non-empty line is exactly `---`. If a future version moves to pure YAML (`.hardware/state.yml`), this is a low-risk change isolated to `state_manager.py`.

> **Security invariant (SEC-01): YAML safe loading.** All YAML parsing in `state_manager.py`, `validate_config.py`, and all hook scripts MUST use `yaml.safe_load()` (never `yaml.load()` or `yaml.FullLoader`). This prevents YAML deserialization attacks where crafted tags (e.g., `!!python/object/apply:os.system`) could execute arbitrary code. See Section 14.1 for the full coding standard.

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
config_hash: "sha256:a1b2c3d4e5f6..."   # SHA-256 of .hardware/config.yml content at pipeline start
config_snapshot_file: ".hardware/config-snapshot-run-2026-04-12-hw01.yml"  # Full config preserved once, outside state file

# Artifact registry (path -> stage metadata)
artifacts:
  ".hardware/artifacts/01-concept/requirements.md":
    stage: 1
    role: hw-product-owner
    timestamp: "2026-04-12T11:00:00Z"
  ".hardware/artifacts/02-schematic/review.md":
    stage: 2
    role: electrical-engineer
    timestamp: "2026-04-12T12:30:00Z"

# Gate results (ordered by execution)
gates:
  - stage: 1
    gate: concept-gate
    result: DONE
    timestamp: "2026-04-12T11:00:00Z"
    validators:
      - id: requirements-completeness
        result: DONE
      - id: feasibility-check
        result: DONE
  - stage: 2
    gate: schematic-review-gate
    result: DONE
    timestamp: "2026-04-12T12:30:00Z"
    reviewers: 2
    findings_total: 7
    findings_deduplicated: 3
    validators:
      - id: power-integrity
        result: DONE
      - id: signal-integrity
        result: DONE
      - id: component-derating
        result: DONE
      - id: pull-ups-pull-downs
        result: DONE
      - id: decoupling
        result: DONE
      - id: voltage-level-compat
        result: DONE
      - id: thermal
        result: DONE

# Rework history
rework_history:
  total_reworks: 2
  paths:
    "prototype->schematic":
      count: 1
      events:
        - iteration: 1
          trigger: "Thermal issue on U3"
          source_stage: 4
          target_stage: 2
          timestamp: "2026-04-12T13:00:00Z"
          resolution: "Added thermal pad, increased copper pour"
    "dfm->layout":
      count: 1
      events:
        - iteration: 1
          trigger: "Trace width below JLCPCB minimum"
          source_stage: 5
          target_stage: 3
          timestamp: "2026-04-12T13:45:00Z"
          resolution: "Widened trace from 0.10mm to 0.15mm"

# Human checkpoints (for human-execution stages)
checkpoints:
  - stage: 4
    stage_name: prototype
    status: completed          # Enum: pending | completed | invalidated
    artifacts_generated: ["ordering-package.md", "test-procedure.md"]
    timestamp: "2026-04-12T14:00:00Z"
---

# Pipeline State: sensor-board-v2

This file tracks the state of the hardware pipeline run `run-2026-04-12-hw01`.
Do not edit manually -- managed by the hardware-flow orchestrator.
```

### 7.2 Path Sanitization (SEC-01 Resolution)

> "A single flaw in the foundation can bring the entire tower to ruin. Every path must be tested before the file is written."

All file paths constructed from user-controlled or config-derived values (`pipeline_id`, `project_name`, stage names in rework history, archived directory names) MUST be sanitized before use. This is a **security invariant** -- violation is a blocking defect.

**Sanitization rules (implemented in `state_manager.py`):**

1. **Whitelist validation**: All path components derived from config or state values MUST match the pattern `^[a-zA-Z0-9._-]+$`. Reject any value containing `/`, `\`, `..`, null bytes (`\x00`), or any character outside the whitelist.
2. **Path canonicalization check**: After constructing a file path, resolve it to an absolute path (`os.path.realpath()`) and verify the result starts with the expected `.hardware/` directory (resolved to absolute form). If the resolved path escapes the `.hardware/` sandbox, raise `HW-STA-005` (see Section 13.2).
3. **Apply at all construction points**: Config snapshot paths (`config-snapshot-<pipeline_id>.yml`), archived artifact paths (`archived/run-N/`), artifact registry paths, and any future path that interpolates user-controlled values.

**`state_manager.py` API:**

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

All path construction in `state_manager.py`, the orchestrator, and sub-agent prompts MUST use `safe_join()` (or equivalent logic) rather than raw string interpolation or `os.path.join()` without validation.

### 7.2.1 State Tampering Accepted Risk (SEC-05 Resolution)

The `.hardware/state.md` file is user-editable on the local filesystem. A user (or script) could manually edit state to skip stages, reset rework counters, or mark gates as DONE when they were NOT_DONE, circumventing quality gates.

**This is an accepted risk for a local development tool.** The user is the primary actor and has legitimate reasons to override pipeline state (e.g., manual prototyping completed outside the pipeline, experimentation).

**Lightweight tamper detection (advisory, not blocking):**

`state_manager.py` computes a SHA-256 integrity hash over the `stages_completed` and `gates` arrays on each state write. On resume, if the hash does not match the current values:

```
WARNING: State file appears to have been manually edited.
Gate results may not reflect actual pipeline execution.
Continue anyway? [Y/n]
```

The pipeline proceeds regardless of the user's answer -- the warning is for awareness, not enforcement. The integrity hash is stored as `_integrity_hash` in the state YAML frontmatter.

### 7.3 State Operations

| Operation | When | What |
|---|---|---|
| **Create** | Pipeline start | Initialize with pipeline_id (sanitized via `sanitize_path_component()`), config_hash (SHA-256), status=in_progress. Save full config copy to `.hardware/config-snapshot-<pipeline_id>.yml` (path constructed via `safe_join()`). |
| **Update (stage complete)** | Stage completion | Add stage to stages_completed, add gate results, register artifacts |
| **Update (rework)** | Rework triggered | Add rework event to rework_history, update current_stage |
| **Pause** | Human-execution stage checkpoint | Set status=paused, save checkpoint entry |
| **Resume** | Session restart with resume request | Load state, validate artifacts exist, continue from current_stage |
| **Complete** | All stages done | Set status=completed, final timestamp |
| **Abort** | User aborts or escalation without override | Set status=aborted, preserve all artifacts |

### 7.4 Resume Protocol

1. Check for `.hardware/state.md` at session start (or on "resume hardware pipeline" trigger)
2. **State file integrity check** (C8 Resolution):
   a. Attempt to parse the YAML frontmatter from `.hardware/state.md`
   b. If YAML parse fails (malformed syntax, encoding error):
      - Report: `STATE_FILE_CORRUPTED: .hardware/state.md -- YAML parse error: <error details>`
      - Present options:
        - **Restart**: Archive the corrupted file to `.hardware/archived/corrupted-<timestamp>.md`, start fresh pipeline with current config
        - **Manual Fix**: Display the parse error and the first 20 lines of the file so the user can fix the syntax error, then retry
   c. If YAML parses but required fields are missing (`pipeline_id`, `status`, `current_stage`, `stages_completed`):
      - Report: `STATE_FILE_INCOMPLETE: Missing required fields: [list]`
      - Present same options (Restart / Manual Fix)
   d. The `state_manager.py` script provides a `validate_state(path) -> (valid: bool, errors: list)` function for this check
3. If `status: in_progress` or `status: paused`:
   - Read YAML frontmatter to load pipeline state
   - Validate all artifact files in the registry exist on disk
   - Compute SHA-256 of current `.hardware/config.yml` and compare against `config_hash` in state file
   - If hash differs: warn "Config has changed since this pipeline started (hash mismatch). Resume uses the original config snapshot (`.hardware/config-snapshot-<pipeline_id>.yml`). Choose Restart to apply new config."
   - Config changes during an active pipeline run are unsupported -- the pipeline always uses the config as snapshotted at start. If the user changes config mid-run, they must restart the pipeline.
   - If artifacts missing: announce which, offer Restart from that stage / Abandon
   - Offer: **Resume** / **Restart** / **Abandon**
4. Resume: load config from snapshot, skip completed stages, start at `current_stage`
5. Restart: archive state file, start fresh with current config
6. Abandon: delete state file, no pipeline runs

### 7.5 Artifact Directory Structure

```
.hardware/
├── config.yml                          # Project configuration
├── state.md                            # Pipeline state (managed by orchestrator)
├── memory/                             # Self-learning memory (see Section 8)
└── artifacts/                          # Pipeline artifacts organized by stage
    ├── 01-concept/
    │   ├── requirements.md
    │   ├── constraints.md
    │   ├── regulatory-scan.md
    │   └── bom-budget.md
    ├── 02-schematic/
    │   ├── schematic-review.md
    │   ├── component-rationale.md
    │   ├── simulation-results.md
    │   └── firmware-interface.md       # Pin table, power domains, bus specs, debug
    ├── 03-layout/
    │   ├── layout-review.md
    │   ├── routing-analysis.md
    │   └── drc-results.md
    ├── 04-prototype/
    │   ├── ordering-package.md
    │   ├── test-procedure.md
    │   ├── test-fixture-requirements.md
    │   └── archived/                   # Archived artifacts from rework iterations
    │       └── run-1/                  # Preserved for reference, never deleted
    ├── 05-dfm-dfa/
    │   ├── dfm-report.md
    │   ├── dfa-report.md
    │   ├── yield-assessment.md
    │   └── bom-validation.md
    ├── 06-compliance/
    │   ├── emc-report.md
    │   ├── safety-analysis.md
    │   ├── environmental-checklist.md
    │   └── compliance-package.md
    ├── 07-pilot-run/
    │   ├── manufacturing-transfer.md
    │   ├── production-test-procedure.md
    │   └── yield-targets.md
    └── 08-production-release/
        ├── production-checklist.md
        ├── final-bom.md
        ├── compliance-package.md
        └── release-documentation.md
```

---

## 8. Self-Learning Memory

> "Memory is the forge upon which future wisdom is hammered. Every pipeline run leaves lessons in the metal."

### 8.1 Memory Architecture

Following delivery-flow's tiered chunked retrieval pattern:

```
.hardware/memory/
├── index.md                     # Memory index: entry IDs, tags, relevance scores
├── lessons-concept.md           # Lessons from Concept stages
├── lessons-schematic.md         # Lessons from Schematic stages
├── lessons-layout.md            # Lessons from Layout stages
├── lessons-prototype.md         # Lessons from Prototype stages
├── lessons-dfm.md               # Lessons from DFM/DFA stages
├── lessons-compliance.md        # Lessons from Compliance stages
├── lessons-rework.md            # Cross-cutting rework pattern lessons
└── lessons-general.md           # General project and process lessons
```

### 8.2 Memory Entry Format

```yaml
- id: MEM-2026-04-12-001
  stage: schematic
  category: component-selection     # Categorizes the lesson type
  lesson: "Capacitor C7 was derated below 50% of rated voltage. Always check capacitor derating against maximum operating voltage, not just nominal, especially for ceramic capacitors where effective capacitance drops with DC bias."
  project: sensor-board-v2
  date: 2026-04-12
  tags: [derating, capacitor, schematic-review, ceramic]
  relevance_decay: 0.95            # 0.0 = one-shot, 1.0 = permanent. 0.95 = slow decay
  source_gate: schematic-review-gate  # Which gate surfaced this lesson
```

### 8.3 Memory Protocol

**Write (after pipeline run completes or aborts)**:

1. Orchestrator reviews pipeline execution: gates that failed, rework paths triggered, human escalations, findings from review gates
2. For each notable event, capture a memory entry in the appropriate `lessons-<stage>.md` file
3. Update `index.md` with the new entry's ID, tags, and initial relevance score
4. Cross-cutting patterns (e.g., "component X repeatedly causes rework") go to `lessons-rework.md`
5. **No-pricing filter (SEC-02):** Memory entries MUST NOT capture specific pricing values, negotiated rates, supplier account identifiers, or supplier-specific commercial terms. Lessons about component selection may reference part numbers and technical rationale (e.g., "Selected MLCC over tantalum for C7 due to DC bias derating") but must redact unit prices (e.g., NOT "Supplier X quoted $0.12/unit for C7"). See Section 14.2 for the full data classification policy.

**Read (at pipeline start and at each stage dispatch)**:

1. Load `index.md` to get the memory index
2. For the stage about to execute, load the corresponding `lessons-<stage>.md`
3. Score relevance: tag match (stage + category), project similarity, recency, decay factor
4. Inject top memories into the sub-agent prompt as a "Lessons from Previous Runs" section

### 8.4 Memory Tiering

| Tier | Criteria | Injection Point |
|---|---|---|
| **Always inject** | Lessons tagged with the current stage AND from the same project | Stage sub-agent prompt (mandatory) |
| **Inject if relevant** | Lessons tagged with the current stage from other projects, top 5 by relevance score | Stage sub-agent prompt (if context budget allows) |
| **Available on request** | All other lessons in `.hardware/memory/` | Sub-agent can Read from memory/ if it needs historical context |

**p95 retrieval target**: < 2 seconds (NFR-008). Achieved by: small index file (scan, not search), per-stage file partitioning (read only one file), capped injection (top 5 per tier).

### 8.5 Memory Influence Observability (C9 Resolution)

To close the feedback loop between memory injection and stage outcomes, each sub-agent that receives injected lessons reports their disposition:

**Sub-agent prompt addition:**
```
You have been provided with lessons from previous pipeline runs in the
"Lessons from Previous Runs" section above. For each injected lesson,
report its disposition in your output using one of:
  MEMORY_APPLIED: <MEM-ID> -- <brief description of how the lesson influenced a decision>
  MEMORY_NOTED: <MEM-ID> -- <brief reason why it was acknowledged but not applicable>
```

**Orchestrator behavior:**
1. After the sub-agent completes, the orchestrator scans the output for `MEMORY_APPLIED` and `MEMORY_NOTED` signals.
2. During the memory write phase (after pipeline completion), the orchestrator updates the memory index with application data:
   - Lessons with `MEMORY_APPLIED` get a relevance boost (+0.1, capped at 1.0)
   - Lessons with `MEMORY_NOTED` across 3+ consecutive runs where the same lesson was injected but never applied get a relevance penalty (-0.05)
3. This data is logged in the gate results under a `memory_disposition` field:
   ```yaml
   memory_disposition:
     - id: MEM-2026-04-12-001
       status: APPLIED
       detail: "Used capacitor derating lesson to flag C12"
     - id: MEM-2026-04-10-003
       status: NOTED
       detail: "Lesson about connector orientation not relevant to this board"
   ```

**Phase 2 extension**: Full relevance scoring model with decay curves informed by application rates. Phase 1 provides the signal; Phase 2 consumes it.

### 8.6 Memory Archival and Cleanup (F-07 Resolution)

> "Even the greatest forge must be swept clean of old slag, lest the clutter dull the craftsman's focus."

Without a cleanup mechanism, memory files grow unbounded as relevance scores asymptotically approach zero. This degrades index scan performance and wastes context budget injecting near-zero-relevance lessons.

**Archival rules:**

| Condition | Action |
|---|---|
| Relevance score < 0.1 after at least 10 pipeline runs | Entry moved to `lessons-archived.md` |
| `memory_entries_limit` exceeded per stage file (default: 100) | Lowest-relevance entries archived until count <= limit |
| `MEMORY_NOTED` across 5+ consecutive runs without a single `MEMORY_APPLIED` | Entry relevance set to 0.0 (triggers archival on next cleanup) |

**Relevance decay floor:** 0.05. Relevance scores are clamped to `max(score * relevance_decay, 0.05)` to ensure the archival threshold (0.1) is reachable in finite runs rather than asymptotically approaching zero forever.

**Archival location:**
```
.hardware/memory/
├── ...existing files...
└── lessons-archived.md          # Archived entries (excluded from index scanning)
```

**Archival behavior:**
1. Entries in `lessons-archived.md` are excluded from `index.md` scanning and are never injected into sub-agent prompts
2. Archived entries are preserved (not deleted) for historical reference -- a human or future tooling can review them
3. Cleanup runs during the memory write phase at the end of each pipeline run (after new lessons are captured)

**Config schema addition:**

| Field | Required | Type | Default | Validation |
|---|---|---|---|---|
| `memory.entries_limit` | No | integer | 100 | Positive integer >= 10 |

---

## 9. Hooks

### 9.1 Hook Definitions (hooks.json)

```json
{
  "description": "Hardware team hooks: config validation, kicad-happy dependency check, KiCad file modification notification",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/check_hw_config.py",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/check_kicad_happy.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/check_pipeline_bypass.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/check_kicad_file.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### 9.2 SessionStart: Config Validation (check_hw_config.py)

**Logic**:
1. Check for `.hardware/config.yml` in current working directory
2. If missing: print warning "No .hardware/config.yml found. Run `hw-setup` to create one."
3. If present:
   - Parse YAML
   - Validate `schema_version` against known versions
   - Validate each field against schema rules (type, enum values, ranges)
   - If outdated schema: warn with migration guidance listing new fields and defaults
   - If invalid fields: warn per-field with expected type/values, note defaults will be used
   - If valid: no output (silent success)
4. Exit 0 always (informational hook, never blocks session start)

### 9.3 SessionStart: kicad-happy Dependency Check (check_kicad_happy.py)

**Logic**:
1. Determine kicad-happy installation path:
   - Primary: `~/.claude/plugins/cache/kicad-happy/`
   - Scan for version directories under the cache path
2. For each of the 11 kicad-happy skills (`kicad`, `spice`, `digikey`, `mouser`, `lcsc`, `element14`, `jlcpcb`, `pcbway`, `bom`, `emc`, `kidoc`):
   - Check if the skill directory and SKILL.md exist under the installed version
3. Report results:
   - All 11 available: "kicad-happy: 11/11 skills available"
   - Partial: "kicad-happy: N/11 skills available. Missing: [list]. Install kicad-happy via Claude Code plugin system."
   - None: "WARNING: Required dependency kicad-happy is not installed. Install it via the Claude Code plugin system."
4. If `.hardware/config.yml` exists with `dependencies.kicad_happy_version`:
   - Compare installed version against required version
   - Warn on mismatch: "kicad-happy version X.Y.Z installed; hardware-team requires >=A.B.C."
5. Exit 0 always (informational, never blocks)

### 9.4 PreToolUse: Pipeline Bypass Detection (F-04 Resolution)

**Script**: `hooks/check_pipeline_bypass.py`

**Logic**:
1. Read `$TOOL_INPUT` from the environment to get the skill being invoked
2. Check if the invoked skill is a hardware-team role skill: `hardware-team:electrical-engineer`, `hardware-team:pcb-layout-engineer`, `hardware-team:manufacturing-engineer`, `hardware-team:compliance-engineer`, `hardware-team:test-engineer`, `hardware-team:hw-product-owner`
3. If it is a role skill:
   a. Check if `.hardware/config.yml` exists (proxy for active pipeline context)
   b. If no config exists: print warning: "Role skills should be invoked through the hardware-flow pipeline for gate validation and quality tracking. Run hardware-team:hardware-flow first, or say 'skip pipeline' to proceed without quality gates."
   c. If config exists: check `.hardware/state.md` for `status: in_progress`. If not in progress, print same warning.
4. If it is NOT a role skill (e.g., `hardware-team:hardware-flow` itself, or any non-hardware-team skill): no output.
5. Exit 0 always (warning only, never blocks skill invocation).

This mirrors delivery-team's pipeline bypass detection hook, preventing users from invoking role skills directly and bypassing the pipeline's quality guardrails.

### 9.5 PostToolUse: KiCad File Modification Notification (P1, F-06 Resolution)

**Script**: `hooks/check_kicad_file.py` (command-type, replaces previous prompt-type hook)

**Logic**:
1. Read `$TOOL_INPUT` from the environment (JSON containing the file path)
2. Extract the file path from the tool input
3. Check if the file extension is `.kicad_sch` or `.kicad_pcb`
4. If yes: print "KiCad file modified: [filename]. Consider running the appropriate validation gate (schematic-review or DRC) to check for issues."
5. If no: exit silently (no output)
6. Exit 0 always (informational, never blocks)

> **Rationale (F-06):** The previous prompt-type hook triggered an LLM inference call on every Write/Edit operation to check a file extension -- a simple string suffix check. The command-type Python script performs this check in microseconds and exits silently for non-KiCad files, eliminating hundreds of unnecessary LLM calls per session.

Full DRC auto-validation (Story 5.4) and BOM drift detection (Story 5.5) are P2 scope. The P1 notification provides awareness without the complexity of automated validation.

### 9.6 Hook Script Security Standards (SEC-06 Resolution)

> "The hooks are the gates of the forge. What enters through them must be examined with care, lest a poisoned ingot corrupt the work."

All hook scripts receive input via environment variables (`$TOOL_INPUT`, `$CLAUDE_PLUGIN_ROOT`). The following coding standards apply to all hook scripts in `hooks/`:

1. **JSON parsing only**: Hook scripts MUST parse `$TOOL_INPUT` as JSON using `json.loads()`. NEVER use `eval()`, `exec()`, or string interpolation to extract values from `$TOOL_INPUT`.
2. **No shell execution of input data**: Hook scripts MUST NOT pass any value extracted from `$TOOL_INPUT` or `$CLAUDE_PLUGIN_ROOT` to `os.system()`, `subprocess.run(shell=True)`, or any shell command constructor. All subprocess invocations (if any) MUST use `subprocess.run()` with `shell=False` and argument lists.
3. **Path validation**: If a hook script constructs file paths from environment variable values (e.g., `check_kicad_file.py` extracts a file path from `$TOOL_INPUT`), it MUST validate that the extracted path does not contain path traversal sequences before any filesystem operation. Use the same whitelist pattern as `state_manager.py` (Section 7.2) or `os.path.realpath()` canonicalization.
4. **Fail safe**: All hooks exit 0 regardless of errors. Errors in input parsing (malformed JSON, missing fields) are logged as warnings but never block the session.

**Template for hook input parsing:**

```python
import json
import os
import sys

def main():
    tool_input_raw = os.environ.get("TOOL_INPUT", "{}")
    try:
        tool_input = json.loads(tool_input_raw)
    except json.JSONDecodeError:
        # Malformed input -- fail safe, do nothing
        sys.exit(0)
    
    # Extract and validate fields -- NEVER pass to shell
    # ... hook logic here ...

if __name__ == "__main__":
    main()
```

---

## 10. Iterative Review Agent Pattern

> "Multiple eyes see what one eye misses. The greatest smiths always had their work reviewed by their peers -- not once, but many times, until the metal rang true."

### 10.1 Schematic Review Gate Architecture

The iterative review pattern from issue #76 is the foundation for the Schematic Review Gate (Story 4.1).

```
Schematic Review Gate
  |
  +-- Pass 1: Agent(EE-Reviewer-1) with forced-find prompting
  |     |
  |     +-- Loads: electrical-engineer/SKILL.md + schematic-review.md
  |     +-- Prompt includes: "You MUST identify at least 2 potential issues across
  |     |   the 7 review categories. If you believe none are real, explain why each
  |     |   candidate was dismissed. For each of the 7 categories, report whether you
  |     |   examined it: CATEGORY_EXAMINED: <name> or CATEGORY_NOT_EXAMINED: <name>."
  |     +-- Invokes: kicad-happy:kicad for schematic analysis
  |     +-- Produces: findings list [{id, severity, category, location, description, fix}]
  |
  +-- Pass 2: Agent(EE-Reviewer-2) with forced-find prompting
  |     |
  |     +-- Same references, INDEPENDENT context (no access to Pass 1 findings)
  |     +-- Same forced-find prompting
  |     +-- Produces: independent findings list
  |
  +-- (Optional Pass 3..N based on review.schematic_review_passes config)
  |
  +-- Deduplication Engine (deterministic algorithm in orchestrator, not a sub-agent)
  |     |
  |     +-- Deterministic matching rules (see 10.1.1 below)
  |     +-- Merge duplicates: keep highest severity, tag "confirmed by N reviewers"
  |     +-- Findings confirmed by multiple reviewers get elevated confidence
  |
  +-- Coverage Check (F-11 resolution: replaces convergence check)
  |     |
  |     +-- Track which of the 7 review categories have been examined across all passes.
  |     +-- A category is "covered" if at least one reviewer produced a finding in that
  |     |   category OR explicitly stated the category was examined and found clean.
  |     +-- Coverage is met when all 7 categories have been covered by at least one
  |     |   reviewer OR the configured number of passes is reached, whichever comes first.
  |     +-- This ensures systematic coverage rather than relying on finding-overlap coincidence.
  |
  +-- Gate Evaluation (severity thresholds governed by `gate_strictness` config)
        |
        +-- Evaluation varies by strictness level (F-13 resolution):
        |
        |   | Strictness | Critical Finding | Major Finding | Minor Finding |
        |   |---|---|---|---|
        |   | strict | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) |
        |   | standard (default) | BLOCKS (NOT_DONE) | BLOCKS (NOT_DONE) | PASS (logged in gate results) |
        |   | relaxed | BLOCKS (NOT_DONE) | PASS (logged as warning) | PASS (logged in gate results) |
        |
        +-- Zero findings --> DONE (clean pass) regardless of strictness
        +-- All non-blocking findings are documented in gate results for visibility
```

### 10.1.1 Deterministic Deduplication Algorithm (F-02 Resolution)

> "Two smiths may name the same flaw differently, but the flaw itself is one. We must have a law of identity, not a guess."

The deduplication engine operates as a deterministic algorithm -- NOT an LLM inference step. This is critical because gate decisions depend on deduplication results, and gates must be deterministic per the Business Rules Engine principle (see CLAUDE.md).

**Matching Rules:**

Each finding from a reviewer is a structured object with fields: `id`, `severity`, `category`, `component`, `net`, `board_issue_id`, `description`, `fix`.

Two findings F1 and F2 are considered **duplicates** if and only if ALL of the following match:

| Field | Match Criterion |
|---|---|
| `component` | Exact string match (e.g., "C7" == "C7"). Case-insensitive. |
| `category` | Exact string match from the 7 review categories (e.g., "component-derating" == "component-derating"). |

If `component` matches but `category` differs, the findings are **distinct**. Rationale: a derating issue and a thermal issue on the same component are different problems requiring different fixes, even though they affect the same part.

If `category` matches but `component` differs, the findings are **distinct**. Rationale: derating on C7 and derating on C12 are different findings.

**Net-level findings** (where `component` is null/empty but `net` is specified, e.g., "VCC_3V3 rail has insufficient bulk capacitance"):
- Match on: `net` (exact string match, case-insensitive) AND `category` (exact match).

**Board-level findings** (where both `component` and `net` are null/empty, e.g., "decoupling strategy is globally insufficient"):
- Match on: `category` (exact match) AND `board_issue_id` (exact string match, case-insensitive).
- Each reviewer prompt MUST classify board-level findings with a `board_issue_id` tag from the defined enum below. This shifts deduplication responsibility to the reviewer prompts (structured classification at generation time) rather than post-hoc text matching, preserving full determinism.
- If a board-level finding does not include a `board_issue_id`, it is treated as **distinct** from all other findings (conservative fallback -- the reviewer failed to classify, so we do not guess).

**Board Issue ID Enum** (extensible -- add new IDs as new global failure patterns are identified):

| `board_issue_id` | Description |
|---|---|
| `global-decoupling` | Global decoupling strategy is insufficient or absent |
| `power-sequencing` | Power supply sequencing order is incorrect or uncontrolled |
| `ground-plane` | Ground plane integrity issue (splits, insufficient copper, impedance) |
| `thermal-management` | Board-level thermal dissipation strategy inadequate |
| `emc-shielding` | Board-level EMC/EMI shielding strategy inadequate |
| `stack-up` | PCB stackup choice creates systemic signal/power integrity issues |
| `voltage-domain-isolation` | Mixed voltage domains lack proper isolation or level shifting |
| `clock-distribution` | Clock distribution topology creates systemic jitter/skew issues |

**Reviewer prompt addition** (injected into each EE-Reviewer and Design Review Board reviewer):
```
For any finding that is board-level (not tied to a specific component or net),
you MUST include a `board_issue_id` field with a value from the board issue
enum: global-decoupling, power-sequencing, ground-plane, thermal-management,
emc-shielding, stack-up, voltage-domain-isolation, clock-distribution.
If none of the enum values fit, use "other-<brief-descriptor>" and the finding
will be treated as distinct (not deduplicated).
```

**Merge Behavior (when duplicates are identified):**

1. **Severity**: Keep the highest severity. Severity ordering: critical > major > minor > info.
2. **Description**: Concatenate both descriptions with reviewer attribution: "Reviewer 1: <desc1>. Reviewer 2: <desc2>."
3. **Fix**: Keep both fix suggestions, attributed by reviewer.
4. **Confirmation tag**: Add `confirmed_by: N` where N is the number of reviewers who independently identified this finding. Confirmed findings (N >= 2) get elevated confidence in the gate report.

**Why deterministic, not LLM-based:** The orchestrator is already managing pipeline state, rework tracking, memory injection, and stage dispatch. Adding a deduplication inference step in the orchestrator context introduces non-determinism in gate outcomes -- the same set of findings could produce different deduplicated results on a re-run, potentially flipping a gate between DONE and NOT_DONE. The deterministic algorithm eliminates this risk entirely.

### 10.2 Review Categories (7)

| # | Category | What It Checks |
|---|---|---|
| 1 | Power Integrity | Bulk caps, decoupling, voltage regulator stability, power sequencing |
| 2 | Signal Integrity | Termination, impedance matching, crosstalk risk, high-speed routing |
| 3 | Component Derating | Voltage/current/temperature derating vs. operating conditions |
| 4 | Pull-ups/Pull-downs | Floating inputs, I2C bus pull-ups, reset pins, enable pins |
| 5 | Decoupling Strategy | Per-IC decoupling, capacitor value selection, placement distance |
| 6 | Voltage Level Compatibility | Logic level translation, mixed-voltage interfaces, tolerance bands |
| 7 | Thermal Considerations | Power dissipation, thermal relief, heat sink requirements |

### 10.3 Configuration

| Parameter | Default | Source | Description |
|---|---|---|---|
| Number of review passes | 2 | `review.schematic_review_passes` in config | How many independent reviewers run |
| Forced-find minimum | 2 | Hardcoded in gate framework | Each reviewer must find at least 2 candidates |
| Coverage threshold | All 7 categories examined | Hardcoded in gate framework | Stop when all 7 review categories covered by at least one reviewer, or configured passes reached |

### 10.4 Model Tier Requirements (OQ-003 Resolution)

Per issue #76 learnings: Haiku is insufficient for geometric/spatial reasoning tasks. Each role's SKILL.md documents its minimum model tier in the frontmatter.

| Role | Minimum Model Tier | Rationale |
|---|---|---|
| HW Product Owner | Haiku | Text-based requirements capture, no spatial reasoning needed |
| Electrical Engineer | Sonnet | Circuit analysis requires moderate structured reasoning |
| PCB Layout Engineer | Sonnet+ | Geometric/spatial reasoning for layout review (Haiku insufficient per #76) |
| Manufacturing Engineer | Sonnet | DFM rules require structured pattern matching |
| Compliance Engineer | Sonnet | Regulatory frameworks require structured cross-referencing |
| Test Engineer | Haiku | Test planning is primarily text-based strategy |
| Schematic Review Gate (reviewers) | Sonnet+ | Multi-category forced-find review demands strong analytical reasoning |

**Enforcement**: Phase 1 is documentation-only (minimum tier stated in SKILL.md frontmatter). The orchestrator announces the recommended tier at stage dispatch but does not programmatically enforce it. Programmatic enforcement (detecting the active model and warning/blocking) is a Phase 2 enhancement.

### 10.5 Design Review Board

The Design Review Board is a multi-role review collaboration pattern applied at key stage transitions:

**Trigger points**: Post-Schematic gate, Post-Layout gate (configurable via `review.design_review_board`)

```
Design Review Board
  |
  +-- Agent(EE) -- reviews from electrical correctness perspective
  +-- Agent(PCB Layout) -- reviews from layout feasibility perspective
  +-- Agent(MfgE) -- reviews from manufacturability perspective
  +-- Agent(CompE) -- reviews from regulatory impact perspective
  |
  (Each reviewer is INDEPENDENT -- no shared context during review)
  |
  +-- Findings aggregated by orchestrator with cross-reviewer deduplication
  +-- Unified severity ranking across all reviewers
  |
  +-- Zero findings: collapsed summary ("All reviewers: APPROVE -- no findings.")
  +-- Findings present: per-reviewer breakdown with unified severity ranking
```

This mirrors delivery-team's adversarial review and review board patterns, adapted for hardware domain expertise.

---

## 11. Component Interaction Diagrams

### C4 Context Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        Claude Code Session                       │
│                                                                  │
│  ┌────────────────┐     ┌─────────────────┐                     │
│  │  hardware-team  │────→│   kicad-happy    │                     │
│  │    plugin       │     │    plugin        │                     │
│  │                 │     │   (external      │                     │
│  │  8-stage        │     │    dependency)   │                     │
│  │  pipeline       │     │  11 specialist   │                     │
│  │  6 roles        │     │  skills          │                     │
│  └───────┬────────┘     └─────────────────┘                     │
│          │                                                       │
│          │ reads/writes                                           │
│          ▼                                                       │
│  ┌────────────────┐                                              │
│  │  .hardware/     │  Project-local state                        │
│  │  config.yml     │  managed by orchestrator                    │
│  │  state.md       │                                              │
│  │  memory/        │                                              │
│  │  artifacts/     │                                              │
│  └────────────────┘                                              │
│          │                                                       │
│          │ analyzes                                               │
│          ▼                                                       │
│  ┌────────────────┐                                              │
│  │  KiCad Project  │  User's hardware design files               │
│  │  .kicad_pro     │                                              │
│  │  .kicad_sch     │                                              │
│  │  .kicad_pcb     │                                              │
│  └────────────────┘                                              │
│                                                                  │
│  ┌────────────────┐                                              │
│  │     Human       │  Physical stages: Prototype, Pilot Run,     │
│  │    Engineer     │  Production Release                         │
│  └────────────────┘                                              │
└──────────────────────────────────────────────────────────────────┘
```

### C4 Container Diagram (hardware-team internal)

```
┌────────────────────── hardware-team plugin ───────────────────────┐
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              hardware-flow (orchestrator)                  │    │
│  │  Pipeline stages | Gates | Rework | State | Memory        │    │
│  │  Config loading | Setup wizard | Stage dispatch            │    │
│  │  NEVER produces domain artifacts (Prime Directive)         │    │
│  └───────────────────────┬──────────────────────────────────┘    │
│                          │ dispatches via Agent tool              │
│         ┌────────┬───────┼───────┬──────────┬────────┐          │
│         ▼        ▼       ▼       ▼          ▼        ▼          │
│  ┌──────────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌────────┐ ┌──────┐    │
│  │  HW PO   │ │ EE  │ │ PCB │ │MfgE │ │ CompE  │ │TestE │    │
│  │          │ │     │ │Layout│ │     │ │        │ │      │    │
│  │ Concept  │ │Schem│ │Layou│ │DFM/ │ │Compli- │ │Proto-│    │
│  │ stage    │ │stage│ │stage│ │DFA  │ │ance    │ │type  │    │
│  └──────────┘ └──┬──┘ └──┬──┘ └──┬──┘ └───┬────┘ └──────┘    │
│                  │       │       │         │                     │
│                  ▼       ▼       ▼         ▼                     │
│            ┌─────────────────────────────────────┐               │
│            │      Skill tool invocations         │               │
│            │    (cross-plugin to kicad-happy)     │               │
│            └─────────────────────────────────────┘               │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ SessionStart     │  │ PreToolUse       │  │ PostToolUse      │ │
│  │ Hooks            │  │ Hook             │  │ Hook             │ │
│  │ config check     │  │ pipeline bypass  │  │ KiCad file       │ │
│  │ kicad-happy deps │  │ detection        │  │ notification     │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
         │                    │
         │ cross-plugin       │
         │ Skill tool         │
         ▼                    ▼
┌─────────────────── kicad-happy plugin ───────────────────────────┐
│ kicad | spice | digikey | mouser | lcsc | element14 |           │
│ jlcpcb | pcbway | bom | emc | kidoc                            │
│                                                                  │
│ Installed at: ~/.claude/plugins/cache/kicad-happy/              │
│ Version: 1.2.0+                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Trade-Off Analysis

| Decision | Option A | Option B | Chosen | Rationale |
|---|---|---|---|---|
| Plugin structure | Custom structure | Mirror delivery-team layout | Mirror delivery-team (B) | Proven pattern; reduces risk; consistent with ecosystem. See ADR-001. |
| kicad-happy integration | Embed kicad-happy references | Cross-plugin Skill invocation | Cross-plugin (B) | Verified working; avoids duplication; respects NFR-003. See ADR-002. |
| Stage count | 8 stages | 5-6 merged stages | 8 stages (A) | Maps 1:1 to real hardware dev; clear responsibility per stage. See ADR-003. |
| Human stage pattern | Attempt full automation | Gate-in/human-action/gate-out | Gate pattern (B) | Physical work cannot be automated by AI. See ADR-004. |
| Namespace | `.delivery/` shared | `.hardware/` separate | Separate (B) | Avoids config collision; clean plugin boundary; independent lifecycle. |
| Rework model | Linear-only pipeline | DAG with bounded backward edges | DAG (B) | Reflects real hardware iteration; bounded by termination conditions. |
| Model tier enforcement | Programmatic at pipeline start | Documentation-only in SKILL.md | Documentation (B for P1) | Simpler P1; programmatic enforcement deferred to P2. |
| Memory system | Shared with `.delivery/memory/` | Separate `.hardware/memory/` | Separate (B) | Clean isolation; hardware lessons don't pollute software memories. |

---

## Quality Attributes

| Attribute | Requirement | How Addressed |
|---|---|---|
| **Modularity** | Each role loads only its own references | Context isolation via separate SKILL.md per role; sub-agent dispatch prevents reference bleed |
| **Extensibility** | New roles and stages can be added without modifying existing skills | Skill directory pattern; config schema forward-compatible; marketplace.json additive |
| **Reliability** | Pipeline does not crash on missing dependencies | Graceful degradation on kicad-happy unavailability; config defaults on invalid values; never fail on config errors |
| **Auditability** | Every gate result, rework event, and stage transition is logged | State file with full history; rework events with timestamps and resolutions |
| **Portability** | No external dependencies beyond Python standard library | All scripts use stdlib only; no pip install required (NFR-001) |
| **Resumability** | Pipeline state survives session boundaries | State persisted to `.hardware/state.md` with config snapshot for divergence detection |
| **Usability** | Gate messages comprehensible to hardware engineers | All findings include: what failed, where (component/net/location), why, and how to fix (NFR-005) |
| **Security** | No path traversal, no YAML injection, sensitive data classified | Path sanitization with sandbox check (SEC-01); `yaml.safe_load()` mandate (SEC-03); BOM data classification with `.gitignore` guidance (SEC-02); hook input sanitization (SEC-06); trust boundaries documented (SEC-04, SEC-05) |

---

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| kicad-happy API/interface changes break dispatch | High | Medium | Config tracks minimum version; explicit output contracts defined in `kicad-integration.md` (Section 5.5); runtime contract assertion in each sub-agent (HW-KCH-004); SessionStart hook warns on version mismatch |
| Context window exhaustion in complex pipelines | Medium | Medium | Three-level loading; sub-agents load only role references; memory tiering with capped injection |
| Rework loops consume excessive context/time | Medium | Medium | Termination conditions (3 per path, 10 total); human escalation with clear options |
| Model tier insufficient for spatial reasoning | High | High (for Haiku) | Documented per-role minimum tiers; Sonnet+ required for layout and review gates; programmatic enforcement in P2 |
| Test fixture seeded defects too artificial | Medium | Low | Based on real-world defect patterns from issue #76; manifest documents each defect with realistic engineering context |
| Config schema evolution breaks old configs | Medium | Low | Forward-compatible schema; missing keys use defaults; unknown keys ignored; version-guided migration |
| Sensitive BOM data committed to public repo | High | Medium | Data classification (Section 14.2); `.gitignore` recommendations in setup wizard; no-pricing filter in memory system |
| Path traversal via crafted config values | High | Low | Whitelist validation + canonicalization in `state_manager.py` (Section 7.2); `HW-STA-005` error on violation |

---

## Assumptions

1. The kicad-happy plugin maintains backward-compatible skill interfaces within a major version (verified at runtime via output contract assertions -- Section 5.5)
2. Cross-plugin skill invocation via the Skill tool is a stable platform feature (verified working)
3. The Agent tool supports sufficient context for sub-agent dispatch with SKILL.md + references
4. Hardware engineers working with this plugin have KiCad project files on the local filesystem
5. Python 3.x standard library is sufficient for all validation scripts (no pip install)
6. The `.hardware/` namespace does not conflict with any existing tool or convention
7. Two review passes are sufficient for the Schematic Review Gate (configurable up to 5)
8. Single-board PCB designs are the dominant use case for Phase 1
9. BOM pricing and supplier data are commercially sensitive and should not be committed to public repositories (SEC-02)
10. The Claude Code plugin harness ensures plugin cache integrity; plugin-level authenticity verification is not required (SEC-04)

---

## 12. End-to-End Testability Strategy (X1 Resolution)

> "A forge untested is a forge untrusted. We must know what can be proven by fire, what requires the smith's own hand, and what the test fixtures reveal."

### 12.1 Testability Classification

| What to Test | Test Type | Method | Automation |
|---|---|---|---|
| Gate evaluation logic | Unit | Run each gate validator against the reference test fixture (Story 4.0) with known-good and known-bad inputs. Verify DONE/NOT_DONE results match expected outcomes. | **Fully automated.** Test fixture + expected results manifest. |
| Rework path triggers | Unit | For each of the 7 rework paths, supply a gate output that should trigger rework and verify the orchestrator selects the correct target stage. | **Fully automated.** Input/output pairs for each rework path. |
| Rework termination | Unit | Simulate N rework iterations and verify the pipeline PAUSES at the configured limit (3 per path, 10 total). | **Fully automated.** Counter-based simulation. |
| State file CRUD | Unit | Create, update, pause, resume, complete, and abort a pipeline state. Verify YAML integrity after each operation. | **Fully automated.** `state_manager.py` function tests. |
| State file corruption recovery | Unit | Feed malformed YAML to the resume protocol. Verify `STATE_FILE_CORRUPTED` is emitted with correct error details and options. | **Fully automated.** Pre-crafted corrupted state files. |
| Config validation | Unit | Run `validate_config.py` against valid, invalid, outdated, and missing configs. Verify warnings, defaults, and migration messages. | **Fully automated.** Config fixture set. |
| Reference availability check | Unit | Invoke a sub-agent prompt template with missing reference paths. Verify `REFERENCE_MISSING` signal in output. | **Semi-automated.** Requires Agent tool invocation with controlled filesystem. |
| Full 8-stage pipeline (happy path) | Integration | Run the pipeline against the reference KiCad project with all kicad-happy skills available. Verify all 8 stages complete, all gates evaluate, artifacts are produced. | **Manual.** Requires human confirmation at Stages 4, 7, 8. |
| Human-execution pause/resume | Integration | Start pipeline, allow it to reach Stage 4, confirm it pauses. Close session. Start new session, verify SessionStart hook reports paused state. Resume and verify continuation from Stage 4. | **Manual.** Cross-session by nature. |
| Memory injection round-trip | Integration | Run pipeline once (generates memories). Run pipeline again on same project, verify memories are injected and `MEMORY_APPLIED`/`MEMORY_NOTED` signals appear. | **Manual.** Requires two pipeline runs. |
| kicad-happy unavailability | Integration | Temporarily rename the kicad-happy plugin cache directory. Run pipeline and verify `SKILL_UNAVAILABLE` signals, graceful degradation, and pipeline continuation. | **Semi-automated.** Filesystem manipulation + pipeline run. |
| Sub-agent dispatch failure | Integration | Intentionally trigger a context overflow (oversized reference set). Verify `PAUSED_DISPATCH_ERROR` state with correct error classification and user options. | **Semi-automated.** Requires crafted oversized context. |
| Path sanitization (SEC-01) | Unit | Call `sanitize_path_component()` with safe values (`run-2026-04-12-hw01`), unsafe values (`../../etc/passwd`, `foo/bar`, `foo\bar`, `foo\x00bar`). Verify safe values pass and unsafe values raise `ValueError`. Call `safe_join()` with components that would escape `.hardware/` sandbox. Verify `HW-STA-005` is raised. | **Fully automated.** Input/output pairs for whitelist and canonicalization. |
| Memory no-pricing filter (SEC-02) | Unit | Submit memory entries containing pricing patterns (`$0.12/unit`, `EUR 1.50`, `quoted at $0.08`). Verify pricing values are redacted to `[PRICE REDACTED]` and `HW-SEC-001` is logged. Submit entries without pricing. Verify they pass through unmodified. | **Fully automated.** Pattern matching test fixtures. |
| YAML safe_load enforcement (SEC-03) | Unit | Feed YAML containing `!!python/object/apply:os.system` tags to `state_manager.py` and `validate_config.py`. Verify `yaml.safe_load()` raises `yaml.constructor.ConstructorError` (tag rejected) rather than executing the payload. | **Fully automated.** Crafted malicious YAML fixtures. |
| Hook input sanitization (SEC-06) | Unit | Set `$TOOL_INPUT` to malformed JSON, JSON with shell metacharacters, and JSON with path traversal sequences. Run each hook script. Verify all exit 0, no shell commands executed, no files created outside `.hardware/`. | **Fully automated.** Environment variable fixtures. |

### 12.2 Test Fixture Coverage

The reference KiCad project (Story 4.0) in `references/test-fixtures/` covers:

| Fixture Component | What It Tests | Defects Seeded |
|---|---|---|
| `reference.kicad_sch` | Schematic Review Gate (7 categories) | 10 defects across power integrity, signal integrity, derating, pull-ups, decoupling, voltage levels, thermal |
| `reference.kicad_pcb` | DRC Gate, DFM Gate | DFM violations (trace width, clearance, via size) |
| `reference-bom.csv` | BOM Gate | Single-source components, over-budget items, obsolete parts |
| `reference-pricing.json` | Offline BOM validation | Static pricing data (no API calls needed for testing) |

**Not covered by test fixtures** (requires manual validation):
- Human-execution stage flow (physical by nature)
- Cross-session state persistence (requires real session boundaries)
- Memory relevance scoring across multiple runs (requires real pipeline history)
- kicad-happy version compatibility (requires different installed versions)

### 12.3 Test Execution Procedure

1. **Before implementation**: Validate test fixture manifest against seeded defects
2. **After each skill creation**: Run `plugin-dev:skill-reviewer`
3. **After plugin skeleton**: Run `plugin-dev:plugin-validator`
4. **After gate implementation**: Run gate validators against test fixtures, verify expected DONE/NOT_DONE results
5. **After orchestrator implementation**: Run full integration test (manual, with human-execution stage confirmation)
6. **After memory implementation**: Run two consecutive pipeline runs, verify memory round-trip

---

## 13. Error Taxonomy (X2 Resolution)

> "Every crack in the metal has a name. To name the failure is the first step toward preventing it."

All error conditions across the architecture are classified into a unified taxonomy. Each error has: a code, a detecting component, a severity, and a defined response.

### 13.1 Error Code Format

`HW-<COMPONENT>-<NUMBER>` where COMPONENT is a 3-letter abbreviation:

| Component Code | Component |
|---|---|
| `DIS` | Sub-agent dispatch |
| `GAT` | Gate evaluation |
| `RWK` | Rework loop |
| `STA` | State management |
| `CFG` | Config validation |
| `REF` | Reference loading |
| `MEM` | Memory system |
| `KCH` | kicad-happy integration |
| `HUM` | Human-execution stages |
| `HOK` | Hooks |
| `SEC` | Security controls |

### 13.2 Full Error Taxonomy

| Code | Error Condition | Detecting Component | Severity | Response Behavior |
|---|---|---|---|---|
| `HW-DIS-001` | Sub-agent dispatch timeout | Orchestrator | Critical | Retry once, then PAUSE with `PAUSED_DISPATCH_ERROR`. User options: Retry / Skip / Abort. |
| `HW-DIS-002` | Sub-agent context overflow | Orchestrator | Critical | Retry once (with reduced references if possible), then PAUSE. User options: Retry / Skip / Abort. |
| `HW-DIS-003` | Sub-agent model error | Orchestrator | Major | Retry once, then PAUSE. Typically transient. |
| `HW-DIS-004` | Sub-agent unknown error | Orchestrator | Critical | Retry once, then PAUSE. Log full error for diagnosis. |
| `HW-GAT-001` | Gate returns NOT_DONE (critical finding) | Gate evaluator | Critical | Pipeline blocks. Rework triggered if rework path exists. |
| `HW-GAT-002` | Gate returns NOT_DONE (major finding) | Gate evaluator | Major | Pipeline blocks. Rework triggered if rework path exists. |
| `HW-GAT-003` | Gate returns DONE with warnings | Gate evaluator | Info | Pipeline advances. Warnings logged in gate results. |
| `HW-RWK-001` | Per-path rework limit exceeded | Orchestrator | Major | Pipeline PAUSES. Escalation to human with rework history. |
| `HW-RWK-002` | Total rework limit exceeded | Orchestrator | Major | Pipeline PAUSES. Escalation to human with full rework history. |
| `HW-STA-001` | State file YAML parse failure | Resume protocol / `state_manager.py` | Critical | Cannot resume. Options: Restart (archive corrupted file) / Manual Fix. |
| `HW-STA-002` | State file missing required fields | Resume protocol / `state_manager.py` | Critical | Cannot resume. Options: Restart / Manual Fix. |
| `HW-STA-003` | Artifact file missing on resume | Resume protocol | Major | Announce missing artifacts. Options: Restart from that stage / Abandon. |
| `HW-STA-004` | Config snapshot divergence on resume | Resume protocol | Warning | Warn user. Resume uses original config; Restart applies new config. |
| `HW-CFG-001` | Config file missing | SessionStart hook | Warning | Print: "No .hardware/config.yml found. Run `hw-setup`." Pipeline uses all defaults. |
| `HW-CFG-002` | Config schema version outdated | SessionStart hook | Info | Announce new defaults applied. Pipeline continues. |
| `HW-CFG-003` | Config field invalid value | SessionStart hook | Warning | Warn per-field. Use default. Pipeline continues. |
| `HW-REF-001` | Reference file missing | Sub-agent (Level 3 load) | Warning | `REFERENCE_MISSING` signal. Sub-agent continues with degraded capability. |
| `HW-REF-002` | Reference file unreadable | Sub-agent (Level 3 load) | Warning | `REFERENCE_CORRUPTED` signal. Sub-agent continues with degraded capability. |
| `HW-MEM-001` | Memory index file missing | Orchestrator (memory read) | Info | No lessons injected. Pipeline continues normally. |
| `HW-MEM-002` | Memory stage file missing | Orchestrator (memory read) | Info | No lessons injected for that stage. Pipeline continues normally. |
| `HW-MEM-003` | Memory stage file unparseable | Orchestrator (memory read) | Warning | Skip memory injection for that stage. Log warning. Pipeline continues. |
| `HW-KCH-001` | kicad-happy skill not installed | Sub-agent (Skill tool) | Major | `SKILL_UNAVAILABLE` signal. Graceful degradation. Pipeline continues. |
| `HW-KCH-002` | kicad-happy version mismatch | SessionStart hook | Warning | Warn about version incompatibility. Pipeline continues. |
| `HW-KCH-003` | kicad-happy skill invocation error | Sub-agent | Major | Report error in sub-agent output. Gate evaluates on available data. |
| `HW-KCH-004` | kicad-happy output contract mismatch | Sub-agent (post-invocation) | Major | `CONTRACT_MISMATCH` signal. Sub-agent does NOT process malformed data. Gate evaluates on available data. |
| `HW-HUM-001` | Pipeline staleness warning | SessionStart hook | Warning | Warn: pipeline paused > N days. Options: Resume / Restart / Abandon. |
| `HW-HUM-002` | Pipeline critical staleness | SessionStart hook | Major | Strongly recommend Restart over Resume. |
| `HW-HUM-003` | Human stage reports failure | Orchestrator | Major | Rework triggered via standard rework path table. |
| `HW-HOK-001` | Hook script execution error | Claude Code harness | Info | Hooks always exit 0. Errors are informational. Session continues. |
| `HW-STA-005` | Path traversal detected | `state_manager.py` / `safe_join()` | Critical | Path construction blocked. Pipeline cannot proceed with unsafe path component. User must fix config value (e.g., `pipeline_id`, `project_name`). |
| `HW-SEC-001` | Pricing data detected in memory entry | Orchestrator (memory write) | Warning | Memory entry redacted. Pricing values stripped before persistence. Pipeline continues. |

### 13.3 Severity Definitions

| Severity | Pipeline Impact | User Action Required |
|---|---|---|
| **Critical** | Pipeline cannot continue automatically | User must choose: Retry / Restart / Abort |
| **Major** | Pipeline pauses or degrades significantly | User should review and decide |
| **Warning** | Pipeline continues with noted limitation | User informed; no action required |
| **Info** | No impact on pipeline execution | Logged for visibility |

---

## 14. Security

> "The finest rings were undone not by brute force, but by subtle corruption -- a whispered word, a hidden flaw, a path that led where it should not. We must name our defenses as clearly as we name our designs."

This section consolidates all security controls, trust boundaries, and accepted risks for the hardware-team plugin. It is the authoritative reference for security posture.

### 14.1 Coding Standards (SEC-03, SEC-06 Resolution)

The following coding standards apply to ALL Python scripts in the hardware-team plugin (`scripts/`, `hooks/`, `skills/*/scripts/`):

| Standard | Requirement | Rationale |
|---|---|---|
| **YAML parsing** | Always use `yaml.safe_load()`. Never use `yaml.load()`, `yaml.FullLoader`, or `yaml.UnsafeLoader`. | Prevents YAML deserialization attacks (arbitrary code execution via `!!python/object` tags). SEC-03. |
| **JSON parsing** | Always use `json.loads()`. Never use `eval()` or `exec()` on JSON strings. | Prevents code injection via crafted JSON payloads. SEC-06. |
| **Subprocess invocation** | Always use `subprocess.run(shell=False)` with argument lists. Never use `shell=True`, `os.system()`, or `os.popen()`. | Prevents command injection via environment variable values. SEC-06. |
| **Path construction** | Always use `safe_join()` from `state_manager.py`. Never use raw string interpolation or unchecked `os.path.join()` for paths derived from user-controlled values. | Prevents path traversal outside the `.hardware/` sandbox. SEC-01. |
| **Environment variable handling** | Treat all values from `$TOOL_INPUT` and `$CLAUDE_PLUGIN_ROOT` as untrusted input. Parse, validate, then use. | Defense in depth for hook scripts. SEC-06. |

### 14.2 Data Classification (SEC-02 Resolution)

> "Not all knowledge should be shared freely. The price of mithril is known to the smith, but need not be etched upon the blade."

BOM artifacts contain commercially sensitive data that must be handled with care. The following data classification applies:

| Classification | Fields | Handling Rules |
|---|---|---|
| **SENSITIVE** | `unit_price`, `total_cost`, `sources[].account_id`, negotiated pricing terms, supplier-specific discount rates | Must not be committed to public repositories. Must not be captured in memory entries. Must be redacted in any artifact shared outside the project. |
| **INTERNAL** | `sources[].supplier_name`, `sources[].mpn`, `datasheet_url`, stock levels | May be committed to private repositories. May be captured in memory entries (part numbers and technical rationale only). |
| **PUBLIC** | Component descriptions, package types, footprint names, reference designators, quantities | No restrictions. |

**Artifact-level classification:**

| Artifact | Classification | Rationale |
|---|---|---|
| `.hardware/artifacts/05-dfm-dfa/bom-validation.md` | SENSITIVE | Contains unit prices and cost totals |
| `.hardware/artifacts/08-production-release/final-bom.md` | SENSITIVE | Contains final pricing and supplier sourcing |
| `.hardware/memory/` (all files) | INTERNAL | May contain component selection rationale (but no pricing per no-pricing filter) |
| All other `.hardware/artifacts/` files | INTERNAL | Engineering data, no pricing |

**`.gitignore` recommendations (setup wizard integration):**

The `hw-setup` wizard (Section 6) MUST offer to create or update the project's `.gitignore` with the following entries:

```gitignore
# hardware-team: sensitive BOM and pricing data
.hardware/artifacts/05-dfm-dfa/bom-validation.md
.hardware/artifacts/08-production-release/final-bom.md
.hardware/memory/
.hardware/config-snapshot-*.yml
```

The wizard presents this as a recommended default. The user may decline (e.g., for private repositories where pricing data exposure is acceptable). The wizard output includes a note: "BOM artifacts contain pricing data classified as SENSITIVE. If this is a public repository, these files should remain in .gitignore."

**Memory no-pricing filter (enforcement):**

During the memory write phase (Section 8.3), the orchestrator applies a no-pricing filter before persisting any memory entry:

1. Scan the `lesson` field for patterns matching pricing data: currency symbols followed by numbers (`$`, `EUR`, `GBP`, `JPY` + digits), phrases like "quoted", "priced at", "costs", "per unit" adjacent to numeric values
2. If detected: redact the pricing value and replace with `[PRICE REDACTED]`. Log `HW-SEC-001` as a warning.
3. The filter is best-effort pattern matching -- it may miss obfuscated pricing. The primary defense is the sub-agent prompt instruction (Section 8.3, step 5) which tells the sub-agent not to include pricing in lessons. The filter is a safety net.

### 14.3 Trust Boundaries

| Boundary | Trust Assumption | Documented In |
|---|---|---|
| Claude Code plugin harness | Ensures plugin authenticity and integrity in the plugin cache | Section 5.1 (SEC-04) |
| kicad-happy output | Structure validated via contracts (Section 5.5); semantic correctness trusted | Section 5.5 |
| `.hardware/state.md` | User-editable; semantic tampering is an accepted risk (SEC-05) | Section 7.2.1 |
| User-provided config values | Structurally validated (Section 6.2); path components sanitized (Section 7.2) | Section 7.2 (SEC-01) |
| Hook environment variables | Treated as untrusted input; parsed via `json.loads()` only | Section 9.6 (SEC-06) |

### 14.4 Accepted Risks

| Risk | Justification | Mitigating Controls |
|---|---|---|
| State file semantic tampering (SEC-05) | Local development tool; user is primary actor with legitimate override needs | Lightweight integrity hash with warning on mismatch (Section 7.2.1) |
| Plugin cache compromise (SEC-04) | Platform-level concern outside plugin scope | Output contract validation catches structural drift (Section 5.5) |
| Best-effort pricing redaction in memory | Pattern matching cannot catch all obfuscated pricing | Primary defense is sub-agent prompt instruction; filter is secondary safety net |

---

## Follow-Up

1. **ADRs produced**: ADR-001 (plugin structure), ADR-002 (kicad-happy integration), ADR-003 (pipeline stages), ADR-004 (human-execution stages) -- all updated with reversibility statements in v1.1
2. **QA evaluation findings addressed (v1.1)**: C2 (dispatch failure handling), C4 (staleness detection), C5 (reference availability check), C8 (state file corruption), C9 (memory influence observability), ADR reversibility statements (ADR-001, ADR-002, ADR-004), X1 (testability strategy), X2 (error taxonomy)
3. **Adversarial review findings addressed (v1.2)**:
   - **F-01 BLOCKING**: kicad-happy output contract validation -- added Section 5.5 with explicit contracts per consumed skill, runtime assertion protocol, and HW-KCH-004 error code
   - **F-02 BLOCKING**: Deterministic deduplication algorithm -- added Section 10.1.1 with exact matching rules (component + category), net-level and board-level matching, merge behavior, and rationale for deterministic over LLM-based approach
   - **F-03 ADVISORY**: State file format trade-off -- documented in Section 7.1 with requirement for robust frontmatter parser
   - **F-04 ADVISORY**: Pipeline bypass detection -- added PreToolUse hook (Section 9.4) with `check_pipeline_bypass.py`
   - **F-05 ADVISORY**: Compliance --> Layout rework path -- added to rework path table (Section 3.3) for layout-specific EMC failures; rework path table declared authoritative over ASCII diagram
   - **F-06 ADVISORY**: PostToolUse hook type -- replaced prompt-type with command-type `check_kicad_file.py` (Section 9.5) to eliminate per-operation LLM overhead
   - **F-07 ADVISORY**: Memory archival -- added Section 8.6 with archival threshold, decay floor, entries limit, and cleanup protocol
   - **F-08 ADVISORY**: Skill path prefix clarity -- added note after Section 2.1 table clarifying plugin-relative vs. repo-relative path conventions
4. **Adversarial review findings addressed (v1.3)**:
   - **F-09 BLOCKING**: Board-level Jaccard dedup replaced with structured `board_issue_id` tag matching -- Section 10.1.1 now uses a defined enum of board issue IDs with exact-match deduplication, eliminating all non-determinism from the dedup algorithm. Reviewer prompts require classification of board-level findings with a `board_issue_id` tag.
   - **F-09b ADVISORY**: Added `Pilot Run --> Schematic` rework path (Section 3.3) for circuit-level issues discovered during pilot run testing (thermal, tolerance, circuit behavior). Avoids double-hop through DFM/DFA.
   - **F-10 ADVISORY**: Config snapshot replaced with hash-based change detection (Section 7.1). State file stores SHA-256 hash only; full config preserved once as `.hardware/config-snapshot-<pipeline_id>.yml`. Mid-run config changes are unsupported.
   - **F-11 ADVISORY**: Convergence check replaced with coverage check (Section 10.1). Review passes stop when all 7 categories are covered or configured passes reached, ensuring systematic coverage instead of finding-overlap coincidence.
   - **F-12 ADVISORY**: Contract versioning added to kicad-happy output contracts (Section 5.5.1). Each contract now includes `contract_version` and `kicad_happy_target_version`. HW-KCH-004 error includes version info for diagnosis. Contract update procedure documented in Section 5.5.4.
   - **F-13 ADVISORY**: Gate strictness behavioral specification defined (Section 10.1 gate evaluation). Strict blocks on all severities; standard blocks on critical+major; relaxed blocks on critical only.
   - **F-14 ADVISORY**: Test Engineer now has optional `kicad-happy:kicad` consumption (Section 5.2) for reading test points, connector pinouts, and debug interfaces directly from PCB design.
5. **Security review findings addressed (v1.4)**:
   - **SEC-01 BLOCKING**: Path traversal prevention -- added Section 7.2 with `sanitize_path_component()` and `safe_join()` API in `state_manager.py`, whitelist pattern (`^[a-zA-Z0-9._-]+$`), canonicalization check, and `HW-STA-005` error code. All path construction points in state management and artifact registry now use `safe_join()`.
   - **SEC-02 BLOCKING**: BOM data classification -- added Section 14.2 with SENSITIVE/INTERNAL/PUBLIC classification for BOM fields, `.gitignore` recommendations integrated into `hw-setup` wizard, no-pricing filter in memory protocol (Section 8.3 step 5), and `HW-SEC-001` error code for pricing detection in memory entries.
   - **SEC-03 ADVISORY**: `yaml.safe_load()` mandate -- added to Section 7.1 (security invariant note) and Section 14.1 (coding standards table). All YAML parsing across all scripts must use `yaml.safe_load()`.
   - **SEC-04 ADVISORY**: Cross-plugin trust boundary -- documented in Section 5.1 (trust assumption paragraph) and Section 14.3 (trust boundaries table). Plugin authenticity is the platform's responsibility.
   - **SEC-05 ADVISORY**: State file tampering -- documented as accepted risk in Section 7.2.1 with lightweight integrity hash and warning on mismatch. Enumerated in Section 14.4 (accepted risks).
   - **SEC-06 ADVISORY**: Hook script input sanitization -- added Section 9.6 with coding standards (JSON parsing, no shell=True, path validation) and template for safe hook input parsing. Consolidated in Section 14.1 coding standards.
6. **Open for Phase 2**: Dynamic stage depth adaptation (FR-021), Firmware Engineer role, Mechanical Engineer role, programmatic model tier enforcement, full DRC/BOM drift PostToolUse hooks, full memory relevance scoring model
7. **Implementation sequence**: Epic 1 (skeleton + orchestrator) --> Epic 2 (roles) --> Epic 3 (kicad-happy integration) --> Epic 4 (test fixtures + gates) --> Epic 5 (collaboration + hooks)
8. **Validation**: Run `plugin-dev:plugin-validator` after skeleton creation (Story 1.1); run `plugin-dev:skill-reviewer` after each skill creation
