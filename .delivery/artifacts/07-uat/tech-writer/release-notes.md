# Release Notes -- hardware-team Plugin v1.0.0

**Author:** Bilbo (Tech Writer)
**Date:** 2026-04-12
**Pipeline:** run-2026-04-12-hw01

> "I think I'm quite ready for another documentation adventure." And what an adventure this one is -- a brand-new plugin, forged from concept to production release in a single pipeline run. Let me tell you the tale of what we built.

---

## What's New

### A Complete Hardware Delivery Team

The `hardware-team` plugin brings structured hardware product development to Claude Code. Think of it as the Fellowship of the Ring, but for PCB design -- every role has a purpose, every stage has a gate, and no one walks into Mordor (or a fab house) without a proper review.

**7 Skills, One Orchestrator:**

| Skill | Role | What It Does |
|-------|------|-------------|
| `hardware-flow` | Pipeline Orchestrator | Coordinates all roles through 8 hardware development stages |
| `hw-product-owner` | Hardware Product Owner | Requirements capture, feasibility analysis, make-vs-buy decisions, BOM budgeting |
| `electrical-engineer` | Electrical Engineer | Schematic design, component selection, SPICE simulation, firmware interface documentation |
| `pcb-layout-engineer` | PCB Layout Engineer | Physical layout, routing, stackup design, DRC validation |
| `manufacturing-engineer` | Manufacturing Engineer | DFM/DFA review, yield optimization, panelization, production transfer |
| `compliance-engineer` | Compliance Engineer | EMC pre-compliance, safety analysis (IEC 62368-1), environmental (RoHS/REACH/WEEE), regulatory docs (FCC/CE/UL) |
| `test-engineer` | Test Engineer | Test strategy, fixture design, production test methodology, validation planning |

### 8-Stage Hardware Pipeline

A structured journey from concept to production release:

1. **Concept** (AI-execution) -- Requirements, constraints, feasibility, initial BOM budget
2. **Schematic** (AI-execution) -- Circuit design, component selection, simulation, firmware interface docs
3. **Layout** (AI-execution) -- PCB physical layout, routing, stackup, impedance control
4. **Prototype** (Human-execution) -- Ordering packages, bring-up test procedures, human builds the board
5. **DFM/DFA** (AI-execution) -- Manufacturability review, assembly process, yield analysis
6. **Compliance** (Human-execution stage support) -- EMC pre-compliance, safety, environmental, regulatory packages
7. **Pilot Run** (Human-execution) -- Small-batch manufacturing preparation, test procedures
8. **Production Release** (Human-execution) -- Manufacturing transfer package, final BOM, production checklists

Human-execution stages follow a gate-in/human-action/gate-out pattern: the AI generates preparation documents, the human performs the physical work, and the AI evaluates the exit gate.

### 5 Validation Gates

Quality gates between stages ensure defects are caught at design time, not after prototype boards arrive:

| Gate | Between Stages | What It Checks |
|------|---------------|----------------|
| **Schematic Review Gate** | Schematic --> Layout | Power integrity, signal integrity, component derating, pull-ups/pull-downs, decoupling, voltage levels, thermal considerations. Uses iterative multi-reviewer pattern with forced-find prompting. |
| **DRC Gate** | Layout --> Prototype | Design rule compliance against target fab house capabilities. Trace width, via sizes, clearances, solder mask apertures. |
| **BOM Gate** | DFM/DFA stage | Component cost vs. budget, availability, lifecycle status (NRND/obsolete flagged), second-source existence. |
| **DFM Gate** | DFM/DFA stage | Fab-specific manufacturability -- minimum trace/space, drill aspect ratios, layer count, surface finish, component footprint availability. |
| **Compliance Gate** | Compliance --> Pilot Run | Evidence-linked regulatory requirements per configured target market (FCC, CE, etc.). Every requirement must link to its evidence artifact. |

### 11 kicad-happy Integrations

The plugin consumes all 11 skills from the `kicad-happy` plugin without reimplementing any of them. Each hardware role knows when and how to invoke the right kicad-happy skill:

- **Component Sourcing:** `kicad-happy:digikey`, `kicad-happy:mouser`, `kicad-happy:lcsc`, `kicad-happy:element14`
- **Fabrication:** `kicad-happy:jlcpcb`, `kicad-happy:pcbway`
- **Analysis:** `kicad-happy:kicad`, `kicad-happy:spice`, `kicad-happy:emc`
- **Documentation:** `kicad-happy:kidoc`, `kicad-happy:bom`

The orchestrator never invokes kicad-happy directly -- role skills own that decision, preserving context isolation.

### Rework Loops

Hardware development is not linear. The pipeline supports controlled backward jumps when issues are found:

- Prototype --> Schematic (circuit error found during bring-up)
- Prototype --> Layout (routing/thermal issue)
- DFM/DFA --> Layout or Schematic (manufacturability issues)
- Compliance --> Layout or Schematic (EMC failures)
- Pilot Run --> DFM/DFA or Schematic (yield or circuit issues)

Rework loops are bounded: `max_rework_iterations` (default 3 per path) and `max_total_reworks` (default 10 per run) prevent infinite loops. When limits are hit, the pipeline pauses and escalates to the human.

### Config-Driven Pipeline

Project-specific settings live in `.hardware/config.yml`:

- Target fabrication house (JLCPCB, PCBWay)
- Compliance regions (FCC, CE, UL, etc.)
- BOM budget thresholds
- Production volume targets
- kicad-happy version compatibility
- Rework termination limits

### Event-Driven Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| Config validation | SessionStart | Validates `.hardware/config.yml` exists and schema is current |
| kicad-happy check | SessionStart | Verifies all 11 kicad-happy skills are available |
| Pipeline bypass detection | PreToolUse | Warns when hardware roles are invoked outside the pipeline |
| KiCad file notification | PostToolUse | Notifies when KiCad files are modified |

---

## Requirements

### Required External Dependency

The `kicad-happy` plugin (v1.2.0 or later) must be installed separately via the Claude Code plugin system. The hardware-team plugin consumes kicad-happy skills for component sourcing, fabrication validation, KiCad analysis, SPICE simulation, EMC pre-compliance, and documentation generation.

**Without kicad-happy installed:** The pipeline will degrade gracefully. Skills that require kicad-happy will report `SKILL_UNAVAILABLE` and document what they could not do. Gates may still evaluate based on available data, but full functionality requires all 11 kicad-happy skills.

### Environment

- Claude Code with plugin support
- Python 3.x (for hook and validation scripts)
- No additional build tools, package managers, or external services required

---

## Known Limitations

1. **Test fixtures are spec-only.** The reference KiCad project (`hardware-team/references/test-fixtures/`) contains manifest specifications for seeded defects but does not yet include actual `.kicad_sch` and `.kicad_pcb` files. Gate acceptance criteria that depend on running against the test fixture will need the actual files to be created before measurable benchmarking is possible.

2. **Phase 1 runs all stages at full depth.** The routing matrix (Hobby vs. Small-Batch vs. Production) is documented but not yet enforced. Dynamic stage depth adaptation (skipping Compliance for hobby projects, etc.) is deferred to Phase 2.

3. **Mechanical Engineer and Firmware Engineer roles are deferred to Phase 2.** The Electrical Engineer produces firmware interface documentation (pin assignments, power domains, bus interfaces) as a bridge artifact, but full firmware pipeline integration is not yet available.

4. **Pipeline state persistence and self-learning memory are P2.** State file format is defined but cross-session resume is not yet implemented. Memory tiering follows the delivery-flow pattern but is not active in v1.0.0.

5. **Challenger/adversarial patterns are prompt-enforced.** The iterative review agent pattern (from issue #76) uses forced-find prompting and deduplication in SKILL.md language. These are structural prompt patterns, not code-enforced runtime checks.

---

## Breaking Changes

Not applicable -- this is the initial release of the hardware-team plugin.

---

## Credits

Built by the Fellowship: Gandalf (PO), Celebrimbor (Architect), Legolas (QA), Sam (DevOps), Bilbo (Tech Writer), Gimli (Developer).

> "And so the hardware-team plugin is documented, its gates are named, and its stages are numbered. Whether it will catch every missing pull-up resistor remains to be seen -- but at least now there is a process for looking."
