# PO DoD Review — Stage 3 Design (IA)

**Reviewer**: Product Owner (Gandalf) | **Date**: 2026-04-08
**Artifact**: `.delivery/artifacts/03-design/ux/information-architecture.md`
**Traces to**: `.delivery/artifacts/02-refine/po/prd.md` (Paired Constraints Primitive)

> *"A product owner does not pass what is half-forged, nor fail what is whole."*

## Gate Checks

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Every PRD FR (1–8) traced to a flow or IA element | PASS | FR-1 schema → §2 field layout + §3 naming table (all 8 fields); FR-2 Refine template → Flow A; FR-3 Architect template + forbidden_vocabulary → Flow B + §2 ordering rationale; FR-4 volatility Golden Rule → §7 (§0 insertion); FR-5 DDD guardrail → §7 (§P-Guard sidebar); FR-6 Architect-in-Plan → honored via Flow C consumption model (not contradicted, downstream of IA scope); FR-7 DoD rule-checks → Flow D; FR-8 dogfood path → Flow A target `02-refine/po/constraints.yml` |
| 2 | No scope expansion beyond PRD | PASS | IA introduces no new fields, stages, or artifacts. §3 naming concerns explicitly routed to Architect as questions, not unilateral renames. §9 Q4 defers enforcement policy to Architect |
| 3 | Five PRD §2 roles covered | PASS | Orchestrator (Flow C kickoff cite), Architect (Flow B), PO (Flow A), DoD validator (Flow D), Human checkpoint (Flow E) — one flow per named actor |
| 4 | Out-of-scope respected | PASS | No mention of BACKLOG-003 board pattern, BACKLOG-005 paradigm restructure, BACKLOG-006 transformation, MAR pilot, or v2.8 schema bump. The fence holds |
| 5 | Open questions bounded | PASS | §9 has 4 tactical questions (inheritance vs restatement, citation structure, extend vs sibling file, order enforcement). All load-bearing for Architect; none existential; none reopen the primitive |
| 6 | Reference IA matches PRD gaps | PASS | §7 seats Golden Rule as new §0 in `volatility-decomposition.md` (Gap 1 / FR-4) with worked anti-pattern; places §P-Guard guardrail sidebar at head of each DDD Phase 1–4 (Gap 2 / FR-5). Repetition-at-temptation-point is correct pedagogy |

## Notes to Architect (Stage 4)

- §9 Q1 (inherit vs restate `forbidden_vocabulary`) is load-bearing for NFR-3 back-compat — decide explicitly.
- §9 Q3 (extend vs sibling constraints.yml across stages) affects FR-7 validator glob paths — decide before Plan.
- §3 M-rated names (`state_variables`, `actions`) — Architect may rename; PO has no objection provided FR-1 schema doc updates in lockstep and the field count stays ≤8.

## Verdict

Six of six gates pass. The mirror is true to the burden — every FR traced, every role served, the fence unbroken, and the forbidden word placed where the hand will pause before it writes.

STATUS: DONE
ARTIFACT: .delivery/artifacts/03-design/dod/po-review.md
SUMMARY: Six gates pass, young hobbit — every FR traced, no scope crept, the fence holds, and the Golden Rule finds its seat before Phase One is read again.
