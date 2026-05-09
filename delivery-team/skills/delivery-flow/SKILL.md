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
maintainer: delivery-team-leads
fitness_review_due: 2026-08-09
context_budget: 500
---

# Delivery Flow Orchestrator

## Design Principle

This skill is the ORCHESTRATOR. It coordinates the delivery team through a structured
pipeline but NEVER produces domain artifacts directly. All domain work — requirements,
designs, architecture, code, tests, plans — is delegated to worker skills operating as
sub-agents with isolated context. Full doctrine elaboration, Core Principles 1–7,
Anti-Patterns catalogue, and Guardrails detail: see
`delivery-team/references/shared/orchestrator-doctrine.md`.

> **Model awareness (Opus 4.7 / F-08):** Under F-08, the 4.7 runtime dispatches fewer
> sub-agents by default unless explicitly steered. "One Role = One Sub-Agent" (Phase 4)
> is a **behaviourally load-bearing** gate, not a style preference. Role-count
> under-dispatch is the highest-confidence regression mode on 4.7.

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
   - **Read `prose_style`** (top-level; default `caveman-lite`; valid `caveman-lite | standard`); cache on loaded-config; consumed at Phase 4 Step 4 (conditional PROSE STYLE block) and Step 7 (DoD validator framing). See ADR-tk3-001.
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

1. **What language/framework?** — auto-detect from codebase, user confirms
2. **How strict?** — Prototype (minimal) / Standard (balanced) / Strict (full)

> **Note**: Project type is detected per run in Phase 1, not configured. Use `routing.force_type` if you want to pin it.

All other settings use smart defaults from `references/config-schema.md` based on the detected project type and strictness level. Generate `.delivery/config.yml` and proceed.

See `references/getting-started.md` for the complete quick-start walkthrough, skill map, and command cheat sheet.

> **Config keys applied to pipeline**: see `references/config-keys.md` (35 settings).

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
| GAME_DEV | "game", "Godot", "Unity", "gameplay", "NPC", "HUD", "GDScript" | MODIFIER — always combines with another type |
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

> **Model awareness (Opus 4.7 / F-08):** On 4.7, silent sub-agent fusion is the
> highest-confidence regression mode. The count of dispatched roles at each DoD
> checkpoint MUST equal the length of `dod_validators.<stage>` in config. A
> short-count dispatch is a Prime Directive violation under 4.7 semantics.

### Two-Channel Communication

The orchestrator uses two communication channels:

- **Signal channel**: STATUS, file paths, summaries (<200 chars) — flows through orchestrator for routing decisions.
- **Artifact channel**: file contents — NEVER flows through orchestrator. Sub-agents write files to disk. Downstream agents read files by path. The orchestrator passes paths, not content.

**The rule**: If information is longer than 200 characters, it belongs in a file. The orchestrator passes the file path. The downstream agent reads the file. The orchestrator NEVER reads an artifact and pastes its content into another agent's prompt.

### Theme-Gated Reporting

When `aliases.theme` is non-business, orchestrator user-facing output reflects the theme's personality across 3 output slots (Step 1 announcements, Step 9 checkpoint quotes, Step 10 state anchors). Business/unset theme = neutral format, zero behavior change. Full 4-paragraph protocol: see `delivery-team/references/shared/orchestrator-doctrine.md` § Theme-Gated Reporting Protocol.

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
`references/pipeline-stages.md` for the exact fields per stage). Required fields:
**SKILL**, **TASK_TYPE**, **ROLE**, **INPUT ARTIFACTS** (file paths only — not content),
**MEMORY LESSONS**, **ALIAS** (personality block if non-business theme; see
`references/pipeline-stages.md` for injection format), **OUTPUT** (namespaced path).

**PROSE STYLE block injection** (post-ALIAS, pre-OUTPUT): if `config.prose_style == caveman-lite` (default), inject the verbatim PROSE STYLE block from `references/prose-style.md` into the dispatch prompt; if `standard`, omit the block entirely (no placeholder line). Same rule applies uniformly to Primary (this Step 4), Supporting (Step 5), and DoD Validator (Step 7) dispatches. See ADR-tk3-001 Element 2.

The sub-agent writes its artifact and responds with a signal block:
```
STATUS: {DONE | NOT_DONE | CODE_COMPLETE}
ARTIFACT: {output_file_path}
SUMMARY: {one sentence, max 200 characters}
```

Verify signal: check `SKILL_LOADED: {expected_skill_name}` first line. If absent,
retry once. If second attempt fails, escalate to user.

### Step 4.5: Delegation Self-Check

Before using Write or Edit on any file in `.delivery/artifacts/`: STOP.
Ask: "Am I writing domain content (a PRD, design, architecture, code, test plan,
review, or analysis)?"

- If YES: do NOT write. Delegate to the appropriate skill via Agent Invocation Template.
- If NO (writing stage-summary.md, state.md, or routing metadata): proceed.

No justification bypasses delegation. "But it's simple", "but I know the answer",
"but no sub-agent exists" — all auto-delegate or escalate. If you construct a
justification to write directly, that IS the Prime Directive violation signal.

The orchestrator MAY use mkdir. It MUST NOT write content into artifact files.

### Step 5: Invoke Supporting Agents

At full depth, invoke supplementary worker sub-agents (metrics, security, test strategy,
etc.) using file paths as inputs. Dispatch independent agents in PARALLEL. Required
agent failure: retry ×2. Optional agent failure: log gap, proceed, notify downstream.
See `references/pipeline-stages.md` for parallel/sequential annotations per stage.

### Step 6: Run Collaboration Patterns

Execute patterns for this stage in order: (1) Evaluator-Optimizer, (2) Adversarial
Review — challenger MUST inherit primary `model:` value; extended thinking default OFF,
(3) Debate, (4) Multi-Perspective Review Board, (5) Consensus. Decision Ownership
Routing triggers at ANY point (routing mechanism, not sequenced). Full protocol:
`references/team-patterns.md`.

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
prompts, same isolation, same signal collection — only wall-clock time differs.

See `references/quality-gates.md` for the full DoD protocol and gate criteria.

### Step 8: Verify Artifact

Verify the ARTIFACT path from the signal block exists on disk. If missing, retry the
primary agent once. Write `stage-summary.md` (agents ran, their signals) to
`.delivery/artifacts/{NN}-{stage}/stage-summary.md` — routing metadata, not domain content.

### Step 8.5: Update Pipeline State

Atomic write to `.delivery/state.md` (`state.tmp.md` → rename): update `current_stage`
(NEXT stage), add completed stage to `stages_completed`, add artifact path to `artifacts`
map, update `last_updated`. Enables resume if session dies.

### Step 9: Check for Human Checkpoint

If this stage has a scheduled human checkpoint, present artifact summary and await
approve / request-changes / abort.

**If `aliases.theme` is non-business:** Read the artifact to select one themed quote
(max 280 chars). Format: `> "quoted text" — Character Name`. Scoped to user-facing
output only — do NOT forward content to downstream agents. If no themed language, omit.

**If `aliases.theme` is `business` or unset:** Standard neutral summary, no quotes.

After approval: add checkpoint name to `human_checkpoints_passed` in state; update
`last_updated`.

**CONTINUATION DIRECTIVE**: After checkpoint approval, IMMEDIATELY proceed to Step 10. Do not wait.

### Step 10: Advance

Move to the next active stage in the routing matrix.

**If `aliases.theme` is non-business:** STATE ANCHOR carries thematic voice. Stage
number, name, and continuation directive MUST be present.

**Otherwise:** **STATE ANCHOR**: "Entering Stage [N+1]: [NAME]. Previous stage [N] complete. CONTINUING pipeline protocol from Step 1."

Then IMMEDIATELY execute Step 1 of the next stage. Do not stop between stages.

---

## Stage Definitions

> **Stage routing and orchestration metadata** is stored in machine-readable form in
> `references/stages.yml` (validated by `references/stages-schema.json`). Load that file
> when you need fields: `runs_for`, `skipped_for`, `light_for`, `dod_validators`,
> `output_path`, `max_self_correction`, `human_checkpoint`, `collaboration_patterns`.
> Full sub-flows, agent invocation templates, and artifact contracts live in
> `references/pipeline-stages.md` — always load the full definition when executing a stage.

> **Anti-Patterns catalogue** (8 patterns): `delivery-team/references/shared/orchestrator-doctrine.md` § Common Orchestrator Anti-Patterns.
> **User Commands** (18): `references/commands.md`. **References manifest** (22 files): `references/manifest.yml`.

## Cross-Stage Artifact Flow

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
