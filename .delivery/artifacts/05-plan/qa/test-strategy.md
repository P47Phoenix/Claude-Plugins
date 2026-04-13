# Test Strategy: hardware-team Plugin

**Author:** QA Engineer (Legolas)
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12
**PRD Version:** 1.1 | **Architecture Version:** 1.4
**Stories Version:** aligned to PRD 1.1

---

> "My eyes see far, and they see every defect. That bug still only counts as one -- but I shall find them all before they reach the prototype stage."

---

## 1. Test Strategy Overview

### 1.1 Scope

This test strategy covers the hardware-team plugin -- a GREENFIELD Claude Code plugin that orchestrates 8-stage hardware development pipelines by consuming kicad-happy skills as building blocks. The plugin comprises:

- 1 pipeline orchestrator (hardware-flow)
- 6 role skills (HW PO, EE, PCB Layout, MfgE, CompE, TestE)
- 5 validation gates (Schematic Review, DRC, BOM, DFM, Compliance)
- 1 integration layer (11 kicad-happy skills consumed)
- 4 hooks (2 SessionStart, 1 PreToolUse, 1 PostToolUse)
- 2 collaboration patterns (Design Review Board, BOM Reconciliation)
- 1 reference test fixture (seeded KiCad project)
- Python scripts (config validation, state management)

### 1.2 Test Objectives

1. Verify all 22 PRD functional requirements are satisfied
2. Verify all 10 non-functional requirements are met
3. Verify cross-plugin skill invocation works correctly for all 11 kicad-happy skills
4. Verify pipeline orchestration: stage routing, gate enforcement, rework loops, state persistence
5. Verify context isolation: each role loads only its own references
6. Verify the reference test fixture provides measurable benchmarks for all 5 gates

### 1.3 Test Approach Summary

| Test Level | Focus | Method | Automation |
|------------|-------|--------|------------|
| Unit | Python scripts, config validation, state management | Manual execution + assertions | Python scripts with assert statements |
| Integration | Cross-plugin skill invocation, role-to-kicad-happy dispatch | Live Skill tool invocation | Semi-automated (scripted invocations) |
| System | Full pipeline run (8 stages, gates, rework) | End-to-end pipeline execution | Manual with checklist |
| Acceptance | PRD FR verification, NFR compliance | FR-by-FR verification matrix | Manual with traceability matrix |

### 1.4 Quality Gate: Entry/Exit Criteria

**Entry Criteria (before testing begins):**
- Plugin skeleton (US-101) is created and structurally complete
- kicad-happy plugin is installed at `~/.claude/plugins/cache/kicad-happy/`
- Reference test fixture (US-400) is complete with all seeded defects documented in MANIFEST.md
- All P1 stories are developer-complete (code complete, self-tested)

**Exit Criteria (before test phase is DONE):**
- All P1 FR test cases pass (100% pass rate required)
- All P1 NFR verifications pass
- All 5 validation gates tested against reference test fixture
- Schematic Review Gate achieves >80% category detection rate (6/7 categories)
- Zero critical defects open
- FR traceability matrix complete (all 22 FRs mapped to at least one executed test)

---

## 2. Test Levels

### 2.1 Unit Testing

**Scope:** Individual Python scripts and isolated components.

| Component | Script Path | Test Approach |
|-----------|-------------|---------------|
| Config validation | `hardware-team/skills/hardware-flow/scripts/validate_config.py` | Execute with valid config, invalid config, missing config, outdated schema version. Assert correct output for each. |
| State manager | `hardware-team/scripts/state_manager.py` | Execute read/write operations. Assert state file format matches architecture Section 3.1.1 schema. Test staleness calculation. |
| Config schema hook | `hardware-team/hooks/check_hw_config.py` | Execute with config present/absent/invalid. Assert correct warning messages. |
| kicad-happy check hook | `hardware-team/hooks/check_kicad_happy.py` | Execute with kicad-happy installed/partially installed/missing. Assert correct availability report. |
| Pipeline bypass hook | `hardware-team/hooks/check_pipeline_bypass.py` | Execute with PreToolUse event for role skill invocation inside/outside pipeline. Assert correct warning. |
| KiCad file hook | `hardware-team/hooks/check_kicad_file.py` | Execute with PostToolUse event for .kicad_sch file edit. Assert DRC notification. |

**Unit test execution pattern:**
```bash
# Each script is tested by direct invocation with controlled inputs
python hardware-team/hooks/check_hw_config.py  # with .hardware/config.yml present
python hardware-team/hooks/check_hw_config.py  # with .hardware/config.yml absent
python hardware-team/skills/hardware-flow/scripts/validate_config.py test-config.yml
```

**Constraints (from memory lessons):** No external dependencies beyond Python standard library (NFR-001). All test scripts must use only stdlib imports.

### 2.2 Integration Testing

**Scope:** Cross-component interactions, cross-plugin skill invocation.

| Integration Point | Components | Test Approach |
|--------------------|------------|---------------|
| kicad-happy skill dispatch | Role SKILL.md + Skill tool + kicad-happy skills | Invoke each of the 11 kicad-happy skills via Skill tool from hardware-team context. Verify SKILL_LOADED signal returns. |
| Role-to-orchestrator | hardware-flow SKILL.md + role SKILL.md | Invoke a role skill via Agent tool from orchestrator context. Verify role produces expected artifact type. |
| Gate-to-role | Gate framework + role skill | Trigger a gate after role completes. Verify gate receives role output and evaluates it. |
| Config-to-pipeline | Config loader + pipeline orchestrator | Load config with specific settings (target_fab, compliance_regions). Verify downstream stages receive config values. |
| Hook-to-event | hooks.json + hook scripts | Trigger SessionStart, PreToolUse, PostToolUse events. Verify hooks fire and produce correct output. |

### 2.3 System Testing

**Scope:** Full pipeline execution end-to-end.

**Test scenarios:**

1. **Happy path:** Execute full 8-stage pipeline on reference test fixture project. Verify all stages execute in order, all gates evaluate, all artifacts are produced.
2. **Rework path:** Trigger rework from Prototype->Schematic. Verify pipeline returns to Schematic, re-executes, re-validates downstream gates.
3. **Gate blocking:** Execute pipeline with reference test fixture defects. Verify gates block advancement on critical findings.
4. **Config variations:** Execute pipeline with different configs (JLCPCB vs PCBWay target fab, different compliance regions). Verify config-driven behavior.
5. **State persistence:** Execute pipeline partially, end session, resume. Verify state loads correctly and pipeline continues from last completed stage.
6. **Rework termination:** Trigger rework loop 4 times on same path (exceeding default limit of 3). Verify escalation to human.

### 2.4 Acceptance Testing

**Scope:** PRD FR and NFR verification.

Every functional requirement is verified against its acceptance criteria using the FR traceability matrix (Section 7). Acceptance testing is performed by walking through each FR's acceptance criteria and executing the mapped test cases.

---

## 3. Test Approach Per Story

### Epic 1: Plugin Foundation & Pipeline Orchestrator

| Story | Acceptance Criteria Verification Approach |
|-------|-------------------------------------------|
| **US-101: Plugin Skeleton** | **Structural inspection.** Verify directory structure matches architecture Section 1.1 layout using `ls -R hardware-team/`. Verify SKILL.md loads in Claude Code harness (invoke `hardware-team` skill, check for SKILL_LOADED). Verify marketplace.json does NOT contain hardware-team (grep). Verify 7 sub-skill directories exist with placeholder SKILL.md files. |
| **US-102: Pipeline Orchestrator** | **Pipeline execution.** Start pipeline on reference project. Verify Stage 1 (Concept) executes first. Advance through stages, verify sequential progression. Inspect orchestrator SKILL.md for "Prime Directive" guardrail language. Verify sub-agent dispatch uses Agent tool (inspect orchestrator prompt for Agent tool invocation patterns). Verify human-execution stages (4, 7, 8) pause for human confirmation. Test dispatch failure: simulate by invoking a non-existent skill, verify retry-then-pause protocol. |
| **US-103: Gate Validation Framework** | **Gate logic testing.** Create a mock gate with 3 validators. Set 2 DONE + 1 NOT_DONE, verify pipeline blocks. Set all 3 DONE, verify pipeline advances. Verify failing validator feedback is returned. Inspect gate-framework.md for all 5 gate types + Human Confirmation Gate. Verify each validator has unique ID, description, pass/fail criteria. |
| **US-104: Config Pipeline** | **Config validation.** Run validate_config.py against: (a) valid config, (b) absent config, (c) invalid config, (d) outdated schema. Verify defaults are used for absent/invalid. Verify config schema includes: version, target_fab, compliance_regions, bom_budget, dependencies.kicad_happy_version, max_rework_iterations, max_total_reworks, staleness thresholds. |
| **US-105: State Persistence** (P2) | **Session resume test.** Execute pipeline through Stage 4. End session. Start new session. Resume pipeline. Verify stages 1-4 are not re-executed. Verify state_manager.py reads/writes .hardware/state.md with correct fields. Test staleness detection at 7+ and 30+ days. |
| **US-106: Self-Learning Memory** (P2) | **Memory injection test.** Complete a pipeline run. Verify lessons stored in .hardware/memory/. Start new pipeline run. Verify relevant memories are injected into stage prompts. Benchmark retrieval time with 100+ entries (NFR-008 target: <2s). |
| **US-107: Rework Loop Support** | **Rework path testing.** Test each of 8 rework paths: Prototype->Schematic, Prototype->Layout, DFM/DFA->Layout, DFM/DFA->Schematic, Compliance->Schematic, Compliance->Layout, Pilot Run->DFM/DFA, Pilot Run->Schematic. For each: verify rework reason is passed as context, verify original artifacts are available, verify downstream gates re-validate. Test per-path limit (trigger 4th rework on same path, verify escalation). Test total limit (trigger 11th total rework, verify escalation). Verify rework history fields: trigger reason, source stage, target stage, resolution, iteration count, total count. |
| **US-108: Marketplace Registration** | **Registry validation.** Verify marketplace.json contains hardware-team entry with unique ID, display name, description, 7 skill paths. Verify no ID conflicts. Verify description mentions kicad-happy dependency. |

### Epic 2: Core Hardware Roles

| Story | Acceptance Criteria Verification Approach |
|-------|-------------------------------------------|
| **US-201: HW Product Owner** | **Skill isolation test.** Load hw-product-owner skill. Verify it loads ONLY HW PO references (hw-requirements.md, feasibility-analysis.md, make-vs-buy.md). Invoke during Concept stage. Verify outputs: requirements document, constraint matrix, regulatory landscape scan, initial BOM budget. Verify model tier is specified in SKILL.md. |
| **US-202: Electrical Engineer** | **Skill isolation + kicad-happy consumption.** Load electrical-engineer skill. Verify it loads ONLY EE references (5 files). Invoke during Schematic stage. Verify component search CONSUMES kicad-happy skills (digikey, mouser, lcsc, element14) -- not reimplemented. Verify SPICE simulation CONSUMES kicad-happy:spice. Verify firmware interface documentation is produced (pin assignment table, power domain map, bus interface spec, debug access points). Verify iterative review uses forced-find prompting. Verify model tier is Sonnet+. |
| **US-203: PCB Layout Engineer** | **Skill isolation + kicad-happy consumption.** Load pcb-layout-engineer skill. Verify it loads ONLY Layout references (3 files). Verify KiCad analysis CONSUMES kicad-happy:kicad. Verify model tier is Sonnet+. |
| **US-204: Manufacturing Engineer** | **Skill isolation + kicad-happy consumption.** Load manufacturing-engineer skill. Verify it loads ONLY MfgE references (4 files). Verify DFM evaluation CONSUMES kicad-happy:jlcpcb and kicad-happy:pcbway. Verify BOM validation CONSUMES kicad-happy:bom. Verify DFM gate checks all required categories. |
| **US-205: Compliance Engineer** | **Skill isolation + kicad-happy consumption.** Load compliance-engineer skill. Verify it loads ONLY CompE references (4 files). Verify EMC analysis CONSUMES kicad-happy:emc. Verify documentation CONSUMES kicad-happy:kidoc. Verify compliance checklist covers all configured regions. |
| **US-206: Test Engineer** | **Skill isolation.** Load test-engineer skill. Verify it loads ONLY TestE references (4 files). Invoke during Prototype stage. Verify outputs: test strategy document, test fixture requirements, bring-up test procedure, validation acceptance criteria. Verify test strategy covers: functional, environmental, reliability, production screening. |

### Epic 3: kicad-happy Integration Layer

| Story | Acceptance Criteria Verification Approach |
|-------|-------------------------------------------|
| **US-301: Integration Architecture** | **Document review + dispatch test.** Verify kicad-integration.md documents all 11 kicad-happy skills with: consuming role(s), stage(s), dispatch pattern, expected input/output. Test dispatch to each of 11 skills via Skill tool. Test graceful failure: temporarily rename kicad-happy install directory, attempt dispatch, verify error message with installation instructions. Verify reimplementation definition with IS/IS NOT examples. |
| **US-302: Component Sourcing** | **Live dispatch test.** From EE role context, invoke kicad-happy:digikey, kicad-happy:mouser, kicad-happy:lcsc, kicad-happy:element14. Verify results include: part number, price, stock quantity, datasheet availability. Verify multi-distributor comparison. |
| **US-303: Fabrication Integration** | **Config-driven dispatch test.** Set config target_fab to jlcpcb, invoke DFM validation, verify kicad-happy:jlcpcb is dispatched. Change to pcbway, verify kicad-happy:pcbway is dispatched. Verify fab-specific constraints are applied. |
| **US-304: Analysis Integration** | **Analysis dispatch test.** Verify EE invokes kicad-happy:spice for simulation. Verify CompE invokes kicad-happy:emc for EMC analysis. Verify analysis results are stored as stage artifacts. |
| **US-305: Documentation Integration** | **Documentation dispatch test.** Verify CompE invokes kicad-happy:kidoc during Compliance stage. Verify MfgE invokes kicad-happy:kidoc + kicad-happy:bom during Production Release. Verify artifact provenance is recorded. |
| **US-306: Dependency Documentation** | **Prerequisites review + hook test.** Verify prerequisites.md documents: kicad-happy as required dependency, installation mechanism, minimum version, step-by-step instructions. Verify config includes kicad_happy_version field. Run SessionStart hook, verify 11/11 report. Remove kicad-happy, verify error message. |

### Epic 4: Hardware-Specific Validation Gates

| Story | Acceptance Criteria Verification Approach |
|-------|-------------------------------------------|
| **US-400: Reference Test Fixture** | **Fixture completeness audit.** Verify test-fixtures/ contains: reference.kicad_sch, reference.kicad_pcb, reference-bom.csv, reference-pricing.json, MANIFEST.md. Verify MANIFEST.md lists each defect with: defect ID, category, location, expected detection gate, expected severity. Count schematic defects: exactly 10 across 7 categories. Count BOM issues: at least 4 types (obsolete, budget-exceeding, single-source, NRND). Count PCB violations: at least 4 types (trace width, via size, solder mask, clearance). Verify reference-pricing.json is offline-testable (no live API calls needed). |
| **US-401: Schematic Review Gate** | **Gate execution against test fixture.** Run Schematic Review Gate against reference.kicad_sch. Verify iterative review with forced-find prompting is applied. Verify all 7 review categories are checked. Verify deduplication across reviewers. Verify findings include: ID, severity, location, description, recommended fix. Verify critical findings block pipeline. **KEY METRIC:** Count categories detected -- must achieve >= 6/7 (>80%). |
| **US-402: DRC Gate** | **Gate execution against test fixture.** Run DRC Gate against reference.kicad_pcb. Verify it CONSUMES kicad-happy:kicad. Verify violations include: rule, location, severity, remediation. Verify gate returns DONE with warnings only, NOT_DONE with errors. Verify all 4 DFM violation types in reference PCB are detected. |
| **US-403: BOM Gate** | **Gate execution against test fixture.** Run BOM Gate against reference-bom.csv + reference-pricing.json. Verify lifecycle check: NRND/obsolete blocks advancement. Verify budget check: total exceeding budget blocks. Verify single-source flagged as warning. Verify offline testability (no live API calls). |
| **US-404: DFM Gate** | **Gate execution against test fixture.** Run DFM Gate against reference.kicad_pcb with target_fab=jlcpcb. Verify JLCPCB-specific rules applied (consuming kicad-happy:jlcpcb). Verify violations include: current value, required value, location, remediation. Verify all 4 reference DFM violations are detected. |
| **US-405: Compliance Gate** | **Gate execution with config.** Set compliance_regions to [FCC, CE]. Run Compliance Gate. Verify checklist generated for each region. Verify evidence linking. Verify missing evidence blocks advancement. Verify EMC analysis CONSUMES kicad-happy:emc. |

### Epic 5: Collaboration Patterns & Hooks

| Story | Acceptance Criteria Verification Approach |
|-------|-------------------------------------------|
| **US-501: Design Review Board** | **Multi-role review test.** Trigger Design Review Board on reference schematic. Verify 3+ roles (EE, Layout, MfgE, CompE) review independently. Verify findings are deduplicated. Verify results organized by role with unified severity ranking. Verify no shared context between reviewers during review. |
| **US-502: BOM Reconciliation** (P2) | **Multi-supplier query test.** Submit BOM for reconciliation. Verify multiple kicad-happy sourcing skills queried per line item. Verify >20% pricing discrepancies flagged. Verify single-source risks identified. |
| **US-503: SessionStart Hook** | **Hook firing test.** Trigger SessionStart with: (a) no config, (b) outdated config, (c) valid config, (d) kicad-happy fully installed, (e) kicad-happy partially missing. Verify correct messages for each scenario. Verify hooks.json defines SessionStart hooks correctly. Test paused pipeline staleness detection. |
| **US-504: Schematic DRC Hook** (P2) | **PostToolUse hook test.** Edit a .kicad_sch file. Verify DRC triggers automatically. Verify violations displayed as non-blocking warnings. Edit a non-.kicad_sch file. Verify no DRC trigger. |
| **US-505: BOM Drift Hook** (P2) | **PostToolUse hook test.** Edit .kicad_sch file when BOM artifact exists. Verify drift detection compares components. Verify new/changed/removed components are listed. |

---

## 4. Reference Test Fixture Strategy

> "The reference fixture is our Palantir -- it shows us what is true, so that we may measure our gates against known ground truth rather than hope."

### 4.1 Purpose

The reference test fixture (US-400) serves as the measurable benchmark for all 5 validation gates. Without it, acceptance criteria for gates would be subjective ("catches defects") rather than quantifiable ("detects 6/7 seeded defect categories").

### 4.2 Fixture Contents

| File | Purpose | Seeded Defects |
|------|---------|----------------|
| `reference.kicad_sch` | Schematic with 10 seeded defects across 7 categories | Power integrity (missing bulk cap), signal integrity (unterminated trace), component derating (cap at operating voltage), missing pull-ups (floating I2C), decoupling (missing IC decoupling), voltage compatibility (5V to 3.3V without level shifter), thermal (high-power without thermal relief) |
| `reference.kicad_pcb` | PCB layout with DFM violations | Trace width below JLCPCB minimum, via size below minimum, solder mask aperture violation, clearance violation |
| `reference-bom.csv` | BOM with known issues | 1 obsolete component, 1 budget-exceeding component, 1 single-source component, 1 NRND component |
| `reference-pricing.json` | Static pricing data for offline testing | Fixed prices matching BOM line items -- enables budget threshold testing without live API calls |
| `MANIFEST.md` | Defect documentation | Every seeded defect with: ID, category, location, expected gate, expected severity |

### 4.3 Fixture Validation Tests

Before using the fixture for gate testing, validate the fixture itself:

- **TC-FIXTURE-01:** Verify all 5 files exist in `hardware-team/references/test-fixtures/`
- **TC-FIXTURE-02:** Open reference.kicad_sch in KiCad, verify it is a valid schematic file
- **TC-FIXTURE-03:** Open reference.kicad_pcb in KiCad, verify it is a valid PCB file
- **TC-FIXTURE-04:** Count defects in MANIFEST.md -- must be >= 10 schematic + 4 BOM + 4 PCB = 18 total
- **TC-FIXTURE-05:** Verify reference-pricing.json is parseable and contains entries for all BOM line items
- **TC-FIXTURE-06:** Cross-reference MANIFEST.md defect locations against actual KiCad file locations

### 4.4 Gate Testing Against Fixture

Each gate is tested against the fixture with a clear pass/fail criterion:

| Gate | Test | Pass Criterion |
|------|------|----------------|
| Schematic Review | Run against reference.kicad_sch | Detects defects in >= 6/7 categories |
| DRC | Run against reference.kicad_pcb | Detects all 4 seeded DFM violation types |
| BOM | Run against reference-bom.csv + reference-pricing.json | Flags all 4 BOM issue types (obsolete, NRND, budget, single-source) |
| DFM | Run against reference.kicad_pcb with target_fab=jlcpcb | Detects all 4 fab-specific violations |
| Compliance | Run with compliance_regions=[FCC, CE] | Produces checklists for both regions with evidence linking |

---

## 5. kicad-happy Integration Testing

> "Eleven skills to bind them. Each must answer when called, and I shall verify every one."

### 5.1 Cross-Plugin Skill Invocation Test Matrix

Each of the 11 kicad-happy skills must be tested for correct invocation from the hardware-team context.

| # | kicad-happy Skill | Consuming Role | Test Method | Expected Result |
|---|-------------------|---------------|-------------|-----------------|
| 1 | `kicad-happy:kicad` | EE, PCB Layout | Invoke Skill tool with `skill: "kicad-happy:kicad"` from EE sub-agent | SKILL_LOADED signal returned; schematic/PCB analysis output produced |
| 2 | `kicad-happy:spice` | EE | Invoke from EE sub-agent during Schematic stage | SKILL_LOADED signal; simulation results returned |
| 3 | `kicad-happy:digikey` | EE | Invoke from EE sub-agent for component search | Part search results with price/availability |
| 4 | `kicad-happy:mouser` | EE | Invoke from EE sub-agent for component search | Part search results with price/availability |
| 5 | `kicad-happy:lcsc` | EE | Invoke from EE sub-agent for component search | Part search results with price/availability |
| 6 | `kicad-happy:element14` | EE | Invoke from EE sub-agent for component search | Part search results with price/availability |
| 7 | `kicad-happy:jlcpcb` | MfgE | Invoke from MfgE sub-agent during DFM/DFA | JLCPCB design rules and constraints returned |
| 8 | `kicad-happy:pcbway` | MfgE | Invoke from MfgE sub-agent during DFM/DFA | PCBWay design rules and constraints returned |
| 9 | `kicad-happy:bom` | MfgE | Invoke from MfgE sub-agent during DFM/DFA | BOM validation results returned |
| 10 | `kicad-happy:emc` | CompE | Invoke from CompE sub-agent during Compliance | EMC pre-compliance analysis returned |
| 11 | `kicad-happy:kidoc` | CompE, MfgE | Invoke from CompE sub-agent during Compliance | Documentation generation output returned |

### 5.2 Failure Mode Testing

| Test Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **INT-FAIL-01** | kicad-happy plugin not installed | SessionStart hook reports 0/11 with installation instructions. Pipeline start blocked with clear error. |
| **INT-FAIL-02** | kicad-happy partially installed (some skills missing) | SessionStart hook reports N/11 with missing skill list. Pipeline warns but allows start (missing skills will fail at dispatch). |
| **INT-FAIL-03** | kicad-happy version mismatch | Version check warns: "kicad-happy version X.Y.Z installed; hardware-team requires >=A.B.C" |
| **INT-FAIL-04** | Skill dispatch timeout | Orchestrator classifies as TIMEOUT, retries once, pauses with PAUSED_DISPATCH_ERROR state. |
| **INT-FAIL-05** | Skill dispatch context overflow | Orchestrator classifies as CONTEXT_OVERFLOW, retries once, pauses with recommendations. |

### 5.3 Non-Reimplementation Verification

Per NFR-003 and C6, verify that no hardware-team role reimplements kicad-happy functionality.

**Test method:** Code review of all role SKILL.md files and reference documents using the operational definition:

> "A capability is reimplemented if a hardware-team role performs an action that would produce the same output as invoking a kicad-happy skill, without invoking that skill."

**Verification checklist:**
- [ ] No role SKILL.md contains instructions to parse `.kicad_sch` files directly (should invoke `kicad-happy:kicad`)
- [ ] No role SKILL.md contains instructions to query distributor APIs directly (should invoke `kicad-happy:digikey/mouser/lcsc/element14`)
- [ ] No role SKILL.md contains instructions to implement EMC rule checks from scratch (should invoke `kicad-happy:emc`)
- [ ] No role SKILL.md contains instructions to generate documentation from scratch (should invoke `kicad-happy:kidoc`)
- [ ] Role-specific domain knowledge that guides WHEN and HOW to invoke kicad-happy skills is confirmed as NOT reimplementation

---

## 6. Pipeline Orchestrator Testing

> "The pipeline is our road through Moria. Each stage is a hall. Each gate is a bridge. And the rework loop -- that is the Balrog, and we must ensure it has a termination condition."

### 6.1 Stage Routing Tests

| Test Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **PIPE-01** | Start new pipeline | Stage 1 (Concept) executes first. HW PO role is dispatched. |
| **PIPE-02** | Complete Stage 1, gate passes | Pipeline advances to Stage 2 (Schematic). EE role is dispatched. |
| **PIPE-03** | Complete all AI-execution stages (1-3, 5-6) | Each stage executes autonomously via Agent tool sub-agent dispatch. |
| **PIPE-04** | Reach human-execution stage (Stage 4: Prototype) | Pipeline generates preparation docs (ordering package, test procedures), pauses for human confirmation. |
| **PIPE-05** | Human confirms Prototype completion | Pipeline advances to Stage 5 (DFM/DFA). |
| **PIPE-06** | Complete all 8 stages | Pipeline finishes with all artifacts produced. No orphan stages. |
| **PIPE-07** | Stage dispatch uses Agent tool | Every stage dispatch inspected for Agent tool invocation (NOT inlined). Orchestrator NEVER produces domain artifacts. |
| **PIPE-08** | Stage dispatch fails | Orchestrator detects failure, retries once, then pauses with PAUSED_DISPATCH_ERROR and error classification (TIMEOUT, CONTEXT_OVERFLOW, MODEL_ERROR, UNKNOWN). |

### 6.2 Rework Loop Tests

| Test Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **REWORK-01** | Prototype identifies schematic issue | Pipeline returns to Schematic stage with rework reason as context. |
| **REWORK-02** | Rework target re-executes | Target stage has access to original artifacts AND rework reason. |
| **REWORK-03** | Rework completes, forward resumes | ALL downstream gates from rework target are re-validated (not skipped). |
| **REWORK-04** | Rework history logging | State includes: trigger reason, source stage, target stage, resolution, iteration count, total count. |
| **REWORK-05** | Per-path limit (default 3) exceeded | 4th trigger on same path -> pipeline PAUSES, escalates to human with rework history and recurring failure pattern. |
| **REWORK-06** | Total rework limit (default 10) exceeded | 11th total rework across all paths -> pipeline PAUSES, escalates with full history, pattern summary, human decision options (continue, abort, override). |
| **REWORK-07** | All 8 rework paths | Test each: Prototype->Schematic, Prototype->Layout, DFM/DFA->Layout, DFM/DFA->Schematic, Compliance->Schematic, Compliance->Layout, Pilot Run->DFM/DFA, Pilot Run->Schematic. |
| **REWORK-08** | Escalation message content | Escalation includes: (a) which limit (per-path or total), (b) count per path, (c) cumulative history, (d) clear pause message. |

### 6.3 State Persistence Tests

| Test Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **STATE-01** | Pipeline in progress, session ends | Current stage, gate results, artifact paths, rework history persisted to `.hardware/state.md`. |
| **STATE-02** | New session, resume requested | State loaded, pipeline continues from last completed stage. Completed stages not re-executed. |
| **STATE-03** | State file format | Fields match architecture Section 3.1.1: stage, gate results, dispatch errors, rework history, timestamps. |
| **STATE-04** | Staleness warning (7+ days paused) | SessionStart hook displays staleness warning. |
| **STATE-05** | Critical staleness (30+ days paused) | SessionStart hook displays critical staleness warning. |
| **STATE-06** | Dispatch error state (PAUSED_DISPATCH_ERROR) | State records: stage, role, error_type, error_detail, retry_attempted, timestamp. |

### 6.4 Gate Enforcement Tests

| Test Case | Scenario | Expected Behavior |
|-----------|----------|-------------------|
| **GATE-01** | All validators DONE | Gate passes, pipeline advances to next stage. |
| **GATE-02** | One validator NOT_DONE (others DONE) | Gate blocks. Failing validator's feedback returned to stage for correction. |
| **GATE-03** | Multiple validators NOT_DONE | Gate blocks. All failing validators' feedback returned. |
| **GATE-04** | Human Confirmation Gate (Prototype stage) | Gate waits for human input. Pipeline does not auto-advance. |
| **GATE-05** | Gate validator metadata | Each validator has: unique ID, description, pass/fail criteria, responsible role. |

---

## 7. FR Traceability Matrix

> "Every functional requirement shall be tracked. Not one shall escape my count. That bug still only counts as one."

| FR ID | Requirement Summary | Story(s) | Test Case(s) | Verification Method |
|-------|---------------------|----------|--------------|---------------------|
| FR-001 | Standard plugin structure | US-101, US-108 | TC-101-01, TC-101-02, TC-108-01 | Structural inspection of directory layout + marketplace.json |
| FR-002 | 8-stage pipeline with execution mode classification | US-102 | PIPE-01 through PIPE-07 | Pipeline execution with stage-by-stage verification |
| FR-003 | Gate DoD validation (ALL validators must DONE) | US-103 | GATE-01 through GATE-05 | Gate logic testing with controlled validator outputs |
| FR-004 | Config-driven pipeline (.hardware/config.yml) | US-104 | TC-104-01 through TC-104-04 | Config validation script execution with multiple configs |
| FR-005 | State persistence and resume | US-105 | STATE-01 through STATE-06 | Session interruption and resume testing |
| FR-006 | Self-learning memory | US-106 | TC-106-01, TC-106-02, TC-106-03 | Pipeline completion + memory retrieval benchmarking |
| FR-007 | Rework loops with termination | US-107 | REWORK-01 through REWORK-08 | Rework path triggering with limit verification |
| FR-008 | 6 role skills with context isolation + EE firmware docs | US-201 through US-206 | TC-201-01 through TC-206-03 | Skill loading + reference file audit per role |
| FR-009 | kicad-happy integration via cross-plugin invocation | US-301 | INT matrix (11 skills), INT-FAIL-01 through INT-FAIL-05 | Live Skill tool invocation for all 11 skills |
| FR-010 | Schematic Review Gate (iterative, forced-find, dedup) | US-401 | TC-401-01 through TC-401-05 | Gate execution against reference test fixture |
| FR-011 | DRC Gate against target fab | US-402 | TC-402-01 through TC-402-04 | Gate execution against reference.kicad_pcb |
| FR-012 | BOM Gate (cost, availability, lifecycle, second-source) | US-403 | TC-403-01 through TC-403-04 | Gate execution against reference-bom.csv |
| FR-013 | DFM Gate against target fab capabilities | US-404 | TC-404-01 through TC-404-04 | Gate execution against reference.kicad_pcb + config |
| FR-014 | Compliance Gate with evidence-linked checklists | US-405 | TC-405-01 through TC-405-04 | Gate execution with configured compliance regions |
| FR-015 | Design Review Board (multi-role, deduplicated) | US-501 | TC-501-01 through TC-501-03 | Multi-role review on reference schematic |
| FR-016 | BOM Reconciliation (multi-supplier, >20% flag) | US-502 | TC-502-01 through TC-502-03 | Multi-supplier query with price comparison |
| FR-017 | SessionStart hook (config + kicad-happy check) | US-503 | TC-503-01 through TC-503-05 | Hook firing with multiple environment states |
| FR-018 | PostToolUse DRC hook on .kicad_sch | US-504 | TC-504-01 through TC-504-03 | File edit event triggering |
| FR-019 | PostToolUse BOM drift detection | US-505 | TC-505-01 through TC-505-03 | Schematic edit with existing BOM artifact |
| FR-020 | Sub-agent dispatch via Agent tool (NOT inlined) | US-102 | PIPE-07 | SKILL.md inspection + runtime dispatch verification |
| FR-021 | Dynamic pipeline adaptation (P2 -- deferred) | Deferred | N/A (P2) | Deferred to Phase 2 |
| FR-022 | Reference test fixture with seeded defects | US-400 | TC-400-01 through TC-400-05, TC-FIXTURE-01 through TC-FIXTURE-06 | Fixture completeness audit + KiCad file validation |

**Coverage summary:** 21/22 FRs have mapped test cases. FR-021 is explicitly deferred to P2. 100% P1 FR coverage achieved.

---

## 8. NFR Verification Matrix

| NFR ID | Requirement | Verification Method | Pass Criterion |
|--------|-------------|---------------------|----------------|
| NFR-001 | No external Python dependencies | `grep -r "^import\|^from" hardware-team/scripts/ hardware-team/hooks/` -- verify all imports are stdlib | 0 non-stdlib imports |
| NFR-002 | Context isolation per role | Load each of 6 roles. Log reference files loaded. Verify each loads ONLY its own. | 0 cross-role references loaded |
| NFR-003 | kicad-happy consumed, never duplicated | Code review per Section 5.3 reimplementation checklist | 0 reimplemented capabilities |
| NFR-004 | Pipeline completes 8 stages in single session | End-to-end pipeline run on reference project | All 8 stages complete without session timeout |
| NFR-005 | Gate messages comprehensible | Review gate output: each message includes what failed, where, why, how to fix | All gate messages include 4 required elements |
| NFR-006 | Forward-compatible config schema | Test v1.0 config against v1.1+ schema | Old config uses defaults for new keys without error |
| NFR-007 | Model tier documented per role | Audit all 6 role SKILL.md files | Each specifies minimum model tier (Haiku/Sonnet/Opus) |
| NFR-008 | Memory retrieval <2s (P2) | Benchmark with 100+ entries | p95 retrieval < 2 seconds |
| NFR-009 | Plugin passes plugin-validator | Run `plugin-dev:plugin-validator` on hardware-team | 0 validation errors |
| NFR-010 | Rework history auditable | Inspect .hardware/state.md after rework runs | 100% of rework events logged with all required fields |

---

## 9. Regression Strategy

> "When one changes a single stone in Moria's foundation, one must verify the whole hall still stands. That is the purpose of regression."

### 9.1 Regression Triggers

Any change to the following requires regression testing:

| Change Area | Regression Scope |
|-------------|------------------|
| Pipeline orchestrator (hardware-flow SKILL.md) | Full pipeline system test (PIPE-01 through PIPE-08) + rework tests + gate tests |
| Any role SKILL.md | Context isolation test for changed role + integration test for its kicad-happy skills |
| Gate framework (gate-framework.md) | All 5 gate tests against reference fixture |
| Config schema (config-schema.md, validate_config.py) | Config validation unit tests + NFR-006 forward compatibility |
| Hook scripts (hooks/*.py) | All hook firing tests (TC-503-xx, TC-504-xx, TC-505-xx) |
| Integration layer (kicad-integration.md) | Cross-plugin dispatch test for all 11 skills |
| Reference test fixture | Fixture validation tests (TC-FIXTURE-01 through TC-FIXTURE-06) + all gate tests |
| Rework paths (rework-paths.md) | All rework loop tests (REWORK-01 through REWORK-08) |
| State manager (state_manager.py) | State persistence tests (STATE-01 through STATE-06) |
| marketplace.json | Marketplace registration validation (TC-108-01 through TC-108-03) |

### 9.2 Regression Test Suite (Minimum)

When time is limited, the minimum regression suite covers:

1. **Plugin structure validation** (TC-101-01) -- structural integrity
2. **Pipeline happy path** (PIPE-01 through PIPE-06) -- core flow
3. **One gate test** (TC-401-05 Schematic Review against fixture) -- gate mechanism
4. **Context isolation spot check** (2 roles: EE + MfgE) -- isolation integrity
5. **Cross-plugin dispatch** (kicad-happy:kicad) -- integration health
6. **Config load with defaults** (TC-104-02) -- config mechanism
7. **SessionStart hook** (TC-503-01, TC-503-03) -- hook mechanism

### 9.3 Regression After kicad-happy Updates

When kicad-happy is updated to a new version:

1. Run full cross-plugin dispatch test matrix (Section 5.1 -- all 11 skills)
2. Verify version compatibility check in SessionStart hook
3. Re-run all 5 gate tests against reference fixture (gate outputs may differ)
4. Verify integration layer input/output contracts still hold

---

## 10. Test Environment Requirements

| Requirement | Detail |
|-------------|--------|
| Claude Code | Current version with Agent tool and Skill tool available |
| kicad-happy plugin | Installed at `~/.claude/plugins/cache/kicad-happy/kicad-happy/1.2.0/` (all 11 skills) |
| Python | 3.x (standard library only) |
| KiCad | Optional for fixture validation (opening .kicad_sch/.kicad_pcb files) |
| Reference test fixture | hardware-team/references/test-fixtures/ fully populated |
| Filesystem | Write access to project root for .hardware/ directory creation |

---

## 11. Risk-Based Test Prioritization

> "Not all tests are equal. Some guard the gates of Helm's Deep. Others guard the stable door. Test the gates first."

| Priority | Test Area | Rationale |
|----------|-----------|-----------|
| P0 (Critical) | Cross-plugin kicad-happy invocation (INT matrix) | Foundation dependency -- if this fails, nothing works |
| P0 (Critical) | Gate enforcement (GATE-01, GATE-02) | Core quality mechanism -- gates must block |
| P0 (Critical) | Reference test fixture completeness (TC-FIXTURE-01 through TC-FIXTURE-06) | All gate testing depends on fixture integrity |
| P1 (High) | Pipeline stage routing (PIPE-01 through PIPE-08) | Core orchestration flow |
| P1 (High) | Rework termination (REWORK-05, REWORK-06) | Prevents infinite loops |
| P1 (High) | Context isolation per role (NFR-002) | Architecture integrity |
| P2 (Medium) | Config validation (TC-104-xx) | Graceful degradation on bad config |
| P2 (Medium) | SessionStart hooks (TC-503-xx) | Early warning system |
| P3 (Low) | State persistence (STATE-xx) | P2 story |
| P3 (Low) | Memory system (TC-106-xx) | P2 story |
| P3 (Low) | BOM Reconciliation (TC-502-xx) | P2 story |

---

## 12. Assumptions and Constraints

**Assumptions:**
1. kicad-happy plugin v1.2.0 is installed and all 11 skills return SKILL_LOADED on invocation
2. Claude Code Agent tool and Skill tool are available and functioning
3. Reference test fixture (US-400) will be developer-complete before gate testing begins
4. No external APIs are required for test execution (reference-pricing.json provides offline data)
5. Python 3.x is available on the test environment

**Constraints (from memory lessons):**
- Test cases must cover ALL PRD functional requirements explicitly -- QA checks FR-by-FR (enforced by Section 7 traceability matrix)
- Plan stage agents need pre-loaded constraints injected into their prompts (reflected in integration test setup)
- No external dependencies beyond Python standard library (NFR-001 verification required)

---

*Test strategy authored by Legolas. Sharp-eyed and precise. Every defect shall be found, every gate shall be tested, every FR shall be traced. That bug still only counts as one.*
