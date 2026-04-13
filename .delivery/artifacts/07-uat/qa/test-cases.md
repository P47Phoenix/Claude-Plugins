# UAT Test Cases: hardware-team Plugin

**Author:** QA Engineer (Legolas)
**Plan:** `./test-plan.md`
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12

**Style:** Preconditions / Steps / Expected Result / FR mapping.
**Legend:** **P0** critical, **P1** high, **P2** medium, **P3** low.

---

> "One hundred and three arrows in my quiver. One for each test. That bug still only counts as one."

---

## Category 1: Plugin Installation Verification (FR-001)

### TC-001 (P0) -- Directory structure matches CLAUDE.md pattern

- **Preconditions:** hardware-team/ directory exists in repo root
- **Steps:**
  1. Run `ls -R hardware-team/` from repo root
  2. Verify the following items exist: SKILL.md, LICENSE.txt, skills/, references/, hooks/, scripts/
  3. Verify skills/ contains exactly 7 sub-directories: hardware-flow/, hw-product-owner/, electrical-engineer/, pcb-layout-engineer/, manufacturing-engineer/, compliance-engineer/, test-engineer/
  4. Verify each sub-directory contains a SKILL.md file
- **Expected Result:** All items present. 7 skill directories confirmed. Each has SKILL.md.
- **FR Mapping:** FR-001

### TC-002 (P0) -- SKILL.md loads with three-level context

- **Preconditions:** hardware-team/SKILL.md exists
- **Steps:**
  1. Invoke `hardware-team` skill via Skill tool
  2. Check response for SKILL_LOADED signal
  3. Verify SKILL.md contains: metadata (name, description, license), skill instructions, resource loading directives
- **Expected Result:** SKILL_LOADED returned. Three-level context loading present in SKILL.md.
- **FR Mapping:** FR-001

### TC-003 (P0) -- marketplace.json contains hardware-team entry

- **Preconditions:** .claude-plugin/marketplace.json exists
- **Steps:**
  1. Open marketplace.json
  2. Search for "hardware-team" entry
  3. Verify entry contains: unique ID ("hardware-team"), display name, description, skill paths for all 7 skills
  4. Verify description mentions kicad-happy dependency
- **Expected Result:** Entry found with all required fields. kicad-happy dependency noted.
- **FR Mapping:** FR-001

### TC-004 (P0) -- No marketplace ID conflicts

- **Preconditions:** marketplace.json contains hardware-team entry
- **Steps:**
  1. Parse all IDs in marketplace.json
  2. Check for duplicates
  3. Verify "hardware-team" does not collide with "delivery-team", "kicad-happy", or any other registered ID
- **Expected Result:** Zero ID conflicts.
- **FR Mapping:** FR-001

### TC-005 (P1) -- LICENSE.txt present and valid

- **Preconditions:** hardware-team/ directory exists
- **Steps:**
  1. Verify hardware-team/LICENSE.txt exists
  2. Verify it contains a recognized license text
- **Expected Result:** LICENSE.txt present with valid license.
- **FR Mapping:** FR-001

---

## Category 2: Skill Discoverability & Context Isolation (FR-008)

### TC-010 (P0) -- hardware-flow orchestrator loads

- **Preconditions:** hardware-team/skills/hardware-flow/SKILL.md exists
- **Steps:**
  1. Invoke `hardware-team:hardware-flow` via Skill tool
  2. Verify SKILL_LOADED signal returned
  3. Verify SKILL.md defines all 8 stages (Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release)
  4. Verify SKILL.md contains Prime Directive guardrail (Agent tool dispatch, NOT inlined)
- **Expected Result:** Skill loads. 8 stages defined. Dispatch guardrail present.
- **FR Mapping:** FR-008, FR-002, FR-020

### TC-011 (P0) -- hw-product-owner loads with isolation

- **Preconditions:** hardware-team/skills/hw-product-owner/SKILL.md exists
- **Steps:**
  1. Invoke `hardware-team:hw-product-owner` via Skill tool
  2. Verify SKILL_LOADED signal
  3. Audit reference files loaded: must include ONLY hw-requirements.md, feasibility-analysis.md, make-vs-buy.md
  4. Verify zero references from other roles (EE, Layout, MfgE, CompE, TestE)
- **Expected Result:** Loads with HW PO references only. Zero cross-role bleed.
- **FR Mapping:** FR-008

### TC-012 (P0) -- electrical-engineer loads with isolation

- **Preconditions:** hardware-team/skills/electrical-engineer/SKILL.md exists
- **Steps:**
  1. Invoke `hardware-team:electrical-engineer` via Skill tool
  2. Verify SKILL_LOADED signal
  3. Audit reference files: must load ONLY EE-specific references (5 files per PRD)
  4. Verify model tier specified as Sonnet+ in SKILL.md
  5. Verify SKILL.md includes firmware interface documentation as output artifact (pin assignment table, power domain map, bus interface spec, debug access points)
- **Expected Result:** Loads with EE references only. Sonnet+ tier documented. Firmware docs output specified.
- **FR Mapping:** FR-008

### TC-013 (P0) -- pcb-layout-engineer loads with isolation

- **Preconditions:** hardware-team/skills/pcb-layout-engineer/SKILL.md exists
- **Steps:**
  1. Invoke `hardware-team:pcb-layout-engineer` via Skill tool
  2. Verify SKILL_LOADED signal
  3. Audit reference files: ONLY layout references (3 files)
  4. Verify model tier specified as Sonnet+ in SKILL.md
- **Expected Result:** Loads with Layout references only. Sonnet+ tier documented.
- **FR Mapping:** FR-008

### TC-014 (P0) -- manufacturing-engineer loads with isolation

- **Preconditions:** hardware-team/skills/manufacturing-engineer/SKILL.md exists
- **Steps:**
  1. Invoke `hardware-team:manufacturing-engineer` via Skill tool
  2. Verify SKILL_LOADED signal
  3. Audit reference files: ONLY MfgE references (4 files)
- **Expected Result:** Loads with MfgE references only.
- **FR Mapping:** FR-008

### TC-015 (P0) -- compliance-engineer loads with isolation

- **Preconditions:** hardware-team/skills/compliance-engineer/SKILL.md exists
- **Steps:**
  1. Invoke `hardware-team:compliance-engineer` via Skill tool
  2. Verify SKILL_LOADED signal
  3. Audit reference files: ONLY CompE references (4 files)
- **Expected Result:** Loads with CompE references only.
- **FR Mapping:** FR-008

### TC-016 (P0) -- test-engineer loads with isolation

- **Preconditions:** hardware-team/skills/test-engineer/SKILL.md exists
- **Steps:**
  1. Invoke `hardware-team:test-engineer` via Skill tool
  2. Verify SKILL_LOADED signal
  3. Audit reference files: ONLY TestE references (4 files)
- **Expected Result:** Loads with TestE references only.
- **FR Mapping:** FR-008

### TC-017 (P1) -- EE produces firmware interface documentation

- **Preconditions:** EE skill loaded, Schematic stage context
- **Steps:**
  1. Invoke EE during Schematic stage
  2. Verify output includes firmware interface documentation artifact
  3. Verify artifact contains: pin assignment table, power domain map, communication bus interface spec (I2C/SPI/UART address map, clock rates, voltage levels), debug interface access points
- **Expected Result:** Firmware interface docs produced with all 4 required sections.
- **FR Mapping:** FR-008 (C4 resolution)

### TC-018 (P1) -- HW PO produces Concept stage artifacts

- **Preconditions:** HW PO skill loaded, Concept stage context
- **Steps:**
  1. Invoke HW PO during Concept stage
  2. Verify output includes: requirements document, constraint matrix, regulatory landscape scan, initial BOM budget
- **Expected Result:** All 4 Concept artifacts produced.
- **FR Mapping:** FR-008

### TC-019 (P1) -- MfgE produces DFM/DFA artifacts

- **Preconditions:** MfgE skill loaded, DFM/DFA stage context
- **Steps:**
  1. Invoke MfgE during DFM/DFA stage
  2. Verify output includes: DFM review report, DFA review report, yield risk assessment, remediation guidance
- **Expected Result:** All 4 DFM/DFA artifacts produced.
- **FR Mapping:** FR-008

### TC-020 (P1) -- CompE produces Compliance artifacts

- **Preconditions:** CompE skill loaded, Compliance stage context with regions=[FCC, CE]
- **Steps:**
  1. Invoke CompE during Compliance stage
  2. Verify output includes: EMC pre-compliance report, safety analysis, environmental compliance checklist, test lab preparation package
- **Expected Result:** All 4 Compliance artifacts produced.
- **FR Mapping:** FR-008

### TC-021 (P1) -- TestE produces Prototype artifacts

- **Preconditions:** TestE skill loaded, Prototype stage context
- **Steps:**
  1. Invoke TestE during Prototype stage
  2. Verify output includes: test strategy document, test fixture requirements, bring-up test procedure, validation acceptance criteria
  3. Verify test strategy covers: functional, environmental, reliability, production screening
- **Expected Result:** All 4 artifacts produced. Strategy covers all 4 testing types.
- **FR Mapping:** FR-008

### TC-022 (P0) -- NFR-007 model tier audit

- **Preconditions:** All 6 role SKILL.md files exist
- **Steps:**
  1. Open each of the 6 role SKILL.md files
  2. Search for model tier specification (Haiku/Sonnet/Opus)
  3. Verify EE and PCB Layout specify Sonnet+ minimum
- **Expected Result:** All 6 roles document minimum model tier. EE and Layout require Sonnet+.
- **FR Mapping:** FR-008, NFR-007

### TC-023 (P0) -- NFR-002 context isolation sweep

- **Preconditions:** All 6 role SKILL.md files exist
- **Steps:**
  1. For each role, extract the list of references/files loaded
  2. Cross-check: no role loads references belonging to another role
  3. Verify hardware-flow orchestrator does NOT load any role-specific references
- **Expected Result:** Zero cross-role reference loading. Orchestrator loads only orchestrator references.
- **FR Mapping:** FR-008, NFR-002

---

## Category 3: Hook Execution (FR-017, FR-018, FR-019)

### TC-030 (P0) -- hooks.json defines all hooks correctly

- **Preconditions:** hardware-team/hooks/hooks.json exists
- **Steps:**
  1. Parse hooks.json
  2. Verify SessionStart hooks defined (config check, kicad-happy check)
  3. Verify PreToolUse hook defined (pipeline bypass detection)
  4. Verify PostToolUse hooks defined (KiCad DRC, BOM drift)
  5. Verify each hook references a valid Python script in hooks/
- **Expected Result:** All hooks defined with correct event types and valid script paths.
- **FR Mapping:** FR-017

### TC-031 (P0) -- SessionStart config check: no config

- **Preconditions:** No .hardware/config.yml in project root
- **Steps:**
  1. Run `python hardware-team/hooks/check_hw_config.py`
  2. Capture output
- **Expected Result:** Warning: "No .hardware/config.yml found. Run `hw-setup` to create one."
- **FR Mapping:** FR-017

### TC-032 (P0) -- SessionStart config check: outdated config

- **Preconditions:** .hardware/config.yml exists with outdated schema version
- **Steps:**
  1. Create config with `config_version: "0.9"`
  2. Run check_hw_config.py
- **Expected Result:** Warning with migration guidance for schema version update.
- **FR Mapping:** FR-017

### TC-033 (P0) -- SessionStart config check: valid config

- **Preconditions:** .hardware/config.yml exists with current schema version
- **Steps:**
  1. Create valid config with current version
  2. Run check_hw_config.py
- **Expected Result:** No config warning displayed (silent success).
- **FR Mapping:** FR-017

### TC-034 (P0) -- SessionStart kicad-happy check: fully installed

- **Preconditions:** kicad-happy v1.2.0+ installed with all 11 skills
- **Steps:**
  1. Run `python hardware-team/hooks/check_kicad_happy.py`
  2. Capture output
- **Expected Result:** "kicad-happy: 11/11 skills available"
- **FR Mapping:** FR-017

### TC-035 (P0) -- SessionStart kicad-happy check: partially installed

- **Preconditions:** kicad-happy installed with some skills missing
- **Steps:**
  1. Simulate partial installation (rename some skill directories)
  2. Run check_kicad_happy.py
- **Expected Result:** "kicad-happy: N/11 skills available. Missing: [list]. Install kicad-happy via Claude Code plugin system."
- **FR Mapping:** FR-017

### TC-036 (P0) -- SessionStart kicad-happy check: not installed

- **Preconditions:** kicad-happy not installed
- **Steps:**
  1. Temporarily rename kicad-happy install directory
  2. Run check_kicad_happy.py
- **Expected Result:** Error: "Required dependency kicad-happy is not installed. Install it via: [installation instructions]."
- **FR Mapping:** FR-017

### TC-037 (P2) -- PostToolUse DRC hook: .kicad_sch edit triggers DRC

- **Preconditions:** PostToolUse hook configured for .kicad_sch files
- **Steps:**
  1. Simulate PostToolUse event for Write to a .kicad_sch file
  2. Feed event JSON to check_kicad_file.py
- **Expected Result:** DRC triggers. Violations displayed as warnings (non-blocking).
- **FR Mapping:** FR-018 (P2)

### TC-038 (P2) -- PostToolUse DRC hook: non-.kicad_sch edit ignored

- **Preconditions:** PostToolUse hook configured
- **Steps:**
  1. Simulate PostToolUse event for Write to a .py file
  2. Feed event JSON to check_kicad_file.py
- **Expected Result:** No DRC trigger. Hook exits silently.
- **FR Mapping:** FR-018 (P2)

### TC-039 (P2) -- PostToolUse BOM drift: detects new components

- **Preconditions:** BOM artifact exists from previous stage, .kicad_sch modified
- **Steps:**
  1. Simulate schematic edit adding new component
  2. Run BOM drift detection
- **Expected Result:** Warning listing new/changed components not in BOM.
- **FR Mapping:** FR-019 (P2)

### TC-040 (P2) -- PostToolUse BOM drift: detects removed components

- **Preconditions:** BOM artifact exists, .kicad_sch modified
- **Steps:**
  1. Simulate schematic edit removing a component
  2. Run BOM drift detection
- **Expected Result:** Warning listing removed components still in BOM.
- **FR Mapping:** FR-019 (P2)

### TC-041 (P1) -- PreToolUse pipeline bypass detection

- **Preconditions:** PreToolUse hook configured for Skill invocation
- **Steps:**
  1. Simulate Skill tool invocation for a role skill (e.g., electrical-engineer) OUTSIDE pipeline context
  2. Feed event JSON to check_pipeline_bypass.py
- **Expected Result:** Warning: role skill invoked outside hardware-flow pipeline context.
- **FR Mapping:** FR-017

### TC-042 (P1) -- PreToolUse pipeline bypass: inside pipeline allowed

- **Preconditions:** PreToolUse hook configured
- **Steps:**
  1. Simulate Skill tool invocation for a role skill INSIDE pipeline context
  2. Feed event JSON to check_pipeline_bypass.py
- **Expected Result:** No warning. Hook exits silently.
- **FR Mapping:** FR-017

---

## Category 4: Config Validation (FR-004)

### TC-050 (P1) -- validate_config.py: valid config passes

- **Preconditions:** hardware-team/skills/hardware-flow/scripts/validate_config.py exists
- **Steps:**
  1. Create a valid .hardware/config.yml with: config_version, target_fab: jlcpcb, compliance_regions: [FCC, CE], bom_budget: 50.00, dependencies: {kicad_happy_version: ">=1.2.0"}, max_rework_iterations: 3, max_total_reworks: 10
  2. Run `python validate_config.py valid-config.yml`
- **Expected Result:** Exit 0. No warnings. All fields parsed correctly.
- **FR Mapping:** FR-004

### TC-051 (P1) -- validate_config.py: missing config uses defaults

- **Preconditions:** No .hardware/config.yml exists
- **Steps:**
  1. Run pipeline without config file
  2. Verify defaults are applied
- **Expected Result:** Log: "No project config found, using defaults." Pipeline proceeds with defaults.
- **FR Mapping:** FR-004

### TC-052 (P1) -- validate_config.py: invalid config warns and defaults

- **Preconditions:** .hardware/config.yml exists with invalid fields
- **Steps:**
  1. Create config with target_fab: "invalid_fab_house", bom_budget: "not_a_number"
  2. Run validate_config.py
- **Expected Result:** Warnings for invalid fields. Defaults used for those fields. Pipeline NOT failed.
- **FR Mapping:** FR-004

### TC-053 (P1) -- validate_config.py: outdated schema warns

- **Preconditions:** Config with old config_version
- **Steps:**
  1. Create config with config_version: "0.5"
  2. Run validate_config.py
- **Expected Result:** Warning with migration guidance. Defaults for missing new-version fields.
- **FR Mapping:** FR-004

### TC-054 (P1) -- Config schema includes all required fields

- **Preconditions:** Config schema documentation exists
- **Steps:**
  1. Review config schema (config-schema.md or equivalent)
  2. Verify presence of: config_version, target_fab, compliance_regions, bom_budget, production_volume, dependencies.kicad_happy_version, max_rework_iterations, max_total_reworks
- **Expected Result:** All required fields documented in schema.
- **FR Mapping:** FR-004

### TC-055 (P1) -- Config: dependencies.kicad_happy_version field

- **Preconditions:** Config schema exists
- **Steps:**
  1. Verify schema defines dependencies.kicad_happy_version
  2. Create config with kicad_happy_version: ">=1.2.0"
  3. Validate config parses this field
- **Expected Result:** Field recognized and parsed. Version constraint stored.
- **FR Mapping:** FR-004 (C2 resolution)

### TC-056 (P1) -- Config: max_rework_iterations default 3

- **Preconditions:** Config schema exists
- **Steps:**
  1. Create config WITHOUT max_rework_iterations
  2. Validate default value is 3
- **Expected Result:** Default 3 applied when field absent.
- **FR Mapping:** FR-004 (C8 resolution)

### TC-057 (P1) -- Config: max_total_reworks default 10

- **Preconditions:** Config schema exists
- **Steps:**
  1. Create config WITHOUT max_total_reworks
  2. Validate default value is 10
- **Expected Result:** Default 10 applied when field absent.
- **FR Mapping:** FR-004 (C8 resolution)

### TC-058 (P1) -- NFR-006 forward compatibility

- **Preconditions:** Config v1.0 file (subset of v1.1+ fields)
- **Steps:**
  1. Create minimal config with only config_version and target_fab
  2. Run validate_config.py (which expects v1.1+ schema)
  3. Verify missing fields use defaults without error
- **Expected Result:** Old config loads successfully. Missing keys default. No pipeline failure.
- **FR Mapping:** FR-004, NFR-006

---

## Category 5: Pipeline Orchestrator (FR-002, FR-003, FR-007, FR-020)

### TC-060 (P0) -- Pipeline starts with Stage 1 (Concept)

- **Preconditions:** New hardware project, pipeline not yet started
- **Steps:**
  1. Start hardware-flow pipeline
  2. Verify Stage 1 (Concept) executes first
  3. Verify HW PO role is dispatched
- **Expected Result:** Concept stage runs first. HW PO dispatched.
- **FR Mapping:** FR-002

### TC-061 (P0) -- Pipeline advances sequentially through 8 stages

- **Preconditions:** Pipeline running
- **Steps:**
  1. Complete Stage 1, verify gate passes
  2. Verify pipeline advances to Stage 2 (Schematic)
  3. Continue through all 8 stages: Concept -> Schematic -> Layout -> Prototype -> DFM/DFA -> Compliance -> Pilot Run -> Production Release
- **Expected Result:** All 8 stages execute in correct order with gate validation between each.
- **FR Mapping:** FR-002

### TC-062 (P0) -- AI-execution stages run autonomously

- **Preconditions:** Pipeline reaches AI-execution stages (1, 2, 3, 5, 6)
- **Steps:**
  1. Verify stages 1 (Concept), 2 (Schematic), 3 (Layout), 5 (DFM/DFA), 6 (Compliance) execute autonomously
  2. Verify each dispatches work via Agent tool sub-agent
  3. Verify no human confirmation required for these stages
- **Expected Result:** AI stages complete autonomously. Agent tool dispatch confirmed.
- **FR Mapping:** FR-002

### TC-063 (P0) -- Human-execution stages pause for confirmation

- **Preconditions:** Pipeline reaches human-execution stages (4, 7, 8)
- **Steps:**
  1. Verify Stage 4 (Prototype) generates preparation docs (ordering package, test procedures)
  2. Verify pipeline pauses and awaits human confirmation
  3. Verify same pattern for Stage 7 (Pilot Run) and Stage 8 (Production Release)
- **Expected Result:** Human stages generate docs, pause for human, resume only on confirmation.
- **FR Mapping:** FR-002

### TC-064 (P1) -- Stage transitions logged

- **Preconditions:** Pipeline running through multiple stages
- **Steps:**
  1. Complete at least 3 stage transitions
  2. Inspect pipeline log/state
  3. Verify each transition logged with: timestamp, gate result, source stage, target stage
- **Expected Result:** All transitions logged with required metadata.
- **FR Mapping:** FR-002

### TC-065 (P1) -- Each stage has purpose, activities, and roles

- **Preconditions:** hardware-flow SKILL.md exists
- **Steps:**
  1. For each of the 8 stages, verify SKILL.md defines: purpose, key activities list, required role(s), execution mode (AI or human)
- **Expected Result:** All 8 stages fully defined.
- **FR Mapping:** FR-002

### TC-066 (P0) -- All stage dispatches use Agent tool

- **Preconditions:** hardware-flow SKILL.md exists
- **Steps:**
  1. Inspect SKILL.md for Agent tool dispatch patterns
  2. Verify explicit guardrail: orchestrator NEVER produces domain artifacts
  3. Verify every stage dispatch is a separate Agent tool invocation
- **Expected Result:** Agent tool dispatch enforced. Guardrail language present.
- **FR Mapping:** FR-020

### TC-067 (P1) -- Dispatch failure: retry-then-pause

- **Preconditions:** Pipeline running
- **Steps:**
  1. Simulate a stage dispatch failure (e.g., invoke non-existent skill)
  2. Verify orchestrator retries once
  3. Verify on second failure, pipeline enters PAUSED_DISPATCH_ERROR state
  4. Verify error classification: TIMEOUT, CONTEXT_OVERFLOW, MODEL_ERROR, or UNKNOWN
- **Expected Result:** Retry once, then pause with classified error.
- **FR Mapping:** FR-020

### TC-070 (P0) -- Gate passes when ALL validators DONE

- **Preconditions:** Gate framework active, mock gate with 3 validators
- **Steps:**
  1. Set all 3 validators to DONE
  2. Evaluate gate
- **Expected Result:** Gate passes. Pipeline advances to next stage.
- **FR Mapping:** FR-003

### TC-071 (P0) -- Gate blocks when ANY validator NOT_DONE

- **Preconditions:** Gate framework active, mock gate with 3 validators
- **Steps:**
  1. Set 2 validators to DONE, 1 to NOT_DONE
  2. Evaluate gate
  3. Verify failing validator's feedback is returned
- **Expected Result:** Gate blocks. Pipeline does NOT advance. Feedback provided for correction.
- **FR Mapping:** FR-003

### TC-072 (P0) -- Gate blocks when multiple validators NOT_DONE

- **Preconditions:** Gate framework active
- **Steps:**
  1. Set 1 DONE, 2 NOT_DONE
  2. Evaluate gate
  3. Verify ALL failing validators' feedback returned
- **Expected Result:** Gate blocks. All failing feedback returned.
- **FR Mapping:** FR-003

### TC-073 (P1) -- Gate validator metadata complete

- **Preconditions:** Gate framework documentation exists
- **Steps:**
  1. Inspect all gate validators across 5 gate types
  2. Verify each has: unique ID, description, pass/fail criteria, responsible role
- **Expected Result:** All validators have complete metadata.
- **FR Mapping:** FR-003

### TC-074 (P1) -- Human Confirmation Gate for physical stages

- **Preconditions:** Pipeline at Prototype stage (Stage 4)
- **Steps:**
  1. Verify gate type is Human Confirmation
  2. Verify pipeline does NOT auto-advance
  3. Verify gate waits for explicit human input
- **Expected Result:** Human gate pauses pipeline. No auto-advancement.
- **FR Mapping:** FR-003

### TC-080 (P2) -- State persistence on session end

- **Preconditions:** Pipeline in progress at Stage 4
- **Steps:**
  1. End session
  2. Verify .hardware/state.md saved with: current stage, gate results, artifact paths, rework history
- **Expected Result:** State persisted with all required fields.
- **FR Mapping:** FR-005 (P2)

### TC-081 (P2) -- State resume loads correctly

- **Preconditions:** .hardware/state.md exists from previous session (stages 1-4 complete)
- **Steps:**
  1. Start new session, request resume
  2. Verify pipeline loads state
  3. Verify stages 1-4 not re-executed
  4. Verify pipeline continues from Stage 5
- **Expected Result:** Resume from last completed stage. No re-execution.
- **FR Mapping:** FR-005 (P2)

### TC-082 (P2) -- State file format matches schema

- **Preconditions:** State file exists
- **Steps:**
  1. Verify state file contains: stage, gate results, dispatch errors, rework history, timestamps
  2. Test staleness detection at 7+ days (warning) and 30+ days (critical)
- **Expected Result:** Format matches architecture specification. Staleness detected.
- **FR Mapping:** FR-005 (P2)

### TC-083 (P2) -- Memory lessons captured after run

- **Preconditions:** Pipeline run completed
- **Steps:**
  1. Verify .hardware/memory/ directory created
  2. Verify lessons stored using tiered chunked retrieval
- **Expected Result:** Memory stored in .hardware/memory/.
- **FR Mapping:** FR-006 (P2)

### TC-084 (P2) -- Memory injected into new run

- **Preconditions:** Memory entries exist from previous run
- **Steps:**
  1. Start new pipeline run
  2. Verify relevant memories injected into stage prompts
- **Expected Result:** Past lessons surfaced in new run.
- **FR Mapping:** FR-006 (P2)

### TC-085 (P0) -- Rework path: Prototype -> Schematic

- **Preconditions:** Pipeline at Prototype stage, schematic-level issue identified
- **Steps:**
  1. Trigger rework from Prototype to Schematic
  2. Verify pipeline returns to Schematic with rework reason as context
  3. Verify original Schematic artifacts available
  4. Verify rework reason documented
- **Expected Result:** Pipeline returns to Schematic. Context and artifacts available.
- **FR Mapping:** FR-007

### TC-086 (P0) -- Rework: downstream gates re-validated

- **Preconditions:** Rework from Prototype to Schematic triggered and completed
- **Steps:**
  1. Complete rework at Schematic stage
  2. Verify pipeline resumes forward progression
  3. Verify ALL downstream gates (Layout gate, Prototype gate) are re-validated
  4. Verify no downstream gates skipped
- **Expected Result:** All downstream gates re-evaluated. None skipped.
- **FR Mapping:** FR-007

### TC-087 (P0) -- All 8 rework paths defined and functional

- **Preconditions:** Pipeline orchestrator SKILL.md exists
- **Steps:**
  1. Verify SKILL.md defines all 8 rework paths:
     - Prototype -> Schematic
     - Prototype -> Layout
     - DFM/DFA -> Layout
     - DFM/DFA -> Schematic
     - Compliance -> Schematic
     - Compliance -> Layout
     - Pilot Run -> DFM/DFA
     - Pilot Run -> Schematic
  2. For each path, verify: source stage, target stage, trigger conditions documented
- **Expected Result:** All 8 paths defined with conditions.
- **FR Mapping:** FR-007

### TC-088 (P0) -- Rework history logged correctly

- **Preconditions:** At least one rework loop triggered
- **Steps:**
  1. Inspect pipeline state after rework
  2. Verify rework history includes: trigger reason, source stage, target stage, resolution, iteration count (per path), total rework count
- **Expected Result:** All rework history fields present.
- **FR Mapping:** FR-007, NFR-010

### TC-089 (P0) -- Per-path rework limit enforced (default 3)

- **Preconditions:** Rework has been triggered 3 times on Prototype -> Schematic path
- **Steps:**
  1. Trigger 4th rework on Prototype -> Schematic
  2. Verify pipeline does NOT loop
  3. Verify escalation to human with: rework history for that path, recurring failure pattern, recommendation to intervene
  4. Verify escalation includes: which limit (per-path), count for that path, cumulative history
- **Expected Result:** Pipeline PAUSES. Human escalation with full context.
- **FR Mapping:** FR-007 (C8)

### TC-090 (P0) -- Total rework limit enforced (default 10)

- **Preconditions:** 10 total reworks across all paths in single pipeline run
- **Steps:**
  1. Trigger 11th total rework (any path)
  2. Verify pipeline PAUSES
  3. Verify escalation with: full rework history, all path counts, pattern summary
  4. Verify human decision options: continue, abort, override limit
- **Expected Result:** Pipeline PAUSES. Full escalation with options.
- **FR Mapping:** FR-007 (C8)

---

## Category 6: kicad-happy Integration (FR-009)

### TC-100 (P0) -- Dispatch kicad-happy:kicad from EE context

- **Preconditions:** kicad-happy installed, EE sub-agent active
- **Steps:**
  1. From EE role context, invoke `Skill tool` with `skill: "kicad-happy:kicad"`
  2. Verify SKILL_LOADED signal returned
  3. Verify schematic/PCB analysis output produced
- **Expected Result:** Skill loads. Analysis output returned.
- **FR Mapping:** FR-009

### TC-101 (P0) -- Dispatch kicad-happy:spice from EE context

- **Preconditions:** kicad-happy installed, EE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:spice` from EE context
  2. Verify SKILL_LOADED
  3. Verify simulation results returned
- **Expected Result:** Skill loads. Simulation results returned.
- **FR Mapping:** FR-009

### TC-102 (P0) -- Dispatch kicad-happy:digikey from EE context

- **Preconditions:** kicad-happy installed, EE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:digikey` from EE context
  2. Verify SKILL_LOADED
  3. Verify results include: part number, price, stock quantity, datasheet availability
- **Expected Result:** Skill loads. Part search results with required fields.
- **FR Mapping:** FR-009

### TC-103 (P0) -- Dispatch kicad-happy:mouser from EE context

- **Preconditions:** kicad-happy installed, EE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:mouser` from EE context
  2. Verify SKILL_LOADED and results with price/availability
- **Expected Result:** Skill loads. Results returned.
- **FR Mapping:** FR-009

### TC-104 (P0) -- Dispatch kicad-happy:lcsc from EE context

- **Preconditions:** kicad-happy installed, EE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:lcsc` from EE context
  2. Verify SKILL_LOADED and results
- **Expected Result:** Skill loads. Results returned.
- **FR Mapping:** FR-009

### TC-105 (P0) -- Dispatch kicad-happy:element14 from EE context

- **Preconditions:** kicad-happy installed, EE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:element14` from EE context
  2. Verify SKILL_LOADED and results
- **Expected Result:** Skill loads. Results returned.
- **FR Mapping:** FR-009

### TC-106 (P0) -- Dispatch kicad-happy:jlcpcb from MfgE context

- **Preconditions:** kicad-happy installed, MfgE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:jlcpcb` from MfgE context
  2. Verify SKILL_LOADED
  3. Verify JLCPCB design rules and constraints returned
- **Expected Result:** Skill loads. Fab-specific rules returned.
- **FR Mapping:** FR-009

### TC-107 (P0) -- Dispatch kicad-happy:pcbway from MfgE context

- **Preconditions:** kicad-happy installed, MfgE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:pcbway` from MfgE context
  2. Verify SKILL_LOADED and PCBWay rules returned
- **Expected Result:** Skill loads. Rules returned.
- **FR Mapping:** FR-009

### TC-108 (P0) -- Dispatch kicad-happy:bom from MfgE context

- **Preconditions:** kicad-happy installed, MfgE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:bom` from MfgE context
  2. Verify SKILL_LOADED and BOM validation results
- **Expected Result:** Skill loads. Validation results returned.
- **FR Mapping:** FR-009

### TC-109 (P0) -- Dispatch kicad-happy:emc from CompE context

- **Preconditions:** kicad-happy installed, CompE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:emc` from CompE context
  2. Verify SKILL_LOADED and EMC analysis returned
- **Expected Result:** Skill loads. EMC analysis returned.
- **FR Mapping:** FR-009

### TC-110 (P0) -- Dispatch kicad-happy:kidoc from CompE context

- **Preconditions:** kicad-happy installed, CompE sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:kidoc` from CompE context
  2. Verify SKILL_LOADED and documentation output returned
- **Expected Result:** Skill loads. Documentation generated.
- **FR Mapping:** FR-009

### TC-111 (P0) -- Graceful failure: kicad-happy not installed

- **Preconditions:** kicad-happy removed/renamed
- **Steps:**
  1. Attempt to dispatch any kicad-happy skill
  2. Verify clear error message with installation instructions
  3. Verify message includes: which skill is missing, how to install kicad-happy
- **Expected Result:** Graceful failure. Error message with install instructions. No crash.
- **FR Mapping:** FR-009

### TC-112 (P1) -- Graceful failure: version mismatch

- **Preconditions:** kicad-happy installed but version < required minimum
- **Steps:**
  1. Simulate version mismatch
  2. Verify warning: "kicad-happy version X.Y.Z installed; hardware-team requires >=A.B.C"
- **Expected Result:** Warning displayed. No crash.
- **FR Mapping:** FR-009

### TC-113 (P0) -- Integration layer: role-to-skill mapping

- **Preconditions:** kicad-integration.md (or equivalent) exists
- **Steps:**
  1. Verify mapping documented:
     - EE -> kicad, spice, digikey, mouser, lcsc, element14
     - PCB Layout -> kicad
     - MfgE -> jlcpcb, pcbway, bom
     - CompE -> emc, kidoc
  2. Verify each skill has: dispatch pattern, expected input, expected output
- **Expected Result:** All 11 skills mapped to roles with full documentation.
- **FR Mapping:** FR-009

### TC-114 (P0) -- Non-reimplementation: no .kicad_sch parsing in roles

- **Preconditions:** All 6 role SKILL.md files exist
- **Steps:**
  1. Search all role SKILL.md files for instructions to parse .kicad_sch files directly
  2. Search for instructions to query distributor APIs directly
  3. Search for instructions to implement EMC rule checks from scratch
  4. Search for instructions to generate documentation from scratch
- **Expected Result:** Zero matches. All capabilities delegate to kicad-happy skills.
- **FR Mapping:** FR-009, NFR-003

### TC-115 (P1) -- Reimplementation definition documented

- **Preconditions:** Integration layer documentation exists
- **Steps:**
  1. Verify operational definition: "A capability is reimplemented if a hardware-team role performs an action that would produce the same output as invoking a kicad-happy skill, without invoking that skill."
  2. Verify IS/IS NOT examples are included
- **Expected Result:** Definition documented with examples.
- **FR Mapping:** FR-009, NFR-003

### TC-116 (P1) -- Config-driven fab dispatch: JLCPCB

- **Preconditions:** Config target_fab: jlcpcb
- **Steps:**
  1. Trigger DFM validation from MfgE context
  2. Verify kicad-happy:jlcpcb dispatched (not pcbway)
- **Expected Result:** JLCPCB skill dispatched per config.
- **FR Mapping:** FR-009, FR-013

### TC-117 (P1) -- Config-driven fab dispatch: PCBWay

- **Preconditions:** Config target_fab: pcbway
- **Steps:**
  1. Trigger DFM validation from MfgE context
  2. Verify kicad-happy:pcbway dispatched (not jlcpcb)
- **Expected Result:** PCBWay skill dispatched per config.
- **FR Mapping:** FR-009, FR-013

### TC-118 (P1) -- Dispatch kicad-happy:kicad from PCB Layout context

- **Preconditions:** kicad-happy installed, Layout sub-agent active
- **Steps:**
  1. Invoke `kicad-happy:kicad` from Layout role
  2. Verify SKILL_LOADED and PCB analysis
- **Expected Result:** Skill loads from Layout context.
- **FR Mapping:** FR-009

### TC-119 (P1) -- Dispatch kicad-happy:kidoc from MfgE context

- **Preconditions:** kicad-happy installed, MfgE at Production Release
- **Steps:**
  1. Invoke `kicad-happy:kidoc` from MfgE context for manufacturing transfer package
  2. Verify documentation output
- **Expected Result:** kidoc accessible from MfgE as well as CompE.
- **FR Mapping:** FR-009

### TC-120 (P1) -- Dependency documentation: prerequisites.md

- **Preconditions:** hardware-team/references/prerequisites.md (or equivalent) exists
- **Steps:**
  1. Verify document states: kicad-happy is required dependency
  2. Verify installation mechanism documented (Claude Code plugin system)
  3. Verify minimum version specified
  4. Verify step-by-step instructions included
- **Expected Result:** Complete dependency documentation.
- **FR Mapping:** FR-009

---

## Category 7: Security Controls

### TC-130 (P1) -- YAML safe_load enforced

- **Preconditions:** All Python scripts that load YAML exist
- **Steps:**
  1. Search all .py files in hardware-team/ for `yaml.load(`
  2. Verify every YAML loading call uses `yaml.safe_load()` or `yaml.SafeLoader`
  3. Verify no use of `yaml.load()` with `Loader=yaml.FullLoader` or `yaml.UnsafeLoader`
- **Expected Result:** All YAML loading is safe. Zero unsafe load calls.
- **FR Mapping:** Security (NFR)

### TC-131 (P1) -- Path sanitization: no traversal

- **Preconditions:** All Python scripts that construct file paths exist
- **Steps:**
  1. Review path construction in config validation, state management, hook scripts
  2. Verify paths are joined safely (os.path.join or pathlib)
  3. Verify no raw string concatenation with user-provided path segments
  4. Test: inject `../../etc/passwd` as config path input, verify rejection
- **Expected Result:** Path traversal prevented. Unsafe paths rejected.
- **FR Mapping:** Security (NFR)

### TC-132 (P1) -- Hook scripts: no arbitrary code execution

- **Preconditions:** All hook .py scripts exist
- **Steps:**
  1. Review each hook script for: eval(), exec(), subprocess with shell=True, os.system()
  2. Verify no user input passed directly to any of these
- **Expected Result:** Zero arbitrary code execution vectors.
- **FR Mapping:** Security (NFR)

### TC-133 (P1) -- Config validation: no injection

- **Preconditions:** validate_config.py exists
- **Steps:**
  1. Create config with YAML injection payloads (e.g., `!!python/object/apply:os.system ["echo pwned"]`)
  2. Run validate_config.py
  3. Verify yaml.safe_load rejects the payload
- **Expected Result:** Injection payload rejected. No code execution.
- **FR Mapping:** Security (NFR)

### TC-134 (P1) -- NFR-001: no external Python dependencies

- **Preconditions:** All .py files in hardware-team/ exist
- **Steps:**
  1. Run `grep -rn "^import \|^from " hardware-team/scripts/ hardware-team/hooks/`
  2. Verify every import is a Python standard library module
  3. Check for: no pip, no requirements.txt, no setup.py with external deps
- **Expected Result:** Zero non-stdlib imports.
- **FR Mapping:** NFR-001

### TC-135 (P1) -- Hook scripts compile cleanly

- **Preconditions:** All hook .py scripts exist
- **Steps:**
  1. Run `python -m py_compile hardware-team/hooks/<each_script>.py`
  2. Verify exit 0 for each
- **Expected Result:** All scripts compile without errors.
- **FR Mapping:** NFR-001

---

## Category 8: Validation Gates Against Reference Fixture (FR-010 through FR-014, FR-022)

### TC-400 (P0) -- Reference fixture: all files present

- **Preconditions:** hardware-team/references/test-fixtures/ exists
- **Steps:**
  1. Verify presence of: reference.kicad_sch, reference.kicad_pcb, reference-bom.csv, reference-pricing.json, MANIFEST.md
- **Expected Result:** All 5 files present.
- **FR Mapping:** FR-022

### TC-401 (P0) -- Reference fixture: schematic defect count

- **Preconditions:** MANIFEST.md exists
- **Steps:**
  1. Count schematic defects in MANIFEST.md
  2. Verify exactly 10 defects across 7 categories: power integrity, signal integrity, component derating, missing pull-ups, decoupling, voltage level compatibility, thermal
- **Expected Result:** 10 defects, 7 categories.
- **FR Mapping:** FR-022

### TC-402 (P0) -- Reference fixture: BOM issue types

- **Preconditions:** MANIFEST.md and reference-bom.csv exist
- **Steps:**
  1. Verify BOM contains at least 4 issue types: 1 obsolete, 1 budget-exceeding, 1 single-source, 1 NRND
- **Expected Result:** All 4 BOM issue types present.
- **FR Mapping:** FR-022

### TC-403 (P0) -- Reference fixture: PCB DFM violations

- **Preconditions:** MANIFEST.md and reference.kicad_pcb exist
- **Steps:**
  1. Verify PCB contains at least 4 violation types: trace width below JLCPCB minimum, via size below minimum, solder mask aperture violation, clearance violation
- **Expected Result:** All 4 DFM violation types present.
- **FR Mapping:** FR-022

### TC-404 (P0) -- Reference fixture: pricing data offline

- **Preconditions:** reference-pricing.json exists
- **Steps:**
  1. Parse reference-pricing.json
  2. Verify it contains fixed pricing for all BOM line items
  3. Verify no live API call required
- **Expected Result:** Offline pricing data complete. No API dependency.
- **FR Mapping:** FR-022

### TC-405 (P0) -- Reference fixture: MANIFEST completeness

- **Preconditions:** MANIFEST.md exists
- **Steps:**
  1. Verify each defect has: defect ID, category, location in KiCad file, expected detection gate, expected severity
  2. Verify total defects >= 18 (10 schematic + 4 BOM + 4 PCB)
- **Expected Result:** All defects fully documented. >= 18 total.
- **FR Mapping:** FR-022

### TC-406 (P1) -- Reference fixture: cross-reference locations

- **Preconditions:** All fixture files exist
- **Steps:**
  1. Cross-reference MANIFEST.md defect locations against actual KiCad file content
  2. Verify locations are real (components/nets/layers exist in the files)
- **Expected Result:** All documented locations exist in the files.
- **FR Mapping:** FR-022

### TC-140 (P0) -- Schematic Review Gate: iterative multi-reviewer

- **Preconditions:** Reference fixture available, Schematic Review Gate configured
- **Steps:**
  1. Run Schematic Review Gate against reference.kicad_sch
  2. Verify iterative review with forced-find prompting applied
  3. Verify multiple reviewers with deduplication across passes
- **Expected Result:** Iterative review executed. Deduplication applied.
- **FR Mapping:** FR-010

### TC-141 (P0) -- Schematic Review Gate: 7 categories checked

- **Preconditions:** Gate running against reference fixture
- **Steps:**
  1. Verify all 7 review categories covered: power integrity, signal integrity, component derating, missing pull-ups/pull-downs, decoupling strategy, voltage level compatibility, thermal considerations
- **Expected Result:** All 7 categories evaluated.
- **FR Mapping:** FR-010

### TC-142 (P0) -- Schematic Review Gate: >= 6/7 category detection

- **Preconditions:** Gate run against reference.kicad_sch with 10 seeded defects
- **Steps:**
  1. Count detected categories from gate output
  2. Compare against MANIFEST.md expected categories
  3. Verify >= 6/7 categories detected (>80%)
- **Expected Result:** KEY METRIC: >= 6/7 categories detected.
- **FR Mapping:** FR-010

### TC-143 (P0) -- Schematic Review Gate: finding format

- **Preconditions:** Gate has findings
- **Steps:**
  1. Verify each finding includes: finding ID, severity (critical/major/minor), location (sheet/component/net), description, recommended fix
- **Expected Result:** All findings have complete metadata.
- **FR Mapping:** FR-010

### TC-144 (P0) -- Schematic Review Gate: critical blocks pipeline

- **Preconditions:** Gate has critical finding(s)
- **Steps:**
  1. Verify gate returns NOT_DONE when any critical finding exists
  2. Verify pipeline does not advance to Layout stage
- **Expected Result:** Critical finding blocks advancement.
- **FR Mapping:** FR-010

### TC-145 (P0) -- DRC Gate: consumes kicad-happy:kicad

- **Preconditions:** Reference.kicad_pcb available, kicad-happy installed
- **Steps:**
  1. Run DRC Gate against reference.kicad_pcb
  2. Verify gate dispatches to kicad-happy:kicad for DRC parsing
  3. Verify SKILL_LOADED from kicad-happy:kicad
- **Expected Result:** DRC consumes kicad-happy:kicad. No reimplementation.
- **FR Mapping:** FR-011

### TC-146 (P0) -- DRC Gate: detects all 4 violation types

- **Preconditions:** Gate running against reference fixture
- **Steps:**
  1. Verify all 4 seeded DFM violations detected: trace width, via size, solder mask, clearance
  2. Cross-reference against MANIFEST.md
- **Expected Result:** 4/4 violation types detected.
- **FR Mapping:** FR-011

### TC-147 (P1) -- DRC Gate: violation format

- **Preconditions:** Gate has violations
- **Steps:**
  1. Verify each violation includes: rule violated, location (layer/coordinates), severity, remediation
- **Expected Result:** All violations have complete metadata.
- **FR Mapping:** FR-011

### TC-148 (P1) -- DRC Gate: DONE/NOT_DONE logic

- **Preconditions:** Gate running
- **Steps:**
  1. Verify: zero errors -> DONE
  2. Verify: warnings only -> DONE (warnings documented)
  3. Verify: any errors -> NOT_DONE
- **Expected Result:** Correct DONE/NOT_DONE logic.
- **FR Mapping:** FR-011

### TC-150 (P0) -- BOM Gate: lifecycle check blocks NRND/obsolete

- **Preconditions:** Reference-bom.csv with NRND and obsolete components
- **Steps:**
  1. Run BOM Gate against reference BOM
  2. Verify NRND component flagged and blocks advancement
  3. Verify obsolete component flagged and blocks advancement
- **Expected Result:** Gate returns NOT_DONE. Lifecycle issues block.
- **FR Mapping:** FR-012

### TC-151 (P0) -- BOM Gate: budget check

- **Preconditions:** Config bom_budget set, reference BOM exceeds budget
- **Steps:**
  1. Run BOM Gate with budget-exceeding BOM
  2. Verify gate returns NOT_DONE with cost breakdown and budget variance
- **Expected Result:** Budget exceeded -> NOT_DONE with breakdown.
- **FR Mapping:** FR-012

### TC-152 (P0) -- BOM Gate: single-source warning

- **Preconditions:** Reference BOM with single-source component
- **Steps:**
  1. Run BOM Gate
  2. Verify single-source flagged as warning (not blocking unless config requires second-source)
- **Expected Result:** Single-source risk flagged as warning.
- **FR Mapping:** FR-012

### TC-153 (P0) -- BOM Gate: offline testability

- **Preconditions:** reference-pricing.json available
- **Steps:**
  1. Run BOM Gate with reference-pricing.json (no live API calls)
  2. Verify budget threshold testing works against static data
- **Expected Result:** Gate operates offline using static pricing.
- **FR Mapping:** FR-012

### TC-155 (P0) -- DFM Gate: fab-specific rules (JLCPCB)

- **Preconditions:** Config target_fab: jlcpcb, reference.kicad_pcb available
- **Steps:**
  1. Run DFM Gate with JLCPCB target
  2. Verify kicad-happy:jlcpcb dispatched
  3. Verify JLCPCB-specific constraints applied (minimum trace/space, via sizes, etc.)
- **Expected Result:** JLCPCB rules applied via kicad-happy:jlcpcb.
- **FR Mapping:** FR-013

### TC-156 (P0) -- DFM Gate: detects all 4 seeded violations

- **Preconditions:** Gate running against reference fixture with JLCPCB target
- **Steps:**
  1. Verify all 4 reference DFM violations detected
  2. Cross-reference against MANIFEST.md
- **Expected Result:** 4/4 violations detected.
- **FR Mapping:** FR-013

### TC-157 (P1) -- DFM Gate: violation format

- **Preconditions:** Gate has violations
- **Steps:**
  1. Verify each violation includes: rule violated, current value, required value, location, remediation
- **Expected Result:** All violations have complete metadata including current vs. required values.
- **FR Mapping:** FR-013

### TC-158 (P1) -- DFM Gate: DONE/NOT_DONE logic

- **Preconditions:** Gate running
- **Steps:**
  1. Verify: zero violations -> DONE
  2. Verify: any violations -> NOT_DONE with remediation plan
- **Expected Result:** Correct DONE/NOT_DONE logic.
- **FR Mapping:** FR-013

### TC-160 (P0) -- Compliance Gate: per-region checklists

- **Preconditions:** Config compliance_regions: [FCC, CE]
- **Steps:**
  1. Run Compliance Gate
  2. Verify separate checklist produced for FCC
  3. Verify separate checklist produced for CE
- **Expected Result:** One checklist per configured region.
- **FR Mapping:** FR-014

### TC-161 (P0) -- Compliance Gate: evidence linking

- **Preconditions:** Compliance Gate running with compliance artifacts
- **Steps:**
  1. Verify each requirement in checklist linked to: standard clause, evidence artifact, pass/fail status
- **Expected Result:** All requirements evidence-linked.
- **FR Mapping:** FR-014

### TC-162 (P0) -- Compliance Gate: missing evidence blocks

- **Preconditions:** Some compliance requirements have no linked evidence
- **Steps:**
  1. Verify gate returns NOT_DONE
  2. Verify missing evidence items listed
- **Expected Result:** Missing evidence -> NOT_DONE with list.
- **FR Mapping:** FR-014

### TC-163 (P0) -- Compliance Gate: consumes kicad-happy:emc

- **Preconditions:** kicad-happy installed
- **Steps:**
  1. Verify Compliance Gate dispatches to kicad-happy:emc for EMC pre-compliance
  2. Verify SKILL_LOADED from kicad-happy:emc
- **Expected Result:** EMC analysis delegated to kicad-happy. No reimplementation.
- **FR Mapping:** FR-014

---

## Category 9: Design Review Board (FR-015)

### TC-170 (P0) -- Design Review Board: multi-role dispatch

- **Preconditions:** Design artifact (schematic) ready, Design Review Board pattern configured
- **Steps:**
  1. Trigger Design Review Board on reference schematic
  2. Verify 3+ roles dispatched as independent reviewers (EE, Layout, MfgE, CompE)
  3. Verify each reviewer is a separate sub-agent invocation
- **Expected Result:** 3+ roles review independently. Separate sub-agents.
- **FR Mapping:** FR-015

### TC-171 (P0) -- Design Review Board: findings deduplication

- **Preconditions:** Multiple reviewers have produced findings
- **Steps:**
  1. Aggregate findings from all reviewers
  2. Verify deduplication applied (same finding from multiple reviewers merged)
- **Expected Result:** Duplicates merged. Each unique finding appears once.
- **FR Mapping:** FR-015

### TC-172 (P0) -- Design Review Board: results organized by role

- **Preconditions:** Review board complete
- **Steps:**
  1. Verify results presented organized by reviewer role
  2. Verify unified severity ranking applied across all roles
- **Expected Result:** Role-organized results with unified severity.
- **FR Mapping:** FR-015

### TC-173 (P1) -- Design Review Board: no shared context

- **Preconditions:** Review board running
- **Steps:**
  1. Verify each reviewer operates independently (no shared context between reviewers during review)
  2. Verify based on adversarial review pattern from delivery-team
- **Expected Result:** Context isolation during review confirmed.
- **FR Mapping:** FR-015

---

## Category 10: P2 Deferred Tests (FR-005, FR-006, FR-016)

### TC-175 (P3) -- BOM Reconciliation: multi-supplier query

- **Preconditions:** BOM ready, multiple sourcing skills available
- **Steps:**
  1. Submit BOM for reconciliation
  2. Verify multiple kicad-happy sourcing skills queried per line item
  3. Verify >20% pricing discrepancies flagged
- **Expected Result:** Multi-supplier comparison with discrepancy flagging.
- **FR Mapping:** FR-016 (P2)

### TC-176 (P3) -- BOM Reconciliation: single-source identification

- **Preconditions:** BOM with single-source components
- **Steps:**
  1. Run reconciliation
  2. Verify single-source risks identified across all suppliers queried
- **Expected Result:** Single-source flagged.
- **FR Mapping:** FR-016 (P2)

---

## Category 11: NFR Verification

### TC-180 (P1) -- NFR-005 gate message quality

- **Preconditions:** At least one gate has produced findings
- **Steps:**
  1. Review gate output messages from all 5 gates
  2. Verify each message includes: (a) what failed, (b) where (component/net/location), (c) why, (d) how to fix
- **Expected Result:** All 4 elements present in every gate message.
- **FR Mapping:** NFR-005

### TC-181 (P1) -- NFR-009 plugin-validator passes

- **Preconditions:** hardware-team plugin structurally complete
- **Steps:**
  1. Run `plugin-dev:plugin-validator` on hardware-team
  2. Verify 0 validation errors
- **Expected Result:** Plugin passes validation.
- **FR Mapping:** NFR-009

### TC-182 (P1) -- NFR-004 full pipeline completion

- **Preconditions:** Reference project, kicad-happy installed
- **Steps:**
  1. Run full 8-stage pipeline end-to-end
  2. Verify all stages complete in single session
  3. Verify all artifacts produced
- **Expected Result:** Pipeline completes without session timeout.
- **FR Mapping:** NFR-004

---

## FR Traceability Summary

| FR ID | Test Cases | Coverage |
|-------|------------|----------|
| FR-001 | TC-001, TC-002, TC-003, TC-004, TC-005 | Complete |
| FR-002 | TC-060, TC-061, TC-062, TC-063, TC-064, TC-065 | Complete |
| FR-003 | TC-070, TC-071, TC-072, TC-073, TC-074 | Complete |
| FR-004 | TC-050, TC-051, TC-052, TC-053, TC-054, TC-055, TC-056, TC-057, TC-058 | Complete |
| FR-005 | TC-080, TC-081, TC-082 | P2 deferred |
| FR-006 | TC-083, TC-084 | P2 deferred |
| FR-007 | TC-085, TC-086, TC-087, TC-088, TC-089, TC-090 | Complete |
| FR-008 | TC-010 through TC-023 | Complete |
| FR-009 | TC-100 through TC-120 | Complete |
| FR-010 | TC-140, TC-141, TC-142, TC-143, TC-144 | Complete |
| FR-011 | TC-145, TC-146, TC-147, TC-148 | Complete |
| FR-012 | TC-150, TC-151, TC-152, TC-153 | Complete |
| FR-013 | TC-155, TC-156, TC-157, TC-158 | Complete |
| FR-014 | TC-160, TC-161, TC-162, TC-163 | Complete |
| FR-015 | TC-170, TC-171, TC-172, TC-173 | Complete |
| FR-016 | TC-175, TC-176 | P2 deferred |
| FR-017 | TC-030, TC-031, TC-032, TC-033, TC-034, TC-035, TC-036, TC-041, TC-042 | Complete |
| FR-018 | TC-037, TC-038 | P2 deferred |
| FR-019 | TC-039, TC-040 | P2 deferred |
| FR-020 | TC-066, TC-067 | Complete |
| FR-021 | N/A | P2 explicitly deferred |
| FR-022 | TC-400, TC-401, TC-402, TC-403, TC-404, TC-405, TC-406 | Complete |

**Total test cases:** 103
**P1 FR coverage:** 21/21 (100%)
**P2 FR deferred:** FR-005, FR-006, FR-016, FR-018, FR-019, FR-021

---

*"One hundred and three arrows. One hundred and three marks. The wind is steady and the bow is true. That bug still only counts as one."* -- Legolas
