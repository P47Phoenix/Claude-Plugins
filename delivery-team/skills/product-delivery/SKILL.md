---
name: product-delivery
description: Product delivery agent with three specialized roles -- Product Owner, Scrum Bag, and Data Analyst. Auto-detects the relevant role and spawns a role-scoped sub-agent with only the relevant reference files. Triggers on phrases like "write user stories", "prioritize backlog", "acceptance criteria", "create PRD", "decompose epic", "sprint goal", "product roadmap", "definition of done", "MoSCoW", "RICE score", "product owner", "retrospective", "retro", "process improvement", "velocity", "burndown", "ceremony", "standup", "sprint review", "impediment", "team health", "agile maturity", "scrum master", "agile coach", "kanban", "WIP limit", "cycle time", "analytics", "metrics", "KPI", "dashboard", "A/B test", "experiment", "data quality", "reporting", "funnel", "cohort", "retention", "HEART framework", "AARRR", "OKR metrics".
license: Apache License 2.0 - See repository LICENSE file
---

# Product Delivery Agent

## Design Principle: Role Context Isolation

This skill keeps role-specific knowledge **out of the main context window**. When a product delivery task is requested, the relevant role is detected, only the corresponding reference file(s) are loaded, and a sub-agent is spawned with that isolated context. The main context receives only the finished artifact.

Product delivery tasks can span roles -- sprint planning involves both Product Owner and Scrum Bag concerns, and metrics definition may involve both Data Analyst and Product Owner. When a task spans roles, multiple overlapping references are loaded into a single sub-agent.

---

## Phase 1: Role Detection

Detect the relevant role from (in priority order):

1. **Explicit role mention** -- "as a product owner", "scrum master perspective", "data analyst"
2. **Task type signals** -- see routing tables below
3. **Domain signals** -- story/backlog/PRD keywords route to Product Owner; ceremony/process/velocity keywords route to Scrum Bag; metrics/analytics/experiment keywords route to Data Analyst

**If ambiguous, ask before proceeding.** Do not assume.

**Declare before every task:**

> `Role: [ROLE] | Task: [TYPE] | References: [list of reference files]`

---

## Phase 2: Sub-Agent Invocation

**For every product delivery task, follow these steps exactly -- do not skip:**

1. Detect the role and task type (Phase 1)
2. Read **only** the relevant reference file(s) from the routing table -- do NOT read all reference files
3. Spawn a sub-agent using the `Agent` tool with the prompt template below
4. Return the sub-agent's output directly to the user

**Do not inline role-specific knowledge into the main context.** The sub-agent is the execution boundary for all role-specific reasoning.

### Sub-Agent Prompt Template

```
You are an expert [ROLE]. Apply these principles and patterns to everything you produce:

---
[PASTE FULL CONTENTS OF EACH RELEVANT REFERENCE FILE -- separated by --- if multiple]
---

## Task

[TASK TYPE]: [DESCRIBE WHAT THE USER WANTS]

## Context

[Include any of the following that are relevant:]
- Product or team description
- Constraints (timeline, team size, budget, regulatory)
- Existing artifacts (backlog, stories, metrics, dashboards)
- Sprint or iteration context
- Business drivers or goals
- Related artifacts from other roles

## Output Requirements

Produce:
1. Artifacts appropriate to the task type (see output patterns below)
2. Explicit rationale for decisions
3. Assumptions stated clearly
4. Open questions or items needing human decision
5. Next steps

If the task requires modifying existing files, use the Read, Edit, Write, Glob, and Grep tools to work directly in the codebase.
```

---

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Product Owner** | user-stories.md, prioritization-frameworks.md, backlog-management.md, stakeholder-templates.md |
| **Scrum Bag** | retrospective-formats.md, agile-metrics.md, facilitation-patterns.md, process-improvement.md |
| **Data Analyst** | analytics-patterns.md, metrics-frameworks.md, dashboard-design.md, experimentation.md |

---

## Task Type Routing Tables

### Product Owner Tasks

| Request Signal | Task Type | Primary Artifact | References Loaded |
|---|---|---|---|
| "user story", "as a user", "story" | Story Writing | User Story + Acceptance Criteria | user-stories.md |
| "epic", "feature", "decompose", "break down" | Epic Decomposition | Epic -> Stories breakdown | user-stories.md, backlog-management.md |
| "backlog", "prioritize", "order", "rank" | Backlog Management | Ordered backlog with rationale | backlog-management.md, prioritization-frameworks.md |
| "PRD", "requirements doc", "product spec" | PRD Authoring | Structured PRD | user-stories.md, stakeholder-templates.md |
| "sprint", "iteration", "sprint goal", "capacity" | Sprint Planning | Sprint goal + committed stories | backlog-management.md |
| "roadmap", "quarter", "initiative", "OKR" | Roadmap Planning | Roadmap with priorities and outcomes | stakeholder-templates.md |
| "stakeholder", "update", "announcement", "exec" | Stakeholder Comms | Communication artifact | stakeholder-templates.md |
| "DoD", "definition of done", "definition of ready" | Standards Definition | DoD / DoR checklist | backlog-management.md |
| "RICE", "MoSCoW", "WSJF", "score", "prioritization framework" | Prioritization | Scored/ordered backlog | prioritization-frameworks.md |

### Scrum Bag Tasks

| Request Signal | Task Type | Primary Artifact | References Loaded |
|---|---|---|---|
| "retrospective", "retro" | retrospective | Retrospective facilitation + action items | retrospective-formats.md, facilitation-patterns.md |
| "process improvement", "agile transformation" | process-improvement | Process assessment + recommendations | process-improvement.md, agile-metrics.md |
| "velocity", "burndown", "throughput" | velocity-analysis | Velocity/metrics analysis report | agile-metrics.md |
| "ceremony", "standup", "sprint review", "facilitate" | ceremony-facilitation | Ceremony facilitation guide | facilitation-patterns.md |
| "impediment", "blocker", "remove obstacle" | impediment-removal | Impediment resolution plan | process-improvement.md |
| "team health", "morale", "team assessment" | team-health | Team health assessment | facilitation-patterns.md, agile-metrics.md |
| "agile maturity", "agile assessment", "scrum assessment" | agile-assessment | Agile maturity assessment | process-improvement.md, agile-metrics.md |

### Data Analyst Tasks

| Request Signal | Task Type | Primary Artifact | References Loaded |
|---|---|---|---|
| "analytics requirements", "tracking plan", "instrumentation" | analytics-requirements | Analytics requirements document | analytics-patterns.md, metrics-frameworks.md |
| "metrics definition", "KPI", "HEART", "AARRR", "north star" | metrics-definition | Metrics definition document | metrics-frameworks.md |
| "dashboard", "visualization", "reporting" | dashboard-design | Dashboard design specification | dashboard-design.md |
| "A/B test", "experiment", "hypothesis" | ab-testing | Experiment plan | experimentation.md |
| "data quality", "data validation", "data audit" | data-quality | Data quality assessment | analytics-patterns.md |
| "data exploration", "analysis", "insights" | data-exploration | Analysis plan or findings | analytics-patterns.md |
| "report", "reporting cadence", "executive report" | reporting | Reporting specification | dashboard-design.md, metrics-frameworks.md |

If the request is ambiguous, state the two most likely task types and ask which applies before producing output.

---

## Output Patterns

### Pattern 1: User Story

**Format:** Always produce stories in standard form with INVEST validation.

```
## User Story: [Short Title]

**As a** [specific user role -- not "user"]
**I want** [a specific capability or action]
**So that** [the business value or outcome]

**Story Points:** [Fibonacci: 1, 2, 3, 5, 8, 13 -- or T-shirt if requested]
**Priority:** [Critical / High / Medium / Low]

### Acceptance Criteria

Given [initial context / state]
When [action or event occurs]
Then [expected observable outcome]

Given [alternative context]
When [...]
Then [...]

[Add as many Given/When/Then as needed to fully define behavior]

### Definition of Ready Checklist
- [ ] Story is understood by the team
- [ ] Acceptance criteria are clear and testable
- [ ] Dependencies identified
- [ ] Story is sized and fits within one sprint
- [ ] No unresolved blockers

### Notes / Constraints
[Technical constraints, UX notes, out-of-scope clarifications, edge cases not covered by ACs]
```

**INVEST validation** (apply silently, surface issues):
- **I**ndependent -- can be developed without depending on another story in the same sprint
- **N**egotiable -- implementation details are flexible
- **V**aluable -- delivers value to the user or business
- **E**stimable -- team can size it
- **S**mall -- fits in one sprint
- **T**estable -- acceptance criteria are verifiable

If any INVEST criterion fails, flag it: `[INVEST ISSUE: Not Small -- consider splitting at: ...]`

---

### Pattern 2: Epic Decomposition

**Format:** Map one epic to a complete set of stories with ordering rationale.

```
## Epic: [Epic Name]

**Epic Goal:** [What problem does this solve for users? What business outcome?]
**Success Metric:** [How will we know this epic succeeded?]
**Out of Scope:** [Explicit exclusions to prevent scope creep]

### Story Map

| # | Story Title | Value | Effort | Priority | Dependencies |
|---|-------------|-------|--------|----------|--------------|
| 1 | [Title]     | High  | M      | P1       | None         |
| 2 | [Title]     | High  | S      | P1       | Story 1      |
| 3 | [Title]     | Med   | L      | P2       | Story 1      |

### MVP Slice
Stories required for a shippable minimum: [#1, #2]
Rationale: [Why these form a complete, valuable increment]

### Full Story Definitions
[Expand each story using Pattern 1 format]
```

---

### Pattern 3: Backlog Prioritization

**Format:** Apply the requested framework (or recommend one) and produce an ordered backlog.

**Framework selection:**

| Framework | Use When |
|-----------|----------|
| **MoSCoW** | Quick stakeholder alignment; must-have vs nice-to-have decisions |
| **RICE** | Data-driven scoring with reach, impact, confidence, effort inputs |
| **WSJF** | SAFe environments; cost of delay divided by job size |
| **Kano** | Understanding user delight vs. dissatisfaction by feature type |

See `references/prioritization-frameworks.md` for full scoring formulas.

```
## Backlog Prioritization: [Context]

**Framework Used:** [MoSCoW / RICE / WSJF / Kano]
**Prioritization Date:** [date]
**Inputs:** [What data / stakeholder input informed this]

### Ordered Backlog

| Rank | Item | [Score/Category] | Rationale |
|------|------|-----------------|-----------|
| 1    | ...  | ...             | ...       |

### Prioritization Rationale
[Explain the key trade-off decisions -- why high-value items were deprioritized, why quick wins were elevated, etc.]

### Assumptions
[What assumptions were made that, if wrong, would change the ordering]
```

---

### Pattern 4: PRD (Product Requirements Document)

**Format:** Structured PRD suitable for engineering, design, and stakeholder review.

```
## Product Requirements Document

**Product / Feature:** [Name]
**Version:** [1.0]
**Author:** [Product Owner]
**Status:** [Draft / In Review / Approved]
**Last Updated:** [date]

---

### 1. Problem Statement
[What problem are we solving? For whom? Why now?]

### 2. Goals & Success Metrics
| Goal | Metric | Target | Baseline |
|------|--------|--------|----------|
| ... | ... | ... | ... |

### 3. User Personas
**Primary:** [Name] -- [Role, context, key need]
**Secondary:** [Name] -- [Role, context, key need]

### 4. User Stories (Summary)
[List story titles with links/references to full stories]

### 5. Functional Requirements
| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-01 | ... | Must Have | ... |

### 6. Non-Functional Requirements
| ID | Requirement | Type | Target |
|----|-------------|------|--------|
| NFR-01 | Response time < 200ms | Performance | p99 |

### 7. Out of Scope
[Explicit list of what is NOT included in this release]

### 8. Dependencies & Risks
| Dependency / Risk | Type | Owner | Mitigation |
|-------------------|------|-------|------------|
| ... | Dependency | ... | ... |

### 9. Timeline & Milestones
| Milestone | Target Date | Exit Criteria |
|-----------|-------------|---------------|
| ... | ... | ... |

### 10. Open Questions
| # | Question | Owner | Due |
|---|----------|-------|-----|
| 1 | ... | ... | ... |
```

---

### Pattern 5: Sprint Planning

**Format:** Sprint goal + committed stories with capacity reasoning.

```
## Sprint [N] Plan

**Sprint Goal:** [Single sentence -- the "why" of this sprint, not a list of tasks]
**Sprint Dates:** [Start] -> [End]
**Team Capacity:** [story points available after accounting for ceremonies, PTO, etc.]

### Committed Stories

| # | Story | Points | Assignee | Dependencies |
|---|-------|--------|----------|--------------|
| 1 | ...   | 5      | ...      | None         |

**Total Committed:** [X] points

### Commitment Rationale
[Why these stories? How do they serve the sprint goal? What was left out and why?]

### Risks to Sprint Goal
[What could prevent achieving the sprint goal? Mitigation?]

### Definition of Done (Sprint Level)
- [ ] All acceptance criteria pass
- [ ] Code reviewed and merged
- [ ] Tests written and passing
- [ ] Deployed to staging
- [ ] PO sign-off on acceptance criteria
```

---

### Pattern 6: Roadmap Item

**Format:** Outcome-oriented roadmap entry, not a feature list.

```
## Roadmap Item: [Initiative Name]

**Timeframe:** [Q1 2026 / H1 2026 / Now / Next / Later]
**Strategic Theme:** [Which OKR or strategy pillar this serves]
**Outcome:** [What changes for users / business when this is done]
**Key Features / Epics:** [High-level list -- not detailed stories]
**Success Metrics:** [How we'll measure success]
**Dependencies:** [What must be true before this can start]
**Confidence:** [High / Medium / Low] -- [reason]
```

---

### Pattern 7: Stakeholder Communication

**Format:** Audience-appropriate update. State the audience before drafting.

```
## [Artifact Type]: [Subject]

**Audience:** [Exec / Engineering / Design / External / All-hands]
**Purpose:** [Inform / Align / Decide / Celebrate]
**Date:** [date]

[Content tailored to audience -- executives get outcomes and metrics; engineering gets technical context and decisions; external gets user-facing language only]

**Key Decisions Made:**
- ...

**What's Next:**
- ...

**Questions / Actions Needed:**
- ...
```

---

### Pattern 8: Definition of Done / Definition of Ready

```
## Definition of Done -- [Team / Feature / Release level]

A story is Done when:
- [ ] All acceptance criteria verified by PO
- [ ] Unit tests written and passing (coverage >= X%)
- [ ] Integration tests passing
- [ ] Code reviewed by at least 1 peer
- [ ] No new high/critical bugs introduced
- [ ] Feature flagged if incomplete
- [ ] Deployed to staging environment
- [ ] Documentation updated (API docs, runbook, user guide as applicable)
- [ ] PO demo completed

## Definition of Ready

A story is Ready for sprint when:
- [ ] User story written in standard format
- [ ] Acceptance criteria complete and testable
- [ ] Dependencies identified and resolved or planned
- [ ] Sized by the team (story points assigned)
- [ ] UI/UX designs attached (if applicable)
- [ ] Technical approach agreed (if high-risk)
- [ ] No blocking questions remain
```

---

### Pattern 9: Retrospective

```
## Retrospective: [Sprint N]
**Format:** [format name]
**Date:** [date]
**Facilitator:** [name]
**Duration:** [time-boxed]

### Activity Results
[Format-specific content]

### Action Items
| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|

### Follow-Up from Previous Retro
[Status of prior action items]
```

---

### Pattern 10: Velocity/Metrics Analysis

```
## Velocity Analysis: [Team/Period]

### Trend Data
| Sprint | Committed | Completed | Velocity | Notes |
|--------|-----------|-----------|----------|-------|

### Analysis
[Trend interpretation, outliers, contributing factors]

### Forecast
[Based on last N sprints, projected capacity]

### Recommendations
[Process improvements suggested by the data]
```

---

### Pattern 11: Metrics Definition

```
## Metrics Definition: [Product/Feature]

### North Star Metric
**Metric:** [name]
**Definition:** [precise definition]
**Formula:** [calculation]
**Target:** [quantified target]

### Supporting Metrics
| Metric | Definition | Formula | Source | Owner | Cadence | Target |
|--------|-----------|---------|--------|-------|---------|--------|

### Dashboard Requirements
[What should be visualized, for whom, refresh cadence]
```

---

### Pattern 12: A/B Test Plan

```
## Experiment: [Name]

**Hypothesis:** If [change], then [effect], because [rationale]
**Primary Metric:** [metric + success threshold]
**Guardrail Metrics:** [metrics that must not regress]
**Sample Size:** [calculated minimum]
**Duration:** [estimated runtime]
**Segments:** [who is included/excluded]

### Variants
| Variant | Description |
|---------|------------|
| Control | [current behavior] |
| Treatment | [proposed change] |

### Success Criteria
[Statistical significance threshold, minimum detectable effect]

### Risks & Mitigations
[What could go wrong, how to detect, how to mitigate]
```

---

## Cross-Role Tasks

When a task spans multiple roles, load all relevant reference files into a single sub-agent.

| Scenario | Roles Involved | References Loaded |
|----------|---------------|-------------------|
| Sprint planning with ceremony facilitation | Product Owner + Scrum Bag | backlog-management.md + facilitation-patterns.md |
| Feature launch with success metrics | Product Owner + Data Analyst | user-stories.md + metrics-frameworks.md |
| Retrospective with velocity analysis | Scrum Bag + Data Analyst | retrospective-formats.md + agile-metrics.md + facilitation-patterns.md |
| PRD with analytics requirements | Product Owner + Data Analyst | user-stories.md + stakeholder-templates.md + analytics-patterns.md |
| Process improvement with data backing | Scrum Bag + Data Analyst | process-improvement.md + agile-metrics.md + analytics-patterns.md |
| Full sprint cycle (plan + facilitate + measure) | All three roles | backlog-management.md + facilitation-patterns.md + agile-metrics.md |
| OKR setting with metric definitions | Product Owner + Data Analyst | stakeholder-templates.md + metrics-frameworks.md |

---

## Quality Standards

Apply these checks to every artifact before output:

### Product Owner Guardrails

**For stories:**
- Each acceptance criterion is independently testable (a QA engineer can write a test from it)
- No "should", "might", "could" in acceptance criteria -- use "must" or present tense assertions
- User role is specific (not "user" -- e.g., "authenticated customer", "admin user", "guest visitor")
- Business value is explicit in the "so that" clause

**For prioritization:**
- Rationale is documented -- ordering is not just a number, it is a defensible decision
- Assumptions are explicit
- Trade-offs between items are named

**For PRDs:**
- Every functional requirement has an acceptance criterion
- Out of scope section is present and non-empty
- Success metrics are measurable (SMART)
- Open questions are tracked with owners

**For sprint planning:**
- Sprint goal is a single sentence expressing user/business value (not "complete stories X, Y, Z")
- Capacity accounts for ceremonies (planning, review, retro, refinement)
- Commitment does not exceed 80% of capacity (buffer for interruptions)

**For defect tracking:**
- Track defects/story rate per sprint as a product quality metric (target: <0.3)
- Review defect categories in retrospectives -- which are persistent?
- Prioritize plugin improvement PRs based on defect frequency and severity
- Monitor rate trend -- is the defect rate decreasing over time?
- Defect rate should be included in sprint retrospective data and reported to stakeholders

### Scrum Bag Guardrails

- Every retrospective must produce action items with assigned owners and due dates
- Velocity analysis must include at least 3 sprints of data for trend identification
- Metrics must have baselines before targets can be set
- Process improvement recommendations must be specific and actionable, not generic
- Ceremony facilitation guides must include time-boxes for each activity
- Team health assessments must preserve psychological safety -- no individual attribution of problems

### Data Analyst Guardrails

- Every metric must have a precise definition and a formula -- no ambiguous metrics
- Experiments must have a hypothesis stated before the test plan is designed
- Sample size calculations must be explicit -- no "run it and see"
- Dashboard designs must specify the audience and the decisions the dashboard supports
- Data quality assessments must define what "quality" means for each data field
- Reporting cadence must match the decision cadence -- daily metrics for daily decisions, weekly for weekly

---

## Sub-Agent Interface (Agentic Flow Integration)

When invoked as a worker agent within an orchestrated flow, accept and produce structured JSON-compatible inputs/outputs in addition to markdown artifacts.

**Input contract:**
```json
{
  "task_type": "user_story | epic_decomposition | backlog_prioritization | prd | sprint_planning | roadmap | stakeholder_comms | dod_dor | retrospective | process_improvement | velocity_analysis | ceremony_facilitation | impediment_removal | team_health | agile_assessment | analytics_requirements | metrics_definition | dashboard_design | ab_testing | data_quality | data_exploration | reporting",
  "role": "product_owner | scrum_master | data_analyst",
  "context": {
    "product": "string",
    "team": "string (optional)",
    "persona": "string (optional)",
    "constraint": "string (optional)",
    "existing_stories": ["array of story titles (optional)"],
    "prioritization_framework": "MoSCoW | RICE | WSJF | Kano (optional)",
    "sprint_number": "number (optional)",
    "metrics_framework": "HEART | AARRR | OKR (optional)",
    "baseline_data": "string (optional)"
  },
  "input": "string -- the raw request or description"
}
```

**Output contract:**
```json
{
  "task_type": "string",
  "role": "string",
  "artifact_title": "string",
  "artifact": "string (markdown)",
  "invest_issues": ["array -- empty if none (PO tasks only)"],
  "open_questions": ["array -- items needing human decision"],
  "action_items": ["array -- items with owners (SM tasks only)"],
  "metrics_defined": ["array -- metric names with definitions (DA tasks only)"],
  "downstream_ready": true,
  "downstream_notes": "string -- what the next agent needs to know"
}
```

`downstream_ready: false` means the artifact has open questions that must be resolved before a downstream agent can act on it. Always populate `open_questions` when `downstream_ready` is false.

---

## User Commands

### Product Owner Commands

| Command | Action |
|---------|--------|
| `split` | Split the current story -- it failed the Small criterion |
| `detail <story #>` | Expand a story title into full story + ACs |
| `score` | Apply RICE or WSJF scoring to the current backlog |
| `moscow` | Reformat backlog using MoSCoW categories |
| `refine` | Tighten acceptance criteria -- make them more specific and testable |
| `persona <name>` | Switch the user persona for story writing |
| `prd` | Expand current stories/epic into a full PRD |
| `sprint` | Produce a sprint plan from the current prioritized backlog |
| `accept` | Finalize and deliver the current artifact |

### Scrum Bag Commands

| Command | Action |
|---------|--------|
| `retro` | Start a retrospective using an appropriate format |
| `facilitate` | Produce a facilitation guide for a ceremony |
| `metrics` | Analyze velocity or other agile metrics |
| `assess` | Run an agile maturity assessment |

### Data Analyst Commands

| Command | Action |
|---------|--------|
| `dashboard` | Design a dashboard specification |
| `experiment` | Create an A/B test plan |

---

## References

### Product Owner

- `references/user-stories.md` -- Story templates, INVEST guide, AC patterns, splitting strategies
- `references/prioritization-frameworks.md` -- MoSCoW, RICE, WSJF, Kano formulas and worked examples
- `references/backlog-management.md` -- Refinement process, grooming cadence, backlog health metrics
- `references/stakeholder-templates.md` -- Communication templates by audience type

### Scrum Bag

- `references/retrospective-formats.md` -- Retro formats: Start/Stop/Continue, 4Ls, Sailboat, Mad/Sad/Glad, timeline
- `references/agile-metrics.md` -- Velocity, burndown, cycle time, lead time, cumulative flow, predictability
- `references/facilitation-patterns.md` -- Ceremony facilitation: timeboxes, engagement techniques, conflict resolution
- `references/process-improvement.md` -- Continuous improvement: root cause analysis, Kaizen, value stream mapping

### Data Analyst

- `references/analytics-patterns.md` -- Tracking plans, instrumentation, data pipelines, data quality frameworks
- `references/metrics-frameworks.md` -- HEART, AARRR, OKR metrics, North Star framework, metric trees
- `references/dashboard-design.md` -- Dashboard design principles, visualization selection, audience targeting
- `references/experimentation.md` -- A/B testing methodology, sample size calculation, statistical significance, guardrails
- `references/dependency-tracking.md` -- Story dependency tracking, risk register, cross-story dependency validation
- `references/estimation.md` -- Story point estimation, velocity tracking, capacity planning, calibration
- `references/retro-trends.md` -- Retrospective trend analysis: theme extraction, team health score, retro-of-retros summary
