# Idea Brief: Hardware Delivery Team Plugin

**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD | **Plugin:** hardware-team

---

## The Burden

Building hardware products with AI assistance today is fragmented. The `kicad-happy/` plugin provides 11 specialist skills for PCB-adjacent tasks -- component sourcing (DigiKey, Mouser, LCSC, element14), fabrication (JLCPCB, PCBWay), BOM management, KiCad analysis, SPICE simulation, EMC pre-compliance, and documentation generation. These skills are powerful individually, but they operate as isolated tools. There is no structured process connecting schematic review to BOM validation to DFM checks to compliance certification. No team-based validation where an electrical engineer's output is reviewed by a manufacturing specialist before it reaches the fab house. No pipeline that guides a hardware product from concept through prototyping to production release.

The existing `delivery-team/` plugin solves this exact problem for software -- 11 skills, 7 pipeline stages, 6 collaboration patterns, self-learning memory, and team DoD validation. But its stages (Idea, Refine, Design, Architect, Plan, Development, UAT) and its roles (Product Owner, Developer, QA, DevOps) are fundamentally software-shaped. Hardware development has different stages (concept, schematic capture, PCB layout, prototype, DFM/DFA, compliance, pilot run, production), different roles (electrical engineer, mechanical engineer, manufacturing engineer, compliance engineer, firmware engineer), and different validation gates (design rule checks, thermal analysis, EMC pre-compliance, BOM costing, assembly yield).

GitHub issue #76 (P47Phoenix/Claude-Plugins#76) documented a KiCad PCB iterative review agent system with 17 specialist review agents, an iterative review loop pattern, and 30+ real defects caught. Key learnings from that work: model tiering matters (Haiku too weak for geometry reasoning), forced-find prompting produces better defect detection, and deduplication is essential when multiple reviewers operate on the same artifact. These patterns should be foundational to the hardware-team plugin's collaboration architecture.

## The Vision

A `hardware-team/` plugin that mirrors the `delivery-team/` architecture -- same three-level context loading, same pipeline-with-gates pattern, same team DoD validation -- but purpose-built for hardware product development. The plugin **consumes** the existing `kicad-happy/` skills as building blocks (component search, BOM management, fabrication rules, EMC analysis, SPICE simulation) rather than duplicating them. It adds the orchestration layer, the hardware-specific roles, the hardware development stages, and the validation gates that turn isolated tools into a structured delivery process.

The hardware pipeline stages reflect the actual hardware development lifecycle:

| Stage | Purpose | Key Activities |
|-------|---------|----------------|
| **1. Concept** | Define the product requirements and constraints | Requirements capture, feasibility analysis, make-vs-buy decisions, initial BOM budgeting, regulatory landscape scan |
| **2. Schematic** | Capture the electrical design | Schematic entry, component selection (consuming kicad-happy supplier skills), design review, simulation (consuming kicad-happy:spice), power tree analysis |
| **3. Layout** | Physical PCB design | PCB layout, routing, stackup definition, impedance control, DRC, thermal analysis, signal integrity |
| **4. Prototype** | Build and validate first articles | Fabrication output generation (consuming kicad-happy:jlcpcb/pcbway), BOM finalization (consuming kicad-happy:bom), assembly, bring-up, test fixture design |
| **5. DFM/DFA** | Design for manufacturability and assembly | DFM review, DFA review, yield analysis, panelization, test point coverage, component availability and lifecycle checks |
| **6. Compliance** | Regulatory certification readiness | EMC pre-compliance (consuming kicad-happy:emc), safety analysis, environmental compliance (RoHS, REACH), documentation packages (consuming kicad-happy:kidoc), test lab preparation |
| **7. Pilot Run** | Small-batch production validation | Pilot build coordination, process validation, quality metrics, production test development, yield targets |
| **8. Production Release** | Transfer to volume manufacturing | Manufacturing transfer package, production BOM lockdown, supply chain qualification, ongoing quality monitoring |

The hardware-team roles mirror hardware org structures:

| Role | Responsibilities | Consumes kicad-happy Skills |
|------|------------------|----------------------------|
| **Electrical Engineer** | Schematic design, component selection, simulation, signal integrity | kicad, spice, digikey, mouser, lcsc, element14 |
| **PCB Layout Engineer** | Physical layout, routing, stackup, DRC | kicad |
| **Mechanical Engineer** | Enclosure design, thermal management, physical integration | -- |
| **Manufacturing Engineer** | DFM/DFA review, assembly process, yield optimization | jlcpcb, pcbway, bom |
| **Compliance Engineer** | EMC, safety, environmental, regulatory documentation | emc, kidoc |
| **Firmware Engineer** | Embedded software, hardware-software interface, bring-up | -- |
| **Hardware Product Owner** | Requirements, trade-offs, schedule, stakeholder communication | -- |
| **Test Engineer** | Test strategy, test fixtures, production test, validation | -- |

## Scope IN

### Core Plugin (hardware-team/)

- **Plugin skeleton**: `hardware-team/` top-level directory following CLAUDE.md conventions (SKILL.md, skills/, references/, hooks/, scripts/)
- **Pipeline orchestrator** (`hardware-team/skills/hardware-flow/`): 8-stage hardware pipeline with stage gates, team DoD validation, self-correction loops, and self-learning memory -- architecturally parallel to `delivery-team/skills/delivery-flow/`
- **8 role-based skills**: One skill per hardware role, each with SKILL.md, role-specific references, and three-level context loading
- **kicad-happy integration layer**: Defined interface for consuming kicad-happy skills as sub-agents from within the hardware pipeline (component search, BOM ops, fab rules, EMC analysis, SPICE simulation, documentation)
- **Hardware-specific collaboration patterns**: Adapted from delivery-team's 6 patterns, plus hardware-specific patterns like Design Review Board (multi-role schematic/layout review), Compliance Gate (regulatory checklist with evidence requirements), and BOM Reconciliation (cross-supplier validation)
- **Config-driven pipeline** (`.hardware/config.yml`): Project configuration with hardware-specific settings (target fab house, compliance regions, BOM budget, production volume targets)
- **Pipeline state persistence and resume**: Same pattern as delivery-flow's `.delivery/state.md`
- **Registration in marketplace.json**: Full plugin registration with unique ID, description, and skill paths

### Hardware-Specific Validation Gates

- **Schematic Review Gate**: Multi-reviewer electrical design review (power integrity, signal integrity, component derating, missing pull-ups/pull-downs, decoupling strategy) -- applying the iterative review agent pattern from issue #76
- **DRC Gate**: Automated design rule check validation with pass/fail and remediation guidance
- **BOM Gate**: Cost validation, component availability check, lifecycle status (not NRND/obsolete), second-source availability
- **DFM Gate**: Manufacturability review against target fab capabilities (minimum trace/space, via sizes, layer count, surface finish compatibility)
- **Compliance Gate**: Regulatory checklist with evidence-linked requirements per target market (FCC, CE, UL, etc.)

### Hooks

- **Config validation** (SessionStart): Validates `.hardware/config.yml` exists and is current
- **Schematic DRC** (PostToolUse): Auto-run DRC validation when KiCad schematic files are modified
- **BOM drift detection** (PostToolUse): Detect when schematic changes invalidate the current BOM

## Scope OUT

- **Replacing kicad-happy skills**: The hardware-team plugin consumes kicad-happy as a dependency. It does NOT reimplement component search, BOM parsing, EMC analysis, SPICE simulation, or any existing kicad-happy capability.
- **3D CAD integration**: Mechanical design tools (FreeCAD, SolidWorks, Fusion 360) are out of scope for the initial plugin. Enclosure design guidance is text-based, not CAD-integrated.
- **Physical lab automation**: The plugin does not control test equipment, lab instruments, or manufacturing machinery. It produces documentation and guidance that humans execute in the physical world.
- **Supply chain management software**: No ERP integration, no purchase order generation, no inventory tracking beyond BOM-level component data.
- **Actual compliance certification**: The plugin performs pre-compliance analysis and documentation preparation. It does not submit to or interact with certification bodies (FCC, CE notified bodies, UL).
- **Firmware development pipeline**: Firmware engineering is a role within the hardware pipeline, but full firmware CI/CD is handled by the existing software `delivery-team/` plugin. The hardware plugin covers the hardware-firmware interface, not firmware development methodology.
- **Multi-board system design**: Initial scope is single-board designs. System-level design with multiple interconnected PCBs, backplanes, or flex-rigid assemblies is deferred.

## Companion Plugins (Future -- Scope OUT for this GREENFIELD)

The hardware domain may eventually require companion plugins. These are explicitly NOT in scope for the initial hardware-team plugin but are documented here to show the vision boundary:

- **simulation-plugin**: Advanced simulation workflows (thermal FEA, vibration analysis, EMC full-wave) beyond what kicad-happy:spice provides
- **supply-chain-plugin**: Lifecycle management, AVL (Approved Vendor List) maintenance, procurement optimization, lead time monitoring
- **compliance-plugin**: Deep regulatory workflow management with certification body submission tracking, test report templates per standard, market-specific regulatory databases

## The Stakes

### Success Metrics

| Metric | Target | Baseline |
|--------|--------|----------|
| Pipeline coverage | Hardware project from concept to production release docs in one pipeline run | No structured process exists today |
| kicad-happy utilization | 100% of applicable kicad-happy skills consumed (not duplicated) | Skills used ad-hoc, not orchestrated |
| Defect detection rate | >80% of reviewable defect categories caught before prototype (applying issue #76 learnings) | Unknown -- no structured review exists |
| Role context isolation | Zero cross-role context bleed (each skill loads only its references) | N/A (new plugin) |
| Config-driven flexibility | Pipeline adapts to project type (1-layer vs 8-layer, prototype vs production, hobby vs certified) | One-size-fits-all |

### Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| kicad-happy skills not available on disk (they appear loaded but no files found in repo) | High | High | Verify kicad-happy installation path; design integration layer to handle both local and remote skill loading |
| Hardware domain breadth exceeds manageable skill count | Medium | Medium | Start with 8 roles, defer Mechanical and Firmware to phase 2 if scope is too large |
| Model limitations on spatial/geometric reasoning (issue #76 learning: Haiku too weak) | High | Medium | Document minimum model tier per role; layout and mechanical roles require Sonnet+ |
| Pipeline stages too rigid for iterative hardware development (hardware often loops back from prototype to schematic) | Medium | High | Design explicit rework loops in pipeline (prototype -> schematic rework path), not just linear progression |

## Anti-Scope

- Do NOT duplicate any kicad-happy skill functionality -- consume, do not copy
- Do NOT modify the existing delivery-team plugin -- hardware-team is a parallel plugin, not an extension of delivery-team
- Do NOT build physical-world automation (lab control, instrument communication, pick-and-place programming)
- Do NOT create a "universal engineering plugin" -- scope is hardware product development, not civil/structural/chemical/aerospace engineering
- Do NOT assume linear pipeline-only flow -- hardware development requires rework loops and stage revisitation

## Open Questions

| # | Question | Owner | Impact |
|---|----------|-------|--------|
| 1 | Where is kicad-happy installed? The skills are loaded in the session but no files exist under `kicad-happy/` in this repo. Is it a separate plugin installation? | PO / Architect | High -- integration architecture depends on this |
| 2 | Should the hardware-team plugin share `.delivery/` namespace or use its own `.hardware/` namespace for config and state? | Architect | Medium -- affects config schema and state management |
| 3 | What is the minimum model tier for each hardware role? Issue #76 found Haiku insufficient for geometry. Should the plugin enforce model requirements? | Architect | Medium -- affects cost and capability |
| 4 | Should firmware be a first-class role in the hardware plugin or delegated entirely to the software delivery-team? | PO | Medium -- scope boundary definition |
| 5 | How should the pipeline handle rework loops (e.g., prototype fails, go back to schematic)? Linear with explicit rework stages, or non-linear DAG? | Architect | High -- fundamental pipeline architecture |
| 6 | Are companion plugins (simulation, supply-chain, compliance) phase 2 of THIS plugin or separate marketplace entries? | PO | Medium -- affects marketplace strategy |
| 7 | Should the hardware-team reuse delivery-team's self-learning memory infrastructure (`.delivery/memory/`) or maintain its own? | Architect | Low -- implementation detail |

## Assumptions

1. The `kicad-happy/` plugin skills are consumable as sub-agents from other plugins (cross-plugin skill invocation is supported by the Claude Code plugin system)
2. The hardware pipeline can follow the same orchestrator pattern as delivery-flow (Agent tool dispatch to role-scoped sub-agents with context isolation)
3. Hardware project files (KiCad schematics, PCB layouts, Gerbers) exist on the local filesystem and are accessible to Claude Code tools
4. Python scripts with no external dependency management is sufficient for hardware validation scripts (DRC parsing, BOM validation, etc.)
5. The marketplace registry supports multiple delivery-style plugins without naming conflicts

## Next Steps

This Idea Brief is the Phase 1 artifact. When downstream_ready, it proceeds to:

1. **Refine** (Phase 2): Product Owner decomposes into epics and stories; Data Analyst defines success metrics; Scrum Bag defines the delivery cadence
2. **Design** (Phase 3): UI/UX designs the pipeline interaction model; defines the config wizard experience
3. **Architect** (Phase 4): Solution Architect produces the plugin structure ADR; defines the kicad-happy integration architecture; resolves open questions 1, 2, 3, 5, 7
