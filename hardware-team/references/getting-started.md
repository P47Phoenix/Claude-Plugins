# Getting Started with Hardware-Team

This guide gets you from zero to a running hardware delivery pipeline. It covers prerequisites, the setup wizard, a skill map, and a command cheat sheet.

---

## Prerequisites

Before starting, ensure:

1. **Claude Code** is installed and working
2. **kicad-happy plugin** is installed (see `references/prerequisites.md` for details)
3. **KiCad project** exists (or you are starting from scratch)

The SessionStart hook automatically checks kicad-happy availability and reports which skills are present.

---

## Quick Start

### Step 1: Initialize the hardware config

```
hw-setup
```

The setup wizard asks about your project: what you are building, target fab house, compliance regions, production volume, and strictness level. It generates `.hardware/config.yml`.

### Step 2: Run the pipeline

```
run hardware pipeline
```

Or invoke the orchestrator skill directly:

```
/hardware-team:hardware-flow
```

The pipeline auto-detects your project type (HOBBY, PROTOTYPE, PRODUCTION, or CERTIFIED) and routes through the appropriate stages with the correct depth.

### Step 3: Follow the stages

The pipeline runs 8 stages:

```
1. Concept     --> Requirements, constraints, feasibility
2. Schematic   --> Circuit design, component selection, simulation
3. Layout      --> PCB layout, routing, DRC
4. Prototype   --> Order boards, build, test (human action)
5. DFM/DFA     --> Manufacturability, BOM validation
6. Compliance  --> EMC, safety, environmental
7. Pilot Run   --> Small production batch (human action)
8. Production  --> Final release package
```

Stages 4, 7, and 8 pause for human action (ordering, assembly, testing). The pipeline saves state and resumes when you return.

---

## Skill Map

The hardware-team has 7 skills. Here is what each one does and when the pipeline invokes it.

```
hardware-team:hardware-flow        Orchestrator. Start here.
hardware-team:hw-product-owner     Requirements, constraints, trade-offs
hardware-team:electrical-engineer  Schematic, simulation, component selection
hardware-team:pcb-layout-engineer  PCB layout, routing, stackup, DRC
hardware-team:manufacturing-engineer  DFM, DFA, BOM, production transfer
hardware-team:compliance-engineer  EMC, safety, environmental, regulatory
hardware-team:test-engineer        Test strategy, validation, fixtures
```

### kicad-happy Skills (External Dependency)

The hardware-team roles invoke these 11 kicad-happy skills internally:

```
kicad-happy:kicad      Schematic/PCB analysis, DRC
kicad-happy:spice      SPICE simulation
kicad-happy:digikey    DigiKey component search
kicad-happy:mouser     Mouser component search
kicad-happy:lcsc       LCSC component search
kicad-happy:element14  Newark/Farnell/element14 search
kicad-happy:jlcpcb     JLCPCB fab rules and ordering
kicad-happy:pcbway     PCBWay fab rules and ordering
kicad-happy:bom        BOM management
kicad-happy:emc        EMC pre-compliance analysis
kicad-happy:kidoc      Engineering documentation generation
```

You do NOT invoke kicad-happy skills directly. The hardware-team roles invoke them when needed.

---

## Config File

The pipeline is driven by `.hardware/config.yml` in your project root. Key settings:

| Setting | Purpose | Example |
|---------|---------|---------|
| `project_name` | Display name | `"Smart Sensor Board"` |
| `target_fab` | Fabrication house | `jlcpcb` or `pcbway` |
| `board_layers` | PCB layer count | `4` |
| `bom_budget` | Per-unit BOM cost target | `"$25.00"` |
| `production_volume` | Target quantity | `1000` |
| `compliance_regions` | Regulatory targets | `["FCC", "CE"]` |
| `second_source_required` | Require backup suppliers | `true` |

See `hardware-flow/references/config-schema.md` for the full schema.

---

## Command Cheat Sheet

### Pipeline Commands

| Command | What It Does |
|---------|-------------|
| `hw-setup` | Run the setup wizard to create/update `.hardware/config.yml` |
| `run hardware pipeline` | Start or resume the pipeline from the current stage |
| `resume hardware pipeline` | Resume a paused pipeline (after human action stages) |
| `pipeline status` | Show current pipeline state, stage, and gate results |
| `prototype complete` | Confirm prototype stage human action is done |
| `prototype failed: <reason>` | Report prototype failure (triggers rework) |
| `pilot run complete` | Confirm pilot run human action is done |
| `production release approved` | Approve final production release |

### Individual Skill Commands

| Command | What It Does |
|---------|-------------|
| `/hardware-team:electrical-engineer` | Invoke EE directly (outside pipeline) |
| `/hardware-team:pcb-layout-engineer` | Invoke PCB layout directly |
| `/hardware-team:manufacturing-engineer` | Invoke MfgE directly |
| `/hardware-team:compliance-engineer` | Invoke compliance directly |
| `/hardware-team:test-engineer` | Invoke test engineer directly |
| `/hardware-team:hw-product-owner` | Invoke HW PO directly |

### State and Artifacts

| Command | What It Does |
|---------|-------------|
| `show gate results` | Display all gate pass/fail results for this run |
| `show rework history` | Display rework path history and iteration counts |
| `save pipeline state` | Persist pipeline state for cross-session resume |

---

## Project Types

The pipeline auto-detects your project type and adjusts stage depth accordingly:

| Type | Stages Run | When Detected |
|------|-----------|---------------|
| **HOBBY** | 1-4 only | Personal/learning projects, no production intent |
| **PROTOTYPE** | 1-5 (DFM light) | Working board, no compliance/production |
| **PRODUCTION** | 1-8 full | Commercial product, volume manufacturing |
| **CERTIFIED** | 1-8 full+extended | Regulatory certification required |

See `hardware-flow/references/project-types.md` for detection signals and routing details.

---

## Directory Structure

After running the pipeline, your project will have:

```
.hardware/
+-- config.yml              # Project configuration
+-- state.md                # Pipeline state (stage, gates, rework)
+-- memory/                 # Self-learning memory
+-- artifacts/
    +-- 01-concept/         # Requirements, constraints, feasibility
    +-- 02-schematic/       # Schematic review, simulation, components
    +-- 03-layout/          # Layout review, routing, DRC
    +-- 04-prototype/       # Ordering package, test procedures
    +-- 05-dfm-dfa/         # DFM/DFA reports, BOM validation
    +-- 06-compliance/      # EMC, safety, environmental
    +-- 07-pilot-run/       # Manufacturing transfer, yield targets
    +-- 08-production-release/  # Final BOM, release docs
```
