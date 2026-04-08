# Sprint Plan: Orchestration Discipline Bundle

**Stage**: 05 — Plan (SM sub-flow)
**Scrum Master**: Aragorn, son of Arathorn
**Source stories**: `.delivery/artifacts/05-plan/po/stories.md` (13 stories, 32 points)
**Source PRD**: `.delivery/artifacts/02-refine/po/prd.md` (16 FRs, 8 NFRs)
**Source architecture**: `.delivery/artifacts/04-architect/solution/architecture.md`
**ADRs**: ADR-001 (origin detection), ADR-002 (project_type migration), ADR-003 (loop convergence)

> *"The road is long and the burden heavy, but we will walk it together, one step at a time, and no step will be skipped. Rest easy — I have studied the path."*
> — Aragorn

---

## 1. Capacity Declaration

| Parameter | Value |
|---|---|
| Sprint length | 1 sprint (atomic-merge bundle) |
| Team size | 1 developer (solo) |
| Nominal capacity | 40 points |
| Utilization ceiling | **80% → 32 points committed maximum** |
| Committed this sprint | **32 points** (exactly at ceiling) |
| Strict headroom | 0 points |
| Conditional headroom | 5 points (if OD-10 is dropped per FR-12 MAY clause) |
| Calibration rule | Markdown / protocol-doc edits estimated one tier lower than equivalent code edits (inherited from PO stories.md) |
| Test artifact rule | Test cases co-located with each story — no split test artifact |
| Atomic merge rule (NFR-08) | All 13 stories ship as a single PR. No partial merges. |

**Commitment stance**: We commit to the 32 points at the exact ceiling because the bundle *requires* atomic shipment (NFR-08). Splitting across sprints would force the same SKILL.md, pipeline-stages.md, team-patterns.md, and config-schema.md files to be re-edited with merge churn — a worse risk profile than committing at the ceiling. OD-10 is the explicit pressure-relief valve per FR-12; if any other story expands mid-sprint, OD-10 drops and we settle at 29 points (~73% utilization).

---

## 2. Sprint Goal

Ship the four orchestration discipline fixes (#73, #71, #70, #69) as one cohesive, atomically-merged PR that the orchestrator demonstrably dogfoods, with schema bumped to v2.7 and every consumer-facing doc in parity.

**Definition of success**: single PR merged; 16/16 FRs traced to passing test cases; OD-13 final grep gates green; dogfood run (NFR-06) executed with every artifact authored by a sub-agent.

---

## 3. Capacity Matrix

Capacity matrix maps committed points against the 40-point nominal / 32-point ceiling, broken out by story type and by the four issues this bundle addresses.

### 3.1 By work type

| Work type | Stories | Points | % of commit | Notes |
|---|---|---|---|---|
| Markdown / protocol doc | OD-01, OD-02, OD-03, OD-04, OD-05, OD-06, OD-08, OD-09, OD-11, OD-12, OD-13 | 21 | 65.6% | 11 stories. Tier-reduced per calibration rule. |
| Executable Python (hook) | OD-07 | 8 | 25.0% | Only load-bearing code story in the bundle. |
| Executable Python (optional hook) | OD-10 | 3 | 9.4% | MAY per FR-12; first drop on expansion. |
| **Total** | **13** | **32** | **100%** | At ceiling. |

### 3.2 By issue (PRD source)

| Issue | Title | Stories | Points | % of commit |
|---|---|---|---|---|
| #73 | Remove `project_type` from config | OD-01, OD-02, OD-03, OD-04 | 7 | 21.9% |
| #71 | Orchestrator delegation bypass | OD-05, OD-06, OD-07 | 12 | 37.5% |
| #70 | One sub-agent per reviewer role | OD-08, OD-09, OD-10 | 6 | 18.75% |
| #69 | Isolated adversarial loops | OD-11, OD-12 | 4 | 12.5% |
| Cross-cutting | Doc parity sweep | OD-13 | 3 | 9.4% |
| **Total** | | **13** | **32** | **100%** |

### 3.3 By priority

| Priority | Stories | Points |
|---|---|---|
| P0 | OD-01, OD-02, OD-03, OD-04, OD-05, OD-06, OD-07, OD-08, OD-09, OD-13 | 25 |
| P1 | OD-11, OD-12 | 4 |
| P2 (MAY) | OD-10 | 3 |
| **Total** | | **32** |

P0 load is 78% of commit. This is the ship-blocking backbone; P1 and P2 trail.

### 3.4 Burn plan (points-per-day, 5-day sprint reference)

| Day | Target burn | Cumulative | Work block |
|---|---|---|---|
| Day 1 | 7 | 7 | Foundation block: OD-01 (2) + OD-04 (2) + OD-03 (1) + OD-02 (2) |
| Day 2 | 5 | 12 | SKILL.md block part 1: OD-05 (3) + OD-06 (1) + OD-08 (1) |
| Day 3 | 5 | 17 | Reference-docs block: OD-09 (2) + OD-11 (3) |
| Day 4 | 9 | 26 | Loop-doc tail OD-12 (1) + hook block OD-07 (8) |
| Day 5 | 6 | 32 | OD-10 (3, conditional) + OD-13 doc parity sweep (3) |

Day 4 is the steepest day because OD-07 is the only large code story and must land after OD-04 (schema v2.7) and OD-05 (Directive section name). If Day 4 slips, OD-10 drops on Day 5 and the sprint lands at 29.

---

## 4. Dependency Graph and Execution Order

The execution order below is the only ordering that respects every dependency in stories.md and the architect's ADR dependencies.

### 4.1 Story dependencies

```
                        OD-01 (schema deprecates project_type)
                          |
        +-----------------+-------------------+
        |                                     |
      OD-02 (SKILL.md Phase 1)              OD-04 (schema v2.7 bump)
                                              |
                                            OD-03 (routing.force_type)
                                              |
                                            OD-07 (hook, code) <--- OD-05
                                              |
                                            OD-13 (doc parity, runs last)

      OD-05 (Delegation Directive, SKILL.md)
        |
        +-----+--------+
        |     |        |
      OD-06  OD-08    OD-07 (also depends on OD-04)
              |
            OD-09

      OD-11 (Isolated Adversarial Loop, ADR-003)
        |
      OD-12 (Stage 4 references OD-11)

      OD-10 (MAY, depends on OD-08)
```

### 4.2 ADR-level dependencies (architect traceability)

| Story | ADR | Binding |
|---|---|---|
| OD-07 | ADR-001 (origin detection) | Layered detection Layer 1/2/3 spec; allowlist; activation gating |
| OD-01, OD-02, OD-03, OD-04 | ADR-002 (project_type migration) | Deprecation narrative and tolerant-parse path |
| OD-11, OD-12 | ADR-003 (loop convergence) | Two-clean / no-new-classes / hard-cap algorithm |
| OD-13 | all three | Doc-parity sweep must cite final ADR-decided terminology |

Confirmed: OD-07 depends on ADR-001 as specified. OD-11 and OD-12 depend on ADR-003 as specified. OD-13 depends on all twelve preceding stories (runs last). Dependencies match the task brief.

### 4.3 Recommended execution order

1. **Foundation block** — OD-01 → OD-04 → OD-03 → OD-02
   Lock config schema, version bump, override key, and SKILL.md Phase 1 rewording in one continuous file-touch session on `config-schema.md` + `SKILL.md` + `setup-wizard.md` + `project-types.md`. Avoids merge churn.

2. **SKILL.md delegation block** — OD-05 → OD-06 → OD-08
   All three touch `SKILL.md`. Execute in one continuous session to keep the Delegation Prime Directive, Step 4.5, and "One Role = One Sub-Agent" callout edits on a single working tree.

3. **Reference-docs block** — OD-09, OD-11, OD-12
   Parallel-safe across distinct files (`team-patterns.md`, `quality-gates.md`, `pipeline-stages.md`). OD-12 must follow OD-11 (same file, and Stage 4 references the pattern name).

4. **Hook block** — OD-07
   Executed only after OD-04 (schema v2.7 + `pipeline.enforce_self_write_block`) and OD-05 (Delegation Prime Directive section name) are final. Largest story; slip risk isolated here.

5. **Optional** — OD-10 (only if OD-07 came in under estimate, otherwise drop)

6. **Doc parity sweep** — OD-13 (last; catches any stale v2.6 references introduced during steps 1–5)

### 4.4 Slip protocol

If at end of Day 4 OD-07 is incomplete or OD-07 is complete but at full estimate with no remaining buffer:

1. **Drop OD-10** immediately (FR-12 explicitly permits this; OD-08 + OD-09 docs-only path satisfies the PRD for issue #70).
2. Sprint re-lands at **29 points (~72.5% utilization)**, restoring 5 points of Day-5 buffer.
3. OD-13 still runs last — the doc-parity gate is not negotiable (NFR-04, NFR-08).
4. If *both* OD-10 is dropped *and* OD-07 still slips, escalate to human checkpoint before splitting the atomic PR — atomic merge (NFR-08) is a harder constraint than sprint boundary.

---

## 5. Coverage Matrix

Coverage matrix maps every PRD FR and NFR to the story or stories that satisfy it, and confirms that every committed story is traced to at least one FR. This is the SM-level view; the PO stories.md already contains the test-case-level coverage audit.

### 5.1 FR coverage (16/16)

| FR | Story | Points contributed | Verification |
|---|---|---|---|
| FR-01 | OD-01, OD-04 | 2 + 2 | Config schema no longer lists `project_type` as active; v2.7 bump |
| FR-02 (a) tolerant parse | OD-04 | (2) | Deprecated-keys section documents tolerant parse + banner |
| FR-02 (b) force_type key | OD-03 | 1 | `routing.force_type` documented with enum + default |
| FR-02 (c) precedence | OD-03 | (1) | Both keys present → `routing.force_type` wins, bare project_type still emits deprecation |
| FR-03 | OD-02 | 2 | Phase 1 detection runs every invocation; no config override branch |
| FR-04 | OD-01 | (2) | Wizard Q1 removed; Q2–Q10 renumbered to Q1–Q9 |
| FR-05 | OD-01, OD-02 | (2) + (2) | Detected type written to `state.md` only, never persisted back |
| FR-06 | OD-05 | 3 | Delegation Prime Directive at top of SKILL.md; cross-referenced ≥3x |
| FR-07 | OD-06 | 1 | Step 4.5 explicitly rejects "simple enough" exemption |
| FR-08 | OD-05 | (3) | Six anti-patterns named, each with alternative |
| FR-09 (a) orchestrator deny / sub-agent allow | OD-07 | 8 | Layer 1 env var + Layer 2 frame check; test cases T1–T3 |
| FR-09 (b) Bash redirection | OD-07 | (8) | Regex covers >, >>, tee, cat <<, dd of=, cp, mv |
| FR-09 (c) sub-agent Bash allow | OD-07 | (8) | Sub-agent frame under same origin rule |
| FR-09 (d) warning fallback | OD-07 | (8) | Layer 3 systemMessage, no deny |
| FR-09 (e) known gaps | OD-07 | (8) | Module docstring + mirror in quality-gates.md |
| FR-10 | OD-08 | 1 | "One Role = One Sub-Agent" callout in SKILL.md |
| FR-11 | OD-09 | 2 | Dispatch rule on all 6 collaboration patterns |
| FR-12 | OD-10 (MAY) | 3 | Compound-role audit warning; negation-aware; non-blocking |
| FR-13 | OD-11 | 3 | Isolated Adversarial Loop pattern with full convergence spec |
| FR-14 | OD-12 | 1 | Stage 4 references pattern by name; loop bounded by config |
| FR-15 | OD-04, OD-11, OD-12 | (2) + (3) + (1) | `max_self_correction` expanded + referenced from loop doc + Stage 4 |
| FR-16 | OD-13 | 3 | CLAUDE.md / README.md / marketplace.json / docs/** at v2.7 |

All 16 FRs are covered. OD-10 is the only FR whose coverage is conditional on commitment level; if OD-10 drops, FR-12 is unsatisfied *for this sprint* and must be carried to the next sprint. Noted as slip-protocol escalation.

### 5.2 NFR coverage (8/8)

| NFR | Story | Verification |
|---|---|---|
| NFR-01 (hook perf ≤ 50ms p95) | OD-07 | OD-07-T8 benchmarks 100 invocations |
| NFR-02 (stdlib only) | OD-07, OD-10 | ACs forbid third-party imports; OD-10-T6 smoke import |
| NFR-03 (backwards compat) | OD-04 | Deprecated-keys tolerant-parse assertion |
| NFR-04 (doc parity) | OD-13 | Final grep gates T5 |
| NFR-05 (graceful degradation) | OD-07, OD-10 | `try/except → sys.exit(0)`; forced-exception tests T11 / T5 |
| NFR-06 (dogfood) | process | Every artifact in this pipeline run authored by a sub-agent; validated at orchestrator checkpoint |
| NFR-07 (plugin-dev skills) | process | `plugin-dev:skill-development` before SKILL.md edits; `plugin-dev:hook-development` before OD-07/OD-10. Validated at developer-stage DoD |
| NFR-08 (atomic merge) | OD-13 + PR discipline | Single-PR check at merge gate |

All 8 NFRs are covered: 6 by stories, 2 by process enforcement at orchestrator and developer-stage DoD.

### 5.3 Story-to-FR reverse check

| Story | At least one FR traced? | Dead weight? |
|---|---|---|
| OD-01 | FR-01, FR-04, FR-05 | No |
| OD-02 | FR-03, FR-05 | No |
| OD-03 | FR-02 (b, c) | No |
| OD-04 | FR-01, FR-02 (a), FR-15, FR-16 | No |
| OD-05 | FR-06, FR-08 | No |
| OD-06 | FR-07 | No |
| OD-07 | FR-09 (a–e), NFR-01, NFR-02, NFR-05 | No |
| OD-08 | FR-10 | No |
| OD-09 | FR-11 | No |
| OD-10 | FR-12 | No (conditional) |
| OD-11 | FR-13, FR-15 | No |
| OD-12 | FR-14, FR-15 | No |
| OD-13 | FR-16, NFR-04, NFR-08 | No |

No dead-weight stories. No FRs uncovered. Coverage matrix is complete.

---

## 6. Risk Register (sprint-level)

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | OD-07 expands beyond 8 points during hook implementation | Medium | High (sprint slip) | Drop OD-10 as first action; escalate if still slipping | Developer + SM |
| R2 | SKILL.md merge churn across OD-05/06/08 (+ OD-02 Phase 1 rewording) | Medium | Medium | Execute SKILL.md edits in one continuous session per block (§4.3) | Developer |
| R3 | OD-13 finds stale `2.6` / `project_type` references introduced by earlier stories | High | Low–Medium | OD-13 runs last and owns the final grep gate | Developer |
| R4 | Dogfood NFR-06 forgotten by orchestrator | Low | High (PRD violation) | Orchestrator must route every artifact write through sub-agent; pipeline-bypass hook catches it | Orchestrator |
| R5 | OD-07 hook introduces a false-positive deny that blocks the rest of the sprint | Low | High | Activation gating defaults effective-`false` until schema is v2.7 + flag true; test on v2.6 config first | Developer |
| R6 | Plugin-dev skills (NFR-07) not loaded before SKILL.md / hook edits | Medium | Medium | SM enforces load at start of SKILL.md block and hook block; surface in developer-stage DoD checklist | SM |
| R7 | OD-10 negation-aware regex has high false-positive rate | Medium | Low | FR-12 permits dropping OD-10; fallback is OD-08 + OD-09 docs-only path | Developer |

---

## 7. Definition of Ready (committed stories)

Every committed story meets DoR because:

- Source PRD FR and architecture §5 edit map name the exact file and change for each story.
- Dependencies are declared and acyclic (§4.1).
- Test cases are co-located per story in stories.md (mandatory artifact pairing).
- Activation gating for OD-07 is pre-resolved (schema_version >= 2.7 AND `pipeline.enforce_self_write_block: true`).
- Plugin-dev skill pre-loads are named in the bundle-level pre-loaded constraints.

---

## 8. Definition of Done (sprint-level, on top of per-story AC)

1. All 13 stories (or 12 if OD-10 dropped) have AC met and co-located test cases green.
2. Final grep gates from OD-13 return clean: no live `2.6` references; no live `project_type` config references outside deprecation notes / changelog / Phase 1 detection prose.
3. Atomic PR opened against `main` containing all committed stories in a single merge.
4. OD-07 hook benchmarked at p95 ≤ 50ms on 100 Write invocations.
5. Dogfood evidence: every artifact in this very pipeline run (stages 01 → UAT) was authored by a sub-agent, not the orchestrator. Verified by enforce_pipeline_scope hook logs and by orchestrator checkpoint attestation.
6. Plugin-dev skills loaded at appropriate points (SKILL.md block, OD-07/OD-10 hook block). Verified in commit messages or developer-stage DoD checklist.
7. If OD-10 was dropped, a next-sprint backlog entry for FR-12 is logged before sprint close (PO auto-logs per memory).

---

## 9. Open Questions from Stories — SM Disposition

| OQ / PQ | PO disposition | SM action |
|---|---|---|
| OQ-2 (OD-10 MAY) | First pressure-relief drop | SM will invoke drop on Day 4 slip, not earlier |
| OQ-4 (Step 4.5 rename) | Captured in OD-06 AC #5 | SM will verify in Day-2 SKILL.md block review |
| OQ-7 (legacy v2.6 fixture) | Quality stage decision | SM tracks as follow-up for Quality stage, non-blocking for this sprint |
| PQ-1 (Layer ordering) | OD-07 AC #1 | SM verifies in OD-07 code review on Day 4 |

---

*"Thirteen stories, thirty-two points, one road. I have counted every step. If the mountain grows during the climb, we set down the lightest pack — OD-10 — and we keep walking. The Directive is not a doctrine to us; it is a promise. Stand, and be delegated."*

— Aragorn, SM
