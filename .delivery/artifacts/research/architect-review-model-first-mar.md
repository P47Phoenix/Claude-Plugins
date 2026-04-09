# Architect Review: Model-First Reasoning & Multi-Agent Reflexion

**Role:** Solution Architect | **Date:** 2026-04-08
**Scope:** Applicability to `delivery-team` plugin (delivery-flow orchestrator + worker skills)

---

## 1. Model-First Paradigm — Structural Fit

The paper's two-phase approach (explicit entities/state/actions/constraints model BEFORE planning) maps onto three candidate insertion points:

- **(a) Refine stage** — PRD acceptance criteria today are prose-shaped. A pre-AC modeling step (entities, state variables, invariants, constraints) would harden criteria and give downstream stages a machine-checkable contract. FKCs already partially do this, but FKCs are *feature-scoped* and authored late; they are not a front-loaded reasoning substrate.
- **(b) Architect stage** — ADRs implicitly encode a domain model, and `architect` already runs Prior Art Analysis + classification tables. This is the *closest existing analog* to Model-First, but it operates on *architectural* entities (components, boundaries), not *problem-domain* entities (business state, rules, constraint variables).
- **(c) Plan stage** — Story decomposition as constrained planning is attractive but premature: without a shared model from Refine, Plan would re-derive it per story.

**Highest-leverage insertion point: Refine stage.** Rationale: (1) earliest point where hallucinated constraints are cheapest to fix; (2) the explicit model becomes a *single source of truth* consumed by Architect (domain model input), Plan (constraint-aware decomposition), Developer (invariants as test oracles), and Quality (property-based test seeds); (3) it fills a real gap — no current artifact captures state variables and constraints in a structured form. Architect's classification table is the right *pattern* but wrong *stage* for problem-domain modeling.

Implementation sketch: a new Refine sub-artifact `problem-model.yml` (entities, state_vars, actions, constraints, invariants) gated before acceptance criteria drafting. Low schema cost, high downstream leverage.

## 2. MAR — Overlap with Existing Patterns

The plugin already has **Debate** (with a Judge synthesizer), **Adversarial Review**, and **Multi-Perspective Review Board**. Assessing MAR's deltas:

- **(a) Persona-diverse reflection vs. Review Board:** Largely duplicative. Review Board already spawns role-scoped reviewers (security, data, UX, ops) whose critiques are multi-persona by construction. MAR's novelty is applying this to *reflection on prior agent output*, not review of artifacts — a subtle but real distinction.
- **(b) Judge role comparison:** Our Debate Judge already synthesizes competing positions. MAR's judge is functionally equivalent; no uplift.
- **(c) Act/diagnose/critique/aggregate separation vs. self-correction loop:** Our current self-correction loop (max 3 iterations) collapses *diagnose* and *critique* into one step, usually performed by the same sub-agent that acted. This is the one place MAR offers genuine structural improvement — separating **diagnosis** (what failed and why) from **critique** (how to fix) from **aggregation** (synthesis) could reduce the "degeneration of thought" we occasionally see when a developer sub-agent re-fails the same way across iterations.

**Net assessment:** MAR is ~70% covered by existing patterns. The remaining 30% is a potential refinement of the self-correction loop, not a new top-level pattern.

## 3. Concrete Recommendations

- **Paper 1 (Model-First): INVESTIGATE.** Spike a `problem-model.yml` artifact in the Refine stage on one real feature to measure downstream quality gains before committing to schema changes.
- **Paper 2 (MAR): DEFER.** Existing Debate + Review Board + Adversarial Review cover the persona-diversity claim; only the act/diagnose/critique/aggregate decomposition is novel, and it's a localized refinement of self-correction, not worth a standalone pattern. Revisit if retrospectives show repeated self-correction failures on the same defect class.

## 4. Risks

- **Model-First in Refine** risks bloating an already dense stage and producing modeling theater (entities/constraints that nobody downstream actually consumes). Mitigation: make the artifact *mandatory consumption* by Architect and Quality, not just mandatory production.
- **Model-First cross-stage coupling:** If the model changes in Architect, Refine must re-validate — adds a backtrack loop we don't currently have.
- **MAR token cost:** Adding a diagnose/critique split to self-correction roughly doubles tokens per iteration for marginal gain given existing debate coverage. Deferring avoids this.
- **Both papers** encourage *more structure*, which is Claude's favorite failure mode: structure for its own sake. Any adoption must be gated on measurable defect-rate reduction in retrospectives, not intuition.
