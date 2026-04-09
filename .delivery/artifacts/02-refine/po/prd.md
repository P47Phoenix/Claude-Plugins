# PRD — Configurable Architecture Board Review Pattern

**Pipeline:** run-2026-04-08-b2c7
**Date:** 2026-04-08
**Source:** BACKLOG-003 (absorbs BACKLOG-002)
**Type:** FEATURE
**Inputs:**
- `.delivery/backlog/BACKLOG-003-architecture-board-review-pattern.md`
- `.delivery/backlog/BACKLOG-002-mar-cross-persona-iteration2.md`
- `.delivery/artifacts/research/architect-examine-decomposition-gaps.md` (Gap 4)
- `delivery-team/skills/delivery-flow/references/team-patterns.md` (Multi-Perspective Review Board, §Pattern 3)
- `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`
- arXiv:2512.20845 — Multi-Agent Reflexion (MAR)

## Problem

A wizard does not choose his council by drawing lots, yet our pipeline does precisely that. Gap 4 of the architect decomposition examination finds the Multi-Perspective Review Board (`team-patterns.md:334-416`) frozen to a fixed 3-role roster (Technical / Business / Risk), with no configurable roster, no per-reviewer persona context, no iteration loop with convergence criterion, and no judge role. The config schema (`config-schema.md`) contains no `architecture_board` block. The primitive exists; the specialization does not. Architecture review — the very stage where persona diversity matters most — is being conducted with one eye closed.

## Users / Actors

- **Orchestrator** — dispatches N reviewer sub-agents per configured board, enforces isolation, invokes the judge, emits the verdict
- **Reviewer sub-agents (N)** — each loads only its own persona's context slice and prompt, emits one review artifact
- **Judge sub-agent** — synthesizes the N reviews into a single verdict (PASS / CONDITIONAL / BLOCK) with findings
- **PO / human** — selects board composition per run by editing `.delivery/config.yml`

## Functional Requirements

- **FR-1** — New `architecture_board` config block in `config-schema.md` with: `enabled` (bool), `reviewers` (list of persona IDs), `max_iterations` (int), `convergence_criterion` (enum: `all_reviewers_done` | `judge_verdict_pass`), `judge` (persona ID)
- **FR-2** — Reviewer persona library at `delivery-team/skills/delivery-flow/references/architecture-board-personas.md` containing ≥3 starter personas: **Volatility Architect**, **DDD Architect**, **Risk Architect** (minimum); **Evolutionary Architect** and **Security Architect** as stretch
- **FR-3** — Each persona declares: `id`, `name`, one-line perspective, context-loading instructions (what files to read), review prompt template, gate criteria (what the persona looks for), signal format
- **FR-4** — Judge persona declares: synthesis protocol, deadlock rule (link to the existing debate pattern's DEADLOCK handling in `team-patterns.md`), final verdict schema (`PASS` | `CONDITIONAL` | `BLOCK` + synthesized findings list)
- **FR-5** — New `architecture-board` collaboration pattern documented in `team-patterns.md` with full protocol: trigger conditions, parallel dispatch rules, iteration loop, judge invocation, output artifact paths (`.delivery/artifacts/04-architect/board/<persona-id>.md` + `judge-verdict.md`)
- **FR-6** — Stage 4 Architect integration in `pipeline-stages.md` — orchestrator checks `architecture_board.enabled` and dispatches reviewers in parallel after the primary architect produces `architecture.md`
- **FR-7** — MAR iteration-2 cross-persona routing — on iteration 2 of the self-correction loop, a *different* reviewer persona reviews the correction (absorbs BACKLOG-002)
- **FR-8** — Dogfood — run the architecture_board on THIS pipeline's (`run-2026-04-08-b2c7`) Stage 4 with ≥3 configured reviewers

## Non-Functional Requirements

- **NFR-1** — Board adds ≤25% token overhead per Architect stage (MAR paper benchmark)
- **NFR-2** — Backwards compat — pipelines without an `architecture_board` block run unchanged; default is disabled
- **NFR-3** — Reviewer context isolation — no reviewer's prompt contains another reviewer's output (enforced by agent prompt audit hook)

## Acceptance Criteria

1. `architecture_board` block documented in `config-schema.md` and accepted by `validate_config.py`
2. `architecture-board-personas.md` exists with ≥3 personas conforming to FR-3 shape
3. Judge role defined per FR-4; deadlock rule cites existing debate pattern
4. `team-patterns.md` contains the new `architecture-board` pattern (FR-5)
5. `pipeline-stages.md` Stage 4 references board dispatch (FR-6)
6. Iteration-2 cross-persona routing implemented and testable (FR-7)
7. Dogfood run on `run-2026-04-08-b2c7` Stage 4 produces ≥3 review artifacts plus one judge verdict
8. Token overhead measurement ≤25%
9. A run with no `architecture_board` block completes without error (backwards compat)

## Out of Scope

- BACKLOG-005 paradigm-as-skill (separate pipeline run)
- BACKLOG-006 transformation planning (separate pipeline run)
- Rewriting the existing fixed Multi-Perspective Review Board
- Wiring the board into stages beyond Stage 4 Architect
- New top-level collaboration pattern categories

## Success Metrics

- Dogfood run emits N=3 distinct review artifacts from 3 distinct personas
- Judge verdict artifact synthesized and persisted
- Token overhead ≤25% (NFR-1)
- Backwards-compat test (no `architecture_board` block) passes green

## Risks + Mitigations

- **R1: Persona redundancy** — two personas produce near-identical reviews. *Mitigation:* persona library enforces distinct `perspective` one-liners and non-overlapping gate criteria; reviewer-set validator warns on overlap.
- **R2: Judge echo chamber** — judge merely averages rather than synthesizes. *Mitigation:* judge prompt requires citing each reviewer's findings individually and declaring explicit agreement/disagreement per finding before issuing the verdict.
- **R3: Token cost explosion** — N reviewers × iterations blows the budget. *Mitigation:* NFR-1 25% cap enforced via `max_iterations` (≤3) and `max_reviewers` (≤6) ceilings; measured in dogfood run.
- **R4: Backwards compat breakage** — existing pipelines fail when loading new schema. *Mitigation:* NFR-2 default-disabled; `architecture_board` block marked optional in schema; regression test run against a prior pipeline config.
