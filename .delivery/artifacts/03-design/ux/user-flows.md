# User Flows: Hardware Delivery Team Plugin

**Version**: 1.1
**Date**: 2026-04-12
**Author**: UX Designer (Galadriel)
**Source PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Project Type**: GREENFIELD
**Role**: UX Designer | Task: user-flow | References: user-flows.md

---

> *"I give you the light of user flows, our most beloved design. May it be a light to you in dark places, when all other CLI output goes out."*

---

## Table of Contents

1. [Flow 1: First-Time Setup](#flow-1-first-time-setup)
2. [Flow 2: Pipeline Execution](#flow-2-pipeline-execution)
3. [Flow 3: Stage Interaction](#flow-3-stage-interaction)
4. [Flow 4: Rework](#flow-4-rework)
5. [Flow 5: kicad-happy Integration](#flow-5-kicad-happy-integration)
6. [Flow 6: Config-Driven Adaptation](#flow-6-config-driven-adaptation)
7. [Flow 7: Resume](#flow-7-resume)
8. [FR Coverage Matrix](#fr-coverage-matrix)

---

## Design Constraints

> "The world has changed. I feel it in the CLI. I smell it in the terminal. Much that once was GUI is lost, for none now live who remember the dropdown menus."

This is a **CLI plugin** -- all interaction is text-based via Claude Code. The "interface" is:

- **Commands**: Text the user types (e.g., invoking skills, answering prompts)
- **Output blocks**: Structured text Claude produces (status, gates, artifacts)
- **Checkpoints**: Points where the pipeline pauses for user confirmation
- **Artifacts**: Files written to the filesystem (`.hardware/`, project directories)

There are no screens, buttons, or visual elements. The user experience IS the conversation flow.

---

## Flow 1: First-Time Setup

**User Goal**: Install the hardware-team plugin, configure my project, and be ready to run the pipeline.
**Primary Persona**: Elena (solo hardware developer)
**Happy Path Steps**: 7
**Covers**: FR-001, FR-004, FR-017, Story 1.1, Story 1.4, Story 1.8, Story 3.6, Story 5.3

### Entry Points

- **E1: Plugin installation** -- User installs hardware-team via Claude Code plugin system
- **E2: First session** -- User starts a Claude Code session in a project directory with KiCad files
- **E3: Explicit invocation** -- User says "set up hardware pipeline" or "hw-setup"

### Happy Path

```
[Start] User installs hardware-team plugin
   |
   1. SessionStart hook fires
   |   +-- Checks for .hardware/config.yml --> NOT FOUND
   |   +-- Checks for kicad-happy skills --> Reports availability
   |   +-- Output:
   |       ┌─────────────────────────────────────────────────┐
   |       │ hardware-team: No .hardware/config.yml found.   │
   |       │ Run `hw-setup` to create one.                   │
   |       │                                                 │
   |       │ kicad-happy: 11/11 skills available             │
   |       └─────────────────────────────────────────────────┘
   |
   2. User invokes: "hw-setup"
   |
   3. Setup wizard asks questions (sequential, one at a time):
   |
   |   Q1: "What is your project name?"
   |       > [User types: "sensor-board-v2"]
   |
   |   Q2: "Target fabrication house?"
   |       Options: [jlcpcb] [pcbway] [other]
   |       > [User types: "jlcpcb"]
   |
   |   Q3: "Target compliance regions? (comma-separated)"
   |       Examples: FCC, CE, UL, none
   |       > [User types: "FCC, CE"]
   |
   |   Q4: "BOM budget target (USD per unit)?"
   |       Default: no limit
   |       > [User types: "12.50"]
   |
   |   Q5: "Production volume target?"
   |       Options: [prototype (<10)] [small-batch (10-1000)]
   |                [production (1000+)]
   |       > [User types: "small-batch"]
   |
   |   Q6: "Board layer count?"
   |       Options: [1] [2] [4] [6] [8+]
   |       > [User types: "4"]
   |
   |   Q7: "Minimum kicad-happy version?"
   |       Default: >=1.2.0
   |       > [User presses Enter for default]
   |
   |   Q8: "Rework iteration limit per path?"
   |       Default: 3
   |       > [User presses Enter for default]
   |
   |   Q9: "Total rework limit per pipeline run?"
   |       Default: 10
   |       > [User presses Enter for default]
   |
   4. Wizard generates .hardware/config.yml
   |   +-- Output:
   |       ┌─────────────────────────────────────────────────┐
   |       │ Created .hardware/config.yml (schema v1.0)      │
   |       │                                                 │
   |       │   project: sensor-board-v2                      │
   |       │   target_fab: jlcpcb                            │
   |       │   compliance_regions: [FCC, CE]                 │
   |       │   bom_budget: 12.50                             │
   |       │   volume: small-batch                           │
   |       │   layers: 4                                     │
   |       │   dependencies:                                 │
   |       │     kicad_happy_version: ">=1.2.0"              │
   |       │   rework:                                       │
   |       │     max_rework_iterations: 3                    │
   |       │     max_total_reworks: 10                       │
   |       │                                                 │
   |       │ Edit .hardware/config.yml to adjust settings.   │
   |       └─────────────────────────────────────────────────┘
   |
   5. Wizard creates directory structure:
   |       .hardware/
   |       ├── config.yml
   |       ├── state.md        (empty, created on first run)
   |       └── memory/         (empty, populated after runs)
   |
   6. Wizard validates config against schema
   |   +-- Output: "Config valid. Ready to run pipeline."
   |
   7. Wizard confirms readiness:
   |       ┌─────────────────────────────────────────────────┐
   |       │ Setup complete. To start the hardware pipeline: │
   |       │                                                 │
   |       │   "Run the hardware pipeline"                   │
   |       │   or invoke: hardware-team:hardware-flow        │
   |       └─────────────────────────────────────────────────┘
   |
[End] User is configured and ready
```

### Alternative Paths

**2a: kicad-happy not installed**
```
   1. SessionStart hook fires
   |   +-- kicad-happy check --> MISSING
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ WARNING: Required dependency kicad-happy is not      │
   |       │ installed. Install it via the Claude Code plugin     │
   |       │ system.                                              │
   |       │                                                      │
   |       │ The hardware-team plugin requires kicad-happy for    │
   |       │ component sourcing, fabrication validation, KiCad    │
   |       │ analysis, and documentation generation.              │
   |       │                                                      │
   |       │ kicad-happy: 0/11 skills available                   │
   |       │ Missing: kicad, spice, digikey, mouser, lcsc,       │
   |       │          element14, jlcpcb, pcbway, bom, emc, kidoc │
   |       └──────────────────────────────────────────────────────┘
   |
   --> User can still run hw-setup (config creation)
   --> Pipeline start is BLOCKED until kicad-happy is installed
```

**2b: kicad-happy partially installed**
```
   1. SessionStart hook fires
   |   +-- kicad-happy check --> PARTIAL
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ kicad-happy: 8/11 skills available                   │
   |       │ Missing: spice, emc, kidoc                           │
   |       │ Install kicad-happy via Claude Code plugin system.   │
   |       └──────────────────────────────────────────────────────┘
```

**2c: kicad-happy version mismatch**
```
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ kicad-happy version 1.1.0 installed; hardware-team   │
   |       │ requires >=1.2.0. Some features may not work.        │
   |       └──────────────────────────────────────────────────────┘
```

**2d: Config already exists**
```
   2. User invokes: "hw-setup"
   |   +-- Detects existing .hardware/config.yml
   |   +-- Output: "Config already exists (schema v1.0). Overwrite? [y/N]"
   |   +-- User: "N" --> setup exits, config preserved
   |   +-- User: "y" --> setup proceeds with wizard
```

### Error Paths

**E1: Invalid config file (manual edit introduced errors)**
```
   SessionStart hook fires
   |   +-- Config validation fails
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ WARNING: .hardware/config.yml has invalid fields:    │
   |       │   - bom_budget: "abc" (expected number)              │
   |       │   - target_fab: "invalid" (expected: jlcpcb, pcbway)│
   |       │ Using defaults for invalid fields.                   │
   |       └──────────────────────────────────────────────────────┘
   --> Pipeline continues with defaults for invalid fields (NEVER fails due to config)
```

**E2: Outdated config schema**
```
   SessionStart hook fires
   |   +-- Config schema version outdated
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ WARNING: .hardware/config.yml uses schema v0.9.     │
   |       │ Current schema is v1.0.                              │
   |       │ Migration: Add 'dependencies.kicad_happy_version'    │
   |       │ and 'rework' section. See config-schema.md.          │
   |       │ Pipeline will use defaults for missing fields.       │
   |       └──────────────────────────────────────────────────────┘
```

---

## Flow 2: Pipeline Execution

**User Goal**: Run my hardware project through the full 8-stage pipeline from concept to production release.
**Primary Persona**: Elena (solo hardware developer), Marcus (team lead)
**Happy Path Steps**: 8 stages + inter-stage gates
**Covers**: FR-002, FR-003, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-020, Story 1.2, Story 1.3

### Entry Points

- **E1: Direct invocation** -- "Run the hardware pipeline" or invoke `hardware-team:hardware-flow`
- **E2: Resume** -- "Resume hardware pipeline" (see Flow 7)

### Happy Path (Full 8-Stage Pipeline)

> "Even the smallest circuit, carefully designed, can change the course of the future."

```
[Start] User: "Run the hardware pipeline"
   |
   0. Pre-flight checks
   |   +-- Load .hardware/config.yml (or defaults)
   |   +-- Verify kicad-happy availability (11/11)
   |   +-- Load memory from .hardware/memory/ (if exists)
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ HARDWARE PIPELINE: sensor-board-v2                   │
   |       │ Config: .hardware/config.yml (v1.0)                  │
   |       │ Fab: jlcpcb | Regions: FCC, CE | Budget: $12.50     │
   |       │ kicad-happy: 11/11 skills available                  │
   |       │ Memory: 3 lessons loaded                             │
   |       │                                                      │
   |       │ Stages: Concept > Schematic > Layout > Prototype >   │
   |       │         DFM/DFA > Compliance > Pilot Run >           │
   |       │         Production Release                           │
   |       └──────────────────────────────────────────────────────┘
   |
   ===== STAGE 1: CONCEPT [AI-execution] =====
   |
   1. Pipeline dispatches Concept stage via Agent tool
   |   +-- Roles: Hardware Product Owner
   |   +-- Activities: requirements capture, constraint matrix,
   |       regulatory landscape scan, initial BOM budget
   |   +-- Sub-agent produces: requirements doc, constraint matrix,
   |       regulatory scan, BOM budget estimate
   |   +-- Output presented to user (see Flow 3 for detail)
   |
   1g. CONCEPT GATE
   |   +-- Validators: requirements completeness, feasibility check
   |   +-- ALL validators must report DONE
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ GATE: Concept --> Schematic                          │
   |       │ [DONE] Requirements completeness                     │
   |       │ [DONE] Feasibility assessment                        │
   |       │ Result: PASS -- advancing to Schematic               │
   |       └──────────────────────────────────────────────────────┘
   |
   ===== STAGE 2: SCHEMATIC [AI-execution] =====
   |
   2. Pipeline dispatches Schematic stage via Agent tool
   |   +-- Roles: Electrical Engineer (primary), HW PO (trade-offs)
   |   +-- Activities: schematic design review, component selection,
   |       SPICE simulation, firmware interface documentation
   |   +-- kicad-happy skills consumed: kicad, spice, digikey,
   |       mouser, lcsc, element14
   |   +-- Sub-agent produces: schematic review, component rationale,
   |       simulation results, firmware interface docs (pin table,
   |       power domains, bus specs, debug interfaces)
   |
   2g. SCHEMATIC REVIEW GATE (multi-reviewer)
   |   +-- Iterative review pattern (issue #76):
   |       - Multiple reviewers with forced-find prompting
   |       - 7 categories: power integrity, signal integrity,
   |         component derating, pull-ups/pull-downs, decoupling,
   |         voltage level compat, thermal
   |       - Deduplication across reviewers
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ SCHEMATIC REVIEW GATE                                │
   |       │                                                      │
   |       │ Reviewers: EE-1, EE-2 (2 passes, deduplicated)      │
   |       │                                                      │
   |       │ Findings (7 unique, 3 duplicates removed):           │
   |       │  [CRITICAL] F-001: Missing bulk cap on U3 VDD       │
   |       │    Location: Sheet 2, U3 pin 14                     │
   |       │    Fix: Add 10uF ceramic cap, place within 3mm      │
   |       │  [MAJOR] F-002: Unterminated SPI_CLK trace          │
   |       │    Location: Sheet 1, Net SPI_CLK                   │
   |       │    Fix: Add series termination resistor (33R)        │
   |       │  [MINOR] F-003: ...                                  │
   |       │                                                      │
   |       │ Result: NOT_DONE -- 1 critical finding               │
   |       │ Pipeline paused. Correct findings and re-run gate.   │
   |       └──────────────────────────────────────────────────────┘
   |   (User corrects, gate re-runs, passes)
   |
   ===== STAGE 3: LAYOUT [AI-execution] =====
   |
   3. Pipeline dispatches Layout stage via Agent tool
   |   +-- Roles: PCB Layout Engineer (primary)
   |   +-- Minimum model tier: Sonnet+ (documented in SKILL.md)
   |   +-- Activities: layout review, routing analysis, DRC
   |   +-- kicad-happy skills consumed: kicad
   |
   3g. DRC GATE
   |   +-- Consumes kicad-happy:kicad for DRC parsing
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ DRC GATE                                             │
   |       │                                                      │
   |       │ [ERROR] V-001: Trace width 0.10mm < JLCPCB min      │
   |       │   0.127mm @ Layer F.Cu (42.3, 18.7)                 │
   |       │   Fix: Increase trace width to >= 0.127mm           │
   |       │ [WARNING] V-002: Via annular ring 0.15mm             │
   |       │   (JLCPCB recommends >= 0.153mm)                    │
   |       │                                                      │
   |       │ Errors: 1 | Warnings: 1                              │
   |       │ Result: NOT_DONE -- errors must be resolved          │
   |       └──────────────────────────────────────────────────────┘
   |
   ===== STAGE 4: PROTOTYPE [Human-execution] =====
   |
   4. Pipeline dispatches Prototype stage via Agent tool
   |   +-- Roles: Test Engineer (primary), EE (support)
   |   +-- Execution mode: gate-in/human-action/gate-out
   |   +-- Activities: ordering package generation, test fixture
   |       requirements, bring-up test procedure
   |   +-- Sub-agent produces: ordering checklist, test procedure,
   |       bring-up sequence
   |   +-- Output + CHECKPOINT:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ PROTOTYPE STAGE                                      │
   |       │                                                      │
   |       │ Artifacts generated:                                 │
   |       │  - Ordering package (Gerber + BOM/CPL for JLCPCB)   │
   |       │  - Bring-up test procedure (14 steps)                │
   |       │  - Test fixture requirements                         │
   |       │                                                      │
   |       │ === HUMAN ACTION REQUIRED ===                        │
   |       │ 1. Order prototype boards from JLCPCB                │
   |       │ 2. Assemble and bring up prototype                   │
   |       │ 3. Execute bring-up test procedure                   │
   |       │ 4. Record test results                               │
   |       │                                                      │
   |       │ When complete, confirm: "prototype complete"         │
   |       │ To report issues: "prototype failed: [description]"  │
   |       └──────────────────────────────────────────────────────┘
   |   +-- Pipeline PAUSES -- awaits human confirmation
   |   +-- User: "prototype complete" --> gate evaluates
   |   +-- User: "prototype failed: ..." --> triggers rework (Flow 4)
   |
   ===== STAGE 5: DFM/DFA [AI-execution] =====
   |
   5. Pipeline dispatches DFM/DFA stage via Agent tool
   |   +-- Roles: Manufacturing Engineer (primary)
   |   +-- Activities: DFM review, DFA review, yield risk
   |   +-- kicad-happy skills consumed: jlcpcb (or pcbway), bom
   |
   5g. DFM GATE + BOM GATE (evaluated together)
   |   +-- DFM: fab-specific rules (trace/space, via, mask, clearance)
   |   +-- BOM: cost vs budget, availability, lifecycle, second-source
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ DFM GATE                                             │
   |       │ [DONE] All DFM rules pass for JLCPCB                │
   |       │                                                      │
   |       │ BOM GATE                                             │
   |       │ [WARNING] C12 (LM1117-3.3): single-source (TI only) │
   |       │ [DONE] Total BOM: $11.23 (within $12.50 budget)     │
   |       │ [DONE] All components active lifecycle               │
   |       │                                                      │
   |       │ Result: PASS -- advancing to Compliance              │
   |       └──────────────────────────────────────────────────────┘
   |
   ===== STAGE 6: COMPLIANCE [AI-execution] =====
   |
   6. Pipeline dispatches Compliance stage via Agent tool
   |   +-- Roles: Compliance Engineer (primary)
   |   +-- Activities: EMC pre-compliance, safety analysis,
   |       environmental compliance, regulatory documentation
   |   +-- kicad-happy skills consumed: emc, kidoc
   |
   6g. COMPLIANCE GATE
   |   +-- Per-region checklist (FCC, CE from config)
   |   +-- Evidence-linked requirements
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ COMPLIANCE GATE                                      │
   |       │                                                      │
   |       │ FCC Part 15:                                         │
   |       │  [DONE] Radiated emissions (EMC report linked)      │
   |       │  [DONE] Conducted emissions (EMC report linked)     │
   |       │  [DONE] Labeling requirements                        │
   |       │ CE RED:                                              │
   |       │  [DONE] EN 55032 (EMC report linked)                │
   |       │  [NOT_DONE] EN 62368-1 safety (no evidence)         │
   |       │                                                      │
   |       │ Result: NOT_DONE -- missing safety evidence          │
   |       └──────────────────────────────────────────────────────┘
   |
   ===== STAGE 7: PILOT RUN [Human-execution] =====
   |
   7. Pipeline dispatches Pilot Run stage via Agent tool
   |   +-- Execution mode: gate-in/human-action/gate-out
   |   +-- Sub-agent produces: manufacturing transfer package,
   |       production test procedure, yield targets
   |   +-- Output + CHECKPOINT (same pattern as Prototype)
   |   +-- Pipeline PAUSES -- awaits human confirmation
   |
   ===== STAGE 8: PRODUCTION RELEASE [Human-execution] =====
   |
   8. Pipeline dispatches Production Release stage via Agent tool
   |   +-- Execution mode: gate-in/human-action/gate-out
   |   +-- Sub-agent produces: production checklist, final BOM,
   |       compliance package, release documentation
   |   +-- kicad-happy skills consumed: kidoc, bom
   |   +-- Output + CHECKPOINT
   |   +-- Pipeline PAUSES -- awaits human confirmation
   |
   8g. FINAL GATE
   |   +-- All artifacts complete, all gates passed
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ PIPELINE COMPLETE: sensor-board-v2                   │
   |       │                                                      │
   |       │ Stages: 8/8 complete                                 │
   |       │ Gates: 7/7 passed                                    │
   |       │ Reworks: 2 (Schematic x1, Layout x1)                │
   |       │ Artifacts: 24 files in .hardware/artifacts/          │
   |       │                                                      │
   |       │ Lessons captured to .hardware/memory/                │
   |       └──────────────────────────────────────────────────────┘
   |
[End] Pipeline complete
```

### Design Review Board Integration (Flow 2 sub-flow)

**Covers**: FR-015, Story 5.1

At key stage transitions (post-Schematic, post-Layout), the Design Review Board pattern activates:

```
   DESIGN REVIEW BOARD (triggered at Schematic and Layout gates)
   |
   1. Orchestrator dispatches independent reviews to:
   |   +-- Electrical Engineer (schematic correctness)
   |   +-- PCB Layout Engineer (layout feasibility)
   |   +-- Manufacturing Engineer (manufacturability)
   |   +-- Compliance Engineer (regulatory impact)
   |   (Each reviews independently -- no shared context during review)
   |
   2. Findings aggregated with deduplication
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ DESIGN REVIEW BOARD: Post-Schematic                  │
   |       │                                                      │
   |       │ EE Review:                                           │
   |       │  [CRITICAL] Missing level shifter on U2-SDA          │
   |       │  [MAJOR] Capacitor C7 derated below 50%              │
   |       │                                                      │
   |       │ MfgE Review:                                         │
   |       │  [MAJOR] QFN-48 not in JLCPCB basic parts           │
   |       │  [MINOR] Footprint 0201 below JLCPCB recommended    │
   |       │                                                      │
   |       │ CompE Review:                                        │
   |       │  [WARNING] No filtering on USB data lines (EMC)     │
   |       │                                                      │
   |       │ PCB Layout Review:                                   │
   |       │  [MAJOR] BGA pitch requires 6-layer (4 configured)  │
   |       │                                                      │
   |       │ Deduplicated: 2 findings merged across reviewers     │
   |       │ Summary: 1 critical, 3 major, 1 minor, 1 warning    │
   |       └──────────────────────────────────────────────────────┘
   |
   3. Unified severity ranking determines gate result

   --- DRB Zero Findings Case ---

   When ALL reviewers return APPROVE with no findings:
   |
   1. Findings aggregation detects zero unique findings
   |
   2. Output uses a collapsed summary (no per-reviewer breakdown):
   |       ┌──────────────────────────────────────────────────────┐
   |       │ DESIGN REVIEW BOARD: Post-Schematic                  │
   |       │                                                      │
   |       │ Reviewers: EE, MfgE, CompE, PCB Layout               │
   |       │ Findings: 0                                           │
   |       │                                                      │
   |       │ All reviewers: APPROVE -- no findings.                │
   |       │                                                      │
   |       │ Result: PASS -- advancing to next stage               │
   |       └──────────────────────────────────────────────────────┘
   |
   3. Gate result: PASS -- pipeline advances automatically

   Design decision: The zero-findings output collapses to a single
   summary line ("All reviewers: APPROVE -- no findings") rather
   than listing each reviewer with "No findings" underneath. This
   is intentional:
     - A clean pass is the happy path -- it should be fast to read
     - Per-reviewer empty blocks add visual noise without information
     - The reviewer names are still listed (for audit trail) but
       their individual sections are omitted
     - If ANY reviewer has findings, the full per-reviewer breakdown
       is shown (existing pattern above)
```

---

## Flow 3: Stage Interaction

**User Goal**: Understand what happens during each stage -- what I see, what I approve, what I can influence.
**Primary Persona**: Elena, Marcus
**Covers**: FR-002, FR-003, FR-008, FR-020

> "In place of a confusing pipeline, you would have one... beautiful and terrible as the dawn. Tempestuous as the sea, and stronger than the foundations of the earth."

### 3A: AI-Execution Stage Pattern (Concept, Schematic, Layout, DFM/DFA, Compliance)

```
[Stage Start]
   |
   1. Stage banner displayed
   |       ┌──────────────────────────────────────────────────────┐
   |       │ ===== STAGE N: [NAME] [AI-execution] =====          │
   |       │ Roles: [list of roles dispatched]                    │
   |       │ Activities: [key activities]                         │
   |       │ kicad-happy skills: [list if applicable]             │
   |       └──────────────────────────────────────────────────────┘
   |
   2. Pipeline dispatches sub-agent(s) via Agent tool
   |   +-- Sub-agent loads ONLY its role's references (context isolation)
   |   +-- Sub-agent consumes kicad-happy skills as needed (transparent)
   |   +-- Sub-agent produces artifacts
   |
   3. Artifacts presented to user
   |       ┌──────────────────────────────────────────────────────┐
   |       │ ARTIFACTS: Stage [N] - [Name]                        │
   |       │                                                      │
   |       │ 1. [artifact-name.md] -- [description]               │
   |       │ 2. [artifact-name.md] -- [description]               │
   |       │    ...                                               │
   |       │                                                      │
   |       │ Saved to: .hardware/artifacts/[stage-name]/          │
   |       └──────────────────────────────────────────────────────┘
   |
   4. Gate validation runs automatically
   |   +-- ALL validators must report DONE
   |   +-- If PASS: pipeline advances (no user action needed)
   |   +-- If NOT_DONE: findings presented, user acts (see below)
   |
   4a. Gate PASS:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ GATE: [Stage N] --> [Stage N+1]                      │
   |       │ [DONE] Validator 1                                   │
   |       │ [DONE] Validator 2                                   │
   |       │ Result: PASS -- advancing to [Stage N+1]             │
   |       └──────────────────────────────────────────────────────┘
   |
   4b. Gate NOT_DONE:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ GATE: [Stage N] --> [Stage N+1]                      │
   |       │ [DONE] Validator 1                                   │
   |       │ [NOT_DONE] Validator 2: [failure reason]             │
   |       │   Finding: [ID] [severity] [description]             │
   |       │   Location: [where in the design]                    │
   |       │   Fix: [specific remediation guidance]               │
   |       │ Result: NOT_DONE -- resolve findings to proceed      │
   |       └──────────────────────────────────────────────────────┘
   |   +-- Sub-agent receives failing feedback
   |   +-- Sub-agent corrects and re-runs
   |   +-- Gate re-evaluates (automatic self-correction loop)
   |
[Stage End]
```

**User actions during AI-execution stages:**
- **Observe**: User sees stage progress, artifacts, gate results
- **Intervene** (optional): User can provide guidance ("focus on power integrity") or override ("skip compliance for this prototype")
- **Wait**: Most AI-execution stages run autonomously

### 3B: Human-Execution Stage Pattern (Prototype, Pilot Run, Production Release)

```
[Stage Start]
   |
   1. Stage banner displayed
   |       ┌──────────────────────────────────────────────────────┐
   |       │ ===== STAGE N: [NAME] [Human-execution] =====       │
   |       │ Mode: gate-in / human-action / gate-out              │
   |       │ Roles: [list of roles producing preparation docs]    │
   |       └──────────────────────────────────────────────────────┘
   |
   2. Gate-in: Sub-agent generates preparation documentation
   |   +-- Ordering packages, test procedures, checklists, etc.
   |
   3. Documentation presented with action items
   |       ┌──────────────────────────────────────────────────────┐
   |       │ === HUMAN ACTION REQUIRED ===                        │
   |       │                                                      │
   |       │ Preparation artifacts:                               │
   |       │  1. [document] -- [description]                      │
   |       │  2. [document] -- [description]                      │
   |       │                                                      │
   |       │ Action items:                                        │
   |       │  [ ] Step 1: [what to do physically]                 │
   |       │  [ ] Step 2: [what to do physically]                 │
   |       │  [ ] Step 3: [what to do physically]                 │
   |       │                                                      │
   |       │ When complete, confirm: "[stage] complete"           │
   |       │ To report issues: "[stage] failed: [description]"   │
   |       │ To pause and resume later: "save pipeline state"    │
   |       └──────────────────────────────────────────────────────┘
   |
   4. Pipeline PAUSES -- awaits human input
   |   +-- User confirms: "[stage] complete"
   |       --> Gate-out evaluates, pipeline advances
   |   +-- User reports failure: "[stage] failed: [description]"
   |       --> Rework triggered (Flow 4)
   |   +-- User saves: "save pipeline state"
   |       --> State persisted, user can resume later (Flow 7)
   |
[Stage End]
```

### 3C: Gate Failure Self-Correction Loop

```
   Gate evaluates --> NOT_DONE
   |
   1. Failing feedback returned to stage sub-agent
   |
   2. Sub-agent attempts correction
   |   +-- Reads failure reason and location
   |   +-- Modifies artifact or invokes kicad-happy skill
   |   +-- Produces corrected artifact
   |
   3. Gate re-evaluates
   |   +-- If PASS: pipeline advances
   |   +-- If NOT_DONE: repeat (bounded by session context)
   |
   Note: This self-correction is within a single stage.
   Cross-stage rework (e.g., layout issue caused by schematic)
   triggers the rework flow (Flow 4) instead.
```

---

## Flow 4: Rework

**User Goal**: Handle the situation where a downstream stage reveals an issue that requires returning to an earlier stage.
**Primary Persona**: Elena, Marcus
**Happy Path Steps**: 5
**Covers**: FR-007, NFR-010, Story 1.7

> "I can see the rework that is needed. Even the wisest engineer cannot foresee all ends. The circuit must be revised, the layout reconsidered."

### Defined Rework Paths

| Source Stage | Target Stage | Trigger Example |
|-------------|-------------|-----------------|
| Prototype | Schematic | Prototype reveals fundamental circuit error |
| Prototype | Layout | Prototype reveals routing/thermal issue |
| DFM/DFA | Layout | DFM violation requires layout change |
| DFM/DFA | Schematic | DFM issue requires component substitution |
| Compliance | Schematic | EMC failure requires filtering/shielding redesign |
| Pilot Run | DFM/DFA | Pilot run reveals assembly yield issue |

### Rework Happy Path

```
[Rework Trigger] Gate identifies cross-stage issue
   |
   1. Pipeline identifies rework path
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ REWORK TRIGGERED                                     │
   |       │                                                      │
   |       │ Source: DFM/DFA (Stage 5)                            │
   |       │ Target: Schematic (Stage 2)                          │
   |       │ Reason: Component U5 (QFN-48) not available at      │
   |       │   JLCPCB. Requires component substitution.          │
   |       │                                                      │
   |       │ Rework path: DFM/DFA --> Schematic                  │
   |       │ Iteration: 1 of 3 (per-path limit)                  │
   |       │ Total reworks this run: 2 of 10                      │
   |       │                                                      │
   |       │ Returning to Schematic stage with rework context...  │
   |       └──────────────────────────────────────────────────────┘
   |
   2. Target stage re-executes with rework context
   |   +-- Sub-agent receives:
   |       - Original stage artifacts
   |       - Rework reason and source stage
   |       - Specific issue to address
   |   +-- Sub-agent corrects the design
   |
   3. Target stage gate re-evaluates
   |   +-- Must pass before advancing
   |
   4. ALL downstream gates re-validated (not skipped)
   |   +-- Layout gate re-runs
   |   +-- Prototype gate re-runs (if already passed)
   |   +-- DFM gate re-runs
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ DOWNSTREAM RE-VALIDATION                             │
   |       │                                                      │
   |       │ Schematic Gate: [DONE] (re-validated)                │
   |       │ Layout Gate: [DONE] (re-validated)                   │
   |       │ DFM Gate: [DONE] (re-validated)                      │
   |       │                                                      │
   |       │ Rework resolved. Pipeline advancing from DFM/DFA.   │
   |       └──────────────────────────────────────────────────────┘
   |
   5. Rework history logged
   |   +-- Persisted to .hardware/state.md
   |   +-- Includes: timestamp, source, target, reason, resolution
   |
[End] Pipeline resumes forward progress
```

### Rework Termination (Per-Path Limit Hit)

```
   Rework path triggered for the Nth time (N > max_rework_iterations)
   |
   1. Pipeline detects per-path limit reached
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ REWORK LIMIT REACHED                                 │
   |       │                                                      │
   |       │ Limit type: Per-path                                 │
   |       │ Path: DFM/DFA --> Schematic                          │
   |       │ Iterations: 3/3 (limit reached)                      │
   |       │                                                      │
   |       │ Rework history for this path:                        │
   |       │  #1: Component U5 unavailable --> substituted U5B    │
   |       │  #2: U5B footprint incompatible --> substituted U5C  │
   |       │  #3: U5C voltage range insufficient --> ?            │
   |       │                                                      │
   |       │ Recurring pattern: Component selection for U5        │
   |       │ position is failing repeatedly.                      │
   |       │                                                      │
   |       │ RECOMMENDATION: Manual intervention needed.          │
   |       │ Consider redesigning the power regulation approach   │
   |       │ rather than iterating on component substitution.     │
   |       │                                                      │
   |       │ === PIPELINE PAUSED ===                              │
   |       │ Options:                                             │
   |       │  "continue" -- override limit, try once more         │
   |       │  "abort" -- stop the pipeline run                    │
   |       │  "override limit N" -- set new per-path limit        │
   |       └──────────────────────────────────────────────────────┘
   |
   2. User decides:
   |   +-- "continue" --> one more iteration allowed
   |   +-- "abort" --> pipeline terminates, state saved
   |   +-- "override limit 5" --> limit raised, pipeline continues
```

### Rework Termination (Total Limit Hit)

```
   Total rework count across ALL paths hits max_total_reworks
   |
   1. Pipeline detects total limit reached
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ TOTAL REWORK LIMIT REACHED                           │
   |       │                                                      │
   |       │ Limit type: Total (across all paths)                 │
   |       │ Total reworks: 10/10 (limit reached)                 │
   |       │                                                      │
   |       │ Rework summary:                                      │
   |       │  DFM-->Schematic: 3 iterations                       │
   |       │  DFM-->Layout: 2 iterations                          │
   |       │  Prototype-->Layout: 3 iterations                    │
   |       │  Compliance-->Schematic: 2 iterations                │
   |       │                                                      │
   |       │ RECOMMENDATION: This design is experiencing          │
   |       │ systemic iteration. Reassess the overall design      │
   |       │ approach before continuing.                          │
   |       │                                                      │
   |       │ === PIPELINE PAUSED ===                              │
   |       │ Options:                                             │
   |       │  "continue" -- override, allow more reworks          │
   |       │  "abort" -- stop the pipeline run                    │
   |       │  "override total N" -- set new total limit           │
   |       └──────────────────────────────────────────────────────┘
```

### Rework From Human-Execution Stage

When a human-execution stage (Prototype, Pilot Run, Production Release) triggers
rework, the transition differs from AI-execution stage rework because there is an
active human checkpoint with generated artifacts (ordering packages, test procedures,
etc.). This sub-flow defines what happens.

> "The prototype has spoken, and its verdict is grim. The human checkpoint must be released, its artifacts archived -- not destroyed, for even failed prototypes carry wisdom."

**Trigger**: User reports failure from a human-execution stage, e.g.:
- `"prototype failed: thermal issue on U3"`
- `"pilot run failed: solder bridging on U12 QFN pad"`
- `"production release failed: yield below 85%"`

```
[Rework From Human-Execution Stage]
   |
   1. User input parsed for failure description
   |   +-- Pipeline detects: stage is human-execution, state is PAUSED
   |   +-- Failure description extracted from user message
   |
   2. Human checkpoint INVALIDATED
   |   +-- Checkpoint state transitions: PENDING --> INVALIDATED
   |   +-- Pipeline state transitions: PAUSED --> REWORK_INITIATED
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ HUMAN CHECKPOINT INVALIDATED                         │
   |       │                                                      │
   |       │ Stage: Prototype (Stage 4)                            │
   |       │ Status: INVALIDATED (was: PENDING human action)      │
   |       │ Reason: "thermal issue on U3"                         │
   |       └──────────────────────────────────────────────────────┘
   |
   3. Stage artifacts ARCHIVED (never deleted)
   |   +-- Existing preparation artifacts moved:
   |       FROM: .hardware/artifacts/prototype/
   |       TO:   .hardware/artifacts/prototype/archived/run-N/
   |   +-- Archived artifacts include:
   |       - Ordering package (Gerber + BOM/CPL)
   |       - Bring-up test procedure
   |       - Test fixture requirements
   |       - Any user-provided test results or notes
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ ARTIFACTS ARCHIVED                                   │
   |       │                                                      │
   |       │ 3 artifacts archived to:                              │
   |       │   .hardware/artifacts/prototype/archived/run-1/      │
   |       │                                                      │
   |       │ Archived artifacts are preserved for reference.       │
   |       │ They will NOT be used by subsequent stages.           │
   |       └──────────────────────────────────────────────────────┘
   |
   4. Rework path determined (same logic as AI-stage rework)
   |   +-- Uses Defined Rework Paths table (above)
   |   +-- Output: standard REWORK TRIGGERED block (see Rework Happy Path)
   |
   5. Target stage re-executes with rework context
   |   +-- Sub-agent receives failure description as additional context
   |   +-- Example: EE sub-agent told "thermal issue on U3 during
   |       prototype testing" when re-executing Schematic stage
   |
   6. Downstream gates re-validated (gate re-evaluation, NOT stage re-execution)
   |   +-- AI-execution stage gates: re-evaluated against updated artifacts
   |   +-- Human-execution stage gates: gate-in re-executes to generate
   |       FRESH preparation artifacts (new ordering package, new test
   |       procedure reflecting the design changes)
   |   +-- The human checkpoint re-presents from scratch:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ ===== STAGE 4: PROTOTYPE [Human-execution] =====    │
   |       │ (Re-entry after rework from Schematic)               │
   |       │                                                      │
   |       │ Previous attempt archived: run-1                     │
   |       │ Rework reason: thermal issue on U3                   │
   |       │ Changes since last attempt:                          │
   |       │  - U3 replaced: LM1117 --> TPS563201 (better Tj)    │
   |       │  - Thermal via array added under U3 pad              │
   |       │                                                      │
   |       │ NEW artifacts generated:                              │
   |       │  - Ordering package (Gerber + BOM/CPL for JLCPCB)   │
   |       │  - Bring-up test procedure (16 steps -- 2 added      │
   |       │    for thermal validation of U3)                     │
   |       │  - Test fixture requirements (updated)               │
   |       │                                                      │
   |       │ === HUMAN ACTION REQUIRED ===                        │
   |       │ 1. Order NEW prototype boards from JLCPCB            │
   |       │ 2. Assemble and bring up prototype                   │
   |       │ 3. Execute bring-up test procedure                   │
   |       │ 4. Record test results                               │
   |       │                                                      │
   |       │ When complete, confirm: "prototype complete"         │
   |       │ To report issues: "prototype failed: [description]"  │
   |       └──────────────────────────────────────────────────────┘
   |   +-- Pipeline PAUSES again -- awaits new human confirmation
   |
   7. Rework history logged (same as AI-stage rework)
   |   +-- Includes: archived artifact path, failure description,
   |       human checkpoint invalidation timestamp
   |
[End] Pipeline awaits human completion of re-entered stage
```

**State Transition Summary (Human-Execution Rework)**:

| State Element | Before Rework | During Rework | After Re-Entry |
|---------------|---------------|---------------|----------------|
| Human checkpoint | PENDING | INVALIDATED | NEW PENDING (fresh) |
| Preparation artifacts | Active in stage dir | Archived to `archived/run-N/` | Fresh artifacts generated |
| Pipeline state | PAUSED | REWORK_INITIATED --> executing target stage | PAUSED (new checkpoint) |
| Previous test results | N/A (or user-provided) | Archived with artifacts | Not carried forward |
| Rework counter | N | N+1 | N+1 (unchanged at re-entry) |

**Key Design Decisions**:

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| Archive, never delete previous artifacts | Failed prototypes carry diagnostic value; deletion risks losing physical test data the user recorded | Delete (rejected: loses data); leave in-place (rejected: ambiguous which are current) |
| Fresh artifacts on re-entry | Design changes after rework mean old ordering packages and test procedures are stale and unsafe to use | Reuse previous artifacts (rejected: stale after rework); diff-only update (rejected: too error-prone for physical manufacturing) |
| Gate re-evaluation not stage re-execution for AI stages | Re-running an entire AI stage is expensive and redundant when only the gate result needs checking against updated artifacts | Full re-execution (rejected: wasted compute); skip re-validation (rejected: unsafe -- downstream may be invalidated) |
| Human stages always re-present full checkpoint | User needs clear instructions for the new physical action; partial instructions risk manufacturing errors | Diff-only re-presentation (rejected: confusing for physical actions) |

---

## Flow 5: kicad-happy Integration

**User Goal**: Use kicad-happy capabilities seamlessly within the hardware pipeline without needing to invoke them manually.
**Primary Persona**: Elena
**Covers**: FR-009, NFR-003, Story 3.1, Story 3.2, Story 3.3, Story 3.4, Story 3.5, Story 3.6

> "I know what you saw in the mirror of component datasheets. You saw the BOM struggling, lost in a forest of obsolete parts. I can show you a different path -- through the integration layer."

### 5A: Transparent Integration (Default -- User Does Not See kicad-happy)

In the normal pipeline flow, kicad-happy skills are consumed transparently by hardware roles. The user sees the *results*, not the invocation mechanism.

```
   EE role executing during Schematic stage
   |
   1. EE sub-agent needs component data
   |   +-- Integration layer dispatches to kicad-happy:digikey
   |   +-- (Transparent to user -- no output about skill dispatch)
   |
   2. User sees ONLY the role's output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ COMPONENT SELECTION: U3 Voltage Regulator            │
   |       │                                                      │
   |       │ Selected: TPS563201 (TI)                             │
   |       │  - Unit price: $0.85 @ 100qty (DigiKey)              │
   |       │  - Stock: 12,450 units                               │
   |       │  - Lifecycle: Active                                  │
   |       │  - Second source: MP2315 (MPS) @ $0.92               │
   |       │  - Datasheet: downloaded to datasheets/TPS563201.pdf │
   |       │                                                      │
   |       │ Rationale: Meets Vin (5-17V), Vout (3.3V @3A),      │
   |       │ available at JLCPCB basic parts library.             │
   |       └──────────────────────────────────────────────────────┘
   |
   (kicad-happy:digikey was invoked, user sees the engineering result)
```

### 5B: Role-to-Skill Mapping (What Happens Behind the Scenes)

```
   Hardware Role                 kicad-happy Skills Consumed
   ─────────────                 ──────────────────────────
   Electrical Engineer    -->    kicad, spice, digikey, mouser, lcsc, element14
   PCB Layout Engineer    -->    kicad
   Manufacturing Engineer -->    jlcpcb, pcbway, bom
   Compliance Engineer    -->    emc, kidoc
   Test Engineer          -->    (none directly -- uses artifacts from above)
   HW Product Owner       -->    (none directly -- uses artifacts from above)
```

### 5C: Graceful Failure When kicad-happy Skill Unavailable

```
   Role sub-agent needs kicad-happy:spice
   |
   1. Integration layer attempts dispatch
   |   +-- Skill not available (not installed)
   |
   2. Graceful failure output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ WARNING: kicad-happy:spice not available             │
   |       │                                                      │
   |       │ Cannot perform SPICE simulation. The Electrical      │
   |       │ Engineer role requires this skill for circuit        │
   |       │ validation.                                          │
   |       │                                                      │
   |       │ Install kicad-happy via the Claude Code plugin       │
   |       │ system to enable simulation capabilities.            │
   |       │                                                      │
   |       │ Pipeline continuing without simulation data.         │
   |       │ Schematic Review Gate may flag unvalidated circuits. │
   |       └──────────────────────────────────────────────────────┘
   |
   3. Pipeline continues (skill unavailability is degraded, not fatal)
   |   +-- Gate may flag the missing validation as a finding
```

### 5D: BOM Reconciliation Pattern (Cross-Supplier Validation)

**Covers**: FR-016, Story 5.2

```
   BOM ready for reconciliation
   |
   1. Pattern dispatches queries to multiple sourcing skills:
   |   +-- kicad-happy:digikey  --> pricing/stock for each part
   |   +-- kicad-happy:mouser   --> pricing/stock for each part
   |   +-- kicad-happy:lcsc     --> pricing/stock for each part
   |   +-- kicad-happy:element14 --> pricing/stock for each part
   |
   2. Results compared and reconciled
   |       ┌──────────────────────────────────────────────────────┐
   |       │ BOM RECONCILIATION                                   │
   |       │                                                      │
   |       │ 24 line items checked across 4 suppliers             │
   |       │                                                      │
   |       │ PRICE DISCREPANCIES (>20%):                          │
   |       │  C5 (100nF 0402): DigiKey $0.008 vs LCSC $0.003     │
   |       │    Recommendation: source from LCSC (62% savings)   │
   |       │                                                      │
   |       │ SINGLE-SOURCE RISKS:                                 │
   |       │  U7 (ATECC608B): Available only from Mouser          │
   |       │    Recommendation: evaluate ATECC608C as alt         │
   |       │                                                      │
   |       │ AVAILABILITY ISSUES:                                 │
   |       │  J3 (USB-C connector): 0 stock at DigiKey            │
   |       │    Available at LCSC (4,200 units)                   │
   |       └──────────────────────────────────────────────────────┘
```

---

## Flow 6: Config-Driven Adaptation

**User Goal**: Have the pipeline adapt its behavior based on my project configuration -- a 1-layer prototype should not go through the same compliance rigor as an 8-layer production board.
**Primary Persona**: Elena (prototype), Marcus (production)
**Covers**: FR-004, FR-021, Story 1.4, NFR-006

> "Instead of a one-size-fits-all pipeline, you would have one... beautiful and terrible as the dawn. Each project receives the scrutiny it deserves, neither more nor less."

### 6A: P1 -- Static Config Reading (How Config Influences Pipeline Today)

In Phase 1, the config is read at pipeline start and passed to stages/gates as parameters. The pipeline structure (all 8 stages) does not change -- but gate behavior adapts.

```
   Config: target_fab: jlcpcb
   |
   Effect on pipeline:
   +-- DFM Gate uses JLCPCB-specific rules (not generic)
   +-- Manufacturing Engineer invokes kicad-happy:jlcpcb (not pcbway)
   +-- Prototype stage generates JLCPCB ordering package

   Config: compliance_regions: [FCC, CE]
   |
   Effect on pipeline:
   +-- Compliance Gate produces checklists for FCC AND CE
   +-- Compliance Engineer evaluates both region's requirements
   +-- Missing evidence for either region blocks advancement

   Config: bom_budget: 12.50
   |
   Effect on pipeline:
   +-- BOM Gate compares total cost against $12.50
   +-- Over-budget triggers NOT_DONE with cost breakdown

   Config: layers: 4
   |
   Effect on pipeline:
   +-- Layout stage knows stackup constraints
   +-- DFM Gate validates 4-layer compatibility at target fab

   Config: rework.max_rework_iterations: 3
   Config: rework.max_total_reworks: 10
   |
   Effect on pipeline:
   +-- Rework loops terminate at configured limits
   +-- Escalation to human when limits are hit
```

### 6B: P2 (Future) -- Dynamic Pipeline Adaptation

```
   P2 auto-detection (not in Phase 1):
   |
   Simple prototype (1-2 layers, no compliance, hobby):
   +-- Compliance stage: MINIMIZED (basic checks only)
   +-- Pilot Run stage: SKIPPED (not needed for <10 units)
   +-- Production Release stage: SKIPPED
   +-- Gate strictness: relaxed
   |
   Production board (4+ layers, FCC+CE, >1000 units):
   +-- All 8 stages fully executed
   +-- Gate strictness: strict
   +-- Full compliance checklists
   +-- Manufacturing transfer package required
```

### 6C: Config Forward Compatibility

```
   User has config v1.0, plugin updated to v1.1:
   |
   1. SessionStart hook detects version mismatch
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ Config schema v1.0 detected; current is v1.1.       │
   |       │ New fields in v1.1: gate_strictness, model_tiers    │
   |       │ Using defaults for missing fields. Pipeline OK.     │
   |       │ Run hw-setup to update config.                       │
   |       └──────────────────────────────────────────────────────┘
   |
   2. Pipeline runs normally -- missing keys use defaults
   |   (Old configs NEVER break the pipeline -- NFR-006)
```

---

## Flow 7: Resume

**User Goal**: Resume a hardware pipeline that was interrupted (session ended, user paused, connection lost).
**Primary Persona**: Elena
**Happy Path Steps**: 4
**Covers**: FR-005, Story 1.5

> "The pipeline may be broken, but it is not ended. Its state endures in the file of persistence."

### Resume Happy Path

```
[Start] User starts new session with existing .hardware/state.md
   |
   1. SessionStart hook fires
   |   +-- Detects .hardware/state.md with persisted pipeline state
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ hardware-team: Persisted pipeline state found.       │
   |       │                                                      │
   |       │ Pipeline: sensor-board-v2                             │
   |       │ Last stage completed: Layout (Stage 3)               │
   |       │ Current stage: Prototype (Stage 4) -- PAUSED         │
   |       │ Human action pending: Order and test prototype       │
   |       │ Rework history: 1 (Schematic rework from Layout)    │
   |       │                                                      │
   |       │ To resume: "Resume hardware pipeline"                │
   |       │ To start fresh: "New hardware pipeline"              │
   |       └──────────────────────────────────────────────────────┘
   |
   2. User: "Resume hardware pipeline"
   |
   3. Pipeline loads persisted state
   |   +-- Completed stages (1-3): NOT re-executed
   |   +-- Their artifacts: available to subsequent stages
   |   +-- Their gate results: preserved
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ RESUMING PIPELINE: sensor-board-v2                   │
   |       │                                                      │
   |       │ Completed: Concept, Schematic, Layout                │
   |       │ Resuming at: Prototype (Stage 4)                     │
   |       │                                                      │
   |       │ === HUMAN ACTION REQUIRED ===                        │
   |       │ (Same checkpoint as when paused)                     │
   |       └──────────────────────────────────────────────────────┘
   |
   4. Pipeline continues from the last completed stage
   |
[End] Pipeline execution resumes normally
```

### Resume After Session Timeout

```
   Session ends unexpectedly (timeout, connection lost)
   |
   1. State auto-saved to .hardware/state.md on session end
   |   +-- Current stage, gate results, artifact paths persisted
   |
   2. Next session: same as Resume Happy Path above
```

### Resume with Stale State

```
   User modified KiCad files between sessions (outside pipeline)
   |
   1. Resume detects file changes
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ WARNING: Source files modified since last pipeline    │
   |       │ run. Schematic (.kicad_sch) changed.                 │
   |       │                                                      │
   |       │ Completed gates may need re-validation.              │
   |       │ Options:                                             │
   |       │  "resume" -- continue from last stage (skip recheck) │
   |       │  "revalidate" -- re-run gates from modified stage   │
   |       │  "restart" -- start pipeline from beginning          │
   |       └──────────────────────────────────────────────────────┘
```

---

## Flow 8: Hook-Driven Automation

**User Goal**: Benefit from automatic validation and drift detection without explicit invocation.
**Covers**: FR-017, FR-018, FR-019, Story 5.3, Story 5.4, Story 5.5

### 8A: SessionStart Hook (Config + Dependency Validation)

Already shown in Flow 1. Fires automatically on every session start. No user action needed.

### 8B: PostToolUse Hook -- Schematic DRC (P2)

```
   User edits a .kicad_sch file (via Write or Edit tool)
   |
   1. PostToolUse hook fires
   |   +-- Detects .kicad_sch extension
   |   +-- Runs DRC validation automatically
   |
   2a. No violations:
   |   +-- (Silent -- no output displayed)
   |
   2b. Violations found:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ DRC WARNING (auto-check on schematic edit):          │
   |       │  [W] Net SPI_CLK: no decoupling on U3 pin 7         │
   |       │  [W] Missing pull-up on I2C_SDA                     │
   |       └──────────────────────────────────────────────────────┘
   |
   (Warnings only -- never blocks the edit)
```

### 8C: PostToolUse Hook -- BOM Drift Detection (P2)

```
   User edits a .kicad_sch file (changes a component)
   |
   1. PostToolUse hook fires
   |   +-- Detects .kicad_sch extension
   |   +-- Checks if BOM artifact exists from previous stage
   |   +-- Compares schematic component list to BOM
   |
   2a. No drift:
   |   +-- (Silent)
   |
   2b. Drift detected:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ BOM DRIFT WARNING:                                   │
   |       │  + Added: U8 (new component, not in BOM)             │
   |       │  - Removed: U5 (in BOM but no longer in schematic)  │
   |       │  ~ Changed: C12 value (100nF --> 220nF)              │
   |       │                                                      │
   |       │ BOM needs updating. Re-run BOM Gate to reconcile.   │
   |       └──────────────────────────────────────────────────────┘
```

---

## Flow 9: Self-Learning Memory

**User Goal**: Have the pipeline learn from past runs and apply lessons to future projects.
**Covers**: FR-006, Story 1.6, NFR-008

### Memory Capture (End of Pipeline Run)

```
   Pipeline run completes (or aborts)
   |
   1. Lessons captured automatically
   |   +-- Gate failures and their resolutions
   |   +-- Rework triggers and patterns
   |   +-- Component substitutions that worked/failed
   |   +-- DFM violations and fixes
   |
   2. Stored to .hardware/memory/ (tiered chunked retrieval)
   |   +-- Output:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ Pipeline lessons captured:                           │
   |       │  3 new lessons saved to .hardware/memory/            │
   |       │  - "JLCPCB: 0201 footprint assembly unreliable"     │
   |       │  - "TPS563201: excellent cost/performance for 3A"   │
   |       │  - "USB-C: always add common-mode choke for CE"     │
   |       └──────────────────────────────────────────────────────┘
```

### Memory Injection (Start of Pipeline Run)

```
   New pipeline run starts
   |
   1. Memory loaded from .hardware/memory/
   |   +-- Relevant lessons matched to current context
   |   +-- Injected into stage prompts
   |
   2. User sees memory in pre-flight:
   |       ┌──────────────────────────────────────────────────────┐
   |       │ Memory: 5 lessons loaded                             │
   |       │  CAUTION: Previous project had DFM violation:       │
   |       │  trace width below JLCPCB minimum (0.127mm).        │
   |       │  Will be monitored during Layout stage.              │
   |       └──────────────────────────────────────────────────────┘
```

---

## FR Coverage Matrix

> "All shall be accounted for, and all shall be covered. Nothing shall remain in darkness."

Every functional requirement from the PRD is mapped to at least one user flow.

| FR ID | Requirement Summary | Covered In Flow(s) | Flow Section |
|-------|--------------------|--------------------|-------------|
| FR-001 | Standard plugin structure | Flow 1 | Setup wizard creates structure |
| FR-002 | 8-stage pipeline with AI/human classification | Flow 2, Flow 3 | Full pipeline; stage patterns 3A/3B |
| FR-003 | Stage gates with team DoD | Flow 2, Flow 3 | Gate outputs; self-correction 3C |
| FR-004 | Config-driven pipeline (.hardware/config.yml) | Flow 1, Flow 6 | Setup wizard; config adaptation |
| FR-005 | Pipeline state persistence and resume | Flow 7 | Resume flow |
| FR-006 | Self-learning memory | Flow 9 | Memory capture and injection |
| FR-007 | Rework loops with termination | Flow 4 | All rework paths, both limits |
| FR-008 | 6 role-based skills with context isolation | Flow 2, Flow 3 | Stage dispatches; role isolation |
| FR-009 | kicad-happy integration layer | Flow 5 | Transparent integration; failure |
| FR-010 | Schematic Review Gate (iterative, multi-reviewer) | Flow 2 | Schematic gate output |
| FR-011 | DRC Gate | Flow 2, Flow 3 | Layout gate output |
| FR-012 | BOM Gate | Flow 2, Flow 5 | DFM/DFA gate; BOM reconciliation |
| FR-013 | DFM Gate | Flow 2 | DFM/DFA gate output |
| FR-014 | Compliance Gate (evidence-linked per region) | Flow 2 | Compliance gate output |
| FR-015 | Design Review Board collaboration | Flow 2 | Design Review Board sub-flow |
| FR-016 | BOM Reconciliation pattern | Flow 5 | Section 5D |
| FR-017 | SessionStart hook (config + dependency validation) | Flow 1, Flow 8 | Setup; hook automation 8A |
| FR-018 | PostToolUse DRC hook | Flow 8 | Section 8B |
| FR-019 | PostToolUse BOM drift hook | Flow 8 | Section 8C |
| FR-020 | Sub-agent dispatch via Agent tool (not inlined) | Flow 2, Flow 3 | Every stage dispatch |
| FR-021 | Dynamic pipeline adaptation (P2) | Flow 6 | Section 6B (future) |
| FR-022 | Reference test fixture | Flow 2 | Gate validation references fixture |

### NFR Coverage

| NFR ID | Requirement | Covered In |
|--------|------------|------------|
| NFR-001 | No external dependencies | Flow 1 (no pip install in setup) |
| NFR-002 | Context isolation per role | Flow 3 (sub-agent dispatch pattern) |
| NFR-003 | kicad-happy consumed, not duplicated | Flow 5 (transparent integration) |
| NFR-004 | Full pipeline in single session | Flow 2 (end-to-end) |
| NFR-005 | Gate messages comprehensible | Flow 3 (output format: what, where, why, fix) |
| NFR-006 | Config forward compatibility | Flow 6 (section 6C) |
| NFR-007 | Model tier documented per role | Flow 3 (stage banner shows roles) |
| NFR-008 | Memory retrieval <2s | Flow 9 (tiered chunked retrieval) |
| NFR-009 | Plugin passes plugin-validator | Flow 1 (plugin structure) |
| NFR-010 | Rework history auditable | Flow 4 (rework history logging) |

### Story Coverage

| Story | Covered In Flow(s) |
|-------|-------------------|
| 1.1 | Flow 1 (plugin skeleton) |
| 1.2 | Flow 2, Flow 3 (pipeline orchestrator) |
| 1.3 | Flow 2, Flow 3 (gate framework) |
| 1.4 | Flow 1, Flow 6 (config) |
| 1.5 | Flow 7 (persistence and resume) |
| 1.6 | Flow 9 (self-learning memory) |
| 1.7 | Flow 4 (rework loops) |
| 1.8 | Flow 1 (marketplace registration) |
| 2.1-2.6 | Flow 2, Flow 3 (role dispatches) |
| 3.1-3.5 | Flow 5 (kicad-happy integration) |
| 3.6 | Flow 1, Flow 5 (dependency documentation) |
| 4.0-4.5 | Flow 2 (gates reference test fixture) |
| 5.1 | Flow 2 (Design Review Board) |
| 5.2 | Flow 5 (BOM Reconciliation) |
| 5.3 | Flow 1, Flow 8 (SessionStart hook) |
| 5.4 | Flow 8 (PostToolUse DRC hook) |
| 5.5 | Flow 8 (PostToolUse BOM drift hook) |

---

## Design Rationale

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| kicad-happy integration is transparent by default | Users want engineering results, not skill dispatch mechanics. The integration layer is an implementation detail. | Explicit invocation (rejected: adds friction without value) |
| Human-execution stages use explicit checkpoint pattern | Physical actions cannot be automated. The pipeline must pause and await human confirmation. | Auto-advance with timer (rejected: hardware actions take days/weeks) |
| Gate outputs include location + severity + fix | NFR-005 requires comprehensible messages. Hardware engineers need to know exactly what to fix and where. | Severity-only output (rejected: not actionable) |
| Rework limits configurable in config | Different projects have different iteration tolerance. A hobby prototype needs less rigor than a certified product. | Fixed limits (rejected: too rigid); no limits (rejected: infinite loops) |
| Setup wizard is sequential Q&A, not a form | CLI interaction is inherently sequential. Each question builds on previous answers. | Single-command with flags (rejected: too many options for first-time setup) |
| Design Review Board reviewers are independent | Per delivery-flow pattern: independent review prevents groupthink and ensures each role applies its own lens. | Sequential review chain (rejected: later reviewers biased by earlier findings) |
| Config errors warn but never fail the pipeline | FR-004: "never fails the pipeline due to config errors." Robustness over strictness. | Strict validation (rejected: blocks users who hand-edited config) |
| State persisted to .hardware/state.md (markdown) | Human-readable, inspectable, editable. Consistent with delivery-flow pattern. | SQLite (rejected: overkill for state); JSON (considered: less readable) |

---

## Assumptions

- The `.hardware/` namespace is used (not `.delivery/`) -- pending Architect confirmation (OQ-002)
- Users invoke the pipeline via natural language or skill name -- exact invocation syntax depends on plugin registration
- kicad-happy is installed as a separate plugin and is NOT part of this repository
- Human-execution stages may span days or weeks in real time (session persistence is critical)
- The setup wizard runs once per project; config can be manually edited afterward
- Gate re-validation after rework is automatic (not user-initiated)

---

## Follow-Up

- Confirm `.hardware/` namespace with Architect (OQ-002)
- Define exact model tier requirements per role with Architect (OQ-003)
- Validate rework DAG architecture with Architect (OQ-004)
- User research: validate checkpoint interaction pattern with Elena persona
- Usability testing: verify gate output format is comprehensible to hardware engineers

---

> "I have shown you the flows that could be. The path is clear, the gates are defined, the rework loops are bounded. Now the fellowship must build what has been designed."
