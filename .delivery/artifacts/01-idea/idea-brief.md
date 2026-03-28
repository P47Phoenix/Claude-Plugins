## Idea Brief: Delivery Pipeline Orchestrator Stalls After Agent Completion

**Project Type**: BUG_FIX
**Date**: 2026-03-27
**GitHub Issue**: #49

### Problem Statement

The delivery-flow orchestrator intermittently stalls after all sub-agents complete their work and return results. The pipeline stops progressing -- no further output, tool calls, or stage transitions occur until the user manually sends another message to "wake" it.

This manifests most frequently:
- Between pipeline stages (e.g., after Stage 2: Refine completes, before Stage 3: Design begins)
- After parallel DoD validators all return DONE/NOT_DONE signals
- After checkpoint reviews where multiple agents contributed results
- During long pipeline runs where context window pressure is highest

**Impact**:
- **User experience**: Users must babysit the pipeline and send nudge messages to keep it moving, defeating the purpose of automated orchestration
- **Pipeline reliability**: Stalls introduce unpredictable delays and break the flow state of the orchestrator's multi-stage execution
- **Trust**: Intermittent failures erode confidence in the pipeline's ability to run autonomously through stages
- **Dogfooding blocker**: The team cannot reliably use delivery-flow on its own work if the pipeline stalls mid-run

### Root Cause Hypothesis

This is a SKILL.md-level bug -- the orchestrator is prompt-driven, not code. The likely root causes are:

1. **Missing explicit continuation directives after agent returns**: When multiple parallel Agent tool calls complete, the orchestrator's SKILL.md does not contain strong enough instructions to immediately process results and advance. The model may "satisfy" itself that work is done without recognizing it must continue to the next step.

2. **Context window pressure during long runs**: By mid-pipeline, the context window contains the full SKILL.md, multiple agent prompts/responses, accumulated artifacts, and state tracking. The orchestrator's "what to do next" instructions may be pushed far enough from the model's attention window that it loses track of the pipeline sequence.

3. **Ambiguous state after parallel completion**: When multiple validators return in parallel, the orchestrator must aggregate results (all DONE? any NOT_DONE?) and decide the next action. If the aggregation logic in SKILL.md is not explicit enough, the model may stall on an implicit decision point.

4. **No self-recovery mechanism**: When the orchestrator loses its place, there is no "heartbeat" or self-check instruction that forces it to re-examine pipeline state and continue.

### Target Users

1. **Anyone running delivery-flow** -- this affects all pipeline executions, all project types
2. **The delivery-team itself** -- dogfooding the pipeline is a P0 gate, and stalls block that

### Proposed Scope

#### 1. Investigate: SKILL.md Phase 4 Execution Protocol

Audit the delivery-flow SKILL.md sections that govern:
- Post-agent-return behavior (what happens after an Agent tool call completes)
- Stage transition logic (how the orchestrator moves from one stage to the next)
- DoD aggregation (how parallel validator results are collected and acted on)
- Checkpoint presentation (how results are surfaced to the user)

Identify any locations where the orchestrator's next action is implicit rather than explicit.

#### 2. Fix: Add Explicit Continuation Directives

For every point where the orchestrator receives agent results, ensure SKILL.md contains an unambiguous "IMMEDIATELY DO X NEXT" instruction. Candidate patterns:
- After each Agent tool call return: "Process result, then proceed to [next step]"
- After all parallel validators return: "Aggregate results. If all DONE, advance to [next stage]. If any NOT_DONE, trigger self-correction loop"
- After checkpoint reviews: "Present summary to user, then wait for user input before proceeding"
- At stage boundaries: "You are now entering Stage N. Execute the following steps in order..."

#### 3. Fix: Add Pipeline State Anchoring

Add a lightweight state-tracking pattern to SKILL.md that the orchestrator maintains throughout execution:
- Current stage number and name
- Current step within the stage
- Pending actions (what must happen next)
- This state block should be re-emitted after every major action to keep it in the model's recent context

#### 4. Fix: Add Self-Recovery Check

Add an instruction that triggers when the orchestrator has not made progress:
- "If you have received all agent results but have not yet taken the next action, re-read the pipeline state and continue immediately"
- This acts as a safety net for cases where the model loses track despite explicit directives

#### 5. Validate: Dogfood the Fix

Run delivery-flow on a real task (this bug fix itself, or another queued item) and observe:
- Does the pipeline advance through all stages without stalling?
- Do parallel validator returns get processed correctly?
- Does the orchestrator maintain awareness of its pipeline position?

### Key Design Decisions

#### 1. Prompt-level fix, not architectural change

**Decision**: Fix this in SKILL.md instructions, not by adding external state management code or keepalive scripts.

**Rationale**:
- The orchestrator is prompt-driven by design -- adding code-based state management would create a parallel control plane
- The root cause is insufficient directive clarity in the prompt, not a missing software component
- Prompt fixes are faster to iterate on and can be validated through dogfooding immediately
- If prompt-level fixes prove insufficient, escalation to architectural changes becomes a separate follow-up item

#### 2. State anchoring over state persistence

**Decision**: Use in-context state re-emission (anchoring) rather than file-based state persistence to maintain pipeline position.

**Rationale**:
- File-based state adds tool call overhead (read/write on every step)
- The problem is attention/context loss within a single session, not cross-session state recovery (that is a separate feature)
- Re-emitting a compact state block keeps the "where am I" information in the model's recent context window where it has highest attention

#### 3. Explicit over implicit at every decision point

**Decision**: Every point where the orchestrator must decide what to do next gets an explicit instruction, even if it seems obvious.

**Rationale**:
- "Obvious" next steps are only obvious to a human reader -- the model needs explicit directives especially under context pressure
- Redundancy in orchestrator instructions is preferable to ambiguity
- This follows the established pattern in the SKILL.md where explicit step-by-step protocols outperform high-level descriptions

### Risks & Open Questions

#### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Prompt bloat from added directives | Increases SKILL.md token count, worsening context pressure -- the very problem we are fixing | Keep directives concise; use structured formats (numbered lists, state blocks) that compress well; measure token count before and after |
| State anchoring adds noise to output | User sees repeated state blocks that are not meaningful to them | Format state blocks as brief inline markers, not verbose dumps; consider using XML tags the model tracks but the user can skim |
| Fix masks deeper architectural issue | Prompt-level patches may not be durable if the real problem is context window limits | Track stall frequency post-fix; if stalls persist, escalate to architectural investigation (chunked context, external state store) |
| Regression in other orchestrator behaviors | Changes to SKILL.md execution protocol could break working stage transitions | Test fix across multiple project types (FEATURE, BUG_FIX, GREENFIELD) during dogfooding |

#### Open Questions

1. **Which specific SKILL.md sections contain the gap?** The investigation step must identify exact locations before writing fixes. The hypothesis points to Phase 4 execution protocol and DoD aggregation, but the actual gap may be elsewhere.
2. **Is there a context window size threshold where stalls become likely?** If stalls only occur after N tokens of context, the fix may need to include context management strategies (summarization, artifact offloading) in addition to continuation directives.
3. **Do stalls correlate with parallel agent count?** If stalls only happen with 3+ parallel validators but never with sequential execution, the fix should focus specifically on parallel result aggregation.
4. **Should the orchestrator emit a "CONTINUING" signal after processing each agent return?** This would make stalls immediately visible (absence of signal = stall) and give the user confidence the pipeline is progressing.
