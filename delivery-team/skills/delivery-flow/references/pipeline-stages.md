# Pipeline Stage Definitions

## Artifact Output Location

All stage artifacts are written to `.delivery/artifacts/` using the namespaced convention:

```
.delivery/artifacts/{NN}-{stage-name}/{role}/{artifact-name}.md
```

Each sub-agent writes to its own dedicated directory. No two agents share a write path. The orchestrator's only write paths are `stage-summary.md` (routing metadata) and `.delivery/state.md` (pipeline state).

### Dispatch Annotations

Each sub-flow step below is annotated with:
- **[PARALLEL]** or **[SEQUENTIAL]**: whether the step can run concurrently with other steps
- **[required]** or **[optional]**: whether the agent's output is mandatory for stage completion

> **One role = one Agent tool call.** The `[PARALLEL]` and `[SEQUENTIAL]`
> annotations imply **one Agent tool call per listed role**. When a step
> lists N roles to run in parallel, the orchestrator dispatches N separate
> Agent tool calls in a single message. Never combine multiple roles into
> a single sub-agent invocation — even when the roles look similar, even
> when one role's output is brief, even when it would be faster. Compound
> multi-role prompts are a Prime Directive violation and are detected by
> `audit_agent_prompt.py`. See SKILL.md "One Role = One Sub-Agent" and
> `references/team-patterns.md` for the full dispatch contract.

---

## Agent Invocation Templates

All agent dispatches -- primary, supporting, and DoD validator -- use the templates below. These templates ensure every agent receives the full prompt context including personality injection when an alias theme is active.

> **ALIAS block protocol**: The `--- ALIAS ---` section is populated using the personality_strength protocol from SKILL.md Phase 4 Step 4. The orchestrator looks up the agent's role ID in the active theme's `roles` map and injects the personality block at the configured strength level:
> - **light**: `You are {character}. {personality}`
> - **moderate**: `You are {character}. {personality} Style: {style}. Example: "{examples[0]}"`
> - **full**: `You are {character}. {personality} Style: {style}. Catchphrase: "{catchphrase}". Examples: "{examples[0]}" / "{examples[1]}". Stay in character throughout your response.`
>
> The `--- ALIAS ---` block is **omitted entirely** when:
> - The theme is `business` (no personality injection)
> - The agent's role has no entry in the active theme (partial theme -- falls back to default professional tone)

### Primary Agent Dispatch Template

Used when invoking the main worker for a stage (e.g., PO for Refine, Architect for Stage 4, Developer for Stage 6).

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {primary_skill}
TASK_TYPE: {task_type}
ROLE: {role}

Begin your response with "SKILL_LOADED: {primary_skill}" to confirm skill activation.

--- TASK ---
{task_description}

--- INPUT ARTIFACTS (read these files) ---
{for each upstream artifact:}
- {artifact_file_path}: {description}

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}
{stage_lessons_if_loaded}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your artifact to: {output_file_path}

When complete, respond with ONLY this signal block:
STATUS: {DONE | NOT_DONE | CODE_COMPLETE}
ARTIFACT: {output_file_path}
SUMMARY: {one sentence, max 200 characters}
{if NOT_DONE: FINDINGS: {bullet list of specific issues}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

### Supporting Agent Dispatch Template

Used when invoking supplementary workers (e.g., Data Analyst in Refine, DevOps in Plan, Tech Writer in Development). Supporting agents receive the same prompt structure as primary agents but are dispatched alongside or after the primary agent.

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {supporting_skill}
TASK_TYPE: {task_type}
ROLE: {role}

Begin your response with "SKILL_LOADED: {supporting_skill}" to confirm skill activation.

--- TASK ---
{task_description}

--- INPUT ARTIFACTS (read these files) ---
{for each upstream artifact:}
- {artifact_file_path}: {description}

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}
{stage_lessons_if_loaded}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your artifact to: {output_file_path}

When complete, respond with ONLY this signal block:
STATUS: {DONE | NOT_DONE}
ARTIFACT: {output_file_path}
SUMMARY: {one sentence, max 200 characters}
{if NOT_DONE: FINDINGS: {bullet list of specific issues}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

### DoD Validator Dispatch Template

Used when invoking DoD validators at the end of each stage. All validators for a stage are dispatched in parallel in a single message. Each validator writes to its own namespaced path under `{stage}/dod/`.

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {validator_skill}
TASK_TYPE: dod-validation
ROLE: {validator_role}

Begin your response with "SKILL_LOADED: {validator_skill}" to confirm skill activation.

--- TASK ---
Validate the stage artifacts against the Definition of Done criteria for your
domain. For each criterion, state PASS or FAIL. If FAIL: cite the specific
artifact section, explain WHY it fails, and provide an actionable fix.
ALL validators must say DONE for the stage to advance.

{role_specific_dod_criteria}

--- INPUT ARTIFACTS (read these files) ---
{for each stage artifact:}
- {artifact_file_path}: {description}

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}
{stage_lessons_if_loaded}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- OUTPUT ---
Write your review to: {stage}/dod/{role}-review.md

When complete, respond with ONLY this signal block:
STATUS: {DONE | NOT_DONE}
ARTIFACT: {stage}/dod/{role}-review.md
SUMMARY: {one sentence, max 200 characters}
{if NOT_DONE: FINDINGS: {bullet list of specific failures}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

---

## Stage 1: Idea

### Purpose
Capture and structure the raw idea into a brief that downstream stages can work from.

### Entry Conditions
- User has provided an idea description (any format: sentence, paragraph, bullet points)
- Project type has been detected

### Sub-Flow
0. **Write initial pipeline state** [SEQUENTIAL] -- Create `.delivery/state.md` with `status: in_progress`, `current_stage: 1`, empty stages_completed, and full config snapshot. Uses atomic write (state.tmp.md -> state.md).
1. **GitHub issue input** [SEQUENTIAL] (if GitHub integration prerequisites pass): Offer to run `gh issue list --state open` and select an existing issue as the idea input, rather than writing a new idea brief from scratch. If the user selects an issue, read it with `gh issue view <number>` and use its title, body, and labels as the raw input. Record the source issue number in the idea brief. See `references/github-integration.md`.
2. **Format the idea** [SEQUENTIAL] into a structured brief. The orchestrator does this directly (no sub-agent needed for simple structuring). If the idea is complex or vague, spawn a Product Owner sub-agent (product-delivery skill, task_type: user_story) to help structure it.
3. **Identify key elements** [SEQUENTIAL]: problem statement, target users, goals, constraints, initial scope
4. **Quality gate** [SEQUENTIAL]: evaluate against Gate 1 criteria
5. **Self-correction** [SEQUENTIAL]: if gate fails, prompt the user for clarification on missing elements (this is the one stage where asking the user is preferred over self-correction, since the input is the user's idea)

### DoD Validators [PARALLEL] -- dispatch all in a single message
- Product Owner [required]: completeness (problem, users, goals present)
  - Writes to: `.delivery/artifacts/01-idea/dod/po-review.md`
- Architect [required]: feasibility signal (is this buildable? any obvious blockers?)
  - Writes to: `.delivery/artifacts/01-idea/dod/architect-review.md`

### Output Artifact: `.delivery/artifacts/01-idea/po/idea-brief.md`
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
1. **Invoke Product Owner** [SEQUENTIAL] [required] (product-delivery skill, task_type: prd)
   - SKILL: `delivery-team:product-delivery`, TASK_TYPE: `prd`, ROLE: `po`
   - Input artifacts: `.delivery/artifacts/01-idea/po/idea-brief.md`
   - Output: `.delivery/artifacts/02-refine/po/prd.md`
2. **Invoke Data Analyst** [SEQUENTIAL after step 1] [optional] (product-delivery skill, task_type: metrics_definition)
   - SKILL: `delivery-team:product-delivery`, TASK_TYPE: `metrics_definition`, ROLE: `data-analyst`
   - Input artifacts: `.delivery/artifacts/02-refine/po/prd.md` (goals section)
   - Output: `.delivery/artifacts/02-refine/data-analyst/metrics.md`
3. **Merge** [SEQUENTIAL] Data Analyst metrics into PRD (PO revises with metrics file path)
4. **Evaluator-Optimizer Loop** [SEQUENTIAL] [required]: QA Engineer (quality skill) evaluates PRD against Gate 2 criteria. If failures, route back to PO with specific feedback. Max 3 iterations.
   - Evaluator writes to: `.delivery/artifacts/02-refine/qa-evaluator/evaluation-round-{N}.md`
5. **Adversarial Review** [SEQUENTIAL after eval-opt] [required]: Challenger questions requirements assumptions, identifies missing edge cases, rates confidence 1-5. If confidence <= 2, escalate to human immediately.
   - Challenger writes to: `.delivery/artifacts/02-refine/challenger/challenge.md`
6. **Primary agent addresses** [SEQUENTIAL] valid challenger findings (receives artifact path + challenge path)
7. **Team DoD Validation** [PARALLEL] -- dispatch all validators in a single message: PO (business value), Architect (technical feasibility), QA (testability)
8. **Human Checkpoint 1** [SEQUENTIAL]: Present PRD summary for approval
9. **GitHub issue creation** [SEQUENTIAL] (if `github.create_issues` is true): For each user story in the PRD, create a GitHub issue using `gh issue create`. Label by priority (P1=critical, P2=high, P3=medium, P4=low). Include acceptance criteria as a checklist in the issue body. Link back to the PRD artifact path. Record issue numbers in the PRD artifact under a "GitHub Issues" section. See `references/github-integration.md`.

### DoD Validators [PARALLEL] -- dispatch all in a single message
- Product Owner [required]: business value clear, stories are valuable
  - Writes to: `.delivery/artifacts/02-refine/dod/po-review.md`
- Architect [required]: technically feasible, no obvious blockers
  - Writes to: `.delivery/artifacts/02-refine/dod/architect-review.md`
- QA Engineer [required]: requirements are testable, acceptance criteria are specific
  - Writes to: `.delivery/artifacts/02-refine/dod/qa-review.md`

### Output Artifact: `.delivery/artifacts/02-refine/po/prd.md`

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
1. **Invoke UX Designer** [SEQUENTIAL] [required] (ui skill, task_type: user-flow)
   - SKILL: `delivery-team:ui`, TASK_TYPE: `user-flow`, ROLE: `ux`
   - Input artifacts: `.delivery/artifacts/02-refine/po/prd.md`
   - Output: `.delivery/artifacts/03-design/ux/user-flows.md`
2. **Invoke UX Designer** [SEQUENTIAL after step 1] [required] (ui skill, task_type: wireframe)
   - SKILL: `delivery-team:ui`, TASK_TYPE: `wireframe`, ROLE: `ux`
   - Input artifacts: `.delivery/artifacts/03-design/ux/user-flows.md`
   - Output: `.delivery/artifacts/03-design/ux/wireframes.md`
3. **Invoke UI Designer** [SEQUENTIAL after step 2] [required] (ui skill, task_type: component-spec or design-system)
   - SKILL: `delivery-team:ui`, TASK_TYPE: `component-spec`, ROLE: `ui`
   - Input artifacts: `.delivery/artifacts/03-design/ux/wireframes.md`
   - Output: `.delivery/artifacts/03-design/ui/component-specs.md`
4. **Invoke UI Designer** [SEQUENTIAL after step 3] [required] (ui skill, task_type: accessibility-review)
   - SKILL: `delivery-team:ui`, TASK_TYPE: `accessibility-review`, ROLE: `ui`
   - Input artifacts: `.delivery/artifacts/03-design/ux/wireframes.md`, `.delivery/artifacts/03-design/ui/component-specs.md`
   - Output: `.delivery/artifacts/03-design/ui/accessibility.md`
5. **Multi-Perspective Review Board** [PARALLEL] [required]: Architect (implementability) + PO (requirement coverage) + QA (testability). ALL reviewers dispatched in parallel. Any BLOCK must be resolved.
   - Each reviewer writes to: `.delivery/artifacts/03-design/review-board/{role}-review.md`
6. **Team DoD Validation** [PARALLEL] -- dispatch all validators in a single message: UX (design quality), PO (coverage), QA (testability), Architect (implementability)

### DoD Validators [PARALLEL] -- dispatch all in a single message
- UX Designer [required]: flows are complete and follow UX best practices
  - Writes to: `.delivery/artifacts/03-design/dod/ux-review.md`
- Product Owner [required]: all PRD requirements are covered in the design
  - Writes to: `.delivery/artifacts/03-design/dod/po-review.md`
- QA Engineer [required]: designs are testable (clear states, measurable outcomes)
  - Writes to: `.delivery/artifacts/03-design/dod/qa-review.md`
- Architect [required]: designs are implementable (no impossible interactions)
  - Writes to: `.delivery/artifacts/03-design/dod/architect-review.md`

### Output Artifacts
- `.delivery/artifacts/03-design/ux/user-flows.md`
- `.delivery/artifacts/03-design/ux/wireframes.md`
- `.delivery/artifacts/03-design/ui/component-specs.md`
- `.delivery/artifacts/03-design/ui/accessibility.md`

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
0. **Impact Analysis Gate** [SEQUENTIAL] -- scan the new feature's PRD for entity references, query
   existing Feature Knowledge Cards in `.delivery/features/`, detect assumption conflicts,
   score risk, and present findings. CRITICAL conflicts block, HIGH/MEDIUM require
   acknowledgment. See `references/feature-knowledge.md`.
1. **Domain Discovery Interview** [SEQUENTIAL] [required] (architect skill, references/domain-discovery.md)
   - Invoke PO (product-delivery skill) with decomposition-specific questions
   - Evaluate answers: sufficient -> proceed, partial -> follow up, insufficient -> escalate to human
   - Record findings as "Domain Discovery" section in architecture artifact
   - If escalation needed: present unanswered questions with architectural impact and suggested respondents
2. **Invoke Architect** [SEQUENTIAL after step 1] [required] (architect skill, task_type: design, role: solution)
   - SKILL: `delivery-team:architect`, TASK_TYPE: `design`, ROLE: `solution`
   - Input artifacts: `.delivery/artifacts/02-refine/po/prd.md`, `.delivery/artifacts/03-design/ux/user-flows.md` (if available), domain discovery findings
   - Output: `.delivery/artifacts/04-architect/solution/architecture.md`
3. **Debate Pattern** [PARALLEL PRO+CON, then SEQUENTIAL JUDGE] [required for contested decisions]:
   - Frame the choice (e.g., "microservices vs monolith")
   - PRO writes to: `.delivery/artifacts/04-architect/debate-pro/argument.md`
   - CON writes to: `.delivery/artifacts/04-architect/debate-con/argument.md`
   - PRO + CON dispatched in parallel (single message with 2 Agent calls)
   - JUDGE receives both file paths, writes to: `.delivery/artifacts/04-architect/debate-judge/decision.md`
   - Produce ADR for each debate
4. **Invoke Security Architect** [SEQUENTIAL after step 2] [required] (architect skill, task_type: security-design)
   - SKILL: `delivery-team:architect`, TASK_TYPE: `security-design`, ROLE: `security`
   - Input artifacts: `.delivery/artifacts/04-architect/solution/architecture.md`
   - Output: `.delivery/artifacts/04-architect/security/security-review.md`
5. **Evaluator-Optimizer Loop** [SEQUENTIAL] [required]: QA reviews for testability, DevOps reviews for deployability. Route findings back to Architect. Max 2 iterations.
   - Evaluator writes to: `.delivery/artifacts/04-architect/qa-evaluator/evaluation-round-{N}.md`
6. **Isolated Adversarial Loop** [SEQUENTIAL after eval-opt, multi-iteration] [required]:
   Replaces the single-pass Adversarial Review at Stage 4. Each loop iteration
   dispatches a **fresh** reviewer sub-agent (one Agent tool call per loop) with
   zero prior-loop context — no prior findings, no loop number, no fix summaries.
   Reviewers tag findings with the fixed class taxonomy
   (`coupling | security | data-integrity | naming | testability | performance | docs`;
   untagged = `misc` = new class). Between loops, the Architect is re-dispatched
   (another fresh Agent call) to address the **current** loop's findings only.
   Convergence rules (ADR-003):
     (1) **Two-clean**: two consecutive zero-finding loops → `converged (two_clean)`
     (2) **No-new-classes**: two consecutive loops whose classes are all subsets
         of classes raised in earlier loops → `converged (class_saturated)` with
         residuals documented
     (3) **Hard cap**: `N >= pipeline.max_self_correction` (default 3) →
         `cap_reached` with residuals documented and surfaced at the human
         checkpoint (cap_reached is a documented exit, not a failure)
   A single zero-finding pass at N=1 does NOT exit — re-run the reviewer on the
   same artifact to seek the second consecutive clean.
   - Each loop's reviewer writes to: `.delivery/artifacts/04-architect/challenger/loop-{N}.md`
   - Architect revisions between loops write to: `.delivery/artifacts/04-architect/solution/architecture.md` (in place)
   - See `references/team-patterns.md` Pattern 2b (Isolated Adversarial Loop) and ADR-003 for the full protocol.
7. **Team DoD Validation** [PARALLEL] -- dispatch all validators in a single message: Architect (soundness), QA (testability), DevOps (deployability), Security (posture)
8. **Human Checkpoint 2** [SEQUENTIAL]: Present architecture summary for approval

### DoD Validators [PARALLEL] -- dispatch all in a single message
- Architect [required]: design is sound, trade-offs documented, patterns appropriate
  - Writes to: `.delivery/artifacts/04-architect/dod/architect-review.md`
- QA Engineer [required]: architecture supports testing (observability, isolation)
  - Writes to: `.delivery/artifacts/04-architect/dod/qa-review.md`
- DevOps [required]: architecture is deployable (CI/CD compatible, environment strategy)
  - Writes to: `.delivery/artifacts/04-architect/dod/devops-review.md`
- Security [required]: security concerns addressed
  - Writes to: `.delivery/artifacts/04-architect/dod/security-review.md`

### Output Artifacts
- `.delivery/artifacts/04-architect/solution/architecture.md`
- `.delivery/artifacts/04-architect/debate-judge/decision.md` (one per major decision, used to generate ADRs)

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
1. **Invoke Product Owner** [SEQUENTIAL] [required] (product-delivery skill, task_type: user_story)
   - SKILL: `delivery-team:product-delivery`, TASK_TYPE: `user_story`, ROLE: `po`
   - Input artifacts: `.delivery/artifacts/02-refine/po/prd.md`
   - Output: `.delivery/artifacts/05-plan/po/stories.md`
2. **Invoke QA Engineer** [SEQUENTIAL per story, after step 1] [required] (quality skill, task_type: test-cases)
   - SKILL: `delivery-team:quality`, TASK_TYPE: `test-cases`, ROLE: `qa`
   - Input artifacts: `.delivery/artifacts/05-plan/po/stories.md` (each story's acceptance criteria)
   - Output: test cases appended per story within `.delivery/artifacts/05-plan/po/stories.md`
   - Test cases MUST be produced alongside stories, not as a separate optional step
   - Each story's output includes: story + acceptance criteria + test cases
3. **Invoke Supporting Agents** [PARALLEL after step 2] -- dispatch SM, QA (test-strategy), DevOps in a single message:
   - **Scrum Bag** [required] (product-delivery skill, task_type: sprint_planning)
     - SKILL: `delivery-team:product-delivery`, TASK_TYPE: `sprint_planning`, ROLE: `sm`
     - Input artifacts: `.delivery/artifacts/05-plan/po/stories.md`, `.delivery/artifacts/04-architect/solution/architecture.md`
     - Output: `.delivery/artifacts/05-plan/sm/sprint-plan.md`
   - **QA Engineer** [required] (quality skill, task_type: test-strategy)
     - SKILL: `delivery-team:quality`, TASK_TYPE: `test-strategy`, ROLE: `qa`
     - Input artifacts: `.delivery/artifacts/02-refine/po/prd.md`, `.delivery/artifacts/04-architect/solution/architecture.md`, `.delivery/artifacts/05-plan/po/stories.md`
     - Output: `.delivery/artifacts/05-plan/qa/test-strategy.md`
   - **DevOps** [optional] (operations skill, task_type: deployment-strategy)
     - SKILL: `delivery-team:operations`, TASK_TYPE: `deployment-strategy`, ROLE: `devops`
     - Input artifacts: `.delivery/artifacts/04-architect/solution/architecture.md`
     - Output: `.delivery/artifacts/05-plan/devops/deploy-plan.md`
4. **Matrix validation** [SEQUENTIAL after step 3] [required]: Verify the sprint plan includes both mandatory matrices:
   - **Capacity matrix**: must be present with all team members listed, available hours > 0, utilization % calculated
   - **Coverage matrix**: must be present with every PRD FR-ID mapped to at least one planned task; any unmapped FR causes a BLOCKING finding
   - **Light Mode (BUG_FIX, DOCS_ONLY)**: Both matrices are WAIVED -- skip this step
   <!-- retros c8f2, k4m9 -->
5. **Consensus Protocol** [PARALLEL per round, SEQUENTIAL between rounds] [required]: SM, PO, QA, DevOps independently estimate and identify risks (R1 parallel), then share and respond (R2 parallel), and converge (R3 parallel if needed). 2-3 rounds.
   - R1 writes to: `.delivery/artifacts/05-plan/consensus/r1/{role}-position.md`
   - R2 writes to: `.delivery/artifacts/05-plan/consensus/r2/{role}-response.md`
   - R3 writes to: `.delivery/artifacts/05-plan/consensus/r3/{role}-final.md` (if needed)
6. **Adversarial Review** [SEQUENTIAL after consensus] [required]: Challenger questions estimates and risk assessments
   - Challenger writes to: `.delivery/artifacts/05-plan/challenger/challenge.md`
7. **Team DoD Validation** [PARALLEL] -- dispatch all validators in a single message: SM (process), PO (scope), QA (coverage), DevOps (readiness)
8. **Git branch creation** [SEQUENTIAL] (if `git.auto_branch` is true): Create feature branch from main (or develop for GitFlow) using the configured `git.branch_strategy`. Branch name: `feature/<issue-number>-<short-description>`. Verify clean working tree before branching. If the branch already exists, append a numeric suffix. Record branch name in `.delivery/state.md`. See `references/git-integration.md`.
9. **Human Checkpoint 3** [SEQUENTIAL]: Present sprint plan for approval

### DoD Validators [PARALLEL] -- dispatch all in a single message
- Scrum Bag [required]: process is sound, capacity realistic, capacity matrix present with utilization calculated, coverage matrix present with all PRD FRs mapped to at least one task. Capacity threshold enforcement: >80% utilization emits WARNING requiring acknowledgment; >100% utilization is BLOCKING <!-- retros c8f2, k4m9 -->
  - Writes to: `.delivery/artifacts/05-plan/dod/sm-review.md`
- Product Owner [required]: scope is correct, stories are valuable
  - Writes to: `.delivery/artifacts/05-plan/dod/po-review.md`
- QA Engineer [required]: test strategy covers critical paths
  - Writes to: `.delivery/artifacts/05-plan/dod/qa-review.md`
- DevOps [optional]: deployment approach is viable
  - Writes to: `.delivery/artifacts/05-plan/dod/devops-review.md`

### Output Artifacts
- `.delivery/artifacts/05-plan/po/stories.md`
- `.delivery/artifacts/05-plan/sm/sprint-plan.md`
- `.delivery/artifacts/05-plan/qa/test-strategy.md`
- `.delivery/artifacts/05-plan/devops/deploy-plan.md`

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
- **Filename reconciliation gate** <!-- retro k4m9 -->: Before Development begins, all file paths referenced in Design (Stage 3) and Architect (Stage 4) artifacts are checked:
  1. Use Glob/Read to extract all file paths from `.delivery/artifacts/03-design/` and `.delivery/artifacts/04-architect/` artifacts
  2. For each referenced file path, check existence on disk using Glob
  3. **Pass criteria**:
     - Path exists on disk: PASS
     - Path appears in the sprint plan's task list as a planned deliverable: PASS
     - Path is annotated `[PLANNED]` in Design artifacts but does NOT appear in the sprint plan: FAIL
     - Path does not exist and is not in the sprint plan: FAIL
  4. **Any FAIL blocks Dev entry** with a list of non-existent references and their source artifacts
  5. Resolution: either create the missing files, add them to the sprint plan as planned deliverables, or remove the references from upstream artifacts
  - **Light Mode**: Applies to all project types including BUG_FIX and DOCS_ONLY
  - **Note**: `[PLANNED]` annotations from Design (FR-05) are NOT accepted as exemptions at Dev entry. This is the enforcement point where all referenced files must be accounted for.

### Sub-Flow
For each story in the sprint plan:

**Independent stories run in PARALLEL** (when `pipeline.parallel_stories` is true). Dependent stories run SEQUENTIALLY. The orchestrator checks story dependencies from the sprint plan. Max concurrent stories: `pipeline.max_parallel_agents` (default 3).

1. **Invoke Developer** [PARALLEL for independent stories, SEQUENTIAL for dependent] [required] (developer skill, task_type: write)
   - SKILL: `delivery-team:developer`, TASK_TYPE: `write`, ROLE: `developer`
   - Input artifacts: `.delivery/artifacts/05-plan/po/stories.md` (specific story), `.delivery/artifacts/04-architect/solution/architecture.md`
   - Output: `.delivery/artifacts/06-dev/developer/{story-id}.md` + code files
2. **Evaluator-Optimizer Loop** [SEQUENTIAL per story] [required]: QA Engineer reviews code against acceptance criteria + coding standards. Route back with feedback. Max 3 iterations per story.
   - Evaluator writes to: `.delivery/artifacts/06-dev/qa-evaluator/{story-id}-round-{N}.md`
3. **Decision Ownership Routing** [on-demand]: If issues arise:
   - Scope questions -> Product Owner
   - Technical questions -> Architect
   - Quality questions -> QA Engineer
4. **Invoke Technical Writer** [SEQUENTIAL] [optional] (operations skill, task_type: api-docs or runbook) if applicable
   - SKILL: `delivery-team:operations`, TASK_TYPE: `api-docs`, ROLE: `tech-writer`
   - Input artifacts: `.delivery/artifacts/06-dev/developer/{story-id}.md`
   - Output: `.delivery/artifacts/06-dev/tech-writer/docs.md`
5. **Regenerate derived artifacts** [SEQUENTIAL per story] [required]: Before Dev DoD, check if any modified source files have derived artifacts. If so:
   1. Identify all derived artifacts (generated docs, compiled schemas, transformed configs, etc.)
   2. Regenerate each derived artifact from its current source
   3. Verify the regenerated artifact matches expectations (no unexpected diffs)
   4. Document the regeneration in the story's implementation notes
   - **Light Mode**: Applies to all project types <!-- retro c8f2 -->
6. **Commit suggestion** [SEQUENTIAL] (if `git.commit_convention` is "conventional"): Suggest a conventional commit message based on the story type. Format: `<type>(<scope>): <description>`. Do NOT auto-commit -- present the suggestion for the user to review and execute. See `references/git-integration.md`.
7. **Team DoD Validation per story** [PARALLEL] -- dispatch all validators in a single message: Developer (quality), QA (tests), Architect (conformance), Tech Writer (docs)

### DoD Validators (per story) [PARALLEL] -- dispatch all in a single message
- Developer [required]: code is clean, follows language best practices, derived artifacts regenerated from current sources <!-- retro c8f2 -->
  - Writes to: `.delivery/artifacts/06-dev/dod/{story-id}-developer-review.md`
  - **Derived artifact check**: If the story modifies source files that have derived artifacts (e.g., generated docs, compiled schemas, transformed configs, built outputs), the developer must confirm all derived artifacts have been regenerated from current sources before marking the story complete. The DoD review must include a "Derived Artifacts" section listing: each derived artifact path, its source file(s), and regeneration status (regenerated / not applicable).
- QA Engineer [required]: tests pass, coverage adequate
  - Writes to: `.delivery/artifacts/06-dev/dod/{story-id}-qa-review.md`
- Architect [required]: implementation conforms to architecture decisions
  - Writes to: `.delivery/artifacts/06-dev/dod/{story-id}-architect-review.md`
- Technical Writer [optional]: inline docs and any required external docs present
  - Writes to: `.delivery/artifacts/06-dev/dod/{story-id}-techwriter-review.md`
- Feature Knowledge: if new feature -- draft FKC auto-generated, developer confirms.
  If existing feature modified -- FKC reviewed and `last_updated` refreshed.

### Output Artifacts
- Actual code files (in the project codebase)
- `.delivery/artifacts/06-dev/developer/{story-id}.md` (per-story implementation notes)
- `.delivery/artifacts/06-dev/tech-writer/docs.md` (if applicable)

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
1. **Invoke QA Engineer** [SEQUENTIAL] [required] (quality skill, task_type: test-plan)
   - SKILL: `delivery-team:quality`, TASK_TYPE: `test-plan`, ROLE: `qa`
   - Input artifacts: `.delivery/artifacts/02-refine/po/prd.md`, `.delivery/artifacts/06-dev/developer/` (all story files)
   - Output: `.delivery/artifacts/07-uat/qa/test-plan.md`
2. **Invoke QA Engineer** [SEQUENTIAL after step 1] [required] (quality skill, task_type: test-cases)
   - SKILL: `delivery-team:quality`, TASK_TYPE: `test-cases`, ROLE: `qa`
   - Input artifacts: `.delivery/artifacts/07-uat/qa/test-plan.md`
   - Output: `.delivery/artifacts/07-uat/qa/test-cases.md`
3. **Execute test descriptions** [SEQUENTIAL] (describe how to test; actual execution depends on test framework availability)
4. **Exploratory testing sessions** [SEQUENTIAL] [required] (quality skill, task_type: exploratory-testing)
   - For GAME_DEV: 2 sessions -- Feature Tour (play all implemented features) + Cross-Story Regression (test interactions between stories modifying shared values)
   - For all types: 1 session -- Cross-Story Interaction (test that independently-completed stories work together)
   - Each session has a charter, is time-boxed, and produces observation notes (not pass/fail)
   - Any bugs found are logged to `.delivery/defects/` immediately
   - See the quality skill's `references/exploratory-testing.md` for session format and heuristics
5. **Shared-module review** [SEQUENTIAL after step 4] [required] (quality skill, task_type: test-plan)
   - **Definition**: A shared module is a file referenced by path or name in 2+ stage artifacts across the current pipeline run.
   - **Identification**: QA agent scans `.delivery/artifacts/` using Glob/Read to collect all file path references across all stage artifacts. Any file path appearing in artifacts from 2+ different stages is flagged as a shared module.
   - **Review**: For each shared module modified during Development, the QA agent must:
     1. List all consuming contexts (stages/artifacts that reference the module)
     2. Verify test coverage exists for each consuming context
     3. Document the shared-module review results in the UAT test plan
   - Output: Shared-module review section within `.delivery/artifacts/07-uat/qa/test-plan.md`
   - **Light Mode**: Applies to all project types including BUG_FIX and DOCS_ONLY <!-- retro c8f2 -->
6. **Invoke Supporting Agents** [PARALLEL] -- dispatch DevOps + Tech Writer in a single message:
   - **DevOps** [required] (operations skill, task_type: release-plan + rollback-procedure)
     - SKILL: `delivery-team:operations`, TASK_TYPE: `release-plan`, ROLE: `devops`
     - Input artifacts: `.delivery/artifacts/04-architect/solution/architecture.md`, `.delivery/artifacts/05-plan/devops/deploy-plan.md`
     - Output: `.delivery/artifacts/07-uat/devops/release-plan.md`
   - **Technical Writer** [optional] (operations skill, task_type: release-notes + user-guide)
     - SKILL: `delivery-team:operations`, TASK_TYPE: `release-notes`, ROLE: `tech-writer`
     - Input artifacts: `.delivery/artifacts/02-refine/po/prd.md`, `.delivery/artifacts/06-dev/developer/` (all story files)
     - Output: `.delivery/artifacts/07-uat/tech-writer/release-notes.md`, `.delivery/artifacts/07-uat/tech-writer/user-guide.md`
7. **Working tree validation** [SEQUENTIAL] (if `git.clean_tree_check` is true): Run `git status --porcelain`. If not clean, list uncommitted changes and warn: "Working tree has uncommitted changes. Commit or stash before UAT acceptance." Do not block -- present the warning and let the user decide. See `references/git-integration.md`.
8. **PR creation** [SEQUENTIAL] (if `github.create_pr` is true): Create a pull request using `gh pr create` with: title from sprint goal, body with change summary + stories implemented (with "Closes #N" for each linked issue) + test results from UAT report + release notes. Label by project type. Record the PR URL in the UAT report artifact. See `references/github-integration.md`.
9. **Multi-Perspective Review Board** [PARALLEL] [required]: QA (tests) + DevOps (release readiness) + Tech Writer (docs). ALL reviewers dispatched in parallel. Go/no-go recommendation.
   - Each reviewer writes to: `.delivery/artifacts/07-uat/review-board/{role}-review.md`
10. **Team DoD Validation** [PARALLEL] -- dispatch all validators in a single message: QA (tests pass), DevOps (rollback ready), PO (acceptance), Tech Writer (docs complete)
11. **Human Checkpoint 4** [SEQUENTIAL]: Present UAT results for accept/reject

### DoD Validators [PARALLEL] -- dispatch all in a single message
- QA Engineer [required]: all tests pass, no critical defects, shared-module review complete (if shared modules were modified)
  - Writes to: `.delivery/artifacts/07-uat/dod/qa-review.md`
- DevOps [required]: deployment plan complete, rollback tested/documented
  - Writes to: `.delivery/artifacts/07-uat/dod/devops-review.md`
- Product Owner [required]: delivered features match expectations
  - Writes to: `.delivery/artifacts/07-uat/dod/po-review.md`
- Technical Writer [optional]: all documentation complete and accurate
  - Writes to: `.delivery/artifacts/07-uat/dod/techwriter-review.md`

### Output Artifacts
- `.delivery/artifacts/07-uat/qa/test-plan.md`
- `.delivery/artifacts/07-uat/qa/test-cases.md`
- `.delivery/artifacts/07-uat/devops/release-plan.md`
- `.delivery/artifacts/07-uat/tech-writer/release-notes.md`
- `.delivery/artifacts/07-uat/tech-writer/user-guide.md`

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
6. **Update Feature Knowledge** -- if new feature: finalize FKC and write to `.delivery/features/`.
   If existing feature modified: update FKC. Regenerate interaction map from all FKCs.
   Check for new decisions to add to Decision Trail.
7. Pipeline complete
