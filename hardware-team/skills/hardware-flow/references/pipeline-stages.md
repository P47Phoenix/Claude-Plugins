# Pipeline Stages Reference

**Status**: COMPLETE (US-103)
**Version**: 1.0
**Architecture Reference**: Section 3.1, 3.2, 3.3, 3.4

This file is the authoritative source for the 8-stage pipeline definitions, agent invocation templates, DoD validator dispatch, artifact output paths, parallel/sequential annotations, and stage-specific self-correction limits.

---

## Stage Index

| # | Stage | Execution Mode | Primary Role | Gate | Annotation |
|---|-------|---------------|-------------|------|------------|
| 1 | Concept | AI-execution | HW Product Owner | Concept Gate | Sequential |
| 2 | Schematic | AI-execution | Electrical Engineer | Schematic Review Gate | Sequential (multi-reviewer parallel within) |
| 3 | Layout | AI-execution | PCB Layout Engineer | DRC Gate | Sequential |
| 4 | Prototype | Human-execution | Test Engineer | Human Confirmation Gate | Sequential (pipeline pauses) |
| 5 | DFM/DFA | AI-execution | Manufacturing Engineer | DFM Gate + BOM Gate | Parallel (DFM and BOM validators run concurrently) |
| 6 | Compliance | AI-execution | Compliance Engineer | Compliance Gate | Sequential |
| 7 | Pilot Run | Human-execution | Manufacturing Engineer | Human Confirmation Gate | Sequential (pipeline pauses) |
| 8 | Production Release | Human-execution | Manufacturing Engineer | Final Gate | Sequential |

---

## Artifact Directory Structure

```
.hardware/artifacts/
+-- 01-concept/
|   +-- requirements.md
|   +-- constraints.md
|   +-- regulatory-scan.md
|   +-- bom-budget.md
+-- 02-schematic/
|   +-- schematic-review.md
|   +-- component-rationale.md
|   +-- simulation-results.md
|   +-- firmware-interface.md
+-- 03-layout/
|   +-- layout-review.md
|   +-- routing-analysis.md
|   +-- drc-results.md
+-- 04-prototype/
|   +-- ordering-package.md
|   +-- test-procedure.md
|   +-- test-fixture-requirements.md
|   +-- archived/
+-- 05-dfm-dfa/
|   +-- dfm-report.md
|   +-- dfa-report.md
|   +-- yield-assessment.md
|   +-- bom-validation.md
+-- 06-compliance/
|   +-- emc-report.md
|   +-- safety-analysis.md
|   +-- environmental-checklist.md
|   +-- compliance-package.md
+-- 07-pilot-run/
|   +-- manufacturing-transfer.md
|   +-- production-test-procedure.md
|   +-- yield-targets.md
+-- 08-production-release/
    +-- production-checklist.md
    +-- final-bom.md
    +-- compliance-package.md
    +-- release-documentation.md
```

---

## Section 1: Concept Stage

### Purpose
Capture and validate hardware requirements, constraints, feasibility, and BOM budget before any design work begins. This is the foundation -- get it wrong here and you pour concrete on sand.

### Entry Conditions
- `.hardware/config.yml` exists and passes schema validation
- Pipeline state is `in_progress` with `current_stage: 1` (or pipeline just started)
- No prior stage required (this is the first stage)

### Execution Mode
**AI-execution** -- fully autonomous

### Agent Invocation Template

```
SKILL: hardware-team:hw-product-owner
TASK_TYPE: write
ROLE: hw-product-owner

--- TASK ---
Execute Concept Stage (Stage 1) of the hardware pipeline.

Capture and validate:
1. Functional requirements with measurable acceptance criteria
2. Non-functional requirements (power, size, thermal, environmental)
3. Interface requirements (connectors, protocols, voltage levels)
4. Regulatory requirements based on config compliance_regions: {config.compliance_regions}
5. BOM budget target: {config.bom_budget}
6. Production volume target: {config.production_volume}
7. Feasibility assessment for key requirements

--- INPUT ARTIFACTS ---
- .hardware/config.yml (project configuration)
- User-provided project description / requirements

--- OUTPUT ---
Write artifacts to .hardware/artifacts/01-concept/
- requirements.md
- constraints.md
- regulatory-scan.md
- bom-budget.md

--- ISOLATION RULES ---
- Read ONLY hw-product-owner/SKILL.md and its references
- Do NOT read electrical-engineer, pcb-layout-engineer, or other role references
```

### Supporting Agents
None. HW Product Owner operates solo in Stage 1.

### Gate
**Concept Gate** -- validators: `requirements-completeness`, `feasibility-check`
See `quality-gates.md` Section 1.

### Self-Correction Limit
Max iterations: 3 (per `rework.max_rework_iterations` config)

### Parallel/Sequential Annotation
**Sequential** -- must complete before Stage 2 begins.

---

## Section 2: Schematic Stage

### Purpose
Design the electrical schematic, select components, run simulations, and perform multi-reviewer schematic review. This is where the circuit is born -- every connection matters.

### Entry Conditions
- Stage 1 (Concept) completed with Concept Gate DONE
- Requirements and constraints artifacts exist at `.hardware/artifacts/01-concept/`
- BOM budget established

### Execution Mode
**AI-execution** -- autonomous with multi-reviewer gate

### Agent Invocation Template

```
SKILL: hardware-team:electrical-engineer
TASK_TYPE: write
ROLE: electrical-engineer

--- TASK ---
Execute Schematic Stage (Stage 2) of the hardware pipeline.

1. Design/review the schematic against requirements from Stage 1
2. Select components with rationale (invoke kicad-happy sourcing skills)
3. Run SPICE simulations on critical subcircuits (invoke kicad-happy:spice)
4. Perform schematic analysis (invoke kicad-happy:kicad)
5. Document firmware interface (pin table, power domains, bus specs, debug)

--- INPUT ARTIFACTS ---
- .hardware/artifacts/01-concept/requirements.md
- .hardware/artifacts/01-concept/constraints.md
- .hardware/artifacts/01-concept/bom-budget.md
- KiCad schematic file (path from user or config)

--- kicad-happy SKILLS ---
- kicad-happy:kicad (schematic analysis)
- kicad-happy:spice (simulation)
- kicad-happy:digikey (component sourcing)
- kicad-happy:mouser (component sourcing)
- kicad-happy:lcsc (component sourcing)
- kicad-happy:element14 (component sourcing)

--- OUTPUT ---
Write artifacts to .hardware/artifacts/02-schematic/
- schematic-review.md
- component-rationale.md
- simulation-results.md
- firmware-interface.md

--- ISOLATION RULES ---
- Read ONLY electrical-engineer/SKILL.md and its references
- Invoke kicad-happy skills via Skill tool (do NOT reimplement their capabilities)
```

### Supporting Agents

**HW Product Owner** (trade-off support) -- dispatched sequentially AFTER primary EE work:
```
SKILL: hardware-team:hw-product-owner
TASK_TYPE: review
ROLE: hw-product-owner

--- TASK ---
Review component trade-offs from Stage 2 schematic design.
Validate that component selections align with BOM budget and requirements.
```

### Gate
**Schematic Review Gate** -- multi-reviewer iterative pattern with 7 category validators.
See `quality-gates.md` Section 2.

**Reviewer dispatch** (parallel within gate):
```
Pass 1: Agent(EE-Reviewer-1) -- independent context, forced-find prompting
  |  (parallel)
Pass 2: Agent(EE-Reviewer-2) -- independent context, forced-find prompting
  |  (parallel, if review.schematic_review_passes >= 3)
Pass 3..N: Agent(EE-Reviewer-N)
  |
  v (sequential after all passes complete)
Deduplication Engine (deterministic, in orchestrator)
  |
Coverage Check
  |
Gate Evaluation
```

### Self-Correction Limit
Max iterations: 3 (per `rework.max_rework_iterations` config)

### Parallel/Sequential Annotation
**Sequential** at stage level (must complete before Stage 3).
**Parallel** within the gate: reviewer passes run concurrently.

### Design Review Board
If `review.design_review_board: true`, DRB activates AFTER the Schematic Review Gate passes, before advancing to Layout. DRB dispatches EE, PCB Layout, MfgE, and CompE reviewers in parallel.

---

## Section 3: Layout Stage

### Purpose
Create the PCB physical layout from the schematic, including component placement, routing, stackup design, and DRC validation. Where the circuit meets the physical world.

### Entry Conditions
- Stage 2 (Schematic) completed with Schematic Review Gate DONE
- Schematic artifacts exist at `.hardware/artifacts/02-schematic/`
- Component footprints selected and validated
- Stackup defined for target layer count (`config.board_layers`)

### Execution Mode
**AI-execution** -- autonomous

### Agent Invocation Template

```
SKILL: hardware-team:pcb-layout-engineer
TASK_TYPE: write
ROLE: pcb-layout-engineer

--- TASK ---
Execute Layout Stage (Stage 3) of the hardware pipeline.

1. Review/create PCB layout against schematic and constraints
2. Validate component placement (thermal, signal integrity, manufacturability)
3. Review routing (impedance control, current capacity, EMC)
4. Run DRC against target fab capabilities (invoke kicad-happy:kicad)
5. Generate stackup documentation

--- INPUT ARTIFACTS ---
- .hardware/artifacts/02-schematic/schematic-review.md
- .hardware/artifacts/02-schematic/component-rationale.md
- .hardware/artifacts/01-concept/constraints.md
- KiCad PCB file (path from user or config)
- Target fab: {config.target_fab}
- Board layers: {config.board_layers}

--- kicad-happy SKILLS ---
- kicad-happy:kicad (PCB analysis, DRC parsing)

--- OUTPUT ---
Write artifacts to .hardware/artifacts/03-layout/
- layout-review.md
- routing-analysis.md
- drc-results.md

--- ISOLATION RULES ---
- Read ONLY pcb-layout-engineer/SKILL.md and its references
- Invoke kicad-happy:kicad via Skill tool for DRC analysis
```

### Supporting Agents
None. PCB Layout Engineer operates solo in Stage 3.

### Gate
**DRC Gate** -- validator: `drc-pass`
See `quality-gates.md` Section 3.

### Self-Correction Limit
Max iterations: 3 (per `rework.max_rework_iterations` config)

### Parallel/Sequential Annotation
**Sequential** -- must complete before Stage 4 begins.

### Design Review Board
If `review.design_review_board: true`, DRB activates AFTER the DRC Gate passes, before advancing to Prototype. DRB dispatches EE, PCB Layout, MfgE, and CompE reviewers in parallel.

---

## Section 4: Prototype Stage

### Purpose
Order prototype PCBs and components, assemble, and perform bring-up testing. The design meets the physical world for the first time.

### Entry Conditions
- Stage 3 (Layout) completed with DRC Gate DONE
- All layout artifacts exist at `.hardware/artifacts/03-layout/`
- DRC clean (zero errors)

### Execution Mode
**Human-execution** -- gate-in / human-action / gate-out pattern

### Agent Invocation Template (Gate-In Phase)

```
SKILL: hardware-team:test-engineer
TASK_TYPE: write
ROLE: test-engineer

--- TASK ---
Execute Prototype Stage (Stage 4) Gate-In: generate preparation artifacts.

1. Generate ordering package for target fab ({config.target_fab})
2. Create test procedure based on requirements and schematic
3. Define test fixture requirements
4. Present numbered action items to user

--- INPUT ARTIFACTS ---
- .hardware/artifacts/01-concept/requirements.md
- .hardware/artifacts/02-schematic/firmware-interface.md
- .hardware/artifacts/03-layout/layout-review.md
- .hardware/artifacts/03-layout/drc-results.md
- Target fab: {config.target_fab}

--- kicad-happy SKILLS ---
- kicad-happy:jlcpcb or kicad-happy:pcbway (ordering package, per config)
- kicad-happy:kicad (optional -- test point locations, connector pinouts)

--- OUTPUT ---
Write artifacts to .hardware/artifacts/04-prototype/
- ordering-package.md
- test-procedure.md
- test-fixture-requirements.md
```

### Supporting Agents

**Electrical Engineer** (bring-up support) -- dispatched sequentially:
```
SKILL: hardware-team:electrical-engineer
TASK_TYPE: review
ROLE: electrical-engineer

--- TASK ---
Review prototype test procedure for electrical completeness.
Verify bring-up sequence covers critical power rails and signal paths.
```

### Gate
**Human Confirmation Gate** -- validator: `human-confirmation`
See `quality-gates.md` Section 4.

### Human Action Phase
Pipeline transitions to `PAUSED_AWAITING_HUMAN`. User performs:
1. Order PCBs from target fab
2. Order components from distributors
3. Assemble prototype (or send to assembly house)
4. Perform bring-up testing per test procedure
5. Respond: `"prototype complete"` or `"prototype failed: <description>"`

### Rework Paths (if failed)
- Prototype --> Schematic: fundamental circuit error
- Prototype --> Layout: routing or thermal issue

### Self-Correction Limit
N/A (human-execution stage -- self-correction is human-driven)

### Parallel/Sequential Annotation
**Sequential** -- pipeline pauses for human action.

---

## Section 5: DFM/DFA Stage

### Purpose
Validate design for manufacturability and assembly, validate BOM cost/availability/lifecycle, and assess production yield. Where engineering meets manufacturing reality.

### Entry Conditions
- Stage 4 (Prototype) completed with Human Confirmation Gate DONE
- Prototype testing passed (or rework completed)
- All prior artifacts exist

### Execution Mode
**AI-execution** -- autonomous

### Agent Invocation Template

```
SKILL: hardware-team:manufacturing-engineer
TASK_TYPE: write
ROLE: manufacturing-engineer

--- TASK ---
Execute DFM/DFA Stage (Stage 5) of the hardware pipeline.

1. Evaluate DFM rules against target fab capabilities (invoke kicad-happy fab skill)
2. Evaluate DFA rules (component placement, orientation, reflow compatibility)
3. Validate BOM: cost vs budget, availability, lifecycle, second-source (invoke kicad-happy:bom)
4. Assess production yield based on DFM/DFA analysis
5. Generate remediation plan for any violations

--- INPUT ARTIFACTS ---
- .hardware/artifacts/02-schematic/component-rationale.md
- .hardware/artifacts/03-layout/layout-review.md
- .hardware/artifacts/03-layout/drc-results.md
- .hardware/artifacts/04-prototype/test-procedure.md (prototype feedback)
- KiCad PCB file
- Target fab: {config.target_fab}
- BOM budget: {config.bom_budget}
- Second source required: {config.second_source_required}
- Production volume: {config.production_volume}

--- kicad-happy SKILLS ---
- kicad-happy:jlcpcb or kicad-happy:pcbway (DFM rules, per config)
- kicad-happy:bom (BOM management)

--- OUTPUT ---
Write artifacts to .hardware/artifacts/05-dfm-dfa/
- dfm-report.md
- dfa-report.md
- yield-assessment.md
- bom-validation.md

--- ISOLATION RULES ---
- Read ONLY manufacturing-engineer/SKILL.md and its references
- Invoke kicad-happy skills via Skill tool
```

### Supporting Agents
None. Manufacturing Engineer operates solo in Stage 5.

### Gate
**DFM Gate + BOM Gate** -- validators: `dfm-pass`, `bom-pass` (run concurrently)
See `quality-gates.md` Sections 5a and 5b.

### Self-Correction Limit
Max iterations: 3 (per `rework.max_rework_iterations` config)

### Rework Paths (if gate fails after max iterations)
- DFM/DFA --> Layout: DFM violation requires layout change
- DFM/DFA --> Schematic: component unavailable at target fab, needs substitution

### Parallel/Sequential Annotation
**Parallel** within gate: DFM and BOM validators run concurrently.
**Sequential** at stage level: must complete before Stage 6.

### Design Review Board
If `review.design_review_board: true`, DRB activates AFTER DFM+BOM Gate passes, before advancing to Compliance.

---

## Section 6: Compliance Stage

### Purpose
Validate regulatory compliance for all configured target markets. Generate evidence-linked compliance documentation. Where the design meets the lawyers.

### Entry Conditions
- Stage 5 (DFM/DFA) completed with DFM Gate + BOM Gate DONE
- All prior artifacts exist
- `compliance_regions` configured in `.hardware/config.yml`

### Execution Mode
**AI-execution** -- autonomous

### Agent Invocation Template

```
SKILL: hardware-team:compliance-engineer
TASK_TYPE: write
ROLE: compliance-engineer

--- TASK ---
Execute Compliance Stage (Stage 6) of the hardware pipeline.

1. Generate per-region compliance checklist based on config: {config.compliance_regions}
2. Perform EMC pre-compliance analysis (invoke kicad-happy:emc)
3. Assess safety compliance per applicable standards
4. Evaluate environmental compliance (RoHS, REACH, WEEE as configured)
5. Link each requirement to evidence artifact
6. Generate compliance package

--- INPUT ARTIFACTS ---
- .hardware/artifacts/02-schematic/schematic-review.md
- .hardware/artifacts/03-layout/layout-review.md
- .hardware/artifacts/05-dfm-dfa/dfm-report.md
- .hardware/artifacts/05-dfm-dfa/bom-validation.md
- KiCad schematic and PCB files
- Compliance regions: {config.compliance_regions}

--- kicad-happy SKILLS ---
- kicad-happy:emc (EMC pre-compliance analysis)
- kicad-happy:kidoc (regulatory documentation generation)

--- OUTPUT ---
Write artifacts to .hardware/artifacts/06-compliance/
- emc-report.md
- safety-analysis.md
- environmental-checklist.md
- compliance-package.md

--- ISOLATION RULES ---
- Read ONLY compliance-engineer/SKILL.md and its references
- Invoke kicad-happy skills via Skill tool
```

### Supporting Agents
None. Compliance Engineer operates solo in Stage 6.

### Gate
**Compliance Gate** -- validator: `compliance-pass`
See `quality-gates.md` Section 6.

### Self-Correction Limit
Max iterations: 3 (per `rework.max_rework_iterations` config)

### Rework Paths (if gate fails after max iterations)
- Compliance --> Schematic: EMC failure requires filtering/shielding component redesign
- Compliance --> Layout: EMC failure requiring layout-specific changes (ground plane, trace rerouting) that do NOT require schematic changes

### Parallel/Sequential Annotation
**Sequential** -- must complete before Stage 7 begins.

---

## Section 7: Pilot Run Stage

### Purpose
Transfer design to manufacturing, execute a pilot production batch, measure yield, and validate production test procedures. Where the prototype becomes a product.

### Entry Conditions
- Stage 6 (Compliance) completed with Compliance Gate DONE
- All compliance artifacts exist at `.hardware/artifacts/06-compliance/`
- Compliance package complete for all configured regions

### Execution Mode
**Human-execution** -- gate-in / human-action / gate-out pattern

### Agent Invocation Template (Gate-In Phase)

```
SKILL: hardware-team:manufacturing-engineer
TASK_TYPE: write
ROLE: manufacturing-engineer

--- TASK ---
Execute Pilot Run Stage (Stage 7) Gate-In: generate manufacturing transfer artifacts.

1. Generate manufacturing transfer package (assembly instructions, component placement)
2. Create production test procedure
3. Define yield targets based on DFM analysis
4. Present numbered action items to user

--- INPUT ARTIFACTS ---
- .hardware/artifacts/05-dfm-dfa/dfm-report.md
- .hardware/artifacts/05-dfm-dfa/dfa-report.md
- .hardware/artifacts/05-dfm-dfa/bom-validation.md
- .hardware/artifacts/06-compliance/compliance-package.md
- Production volume: {config.production_volume}
- Target fab: {config.target_fab}

--- kicad-happy SKILLS ---
- kicad-happy:kidoc (manufacturing documentation)
- kicad-happy:bom (production BOM finalization)

--- OUTPUT ---
Write artifacts to .hardware/artifacts/07-pilot-run/
- manufacturing-transfer.md
- production-test-procedure.md
- yield-targets.md
```

### Supporting Agents

**Test Engineer** (production test support) -- dispatched sequentially:
```
SKILL: hardware-team:test-engineer
TASK_TYPE: review
ROLE: test-engineer

--- TASK ---
Review production test procedure for coverage and feasibility.
Validate test fixture requirements against manufacturing constraints.
```

### Gate
**Human Confirmation Gate** -- validator: `human-confirmation`
See `quality-gates.md` Section 4 (same pattern).

### Human Action Phase
Pipeline transitions to `PAUSED_AWAITING_HUMAN`. User performs:
1. Transfer design package to contract manufacturer
2. Execute pilot production run
3. Measure first-pass yield
4. Run production tests on pilot batch
5. Respond: `"pilot run complete"` or `"pilot run failed: <description>"`

### Rework Paths (if failed)
- Pilot Run --> DFM/DFA: assembly yield issue requires DFM adjustment
- Pilot Run --> Schematic: circuit-level issue discovered during pilot testing

### Self-Correction Limit
N/A (human-execution stage)

### Parallel/Sequential Annotation
**Sequential** -- pipeline pauses for human action.

---

## Section 8: Production Release Stage

### Purpose
Final validation that all artifacts are complete, all gates passed, and the design is ready for volume production. The last gate before the product ships.

### Entry Conditions
- Stage 7 (Pilot Run) completed with Human Confirmation Gate DONE
- All prior artifacts exist
- Pilot run yield meets targets

### Execution Mode
**Human-execution** -- gate-in / human-action / gate-out pattern

### Agent Invocation Template (Gate-In Phase)

```
SKILL: hardware-team:manufacturing-engineer
TASK_TYPE: write
ROLE: manufacturing-engineer

--- TASK ---
Execute Production Release Stage (Stage 8) Gate-In: generate release artifacts.

1. Generate production checklist (all gates, all artifacts, all waivers)
2. Finalize production BOM (invoke kicad-happy:bom)
3. Compile final compliance package
4. Generate release documentation (revision history, known issues, errata)
5. Present final review action items to user

--- INPUT ARTIFACTS ---
- ALL artifacts from stages 1-7
- .hardware/state.md (gate results, rework history, waivers)
- Production volume: {config.production_volume}

--- kicad-happy SKILLS ---
- kicad-happy:kidoc (release documentation)
- kicad-happy:bom (final BOM)

--- OUTPUT ---
Write artifacts to .hardware/artifacts/08-production-release/
- production-checklist.md
- final-bom.md
- compliance-package.md
- release-documentation.md
```

### Supporting Agents
None. Manufacturing Engineer operates solo for release preparation.

### Gate
**Final Gate** -- validator: `final-aggregate`
See `quality-gates.md` Section 7.

### Human Action Phase
Pipeline transitions to `PAUSED_AWAITING_HUMAN`. User performs:
1. Review production checklist
2. Review all waivers and risk acceptances
3. Approve release documentation
4. Respond: `"production release approved"` or `"production release rejected: <description>"`

### Self-Correction Limit
N/A (human-execution stage)

### Parallel/Sequential Annotation
**Sequential** -- final stage, pipeline completes on approval.

---

## Stage Routing Matrix by Project Type

Phase 1 behavior: ALL stages execute at full depth. This matrix is informational guidance for Phase 2 dynamic depth adaptation.

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

---

## Rework Path Summary

| Rework Path | Trigger Examples | Target Stage |
|-------------|-----------------|-------------|
| Prototype --> Schematic | Fundamental circuit error during bring-up | 2 |
| Prototype --> Layout | Routing or thermal issue revealed by prototype | 3 |
| DFM/DFA --> Layout | DFM violation requires layout change | 3 |
| DFM/DFA --> Schematic | Component unavailable at target fab | 2 |
| Compliance --> Schematic | EMC failure requires filtering/shielding redesign | 2 |
| Compliance --> Layout | EMC failure requiring layout-only changes | 3 |
| Pilot Run --> DFM/DFA | Assembly yield issue requires DFM adjustment | 5 |
| Pilot Run --> Schematic | Circuit-level issue from pilot testing | 2 |

All rework paths re-validate downstream gates from the target stage forward. See `rework-paths.md` for full rework execution semantics.
