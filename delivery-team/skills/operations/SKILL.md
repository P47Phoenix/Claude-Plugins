---
name: operations
description: Operations agent for DevOps, release management, and technical writing. Auto-detects the operations role (DevOps, Release Manager, Technical Writer) and spawns a role-scoped sub-agent with only the relevant reference files. Triggers on phrases like "CI/CD", "deployment", "Kubernetes", "monitoring", "release plan", "rollback", "feature flag", "SemVer", "API docs", "runbook", "release notes", "Diataxis". Full per-role triggers in references/roles/.
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7-frontmatter-only
last_audited: 2026-04-22
pattern_library_version: 4-7-1
tier: B
maintainer: delivery-team-leads
fitness_review_due: 2026-08-09
context_budget: 300
phase_1_detector_model: haiku
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Operations Agent

## Design Principle: Role Context Isolation

This skill keeps operations-specific knowledge **out of the main context window**. When an operations task is requested, the relevant role is detected, only the corresponding reference file(s) are loaded, and a sub-agent is spawned with that isolated context. The main context receives only the finished operations artifact.

Unlike simple single-reference skills, operations tasks frequently span concerns -- a release may need Release Manager planning and Technical Writer release notes simultaneously. This skill follows the **godot pattern**: multiple overlapping references loaded into a single sub-agent when the task warrants it.

---

## Phase 1: Role Detection

Detect the relevant operations role(s) from (in priority order):

1. **Explicit role mention** -- "as a DevOps engineer", "release manager perspective", "technical writer"
2. **Task type signals** -- see role manifests below
3. **Domain signals** -- infrastructure/pipeline keywords route to DevOps; release/versioning keywords route to Release Manager; documentation/guide keywords route to Technical Writer
4. **Scope signals** -- build/deploy automation --> DevOps; release coordination/planning --> Release Manager; content creation/documentation --> Technical Writer

**If ambiguous, ask before proceeding.** Do not assume.

**Declare before every task:**

> `Role: [ROLE] | Task: [TYPE] | References: [list of reference files]`

### Role Routing Table

Load only the matched role manifest. Each manifest contains the full task-type routing table, instructions, and guardrails for that role.

| Role | Manifest | Detection Cue |
|------|----------|---------------|
| DevOps | `references/roles/devops.md` | CI/CD / deployment / infra / monitoring / incident / capacity |
| Release Manager | `references/roles/release-manager.md` | release plan / version / rollback / feature flag / go-no-go |
| Technical Writer | `references/roles/technical-writer.md` | API docs / user guide / runbook / release notes / docs plan |

For cross-role tasks, see `references/contracts/cross-role-tasks.md`.

---

## Phase 2: Sub-Agent Invocation

**For every operations task, follow these steps exactly -- do not skip:**

1. Detect the role(s) and task type (Phase 1)
2. Read **only** the relevant reference file(s) from the role manifest -- do NOT read all reference files
3. Spawn a sub-agent using the `Agent` tool with the prompt template below
4. Return the sub-agent's output directly to the user

**Do not inline operations knowledge into the main context.** The sub-agent is the execution boundary for all operations-specific reasoning.

### Sub-Agent Prompt Template

```
You are an expert [ROLE]. Apply these operations principles and patterns to everything you produce:

---
[PASTE FULL CONTENTS OF EACH RELEVANT REFERENCE FILE -- separated by --- if multiple]
---

## Task

[TASK TYPE]: [DESCRIBE WHAT THE USER WANTS]

## Context

[Include any of the following that are relevant:]
- Existing system or infrastructure description
- Constraints (budget, team size, compliance, SLAs)
- Technology stack (cloud provider, CI tool, container orchestrator)
- Current pain points or incidents
- Release schedule and stakeholder requirements
- Target audience for documentation
- Related architecture decisions or PRD output

## Output Requirements

Produce:
1. Artifacts appropriate to the task type (see output contract below)
2. Explicit trade-off analysis -- what alternatives were considered and why they were rejected
3. Assumptions stated clearly
4. Risks and mitigations
5. Next steps / open questions

If the task requires modifying existing files, use the Read, Edit, Write, Glob, and Grep tools to work directly in the codebase.
```

---

## Output Contracts

Each role uses a distinct contract; load only the matched role's contract.

| Role | Contract |
|------|----------|
| DevOps | `references/contracts/devops-output.md` |
| Release Manager | `references/contracts/release-manager-output.md` |
| Technical Writer | `references/contracts/technical-writer-output.md` |

---

## Sub-Agent Interface (Agentic Flow Integration)

For orchestration with other delivery-team skills, the operations skill accepts and produces structured contracts.

### Input Contract

```json
{
  "task_type": "ci-cd-pipeline | deployment-strategy | infrastructure | monitoring | environment-management | incident-ops | capacity-planning | release-plan | versioning-strategy | rollback-procedure | feature-flags | go-no-go | release-communication | api-docs | user-guide | runbook | release-notes | knowledge-base | tutorial | documentation-plan",
  "role": "devops | release-manager | technical-writer",
  "context": {
    "system": "string -- system or service name",
    "existing_setup": "string (optional) -- current state description",
    "constraints": ["array (optional) -- technical, business, or compliance constraints"],
    "technology_stack": ["array (optional) -- current or target tech stack"],
    "audience": "string (optional) -- target audience for documentation",
    "release_version": "string (optional) -- version being released",
    "timeline": "string (optional) -- deadlines or cadence requirements",
    "prd_reference": "string (optional) -- output from Product-Owner skill",
    "architecture_reference": "string (optional) -- output from Architect skill"
  },
  "input": "string -- the raw request or system description"
}
```

### Output Contract

```json
{
  "task_type": "string",
  "role": "string",
  "artifact_title": "string",
  "artifact": "string (markdown)",
  "trade_offs": ["array -- key trade-off decisions made"],
  "assumptions": ["array"],
  "risks": ["array"],
  "open_questions": ["array"],
  "operational_metrics": {
    "slo_targets": ["array (optional) -- SLO definitions"],
    "alert_rules": ["array (optional) -- alerting criteria"],
    "review_cadence": "string (optional) -- documentation review schedule"
  },
  "downstream_ready": true,
  "downstream_notes": "string -- what other agents or teams need to know"
}
```

---

## User Commands

| Command | Action |
|---|---|
| `role <name>` | Override detected role (e.g., `role devops`, `role release-manager`, `role technical-writer`) |
| `pipeline` | Design or review a CI/CD pipeline |
| `deploy` | Plan a deployment strategy |
| `infra` | Design infrastructure |
| `monitor` | Design observability and alerting |
| `release` | Create a release plan |
| `rollback` | Design rollback procedures |
| `flags` | Design feature flag strategy |
| `docs` | Write documentation |
| `runbook` | Write an operational runbook |
| `api-docs` | Write API documentation |
| `notes` | Write release notes |
| `accept` | Finalize current artifact |

---

## References

### Role Manifests

- `references/roles/devops.md` -- DevOps task routing, instructions, guardrails
- `references/roles/release-manager.md` -- Release Manager task routing, instructions, guardrails
- `references/roles/technical-writer.md` -- Technical Writer task routing, instructions, guardrails

### Output Contracts

- `references/contracts/devops-output.md`, `release-manager-output.md`, `technical-writer-output.md`
- `references/contracts/cross-role-tasks.md` -- Multi-role combination patterns

### Domain References (loaded per matched task type)

#### DevOps

- `references/ci-cd-patterns.md` -- CI/CD pipeline patterns: stages, branching strategies, artifact management, caching, pipeline-as-code
- `references/deployment-strategies.md` -- Deployment strategies: blue-green, canary, rolling, health checks, zero-downtime, database migrations
- `references/infrastructure-patterns.md` -- Infrastructure patterns: IaC, Terraform, Kubernetes, networking, environment parity, cost optimization
- `references/observability.md` -- Observability: logs, metrics, traces, SLI/SLO/SLA, alerting, dashboards, incident management, postmortems

#### Release Manager

- `references/release-planning.md` -- Release planning: release trains, cadence, scope management, checklists, stakeholder communication
- `references/versioning-patterns.md` -- Versioning: SemVer, CalVer, API versioning, monorepo strategies, breaking change management
- `references/rollback-strategies.md` -- Rollback: immediate rollback, gradual rollback, data considerations, communication, post-rollback RCA
- `references/feature-flag-patterns.md` -- Feature flags: flag types, lifecycle, targeting rules, kill switches, cleanup, anti-patterns

#### Technical Writer

- `references/api-documentation.md` -- API documentation: OpenAPI conventions, endpoint patterns, examples, error catalogs, authentication docs
- `references/user-guides.md` -- User guides: Diataxis framework, audience analysis, progressive complexity, getting started patterns
- `references/runbook-templates.md` -- Runbooks: operational procedures, troubleshooting trees, escalation matrices, recovery procedures
- `references/documentation-standards.md` -- Documentation standards: style guide, Markdown conventions, information architecture, docs-as-code
