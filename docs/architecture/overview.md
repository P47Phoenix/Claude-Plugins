# Architecture Overview

The delivery-team plugin is built on a few core architectural patterns.

## Pipeline Architecture

The delivery pipeline follows a **delegation, not execution** model:

- The **orchestrator** (`delivery-flow`) manages flow, routing, and validation
- **Worker skills** (developer, architect, quality, etc.) produce all artifacts
- Workers are invoked as **sub-agents** using the Agent tool with isolated context

### Two-Channel Communication

| Channel | Content | Flow |
|---------|---------|------|
| **Signal** | STATUS, file paths, summaries (<200 chars) | Through orchestrator for routing |
| **Artifact** | File contents (any length) | Written to disk by sub-agents |

The orchestrator passes file paths between agents, never artifact content. If information is longer than 200 characters, it belongs in a file.

### Context Isolation

Each sub-agent receives only:

- Upstream artifact file paths (not content — it reads them from disk)
- Memory lessons relevant to its task
- Its own SKILL.md and reference files
- Alias personality block (if theme is active)

No agent sees the full pipeline state. No agent sees another agent's reasoning.

## Artifact Flow

Artifacts follow a namespaced convention:

```
.delivery/artifacts/{NN}-{stage-name}/{role}/{artifact-name}.md
```

Each sub-agent writes to its own dedicated directory. No two agents share a write path. The orchestrator writes only to `stage-summary.md` (metadata) and `.delivery/state.md` (pipeline state).

### Stage-to-Stage Contracts

Each stage transition has defined contracts specifying required output sections. The downstream stage validates its inputs before starting work.

| Transition | Key Artifact | Required Sections |
|-----------|-------------|-------------------|
| Idea to Refine | `01-idea/po/idea-brief.md` | Problem Statement, Target Users, Goals |
| Refine to Design | `02-refine/po/prd.md` | Personas, Stories with ACs |
| Design to Architect | `03-design/ux/design.md` | User flows, wireframes |
| Architect to Plan | `04-architect/architect/architecture.md` | Components, data models, ADRs |
| Plan to Dev | `05-plan/sm/sprint-plan.md` | Tasks, test cases, dependencies |
| Dev to UAT | `06-dev/developer/*.md` | Implementation per story |

## Feature Knowledge System

Every delivered feature gets a **Feature Knowledge Card (FKC)** at `.delivery/features/<feature-slug>.md`. Cards track:

- What the feature provides (interfaces, contracts)
- What it consumes (dependencies, assumptions)
- Data profile (storage, access patterns, volume)
- Operations concerns (config keys, migrations, deployment dependencies)
- Known fragilities and boundary tests

The **Impact Analysis Gate** runs before architecture decisions to check existing FKCs for potential conflicts.

## Self-Learning Memory

Memory uses a tiered chunked system. See the [Memory System](../reference/memory.md) reference for full details.

Key design decisions:

- Routing index (~50 lines) is the only file read on every pipeline start
- Stage chunks (~100 lines each) are loaded per-stage, not upfront
- Topic chunks are loaded based on context (checkpoints, decisions, gate failures)
- Run archives are preserved but never loaded during normal execution

## Pipeline State Persistence

Pipeline state is persisted in `.delivery/state.md` as YAML frontmatter. On session interruption:

- **Resume**: Load state, skip completed stages, continue from current stage
- **Restart**: Archive old state, start fresh
- **Config divergence**: If config changed since pipeline started, warn and offer restart

## Defect Tracking

The pipeline tracks defect rates per sprint as a quality metric:

- Target: less than 0.3 defects per story
- Defect categories reviewed in retrospectives
- Persistent patterns trigger plugin self-improvement PRs
- Rate trends monitored over time

## Git and GitHub Integration

The pipeline integrates with Git for branching, commits, and PRs:

- **Branching**: trunk-based, github-flow, or gitflow (configurable)
- **Commits**: Conventional commit messages with issue linking
- **Issues**: Auto-create GitHub issues from user stories at Refine
- **PRs**: Auto-create PR at UAT stage
- **Branch naming**: `<type>/<issue-number>-<short-description>`
