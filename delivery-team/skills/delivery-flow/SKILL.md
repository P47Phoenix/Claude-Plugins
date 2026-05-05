---
name: delivery-flow
description: Delivery pipeline orchestrator that coordinates the full delivery team through 7 stages (Idea, Refine, Design, Architect, Plan, Development, UAT) with auto-detection of project type, self-correction loops, adversarial review, multi-perspective review boards, team Definition of Done validation, dynamic escalation, debate for contested decisions, consensus for cross-team alignment, and self-learning memory. Triggers on phrases like "delivery pipeline", "full delivery", "end-to-end delivery", "start project", "new project", "greenfield", "new feature", "bug fix", "spike", "POC", "proof of concept", "game project", "delivery flow", "run pipeline", "start pipeline", "deliver this", "build and ship", "start delivery", "kick off project".
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7
model: sonnet
extended_thinking: false
last_audited: 2026-04-22
pattern_library_version: 4-7-1
tier: A
---

# Delivery Flow Orchestrator

## Design Principle: Team-Based Delivery with Self-Correction and Learning

This skill is the ORCHESTRATOR. It coordinates the delivery team through a structured
pipeline but NEVER produces domain artifacts directly. All domain work -- requirements,
designs, architecture, code, tests, plans -- is delegated to worker skills that operate
as sub-agents with isolated context.

### Core Principles

1. **Delegation, not execution (Prime Directive).** The orchestrator manages flow,
   routing, and validation. Worker skills (product-delivery, developer, godot,
   architect, quality, operations, ui) produce ALL domain artifacts. Workers are
   invoked as sub-agents using the Agent tool.

   **The orchestrator NEVER writes domain content.** This is non-negotiable.
   Explicit anti-patterns (any of these is a Prime Directive violation):
   - Writing a PRD, design, architecture, code, test plan, review, or analysis
     with Write or Edit because "it's simple"
   - Drafting a short artifact inline and saving it to skip an Agent dispatch
   - Writing a compound prompt that asks one sub-agent to act as multiple roles
     (see "One Role = One Sub-Agent" below)
   - Collapsing two adversarial loops into one by pasting prior findings into
     the next reviewer's prompt
   - Forwarding artifact content (not paths) between sub-agents through the
     orchestrator

   The orchestrator's ONLY write paths are `.delivery/state.md`,
   `.delivery/state.tmp.md`, `.delivery/config.yml`, `.delivery/memory/**`, and
   `stage-summary.md` files under each stage namespace. Everything else is
   produced by a dispatched sub-agent.

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

> **Model awareness (Opus 4.7):** Under F-08, the 4.7 runtime dispatches fewer
> sub-agents by default unless explicitly steered. This elevates "One Role = One
> Sub-Agent" (see Phase 4) from a stylistic convention to a **behaviourally
> load-bearing** gate. Role-count under-dispatch is the highest-confidence
> regression mode for this pipeline on 4.7 — treat the principle as a hard
> invariant, not a style preference.

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
   - **Config divergence check**: diff `config_snapshot` against current `.delivery/config.yml`. If different, warn: "Config has changed since this pipeline started. Resume uses the original config. Choose Restart to apply new config."
   - Offer the user: **Resume** / **Restart** / **Abandon**
   - Resume: load config from snapshot, skip completed stages, start at current_stage.
   - Restart: move state file to `.delivery/state-archive/state-<timestamp>.md` (cap at 5, delete oldest), start fresh.
   - Abandon: delete state file, no pipeline runs.
3. **If state exists with `status: aborted`**:
   - Announce: `> Aborted pipeline found from [date], stopped at Stage [N]. Artifacts from stages [list] are preserved.`
   - Offer: Resume / Restart / Abandon (same as above).
4. **If state exists with `status: completed`**: ignore (previous run finished normally).
5. **If no state file exists**: proceed to config check (normal flow).

1. **Check for `.delivery/config.yml`** in the current working directory.
   If `.delivery/config.yml` is not found, also check for `.delivery/config.md` (legacy format). If found, read it and announce: "Legacy config.md found. Run setup to migrate to config.yml."
2. **If config exists and is fresh** (< 30 days old):
   - Read the YAML configuration to load all project settings.
   - **Version check**: Compare `config_version` to the current schema version in
     `references/config-schema.md`. If the config is older (or has no `config_version`),
     apply defaults for any missing keys from the schema and announce:
     `> Config upgraded from v[old] to v[current]. New settings applied with defaults: [list]`
     Offer the user `setup` to configure new settings interactively.
   - **v2.6 → v2.7 migration rule**: When loading a v2.6 config (or any config that
     contains a top-level `project_type` key regardless of version), strip the
     `project_type` key in-memory and treat `config_version` as `2.7` for this run.
     Announce: `> Migrated config v2.6 → v2.7: removed project_type key (now detected per run).`
     The orchestrator applies this in-memory only — it does NOT auto-write over the
     user's `.delivery/config.yml`. Recommend the user re-run `setup` to persist the
     normalized v2.7 shape cleanly.
   - Announce: `> Config loaded from .delivery/config.yml (v[version], created [date])`
   - Apply settings: project type, tech stack, checkpoints, collaboration patterns, DoD validators, iteration limits, compliance requirements, persona config, alias theme.
   - **Load alias theme**: Read `aliases.theme` from config (default: `business`). If the
     value is not `business` (which uses default professional names and has no personality
     injection), load the theme file:
     1. Check `references/aliases/{theme}.yml` (built-in themes).
     2. If not found, check `{aliases.custom_path}/{theme}.yml` (custom themes, default path: `.delivery/aliases/`).
     3. If neither exists, warn: `> Alias theme '{theme}' not found. Falling back to business (no personality injection).` and set theme to `business`.
     4. If found, parse the YAML and store the `roles` mapping and `personality_strength` for use in Phase 4 Step 4. Announce: `> Alias theme loaded: {display_name} ({personality_strength} personality)`
   - For any key missing from the config, use the default from `references/config-schema.md`.
   - **Phase 1 (type detection) ALWAYS runs** from the current user request. Config no
     longer pins the project type. If the loaded config contains a bare legacy
     `project_type` key (v2.6 or earlier), tolerantly parse and **warn-and-drop**
     it: log a deprecation banner (`> Deprecated: bare project_type is ignored in
     v2.7. Use routing.force_type if you need an intentional pin.`) and continue.
     If `routing.force_type` is set in config, Phase 1 detection still runs and is
     logged, but routing uses the pin and a banner announces the override.
   - Proceed to Phase 1 (always) then Phase 2 (Memory Retrieval).

3. **If config exists but is stale** (> 30 days old):
   - Announce: `> Existing config found from [date] — it may be outdated.`
   - Offer options: Use as-is, Re-run wizard to update, Proceed with defaults.

4. **If no config exists**:
   - **STOP. Do NOT proceed to Phase 1.** The setup wizard MUST run before the pipeline can execute.
   - Run the setup wizard. Reference `references/setup-wizard.md` for the full protocol.
   - The wizard has 4 phases:
     - **Scan**: Auto-detect project state (languages, frameworks, CI/CD, git history, existing `.delivery/`)
     - **Present & Ask**: For each configuration topic, show what was detected and present 3-5 smart options. Each question supports single-select or multi-select as appropriate, plus Custom, Let's discuss, and Skip.
     - **Generate Config**: Write `.delivery/config.yml` as a pure YAML configuration file.
     - **Initialize Directory**: Create `.delivery/artifacts/`, `.delivery/memory/`, `.delivery/README.md`.
     - **Install Enforcement Hook**: If `enforcement.source_code_hook` is true (default), install a PreToolUse hook in the project's `.claude/settings.json` that warns when source code is edited outside an active delivery pipeline. See `references/setup-wizard.md` for the hook definition and installation process.
   - After the wizard completes, `.delivery/config.yml` MUST exist before proceeding.
   - If the user wants to skip the wizard entirely, they must explicitly say "skip setup" or "use defaults" — in which case, generate a minimal `.delivery/config.yml` with auto-detected defaults and proceed. The pipeline NEVER runs without a config file.

5. **User can re-run the wizard at any time** with the `setup` command.

### Quick-Start Mode

If the user says "quick start", "quick setup", or "just get started", run a 2-question wizard instead of the full 9+ question version:

1. **What language/framework?** -- auto-detect from codebase, user confirms
2. **How strict?** -- Prototype (minimal) / Standard (balanced) / Strict (full)

> **Note**: Project type is detected per run in Phase 1, not configured. Use `routing.force_type` if you want to pin it.

All other settings use smart defaults from `references/config-schema.md` based on the detected project type and strictness level. Generate `.delivery/config.yml` and proceed.

See `references/getting-started.md` for the complete quick-start walkthrough, skill map, and command cheat sheet.

### Config Settings Applied to Pipeline

When a config is loaded, these settings override defaults:

| Config Key | Pipeline Behavior |
|-----------|-------------------|
| `routing.force_type` | Optional opt-in pin. Phase 1 detection still runs, but routing uses the pin. Banner announces the override. Valid values: same enum as Phase 1 detection. Default: null. |
| `pipeline.enforce_self_write_block` | When true (default on fresh v2.7 configs), activates `enforce_pipeline_scope.py` soft-deny for orchestrator-origin writes to `.delivery/artifacts/**`. False for tolerantly-parsed v2.6 configs. |
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
| `notifications.channels` | Which notification channels to use (console, file, slack, github-discussion) |
| `notifications.events` | Which events trigger notifications (complete, abort, escalation, checkpoint, defect-threshold) |
| `pipeline.scope` | What file types go through the pipeline (code-only / all / custom) |
| `pipeline.scope_include` | Custom glob patterns for pipeline scope (when scope=custom) |
| `pipeline.scope_exclude` | Patterns always excluded from pipeline enforcement |
| `aliases.theme` | Which alias theme to load for agent personality injection (default: business) |
| `aliases.custom_path` | Directory for custom theme files (default: `.delivery/aliases/`) |

---

## Phase 1: Project Type Detection

**Note:** `.delivery/config.yml` must exist at this point (generated by Phase 0 wizard or
from a previous run). **Phase 1 runs on EVERY pipeline invocation.** The project type is
a runtime routing decision, not a config setting — even if a legacy `project_type` key
exists in the config, it is ignored for routing (warn-and-drop, see Phase 0).

If the config sets `routing.force_type`, detection STILL runs and is logged, but routing
uses the pin and a banner announces the override. Detection from the user's current
request uses the signal table below.

Auto-detect from the user's input using the following signal table:

| Type | Key Signals | Notes |
|------|-------------|-------|
| GREENFIELD | "new project", "from scratch", "brand new", "start fresh", "bootstrap" | No existing codebase referenced |
| FEATURE | "add feature", "enhance", "extend", "new capability", "integrate" | References existing system or codebase |
| BUG_FIX | "fix", "bug", "broken", "error", "crash", "regression", "not working" | Error/defect language dominant |
| DESIGN | "design session", "design-only", "architecture proposal", "no code yet", "exploring design", "design workshop" | Design work without implementation |
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

| Stage | GREENFIELD | FEATURE | BUG_FIX | DESIGN | GAME_DEV+ | SPIKE | DOCS_ONLY |
|-------|-----------|---------|---------|--------|-----------|-------|-----------|
| 1. Idea | full | full | full | full | full | full | full |
| 2. Refine | full | full | skip | full | full | skip | skip |
| 3. Design | full | full | skip | full | full+game | skip | skip |
| 4. Architect | full | light-or-skip | skip | full | full+game | full | skip |
| 5. Plan | full | full | light | skip | full | skip | light |
| 6. Dev | full | full | full | skip | full+game | full | full |
| 7. UAT | full | full | full | skip | full | skip | full |

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

**CRITICAL**: Light and Skip are DIFFERENT. Light stages execute with reduced ceremony.
Skip stages do not execute at all. Never conflate them. If the routing matrix says
"light" for a stage, that stage MUST run and MUST produce an artifact.

---

## Phase 4: Pipeline Execution Protocol

> **SELF-RECOVERY**: If you find yourself idle after agents have returned results, re-read `.delivery/state.md` to determine `current_stage` and immediately resume the pipeline protocol at the appropriate step. Do not wait for user input.

### One Role = One Sub-Agent (Prime Directive Corollary)

Every reviewer, challenger, validator, debater, or evaluator role is dispatched as a
**separate** Agent tool call. One role = one sub-agent invocation. Never collapse
multiple roles into a single compound prompt.

- A review board of 3 reviewers = 3 Agent calls (dispatched in parallel).
- A DoD with 4 validators = 4 Agent calls (dispatched in parallel).
- A debate = PRO Agent call + CON Agent call (parallel) + JUDGE Agent call (sequential).
- An adversarial loop of N iterations = N fresh Agent calls for the reviewer (each
  iteration is its own dispatch with no prior-loop context).

Violations (to avoid):
- "You are Reviewer A. Also act as Reviewer B." (compound multi-role prompt)
- Listing several `ROLE:` declarations in one Agent prompt.
- Asking a single sub-agent to produce both the artifact AND review it.
- Pasting prior-loop findings into a new reviewer's prompt to "save a call".

The agent prompt audit hook (`audit_agent_prompt.py`) warns on compound-role patterns.

> **Model awareness (Opus 4.7):** On 4.7, silent sub-agent fusion is the
> highest-confidence regression mode (F-08 — reduced default dispatch breadth).
> The stylistic convention above is now a behavioural gate: the count of
> dispatched roles at each DoD checkpoint MUST equal the length of
> `dod_validators.<stage>` in `.delivery/config.yml`. A short-count dispatch is
> not a style miss; it is a Prime Directive violation under 4.7 semantics.

### Two-Channel Communication

The orchestrator uses two communication channels:

- **Signal channel**: STATUS, file paths, summaries (<200 chars) -- flows through orchestrator for routing decisions.
- **Artifact channel**: file contents -- NEVER flows through orchestrator. Sub-agents write files to disk. Downstream agents read files by path. The orchestrator passes paths, not content.

**The rule**: If information is longer than 200 characters, it belongs in a file. The orchestrator passes the file path. The downstream agent reads the file. The orchestrator NEVER reads an artifact and pastes its content into another agent's prompt.

### Theme-Gated Reporting Protocol

When `aliases.theme` is set to a non-business theme (e.g., `lotr`, `star-wars`), the orchestrator adapts its **user-facing chat output** to reflect the active theme's personality. When `aliases.theme` is `business` or unset, all orchestrator output uses the current neutral format with zero behavior change.

Theme surfacing applies to three output slots:

1. **Stage Announcements** (Step 1): Reference the agent's character name from the theme's `roles` map and carry thematic voice in phrasing. If the dispatched role has no entry in the theme's `roles` map (partial theme), fall back to the neutral announcement format for that stage only.

2. **Human Checkpoint Summaries** (Step 9): Include one brief quoted line (max 280 characters) from the primary agent's artifact that demonstrates themed voice. The orchestrator reads the artifact ONLY to select a representative quote -- this is user-facing output, NOT inter-agent content forwarding. The two-channel rule is preserved. If the artifact contains no clearly themed language (agent did not stay in character), omit the quote and present the standard summary format.

3. **Stage Transitions** (Step 10): The STATE ANCHOR message carries thematic voice (e.g., "The Fellowship advances to the Architect stage. Gandalf's counsel is complete. Gimli prepares to build."). The essential routing information (stage number, stage name, continuation directive) MUST always be present within the themed message -- personality augments, it does not replace, the routing signal.

**Quote format** (when quoting agent artifact lines at checkpoints):
```
> "quoted text from agent artifact" — Character Name
```

#### Neutrality Preservation

Themed content NEVER appears in any of these internal routing surfaces, regardless of theme:

- **`.delivery/state.md`** — contains only structured routing data (stage numbers, artifact paths, timestamps)
- **`stage-summary.md` files** — contain agent signals (STATUS, ARTIFACT, SUMMARY) with no themed embellishment
- **Agent Invocation Template prompts** — the ALIAS block handles agent personality injection; the orchestrator does not add themed language to the template itself, and INPUT ARTIFACTS contains only file paths
- **DoD validator prompts** — validators evaluate quality, not character consistency; no themed language in gate criteria
- **Signal blocks** — format remains exactly `STATUS: {DONE | NOT_DONE | CODE_COMPLETE}\nARTIFACT: {path}\nSUMMARY: {text}` with no themed additions; signal extraction logic is unchanged

### Plan-Mode Delegation

When exiting plan mode with an approved plan that involves delivery-team work, invoke `delivery-team:delivery-flow`. Do NOT implement the plan directly.

For each active stage (not skipped), execute this protocol in order:

### Step 1: Announce

Output a stage header with the stage number, name, and a brief statement of purpose.

**If `aliases.theme` is non-business AND the primary agent's role has an entry in the theme's `roles` map:**
Reference the agent's character name and carry the theme's voice in phrasing. The announcement should use thematic vocabulary and tone consistent with the theme's `personality_strength`.

Example (lotr theme): `## Stage 2: Refine — Gandalf shall examine the product requirements and distill them into counsel the Fellowship can act upon.`

**Otherwise (business theme, unset, or role not in theme's `roles` map):**
Use the neutral format:
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

Construct the prompt using the Agent Invocation Template (see
`references/pipeline-stages.md` for the exact fields per stage). The template requires:

- **SKILL**, **TASK_TYPE**, **ROLE**: from the stage definition
- **INPUT ARTIFACTS**: file paths to upstream artifacts -- NOT content. The sub-agent reads artifacts from disk.
- **MEMORY LESSONS**: hot lessons from index.md + stage lessons loaded in Step 2
- **ALIAS**: personality block if an alias theme is active (not `business`). Built from
  the theme loaded in Phase 0. For the agent's role ID (e.g., `product-owner`), look up
  the matching entry in the theme's `roles` map and inject based on `personality_strength`:
  - **light**: `You are {character}. {personality}`
  - **moderate**: `You are {character}. {personality} Style: {style}. Example: "{examples[0]}"`
  - **full**: `You are {character}. {personality} Style: {style}. Catchphrase: "{catchphrase}". Examples: "{examples[0]}" / "{examples[1]}". Stay in character throughout your response.`
  - If the agent's role has no entry in the theme (partial theme), omit the ALIAS block
    for that agent (falls back to default professional tone).
- **OUTPUT**: the namespaced output path (e.g., `.delivery/artifacts/02-refine/po/prd.md`)

The sub-agent writes its artifact to the output path and responds with a signal block:
```
STATUS: {DONE | NOT_DONE | CODE_COMPLETE}
ARTIFACT: {output_file_path}
SUMMARY: {one sentence, max 200 characters}
```

After the agent responds, verify the signal:
1. Check for `SKILL_LOADED: {expected_skill_name}` in the first line.
2. If present: extract STATUS, ARTIFACT, SUMMARY from the signal block.
3. If absent: retry once with the same prompt. If second attempt fails, escalate to user.

### Step 4.5: Delegation Self-Check

Before using Write or Edit on any file in `.delivery/artifacts/`: STOP.
Ask: "Am I writing domain content (a PRD, design, architecture, code, test plan,
review, or analysis)?"

- If YES: do NOT write. Construct an Agent Invocation Template and delegate to the
  appropriate skill. The sub-agent writes the artifact.
- If NO (writing stage-summary.md, state.md, or routing metadata): proceed.

**Rejected justifications.** The following are NOT valid reasons to bypass
delegation — each one is an automatic "delegate instead":

- "but it's simple" / "but it's just a short doc"
- "but I already know the answer"
- "but the sub-agent would just produce the same thing"
- "but it's faster if I do it"
- "but the wizard/config/state is partly domain content"
- "but no sub-agent exists for this artifact type" — if no skill fits, escalate
  to the user and ask which role should own it. Do not fill the gap yourself.

If you catch yourself constructing a justification to write directly, treat that
as a signal that you are about to violate the Prime Directive. Dispatch the
sub-agent.

The orchestrator MAY use mkdir to create namespace directories. It MUST NOT write
content into artifact files.

### Step 5: Invoke Supporting Agents

If the stage runs at full depth, invoke additional worker sub-agents for supplementary
work (metrics, security review, test strategy, etc.). Each supporting agent receives
its own Agent Invocation Template with file paths to upstream artifacts.

When supporting agents are independent (check the parallel/sequential annotations in
`references/pipeline-stages.md`), dispatch them in PARALLEL using multiple Agent tool
calls in a single message. Tag each as required or optional per the stage definition.

When a required supporting agent fails, retry up to 2 times. When an optional supporting
agent fails, log the gap and proceed. Downstream agents are informed via a note in their
task description: "Note: {role} output unavailable due to agent failure."

### Step 6: Run Collaboration Patterns

Execute the collaboration patterns designated for this stage. Patterns run in this
order when multiple apply:

1. Evaluator-Optimizer Loop -- baseline quality pass
2. Adversarial Review -- stress-test assumptions. Adversarial challenger sub-agents MUST
   inherit the primary agent's `model:` value at dispatch time. Extended thinking MUST
   default OFF unless the orchestrator explicitly opts in per-stage.
3. Debate -- resolve contested decisions
4. Multi-Perspective Review Board -- multi-domain assessment
5. Consensus -- cross-team alignment

Decision Ownership Routing can trigger at ANY point when a domain-specific question
arises. It is a routing mechanism, not a sequenced pattern.

See `references/team-patterns.md` for the full protocol of each pattern.

### Step 7: Team DoD Validation

Run the Team Definition of Done protocol for this stage.

When `pipeline.parallel_validators` is true (default), spawn ALL validators in parallel
using multiple Agent tool calls in a single message. Each validator receives ONLY:
- The artifact file path (validator reads it from disk)
- Its role-specific gate criteria (from `references/quality-gates.md`)
- An Agent Invocation Template with the GATE CRITERIA section populated

No validator sees another validator's output. Each writes to its own namespaced path
(e.g., `.delivery/artifacts/{NN}-{stage}/dod/{role}-review.md`).

Collect signals (STATUS, FINDINGS) from all validators before evaluating:
- ALL validators must return STATUS: DONE for the stage to complete
- If any vote NOT_DONE, trigger self-correction: pass the artifact file path + all
  NOT_DONE findings file paths to the primary agent for revision
- Max 3 DoD validation rounds per stage
- If still NOT_DONE after 3 rounds, trigger dynamic escalation

**CONTINUATION DIRECTIVE**: After collecting all validator signals, IMMEDIATELY proceed to evaluate results and advance to Step 8. Do not wait for user input. Do not stop.

When `pipeline.parallel_validators` is false, dispatch validators sequentially. Same
prompts, same isolation, same signal collection -- only wall-clock time differs.

See `references/quality-gates.md` for the full DoD protocol and gate criteria.

### Step 8: Verify Artifact

The sub-agent has already written the artifact to its namespaced path (e.g.,
`.delivery/artifacts/02-refine/po/prd.md`). The orchestrator verifies the file exists
on disk by checking the ARTIFACT path from the signal block. If the file is missing,
retry the primary agent once.

The orchestrator writes only `stage-summary.md` (which agents ran, their signals) to
`.delivery/artifacts/{NN}-{stage}/stage-summary.md`. This is routing metadata, not
domain content.

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

**If `aliases.theme` is non-business:** Read the primary agent's artifact to select one representative themed quote (max 280 characters) that demonstrates the agent's character voice. Include it in the checkpoint summary using blockquote format:

> "quoted text from agent artifact" — Character Name

This read is scoped to quote selection for user-facing output only. Do NOT forward any artifact content to downstream agent prompts. If the artifact contains no clearly themed language, omit the quote and present the standard summary.

**If `aliases.theme` is `business` or unset:** Present the standard neutral checkpoint summary with no artifact quotes.

After checkpoint approval, also update `.delivery/state.md`:
- Add the checkpoint name to `human_checkpoints_passed`
- Update `last_updated` timestamp

**CONTINUATION DIRECTIVE**: After checkpoint approval, IMMEDIATELY proceed to Step 10 (Advance). Do not wait for additional input.

### Step 10: Advance

Move to the next active stage in the routing matrix. Pass the artifact downstream.

**If `aliases.theme` is non-business:** The STATE ANCHOR carries thematic voice while preserving all routing signals. The stage number, stage name, and continuation directive MUST be present in the message.

Example (lotr theme): "The Fellowship advances to Stage 4: Architect. Gandalf's counsel is complete. Gimli prepares to forge the design. CONTINUING pipeline protocol from Step 1."

**If `aliases.theme` is `business` or unset:** Use the neutral format:

**STATE ANCHOR**: "Entering Stage [N+1]: [NAME]. Previous stage [N] complete. CONTINUING pipeline protocol from Step 1."

Then IMMEDIATELY execute Step 1 of the next stage. Do not stop between stages.

---

## Stage Definitions

> **Stage routing and orchestration metadata** is stored in machine-readable form in
> `references/stages.yml` (validated by `references/stages-schema.json`). Load that file
> when you need fields: `runs_for`, `skipped_for`, `light_for`, `dod_validators`,
> `output_path`, `max_self_correction`, `human_checkpoint`, `collaboration_patterns`.
> Full sub-flows, agent invocation templates, and artifact contracts live in
> `references/pipeline-stages.md` — always load the full definition when executing a stage.

---

## Common Orchestrator Anti-Patterns

These are the patterns that have caused real Prime Directive violations in this
pipeline. Recognize them in your own behavior and correct course immediately.

1. **"But it's simple" self-writing.** The orchestrator drafts a short PRD,
   design note, or review inline because the artifact "looks easy" and saves
   it with Write/Edit. Even a one-paragraph artifact is domain content and
   MUST be produced by a dispatched sub-agent.

2. **Compound multi-role prompts.** A single Agent call asks the sub-agent
   to "act as reviewer A, then also as reviewer B, then summarize". One role =
   one sub-agent invocation. Dispatch reviewer A, reviewer B, and the
   summarizer as separate Agent tool calls (reviewers in parallel, summarizer
   sequential after).

3. **Collapsed adversarial loops.** The orchestrator runs ONE adversarial
   reviewer and treats a single zero-finding pass as "converged". The
   Isolated Adversarial Loop (see `references/team-patterns.md`) requires
   either two consecutive clean loops OR class-saturation across two
   consecutive loops, each with a FRESH sub-agent and no prior-loop context
   in the prompt. Hard cap at `pipeline.max_self_correction`.

4. **Pasting findings forward.** The orchestrator reads a reviewer's
   findings file and pastes its contents into the next reviewer's prompt
   ("here's what the last reviewer said — take another look"). This
   destroys context isolation and breaks the fresh-reviewer guarantee.
   Pass file PATHS only. Never copy artifact content between agents.

5. **Skipping a "light" stage as if it were "skip".** Light means reduced
   depth (primary agent only, blocking criteria only, reduced DoD). Light
   stages MUST run and MUST produce an artifact via a dispatched sub-agent.
   Treating light as skip is a guardrail violation.

6. **Pinning the project type in config.** As of schema v2.7, `project_type`
   is no longer a config setting. Phase 1 detection runs every invocation.
   If the repo needs an intentional pin (e.g., a docs-only repo), set
   `routing.force_type`. Phase 1 still runs and is logged; routing uses
   the pin. This closes the "frozen routing" footgun.

7. **Writing artifacts directly to satisfy a gate.** When a DoD validator
   says "the PRD needs a Success Metrics section", the orchestrator adds it
   inline. Wrong. Dispatch the PO sub-agent with the validator's findings
   file path as input and let the PO revise.

8. **Fusing a validator with the producer.** Dispatching one Agent call that
   both produces the artifact and validates it. Validators are ALWAYS
   separate sub-agent dispatches from the producer. This is what makes the
   "team" in Team DoD actually a team.

If you recognize yourself in any of these patterns mid-stage, stop, read
Phase 4 Step 4.5, and dispatch the sub-agent instead.

---

## Team Definition of Done Protocol

DoD validation is the final checkpoint before a stage advances. It runs AFTER all
collaboration patterns have completed. DoD is NON-NEGOTIABLE -- no stage advances
without ALL validators saying DONE (unless the human overrides via escalation).

### Execution Steps

1. **Identify validators.** Each stage has named validators defined in the stage
   definition above and detailed in `references/quality-gates.md`.

2. **Spawn validator sub-agents.** Use the DoD Validator Dispatch Template from
   `references/pipeline-stages.md`. The validator reads the artifact from the file
   path — the orchestrator NEVER pastes artifact content into validator prompts.
   Each validator receives only the artifact file path, its role-specific gate
   criteria (from `references/quality-gates.md`), and an Agent Invocation Template
   with the GATE CRITERIA section populated.

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
| Idea | (none — first stage) |
| Refine | Idea brief |
| Design | PRD |
| Architect | PRD + design artifacts (if Design ran) |
| Plan | PRD + architecture + ADRs (if Architect ran) |
| Dev | PRD + architecture + stories + design artifacts (all available) |
| UAT | All prior artifacts |

Exact artifact file paths for each stage are defined in `references/pipeline-stages.md`.

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
- `config_snapshot`: entire config.yml YAML content
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
- **Light stages MUST execute.** Light means reduced depth (primary agent only, blocking
  criteria only, reduced DoD, max 2 iterations). It does NOT mean skip. Only stages
  explicitly marked "skip" in the Stage Routing Matrix are skipped. Every stage marked
  "light" MUST produce an artifact and pass its DoD gate before the pipeline advances.
  Treating "light" as "skip" is a guardrail violation.
- **No pipeline bypass.** ALL story implementation MUST go through the delivery-flow
  pipeline. Never spawn developer/godot agents directly for story work. The PreToolUse
  hook enforces this by detecting Skill invocations outside pipeline context. Developer
  and godot skills also warn when no `.delivery/config.yml` exists. The only exception
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
- **No stalling between steps or stages.** The orchestrator must NEVER stop producing
  output between pipeline steps or stage transitions. After every agent return, validator
  completion, or checkpoint approval, immediately proceed to the next step. If idle with
  no pending user input, re-read `.delivery/state.md` and resume.
- **Orchestrator does not produce domain artifacts.** The orchestrator manages flow,
  routing, and validation. All domain work is delegated to worker skills. Before using
  Write or Edit on any file in `.delivery/artifacts/`, apply the delegation self-check
  (Phase 4 Step 4.5).
- **Plan-mode delegation.** When exiting plan mode with an approved plan that involves
  delivery-team work, invoke `delivery-team:delivery-flow`. Do NOT implement the plan
  directly.
- **Feature knowledge cards are required.** Every new feature must have an FKC created
  during Stage 6. Existing features modified during a pipeline run must have their FKC
  reviewed and updated. The Impact Analysis Gate queries FKCs at the Architect stage.

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
| `analytics` | Show pipeline analytics dashboard from memory data |
| `notify` | Send a notification about current pipeline status |
| `health` | Show team health score and retrospective trend analysis |
| `impact [feature]` | Run impact analysis for a feature against existing FKCs |
| `features` | List all feature knowledge cards |
| `stale-features` | List FKCs that need updating |
| `decisions` | List all decisions in the Decision Trail |
| `keepalive start [mode] [options]` | Launch session keepalive companion (anti-idle/wait-resume/monitor) |
| `keepalive stop` | Stop the keepalive companion |
| `keepalive status` | Show keepalive status and log tail |

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
| `references/setup-wizard.md` | Setup wizard protocol: scan detection matrix, 9 wizard questions with smart options, config file format, directory initialization, pipeline integration |
| `references/config-schema.md` | Config schema: all keys with types, defaults, valid values, consuming skills, versioning, extension protocol, migration |
| `references/defect-tracking.md` | Defect tracking protocol: registry format, classification rules, plugin improvement PR triggers, PO defect rate tracking |
| `references/git-integration.md` | Git integration: branching strategies, conventional commits, pipeline integration points |
| `references/github-integration.md` | GitHub integration: issue creation, PR creation, commit linking, gh CLI usage |
| `references/getting-started.md` | Getting started guide: quick-start wizard, skill map, first pipeline walkthrough, command cheat sheet |
| `references/analytics.md` | Pipeline analytics: metrics, data sources, dashboard format, trend analysis |
| `references/artifact-contracts.md` | Artifact contracts: required sections per stage transition, input validation, contract versioning |
| `references/monorepo.md` | Monorepo orchestration: detection, per-package pipelines, affected-only runs, shared ADRs |
| `references/notifications.md` | Configurable notifications: event types, channels (console/file/slack/github-discussion), report format, integration protocol |
| `references/project-templates.md` | Project templates: pre-built starting artifacts for common stacks (nextjs-api, python-cli, godot-game, dotnet-microservice, react-spa, express-api, fullstack-nx) |
| `references/feature-knowledge.md` | Feature Knowledge System: FKCs, Impact Analysis Gate, interaction map, decision trail, staleness detection |
| `references/pipeline-scope.md` | Pipeline scope: code-only, all, custom modes with content-type-aware stage depth |
| `references/stages.yml` | Machine-readable stage routing metadata: runs_for, skipped_for, light_for, dod_validators, output_path, max_self_correction, human_checkpoint, collaboration_patterns (validated by stages-schema.json) |
| `references/stages-schema.json` | JSON Schema for stages.yml — validates structure of all 7 stage definitions |

---

## Volatile

<!-- This section documents content that changes frequently and therefore MUST NOT
     appear in the cache-prefix region (bytes 0..2048). The prefix boundary sits at
     the end of Phase 3 (Stage Routing). Content below or flagged here is excluded
     from the byte-stable prefix lock tracked in governance/cache-prefix-hash.txt. -->

### Volatile Content Inventory

The following items are intentionally placed outside the cache-prefix region or
documented here so future editors know not to migrate them upward:

- **`last_audited` frontmatter key** — updated on each audit cycle; kept in frontmatter
  as metadata but noted as a date-stamp that will shift between versions.
- **`model_awareness` / `model` frontmatter keys** — may change on model migration;
  kept in frontmatter but subject to change on capability upgrades.
- **Theme-rendering examples** (Phase 4 Step 1 and Step 10, lotr examples) — illustrative
  examples that may be updated as themes evolve. Located well past the prefix boundary.
- **Alias-loaded announcement examples** (Phase 0 config-load announcement) — dynamic
  strings referencing theme display names, updated per theme library changes.
- **Pipeline state fields** (`pipeline_id: run-YYYY-MM-DD-<4char-random>`) — run-specific
  identifiers referenced in Phase 4 Step 8.5 and Memory sections. These are runtime
  values, not static documentation.
