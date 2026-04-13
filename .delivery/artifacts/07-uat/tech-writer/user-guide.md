# User Guide -- hardware-team Plugin v1.0.0

**Author:** Bilbo (Tech Writer)
**Date:** 2026-04-12
**Pipeline:** run-2026-04-12-hw01

> "I think I'm quite ready for another documentation adventure." This guide will walk you through everything you need to know to use the hardware-team plugin -- from installation to your first pipeline run to troubleshooting when things go sideways. Like any good journey, we start at the front door.

---

## Table of Contents

1. [Installation](#1-installation)
2. [Quick Start](#2-quick-start)
3. [Available Skills and When to Use Them](#3-available-skills-and-when-to-use-them)
4. [Configuration Reference](#4-configuration-reference)
5. [Pipeline Stages Overview](#5-pipeline-stages-overview)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Installation

### Prerequisites

Before installing hardware-team, you need:

- **Claude Code** with plugin support enabled
- **Python 3.x** (for hook scripts and config validation)
- **kicad-happy plugin v1.2.0+** (required external dependency -- see below)

### Step 1: Clone the Repository

If you have not already cloned the Claude-Plugins repository:

```bash
git clone https://github.com/P47Phoenix/Claude-Plugins.git
```

The `hardware-team/` directory lives at the repository root alongside other plugins.

### Step 2: Install kicad-happy (Required Dependency)

The hardware-team plugin consumes all 11 skills from the kicad-happy plugin. You must install kicad-happy separately via the Claude Code plugin system.

kicad-happy installs to `~/.claude/plugins/cache/kicad-happy/kicad-happy/<version>/`.

To verify the installation, start a Claude Code session and check that the following skills appear in your available skills list:

- `kicad-happy:kicad`
- `kicad-happy:spice`
- `kicad-happy:digikey`
- `kicad-happy:mouser`
- `kicad-happy:lcsc`
- `kicad-happy:element14`
- `kicad-happy:jlcpcb`
- `kicad-happy:pcbway`
- `kicad-happy:bom`
- `kicad-happy:emc`
- `kicad-happy:kidoc`

### Step 3: Register in Marketplace

The plugin must be registered in `.claude-plugin/marketplace.json` with its unique ID, display name, description, and skill paths. The marketplace entry looks like:

```json
{
  "name": "hardware-team",
  "description": "Hardware delivery team with 8-stage pipeline orchestrator for structured hardware product development. Coordinates 6 hardware roles through concept-to-production pipeline. Consumes kicad-happy skills for component sourcing, fabrication, analysis, and documentation.",
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

### Step 4: Verify Installation

Start a new Claude Code session. The SessionStart hooks will run automatically and report:

- Whether `.hardware/config.yml` exists (it will not on first run -- that is expected)
- How many kicad-happy skills are available (aim for 11/11)

If you see `kicad-happy: 11/11 skills available`, you are ready to go.

---

## 2. Quick Start

### Run the Setup Wizard

The fastest way to get started is the setup wizard:

```
hw-setup
```

The wizard will ask you about your project and create a `.hardware/config.yml` file with appropriate defaults. Questions cover:

- Project name and description
- Target fabrication house (JLCPCB, PCBWay, or other)
- Compliance regions (FCC, CE, UL, etc.)
- BOM budget
- Production volume target (hobby, small-batch, production)
- Board complexity (single-layer, 2-layer, 4-layer, etc.)

If you prefer to skip the wizard, the pipeline will use sensible defaults and log "No project config found, using defaults."

### Your First Pipeline Run

Once your config is set (or you are happy with defaults), start the pipeline:

```
Run the hardware pipeline
```

The orchestrator will guide your project through the 8 stages sequentially. Each stage:

1. Dispatches work to the appropriate role skill(s) as sub-agents
2. Produces stage artifacts saved to `.hardware/artifacts/<stage-name>/`
3. Evaluates the stage gate(s)
4. Advances to the next stage if all gates pass, or returns feedback for correction

For human-execution stages (Prototype, Pilot Run, Production Release), the pipeline will pause and present you with preparation documents and action items. Confirm completion with `<stage> complete` or report issues with `<stage> failed: <description>`.

### What to Expect on a Typical Run

A simple single-board project will typically progress as follows:

1. **Concept** (2-5 minutes) -- PO captures requirements, constraints, feasibility
2. **Schematic** (5-15 minutes) -- EE reviews/designs circuit, selects components, runs simulation
3. **Layout** (5-10 minutes) -- PCB Layout Engineer reviews physical design, runs DRC
4. **Prototype** (pauses for human) -- You order boards, assemble, test
5. **DFM/DFA** (5-10 minutes) -- MfgE validates manufacturability
6. **Compliance** (5-10 minutes) -- CompE runs EMC pre-compliance, regulatory checks
7. **Pilot Run** (pauses for human) -- Small-batch manufacturing preparation
8. **Production Release** (pauses for human) -- Final manufacturing transfer package

---

## 3. Available Skills and When to Use Them

### hardware-flow (Pipeline Orchestrator)

**When to use:** Always. This is the entry point for structured hardware development. It coordinates all other roles.

**Trigger phrases:** "Run the hardware pipeline", "start hardware flow", "hw-flow"

**What it does:** Manages the 8-stage pipeline, dispatches sub-agents, evaluates gates, handles rework loops, and tracks pipeline state.

### hw-product-owner (Hardware Product Owner)

**When to use:** At the Concept stage, or anytime you need to capture hardware requirements, evaluate feasibility, or make make-vs-buy decisions.

**Trigger phrases:** "hardware requirements", "hw product owner", "feasibility analysis", "BOM budget"

**What it does:** Produces requirements documents, constraint matrices, regulatory landscape scans, and initial BOM budgets. Documents trade-off decisions using decision records.

### electrical-engineer (Electrical Engineer)

**When to use:** During the Schematic stage, or when you need schematic review, component selection guidance, SPICE simulation, or power analysis.

**Trigger phrases:** "schematic review", "component selection", "electrical engineer", "SPICE simulation"

**What it does:** Reviews schematics across 7 categories (power integrity, signal integrity, component derating, pull-ups/pull-downs, decoupling, voltage levels, thermal). Selects components using kicad-happy sourcing skills. Runs SPICE simulations. Produces firmware interface documentation (pin assignments, power domains, bus interfaces).

**kicad-happy skills consumed:** `kicad`, `spice`, `digikey`, `mouser`, `lcsc`, `element14`

### pcb-layout-engineer (PCB Layout Engineer)

**When to use:** During the Layout stage, or when you need PCB layout review, routing analysis, stackup design, or DRC validation.

**Trigger phrases:** "PCB layout", "routing review", "stackup", "DRC"

**What it does:** Reviews physical layout, analyzes routing and impedance control, designs stackups, and validates design rules against fab capabilities. Requires Sonnet-tier model or higher for spatial/geometric reasoning tasks.

**kicad-happy skills consumed:** `kicad`

### manufacturing-engineer (Manufacturing Engineer)

**When to use:** During the DFM/DFA stage, or when you need manufacturability review, panelization guidance, or production transfer documentation.

**Trigger phrases:** "DFM review", "manufacturing engineer", "assembly process", "production transfer"

**What it does:** Evaluates DFM rules (trace/space, via sizes, drill ratios, surface finish), DFA guidelines (component placement, soldering accessibility), yield risk, and panelization. Generates production transfer packages.

**kicad-happy skills consumed:** `jlcpcb`, `pcbway`, `bom`, `kidoc`

### compliance-engineer (Compliance Engineer)

**When to use:** During the Compliance stage, or when you need EMC pre-compliance analysis, safety review, environmental compliance, or regulatory documentation.

**Trigger phrases:** "compliance review", "EMC analysis", "FCC", "CE marking", "RoHS"

**What it does:** Runs EMC pre-compliance checks, evaluates safety standards (IEC 62368-1), checks environmental regulations (RoHS, REACH, WEEE), and produces evidence-linked regulatory packages for each target market.

**kicad-happy skills consumed:** `emc`, `kidoc`

### test-engineer (Test Engineer)

**When to use:** During the Prototype stage and beyond, or when you need test strategy, fixture design, or validation planning.

**Trigger phrases:** "test strategy", "test engineer", "fixture design", "validation plan"

**What it does:** Creates test strategies covering functional, environmental, reliability, and production screening tests. Designs test fixture requirements, bring-up procedures, and validation acceptance criteria.

**kicad-happy skills consumed:** `kicad` (optional, for reading test points and debug interfaces)

---

## 4. Configuration Reference

### File Location

```
<project-root>/.hardware/config.yml
```

### Schema Version

The current schema version is `1.0`. The config file must include a `version` field.

### Complete Field Reference

```yaml
# .hardware/config.yml -- Schema v1.0
version: "1.0"

# Project metadata
project:
  name: "My Hardware Project"
  description: "A brief description of the project"

# Target fabrication house
fabrication:
  target_fab: jlcpcb          # jlcpcb | pcbway | other
  board_layers: 4             # Number of PCB layers
  surface_finish: HASL        # HASL | ENIG | OSP | Immersion Silver

# Compliance regions to evaluate
compliance:
  regions:                     # List of regulatory regimes
    - FCC                      # FCC Part 15 (US)
    - CE                       # CE RED (EU)
  # Additional options: UL, IC (Canada), MIC (Korea), TELEC (Japan)

# BOM constraints
bom:
  budget: 25.00               # Maximum BOM cost per unit (USD)
  require_second_source: false # Whether single-source components block the BOM gate
  currency: USD               # USD | EUR | GBP | CNY

# Production targets
production:
  volume: 100                 # Target production volume
  type: small-batch           # hobby | small-batch | production

# Rework termination limits
rework:
  max_rework_iterations: 3    # Max reworks per individual path (e.g., Prototype-->Schematic)
  max_total_reworks: 10       # Max total reworks across all paths in one pipeline run

# Pipeline behavior
pipeline:
  staleness_warning_days: 7   # Days before paused pipeline shows staleness warning
  staleness_critical_days: 30 # Days before paused pipeline shows critical warning

# External dependencies
dependencies:
  kicad_happy_version: ">=1.2.0"  # Minimum compatible kicad-happy version
```

### Field Behavior

- **All fields are optional.** Missing fields use sensible defaults.
- **Invalid fields produce warnings**, not errors. The pipeline never fails due to config problems.
- **The `version` field** enables schema migration. Future versions will include migration guidance in SessionStart hook warnings.
- **The `dependencies` section** is checked at session start by the kicad-happy availability hook.

---

## 5. Pipeline Stages Overview

### Stage Flow Diagram

```
Concept --> Schematic --> Layout --> Prototype --> DFM/DFA --> Compliance --> Pilot Run --> Production Release
                ^           ^                       ^            ^   ^                         
                |           |                       |            |   |                         
                +-----------+-- Prototype ----------+            |   |                         
                |           +-- DFM/DFA ------------+            |   |                         
                +-------------- DFM/DFA -------------------------+   |                         
                +-------------- Compliance --------------------------+                         
                +-------------- Pilot Run ---------------------------+                         
```

Arrows pointing backward represent rework paths. These are bounded by configurable limits.

### Stage Details

#### Stage 1: Concept (AI-Execution)

**Primary Role:** Hardware Product Owner
**Gate:** Requirements Completeness + Feasibility
**Artifacts Produced:**
- Requirements document
- Constraint matrix (electrical, mechanical, environmental, cost)
- Regulatory landscape scan
- Initial BOM budget estimate
- Make-vs-buy analysis (where applicable)

#### Stage 2: Schematic (AI-Execution)

**Primary Role:** Electrical Engineer | **Support:** HW Product Owner (trade-offs)
**Gate:** Schematic Review Gate (multi-reviewer, 7 categories)
**Artifacts Produced:**
- Schematic review findings (with severity, location, recommended fixes)
- Component selection rationale
- SPICE simulation results
- Power tree analysis
- Firmware interface documentation (pin assignments, power domains, bus specs)

#### Stage 3: Layout (AI-Execution)

**Primary Role:** PCB Layout Engineer
**Gate:** DRC Gate
**Artifacts Produced:**
- Layout review findings
- Routing analysis (impedance, length matching)
- Stackup recommendation
- DRC results with remediation guidance

#### Stage 4: Prototype (Human-Execution)

**Primary Role:** Test Engineer | **Support:** Electrical Engineer
**Gate:** Human Confirmation Gate
**What the AI Produces:**
- Ordering package (Gerbers, drill files, BOM/CPL for fab)
- Bring-up test procedure
- Test fixture requirements
- Known risk list from prior stages

**What You Do:** Order boards, assemble (or have assembled), run bring-up tests, report results.

#### Stage 5: DFM/DFA (AI-Execution)

**Primary Role:** Manufacturing Engineer
**Gates:** DFM Gate + BOM Gate
**Artifacts Produced:**
- DFM review report (fab-specific rules applied)
- DFA review report (assembly process evaluation)
- Yield risk assessment
- BOM validation (cost, availability, lifecycle, second-source)
- Remediation guidance for any violations

#### Stage 6: Compliance (AI-Execution)

**Primary Role:** Compliance Engineer
**Gate:** Compliance Gate (evidence-linked per region)
**Artifacts Produced:**
- EMC pre-compliance report
- Safety analysis (IEC 62368-1 / IEC 60950)
- Environmental compliance checklist (RoHS, REACH, WEEE)
- Test lab preparation package
- Regulatory checklist per configured region with evidence links

#### Stage 7: Pilot Run (Human-Execution)

**Primary Role:** Manufacturing Engineer | **Support:** Test Engineer
**Gate:** Human Confirmation Gate
**What the AI Produces:**
- Small-batch manufacturing preparation package
- Production test procedures
- Yield acceptance criteria
- Assembly work instructions

**What You Do:** Run a small production batch, execute production tests, evaluate yield.

#### Stage 8: Production Release (Human-Execution)

**Primary Role:** Manufacturing Engineer
**Gate:** Final Gate (all artifacts complete)
**What the AI Produces:**
- Complete manufacturing transfer package
- Final BOM with approved vendors
- Production test suite
- Quality acceptance criteria
- Regulatory compliance package

**What You Do:** Hand off to manufacturing, start production.

---

## 6. Troubleshooting

### kicad-happy Not Found

**Symptom:** SessionStart hook reports `kicad-happy: 0/11 skills available` or a skill invocation returns `SKILL_UNAVAILABLE`.

**Cause:** The kicad-happy plugin is not installed in the Claude Code plugin system.

**Fix:**
1. Install kicad-happy via the Claude Code plugin system
2. Verify it is present at `~/.claude/plugins/cache/kicad-happy/`
3. Start a new Claude Code session and check that the SessionStart hook reports `kicad-happy: 11/11 skills available`

**Note:** The pipeline will not crash without kicad-happy -- it degrades gracefully. But full functionality (component sourcing, DFM validation, SPICE simulation, EMC analysis, documentation generation) requires all 11 skills.

### kicad-happy Version Mismatch

**Symptom:** Warning message: `kicad-happy version X.Y.Z installed; hardware-team requires >=1.2.0`

**Cause:** An older version of kicad-happy is installed that may not support all required output contracts.

**Fix:** Update kicad-happy to version 1.2.0 or later via the Claude Code plugin system.

### Config Validation Errors

**Symptom:** SessionStart hook warns about config schema issues.

**Common causes and fixes:**

| Warning | Cause | Fix |
|---------|-------|-----|
| "No .hardware/config.yml found" | Config file does not exist | Run `hw-setup` to create one, or let the pipeline use defaults |
| "Schema version outdated" | Config file uses an older schema version | Follow the migration guidance in the warning message |
| "Invalid field: `<field>`" | A config field has an invalid value | Check the field reference in Section 4 and correct the value |

**Important:** Config errors never block the pipeline. Invalid fields fall back to defaults with a warning.

### Pipeline Paused -- Rework Limit Hit

**Symptom:** Pipeline reports `PAUSED` with a message about rework limits.

**Cause:** Either a single rework path has been triggered more than `max_rework_iterations` times (default 3), or the total rework count across all paths exceeds `max_total_reworks` (default 10).

**Options:**
- **Continue:** Allow one more rework iteration
- **Abort:** Stop the pipeline and save state
- **Override limit N:** Raise the rework limit to N

**Recommendation:** If the same rework path keeps triggering, the root cause is likely a fundamental design issue that needs human intervention rather than another automated pass.

### Pipeline Paused -- Awaiting Human Action

**Symptom:** Pipeline reports `PAUSED_AWAITING_HUMAN` at a Prototype, Pilot Run, or Production Release stage.

**This is normal.** These are human-execution stages. The AI has generated preparation documents for you. Complete the physical work and report back:

- `prototype complete` -- to advance past the Prototype stage
- `prototype failed: <description>` -- to trigger a rework loop
- `save pipeline state` -- to save progress and resume later

### Stale Pipeline Warning

**Symptom:** SessionStart hook warns that a pipeline has been paused for more than 7 days.

**Cause:** A pipeline was paused (awaiting human action or due to an error) and has not been resumed.

**Options:**
- **Resume:** Continue from where you left off (uses original config snapshot)
- **Restart:** Start fresh with current config
- **Abandon:** Discard the paused pipeline state

After 30 days, the warning escalates to `CRITICAL` and strongly recommends restarting rather than resuming.

### Dispatch Error

**Symptom:** Pipeline reports `PAUSED_DISPATCH_ERROR` with an error type (TIMEOUT, CONTEXT_OVERFLOW, MODEL_ERROR, UNKNOWN).

**Cause:** A sub-agent dispatch failed even after one automatic retry.

**Options:**
- **Retry:** Attempt the dispatch again
- **Skip:** Mark the stage as skipped (only for non-critical stages)
- **Abort:** Save pipeline state and stop

**For CONTEXT_OVERFLOW errors:** The stage prompt may be too large. Consider whether all Level 3 references are necessary for the current task.

---

> "And there you have it -- the whole guide, from installation to troubleshooting, laid out like a map of the Shire. May your traces be wide, your vias be plated, and your gates all pass on the first review. Now, if you will excuse me, I believe it is time for second breakfast."
