# Sprint Plan — BACKLOG-006 transformation-planning
**Role:** Aragorn (Scrum Bag)
**Stage:** 05-plan
**Capacity:** sprint ceiling 4 pts; hard cap 5 pts; markdown tier
**Pipeline:** run-2026-04-09-c4d1

## Constraints
- Dependency order: US-1 → US-2 → {US-3, US-4, US-5} → US-6 → US-7 → US-8
- US-7 before US-8 (Phase 1A output is US-8 input)
- Capacity 4/sprint; hard cap 5 only with written justification

## Allocation (21 pts → 6 sprints)

### Sprint P1 — Foundation  (3 pts)
- US-1 Register task_type  (1)
- US-2 Master protocol doc  (2)
Goal: dispatchable task_type + protocol contract landed. Headroom: 1 pt.

### Sprint P2 — Phase 1A Doc  (3 pts)
- US-3 Phase 1A reference doc  (3)
Goal: behavioral protocol landed; unblocks template work. Headroom: 1 pt.

### Sprint P3 — Phase 1B Doc  (3 pts)
- US-4 Phase 1B reference doc  (3)
Goal: structural protocol landed. Headroom: 1 pt.
(Note: US-4+US-5 at 6 pts together violates hard cap — split.)

### Sprint P4 — Phase 2/3 Docs + Templates  (5 pts, HARD CAP)
- US-5 Phase 2 + 3 reference docs  (3)
- US-6 Template files  (2)
**Justification for hard cap:** US-6 is file-only scaffolding with near-zero unknowns; US-5 authors a pre-frozen schema (ADR-002 already fixes the big-bang rule). Splitting into 3+2 across two sprints delays dogfood by a full sprint for no quality gain. Logged per hard-cap discipline.
Goal: all reference docs + templates landed; dogfood unblocked.

### Sprint P5 — Dogfood Phase 1A  (3 pts)
- US-7 Dogfood Phase 1A vs Claude-Plugins  (3)
Goal: ≥5 use cases with evidence citations, ≥1 low-confidence, MAR review recorded. Headroom: 1 pt.

### Sprint P6 — Dogfood Phases 1B+2+3  (4 pts)
- US-8 Structural + TO-BE + roadmap dogfood  (4)
Goal: all four linked artifacts committed; validator exits 0; forbidden-vocab oracle clean on TO-BE. Headroom: 0 pt — at ceiling.

## Adversarial Self-Check
- **P4 hard-cap defensible?** Yes — US-6 zero unknowns; US-5 schema pre-frozen in ADR-002. Alternative (split) extends critical path one sprint for no quality gain. Logged.
- **Can US-3/US-4/US-5 parallelize?** Technically yes, but sequential gives cleaner review cadence and schema-drift protection; no velocity gain at markdown tier.
- **US-8 at 4 pts realistic?** Tight — roadmap authoring on a large codebase is the risk. Mitigation: clean US-7 low-confidence handling so P6 doesn't inherit ambiguity.
- **Critical path = 6 sprints. Shrinkable?** Only by violating deps or bundling US-7+US-8 (6 pts, above cap). Rejected.
- **Memory lesson run a1f3 (propagate amendments):** amendments merged in stories.md §Amendments; sprint plan reflects corrected dogfood path and US-2-as-hard-prereq.
