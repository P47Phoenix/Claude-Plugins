# Idea Brief — Paired Constraints Primitive (BACKLOG-001 ∥ BACKLOG-004)

**Stage**: 1 (Idea) | **Role**: Product Owner (Gandalf) | **Date**: 2026-04-08
**Project type**: FEATURE (paired) | **Pipeline**: delivery-flow
**Inputs**: BACKLOG-001, BACKLOG-004, architect-examine-decomposition-gaps, po-synthesis-model-first-mar, po-revision-research-integration

> *"A product owner is never late, nor early. They prioritize precisely when they mean to."*

---

## 1. The Burden

The delivery-team plugin limps where it should stride. The evidence — gathered not in rumor but in the stone of our own memory — tells a plain tale:

- **Plan stage first-try pass rate sits at 57%** (`.delivery/memory/stages/plan.md`, 3 of 7 runs reworked on constraints that were *already known* at Refine time). Gate-patterns memory injection has proved the cure in run-r4x2; we have simply not generalized it.
- **The Golden Rule of volatility decomposition is unnamed.** The Architect examination (`architect-examine-decomposition-gaps.md`, Gap 1) confirms `volatility-decomposition.md` never states Löwy's rule — *"decompose by volatility, not by functionality"* — as a rule. Architects slide, unprompted, into functional decomposition wearing volatility's cloak.
- **Implementation-detail contamination bleeds upward.** The same examination (Gap 2) finds Phases 1–4 of both volatility and DDD references contain no prohibition against naming `lambda`, `ecr`, `sqs`, languages, or runtimes during decomposition. What belongs to Plan and Dev has crept into Architect.
- **The Architect is absent from Stage 5 Plan** (Gap 3). `pipeline-stages.md:428-449` invokes PO, QA, Scrum Bag, and DevOps — but not the one who drew the map. The decomposition-to-plan handoff loses fidelity precisely where fidelity matters most.

These are not four burdens. They are one burden wearing four faces: **constraints known but not structured, and therefore not consumed.**

## 2. The Vision

One primitive to bind them. We will forge a shared `constraints.yml` schema, co-developed across two domains in a single paired run so the schema is pressure-tested before it hardens.

- **The Primitive**: a narrow, rule-checkable `constraints.yml` (≤8 fields) — the Model-First (arXiv:2512.14474) instantiation of explicit entities/state/actions/constraints, scoped narrowly to avoid the modeling-theater trap.
- **Domain A — Refine (BACKLOG-001)**: problem constraints authored pre-AC. Numeric ceilings, mandatory artifacts, FR ids, NFR thresholds, ADR invariants. Consumed by Plan and Architect DoD validators via deterministic rule checks.
- **Domain B — Architect (BACKLOG-004)**: decomposition constraints. The Golden Rule as a named invariant; the banned-token lint (`lambda|ecr|sqs|ec2|s3|dynamodb|<language-name>`) as a structured constraint entry, not prose.
- **New architect reference content** (per Architect examination Option A): Golden Rule section with Löwy citation, "No Implementation Nouns at Decomposition" guardrail threaded through Phases 1–4 of both `volatility-decomposition.md` and `strategic-ddd.md`, a functional-decomposition-trap anti-pattern with worked example, and an Architect invocation step wired into Stage 5 Plan producing `.delivery/artifacts/05-plan/architect/sequencing.md`.

## 3. The Fellowship's Reach

**IN scope:**
- `constraints.yml` schema design (≤8 fields), single source of truth used by both stages
- Refine-stage template + DoD validator hook
- Architect-stage decomposition-constraints entries (Golden Rule invariant + banned-token lint)
- New/updated content in `volatility-decomposition.md` and `strategic-ddd.md` for the three Architect-confirmed gaps
- Architect integration into Stage 5 Plan as a named participant producing `sequencing.md`
- Dogfood validation run proving the metrics (P0 UAT gate per memory)
- Installed↔source file sync (commit to source, validators check installed)

**OUT of scope (explicit — so the Fellowship does not wander):**
- BACKLOG-005 paradigm-as-skill restructure (separate FEATURE-XL pipeline run, blocked on BACKLOG-006)
- BACKLOG-003 configurable architecture board pattern (next run; consumes *our* output as its rule set)
- BACKLOG-006 transformation planning (runs after BACKLOG-003)
- MAR cross-persona pilot (absorbed into BACKLOG-003 per `po-revision-research-integration.md`)
- Rewriting existing architect content beyond the three confirmed gaps
- `.delivery/config.yml` schema bump to v2.8 (deferred until schema survives both domains)

## 4. The Stakes

Measurable, every one of them — no intuition, no theater:

1. **Plan stage first-try pass rate ≥80% over the next 5 runs** (baseline 57%, `.delivery/memory/stages/plan.md`).
2. **Zero implementation-detail contamination** in any Architect decomposition artifact from a subsequent pipeline run — zero occurrences of the banned-token set, verified by deterministic rule check.
3. **Golden Rule explicitly cited** in every volatility-based decomposition artifact when volatility is the selected strategy.
4. **Shared schema consumed by both stages without divergence** — one `constraints.yml` shape, two domain instances, same DoD hook pattern.
5. **Mandatory downstream consumption** — Plan and Architect DoD validators perform at least one deterministic rule check against `constraints.yml` (not produce-and-ignore).
6. **Architect named as Stage 5 participant** with at least one validation note on a real dogfood run.

## 5. What I Counsel Against

> *"Many features that are requested deserve to be deprioritized. And some that are deprioritized deserve to ship."*

- **No paradigm-as-skill restructure during this run.** BACKLOG-005 is its own journey and must wait for BACKLOG-006's AS-IS model.
- **No new collaboration patterns.** The architecture board (BACKLOG-003) is the *next* run, not this one. We build the rule set here; the board consumes it there.
- **No rewriting architect content beyond the three confirmed gaps.** Discipline over ambition.
- **No feature flag that makes this opt-in forever.** The schema becomes load-bearing. A spike flag is acceptable only during the 5-run A/B window per BACKLOG-001 AC; after that it is the pipeline's bone and sinew, or it is rejected and reverted.
- **No schema bump to v2.8 during this run.** The primitive earns its version number only after surviving both domains.
- **No routing around the pipeline.** All work routes through delivery-flow. Plans are prompts to the team, not implementation details.

## 6. The Road Ahead

- **Refine (Stage 2)** — PRD defining the `constraints.yml` schema contract, both domain templates, acceptance criteria tied to the five stakes above, and the dogfood run as a P0 UAT gate.
- **Design (Stage 3)** — reference-file layout (which files change, which are new), schema field definitions with types and validation rules, and the two domain templates side-by-side.
- **Architect (Stage 4, light)** — integration points: DoD validator hook shape, Stage 5 Architect invocation wiring, installed↔source sync boundary, and explicit identification of the Architect-in-Plan touchpoint.
- **Plan (Stage 5)** — stories sized for a single sprint with pre-loaded constraints (sprint ceiling, mandatory artifacts — lesson from memory), Architect named as participant.
- **Development (Stage 6)** — schema file, both domain templates, reference content updates, DoD validator hook wiring, Stage 5 pipeline wiring.
- **UAT (Stage 7)** — dogfood pipeline run on a real feature, measuring all five stakes. No DoD submission before the dogfood. This is the P0 gate.

---

> *"All we have to decide is what to build with the time that is given to us. And I decide we build the shared constraints primitive first — narrow, measured, and load-bearing."*

The seed is planted. Stage 2 will grow it into a PRD. Nothing here is the tree; all of it is the intent from which the tree will rise.

— Gandalf, Product Owner, speaking precisely when he means to
