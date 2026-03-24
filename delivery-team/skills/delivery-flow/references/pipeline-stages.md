# Pipeline Stage Definitions

## Artifact Output Location

All stage artifacts are written to `.delivery/artifacts/` in the current working directory. Each file is numbered by stage for clear ordering.

---

## Stage 1: Idea

### Purpose
Capture and structure the raw idea into a brief that downstream stages can work from.

### Entry Conditions
- User has provided an idea description (any format: sentence, paragraph, bullet points)
- Project type has been detected

### Sub-Flow
0. **Write initial pipeline state** -- Create `.delivery/state.md` with `status: in_progress`, `current_stage: 1`, empty stages_completed, and full config snapshot. Uses atomic write (state.tmp.md → state.md).
1. **GitHub issue input** (if GitHub integration prerequisites pass): Offer to run `gh issue list --state open` and select an existing issue as the idea input, rather than writing a new idea brief from scratch. If the user selects an issue, read it with `gh issue view <number>` and use its title, body, and labels as the raw input. Record the source issue number in the idea brief. See `references/github-integration.md`.
2. **Format the idea** into a structured brief. The orchestrator does this directly (no sub-agent needed for simple structuring). If the idea is complex or vague, spawn a Product Owner sub-agent (product-delivery skill, task_type: user_story) to help structure it.
3. **Identify key elements**: problem statement, target users, goals, constraints, initial scope
4. **Quality gate**: evaluate against Gate 1 criteria
5. **Self-correction**: if gate fails, prompt the user for clarification on missing elements (this is the one stage where asking the user is preferred over self-correction, since the input is the user's idea)

### DoD Validators
- Product Owner: completeness (problem, users, goals present)
- Architect: feasibility signal (is this buildable? any obvious blockers?)

### Output Artifact: `.delivery/artifacts/01-idea-brief.md`
```markdown
## Idea Brief

**Project Type**: [detected type]
**Date**: [date]

### Problem Statement
[What problem does this solve? For whom?]

### Target Users
- [Persona 1]: [brief description]
- [Persona 2]: [brief description]

### Goals
1. [Measurable goal]
2. [Measurable goal]

### Constraints
- [Known limitation or constraint]

### Initial Scope
[High-level scope description]

### Out of Scope (initial)
[What this is NOT]
```

---

## Stage 2: Refine

### Purpose
Transform the idea brief into a complete PRD with acceptance criteria, success metrics, and validated requirements.

### Entry Conditions
- `01-idea-brief.md` exists and passed Gate 1

### Sub-Flow
1. **Invoke Product Owner** (product-delivery skill, task_type: prd)
   - Input: idea brief + lessons from `memory/stages/<stage>.md` + hot lessons from `memory/index.md`
   - Output: draft PRD
2. **Invoke Data Analyst** (product-delivery skill, task_type: metrics_definition)
   - Input: PRD goals section
   - Output: success metrics with targets and measurement approach
3. **Merge** Data Analyst metrics into PRD
4. **Evaluator-Optimizer Loop**: QA Engineer (quality skill) evaluates PRD against Gate 2 criteria. If failures, route back to PO with specific feedback. Max 3 iterations.
5. **Adversarial Review**: Challenger questions requirements assumptions, identifies missing edge cases, rates confidence 1-5. If confidence <= 2, escalate to human immediately.
6. **Primary agent addresses** valid challenger findings
7. **Team DoD Validation**: PO (business value), Architect (technical feasibility), QA (testability)
8. **Human Checkpoint 1**: Present PRD summary for approval
9. **GitHub issue creation** (if `github.create_issues` is true): For each user story in the PRD, create a GitHub issue using `gh issue create`. Label by priority (P1=critical, P2=high, P3=medium, P4=low). Include acceptance criteria as a checklist in the issue body. Link back to the PRD artifact path. Record issue numbers in the PRD artifact under a "GitHub Issues" section. See `references/github-integration.md`.

### DoD Validators
- Product Owner: business value clear, stories are valuable
- Architect: technically feasible, no obvious blockers
- QA Engineer: requirements are testable, acceptance criteria are specific

### Output Artifact: `.delivery/artifacts/02-prd.md`

### Game Dev Additions
- UX Designer also reviews for game UX patterns
- Game-specific NFRs added (FPS targets, input latency, platform requirements)

---

## Stage 3: Design

### Purpose
Create user experience design: flows, wireframes, interaction patterns, and accessibility considerations.

### Entry Conditions
- `02-prd.md` exists and passed Gate 2 + human approval

### Sub-Flow
1. **Invoke UX Designer** (ui skill, task_type: user-flow)
   - Input: PRD user stories and personas
   - Output: user flows for all key journeys
2. **Invoke UX Designer** (ui skill, task_type: wireframe)
   - Input: user flows
   - Output: wireframes for key screens
3. **Invoke UI Designer** (ui skill, task_type: component-spec or design-system)
   - Input: wireframes
   - Output: component specifications, design tokens
4. **Invoke UI Designer** (ui skill, task_type: accessibility-review)
   - Input: wireframes + component specs
   - Output: accessibility findings
5. **Multi-Perspective Review Board**: Architect (implementability) + PO (requirement coverage) + QA (testability). Any BLOCK must be resolved.
6. **Team DoD Validation**: UX (design quality), PO (coverage), QA (testability), Architect (implementability)

### DoD Validators
- UX Designer: flows are complete and follow UX best practices
- Product Owner: all PRD requirements are covered in the design
- QA Engineer: designs are testable (clear states, measurable outcomes)
- Architect: designs are implementable (no impossible interactions)

### Output Artifact: `.delivery/artifacts/03-ux-design.md`

### Game Dev Additions
- Game UI Designer (ui skill) invoked for HUD, menu, inventory UI patterns
- Game-specific accessibility review (colorblind modes, subtitle systems, input remapping)

---

## Stage 4: Architect

### Purpose
Create technical architecture: system design, C4 models, ADRs, technology decisions.

### Entry Conditions
- `02-prd.md` exists (required)
- `03-ux-design.md` exists if Design stage ran

### Sub-Flow
1. **Domain Discovery Interview** (architect skill, references/domain-discovery.md)
   - Invoke PO (product-delivery skill) with decomposition-specific questions
   - Evaluate answers: sufficient → proceed, partial → follow up, insufficient → escalate to human
   - Record findings as "Domain Discovery" section in architecture artifact
   - If escalation needed: present unanswered questions with architectural impact and suggested respondents
2. **Invoke Architect** (architect skill, task_type: design, role: solution)
   - Input: PRD + UX design (if available) + domain discovery findings + memory lessons
   - Output: system architecture with C4 diagram descriptions
3. **For contested decisions** -- run **Debate Pattern**:
   - Frame the choice (e.g., "microservices vs monolith")
   - PRO agent argues Option A, CON agent argues Option B
   - JUDGE (Enterprise Architect) decides
   - Produce ADR for each debate
4. **Invoke Security Architect** (architect skill, task_type: security-design)
   - Input: system architecture
   - Output: security review findings
5. **Evaluator-Optimizer Loop**: QA reviews for testability, DevOps reviews for deployability. Route findings back to Architect. Max 2 iterations.
6. **Adversarial Review**: Challenger questions architecture assumptions, rates confidence
7. **Team DoD Validation**: Architect (soundness), QA (testability), DevOps (deployability), Security (posture)
8. **Human Checkpoint 2**: Present architecture summary for approval

### DoD Validators
- Architect: design is sound, trade-offs documented, patterns appropriate
- QA Engineer: architecture supports testing (observability, isolation)
- DevOps: architecture is deployable (CI/CD compatible, environment strategy)
- Security: security concerns addressed

### Output Artifacts
- `.delivery/artifacts/04-architecture.md`
- `.delivery/artifacts/04a-adrs/ADR-001.md` (one per major decision)

### Game Dev Additions
- Game architecture roles invoked: Game Systems, Level/World, Network/Multiplayer, Graphics/Rendering as relevant
- Performance budgets required (frame time, memory, bandwidth)

---

## Stage 5: Plan

### Purpose
Create sprint plan with stories, estimates, test strategy, and deployment approach.

### Entry Conditions
- `02-prd.md` exists (required)
- `04-architecture.md` exists if Architect stage ran

### Sub-Flow
1. **Invoke Product Owner** (product-delivery skill, task_type: user_story)
   - Input: PRD
   - Output: detailed user stories with acceptance criteria
2. **Invoke QA Engineer** (quality skill, task_type: test-cases) — REQUIRED per story
   - Input: each user story's acceptance criteria
   - Output: test cases per story (these are part of the story artifact, not separate)
   - Test cases MUST be produced alongside stories, not as a separate optional step
   - Each story's output includes: story + acceptance criteria + test cases
3. **Invoke Scrum Bag** (product-delivery skill, task_type: sprint_planning)
   - Input: user stories (with test cases) + architecture constraints
   - Output: sprint plan draft
4. **Invoke QA Engineer** (quality skill, task_type: test-strategy)
   - Input: PRD + architecture + user stories + test cases
   - Output: overall test strategy (in addition to per-story test cases)
5. **Invoke DevOps** (operations skill, task_type: deployment-strategy)
   - Input: architecture
   - Output: deployment plan
6. **Consensus Protocol**: SM, PO, QA, DevOps independently estimate and identify risks, then share, respond, and converge. 2-3 rounds.
7. **Adversarial Review**: Challenger questions estimates and risk assessments
8. **Team DoD Validation**: SM (process), PO (scope), QA (coverage), DevOps (readiness)
9. **Git branch creation** (if `git.auto_branch` is true): Create feature branch from main (or develop for GitFlow) using the configured `git.branch_strategy`. Branch name: `feature/<issue-number>-<short-description>`. Verify clean working tree before branching. If the branch already exists, append a numeric suffix. Record branch name in `.delivery/state.md`. See `references/git-integration.md`.
10. **Human Checkpoint 3**: Present sprint plan for approval

### DoD Validators
- Scrum Bag: process is sound, capacity realistic
- Product Owner: scope is correct, stories are valuable
- QA Engineer: test strategy covers critical paths
- DevOps: deployment approach is viable

### Output Artifact: `.delivery/artifacts/05-sprint-plan.md`

### Light Mode (BUG_FIX, DOCS_ONLY)
- PO writes a single story for the fix/doc task
- SM produces minimal plan (no full sprint plan)
- Skip consensus protocol and adversarial review
- QA still validates testability

---

## Stage 6: Development

### Purpose
Implement the code, write tests, and produce development documentation.

### Entry Conditions
- `05-sprint-plan.md` exists if Plan stage ran
- At minimum: user stories with acceptance criteria must exist

### Sub-Flow
For each story in the sprint plan:
1. **Invoke Developer** (developer skill, task_type: write)
   - Input: user story + acceptance criteria + architecture constraints
   - Output: implementation code
2. **Evaluator-Optimizer Loop**: QA Engineer reviews code against acceptance criteria + coding standards. Route back with feedback. Max 3 iterations per story.
3. **Decision Ownership Routing**: If issues arise:
   - Scope questions -> Product Owner
   - Technical questions -> Architect
   - Quality questions -> QA Engineer
4. **Invoke Technical Writer** (operations skill, task_type: api-docs or runbook) if applicable
5. **Commit suggestion** (if `git.commit_convention` is "conventional"): Suggest a conventional commit message based on the story type. Format: `<type>(<scope>): <description>`. Do NOT auto-commit -- present the suggestion for the user to review and execute. See `references/git-integration.md`.
6. **Team DoD Validation per story**: Developer (quality), QA (tests), Architect (conformance), Tech Writer (docs)

### DoD Validators (per story)
- Developer: code is clean, follows language best practices
- QA Engineer: tests pass, coverage adequate
- Architect: implementation conforms to architecture decisions
- Technical Writer: inline docs and any required external docs present

### Output Artifacts
- Actual code files (in the project codebase)
- `.delivery/artifacts/06-dev-notes.md` (summary of implementation decisions, known issues)

### Milestone Testing (all project types)

After each sprint's stories pass DoD, run a milestone validation session using the quality skill's `references/milestone-testing.md`. The protocol is project-type-specific:

- **Web/React**: 20 min — responsive breakpoints, form flows, accessibility, Core Web Vitals
- **API/Backend**: 15 min — auth flow, CRUD cycle, error handling, contract testing
- **Enterprise/B2B**: 25 min — multi-tenant isolation, RBAC, audit logs, compliance
- **Mobile**: 20 min — offline/resume, permissions, interruptions, touch targets
- **CLI**: 15 min — pipe compatibility, exit codes, flag combinations, config precedence

Each session uses role-specific checklists (PO, QA, Dev, Architect/UX) and cross-feature interaction questions. Findings classified as Bug, UX, Performance, Spec Gap, or Integration Issue. Bugs → `.delivery/defects/`, rest → backlog.

### Game Dev Additions
- Godot skill invoked for Godot engine projects
- Game-specific testing (playtest scenarios, performance profiling)
- **Milestone playtest checkpoint**: After each sprint that delivers playable/empirical features, run a structured 15-minute playtest session using the quality skill's `references/exploratory-testing.md` milestone protocol. Use role-specific checklists (PO: gameplay feel, QA: cross-story interactions, Dev: performance). Classify findings as Bug, Balance, UX, Narrative, Spec Gap, or Performance. Bugs go to `.delivery/defects/`, everything else becomes backlog items for the next sprint.

---

## Stage 7: UAT

### Purpose
Execute user acceptance testing, prepare release artifacts, and get final approval.

### Entry Conditions
- Development stage complete (all stories pass DoD)
- `06-dev-notes.md` exists

### Sub-Flow
1. **Invoke QA Engineer** (quality skill, task_type: test-plan)
   - Input: PRD acceptance criteria + developed features
   - Output: UAT test plan with test cases
2. **Invoke QA Engineer** (quality skill, task_type: test-cases)
   - Input: test plan
   - Output: detailed test cases with expected results
3. **Execute test descriptions** (describe how to test; actual execution depends on test framework availability)
4. **Exploratory testing sessions** (quality skill, task_type: exploratory-testing)
   - For GAME_DEV: 2 sessions — Feature Tour (play all implemented features) + Cross-Story Regression (test interactions between stories modifying shared values)
   - For all types: 1 session — Cross-Story Interaction (test that independently-completed stories work together)
   - Each session has a charter, is time-boxed, and produces observation notes (not pass/fail)
   - Any bugs found are logged to `.delivery/defects/` immediately
   - See the quality skill's `references/exploratory-testing.md` for session format and heuristics
5. **Invoke DevOps** (operations skill, task_type: release-plan + rollback-procedure)
   - Input: architecture + deployment strategy
   - Output: release plan with rollback procedure
6. **Invoke Technical Writer** (operations skill, task_type: release-notes + user-guide)
   - Input: PRD + dev notes + features implemented
   - Output: release notes, user guide updates
7. **Working tree validation** (if `git.clean_tree_check` is true): Run `git status --porcelain`. If not clean, list uncommitted changes and warn: "Working tree has uncommitted changes. Commit or stash before UAT acceptance." Do not block -- present the warning and let the user decide. See `references/git-integration.md`.
8. **PR creation** (if `github.create_pr` is true): Create a pull request using `gh pr create` with: title from sprint goal, body with change summary + stories implemented (with "Closes #N" for each linked issue) + test results from UAT report + release notes. Label by project type. Record the PR URL in the UAT report artifact. See `references/github-integration.md`.
9. **Multi-Perspective Review Board**: QA (tests) + DevOps (release readiness) + Tech Writer (docs). Go/no-go recommendation.
10. **Team DoD Validation**: QA (tests pass), DevOps (rollback ready), PO (acceptance), Tech Writer (docs complete)
11. **Human Checkpoint 4**: Present UAT results for accept/reject

### DoD Validators
- QA Engineer: all tests pass, no critical defects
- DevOps: deployment plan complete, rollback tested/documented
- Product Owner: delivered features match expectations
- Technical Writer: all documentation complete and accurate

### Output Artifacts
- `.delivery/artifacts/07-uat-report.md`
- `.delivery/artifacts/07a-release-plan.md`
- `.delivery/artifacts/07b-documentation.md`

### Post-Acceptance
After human accepts:
0. **Pipeline state cleanup** -- Set state.md status to `completed`, then delete the state file. Artifacts and memory persist independently.
1. **Invoke Scrum Bag** (product-delivery skill, task_type: retrospective) -- capture lessons. This step is MANDATORY — the Stop hook enforces it.
2. **Write run archive** to `memory/archive/run-YYYY-MM-DD-<id>.md`
3. **Extract and route lessons** to stage chunks (`memory/stages/*.md`) and topic chunks (`memory/topics/*.md`)
4. **Rebuild routing index** (`memory/index.md`) with updated stats and hot lessons
5. **Defect review** — analyze defects found during this run:
   - Log all defects to `.delivery/defects/sprint-N.md`
   - Calculate defects/story rate
   - Classify as one-off vs systemic (see `references/defect-tracking.md`)
   - For systemic patterns: draft plugin improvement PRs
   - Update `.delivery/defects/index.md`
   - Update `memory/topics/defect-patterns.md`
See `references/memory-protocol.md` for the full tiered memory protocol.
6. Pipeline complete
