## Product Requirements Document

**Product / Feature:** Agent Delegation, Isolation, and Parallelism
**Version:** 1.0
**Author:** Gandalf (Product Owner)
**Status:** Draft
**Last Updated:** 2026-03-24
**GitHub Issues:** #25, #26, #27, #28

---

### 1. Problem Statement

The delivery-flow orchestrator suffers from a threefold failure in how it manages its agents -- and these three failures share a single root cause: the absence of a proper agent lifecycle discipline.

**The first failure is delegation (#25).** The orchestrator sometimes neglects to delegate work to sub-agents at all. Instead of spawning a dedicated agent instance with the correct skill loaded, it runs the task inline within its own context window. When this happens, the worker role's SKILL.md and reference documents are never loaded. The Product Owner writes a PRD without the product-delivery skill's guidance. The Architect designs without the architect skill's references. The orchestrator plays every part itself, poorly, like a single actor performing all roles in the play without ever reading the scripts.

**The second failure is isolation (#26).** Even when sub-agents are spawned, they inherit context from the orchestrator's conversation. The QA engineer can see the developer's reasoning. The adversarial reviewer -- whose entire purpose is to provide an independent challenge -- can see how the primary agent produced the artifact. You cannot get an honest second opinion from someone who watched you write the first one. This defeats every collaboration pattern the pipeline defines: evaluator-optimizer, adversarial review, review board, debate, and consensus all assume that each agent brings an independent perspective. Shared context makes that independence a fiction.

**The third failure is sequencing (#27).** The pipeline executes everything sequentially, even when tasks have no dependencies on each other. DoD validators run one after another when they could run simultaneously. Review board members wait in line. Independent stories are implemented one at a time. Supporting agents queue behind the primary worker. A real team does not work this way. A real team assigns independent tasks to independent people and lets them work in parallel.

These three issues share a root cause: the orchestrator lacks a disciplined agent lifecycle protocol that governs how agents are created, what context they receive, and whether independent agents can run concurrently.

---

### 2. Goals & Success Metrics

**Goals:**

1. Sub-agent delegation is reliable -- the orchestrator never falls back to inline execution when a sub-agent is specified by the pipeline stage definition
2. Each sub-agent runs in a fully isolated context, receiving only artifact file paths and its own skill references -- no orchestrator reasoning, no other agent output, no shared conversation history
3. Independent tasks within a stage run concurrently where the platform supports it
4. Agent communication happens exclusively through artifact files in `.delivery/artifacts/` -- no context passing, no inline handoffs
5. All six existing collaboration patterns continue to function correctly under the new execution model

**Success Metrics:**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Delegation reliability | 100% of stage-defined sub-agent invocations use the Agent tool | Audit pipeline execution: every task listed in pipeline-stages.md is dispatched via Agent tool, never produced inline |
| Context isolation | 100% of orchestrator-to-agent prompts pass metadata-only audit | Orchestrator passes only: file paths, status enums, role IDs, summaries (<200 chars). No code fences, no artifact content, no other agent output. PreToolUse audit hook validates. |
| Parallel speedup | DoD validation wall-clock time reduced vs sequential baseline | Time DoD validation with parallel vs sequential execution; parallel should complete faster |
| Artifact-only communication | 100% of inter-agent data passes through `.delivery/artifacts/` files | Audit agent prompts: no artifact content pasted inline, no summarized output forwarded, only file paths provided |
| Collaboration pattern correctness | All 6 patterns produce valid results under new model | Run each pattern and verify output quality matches pre-change baseline |
| Backward compatibility | Existing config.yml files work without modification | Run pipeline with a config.yml that has no parallel keys; defaults apply, pipeline completes normally |

---

### 3. User Personas

**The Pipeline User (any project type)**

Every user running delivery-flow is affected. Inline execution can happen on any run. Context bleed undermines every collaboration pattern. Sequential execution slows every multi-agent stage. This user needs the orchestrator to delegate reliably, isolate properly, and parallelize where possible -- without requiring any change to their workflow.

**The Quality-Sensitive User**

This user relies on adversarial review and Team DoD validation to catch real problems. They trust the pipeline to provide genuine independent assessment. If the reviewer already saw the work being produced, the review is theater, not verification. This user needs context isolation to be absolute, not aspirational.

**The Large-Pipeline User**

This user runs GREENFIELD or GAME_DEV projects with full depth settings. These pipelines invoke the most sub-agents and suffer the most from sequential bottlenecks. A full pipeline with evaluator-optimizer loops, adversarial review, debate, consensus, and Team DoD at every stage -- run sequentially -- takes far longer than it should. This user needs parallel execution for independent tasks to bring pipeline duration closer to the critical path.

---

### 4. User Stories

**US-01: Orchestrator delegates ALL domain work via Agent tool**

As the orchestrator, I delegate ALL domain work to sub-agents via the Agent tool, never producing artifacts inline, so that each worker role executes with its proper skill loaded and its full reference set available.

**Acceptance Criteria:**
- Every task defined in pipeline-stages.md is dispatched via the Agent tool
- The orchestrator never uses Write/Edit to produce domain content (PRDs, designs, architecture docs, code, test plans) directly
- Each Agent invocation specifies the correct skill name and task_type
- If the Agent tool is unavailable or fails, the orchestrator reports the failure rather than falling back to inline execution

**US-02: Sub-agents receive only artifact file paths and skill references**

As a sub-agent, I receive only artifact file paths and my skill references -- no orchestrator conversation history -- so that my work is based solely on the defined inputs and my specialized knowledge.

**Acceptance Criteria:**
- The sub-agent prompt contains: skill name, task description, file paths to upstream artifacts, memory lessons for this stage, alias personality (if theme active)
- The sub-agent prompt does NOT contain: orchestrator reasoning, other agents' output, conversation history, artifact content pasted inline
- The sub-agent reads artifact files itself using the file paths provided
- The sub-agent loads its own SKILL.md and references (not pre-loaded by the orchestrator)

**US-03: DoD validators run in parallel**

As a DoD validator, I run in parallel with other validators, seeing only the artifact and gate criteria, so that validation completes faster and each validator's judgment is independent.

**Acceptance Criteria:**
- All DoD validators for a stage are spawned in a single message (parallel Agent calls)
- Each validator receives: the artifact file path, its role-specific gate criteria, and the instruction to vote DONE or NOT_DONE
- No validator sees another validator's output or vote
- Results are collected after all validators complete; the orchestrator synthesizes the outcome

**US-04: Adversarial reviewers receive only the artifact**

As an adversarial reviewer, I receive only the artifact to review -- not the production conversation or the primary agent's reasoning -- so that my challenge is genuinely independent.

**Acceptance Criteria:**
- The challenger agent receives: the artifact file path, the adversarial review prompt template, and gate criteria
- The challenger does NOT receive: the primary agent's prompt, the primary agent's reasoning, the evaluator-optimizer loop history, or the orchestrator's internal notes
- The challenger reads the artifact from the file path and produces its challenge based solely on the artifact content

**US-05: Independent stories run in parallel**

As a developer implementing independent stories, I run in parallel with other story agents (max configurable), so that stories without dependency edges are completed concurrently.

**Acceptance Criteria:**
- Stories with no dependency edges are dispatched as parallel Agent calls (up to `pipeline.max_parallel_agents`)
- Each story agent receives: the story file path, the architecture artifact file path, and relevant references
- Stories with dependency edges are dispatched sequentially in dependency order
- The max parallel agent count is configurable via `pipeline.max_parallel_agents` (default: 3)

**US-06: Orchestrator communicates through artifact files exclusively**

As the orchestrator, I communicate with sub-agents exclusively through artifact files in `.delivery/artifacts/`, so that no information passes through my context as a bridge between agents.

**Acceptance Criteria:**
- The orchestrator passes file paths to sub-agents, not file content
- When a sub-agent produces output, the orchestrator writes it to an artifact file before the next agent references it
- The orchestrator does not summarize, paraphrase, or filter a sub-agent's output when passing it downstream
- The next sub-agent reads the artifact file directly

**US-07: Review board members produce independent reviews**

As a review board member, I produce my review independently -- I do not see other reviewers' output until synthesis -- so that my perspective is uncontaminated by groupthink.

**Acceptance Criteria:**
- All review board members are spawned in a single message (parallel Agent calls)
- Each reviewer receives: the artifact file path, their role-specific evaluation criteria, and the instruction to vote RECOMMEND or BLOCK
- No reviewer sees another reviewer's findings or vote during their review
- The orchestrator collects all reviews after completion and performs synthesis

**US-08: Consensus participants produce independent Round 1 analysis**

As a consensus participant, my Round 1 analysis is independent -- I see other agents' positions only in Round 2 -- so that the consensus process begins with genuinely diverse perspectives.

**Acceptance Criteria:**
- All consensus participants are spawned in parallel for Round 1
- Each participant receives: the topic, artifact file paths, and their role-specific perspective prompt
- No participant sees another's Round 1 output
- In Round 2, all Round 1 outputs are written to artifact files and all participants receive file paths to all Round 1 outputs
- Round 2 participants are spawned in parallel with the full set of Round 1 artifact file paths

**US-09: Orchestrator delegates to delivery-flow after plan approval (Must Have)**

As the orchestrator exiting plan mode, when the approved plan involves delivery-team work (code, architecture, testing, docs), I invoke delivery-team:delivery-flow rather than implementing directly.

**Acceptance Criteria:**
- When exiting plan mode with an approved plan that involves code, architecture, testing, or documentation changes, the orchestrator invokes `delivery-team:delivery-flow`
- The orchestrator does NOT implement the plan directly
- The delivery-flow pipeline receives the approved plan as input and executes it through the standard stage progression

---

### 5. Functional Requirements

#### FR-01: Agent Invocation Protocol

Every domain task specified in pipeline-stages.md MUST be executed via the Agent tool. Each invocation SHALL include:

- The specific skill name and task_type
- Input: file paths to upstream artifacts (NOT content pasted inline)
- Skill references loaded by the sub-agent itself (NOT pre-loaded by the orchestrator)
- Alias personality injection (from active theme, if any)
- Memory lessons (from relevant stage/topic chunks)
- Explicit instruction: "Read artifacts from the file paths provided. Do not reference any prior conversation context."

The orchestrator constructs the agent prompt. The sub-agent instructs and verifies skill loading, reads the artifacts, and executes the task. The orchestrator collects the result.

**Skill Loading Verification (Verify-After-Invoke):**
- The orchestrator's delegation prompt includes: "Begin your response with 'SKILL_LOADED: [skill-name]' to confirm you have loaded the skill."
- The orchestrator checks the sub-agent's output for this marker.
- If marker is absent or mismatched: flag as unreliable delegation, retry once, then escalate.
- A PostToolUse hook on Agent invocations provides a second verification layer.

#### FR-02: Context Isolation Protocol

Each sub-agent receives a fresh context containing ONLY:

- Its skill's SKILL.md and relevant references (loaded by the skill itself when the Agent tool invokes it)
- File paths to upstream artifacts (the agent reads them)
- Memory lessons for this stage (from `.delivery/memory/`)
- Alias personality (if theme is active)
- Gate criteria (for validators)

Each sub-agent does NOT receive:

- Orchestrator reasoning or internal notes
- Other agents' output, findings, or votes
- Conversation history from the orchestrator's context
- Artifact content pasted inline (only file paths)

This isolation is enforced by the Agent tool's natural context boundary. The orchestrator's responsibility is to never include prohibited context in the agent prompt.

#### FR-03: Two-Channel Communication Model

The orchestrator uses two strictly separated communication channels:

**Signal Channel** (flows through orchestrator):
- DoD votes: DONE / NOT_DONE / CODE_COMPLETE
- Routing decisions: RECOMMEND / BLOCK
- Stage status: completed / failed / skipped
- File paths to artifacts
- Summary strings (max 200 characters)

**Artifact Channel** (never flows through orchestrator):
- File contents -- sub-agents read artifact files directly by path
- The orchestrator passes file PATHS, never file CONTENTS
- Sub-agents return: STATUS + FILE_PATHS + SUMMARY (signal only)
- Downstream agents receive file paths and read files themselves

**Exception**: Collaboration patterns requiring multi-round interaction (Consensus Round 2, Debate Judge) intentionally share prior-round artifacts in later rounds. This is defined in each pattern's protocol.

The orchestrator NEVER reads artifact file contents. It reads only signal-channel data from sub-agent responses.

#### FR-04: Parallel Execution for Independent Tasks

When tasks have no dependencies, the orchestrator SHALL spawn multiple Agent calls in a single message. The following task groups are eligible for parallel execution:

- **DoD validators:** ALL validators for a stage run in parallel
- **Review Board:** ALL reviewers run in parallel
- **Consensus Round 1:** ALL participants run in parallel
- **Supporting agents:** Independent supporting agents within a stage (e.g., Data Analyst + UX Researcher at Refine) run in parallel
- **Independent stories:** Stories with no dependency edges run in parallel (max `pipeline.max_parallel_agents`)
- **Debate PRO/CON:** Both sides of a debate run in parallel (the Judge runs after, sequentially)

#### FR-05: Parallel Execution Map

The following table defines explicitly which tasks are sequential (order required) versus parallel (independent) at each pipeline stage:

| Stage | Sequential (order required) | Parallel (independent) |
|-------|---------------------------|----------------------|
| 2 Refine | PRD creation first | Metrics + UX research after PRD |
| 3 Design | UX flows first | UI specs + accessibility review after flows |
| 5 Plan | Story writing first | Test strategy + deploy plan + estimates after stories |
| 6 Dev | Dependent stories in order | Independent stories (max 3 parallel) |
| 7 UAT | Test plan first | Release plan + docs + test execution after plan |
| All DoD | -- | All validators in parallel |
| Review Board | -- | All reviewers in parallel |
| Consensus R1 | -- | All participants in parallel |
| Consensus R2 | -- | All participants in parallel (with R1 outputs) |
| Adversarial | Primary artifact first | Challenger runs independently after |
| Debate | -- | PRO + CON in parallel; Judge sequential after |

#### FR-06: Delegation Guardrail

The orchestrator MUST NOT:

1. Use Write/Edit to create domain content in `.delivery/artifacts/` directly (permitted only for writing sub-agent output to file)
2. Paste artifact content into a sub-agent prompt (pass file path instead)
3. Summarize or paraphrase a sub-agent's output for the next agent (let the next agent read the file)
4. Skip a sub-agent invocation that is defined in pipeline-stages.md
5. Fall back to inline execution when the Agent tool is available

If the orchestrator detects that it is about to produce domain content inline (a self-check), it SHALL stop and delegate to the appropriate sub-agent instead.
- When exiting plan mode with an approved plan that involves code, architecture, testing, or documentation changes, the orchestrator MUST invoke `delivery-team:delivery-flow` to execute the plan. It MUST NOT implement the plan directly.

#### FR-07: Parallel Configuration

New config keys added to `.delivery/config.yml` under the `pipeline` section:

```yaml
pipeline:
  max_parallel_agents: 3     # max concurrent sub-agents per parallel group
  parallel_stories: true      # enable parallel story implementation in Stage 6
  parallel_validators: true   # enable parallel DoD validation at all stages
```

**Defaults:** If these keys are absent from config.yml, the following defaults apply:
- `max_parallel_agents`: 3
- `parallel_stories`: true
- `parallel_validators`: true

These defaults ensure backward compatibility -- existing config files work without modification.

#### FR-08: Graceful Degradation

If parallel execution is not supported by the platform (e.g., the Agent tool does not support multiple concurrent calls), the orchestrator SHALL fall back to sequential execution transparently. The pipeline produces identical results whether run in parallel or sequential -- only wall-clock time differs. The orchestrator SHALL NOT error or abort due to a platform limitation on parallelism.

#### FR-09: Parallel Failure Handling (Scatter-Gather Model)

Each agent in a parallel group is tagged `required` or `optional` in the stage definition:
- **Required agent fails/times out**: Stage halts. Error report names the failed agent, the error, and the stage context. Orchestrator retries the failed agent only (not the full group), up to 2 attempts. After 2 retries, escalate to user.
- **Optional agent fails/times out**: Orchestrator logs the gap, proceeds with partial results. The gap is noted in the stage artifact.
- **All agents timeout**: Clean stage-level failure with error report.
- **Per-agent timeout**: Configurable, default 120 seconds.
- **Retry targets only the failed agent**, never re-runs successful agents in the group.

#### FR-10: Sub-Agent Write Ownership

Sub-agents always write their own artifacts. The orchestrator never writes artifact content.

**Namespace isolation**: Each sub-agent writes to `.delivery/artifacts/{stage-number}-{stage-name}/{role}/`. Examples:
- Architect writes to `.delivery/artifacts/04-architect/solution/`
- Developer writes to `.delivery/artifacts/06-development/developer/`
- QA validator writes to `.delivery/artifacts/06-development/qa-review/`

No two agents share a write directory. Collisions are impossible by structure.

The orchestrator's only file-write responsibilities:
- `.delivery/state.md` (pipeline state)
- `.delivery/artifacts/` stage summary/routing metadata
- Never artifact content

---

### 6. Non-Functional Requirements

**NFR-01: Artifact Quality Preservation.** No change to artifact quality as a result of context isolation. The same DoD pass rate must be achievable with isolated agents as with the current (non-isolated) model. If isolation causes a quality regression, the isolation protocol must be revised -- not the quality bar.

**NFR-02: Parallel Performance.** Parallel DoD validation should complete in less wall-clock time than sequential validation for the same set of validators. The improvement scales with the number of validators (2-4 per stage).

**NFR-03: Backward Compatibility.** Existing `.delivery/config.yml` files that do not contain the new parallel configuration keys SHALL work without modification. Default values are applied for absent keys. No existing pipeline behavior changes unless the user opts in via config.

**NFR-04: Collaboration Pattern Correctness.** All six collaboration patterns (evaluator-optimizer, adversarial review, multi-perspective review board, decision ownership routing, debate, consensus) SHALL produce correct results under the new agent lifecycle model. Correctness means: each pattern's protocol (as defined in `references/team-patterns.md`) is followed exactly, with the additional guarantee that context isolation is enforced at every agent boundary.

**NFR-05: Hook Contract Preservation.** Hook contracts (PreToolUse, PostToolUse, SubagentStop) SHALL fire correctly for agents spawned in parallel. Each agent's lifecycle events trigger hooks independently. Parallel execution does not suppress, duplicate, or reorder hook events.

---

### 7. Out of Scope

These items are explicitly excluded from this feature:

- **Agent-to-agent direct communication.** Agents communicate through artifact files, not to each other. No message-passing, no shared memory, no direct invocation between sub-agents.
- **Dynamic parallelism tuning based on system load or token budgets.** Parallelism is configured statically via `max_parallel_agents`. Adaptive throttling is a future consideration.
- **Partial result streaming from sub-agents back to the orchestrator mid-execution.** Sub-agents complete their full task before the orchestrator processes results.
- **Changes to pipeline stage definitions.** This feature fixes how agents are managed, not what stages do. The stages, their agents, and their artifacts remain as defined in `references/pipeline-stages.md`.
- **Multi-orchestrator or distributed pipeline execution.** The orchestrator remains a single coordinating agent. We are fixing delegation, not creating a distributed system.
- **New collaboration patterns beyond the existing six.** The six patterns are unchanged in definition; only their execution model (isolation and parallelism) is improved.

---

### 8. Dependencies & Risks

**Dependencies:**

| Dependency | Nature | Impact |
|-----------|--------|--------|
| Agent tool support for parallel calls | Multiple Agent tool invocations in a single message must be supported by the platform | High -- if not supported, FR-04 degrades to sequential (FR-08 mitigates) |
| Agent tool context isolation | The Agent tool must create a fresh context for each sub-agent, not inheriting the caller's conversation | High -- if the Agent tool shares context, FR-02 cannot be fully enforced |
| Existing pipeline-stages.md definitions | Stage definitions specify which agents to invoke and in what order | Low -- no changes to stage definitions required |
| Artifact file contracts (artifact-contracts.md) | Artifacts must have well-defined schemas so sub-agents can read them without additional context | Medium -- poorly defined artifact contracts may require sub-agents to need more context than file paths alone |
| Config schema (config-schema.md) | New parallel config keys must follow the extension protocol | Low -- additive keys with defaults |
| State persistence (Issue #11) | State file write points must account for parallel agent completion | Low -- state writes occur after all agents for a step complete, not during |

**Risks:**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Agent tool does not support parallel invocation | Medium | High -- no parallel speedup | FR-08 graceful degradation: fall back to sequential execution transparently |
| Context isolation incomplete -- Agent tool leaks caller context | Medium | High -- collaboration patterns compromised | Validate sub-agent prompts explicitly; include instruction to ignore prior context; test isolation empirically |
| Artifact files insufficient as sole communication channel | Low | Medium -- sub-agents may lack context needed for quality output | Strengthen artifact-contracts.md to ensure artifacts are self-contained; include all necessary context in artifact files |
| Parallel agents produce conflicting writes to the same artifact file | Low | High -- data corruption | Each parallel agent writes to a distinct output file; the orchestrator merges if needed |
| Hook events fire in unexpected order under parallel execution | Medium | Medium -- hook side effects may conflict | Document hook behavior under parallelism; ensure hooks are idempotent where possible |
| Quality regression from strict isolation (agents lack helpful context they previously received) | Medium | High -- DoD pass rate drops | Monitor DoD pass rates; if isolation causes regression, enrich artifact files rather than loosening isolation |

---

### 9. Timeline

This feature is scoped for a single sprint (FEATURE type pipeline) with the following stage estimates:

| Stage | Effort | Notes |
|-------|--------|-------|
| 1 Idea | Done | Idea brief completed (01-idea-brief.md) |
| 2 Refine (PRD) | Done | This document |
| 3 Design | Minimal | No user-facing UI. The "design" is the agent invocation protocol and parallel execution map defined in FR-01 through FR-05 |
| 4 Architect | Light | Integration points: SKILL.md Phase 4 execution protocol, team-patterns.md collaboration protocols, config-schema.md extension |
| 5 Plan | Light | Implementation stories derived from FR-01 through FR-10 |
| 6 Development | Medium | Modify SKILL.md Phase 4 (Steps 4-7) to enforce delegation, isolation, and parallelism. Update team-patterns.md templates. Add parallel config keys to config-schema.md |
| 7 UAT | Medium | Verify all 6 collaboration patterns under new model. Verify parallel execution. Verify graceful degradation. Verify backward compatibility |

The primary implementation work is in the Development stage: rewriting the Pipeline Execution Protocol (SKILL.md Phase 4, Steps 4 through 7) and the collaboration pattern templates (team-patterns.md) to enforce the agent invocation protocol, context isolation, and parallel dispatch.

---

### 10. Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | Does the Agent tool support multiple concurrent invocations in a single message? | Gandalf (PO) | RESOLVED -- Yes. Claude Code supports multiple tool calls in a single response. FR-08 provides graceful degradation if this changes. |
| 2 | Does the Agent tool create a truly fresh context, or does it inherit the caller's conversation history? | Gandalf (PO) | RESOLVED -- The Agent tool creates a fresh context. The sub-agent receives only what is explicitly passed in the prompt. The orchestrator's responsibility is to pass only permitted content. |
| 3 | Should the orchestrator be allowed to read artifact content for routing decisions (e.g., checking a DoD vote)? | Gandalf (PO) | RESOLVED -- Yes. The orchestrator may read artifacts for routing and control flow. The prohibition is on pasting artifact content into another agent's prompt as a substitute for passing the file path. |
| 4 | Should `max_parallel_agents` apply globally or per-stage? | Gandalf (PO) | RESOLVED -- Globally, in v1. A per-stage override is unnecessary complexity for the initial implementation. The global default of 3 is sufficient for all current parallel groups (max 4 DoD validators, but 3 concurrent is acceptable). |
| 5 | How should the orchestrator handle a sub-agent that fails or times out during parallel execution? | Gandalf (PO) | RESOLVED -- Scatter-Gather model with required/optional tags. Required failure halts + retry (max 2). Optional failure logs + continues. See FR-09. |
| 6 | Should Debate PRO and CON agents run in parallel or sequentially? | Gandalf (PO) | RESOLVED -- In parallel. The PRO and CON agents argue independently by definition. Neither needs to see the other's arguments. The Judge runs sequentially after both complete. |

---

*"A wizard is never late, nor is he early -- but an orchestra that plays every instrument one at a time will empty the hall before the overture is done. Let the instruments that can play together, play together. Let each musician read only their own sheet. And let no one conduct by playing every part themselves."*

-- Gandalf, Product Owner
