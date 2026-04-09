# Idea Brief — Configurable Architecture Board Review Pattern

**Pipeline:** run-2026-04-08-b2c7 (FEATURE) | **Source:** BACKLOG-003 (absorbs BACKLOG-002) | **Author:** PO (Gandalf)

## The Burden

Many counselors gathered at the council, yet our Review Board admits only three seats — Technical, Business, Risk — and those chairs are nailed to the floor. Gap 4 of `architect-examine-decomposition-gaps.md` names it plain: the Multi-Perspective Review Board (`team-patterns.md:334-416`) has a fixed 3-role roster, no configurable reviewer personas, no agentic loop with convergence criterion, and no judge role. The config schema holds no `architecture_board` block. The primitive exists; the specialization does not.

## The Vision

A new collaboration pattern, `architecture_board` — a specialization of the Review Board in which N reviewers (configurable per run or per stage) are summoned, each with its own isolated context, its own perspective (Volatility Architect, DDD Architect, Evolutionary, Risk, Security — any subset the config names), its own prompt. An agentic loop with an iteration cap and a convergence criterion drives them. A Judge sub-agent — the wise one at the head of the table — synthesizes the several verdicts into one. The iteration-2 cross-persona routing from BACKLOG-002 (MAR, arXiv:2512.20845) is absorbed: when self-correction enters its second round, a *different* reviewer reads the correction. Persona diversity across rounds is load-bearing.

## Scope IN

- New `architecture_board` config block in `config-schema.md`
- New pattern documented in `team-patterns.md` (augmenting, not replacing, the existing Review Board)
- Reviewer persona library at `architecture-board-personas.md` (≥3 starter personas)
- Judge role definition (synthesis protocol, deadlock rule, verdict schema)
- Stage 4 Architect integration (primary insertion point)
- Dogfood: run the board on THIS pipeline's Stage 4

## Scope OUT

- BACKLOG-005 paradigm-as-skill (its own pipeline)
- BACKLOG-006 transformation planning (its own pipeline)
- Rewriting the existing Review Board (augment only)
- Wiring the board into every stage (Architect-only for MVP)

## The Stakes (measurable)

1. Pattern documented in `team-patterns.md`
2. ≥3 reviewer personas in the library file
3. ≥1 judge role defined
4. Config schema accepts `architecture_board` block and validates
5. Dogfood run emits N distinct review artifacts from N distinct personas plus a synthesized judge verdict

## Anti-Scope

No changes to the existing fixed Review Board. No new top-level pattern categories beyond the 6 existing. No pipeline-wide loop.

## The Road

- **Refine** — PRD + constraints.yml (this dispatch)
- **Design** — dispatch flow, artifact layout
- **Architect** — pattern protocol, config schema extension, persona library shape
- **Plan** — stories, sequencing, dogfood run plan
- **Development** — author personas, wire orchestrator, update references
- **UAT** — dogfood run produces required artifacts; acceptance criteria met
