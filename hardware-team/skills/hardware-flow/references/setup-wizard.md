# Setup Wizard Protocol

## Overview

The setup wizard runs when the user invokes `hw-setup` to configure project-specific settings for the hardware pipeline. It produces `.hardware/config.yml` and initializes the `.hardware/` directory structure.

The wizard serves four purposes:

1. **Auto-detect project state** from the codebase using Glob, Grep, Read, and Bash tools
2. **Present findings with smart options** so the user confirms or overrides detected values
3. **Generate `.hardware/config.yml`** as the persistent configuration file (pure YAML, no frontmatter)
4. **Initialize the `.hardware/` directory structure** for artifacts, state, and memory

### Four Phases

```
Scan --> Present & Ask --> Generate Config --> Initialize Directory
```

- **Scan**: Gather signals from the codebase (KiCad files, existing config, project structure)
- **Present & Ask**: Show detected values, ask questions with smart defaults
- **Generate Config**: Write `.hardware/config.yml` as a pure YAML configuration file
- **Initialize Directory**: Create `.hardware/`, `artifacts/`, `memory/`, and `state.md`

---

## Scan Protocol

Before presenting any questions, scan the codebase to populate smart defaults. Each scan uses specific tools and looks for specific signals.

| What | How to Detect | Signals |
|------|---------------|---------|
| KiCad project | Glob for `*.kicad_pro`, `*.kicad_sch`, `*.kicad_pcb` | Project file presence, schematic/PCB existence |
| Board layers | Read `*.kicad_pcb` for layer definitions | Copper layer count in PCB file |
| Existing config | Check for `.hardware/config.yml` | Prior wizard run, config staleness |
| Existing state | Check for `.hardware/state.md` | Prior pipeline run, resume candidate |
| kicad-happy | Check for kicad-happy skills in marketplace | Plugin availability |
| Fab files | Glob for `*gerber*`, `*Gerber*`, `*.gbr`, `fabrication/` | Existing manufacturing outputs |
| BOM files | Glob for `*bom*`, `*BOM*`, `*.csv` in project root | Existing BOM data |
| Compliance docs | Glob for `*compliance*`, `*certification*`, `*fcc*`, `*ce*` | Existing compliance artifacts |
| Git state | Run: `git log --oneline -10`, `git remote -v` | Project maturity, remote URL |
| Project name | Read `*.kicad_pro` for project name, or use directory name | Auto-detect project identity |

For each scan, the orchestrator uses Glob, Grep, Read, and Bash tools to gather data. Results are compiled into a `detected_state` object that feeds smart defaults into every wizard question.

---

## Two Wizard Modes

### Quick-Start Mode (3 questions)

For users who want to get going fast. Uses aggressive auto-detection and sensible defaults for everything else.

**Trigger**: User says "quick setup", "fast setup", or the wizard detects a simple project (single KiCad project file, no existing compliance artifacts).

**Questions**:

1. **Project name** -- auto-detected from KiCad project file or directory name
2. **Target fab house** -- jlcpcb (default) / pcbway / custom
3. **Board layer count** -- auto-detected from PCB file or default to 2

All other fields use defaults from the schema (see `config-schema.md`).

### Full Wizard Mode (9 questions)

For users who want full control over pipeline configuration.

**Trigger**: User says "full setup", "configure everything", or the wizard detects a complex project (multiple KiCad files, compliance artifacts present, production indicators).

---

## Wizard Questions (Full Mode)

The wizard asks 9 questions in order. Each question follows a consistent protocol: auto-detect a smart default, present what was found, offer options, and record the answer.

---

### Q1: Project Name

**Auto-detect**: Read `*.kicad_pro` for project name. Fallback: use current directory name.

**Present**: "I detected your project name as: [name]. Use this?"

**Options**:
1. Accept detected name
2. Enter a different name

**Config key**: `project_name`

---

### Q2: Target Fabrication House

**Auto-detect**: Check for existing Gerber/fabrication outputs. If JLCPCB-formatted files found, suggest jlcpcb. If PCBWay-formatted, suggest pcbway.

**Present**: "Target fabrication house?"

**Options**:
1. **jlcpcb** (default) -- JLCPCB
2. **pcbway** -- PCBWay
3. **custom** -- Other fab house (will prompt for name)

**Config keys**: `target_fab`, `custom_fab_name`

---

### Q3: Compliance Regions

**Auto-detect**: Check for existing compliance documents. If FCC/CE documents found, pre-select those regions.

**Present**: "Target compliance regions? (comma-separated, or 'none')"

**Examples**: FCC, CE, UL, RoHS, REACH, none

**Options**:
1. Accept detected regions
2. Enter regions manually
3. None -- skip compliance

**Config key**: `compliance_regions`

---

### Q4: BOM Budget

**Auto-detect**: Check existing BOM files for cost data.

**Present**: "BOM budget target (USD per unit)?"

**Options**:
1. Enter a budget (e.g., 12.50)
2. No limit (default)

**Config keys**: `bom_budget`, `second_source_required`

**Follow-up** (if budget entered): "Require second source for all components? [y/N]"

---

### Q5: Production Volume

**Present**: "Production volume target?"

**Options**:
1. **prototype** (default) -- fewer than 10 units
2. **small-batch** -- 10 to 1,000 units
3. **production** -- more than 1,000 units

**Config key**: `production_volume`

---

### Q6: Board Layer Count

**Auto-detect**: Read `*.kicad_pcb` for copper layer definitions. Count `Cu` layers.

**Present**: "Board layer count? (detected: [N] from PCB file)"

**Options**: 1, 2, 4, 6, 8

**Config key**: `board_layers`

---

### Q7: kicad-happy Version

**Auto-detect**: Check installed kicad-happy version.

**Present**: "Minimum kicad-happy version?"

**Default**: >=1.2.0

**Config key**: `dependencies.kicad_happy_version`

---

### Q8: Rework Iteration Limit

**Present**: "Maximum rework iterations per path?"

**Default**: 3

**Explanation**: "How many times a single rework path (e.g., schematic->layout->schematic) can repeat before escalating to the user."

**Config key**: `rework.max_rework_iterations`

---

### Q9: Total Rework Limit

**Present**: "Maximum total reworks per pipeline run?"

**Default**: 10

**Explanation**: "Pipeline-wide cap on all rework iterations combined. When hit, the pipeline escalates to the user."

**Config key**: `rework.max_total_reworks`

---

## Full Mode Additional Settings

After the 9 questions, if in full mode, the wizard asks about advanced settings:

- **Gate strictness**: strict / standard (default) / relaxed
- **Schematic review passes**: 1-5 (default: 2)
- **Design review board**: yes (default) / no
- **Staleness thresholds**: warning days (default: 7), critical days (default: 30)

These are presented as: "Advanced settings -- press Enter to accept all defaults, or type 'configure' to set individually."

---

## Config Generation

After all questions are answered, the wizard generates `.hardware/config.yml`:

1. Build the YAML structure from answers + defaults for unanswered fields
2. Write the file as pure YAML (no `---` frontmatter delimiters)
3. Display a summary of the generated config
4. Validate the config against the schema using `validate_config.py`

**Output**:
```
Created .hardware/config.yml (schema v1.0)

  project: sensor-board-v2
  target_fab: jlcpcb
  compliance_regions: [FCC, CE]
  bom_budget: 12.50
  volume: small-batch
  layers: 4
  dependencies:
    kicad_happy_version: ">=1.2.0"
  rework:
    max_rework_iterations: 3
    max_total_reworks: 10

Edit .hardware/config.yml to adjust settings.
```

---

## Directory Initialization

The wizard creates the `.hardware/` directory structure:

```
.hardware/
├── config.yml          # Project configuration (just created)
├── state.md            # Pipeline state (empty, created on first run)
├── memory/             # Self-learning memory (empty, populated after runs)
└── artifacts/          # Pipeline artifacts (created by stages)
    ├── 01-concept/
    ├── 02-schematic/
    ├── 03-layout/
    ├── 04-prototype/
    ├── 05-compliance/
    ├── 06-pilot-run/
    ├── 07-production-release/
    └── 08-manufacturing/
```

---

## Existing Config Handling

If `.hardware/config.yml` already exists when `hw-setup` is invoked:

1. Detect and display current config version
2. Ask: "Config already exists (schema v1.0). Overwrite? [y/N]"
3. If N: exit, config preserved
4. If y: proceed with wizard (old config values used as smart defaults)

---

## Gitignore Offer

At the end of setup, the wizard MUST offer to create or update the project's `.gitignore` with hardware-specific entries:

```
# Hardware pipeline state (session-specific)
.hardware/state.md
.hardware/config-snapshot-*.yml

# Memory (project-specific, optional to track)
# .hardware/memory/
```

---

## Validation

After config generation, the wizard runs validation:

```
Config valid. Ready to run pipeline.

Setup complete. To start the hardware pipeline:
  "Run the hardware pipeline"
  or invoke: hardware-team:hardware-flow
```

If validation finds issues (should not happen with wizard-generated config):

```
WARNING: Config validation found issues:
  - [field]: [issue description] (using default: [value])

Config usable. Pipeline will use defaults for invalid fields.
```
