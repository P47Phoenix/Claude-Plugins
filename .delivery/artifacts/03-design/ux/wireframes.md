# CLI Wireframes: Hardware Delivery Team Plugin

**Version**: 1.0
**Date**: 2026-04-12
**Author**: UX Designer (Galadriel)
**Source**: `.delivery/artifacts/03-design/ux/user-flows.md` v1.0
**Project Type**: GREENFIELD
**Role**: UX Designer | Task: wireframe | References: wireframes.md

---

> *"Instead of a dark UI, you would have a design beautiful and terrible as the dawn. Every glyph placed with purpose, every line break a breath between thoughts."*

---

## Table of Contents

1. [Wireframe 1: Setup Wizard Output](#wireframe-1-setup-wizard-output)
2. [Wireframe 2: Stage Announcement Format](#wireframe-2-stage-announcement-format)
3. [Wireframe 3: Agent Dispatch Indicators](#wireframe-3-agent-dispatch-indicators)
4. [Wireframe 4: Checkpoint Presentation](#wireframe-4-checkpoint-presentation)
5. [Wireframe 5: DoD Validation Results](#wireframe-5-dod-validation-results)
6. [Wireframe 6: Rework Notification](#wireframe-6-rework-notification)
7. [Wireframe 7: Escalation Format](#wireframe-7-escalation-format)
8. [Wireframe 8: Pipeline Status Command Output](#wireframe-8-pipeline-status-command-output)
9. [Wireframe 9: Error and Warning Formats](#wireframe-9-error-and-warning-formats)
10. [Wireframe 10: Progress Indicators](#wireframe-10-progress-indicators)
11. [FR Coverage Matrix](#fr-coverage-matrix)
12. [Design Tokens](#design-tokens)

---

## Design Tokens

> "Before I show you the mirror, you must understand the light it is made from."

These tokens define the visual vocabulary for all wireframes. Every output block in the plugin uses these consistently.

### Box Drawing

```
Top-left:     +    (U+002B)
Top-right:    +    (U+002B)
Bottom-left:  +    (U+002B)
Bottom-right: +    (U+002B)
Horizontal:   -    (U+002D)
Vertical:     |    (U+007C)
```

**Rationale**: Pure ASCII box drawing. Unicode box characters (e.g., `U+250C`) render inconsistently across terminals, fonts, and SSH sessions. ASCII ensures every terminal on every OS renders identically.

### Severity Icons

```
[DONE]      -- Validator passed
[NOT_DONE]  -- Validator failed (blocks advancement)
[CRITICAL]  -- Finding: design-breaking issue
[MAJOR]     -- Finding: significant issue requiring fix
[MINOR]     -- Finding: improvement recommended
[WARNING]   -- Finding: informational, does not block
[ERROR]     -- System error or hard failure
[INFO]      -- Informational message
```

### Status Markers

```
PASS        -- Gate passed, pipeline advances
NOT_DONE    -- Gate failed, pipeline paused
PAUSED      -- Pipeline awaiting human input
REWORK      -- Pipeline returned to earlier stage
COMPLETE    -- Pipeline finished successfully
ABORTED     -- Pipeline terminated by user
```

### Width

All output blocks target **60 characters** wide (fits 80-column terminals with margin). Content wraps at 56 characters (60 minus borders and padding).

### LOTR Theme Token Mapping

When LOTR alias theme is active, the following substitutions apply:

| Neutral Token | LOTR Token |
|--------------|-----------|
| `HARDWARE PIPELINE` | `THE FELLOWSHIP OF THE BOARD` |
| `STAGE N:` | `CHAPTER N:` |
| `GATE:` | `THE COUNCIL OF` |
| `PASS` | `THE PATH IS CLEAR` |
| `NOT_DONE` | `THE WAY IS SHUT` |
| `REWORK TRIGGERED` | `A SHADOW RETURNS` |
| `PIPELINE PAUSED` | `THE FELLOWSHIP RESTS` |
| `PIPELINE COMPLETE` | `THE QUEST IS FULFILLED` |
| `HUMAN ACTION REQUIRED` | `A TASK FOR MORTAL HANDS` |
| `Advancing to` | `The fellowship journeys to` |
| `Returning to` | `The fellowship retreats to` |
| `DESIGN REVIEW BOARD` | `THE WHITE COUNCIL` |
| `REWORK LIMIT REACHED` | `THE DOOM OF THE NOLDOR` |
| `RESUMING PIPELINE` | `THE QUEST RESUMES` |

---

## Wireframe 1: Setup Wizard Output

**Source flow**: Flow 1 (First-Time Setup)
**Covers**: FR-001, FR-004, FR-017, Story 1.1, Story 1.4, Story 1.8, Story 3.6, Story 5.3

### 1A: SessionStart -- No Config Found

**Neutral theme:**

```
+------------------------------------------------------------+
| hardware-team: No .hardware/config.yml found.              |
| Run `hw-setup` to create one.                              |
|                                                            |
| kicad-happy: 11/11 skills available                        |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| The land is unshaped. No .hardware/config.yml yet forged.  |
| Speak `hw-setup` to begin the crafting.                    |
|                                                            |
| Allies of the fellowship: 11/11 kicad-happy skills stand   |
| ready.                                                     |
+------------------------------------------------------------+
```

### 1B: Setup Wizard -- Question Presentation

Each question follows this exact format. One question at a time, sequentially.

**Neutral theme:**

```
+------------------------------------------------------------+
| SETUP: Question 1 of 9                                     |
+------------------------------------------------------------+
| What is your project name?                                 |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

```
+------------------------------------------------------------+
| SETUP: Question 2 of 9                                     |
+------------------------------------------------------------+
| Target fabrication house?                                  |
|                                                            |
| Options:                                                   |
|   [1] jlcpcb                                               |
|   [2] pcbway                                               |
|   [3] other                                                |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

```
+------------------------------------------------------------+
| SETUP: Question 3 of 9                                     |
+------------------------------------------------------------+
| Target compliance regions? (comma-separated)               |
|                                                            |
| Examples: FCC, CE, UL, none                                |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

```
+------------------------------------------------------------+
| SETUP: Question 4 of 9                                     |
+------------------------------------------------------------+
| BOM budget target (USD per unit)?                          |
|                                                            |
| Default: no limit                                          |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

```
+------------------------------------------------------------+
| SETUP: Question 5 of 9                                     |
+------------------------------------------------------------+
| Production volume target?                                  |
|                                                            |
| Options:                                                   |
|   [1] prototype (<10)                                      |
|   [2] small-batch (10-1000)                                |
|   [3] production (1000+)                                   |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

```
+------------------------------------------------------------+
| SETUP: Question 6 of 9                                     |
+------------------------------------------------------------+
| Board layer count?                                         |
|                                                            |
| Options:                                                   |
|   [1] 1    [2] 2    [3] 4    [4] 6    [5] 8+              |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

```
+------------------------------------------------------------+
| SETUP: Question 7 of 9                                     |
+------------------------------------------------------------+
| Minimum kicad-happy version?                               |
|                                                            |
| Default: >=1.2.0                                           |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

```
+------------------------------------------------------------+
| SETUP: Question 8 of 9                                     |
+------------------------------------------------------------+
| Rework iteration limit per path?                           |
|                                                            |
| Default: 3                                                 |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

```
+------------------------------------------------------------+
| SETUP: Question 9 of 9                                     |
+------------------------------------------------------------+
| Total rework limit per pipeline run?                       |
|                                                            |
| Default: 10                                                |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

**LOTR theme (example -- Question 2):**

```
+------------------------------------------------------------+
| THE CRAFTING: Inscription 2 of 9                           |
+------------------------------------------------------------+
| To which forge shall the boards be sent?                   |
|                                                            |
| The forges of Middle-earth:                                |
|   [1] jlcpcb    -- The Mines of Fabrication                |
|   [2] pcbway    -- The Forges of the East                  |
|   [3] other     -- A forge unknown to us                   |
|                                                            |
| > _                                                        |
+------------------------------------------------------------+
```

### 1C: Config Confirmation

**Neutral theme:**

```
+------------------------------------------------------------+
| Created .hardware/config.yml (schema v1.0)                 |
|                                                            |
|   project: sensor-board-v2                                 |
|   target_fab: jlcpcb                                       |
|   compliance_regions: [FCC, CE]                            |
|   bom_budget: 12.50                                        |
|   volume: small-batch                                      |
|   layers: 4                                                |
|   dependencies:                                            |
|     kicad_happy_version: ">=1.2.0"                         |
|   rework:                                                  |
|     max_rework_iterations: 3                               |
|     max_total_reworks: 10                                  |
|                                                            |
| Edit .hardware/config.yml to adjust settings.              |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| The config is forged. .hardware/config.yml (schema v1.0)   |
|                                                            |
|   quest: sensor-board-v2                                   |
|   forge: jlcpcb                                            |
|   realms_of_law: [FCC, CE]                                 |
|   treasury_per_unit: 12.50 gold pieces                     |
|   host_count: small-batch                                  |
|   layers_of_the_board: 4                                   |
|   allies:                                                  |
|     kicad_happy_version: ">=1.2.0"                         |
|   trials:                                                  |
|     max_rework_iterations: 3                               |
|     max_total_reworks: 10                                  |
|                                                            |
| The inscriptions may be altered by hand, should you wish.  |
+------------------------------------------------------------+
```

### 1D: Setup Complete

**Neutral theme:**

```
+------------------------------------------------------------+
| Config valid. Ready to run pipeline.                       |
+------------------------------------------------------------+

+------------------------------------------------------------+
| Setup complete. To start the hardware pipeline:            |
|                                                            |
|   "Run the hardware pipeline"                              |
|   or invoke: hardware-team:hardware-flow                   |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| The ring of configuration is complete. Its power is ready. |
+------------------------------------------------------------+

+------------------------------------------------------------+
| The fellowship is assembled. To begin the quest:           |
|                                                            |
|   "Begin the quest of the board"                           |
|   or invoke: hardware-team:hardware-flow                   |
+------------------------------------------------------------+
```

### 1E: Config Already Exists

**Neutral theme:**

```
Config already exists (schema v1.0). Overwrite? [y/N] _
```

**LOTR theme:**

```
A config already lies in the deep places. Reforge it? [y/N] _
```

---

## Wireframe 2: Stage Announcement Format

**Source flow**: Flow 2 (Pipeline Execution), Flow 3 (Stage Interaction)
**Covers**: FR-002, FR-003, FR-008, FR-020

### 2A: Pre-Flight Summary

**Neutral theme:**

```
+------------------------------------------------------------+
| HARDWARE PIPELINE: sensor-board-v2                         |
| Config: .hardware/config.yml (v1.0)                        |
| Fab: jlcpcb | Regions: FCC, CE | Budget: $12.50           |
| kicad-happy: 11/11 skills available                        |
| Memory: 3 lessons loaded                                   |
|                                                            |
| Stages: Concept > Schematic > Layout > Prototype >         |
|         DFM/DFA > Compliance > Pilot Run >                 |
|         Production Release                                 |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| THE FELLOWSHIP OF THE BOARD: sensor-board-v2               |
| Scroll: .hardware/config.yml (v1.0)                        |
| Forge: jlcpcb | Realms: FCC, CE | Treasury: $12.50        |
| Allies: 11/11 kicad-happy skills stand ready               |
| Lore: 3 lessons recalled from the archive                  |
|                                                            |
| The road goes ever on:                                     |
|   Shire > Rivendell > Moria > Rohan >                      |
|   Helm's Deep > Gondor > Pelennor >                        |
|   Mount Doom                                               |
| (Concept > Schematic > Layout > Prototype >                |
|  DFM/DFA > Compliance > Pilot Run >                        |
|  Production Release)                                       |
+------------------------------------------------------------+
```

### 2B: AI-Execution Stage Banner

**Neutral theme:**

```
============================================================
  STAGE 2: SCHEMATIC [AI-execution]
  Roles: Electrical Engineer (primary), HW PO (trade-offs)
  Activities: schematic review, component selection,
              SPICE simulation, firmware interface docs
  kicad-happy: kicad, spice, digikey, mouser, lcsc, element14
============================================================
```

**LOTR theme:**

```
============================================================
  CHAPTER 2: THE COUNCIL OF RIVENDELL [AI-execution]
  (Schematic)
  Companions: Electrical Engineer (primary),
              HW Product Owner (counsel)
  Deeds: schematic review, component selection,
         SPICE simulation, firmware interface docs
  Allies summoned: kicad, spice, digikey, mouser, lcsc,
                   element14
============================================================
```

### 2C: Human-Execution Stage Banner

**Neutral theme:**

```
============================================================
  STAGE 4: PROTOTYPE [Human-execution]
  Mode: gate-in / human-action / gate-out
  Roles: Test Engineer (primary), EE (support)
============================================================
```

**LOTR theme:**

```
============================================================
  CHAPTER 4: THE RIDERS OF ROHAN [Human-execution]
  (Prototype)
  Mode: counsel-given / mortal-deed / counsel-reviewed
  Companions: Test Engineer (primary), EE (support)
============================================================
```

### 2D: Stage Transition (Gate Pass)

**Neutral theme:**

```
+------------------------------------------------------------+
| GATE: Concept --> Schematic                                |
| [DONE] Requirements completeness                          |
| [DONE] Feasibility assessment                             |
| Result: PASS -- advancing to Schematic                     |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| THE COUNCIL OF: Concept --> Schematic                      |
| [DONE] Requirements completeness                          |
| [DONE] Feasibility assessment                             |
| The path is clear -- the fellowship journeys to Schematic  |
+------------------------------------------------------------+
```

---

## Wireframe 3: Agent Dispatch Indicators

**Source flow**: Flow 3A (AI-Execution Stage Pattern)
**Covers**: FR-008, FR-020, NFR-002

### 3A: Sub-Agent Dispatch (Start)

When the orchestrator dispatches a sub-agent via the Agent tool, the user sees a brief indicator before the agent runs.

**Neutral theme:**

```
  [>] Dispatching: Electrical Engineer
      Context: Schematic stage, rework=false
      Skills: kicad, spice, digikey, mouser, lcsc, element14
```

**LOTR theme:**

```
  [>] Summoning: Electrical Engineer
      Quest: Schematic chapter, no shadow upon it
      Allies: kicad, spice, digikey, mouser, lcsc, element14
```

### 3B: Multi-Agent Dispatch (Design Review Board)

When the Design Review Board dispatches multiple independent reviewers:

**Neutral theme:**

```
  [>] Dispatching: DESIGN REVIEW BOARD (Post-Schematic)
      Reviewers:
        [>] Electrical Engineer -- schematic correctness
        [>] PCB Layout Engineer -- layout feasibility
        [>] Manufacturing Engineer -- manufacturability
        [>] Compliance Engineer -- regulatory impact
      Mode: independent review (no shared context)
```

**LOTR theme:**

```
  [>] Convening: THE WHITE COUNCIL (Post-Schematic)
      Council members:
        [>] Electrical Engineer -- the light of circuits
        [>] PCB Layout Engineer -- the paths of copper
        [>] Manufacturing Engineer -- the craft of making
        [>] Compliance Engineer -- the law of realms
      Mode: each sees through their own palantir
```

### 3C: Sub-Agent Completion

**Neutral theme:**

```
  [+] Complete: Electrical Engineer (artifacts: 4)
```

**LOTR theme:**

```
  [+] Returned: Electrical Engineer (scrolls: 4)
```

---

## Wireframe 4: Checkpoint Presentation

**Source flow**: Flow 3A (artifacts), Flow 3B (human-action checkpoints)
**Covers**: FR-002, FR-003, FR-008

### 4A: Artifact Summary (AI-Execution Stage)

Shown after a sub-agent completes its work.

**Neutral theme:**

```
+------------------------------------------------------------+
| ARTIFACTS: Stage 2 - Schematic                             |
|                                                            |
| 1. schematic-review.md -- EE schematic review findings     |
| 2. component-rationale.md -- selection rationale per part  |
| 3. spice-results.md -- simulation results for U3, U7      |
| 4. firmware-interface.md -- pin table, power domains,      |
|    bus specs, debug interfaces                             |
|                                                            |
| Saved to: .hardware/artifacts/02-schematic/                |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| SCROLLS OF: Chapter 2 - The Council of Rivendell           |
|                                                            |
| 1. schematic-review.md -- the mirror reveals all flaws     |
| 2. component-rationale.md -- why each ally was chosen      |
| 3. spice-results.md -- the fires of simulation tested U3,  |
|    U7                                                      |
| 4. firmware-interface.md -- the map of pins, the domains   |
|    of power, the roads of data                             |
|                                                            |
| Stored in: .hardware/artifacts/02-schematic/               |
+------------------------------------------------------------+
```

### 4B: Human-Action Checkpoint

Shown when the pipeline pauses for physical action.

**Neutral theme:**

```
+------------------------------------------------------------+
| === HUMAN ACTION REQUIRED ===                              |
|                                                            |
| Preparation artifacts:                                     |
|  1. ordering-package.md -- Gerber + BOM/CPL for JLCPCB    |
|  2. bring-up-procedure.md -- 14-step test procedure        |
|  3. test-fixture-reqs.md -- fixture requirements           |
|                                                            |
| Action items:                                              |
|  [ ] 1. Order prototype boards from JLCPCB                 |
|  [ ] 2. Assemble and bring up prototype                    |
|  [ ] 3. Execute bring-up test procedure                    |
|  [ ] 4. Record test results                                |
|                                                            |
| When complete, confirm: "prototype complete"               |
| To report issues: "prototype failed: [description]"        |
| To pause and resume later: "save pipeline state"           |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| === A TASK FOR MORTAL HANDS ===                            |
|                                                            |
| Scrolls prepared for your journey:                         |
|  1. ordering-package.md -- the order for the forge         |
|  2. bring-up-procedure.md -- 14 steps to awaken the board |
|  3. test-fixture-reqs.md -- the tools you shall need       |
|                                                            |
| Your deeds:                                                |
|  [ ] 1. Send the order to the forges of JLCPCB            |
|  [ ] 2. Assemble the prototype with your own hands         |
|  [ ] 3. Walk the 14 steps of the bring-up ritual           |
|  [ ] 4. Record what the board reveals                      |
|                                                            |
| When the deed is done: "prototype complete"                |
| If shadow falls: "prototype failed: [description]"         |
| To rest and return: "save pipeline state"                  |
+------------------------------------------------------------+
```

---

## Wireframe 5: DoD Validation Results

**Source flow**: Flow 2 (gates), Flow 3C (self-correction)
**Covers**: FR-003, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015

### 5A: Simple Gate -- All Pass

**Neutral theme:**

```
+------------------------------------------------------------+
| GATE: Concept --> Schematic                                |
| [DONE] Requirements completeness                          |
| [DONE] Feasibility assessment                             |
| Result: PASS -- advancing to Schematic                     |
+------------------------------------------------------------+
```

### 5B: Simple Gate -- Failure with Findings

**Neutral theme:**

```
+------------------------------------------------------------+
| GATE: Schematic --> Layout                                 |
| [DONE] Component lifecycle check                          |
| [NOT_DONE] Schematic review                               |
|   [CRITICAL] F-001: Missing bulk cap on U3 VDD            |
|     Location: Sheet 2, U3 pin 14                          |
|     Fix: Add 10uF ceramic cap, place within 3mm           |
|   [MAJOR] F-002: Unterminated SPI_CLK trace               |
|     Location: Sheet 1, Net SPI_CLK                        |
|     Fix: Add series termination resistor (33R)            |
|   [MINOR] F-003: LED current resistor oversized           |
|     Location: Sheet 1, R12                                |
|     Fix: Change R12 from 1K to 470R for 10mA target       |
| Result: NOT_DONE -- 1 critical finding                     |
| Pipeline paused. Correct findings and re-run gate.         |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| THE COUNCIL OF: Schematic --> Layout                       |
| [DONE] Component lifecycle check                          |
| [NOT_DONE] Schematic review                               |
|   [CRITICAL] F-001: A darkness upon U3 -- no bulk cap     |
|     Where: Sheet 2, U3 pin 14                             |
|     Remedy: Place a 10uF ceramic ward within 3mm          |
|   [MAJOR] F-002: SPI_CLK wanders unterminated             |
|     Where: Sheet 1, Net SPI_CLK                           |
|     Remedy: A 33R resistor to end its wandering            |
|   [MINOR] F-003: The LED burns too dim                    |
|     Where: Sheet 1, R12                                   |
|     Remedy: Change R12 from 1K to 470R                    |
| The way is shut -- 1 critical shadow found                 |
| The fellowship rests. Correct the darkness and return.     |
+------------------------------------------------------------+
```

### 5C: DRC Gate (Layout Stage)

**Neutral theme:**

```
+------------------------------------------------------------+
| DRC GATE                                                   |
|                                                            |
| [ERROR] V-001: Trace width 0.10mm < JLCPCB min 0.127mm   |
|   Layer: F.Cu @ (42.3, 18.7)                              |
|   Fix: Increase trace width to >= 0.127mm                  |
| [WARNING] V-002: Via annular ring 0.15mm                   |
|   (JLCPCB recommends >= 0.153mm)                          |
|                                                            |
| Errors: 1 | Warnings: 1                                   |
| Result: NOT_DONE -- errors must be resolved                |
+------------------------------------------------------------+
```

### 5D: BOM Gate

**Neutral theme:**

```
+------------------------------------------------------------+
| BOM GATE                                                   |
|                                                            |
| [DONE] Total BOM: $11.23 (within $12.50 budget)           |
| [DONE] All components active lifecycle                     |
| [WARNING] C12 (LM1117-3.3): single-source (TI only)      |
|                                                            |
| Result: PASS                                               |
+------------------------------------------------------------+
```

### 5E: Compliance Gate (Multi-Region)

**Neutral theme:**

```
+------------------------------------------------------------+
| COMPLIANCE GATE                                            |
|                                                            |
| FCC Part 15:                                               |
|  [DONE] Radiated emissions (EMC report linked)            |
|  [DONE] Conducted emissions (EMC report linked)           |
|  [DONE] Labeling requirements                             |
| CE RED:                                                    |
|  [DONE] EN 55032 (EMC report linked)                      |
|  [NOT_DONE] EN 62368-1 safety (no evidence)               |
|                                                            |
| Result: NOT_DONE -- missing safety evidence                |
+------------------------------------------------------------+
```

### 5F: Design Review Board Results

**Neutral theme:**

```
+------------------------------------------------------------+
| DESIGN REVIEW BOARD: Post-Schematic                        |
|                                                            |
| EE Review:                                                 |
|  [CRITICAL] Missing level shifter on U2-SDA               |
|  [MAJOR] Capacitor C7 derated below 50%                   |
|                                                            |
| MfgE Review:                                              |
|  [MAJOR] QFN-48 not in JLCPCB basic parts                 |
|  [MINOR] Footprint 0201 below JLCPCB recommended          |
|                                                            |
| CompE Review:                                             |
|  [WARNING] No filtering on USB data lines (EMC)           |
|                                                            |
| PCB Layout Review:                                        |
|  [MAJOR] BGA pitch requires 6-layer (4 configured)        |
|                                                            |
| Deduplicated: 2 findings merged across reviewers          |
| Summary: 1 critical, 3 major, 1 minor, 1 warning          |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| THE WHITE COUNCIL: Post-Schematic                          |
|                                                            |
| The Electrical Engineer speaks:                            |
|  [CRITICAL] A shadow on U2-SDA -- no level shifter        |
|  [MAJOR] Capacitor C7 weakened beyond half its strength    |
|                                                            |
| The Manufacturing Engineer speaks:                         |
|  [MAJOR] QFN-48 is not among the basic stores of JLCPCB   |
|  [MINOR] 0201 is smaller than the forge recommends         |
|                                                            |
| The Compliance Engineer speaks:                            |
|  [WARNING] USB data lines unshielded against the storms    |
|                                                            |
| The PCB Layout Engineer speaks:                            |
|  [MAJOR] BGA demands 6 layers; only 4 were forged         |
|                                                            |
| Voices echoed: 2 findings spoken by more than one          |
| The council tallies: 1 critical, 3 major, 1 minor,        |
|                      1 warning                             |
+------------------------------------------------------------+
```

### 5G: Schematic Review Gate (Multi-Reviewer, Iterative)

**Neutral theme:**

```
+------------------------------------------------------------+
| SCHEMATIC REVIEW GATE                                      |
|                                                            |
| Reviewers: EE-1, EE-2 (2 passes, deduplicated)            |
|                                                            |
| Findings (7 unique, 3 duplicates removed):                 |
|  [CRITICAL] F-001: Missing bulk cap on U3 VDD             |
|    Location: Sheet 2, U3 pin 14                           |
|    Category: decoupling                                    |
|    Fix: Add 10uF ceramic cap, place within 3mm            |
|  [MAJOR] F-002: Unterminated SPI_CLK trace                |
|    Location: Sheet 1, Net SPI_CLK                         |
|    Category: signal integrity                              |
|    Fix: Add series termination resistor (33R)             |
|  [MAJOR] F-003: No pull-up on I2C_SDA                    |
|    Location: Sheet 1, Net I2C_SDA                         |
|    Category: pull-ups/pull-downs                           |
|    Fix: Add 4.7K pull-up to 3.3V                          |
|  [MINOR] F-004: ...                                       |
|  [MINOR] F-005: ...                                       |
|  [WARNING] F-006: ...                                     |
|  [WARNING] F-007: ...                                     |
|                                                            |
| Result: NOT_DONE -- 1 critical finding                     |
| Pipeline paused. Correct findings and re-run gate.         |
+------------------------------------------------------------+
```

### 5H: DFM Gate + BOM Gate (Combined)

**Neutral theme:**

```
+------------------------------------------------------------+
| DFM GATE                                                   |
| [DONE] All DFM rules pass for JLCPCB                      |
|                                                            |
| BOM GATE                                                   |
| [WARNING] C12 (LM1117-3.3): single-source (TI only)      |
| [DONE] Total BOM: $11.23 (within $12.50 budget)           |
| [DONE] All components active lifecycle                     |
|                                                            |
| Result: PASS -- advancing to Compliance                    |
+------------------------------------------------------------+
```

### 5I: Final Gate (Pipeline Complete)

**Neutral theme:**

```
+------------------------------------------------------------+
| PIPELINE COMPLETE: sensor-board-v2                         |
|                                                            |
| Stages: 8/8 complete                                       |
| Gates: 7/7 passed                                          |
| Reworks: 2 (Schematic x1, Layout x1)                      |
| Artifacts: 24 files in .hardware/artifacts/                |
|                                                            |
| Lessons captured to .hardware/memory/                      |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| THE QUEST IS FULFILLED: sensor-board-v2                    |
|                                                            |
| Chapters: 8/8 complete                                     |
| Councils passed: 7/7                                       |
| Shadows overcome: 2 (Schematic x1, Layout x1)             |
| Scrolls: 24 files in .hardware/artifacts/                  |
|                                                            |
| Lore captured to .hardware/memory/                         |
| The age of this board begins.                              |
+------------------------------------------------------------+
```

---

## Wireframe 6: Rework Notification

**Source flow**: Flow 4 (Rework)
**Covers**: FR-007, NFR-010, Story 1.7

### 6A: Rework Triggered

**Neutral theme:**

```
+------------------------------------------------------------+
| REWORK TRIGGERED                                           |
|                                                            |
| Source: DFM/DFA (Stage 5)                                  |
| Target: Schematic (Stage 2)                                |
| Reason: Component U5 (QFN-48) not available at JLCPCB.    |
|   Requires component substitution.                         |
|                                                            |
| Rework path: DFM/DFA --> Schematic                         |
| Iteration: 1 of 3 (per-path limit)                        |
| Total reworks this run: 2 of 10                            |
|                                                            |
| Returning to Schematic stage with rework context...        |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| A SHADOW RETURNS                                           |
|                                                            |
| From: DFM/DFA (Chapter 5)                                 |
| To: Schematic (Chapter 2)                                  |
| The darkness: Component U5 (QFN-48) cannot be found in     |
|   the stores of JLCPCB. A new ally must be chosen.         |
|                                                            |
| Shadow path: DFM/DFA --> Schematic                         |
| Trial: 1 of 3 (per-path doom)                             |
| Shadows faced this quest: 2 of 10                          |
|                                                            |
| The fellowship retreats to Schematic, bearing knowledge    |
| of what went wrong...                                      |
+------------------------------------------------------------+
```

### 6B: Downstream Re-Validation After Rework

**Neutral theme:**

```
+------------------------------------------------------------+
| DOWNSTREAM RE-VALIDATION                                   |
|                                                            |
| Schematic Gate: [DONE] (re-validated)                      |
| Layout Gate: [DONE] (re-validated)                         |
| DFM Gate: [DONE] (re-validated)                            |
|                                                            |
| Rework resolved. Pipeline advancing from DFM/DFA.          |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| THE PATH IS CLEAR ONCE MORE                                |
|                                                            |
| Council of Schematic: [DONE] (re-judged)                   |
| Council of Layout: [DONE] (re-judged)                      |
| Council of DFM: [DONE] (re-judged)                         |
|                                                            |
| The shadow is lifted. The fellowship advances from DFM/DFA.|
+------------------------------------------------------------+
```

---

## Wireframe 7: Escalation Format

**Source flow**: Flow 4 (Rework Termination)
**Covers**: FR-007, NFR-010

### 7A: Per-Path Rework Limit Reached

**Neutral theme:**

```
+------------------------------------------------------------+
| REWORK LIMIT REACHED                                       |
|                                                            |
| Limit type: Per-path                                       |
| Path: DFM/DFA --> Schematic                                |
| Iterations: 3/3 (limit reached)                            |
|                                                            |
| Rework history for this path:                              |
|  #1: Component U5 unavailable --> substituted U5B          |
|  #2: U5B footprint incompatible --> substituted U5C        |
|  #3: U5C voltage range insufficient --> ?                  |
|                                                            |
| Recurring pattern: Component selection for U5 position     |
| is failing repeatedly.                                     |
|                                                            |
| RECOMMENDATION: Manual intervention needed. Consider       |
| redesigning the power regulation approach rather than      |
| iterating on component substitution.                       |
|                                                            |
| === PIPELINE PAUSED ===                                    |
| Options:                                                   |
|  "continue" -- override limit, try once more               |
|  "abort" -- stop the pipeline run                          |
|  "override limit N" -- set new per-path limit              |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| THE DOOM OF THE NOLDOR                                     |
|                                                            |
| Doom: Per-path                                             |
| Path: DFM/DFA --> Schematic                                |
| Trials endured: 3/3 (the limit of endurance)               |
|                                                            |
| Chronicle of this path:                                    |
|  #1: U5 fell -- U5B took its place                         |
|  #2: U5B's form did not fit -- U5C was summoned            |
|  #3: U5C's power was insufficient -- none remain           |
|                                                            |
| The pattern repeats: the U5 seat cannot be filled          |
| by simple substitution.                                    |
|                                                            |
| COUNSEL: The approach must change. Redesign the power      |
| regulation rather than seeking yet another component.      |
|                                                            |
| === THE FELLOWSHIP RESTS ===                               |
| Speak your will:                                           |
|  "continue" -- one more trial                              |
|  "abort" -- end the quest                                  |
|  "override limit N" -- extend the doom                     |
+------------------------------------------------------------+
```

### 7B: Total Rework Limit Reached

**Neutral theme:**

```
+------------------------------------------------------------+
| TOTAL REWORK LIMIT REACHED                                 |
|                                                            |
| Limit type: Total (across all paths)                       |
| Total reworks: 10/10 (limit reached)                       |
|                                                            |
| Rework summary:                                            |
|  DFM-->Schematic: 3 iterations                             |
|  DFM-->Layout: 2 iterations                                |
|  Prototype-->Layout: 3 iterations                          |
|  Compliance-->Schematic: 2 iterations                      |
|                                                            |
| RECOMMENDATION: This design is experiencing systemic       |
| iteration. Reassess the overall design approach before     |
| continuing.                                                |
|                                                            |
| === PIPELINE PAUSED ===                                    |
| Options:                                                   |
|  "continue" -- override, allow more reworks                |
|  "abort" -- stop the pipeline run                          |
|  "override total N" -- set new total limit                 |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| THE DOOM OF THE NOLDOR (Total)                             |
|                                                            |
| Doom: Total (across all paths of shadow)                   |
| Shadows faced: 10/10 (the final count)                     |
|                                                            |
| Chronicle of all shadows:                                  |
|  DFM-->Schematic: 3 trials                                 |
|  DFM-->Layout: 2 trials                                    |
|  Prototype-->Layout: 3 trials                              |
|  Compliance-->Schematic: 2 trials                          |
|                                                            |
| COUNSEL: The board is cursed by systemic failure.          |
| The design itself must be reconsidered -- not merely       |
| its parts.                                                 |
|                                                            |
| === THE FELLOWSHIP RESTS ===                               |
| Speak your will:                                           |
|  "continue" -- defy the doom                               |
|  "abort" -- abandon the quest                              |
|  "override total N" -- extend the doom's reach             |
+------------------------------------------------------------+
```

---

## Wireframe 8: Pipeline Status Command Output

**Source flow**: Flow 2 (Pipeline Execution), Flow 7 (Resume)
**Covers**: FR-002, FR-005

### 8A: Pipeline In Progress

**Neutral theme:**

```
+------------------------------------------------------------+
| PIPELINE STATUS: sensor-board-v2                           |
|                                                            |
| Stage 1: Concept              [DONE]                       |
| Stage 2: Schematic            [DONE] (rework x1)          |
| Stage 3: Layout               [DONE]                       |
| Stage 4: Prototype            [PAUSED] -- human action     |
| Stage 5: DFM/DFA              [ ]                          |
| Stage 6: Compliance           [ ]                          |
| Stage 7: Pilot Run            [ ]                          |
| Stage 8: Production Release   [ ]                          |
|                                                            |
| Current: Stage 4 (Prototype) -- awaiting confirmation      |
| Reworks: 1 total (1 of 10 limit)                           |
| State: .hardware/state.md (last saved: 2026-04-12 14:32)  |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| QUEST STATUS: sensor-board-v2                              |
|                                                            |
| Ch 1: Concept (The Shire)     [DONE]                       |
| Ch 2: Schematic (Rivendell)   [DONE] (shadow x1)          |
| Ch 3: Layout (Moria)          [DONE]                       |
| Ch 4: Prototype (Rohan)       [PAUSED] -- mortal deed      |
| Ch 5: DFM/DFA (Helm's Deep)   [ ]                          |
| Ch 6: Compliance (Gondor)     [ ]                          |
| Ch 7: Pilot Run (Pelennor)    [ ]                          |
| Ch 8: Prod Release (Mt Doom)  [ ]                          |
|                                                            |
| The fellowship rests at: Chapter 4 (Rohan)                 |
| Shadows faced: 1 of 10                                     |
| Scroll: .hardware/state.md (inscribed: 2026-04-12 14:32)  |
+------------------------------------------------------------+
```

### 8B: Resume Notification (SessionStart)

**Neutral theme:**

```
+------------------------------------------------------------+
| hardware-team: Persisted pipeline state found.             |
|                                                            |
| Pipeline: sensor-board-v2                                  |
| Last stage completed: Layout (Stage 3)                     |
| Current stage: Prototype (Stage 4) -- PAUSED               |
| Human action pending: Order and test prototype             |
| Rework history: 1 (Schematic rework from Layout)          |
|                                                            |
| To resume: "Resume hardware pipeline"                      |
| To start fresh: "New hardware pipeline"                    |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| A quest unfinished awaits in .hardware/state.md.           |
|                                                            |
| Quest: sensor-board-v2                                     |
| Last chapter completed: Layout (Chapter 3)                 |
| The fellowship rests at: Prototype (Chapter 4)             |
| A mortal deed awaits: Order and test prototype             |
| Shadows overcome: 1 (Schematic rework from Layout)        |
|                                                            |
| To continue the quest: "Resume hardware pipeline"          |
| To begin anew: "New hardware pipeline"                     |
+------------------------------------------------------------+
```

### 8C: Resuming Pipeline

**Neutral theme:**

```
+------------------------------------------------------------+
| RESUMING PIPELINE: sensor-board-v2                         |
|                                                            |
| Completed: Concept, Schematic, Layout                      |
| Resuming at: Prototype (Stage 4)                           |
|                                                            |
| === HUMAN ACTION REQUIRED ===                              |
| (Same checkpoint as when paused)                           |
+------------------------------------------------------------+
```

### 8D: Stale State Warning

**Neutral theme:**

```
+------------------------------------------------------------+
| WARNING: Source files modified since last pipeline run.     |
| Schematic (.kicad_sch) changed.                            |
|                                                            |
| Completed gates may need re-validation.                    |
| Options:                                                   |
|  "resume" -- continue from last stage (skip recheck)       |
|  "revalidate" -- re-run gates from modified stage          |
|  "restart" -- start pipeline from beginning                |
+------------------------------------------------------------+
```

---

## Wireframe 9: Error and Warning Formats

**Source flow**: Flow 1 (error paths), Flow 5 (graceful failure), Flow 8 (hooks)
**Covers**: FR-004, FR-009, FR-017, FR-018, FR-019, NFR-006

### 9A: kicad-happy Not Installed

**Neutral theme:**

```
+------------------------------------------------------------+
| WARNING: Required dependency kicad-happy is not installed. |
| Install it via the Claude Code plugin system.              |
|                                                            |
| The hardware-team plugin requires kicad-happy for          |
| component sourcing, fabrication validation, KiCad          |
| analysis, and documentation generation.                    |
|                                                            |
| kicad-happy: 0/11 skills available                         |
| Missing: kicad, spice, digikey, mouser, lcsc, element14,  |
|          jlcpcb, pcbway, bom, emc, kidoc                   |
+------------------------------------------------------------+
```

**LOTR theme:**

```
+------------------------------------------------------------+
| WARNING: The allies of kicad-happy have not been           |
| summoned to this realm. Install via the plugin system.     |
|                                                            |
| Without them, the fellowship cannot source components,     |
| validate fabrication, analyze schematics, or produce       |
| the scrolls of documentation.                              |
|                                                            |
| Allies present: 0/11                                       |
| Missing: kicad, spice, digikey, mouser, lcsc, element14,  |
|          jlcpcb, pcbway, bom, emc, kidoc                   |
+------------------------------------------------------------+
```

### 9B: kicad-happy Partially Installed

**Neutral theme:**

```
+------------------------------------------------------------+
| kicad-happy: 8/11 skills available                         |
| Missing: spice, emc, kidoc                                 |
| Install kicad-happy via Claude Code plugin system.         |
+------------------------------------------------------------+
```

### 9C: kicad-happy Version Mismatch

**Neutral theme:**

```
+------------------------------------------------------------+
| kicad-happy version 1.1.0 installed; hardware-team         |
| requires >=1.2.0. Some features may not work.              |
+------------------------------------------------------------+
```

### 9D: Invalid Config Fields

**Neutral theme:**

```
+------------------------------------------------------------+
| WARNING: .hardware/config.yml has invalid fields:          |
|   - bom_budget: "abc" (expected number)                    |
|   - target_fab: "invalid" (expected: jlcpcb, pcbway)      |
| Using defaults for invalid fields.                         |
+------------------------------------------------------------+
```

### 9E: Outdated Config Schema

**Neutral theme:**

```
+------------------------------------------------------------+
| WARNING: .hardware/config.yml uses schema v0.9.            |
| Current schema is v1.0.                                    |
| Migration: Add 'dependencies.kicad_happy_version' and      |
| 'rework' section. See config-schema.md.                    |
| Pipeline will use defaults for missing fields.             |
+------------------------------------------------------------+
```

### 9F: Config Schema Upgrade Notification (Forward Compatibility)

**Neutral theme:**

```
+------------------------------------------------------------+
| Config schema v1.0 detected; current is v1.1.              |
| New fields in v1.1: gate_strictness, model_tiers           |
| Using defaults for missing fields. Pipeline OK.            |
| Run hw-setup to update config.                             |
+------------------------------------------------------------+
```

### 9G: kicad-happy Skill Unavailable During Stage

**Neutral theme:**

```
+------------------------------------------------------------+
| WARNING: kicad-happy:spice not available                   |
|                                                            |
| Cannot perform SPICE simulation. The Electrical Engineer   |
| role requires this skill for circuit validation.           |
|                                                            |
| Install kicad-happy via the Claude Code plugin system      |
| to enable simulation capabilities.                         |
|                                                            |
| Pipeline continuing without simulation data.               |
| Schematic Review Gate may flag unvalidated circuits.       |
+------------------------------------------------------------+
```

### 9H: PostToolUse Hook -- DRC Warning

**Neutral theme:**

```
+------------------------------------------------------------+
| DRC WARNING (auto-check on schematic edit):                |
|  [W] Net SPI_CLK: no decoupling on U3 pin 7               |
|  [W] Missing pull-up on I2C_SDA                           |
+------------------------------------------------------------+
```

### 9I: PostToolUse Hook -- BOM Drift Warning

**Neutral theme:**

```
+------------------------------------------------------------+
| BOM DRIFT WARNING:                                         |
|  + Added: U8 (new component, not in BOM)                   |
|  - Removed: U5 (in BOM but no longer in schematic)        |
|  ~ Changed: C12 value (100nF --> 220nF)                   |
|                                                            |
| BOM needs updating. Re-run BOM Gate to reconcile.          |
+------------------------------------------------------------+
```

---

## Wireframe 10: Progress Indicators

**Source flow**: Flow 2 (long-running stages), Flow 3 (sub-agent execution)
**Covers**: FR-002, FR-020

### 10A: Stage Progress (Within a Stage)

Since this is a CLI conversation, progress is communicated inline as the sub-agent works. There are no spinners or progress bars -- instead, the sub-agent narrates its work.

**Neutral theme:**

```
  [>] Dispatching: Electrical Engineer
      Context: Schematic stage, rework=false

  ... Electrical Engineer working ...

  [~] Component selection: querying DigiKey for U3...
  [~] Component selection: querying Mouser for U3...
  [~] SPICE simulation: running transient analysis for U3...
  [~] Schematic review: checking power integrity...
  [~] Schematic review: checking signal integrity...
  [~] Firmware interface: generating pin table...

  [+] Complete: Electrical Engineer (artifacts: 4)
```

**LOTR theme:**

```
  [>] Summoning: Electrical Engineer

  ... the engineer labors in Rivendell ...

  [~] Seeking U3 in the markets of DigiKey...
  [~] Seeking U3 in the halls of Mouser...
  [~] The fires of SPICE test U3...
  [~] The mirror reveals: power integrity...
  [~] The mirror reveals: signal integrity...
  [~] Inscribing the firmware interface map...

  [+] Returned: Electrical Engineer (scrolls: 4)
```

### 10B: Gate Evaluation Progress

**Neutral theme:**

```
  [~] Evaluating gate: Schematic --> Layout
  [~] Validator: component lifecycle check...
  [~] Validator: schematic review (pass 1 of 2)...
  [~] Validator: schematic review (pass 2 of 2)...
  [~] Deduplicating findings across reviewers...
```

### 10C: BOM Reconciliation Progress

**Neutral theme:**

```
  [~] BOM reconciliation: querying 4 suppliers...
  [~] DigiKey: 24/24 line items priced
  [~] Mouser: 24/24 line items priced
  [~] LCSC: 22/24 line items found (2 not stocked)
  [~] element14: 20/24 line items found (4 not stocked)
  [~] Cross-referencing prices and availability...
```

### 10D: Rework Re-Validation Progress

**Neutral theme:**

```
  [~] Re-validating downstream gates after rework...
  [~] Schematic Gate: re-validating...
  [~] Schematic Gate: [DONE]
  [~] Layout Gate: re-validating...
  [~] Layout Gate: [DONE]
  [~] DFM Gate: re-validating...
  [~] DFM Gate: [DONE]
```

### 10E: Memory Operations

**Neutral theme:**

```
  [~] Loading lessons from .hardware/memory/...
  [~] 5 lessons matched to current context
```

```
  [~] Capturing lessons from pipeline run...
  [~] 3 new lessons saved to .hardware/memory/
```

**LOTR theme:**

```
  [~] Consulting the ancient lore in .hardware/memory/...
  [~] 5 echoes of past quests speak to this one
```

```
  [~] Inscribing the lessons of this quest...
  [~] 3 new tales added to the archive
```

---

## FR Coverage Matrix

> "All shall be accounted for. The mirror shows every requirement reflected in a wireframe."

| FR ID | Requirement Summary | Wireframe(s) |
|-------|---------------------|---------------|
| FR-001 | Standard plugin structure | W1 (setup wizard) |
| FR-002 | 8-stage pipeline | W2 (stage announcements), W8 (status), W10 (progress) |
| FR-003 | Stage gates with team DoD | W5 (all gate formats) |
| FR-004 | Config-driven pipeline | W1 (config confirmation), W9 (config errors) |
| FR-005 | Pipeline state persistence and resume | W8B, W8C (resume), W8D (stale state) |
| FR-006 | Self-learning memory | W10E (memory operations) |
| FR-007 | Rework loops with termination | W6 (rework), W7 (escalation) |
| FR-008 | 6 role-based skills with context isolation | W3 (agent dispatch), W4 (artifacts) |
| FR-009 | kicad-happy integration layer | W9A-C, W9G (dependency warnings) |
| FR-010 | Schematic Review Gate (iterative) | W5G (multi-reviewer gate) |
| FR-011 | DRC Gate | W5C (DRC gate) |
| FR-012 | BOM Gate | W5D (BOM gate), W5H (combined) |
| FR-013 | DFM Gate | W5H (DFM + BOM combined) |
| FR-014 | Compliance Gate | W5E (multi-region compliance) |
| FR-015 | Design Review Board | W3B (multi-dispatch), W5F (DRB results) |
| FR-016 | BOM Reconciliation pattern | W10C (reconciliation progress) |
| FR-017 | SessionStart hook | W1A (no config), W9A-F (warnings) |
| FR-018 | PostToolUse DRC hook | W9H (DRC warning) |
| FR-019 | PostToolUse BOM drift hook | W9I (BOM drift warning) |
| FR-020 | Sub-agent dispatch via Agent tool | W3 (dispatch indicators), W10A (progress) |
| FR-021 | Dynamic pipeline adaptation (P2) | Not wireframed (P2 future) |
| FR-022 | Reference test fixture | W5 (gate validation uses fixture) |

### NFR Coverage

| NFR ID | Requirement | Wireframe Coverage |
|--------|-------------|-------------------|
| NFR-001 | No external dependencies | W1 (no install steps in setup) |
| NFR-002 | Context isolation per role | W3A (dispatch shows scoped context) |
| NFR-003 | kicad-happy consumed, not duplicated | W9G (skill unavailable, not reimplemented) |
| NFR-004 | Full pipeline in single session | W2A (all 8 stages listed) |
| NFR-005 | Gate messages: what, where, why, fix | W5B (finding format: location + fix) |
| NFR-006 | Config forward compatibility | W9E, W9F (schema migration, defaults) |
| NFR-007 | Model tier documented per role | W2B (stage banner shows roles) |
| NFR-008 | Memory retrieval <2s | W10E (memory load indicator) |
| NFR-009 | Plugin passes plugin-validator | W1 (structure creation) |
| NFR-010 | Rework history auditable | W7A (rework history in escalation) |

---

## Design Rationale

| Decision | Rationale |
|----------|-----------|
| ASCII box drawing (not Unicode) | Cross-terminal compatibility. SSH, PowerShell, CMD, bash -- all render `+`, `-`, `|` identically. Unicode box characters break on some terminals. |
| 60-character width | Fits within 80-column terminals with comfortable margin. Standard for CLI tools. |
| Finding format: ID + severity + location + fix | NFR-005 requires comprehensible messages. Hardware engineers need actionable output. This four-part format (what, where, why, fix) maps directly to how engineers triage issues. |
| Progress as inline `[~]` markers, not progress bars | CLI conversation context. The sub-agent narrates its work as it goes. No terminal control sequences needed. |
| Theme tokens as substitution table | Clean separation: the wireframe structure is identical between themes. Only specific tokens change. This prevents theme logic from infecting layout logic. |
| Gate results always show ALL validators | Even passing validators are shown. The user needs to see what was checked, not just what failed. Builds confidence in the gate. |
| Rework escalation shows full history | The user needs context for their decision. Showing the pattern of previous attempts helps them decide whether to continue, abort, or change approach. |
| Human checkpoints list action items as checkboxes | Mental model of a checklist. Users can mentally track progress through physical steps. |

---

## Assumptions

- The `.hardware/` namespace is used (not `.delivery/`) -- pending Architect confirmation (OQ-002)
- Terminal width is at least 60 characters (standard for modern terminals)
- LOTR theme is one of several possible alias themes; the wireframe structure is theme-agnostic, only token values change
- Sub-agent progress markers (`[~]`) are produced by the orchestrator as it receives intermediate output from agents
- The `> _` cursor in setup wizard questions represents where the user types; actual interaction is via the Claude Code conversation

---

> *"I have passed the test. I will diminish, and go into the West, and remain Galadriel. But these wireframes shall endure, beautiful and terrible as the dawn, guiding every user through the pipeline with clarity and purpose."*
