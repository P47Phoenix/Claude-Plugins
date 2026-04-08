# SM DoD Review — Stage 5 Plan

**Reviewer**: Aragorn, son of Arathorn (SM validator)
**Stage**: 05 — Plan
**Artifacts reviewed**:
- `.delivery/artifacts/05-plan/po/stories.md`
- `.delivery/artifacts/05-plan/sm/sprint-plan.md`

> *"I have walked the plan end to end. The road is measured, the packs are weighed, and no step is orphaned. Rest easy — the fellowship is ready to march."*

---

## 1. Capacity Matrix — PRESENT, utilization calculated

**Location**: sprint-plan.md §3 (Capacity Matrix), backed by §1 (Capacity Declaration).

| Check | Finding | Status |
|---|---|---|
| Nominal capacity declared | 40 points (1 dev × 1 sprint, calibrated) | PASS |
| Ceiling declared | 80% → 32 points | PASS |
| Commit declared | 32 points | PASS |
| Utilization calculated | 32/40 = **80.0% exactly at ceiling** | PASS |
| Breakdown by work type | §3.1: markdown (21 pts / 65.6%), code hook (8 pts / 25.0%), optional hook (3 pts / 9.4%) — sums to 32/100% | PASS |
| Breakdown by issue | §3.2: #73 (7), #71 (12), #70 (6), #69 (4), cross-cutting (3) — sums to 32 | PASS |
| Breakdown by priority | §3.3: P0 (25), P1 (4), P2 (3) — sums to 32 | PASS |
| Burn plan present | §3.4: Day-by-day 7/5/5/9/6 → 32 cumulative | PASS |
| Calibration rule stated | Markdown tier-reduced one level vs. code (inherited from PO) | PASS |

**Capacity matrix verdict**: PRESENT and complete. Multiple orthogonal breakdowns (work type, issue, priority, burn-day) all reconcile to 32.

---

## 2. Utilization ≤ 80% check

| Metric | Value | Threshold | Result |
|---|---|---|---|
| Committed points | 32 | — | — |
| Nominal capacity | 40 | — | — |
| Utilization | **80.0%** | ≤ 80% warn / ≤ 100% block | **AT CEILING — pass, no warn** |

**Finding**: Commitment lands exactly at the 80% ceiling, not above it. Per the DoD rule ("warn > 80%, block > 100%"), 80.0% is a strict pass with no warning trigger. The SM justification for committing at the ceiling is sound and explicit: atomic-merge NFR-08 forces single-sprint delivery, and splitting would introduce worse merge-churn risk than committing at ceiling. A named pressure-relief valve exists (OD-10 drops to 29 pts / 72.5% per §4.4 slip protocol, backed by FR-12 MAY clause).

**Verdict**: PASS. No warning needed.

---

## 3. Coverage Matrix — every FR mapped to ≥1 task

**Location**: sprint-plan.md §5 (Coverage Matrix), §5.1 FR coverage, §5.3 story-to-FR reverse check.

### 3.1 FR → story coverage (every FR must have ≥1 task)

| FR | Stories | ≥1 task? |
|---|---|---|
| FR-01 | OD-01, OD-04 | YES |
| FR-02 (a/b/c) | OD-04, OD-03 | YES |
| FR-03 | OD-02 | YES |
| FR-04 | OD-01 | YES |
| FR-05 | OD-01, OD-02 | YES |
| FR-06 | OD-05 | YES |
| FR-07 | OD-06 | YES |
| FR-08 | OD-05 | YES |
| FR-09 (a–e) | OD-07 | YES |
| FR-10 | OD-08 | YES |
| FR-11 | OD-09 | YES |
| FR-12 | OD-10 (MAY) | YES (conditional) |
| FR-13 | OD-11 | YES |
| FR-14 | OD-12 | YES |
| FR-15 | OD-04, OD-11, OD-12 | YES |
| FR-16 | OD-13 | YES |

**All 16/16 FRs have at least one story mapped.** FR-12 is the only FR whose coverage is conditional (OD-10 is MAY); the plan explicitly calls out that if OD-10 drops, FR-12 carries to the next sprint and PO auto-logs a backlog entry (§4.4, §8 DoD item 7). This is an acceptable, PRD-sanctioned pressure-relief path, not a coverage gap.

### 3.2 NFR coverage (bonus check)

All 8/8 NFRs traced in §5.2 (6 via stories, 2 via process enforcement).

### 3.3 Reverse check — no dead-weight stories

§5.3 confirms every committed story (OD-01 through OD-13) traces to ≥1 FR. No orphan work.

**Verdict**: PASS. FR → task coverage is 16/16 with one conditional entry that has an explicit, authorized fallback.

---

## 4. Sprint Goal — value-expressing check

**Location**: sprint-plan.md §2.

**Stated goal**:
> "Ship the four orchestration discipline fixes (#73, #71, #70, #69) as one cohesive, atomically-merged PR that the orchestrator demonstrably dogfoods, with schema bumped to v2.7 and every consumer-facing doc in parity."

| Criterion | Finding |
|---|---|
| States an outcome, not a task list | YES — "ship ... as one cohesive atomically-merged PR that the orchestrator demonstrably dogfoods" |
| Expresses value / why | YES — restoring orchestration discipline across four linked issues; dogfooding proves the fix works on the team's own workflow; doc parity ensures consumers see one consistent story |
| Measurable definition of success | YES — "single PR merged; 16/16 FRs traced to passing test cases; OD-13 final grep gates green; dogfood run (NFR-06) executed with every artifact authored by a sub-agent" |
| Bounded to the sprint | YES — names a concrete PR and a concrete set of four issues |
| Avoids "do the stories" anti-pattern | YES — frames the goal around cohesion, dogfooding, and doc parity, not "complete OD-01 through OD-13" |

**Verdict**: PASS. The goal expresses value (restored orchestration discipline, proven by dogfooding and doc parity) rather than enumerating tasks. It has a hard, testable definition of success.

---

## 5. Additional SM observations (non-blocking, for the record)

1. **Dependency graph (§4.1) is acyclic and named** — foundation → SKILL.md delegation → reference-docs → hook → optional → doc-parity sweep. Execution order respects every declared dependency.
2. **Slip protocol (§4.4) is explicit** — OD-10 is first drop, lands at 29 pts / 72.5% utilization, restores 5 pts of Day-5 buffer. Atomic-merge is called out as a harder constraint than sprint boundary, with escalation path if both OD-10 drop and OD-07 slip occur.
3. **Risk register (§6) is populated** with 7 sprint-level risks, each with likelihood, impact, mitigation, and owner. R1 (OD-07 expansion) and R4 (dogfood forgotten) are the right top risks to surface.
4. **DoR (§7)** and **sprint-level DoD (§8)** both present and concrete. Sprint-level DoD includes hook performance (NFR-01 p95 ≤ 50ms), dogfood evidence, and plugin-dev skill load verification — all testable at sprint close.
5. **Open questions from PO stories (§9)** — all four (OQ-2, OQ-4, OQ-7, PQ-1) have an explicit SM disposition with a named verification day or follow-up owner. No dangling PO questions.
6. **Alias discipline**: both artifacts stay in character (Gandalf for PO, Aragorn for SM) without sacrificing the technical rigor expected at Stage 5 Plan.

No defects. No warnings. No blockers.

---

## 6. SM DoD Decision

| DoD criterion | Result |
|---|---|
| Capacity matrix present with utilization calculated | **PASS** |
| Coverage matrix maps every FR to ≥1 task | **PASS** (16/16) |
| Capacity ≤ 80% (warn > 80%, block > 100%) | **PASS** (80.0% exactly — at ceiling, not above) |
| Sprint goal is value-expressing | **PASS** |

**SM DoD Status**: **DONE**

> *"Thirteen stories, thirty-two points, one road. Every footfall accounted for, every burden weighed, every FR walked to its bearer. The plan is sound. Ride."*
> — Aragorn, SM validator
