## Idea Brief

**Project Type**: FEATURE
**Date**: 2026-03-24
**GitHub Issues**: #25 (Bug), #26 (Enhancement), #27 (Enhancement)
**Applies To**: All project types

### Problem Statement

The delivery-flow orchestrator has a fundamental execution model problem that manifests in three related ways. First, the orchestrator sometimes fails to delegate work to sub-agents entirely -- it runs tasks inline within its own context window instead of spawning dedicated agent instances (#25). This breaks context isolation and means reference documents never get loaded for the worker role. Second, even when sub-agents are spawned, they share context from the main orchestrator window (#26). The QA engineer can see the developer's reasoning. The adversarial reviewer can see the primary agent's work. This defeats the purpose of independent review -- you cannot get an honest second opinion from someone who watched you write the first one. Third, the pipeline executes everything sequentially even when tasks have no dependencies on each other (#27). DoD validators run one after another. Review board members wait in line. Independent stories are implemented one at a time. Supporting agents (Data Analyst, Challenger) queue behind the primary worker. This wastes time and does not reflect how a real team operates.

These three issues share a root cause: the orchestrator lacks a proper agent lifecycle manager that controls how agents are created, what context they receive, and whether independent agents can run concurrently.

### Target Users

- **Pipeline user (any project type)**: Every user running delivery-flow is affected. Inline execution (#25) can happen on any run. Context bleed (#26) undermines every collaboration pattern -- evaluator-optimizer, adversarial review, review board, debate, and consensus all assume isolated perspectives. Sequential execution (#27) slows every multi-agent stage.
- **Quality-sensitive user**: Users relying on adversarial review and team DoD validation to catch real problems. If the reviewer already saw the work being produced, the review is theater, not verification.
- **Large-pipeline user**: Users running GREENFIELD or GAME_DEV projects with full depth settings. These pipelines hit the most sub-agent invocations and suffer the most from sequential bottlenecks.

### Goals

1. Sub-agent delegation is reliable -- the orchestrator never falls back to inline execution when a sub-agent is specified by the pipeline stage definition
2. Each sub-agent runs in a fully isolated context, receiving only the artifact files and reference documents defined by its stage contract -- no orchestrator reasoning, no other agent output, no shared conversation history
3. Independent tasks within a stage run concurrently where the platform supports it (parallel sub-agent spawning for DoD validators, review board members, independent stories, and supporting agents)
4. Agent communication happens exclusively through artifact files in `.delivery/artifacts/` -- no context passing, no shared memory, no inline handoffs
5. All existing collaboration patterns (evaluator-optimizer, adversarial review, review board, debate, consensus) continue to function correctly under the new execution model

### Constraints

- Must work within Claude Code's sub-agent capabilities -- we cannot invent agent primitives that the platform does not support
- Artifact file contracts (defined in `references/artifact-contracts.md`) are the only sanctioned communication channel between agents
- Cannot break existing pipeline stage definitions or config schema -- changes must be backward compatible with current `.delivery/config.yml` files
- Parallel execution must degrade gracefully to sequential if the platform does not support concurrent sub-agents
- The orchestrator must remain a single coordinating agent -- we are fixing delegation, not creating a multi-orchestrator architecture
- Hook contracts (PreToolUse, PostToolUse, SubagentStop) must continue to fire correctly under the new execution model

### Initial Scope

- Agent lifecycle manager within the orchestrator that handles spawn, context loading, artifact passing, and result collection
- Strict context isolation: each sub-agent receives only its designated input artifacts and skill references, constructed fresh without orchestrator conversation history
- Parallel dispatch for independent agent groups: DoD validators (all run simultaneously, results collected and merged), review board members, independent story implementations, and supporting agents within a stage
- Artifact-only communication protocol enforced at the orchestrator level -- no context forwarding between agents
- Regression validation that all six collaboration patterns produce correct results under the new model

### Out of Scope (initial)

- Agent-to-agent direct communication (agents talk through artifacts, not to each other)
- Dynamic parallelism tuning based on system load or token budgets
- Partial result streaming from sub-agents back to the orchestrator mid-execution
- Changes to the pipeline stage definitions themselves -- this batch fixes how agents are managed, not what stages do
- Multi-orchestrator or distributed pipeline execution
- New collaboration patterns beyond the existing six
