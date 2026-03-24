---
name: delivery-flow
description: Delivery pipeline orchestrator that coordinates the full delivery team through 7 stages (Idea, Refine, Design, Architect, Plan, Development, UAT) with auto-detection of project type, self-correction loops, adversarial review, multi-perspective review boards, team Definition of Done validation, dynamic escalation, debate for contested decisions, consensus for cross-team alignment, and self-learning memory. Triggers on phrases like "delivery pipeline", "full delivery", "end-to-end delivery", "start project", "new project", "greenfield", "new feature", "bug fix", "spike", "POC", "proof of concept", "game project", "delivery flow", "run pipeline", "start pipeline", "deliver this", "build and ship", "start delivery", "kick off project".
license: Apache License 2.0 - See repository LICENSE file
---

# Delivery Flow Orchestrator

## Design Principle: Team-Based Delivery with Self-Correction and Learning

This skill is the ORCHESTRATOR. It coordinates the delivery team through a structured
pipeline but NEVER produces domain artifacts directly. All domain work -- requirements,
designs, architecture, code, tests, plans -- is delegated to worker skills that operate
as sub-agents with isolated context.

### Core Principles

1. **Delegation, not execution.** The orchestrator manages flow, routing, and validation.
   Worker skills (product-delivery, developer, godot, architect, quality, operations, ui)
   produce all artifacts. Workers are invoked as sub-agents using the Agent tool.

2. **Multi-perspective validation.** Every artifact is validated by MULTIPLE team roles
   (Team Definition of Done) before a stage is complete. No single perspective gates
   quality -- the team decides collectively.

3. **Self-correction with bounds.** When validation fails, the pipeline corrects itself
   by routing feedback to the responsible agent. Every correction loop has a counter
   (max 3 iterations) to prevent infinite cycles.

4. **Dynamic escalation.** Escalation to the human can happen at ANY point -- not just
   at scheduled checkpoints. Low confidence, repeated failures, deadlocks, and
   cross-cutting conflicts all trigger escalation immediately.

5. **Learning from every run.** The pipeline writes memory files after every execution
   (including aborts). Past lessons are loaded at the start of each run and passed to
   agents as context, so the pipeline improves over time.

6. **Six collaboration patterns.** Quality is ensured through structured collaboration:
   Evaluator-Optimizer loops, Adversarial Review, Multi-Perspective Review Boards,
   Decision Ownership Routing, Debate for contested decisions, and Consensus for
   cross-team alignment. See `references/team-patterns.md` for full protocol details.

7. **Context isolation.** Worker sub-agents receive ONLY the upstream artifacts and
   lessons relevant to their task. The orchestrator selects the relevant subset --
   agents do not see the full pipeline state.

---

## Phase 0: Setup Wizard

Before the pipeline executes, check for project configuration:

### State Detection (Resume Check)

Before checking config, check for an existing pipeline state:

1. **Check for `.delivery/state.md`** in the current working directory.
2. **If state exists with `status: in_progress`**:
   - Read the YAML frontmatter to load pipeline state.
   - Announce: `> Existing pipeline found: [pipeline_id], started [date], last completed Stage [N] ([name]). Currently at Stage [N+1].`
   - **Validate**: verify all artifact files in the `artifacts` map exist on disk. If any are missing, announce which and offer: Restart from that stage / Abandon.
   - **Semantic validation**: current_stage in range 1-7, not in stages_completed, no gaps in completed+skipped.
   - **Config divergence check**: diff `config_snapshot` against current `.delivery/config.md`. If different, warn: "Config has changed since this pipeline started. Resume uses the original config. Choose Restart to apply new config."
   - Offer the user: **Resume** / **Restart** / **Abandon**
   - Resume: load config from snapshot, skip completed stages, start at current_stage.
   - Restart: move state file to `.delivery/state-archive/state-<timestamp>.md` (cap at 5, delete oldest), start fresh.
   - Abandon: delete state file, no pipeline runs.
3. **If state exists with `status: aborted`**:
   - Announce: `> Aborted pipeline found from [date], stopped at Stage [N]. Artifacts from stages [list] are preserved.`
   - Offer: Resume / Restart / Abandon (same as above).
4. **If state exists with `status: completed`**: ignore (previous run finished normally).
5. **If no state file exists**: proceed to config check (normal flow).

1. **Check for `.delivery/config.md`** in the current working directory.
2. **If config exists and is fresh** (< 30 days old):
   - Read the YAML frontmatter to load all project settings.
   - **Version check**: Compare `config_version` to the current schema version in
     `references/config-schema.md`. If the config is older (or has no `config_version`),
     apply defaults for any missing keys from the schema and announce:
     `> Config upgraded from v[old] to v[current]. New settings applied with defaults: [list]`
     Offer the user `setup` to configure new settings interactively.
   - Announce: `> Config loaded from .delivery/config.md (v[version], created [date])`
   - Apply settings: project type, tech stack, checkpoints, collaboration patterns, DoD validators, iteration limits, compliance requirements, persona config.
   - For any key missing from the config, use the default from `references/config-schema.md`.
   - Skip Phase 1 (type detection) — use `project_type` from config.
   - Proceed directly to Phase 2 (Memory Retrieval).

3. **If config exists but is stale** (> 30 days old):
   - Announce: `> Existing config found from [date] — it may be outdated.`
   - Offer options: Use as-is, Re-run wizard to update, Proceed with defaults.

4. **If no config exists**:
   - **STOP. Do NOT proceed to Phase 1.** The setup wizard MUST run before the pipeline can execute.
   - Run the setup wizard. Reference `references/setup-wizard.md` for the full protocol.
   - The wizard has 4 phases:
     - **Scan**: Auto-detect project state (languages, frameworks, CI/CD, git history, existing `.delivery/`)
     - **Present & Ask**: For each configuration topic, show what was detected and present 3-5 smart options. Each question supports single-select or multi-select as appropriate, plus Custom, Let's discuss, and Skip.
     - **Generate Config**: Write `.delivery/config.md` with all settings as YAML frontmatter + markdown context.
     - **Initialize Directory**: Create `.delivery/artifacts/`, `.delivery/memory/`, `.delivery/README.md`.
     - **Install Enforcement Hook**: If `enforcement.source_code_hook` is true (default), install a PreToolUse hook in the project's `.claude/settings.json` that warns when source code is edited outside an active delivery pipeline. See `references/setup-wizard.md` for the hook definition and installation process.
   - After the wizard completes, `.delivery/config.md` MUST exist before proceeding.
   - If the user wants to skip the wizard entirely, they must explicitly say "skip setup" or "use defaults" — in which case, generate a minimal `.delivery/config.md` with auto-detected defaults and proceed. The pipeline NEVER runs without a config file.

5. **User can re-run the wizard at any time** with the `setup` command.

### Quick-Start Mode

If the user says "quick start", "quick setup", or "just get started", run a 3-question wizard instead of the full 9+ question version:

1. **What are you building?** -- auto-detect project type from the answer
2. **What language/framework?** -- auto-detect from codebase, user confirms
3. **How strict?** -- Prototype (minimal) / Standard (balanced) / Strict (full)

All other settings use smart defaults from `references/config-schema.md` based on the project type and strictness level. Generate `.delivery/config.md` and proceed.

See `references/getting-started.md` for the complete quick-start walkthrough, skill map, and command cheat sheet.

### Config Settings Applied to Pipeline

When a config is loaded, these settings override defaults:

| Config Key | Pipeline Behavior |
|-----------|-------------------|
| `project_type` | Skips Phase 1 detection, uses configured type |
| `pipeline.checkpoints` | Enables/disables human checkpoints per stage |
| `pipeline.collaboration_patterns` | Enables/disables patterns per stage |
| `pipeline.max_self_correction` | Overrides default iteration limit (default: 3) |
| `pipeline.max_dod_rounds` | Overrides default DoD rounds (default: 3) |
| `dod_validators.*` | Sets per-stage validator roles |
| `compliance.frameworks` | Triggers Compliance Officer and Privacy Engineer involvement |
| `team.size` | Influences architecture decisions (microservices viability, etc.) |
| `deployment.environment` | Influences DevOps and operations planning |
| `timeline.risk_tolerance` | Influences pattern depth and ceremony level |
| `tech_stack.*` | Passed to Developer and Architect for language/framework context |
| `tech_stack.paradigm` | Default paradigm for multi-paradigm languages (auto/oop/fp/hybrid) |
| `tech_stack.paradigm_by_language` | Per-language paradigm override (e.g., python: oop, typescript: fp) |
| `tech_stack.nx_workspace` | Whether Nx monorepo reference is loaded (auto-detected from nx.json) |
| `personas.categories` | Which persona categories to load (gamers, web-users, enterprise, demographics) |
| `personas.selected` | Specific persona names to include in every feedback round |
| `personas.feedback_stages` | Which pipeline stages run persona feedback (default: refine, design, dev, uat) |
| `personas.custom` | Custom persona definitions (see user-feedback skill's `references/custom-personas.md`) |
| `enforcement.source_code_hook` | Whether project-level PreToolUse hook warns on Edit/Write outside pipeline |
| `enforcement.retro_frequency` | How often retrospectives are required (every-run / every-n-runs / manual) |
| `enforcement.retro_skip_allowed` | Whether "skip retro" is allowed (false for mission-critical) |
| `git.branch_strategy` | Branching strategy for feature branches |
| `git.auto_branch` | Whether to auto-create branches at Plan stage |
| `git.commit_convention` | Commit message convention (conventional commits) |
| `git.clean_tree_check` | Whether UAT validates clean working tree |
| `github.create_issues` | Whether to create GitHub issues from user stories at Refine |
| `github.create_pr` | Whether to create a PR at UAT stage |
| `github.link_commits` | Whether commit messages reference issue numbers |

---

## Phase 1: Project Type Detection

**Note:** `.delivery/config.md` must exist at this point (generated by Phase 0 wizard or
from a previous run). If it contains `project_type`, this phase is skipped and the config
value is used directly. If `project_type` is not set in config (user skipped that question
during wizard), detect from the user's input using the signal table below.

Auto-detect from the user's input using the following signal table:

| Type | Key Signals | Notes |
|------|-------------|-------|
| GREENFIELD | "new project", "from scratch", "brand new", "start fresh", "bootstrap" | No existing codebase referenced |
| FEATURE | "add feature", "enhance", "extend", "new capability", "integrate" | References existing system or codebase |
| BUG_FIX | "fix", "bug", "broken", "error", "crash", "regression", "not working" | Error/defect language dominant |
| GAME_DEV | "game", "Godot", "Unity", "gameplay", "NPC", "HUD", "GDScript" | MODIFIER -- always combines with another type |
| SPIKE | "spike", "POC", "prototype", "investigate", "feasibility", "explore" | Time-boxed, throwaway output |
| DOCS_ONLY | "documentation", "docs only", "write docs", "user guide", "runbook" | No code changes described |

### Detection Rules

- GAME_DEV is a modifier, never standalone. It combines with a base type:
  GAME_DEV+GREENFIELD, GAME_DEV+FEATURE, GAME_DEV+BUG_FIX.
  If GAME_DEV signals are present but no base type is clear, default base is GREENFIELD.
- BUG_FIX takes precedence when error/defect language is the dominant signal.
- Existing codebase context defaults to FEATURE when otherwise ambiguous.
- SPIKE vs FEATURE: concrete deliverable with production intent is FEATURE, even if
  "explore" is used. SPIKE implies throwaway or time-boxed output.
- DOCS_ONLY is strict: if any code changes are described, reclassify as the
  appropriate type with documentation as a deliverable.
- If ambiguous after applying these rules, ask the user before proceeding.

See `references/project-types.md` for the full detection matrix with confidence
boosters, confidence reducers, and disambiguation logic.

### Declaration

Before proceeding to pipeline execution, declare the detected type:

> Project Type: [TYPE] | Stages: [list of active stages] | Checkpoints: [N]

---

## Phase 2: Memory Retrieval

Memory uses a **tiered chunked system** — read only what's needed, never everything.
See `references/memory-protocol.md` for the full architecture.

### At Pipeline Start (this phase)

1. Check if `.delivery/memory/index.md` exists in the current working directory.
2. If yes, read **only** `memory/index.md` (the routing index, ~50 lines max).
   This tells you:
   - **Stage health**: which stages have low first-try pass rates (flag for extra attention)
   - **Hot lessons**: top 5 most impactful lessons (inject into ALL agent prompts)
   - **Topic pointers**: which chunk files to read and when
3. If `index.md` references `topics/project-types.md`, read it and filter to the
   detected project type for type-specific lessons.
4. Do NOT read stage chunks yet — those are loaded per-stage in Phase 4 (Step 2).
5. If no memory directory exists, proceed without lessons. The first run establishes
   the baseline.

### What Gets Injected Into Every Agent Prompt

```
Lessons from past runs on this project (apply these):
- [Hot Lesson 1 — from index.md]
- [Hot Lesson 2 — from index.md]
- [Project type lesson — from topics/project-types.md if relevant]

Active decisions to respect:
- [Decision — from topics/team-decisions.md if loaded]
```

---

## Phase 3: Stage Routing

Based on the detected project type, determine which stages execute and at what depth.

### Stage Routing Matrix

| Stage | GREENFIELD | FEATURE | BUG_FIX | GAME_DEV+ | SPIKE | DOCS_ONLY |
|-------|-----------|---------|---------|-----------|-------|-----------|
| 1. Idea | full | full | full | full | full | full |
| 2. Refine | full | full | skip | full | skip | skip |
| 3. Design | full | full | skip | full+game | skip | skip |
| 4. Architect | full | light-or-skip | skip | full+game | full | skip |
| 5. Plan | full | full | light | full | skip | light |
| 6. Dev | full | full | full | full+game | full | full |
| 7. UAT | full | full | full | full | skip | full |

### Depth Definitions

- **Full**: All agents invoked, all collaboration patterns run, full quality gate with
  all severity levels, full team DoD validation, max 3 self-correction iterations.
- **Light**: Primary agent only, blocking criteria only, reduced DoD (primary + 1
  reviewer), max 2 self-correction iterations. No adversarial review or debate.
- **Skip**: Stage does not execute. Pipeline advances to the next active stage.
  Downstream stages receive whatever upstream artifacts are available.
- **Full+Game**: Everything in Full, plus game-specific augmentations (game UI review
  at Design, game architecture roles at Architect, engine skill at Dev, playtest
  scenarios at UAT).

For FEATURE at the Architect stage, apply Light if the feature involves new APIs, new
data models, external integrations, security-sensitive changes, or touches more than 3
modules. Apply Skip if the change is UI-only, contained within a single module, with no
new data models, no security implications, and no new external dependencies.

---

## Phase 4: Pipeline Execution Protocol

For each active stage (not skipped), execute this protocol in order:

### Step 1: Announce

Output a stage header with the stage number, name, and a brief statement of purpose:

```
## Stage [N]: [NAME]
Purpose: [one-line description of what this stage produces]
```

### Step 2: Load Stage Memory

Read the **stage-specific chunk** from `memory/stages/<stage>.md` (e.g., `memory/stages/refine.md`
for the Refine stage). This file contains lessons specific to this stage (~100 lines max).

Additionally, load relevant **topic chunks** based on context:
- If this stage has a **human checkpoint** → also read `memory/topics/human-preferences.md`
- If this stage involves **decisions** (Architect, Plan) → also read `memory/topics/team-decisions.md`
- If this stage's **first-try pass rate is <80%** (from index.md) → also read `memory/topics/gate-patterns.md`

**Total reads per stage: 1-3 chunk files, never more.**

Combine the stage lessons + hot lessons (from Phase 2) + any topic lessons into the
agent prompt context for this stage.

### Step 3: Load Stage Definition

Read the stage sub-flow from `references/pipeline-stages.md`. This defines the
specific agents to invoke, their task types, and the sub-flow sequence.

### Step 4: Invoke Primary Agent

Spawn the worker skill sub-agent using the Agent tool. Provide:
- The task description and task type
- Upstream artifacts from prior stages (context isolation -- only what this agent needs)
- Relevant memory lessons from past runs
- Any human feedback from prior checkpoints

### Step 5: Invoke Supporting Agents

If the stage runs at full depth, invoke additional worker sub-agents for supplementary
work (metrics, security review, test strategy, etc.). Merge their output into the
primary artifact or produce companion artifacts.

### Step 6: Run Collaboration Patterns

Execute the collaboration patterns designated for this stage. Patterns run in this
order when multiple apply:

1. Evaluator-Optimizer Loop -- baseline quality pass
2. Adversarial Review -- stress-test assumptions
3. Debate -- resolve contested decisions
4. Multi-Perspective Review Board -- multi-domain assessment
5. Consensus -- cross-team alignment

Decision Ownership Routing can trigger at ANY point when a domain-specific question
arises. It is a routing mechanism, not a sequenced pattern.

See `references/team-patterns.md` for the full protocol of each pattern.

### Step 7: Team DoD Validation

Run the Team Definition of Done protocol for this stage:
- Spawn DoD validator sub-agents (2-4 per stage, as defined in the stage definition)
- Each validator reviews the artifact from their role's perspective
- Each votes DONE or NOT_DONE with specific findings
- ALL validators must say DONE for the stage to complete
- If any vote NOT_DONE, trigger self-correction (see Section 7 below)
- Max 3 DoD validation rounds per stage
- If still NOT_DONE after 3 rounds, trigger dynamic escalation

See `references/quality-gates.md` for the full DoD protocol and gate criteria.

### Step 8: Write Artifact

Save the validated artifact to `.delivery/artifacts/[NN]-[name].md`. Write the file
before proceeding to the next stage. This ensures artifacts survive aborts.

### Step 8.5: Update Pipeline State

Write the current pipeline state to `.delivery/state.md` using atomic write (write to `state.tmp.md`, rename to `state.md`):
- Update `current_stage` to the NEXT stage number
- Add the just-completed stage to `stages_completed`
- Add the artifact file path to the `artifacts` map
- Update `last_updated` timestamp

This ensures state survives session loss. If the session dies after this point, the next session can resume from the next stage.

### Step 9: Check for Human Checkpoint

If this stage has a scheduled human checkpoint, present a summary of the artifact and
wait for the user to approve, request changes, or abort.

After checkpoint approval, also update `.delivery/state.md`:
- Add the checkpoint name to `human_checkpoints_passed`
- Update `last_updated` timestamp

### Step 10: Advance

Move to the next active stage in the routing matrix. Pass the artifact downstream.

---

## Stage Definitions

### Stage 1: Idea

**Runs for**: all project types (full depth)

**Purpose**: Capture and structure the raw idea into a brief that downstream stages
can work from.

**Primary agent**: Product Owner (product-delivery skill, task_type: user_story) for
complex or vague ideas. For simple, well-structured input, the orchestrator formats
the brief directly.

**Upstream artifacts**: none (this is the first stage).

**Collaboration patterns**: none. This is the initial capture stage.

**DoD validators**:
- Product Owner (product-delivery skill): completeness -- problem statement, target
  users, and goals are all present and specific.
- Architect (architect skill): feasibility signal -- is this buildable? Any obvious
  technical blockers?

**Self-correction note**: At the Idea stage, if the gate fails due to missing
information, prefer asking the user for clarification over self-correction. The input
is the user's idea -- the orchestrator should not invent details.

**Output**: `.delivery/artifacts/01-idea-brief.md`

**Human checkpoint**: none.

**Max self-correction**: 2 iterations.

---

### Stage 2: Refine

**Runs for**: GREENFIELD (full), FEATURE (full), GAME_DEV+ (full).
Skipped for: BUG_FIX, SPIKE, DOCS_ONLY.

**Purpose**: Transform the idea brief into a complete PRD with acceptance criteria,
success metrics, and validated requirements.

**Primary agent**: Product Owner (product-delivery skill, task_type: prd).
- Input: idea brief + relevant memory lessons.
- Output: draft PRD.

**Supporting agent**: Data Analyst (product-delivery skill, task_type: metrics_definition).
- Input: PRD goals section.
- Output: success metrics with targets and measurement approach.
- Merge metrics into the PRD.

**Upstream artifacts**: `01-idea-brief.md`.

**Collaboration patterns**:
1. Evaluator-Optimizer: QA Engineer (quality skill) evaluates PRD against Gate 2
   criteria. If failures, route feedback to PO for revision. Max 3 iterations.
2. Adversarial Review: Challenger questions requirements assumptions, identifies
   missing edge cases, rates confidence 1-5. If confidence <= 2, escalate to human
   immediately.

**DoD validators**:
- Product Owner (product-delivery skill): business value is clear, stories are
  valuable, scope is appropriate.
- Architect (architect skill): technically feasible, no obvious blockers, NFRs are
  realistic.
- QA Engineer (quality skill): requirements are testable, acceptance criteria are
  specific and measurable.

**Output**: `.delivery/artifacts/02-prd.md`

**Human checkpoint**: CHECKPOINT 1 -- present PRD summary for approval.
User can approve, request changes, or abort.

**Max self-correction**: 3 iterations.

**Game dev additions**: UX Designer also reviews for game UX patterns. Game-specific
NFRs added (FPS targets, input latency, platform requirements).

---

### Stage 3: Design

**Runs for**: GREENFIELD (full), FEATURE (full), GAME_DEV+ (full+game).
Skipped for: BUG_FIX, SPIKE, DOCS_ONLY.

**Purpose**: Create user experience design: user flows, wireframes, interaction
patterns, component specifications, and accessibility considerations.

**Primary agents**:
1. UX Designer (ui skill, task_type: user-flow).
   - Input: PRD user stories and personas.
   - Output: user flows for all key journeys.
2. UX Designer (ui skill, task_type: wireframe).
   - Input: user flows.
   - Output: wireframes for key screens.
3. UI Designer (ui skill, task_type: component-spec or design-system).
   - Input: wireframes.
   - Output: component specifications, design tokens.
4. UI Designer (ui skill, task_type: accessibility-review).
   - Input: wireframes + component specs.
   - Output: accessibility findings.

**Upstream artifacts**: `02-prd.md`.

**Collaboration patterns**:
1. Multi-Perspective Review Board:
   - Technical Reviewer (Architect skill): implementability.
   - Business Reviewer (Product Owner via product-delivery): requirement coverage.
   - Risk Reviewer (QA Engineer via quality): testability.
   - Any BLOCK must be resolved via Decision Ownership Routing before advancing.

**DoD validators**:
- UX Designer (ui skill): flows are complete, follow UX best practices, edge cases
  addressed (empty states, errors, first-time use).
- Product Owner (product-delivery skill): all PRD requirements have corresponding
  design elements.
- QA Engineer (quality skill): designs are testable with clear states and measurable
  outcomes.
- Architect (architect skill): designs are implementable, no impossible interactions
  or unrealistic technical assumptions.

**Output**: `.delivery/artifacts/03-ux-design.md`

**Human checkpoint**: none (combined with Architect checkpoint if both stages run).

**Max self-correction**: 3 iterations.

**Game dev additions**: Game UI Designer (ui skill) invoked for HUD, menu, inventory
UI patterns. Game-specific accessibility review (colorblind modes, subtitle systems,
input remapping).

---

### Stage 4: Architect

**Runs for**: GREENFIELD (full), significant FEATURE (light), GAME_DEV+ (full+game),
SPIKE (full).
Skipped for: BUG_FIX, DOCS_ONLY, simple FEATURE.

**Purpose**: Create technical architecture: system design, C4 model descriptions,
Architecture Decision Records, and technology decisions.

**Primary agent**: Architect (architect skill, task_type: design, role: solution).
- Input: PRD + UX design (if available) + memory lessons.
- Output: system architecture with C4 diagram descriptions.

**Supporting agents**:
- Security Architect (architect skill, task_type: security-design).
  - Input: system architecture.
  - Output: security review findings, threat model.
- Data Architect (architect skill, task_type: data-design) if data-intensive.
  - Input: system architecture + PRD data requirements.
  - Output: data model, data flow design.

**Upstream artifacts**: `02-prd.md`, `03-ux-design.md` (if Design stage ran).

**Collaboration patterns**:
1. Debate: For contested technical decisions (e.g., microservices vs monolith,
   framework selection, build vs buy).
   - Frame the choice with project constraints, NFRs, team context.
   - PRO agent argues Option A, CON agent argues Option B.
   - JUDGE (Enterprise Architect) decides with documented rationale.
   - Produce an ADR for each debate.
   - If DEADLOCK, escalate to human.
2. Evaluator-Optimizer: QA reviews for testability, DevOps reviews for deployability.
   Route findings back to Architect. Max 2 iterations.
3. Adversarial Review: Challenger questions architecture assumptions, failure modes,
   security posture. Rates confidence 1-5.

**DoD validators**:
- Architect (architect skill): design is sound, trade-offs documented, patterns are
  appropriate for the context.
- QA Engineer (quality skill): architecture supports testing (observability,
  component isolation, test environments).
- DevOps (operations skill): architecture is deployable (CI/CD compatible,
  environment strategy defined, scaling approach clear).
- Security (architect skill, role: security): security concerns addressed,
  authentication/authorization designed, data protection specified.

**Output**:
- `.delivery/artifacts/04-architecture.md`
- `.delivery/artifacts/04a-adrs/ADR-001.md` (one per major decision)

**Human checkpoint**: CHECKPOINT 2 -- present architecture summary for approval.

**Max self-correction**: 2 iterations.

**Game dev additions**: Game architecture roles invoked as relevant:
- Game Systems Architect (ECS, state machines, game loop).
- Level/World Designer (scene structure, streaming, persistence).
- Network/Multiplayer Architect (netcode, sync, lobbies) -- only if multiplayer.
- Graphics/Rendering Specialist (shaders, particles, performance) -- only if
  graphically intensive.
Performance budgets required (frame time, memory, bandwidth).

---

### Stage 5: Plan

**Runs for**: GREENFIELD (full), FEATURE (full), GAME_DEV+ (full),
BUG_FIX (light), DOCS_ONLY (light).
Skipped for: SPIKE.

**Purpose**: Create sprint plan with user stories, estimates, test strategy, and
deployment approach.

**Primary agents**:
1. Product Owner (product-delivery skill, task_type: user_story).
   - Input: PRD.
   - Output: detailed user stories with acceptance criteria.
2. Scrum Bag (product-delivery skill, task_type: sprint_planning).
   - Input: user stories + architecture constraints.
   - Output: sprint plan draft with capacity and sequencing.
3. QA Engineer (quality skill, task_type: test-strategy).
   - Input: PRD + architecture + user stories.
   - Output: test strategy (what to test, how, when).
4. DevOps (operations skill, task_type: deployment-strategy).
   - Input: architecture.
   - Output: deployment plan (how and when completed work ships).

**Upstream artifacts**: `02-prd.md`, `04-architecture.md` + `04a-adrs/` (if Architect
stage ran).

**Collaboration patterns**:
1. Consensus Protocol: SM, PO, QA, and DevOps independently analyze estimates, risks,
   and capacity. Then share positions, respond to disagreements, and converge. 2-3
   rounds as needed.
2. Adversarial Review: Challenger questions estimates, risk assessments, and capacity
   assumptions. Rates confidence 1-5.

**DoD validators**:
- Scrum Bag (product-delivery skill): process is sound, capacity is realistic,
  commitment does not exceed 80% of available capacity.
- Product Owner (product-delivery skill): scope is correct, stories are valuable and
  properly prioritized.
- QA Engineer (quality skill): test strategy covers critical paths, test approach is
  referenced for each story.
- DevOps (operations skill): deployment approach is viable, environment strategy is
  clear.

**Output**: `.delivery/artifacts/05-sprint-plan.md`

**Human checkpoint**: CHECKPOINT 3 -- present sprint plan for approval.

**Max self-correction**: 2 iterations.

**Light mode** (BUG_FIX, DOCS_ONLY):
- PO writes a single story for the fix or documentation task.
- SM produces a minimal plan (no full sprint plan).
- Skip consensus protocol and adversarial review.
- QA still validates testability.
- Reduced DoD: SM + QA only.

---

### Stage 6: Development

**Runs for**: all project types (full depth for all; full+game for GAME_DEV+).

**Purpose**: Implement the code, write tests, and produce development documentation.

**Primary agent**: Developer (developer skill, task_type: write).
- Input: user story + acceptance criteria + architecture constraints.
- Output: implementation code.

**Supporting agent**: QA Engineer (quality skill) for test writing and code review.

**Upstream artifacts**: `02-prd.md`, `04-architecture.md` (if available),
`05-sprint-plan.md` (if available), `03-ux-design.md` (if available).

**Execution**: For each story in the sprint plan (or the single story for BUG_FIX):

1. Invoke Developer with the story, acceptance criteria, and architecture constraints.
2. Evaluator-Optimizer Loop: QA Engineer reviews code against acceptance criteria and
   coding standards. Route feedback to Developer. Max 3 iterations per story.
3. Decision Ownership Routing for mid-story issues:
   - Scope questions -> Product Owner (product-delivery skill).
   - Technical questions -> Architect (architect skill).
   - Quality questions -> QA Engineer (quality skill).
4. Technical Writer (operations skill, task_type: api-docs or runbook) if applicable.
5. Team DoD Validation per story.

**Collaboration patterns**:
1. Evaluator-Optimizer per story (code -> QA review -> fix cycle).
2. Decision Ownership Routing as needed.

**DoD validators** (per story):
- Developer (developer skill): code is clean, follows language and framework best
  practices, no hardcoded secrets. Must include "Verification Status" in output.
- QA Engineer (quality skill): tests pass, coverage is adequate, no critical issues.
  If developer's Verification Status includes "Requires runtime validation" items,
  return **CODE_COMPLETE** instead of DONE (see the quality skill's `references/empirical-validation.md`).
- Architect (architect skill): implementation conforms to architecture decisions, no
  architectural drift.
- Technical Writer (operations skill): inline documentation present for non-obvious
  logic, API docs if applicable.
- Defect Prevention Gate (godot skill, references/defect-prevention.md): for GAME_DEV
  projects, run the defect prevention checklist against all modified .gd and .tscn files.
  Structural checklist failures (mouse_filter missing, convention violations) are NOT_DONE.
  Empirical checklist items that cannot be verified without the Godot editor (scene
  instancing test, visual render check) produce CODE_COMPLETE with items carried to Stage 7.

**DoD status options**: DONE, CODE_COMPLETE, or NOT_DONE.
- **CODE_COMPLETE** means: code passes all structural/inspectable criteria, but empirical
  validation is pending. The story advances, and pending validations carry forward to
  Stage 7 (UAT) as mandatory test cases.

**Output**:
- Code files in the project codebase.
- `.delivery/artifacts/06-dev-notes.md` (summary of implementation decisions, known
  issues, deviations from plan, and any CODE_COMPLETE stories with their pending
  empirical validations).

**Human checkpoint**: none.

**Max self-correction**: 3 iterations per story.

**Milestone testing** (all project types): After each sprint's stories pass DoD, run a
milestone validation session using the quality skill's `references/milestone-testing.md`.
Protocol is project-type-specific (Web: responsive/a11y, API: auth/CRUD/errors, Enterprise:
multi-tenant/RBAC, Mobile: offline/permissions, CLI: pipes/exit codes). Uses role-specific
checklists and cross-feature interaction questions. Findings classified and routed.

**Game dev additions**: Godot skill (or relevant engine skill) invoked alongside
Developer for engine-specific work. Game-specific testing:
- **Headless validation**: After each story, run `godot --headless --path <project> --quit` as part of the evaluator-optimizer loop. Any new ERROR lines trigger a correction cycle.
- **Empirical AC classification**: Classify each acceptance criterion as "structural" (verifiable by code inspection) or "empirical" (requires runtime). If empirical ACs exist and no validation tool was used, mark story as "code-complete, pending validation" rather than "done".
- **Performance profiling**: Profile against frame budgets, memory limits, and draw call targets.
- **Playtest scenarios**: Game feel, difficulty curve, progression balance, and player experience.
- **Milestone playtest checkpoint**: After each sprint delivering playable features, run a
  structured playtest (15 min) using the quality skill's `references/exploratory-testing.md`
  milestone protocol. Role-specific checklists (PO: gameplay/design, QA: cross-story
  interactions, Dev: performance, Architect: system interactions). Classify findings as
  Bug/Balance/UX/Narrative/Performance/Spec Gap. Bugs → `.delivery/defects/`, rest → backlog.

---

### Stage 7: UAT

**Runs for**: GREENFIELD (full), FEATURE (full), BUG_FIX (full), GAME_DEV+ (full),
DOCS_ONLY (full).
Skipped for: SPIKE.

**Purpose**: Execute user acceptance testing, prepare release artifacts, and get
final approval for delivery.

**Primary agents**:
1. QA Engineer (quality skill, task_type: test-plan).
   - Input: PRD acceptance criteria + developed features + **pending empirical
     validations from Stage 6** (CODE_COMPLETE stories with their runtime
     verification requirements).
   - Output: UAT test plan with test cases. Pending empirical validations from
     Stage 6 MUST be included as mandatory UAT test cases.
2. QA Engineer (quality skill, task_type: test-cases).
   - Input: test plan (including empirical validation test cases).
   - Output: detailed test cases with expected results.
3. DevOps (operations skill, task_type: release-plan + rollback-procedure).
   - Input: architecture + deployment strategy.
   - Output: release plan with rollback procedure.
4. Technical Writer (operations skill, task_type: release-notes + user-guide).
   - Input: PRD + dev notes + features implemented.
   - Output: release notes, user guide updates.

**Upstream artifacts**: all prior artifacts (PRD, architecture, sprint plan, UX
design, dev notes).

**Collaboration patterns**:
1. Multi-Perspective Review Board (go/no-go recommendation):
   - QA (quality skill): test results, defect status.
   - DevOps (operations skill): release readiness, rollback readiness.
   - Technical Writer (operations skill): documentation completeness.
   - Any BLOCK must be resolved before proceeding to human checkpoint.

**DoD validators**:
- QA Engineer (quality skill): all tests pass (100% critical, 90% overall), no
  critical defects, test coverage complete.
- DevOps (operations skill): deployment plan complete, rollback procedure documented
  and validated.
- Product Owner (product-delivery skill): delivered features match business
  expectations, acceptance criteria met.
- Technical Writer (operations skill): release notes, user guides, and API docs are
  complete and accurate.

**Output**:
- `.delivery/artifacts/07-uat-report.md`
- `.delivery/artifacts/07a-release-plan.md`
- `.delivery/artifacts/07b-documentation.md`

**Human checkpoint**: CHECKPOINT 4 -- present UAT results, release plan, and
documentation for accept or reject. If any stories were CODE_COMPLETE from Stage 6,
explicitly show the **pending empirical validations** that need runtime verification,
with recommended validation approaches per technology (from
the quality skill's `references/empirical-validation.md`). The user must confirm these have been
validated (or accept the risk) before the pipeline marks them DONE.

**Max self-correction**: 2 iterations.

**Game dev additions**: Game-specific test patterns applied:
- Playtest scenarios (game feel, difficulty curve, progression balance).
- Performance budgets validated (frame time targets, memory limits, draw call budgets).
- Input scheme validation (keyboard, controller, touch as applicable).
- Platform-specific checks (if targeting multiple platforms).

**Post-acceptance**: After human accepts, proceed to memory update (see Phase 5 below).

---

## Team Definition of Done Protocol

DoD validation is the final checkpoint before a stage advances. It runs AFTER all
collaboration patterns have completed. DoD is NON-NEGOTIABLE -- no stage advances
without ALL validators saying DONE (unless the human overrides via escalation).

### Execution Steps

1. **Identify validators.** Each stage has named validators defined in the stage
   definition above and detailed in `references/quality-gates.md`.

2. **Spawn validator sub-agents.** Each validator is spawned as a sub-agent with the
   relevant skill and a role-specific review prompt:

   ```
   You are validating this artifact as the [ROLE] on the delivery team.

   Review the artifact strictly from your perspective. Apply these criteria:

   [ROLE-SPECIFIC CRITERIA from quality-gates.md]

   Artifact:
   ---
   [ARTIFACT CONTENT]
   ---

   Respond with:
   - DONE or NOT_DONE
   - If NOT_DONE, list each failing criterion with:
     - What specifically fails (quote the relevant section)
     - Why it matters (impact if shipped as-is)
     - Actionable suggestion to fix it (specific enough to implement)
   ```

3. **Evaluate votes.** ALL validators must return DONE for the stage to complete.

4. **Self-correction on NOT_DONE.** If any validator returns NOT_DONE:
   - Aggregate ALL findings from all validators (include DONE results for context).
   - Construct targeted feedback listing each failing criterion with actionable fixes.
   - Re-invoke the primary agent with: original context + current artifact + feedback.
   - The primary agent must address every finding explicitly without regressing on
     criteria that already passed.
   - Re-run ALL validators (not just the ones that failed), because revisions can
     introduce regressions.

5. **Track iteration count.** Maximum 3 DoD validation rounds per stage (or the
   stage-specific override from quality-gates.md).

6. **Escalate on exhaustion.** After 3 rounds with unresolved findings, trigger
   dynamic escalation to the human with all attempts shown.

---

## Dynamic Escalation Protocol

Escalation is not limited to scheduled human checkpoints. The orchestrator monitors
for escalation conditions continuously throughout pipeline execution.

### Escalation Triggers

| Trigger | Condition |
|---------|-----------|
| Repeated DoD failure | Same criterion fails across 3 consecutive validation cycles |
| Low adversarial confidence | Challenger agent rates artifact confidence at 2/5 or below |
| Decision deadlock | Decision Owner cannot resolve a routed issue (insufficient information, equal trade-offs) |
| Debate stalemate | Judge agent returns DEADLOCK (arguments equally compelling, no clear winner) |
| No correction progress | Self-correction iteration produces no meaningful change to failing criteria |
| Cross-cutting conflict | Two roles produce contradictory NOT_DONE findings that cannot be reconciled |

### Escalation Format

Every escalation presented to the human follows this structure:

```
## Escalation: [Stage Name] -- [Brief Issue Description]

**Issue**: [What went wrong, stated clearly in 1-2 sentences]

**Attempts**: [What was tried and how many iterations occurred]

**Current state**: [Where the artifact stands -- what passes, what still fails]

**Findings**:
[Aggregated validator/reviewer feedback from the most recent cycle]

**Options**:
1. **Provide guidance**: [Describe what kind of input would unblock progress]
2. **Override**: Proceed despite the issue (risk: [state the specific risk])
3. **Redirect**: Try a different approach (suggestion: [if applicable])
4. **Abort**: Halt pipeline execution, preserve all artifacts produced so far
```

The user responds with any option. The pipeline resumes accordingly:
- **Provide guidance**: Inject the guidance as context and re-attempt.
- **Override**: Record the override decision and advance. Carry the risk forward as
  context for downstream stages.
- **Redirect**: Re-invoke the stage with the new approach.
- **Abort**: Halt immediately. Write all artifacts produced so far. Write memory file.

---

## Cross-Stage Artifact Flow

Each stage receives upstream artifacts from prior stages. The orchestrator selects the
relevant subset for each worker sub-agent (context isolation -- agents do not see the
full pipeline state).

| Stage | Receives From Upstream |
|-------|------------------------|
| Idea | (none -- first stage) |
| Refine | idea brief |
| Design | PRD |
| Architect | PRD + UX design (if Design stage ran) |
| Plan | PRD + architecture + ADRs (if Architect ran) |
| Dev | PRD + architecture + sprint plan + UX design (all available) |
| UAT | all prior artifacts |

Worker sub-agents receive ONLY what they need for their specific task. For example,
a QA Engineer validating a PRD receives the PRD and the gate criteria, but not the
idea brief or architecture docs. The orchestrator is responsible for selecting the
correct subset.

---

## Memory and Self-Learning

After pipeline completion (or abort), the orchestrator captures lessons learned.

### Pipeline State Management

**At pipeline start** (after Phase 0 completes, before Stage 1):
Write initial state file to `.delivery/state.md` with atomic write:
- `pipeline_id`: `run-YYYY-MM-DD-<4char-random>`
- `status`: `in_progress`
- `current_stage`: 1
- `stages_completed`: []
- `config_snapshot`: entire config.md YAML frontmatter
- `artifacts`: {}

**At pipeline completion** (after UAT accepted):
- Set `status: completed` in state file
- Delete `.delivery/state.md` (artifacts and memory persist independently)

**At pipeline abort**:
- Set `status: aborted` in state file
- Preserve `.delivery/state.md` for potential resume
- Record `abort_stage` in the state file

### Post-Pipeline Protocol

1. **Run retrospective.** Invoke Scrum Bag (product-delivery skill, task_type:
   retrospective) to capture what went well, what did not, and improvement actions.

2. **Write run archive.** Save full run log to `memory/archive/run-YYYY-MM-DD-<id>.md`
   with gate results, checkpoint deltas, adversarial insights, DoD patterns, decisions,
   and debate outcomes.

3. **Extract and route lessons to chunks.** For each lesson learned:
   - Stage-specific lesson → `memory/stages/<stage>.md`
   - Human preference learned → `memory/topics/human-preferences.md`
   - Decision made → `memory/topics/team-decisions.md`
   - Gate pattern observed → `memory/topics/gate-patterns.md`
   - Project type insight → `memory/topics/project-types.md`

4. **Deduplicate and validate.** When adding to a chunk:
   - If similar lesson exists: increment `validated` count, update `last` run.
   - If contradicts existing: note contradiction, remove after 3 consecutive contradictions.
   - If chunk exceeds 100 lines: prune least-validated, oldest entries.

5. **Rebuild routing index.** Rebuild `memory/index.md`:
   - Recalculate stage health stats from last 5 runs.
   - Update hot lessons (top 5 by validation count).
   - Update topic file pointers.

6. **Archive maintenance.** Max 20 run files in archive. Delete oldest first, ensuring
   all lessons are captured in chunks before deletion.

7. **Defect review.** If defects were found during this pipeline run:
   - Count defects and calculate defects/story rate
   - Categorize by root cause
   - Compare to history (is the rate improving?)
   - For systemic patterns (2+ occurrences or new categories): check if covered by existing skill references
   - If not covered → draft plugin improvement PR with `[DEFECT-FIX]` prefix and `defect-prevention` label
   - Update `.delivery/defects/index.md` with current data
   - See `references/defect-tracking.md` for the full protocol

See `references/memory-protocol.md` for the full tiered memory architecture, chunk
formats, size limits, pruning rules, and decay protocol.

---

## Guardrails

These guardrails prevent runaway execution and ensure predictable behavior:

- **Max self-correction iterations per stage**: 3 (or stage-specific override).
  Every correction loop has a counter. When exhausted, escalate.
- **Max DoD validation rounds per stage**: 3 (or stage-specific override).
  After 3 rounds with unresolved findings, escalate.
- **No infinite loops.** Every loop in the pipeline has a bounded counter. The
  orchestrator tracks iteration counts and halts at limits.
- **Write before advancing.** Artifacts are written to `.delivery/artifacts/` before
  the pipeline advances to the next stage. This ensures artifacts survive aborts.
- **Context isolation.** Worker skills receive only the upstream artifacts relevant to
  their task. They do not see the full pipeline state or other workers' intermediate
  outputs.
- **No skipping DoD.** Every active stage must pass team DoD validation before
  advancing. There is no bypass except human override via escalation.
- **No pipeline bypass.** ALL story implementation MUST go through the delivery-flow
  pipeline. Never spawn developer/godot agents directly for story work. The PreToolUse
  hook enforces this by detecting Skill invocations outside pipeline context. Developer
  and godot skills also warn when no `.delivery/config.md` exists. The only exception
  is quick one-off fixes explicitly approved by the user (not story implementations).
- **Test cases per story are mandatory.** Stage 5 (Plan) produces test cases alongside
  every user story — not as a separate QA step that can be skipped. Every story artifact
  includes: story + acceptance criteria + test cases.
- **Retrospective is mandatory.** The post-pipeline protocol (retrospective + memory write
  + defect review) MUST run after every pipeline completion or abort. The Stop hook
  enforces this — it blocks session end if pipeline work occurred but the retrospective
  was not completed. Never skip the retrospective for velocity.
- **Preserve on abort.** If the pipeline is aborted at any point, all artifacts
  produced so far are preserved in `.delivery/artifacts/`. The memory file is written
  even for aborted runs (with `completed: false` and `abort_stage` recorded).
- **State persistence after every stage.** Pipeline state is written to `.delivery/state.md`
  after every stage gate passes using atomic write (temp file → rename). If a session
  dies, the next session can resume from the last completed stage.
- **Orchestrator does not produce domain artifacts.** The orchestrator manages flow,
  routing, and validation. All domain work is delegated to worker skills.

---

## User Commands

| Command | Action |
|---------|--------|
| `setup` | Run (or re-run) the setup wizard to configure the delivery pipeline |
| `start` | Begin delivery pipeline (runs wizard first if no config exists) |
| `status` | Show current pipeline state (stage, progress, issues) |
| `skip` | Skip current stage (requires confirmation, records reason) |
| `back` | Return to previous stage for rework |
| `approve` | Approve artifact at human checkpoint |
| `request-changes [feedback]` | Request changes at human checkpoint with specific feedback |
| `abort` | Halt pipeline, preserve all artifacts, write memory file |
| `type <TYPE>` | Override detected project type (e.g., `type FEATURE`) |
| `memory` | Show lessons from past runs relevant to current project |
| `escalate` | Manually trigger escalation for current stage |
| `resume` | Resume a previously interrupted pipeline run |
| `defect-review` | Run defect analysis and check for plugin improvement PR candidates |

---

## References

All reference files are located in the `references/` directory relative to this skill.
They are loaded on demand during pipeline execution -- not pre-loaded into context.

| File | Purpose |
|------|---------|
| `references/pipeline-stages.md` | Detailed sub-flow for each of the 7 stages: entry conditions, agent invocations, task types, output artifact templates |
| `references/project-types.md` | Full detection matrix for all 6 project types: signals, confidence boosters/reducers, disambiguation rules, stage routing matrix, depth definitions |
| `references/quality-gates.md` | Gate criteria for all 7 stages with severity levels (blocking, warning, suggestion), DoD validator assignments, self-correction protocol, escalation rules |
| `references/team-patterns.md` | All 6 collaboration patterns with protocols and prompt templates: Evaluator-Optimizer, Adversarial Review, Multi-Perspective Review Board, Decision Ownership Routing, Debate, Consensus |
| `references/memory-protocol.md` | Tiered chunked memory system: routing index (Tier 1), stage + topic chunks (Tier 2), run archive (Tier 3), retrieval protocol (2-3 reads per stage), chunk size limits, pruning rules, decay protocol |
| `references/setup-wizard.md` | Setup wizard protocol: scan detection matrix, 10 wizard questions with smart options, config file format, directory initialization, pipeline integration |
| `references/config-schema.md` | Config schema: all keys with types, defaults, valid values, consuming skills, versioning, extension protocol, migration |
| `references/defect-tracking.md` | Defect tracking protocol: registry format, classification rules, plugin improvement PR triggers, PO defect rate tracking |
| `references/git-integration.md` | Git integration: branching strategies, conventional commits, pipeline integration points |
| `references/github-integration.md` | GitHub integration: issue creation, PR creation, commit linking, gh CLI usage |
| `references/getting-started.md` | Getting started guide: quick-start wizard, skill map, first pipeline walkthrough, command cheat sheet |
