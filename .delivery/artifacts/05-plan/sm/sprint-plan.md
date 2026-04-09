# Sprint Plan — Architecture Board Review Pattern

*Voice: Aragorn son of Arathorn, Scrum Bag. Run: run-2026-04-08-b2c7.*
*"A day may come when sprints overflow — but it is not this day."*

## Capacity Declaration

- **Velocity baseline:** 4 pts/sprint (markdown tier)
- **Ceiling (80% target):** 4 pts
- **Hard cap:** 5 pts (never exceed)
- **Total backlog:** 7 stories, 13 pts
- **Sprints required:** 4
- **DoD iteration ceiling:** 3 rounds per sprint

## Sprint Allocation

| Sprint | Stories | Pts | % of ceiling | Notes |
|--------|---------|-----|--------------|-------|
| **S1** | US-1 (2), US-2 (2) | 4 | 100% | Foundation: schema contract + persona library scaffold. No dependencies. |
| **S2** | US-3 (2), US-4 (2) | 4 | 100% | Judge protocol + Pattern 3b. Depends on S1. |
| **S3** | US-5 (2), US-6 (1) | 3 | 75% | Pipeline integration + MAR iteration-2. Slack for DoD rounds. |
| **S4** | US-7 (2) | 2 | 50% | Dogfood + backwards-compat. Slack for correction rounds. |

**Total:** 13 pts across 4 sprints. No sprint >4 pts. Hard cap (5) never approached.

## Sequencing Rationale

1. **US-1 first** — its field names are the interface contract for US-4, US-5, US-7 (Celebrimbor amendment; merged into stories.md US-1 "Contract role" line).
2. **US-2 parallel with US-1** (same sprint) — library can be drafted against the draft schema; persona ids reconciled at S1 DoD.
3. **US-3 after US-2** — judge lives in the same file; avoid merge collisions.
4. **US-4 after US-3** — Pattern 3b references the library.
5. **US-5 after US-4** — Stage 4 integration references Pattern 3b.
6. **US-6 with US-5** — small amendment spanning Pattern 3b and pipeline-stages.md.
7. **US-7 last** — dogfood requires all upstream shipped.

## Adversarial Self-Check (Challenger pass)

- *"Is any 100% sprint actually 120% in disguise?"* — S1/S2 are each 2+2 markdown-tier. 2 pts = one doc edit of ~50–150 lines. Fits a single focused session.
- *"US-3 really 2 pts or 3?"* — Judge protocol is 6 steps + schema + deadlock link. ADR-002 already provides the text; authoring is mechanical. 2 holds.
- *"US-7 under-priced?"* — Token measurement is deferred to UAT (stories.md US-7 AC-6). Without measurement, US-7 = 3 reviewer dispatches + judge + backwards-compat sanity run. 2 pts holds.
- *"Did we leave amendments in adjacent docs only?"* — No. Celebrimbor's contract amendment is written into stories.md US-1 directly. Memory lesson honored.
- *"Forbidden vocab?"* — grep clean across this plan.

## Risks

- **R1** — S2 depends on S1 DoD closing cleanly; persona id reconciliation could slip. *Mitigation:* S1 DoD explicitly gates on id match between schema and library.
- **R2** — S4 dogfood may trigger correction loop (US-6 cross-persona) and exceed S4 budget. *Mitigation:* S4 is 50% loaded; 2 pts of slack absorb one correction round.

## Amendments Merged (Architect → SM → PO, authoritative propagation)

Per plan.md memory lesson, these Celebrimbor amendments are written into stories.md (authoritative), not just here:

1. US-1 field set IS the interface contract for US-4/US-5/US-7 → stories.md US-1 "Contract role" line.
2. US-2 + US-3 collapse to a single authoritative file → stories.md US-3 "same file" dependency.
3. US-7 token measurement deferred to UAT → stories.md US-7 AC-6.

*"Forth Eorlingas — to Sprint 1."* — A.
