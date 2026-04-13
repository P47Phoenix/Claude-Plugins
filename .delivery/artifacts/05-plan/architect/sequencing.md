# Implementation Sequencing: hardware-team Plugin

**Stage:** 05-Plan | **Role:** Solution Architect (Celebrimbor) | **Task:** implementation-sequencing
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12
**Architecture Version:** 1.4 | **Stories Version:** PRD 1.1

---

> "Let us forge something that will endure beyond the ages. The ordering of the work is as important as the work itself -- a ring forged out of sequence shatters under the first test."

---

## 1. Technical Dependency Ordering

Role: Solution Architect | Task: implementation-sequencing | References: architecture.md (Section 1.1, 2.1, 3.1), stories.md (dependency graph)

### 1.1 Dependency Graph (Authoritative)

The PO's dependency graph is technically sound. I confirm the following dependency chains after cross-referencing the architecture:

```
TIER 0 (no dependencies):
  US-101  Plugin Skeleton

TIER 1 (depends on US-101 only):
  US-108  Marketplace Registration
  US-201  HW Product Owner Skill
  US-202  Electrical Engineer Skill
  US-203  PCB Layout Engineer Skill
  US-204  Manufacturing Engineer Skill
  US-205  Compliance Engineer Skill
  US-206  Test Engineer Skill
  US-301  Integration Layer Architecture
  US-400  Reference Test Fixture Creation

TIER 2 (depends on US-101 + one TIER 1 story):
  US-102  Pipeline Orchestrator           [depends: US-101]
  US-302  Component Sourcing Integration  [depends: US-301]
  US-303  Fabrication Integration         [depends: US-301]
  US-304  Analysis Integration            [depends: US-301]
  US-305  Documentation Integration       [depends: US-301]
  US-306  Dependency Docs & Verification  [depends: US-301]

TIER 3 (depends on TIER 2 stories):
  US-103  Stage Gate Validation Framework [depends: US-102]
  US-104  Config-Driven Pipeline          [depends: US-102]
  US-105  Pipeline State Persistence      [depends: US-102]
  US-106  Self-Learning Memory            [depends: US-102]
  US-501  Design Review Board             [depends: US-102, US-202, US-203, US-204]

TIER 4 (depends on TIER 3 stories):
  US-107  Rework Loop Support             [depends: US-102, US-103]
  US-401  Schematic Review Gate           [depends: US-103, US-202, US-400]
  US-402  DRC Gate                        [depends: US-103, US-203, US-400]
  US-403  BOM Gate                        [depends: US-103, US-302, US-400]
  US-404  DFM Gate                        [depends: US-103, US-204, US-303, US-400]
  US-405  Compliance Gate                 [depends: US-103, US-205, US-304, US-400]
  US-503  SessionStart Hook               [depends: US-104, US-306]

TIER 5 (depends on TIER 4 stories):
  US-502  BOM Reconciliation              [depends: US-302, US-403]
  US-504  Schematic DRC Hook              [depends: US-402]
  US-505  BOM Drift Detection Hook        [depends: US-403]
```

### 1.2 Critical Path

The longest dependency chain determines the minimum number of sequential implementation phases:

```
US-101 (2) --> US-102 (8) --> US-103 (8) --> US-107 (8) = 26 pts, 4 tiers
                                         --> US-401 (5) = 23 pts, 4 tiers
                                         --> US-405 (3) = 21 pts, 4 tiers
```

**Critical path: US-101 -> US-102 -> US-103 -> US-107** (26 points across 4 sequential tiers). This is the pipeline skeleton -> orchestrator -> gates -> rework chain. No parallelization can shorten this chain; it must be completed in order.

A secondary critical path runs through kicad-happy integration:

```
US-101 (2) --> US-301 (5) --> US-302 (3) --> US-403 (3) = 13 pts, 4 tiers
```

This is shorter in points but the same tier depth. The two paths converge at the gate stories (US-401 through US-405), which require BOTH the gate framework (US-103) AND the integration sub-stories plus role skills.

### 1.3 Architect Amendment: US-102 and US-104 Relationship

The PO places US-102 and US-104 as independent within Sprint 1, both depending only on US-101. This is technically correct but operationally suboptimal. The pipeline orchestrator (US-102) must read config values to determine stage routing behavior (architecture Section 3.2). I recommend US-104 be implemented immediately after US-102 within the same sprint -- not in parallel -- so the orchestrator's SKILL.md can reference the config schema from inception rather than requiring a retrofit.

**This is guidance, not a gate. PO retains ownership of sprint composition.**

---

## 2. Risk-First Sequencing

### 2.1 High-Risk Items (Tackle Early)

| Risk | Story | Rationale | Recommended Timing |
|------|-------|-----------|-------------------|
| **Cross-plugin invocation reliability** | US-301, US-306 | Architecture's entire value proposition depends on kicad-happy skills being consumable. Verified once (C1), but 11 skills across 6 roles is the broadest integration surface. Early implementation validates the pattern at scale. | Sprint 1 |
| **Orchestrator complexity** | US-102 | 8-stage pipeline with AI/human-execution mode classification, sub-agent dispatch, and error handling (Section 3.1.1) is the most complex single artifact. If the orchestrator SKILL.md exceeds context window limits, the entire pipeline is blocked. | Sprint 1 |
| **Gate framework viability** | US-103 | Team DoD validation adapted for hardware is unproven. If the gate pattern does not translate from software to hardware domains (e.g., DRC validation requires different semantics than unit tests), the architecture must adapt. | Sprint 2 (earliest possible after US-102) |
| **Rework loop termination** | US-107 | Non-linear pipeline behavior is the highest-complexity orchestration pattern. If rework execution semantics (Section 3.3) prove impractical in the SKILL.md format, the design must be revised. | Sprint 2 (after US-103) |
| **Reference test fixture realism** | US-400 | All 5 gate acceptance criteria depend on this fixture. If seeded defects are too simple or too complex, gate validation becomes meaningless. | Sprint 1 (parallel track) |

### 2.2 Low-Risk Items (Defer Safely)

| Story | Risk Level | Rationale |
|-------|-----------|-----------|
| US-105 (State Persistence) | Low | Pattern proven in delivery-flow. Python script mirrors existing `state_manager.py`. |
| US-106 (Memory) | Low | Pattern proven in delivery-flow. Markdown reference document only. |
| US-502 (BOM Reconciliation) | Low | Collaboration pattern document. No integration risk. |
| US-504, US-505 (PostToolUse Hooks) | Low | Simple event hooks. Pattern proven in delivery-team hooks. |

---

## 3. Integration Points: kicad-happy Verification Strategy

### 3.1 Integration Dependencies

The architecture specifies 11 kicad-happy skills consumed by 6 hardware roles (architecture Section 5.2). The integration risk is concentrated in three areas:

| Integration Area | Stories | kicad-happy Skills | Verification Strategy |
|-----------------|---------|-------------------|----------------------|
| **Component sourcing** | US-302 | digikey, mouser, lcsc, element14 | Verify all 4 sourcing skills return parts[] with expected contract (Section 5.5.1). Test with known MPN. |
| **Fabrication rules** | US-303 | jlcpcb, pcbway | Verify DFM rules return dfm_rules[] with pass/fail. Test against reference PCB (US-400). |
| **Analysis pipeline** | US-304 | kicad, spice, emc | Verify schematic analysis, SPICE simulation, and EMC checks against reference fixture. These are the most complex outputs. |

### 3.2 Recommended Integration Verification Sequence

1. **Sprint 1**: US-301 defines the integration architecture document. As part of US-301, verify each of the 11 kicad-happy skills loads via `Skill("kicad-happy:<name>")`. This is a smoke test -- load verification, not full contract validation.
2. **Sprint 2**: US-302/303/304/305 implement the specific dispatch patterns. Each sub-story should validate its kicad-happy output contracts (Section 5.5) against the reference test fixture (US-400).
3. **Sprint 2**: US-306 implements the SessionStart verification hook. This becomes the ongoing health check.

### 3.3 Architect Guidance: Integration Layer Before Gates

The 5 validation gates (US-401 through US-405) depend on kicad-happy integration being verified because gates consume kicad-happy output:
- US-401 (Schematic Gate) needs kicad-happy:kicad output for schematic analysis
- US-402 (DRC Gate) needs kicad-happy:kicad output for DRC parsing
- US-403 (BOM Gate) needs sourcing skill output for pricing/availability
- US-404 (DFM Gate) needs jlcpcb/pcbway output for fab rules
- US-405 (Compliance Gate) needs kicad-happy:emc output for EMC analysis

**Therefore: US-301 through US-306 must be complete before gates are validated end-to-end.** Gate definitions (markdown) can be written in parallel with integration sub-stories, but acceptance testing of gates against the reference fixture requires working integration dispatch.

---

## 4. Parallel Opportunities

### 4.1 Fully Parallel Tracks (No Shared Dependencies)

The following groups of stories can be developed concurrently within each sprint:

**Sprint 1 Parallel Groups:**

```
Group A (Plugin Core):        Group B (Role Skills):           Group C (Integration + Fixture):
  US-101 (skeleton)             US-201 (HW PO)                   US-301 (integration arch)
  US-108 (marketplace)          US-202 (EE)                      US-400 (test fixture)
  US-102 (orchestrator)*        US-203 (PCB Layout)
  US-104 (config)*              US-204 (MfgE)
                                US-205 (CompE)
                                US-206 (TestE)

* US-102 and US-104 depend on US-101; the rest of Group B/C also depend on US-101.
  US-101 must complete first, then Groups A(rest), B, and C run in parallel.
```

**Sprint 2 Parallel Groups:**

```
Group D (Gate Definitions):   Group E (Integration Subs):    Group F (Pipeline Logic):
  US-401 (Schematic Gate)       US-302 (Sourcing)              US-103 (Gate Framework)
  US-402 (DRC Gate)             US-303 (Fabrication)           US-107 (Rework Loops)
  US-403 (BOM Gate)             US-304 (Analysis)
  US-404 (DFM Gate)             US-305 (Documentation)
  US-405 (Compliance Gate)      US-306 (Dependency Docs)
                                US-503 (SessionStart Hook)

Note: Group D depends on Group F (US-103) completing first.
      US-503 depends on US-104 (Sprint 1) and US-306.
      US-501 (Design Review Board) depends on US-102, US-202, US-203, US-204 (Sprint 1).
```

### 4.2 File Contention Analysis

| File / Directory | Stories | Conflict Risk | Mitigation |
|-----------------|---------|---------------|-----------|
| `hardware-team/SKILL.md` | US-101, US-102 | Low | US-101 creates skeleton; US-102 fills orchestrator content |
| `marketplace.json` | US-108 | None | Single story, single edit |
| `hardware-flow/SKILL.md` | US-102, US-103, US-107 | **Medium** | Sequential within sprint. US-102 creates; US-103 adds gate sections; US-107 adds rework sections |
| `hardware-flow/references/gate-framework.md` | US-103, US-401-405 | Low | US-103 creates framework; US-401-405 add specific gate definitions. Separate sections. |
| `hardware-flow/references/kicad-integration.md` | US-301, US-302-305 | Low | US-301 creates document; US-302-305 add dispatch pattern details for specific skill categories |
| `hooks/hooks.json` | US-503, US-504, US-505 | Low | Additive entries. Sequential sprints. |

The highest contention file is `hardware-flow/SKILL.md`, which is touched by US-102, US-103, and US-107. These three stories MUST be implemented sequentially (US-102 first, then US-103, then US-107) as they build on each other. This is already reflected in the dependency graph.

---

## 5. Sprint Allocation Guidance

### 5.1 PO Sprint Plan Assessment

The PO's proposed sprint plan is structurally sound. My sequencing analysis confirms the sprint boundaries align with the dependency tiers. I offer the following amendments as guidance -- the PO retains ownership.

### 5.2 Sprint 1 Amendment: Sequence Within Sprint

The PO's Sprint 1 lists 12 stories totaling 48 points. The dependency ordering within the sprint matters:

**Phase 1a (Day 1):** US-101 (Plugin Skeleton, 2 pts)
- Must complete before anything else. Creates all directories and placeholder files.

**Phase 1b (Parallel, after US-101):**
- Track A: US-108 (Marketplace, 1 pt) -- trivial, complete immediately
- Track B: US-102 (Orchestrator, 8 pts) then US-104 (Config, 5 pts) -- sequential, core pipeline
- Track C: US-201 through US-206 (Role Skills, 22 pts total) -- all parallel with each other
- Track D: US-301 (Integration Layer, 5 pts) -- parallel with Tracks B and C
- Track E: US-400 (Test Fixture, 5 pts) -- parallel with all, no code dependencies

**Rationale:** Tracks B-E are independent after US-101 completes. Track B is sequential internally (US-104 should follow US-102). Track C stories are fully parallel -- each role skill is an isolated SKILL.md with its own references directory.

### 5.3 Sprint 2 Amendment: Gate Framework Before Individual Gates

The PO's Sprint 2 lists 14 stories totaling 55 points. The internal sequencing requires attention:

**Phase 2a (Sprint 2, first):**
- US-103 (Gate Framework, 8 pts) -- all 5 individual gates depend on this
- US-107 (Rework Loops, 8 pts) -- depends on US-103, can begin as soon as US-103 is done
- US-302-306 (Integration Subs, 14 pts total) -- all parallel with each other, depend on US-301 (Sprint 1)

**Phase 2b (Sprint 2, after US-103):**
- US-401-405 (Individual Gates, 17 pts total) -- all parallel with each other, all depend on US-103
- US-501 (Design Review Board, 3 pts) -- depends on Sprint 1 role skills
- US-503 (SessionStart Hook, 5 pts) -- depends on US-104 and US-306

**Concern: Sprint 2 at 55 points is 115% of Sprint 1's 48 points, with no velocity baseline established.** The PO correctly notes this is a GREENFIELD project with no velocity baseline. I recommend the PO consider moving US-501 (Design Review Board) to Sprint 3 if Sprint 2 velocity proves insufficient, as it is a collaboration pattern document that does not block any other P1 story. This would reduce Sprint 2 to 52 points.

### 5.4 Sprint 3: No Sequencing Concerns

Sprint 3 contains 5 P2 stories totaling 14 points. All stories are independent of each other (US-105, US-106 depend only on US-102; US-502 on US-302+403; US-504 on US-402; US-505 on US-403). Full parallelization is possible. This sprint is correctly sized as a buffer sprint.

### 5.5 Sprint Capacity Summary

| Sprint | Stories | Points | Internal Dependencies | Risk |
|--------|---------|--------|-----------------------|------|
| Sprint 1 | 12 | 48 | US-101 must be first; US-104 after US-102; rest parallel | **Medium** -- high story count but markdown-heavy |
| Sprint 2 | 14 | 55 | US-103 before US-401-405 and US-107; US-306 before US-503 | **High** -- most complex stories, no baseline velocity |
| Sprint 3 | 5 | 14 | None significant | **Low** -- proven patterns, small scope |

---

## 6. Assumptions

- kicad-happy skills remain stable at version >=1.2.x throughout implementation. No breaking changes to output contracts.
- The Claude Code harness supports cross-plugin skill invocation reliably for 11 concurrent skill registrations.
- Markdown-heavy estimation calibration (one tier lower than code-heavy work) is accurate for this project's file count.
- The reference test fixture (US-400) can be created with realistic KiCad files that exercise all 7 schematic review categories and 4 DFM violation types.

## 7. Risks to Sequencing

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Sprint 2 overcommitment (55 pts, no baseline) | Sprint 2 spillover delays Sprint 3 | Medium | Move US-501 to Sprint 3 as buffer. Monitor velocity after Sprint 1. |
| Gate framework (US-103) complexity underestimated | Blocks all 5 individual gates | Medium | Start US-103 first in Sprint 2. Hardware-specific DoD criteria may require iteration. |
| kicad-happy output contract drift | Gates produce false positives/negatives | Low | Contract validation (Section 5.5) with version pinning mitigates. US-306 adds pre-flight check. |
| Reference test fixture (US-400) insufficient realism | Gate acceptance criteria unmeasurable | Medium | Seed defects from real-world examples (issue #76 documented 30+ real defects). |
| hardware-flow/SKILL.md exceeds context window | Orchestrator non-functional | Low | Architecture Section 4 three-level loading limits Level 2 to 500-2000 tokens. Monitor during US-102. |

---

> "Let us forge something that will endure beyond the ages. The sequencing is set. The dependency chains are mapped. The risks are named. Now the fellowship must execute -- foundations first, then gates, then the bindings that hold them together."
