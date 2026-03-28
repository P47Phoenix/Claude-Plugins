# Sprint Plan: Fix Pipeline Orchestrator Stalls (Issue #49)

**Project Type**: BUG_FIX (light mode)
**Date**: 2026-03-27
**GitHub Issue**: #49
**Inputs**: Idea Brief v1.0

---

## Capacity Declaration

| Metric | Value |
|--------|-------|
| Velocity baseline | 8 pts/sprint |
| 80% ceiling | 6 pts |
| Committed this sprint | 3 pts |
| Buffer | 3 pts (reserved for investigation variance) |

---

## Story: Fix Orchestrator Stalls After Agent Completion

**ID**: BUG-49
**Points**: 3
**Priority**: P0

### User Story

**As a** delivery-flow user,
**I want** the pipeline orchestrator to immediately continue execution after sub-agents return results,
**So that** the pipeline runs autonomously through all stages without requiring manual nudge messages.

### Acceptance Criteria

#### AC-1: Immediate continuation after parallel DoD validators complete

**Given** multiple parallel DoD validators have been dispatched
**When** all validators return their DONE/NOT_DONE signals
**Then** the orchestrator immediately aggregates results and either advances (all DONE) or triggers self-correction (any NOT_DONE), with no pause requiring user intervention

#### AC-2: Immediate stage advancement after stage completion

**Given** the current stage has completed all its steps and produced its artifacts
**When** the stage is marked complete
**Then** the orchestrator immediately emits a state anchor and begins the next stage, with no stall between stages

#### AC-3: Immediate continuation after checkpoint approval

**Given** the orchestrator has presented a checkpoint for user review
**When** the user approves the checkpoint
**Then** the orchestrator immediately continues to the next step or stage, with no stall after approval

#### AC-4: Full pipeline completion without stalls

**Given** a pipeline run of 5 or more stages (e.g., FEATURE or GREENFIELD project type)
**When** the pipeline executes from start to finish
**Then** all stage transitions occur without stalling, and the pipeline completes without requiring any manual nudge messages

#### AC-5: Self-recovery from stalled state

**Given** the orchestrator has received all agent results but has not taken the next action
**When** the orchestrator detects it has not progressed (no tool call, no output, no stage transition)
**Then** it re-reads the current pipeline state and immediately continues execution

---

### Test Cases

#### TC-1: Parallel DoD validator continuation (covers AC-1)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Trigger a stage that dispatches 3+ parallel DoD validators | Validators are dispatched in parallel |
| 2 | All validators return DONE | Orchestrator emits aggregation result within its next output block |
| 3 | Observe orchestrator behavior | Orchestrator advances to next stage without user sending a message |
| 4 | Repeat with one validator returning NOT_DONE | Orchestrator triggers self-correction loop immediately |

#### TC-2: Stage transition without stall (covers AC-2)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run a BUG_FIX pipeline (stages: Idea, Refine, Design, Plan, Development, UAT) | Pipeline starts at Stage 1 |
| 2 | Complete Stage 2 (Refine) | Orchestrator emits state anchor showing "Entering Stage 3: Design" |
| 3 | Observe transition timing | No gap where orchestrator stops producing output between stages |
| 4 | Verify state anchor content | State anchor includes: current stage, current step, pending actions |

#### TC-3: Post-checkpoint continuation (covers AC-3)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Pipeline reaches a checkpoint (e.g., end of Refine) | Orchestrator presents checkpoint summary to user |
| 2 | User approves checkpoint | Orchestrator immediately continues to next stage |
| 3 | Observe orchestrator output | Next stage begins in the same response or immediately following response |

#### TC-4: Full pipeline run without stalls (covers AC-4)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Start a FEATURE pipeline (7 stages) | Pipeline begins at Idea stage |
| 2 | Allow pipeline to run through all stages | Each stage transition occurs without manual intervention |
| 3 | Count any stalls requiring user nudge | Stall count = 0 |
| 4 | Verify all 7 stages completed | Pipeline reaches UAT and completes |

#### TC-5: Self-recovery mechanism (covers AC-5)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Observe a pipeline run under context pressure (large artifacts, many agent returns) | Pipeline is mid-execution |
| 2 | If orchestrator pauses after receiving agent results | Self-recovery instruction triggers |
| 3 | Observe recovery behavior | Orchestrator re-reads pipeline state and continues without user message |
| 4 | Verify recovery output | Orchestrator emits a continuation signal indicating self-recovery activated |

#### TC-6: Dogfooding validation (covers AC-1 through AC-5)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Use delivery-flow to run this bug fix (issue #49) through the pipeline | Pipeline executes on its own codebase |
| 2 | Monitor for any stalls throughout the run | Zero stalls requiring manual nudge |
| 3 | Verify all stage transitions are smooth | Each transition includes a state anchor |
| 4 | Confirm fix does not regress other orchestrator behaviors | Checkpoint presentation, DoD validation, and self-correction all work correctly |

---

### Implementation Scope

All changes target `delivery-team/delivery-flow/SKILL.md`:

1. **Continuation directives** -- Add explicit "IMMEDIATELY DO X NEXT" instructions after every agent return point in Phase 4 execution protocol
2. **State anchoring blocks** -- Add compact state re-emission pattern at stage transitions (current stage, current step, pending actions)
3. **Self-recovery instructions** -- Add fallback instruction: "If you have received all agent results but have not taken the next action, re-read pipeline state and continue immediately"
4. **Token impact measurement** -- Measure SKILL.md token count before and after; directive additions must not exceed ~500 tokens net increase

### Definition of Done

- [ ] All 5 acceptance criteria verified via test cases
- [ ] Dogfooding gate passed (TC-6)
- [ ] SKILL.md token count delta measured and documented
- [ ] No regression in existing pipeline behaviors

---

## Sprint Summary

| Item | Detail |
|------|--------|
| Sprint goal | Fix pipeline orchestrator stalls after agent completion (issue #49) |
| Stories committed | 1 (BUG-49: 3 pts) |
| Capacity used | 3 / 6 pts (50%) |
| Risk | Prompt bloat worsening context pressure; mitigated by 500-token ceiling on additions |
| Validation gate | Dogfooding (P0) |
