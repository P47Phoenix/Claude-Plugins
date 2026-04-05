# Pipeline Stages

The delivery pipeline has 7 stages. Each stage produces artifacts, runs quality gates, and validates through a team Definition of Done before advancing.

## Stage Overview

| # | Stage | Purpose | Primary Agent | Human Checkpoint |
|---|-------|---------|---------------|:----------------:|
| 1 | **Idea** | Capture and structure the raw idea | Product Owner | No |
| 2 | **Refine** | Write PRD with stories and acceptance criteria | Product Owner | Yes (configurable) |
| 3 | **Design** | Create user flows and wireframes | UX Designer | No |
| 4 | **Architect** | Design system architecture | Architect | Yes (configurable) |
| 5 | **Plan** | Sprint plan with tasks and test cases | Scrum Master | Yes (configurable) |
| 6 | **Development** | Implement stories | Developer | No |
| 7 | **UAT** | User Acceptance Testing | QA Engineer | Yes (always) |

---

## Stage Details

### Stage 1: Idea

**Purpose**: Capture and structure the raw idea into a brief that downstream stages can work from.

**Entry conditions**: User has provided an idea description (any format).

**What happens**:

1. The orchestrator formats the idea into a structured brief (or spawns PO for complex ideas)
2. Key elements identified: problem statement, target users, goals, constraints, scope
3. Quality gate evaluates completeness
4. If the gate fails, the user is asked for clarification

**DoD Validators**: Product Owner (completeness), Architect (feasibility)

**Output**: `.delivery/artifacts/01-idea/po/idea-brief.md`

---

### Stage 2: Refine

**Purpose**: Transform the idea brief into a complete Product Requirements Document.

**What happens**:

1. Product Owner writes a PRD with user stories, acceptance criteria, personas, and NFRs
2. Data Analyst contributes analytics requirements (if applicable)
3. Evaluator-optimizer loop reviews quality
4. Adversarial review challenges requirements completeness
5. Human checkpoint (if enabled): you review and approve the PRD

**DoD Validators**: Product Owner, Architect, QA Engineer

**Output**: `.delivery/artifacts/02-refine/po/prd.md`

---

### Stage 3: Design

**Purpose**: Create user experience design from the PRD.

**What happens**:

1. UX Designer creates user flows, wireframes, and navigation structure
2. For game projects: Game UI Designer reviews HUD, menus, and game-specific UX
3. Quality gate evaluates design completeness and usability

**DoD Validators**: UX Designer, Product Owner, QA Engineer, Architect

**Output**: `.delivery/artifacts/03-design/ux/design.md`

---

### Stage 4: Architect

**Purpose**: Design the technical architecture for the system.

**What happens**:

1. Domain discovery interview (Architect queries PO for business context)
2. Architect designs component decomposition, data models, API contracts
3. Architecture Decision Records (ADRs) produced for key decisions
4. Evaluator-optimizer loop reviews against quality attributes
5. Adversarial review challenges design decisions and trade-offs
6. Human checkpoint (if enabled): you approve the architecture

**DoD Validators**: Architect, QA Engineer, DevOps, Security

**Output**: `.delivery/artifacts/04-architect/architect/architecture.md`

---

### Stage 5: Plan

**Purpose**: Create an implementable sprint plan.

**What happens**:

1. Scrum Master breaks stories into implementable tasks
2. QA Engineer contributes test cases for each story
3. DevOps provides deployment considerations
4. Adversarial review challenges estimates and risk assessments
5. Human checkpoint (if enabled): you approve the plan

**DoD Validators**: Scrum Master, Product Owner, QA Engineer, DevOps

**Output**: `.delivery/artifacts/05-plan/sm/sprint-plan.md`

---

### Stage 6: Development

**Purpose**: Implement the planned stories.

**What happens**:

1. Developer implements each story against acceptance criteria
2. QA Engineer reviews each implementation (evaluator-optimizer loop)
3. Self-correction loops handle issues (up to configured max iterations)
4. For game projects: Godot skill invoked alongside Developer skill
5. Technical Writer produces documentation artifacts

**DoD Validators**: Developer, QA Engineer, Architect, Technical Writer

**Output**: `.delivery/artifacts/06-dev/developer/` (per-story artifacts)

---

### Stage 7: UAT

**Purpose**: Validate the deliverables meet acceptance criteria.

**What happens**:

1. QA Engineer runs acceptance test scenarios
2. Simulated personas test the deliverables (user-feedback skill)
3. DevOps validates deployment readiness
4. Human checkpoint (always): you review and accept or reject
5. On acceptance: pipeline completes, retrospective runs, memory written

**DoD Validators**: QA Engineer, DevOps, Product Owner, Technical Writer

**Output**: `.delivery/artifacts/07-uat/qa/uat-report.md`

---

## Stage Routing Matrix

Not every project type runs all stages. The routing matrix determines which stages execute and at what depth:

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

- **Full** — All agents invoked, all collaboration patterns, full quality gate, full team DoD, max 3 self-correction iterations
- **Light** — Primary agent only, blocking criteria only, reduced DoD (primary + 1 reviewer), max 2 iterations. Light means reduced depth, NOT skipped.
- **Skip** — Stage does not execute. Pipeline advances to next active stage.
- **Full+Game** — Everything in Full, plus game-specific augmentations (Game UI at Design, game architecture at Architect, engine skill at Dev, playtest scenarios at UAT)

## Quality Gates

Every stage artifact must pass quality gates before advancing. The process:

1. Stage produces its primary artifact
2. Collaboration patterns run (evaluator-optimizer, adversarial review, etc.)
3. Revised artifact submitted to DoD validators
4. **All validators must return DONE** for the stage to advance
5. Any NOT_DONE triggers self-correction with targeted feedback
6. After max iterations, unresolved findings escalate to the user
