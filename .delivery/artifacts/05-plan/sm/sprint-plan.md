# Sprint Plan: hardware-team Plugin (Revised)

**Stage:** 05-Plan | **Role:** Scrum Master (Aragorn) | **Task:** sprint-planning
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12
**Stories Version:** PRD 1.1 | **Architecture Version:** 1.4 | **Sequencing Version:** Architect 1.0
**Revision:** 2.0 -- Rebalanced per adversarial challenger findings (challenge.md)

---

> "I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall. The challenger spoke true -- we marched too heavy in Sprint 2, and the calibration sprint left no room to learn. A wise captain adjusts the formation before the battle, not during it."

---

## 1. Capacity Declaration (MANDATORY)

### 1.1 Velocity Baseline

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Team size** | 1 developer (solo contributor) | GREENFIELD project, single implementer |
| **Sprint duration** | 2 weeks (10 working days) | Standard sprint cadence |
| **Estimated raw velocity** | 50 story points/sprint | Calibrated for markdown-heavy work. This plugin is ~85% markdown files (SKILL.md, references/*.md) and ~15% Python scripts. PO's calibrated estimates already apply the "one tier lower" markdown adjustment. Solo contributor on focused plugin work with no context switching. |
| **80% ceiling** | 40 story points/sprint | 50 x 0.80 = 40 pts. Never exceeded. |
| **Ceremony overhead** | Included in 80% buffer | Planning, review, retro, refinement absorbed into the 20% margin |

### 1.2 Per-Sprint Commitment Percentage

| Sprint | Committed Points | % of 80% Ceiling (40 pts) | Buffer | Rationale |
|--------|-----------------|---------------------------|--------|-----------|
| Sprint 1 | 32 | 80% of ceiling | 8 pts | **Calibration sprint.** No velocity baseline exists. Committing to exactly 80% of the ceiling leaves meaningful room to measure true sustainable velocity without self-fulfilling the estimate. Markdown-heavy stories (low complexity) mitigate undercommitment risk. |
| Sprint 2 | 33 | 83% of ceiling | 7 pts | Post-calibration. Contains the two highest-complexity P1 stories (US-103 at 8 pts, integration subs). 7-point buffer absorbs uncertainty from L-sized stories. |
| Sprint 3 | 35 | 88% of ceiling | 5 pts | By Sprint 3 we have two sprints of velocity data. Contains US-107 (8 pts, most complex story) but dependencies are resolved. 5-point buffer for Sprint 2 spillover. |
| Sprint 4 | 17 | 43% of ceiling | 23 pts | Stabilization sprint. Final P1 story (US-503) plus P2 stories deferred from Sprint 3. Heavy buffer for end-to-end integration testing, Sprint 2/3 spillover, and bug fixes. |

### 1.3 Adversarial Corrections Applied (v2.0)

The v1.0 plan had Sprint 2 at 100% of ceiling (BLOCKING) and Sprint 1 at 95% (WARNING). The challenger correctly identified these as capacity violations:

| Issue | v1.0 | v2.0 | Correction |
|-------|------|------|------------|
| Sprint 1 overloaded (calibration sprint) | 38 pts (95%) | 32 pts (80%) | Moved US-204 (Manufacturing Engineer, 3 pts) and US-206 (Test Engineer, 3 pts) to Sprint 2. These are independent role skills with no Sprint 1 downstream dependencies. |
| Sprint 2 at ceiling (zero buffer) | 40 pts (100%) | 33 pts (83%) | Moved US-107 (Rework Loops, 8 pts) to Sprint 3 and US-305 (Documentation Integration, 2 pts) + US-306 (Dependency Docs, 3 pts) to Sprint 3. Added US-204 (3 pts) + US-206 (3 pts) from Sprint 1. Net: -8 -2 -3 +3 +3 = -7 pts. |
| Sprint 3 rebalance | 34 pts (85%) | 35 pts (88%) | Absorbed US-107 (8 pts), US-305 (2 pts), US-306 (3 pts) from Sprint 2. Moved US-105 (5 pts), US-106 (3 pts), US-504 (2 pts), US-505 (2 pts) to Sprint 4 to stay within ceiling. |
| Sprint 4 underloaded | 5 pts (13%) | 17 pts (43%) | Absorbed US-105, US-106, US-504, US-505 from Sprint 3. Better utilization while retaining stabilization buffer. |

**Point discrepancy resolved (Finding 3):** The PO's summary table stated 113 pts. The per-story authoritative values sum to 117 pts (P1 + P2). This plan uses 117 pts as the source of truth. The discrepancy arose from the PO's summary table not reflecting individual story estimates. PO must update the summary table to match per-story values.

**Sprint 1 calibration acknowledgment (Finding 2):** Sprint 1 velocity will reflect markdown-heavy throughput. Sprint 2 contains higher-complexity work (gate framework, integration layer). Sprint 2 commitment must NOT assume Sprint 1 markdown velocity applies to Sprint 2 complexity. The adjustment protocol (Section 6) accounts for this.

The fellowship adjusts its march. We do not carry more than we can bear, especially when the road ahead is unmapped.

---

## 2. Sprint Breakdown

### Sprint 1: Skeleton, Orchestrator, Config, and Core Role Skills

**Sprint Goal:** Establish the plugin skeleton, pipeline orchestrator, config system, and 4 core role skills (Product Owner, Electrical Engineer, PCB Layout Engineer, Compliance Engineer) so the plugin is structurally complete and foundational roles can be invoked independently.

**Sprint Dates:** Sprint 1 (Weeks 1-2)
**Team Capacity:** 40 story points (80% ceiling)
**Committed:** 32 story points (80% of ceiling)

#### Committed Stories

| # | Story | Points | Priority | Dependencies | Internal Sequence |
|---|-------|--------|----------|--------------|-------------------|
| 1 | US-101: Plugin Skeleton | 2 | P1 | None | Phase 1a (Day 1) |
| 2 | US-108: Marketplace Registration | 1 | P1 | US-101 | Phase 1b (after US-101) |
| 3 | US-102: Pipeline Orchestrator | 8 | P1 | US-101 | Phase 1b (after US-101) |
| 4 | US-104: Config-Driven Pipeline | 5 | P1 | US-102 | Phase 1c (after US-102, per Architect guidance) |
| 5 | US-201: HW Product Owner | 3 | P1 | US-101 | Phase 1b (parallel) |
| 6 | US-202: Electrical Engineer | 5 | P1 | US-101 | Phase 1b (parallel) |
| 7 | US-203: PCB Layout Engineer | 5 | P1 | US-101 | Phase 1b (parallel) |
| 8 | US-205: Compliance Engineer | 3 | P1 | US-101 | Phase 1b (parallel) |
| | **Sprint Total** | **32** | | | |

**Commitment:** 32 of 40 pts (80% of ceiling). 8-point buffer retained for calibration measurement.

#### What Was Deferred from Sprint 1

| Story | Points | Reason for Deferral | Moved To |
|-------|--------|---------------------|----------|
| US-204: Manufacturing Engineer | 3 | Calibration sprint reduction. Independent role skill, no Sprint 1 downstream dependencies. | Sprint 2 |
| US-206: Test Engineer | 3 | Calibration sprint reduction. Independent role skill, no Sprint 1 downstream dependencies. | Sprint 2 |

#### Commitment Rationale

The sprint goal focuses on structural completeness of the core: after Sprint 1, the plugin exists, the orchestrator defines all 8 stages, config is in place, and 4 of 6 role skills have their SKILL.md and references. US-204 (Manufacturing Engineer) and US-206 (Test Engineer) are deferred to Sprint 2 because they are fully independent role skills with no downstream dependencies within Sprint 1. Deferring them gives the calibration sprint room to measure true sustainable velocity rather than pushing to 95% and creating a self-fulfilling measurement.

The fellowship walks before it runs -- and it measures its pace on the first day, not the last.

#### Internal Sequencing

```
Phase 1a (Day 1):
  US-101 (Plugin Skeleton, 2 pts)

Phase 1b (Days 2-7, parallel after US-101):
  Track A: US-108 (Marketplace, 1 pt) -- trivial, complete immediately
  Track B: US-102 (Orchestrator, 8 pts) -- core pipeline
  Track C: US-201, US-202, US-203, US-205 (Role Skills, 16 pts) -- all parallel

Phase 1c (Days 7-10, after US-102):
  US-104 (Config, 5 pts) -- sequential after US-102
```

#### Definition of Done -- Sprint 1

- [ ] Plugin directory structure matches architecture Section 1.1
- [ ] SKILL.md loads without error in Claude Code harness (US-101)
- [ ] marketplace.json contains hardware-team entry (US-108)
- [ ] Pipeline orchestrator defines all 8 stages with dispatch patterns (US-102)
- [ ] Config schema documented with validation script functional (US-104)
- [ ] 4 role SKILL.md files load in isolation with correct reference loading (US-201, US-202, US-203, US-205)
- [ ] Zero cross-role context bleed verified for each role skill
- [ ] All acceptance criteria for committed stories pass
- [ ] PO sign-off on each completed story

---

### Sprint 2: Integration Layer, Test Fixture, Gate Framework, and Remaining Roles

**Sprint Goal:** Establish the integration layer with kicad-happy, create the reference test fixture, build the gate validation framework, and complete the remaining 2 role skills so that all foundations are in place for gate implementation in Sprint 3.

**Sprint Dates:** Sprint 2 (Weeks 3-4)
**Team Capacity:** 40 story points (80% ceiling)
**Committed:** 33 story points (83% of ceiling)

#### Committed Stories

| # | Story | Points | Priority | Dependencies | Internal Sequence |
|---|-------|--------|----------|--------------|-------------------|
| 1 | US-204: Manufacturing Engineer | 3 | P1 | US-101 | Phase 2a (Days 1-2, parallel) |
| 2 | US-206: Test Engineer | 3 | P1 | US-101 | Phase 2a (Days 1-2, parallel) |
| 3 | US-301: Integration Layer Architecture | 5 | P1 | US-101 | Phase 2a (Days 1-3) |
| 4 | US-400: Reference Test Fixture | 5 | P1 | US-101 | Phase 2a (Days 1-4, parallel) |
| 5 | US-103: Stage Gate Validation Framework | 8 | P1 | US-102 | Phase 2a (Days 1-5) |
| 6 | US-302: Sourcing Integration | 3 | P1 | US-301 | Phase 2b (after US-301) |
| 7 | US-303: Fabrication Integration | 3 | P1 | US-301 | Phase 2b (after US-301) |
| 8 | US-304: Analysis Integration | 3 | P1 | US-301 | Phase 2b (after US-301) |
| | **Sprint Total** | **33** | | | |

**Commitment:** 33 of 40 pts (83% of ceiling). 7-point buffer for the highest-complexity story (US-103 Gate Framework, 8 pts).

#### What Was Deferred from Original Sprint 2

| Story | Points | Reason for Deferral | Moved To |
|-------|--------|---------------------|----------|
| US-107: Rework Loop Support | 8 | Most complex story in the backlog. Removing it from the densest sprint and placing it after US-103 is complete. Critical path preserved (US-103 Sprint 2 -> US-107 Sprint 3). | Sprint 3 |
| US-305: Documentation Integration | 2 | Low-risk integration sub-story. No Sprint 2 internal consumers. | Sprint 3 |
| US-306: Dependency Docs & Verification | 3 | Low-risk. US-503 (SessionStart Hook) depends on US-306 but is in Sprint 4 -- no impact from deferral. | Sprint 3 |

#### Commitment Rationale

This sprint builds the three pillars that gates need: the integration layer (US-301 + US-302-304), the gate framework (US-103), and the test fixture (US-400). US-204 and US-206 (deferred from Sprint 1's calibration reduction) slot in cleanly at 3 pts each with zero contention -- they are isolated role SKILL.md files.

US-107 (Rework Loops, 8 pts) has been moved to Sprint 3. In v1.0, it shared Sprint 2 with US-103 (Gate Framework, 8 pts) -- the two most complex stories packed into a zero-buffer sprint. The challenger was right: that was the exact failure pattern the 80% rule prevents. US-107 depends on US-103, so sequencing it one sprint later is natural. The critical path (US-101 -> US-102 -> US-103 -> US-107) now spans Sprints 1-3 instead of being compressed into Sprints 1-2.

US-305 and US-306 are moved to Sprint 3 because no Sprint 2 story depends on them. US-306's downstream consumer (US-503) is in Sprint 4.

The road through Moria is still perilous -- but now we carry fewer packs through the mines, and the Balrog of US-107 waits for us on steadier ground.

#### Internal Sequencing

```
Phase 2a (Days 1-5, parallel tracks):
  Track A: US-103 (Gate Framework, 8 pts) -- critical path, start immediately
  Track B: US-301 (Integration Layer, 5 pts) -- foundation for integration subs
  Track C: US-400 (Test Fixture, 5 pts) -- no code dependencies, parallel
  Track D: US-204, US-206 (Role Skills, 6 pts) -- isolated, parallel, complete early

Phase 2b (Days 5-10, after Phase 2a):
  Track E: US-302-304 (Integration Subs, 9 pts) -- after US-301, all parallel
```

#### Definition of Done -- Sprint 2

- [ ] Gate framework defines all 5 gate types with validator patterns (US-103)
- [ ] Integration layer maps all 11 kicad-happy skills to consuming roles (US-301)
- [ ] Integration sub-stories document dispatch patterns for sourcing, fab, analysis (US-302-304)
- [ ] Reference test fixture contains seeded defects in all required categories (US-400)
- [ ] Manufacturing Engineer and Test Engineer SKILL.md files load in isolation (US-204, US-206)
- [ ] Zero cross-role context bleed verified for US-204 and US-206
- [ ] All acceptance criteria for committed stories pass
- [ ] PO sign-off on each completed story

---

### Sprint 3: Rework Loops, Validation Gates, Design Review Board, and Integration Docs

**Sprint Goal:** Rework loop support operational. All 5 validation gates implemented and tested against the reference fixture. Design Review Board and remaining integration documentation complete.

**Sprint Dates:** Sprint 3 (Weeks 5-6)
**Team Capacity:** 40 story points (80% ceiling)
**Committed:** 35 story points (88% of ceiling)

#### Committed Stories

| # | Story | Points | Priority | Dependencies | Internal Sequence |
|---|-------|--------|----------|--------------|-------------------|
| 1 | US-107: Rework Loop Support | 8 | P1 | US-102, US-103 | Phase 3a (Days 1-5) |
| 2 | US-305: Documentation Integration | 2 | P1 | US-301 | Phase 3a (Days 1-2, parallel) |
| 3 | US-306: Dependency Docs & Verification | 3 | P1 | US-301 | Phase 3a (Days 1-3, parallel) |
| 4 | US-401: Schematic Review Gate | 5 | P1 | US-103, US-202, US-400 | Phase 3a (parallel) |
| 5 | US-402: DRC Gate | 3 | P1 | US-103, US-203, US-400 | Phase 3a (parallel) |
| 6 | US-403: BOM Gate | 3 | P1 | US-103, US-302, US-400 | Phase 3a (parallel) |
| 7 | US-404: DFM Gate | 3 | P1 | US-103, US-204, US-303, US-400 | Phase 3a (parallel) |
| 8 | US-405: Compliance Gate | 3 | P1 | US-103, US-205, US-304, US-400 | Phase 3a (parallel) |
| 9 | US-501: Design Review Board | 3 | P1 | US-102, US-202, US-203, US-204 | Phase 3a (parallel) |
| 10 | US-502: BOM Reconciliation | 2 | P2 | US-302, US-403 | Phase 3b (after US-403) |
| | **Sprint Total** | **35** | | | |

**Commitment:** 35 of 40 pts (88% of ceiling). 5-point buffer for Sprint 2 spillover absorption.

#### What Was Deferred from Original Sprint 3

| Story | Points | Reason for Deferral | Moved To |
|-------|--------|---------------------|----------|
| US-105: Pipeline State Persistence | 5 | P2 story. Moved to Sprint 4 to make room for US-107 (P1, critical path). | Sprint 4 |
| US-106: Self-Learning Memory | 3 | P2 story. Moved to Sprint 4 for the same reason. | Sprint 4 |
| US-504: Schematic DRC Hook | 2 | P2 hook. Depends on US-402 (this sprint). Can be implemented in Sprint 4 after gates are stable. | Sprint 4 |
| US-505: BOM Drift Detection Hook | 2 | P2 hook. Depends on US-403 (this sprint). Can be implemented in Sprint 4 after gates are stable. | Sprint 4 |

#### Commitment Rationale

This is the gate sprint. All 5 individual gates (US-401-405) are built and tested against the infrastructure completed in Sprint 2 (gate framework, integration layer, test fixture). All 5 are fully parallel -- each gate is a separate section with no cross-gate dependencies.

US-107 (Rework Loops, 8 pts) joins this sprint after being deferred from Sprint 2's overloaded plan. Its dependencies (US-102 Sprint 1, US-103 Sprint 2) are fully resolved. It is the most complex story in the backlog but now has the breathing room it needs -- it does not share a sprint with another 8-point story.

US-305 and US-306 (deferred from Sprint 2) complete the integration layer documentation. US-306 must finish here because US-503 (Sprint 4) depends on it.

US-502 (BOM Reconciliation) depends on US-403 (BOM Gate, this sprint) so it is sequenced into Phase 3b.

P2 stories (US-105, US-106, US-504, US-505) are moved to Sprint 4 to keep this sprint focused on completing ALL remaining P1 work. After Sprint 3, every P1 story except US-503 is done.

The 5-point buffer is intentional. If Sprint 2 slips (US-103 is 8 pts of complex gate framework work), this sprint absorbs it. That is not weakness -- it is wisdom. A good plan accounts for the Balrog.

#### Internal Sequencing

```
Phase 3a (Days 1-7, parallel tracks):
  Track A: US-107 (Rework Loops, 8 pts) -- critical path, start immediately
  Track B: US-305 (Doc Integration, 2 pts) + US-306 (Dep Docs, 3 pts) -- parallel
  Track C: US-401-405 (Gates, 17 pts) -- all 5 parallel, each is isolated gate definition
  Track D: US-501 (Design Review Board, 3 pts) -- parallel, collaboration pattern doc

Phase 3b (Days 7-10, after gates complete):
  US-502 (BOM Reconciliation, 2 pts) -- after US-403
```

#### Definition of Done -- Sprint 3

- [ ] Rework loops define all 8 paths with termination conditions (US-107)
- [ ] All 5 gates detect seeded defects in reference test fixture (>80% category detection for schematic gate)
- [ ] Critical findings block pipeline advancement for all gates
- [ ] Documentation integration dispatch patterns complete (US-305)
- [ ] kicad-happy dependency documented with verification script (US-306)
- [ ] Design Review Board dispatches to 3+ roles independently with deduplication (US-501)
- [ ] BOM reconciliation flags >20% pricing discrepancies (US-502)
- [ ] All acceptance criteria for committed stories pass
- [ ] PO sign-off on each completed story

---

### Sprint 4: SessionStart Hook, P2 Stories, and Stabilization

**Sprint Goal:** SessionStart hook validates environment readiness. Pipeline state persistence and self-learning memory operational. All P1 and P2 stories complete. Plugin ready for end-to-end UAT.

**Sprint Dates:** Sprint 4 (Weeks 7-8)
**Team Capacity:** 40 story points (80% ceiling)
**Committed:** 17 story points (43% of ceiling)

#### Committed Stories

| # | Story | Points | Priority | Dependencies | Internal Sequence |
|---|-------|--------|----------|--------------|-------------------|
| 1 | US-503: SessionStart Hook | 5 | P1 | US-104, US-306 | Phase 4a (Days 1-3) |
| 2 | US-105: Pipeline State Persistence | 5 | P2 | US-102 | Phase 4a (Days 1-3, parallel) |
| 3 | US-106: Self-Learning Memory | 3 | P2 | US-102 | Phase 4a (Days 1-2, parallel) |
| 4 | US-504: Schematic DRC Hook | 2 | P2 | US-402 | Phase 4a (Days 1-2, parallel) |
| 5 | US-505: BOM Drift Detection Hook | 2 | P2 | US-403 | Phase 4a (Days 1-2, parallel) |
| | **Sprint Total** | **17** | | | |

**Commitment:** 17 of 40 pts (43% of ceiling). 23-point buffer for Sprint 2/3 spillover, end-to-end integration testing, bug fixes, and documentation polish.

#### Commitment Rationale

US-503 is the final P1 story. It depends on both US-104 (Sprint 1) and US-306 (Sprint 3). The remaining 4 stories are P2 work deferred from Sprint 3 to make room for US-107 and gate stories. All P2 stories have their dependencies resolved from prior sprints.

This sprint is intentionally light to serve as a stabilization and integration testing phase. The remaining 23 points of capacity are available for:

1. **Sprint 2/3 spillover** -- if the complex stories (US-103, US-107, US-401) took longer than estimated
2. **End-to-end integration testing** -- run the full pipeline against the reference test fixture
3. **Bug fixes and refinements** -- address issues found during integration testing
4. **Documentation polish** -- ensure all references are consistent and cross-linked

After this sprint, all 27 P1 stories and 5 P2 stories are complete. The plugin is ready for UAT.

The return of the king is not hurried. We arrive when the road is clear and the fellowship is whole.

#### Internal Sequencing

```
Phase 4a (Days 1-5, parallel):
  US-503 (SessionStart Hook, 5 pts)
  US-105 (State Persistence, 5 pts)
  US-106 (Memory, 3 pts)
  US-504 (Schematic DRC Hook, 2 pts)
  US-505 (BOM Drift Detection Hook, 2 pts)

Phase 4b (Days 5-10):
  End-to-end integration testing
  Spillover absorption
  Documentation polish
```

#### Definition of Done -- Sprint 4

- [ ] SessionStart hook validates config and reports kicad-happy availability (US-503)
- [ ] Paused pipeline staleness detection functional (US-503)
- [ ] State persistence saves/restores pipeline state across sessions (US-105)
- [ ] Memory protocol stores/retrieves lessons with tiered chunked retrieval (US-106)
- [ ] PostToolUse hooks trigger on .kicad_sch file modifications (US-504, US-505)
- [ ] All 27 P1 stories complete with acceptance criteria passing
- [ ] All 5 P2 stories complete with acceptance criteria passing
- [ ] End-to-end pipeline run against reference test fixture succeeds
- [ ] All hooks fire correctly (SessionStart, PostToolUse)
- [ ] PO sign-off on sprint and overall delivery

---

## 3. Capacity Matrix

| Sprint | Raw Velocity | 80% Ceiling | Committed | % of Ceiling | Buffer | Cumulative Pts | Stories |
|--------|-------------|-------------|-----------|--------------|--------|---------------|---------|
| Sprint 1 | 50 | 40 | 32 | 80% | 8 pts | 32 | 8 |
| Sprint 2 | 50 | 40 | 33 | 83% | 7 pts | 65 | 8 |
| Sprint 3 | 50 | 40 | 35 | 88% | 5 pts | 100 | 10 |
| Sprint 4 | 50 | 40 | 17 | 43% | 23 pts | 117 | 5 |
| **Total** | | **160** | **117** | **73% avg** | **43 pts total** | **117** | **31** |

### Point Verification

| Sprint | Stories (with points) | Sum |
|--------|----------------------|-----|
| Sprint 1 | US-101(2) + US-108(1) + US-102(8) + US-104(5) + US-201(3) + US-202(5) + US-203(5) + US-205(3) | **32** |
| Sprint 2 | US-204(3) + US-206(3) + US-301(5) + US-400(5) + US-103(8) + US-302(3) + US-303(3) + US-304(3) | **33** |
| Sprint 3 | US-107(8) + US-305(2) + US-306(3) + US-401(5) + US-402(3) + US-403(3) + US-404(3) + US-405(3) + US-501(3) + US-502(2) | **35** |
| Sprint 4 | US-503(5) + US-105(5) + US-106(3) + US-504(2) + US-505(2) | **17** |
| **Grand Total** | **31 stories** | **117 pts** |

**Point discrepancy resolved:** The PO's summary table stated 113 pts. The per-story authoritative values sum to 117 pts (99 P1 + 18 P2). This plan uses 117 pts as the source of truth. The 4-point discrepancy arose from the PO's summary table not reflecting individual story point estimates. The PO artifact (stories.md) must be updated to reconcile the summary table with per-story values.

**Excluded from plan:** US-601 (8 pts, P3) and US-602 (5 pts, P3) are deferred to Phase 2.

---

## 4. Coverage Matrix: FR-ID to Sprint Mapping

| FR-ID | Story(s) | Sprint | Covered |
|-------|----------|--------|---------|
| FR-001 | US-101, US-108 | Sprint 1 | Yes |
| FR-002 | US-102 | Sprint 1 | Yes |
| FR-003 | US-103 | Sprint 2 | Yes |
| FR-004 | US-104 | Sprint 1 | Yes |
| FR-005 | US-105 | Sprint 4 | Yes |
| FR-006 | US-106 | Sprint 4 | Yes |
| FR-007 | US-107 | Sprint 3 | Yes |
| FR-008 | US-201, US-202, US-203, US-204, US-205, US-206 | Sprint 1-2 | Yes |
| FR-009 | US-301 | Sprint 2 | Yes |
| FR-010 | US-401 | Sprint 3 | Yes |
| FR-011 | US-402 | Sprint 3 | Yes |
| FR-012 | US-403 | Sprint 3 | Yes |
| FR-013 | US-404 | Sprint 3 | Yes |
| FR-014 | US-405 | Sprint 3 | Yes |
| FR-015 | US-501 | Sprint 3 | Yes |
| FR-016 | US-502 | Sprint 3 | Yes |
| FR-017 | US-503 | Sprint 4 | Yes |
| FR-018 | US-504 | Sprint 4 | Yes |
| FR-019 | US-505 | Sprint 4 | Yes |
| FR-020 | US-102 (Agent tool dispatch guardrail) | Sprint 1 | Yes |
| FR-021 | Deferred to Phase 2 (P2) | Deferred | Deferred (P2) |
| FR-022 | US-400 | Sprint 2 | Yes |

**All 22 FRs mapped. No orphans. No gaps.** FR-021 marked as "Deferred (P2)" per challenger advisory A1 -- it is not covered by any P1 story in this plan.

---

## 5. Risk Register

| # | Risk | Sprint | Impact | Likelihood | Mitigation |
|---|------|--------|--------|------------|------------|
| R-01 | **Sprint 2 complexity** -- US-103 (Gate Framework, 8 pts) is the most complex Sprint 2 story | Sprint 2 | Sprint 2 spillover delays gates in Sprint 3 | Medium | Sprint 2 now has 7-point buffer (v1.0 had zero). Sprint 3 has 5-point buffer. US-107 no longer shares Sprint 2 with US-103, eliminating dual-L-story risk. |
| R-02 | **Gate framework (US-103) complexity underestimated** -- hardware-specific DoD criteria may require iteration | Sprint 2 | Blocks all 5 individual gates in Sprint 3 | Medium | Start US-103 first in Sprint 2 (Phase 2a). If it slips, gates slip within Sprint 3 buffer or to Sprint 4 where 23-point buffer absorbs them. |
| R-03 | **Rework loop (US-107) non-linear semantics** -- most complex orchestration pattern in the backlog | Sprint 3 | Rework loops non-functional; pipeline is linear-only | Medium | US-107 now has its own sprint (Sprint 3) separate from US-103. If rework proves impractical in SKILL.md format, pivot to simplified rework (reduce 8 paths to 3 critical paths). Sprint 4 buffer absorbs spillover. |
| R-04 | **kicad-happy output contract drift** -- integration layer depends on stable kicad-happy contracts | Sprint 2-3 | Gates produce false positives/negatives | Low | US-306 adds pre-flight check (Sprint 3). Config pins minimum kicad-happy version. Contract validation in integration subs. |
| R-05 | **Reference test fixture (US-400) insufficient realism** -- seeded defects too simple for meaningful gate testing | Sprint 2 | Gate acceptance criteria unmeasurable; North Star metric unquantifiable | Medium | Seed defects from real-world examples (issue #76 documented 30+ real defects). MANIFEST.md enables iterative fixture improvement. |
| R-06 | **hardware-flow/SKILL.md exceeds context window** -- orchestrator grows large with stage definitions and dispatch patterns | Sprint 1 | Orchestrator non-functional at runtime | Low | Architecture Section 4 three-level loading limits Level 2 to 500-2000 tokens. Monitor token count during US-102. Refactor to references if needed. |
| R-07 | **No velocity baseline** -- first GREENFIELD sprint has no historical data for calibration | Sprint 1 | Commitment is inaccurate; Sprint 2 planning unreliable | High | Sprint 1 IS the calibration sprint, now at 80% ceiling (v1.0 was 95%). Actual velocity measured and applied to Sprint 2 commitment. **Calibration caveat:** Sprint 1 markdown velocity does not predict Sprint 2 code-complexity velocity. Adjustment protocol accounts for this. |
| R-08 | **Solo contributor risk** -- single-point-of-failure on all implementation | All | Any blocker (illness, context switching) halts all progress | Medium | Sprint plan has 43 pts of total buffer across all sprints. Sprint 4 is intentionally light. Stories are independent enough to reorder if one blocks. |

---

## 6. Sprint Velocity Tracking (Template)

> "The fellowship does not guess its pace. It measures, learns, and adjusts."

| Sprint | Committed | Completed | Velocity | Accuracy | Notes |
|--------|-----------|-----------|----------|----------|-------|
| Sprint 1 | 32 | TBD | TBD | TBD | Calibration sprint (markdown-heavy -- see caveat below) |
| Sprint 2 | 33 | TBD | TBD | TBD | Re-plan if Sprint 1 velocity < 28 |
| Sprint 3 | 35 | TBD | TBD | TBD | Buffer sprint -- absorbs spillover |
| Sprint 4 | 17 | TBD | TBD | TBD | Stabilization sprint |

**Calibration caveat:** Sprint 1 is ~95% markdown work (role SKILL.md files, plugin skeleton, config schema). Sprint 2 introduces higher-complexity work (gate framework, integration layer). Sprint 1 actual velocity should NOT be taken at face value for Sprint 2 planning. Apply a 15-20% complexity discount when projecting Sprint 2 capacity from Sprint 1 actuals.

**Adjustment protocol:**
- If Sprint 1 velocity < 25: reduce Sprint 2 commitment to 25 pts (move US-103 Phase 2b items to Sprint 3)
- If Sprint 1 velocity < 28: reduce Sprint 2 commitment to 28 pts (move US-304 to Sprint 3)
- If Sprint 1 velocity > 38: Sprint 2 can absorb 1-2 additional stories from Sprint 3 (but NOT US-107 -- keep it in Sprint 3 where it has room)

---

## 7. Assumptions

1. Sprint duration is 2 weeks (10 working days), standard for this team.
2. Solo contributor works full-time on this plugin during sprint execution.
3. Markdown-heavy estimation calibration (one tier lower than code-heavy) from PO is accurate.
4. kicad-happy plugin remains stable at version >= 1.2.x throughout implementation.
5. The Claude Code harness supports cross-plugin skill invocation for 11 concurrent skill registrations.
6. No external blockers (dependency on other teams, infrastructure provisioning, etc.).
7. The 80% ceiling adequately accounts for ceremony overhead, context switching, and unexpected issues for a solo contributor.
8. Sprint 1 markdown velocity is NOT directly transferable to Sprint 2 complexity -- adjustment protocol applies a complexity discount.

---

## 8. Challenger Findings Resolution

| Finding | Severity | Status | Resolution |
|---------|----------|--------|------------|
| Sprint 2 at 100% of ceiling | BLOCKING | RESOLVED | Sprint 2 reduced from 40 pts (100%) to 33 pts (83%). US-107 moved to Sprint 3. US-305/US-306 moved to Sprint 3. US-204/US-206 added from Sprint 1 rebalance. |
| Sprint 1 at 95% (calibration sprint) | WARNING | RESOLVED | Sprint 1 reduced from 38 pts (95%) to 32 pts (80%). US-204 and US-206 moved to Sprint 2. Calibration caveat added to velocity tracking. |
| 4-point discrepancy unresolved | WARNING | RESOLVED | Per-story values (117 pts) adopted as source of truth. PO must update summary table. No longer an open question. |
| FR-021 coverage misleading | ADVISORY | RESOLVED | FR-021 marked as "Deferred (P2)" in coverage matrix instead of "Yes." |
| Sprint 4 underloaded | ADVISORY | MITIGATED | Sprint 4 increased from 5 pts to 17 pts. Still intentionally light for stabilization but better utilized. |
| Test strategy depth | ADVISORY | ACKNOWLEDGED | Sprint 4 Phase 4b explicitly allocates time for end-to-end integration testing. Story points not allocated because testing effort is absorbed by the 23-point buffer. |
| Architect sequencing divergence | ADVISORY | ACKNOWLEDGED | US-301 remains in Sprint 2 (not Sprint 1). The SM accepts the risk that cross-plugin integration issues are deferred by one sprint. The calibration sprint's 80% target takes priority over early integration validation. |

---

## 9. Open Questions

| # | Question | Owner | Impact |
|---|----------|-------|--------|
| 1 | What is the actual Sprint 1 velocity? This determines whether Sprint 2 needs re-planning (threshold: 28 pts). | SM | High -- Sprint 2 adjustment protocol depends on this |
| 2 | Should US-503 (SessionStart Hook) be merged into Sprint 3 if Sprint 3 completes with remaining capacity? | SM + PO | Low -- Sprint 4 exists as stabilization regardless |

---

> "The road is long, and it does not do to leave the sprint planning to the last minute. Four sprints. Thirty-one stories. One fellowship. The challenger tested our plan, and we are stronger for it. Every sprint now carries what it can bear -- no more, no less. I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."
