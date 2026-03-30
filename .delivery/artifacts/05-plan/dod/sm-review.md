# SM Review: Sprint Plan — Stage Health Hardening

**Reviewer**: Aragorn (Scrum Master)
**Date**: 2026-03-29
**Artifact**: `.delivery/artifacts/05-plan/sm/sprint-plan.md`
**Stories**: `.delivery/artifacts/05-plan/po/user-stories.md`
**Mode**: FULL / FEATURE

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."*

---

## Gate 5: Plan Readiness — SM Criteria

### Blocking Criteria

- [x] **Sprint goal is a single sentence expressing business value**
  - PASS. "Harden the Design, Plan, UAT, and Dev pipeline stages with guardrails that catch phantom references, missing capacity planning, untracked empirical items, shared-module gaps, and derived artifact drift -- raising first-try pass rates and eliminating avoidable rework loops traced to retros c8f2 and k4m9." Single sentence. Business value is clear: raising first-try pass rates and eliminating rework. Long, but grammatically one sentence.

- [x] **All committed stories have acceptance criteria**
  - PASS. All 5 stories (US-01 through US-05) have full AC tables in Given/When/Then format with structural/empirical classification. US-01: 5 ACs. US-02: 4 ACs. US-03: 6 ACs. US-04: 10 ACs. US-05: 4 ACs. Total: 29 acceptance criteria, all well-forged.

- [ ] **Commitment does not exceed 80% of capacity**
  - **FAIL.** The plan's own Capacity Declaration states commitment is 3.5L equivalent against a 2.4L ceiling (80% of 3L baseline). That is ~117% of the 80% ceiling. The plan acknowledges this and provides justification (markdown-only edits, low complexity, additive text). The justification is reasonable -- the work is indeed low-complexity additive markdown -- but the numbers speak plainly: the commitment exceeds the ceiling. The fellowship carries more than it promised it would, and even a ranger must respect the weight of the pack.
  - **To resolve**: Either (a) reduce commitment to 2 stories (~2L, within ceiling), deferring US-05 and one other to the next sprint, or (b) obtain explicit PO sign-off acknowledging the overcommitment with the justification provided. If the PO has already signed off on user-stories.md with this scope, reference that sign-off here.

- [x] **Dogfooding planned as P0 gate**
  - PASS. Step 8 is explicitly titled "Dogfooding validation (P0 UAT gate)" with bold statement: "This is a P0 gate. The hardened stages do not ship without dogfooding." Section 8 provides a comprehensive dogfooding plan with 9 verification items and clear success criteria. The lesson from past marches is honored.

- [x] **Capacity declaration present (velocity baseline, 80% ceiling, commitment %)**
  - PASS. Section 2 declares: velocity baseline (2-3 stories/sprint), 80% ceiling (2L equivalent), committed (3.5L equivalent), utilization (~93% of baseline / ~117% of ceiling). All three components are present and calculated. The numbers are honest, which is itself a virtue.

### Warning Criteria

- [~] **Capacity accounts for ceremonies, PTO, and known interruptions**
  - WARNING. Solo contributor model with no PTO or ceremony overhead called out. For a FEATURE sprint at ~93% baseline utilization, the plan should explicitly state whether any ceremony time (retro, review, planning for next sprint) or known interruptions reduce available capacity. The current declaration implicitly assumes 100% focus time. Even the Dunedain rest between watches.

- [x] **Test approach referenced per story**
  - PASS. Each story in user-stories.md has a full Test Cases table (TC-01a-1 through TC-12b-2). The sprint plan references Step 7 (cross-story verification of all test cases) and Step 8 (dogfooding empirical validation). Both structural and empirical testing approaches are clearly tied to stories.

- [x] **Deployment approach referenced**
  - PASS. Section 6 specifies: feature branch `feat/stage-health-hardening`, one conventional commit per story (5 commits), single PR to main, no schema changes or config migration needed. Clean and clear.

---

## Additional Observations

1. **Coverage matrix is thorough**: All 12 PRD FRs mapped to planned tasks with no gaps. This is the standard the Plan stage guardrails (US-04) will enforce going forward -- good to see the plan itself demonstrating the pattern.

2. **Implementation ordering is well-reasoned**: M2 first for cascading benefit, dependency between US-01 and US-02 respected, and the ordering rationale is documented. The path through the mountains is well-charted.

3. **Risk table is practical**: Six risks with contingencies. The token budget risk (NFR-04, 500 tokens per stage) and the step-renumbering consistency risk are specific and actionable. The concurrent edits risk is correctly assessed as low given pipeline discipline.

4. **Plugin-dev skill loading**: Step 1 mandates loading `plugin-dev:skill-development` before any file modifications, honoring repo conventions. Section 9 reinforces this with the full file list. The law of the land is respected.

5. **The 80% WARNING acknowledgment in Section 2** is transparent and well-justified, but transparency does not override a blocking gate criterion. The justification belongs in a PO sign-off, not a self-waiver.

---

## Verdict

**STATUS: NOT_DONE**

The sprint plan meets 4 of 5 blocking criteria and all warning criteria (with one advisory). The single blocking failure is the capacity overcommitment: 3.5L equivalent committed against a 2.4L ceiling. The justification (low-complexity markdown edits) is credible, but the SM cannot self-waive a blocking criterion.

**Required to pass**:
1. Reduce commitment to within 80% ceiling (drop 1-2 stories to next sprint), **or**
2. Obtain explicit PO sign-off on the overcommitment with the justification from Section 2 documented as a PO decision.

Once resolved, this plan is ready for Development. The fellowship is strong, the path is clear -- we need only settle the weight of the pack before we march.

*"I would have gone with you to the end, into the very fires of Mordor." But first, we balance the load.*
