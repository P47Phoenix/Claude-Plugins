# PO Synthesis: Model-First Reasoning & Multi-Agent Reflexion

**Role**: Product Owner (delivery-team:product-delivery) | **Date**: 2026-04-08
**Source reviews**:
- `.delivery/artifacts/research/architect-review-model-first-mar.md`
- `.delivery/artifacts/research/quality-review-model-first-mar.md`

## Verdicts

| Paper | Architect | Quality | **PO Decision** | Rationale |
|---|---|---|---|---|
| Model-First Reasoning (arXiv:2512.14474) | INVESTIGATE | ADOPT | **INVESTIGATE (committed spike)** | QA has overwhelming evidence (57% Plan first-try, 3/7 runs reworked on known constraints, gate-patterns memory injection already proved the mechanism in r4x2). Architect's modeling-theater and cross-stage coupling risks are real but mitigable by scoping to a narrow `constraints.yml` (not a full `problem-model.yml`) and gating adoption on measured Plan first-try ≥80% over 5 runs. This is stronger than a plain "investigate" — it's a committed spike with an A/B exit criterion, and if the metric hits, it ships. |
| Multi-Agent Reflexion (arXiv:2512.20845) | DEFER | INVESTIGATE | **INVESTIGATE (narrow pilot only)** | Architect's "70% already covered by Debate + Review Board + Adversarial Review" is correct — MAR is not a new top-level pattern. But QA's cross-run recurrence evidence ("installed-vs-source sync" 3x, "stale derived artifacts" 2x) points at a genuine degeneration-of-thought failure mode at the macro scale, not the single-iteration scale. Pilot the single novel MAR idea (different persona on iteration-2 of self-correction), nothing more. If the pilot fails, close as REJECT per Architect's framing. |

## Disagreement Resolution (PO owns prioritization)

**Model-First**: Quality's ADOPT and Architect's INVESTIGATE are close. Resolved toward INVESTIGATE-with-teeth: start narrow (`constraints.yml` only), dogfood behind a feature flag, measure against memory metrics that already exist, ship or kill at 5 runs. This honors Architect's "measurable defect-rate reduction, not intuition" principle (also a team memory) while capturing Quality's strong quantitative case.

**MAR**: Architect's DEFER and Quality's INVESTIGATE disagree at the verdict level but agree on substance — both note existing patterns already cover most of MAR, and both flag the self-correction loop as the one candidate site. Resolved as INVESTIGATE but sized S (not a full architectural change) and scoped to an iteration-2 persona swap only.

## Backlog Items Created

- **BACKLOG-001** — Model-First `constraints.yml` spike in Refine stage (Priority P1, Size M) → `.delivery/backlog/BACKLOG-001-model-first-constraints-spike.md`
- **BACKLOG-002** — MAR cross-persona self-correction pilot (Priority P3, Size S) → `.delivery/backlog/BACKLOG-002-mar-cross-persona-iteration2.md`

## Recommended Next Action

**Kick off BACKLOG-001 as a delivery-flow SPIKE run this week** — the expected Plan first-try lift (57%→80%) dominates any other queued improvement, and all measurement infrastructure (memory index, run-level self-correction counts) already exists. BACKLOG-002 stays queued behind it; pilot after BACKLOG-001 either ships or closes, to avoid confounding two experimental changes in the same runs.

## Risk Notes Carried Forward
- Architect's "structure for its own sake is Claude's favorite failure mode" — BACKLOG-001 acceptance criteria enforce *mandatory downstream consumption*, not just production
- Token cost concern on MAR — BACKLOG-002 acceptance criteria cap iteration-2 overhead at <25%
- Cross-stage coupling on Model-First — deferred; if spike passes, address in follow-up before schema bump to v2.8
