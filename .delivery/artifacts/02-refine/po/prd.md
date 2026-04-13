# Product Requirements Document: Hardware Delivery Team Plugin

**Product / Feature:** hardware-team plugin
**Version:** 1.1 (Revised — Adversarial Challenges Addressed)
**Author:** Product Owner (Gandalf)
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Status:** Draft — Revised
**Last Updated:** 2026-04-12

---

> "All we have to decide is what to build with the time that is given to us. And I decide we build the orchestration layer first -- the one that turns eleven isolated skills into a fellowship."

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-12 | PO (Gandalf) | Initial PRD |
| 1.1 | 2026-04-12 | PO (Gandalf) | Adversarial challenge resolution: C1 RESOLVED (verified), C2 RESOLVED (dependency story added), C5 RESOLVED (test fixture story added), C8 RESOLVED (rework termination added), C10 RESOLVED (fallback removed). Advisory items C3, C4, C6, C7, C9 incorporated. |

---

## Challenge Resolution Summary

> "Even the smallest challenge, when addressed with precision, can change the course of a delivery."

| # | Challenge | Severity | Resolution | Status |
|---|-----------|----------|------------|--------|
| C1 | Cross-plugin skill invocation unverified | BLOCKING | **VERIFIED** — live test confirmed `kicad-happy:kicad` loads via Skill tool from separate plugin context. kicad-happy installed at `C:\Users\micha\.claude\plugins\cache\kicad-happy\kicad-happy\1.2.0\`. | RESOLVED |
| C2 | kicad-happy not in repository | BLOCKING | Added Story 3.6 (kicad-happy Dependency Documentation), config version compatibility, SessionStart hook skill availability check (Story 5.3 extended). | RESOLVED |
| C3 | 8-stage pipeline over-decomposed for AI context | ADVISORY | Clarified AI role during physical stages (Prototype, Pilot Run, Production Release) in Story 1.2. These are "human execution stages" with gate-in/gate-out pattern. | INCORPORATED |
| C4 | Firmware-hardware interface missing in Phase 1 | ADVISORY | Added firmware interface documentation as an EE output during Schematic stage (Story 2.2 AC extended). | INCORPORATED |
| C5 | Acceptance criteria untestable without reference fixture | BLOCKING | Added Story 4.0 (Reference Test Fixture Creation) to Epic 4 before Story 4.1. | RESOLVED |
| C6 | "0 reimplemented" counter-metric unenforceable | ADVISORY | Added operational definition of "reimplementation" to NFR-003 and Story 3.1 acceptance criteria. | INCORPORATED |
| C7 | Config-driven flexibility scope creep risk | ADVISORY | Separated P1 static config reading from P2 dynamic pipeline adaptation. Story 1.4 AC updated to require only static config reading. FR-021 clarified as P2-only dynamic adaptation. | INCORPORATED |
| C8 | Rework loops lack termination conditions | BLOCKING | Added `max_rework_iterations` (default 3 per path) and `max_total_reworks` (default 10 per run) to Story 1.7 AC, FR-007, config schema, and NFR-010. | RESOLVED |
| C9 | Metrics targets without meaningful baselines | ADVISORY | North Star metric definition amended to exclude infrastructure failures and user abandonment. Root cause categorization added. | INCORPORATED |
| C10 | Fallback architecture undefined | BLOCKING | **RESOLVED BY VERIFICATION** — cross-plugin invocation confirmed working. Fallback removed from risk register. R-005 retired. | RESOLVED |

---

## 1. Executive Summary

### Problem Statement

Building hardware products with AI assistance today is fragmented. The `kicad-happy/` plugin provides 11 specialist skills for PCB-adjacent tasks -- component sourcing (DigiKey, Mouser, LCSC, element14), fabrication (JLCPCB, PCBWay), BOM management, KiCad analysis, SPICE simulation, EMC pre-compliance, and documentation generation. These skills are powerful individually, but they operate as isolated tools. There is no structured process connecting schematic review to BOM validation to DFM checks to compliance certification. No team-based validation where an electrical engineer's output is reviewed by a manufacturing specialist before it reaches the fab house. No pipeline that guides a hardware product from concept through prototyping to production release.

The existing `delivery-team/` plugin solves this exact problem for software -- 11 skills, 7 pipeline stages, 6 collaboration patterns, self-learning memory, and team DoD validation. But its stages and roles are fundamentally software-shaped. Hardware development has different stages (concept, schematic capture, PCB layout, prototype, DFM/DFA, compliance, pilot run, production), different roles (electrical engineer, PCB layout engineer, manufacturing engineer, compliance engineer, firmware engineer, mechanical engineer, test engineer), and different validation gates (design rule checks, thermal analysis, EMC pre-compliance, BOM costing, assembly yield).

### Why Now

GitHub issue #76 documented a KiCad PCB iterative review agent system with 17 specialist review agents, an iterative review loop pattern, and 30+ real defects caught. The patterns and learnings from that work -- model tiering, forced-find prompting, deduplication -- are mature enough to be foundational. The kicad-happy skills are installed and available. The delivery-team architecture is proven. Cross-plugin skill invocation has been verified to work (kicad-happy:kicad loads successfully via the Skill tool from a separate plugin context). The only missing piece is the orchestration layer that connects them into a structured hardware development process.

### What This Plugin Does

A `hardware-team/` plugin that mirrors the `delivery-team/` architecture -- same three-level context loading, same pipeline-with-gates pattern, same team DoD validation -- but purpose-built for hardware product development. The plugin **consumes** the existing `kicad-happy/` skills (installed separately via the Claude Code plugin system at `~/.claude/plugins/cache/kicad-happy/`) as building blocks rather than duplicating them. It adds the orchestration layer, the hardware-specific roles, the hardware development stages, and the validation gates that turn isolated tools into a structured delivery process.

---

## 2. User Personas

### Primary Personas

**Persona 1: Elena -- The Solo Hardware Developer**
- **Role:** Independent electronics engineer / maker
- **Context:** Designs single-board PCBs for personal projects, small-batch products, or freelance clients. Works alone, handling everything from schematic to production handoff. Uses KiCad as primary EDA tool.
- **Key Need:** A structured process that catches the mistakes a solo developer misses -- the forgotten pull-up resistor, the BOM with an obsolete part, the layout that violates the fab house's minimum trace width. Needs the "second pair of eyes" that a team would provide.
- **Pain Points:** No review process. Easy to forget DFM checks. Compliance is a mystery. Moves from schematic to fabrication without structured validation gates.
- **Technical Level:** High on electrical engineering, moderate on manufacturing, low on compliance/regulatory.

**Persona 2: Marcus -- The Hardware Team Lead**
- **Role:** Hardware engineering lead at a startup (3-8 person team)
- **Context:** Manages a small team developing IoT devices or consumer electronics. Needs consistency across team members' outputs. Wants structured reviews without the overhead of heavyweight PLM tools.
- **Key Need:** A repeatable pipeline that enforces quality gates -- every design goes through schematic review, DRC, BOM validation, DFM check, and compliance scan before prototyping. Wants to catch issues at design time, not after $5,000 in prototype boards arrive with errors.
- **Pain Points:** Reviews are ad hoc. No standard process for design handoff. Different engineers use different checklists (or none). Prototype failures trace back to skipped review steps.
- **Technical Level:** High across all hardware disciplines.

**Persona 3: Priya -- The Firmware/Hardware Bridge Engineer**
- **Role:** Firmware engineer who must interface with hardware designs
- **Context:** Writes embedded software for boards designed by others. Needs to understand the hardware-software interface: pin assignments, power domains, communication buses, debug interfaces.
- **Key Need:** A structured handoff from hardware design to firmware bring-up. Wants clear documentation of the hardware interface, test points, and known hardware limitations before writing a line of code.
- **Pain Points:** Receives schematics without interface documentation. Discovers pin assignment conflicts during bring-up. No structured place to capture firmware requirements that feed back into hardware design.
- **Technical Level:** High on firmware, moderate on electrical engineering, low on PCB layout and manufacturing.
- **Phase 1 Coverage:** Firmware interface documentation (pin assignment table, power domain map, communication bus interface spec) is produced by the Electrical Engineer role during the Schematic stage. Full firmware pipeline integration is deferred to Phase 2. [C4 resolution]

### Secondary Personas

**Persona 4: David -- The Compliance Specialist**
- **Role:** Regulatory compliance consultant
- **Context:** Reviews hardware designs for EMC, safety, and environmental compliance (FCC, CE, UL, RoHS, REACH). Engaged at specific milestones in the development process.
- **Key Need:** A structured compliance gate with evidence-linked requirements per target market. Wants to see the EMC pre-compliance analysis, safety analysis, and environmental compliance documentation in a standardized format.
- **Pain Points:** Receives designs at random points in development. No standard checklist. Often engaged too late to influence design decisions cost-effectively.
- **Technical Level:** High on compliance/regulatory, moderate on electrical engineering, low on PCB layout.

**Persona 5: Wei -- The Manufacturing Engineer**
- **Role:** DFM/DFA specialist at a contract manufacturer
- **Context:** Reviews designs for manufacturability before quoting or accepting a production run. Needs standardized DFM review artifacts.
- **Key Need:** Designs that arrive with DFM/DFA pre-screening already done -- correct panelization, adequate test point coverage, components that match the CM's capabilities, and complete manufacturing transfer packages.
- **Pain Points:** Receives designs with fundamental DFM violations. BOM includes obsolete or long-lead-time parts. No standard format for manufacturing transfer packages.
- **Technical Level:** High on manufacturing, moderate on electrical engineering, low on firmware.

---

## 3. User Stories (by Epic)

### Epic 1: Plugin Foundation & Pipeline Orchestrator

**Epic Goal:** Establish the hardware-team plugin skeleton and 8-stage pipeline orchestrator that coordinates hardware development from concept to production release.
**Success Metric:** Pipeline executes all 8 stages with gate validation between each stage for a simple single-board project.
**Out of Scope:** Role-specific skill content (covered in Epics 2-4).

| # | Story Title | Priority | Points | Dependencies |
|---|-------------|----------|--------|--------------|
| 1.1 | Plugin skeleton creation | P1 | 5 | None |
| 1.2 | Pipeline orchestrator with 8 stages | P1 | 8 | 1.1 |
| 1.3 | Stage gate validation framework | P1 | 8 | 1.2 |
| 1.4 | Config-driven pipeline (.hardware/config.yml) | P1 | 5 | 1.2 |
| 1.5 | Pipeline state persistence and resume | P2 | 5 | 1.2 |
| 1.6 | Self-learning memory (.hardware/memory/) | P2 | 5 | 1.2 |
| 1.7 | Rework loop support (non-linear stage revisitation) | P1 | 8 | 1.2, 1.3 |
| 1.8 | Marketplace registration | P1 | 2 | 1.1 |

**Story 1.1: Plugin Skeleton Creation**

As a **plugin developer**, I want the `hardware-team/` directory to be created with the standard plugin structure (SKILL.md, skills/, references/, hooks/, scripts/), so that the plugin follows CLAUDE.md conventions and is discoverable by the Claude Code harness.

Acceptance Criteria:
- Given the `hardware-team/` directory does not exist, when the plugin skeleton is created, then the directory structure matches the pattern defined in CLAUDE.md (SKILL.md, skills/, references/, hooks/, scripts/, LICENSE.txt)
- Given the SKILL.md is created, when it is loaded by the Claude Code harness, then it contains metadata (name, description, license) and three-level context loading instructions
- Given the plugin skeleton exists, when `marketplace.json` is checked, then hardware-team is NOT yet registered (registration is a separate story)

**Story 1.2: Pipeline Orchestrator with 8 Stages**

As a **hardware developer (Elena)**, I want a pipeline orchestrator that guides my project through 8 hardware development stages (Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release), so that I follow a structured process instead of ad-hoc development.

Acceptance Criteria:
- Given a new hardware project, when the pipeline starts, then Stage 1 (Concept) is executed first
- Given a stage completes and passes its gate, when the pipeline advances, then the next stage in sequence is activated
- Given all 8 stages exist, when the pipeline is inspected, then each stage has a defined purpose, key activities list, and required role(s)
- Given the orchestrator dispatches work, when a stage is executed, then it is dispatched as a sub-agent via the Agent tool (NOT inlined -- same guardrail as delivery-flow)
- Given the pipeline runs, when stage transitions occur, then each transition is logged with timestamp and gate result
- **[C3]** Given stages are classified by execution mode, when inspected, then each stage is marked as one of:
  - **AI-execution stage** (Concept, Schematic, Layout, DFM/DFA, Compliance): The AI agent performs analysis, generates artifacts, and evaluates gates autonomously
  - **Human-execution stage** (Prototype, Pilot Run, Production Release): The AI agent generates preparation documentation (ordering packages, test procedures, manufacturing transfer packages, production checklists), presents it to the human, and then awaits human confirmation of physical completion before evaluating the exit gate. These stages follow a gate-in/human-action/gate-out orchestration pattern where the AI generates the "what to do" and the human executes it physically.

**Story 1.3: Stage Gate Validation Framework**

As a **hardware team lead (Marcus)**, I want validation gates between pipeline stages that enforce quality checks before advancing, so that defects are caught at design time rather than after prototype fabrication.

Acceptance Criteria:
- Given the gate framework exists, when a stage completes, then the gate evaluates all required validators for that stage
- Given a gate has multiple validators, when ALL validators report DONE, then the gate passes and the pipeline advances
- Given ANY validator reports NOT_DONE, when the gate evaluates, then the pipeline does not advance and the failing validator's feedback is returned to the stage for correction
- Given gate validators are defined, when they are inspected, then each has: unique ID, description, pass/fail criteria, and the role responsible for evaluation
- Given the Team DoD pattern from delivery-flow, when applied to hardware, then hardware-specific DoD criteria replace software-specific criteria (e.g., "DRC passes" instead of "unit tests pass")

**Story 1.4: Config-Driven Pipeline (.hardware/config.yml)**

As a **hardware developer (Elena)**, I want to configure my project settings (target fab house, compliance regions, BOM budget, production volume targets) in a `.hardware/config.yml` file, so that the pipeline adapts to my specific project constraints.

Acceptance Criteria:
- Given a `.hardware/config.yml` file exists in the project root, when the pipeline starts, then it loads and validates the config against the schema
- Given the config specifies `target_fab: jlcpcb`, when DFM validation runs, then it reads the config value and passes it to the DFM gate for fab-specific rule selection [C7: P1 reads static config values; dynamic pipeline adaptation is P2 via FR-021]
- Given the config specifies `compliance_regions: [FCC, CE]`, when the Compliance stage runs, then it reads the config value and evaluates requirements for the specified regions
- Given no `.hardware/config.yml` exists, when the pipeline starts, then it uses sensible defaults and logs "No project config found, using defaults"
- Given an invalid config file, when validation runs, then it warns about invalid fields and uses defaults for those fields (never fails the pipeline due to config errors)
- Given the config schema, when inspected, then it has a version field and follows the extension protocol pattern from delivery-flow's config-schema.md
- Given the config schema, when inspected, then it includes a `dependencies` section with `kicad_happy_version` field for version compatibility tracking [C2]
- Given the config schema, when inspected, then it includes rework termination fields: `max_rework_iterations` (default 3, per path) and `max_total_reworks` (default 10, per pipeline run) [C8]

**Story 1.5: Pipeline State Persistence and Resume**

As a **hardware developer (Elena)**, I want the pipeline to save its state so I can resume a hardware project across multiple sessions, so that I do not lose progress when a session ends.

Acceptance Criteria:
- Given a pipeline is in progress, when the session ends, then the current stage, gate results, and artifact paths are persisted to `.hardware/state.md`
- Given a persisted state exists, when a new session starts and the user requests to resume, then the pipeline loads the saved state and continues from the last completed stage
- Given a pipeline has completed stages 1-4, when resumed, then stages 1-4 are not re-executed and their artifacts are available to subsequent stages

**Story 1.6: Self-Learning Memory**

As a **hardware developer (Elena)**, I want the pipeline to learn from past project runs and apply those lessons to future runs, so that repeated mistakes are avoided and best practices accumulate.

Acceptance Criteria:
- Given a pipeline run completes, when lessons are captured, then they are stored in `.hardware/memory/` using tiered chunked retrieval (same pattern as delivery-flow)
- Given memory entries exist, when a new pipeline run starts, then relevant memories are injected into stage prompts
- Given a memory entry exists for "DFM violation: trace width below JLCPCB minimum on previous project", when the Layout stage runs, then the memory is surfaced as a caution

**Story 1.7: Rework Loop Support**

As a **hardware developer (Elena)**, I want the pipeline to support rework loops (e.g., prototype failure triggers return to schematic stage) instead of only linear progression, so that the pipeline reflects actual hardware development where iteration between stages is normal.

Acceptance Criteria:
- Given a prototype stage identifies a schematic-level issue, when the rework loop triggers, then the pipeline returns to the Schematic stage with the specific issue documented as context
- Given a rework loop is triggered, when the target stage re-executes, then it has access to the original stage artifacts AND the rework reason
- Given the pipeline supports rework, when rework loops are inspected, then the following paths are defined: Prototype -> Schematic, Prototype -> Layout, DFM/DFA -> Layout, DFM/DFA -> Schematic, Compliance -> Schematic, Pilot Run -> DFM/DFA
- Given a rework loop completes, when the pipeline resumes forward, then all downstream gates from the rework target are re-validated (not skipped)
- Given rework occurs, when the pipeline state is inspected, then the rework history is logged with: trigger reason, source stage, target stage, and resolution
- **[C8]** Given a rework path has been triggered N times (configurable via `max_rework_iterations`, default 3), when it triggers again, then the pipeline DOES NOT loop. Instead, it escalates to the human with: the rework history for that path, the recurring failure pattern, and a recommendation to intervene manually.
- **[C8]** Given the total rework count across ALL paths in a single pipeline run reaches the limit (configurable via `max_total_reworks`, default 10), when any rework triggers, then the pipeline escalates to the human with: the full rework history, a summary of all rework patterns, and a recommendation to reassess the design approach.
- **[C8]** Given rework termination triggers, when the pipeline escalates, then the escalation includes: (a) which limit was hit (per-path or total), (b) the count of reworks for each path, (c) the cumulative rework history, and (d) a clear message that the pipeline is paused pending human decision (continue, abort, or override limit).

**Story 1.8: Marketplace Registration**

As a **plugin marketplace user**, I want the hardware-team plugin to be registered in `marketplace.json` with a unique ID, display name, and description, so that it is discoverable alongside other plugins.

Acceptance Criteria:
- Given the plugin skeleton exists, when `marketplace.json` is updated, then it contains an entry with unique ID `hardware-team`, display name, description, and skill paths
- Given the marketplace entry exists, when validated against other entries, then there are no ID conflicts with existing plugins
- Given the marketplace entry, when inspected, then the description clearly states the plugin's purpose and its relationship to kicad-happy skills (external dependency)

---

### Epic 2: Core Hardware Roles (Phase 1)

**Epic Goal:** Implement the 6 first-class hardware roles as context-isolated skills with three-level loading.
**Success Metric:** Each role skill loads only its own references, produces role-appropriate artifacts, and integrates with the pipeline orchestrator.
**Out of Scope:** Mechanical Engineer and Firmware Engineer are deferred to Phase 2 per risk mitigation.

| # | Story Title | Priority | Points | Dependencies |
|---|-------------|----------|--------|--------------|
| 2.1 | Hardware Product Owner skill | P1 | 5 | 1.1 |
| 2.2 | Electrical Engineer skill | P1 | 8 | 1.1 |
| 2.3 | PCB Layout Engineer skill | P1 | 8 | 1.1 |
| 2.4 | Manufacturing Engineer skill | P1 | 5 | 1.1 |
| 2.5 | Compliance Engineer skill | P1 | 5 | 1.1 |
| 2.6 | Test Engineer skill | P1 | 5 | 1.1 |

**Story 2.1: Hardware Product Owner Skill**

As a **hardware team lead (Marcus)**, I want a Hardware Product Owner role that manages requirements, trade-offs, schedule, and stakeholder communication for hardware projects, so that hardware development has the same product discipline as software delivery.

Acceptance Criteria:
- Given the HW PO skill exists at `hardware-team/skills/hw-product-owner/SKILL.md`, when loaded, then it contains role-specific references for hardware requirements capture, feasibility analysis, make-vs-buy decisions, and BOM budgeting
- Given a Concept stage task, when the HW PO is invoked, then it produces: requirements document, constraint matrix, regulatory landscape scan, and initial BOM budget
- Given the skill is loaded, when it executes, then it loads ONLY HW PO references (zero cross-role context bleed)
- Given the HW PO interacts with other roles, when trade-off decisions are needed, then it documents the decision rationale using the decision record pattern

**Story 2.2: Electrical Engineer Skill**

As a **hardware developer (Elena)**, I want an Electrical Engineer role that handles schematic design, component selection, simulation, and signal integrity analysis, so that electrical design follows structured review practices.

Acceptance Criteria:
- Given the EE skill exists at `hardware-team/skills/electrical-engineer/SKILL.md`, when loaded, then it contains references for schematic design, component selection criteria, simulation methodology, and power tree analysis
- Given a Schematic stage task, when the EE is invoked, then it produces: schematic review artifacts, component selection rationale, and simulation results
- Given the EE needs to select components, when it performs component search, then it CONSUMES `kicad-happy:digikey`, `kicad-happy:mouser`, `kicad-happy:lcsc`, and `kicad-happy:element14` skills (does NOT reimplement search)
- Given the EE needs to run simulations, when it performs SPICE analysis, then it CONSUMES `kicad-happy:spice` (does NOT reimplement simulation)
- Given the EE reviews a schematic, when the iterative review pattern (from issue #76) is applied, then the review uses forced-find prompting and deduplication across multiple review passes
- **[C4]** Given the EE is in the Schematic stage, when schematic design is complete, then the EE produces firmware interface documentation as an additional output artifact: pin assignment table, power domain map, communication bus interface spec (I2C/SPI/UART address map, clock rates, voltage levels), and debug interface access points. This artifact serves Persona 3 (Priya) and is a required input for the Phase 2 Firmware Engineer role.

**Story 2.3: PCB Layout Engineer Skill**

As a **hardware developer (Elena)**, I want a PCB Layout Engineer role that handles physical layout, routing, stackup definition, impedance control, and DRC validation, so that PCB layout follows structured design rules.

Acceptance Criteria:
- Given the Layout skill exists at `hardware-team/skills/pcb-layout-engineer/SKILL.md`, when loaded, then it contains references for layout best practices, routing guidelines, stackup design, and impedance control
- Given a Layout stage task, when the Layout Engineer is invoked, then it produces: layout review artifacts, routing analysis, and DRC results
- Given the Layout Engineer needs to analyze a KiCad PCB, when it performs analysis, then it CONSUMES `kicad-happy:kicad` (does NOT reimplement KiCad analysis)
- Given the Layout Engineer operates on spatial/geometric reasoning tasks, when the skill's SKILL.md is inspected, then it documents a minimum model tier requirement of Sonnet+ (per issue #76 learning: Haiku is insufficient for geometry reasoning)

**Story 2.4: Manufacturing Engineer Skill**

As a **manufacturing engineer (Wei)**, I want a Manufacturing Engineer role that handles DFM/DFA review, assembly process guidance, yield optimization, and production transfer, so that designs are manufacturable before they reach the fab house.

Acceptance Criteria:
- Given the MfgE skill exists at `hardware-team/skills/manufacturing-engineer/SKILL.md`, when loaded, then it contains references for DFM rules, DFA guidelines, panelization, and test point coverage requirements
- Given a DFM/DFA stage task, when the MfgE is invoked, then it produces: DFM review report, DFA review report, yield risk assessment, and remediation guidance
- Given the MfgE needs fab-specific rules, when it evaluates DFM, then it CONSUMES `kicad-happy:jlcpcb` and `kicad-happy:pcbway` for fab-house-specific design rules
- Given the MfgE needs BOM data, when it evaluates component availability, then it CONSUMES `kicad-happy:bom` for BOM validation
- Given the MfgE reviews a design, when the DFM gate evaluates, then it checks: minimum trace/space, via sizes, layer count compatibility, surface finish compatibility, and component footprint availability at the target CM

**Story 2.5: Compliance Engineer Skill**

As a **compliance specialist (David)**, I want a Compliance Engineer role that handles EMC pre-compliance, safety analysis, environmental compliance, and regulatory documentation, so that designs are compliance-ready before engaging test labs.

Acceptance Criteria:
- Given the CompE skill exists at `hardware-team/skills/compliance-engineer/SKILL.md`, when loaded, then it contains references for EMC design rules, safety standards (IEC 62368-1, IEC 60950), environmental regulations (RoHS, REACH, WEEE), and market-specific requirements (FCC Part 15, CE RED, UL)
- Given a Compliance stage task, when the CompE is invoked, then it produces: EMC pre-compliance report, safety analysis, environmental compliance checklist, and test lab preparation package
- Given the CompE needs EMC analysis, when it performs pre-compliance checks, then it CONSUMES `kicad-happy:emc` (does NOT reimplement EMC analysis)
- Given the CompE needs documentation, when it generates regulatory packages, then it CONSUMES `kicad-happy:kidoc` (does NOT reimplement documentation generation)
- Given the config specifies `compliance_regions: [FCC, CE]`, when the compliance gate evaluates, then it produces a checklist with evidence-linked requirements for EACH specified region

**Story 2.6: Test Engineer Skill**

As a **hardware team lead (Marcus)**, I want a Test Engineer role that handles test strategy, test fixture design, production test development, and validation planning, so that hardware is testable and test coverage is planned from the start.

Acceptance Criteria:
- Given the TestE skill exists at `hardware-team/skills/test-engineer/SKILL.md`, when loaded, then it contains references for test strategy frameworks, test fixture design patterns, production test methodologies, and validation planning
- Given a Prototype stage task, when the TestE is invoked, then it produces: test strategy document, test fixture requirements, bring-up test procedure, and validation acceptance criteria
- Given the TestE plans production tests, when test point coverage is evaluated, then it cross-references the PCB layout for adequate test access
- Given the TestE produces a test strategy, when it is inspected, then it covers: functional testing, environmental testing (if applicable), reliability testing, and production screening

---

### Epic 3: kicad-happy Integration Layer

**Epic Goal:** Define and implement the interface for consuming kicad-happy skills as sub-agents within the hardware pipeline.
**Success Metric:** All 11 kicad-happy skills are consumable through the integration layer without duplication of functionality.
**Out of Scope:** Modifying kicad-happy skills themselves.

| # | Story Title | Priority | Points | Dependencies |
|---|-------------|----------|--------|--------------|
| 3.1 | Integration layer architecture | P1 | 8 | 1.1 |
| 3.2 | Component sourcing integration (DigiKey, Mouser, LCSC, element14) | P1 | 5 | 3.1 |
| 3.3 | Fabrication integration (JLCPCB, PCBWay) | P1 | 5 | 3.1 |
| 3.4 | Analysis integration (KiCad, SPICE, EMC) | P1 | 5 | 3.1 |
| 3.5 | Documentation integration (kidoc, BOM) | P1 | 3 | 3.1 |
| 3.6 | kicad-happy dependency documentation & verification | P1 | 5 | 3.1 |

**Story 3.1: Integration Layer Architecture**

As a **plugin developer**, I want a defined interface for consuming kicad-happy skills from within the hardware pipeline, so that the hardware-team orchestrator can dispatch to kicad-happy skills without reimplementing their functionality.

Acceptance Criteria:
- Given the integration layer is defined, when a hardware role needs a kicad-happy capability, then the integration layer provides a dispatch pattern (skill name, expected input, expected output)
- Given the integration layer exists, when it dispatches to a kicad-happy skill, then it uses cross-plugin skill invocation via the Skill tool (verified to work -- kicad-happy is installed at `~/.claude/plugins/cache/kicad-happy/kicad-happy/1.2.0/`)
- Given a kicad-happy skill is unavailable (not installed), when the integration layer attempts dispatch, then it fails gracefully with a clear error message indicating which skill is missing and how to install it (install instructions reference `kicad-happy` plugin installation via Claude Code plugin system)
- Given the integration layer maps roles to skills, when the mapping is inspected, then each kicad-happy skill is mapped to the hardware role(s) that consume it:
  - Electrical Engineer -> kicad, spice, digikey, mouser, lcsc, element14
  - PCB Layout Engineer -> kicad
  - Manufacturing Engineer -> jlcpcb, pcbway, bom
  - Compliance Engineer -> emc, kidoc
- **[C6]** Given the integration layer architecture document, when it defines "reimplementation," then it uses this operational definition: "A capability is reimplemented if a hardware-team role performs an action that would produce the same output as invoking a kicad-happy skill, without invoking that skill." Examples included:
  - **IS reimplementation:** A hardware role parsing `.kicad_sch` files to extract BOM data instead of invoking `kicad-happy:kicad`. A hardware role querying DigiKey's API directly instead of invoking `kicad-happy:digikey`. A hardware role implementing EMC rule checks from scratch instead of invoking `kicad-happy:emc`.
  - **IS NOT reimplementation:** A hardware role's SKILL.md containing domain knowledge that guides *when* and *how* to invoke a kicad-happy skill (e.g., "check capacitor derating" as a review checklist item that triggers a `kicad-happy:kicad` invocation). A hardware role interpreting kicad-happy output and making engineering judgments about it.

**Story 3.2: Component Sourcing Integration**

As an **electrical engineer (Elena)**, I want to search multiple component distributors (DigiKey, Mouser, LCSC, element14) through the pipeline's Electrical Engineer role, so that component selection is part of the structured design process rather than a separate ad-hoc step.

Acceptance Criteria:
- Given the EE role is in the Schematic stage, when component selection is needed, then the EE can invoke `kicad-happy:digikey`, `kicad-happy:mouser`, `kicad-happy:lcsc`, or `kicad-happy:element14` via the integration layer
- Given a component search returns results from multiple distributors, when the EE evaluates options, then it considers: price, availability, lead time, lifecycle status, and second-source availability
- Given the integration layer dispatches to a sourcing skill, when the result returns, then it includes: part number, price, stock quantity, and datasheet availability

**Story 3.3: Fabrication Integration**

As a **manufacturing engineer (Wei)**, I want to validate designs against specific fabrication house capabilities (JLCPCB, PCBWay) through the pipeline, so that DFM checks are fab-specific rather than generic.

Acceptance Criteria:
- Given the MfgE role is in the DFM/DFA stage, when DFM validation runs, then it invokes `kicad-happy:jlcpcb` or `kicad-happy:pcbway` based on the `target_fab` config setting
- Given JLCPCB is the target fab, when DFM rules are evaluated, then JLCPCB-specific constraints (minimum trace/space, via sizes, layer stackup options, assembly capabilities) are applied
- Given fabrication output generation is needed, when the Prototype stage runs, then Gerber, drill, and BOM/CPL files are generated consuming the appropriate kicad-happy fab skill

**Story 3.4: Analysis Integration**

As an **electrical engineer (Elena)**, I want to run KiCad analysis, SPICE simulation, and EMC pre-compliance checks through the pipeline, so that design validation is part of the structured process.

Acceptance Criteria:
- Given the EE role is in the Schematic stage, when simulation is needed, then it invokes `kicad-happy:spice` via the integration layer
- Given the CompE role is in the Compliance stage, when EMC pre-compliance is needed, then it invokes `kicad-happy:emc` via the integration layer
- Given any role needs KiCad project analysis, when schematic or PCB analysis is needed, then it invokes `kicad-happy:kicad` via the integration layer
- Given an analysis skill returns results, when the results are integrated into the pipeline, then they are stored as stage artifacts and available to downstream gates

**Story 3.5: Documentation Integration**

As a **compliance specialist (David)**, I want to generate professional engineering documentation (HDD, CE Technical Files, Manufacturing Transfer Packages) through the pipeline, so that documentation is produced as part of the structured process rather than as an afterthought.

Acceptance Criteria:
- Given the CompE role is in the Compliance stage, when regulatory documentation is needed, then it invokes `kicad-happy:kidoc` via the integration layer
- Given the MfgE role is in the Production Release stage, when the manufacturing transfer package is needed, then it invokes `kicad-happy:kidoc` for document generation and `kicad-happy:bom` for BOM finalization
- Given documentation is generated, when it is stored, then it is saved as a stage artifact with clear provenance (which skill produced it, which stage, which gate)

**Story 3.6: kicad-happy Dependency Documentation & Verification [C2]**

As a **hardware developer (Elena)**, I want clear documentation of the kicad-happy dependency, version compatibility tracking, and automated availability verification at session start, so that I know whether my environment is correctly configured before starting a pipeline run.

Acceptance Criteria:
- Given the hardware-team plugin is installed, when its documentation is inspected, then it includes a "Prerequisites" section that: (a) states kicad-happy is a required external dependency, (b) documents the installation mechanism (Claude Code plugin system via `~/.claude/plugins/`), (c) lists the minimum compatible kicad-happy version, and (d) provides step-by-step installation instructions
- Given `.hardware/config.yml` exists, when the `dependencies` section is inspected, then it includes a `kicad_happy_version` field that specifies the minimum compatible version (e.g., `kicad_happy_version: ">=1.2.0"`)
- Given the SessionStart hook fires (Story 5.3), when kicad-happy availability is checked, then the hook verifies that all 11 kicad-happy skills are loadable and reports: (a) which skills are available, (b) which skills are missing, and (c) installation instructions for any missing skills
- Given kicad-happy is not installed, when the pipeline attempts to start, then it displays a clear error: "Required dependency kicad-happy is not installed. Install it via: [installation instructions]. The hardware-team plugin requires kicad-happy for component sourcing, fabrication validation, KiCad analysis, and documentation generation."
- Given the kicad-happy version does not meet the minimum compatibility requirement, when version checking runs, then a warning is displayed: "kicad-happy version X.Y.Z installed; hardware-team requires >=A.B.C. Some features may not work correctly."

---

### Epic 4: Hardware-Specific Validation Gates

**Epic Goal:** Implement the 5 hardware-specific validation gates that enforce quality between pipeline stages, backed by a reference test fixture for measurable acceptance criteria.
**Success Metric:** Each gate catches its target defect category with >80% detection rate (applying issue #76 iterative review learnings).

| # | Story Title | Priority | Points | Dependencies |
|---|-------------|----------|--------|--------------|
| 4.0 | Reference test fixture creation | P1 | 5 | 1.1 |
| 4.1 | Schematic Review Gate | P1 | 8 | 1.3, 2.2, 4.0 |
| 4.2 | DRC Gate | P1 | 5 | 1.3, 2.3, 4.0 |
| 4.3 | BOM Gate | P1 | 5 | 1.3, 3.2, 4.0 |
| 4.4 | DFM Gate | P1 | 5 | 1.3, 2.4, 3.3, 4.0 |
| 4.5 | Compliance Gate | P1 | 5 | 1.3, 2.5, 3.4, 4.0 |

**Story 4.0: Reference Test Fixture Creation [C5]**

As a **plugin developer**, I want a reference KiCad project with known, seeded defects across all validation categories, so that all 5 validation gates (Stories 4.1-4.5) have a measurable benchmark for acceptance criteria and the North Star metric is quantifiable.

Acceptance Criteria:
- Given the test fixture directory exists at `hardware-team/references/test-fixtures/`, when it is inspected, then it contains:
  - **(a) Reference KiCad schematic** (`.kicad_sch`) with exactly 10 seeded defects across all 7 schematic review categories: power integrity (e.g., missing bulk capacitor on voltage regulator), signal integrity (e.g., unterminated high-speed trace), component derating (e.g., capacitor rated at exactly operating voltage), missing pull-ups/pull-downs (e.g., floating I2C lines), decoupling strategy (e.g., missing decoupling cap on IC power pin), voltage level compatibility (e.g., 5V signal to 3.3V input without level shifter), thermal considerations (e.g., high-power component without thermal relief)
  - **(b) Reference BOM** with known issues: at least 1 obsolete component, at least 1 component exceeding a test budget threshold, at least 1 single-source component with no second source, at least 1 NRND (not recommended for new designs) component
  - **(c) Reference PCB layout** (`.kicad_pcb`) with DFM violations: at least 1 trace width below JLCPCB minimum, at least 1 via size below minimum, at least 1 solder mask aperture violation, at least 1 clearance violation
- Given each seeded defect, when it is documented, then a manifest file (`test-fixtures/MANIFEST.md`) lists: defect ID, category, location in the KiCad file, expected detection gate, and expected severity
- Given the test fixtures exist, when they are used by Stories 4.1-4.5, then each gate's acceptance criteria can be verified against a known ground truth (not dependent on real-world projects or live API data)
- Given the BOM test fixture, when it is used by Story 4.3 (BOM Gate), then it includes static reference pricing data (not requiring live distributor API calls) so that budget threshold acceptance criteria are testable offline

**Story 4.1: Schematic Review Gate**

As a **hardware team lead (Marcus)**, I want a multi-reviewer schematic review gate that catches electrical design issues before layout begins, so that fundamental design errors do not propagate to PCB layout and prototyping.

Acceptance Criteria:
- Given a schematic is ready for review, when the Schematic Review Gate activates, then it applies the iterative review agent pattern from issue #76 (multiple reviewers with forced-find prompting)
- Given the gate runs, when review categories are checked, then the following categories are covered: power integrity, signal integrity, component derating, missing pull-ups/pull-downs, decoupling strategy, voltage level compatibility, thermal considerations
- Given multiple reviewers operate on the same schematic, when their findings are aggregated, then deduplication is applied (per issue #76 learning)
- Given a finding is reported, when it is presented, then it includes: finding ID, severity (critical/major/minor), location (sheet/component/net), description, and recommended fix
- Given ANY critical finding exists, when the gate evaluates, then it returns NOT_DONE and blocks pipeline advancement
- Given the reference test fixture (Story 4.0), when the gate is run against it, then it detects defects in at least 6 of 7 seeded categories (>80% category detection rate per M2)

**Story 4.2: DRC Gate**

As a **hardware developer (Elena)**, I want an automated DRC gate that validates design rule compliance with pass/fail results and remediation guidance, so that PCB layouts meet fab house requirements before prototype ordering.

Acceptance Criteria:
- Given a PCB layout is ready for DRC, when the DRC Gate activates, then it runs design rule checks against the target fab house's capabilities
- Given DRC violations are found, when they are reported, then each violation includes: rule violated, location (layer/coordinates), severity, and specific remediation steps
- Given zero DRC violations of severity "error" exist, when the gate evaluates, then it returns DONE
- Given DRC violations of severity "warning" exist but no "errors", when the gate evaluates, then it returns DONE with warnings documented
- Given the DRC gate uses KiCad analysis, when it runs, then it CONSUMES `kicad-happy:kicad` for DRC parsing

**Story 4.3: BOM Gate**

As a **manufacturing engineer (Wei)**, I want a BOM validation gate that checks cost, component availability, lifecycle status, and second-source availability, so that prototypes are not ordered with unobtainable or obsolete parts.

Acceptance Criteria:
- Given a BOM is ready for validation, when the BOM Gate activates, then it checks each line item for: price vs. budget, stock availability, lifecycle status (active, NRND, obsolete, EOL), and second-source existence
- Given a component has lifecycle status NRND or obsolete, when the BOM Gate evaluates, then it returns NOT_DONE with a finding requiring substitution or explicit risk acceptance
- Given the BOM budget is defined in config, when total BOM cost exceeds the budget, then the gate returns NOT_DONE with a cost breakdown and budget variance
- Given the BOM Gate needs pricing data, when it evaluates, then it CONSUMES kicad-happy sourcing skills (digikey, mouser, lcsc, element14) via the integration layer
- Given a component has no second source, when the BOM Gate evaluates, then it flags it as a single-source risk (warning, not blocking unless config requires second-source)

**Story 4.4: DFM Gate**

As a **manufacturing engineer (Wei)**, I want a DFM validation gate that checks manufacturability against the target fab house's capabilities, so that designs are producible before prototype ordering.

Acceptance Criteria:
- Given a design is ready for DFM review, when the DFM Gate activates, then it evaluates: minimum trace width/spacing, via sizes, drill aspect ratios, layer count vs. fab capability, surface finish compatibility, solder mask aperture sizes, and component footprint availability
- Given the target fab is JLCPCB, when DFM rules are evaluated, then JLCPCB-specific capabilities and limitations are applied (consuming `kicad-happy:jlcpcb`)
- Given a DFM violation is found, when it is reported, then it includes: rule violated, current value, required value, location, and remediation guidance
- Given zero DFM violations exist, when the gate evaluates, then it returns DONE
- Given DFM violations exist, when the gate evaluates, then it returns NOT_DONE with a remediation plan

**Story 4.5: Compliance Gate**

As a **compliance specialist (David)**, I want a regulatory compliance gate with evidence-linked requirements per target market, so that compliance readiness is validated before engaging test labs.

Acceptance Criteria:
- Given the config specifies `compliance_regions: [FCC, CE]`, when the Compliance Gate activates, then it produces a checklist for EACH specified region
- Given a compliance checklist, when each requirement is evaluated, then it is linked to: the standard clause, the evidence artifact (EMC report, safety analysis, etc.), and pass/fail status
- Given the Compliance Gate needs EMC analysis, when it evaluates, then it CONSUMES `kicad-happy:emc` for EMC pre-compliance data
- Given ANY requirement has no linked evidence, when the gate evaluates, then it returns NOT_DONE with the missing evidence items listed
- Given all requirements have linked evidence and pass, when the gate evaluates, then it returns DONE with the complete compliance package

---

### Epic 5: Collaboration Patterns & Hooks

**Epic Goal:** Implement hardware-specific collaboration patterns and event-driven hooks.
**Success Metric:** Design Review Board pattern executes with 3+ role reviewers. Hooks fire correctly on their trigger events.

| # | Story Title | Priority | Points | Dependencies |
|---|-------------|----------|--------|--------------|
| 5.1 | Design Review Board pattern | P1 | 5 | 1.2, 2.2, 2.3, 2.4 |
| 5.2 | BOM Reconciliation pattern | P2 | 3 | 3.2, 4.3 |
| 5.3 | Config & dependency validation hook (SessionStart) | P1 | 5 | 1.4, 3.6 |
| 5.4 | Schematic DRC hook (PostToolUse) | P2 | 3 | 4.2 |
| 5.5 | BOM drift detection hook (PostToolUse) | P2 | 3 | 4.3 |

**Story 5.1: Design Review Board Pattern**

As a **hardware team lead (Marcus)**, I want a Design Review Board collaboration pattern where multiple hardware roles review a design artifact from their respective perspectives, so that cross-discipline issues are caught before stage advancement.

Acceptance Criteria:
- Given a design artifact (schematic or layout) is ready for review, when the Design Review Board pattern activates, then it dispatches review tasks to: Electrical Engineer, PCB Layout Engineer, Manufacturing Engineer, and Compliance Engineer (as applicable to the stage)
- Given multiple reviewers produce findings, when findings are aggregated, then deduplication is applied across reviewers
- Given the Design Review Board completes, when results are presented, then they are organized by reviewer role with a unified severity ranking
- Given the Design Review Board is based on delivery-team's adversarial review pattern, when it executes, then each reviewer independently evaluates the artifact (no shared context between reviewers during review)

**Story 5.2: BOM Reconciliation Pattern**

As a **manufacturing engineer (Wei)**, I want a BOM Reconciliation collaboration pattern that cross-validates BOM data across multiple suppliers, so that pricing and availability discrepancies are identified before ordering.

Acceptance Criteria:
- Given a BOM is ready for reconciliation, when the pattern activates, then it queries multiple kicad-happy sourcing skills for each BOM line item
- Given pricing data from multiple suppliers, when reconciliation completes, then discrepancies >20% between suppliers are flagged
- Given availability data from multiple suppliers, when reconciliation completes, then components available from only one supplier are flagged as single-source risk

**Story 5.3: Config & Dependency Validation Hook (SessionStart) [C2 extended]**

As a **hardware developer (Elena)**, I want the pipeline to validate both `.hardware/config.yml` and kicad-happy skill availability at session start, so that I am warned early if my config is missing, outdated, or my environment lacks required dependencies.

Acceptance Criteria:
- Given a SessionStart event fires, when `.hardware/config.yml` does not exist, then a warning is displayed: "No .hardware/config.yml found. Run `hw-setup` to create one."
- Given a SessionStart event fires, when `.hardware/config.yml` exists but has an outdated schema version, then a warning is displayed with migration guidance
- Given a SessionStart event fires, when `.hardware/config.yml` exists and is valid, then no config warning is displayed
- **[C2]** Given a SessionStart event fires, when kicad-happy skill availability is checked, then the hook attempts to verify that each of the 11 kicad-happy skills (kicad, spice, digikey, mouser, lcsc, element14, jlcpcb, pcbway, bom, emc, kidoc) is available, and reports: available count, missing skills list, and installation instructions for missing skills
- **[C2]** Given kicad-happy is fully installed, when the availability check completes, then a confirmation is displayed: "kicad-happy: 11/11 skills available"
- **[C2]** Given kicad-happy is partially installed or missing, when the availability check completes, then a warning is displayed: "kicad-happy: N/11 skills available. Missing: [list]. Install kicad-happy via Claude Code plugin system."

**Story 5.4: Schematic DRC Hook (PostToolUse)**

As a **hardware developer (Elena)**, I want DRC validation to run automatically when KiCad schematic files are modified, so that I get immediate feedback on design rule violations.

Acceptance Criteria:
- Given a PostToolUse event fires for Write or Edit, when the modified file has a `.kicad_sch` extension, then DRC validation is triggered automatically
- Given DRC validation runs, when violations are found, then they are displayed as warnings (not blocking the edit)
- Given DRC validation runs, when no violations are found, then no output is displayed (silent success)

**Story 5.5: BOM Drift Detection Hook (PostToolUse)**

As a **hardware developer (Elena)**, I want to be warned when schematic changes invalidate the current BOM, so that I know the BOM needs updating before I order parts.

Acceptance Criteria:
- Given a PostToolUse event fires for Write or Edit on a `.kicad_sch` file, when a BOM artifact exists from a previous pipeline stage, then the hook compares the current schematic's component list against the BOM
- Given the schematic has components not in the BOM, when drift is detected, then a warning is displayed listing the new/changed components
- Given the BOM has components not in the schematic, when drift is detected, then a warning is displayed listing the removed components

---

### Epic 6: Phase 2 Roles (Deferred)

**Epic Goal:** Add Mechanical Engineer and Firmware Engineer roles.
**Note:** This epic is explicitly deferred to Phase 2 per risk mitigation. Documented here for completeness and dependency tracking.

| # | Story Title | Priority | Points | Dependencies |
|---|-------------|----------|--------|--------------|
| 6.1 | Mechanical Engineer skill | P3 | 8 | 1.1 |
| 6.2 | Firmware Engineer skill | P3 | 5 | 1.1, 2.2 (firmware interface docs from EE) |

---

## 4. Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-001 | Plugin follows standard plugin structure (SKILL.md, skills/, references/, hooks/, scripts/, LICENSE.txt) per CLAUDE.md conventions | P1 | Directory structure matches pattern; SKILL.md loads with three-level context; marketplace.json contains valid entry |
| FR-002 | Pipeline orchestrator implements 8 hardware stages: Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release. Stages classified as AI-execution (Concept, Schematic, Layout, DFM/DFA, Compliance) or human-execution (Prototype, Pilot Run, Production Release) with gate-in/human-action/gate-out pattern for physical stages. [C3] | P1 | All 8 stages exist with defined purpose, key activities, required roles, and execution mode classification; AI stages execute autonomously; human stages generate preparation docs and await human confirmation |
| FR-003 | Stage gates enforce team DoD validation -- ALL validators must report DONE before pipeline advances | P1 | Gate with 3 validators: if 2 report DONE and 1 reports NOT_DONE, pipeline does NOT advance; failing validator's feedback is returned for correction |
| FR-004 | Config-driven pipeline via `.hardware/config.yml` with versioned schema. P1 scope: static config reading (fab target, compliance regions, BOM budget, dependency versions). P2 scope: dynamic pipeline adaptation per project type (FR-021). [C7] | P1 | Config loads at pipeline start; absent config uses defaults; invalid config warns and uses defaults for invalid fields; config version is tracked; `dependencies.kicad_happy_version` field present [C2] |
| FR-005 | Pipeline state persists to `.hardware/state.md` and resumes across sessions | P2 | State saved on session end; state loaded on resume; completed stages not re-executed |
| FR-006 | Self-learning memory in `.hardware/memory/` with tiered chunked retrieval | P2 | Lessons captured after pipeline run; relevant memories injected into stage prompts on subsequent runs |
| FR-007 | Rework loops support non-linear stage revisitation with defined paths AND termination conditions [C8] | P1 | Rework paths defined (Prototype->Schematic, Prototype->Layout, DFM->Layout, DFM->Schematic, Compliance->Schematic, Pilot->DFM); downstream gates re-validated after rework; rework history logged; per-path limit (default 3) and total limit (default 10) enforced; escalation to human when limits hit |
| FR-008 | 6 role-based skills (HW PO, EE, PCB Layout, MfgE, CompE, TestE) with context isolation. EE produces firmware interface documentation during Schematic stage. [C4] | P1 | Each skill loads ONLY its own references; zero cross-role context bleed verified; each role produces role-specific artifacts; EE produces pin assignment table, power domain map, bus interface spec |
| FR-009 | kicad-happy integration layer dispatches to kicad-happy skills via cross-plugin skill invocation (VERIFIED to work) | P1 | All 11 kicad-happy skills mapped to consuming roles; dispatch uses Skill tool; graceful failure when skill unavailable with installation instructions |
| FR-010 | Schematic Review Gate applies iterative multi-reviewer pattern with forced-find prompting and deduplication | P1 | 7 review categories covered; multiple reviewers with deduplication; critical findings block advancement |
| FR-011 | DRC Gate validates design rules against target fab capabilities | P1 | Consumes kicad-happy:kicad for DRC; violations include location, severity, remediation; zero errors = DONE |
| FR-012 | BOM Gate validates cost, availability, lifecycle status, and second-source for all components | P1 | NRND/obsolete components block advancement; budget exceeded blocks advancement; single-source flagged as warning |
| FR-013 | DFM Gate validates manufacturability against target fab house capabilities | P1 | Fab-specific rules applied (JLCPCB or PCBWay via config); violations include current vs. required values and remediation |
| FR-014 | Compliance Gate produces evidence-linked regulatory checklists per target market | P1 | Checklist per region in config; each requirement linked to evidence artifact; missing evidence blocks advancement |
| FR-015 | Design Review Board collaboration pattern dispatches multi-role reviews with deduplication | P1 | 3+ roles review independently; findings deduplicated; results organized by role with unified severity |
| FR-016 | BOM Reconciliation pattern cross-validates across multiple suppliers | P2 | Pricing discrepancies >20% flagged; single-source risks identified |
| FR-017 | SessionStart hook validates `.hardware/config.yml` existence, schema version, AND kicad-happy skill availability [C2] | P1 | Missing config warns; outdated schema warns with migration guidance; valid config is silent; kicad-happy availability checked (11/11 or missing list with install instructions) |
| FR-018 | PostToolUse hook auto-runs DRC on `.kicad_sch` file modifications | P2 | DRC triggers on schematic edit; violations displayed as warnings; silent on success |
| FR-019 | PostToolUse hook detects BOM drift when schematic changes invalidate existing BOM | P2 | New/changed components listed; removed components listed; warning only (not blocking) |
| FR-020 | All pipeline stages and role dispatches use sub-agent invocation via Agent tool (NOT inlined) | P1 | Every stage dispatch is a separate Agent tool invocation; SKILL.md contains explicit guardrail language; same enforcement pattern as delivery-flow |
| FR-021 | Pipeline auto-detects project type (1-layer prototype vs. 8-layer production, hobby vs. certified) and dynamically adapts stage depth. This is P2 scope -- P1 reads static config values only. [C7] | P2 | Simple projects skip or minimize Compliance and Pilot Run stages; certified products enforce full Compliance gate; detection runs at pipeline start; requires FR-004 static config as foundation |
| FR-022 | Reference test fixture with seeded defects for all validation gate categories [C5] | P1 | Reference KiCad schematic (10 defects, 7 categories), reference BOM (4 issue types), reference PCB layout (4 DFM violation types); manifest documenting all seeded defects; stored in `hardware-team/references/test-fixtures/` |

---

## 5. Non-Functional Requirements

| ID | Requirement | Type | Target | Measurement Method |
|----|-------------|------|--------|--------------------|
| NFR-001 | No external dependencies beyond Python standard library | Portability | 0 external packages required | Inspect all scripts for import statements; verify no pip install needed |
| NFR-002 | Context isolation: each role skill loads only its own references | Performance / Correctness | 0 cross-role reference files loaded per skill invocation | Audit SKILL.md reference loading directives; test with context window logging |
| NFR-003 | kicad-happy skills consumed, never duplicated. [C6] Operational definition: "A capability is reimplemented if a hardware-team role performs an action that would produce the same output as invoking a kicad-happy skill, without invoking that skill." Role-specific domain knowledge that guides when/how to invoke kicad-happy skills is NOT reimplementation. | Architecture | 0 reimplemented kicad-happy capabilities in hardware-team codebase | Code review using operational definition; examples of IS and IS NOT reimplementation documented in integration layer architecture (Story 3.1) |
| NFR-004 | Pipeline completes 8 stages for a simple single-board project within a single extended session | Performance | Full pipeline run completes without session timeout | End-to-end test with a reference KiCad project |
| NFR-005 | Gate validation messages are comprehensible to hardware engineers who are not plugin developers | Usability | All gate messages include: what failed, where (component/net/location), why, and how to fix | Review sample gate outputs with persona validation |
| NFR-006 | Config schema is forward-compatible: old configs work with new plugin versions | Compatibility | Old config files missing new keys use defaults without error | Test with v1.0 config against v1.1+ schema |
| NFR-007 | Minimum model tier documented per role | Documentation | Each role SKILL.md specifies minimum model tier (Haiku/Sonnet/Opus) | Audit all 6 role SKILL.md files for model tier specification |
| NFR-008 | Memory lessons are retrievable in <2 seconds for tiered chunked retrieval | Performance | p95 retrieval < 2 seconds | Benchmark with 100+ memory entries |
| NFR-009 | Plugin structure passes plugin-dev:plugin-validator without errors | Quality | 0 validation errors | Run plugin-validator after implementation |
| NFR-010 | Rework loop history is auditable -- every rework trigger, path, resolution, AND termination event is logged [C8] | Auditability | 100% of rework events logged with: timestamp, source stage, target stage, trigger reason, resolution, iteration count for that path, total rework count | Inspect .hardware/state.md after pipeline runs with rework; verify termination events include limit type, counts, and escalation message |

---

## 6. Success Metrics

| Metric | Target | Baseline | Measurement Method |
|--------|--------|----------|--------------------|
| Pipeline coverage | Hardware project from concept to production release docs in one pipeline run | No structured process exists today | Run end-to-end pipeline on reference KiCad project (Story 4.0); verify all 8 stages produce artifacts |
| kicad-happy utilization | 100% of applicable kicad-happy skills consumed (11/11 mapped, 0 reimplemented per operational definition in NFR-003) [C6] | Skills used ad-hoc, not orchestrated | Code review using operational reimplementation definition; verify integration layer maps all 11 skills |
| Defect detection rate (Schematic Review Gate) | >80% of reviewable defect categories caught before prototype stage | Unknown -- no structured review exists | Run gate against reference test fixture (Story 4.0) with 10 seeded defects across 7 categories; count detection rate [C5] |
| Role context isolation | Zero cross-role context bleed across all 6 role skills | N/A (new plugin) | Audit each skill invocation log for reference files loaded; verify each loads only its own |
| Config-driven flexibility | Pipeline reads and applies 3+ distinct project configs without code changes (P1: static reading; P2: dynamic adaptation) [C7] | One-size-fits-all | P1: Configure 3 different project types via .hardware/config.yml; verify pipeline reads correct values. P2: Verify pipeline adapts stage depth. |
| Rework loop effectiveness | Pipeline correctly handles rework across all 6 defined rework paths, AND terminates rework loops at configured limits [C8] | No rework support exists | Trigger each rework path in test; verify downstream gates re-validate after rework; trigger rework limit to verify escalation |
| Gate quality | Each of the 5 gates produces actionable findings with location, severity, and remediation, measurable against reference test fixture [C5] | No gates exist | Review gate outputs against reference test fixture (Story 4.0); verify all findings include required fields |
| Pipeline completion rate (North Star) [C9] | 80% completion rate within first 3 months | 0% | Formula: `(qualifying_runs_completing_all_configured_stages / qualifying_runs_started) * 100`. A run is "qualifying" only if: (a) all required kicad-happy skills are available at pipeline start (infrastructure check passes per Story 5.3), AND (b) the user does not explicitly abandon the run. Infrastructure failures and user abandonment are excluded from both numerator and denominator. Root cause categorization (pipeline logic failure, infrastructure failure, domain failure, user abandonment) logged per failed run. |

---

## 7. Out of Scope

> "Many features that are requested deserve to be deprioritized. And some that are deprioritized deserve to ship. Can you give that judgment?"

The following items are explicitly NOT in scope for this GREENFIELD plugin:

1. **Replacing kicad-happy skills** -- The hardware-team plugin CONSUMES kicad-happy as a dependency. It does NOT reimplement component search, BOM parsing, EMC analysis, SPICE simulation, or any existing kicad-happy capability.
2. **3D CAD integration** -- Mechanical design tools (FreeCAD, SolidWorks, Fusion 360) are out of scope. Enclosure design guidance is text-based, not CAD-integrated.
3. **Physical lab automation** -- The plugin does not control test equipment, lab instruments, or manufacturing machinery. It produces documentation and guidance that humans execute in the physical world. Physical stages (Prototype, Pilot Run, Production Release) follow a gate-in/human-action/gate-out pattern. [C3]
4. **Supply chain management software** -- No ERP integration, no purchase order generation, no inventory tracking beyond BOM-level component data.
5. **Actual compliance certification** -- The plugin performs pre-compliance analysis and documentation preparation. It does not submit to or interact with certification bodies.
6. **Firmware development pipeline** -- Firmware engineering is deferred to Phase 2. Full firmware CI/CD is handled by the existing software `delivery-team/` plugin. Phase 1 provides firmware interface documentation via the EE role. [C4]
7. **Multi-board system design** -- Initial scope is single-board designs. System-level design with multiple interconnected PCBs, backplanes, or flex-rigid assemblies is deferred.
8. **Companion plugins** -- The simulation-plugin, supply-chain-plugin, and compliance-plugin are separate future marketplace entries, not part of this GREENFIELD.
9. **Modifying delivery-team plugin** -- hardware-team is a parallel plugin, not an extension of delivery-team.
10. **Universal engineering** -- Scope is hardware product development (electronics/PCB), not civil/structural/chemical/aerospace engineering.
11. **Mechanical Engineer role** -- Deferred to Phase 2 (Epic 6) per risk mitigation for scope.
12. **Firmware Engineer role** -- Deferred to Phase 2 (Epic 6) per risk mitigation for scope.
13. **Dynamic pipeline adaptation per project type** -- P2 scope (FR-021). P1 reads static config values only. [C7]

---

## 8. Dependencies

| # | Dependency | Type | Owner | Status | Impact if Unresolved |
|---|-----------|------|-------|--------|----------------------|
| D-001 | kicad-happy skills installed via Claude Code plugin system (external dependency, installed at `~/.claude/plugins/cache/kicad-happy/`) | Technical | User environment | **VERIFIED** -- kicad-happy installed at `C:\Users\micha\.claude\plugins\cache\kicad-happy\kicad-happy\1.2.0\`; SessionStart hook (Story 5.3) will verify at runtime [C2] | High -- integration layer cannot dispatch without installed skills; SessionStart hook provides early warning with installation instructions |
| D-002 | Claude Code plugin system supports cross-plugin skill invocation | Platform | Anthropic | **VERIFIED** -- live test confirmed `kicad-happy:kicad` loads successfully via Skill tool from separate plugin context [C1, C10] | ~~High~~ Resolved -- cross-plugin invocation confirmed working |
| D-003 | `marketplace.json` schema supports multiple delivery-style plugins | Registry | Plugin ecosystem | **Confirmed** -- delivery-team and other plugins coexist | Low -- naming convention avoids conflicts |
| D-004 | Python 3.x available on target systems (standard library only) | Runtime | User environment | **Confirmed** -- required by existing plugins | Low -- no new runtime requirements |
| D-005 | KiCad project files (.kicad_pro, .kicad_sch, .kicad_pcb) accessible on local filesystem | User environment | User | **Confirmed** -- same assumption as kicad-happy | Medium -- pipeline cannot analyze designs without project files |
| D-006 | Agent tool available for sub-agent dispatch | Platform | Anthropic | **Confirmed** -- used by delivery-team | Low -- proven pattern |
| D-007 | delivery-flow architecture patterns documented and stable (pipeline, gates, DoD, memory) | Knowledge | delivery-team plugin | **Confirmed** -- v2.7 config schema, stable architecture | Low -- patterns are well-documented in existing codebase |

---

## 9. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R-001 | kicad-happy not installed in user environment -- users attempt to use hardware-team without kicad-happy | Medium | High | SessionStart hook (Story 5.3) verifies all 11 kicad-happy skills at session start with clear installation instructions; config tracks minimum compatible version (Story 3.6) [C2] |
| R-002 | Hardware domain breadth exceeds manageable skill count for initial release | Medium | Medium | Start with 6 roles (defer Mechanical and Firmware to Phase 2); apply MoSCoW to role capabilities within each skill |
| R-003 | Model limitations on spatial/geometric reasoning (issue #76 learning: Haiku too weak) | High | Medium | Document minimum model tier per role in each SKILL.md; Layout and Compliance roles require Sonnet+; add model tier validation to pipeline start |
| R-004 | Pipeline stages too rigid for iterative hardware development | Medium | High | Design explicit rework loops (Story 1.7) with 6 defined rework paths; pipeline is a DAG with controlled backward edges, not strictly linear; rework termination conditions prevent infinite loops [C8] |
| R-005 | ~~Cross-plugin skill invocation not supported by platform~~ | ~~Medium~~ | ~~High~~ | **RETIRED** -- cross-plugin invocation verified working via live test. kicad-happy:kicad loads successfully from separate plugin context. [C1, C10] |
| R-006 | Gate validation produces false positives that slow the pipeline | Medium | Medium | Tune gate thresholds based on self-learning memory; allow config-based gate strictness levels (strict, standard, relaxed) |
| R-007 | Schematic Review Gate's iterative multi-reviewer pattern is too slow for complex schematics | Medium | Medium | Default to 2 review passes; make pass count configurable; apply deduplication aggressively to reduce redundant findings |
| R-008 | Config schema evolution creates backward compatibility issues | Low | Medium | Implement forward-compatible schema (missing keys use defaults, unknown keys ignored); version field enables migration guidance |
| R-009 | kicad-happy version incompatibility -- kicad-happy updates skill interfaces breaking hardware-team dispatch patterns | Medium | High | Config tracks `dependencies.kicad_happy_version` for minimum compatible version; SessionStart hook warns on version mismatch; integration layer architecture documents expected input/output contracts per skill [C2] |
| R-010 | Rework loops consume excessive context window and session time | Medium | Medium | Rework termination conditions (max 3 per path, max 10 total per run) with human escalation prevent unbounded loops [C8] |

---

## 10. Assumptions

1. ~~The `kicad-happy/` plugin skills are consumable as sub-agents from other plugins (cross-plugin skill invocation is supported by the Claude Code plugin system)~~ **VERIFIED** -- cross-plugin skill invocation confirmed working via live test. kicad-happy:kicad loads successfully from `C:\Users\micha\.claude\plugins\cache\kicad-happy\kicad-happy\1.2.0\`. [C1]
2. The hardware pipeline can follow the same orchestrator pattern as delivery-flow (Agent tool dispatch to role-scoped sub-agents with context isolation)
3. Hardware project files (KiCad schematics, PCB layouts, Gerbers) exist on the local filesystem and are accessible to Claude Code tools
4. Python scripts with no external dependency management are sufficient for hardware validation scripts (DRC parsing, BOM validation, config validation)
5. The marketplace registry supports multiple delivery-style plugins without naming conflicts
6. Single-board PCB designs are the dominant use case for the initial release (multi-board deferred)
7. Users have a target fabrication house in mind when starting the pipeline (config-driven DFM)
8. The 6 rework paths defined in Story 1.7 cover >90% of real-world hardware development iteration patterns
9. The issue #76 learnings (forced-find prompting, deduplication, model tiering) are transferable from PCB review to the broader hardware pipeline
10. The `.hardware/` namespace (not `.delivery/`) is appropriate for hardware-team state and config (avoids collision with delivery-team; to be confirmed by Architect)
11. kicad-happy is installed as a separate plugin via the Claude Code plugin system and is NOT expected to exist in this repository [C2]
12. Rework loops are bounded -- hardware development iteration, while normal, terminates after a reasonable number of attempts before requiring human intervention [C8]

---

## 11. Open Questions

| # | Question | Owner | Due | Impact Assessment |
|---|----------|-------|-----|-------------------|
| OQ-001 | ~~Where is kicad-happy installed?~~ **RESOLVED** -- kicad-happy is installed via Claude Code plugin system at `~/.claude/plugins/cache/kicad-happy/kicad-happy/1.2.0/`. [C1, C2] | ~~Architect~~ | ~~Design stage~~ | **Resolved** |
| OQ-002 | Should the hardware-team plugin use `.hardware/` namespace or share `.delivery/` namespace for config and state? | Architect | Design stage | **Medium** -- Affects config schema, state management, and memory infrastructure. Using `.hardware/` avoids collision with delivery-team but means parallel infrastructure. Sharing `.delivery/` means shared memory but potential config conflicts. Current assumption: `.hardware/` (separate). |
| OQ-003 | What is the minimum model tier for each hardware role? Issue #76 found Haiku insufficient for geometry reasoning. Should the plugin enforce model requirements or only document them? | Architect | Design stage | **Medium** -- Affects cost (Sonnet vs. Opus), capability, and user experience. Enforcement requires model tier detection at pipeline start. Documentation-only is simpler but risks degraded output quality. |
| OQ-004 | How should the pipeline handle rework loops -- linear with explicit rework stages, or non-linear DAG? | Architect | Architect stage | **High** -- Fundamental pipeline architecture decision. Current assumption: DAG with controlled backward edges (6 defined rework paths) with termination conditions (C8). Alternative: linear-only with "rework" as a special stage type. Architect must produce an ADR for this. |
| OQ-005 | Are companion plugins (simulation, supply-chain, compliance) phase 2 of THIS plugin or separate marketplace entries? | PO | Refine stage | **Medium** -- Affects marketplace strategy and plugin boundaries. Current decision: separate marketplace entries (documented in Out of Scope). This can be revisited when Phase 1 is complete. |
| OQ-006 | Should the hardware-team reuse delivery-team's self-learning memory infrastructure (`.delivery/memory/`) or maintain its own? | Architect | Design stage | **Low** -- Implementation detail. Sharing memory enables cross-plugin learning. Separate memory ensures isolation. Tied to OQ-002 (namespace decision). |
| OQ-007 | Should firmware be a first-class role in the hardware plugin (Phase 2) or delegated entirely to the software delivery-team? | PO | Refine stage | **Medium** -- The firmware-hardware interface is a critical handoff point. Current decision: deferred to Phase 2 as a hardware-team role (not delegated to delivery-team), because the hardware-firmware interface needs hardware context. Phase 1 provides firmware interface documentation via the EE role (C4). |

---

## 12. Timeline & Milestones

| Milestone | Target | Exit Criteria |
|-----------|--------|---------------|
| M1: Plugin skeleton + pipeline orchestrator | Sprint 1 | Epic 1 (Stories 1.1-1.4, 1.7, 1.8) complete; pipeline executes 8 stages with gates for a reference project; rework termination conditions implemented [C8] |
| M2: Core roles implemented | Sprint 2 | Epic 2 (Stories 2.1-2.6) complete; all 6 roles produce artifacts within their stage; EE produces firmware interface documentation [C4] |
| M3: kicad-happy integration + dependency management | Sprint 2-3 | Epic 3 (Stories 3.1-3.6) complete; all 11 kicad-happy skills mapped and consumable; dependency documentation and version compatibility in place [C2] |
| M4: Test fixtures + validation gates operational | Sprint 3 | Story 4.0 complete (reference test fixtures); Epic 4 (Stories 4.1-4.5) complete; all 5 gates enforce quality with >80% defect detection measured against test fixtures [C5] |
| M5: Collaboration patterns + hooks | Sprint 3-4 | Epic 5 (Stories 5.1-5.5) complete; Design Review Board executes; hooks fire on events; kicad-happy availability check operational [C2] |
| M6: State persistence + memory | Sprint 4 | Stories 1.5, 1.6 complete; pipeline resumes across sessions; memory accumulates lessons |
| M7: End-to-end validation | Sprint 4 | Full pipeline run on reference KiCad project; all success metrics measured against reference test fixtures; plugin-validator passes; North Star metric calculated with qualifying run definition [C9] |

---

## 13. MoSCoW Prioritization Summary

### Must Have (P1) -- 60% of scope
- Plugin skeleton and marketplace registration (FR-001)
- 8-stage pipeline orchestrator with AI/human stage classification (FR-002) [C3]
- Stage gate validation framework with team DoD (FR-003)
- Config-driven pipeline -- static reading (FR-004) [C7]
- Rework loop support with termination conditions (FR-007) [C8]
- 6 core role skills with context isolation, EE firmware interface docs (FR-008) [C4]
- kicad-happy integration layer (FR-009)
- All 5 validation gates (FR-010 through FR-014)
- Design Review Board collaboration pattern (FR-015)
- Config & dependency validation hook (FR-017) [C2]
- Sub-agent dispatch guardrail (FR-020)
- Reference test fixture (FR-022) [C5]
- kicad-happy dependency documentation & verification (Story 3.6) [C2]

### Should Have (P2) -- 20% of scope
- Pipeline state persistence and resume (FR-005)
- Self-learning memory (FR-006)
- BOM Reconciliation pattern (FR-016)
- Schematic DRC hook (FR-018)
- BOM drift detection hook (FR-019)
- Project type auto-detection with dynamic pipeline adaptation (FR-021) [C7]

### Could Have (P3) -- 15% of scope
- Mechanical Engineer role (Phase 2)
- Firmware Engineer role (Phase 2)
- Gate strictness levels in config (relaxed/standard/strict)
- Pipeline analytics dashboard

### Won't Have (this release) -- 5%
- Companion plugins (simulation, supply-chain, compliance)
- 3D CAD integration
- Multi-board system design
- Physical lab automation

---

> "A product owner is never late, nor early. They prioritize precisely when they mean to."

This PRD has been revised to address all 5 BLOCKING and 5 ADVISORY challenges from the adversarial review. The cross-plugin invocation foundation is verified. The path forward is clear. The fellowship may proceed to Design.
