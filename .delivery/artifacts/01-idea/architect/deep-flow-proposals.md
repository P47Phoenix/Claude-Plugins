# Deep Flow Proposals — delivery-team Architecture Supplements

> *Celebrimbor of Eregion, master smith: I have walked the ring-graven halls of
> `delivery-flow` and read its true inscriptions. The high map at
> `delivery-team/ARCHITECTURE.md` (250 lines, at cap) names the wheels but does
> not show their teeth. What follows are seven supplementary forgings — each a
> discrete flow diagram set under a new `delivery-team/architecture/` forge-room,
> built on load-bearing evidence from the codebase. No ornament fabricated.*

## Honest Framing

- The existing `ARCHITECTURE.md` covers component overview, 7-stage pipeline,
  project-type routing, a pattern table, state/memory stub, and hook table. It
  does NOT drill into decision trees, state machines, or sequence choreography.
- **On the BRE**: the literal `business_rules_engine.py` lives in
  `prd-quality-gate-flow/` (and is referenced by `agentic-flow-builder/`).
  delivery-team has NO BRE module. Its deterministic gating is the DoD validator
  panel + routing matrix + project-type detection + confidence-rating thresholds.
  The supplement must document that relationship honestly, not invent one.
- Seven proposals below are ranked by value to the PO's explicit asks
  (adversarial triggers, BRE usage) and by gaps I observed.

---

## Proposal 1 — Adversarial Review Trigger Flow (PO explicit ask)

- **Filename**: `delivery-team/architecture/adversarial-review-triggers.md`
- **Audience**: both
- **Why it matters**: The current doc lists adversarial review as one of six
  patterns in a one-line table cell. It does not show WHEN it fires (stages
  2/4/5 only — SKILL.md L626, L662, L680), the confidence 1–5 escalation
  threshold (`team-patterns.md` L131 — `confidence <= 2` escalates
  immediately), the isolated-loop variant (Pattern 2b), or the interaction
  with DoD. This is the PO's #1 ask.
- **Diagrams**:
  1. **Flowchart** — decision tree: stage entry → is stage in {Refine,
     Architect, Plan}? → run evaluator-optimizer first → then challenger
     dispatch → confidence rating branch (1–2 escalate | 3–5 revise) → loop
     bound check.
  2. **Sequence** — orchestrator → primary → evaluator → primary revision →
     challenger (isolated) → confidence branch → human if ≤2.
  3. **Flowchart** — light-mode suppression: Pattern 2 is SKIPPED when
     `stage_mode == light` (SKILL.md L304); show the routing gate.
- **Complexity**: **M**

## Proposal 2 — Deterministic Gating & BRE Relationship Flow (PO explicit ask)

- **Filename**: `delivery-team/architecture/deterministic-gating.md`
- **Audience**: contributor
- **Why it matters**: PO asked about BRE usage. Truth: delivery-team has no
  BRE. Its determinism emerges from four layered mechanisms — (a) Phase 1
  project-type detection, (b) routing matrix (full/light/skip per type/stage),
  (c) DoD validator unanimity rule (`quality-gates.md` L16: "ALL validators
  must return DONE"), (d) confidence-rating thresholds
  (`team-patterns.md` L131). This doc must ALSO cite the sister plugins'
  real BRE (`prd-quality-gate-flow/business_rules_engine.py`,
  20 rules across 7 gates) and contrast the two approaches: rule-DSL-in-SQLite
  vs. distributed-validator-consensus. No pretending delivery-team has what it
  does not.
- **Diagrams**:
  1. **Flowchart** — the four deterministic layers in delivery-team, with
     inputs and verdicts per layer.
  2. **Side-by-side flowchart** — delivery-team gate (N validators, unanimous
     DONE) vs. prd-quality-gate-flow gate (BRE rule tree, AND/OR/NOT → single
     decision). Shows where each is appropriate.
- **Complexity**: **M**

## Proposal 3 — DoD Validation & Self-Correction State Machine

- **Filename**: `delivery-team/architecture/dod-self-correction.md`
- **Audience**: both
- **Why it matters**: The existing doc's state diagram (L170-185) has one
  `correcting` node. Reality: validators dispatch in parallel
  (`pipeline.parallel_validators`, SKILL.md L516), findings aggregate, primary
  revises against ALL NOT_DONE findings at once, max 3 rounds
  (SKILL.md L529), then escalation. The `CODE_COMPLETE` status for Stage 6
  (empirical pending, carried to Stage 7 — SKILL.md L699) is a third verdict
  the current doc omits entirely. The delegation meta-gate
  (`quality-gates.md` L56-72) is also invisible upstream.
- **Diagrams**:
  1. **State diagram** — `validator_pending` → `aggregating` →
     `{all_done | mixed | all_not_done}` → `correcting` (counter++) →
     back to `validator_pending` → terminal `stage_complete | escalated |
     deferred_to_uat (CODE_COMPLETE)`.
  2. **Sequence** — parallel validator fan-out, finding aggregation,
     correction prompt assembly, delegation meta-gate check, re-dispatch.
- **Complexity**: **M**

## Proposal 4 — Dynamic Escalation Decision Tree

- **Filename**: `delivery-team/architecture/dynamic-escalation.md`
- **Audience**: both
- **Why it matters**: SKILL.md L826-835 lists six triggers but the high-level
  doc does not map them. Each trigger has a distinct detector, a distinct
  "Attempts" narrative, and a distinct recommended user option set (provide
  guidance | override | redirect | abort — SKILL.md L853-858). A trigger
  table plus decision tree would let a contributor add a new trigger without
  archaeology.
- **Diagrams**:
  1. **Flowchart** — per-stage monitoring loop: after every iteration, evaluate
     six trigger conditions in priority order → if any fires → build
     escalation payload → present to user → branch on user choice.
  2. **Sequence** — how `Repeated DoD failure` and `Low adversarial confidence`
     interact when both could fire in the same stage (priority ordering).
- **Complexity**: **S**

## Proposal 5 — Architecture Board Loop (recently shipped)

- **Filename**: `delivery-team/architecture/architecture-board.md`
- **Audience**: advanced user
- **Why it matters**: Listed in ARCHITECTURE.md L198 under "recently-shipped
  primitives" with one line. Actual protocol (`team-patterns.md` L420-468)
  has: parallel N-reviewer dispatch with per-persona context files, judge
  synthesis → verdict, iteration-2 MAR cross-persona routing rule (BACKLOG-002
  absorbed), convergence detection, deadlock escalation via Debate pattern.
  This is load-bearing for Stage 4 and deserves its own diagram set.
- **Diagrams**:
  1. **Sequence** — orchestrator → N reviewers (parallel) → judge → verdict;
     each reviewer shows only its persona-specific `context-files-to-load`.
  2. **State diagram** — iteration 1 (independent) → judge → not converged →
     iteration 2 (MAR cross-persona routing: reviewer A sees reviewer B's
     findings by persona, never full prompt) → convergence or DEADLOCK →
     Debate fallback.
- **Complexity**: **L**

## Proposal 6 — Sub-Agent Dispatch & Two-Channel Communication

- **Filename**: `delivery-team/architecture/agent-dispatch.md`
- **Audience**: contributor
- **Why it matters**: The Prime Directive (orchestrator writes no domain
  artifacts) and two-channel rule (signals in response, artifacts on disk —
  `artifact-contracts.md`) are the most violated conventions in the repo
  (the `audit_agent_prompt.py` and `enforce_pipeline_scope.py` hooks exist
  precisely for this). A diagram of "correct dispatch" vs. "common violations"
  would prevent more harm than any prose. Also covers the compound-role
  detector (`quality-gates.md` L49-53) and the delegation meta-gate.
- **Diagrams**:
  1. **Sequence** — correct path: orchestrator → Agent call with scoped prompt
     + paths → sub-agent reads inputs from disk → writes artifact to disk →
     returns ≤200-char signal block → orchestrator reads signal only.
  2. **Flowchart** — anti-pattern detection: orchestrator direct Write to
     `artifacts/**` → hook blocks (ADR-001 layered origin detection) → or
     compound-role prompt → audit_agent_prompt.py warns.
- **Complexity**: **M**

## Proposal 7 — Hook Firing Sequence & Pipeline Timeline

- **Filename**: `delivery-team/architecture/hook-timeline.md`
- **Audience**: contributor
- **Why it matters**: ARCHITECTURE.md L210-223 is a static hook table.
  Contributors adding a hook need the TEMPORAL picture: when does
  `check_config.py` fire relative to Phase 0? When does
  `flag_empirical_validation.py` fire relative to CODE_COMPLETE?
  Where does the Stop hook's retrospective enforcement sit relative to
  `.delivery/state.md` deletion?
- **Diagrams**:
  1. **Sequence (timeline)** — horizontal lanes for {User, Session,
     Orchestrator, Sub-Agents, Hooks, State}. Shows SessionStart →
     PreToolUse(Skill) → PreToolUse(Agent) → sub-agent execution →
     PostToolUse(Write/Edit) → PostToolUse(Agent) → SubagentStop → next
     iteration → eventually Stop.
  2. **Flowchart** — hook outcomes: each hook's block/warn/pass paths and
     what the orchestrator does on each (the `check_config.py` block
     interrupts Phase 0; the empirical-validation flag modifies the
     Stage 6→7 handoff).
- **Complexity**: **M**

---

## Recommended Sequence

Forge in this order — each builds shared vocabulary for the next:

1. Proposal 6 (dispatch) — foundation vocabulary
2. Proposal 3 (DoD state machine) — uses dispatch
3. Proposal 1 (adversarial triggers) — uses DoD states
4. Proposal 4 (escalation) — aggregates triggers from 1 and 3
5. Proposal 2 (determinism vs. BRE) — PO ask, synthesizes 3 and 4
6. Proposal 5 (architecture board) — specialized application
7. Proposal 7 (hook timeline) — contributor-facing reference, written last

## Explicitly Deferred

- **Memory read/write lifecycle** — `memory-protocol.md` is already dense and
  well-structured; a diagram-only supplement would duplicate, not add.
- **State persistence & resume** — SKILL.md Step 8.5 and the atomic-write
  protocol are short enough to stay in the main doc; no separate deep flow
  earns its keep.
- **Self-correction as a standalone doc** — folded into Proposal 3 to avoid
  artificial splits.

*Thus ends the reckoning. Seven rings proposed; three set aside with reason.*
— Celebrimbor
