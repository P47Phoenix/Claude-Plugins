## Architecture: Agent Delegation, Isolation, and Parallelism

**Role**: Celebrimbor (Solution Architect)
**Task**: design (FEATURE)
**PRD**: `.delivery/artifacts/02-prd.md`
**GitHub Issues**: #25, #26, #27, #28

*"Three Rings for the Elven-kings -- and three principles for the orchestrator: delegate every craft to the craftsman who knows it, let no craftsman see another's forge, and when their work is independent, let them work at the same time. These are not aspirations. They are the engineering."*

---

### 1. Context and Drivers

The delivery-flow orchestrator has three structural failures: it sometimes produces artifacts inline instead of delegating (Issue #25), sub-agents inherit context that contaminates independent judgment (Issue #26), and independent tasks run sequentially when they could run in parallel (Issue #27). These share a root cause: the absence of a disciplined agent lifecycle protocol in Phase 4 of SKILL.md.

The fix is entirely in prompt engineering and orchestrator instructions. No new scripts, no new tools, no code. Every change is an Edit to existing `.md` files that govern how the orchestrator constructs sub-agent prompts and manages their lifecycle.

---

### 2. Architecture Decision: Prompt-Only Agent Lifecycle

**Decision**: All changes are implemented as rewritten instructions in SKILL.md and reference files. The Agent tool already provides context isolation (fresh context per invocation) and supports parallel dispatch (multiple Agent calls in a single message). We do not need new infrastructure -- we need the orchestrator's instructions to use the existing infrastructure correctly.

**Rationale**: The Agent tool is the mechanism. The SKILL.md is the policy. The policy is broken, not the mechanism. We fix the policy.

**Alternative rejected**: A hook-based enforcement layer (PreToolUse hook that validates agent prompts). This adds runtime complexity for a problem that is fundamentally about the orchestrator's instructions being insufficiently prescriptive. If the instructions are precise enough, the orchestrator follows them. We can add hook-based auditing later as a belt-and-suspenders measure, but it is not the primary fix.

---

### 3. Agent Invocation Template

Every sub-agent call from the orchestrator MUST use this exact prompt structure. No variation. No shortcuts. The template is the contract.

```
AGENT INVOCATION TEMPLATE
=========================

SKILL: {skill_name}
TASK_TYPE: {task_type}
ROLE: {role_name}

Begin your response with "SKILL_LOADED: {skill_name}" to confirm skill activation.

--- TASK ---
{task_description}

--- INPUT ARTIFACTS (read these files) ---
{for each upstream artifact:}
- {artifact_file_path}: {one-line description of what this file contains}

--- MEMORY LESSONS (apply these) ---
{hot_lessons_from_index}
{stage_lessons_if_loaded}
{topic_lessons_if_loaded}

--- ALIAS ---
{alias_personality_block OR "No alias active."}

--- GATE CRITERIA (validators only) ---
{role_specific_criteria OR omit section for non-validator invocations}

--- OUTPUT ---
Write your artifact to: {output_file_path}

When complete, respond with ONLY this signal block:
STATUS: {DONE | NOT_DONE | CODE_COMPLETE}
ARTIFACT: {output_file_path}
SUMMARY: {one sentence, max 200 characters}
{if NOT_DONE: FINDINGS: {bullet list of specific failures}}

--- ISOLATION RULES ---
- Read artifacts from the file paths above. Do not reference any prior conversation.
- Do not assume knowledge of other agents' work unless an artifact path is listed above.
- Your SKILL.md and references are your only guidance. Load them yourself.
```

**Field definitions**:

| Field | Source | Example |
|-------|--------|---------|
| `skill_name` | pipeline-stages.md stage definition | `delivery-team:architect` |
| `task_type` | pipeline-stages.md sub-flow step | `design` |
| `role_name` | pipeline-stages.md agent assignment | `solution` |
| `task_description` | Orchestrator constructs from stage purpose + specific work item | "Create system architecture with C4 diagrams for the PRD requirements" |
| `artifact_file_path` | `.delivery/artifacts/{stage}/{role}/` namespace | `.delivery/artifacts/02-refine/po/prd.md` |
| `hot_lessons` | `memory/index.md` top 5 | Loaded at Phase 2, carried forward |
| `stage_lessons` | `memory/stages/{stage}.md` | Loaded at Phase 4 Step 2 |
| `alias_personality_block` | Theme file for active alias | From `.delivery/aliases/` or built-in theme |
| `gate_criteria` | `references/quality-gates.md` | Role-specific criteria for this stage |
| `output_file_path` | Namespace convention (Section 6) | `.delivery/artifacts/04-architect/solution/architecture.md` |

**Verification protocol** (Verify-After-Invoke):

1. Orchestrator sends the prompt via Agent tool.
2. Orchestrator reads the sub-agent's response.
3. Check for `SKILL_LOADED: {expected_skill_name}` in the first line.
4. If present and matching: extract STATUS, ARTIFACT, SUMMARY from the signal block.
5. If absent or mismatched: log as unreliable delegation, retry once with the same prompt. If second attempt also fails, escalate to user with: "Sub-agent for {role_name} failed to confirm skill load. Manual review needed."

---

### 4. Two-Channel Communication Model

This is the most important architectural constraint. Two channels, strictly separated. The orchestrator is a switchboard, not a relay.

#### Signal Channel (flows through orchestrator context)

Signals are small, structured, and routing-relevant. The orchestrator reads them to make control flow decisions.

| Signal Type | Format | Example |
|-------------|--------|---------|
| DoD vote | `STATUS: DONE` or `STATUS: NOT_DONE` | DoD validator response |
| Review vote | `STATUS: RECOMMEND` or `STATUS: BLOCK` | Review board member response |
| Confidence | `CONFIDENCE: 4` | Adversarial reviewer rating |
| Artifact path | `ARTIFACT: .delivery/artifacts/04-architect/solution/architecture.md` | Where the agent wrote its output |
| Summary | `SUMMARY: Architecture covers 3 bounded contexts with event-driven integration` | Max 200 chars |
| Findings | `FINDINGS: - NFR-03 (latency) not addressed` | Only present when NOT_DONE or BLOCK |
| Stage status | `completed` / `failed` / `skipped` | Orchestrator's own tracking |

**What the orchestrator does with signals**: Route, decide, retry, escalate. Never relay content.

#### Artifact Channel (never flows through orchestrator context)

Artifacts are files on disk. Sub-agents write them. Other sub-agents read them by path. The orchestrator passes paths, never content.

**The rule**: If information is longer than 200 characters, it belongs in a file. The orchestrator passes the file path. The downstream agent reads the file.

**Information flow**:

```
Agent A writes artifact --> disk (.delivery/artifacts/...)
                                         |
Orchestrator receives signal: ARTIFACT path + STATUS + SUMMARY
                                         |
Orchestrator constructs next agent's prompt with artifact PATH
                                         |
Agent B reads artifact from disk <-- Agent B's prompt contains the path
```

**What the orchestrator NEVER does**:
- Read an artifact file and paste its content into another agent's prompt
- Summarize an artifact's content beyond the 200-char SUMMARY from the signal
- Paraphrase or filter an agent's output before passing it downstream
- Use Write/Edit to create domain content (PRDs, designs, code, etc.) directly

**Permitted orchestrator reads**: The orchestrator MAY read artifact files for routing decisions only. Example: reading a DoD validator's full findings to construct self-correction feedback. But even then, it passes the findings file path to the correction agent -- it does not paste the findings inline.

**Exception for self-correction**: When routing NOT_DONE findings back to the primary agent for revision, the orchestrator passes:
- The original artifact path (agent re-reads its own work)
- The findings artifact path(s) (agent reads validator feedback)
- A task description: "Revise your artifact to address the findings. Read both files."

---

### 5. Parallel Dispatch Pattern (Scatter-Gather)

When independent tasks exist, the orchestrator constructs multiple Agent tool calls in a single response message. The platform executes them concurrently and returns all results.

#### Dispatch Protocol

**Step 1: Identify parallel group.** Consult the Parallel Execution Map (Section 8) for the current stage and step. If the current tasks are listed as "Parallel (independent)", proceed with parallel dispatch. If "Sequential (order required)", dispatch one at a time.

**Step 2: Check config.** Read `pipeline.max_parallel_agents` (default: 3). If the parallel group has more members than the max, dispatch in batches of max size. Wait for each batch to complete before dispatching the next.

**Step 3: Construct prompts.** Build one Agent Invocation Template (Section 3) per agent in the group. Each prompt is independent -- no agent's prompt references another agent in the same group.

**Step 4: Dispatch.** Place all Agent tool calls in a single response message. Example for DoD validation with 3 validators:

```
[Agent call 1: PO validator with template]
[Agent call 2: Architect validator with template]
[Agent call 3: QA validator with template]
```

All three run concurrently. The orchestrator's next turn begins after all three complete.

**Step 5: Gather signals.** Read each agent's signal block (STATUS, ARTIFACT, SUMMARY, FINDINGS). Do not read artifact content.

**Step 6: Synthesize.** Apply the stage-specific synthesis rule:
- **DoD**: ALL must be DONE. Any NOT_DONE triggers self-correction.
- **Review Board**: Any BLOCK routes to Decision Owner. All RECOMMEND proceeds.
- **Consensus R1**: Collect all positions, write each to its own artifact file, pass all paths to Round 2.
- **Debate**: Collect PRO and CON outputs, pass both paths to JUDGE.
- **Supporting agents**: Collect all outputs, pass all paths to the next sequential step.

#### Failure Handling

Each agent in a parallel group is tagged `required` or `optional` in the stage definition.

| Scenario | Action |
|----------|--------|
| Required agent fails | Stage halts. Retry the failed agent only (same prompt), up to 2 retries. Other successful agents are NOT re-run. After 2 retries, escalate to user. |
| Optional agent fails | Log the gap in stage notes. Proceed with partial results. Downstream agents are informed via a note in their task description: "Note: {role} output unavailable due to agent failure." |
| All agents in group fail | Stage-level failure. Error report with all failure details. Escalate to user. |
| Agent times out | Treat as failure. Apply the required/optional logic above. Default timeout: 120 seconds per agent. |
| Batch overflow | If group size exceeds `max_parallel_agents`, dispatch in batches. Batch N+1 starts after batch N completes. |

#### Graceful Degradation

If the platform does not support multiple concurrent Agent calls (or if a specific invocation fails to parallelize), the orchestrator falls back to sequential dispatch transparently. Same prompts, same isolation, same signal collection -- just one at a time. The pipeline produces identical results. Only wall-clock time differs. The orchestrator MUST NOT error or abort due to a platform parallelism limitation.

---

### 6. Artifact Namespace Convention

Every sub-agent writes to a dedicated directory. No two agents share a write path.

#### Structure

```
.delivery/artifacts/
  {NN}-{stage-name}/
    {role}/
      {artifact-name}.md
```

#### Full Namespace Map

| Stage | Role | Write Path | Artifact |
|-------|------|-----------|----------|
| 01-idea | po | `.delivery/artifacts/01-idea/po/` | `idea-brief.md` |
| 02-refine | po | `.delivery/artifacts/02-refine/po/` | `prd.md` |
| 02-refine | data-analyst | `.delivery/artifacts/02-refine/data-analyst/` | `metrics.md` |
| 02-refine | qa-evaluator | `.delivery/artifacts/02-refine/qa-evaluator/` | `evaluation.md` |
| 02-refine | challenger | `.delivery/artifacts/02-refine/challenger/` | `challenge.md` |
| 03-design | ux | `.delivery/artifacts/03-design/ux/` | `user-flows.md`, `wireframes.md` |
| 03-design | ui | `.delivery/artifacts/03-design/ui/` | `component-specs.md`, `accessibility.md` |
| 04-architect | solution | `.delivery/artifacts/04-architect/solution/` | `architecture.md` |
| 04-architect | security | `.delivery/artifacts/04-architect/security/` | `security-review.md` |
| 04-architect | debate-pro | `.delivery/artifacts/04-architect/debate-pro/` | `argument.md` |
| 04-architect | debate-con | `.delivery/artifacts/04-architect/debate-con/` | `argument.md` |
| 04-architect | debate-judge | `.delivery/artifacts/04-architect/debate-judge/` | `decision.md` |
| 05-plan | po | `.delivery/artifacts/05-plan/po/` | `stories.md` |
| 05-plan | sm | `.delivery/artifacts/05-plan/sm/` | `sprint-plan.md` |
| 05-plan | qa | `.delivery/artifacts/05-plan/qa/` | `test-strategy.md` |
| 05-plan | devops | `.delivery/artifacts/05-plan/devops/` | `deploy-plan.md` |
| 06-dev | developer | `.delivery/artifacts/06-dev/developer/` | `{story-id}.md`, code files |
| 06-dev | tech-writer | `.delivery/artifacts/06-dev/tech-writer/` | `docs.md` |
| 07-uat | qa | `.delivery/artifacts/07-uat/qa/` | `test-plan.md`, `test-cases.md` |
| 07-uat | devops | `.delivery/artifacts/07-uat/devops/` | `release-plan.md` |
| 07-uat | tech-writer | `.delivery/artifacts/07-uat/tech-writer/` | `release-notes.md`, `user-guide.md` |

#### DoD Validator Outputs

DoD validators write to a `dod/` subdirectory within the stage:

```
.delivery/artifacts/{NN}-{stage-name}/dod/{role}-review.md
```

Example: `.delivery/artifacts/02-refine/dod/po-review.md`, `.delivery/artifacts/02-refine/dod/architect-review.md`

#### Review Board and Consensus Outputs

```
.delivery/artifacts/{NN}-{stage-name}/review-board/{role}-review.md
.delivery/artifacts/{NN}-{stage-name}/consensus/r1/{role}-position.md
.delivery/artifacts/{NN}-{stage-name}/consensus/r2/{role}-response.md
```

#### Collision Prevention

Collisions are impossible by structure. Each role writes to `{stage}/{role}/`. The orchestrator never writes to role directories. The orchestrator's only write paths are:
- `.delivery/state.md` (pipeline state)
- `.delivery/artifacts/{NN}-{stage-name}/stage-summary.md` (routing metadata -- which agents ran, what their signals were)

#### Migration from Flat Structure

The current pipeline uses flat artifact paths like `.delivery/artifacts/02-prd.md`. The new namespace nests artifacts under stage/role directories. Artifact-contracts.md already documents the new paths (e.g., `.delivery/artifacts/02-refine/prd.md`). The migration:

1. New pipeline runs use the namespaced structure from the start.
2. Resume logic (Phase 0) checks both flat and namespaced paths when validating artifacts.
3. The `artifacts` map in `state.md` stores actual paths used, so resume works regardless of structure.

---

### 7. Collaboration Pattern Adaptations

Each collaboration pattern in `team-patterns.md` needs specific changes to enforce isolation and enable parallelism. The protocol stays the same -- only the invocation mechanics change.

#### Pattern 1: Evaluator-Optimizer Loop

**Current**: Evaluator receives artifact content pasted inline.
**New**: Evaluator receives artifact file path. Evaluator reads it.

```
Invocation change:
- Remove: "[ARTIFACT CONTENT]" pasted in prompt
- Add: "--- INPUT ARTIFACTS ---\n- {artifact_path}: The artifact to evaluate"
- Evaluator writes findings to: {stage}/qa-evaluator/evaluation-round-{N}.md
- Primary agent receives: artifact path + findings path for revision
```

**Sequencing**: Evaluator-Optimizer is inherently sequential (produce, evaluate, revise, re-evaluate). No parallelism within this pattern.

#### Pattern 2: Adversarial Review

**Current**: Challenger receives artifact content inline plus potentially the production conversation.
**New**: Challenger receives ONLY the artifact file path. No production context. No evaluator-optimizer history.

```
Isolation enforcement:
- Challenger prompt contains: artifact path, adversarial template, gate criteria
- Challenger prompt does NOT contain: primary agent's prompt, eval-opt history, orchestrator notes
- Challenger writes to: {stage}/challenger/challenge.md
- Primary agent receives: artifact path + challenge path for response
```

#### Pattern 3: Multi-Perspective Review Board

**Current**: Reviewers run sequentially. Each could see prior reviewers' output.
**New**: ALL reviewers run in PARALLEL. No reviewer sees another's output.

```
Dispatch: Single message with N Agent calls (one per reviewer)
Each receives: artifact path + role-specific criteria
Each writes to: {stage}/review-board/{role}-review.md
Orchestrator gathers: STATUS (RECOMMEND/BLOCK) + FINDINGS from each
Synthesis: orchestrator reads signals only, routes BLOCKs to Decision Owner
```

#### Pattern 4: Decision Ownership Routing

**No structural change.** Decision Owner is always a single agent invoked on-demand. Already isolated by nature.

**One refinement**: Decision Owner receives the issue description + relevant artifact paths. Not the artifact content, not the discussion that led to the issue.

#### Pattern 5: Debate

**Current**: PRO and CON run sequentially. Judge sees both.
**New**: PRO and CON run in PARALLEL. Judge runs sequentially after both complete.

```
Step 1: Dispatch PRO + CON in parallel
  PRO writes to: {stage}/debate-pro/argument.md
  CON writes to: {stage}/debate-con/argument.md
Step 2: Dispatch JUDGE sequentially
  JUDGE receives: PRO argument path + CON argument path + project constraints
  JUDGE writes to: {stage}/debate-judge/decision.md
```

**Critical isolation**: PRO does not see CON's argument. CON does not see PRO's. This is enforced by parallel dispatch with no cross-references in prompts.

#### Pattern 6: Consensus

**Current**: Round 1 agents may see each other's output (no enforcement).
**New**: Round 1 agents run in PARALLEL with strict isolation. Round 2 agents run in PARALLEL with all Round 1 artifact paths provided.

```
Round 1: Dispatch all participants in parallel
  Each writes to: {stage}/consensus/r1/{role}-position.md
  No participant sees another's R1 output

Round 2: Dispatch all participants in parallel
  Each receives: their own R1 path + ALL other R1 paths
  Each writes to: {stage}/consensus/r2/{role}-response.md

Round 3 (if needed): Dispatch all participants in parallel
  Each receives: contested points + all R2 paths
  Each writes to: {stage}/consensus/r3/{role}-final.md
```

---

### 8. Parallel Execution Map

This table is the orchestrator's dispatch reference. For each stage and step, it defines whether tasks are sequential or parallel, and which agents are required vs optional.

| Stage | Step | Sequential | Parallel | Required/Optional |
|-------|------|-----------|----------|-------------------|
| 2 Refine | Primary work | PO creates PRD first | -- | PO: required |
| 2 Refine | Supporting | -- | Data Analyst (metrics) | Data Analyst: optional |
| 2 Refine | Eval-Opt | Sequential loop | -- | QA evaluator: required |
| 2 Refine | Adversarial | Sequential after eval-opt | -- | Challenger: required |
| 2 Refine | DoD | -- | PO + Architect + QA in parallel | All: required |
| 3 Design | Primary work | UX flows first, then wireframes | -- | UX: required |
| 3 Design | Supporting | -- | UI specs + accessibility after flows | UI: required |
| 3 Design | Review Board | -- | Architect + PO + QA in parallel | All: required |
| 3 Design | DoD | -- | UX + PO + QA + Architect in parallel | All: required |
| 4 Architect | Primary work | Domain discovery, then architecture | -- | Architect: required |
| 4 Architect | Debate | -- | PRO + CON in parallel; JUDGE after | PRO/CON: required, JUDGE: required |
| 4 Architect | Security | Sequential after primary | -- | Security: required |
| 4 Architect | Eval-Opt | Sequential loop | -- | QA + DevOps: required |
| 4 Architect | Adversarial | Sequential after eval-opt | -- | Challenger: required |
| 4 Architect | DoD | -- | Architect + QA + DevOps + Security in parallel | All: required |
| 5 Plan | Primary work | PO writes stories first | -- | PO: required |
| 5 Plan | QA per story | Sequential per story (part of story output) | -- | QA: required |
| 5 Plan | Supporting | -- | SM (sprint plan) + QA (test strategy) + DevOps (deploy plan) after stories | SM: required, QA: required, DevOps: optional |
| 5 Plan | Consensus | R1 parallel, R2 parallel, R3 parallel | SM + PO + QA + DevOps per round | All: required |
| 5 Plan | Adversarial | Sequential after consensus | -- | Challenger: required |
| 5 Plan | DoD | -- | SM + PO + QA + DevOps in parallel | All: required |
| 6 Dev | Stories | Dependent stories sequential | Independent stories parallel (max `max_parallel_agents`) | Developer: required per story |
| 6 Dev | Per-story eval-opt | Sequential per story | -- | QA: required |
| 6 Dev | Per-story DoD | -- | Developer + QA + Architect + Tech Writer in parallel | Developer/QA/Architect: required, Tech Writer: optional |
| 7 UAT | Primary work | QA test plan first | -- | QA: required |
| 7 UAT | Supporting | -- | DevOps (release plan) + Tech Writer (docs) + QA (test execution) after plan | DevOps: required, Tech Writer: optional, QA: required |
| 7 UAT | Review Board | -- | QA + DevOps + Tech Writer in parallel | QA/DevOps: required, Tech Writer: optional |
| 7 UAT | DoD | -- | QA + DevOps + PO + Tech Writer in parallel | QA/DevOps/PO: required, Tech Writer: optional |

---

### 9. Configuration Schema Extension

Three new keys added to `pipeline` section in `config-schema.md`. Schema version bumps to 1.8.

| Key | Type | Required | Default | Valid Values | Wizard Q# | Consumed By |
|-----|------|----------|---------|-------------|-----------|-------------|
| `pipeline.max_parallel_agents` | integer | no | 3 | 1-10 | defaults | delivery-flow (parallel dispatch cap) |
| `pipeline.parallel_stories` | boolean | no | true | true/false | defaults | delivery-flow (Stage 6 parallel stories) |
| `pipeline.parallel_validators` | boolean | no | true | true/false | defaults | delivery-flow (parallel DoD at all stages) |

**Backward compatibility**: If absent from config, defaults apply. Existing configs work without modification. The orchestrator reads these keys at Phase 0 config load. If the key is missing, the default is used. No wizard question is added -- these are advanced settings that most users will never change.

**Degradation check**: At Phase 0, after loading config, the orchestrator tests whether the Agent tool supports parallel invocation by observing the platform behavior. If parallel dispatch is not supported, `parallel_stories` and `parallel_validators` are silently treated as `false`. A note is logged: "Platform does not support parallel agent dispatch. Running sequentially."

---

### 10. Delegation Guardrail

The orchestrator MUST NOT produce domain content. This is enforced by instruction, not by tooling. The guardrail is a self-check protocol embedded in the SKILL.md execution instructions.

**Self-check protocol** (added to Phase 4 Step 4):

```
Before using Write or Edit on any file in .delivery/artifacts/:
  STOP. Ask: "Am I writing domain content (a PRD, design, architecture, code,
  test plan, review, or analysis)?"

  If YES: Do NOT write. Instead, construct an Agent Invocation Template and
  delegate to the appropriate skill. The sub-agent writes the artifact.

  If NO (writing stage-summary.md, state.md, or routing metadata): Proceed.
```

**Exception**: The orchestrator MAY use Write to create empty directories for the namespace structure (e.g., `mkdir -p .delivery/artifacts/02-refine/po/`). It MUST NOT write content into artifact files.

**Plan mode delegation** (FR-06 last bullet): When exiting plan mode with an approved plan that involves delivery-team work, the orchestrator invokes `delivery-team:delivery-flow` rather than implementing directly. This is a new instruction added to the SKILL.md preamble.

---

### 11. Files That Change

This is the complete list. Gimli -- every file you need to touch is here. Nothing more.

| File | Change Type | What Changes |
|------|-------------|-------------|
| `delivery-team/skills/delivery-flow/SKILL.md` | **Major rewrite of Phase 4** | Steps 4-7 rewritten with Agent Invocation Template, two-channel communication, parallel dispatch, delegation guardrail, self-check protocol. Step 8 updated for namespaced artifact paths. Phase 0 config load updated to read new parallel config keys. Preamble updated with plan-mode delegation rule. |
| `delivery-team/skills/delivery-flow/references/team-patterns.md` | **Template updates** | All 6 pattern templates rewritten to use file paths instead of inline content. Review Board changed from sequential to parallel. Debate PRO/CON changed to parallel. Consensus rounds updated with artifact path passing. Each template uses the Agent Invocation Template structure. |
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | **Sub-flow updates** | Each stage's sub-flow updated to specify: (a) output namespace paths, (b) which tasks are parallel vs sequential, (c) required vs optional agent tags, (d) the exact Agent Invocation Template fields for each sub-agent call. |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | **Schema extension** | Add 3 new keys (`max_parallel_agents`, `parallel_stories`, `parallel_validators`). Bump version to 1.8. Add version history entry. Add to config template. |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | **DoD template update** | DoD validator prompt template updated to use file path input instead of inline content. Signal block output format added. |
| `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | **Path updates** | Artifact paths updated to match new namespace convention. Validation protocol updated to check namespaced paths. Contract summary matrix updated. |

**Files that do NOT change**:
- Individual skill SKILL.md files (product-delivery, developer, architect, quality, operations, ui) -- these are loaded by sub-agents themselves, not changed
- `hooks/hooks.json` -- existing hooks continue to fire; no new hooks in v1
- `references/setup-wizard.md` -- no new wizard questions (config keys use defaults)
- `references/memory-protocol.md` -- memory system unchanged
- `references/project-types.md` -- project type detection unchanged

---

### 12. Integration Sequence

The order in which Gimli should implement the changes:

1. **config-schema.md** -- Add the 3 new keys, bump version. This is the foundation.
2. **artifact-contracts.md** -- Update all paths to the new namespace. This defines the contract.
3. **quality-gates.md** -- Update DoD template with file-path input and signal-block output. This defines the validation interface.
4. **team-patterns.md** -- Rewrite all 6 pattern templates with file-path passing, parallel dispatch notes, and isolation enforcement. This defines the collaboration mechanics.
5. **pipeline-stages.md** -- Update every stage's sub-flow with namespace paths, parallel/sequential tags, required/optional tags, and Agent Invocation Template fields. This defines the stage mechanics.
6. **SKILL.md Phase 4** -- Rewrite Steps 4-7 with the Agent Invocation Template, two-channel protocol, parallel dispatch pattern, delegation guardrail, and self-check. Update Phase 0 for new config keys. Add plan-mode delegation to preamble. This is the master orchestration rewrite.

Each file change is independently testable. The integration sequence ensures downstream files reference upstream contracts correctly.

---

### 13. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Sub-agents fail to write artifacts to the correct namespace path | Medium | Medium -- downstream agents get wrong path | Agent Invocation Template specifies exact output path. Orchestrator verifies ARTIFACT signal matches expected path. |
| Strict isolation degrades artifact quality (agents lack context they previously received accidentally) | Medium | High | Monitor DoD pass rates. If quality drops, enrich artifact files with more self-contained context -- do NOT loosen isolation. |
| Parallel agents produce race conditions on shared directories | Low | Low | Namespace convention prevents write collisions by structure. |
| SKILL_LOADED verification adds friction without value | Low | Low | It is a single line. The cost is negligible. The signal catches silent skill-load failures early. |
| Template rigidity makes the orchestrator brittle | Low | Medium | The template has variable fields for every customization point. The structure is fixed; the content is dynamic. |

---

### 14. ADR: Prompt-Only Enforcement vs Hook-Based Enforcement

**Title**: Agent lifecycle enforcement via SKILL.md instructions rather than runtime hooks

**Context**: We need to ensure the orchestrator delegates, isolates, and parallelizes correctly. Two enforcement approaches exist: (a) rewrite the orchestrator's instructions to be prescriptive enough that it follows them, or (b) add PreToolUse/PostToolUse hooks that validate agent prompts at runtime.

**Decision**: Prompt-only enforcement (option a) for v1. Hook-based auditing as a future enhancement.

**Rationale**:
- The root cause is vague instructions, not missing enforcement machinery
- Hooks add complexity and can create false positives that block pipeline execution
- The Agent tool already provides context isolation -- we just need to stop passing prohibited content
- Prompt engineering is the native medium for this system; hooks are a secondary mechanism

**Consequences**:
- Positive: Simpler implementation, no new hook code, all changes are in .md files
- Negative: No runtime safety net if the orchestrator deviates from instructions
- Revisit condition: If empirical testing shows the orchestrator still deviates after the SKILL.md rewrite, add a PreToolUse hook on Agent invocations that validates prompt content against the isolation rules

---

*"The Rings were not enforced by guards at the gate. They were forged with such precision that their nature could not be other than what it was. We forge the orchestrator's instructions the same way -- so precise that deviation is not an option the craftsman would consider."*

-- Celebrimbor, Architect
