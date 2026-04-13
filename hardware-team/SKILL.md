---
name: hardware-team
description: Hardware delivery team with 8-stage pipeline orchestrator for structured hardware product development. Coordinates 6 hardware roles (HW Product Owner, Electrical Engineer, PCB Layout Engineer, Manufacturing Engineer, Compliance Engineer, Test Engineer) through concept-to-production pipeline. Consumes kicad-happy skills for component sourcing, fabrication, analysis, and documentation.
license: MIT License - See LICENSE.txt
---

# Hardware Team Plugin

A Claude Code plugin that provides a structured hardware delivery pipeline, coordinating 6 specialized hardware engineering roles through an 8-stage development process from concept to production release.

## Available Skills

| Skill | Path | Purpose |
|-------|------|---------|
| `hardware-flow` | `skills/hardware-flow/` | Pipeline orchestrator -- coordinates all roles through 8 stages (Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release) |
| `hw-product-owner` | `skills/hw-product-owner/` | Hardware Product Owner -- requirements capture, feasibility analysis, constraints, BOM budgeting |
| `electrical-engineer` | `skills/electrical-engineer/` | Electrical Engineer -- schematic design, component selection, SPICE simulation, firmware interface docs |
| `pcb-layout-engineer` | `skills/pcb-layout-engineer/` | PCB Layout Engineer -- physical layout, routing, stackup design, DRC |
| `manufacturing-engineer` | `skills/manufacturing-engineer/` | Manufacturing Engineer -- DFM/DFA review, panelization, yield, production transfer |
| `compliance-engineer` | `skills/compliance-engineer/` | Compliance Engineer -- EMC, safety, environmental, regulatory documentation |
| `test-engineer` | `skills/test-engineer/` | Test Engineer -- test strategy, fixture design, production test, validation planning |

## Three-Level Context Loading

This plugin follows the three-level context loading pattern to minimize context window usage:

### Level 1: Metadata (Always Loaded)
The `marketplace.json` entry is loaded by the Claude Code harness whenever the plugin is installed. Contains only plugin name, description, and skill paths. Cost: ~200 tokens.

### Level 2: SKILL.md (Loaded When Skill Triggers)
Each skill's SKILL.md is loaded when the skill is invoked -- either by a user trigger phrase or by the orchestrator dispatching a sub-agent via the Agent tool. Contains role description, reference file list, task routing, kicad-happy skills consumed, output contracts, and anti-patterns. Cost: 500-2000 tokens per skill.

### Level 3: References (Loaded On Demand)
Reference files are loaded ONLY when the skill needs them for a specific task. The SKILL.md declares which references exist; the sub-agent reads them via the Read tool when the task requires that knowledge. Cost: 1000-5000 tokens per reference, loaded only when needed.

**Context isolation rule**: A skill loads ONLY its own references. The electrical-engineer skill never loads manufacturing-engineer references, and vice versa. The orchestrator never loads role-specific references directly.

## Usage

To start a hardware development pipeline:
- Invoke `hardware-team:hardware-flow` to run the full pipeline
- Invoke individual role skills directly for standalone tasks (e.g., `hardware-team:electrical-engineer` for schematic review)

## kicad-happy Integration

This plugin consumes 11 kicad-happy skills for hardware-specific operations. Role skills invoke kicad-happy skills internally via the Skill tool. The orchestrator does NOT invoke kicad-happy directly -- this preserves role context isolation.

## Configuration

Pipeline configuration is stored in `.hardware/config.yml` (separate from `.delivery/` namespace). Pipeline state is tracked in `.hardware/state.md`.
