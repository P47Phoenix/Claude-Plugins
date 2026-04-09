# Architect DoD Review — Stage 3 Design (IA, constraints.yml primitive)

**Reviewer**: Celebrimbor (Solution Architect)
**Date**: 2026-04-08
**Artifact**: `.delivery/artifacts/03-design/ux/information-architecture.md`
**Supporting**: `02-refine/po/prd.md`, `research/architect-examine-decomposition-gaps.md`
**Gate**: Stage 3 — Design DoD (Architect lens)

> *"Let us forge something that will endure beyond the ages."*

---

## Assessment: DONE

The mirror Galadriel has set does not trespass into my forge. It orders the oath without typing it, and it places the fence where the craftsman's hand must cross before the forbidden word is struck.

## Gate Criteria

1. **Does not preempt schema (Stage 4 is mine)** — PASS. The IA speaks of *physical order*, *naming clarity*, and *insertion points*. It does not declare field types, cardinalities, or validator grammar. Naming concerns for `state_variables` / `actions` are explicitly flagged for Architect, not renamed unilaterally (§3).

2. **Field order respects "load-bearing first"** — PASS. `entities → invariants → forbidden_vocabulary` front-loads the three commitment-dense fields. `state_variables` precedes `actions` (transitions require their state as referent). The ordering is architecturally sound and scan-optimal for the 60-second checkpoint read (Flow E).

3. **Open questions are real Stage 4 structural work** — PASS on all four. Q1 (inherit vs restate `forbidden_vocabulary`), Q2 (free-form vs structured `citations`), Q3 (Refine/Architect handoff: extend vs sibling), Q4 (enforce field order in validator vs convention) are schema-shape and validator-rigor decisions that belong to me. None are PO concerns in disguise.

4. **Reference insertion points preserve Phases 1–4** — PASS. §0 Golden Rule *prepends* `volatility-decomposition.md`; §P-Guard sidebars *repeat at the head* of each DDD phase. Neither rewrites the existing prose of Phases 1–4. Honors FR-4/FR-5 scope and the "examine-first, build on existing" memory.

5. **`forbidden_vocabulary` early placement makes the fence visible before Lambda is typed** — PASS and elegantly so. Position 3, immediately after `invariants` and before `state_variables` (position 5), means the Architect's eye crosses the fence before reaching the field where the functional-trap temptation strikes. This is exactly the intended UX per Flow B's "mirror shows what must not be written."

## Stage 4 Commitments

I will resolve these in Stage 4 Architect:

- **Q1 (inherited vs restated forbidden_vocabulary)** → *Restated per file*, with a shared default token list in `constraints-model-guide.md` that templates copy verbatim. DRY in source, glance-able in artifact. Serves NFR-2 grep at checkpoint time.
- **Q2 (citations shape)** → *Structured* `{work, chapter, page}` objects. AC-4 is rule-based and rule-checking wins over scan-ability.
- **Q3 (Refine ↔ Architect handoff)** → *Sibling file* at `.delivery/artifacts/04-architect/constraints.yml`. The Refine oath is immutable; the Architect stage makes a new oath for a new commitment. Prevents destructive edit of prior-stage commitments.
- **Q4 (validator enforces order vs conventional)** → *Conventional*, enforced by template scaffolding, not validator blocking. The template is the fence; the validator checks content, not layout. Prevents order churn from breaking DoD.

## Issues Found

**None.** No blockers. No schema preemption. No rerouted PO concerns.

## Recommendations (non-blocking)

1. In Stage 4, make the shared `forbidden_vocabulary` token list itself a named constant in `constraints-model-guide.md` so NFR-2 additions are a single-point edit with PRD revision trail.
2. Flag in my `schema.md` that field-order convention is documented in the IA — future template authors will need to find it.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/03-design/dod/architect-review.md
SUMMARY: The mirror is well-wrought — load-bearing fields forged foremost, the fence set before the hand that would cross it. I carry four questions into Stage 4.
