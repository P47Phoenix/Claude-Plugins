# Sprint Plan: MTG Commander Adversarial Review Loops

**Stage:** 05-Plan | **Role:** SM (Aragorn) | **Plugin:** mtg-commander
**Pipeline:** run-2026-04-11-e6f3

---

## Capacity

- **Velocity baseline:** 8 pts/sprint (code), 6 pts/sprint (markdown-tier calibrated)
- **80% ceiling:** 6 pts/sprint (markdown-tier work)
- **Hard cap:** 5 pts single story
- **Team size:** 1 developer (all work is SKILL.md + reference markdown edits)

---

## Sprint 1: Foundation (6 pts)

**Goal:** Establish challenger templates and config loading -- the two independent pillars.

| Story | Pts | Assignee | Notes |
|-------|-----|----------|-------|
| US-1: Challenger agents | 3 | Developer | 4 challenger templates in SKILL.md + signal format |
| US-3: Config loading | 3 | Developer | Config protocol + schema docs + references/config-reference.md |

**Rationale:** US-1 and US-3 have no mutual dependency. Parallel-capable. US-2 depends on US-1 so deferred.

**Exit criteria:** SKILL.md contains 4 challenger sections; config-reference.md exists; pipeline works without config file.

---

## Sprint 2: Loop Protocol + Defect Fixes (6 pts)

**Goal:** Wire challengers into loop protocol; close DEFECT-001; add price goal flow.

| Story | Pts | Assignee | Notes |
|-------|-----|----------|-------|
| US-2: Loop protocol | 3 | Developer | Depends on US-1 (challenger templates exist) |
| US-5: DEFECT-001 fix | 1 | Developer | Depends on US-1 (Rules Challenger exists) |
| US-4: Price rules | 2 | Developer | Depends on US-3 (config provides max_card_price) |

**Rationale:** US-2 builds on US-1's templates. US-5 is small, scoped to Rules Challenger. US-4 needs config from US-3.

**Exit criteria:** Full loop flow documented; validate-deck mandated; price escalation format in SKILL.md.

---

## Sprint 3: Guardrails + Polish (3 pts)

**Goal:** Harden guardrails, update reference guides, verify with dogfood grep.

| Story | Pts | Assignee | Notes |
|-------|-----|----------|-------|
| US-6: DEFECT-002 fix | 1 | Developer | CK divergence in Price Challenger |
| US-7: Sub-agent guardrail | 1 | Developer | NON-NEGOTIABLE section + anti-pattern callout |
| US-8: Reference guide updates | 1 | Developer | price-evaluator-guide, rules-judge-guide |
| US-9: Dogfood verification | 0 | QA | Grep test, structural review |

**Rationale:** US-8 aggregates all guide updates after functional stories complete. US-9 is zero-cost verification.

**Exit criteria:** Grep test passes (>=3 matches); reference guides reflect adversarial flow; AC-11 verified.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| US-1 at 3 pts is largest single item | 4 independent templates -- can split if blocked |
| Sprint 2 at ceiling (6 pts) | US-5 is 1pt safety margin; can slip to Sprint 3 |
| Reference guide updates depend on 4 stories | US-8 deliberately last; all inputs stable by Sprint 3 |

---

## Definition of Done (Sprint-level)

- All stories in sprint meet their AC
- SKILL.md compiles (no broken markdown references)
- No new external dependencies introduced (NFR-1)
- Pipeline works without `.mtg-commander.yml` at every sprint boundary (NFR-2)
