# User Stories: hardware-team Plugin

**Author:** Product Owner (Gandalf)
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12
**PRD Version:** 1.1 (Revised)
**Architecture Version:** 1.4

---

> "All we have to decide is what to build with the time that is given to us. And I decide we build these stories in the order that the fellowship requires -- foundations first, then the roles, then the gates, then the bindings that hold them together."

---

## Capacity Declaration

**Velocity baseline:** Not yet established (GREENFIELD -- first pipeline run)
**Sprint capacity:** 80% utilization ceiling applied to all sprint plans
**Estimation calibration:** This plugin is primarily Markdown files (SKILL.md, references/*.md) and Python scripts (hooks, config validation, state management). Per memory lesson, markdown-heavy work is estimated one tier lower than code-heavy work. Estimates below reflect this calibration.

**Estimate key:**
- **S (Small):** 1-2 story points. Pure markdown creation, single-file edits, registration tasks.
- **M (Medium):** 3-5 story points. Multiple markdown files with cross-references, simple Python scripts, config schemas.
- **L (Large):** 5-8 story points. Complex orchestration logic, multi-file Python scripts, integration patterns with multiple touchpoints.
- **XL (Extra Large):** 8-13 story points. Pipeline orchestrator, gate frameworks with multiple validators, iterative review patterns.

---

## FR Traceability Matrix

| FR | Story(s) | Covered |
|----|----------|---------|
| FR-001 | US-101, US-108 | Yes |
| FR-002 | US-102 | Yes |
| FR-003 | US-103 | Yes |
| FR-004 | US-104 | Yes |
| FR-005 | US-105 | Yes |
| FR-006 | US-106 | Yes |
| FR-007 | US-107 | Yes |
| FR-008 | US-201, US-202, US-203, US-204, US-205, US-206 | Yes |
| FR-009 | US-301 | Yes |
| FR-010 | US-401 | Yes |
| FR-011 | US-402 | Yes |
| FR-012 | US-403 | Yes |
| FR-013 | US-404 | Yes |
| FR-014 | US-405 | Yes |
| FR-015 | US-501 | Yes |
| FR-016 | US-502 | Yes |
| FR-017 | US-503 | Yes |
| FR-018 | US-504 | Yes |
| FR-019 | US-505 | Yes |
| FR-020 | US-102 (AC explicitly requires Agent tool dispatch) | Yes |
| FR-021 | Deferred to Phase 2 (P2) -- noted in US-104 | Yes |
| FR-022 | US-400 | Yes |

All 22 FRs are mapped. No orphans.

---

## Epic 1: Plugin Foundation & Pipeline Orchestrator

> "Even the smallest plugin, if well-structured, can change the course of a hardware project."

**Epic Goal:** Establish the hardware-team plugin skeleton and 8-stage pipeline orchestrator that coordinates hardware development from concept to production release.

---

### US-101: Plugin Skeleton Creation
**Epic**: Plugin Foundation & Pipeline Orchestrator
**Priority**: P1
**Estimate**: S (2 pts) -- primarily directory creation and markdown templates
**As a** plugin developer, **I want** the `hardware-team/` directory created with the standard plugin structure (SKILL.md, skills/, references/, hooks/, scripts/, LICENSE.txt), **so that** the plugin follows CLAUDE.md conventions and is discoverable by the Claude Code harness.

**Acceptance Criteria**:
- [ ] Given the `hardware-team/` directory does not exist, when the plugin skeleton is created, then the directory structure matches the architecture's Section 1.1 layout: top-level SKILL.md, LICENSE.txt, hooks/, scripts/, skills/ (with 7 sub-skill directories), references/ (with test-fixtures/)
- [ ] Given the SKILL.md is created, when it is loaded by the Claude Code harness, then it contains metadata (name, description, license) and three-level context loading instructions per architecture Section 4
- [ ] Given the plugin skeleton exists, when `marketplace.json` is checked, then hardware-team is NOT yet registered (registration is US-108)
- [ ] Given the skills/ directory is created, when inspected, then it contains exactly 7 sub-directories: hardware-flow/, hw-product-owner/, electrical-engineer/, pcb-layout-engineer/, manufacturing-engineer/, compliance-engineer/, test-engineer/ -- each with a placeholder SKILL.md

**Test Cases** (placeholder -- QA will expand):
- TC-101-01: Verify directory structure matches architecture Section 1.1
- TC-101-02: Verify SKILL.md loads without error in Claude Code harness
- TC-101-03: Verify marketplace.json does NOT contain hardware-team entry yet

**Dependencies**: none

---

### US-102: Pipeline Orchestrator with 8 Stages
**Epic**: Plugin Foundation & Pipeline Orchestrator
**Priority**: P1
**Estimate**: L (8 pts) -- complex orchestration SKILL.md with stage definitions, dispatch patterns, and multiple reference documents
**As a** hardware developer (Elena), **I want** a pipeline orchestrator that guides my project through 8 hardware development stages (Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release), **so that** I follow a structured process instead of ad-hoc development.

**Acceptance Criteria**:
- [ ] Given a new hardware project, when the pipeline starts, then Stage 1 (Concept) is executed first
- [ ] Given a stage completes and passes its gate, when the pipeline advances, then the next stage in sequence is activated
- [ ] Given all 8 stages exist, when the pipeline is inspected, then each stage has: defined purpose, key activities list, required role(s), execution mode (AI or human), and applicable gates per architecture Section 3.1
- [ ] Given the orchestrator dispatches work, when a stage is executed, then it is dispatched as a sub-agent via the Agent tool (NOT inlined -- FR-020 guardrail)
- [ ] Given the pipeline runs, when stage transitions occur, then each transition is logged with timestamp and gate result
- [ ] Given stages are classified by execution mode, when inspected, then AI-execution stages (Concept, Schematic, Layout, DFM/DFA, Compliance) execute autonomously, and human-execution stages (Prototype, Pilot Run, Production Release) follow gate-in/human-action/gate-out pattern per architecture Section 3.4
- [ ] Given the orchestrator SKILL.md exists at `hardware-team/skills/hardware-flow/SKILL.md`, when loaded, then it contains: stage definitions, dispatch patterns, and explicit "Prime Directive" guardrail (orchestrator NEVER produces domain artifacts directly)
- [ ] Given the references/ directory for hardware-flow exists, when inspected, then it contains: pipeline-stages.md, config-schema.md, rework-paths.md, gate-framework.md, memory-protocol.md, kicad-integration.md, setup-wizard.md per architecture Section 1.1
- [ ] Given sub-agent dispatch fails, when the orchestrator handles the error, then it follows the dispatch failure protocol: detect, retry once, pause with error classification per architecture Section 3.1.1

**Test Cases** (placeholder -- QA will expand):
- TC-102-01: Verify pipeline starts at Stage 1 (Concept)
- TC-102-02: Verify stage dispatch uses Agent tool (not inlined)
- TC-102-03: Verify human-execution stages pause for human confirmation
- TC-102-04: Verify dispatch failure triggers retry then pause with error classification
- TC-102-05: Verify all 8 stages have defined purpose, activities, roles, execution mode

**Dependencies**: US-101

---

### US-103: Stage Gate Validation Framework
**Epic**: Plugin Foundation & Pipeline Orchestrator
**Priority**: P1
**Estimate**: L (8 pts) -- gate framework reference document plus validation patterns, hardware-specific DoD criteria
**As a** hardware team lead (Marcus), **I want** validation gates between pipeline stages that enforce quality checks before advancing, **so that** defects are caught at design time rather than after prototype fabrication.

**Acceptance Criteria**:
- [ ] Given the gate framework exists, when a stage completes, then the gate evaluates all required validators for that stage
- [ ] Given a gate has multiple validators, when ALL validators report DONE, then the gate passes and the pipeline advances
- [ ] Given ANY validator reports NOT_DONE, when the gate evaluates, then the pipeline does not advance and the failing validator's feedback is returned to the stage for correction
- [ ] Given gate validators are defined, when they are inspected, then each has: unique ID, description, pass/fail criteria, and the role responsible for evaluation
- [ ] Given the Team DoD pattern from delivery-flow, when applied to hardware, then hardware-specific DoD criteria replace software-specific criteria (e.g., "DRC passes" instead of "unit tests pass")
- [ ] Given the gate framework reference exists at `hardware-team/skills/hardware-flow/references/gate-framework.md`, when loaded, then it documents all 5 gate types: Schematic Review, DRC, BOM, DFM, Compliance, plus the Human Confirmation Gate pattern

**Test Cases** (placeholder -- QA will expand):
- TC-103-01: Verify gate with 3 validators blocks when 1 reports NOT_DONE
- TC-103-02: Verify gate passes when ALL validators report DONE
- TC-103-03: Verify failing validator feedback is returned to stage
- TC-103-04: Verify each gate validator has unique ID, description, pass/fail criteria

**Dependencies**: US-102

---

### US-104: Config-Driven Pipeline (.hardware/config.yml)
**Epic**: Plugin Foundation & Pipeline Orchestrator
**Priority**: P1
**Estimate**: M (5 pts) -- config schema document (markdown) + Python validation script
**As a** hardware developer (Elena), **I want** to configure my project settings (target fab house, compliance regions, BOM budget, production volume targets) in a `.hardware/config.yml` file, **so that** the pipeline adapts to my specific project constraints.

**Acceptance Criteria**:
- [ ] Given a `.hardware/config.yml` file exists in the project root, when the pipeline starts, then it loads and validates the config against the schema
- [ ] Given the config specifies `target_fab: jlcpcb`, when DFM validation runs, then it reads the config value and passes it to the DFM gate for fab-specific rule selection (P1: static reading only; P2: dynamic adaptation per FR-021)
- [ ] Given the config specifies `compliance_regions: [FCC, CE]`, when the Compliance stage runs, then it reads the config value and evaluates requirements for the specified regions
- [ ] Given no `.hardware/config.yml` exists, when the pipeline starts, then it uses sensible defaults and logs "No project config found, using defaults"
- [ ] Given an invalid config file, when validation runs, then it warns about invalid fields and uses defaults for those fields (never fails the pipeline due to config errors)
- [ ] Given the config schema, when inspected, then it has a version field and follows the extension protocol pattern from delivery-flow's config-schema.md
- [ ] Given the config schema, when inspected, then it includes a `dependencies` section with `kicad_happy_version` field for version compatibility tracking
- [ ] Given the config schema, when inspected, then it includes rework termination fields: `max_rework_iterations` (default 3, per path) and `max_total_reworks` (default 10, per pipeline run)
- [ ] Given the config schema, when inspected, then it includes staleness detection fields: `pipeline.staleness_warning_days` (default 7), `pipeline.staleness_critical_days` (default 30) per architecture Section 3.4.1
- [ ] Given the config schema reference exists at `hardware-team/skills/hardware-flow/references/config-schema.md`, when loaded, then it documents all fields, types, defaults, and validation rules
- [ ] Given the validation script exists at `hardware-team/skills/hardware-flow/scripts/validate_config.py`, when run, then it validates a config file against the schema and reports errors

**Test Cases** (placeholder -- QA will expand):
- TC-104-01: Verify config loads and validates against schema
- TC-104-02: Verify absent config uses defaults
- TC-104-03: Verify invalid config warns but does not fail pipeline
- TC-104-04: Verify config schema includes all required fields (version, target_fab, compliance_regions, bom_budget, dependencies, rework limits, staleness thresholds)

**Dependencies**: US-102

---

### US-105: Pipeline State Persistence and Resume
**Epic**: Plugin Foundation & Pipeline Orchestrator
**Priority**: P2
**Estimate**: M (5 pts) -- state manager Python script + state file format document
**As a** hardware developer (Elena), **I want** the pipeline to save its state so I can resume a hardware project across multiple sessions, **so that** I do not lose progress when a session ends.

**Acceptance Criteria**:
- [ ] Given a pipeline is in progress, when the session ends, then the current stage, gate results, and artifact paths are persisted to `.hardware/state.md`
- [ ] Given a persisted state exists, when a new session starts and the user requests to resume, then the pipeline loads the saved state and continues from the last completed stage
- [ ] Given a pipeline has completed stages 1-4, when resumed, then stages 1-4 are not re-executed and their artifacts are available to subsequent stages
- [ ] Given the state manager script exists at `hardware-team/scripts/state_manager.py`, when invoked, then it reads/writes pipeline state to `.hardware/state.md` with fields per architecture Section 3.1.1 (stage, gate results, dispatch errors, rework history, timestamps)
- [ ] Given a paused pipeline state exists, when SessionStart hook fires, then it displays paused status with staleness detection per architecture Section 3.4.1

**Test Cases** (placeholder -- QA will expand):
- TC-105-01: Verify state persists on session end
- TC-105-02: Verify resume loads saved state and continues from last completed stage
- TC-105-03: Verify staleness warning at 7+ days paused
- TC-105-04: Verify critical staleness warning at 30+ days paused

**Dependencies**: US-102

---

### US-106: Self-Learning Memory
**Epic**: Plugin Foundation & Pipeline Orchestrator
**Priority**: P2
**Estimate**: M (3 pts) -- memory protocol reference document (markdown) + directory structure
**As a** hardware developer (Elena), **I want** the pipeline to learn from past project runs and apply those lessons to future runs, **so that** repeated mistakes are avoided and best practices accumulate.

**Acceptance Criteria**:
- [ ] Given a pipeline run completes, when lessons are captured, then they are stored in `.hardware/memory/` using tiered chunked retrieval (same pattern as delivery-flow)
- [ ] Given memory entries exist, when a new pipeline run starts, then relevant memories are injected into stage prompts
- [ ] Given a memory entry exists for "DFM violation: trace width below JLCPCB minimum on previous project", when the Layout stage runs, then the memory is surfaced as a caution
- [ ] Given the memory protocol reference exists at `hardware-team/skills/hardware-flow/references/memory-protocol.md`, when loaded, then it documents the tiered retrieval strategy, memory file format, and injection patterns

**Test Cases** (placeholder -- QA will expand):
- TC-106-01: Verify lessons are stored after pipeline completion
- TC-106-02: Verify relevant memories are injected into stage prompts
- TC-106-03: Verify memory retrieval completes within NFR-008 target (<2s for 100+ entries)

**Dependencies**: US-102

---

### US-107: Rework Loop Support
**Epic**: Plugin Foundation & Pipeline Orchestrator
**Priority**: P1
**Estimate**: L (8 pts) -- rework path definitions, termination logic, re-validation semantics, reference document
**As a** hardware developer (Elena), **I want** the pipeline to support rework loops (e.g., prototype failure triggers return to schematic stage) instead of only linear progression, **so that** the pipeline reflects actual hardware development where iteration between stages is normal.

**Acceptance Criteria**:
- [ ] Given a prototype stage identifies a schematic-level issue, when the rework loop triggers, then the pipeline returns to the Schematic stage with the specific issue documented as context
- [ ] Given a rework loop is triggered, when the target stage re-executes, then it has access to the original stage artifacts AND the rework reason
- [ ] Given the pipeline supports rework, when rework paths are inspected, then all 8 paths are defined per architecture Section 3.3: Prototype->Schematic, Prototype->Layout, DFM/DFA->Layout, DFM/DFA->Schematic, Compliance->Schematic, Compliance->Layout, Pilot Run->DFM/DFA, Pilot Run->Schematic
- [ ] Given a rework loop completes, when the pipeline resumes forward, then all downstream gates from the rework target are re-validated (not skipped) per architecture Section 3.3 execution semantics
- [ ] Given rework occurs, when the pipeline state is inspected, then the rework history is logged with: trigger reason, source stage, target stage, resolution, iteration count for that path, total rework count
- [ ] Given a rework path has been triggered N times (configurable via `max_rework_iterations`, default 3), when it triggers again, then the pipeline PAUSES and escalates to the human with: rework history for that path, recurring failure pattern, and recommendation to intervene manually
- [ ] Given the total rework count across ALL paths reaches `max_total_reworks` (default 10), when any rework triggers, then the pipeline PAUSES and escalates with full rework history, pattern summary, and human decision options (continue, abort, override limit)
- [ ] Given the rework paths reference exists at `hardware-team/skills/hardware-flow/references/rework-paths.md`, when loaded, then it documents all 8 rework paths, termination conditions, escalation protocol, and execution semantics

**Test Cases** (placeholder -- QA will expand):
- TC-107-01: Verify rework from Prototype->Schematic passes rework reason as context
- TC-107-02: Verify downstream gates re-validate after rework
- TC-107-03: Verify per-path rework limit (default 3) triggers escalation
- TC-107-04: Verify total rework limit (default 10) triggers escalation
- TC-107-05: Verify rework history is logged with all required fields

**Dependencies**: US-102, US-103

---

### US-108: Marketplace Registration
**Epic**: Plugin Foundation & Pipeline Orchestrator
**Priority**: P1
**Estimate**: S (1 pt) -- single JSON entry in marketplace.json
**As a** plugin marketplace user, **I want** the hardware-team plugin to be registered in `marketplace.json` with a unique ID, display name, and description, **so that** it is discoverable alongside other plugins.

**Acceptance Criteria**:
- [ ] Given the plugin skeleton exists, when `marketplace.json` is updated, then it contains an entry with unique ID `hardware-team`, display name, description, and 7 skill paths per architecture Section 4 (Level 1 metadata)
- [ ] Given the marketplace entry exists, when validated against other entries, then there are no ID conflicts with existing plugins
- [ ] Given the marketplace entry, when inspected, then the description clearly states the plugin's purpose and its relationship to kicad-happy skills (external dependency)

**Test Cases** (placeholder -- QA will expand):
- TC-108-01: Verify marketplace.json contains hardware-team entry
- TC-108-02: Verify no ID conflicts with existing plugins
- TC-108-03: Verify description mentions kicad-happy dependency

**Dependencies**: US-101

---

## Epic 2: Core Hardware Roles (Phase 1)

> "Six there shall be, each with their own wisdom, each bound to their own domain. An Electrical Engineer is never late, nor early -- they review the schematic precisely when they mean to."

**Epic Goal:** Implement the 6 first-class hardware roles as context-isolated skills with three-level loading.

---

### US-201: Hardware Product Owner Skill
**Epic**: Core Hardware Roles
**Priority**: P1
**Estimate**: M (3 pts) -- SKILL.md + 3 reference documents (all markdown)
**As a** hardware team lead (Marcus), **I want** a Hardware Product Owner role that manages requirements, trade-offs, schedule, and stakeholder communication for hardware projects, **so that** hardware development has the same product discipline as software delivery.

**Acceptance Criteria**:
- [ ] Given the HW PO skill exists at `hardware-team/skills/hw-product-owner/SKILL.md`, when loaded, then it contains role-specific references for hardware requirements capture, feasibility analysis, make-vs-buy decisions, and BOM budgeting
- [ ] Given a Concept stage task, when the HW PO is invoked, then it produces: requirements document, constraint matrix, regulatory landscape scan, and initial BOM budget
- [ ] Given the skill is loaded, when it executes, then it loads ONLY HW PO references (zero cross-role context bleed -- NFR-002)
- [ ] Given the HW PO interacts with other roles, when trade-off decisions are needed, then it documents the decision rationale using the decision record pattern
- [ ] Given the references/ directory contains 3 files (hw-requirements.md, feasibility-analysis.md, make-vs-buy.md), when loaded, then each provides domain-specific guidance per architecture Section 1.1
- [ ] Given the SKILL.md, when inspected, then it specifies minimum model tier per NFR-007

**Test Cases** (placeholder -- QA will expand):
- TC-201-01: Verify SKILL.md loads only HW PO references
- TC-201-02: Verify Concept stage produces requirements, constraint matrix, regulatory scan, BOM budget
- TC-201-03: Verify model tier is specified in SKILL.md

**Dependencies**: US-101

---

### US-202: Electrical Engineer Skill
**Epic**: Core Hardware Roles
**Priority**: P1
**Estimate**: M (5 pts) -- SKILL.md + 5 reference documents (markdown) + kicad-happy invocation patterns + firmware interface template
**As a** hardware developer (Elena), **I want** an Electrical Engineer role that handles schematic design, component selection, simulation, and signal integrity analysis, **so that** electrical design follows structured review practices.

**Acceptance Criteria**:
- [ ] Given the EE skill exists at `hardware-team/skills/electrical-engineer/SKILL.md`, when loaded, then it contains references for schematic design, component selection criteria, simulation methodology, power tree analysis, and firmware interface documentation
- [ ] Given a Schematic stage task, when the EE is invoked, then it produces: schematic review artifacts, component selection rationale, and simulation results
- [ ] Given the EE needs to select components, when it performs component search, then it CONSUMES `kicad-happy:digikey`, `kicad-happy:mouser`, `kicad-happy:lcsc`, and `kicad-happy:element14` skills (does NOT reimplement search -- NFR-003)
- [ ] Given the EE needs to run simulations, when it performs SPICE analysis, then it CONSUMES `kicad-happy:spice` (does NOT reimplement simulation)
- [ ] Given the EE reviews a schematic, when the iterative review pattern (from issue #76) is applied, then the review uses forced-find prompting and deduplication across multiple review passes
- [ ] Given the EE is in the Schematic stage, when schematic design is complete, then the EE produces firmware interface documentation: pin assignment table, power domain map, communication bus interface spec (I2C/SPI/UART address map, clock rates, voltage levels), and debug interface access points (FR-008, C4 resolution)
- [ ] Given the references/ directory contains 5 files (schematic-review.md, component-selection.md, simulation-guide.md, power-analysis.md, firmware-interface.md), when loaded, then each provides domain-specific guidance per architecture Section 1.1
- [ ] Given the SKILL.md, when inspected, then it specifies minimum model tier (Sonnet+ for geometry reasoning per R-003)

**Test Cases** (placeholder -- QA will expand):
- TC-202-01: Verify SKILL.md loads only EE references
- TC-202-02: Verify component search consumes kicad-happy skills (not reimplemented)
- TC-202-03: Verify firmware interface documentation is produced during Schematic stage
- TC-202-04: Verify iterative review uses forced-find prompting
- TC-202-05: Verify model tier is specified as Sonnet+

**Dependencies**: US-101

---

### US-203: PCB Layout Engineer Skill
**Epic**: Core Hardware Roles
**Priority**: P1
**Estimate**: M (5 pts) -- SKILL.md + 3 reference documents (markdown) + kicad-happy invocation patterns
**As a** hardware developer (Elena), **I want** a PCB Layout Engineer role that handles physical layout, routing, stackup definition, impedance control, and DRC validation, **so that** PCB layout follows structured design rules.

**Acceptance Criteria**:
- [ ] Given the Layout skill exists at `hardware-team/skills/pcb-layout-engineer/SKILL.md`, when loaded, then it contains references for layout best practices, routing guidelines, stackup design, and impedance control
- [ ] Given a Layout stage task, when the Layout Engineer is invoked, then it produces: layout review artifacts, routing analysis, and DRC results
- [ ] Given the Layout Engineer needs to analyze a KiCad PCB, when it performs analysis, then it CONSUMES `kicad-happy:kicad` (does NOT reimplement KiCad analysis -- NFR-003)
- [ ] Given the Layout Engineer operates on spatial/geometric reasoning tasks, when the skill's SKILL.md is inspected, then it documents a minimum model tier requirement of Sonnet+ (per issue #76 learning: Haiku is insufficient for geometry reasoning)
- [ ] Given the references/ directory contains 3 files (layout-guidelines.md, routing-rules.md, stackup-design.md), when loaded, then each provides domain-specific guidance

**Test Cases** (placeholder -- QA will expand):
- TC-203-01: Verify SKILL.md loads only PCB Layout references
- TC-203-02: Verify KiCad analysis consumes kicad-happy:kicad (not reimplemented)
- TC-203-03: Verify model tier is specified as Sonnet+

**Dependencies**: US-101

---

### US-204: Manufacturing Engineer Skill
**Epic**: Core Hardware Roles
**Priority**: P1
**Estimate**: M (3 pts) -- SKILL.md + 4 reference documents (markdown) + kicad-happy invocation patterns
**As a** manufacturing engineer (Wei), **I want** a Manufacturing Engineer role that handles DFM/DFA review, assembly process guidance, yield optimization, and production transfer, **so that** designs are manufacturable before they reach the fab house.

**Acceptance Criteria**:
- [ ] Given the MfgE skill exists at `hardware-team/skills/manufacturing-engineer/SKILL.md`, when loaded, then it contains references for DFM rules, DFA guidelines, panelization, and test point coverage requirements
- [ ] Given a DFM/DFA stage task, when the MfgE is invoked, then it produces: DFM review report, DFA review report, yield risk assessment, and remediation guidance
- [ ] Given the MfgE needs fab-specific rules, when it evaluates DFM, then it CONSUMES `kicad-happy:jlcpcb` and `kicad-happy:pcbway` for fab-house-specific design rules (NFR-003)
- [ ] Given the MfgE needs BOM data, when it evaluates component availability, then it CONSUMES `kicad-happy:bom` for BOM validation (NFR-003)
- [ ] Given the MfgE reviews a design, when the DFM gate evaluates, then it checks: minimum trace/space, via sizes, layer count compatibility, surface finish compatibility, and component footprint availability at the target CM
- [ ] Given the references/ directory contains 4 files (dfm-rules.md, dfa-guidelines.md, panelization.md, test-point-coverage.md), when loaded, then each provides domain-specific guidance

**Test Cases** (placeholder -- QA will expand):
- TC-204-01: Verify SKILL.md loads only MfgE references
- TC-204-02: Verify DFM evaluation consumes kicad-happy fab skills (not reimplemented)
- TC-204-03: Verify DFM gate checks all required categories

**Dependencies**: US-101

---

### US-205: Compliance Engineer Skill
**Epic**: Core Hardware Roles
**Priority**: P1
**Estimate**: M (3 pts) -- SKILL.md + 4 reference documents (markdown) + kicad-happy invocation patterns
**As a** compliance specialist (David), **I want** a Compliance Engineer role that handles EMC pre-compliance, safety analysis, environmental compliance, and regulatory documentation, **so that** designs are compliance-ready before engaging test labs.

**Acceptance Criteria**:
- [ ] Given the CompE skill exists at `hardware-team/skills/compliance-engineer/SKILL.md`, when loaded, then it contains references for EMC design rules, safety standards (IEC 62368-1, IEC 60950), environmental regulations (RoHS, REACH, WEEE), and market-specific requirements (FCC Part 15, CE RED, UL)
- [ ] Given a Compliance stage task, when the CompE is invoked, then it produces: EMC pre-compliance report, safety analysis, environmental compliance checklist, and test lab preparation package
- [ ] Given the CompE needs EMC analysis, when it performs pre-compliance checks, then it CONSUMES `kicad-happy:emc` (does NOT reimplement EMC analysis -- NFR-003)
- [ ] Given the CompE needs documentation, when it generates regulatory packages, then it CONSUMES `kicad-happy:kidoc` (does NOT reimplement documentation generation -- NFR-003)
- [ ] Given the config specifies `compliance_regions: [FCC, CE]`, when the compliance gate evaluates, then it produces a checklist with evidence-linked requirements for EACH specified region
- [ ] Given the references/ directory contains 4 files (emc-design-rules.md, safety-standards.md, environmental.md, market-requirements.md), when loaded, then each provides domain-specific guidance

**Test Cases** (placeholder -- QA will expand):
- TC-205-01: Verify SKILL.md loads only CompE references
- TC-205-02: Verify EMC analysis consumes kicad-happy:emc (not reimplemented)
- TC-205-03: Verify compliance checklist covers all configured regions

**Dependencies**: US-101

---

### US-206: Test Engineer Skill
**Epic**: Core Hardware Roles
**Priority**: P1
**Estimate**: M (3 pts) -- SKILL.md + 4 reference documents (markdown)
**As a** hardware team lead (Marcus), **I want** a Test Engineer role that handles test strategy, test fixture design, production test development, and validation planning, **so that** hardware is testable and test coverage is planned from the start.

**Acceptance Criteria**:
- [ ] Given the TestE skill exists at `hardware-team/skills/test-engineer/SKILL.md`, when loaded, then it contains references for test strategy frameworks, test fixture design patterns, production test methodologies, and validation planning
- [ ] Given a Prototype stage task, when the TestE is invoked, then it produces: test strategy document, test fixture requirements, bring-up test procedure, and validation acceptance criteria
- [ ] Given the TestE plans production tests, when test point coverage is evaluated, then it cross-references the PCB layout for adequate test access
- [ ] Given the TestE produces a test strategy, when it is inspected, then it covers: functional testing, environmental testing (if applicable), reliability testing, and production screening
- [ ] Given the references/ directory contains 4 files (test-strategy.md, fixture-design.md, production-test.md, validation-planning.md), when loaded, then each provides domain-specific guidance

**Test Cases** (placeholder -- QA will expand):
- TC-206-01: Verify SKILL.md loads only TestE references
- TC-206-02: Verify test strategy covers all required testing types
- TC-206-03: Verify test point coverage cross-references PCB layout

**Dependencies**: US-101

---

## Epic 3: kicad-happy Integration Layer

> "Eleven skills to bind them. Not to forge anew, but to call upon what already exists. The wisest course is to consume, never to reimplement."

**Epic Goal:** Define and implement the interface for consuming kicad-happy skills as sub-agents within the hardware pipeline.

---

### US-301: Integration Layer Architecture
**Epic**: kicad-happy Integration Layer
**Priority**: P1
**Estimate**: L (5 pts) -- integration reference document (markdown) with dispatch patterns, role-to-skill mappings, error handling, reimplementation definition
**As a** plugin developer, **I want** a defined interface for consuming kicad-happy skills from within the hardware pipeline, **so that** the hardware-team orchestrator can dispatch to kicad-happy skills without reimplementing their functionality.

**Acceptance Criteria**:
- [ ] Given the integration layer is defined, when a hardware role needs a kicad-happy capability, then the integration layer provides a dispatch pattern (skill name, expected input, expected output) per architecture Section 2.3
- [ ] Given the integration layer exists, when it dispatches to a kicad-happy skill, then it uses cross-plugin skill invocation via the Skill tool (verified to work -- kicad-happy installed at `~/.claude/plugins/cache/kicad-happy/kicad-happy/1.2.0/`)
- [ ] Given a kicad-happy skill is unavailable (not installed), when the integration layer attempts dispatch, then it fails gracefully with a clear error message indicating which skill is missing and how to install it
- [ ] Given the integration layer maps roles to skills, when the mapping is inspected, then each kicad-happy skill is mapped to the hardware role(s) that consume it per architecture Section 2.2 (EE->6 skills, PCB Layout->1, MfgE->3, CompE->2)
- [ ] Given the integration layer architecture document, when it defines "reimplementation," then it uses the operational definition from NFR-003/C6 with IS and IS NOT examples
- [ ] Given the integration reference exists at `hardware-team/skills/hardware-flow/references/kicad-integration.md`, when loaded, then it documents all 11 kicad-happy skills with: consuming role(s), stage(s), dispatch pattern, expected input/output contract

**Test Cases** (placeholder -- QA will expand):
- TC-301-01: Verify all 11 kicad-happy skills are mapped to consuming roles
- TC-301-02: Verify dispatch uses Skill tool for cross-plugin invocation
- TC-301-03: Verify graceful failure when kicad-happy skill is unavailable
- TC-301-04: Verify reimplementation definition with IS/IS NOT examples

**Dependencies**: US-101

---

### US-302: Component Sourcing Integration
**Epic**: kicad-happy Integration Layer
**Priority**: P1
**Estimate**: M (3 pts) -- dispatch patterns for 4 sourcing skills (documented in integration reference, tested via EE skill)
**As an** electrical engineer (Elena), **I want** to search multiple component distributors (DigiKey, Mouser, LCSC, element14) through the pipeline's Electrical Engineer role, **so that** component selection is part of the structured design process rather than a separate ad-hoc step.

**Acceptance Criteria**:
- [ ] Given the EE role is in the Schematic stage, when component selection is needed, then the EE can invoke `kicad-happy:digikey`, `kicad-happy:mouser`, `kicad-happy:lcsc`, or `kicad-happy:element14` via the integration layer
- [ ] Given a component search returns results from multiple distributors, when the EE evaluates options, then it considers: price, availability, lead time, lifecycle status, and second-source availability
- [ ] Given the integration layer dispatches to a sourcing skill, when the result returns, then it includes: part number, price, stock quantity, and datasheet availability

**Test Cases** (placeholder -- QA will expand):
- TC-302-01: Verify EE can invoke all 4 sourcing skills
- TC-302-02: Verify multi-distributor comparison includes price, availability, lifecycle
- TC-302-03: Verify sourcing results include part number, price, stock, datasheet

**Dependencies**: US-301

---

### US-303: Fabrication Integration
**Epic**: kicad-happy Integration Layer
**Priority**: P1
**Estimate**: M (3 pts) -- dispatch patterns for 2 fab skills (JLCPCB, PCBWay), config-driven selection
**As a** manufacturing engineer (Wei), **I want** to validate designs against specific fabrication house capabilities (JLCPCB, PCBWay) through the pipeline, **so that** DFM checks are fab-specific rather than generic.

**Acceptance Criteria**:
- [ ] Given the MfgE role is in the DFM/DFA stage, when DFM validation runs, then it invokes `kicad-happy:jlcpcb` or `kicad-happy:pcbway` based on the `target_fab` config setting
- [ ] Given JLCPCB is the target fab, when DFM rules are evaluated, then JLCPCB-specific constraints (minimum trace/space, via sizes, layer stackup options, assembly capabilities) are applied
- [ ] Given fabrication output generation is needed, when the Prototype stage runs, then Gerber, drill, and BOM/CPL files are generated consuming the appropriate kicad-happy fab skill

**Test Cases** (placeholder -- QA will expand):
- TC-303-01: Verify config-driven fab selection (JLCPCB vs PCBWay)
- TC-303-02: Verify fab-specific constraints are applied
- TC-303-03: Verify Gerber generation consumes kicad-happy fab skill

**Dependencies**: US-301

---

### US-304: Analysis Integration
**Epic**: kicad-happy Integration Layer
**Priority**: P1
**Estimate**: M (3 pts) -- dispatch patterns for 3 analysis skills (KiCad, SPICE, EMC)
**As an** electrical engineer (Elena), **I want** to run KiCad analysis, SPICE simulation, and EMC pre-compliance checks through the pipeline, **so that** design validation is part of the structured process.

**Acceptance Criteria**:
- [ ] Given the EE role is in the Schematic stage, when simulation is needed, then it invokes `kicad-happy:spice` via the integration layer
- [ ] Given the CompE role is in the Compliance stage, when EMC pre-compliance is needed, then it invokes `kicad-happy:emc` via the integration layer
- [ ] Given any role needs KiCad project analysis, when schematic or PCB analysis is needed, then it invokes `kicad-happy:kicad` via the integration layer
- [ ] Given an analysis skill returns results, when the results are integrated into the pipeline, then they are stored as stage artifacts and available to downstream gates

**Test Cases** (placeholder -- QA will expand):
- TC-304-01: Verify SPICE simulation dispatches via kicad-happy:spice
- TC-304-02: Verify EMC analysis dispatches via kicad-happy:emc
- TC-304-03: Verify analysis results are stored as stage artifacts

**Dependencies**: US-301

---

### US-305: Documentation Integration
**Epic**: kicad-happy Integration Layer
**Priority**: P1
**Estimate**: S (2 pts) -- dispatch patterns for 2 documentation skills (kidoc, BOM)
**As a** compliance specialist (David), **I want** to generate professional engineering documentation (HDD, CE Technical Files, Manufacturing Transfer Packages) through the pipeline, **so that** documentation is produced as part of the structured process rather than as an afterthought.

**Acceptance Criteria**:
- [ ] Given the CompE role is in the Compliance stage, when regulatory documentation is needed, then it invokes `kicad-happy:kidoc` via the integration layer
- [ ] Given the MfgE role is in the Production Release stage, when the manufacturing transfer package is needed, then it invokes `kicad-happy:kidoc` for document generation and `kicad-happy:bom` for BOM finalization
- [ ] Given documentation is generated, when it is stored, then it is saved as a stage artifact with clear provenance (which skill produced it, which stage, which gate)

**Test Cases** (placeholder -- QA will expand):
- TC-305-01: Verify kidoc invocation during Compliance stage
- TC-305-02: Verify kidoc + BOM invocation during Production Release
- TC-305-03: Verify artifact provenance is recorded

**Dependencies**: US-301

---

### US-306: kicad-happy Dependency Documentation & Verification
**Epic**: kicad-happy Integration Layer
**Priority**: P1
**Estimate**: M (3 pts) -- prerequisites.md document + Python verification hook script
**As a** hardware developer (Elena), **I want** clear documentation of the kicad-happy dependency, version compatibility tracking, and automated availability verification at session start, **so that** I know whether my environment is correctly configured before starting a pipeline run.

**Acceptance Criteria**:
- [ ] Given the hardware-team plugin is installed, when its documentation is inspected, then it includes a "Prerequisites" section at `hardware-team/references/prerequisites.md` that: (a) states kicad-happy is a required external dependency, (b) documents the installation mechanism, (c) lists the minimum compatible kicad-happy version, and (d) provides step-by-step installation instructions
- [ ] Given `.hardware/config.yml` exists, when the `dependencies` section is inspected, then it includes a `kicad_happy_version` field that specifies the minimum compatible version (e.g., `kicad_happy_version: ">=1.2.0"`)
- [ ] Given the SessionStart hook fires (US-503), when kicad-happy availability is checked, then the hook verifies that all 11 kicad-happy skills are loadable and reports: (a) which skills are available, (b) which skills are missing, and (c) installation instructions for any missing skills
- [ ] Given kicad-happy is not installed, when the pipeline attempts to start, then it displays a clear error with installation instructions
- [ ] Given the kicad-happy version does not meet the minimum compatibility requirement, when version checking runs, then a warning is displayed

**Test Cases** (placeholder -- QA will expand):
- TC-306-01: Verify prerequisites.md documents installation steps
- TC-306-02: Verify config includes kicad_happy_version field
- TC-306-03: Verify SessionStart hook reports 11/11 when all skills available
- TC-306-04: Verify error message when kicad-happy is not installed

**Dependencies**: US-301

---

## Epic 4: Hardware-Specific Validation Gates

> "Five gates to guard the way. No design shall pass that has not been weighed and found worthy. The reference fixture is our touchstone -- seeded with known flaws so that we may measure our gates against truth."

**Epic Goal:** Implement the 5 hardware-specific validation gates that enforce quality between pipeline stages, backed by a reference test fixture for measurable acceptance criteria.

---

### US-400: Reference Test Fixture Creation
**Epic**: Hardware-Specific Validation Gates
**Priority**: P1
**Estimate**: M (5 pts) -- KiCad schematic/PCB files with seeded defects, BOM CSV, pricing JSON, manifest document
**As a** plugin developer, **I want** a reference KiCad project with known, seeded defects across all validation categories, **so that** all 5 validation gates have a measurable benchmark for acceptance criteria and the North Star metric is quantifiable.

**Acceptance Criteria**:
- [ ] Given the test fixture directory exists at `hardware-team/references/test-fixtures/`, when inspected, then it contains: reference.kicad_sch (10 seeded defects across 7 categories), reference.kicad_pcb (4+ DFM violations), reference-bom.csv (4+ issue types), reference-pricing.json (static offline pricing data), MANIFEST.md
- [ ] Given each seeded defect in the schematic, when categorized, then the 7 categories are covered: power integrity, signal integrity, component derating, missing pull-ups/pull-downs, decoupling strategy, voltage level compatibility, thermal considerations
- [ ] Given each seeded defect in the BOM, when categorized, then it includes: at least 1 obsolete component, 1 budget-exceeding component, 1 single-source component, 1 NRND component
- [ ] Given each seeded defect in the PCB layout, when categorized, then it includes: at least 1 trace width violation, 1 via size violation, 1 solder mask aperture violation, 1 clearance violation
- [ ] Given the MANIFEST.md exists, when inspected, then it lists each defect with: defect ID, category, location in KiCad file, expected detection gate, expected severity
- [ ] Given the BOM test fixture, when used by US-403, then it includes static reference pricing data (not requiring live distributor API calls) so budget threshold acceptance criteria are testable offline

**Test Cases** (placeholder -- QA will expand):
- TC-400-01: Verify test fixture contains all required files
- TC-400-02: Verify MANIFEST.md lists all seeded defects with required fields
- TC-400-03: Verify schematic has defects in all 7 categories
- TC-400-04: Verify BOM has all 4 issue types
- TC-400-05: Verify PCB has all 4 DFM violation types

**Dependencies**: US-101

---

### US-401: Schematic Review Gate
**Epic**: Hardware-Specific Validation Gates
**Priority**: P1
**Estimate**: L (5 pts) -- gate definition in gate-framework.md + iterative review pattern + forced-find prompting instructions
**As a** hardware team lead (Marcus), **I want** a multi-reviewer schematic review gate that catches electrical design issues before layout begins, **so that** fundamental design errors do not propagate to PCB layout and prototyping.

**Acceptance Criteria**:
- [ ] Given a schematic is ready for review, when the Schematic Review Gate activates, then it applies the iterative review agent pattern from issue #76 (multiple reviewers with forced-find prompting)
- [ ] Given the gate runs, when review categories are checked, then the following 7 categories are covered: power integrity, signal integrity, component derating, missing pull-ups/pull-downs, decoupling strategy, voltage level compatibility, thermal considerations
- [ ] Given multiple reviewers operate on the same schematic, when their findings are aggregated, then deduplication is applied (per issue #76 learning)
- [ ] Given a finding is reported, when it is presented, then it includes: finding ID, severity (critical/major/minor), location (sheet/component/net), description, and recommended fix
- [ ] Given ANY critical finding exists, when the gate evaluates, then it returns NOT_DONE and blocks pipeline advancement
- [ ] Given the reference test fixture (US-400), when the gate is run against it, then it detects defects in at least 6 of 7 seeded categories (>80% category detection rate)

**Test Cases** (placeholder -- QA will expand):
- TC-401-01: Verify iterative review with forced-find prompting
- TC-401-02: Verify all 7 review categories are covered
- TC-401-03: Verify deduplication across multiple reviewers
- TC-401-04: Verify critical findings block pipeline advancement
- TC-401-05: Verify >80% detection rate against reference test fixture

**Dependencies**: US-103, US-202, US-400

---

### US-402: DRC Gate
**Epic**: Hardware-Specific Validation Gates
**Priority**: P1
**Estimate**: M (3 pts) -- gate definition in gate-framework.md + kicad-happy:kicad dispatch pattern
**As a** hardware developer (Elena), **I want** an automated DRC gate that validates design rule compliance with pass/fail results and remediation guidance, **so that** PCB layouts meet fab house requirements before prototype ordering.

**Acceptance Criteria**:
- [ ] Given a PCB layout is ready for DRC, when the DRC Gate activates, then it runs design rule checks against the target fab house's capabilities
- [ ] Given DRC violations are found, when they are reported, then each violation includes: rule violated, location (layer/coordinates), severity, and specific remediation steps
- [ ] Given zero DRC violations of severity "error" exist, when the gate evaluates, then it returns DONE
- [ ] Given DRC violations of severity "warning" exist but no "errors", when the gate evaluates, then it returns DONE with warnings documented
- [ ] Given the DRC gate uses KiCad analysis, when it runs, then it CONSUMES `kicad-happy:kicad` for DRC parsing

**Test Cases** (placeholder -- QA will expand):
- TC-402-01: Verify DRC gate consumes kicad-happy:kicad
- TC-402-02: Verify violations include location, severity, remediation
- TC-402-03: Verify gate passes with warnings only (no errors)
- TC-402-04: Verify gate blocks on errors

**Dependencies**: US-103, US-203, US-400

---

### US-403: BOM Gate
**Epic**: Hardware-Specific Validation Gates
**Priority**: P1
**Estimate**: M (3 pts) -- gate definition in gate-framework.md + sourcing skill dispatch pattern + budget logic
**As a** manufacturing engineer (Wei), **I want** a BOM validation gate that checks cost, component availability, lifecycle status, and second-source availability, **so that** prototypes are not ordered with unobtainable or obsolete parts.

**Acceptance Criteria**:
- [ ] Given a BOM is ready for validation, when the BOM Gate activates, then it checks each line item for: price vs. budget, stock availability, lifecycle status (active, NRND, obsolete, EOL), and second-source existence
- [ ] Given a component has lifecycle status NRND or obsolete, when the BOM Gate evaluates, then it returns NOT_DONE with a finding requiring substitution or explicit risk acceptance
- [ ] Given the BOM budget is defined in config, when total BOM cost exceeds the budget, then the gate returns NOT_DONE with a cost breakdown and budget variance
- [ ] Given the BOM Gate needs pricing data, when it evaluates, then it CONSUMES kicad-happy sourcing skills (digikey, mouser, lcsc, element14) via the integration layer
- [ ] Given a component has no second source, when the BOM Gate evaluates, then it flags it as a single-source risk (warning, not blocking unless config requires second-source)

**Test Cases** (placeholder -- QA will expand):
- TC-403-01: Verify lifecycle status check (NRND/obsolete blocks advancement)
- TC-403-02: Verify budget check blocks when exceeded
- TC-403-03: Verify single-source flagged as warning
- TC-403-04: Verify offline testability via reference-pricing.json

**Dependencies**: US-103, US-302, US-400

---

### US-404: DFM Gate
**Epic**: Hardware-Specific Validation Gates
**Priority**: P1
**Estimate**: M (3 pts) -- gate definition in gate-framework.md + fab-specific rule dispatch
**As a** manufacturing engineer (Wei), **I want** a DFM validation gate that checks manufacturability against the target fab house's capabilities, **so that** designs are producible before prototype ordering.

**Acceptance Criteria**:
- [ ] Given a design is ready for DFM review, when the DFM Gate activates, then it evaluates: minimum trace width/spacing, via sizes, drill aspect ratios, layer count vs. fab capability, surface finish compatibility, solder mask aperture sizes, and component footprint availability
- [ ] Given the target fab is JLCPCB, when DFM rules are evaluated, then JLCPCB-specific constraints are applied (consuming `kicad-happy:jlcpcb`)
- [ ] Given a DFM violation is found, when it is reported, then it includes: rule violated, current value, required value, location, and remediation guidance
- [ ] Given zero DFM violations exist, when the gate evaluates, then it returns DONE
- [ ] Given DFM violations exist, when the gate evaluates, then it returns NOT_DONE with a remediation plan

**Test Cases** (placeholder -- QA will expand):
- TC-404-01: Verify fab-specific rules applied (JLCPCB vs PCBWay)
- TC-404-02: Verify violations include current vs required values
- TC-404-03: Verify gate blocks on DFM violations
- TC-404-04: Verify reference test fixture DFM violations are detected

**Dependencies**: US-103, US-204, US-303, US-400

---

### US-405: Compliance Gate
**Epic**: Hardware-Specific Validation Gates
**Priority**: P1
**Estimate**: M (3 pts) -- gate definition in gate-framework.md + evidence-linked checklist pattern
**As a** compliance specialist (David), **I want** a regulatory compliance gate with evidence-linked requirements per target market, **so that** compliance readiness is validated before engaging test labs.

**Acceptance Criteria**:
- [ ] Given the config specifies `compliance_regions: [FCC, CE]`, when the Compliance Gate activates, then it produces a checklist for EACH specified region
- [ ] Given a compliance checklist, when each requirement is evaluated, then it is linked to: the standard clause, the evidence artifact (EMC report, safety analysis, etc.), and pass/fail status
- [ ] Given the Compliance Gate needs EMC analysis, when it evaluates, then it CONSUMES `kicad-happy:emc` for EMC pre-compliance data
- [ ] Given ANY requirement has no linked evidence, when the gate evaluates, then it returns NOT_DONE with the missing evidence items listed
- [ ] Given all requirements have linked evidence and pass, when the gate evaluates, then it returns DONE with the complete compliance package

**Test Cases** (placeholder -- QA will expand):
- TC-405-01: Verify checklist generated per configured region
- TC-405-02: Verify evidence linking for each requirement
- TC-405-03: Verify missing evidence blocks advancement
- TC-405-04: Verify EMC analysis consumes kicad-happy:emc

**Dependencies**: US-103, US-205, US-304, US-400

---

## Epic 5: Collaboration Patterns & Hooks

> "Many that live deserve review. And some that are reviewed deserve shipping. Do not be too eager to deal out judgment on features alone. The Design Review Board shall weigh all perspectives."

**Epic Goal:** Implement hardware-specific collaboration patterns and event-driven hooks.

---

### US-501: Design Review Board Pattern
**Epic**: Collaboration Patterns & Hooks
**Priority**: P1
**Estimate**: M (3 pts) -- collaboration pattern definition (markdown) referenced from orchestrator
**As a** hardware team lead (Marcus), **I want** a Design Review Board collaboration pattern where multiple hardware roles review a design artifact from their respective perspectives, **so that** cross-discipline issues are caught before stage advancement.

**Acceptance Criteria**:
- [ ] Given a design artifact (schematic or layout) is ready for review, when the Design Review Board pattern activates, then it dispatches review tasks to: Electrical Engineer, PCB Layout Engineer, Manufacturing Engineer, and Compliance Engineer (as applicable to the stage)
- [ ] Given multiple reviewers produce findings, when findings are aggregated, then deduplication is applied across reviewers
- [ ] Given the Design Review Board completes, when results are presented, then they are organized by reviewer role with a unified severity ranking
- [ ] Given the Design Review Board is based on delivery-team's adversarial review pattern, when it executes, then each reviewer independently evaluates the artifact (no shared context between reviewers during review)

**Test Cases** (placeholder -- QA will expand):
- TC-501-01: Verify 3+ roles review independently
- TC-501-02: Verify findings are deduplicated across reviewers
- TC-501-03: Verify results organized by role with unified severity

**Dependencies**: US-102, US-202, US-203, US-204

---

### US-502: BOM Reconciliation Pattern
**Epic**: Collaboration Patterns & Hooks
**Priority**: P2
**Estimate**: S (2 pts) -- collaboration pattern definition (markdown)
**As a** manufacturing engineer (Wei), **I want** a BOM Reconciliation collaboration pattern that cross-validates BOM data across multiple suppliers, **so that** pricing and availability discrepancies are identified before ordering.

**Acceptance Criteria**:
- [ ] Given a BOM is ready for reconciliation, when the pattern activates, then it queries multiple kicad-happy sourcing skills for each BOM line item
- [ ] Given pricing data from multiple suppliers, when reconciliation completes, then discrepancies >20% between suppliers are flagged
- [ ] Given availability data from multiple suppliers, when reconciliation completes, then components available from only one supplier are flagged as single-source risk

**Test Cases** (placeholder -- QA will expand):
- TC-502-01: Verify multi-supplier query for each BOM line item
- TC-502-02: Verify >20% pricing discrepancy flagged
- TC-502-03: Verify single-source risk flagged

**Dependencies**: US-302, US-403

---

### US-503: Config & Dependency Validation Hook (SessionStart)
**Epic**: Collaboration Patterns & Hooks
**Priority**: P1
**Estimate**: M (5 pts) -- Python hook scripts (check_hw_config.py + check_kicad_happy.py) + hooks.json configuration
**As a** hardware developer (Elena), **I want** the pipeline to validate both `.hardware/config.yml` and kicad-happy skill availability at session start, **so that** I am warned early if my config is missing, outdated, or my environment lacks required dependencies.

**Acceptance Criteria**:
- [ ] Given a SessionStart event fires, when `.hardware/config.yml` does not exist, then a warning is displayed: "No .hardware/config.yml found. Run `hw-setup` to create one."
- [ ] Given a SessionStart event fires, when `.hardware/config.yml` exists but has an outdated schema version, then a warning is displayed with migration guidance
- [ ] Given a SessionStart event fires, when `.hardware/config.yml` exists and is valid, then no config warning is displayed
- [ ] Given a SessionStart event fires, when kicad-happy skill availability is checked, then the hook verifies all 11 kicad-happy skills and reports: available count, missing skills list, installation instructions for missing skills
- [ ] Given kicad-happy is fully installed, when the availability check completes, then a confirmation is displayed: "kicad-happy: 11/11 skills available"
- [ ] Given kicad-happy is partially installed or missing, when the availability check completes, then a warning lists missing skills with installation instructions
- [ ] Given a paused pipeline state exists, when SessionStart fires, then it displays paused pipeline status with staleness detection per architecture Section 3.4.1
- [ ] Given the hooks.json exists at `hardware-team/hooks/hooks.json`, when inspected, then it defines SessionStart hooks for config validation and kicad-happy availability

**Test Cases** (placeholder -- QA will expand):
- TC-503-01: Verify missing config warning message
- TC-503-02: Verify outdated schema version warning
- TC-503-03: Verify kicad-happy 11/11 confirmation
- TC-503-04: Verify partial kicad-happy warning with missing list
- TC-503-05: Verify paused pipeline staleness detection

**Dependencies**: US-104, US-306

---

### US-504: Schematic DRC Hook (PostToolUse)
**Epic**: Collaboration Patterns & Hooks
**Priority**: P2
**Estimate**: S (2 pts) -- Python hook script + hooks.json entry
**As a** hardware developer (Elena), **I want** DRC validation to run automatically when KiCad schematic files are modified, **so that** I get immediate feedback on design rule violations.

**Acceptance Criteria**:
- [ ] Given a PostToolUse event fires for Write or Edit, when the modified file has a `.kicad_sch` extension, then DRC validation is triggered automatically
- [ ] Given DRC validation runs, when violations are found, then they are displayed as warnings (not blocking the edit)
- [ ] Given DRC validation runs, when no violations are found, then no output is displayed (silent success)

**Test Cases** (placeholder -- QA will expand):
- TC-504-01: Verify DRC triggers on .kicad_sch file edit
- TC-504-02: Verify violations displayed as non-blocking warnings
- TC-504-03: Verify silent success when no violations

**Dependencies**: US-402

---

### US-505: BOM Drift Detection Hook (PostToolUse)
**Epic**: Collaboration Patterns & Hooks
**Priority**: P2
**Estimate**: S (2 pts) -- Python hook script + hooks.json entry
**As a** hardware developer (Elena), **I want** to be warned when schematic changes invalidate the current BOM, **so that** I know the BOM needs updating before I order parts.

**Acceptance Criteria**:
- [ ] Given a PostToolUse event fires for Write or Edit on a `.kicad_sch` file, when a BOM artifact exists from a previous pipeline stage, then the hook compares the current schematic's component list against the BOM
- [ ] Given the schematic has components not in the BOM, when drift is detected, then a warning is displayed listing the new/changed components
- [ ] Given the BOM has components not in the schematic, when drift is detected, then a warning is displayed listing the removed components

**Test Cases** (placeholder -- QA will expand):
- TC-505-01: Verify BOM drift detection on schematic edit
- TC-505-02: Verify new components listed in warning
- TC-505-03: Verify removed components listed in warning

**Dependencies**: US-403

---

## Epic 6: Phase 2 Roles (Deferred)

> "Many features that are requested deserve to be deprioritized. And some that are deprioritized deserve to ship. These two roles shall wait for Phase 2."

**Note:** This epic is explicitly deferred to Phase 2 per risk mitigation. Documented here for dependency tracking only.

---

### US-601: Mechanical Engineer Skill
**Epic**: Phase 2 Roles (Deferred)
**Priority**: P3
**Estimate**: L (8 pts)
**As a** hardware developer, **I want** a Mechanical Engineer role for enclosure design guidance, thermal management, and mechanical integration, **so that** hardware projects consider the full physical product.

**Acceptance Criteria**:
- [ ] Deferred to Phase 2 -- acceptance criteria to be defined when epic is scheduled

**Test Cases** (placeholder):
- TC-601-01: Deferred

**Dependencies**: US-101

---

### US-602: Firmware Engineer Skill
**Epic**: Phase 2 Roles (Deferred)
**Priority**: P3
**Estimate**: M (5 pts)
**As a** firmware engineer (Priya), **I want** a Firmware Engineer role integrated into the hardware pipeline, **so that** firmware bring-up is coordinated with hardware design.

**Acceptance Criteria**:
- [ ] Deferred to Phase 2 -- acceptance criteria to be defined when epic is scheduled
- [ ] Depends on firmware interface documentation produced by EE role (US-202)

**Test Cases** (placeholder):
- TC-602-01: Deferred

**Dependencies**: US-101, US-202

---

## Story Sequencing & Sprint Plan

> "A product owner is never late, nor early. They prioritize precisely when they mean to."

### Dependency Graph (Critical Path)

```
US-101 (Plugin Skeleton)
  |
  +-- US-108 (Marketplace Registration)
  |
  +-- US-102 (Pipeline Orchestrator) --+-- US-103 (Gate Framework) --+-- US-107 (Rework Loops)
  |     |                               |
  |     +-- US-104 (Config) -----+      +-- US-401 (Schematic Gate)
  |     |                        |      +-- US-402 (DRC Gate)
  |     +-- US-105 (P2: State)   |      +-- US-403 (BOM Gate)
  |     +-- US-106 (P2: Memory)  |      +-- US-404 (DFM Gate)
  |                              |      +-- US-405 (Compliance Gate)
  |                              |
  |                              +-- US-503 (SessionStart Hook)
  |
  +-- US-201 (HW PO)
  +-- US-202 (EE)
  +-- US-203 (PCB Layout)
  +-- US-204 (MfgE)
  +-- US-205 (CompE)
  +-- US-206 (TestE)
  |
  +-- US-301 (Integration Layer) --+-- US-302 (Sourcing)
  |                                +-- US-303 (Fabrication)
  |                                +-- US-304 (Analysis)
  |                                +-- US-305 (Documentation)
  |                                +-- US-306 (Dependency Docs)
  |
  +-- US-400 (Reference Test Fixture)
  |
  +-- US-501 (Design Review Board) -- needs US-102, US-202, US-203, US-204
```

### Sprint 1: Foundations (P1 stories with no dependencies or only US-101)

**Capacity:** 80% of available velocity (baseline TBD -- first sprint)
**Sprint goal:** Plugin skeleton, pipeline orchestrator, and all role skills created. Integration layer architecture defined.

| Story | Points | Type |
|-------|--------|------|
| US-101: Plugin Skeleton | 2 | Markdown + directory creation |
| US-108: Marketplace Registration | 1 | JSON edit |
| US-102: Pipeline Orchestrator | 8 | Markdown (SKILL.md + 7 references) |
| US-104: Config-Driven Pipeline | 5 | Markdown + Python script |
| US-201: HW Product Owner | 3 | Markdown (SKILL.md + 3 references) |
| US-202: Electrical Engineer | 5 | Markdown (SKILL.md + 5 references) |
| US-203: PCB Layout Engineer | 5 | Markdown (SKILL.md + 3 references) |
| US-204: Manufacturing Engineer | 3 | Markdown (SKILL.md + 4 references) |
| US-205: Compliance Engineer | 3 | Markdown (SKILL.md + 4 references) |
| US-206: Test Engineer | 3 | Markdown (SKILL.md + 4 references) |
| US-301: Integration Layer | 5 | Markdown (integration reference) |
| US-400: Reference Test Fixture | 5 | KiCad files + manifest |
| **Sprint Total** | **48** | |

**Note:** This sprint is heavily markdown-weighted (40 of 48 points are markdown files). Calibrated estimates already account for the markdown tier reduction. The high point count reflects the number of files to create (50+ files), not code complexity.

### Sprint 2: Gates, Rework, Integration Details, and Hooks (P1 stories with Sprint 1 dependencies)

**Capacity:** 80% of available velocity
**Sprint goal:** All validation gates operational against reference test fixture. Rework loops functional. Integration sub-stories complete. SessionStart hook active.

| Story | Points | Type |
|-------|--------|------|
| US-103: Gate Framework | 8 | Markdown (gate-framework.md) |
| US-107: Rework Loop Support | 8 | Markdown (rework-paths.md) + orchestrator updates |
| US-302: Sourcing Integration | 3 | Markdown (integration patterns) |
| US-303: Fabrication Integration | 3 | Markdown (integration patterns) |
| US-304: Analysis Integration | 3 | Markdown (integration patterns) |
| US-305: Documentation Integration | 2 | Markdown (integration patterns) |
| US-306: Dependency Docs | 3 | Markdown + Python hook script |
| US-401: Schematic Review Gate | 5 | Markdown (gate definition + review pattern) |
| US-402: DRC Gate | 3 | Markdown (gate definition) |
| US-403: BOM Gate | 3 | Markdown (gate definition) |
| US-404: DFM Gate | 3 | Markdown (gate definition) |
| US-405: Compliance Gate | 3 | Markdown (gate definition) |
| US-501: Design Review Board | 3 | Markdown (collaboration pattern) |
| US-503: SessionStart Hook | 5 | Python hooks + hooks.json |
| **Sprint Total** | **55** | |

### Sprint 3: P2 Stories (Should Have)

**Capacity:** 80% of available velocity
**Sprint goal:** State persistence, self-learning memory, remaining hooks, BOM reconciliation.

| Story | Points | Type |
|-------|--------|------|
| US-105: Pipeline State Persistence | 5 | Python script + markdown |
| US-106: Self-Learning Memory | 3 | Markdown (memory protocol) |
| US-502: BOM Reconciliation | 2 | Markdown (collaboration pattern) |
| US-504: Schematic DRC Hook | 2 | Python hook script |
| US-505: BOM Drift Detection Hook | 2 | Python hook script |
| **Sprint Total** | **14** | |

### Summary

| Priority | Stories | Total Points |
|----------|---------|-------------|
| P1 (Must Have) | 27 stories | 99 pts |
| P2 (Should Have) | 5 stories | 14 pts |
| P3 (Could Have / Deferred) | 2 stories | 13 pts |
| **Total** | **34 stories** | **126 pts** |

---

> "The road goes ever on and on, but with these stories, we know exactly where it leads. The fellowship has its map. Now we march."
