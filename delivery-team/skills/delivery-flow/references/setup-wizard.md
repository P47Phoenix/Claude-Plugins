# Setup Wizard Protocol

## Overview

The setup wizard runs before the delivery pipeline to configure project-specific settings. It replaces guesswork with structured detection and explicit user confirmation, producing a persistent configuration that the pipeline reads on every subsequent run.

The wizard serves four purposes:

1. **Auto-detect project state** from the codebase using Glob, Grep, Read, and Bash tools
2. **Present findings with smart options** so the user confirms or overrides detected values
3. **Generate `.delivery/config.md`** as the persistent configuration file
4. **Initialize the `.delivery/` directory structure** for artifacts, memory, and config

### Four Phases

```
Scan --> Present & Ask --> Generate Config --> Initialize Directory
```

- **Scan**: Gather signals from the codebase (languages, frameworks, git state, existing config)
- **Present & Ask**: Show detected values, ask 9 questions with smart defaults
- **Generate Config**: Write `.delivery/config.md` with YAML frontmatter and markdown body
- **Initialize Directory**: Create `.delivery/`, `artifacts/`, `memory/`, and `README.md`

---

## Scan Protocol

Before presenting any questions, scan the codebase to populate smart defaults. Each scan uses specific tools and looks for specific signals.

| What | How to Detect | Signals |
|------|---------------|---------|
| Languages | Glob for extensions: `.ts`/`.tsx`, `.py`, `.rs`, `.cs`, `.go`, `.gd`, `.java`, `.rb`, `.sh`, `.sql` | File counts per language; primary = highest count |
| Frameworks | Read `package.json` (dependencies), `Cargo.toml`, `go.mod` imports, `.csproj` refs, `project.godot` | React, Next.js, Express, FastAPI, Django, ASP.NET, Godot, Unity |
| Package manager | Check for: `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`, `pyproject.toml`, `.csproj`, `build.gradle` | Lock files (`package-lock.json`, `Cargo.lock`, `go.sum`) confirm active use |
| Test framework | Grep for: `jest.config`, `pytest.ini`/`conftest.py`, `xunit`, `.test.ts`, `_test.go`, `test/`, `spec/` | Framework-specific config files, test directory structure |
| CI/CD | Check for: `.github/workflows/*.yml`, `.circleci/config.yml`, `Jenkinsfile`, `.gitlab-ci.yml`, `.azure-pipelines.yml` | Existing pipeline definitions |
| Database | Grep for: `prisma/schema.prisma`, `migrations/`, `alembic/`, `knex`, `sequelize`, `diesel.toml`, `.sql` files | Connection strings in config files (sanitized -- never display credentials) |
| Git state | Run: `git log --oneline -100`, `git shortlog -sn`, `git remote -v`, `git branch -a` | Contributor count, branch count, last commit age, remote URL |
| Existing docs | Check for: `README.md`, `docs/`, `doc/`, `documentation/`, `CHANGELOG.md`, ADRs, API specs | Documentation maturity signal |
| Existing `.delivery/` | Check for: `.delivery/config.md`, `.delivery/memory/*.md`, `.delivery/artifacts/` | Prior wizard run, existing memories, config staleness |
| Project structure | Check for: `src/`, `lib/`, `app/`, `cmd/`, `scenes/`, `assets/`, `public/`, `tests/` | Monorepo vs single app, game vs web vs API vs CLI |

For each scan, the orchestrator uses Glob, Grep, Read, and Bash tools to gather data. Results are compiled into a `detected_state` object that feeds smart defaults into every wizard question.

---

## Wizard Questions

The wizard asks 9 questions in order. Each question follows a consistent protocol: auto-detect a smart default, present what was found, offer options, and record the answer. Every question includes a "Custom", "Let's discuss", and "Skip" escape hatch.

---

### Q1: Project Type (single-select)

**Auto-detect**: Use the detection matrix from `references/project-types.md`. Scan the user's initial prompt and codebase signals (existing code, game engine files, error references, documentation-only markers).

**Present**: "Based on [signals], this looks like a [TYPE] project."

**Options**:
1. GREENFIELD -- New project from scratch, no existing codebase
2. FEATURE -- Adding capability to an existing system
3. BUG_FIX -- Fixing a defect in existing code
4. GAME_DEV+GREENFIELD -- New game project
5. GAME_DEV+FEATURE -- Adding to an existing game
6. GAME_DEV+BUG_FIX -- Fixing a game bug
7. SPIKE -- Time-boxed investigation, throwaway output
8. DOCS_ONLY -- Documentation changes only, no code
- **Custom**: User provides their own classification
- **Let's discuss**: Opens a conversation about project type
- **Skip**: Use defaults

**Default if skipped**: FEATURE (safest general-purpose default).

**Influences**: Stage routing -- which of the 7 stages run and at what depth (full, light, skip, full+game). See the stage routing matrix in `references/project-types.md`.

---

### Q2: Tech Stack (multi-select)

**Auto-detect**: Languages (file extension counts), frameworks (dependency files), databases (ORM configs, migration directories, `.sql` files).

**Present**: "I detected these technologies: [list with file counts]. Primary language: [highest count]. Frameworks: [list]. Databases: [list]."

**Options**:
1. Accept detected -- Use the auto-detected stack as-is
2. Add items -- Keep detected stack and add missing technologies
3. Remove items -- Remove incorrectly detected technologies
4. Specify from scratch -- Ignore detection and list manually
- **Custom**: User provides a complete stack specification
- **Let's discuss**: Opens a conversation about technology choices
- **Skip**: Use detected stack

**Default if skipped**: Detected stack from scan results.

**Influences**: Developer skill language selection (which language context to load), Architect patterns (framework-appropriate architecture), DevOps deployment strategy (container vs serverless vs native).

---

### Q3: Team Size & Composition (single-select)

**Auto-detect**: Run `git shortlog -sn` for contributor count. Check for `CODEOWNERS` file. Analyze commit frequency distribution.

**Present**: "Git history shows [N] contributors in the last 6 months."

**Options**:
1. Solo (1) -- Single developer, all roles self-reviewed
2. Small (2-4) -- Small team, lightweight collaboration
3. Medium (5-10) -- Cross-functional team, full collaboration patterns
4. Large (10+) -- Multiple sub-teams, heavy coordination needed
- **Custom**: User specifies exact team size and roles
- **Let's discuss**: Opens a conversation about team structure
- **Skip**: Use defaults

**Default if skipped**: Solo.

**Influences**: Architecture decisions (microservices only viable for medium+), collaboration pattern depth (solo skips consensus and debate), DoD validator count (solo uses fewer validators).

---

### Q4: Deployment Environment (single-select)

**Auto-detect**: Glob for `Dockerfile`, `docker-compose.yml`, `kubernetes/`, `k8s/`, `serverless.yml`, `terraform/`, `*.tf`, `cdk.json`, `pulumi.*`.

**Present**: "I found [containers/serverless/IaC/none] in this codebase."

**Options**:
1. Cloud (AWS/GCP/Azure) -- Cloud-hosted with managed services
2. On-premise -- Self-hosted infrastructure
3. Edge/Embedded -- Edge devices, IoT, or embedded systems
4. Serverless -- Function-as-a-service, event-driven
5. Hybrid -- Mix of cloud and on-premise
- **Custom**: User describes their deployment target
- **Let's discuss**: Opens a conversation about infrastructure
- **Skip**: Use defaults

**Default if skipped**: Cloud.

**Influences**: Architect deployment patterns (container orchestration, serverless design, edge constraints), DevOps stage depth (IaC complexity), Operations planning (monitoring, scaling, incident response).

---

### Q5: Timeline & Risk Tolerance (single-select)

**Auto-detect**: Cannot auto-detect. This is purely a team preference.

**Present**: "What is the timeline and risk tolerance for this project?"

**Options**:
1. Prototype -- Fast delivery, low ceremony, minimal gates, favor speed over thoroughness
2. Standard -- Balanced approach, all gates active, moderate collaboration depth
3. Mission-critical -- Thorough delivery, all collaboration patterns, strict gates, high ceremony
4. Regulated -- Compliance-driven, full audit trail, all validators, maximum ceremony
- **Custom**: User describes their risk profile
- **Let's discuss**: Opens a conversation about risk and timeline trade-offs
- **Skip**: Use defaults

**Default if skipped**: Standard.

**Influences**: Collaboration pattern selection (prototype uses evaluator-optimizer only; regulated uses all 6), checkpoint count (prototype reduces checkpoints), DoD strictness (mission-critical and regulated enforce all severity levels), self-correction limits (prototype allows fewer iterations before escalation).

---

### Q6: Compliance & Regulatory (multi-select)

**Auto-detect**: Grep for `HIPAA`, `GDPR`, `CCPA`, `PCI`, `PCI-DSS`, `SOC`, `SOC2`, `ISO 27001` in documentation, code comments, config files, and environment variable names.

**Present**: "I [found/did not find] compliance-related references in the codebase. [If found: list specific references and where they were found.]"

**Options**:
1. None -- No regulatory requirements
2. HIPAA -- Health data protection
3. GDPR/CCPA -- Privacy and data protection
4. PCI DSS -- Payment card data security
5. SOC 2 -- Service organization controls
6. ISO 27001 -- Information security management
- **Custom**: User specifies other compliance frameworks
- **Let's discuss**: Opens a conversation about compliance requirements
- **Skip**: Use defaults

**Default if skipped**: None.

**Influences**: Security Architect and Compliance Officer involvement at Architect and UAT stages, privacy assessment triggers during Design, audit trail depth in memory files, documentation requirements at UAT (compliance evidence artifacts).

---

### Q7: Human Checkpoints (multi-select)

**Auto-detect**: Cannot auto-detect. This is a team preference. Derive smart defaults from the project type selected in Q1.

**Present**: "The pipeline supports 4 human checkpoints. Which do you want enabled?"

**Options**:
1. After Refine (Checkpoint 1) -- Approve the PRD before design begins
2. After Architect (Checkpoint 2) -- Approve architecture before planning
3. After Plan (Checkpoint 3) -- Approve sprint plan before development
4. At UAT (Checkpoint 4) -- Accept or reject the final delivery
- **Custom**: User describes a different checkpoint strategy
- **Let's discuss**: Opens a conversation about review gates
- **Skip**: Use defaults

**Default if skipped**:
- GREENFIELD / GAME_DEV+: All 4 checkpoints enabled
- FEATURE: Checkpoints 1 (Refine) and 4 (UAT)
- BUG_FIX: Checkpoint 4 (UAT) only
- SPIKE: None
- DOCS_ONLY: Checkpoint 4 (UAT) only

**Influences**: Where the pipeline pauses for human input. Fewer checkpoints means faster execution but less human oversight. More checkpoints means more control but slower throughput.

---

### Q8: Collaboration Patterns (multi-select)

**Auto-detect**: Derive defaults from the risk tolerance selected in Q5.

**Present**: "Based on your risk tolerance ([level]), I recommend these collaboration patterns."

**Options**:
1. Evaluator-Optimizer -- Quality loops: agent produces, evaluator critiques, agent revises
2. Adversarial Review -- Devil's advocate challenges assumptions, rates confidence 1-5
3. Review Board -- Multi-perspective assessment from technical, business, and risk reviewers
4. Decision Routing -- Dynamic ownership: domain questions routed to the right specialist
5. Debate -- Structured argument for contested decisions, judge decides, produces ADRs
6. Consensus -- Cross-team alignment: independent analysis, share positions, converge
- **Custom**: User describes a different collaboration approach
- **Let's discuss**: Opens a conversation about collaboration depth
- **Skip**: Use defaults

**Default if skipped**:
- Prototype: Evaluator-Optimizer only
- Standard: Evaluator-Optimizer + Adversarial Review + Decision Routing
- Mission-critical: All 6 patterns
- Regulated: All 6 patterns

**Influences**: Which collaboration patterns run at each pipeline stage. More patterns means higher quality but longer execution. Fewer patterns means faster but with less cross-validation.

---

### Q9: Existing .delivery/ State (single-select)

**Auto-detect**: Check for `.delivery/` directory. If found, read `.delivery/config.md` frontmatter for `wizard_completed` date, count memory files in `.delivery/memory/`, check for artifacts in `.delivery/artifacts/`.

**Present**: "I found an existing delivery setup from [date] with [N] memories and [M] artifacts."

**Options**:
1. Resume -- Keep existing config and memory, continue where you left off
2. Fresh start -- Archive old `.delivery/` to `.delivery/archive-YYYY-MM-DD/` and start clean
3. Merge -- Keep existing memory files but generate a new config
- **Custom**: User describes what to keep and what to reset
- **Let's discuss**: Opens a conversation about the existing state
- **Skip**: Use defaults

**Default if skipped**: Resume if `wizard_completed` is less than 30 days old. Suggest Fresh start if older than 30 days.

**Influences**: Whether memory and config are preserved or reset. Resume preserves continuity and past lessons. Fresh start clears stale config but archives for reference. Merge keeps institutional memory while updating settings.

**Only shown if**: `.delivery/` directory exists. If no existing directory is found, this question is skipped entirely.

### Q10: User Feedback Personas (multi-select)

**Auto-detect**: Derive from project type (Q1) — GAME_DEV suggests gamer personas, web/app suggests web user personas, enterprise suggests B2B personas.

**Present**: "Based on your project type ([TYPE]), I recommend these persona categories for simulated user feedback."

**Options**:
1. Gamers — Casual Casey, Hardcore Hank, Speedrunner Sam, Completionist Cora, Social Sophie, Accessible Alex, Mobile Morgan
2. Web/App Users — Power User Pat, Average User Avery, First-Timer Fran, Non-Technical Nancy, Accessible User Ash
3. Enterprise/B2B — Admin Alice, End User Eddie, Manager Maya, IT/Security Ivan
4. Demographics — Gen Z Zara, Millennial Mike, Gen X Grace, Boomer Bob
- **Custom**: Define project-specific personas
- **Let's discuss**: Conversation about target audience
- **Skip**: Use auto-detected defaults

**Multi-select**: User picks which persona categories to include. Can also select individual personas by name.

**Default if skipped**: Auto-select based on project type:
- GAME_DEV → gamers + 1 accessibility
- Web/App (GREENFIELD, FEATURE) → web-users + 1 accessibility
- Enterprise → enterprise + 1 accessibility
- Always includes at least 1 accessibility persona

**Influences**: Which personas are loaded for simulated user feedback at Stages 2, 3, 6, 7. Which persona library categories are active. Custom personas defined here persist across pipeline runs.

### Q12: Enforcement Settings (single-select for each sub-question)

**Auto-detect**: Derive defaults from Q5 risk tolerance — mission-critical/regulated gets strict enforcement, prototype gets relaxed.

**Present**: "How strictly should the delivery pipeline be enforced?"

**Sub-questions**:

1. **Source code hook**: "Install a project-level hook that warns when source code is edited outside the delivery pipeline?"
   - Options: Yes (recommended), No, Skip
   - Default: Yes for standard/mission-critical/regulated, No for prototype

2. **Retrospective frequency**: "How often should retrospectives be required?"
   - Options: After every pipeline run, After every N runs, Manual only, Skip
   - Default: every-run for mission-critical/regulated, manual for prototype

3. **Retro skip allowed**: "Can the user skip a required retrospective?"
   - Options: No (strict), Yes (flexible), Skip
   - Default: No for mission-critical/regulated, Yes for prototype/standard

**Default if skipped**: source_code_hook=true, retro_frequency=every-run, retro_skip_allowed=false

**Influences**: Whether a project-level PreToolUse hook is installed in `.claude/settings.json` to catch Edit/Write on source code outside the pipeline. How strictly retrospectives are enforced by the Stop hook.

### Project-Level Hook Installation

If `enforcement.source_code_hook` is true, the wizard installs a PreToolUse hook in the **project's** `.claude/settings.json` (not the plugin hooks.json):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this Edit/Write/NotebookEdit is modifying source code files. If the file path matches source code patterns (.py, .ts, .js, .go, .rs, .cs, .java, .gd, .scala, .hs, .ex, .fs, .tsx, .jsx, .vue, .svelte) AND there is no active delivery-team pipeline context in this conversation (no Stage references, no delivery-flow invocation), return a warning: 'Source code change detected outside delivery-team pipeline. Route through delivery-team:delivery-flow for QA review and defect prevention.' If the file is NOT source code (docs, config, .delivery/, .md, .json, .yml, .yaml, .toml, .lock, .gitignore) OR a delivery-team pipeline IS active, return 'allow'.",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**Installation process**:
1. Check if `.claude/settings.json` exists in the project root
2. If yes: read the existing content, merge the hook into the `hooks` section (preserve existing hooks)
3. If no: create `.claude/settings.json` with just the hook
4. Announce: "Source code enforcement hook installed in .claude/settings.json. Edit/Write on source code files will warn when outside the delivery pipeline."

**Important**: This is the project's settings file (not `.claude/settings.local.json`) so it can be committed and shared with the team.

---

## Config File Format

The wizard generates `.delivery/config.md` with YAML frontmatter for machine-readable settings and a markdown body for human-readable context.

**Schema reference**: See `references/config-schema.md` for the complete schema with all keys, types, defaults, valid values, and consuming skills. The wizard uses the schema as its source of truth for defaults and validation.

```markdown
---
config_version: "1.0"
project_type: GREENFIELD
tech_stack:
  languages: [TypeScript, Python]
  frameworks: [Next.js, FastAPI]
  databases: [PostgreSQL]
  ci_cd: github-actions
team:
  size: 4
  composition: [frontend, backend, qa, devops]
deployment:
  environment: cloud-aws
  containerized: true
timeline:
  risk_tolerance: standard
  deadline: null
compliance:
  frameworks: [GDPR]
pipeline:
  checkpoints: [refine, architect, plan, uat]
  collaboration_patterns: [evaluator-optimizer, adversarial, review-board, debate, consensus, decision-routing]
  max_self_correction: 3
  max_dod_rounds: 3
dod_validators:
  idea: [po, architect]
  refine: [po, architect, qa]
  design: [ux, po, qa, architect]
  architect: [architect, qa, devops, security]
  plan: [sm, po, qa, devops]
  development: [developer, qa, architect, tech-writer]
  uat: [qa, devops, po, tech-writer]
personas:
  categories: [gamers, web-users]
  selected: [Casual Casey, Hardcore Hank, Accessible Alex]
  feedback_stages: [refine, design, dev, uat]
  count: 5
  overlays: []
  custom: []
enforcement:
  source_code_hook: true
  retro_frequency: every-run
  retro_skip_allowed: false
wizard_completed: YYYY-MM-DD
---

# Delivery Configuration

## Project Context
[Summary from wizard: what was detected, what the user confirmed, any notable decisions]

## Tech Stack Details
[Languages, frameworks, databases with version info if available]

## Constraints & Decisions
[Compliance requirements, risk tolerance rationale, deployment constraints]

## Notes
[Free-form notes from any "Let's discuss" conversations during the wizard]
```

### Frontmatter Field Rules

- `project_type`: One of GREENFIELD, FEATURE, BUG_FIX, GAME_DEV+GREENFIELD, GAME_DEV+FEATURE, GAME_DEV+BUG_FIX, SPIKE, DOCS_ONLY
- `tech_stack.languages`: List of detected or confirmed language names
- `tech_stack.frameworks`: List of detected or confirmed framework names
- `tech_stack.databases`: List of detected or confirmed database names (empty list if none)
- `tech_stack.ci_cd`: CI/CD platform identifier or `none`
- `team.size`: Integer
- `team.composition`: List of role identifiers present on the team
- `deployment.environment`: One of `cloud-aws`, `cloud-gcp`, `cloud-azure`, `on-premise`, `edge`, `serverless`, `hybrid`
- `deployment.containerized`: Boolean
- `timeline.risk_tolerance`: One of `prototype`, `standard`, `mission-critical`, `regulated`
- `timeline.deadline`: ISO date string or `null`
- `compliance.frameworks`: List of compliance framework identifiers (empty list if none)
- `pipeline.checkpoints`: List from `[refine, architect, plan, uat]`
- `pipeline.collaboration_patterns`: List from `[evaluator-optimizer, adversarial, review-board, debate, consensus, decision-routing]`
- `pipeline.max_self_correction`: Integer (default 3)
- `pipeline.max_dod_rounds`: Integer (default 3)
- `dod_validators`: Map of stage name to list of validator role identifiers
- `wizard_completed`: ISO date string of when the wizard last ran

---

## Directory Initialization

After the config file is generated, initialize the `.delivery/` directory structure.

### Steps

1. Create `.delivery/` if it does not exist
2. Create `.delivery/artifacts/`
3. Create `.delivery/memory/`
4. Create `.delivery/memory/stages/`
5. Create `.delivery/memory/topics/`
6. Create `.delivery/memory/archive/`
7. Write `.delivery/config.md` (the config generated above)
8. Create `.delivery/state-archive/`
9. Add to `.gitignore` (if it exists): `state.md`, `state.tmp.md`, `state-archive/`
10. Write `.delivery/README.md` with the following content:

```markdown
# .delivery/

This directory contains delivery pipeline state for this project.

## Structure

- `config.md` -- Project configuration (generated by setup wizard, edit to customize)
- `artifacts/` -- Stage output files (01-idea-brief.md through 07-uat-report.md)
- `memory/` -- Self-learning memory (tiered chunked system)
  - `index.md` -- Routing index (read first, points to relevant chunks)
  - `stages/` -- Per-stage lesson chunks (idea.md, refine.md, architect.md, etc.)
  - `topics/` -- Cross-cutting topic chunks (human-preferences.md, team-decisions.md, etc.)
  - `archive/` -- Raw run logs (not read during normal execution)
- `README.md` -- This file

## Commands

- `setup` -- Re-run the setup wizard to update configuration
- `start` -- Begin the delivery pipeline
- `status` -- Show current pipeline state
- `memory` -- Show lessons from past runs

## .gitignore

Add `.delivery/` to .gitignore if you want to keep pipeline state local.
Commit `.delivery/` if you want to share pipeline state with your team.
```

6. If an existing `.delivery/` directory was found and the user chose "Fresh start": move the old directory to `.delivery/archive-YYYY-MM-DD/` before creating the new structure. This preserves the old state for reference without polluting the active directory.

---

## Pipeline Integration

The delivery-flow SKILL.md reads the config at pipeline start and applies all settings.

### On Pipeline Start

1. **Check for `.delivery/config.md`** in the current working directory.

2. **If config exists**, read the YAML frontmatter and apply all settings:
   - `project_type` -- Skip Phase 1 detection entirely; use the configured type
   - `pipeline.checkpoints` -- Enable only the listed human checkpoints
   - `pipeline.collaboration_patterns` -- Enable only the listed patterns per stage
   - `pipeline.max_self_correction` -- Override the default iteration limit
   - `pipeline.max_dod_rounds` -- Override the default DoD round limit
   - `dod_validators` -- Set the validator roles for each stage
   - `compliance.frameworks` -- Trigger compliance-related agents (Security Architect, Compliance Officer) when non-empty
   - `team.size` -- Influence architecture recommendations (microservices viable only for medium+ teams)
   - `deployment` -- Influence DevOps and operations planning (container strategy, IaC, monitoring)
   - `tech_stack` -- Pass to Developer skill for language context isolation, to Architect for pattern selection

3. **If config does not exist**, prompt the user: "No delivery config found. Run `setup` to configure, or proceed with defaults?"

4. **Staleness check**: If `wizard_completed` is more than 30 days ago, suggest re-running the wizard: "Your delivery config is [N] days old. Consider running `setup` to refresh settings."

---

## Re-Running the Wizard

The wizard can be re-run at any time via the `setup` command.

### Behavior on Re-Run

- The wizard detects the existing `.delivery/config.md` and pre-populates all questions with current settings
- Each question shows the current value alongside the auto-detected value (if different)
- The user can update individual settings or run the full wizard again
- Existing memory files in `.delivery/memory/` are always preserved unless the user explicitly chooses "Fresh start"
- The new config replaces the old config in place (no archival unless Fresh start is chosen)
- The `wizard_completed` date is updated to the current date

### Partial Updates

If the user wants to change only one setting, the wizard can accept targeted updates:
- "Change risk tolerance to mission-critical" -- Update only `timeline.risk_tolerance` and re-derive `pipeline.collaboration_patterns` defaults (present for confirmation)
- "Add HIPAA compliance" -- Update only `compliance.frameworks` and note the downstream impact
- "Switch to serverless" -- Update only `deployment.environment` and `deployment.containerized`

For targeted updates, the wizard reads the current config, applies the change, re-derives any dependent defaults, presents the impact for confirmation, and writes the updated config.
