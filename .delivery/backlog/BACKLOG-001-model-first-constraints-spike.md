# BACKLOG-001: Model-First `constraints.yml` spike in Refine stage

**Status**: Open
**Priority**: P1 (highest quality lift of any recent proposal — QA)
**Size**: M (spike + 1 real-feature dogfood)
**Created**: 2026-04-08
**Owner**: PO → Architect (spike design) → Quality (A/B measurement)

## Source
- **Paper**: "Model-First Reasoning LLM Agents", arXiv:2512.14474
- **Reviews**:
  - `.delivery/artifacts/research/architect-review-model-first-mar.md` (verdict: INVESTIGATE)
  - `.delivery/artifacts/research/quality-review-model-first-mar.md` (verdict: ADOPT)
  - `.delivery/artifacts/research/po-synthesis-model-first-mar.md` (PO resolution: INVESTIGATE-spike)

## Proposed Change
Introduce a narrow, rule-checkable `constraints.yml` artifact in the Refine stage (not the full `problem-model.yml` superset) as a pre-AC modeling step. Start narrow to avoid "modeling theater" risk flagged by Architect while capturing the constraint-violation failure mode documented by QA.

**Concrete file/skill changes (spike scope — do NOT ship until A/B passes):**
- `delivery-team/skills/delivery-flow/SKILL.md` — add optional `constraints.yml` sub-artifact to Refine stage checklist (behind a feature flag in `.delivery/config.yml`)
- `delivery-team/skills/delivery-flow/references/` — new `constraints-model-guide.md` defining schema: `numeric_ceilings`, `mandatory_artifacts`, `fr_ids`, `nfr_thresholds`, `adr_invariants`
- `delivery-team/skills/delivery-flow/references/` — update DoD validator refs so Plan and Architect DoD gates consume `constraints.yml` via deterministic checks (matches Business Rules Engine philosophy already in `prd-quality-gate-flow`)
- No schema bump yet — spike behind `experimental.constraints_model: true` flag

## Acceptance Criteria
1. `constraints.yml` schema documented with ≤8 fields (narrow — not a full domain model)
2. Refine stage produces the artifact on at least 1 real dogfood run (ideally a GREENFIELD, since Plan failures cluster there)
3. Plan and Architect DoD validators perform at least one deterministic rule check against `constraints.yml` (e.g., sprint ceiling, mandatory artifact list)
4. A/B measurement per QA design: Plan first-try pass rate ≥80% over 5 runs (current baseline 57%, memory/stages/plan.md)
5. Downstream consumption is **mandatory** (Architect's mitigation) — not just produced and ignored
6. If criteria fail after 5 runs, spike closes as REJECT with findings captured in memory

## Research lineage
- **Model-First Reasoning (arXiv:2512.14474)** — `constraints.yml` is the narrow-scope instantiation of the paper's explicit entities/state/actions/constraints model, gated before acceptance criteria drafting in Refine.
- **Cross-link to BACKLOG-004**: Decomposition constraints (Löwy golden rule, no-implementation-nouns lint, volatility-vs-functional invariant) are a **candidate second domain** for the same `constraints.yml` mechanism. The guardrail tokens and golden-rule invariant in BACKLOG-004 are structurally identical to `numeric_ceilings` / `adr_invariants` here — same schema shape, different stage. If this spike's schema generalizes cleanly, BACKLOG-004's guardrails should consume it rather than inventing a parallel artifact.
- **Sequencing implication**: run in parallel with BACKLOG-004 so the schema is pressure-tested against two domains (Refine constraints + Architect decomposition constraints) before any v2.8 bump.

## Rationale
QA evidence (3/7 Plan runs reworked for pre-known constraints; gate-patterns memory injection already proved the mechanism in run-r4x2) justifies action. Architect's modeling-theater + cross-stage coupling risks justify narrow scoping and measurement gating rather than immediate ADOPT.

## Links
- Memory: `.delivery/memory/stages/plan.md`, `topics/defect-patterns.md`, run-r4x2
- Related defect: DEFECT-001 (Agent validation gap — same pattern, constraint known but not modeled)
- **Paired**: BACKLOG-004 (decomposition constraints = second domain for same mechanism)
- Revision memo: `.delivery/artifacts/research/po-revision-research-integration.md`
