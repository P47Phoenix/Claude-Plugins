# Adversarial Challenge: Sprint Plan for hardware-team Plugin

**Stage:** 05-Plan | **Role:** Challenger (QA Engineer) | **Task:** adversarial-review
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12
**Artifact Under Review:** sprint-plan.md (SM/Aragorn)

---

## Challenge Summary

The sprint plan is structurally strong -- the SM correctly redistributed the PO overloaded sprints (48 pts and 55 pts) into 4 sprints respecting the 80% ceiling, declared capacity explicitly, and sequenced dependencies properly. However, I identify **3 findings** that require correction and **4 advisory observations**.

---

## Challenge Findings

### FINDING 1: Sprint 2 at 100% of ceiling violates the spirit of the 80% rule [BLOCKING]

**What:** Sprint 2 commits 40 of 40 points -- exactly 100% of the 80% ceiling. The plan even states "No buffer -- this is the densest sprint."

**Why this matters:** The 80% ceiling exists precisely to absorb uncertainty. Committing to the ceiling with zero buffer in a GREENFIELD project with no established velocity baseline is the exact failure pattern this gate is designed to catch. The SM own risk register (R-01) acknowledges "Sprint 2 overcommitment" as a medium-likelihood risk, yet the plan commits to the maximum anyway and relies on Sprint 3/4 to absorb spillover.

Memory lesson applied: "Adversarial review at Plan stage catches sprint overloading that SM correction alone misses."

**The problem compounds:** Sprint 2 contains the TWO most complex stories in the entire backlog (US-103 Gate Framework at 8 pts and US-107 Rework Loops at 8 pts). These are both L/XL estimates with high uncertainty. Packing both into a zero-buffer sprint is exactly how the Plan stage achieves a 57% first-try pass rate.

**Required correction:** Reduce Sprint 2 to at most 85% of ceiling (34 pts). Move US-305 (Documentation Integration, 2 pts) and US-306 (Dependency Docs and Verification, 3 pts) to Sprint 3. These are the lowest-risk integration sub-stories with no downstream Sprint 2 dependencies. Sprint 2 drops to 35 pts (88% of ceiling). Alternatively, move US-107 (Rework Loops, 8 pts) to Sprint 3 -- the SM own adjustment protocol says "if Sprint 1 velocity < 30: reduce Sprint 2 commitment to 30 pts (move US-107 to Sprint 3)" -- why not just move it proactively?

**Note on US-306 dependency:** US-503 (SessionStart Hook, Sprint 4) depends on US-306. Moving US-306 to Sprint 3 does not impact US-503 since Sprint 4 follows Sprint 3. However, the SM must verify this does not break any Sprint 2 internal sequencing.

---

### FINDING 2: Sprint 1 at 95% of ceiling is risky for a calibration sprint [WARNING]

**What:** Sprint 1 commits 38 of 40 points (95% of ceiling). The plan calls it a "calibration sprint" (Section 6 velocity tracking) but loads it to near-maximum.

**Why this matters:** If this is genuinely the calibration sprint -- the one that establishes the velocity baseline for all subsequent sprints -- then committing to 95% defeats the purpose. A calibration sprint should leave margin to measure true sustainable velocity, not push to the limit and then learn "our velocity is 38 because we committed 38." That is a self-fulfilling measurement.

**Mitigating factor:** Sprint 1 is almost entirely markdown-heavy work (role SKILL.md files at 3-5 pts each, plugin skeleton at 2 pts). The complexity risk is genuinely low. The 6 role skills (US-201-206) are fully parallel with no file contention. This mitigates but does not eliminate the concern.

**Recommended action:** Acknowledge that Sprint 1 velocity measurement may be inflated due to the markdown-heavy nature of the stories, and that Sprint 2 velocity should not be planned assuming Sprint 1 actual throughput applies equally to Sprint 2 higher-complexity work.

---

### FINDING 3: Point total discrepancy is acknowledged but not resolved [WARNING]

**What:** The sprint plan acknowledges a 4-point discrepancy between the PO stated total (113 pts) and the per-story sum (117 pts) in Section 3, Open Question #3. The plan uses the per-story values as source of truth.

**Why this matters:** An unresolved 4-point discrepancy means either (a) the PO miscounted, or (b) individual story estimates were changed without updating the summary. Either way, the SM should have flagged this for PO resolution before committing the plan, not carried it as an open question. In a 117-point plan, 4 points is one full medium story -- enough to shift a sprint boundary.

**Required correction:** Resolve with PO which total is correct. If the per-story values are authoritative (they should be), the PO must update the summary table. This should not remain an open question at Plan stage exit.

---

## Advisory Observations

### A1: FR-021 coverage is misleading in the coverage matrix

The coverage matrix maps FR-021 to US-104 with note "Deferred to Phase 2 -- noted" and marks Sprint 1 with "Yes" for coverage. But FR-021 is explicitly P2 scope (dynamic pipeline adaptation). US-104 covers only the P1 static config reading (FR-004). Mapping FR-021 as "covered" by a P1 story that does not implement it is technically misleading. The coverage matrix should mark FR-021 as "Deferred (P2)" rather than "Yes."

### A2: Sprint 4 is heavily underloaded -- consider 3-sprint plan

Sprint 4 commits only 5 of 40 points (13% of ceiling) with 35 points of buffer. While stabilization is wise, this extreme undercommitment means the team is planning for 8 weeks of work that realistically could fit in 6 weeks (3 sprints). If the SM own adjustment protocol would move stories forward on high Sprint 1 velocity, the reverse question applies: is Sprint 4 justified as a full 2-week sprint, or should the plan acknowledge this is a "sprint and a half" of real work?

This is advisory -- having buffer for integration testing is legitimate. But a 4-sprint plan with 73% average utilization may invite scrutiny from stakeholders.

### A3: Test strategy depth is not addressed in the sprint plan

The sprint plan covers story allocation, sequencing, and capacity. It does not address HOW the 31 stories will be validated beyond "PO sign-off on each completed story" and the per-sprint DoD checklists. For a GREENFIELD plugin with 22 FRs, 5 validation gates, and a reference test fixture, there should be at least a sentence on:
- When will end-to-end pipeline testing occur? (Sprint 4 mentions it but does not allocate points for it.)
- Who validates that each gate catches its seeded defects? (US-401-405 AC requires this but no test story exists.)
- Is there a regression strategy for cross-sprint changes?

The Sprint 4 DoD includes "End-to-end pipeline run against reference test fixture succeeds" but no story points are allocated for this activity. If it takes non-trivial effort, it should be a story or at least an explicit time allocation.

### A4: Architect sequencing guidance partially overridden without acknowledgment

The Architect Sprint 1 guidance (sequencing.md Section 5.2) lists 12 stories totaling 48 points for Sprint 1, including US-301 (Integration Layer) and US-400 (Test Fixture). The SM moved both to Sprint 2. While the SM explains the rationale ("Does not block Sprint 1 role skills"), the Architect specifically flagged US-301 as a high-risk item that should be tackled early (sequencing.md Section 2.1: "Early implementation validates the pattern at scale"). The SM should explicitly acknowledge this divergence from Architect guidance and accept the risk that cross-plugin integration issues are deferred to Sprint 2.

---

## Capacity Check Summary

| Check | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Verdict |
|-------|----------|----------|----------|----------|---------|
| At or below 80% ceiling (40 pts)? | 38 pts -- YES | 40 pts -- AT CEILING | 34 pts -- YES | 5 pts -- YES | **FAIL (Sprint 2)** |
| Buffer retained? | 2 pts (5%) | 0 pts (0%) | 6 pts (15%) | 35 pts (88%) | **FAIL (Sprint 2)** |
| Point sum verified? | 38 -- CORRECT | 40 -- CORRECT | 34 -- CORRECT | 5 -- CORRECT | PASS |

## Coverage Matrix Verification

All 22 PRD FRs (FR-001 through FR-022) are mapped to at least one story in the coverage matrix. No orphan FRs. FR-021 mapping is technically misleading (see A1) but not a gap -- the story exists, the FR is just deferred to P2.

**Coverage verdict: PASS** (with advisory on FR-021 marking)

## Estimate Calibration Check

| Story | Type | Points | Markdown-Heavy? | Calibration Applied? | Verdict |
|-------|------|--------|-----------------|---------------------|---------|
| US-102 | Orchestrator SKILL.md | 8 | Yes (SKILL.md + references) | PO says yes | Acceptable -- complexity is in design, not code |
| US-103 | Gate framework markdown | 8 | Yes | PO says yes | Acceptable -- hardware DoD adaptation is genuinely complex |
| US-107 | Rework loop markdown | 8 | Yes | PO says yes | **Questionable** -- rework semantics are complex but the output is markdown. 8 pts for a markdown file is tier L, not M. |
| US-201-206 | Role SKILL.md files | 3-5 each | Yes | PO says yes | Acceptable -- parallel, isolated files |

**Estimate verdict: PASS with advisory** -- US-107 at 8 pts may be over-estimated for markdown work, but given the non-linear semantics risk (SM R-03), the conservative estimate is defensible.

## Dependency Sequencing Check

| Check | Status |
|-------|--------|
| US-101 before everything else? | PASS |
| US-102 before US-103, US-104, US-105, US-106, US-107? | PASS |
| US-103 before US-107 and US-401-405? | PASS |
| US-301 before US-302-306? | PASS |
| US-104 after US-102 (per Architect guidance)? | PASS -- Phase 1c after Phase 1b |
| US-400 available before gates (US-401-405)? | PASS -- Sprint 2 before Sprint 3 |
| US-306 before US-503? | PASS -- Sprint 2 before Sprint 4 |
| US-402 before US-504; US-403 before US-505? | PASS -- Phase 3a before Phase 3b |

**Dependency verdict: PASS** -- all dependencies correctly sequenced.

---

## Confidence Rating

**Confidence: 3 / 5**

Rationale: The sprint plan is well-structured with explicit capacity declarations, correct dependency sequencing, complete FR coverage, and a thorough risk register. However, Sprint 2 at 100% of ceiling with the two most complex stories and zero buffer is a significant risk that the SM has identified but not mitigated. Sprint 1 at 95% on a calibration sprint is a secondary concern. The point discrepancy is minor but should be resolved. With the Sprint 2 correction applied, confidence would rise to 4/5.

---

## Required Corrections Before Plan Stage Exit

1. **[BLOCKING] Reduce Sprint 2 below 100% of ceiling.** Move 5-8 points to Sprint 3 or Sprint 4. Recommended: move US-305 (2 pts) + US-306 (3 pts) to Sprint 3, reducing Sprint 2 to 35 pts and Sprint 3 to 39 pts (both within ceiling with buffer).
2. **[WARNING] Resolve the 4-point discrepancy** with PO before plan exit.
3. **[WARNING] Acknowledge Sprint 1 velocity calibration limitation** -- markdown velocity does not predict code-complexity velocity.
