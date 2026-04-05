# Delivery Flow

**Invocation**: `delivery-team:delivery-flow`

The pipeline orchestrator that coordinates the full delivery team through 7 stages. This is the entry point for all structured delivery work.

## What It Does

- Coordinates 11 specialized skills through a 7-stage pipeline
- Auto-detects project type and routes through appropriate stages
- Runs quality gates with multi-role Definition of Done validation
- Self-corrects when validation fails (max 3 iterations per stage)
- Learns from every run via self-learning memory
- Supports 6 collaboration patterns for structured quality assurance
- Manages alias themes for agent personality injection

## How to Trigger

Say any of:

- "start a new feature"
- "delivery pipeline"
- "new project"
- "greenfield"
- "bug fix"
- "start delivery"
- "run pipeline"

## Key Concepts

### Setup Wizard

Before the pipeline runs, it checks for `.delivery/config.yml`. If none exists, the setup wizard launches. Options:

- **Full wizard**: 9+ questions covering project type, tech stack, team size, deployment, risk tolerance, compliance, checkpoints, patterns, and personas
- **Quick start**: 3 questions — what you are building, language/framework, strictness level

### Pipeline Phases

1. **Phase 0: Setup** — Config detection, state resume check, wizard if needed
2. **Phase 1: Type Detection** — Auto-detect project type from user input
3. **Phase 2: Memory Retrieval** — Load lessons from previous runs
4. **Phase 3: Stage Routing** — Determine which stages run and at what depth
5. **Phase 4: Execution** — Execute each active stage with the protocol below

### Per-Stage Protocol

For each active stage:

1. **Announce** the stage with purpose
2. **Load stage memory** from chunked topic files
3. **Load stage definition** from pipeline-stages reference
4. **Invoke primary agent** with the Agent Invocation Template
5. **Run collaboration patterns** (evaluator-optimizer, adversarial review, etc.)
6. **Run DoD validation** — all validators must say DONE
7. **Self-correct** if validation fails (route feedback, re-invoke, re-validate)
8. **Human checkpoint** if configured for this stage
9. **Update state** and advance to next stage

### Two-Channel Communication

- **Signal channel**: STATUS, file paths, summaries (max 200 chars) — for routing decisions
- **Artifact channel**: File contents written to disk — the orchestrator passes paths, never content

### State Persistence

Pipeline state is persisted in `.delivery/state.md`. If a session is interrupted:

- **Resume**: Load config from snapshot, skip completed stages
- **Restart**: Archive old state, start fresh
- **Abandon**: Delete state file

## Example Usage

```
User: "Start a new feature — add search to our API"

Pipeline detects: FEATURE
Stages: Idea (full), Refine (full), Design (full), Architect (light),
        Plan (full), Dev (full), UAT (full)
Checkpoints: Refine, UAT

Stage 1: Product Owner captures idea brief
Stage 2: Product Owner writes PRD with stories and ACs
  [Checkpoint: User reviews PRD]
Stage 3: UX Designer creates user flows
Stage 4: Architect designs search architecture (light depth)
Stage 5: Scrum Master creates sprint plan
Stage 6: Developer implements each story
Stage 7: QA runs acceptance tests, personas test the feature
  [Checkpoint: User accepts or rejects]
```

## Configuration

The delivery flow reads all keys from `.delivery/config.yml`. See the [Configuration Reference](../user-guide/config.md) for the complete key list.

Key settings that affect pipeline behavior:

| Setting | Effect |
|---------|--------|
| `project_type` | Determines stage routing |
| `pipeline.checkpoints` | Which stages have human checkpoints |
| `pipeline.collaboration_patterns` | Which quality patterns run |
| `pipeline.max_self_correction` | Iteration limit per stage |
| `aliases.theme` | Agent personality injection |
| `personas.feedback_stages` | When persona testing runs |
