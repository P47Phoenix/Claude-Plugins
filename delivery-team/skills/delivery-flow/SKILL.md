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

## Phase 1: Project Type Detection

Before the pipeline can execute, the project type must be determined. The type drives
which stages run, at what depth, and which agents participate.

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

Before starting pipeline execution, retrieve lessons from past runs:

1. Check if `.delivery/memory/` exists in the current working directory.
2. If yes, read `.delivery/memory/lessons-index.md` for aggregated lessons.
3. Filter lessons relevant to:
   - The detected project type
   - The stages that will execute in this run
4. Pass relevant lessons to agents as context throughout the pipeline. Include them
   in agent prompts as:
   ```
   Lessons from past runs on this project:
   - [Lesson 1]
   - [Lesson 2]
   Consider these as you work. They reflect patterns observed in previous deliveries.
   ```
5. If no memory directory exists, proceed without lessons. The first run establishes
   the baseline.

See `references/memory-protocol.md` for the full retrieval and update protocol.

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

### Step 2: Load Memory

Retrieve stage-specific lessons from past runs. Filter the lessons loaded in Phase 2
to only those relevant to this stage. Pass them to the agents invoked in this stage.

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

### Step 9: Check for Human Checkpoint

If this stage has a scheduled human checkpoint, present a summary of the artifact and
wait for the user to approve, request changes, or abort.

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
2. Scrum Master (product-delivery skill, task_type: sprint_planning).
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
- Scrum Master (product-delivery skill): process is sound, capacity is realistic,
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
  practices, no hardcoded secrets.
- QA Engineer (quality skill): tests pass, coverage is adequate, no critical issues.
- Architect (architect skill): implementation conforms to architecture decisions, no
  architectural drift.
- Technical Writer (operations skill): inline documentation present for non-obvious
  logic, API docs if applicable.

**Output**:
- Code files in the project codebase.
- `.delivery/artifacts/06-dev-notes.md` (summary of implementation decisions, known
  issues, deviations from plan).

**Human checkpoint**: none.

**Max self-correction**: 3 iterations per story.

**Game dev additions**: Godot skill (or relevant engine skill) invoked alongside
Developer for engine-specific work. Game-specific testing (playtest scenarios,
performance profiling against frame budgets).

---

### Stage 7: UAT

**Runs for**: GREENFIELD (full), FEATURE (full), BUG_FIX (full), GAME_DEV+ (full),
DOCS_ONLY (full).
Skipped for: SPIKE.

**Purpose**: Execute user acceptance testing, prepare release artifacts, and get
final approval for delivery.

**Primary agents**:
1. QA Engineer (quality skill, task_type: test-plan).
   - Input: PRD acceptance criteria + developed features.
   - Output: UAT test plan with test cases.
2. QA Engineer (quality skill, task_type: test-cases).
   - Input: test plan.
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
documentation for accept or reject.

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

### Post-Pipeline Protocol

1. **Run retrospective.** Invoke Scrum Master (product-delivery skill, task_type:
   retrospective) to capture what went well, what did not, and improvement actions.

2. **Construct memory file.** Build the memory file from pipeline execution data:
   - Gate results (pass/fail per stage, iteration counts)
   - Human checkpoint deltas (what changed at each approval)
   - Adversarial review insights (valid findings accepted, confidence ratings)
   - DoD validation patterns (which validators found issues, which criteria failed)
   - Decisions made and their context
   - Debate outcomes and ADRs produced

3. **Write memory file.** Save to `.delivery/memory/run-YYYY-MM-DD-<4char-id>.md`.

4. **Update lessons index.** Update `.delivery/memory/lessons-index.md`:
   - Add new lessons from this run.
   - Consolidate repeated lessons (increment run count).
   - Remove lessons contradicted by this run's evidence.

5. **Apply memory decay.** Lessons from the last 5 runs are weighted most heavily.
   Lessons older than 10 runs are candidates for removal unless still validated.
   Lessons contradicted by 3 consecutive runs are removed.

See `references/memory-protocol.md` for the full memory file format, lessons index
structure, and decay rules.

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
- **Preserve on abort.** If the pipeline is aborted at any point, all artifacts
  produced so far are preserved in `.delivery/artifacts/`. The memory file is written
  even for aborted runs (with `completed: false` and `abort_stage` recorded).
- **Orchestrator does not produce domain artifacts.** The orchestrator manages flow,
  routing, and validation. All domain work is delegated to worker skills.

---

## User Commands

| Command | Action |
|---------|--------|
| `start` | Begin delivery pipeline with project type detection |
| `status` | Show current pipeline state (stage, progress, issues) |
| `skip` | Skip current stage (requires confirmation, records reason) |
| `back` | Return to previous stage for rework |
| `approve` | Approve artifact at human checkpoint |
| `request-changes [feedback]` | Request changes at human checkpoint with specific feedback |
| `abort` | Halt pipeline, preserve all artifacts, write memory file |
| `type <TYPE>` | Override detected project type (e.g., `type FEATURE`) |
| `memory` | Show lessons from past runs relevant to current project |
| `escalate` | Manually trigger escalation for current stage |

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
| `references/memory-protocol.md` | Memory file format, lessons index structure, retrieval protocol, update protocol, memory decay rules, .delivery directory structure |
