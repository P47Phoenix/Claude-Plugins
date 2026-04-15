# Plugin Architecture Inventory

> Celebrimbor, Master of Eregion — a reckoning of six works, their inner wheels, and
> the diagrams that would show them true. No architecture fabricated; every claim
> traceable to the stone from which it was quarried. Scope: 6 plugins. Purpose:
> prepare ARCHITECTURE.md authoring (DOCS_ONLY). No code changes.

---

## 1. `delivery-team/` — Orchestrated Delivery Pipeline (11 sub-skills)

**What it does.** A marketplace bundle that coordinates a full delivery team through 7
stages (Idea → Refine → Design → Architect → Plan → Development → UAT) with team-based
Definition of Done, self-correction loops, adversarial review, debate/consensus
patterns, and self-learning memory. The `delivery-flow` sub-skill is the orchestrator
and NEVER produces domain artifacts itself — all domain work is delegated to worker
sub-skills via the Agent tool (Prime Directive, `delivery-flow/SKILL.md` L17-38).

**Internal components.**
- **Sub-skills (11):** `delivery-flow` (orchestrator), `product-delivery`, `developer`,
  `godot`, `architect`, `quality`, `operations`, `ui`, `user-feedback`,
  `alias-creator`, `presentation`.
- **delivery-flow references (28):** `team-patterns.md`, `pipeline-stages.md`,
  `project-types.md`, `quality-gates.md`, `config-schema.md` (+ `.json`),
  `constraints-schema.json`, `memory-protocol.md`, `feature-knowledge.md`,
  `setup-wizard.md`, `github-integration.md`, `artifact-contracts.md`, and more.
- **delivery-flow scripts:** `check_dod_constraints.py`, `validate_constraints.py`.
- **Plugin-level scripts:** `condition_evaluator.py`, `delivery_rules_adapter.py`,
  `evaluate_rules.py`, `yaml_to_rules.py`, `generate-schema.py`, `validate-config.py`,
  `validate_cross_refs.py`, `session_keepalive.py`.
- **Hooks (7 across 5 event types):** `check_config.py` (SessionStart),
  `enforce_pipeline_scope.py` (PreToolUse Skill), `audit_agent_prompt.py`
  (PreToolUse Agent), `verify_skill_load.py` (PostToolUse Agent),
  `validate_gdscript.py` (PostToolUse Write/Edit),
  `flag_empirical_validation.py` (SubagentStop), retrospective-enforcement (Stop).

**Key flow patterns.** Sequential stage pipeline with state-machine resume (checkpoint
via `.delivery/state.md`); hierarchical delegation (orchestrator → role sub-agents);
event-driven hook layer; six collaboration patterns (evaluator-optimizer loop,
adversarial review, review board, decision ownership, debate, consensus).

**External dependencies.** None required at runtime. Integrates with git/GitHub CLI
when available. Hooks shell out to `godot --headless` for GDScript validation.

**Diagram needs.**
- **Flowchart (TD) — 7-stage pipeline with DoD gates and correction loops** (primary).
- **Component diagram — orchestrator / 10 worker skills / hooks / memory boundaries**.
- **State diagram — pipeline resume state machine (`.delivery/state.md` statuses).**
- **Sequence diagram — one adversarial-review loop (maker → reviewer → correction)**.

---

## 2. `mtg-commander/` — 8-Dispatch Adversarial Deck Pipeline

**What it does.** Builds synergy-dense, format-legal, budget-compliant 100-card MTG
Commander decklists via a multi-agent pipeline. Four primary agents (Deck Builder,
Rules Judge, Optimizer, Price Evaluator) each paired with an adversarial challenger —
eight total sub-agent dispatches, NONE inlined (SKILL.md L18-37). Synergy-first card
selection via the Scryfall API.

**Internal components.**
- `SKILL.md` (orchestrator instructions + `.mtg-commander.yml` schema v1).
- `scripts/card_lookup.py` (Scryfall helper).
- `references/` (11 docs): `api-reference.md`, `archetype-patterns.md`,
  `banned-list.md`, `commander-rules.md`, `config-walkthrough.md`,
  `intake-questions.md`, `optimizer-guide.md`, `price-evaluator-guide.md`,
  `rules-judge-guide.md`, `structural-minimums.md`, `synergy-taxonomy.md`.

**Key flow patterns.** Linear 4-stage pipeline, each stage wrapping a
primary-vs-challenger adversarial loop (configurable caps via
`loops.deck_builder/rules_judge/optimizer/price_evaluator`, default 2). Config-driven
escalation (`on_loop_exhaustion: warn | block | best-effort`).

**External dependencies.** Scryfall API (public, no auth) for card lookup and pricing.

**Diagram needs.**
- **Flowchart (TD) — 4 primary stages → adversarial loop → next stage**.
- **Sequence diagram — one loop (Primary → Challenger → correction → PASS/escalate)**.
- **Class/entity diagram — `.mtg-commander.yml` schema v1 (loops, price_rules, escalation)**.

---

## 3. `agentic-flow-builder/` — ReAcTree Hierarchical Flow Toolkit

**What it does.** A guidance skill plus a reference implementation for building
production-grade agentic flows combining ReAcTree hierarchical decomposition,
Anthropic's workflow patterns, a deterministic Business Rules Engine for gating, a
dual memory system (episodic + working), and SQLite persistence with audit trails
(SKILL.md L7-16). Core philosophy: start simple, add complexity only when justified.

**Internal components.**
- `skills/flow-builder/SKILL.md` (the guidance skill).
- `scripts/` (reference implementation, 4 modules):
  - `database.py` — SQLite schema, DAL, execution tracking, audit logs.
  - `business_rules_engine.py` — deterministic AND/OR/NOT gate evaluator.
  - `flow_orchestrator.py` — hierarchical execution + episodic/working memory.
  - `agent_registry.py` — dynamic agent discovery and performance tracking.
- `references/complete_example.py` — end-to-end worked example.

**Key flow patterns.** Hierarchical (tree) decomposition; deterministic rule-driven
gates (no AI variance); dynamic agent-registry routing; dual-memory context
management; SQLite-backed audit log.

**External dependencies.** SQLite (stdlib). No external services required.

**Diagram needs.**
- **Component diagram — registry / orchestrator / BRE / DB boundaries**.
- **Class diagram — SQLite schema (nodes, executions, memory, audit_log)**.
- **Sequence diagram — one flow execution (plan → dispatch → gate → persist)**.

---

## 4. `prd-quality-gate-flow/` — 7-Gate PRD Workflow with SQLite

**What it does.** Production-grade agentic workflow that guides a PRD from idea to
completion through 7 quality gates with a deterministic Business Rules Engine, full
audit trails, and episodic memory for learning from past runs (README L1-15).

**Internal components.**
- Orchestration Python (flat layout): `prd_flow_builder.py` (build tree),
  `prd_execute.py` (run), `flow_orchestrator.py`, `business_rules_engine.py`,
  `gate_definitions.py`, `stage_definitions.py`, `schema.py`, `shared.py`.
- Utilities: `check_db.py` (DB inspection), `fix_and_run.py` (end-to-end).
- Persistence: `prd_flows.db` (SQLite), `prd_flow_diagram.txt` (ASCII reference).
- Docs: `README.md`, `QUICKSTART.md`, `IMPLEMENTATION_SUMMARY.md`,
  `DEMONSTRATION_RESULTS.md`.

**Key flow patterns.** Linear 7-gate pipeline interleaved with 8 specialized agents
(PRD Creator, Technical Reviewer, Stakeholder Orchestrator, Executive Approver,
Implementation Planner, Task Flow Generator, Evaluator, Retrospective). Gates are
deterministic (BRE) — humans sign the executive/UAT gates. SQLite persistence.

**External dependencies.** SQLite (stdlib). No external services required.

**Diagram needs.**
- **Flowchart (TD) — 7 gates + 8 agents (mirror the README ASCII diagram in Mermaid)**.
- **Class diagram — SQLite schema (flows, gates, decisions, audit)**.
- **State diagram — PRD lifecycle (draft → review → approved → implemented → closed)**.

---

## 5. `prompt-engineer/` — Focused Prompt-Optimization Skill

**What it does.** A single Opus-model skill that helps users design, display, and
iterate on LLM prompts using documented techniques (few-shot, CoT, role-playing,
output-format specification, constitutional AI, recursive prompting, tree-of-thoughts,
self-consistency) — SKILL.md enforces that every generated prompt is displayed in full.

**Internal components.** `SKILL.md` + `README.md` + `LICENSE.txt`. No scripts, no
references, no hooks. The entire plugin surface is the single skill file.

**Key flow patterns.** Single-skill router — on invocation it analyzes the use case,
selects a pattern, displays the prompt, and iterates. No pipeline, no sub-agents.

**External dependencies.** None.

**Diagram needs.**
- **Flowchart (LR) — 5-step router (Analyze → Design → Display → Explain → Iterate)**.
- *(Optional)* **Mind-map or flowchart — technique taxonomy (CoT / few-shot / ToT / …)**.

---

## 6. `research-agent/` — Auto-Routed 5-Type Research Skill

**What it does.** Systematic, academically-grounded research skill that auto-detects
research type (Exploratory, Descriptive, Explanatory, Evaluative, Comparative),
applies the matching framework (PICO / SPICE / PECO / None), and produces source-backed,
bias-aware findings with GRADE confidence ratings and explicit `[HYPOTHESIS]` /
`[INFERENCE]` labels (SKILL.md L7-22).

**Internal components.**
- `SKILL.md` (auto-detect router + phased protocol).
- `references/` (4 docs): `research-type-patterns.md`, `systematic-review.md`,
  `prompt-library.md`, `api-research.md`.

**Key flow patterns.** Decision-tree router (keyword → type); phased protocol
(Type Detection → Question Structuring → Search → Synthesis → Grading); ReAct
(Reason → Act → Observe) investigation cycles.

**External dependencies.** Optional web/API research per `api-research.md`. No
hard runtime dependency.

**Diagram needs.**
- **Flowchart (TD) — research-type decision tree (keyword → type → framework)**.
- **Sequence diagram — one ReAct cycle (Reason → Act → Observe → loop/exit)**.

---

## Diagram Count per Plugin

| Plugin | Diagrams | Types |
|---|---|---|
| `delivery-team` | 4 | flowchart, component, state, sequence |
| `mtg-commander` | 3 | flowchart, sequence, class (config schema) |
| `agentic-flow-builder` | 3 | component, class (DB), sequence |
| `prd-quality-gate-flow` | 3 | flowchart (7-gate), class (DB), state |
| `prompt-engineer` | 1-2 | flowchart (router) |
| `research-agent` | 2 | flowchart (decision tree), sequence (ReAct) |

Total target: ~16 diagrams across six ARCHITECTURE.md files.