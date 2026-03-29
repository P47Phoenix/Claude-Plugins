# Sprint Plan: Deterministic Rules Engine Integration

**Version**: 1.0
**Author**: Aragorn (Scrum Master)
**Date**: 2026-03-28
**Status**: Committed
**Inputs**: Stories v1.0 (Gandalf/PO), Architecture v1.0 (Celebrimbor/Architect)

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."*

---

## Capacity Model

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Team size | 1 developer | Single contributor model |
| Velocity | ~40 SP/sprint | Plugin-level work: Python scripts, JSON rule files, YAML config, markdown specs |
| Commitment cap | 80% of capacity = **32 SP** | Reserve 20% for unknowns, code review rework, and integration friction |
| Sprint count | 4 sprints | Maps 1:1 to PRD Phases 0-3 |

**Total backlog**: 98 story points across 19 stories.

---

## Sprint 1 -- Phase 0: Foundation Extraction

**Sprint Goal**: Extract the proven BRE condition evaluation logic into a standalone module and produce a PO-approved routing decision specification that serves as the single source of truth for all 126 routing cells.

### Committed Stories

| Order | Story | Points | Rationale for Sequence |
|-------|-------|--------|------------------------|
| 1 | US-01: BRE Condition Evaluator Extraction | 5 | Zero dependencies. Must land first -- every Phase 1+ story depends on C1. |
| 2 | US-02: Routing Decision Specification | 8 | No code dependency, but requires focused PO collaboration for 126-cell sign-off. Can begin in parallel with US-01 but sequenced second because US-01 is the harder technical risk to retire early. |

### Capacity

| Metric | Value |
|--------|-------|
| Committed points | 13 |
| Capacity (80%) | 32 |
| Utilization | 41% |
| Buffer | 19 SP |

**Why the low utilization is intentional**: Phase 0 is foundation. The condition evaluator must be proven byte-equivalent to the original BRE across all 17 test cases before anything else proceeds. The routing specification requires PO review of 126 cells with scope constraints for every "light" entry. Rushing either artifact propagates defects into all downstream phases. The buffer absorbs: (a) discovery of edge cases in the original BRE logic, (b) PO iteration cycles on the routing spec, (c) any original BRE behavior that is ambiguous and needs clarification.

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| BRE extraction reveals undocumented edge cases in condition evaluation | Medium | High -- blocks all downstream | Start US-01 first; run all 17 test cases against the original BRE *before* extracting to establish baseline |
| PO routing spec (126 cells) requires multiple review cycles | Medium | Medium -- delays Phase 1 start | Draft the table with sensible defaults from PRD constraints; PO reviews deltas, not blank cells |
| Original BRE behavior is inconsistent (bug in source) | Low | High -- must decide: match bug or fix | Treat original behavior as canonical per AC-6 (parallel module, not refactor). Document discrepancies for future cleanup. |

### Exit Criteria

- [ ] `condition_evaluator.py` passes all 17 test cases with identical results to original BRE
- [ ] Zero SQLite imports in `condition_evaluator.py`
- [ ] Routing Decision Specification has 126 cells, all "full" or "light", all "light" cells have scope constraints
- [ ] PO sign-off recorded on routing spec

---

## Sprint 2 -- Phase 1: Stage Routing Rules and Core Engine

**Sprint Goal**: Build the core rules engine infrastructure -- adapter, context builder, translation layer, CLI entry point, routing rules, and preset profiles -- so that routing decisions are fully deterministic and code-executed by sprint end.

### Committed Stories

| Order | Story | Points | Rationale for Sequence |
|-------|-------|--------|------------------------|
| 1 | US-04: Pipeline Context Builder | 5 | Zero Phase 1 dependencies (utility module). Start here to unblock US-07. |
| 2 | US-06: YAML-to-JSON Translation Layer | 5 | Depends only on US-01 (done). Start in parallel with US-04. |
| 3 | US-03: Delivery Rules Adapter | 8 | Depends on US-01 (done). Core adapter -- US-07 and all Phase 2 stories need this. |
| 4 | US-05: Stage Routing Rules (JSON) | 5 | Depends on US-01 + US-02 (both done). Can begin in parallel with US-03. |
| 5 | US-08: Preset Profile Rule Sets | 5 | Depends on US-05. Must follow routing rules. |
| 6 | US-07: Evaluation Script (CLI Entry Point) | 8 | Depends on US-01, US-03, US-04, US-05, US-06. Integration point -- must be last. |

### Capacity

| Metric | Value |
|--------|-------|
| Committed points | 36 |
| Capacity (80%) | 32 |
| Utilization | **113% -- OVER CAPACITY** |

**Overcommitment resolution**: Phase 1 is 36 SP against a 32 SP cap. Three options:

1. **Recommended**: Accept the overcommitment. Sprint 1 used only 41% capacity, leaving substantial runway. If Sprint 1 finishes early (likely given the 19 SP buffer), the developer can pull US-04 and US-06 forward into Sprint 1 as stretch goals, dropping Sprint 2 effective load to 26 SP. This is the fellowship's plan.
2. Alternative A: Defer US-08 (Presets, 5 SP) to Sprint 3. Risk: Sprint 3 is already 29 SP and presets are needed for Phase 2 override testing.
3. Alternative B: Defer US-07 (Eval Script, 8 SP) to Sprint 3. Risk: Unacceptable -- the CLI entry point is the integration proof for Phase 1.

**Adopted strategy**: Plan for Sprint 1 stretch. If stretch does not materialize, US-04 (5 SP) and US-06 (5 SP) can begin early in Sprint 2 while US-03 design is being finalized, exploiting the parallelism in the dependency graph.

### Parallel Execution Lanes

```
Week 1:  US-04 (Context Builder) ─────┐
         US-06 (Translation Layer) ────┤
         US-03 (Adapter) begins ───────┤
         US-05 (Routing Rules) ────────┘
                                       │
Week 2:  US-03 (Adapter) completes ────┤
         US-08 (Presets) ──────────────┤
         US-07 (Eval Script) ──────────┘
```

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Adapter complexity exceeds estimate (8 SP) | Medium | High -- cascading delay to US-07 | Time-box adapter to 10 SP equivalent. If layer merge logic is complex, implement scalar-only merge first, add list/map merge semantics in US-14 (Phase 2). |
| Routing rules JSON does not match routing spec 1:1 | Low | Medium -- rework | Auto-generate routing.json from routing spec as a translation step, then validate both directions |
| Eval script integration surfaces interface mismatches | Medium | Medium | Define stdout/stderr contract (architecture Section 2.4) as the handshake protocol. Write contract tests before integration. |
| Overcommitment causes quality shortcuts | Medium | High | If behind by mid-sprint, defer US-08 (Presets) to Sprint 3 rather than cutting test coverage |

### Exit Criteria

- [ ] `evaluate_rules.py --decision-type routing` produces deterministic routing for all 6 project types
- [ ] 10 identical routing evaluations for the same input (byte-identical JSON)
- [ ] All 3 preset profiles (solo, standard, strict) load and apply correctly
- [ ] CLI exit codes: 0 (success), 1 (input error), 2 (evaluation error)
- [ ] Layer 1 + Layer 2 merge produces correct resolved rules

---

## Sprint 3 -- Phase 2: DoD Gates, Config Extension, and Escalation

**Sprint Goal**: Extend the rules engine to cover all remaining flow-control decisions -- DoD gates, escalation triggers, collaboration pattern selection -- and extend the config schema to v2.4 with full error handling, so that zero flow-control decisions remain AI-interpreted.

### Committed Stories

| Order | Story | Points | Rationale for Sequence |
|-------|-------|--------|------------------------|
| 1 | US-12: Config Schema Extension (v2.4) | 5 | No code dependency on other Phase 2 stories. Unblocks US-13 and US-14. Config-first approach. |
| 2 | US-09: DoD Gate Rules | 8 | Depends on US-01, US-03 (done). Largest Phase 2 story -- start early. |
| 3 | US-10: Escalation Trigger Rules | 5 | Depends on US-01, US-03 (done). Can run in parallel with US-09. |
| 4 | US-11: Collaboration Pattern Selection Rules | 3 | Depends on US-03, US-05 (done). Smallest story -- fits in parallel. |
| 5 | US-14: Rule Override Mechanism (L3 over L2 over L1) | 3 | Depends on US-03, US-08 (done). Merge semantics -- pairs with US-12 config work. |
| 6 | US-13: Error Handling and Fallback Behavior | 5 | Depends on US-03, US-07 (done). Must be last -- validates all error paths across gate, routing, and escalation. |

### Capacity

| Metric | Value |
|--------|-------|
| Committed points | 29 |
| Capacity (80%) | 32 |
| Utilization | 91% |
| Buffer | 3 SP |

### Parallel Execution Lanes

```
Week 1:  US-12 (Config Schema) ────────┐
         US-09 (DoD Gate Rules) ───────┤
         US-10 (Escalation Rules) ─────┤
         US-11 (Collab Patterns) ──────┘
                                       │
Week 2:  US-09 (DoD Gate Rules) cont. ─┤
         US-14 (Rule Overrides) ───────┤
         US-13 (Error Handling) ───────┘
```

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| DoD gate rules (7 stages x N validators) are more complex than estimated | Medium | High -- 8 SP may not suffice | Start with 3 critical stages (Design, Development, UAT). If under pressure, the remaining 4 lighter stages can use simplified rule sets initially. |
| Config schema v2.4 migration path creates backward compatibility issues | Low | Medium | Implement migration detection (AC-4) early. Validate against 3 sample configs: empty rules, partial rules, full rules. |
| Error handling three-option UX (US-13) is hard to test without real pipeline context | Medium | Low | Test error paths with synthetic errors injected into evaluate_rules.py. Dogfooding in Sprint 4 will validate the real UX. |
| Tight buffer (3 SP) leaves no room for surprises | Medium | Medium | US-11 (3 SP) and US-14 (3 SP) are low-risk. If US-09 overruns, defer US-14 merge semantics to Sprint 4 (it has no Phase 3 dependents except US-19 dogfooding). |

### Exit Criteria

- [ ] DoD gates evaluate all 7 stages with weighted scoring and critical-rule override
- [ ] Escalation rules produce correct ESCALATE/CONTINUE decisions for all 3 sensitivity profiles
- [ ] Collaboration pattern rules return deterministic patterns for all project type + stage combinations
- [ ] Config schema v2.4 documented with `rules.*` section, migration path from v2.3
- [ ] Error handling: strict mode halts, default mode presents 3 options
- [ ] Layer 1/2/3 override cascade works with per-key granularity, list replace, and list extend

---

## Sprint 4 -- Phase 3: Audit Trail, Integration, Wizard, and Dogfooding

**Sprint Goal**: Complete the rules engine integration by adding the audit trail, updating SKILL.md to defer all flow-control to the engine, extending the setup wizard, enabling dry-run preview, and validating the entire system through a dogfooding pipeline run.

### Committed Stories

| Order | Story | Points | Rationale for Sequence |
|-------|-------|--------|------------------------|
| 1 | US-15: Structured Audit Trail | 5 | No Phase 3 internal dependencies. Foundation for dogfooding evidence. |
| 2 | US-18: Dry-Run Preview | 2 | Depends on US-07 (done). Small, quick win. Useful for validating before dogfooding. |
| 3 | US-17: Setup Wizard Extension | 3 | Depends on US-12 (done). Straightforward -- 3 new wizard questions. |
| 4 | US-16: SKILL.md Orchestrator Integration | 5 | Depends on all Phase 1+2 (done). This is the keystone -- rewrites how the orchestrator makes decisions. Must precede dogfooding. |
| 5 | US-19: Dogfooding Validation | 5 | Depends on everything. Final validation. Must be last. |

### Capacity

| Metric | Value |
|--------|-------|
| Committed points | 20 |
| Capacity (80%) | 32 |
| Utilization | 63% |
| Buffer | 12 SP |

**Why the buffer is appropriate**: Sprint 4 includes dogfooding (US-19), which is inherently unpredictable. The dogfooding run will surface integration issues, edge cases, and rework needs from Phases 0-2. The 12 SP buffer absorbs defect fixes discovered during dogfooding without requiring a Sprint 5.

### Parallel Execution Lanes

```
Week 1:  US-15 (Audit Trail) ──────────┐
         US-18 (Dry-Run Preview) ──────┤
         US-17 (Setup Wizard) ─────────┘
                                       │
Week 2:  US-16 (SKILL.md Integration) ─┤
         US-19 (Dogfooding Validation) ┘
```

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SKILL.md rewrite (US-16) introduces regressions in existing pipeline behavior | High | High -- breaks production pipeline | Diff-review every SKILL.md change against current behavior. Test with dry-run before dogfooding. Keep original SKILL.md sections in a backup branch. |
| Dogfooding reveals rules engine defects requiring rework | High | Medium -- 12 SP buffer absorbs this | Budget 5 SP of the 12 SP buffer explicitly for dogfooding rework. If rework exceeds 5 SP, descope US-17 (wizard) to a follow-up. |
| Audit trail JSONL format does not capture sufficient detail for reproducibility proof | Low | Medium | Define the JSONL schema before implementation. Include full `input_context` snapshot per AC-1. |
| Dogfooding run takes longer than budgeted due to pipeline complexity | Medium | Low -- the run itself is the deliverable | Time-box dogfooding to the equivalent of 5 SP. Document any incomplete validation as follow-up items in the retrospective. |

### Exit Criteria

- [ ] Audit trail written as JSONL with all required fields per US-15 AC-1
- [ ] Dry-run preview matches actual pipeline routing decisions
- [ ] Setup wizard writes correct `rules.*` config keys
- [ ] SKILL.md defers all routing, gating, and escalation to `evaluate_rules.py`
- [ ] Dogfooding run: zero category (c) flow-control decisions in audit log
- [ ] Dogfooding run: 10 replayed routing evaluations produce byte-identical results
- [ ] Retrospective produced with lessons learned

---

## Cross-Sprint Summary

| Sprint | Phase | Stories | Points | Cap (80%) | Utilization | Goal |
|--------|-------|---------|--------|-----------|-------------|------|
| 1 | 0 | US-01, US-02 | 13 | 32 | 41% | Extract BRE core + routing spec |
| 2 | 1 | US-03 - US-08 | 36 | 32 | 113%* | Core engine + deterministic routing |
| 3 | 2 | US-09 - US-14 | 29 | 32 | 91% | Gates, escalation, config, error handling |
| 4 | 3 | US-15 - US-19 | 20 | 32 | 63% | Audit, integration, dogfooding |
| **Total** | | **19 stories** | **98** | **128** | **77%** | |

*Sprint 2 overcommitment mitigated by Sprint 1 stretch goal strategy (pull US-04 + US-06 forward).

### Cumulative Burndown Target

```
Sprint 1 end:  13 SP done  (13 of 98  = 13%)
Sprint 2 end:  49 SP done  (49 of 98  = 50%)
Sprint 3 end:  78 SP done  (78 of 98  = 80%)
Sprint 4 end:  98 SP done  (98 of 98  = 100%)
```

### Critical Path

```
US-01 -> US-03 -> US-07 -> US-13 -> US-16 -> US-19
  5       8        8        5        5        5    = 36 SP on critical path
```

The critical path runs through the condition evaluator, adapter, CLI script, error handling, SKILL.md integration, and dogfooding. Any delay on these stories cascades to the final delivery. The Scrum Master will track these six stories with daily attention.

---

*"There is always hope." But hope is not a strategy. This plan has buffers, parallel lanes, and fallback options. The fellowship will hold.*
