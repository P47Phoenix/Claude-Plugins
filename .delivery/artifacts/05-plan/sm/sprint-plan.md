# Sprint Plan: Architect Prior Art Analysis

**Pipeline**: run-2026-04-04-w7m3
**Project Type**: BUG_FIX (light mode)
**Date**: 2026-04-04
**Scrum Master**: Aragorn
**Source**: GitHub Issue #55

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."*

---

## Sprint Goal

Add a mandatory "Prior Art Analysis" step to the architect skill so it validates and builds on user-provided specifications before proposing architecture, eliminating wasted pipeline cycles from overridden designs.

---

## Story Reference

**Story ID**: To be written by PO to `05-plan/po/stories.md`

> As a plugin developer who provides a detailed spec, I want the Architect to read, summarize, and build on my spec before proposing architecture, so that my design decisions are respected and pipeline cycles are not wasted on competing redesigns.

**Expected Acceptance Criteria** (from idea brief):
1. Architect SKILL.md contains a "Prior Art Analysis" section that executes before any design work
2. The step reads and summarizes user-provided specs, distinguishing "decisions already made" from "open questions"
3. Alternatives are only proposed when clear technical blockers are documented
4. Existing pipelines without user-provided specs are unaffected (backward-compatible)
5. Dogfooding validates the fix against a scenario with a user-provided spec

---

## Task Breakdown

| # | Task | File(s) | Estimate | Notes |
|---|------|---------|----------|-------|
| T1 | Add "Prior Art Analysis" section to SKILL.md -- new mandatory step between Phase 1 (Role Detection) and Phase 2 (Sub-Agent Invocation) | `delivery-team/skills/architect/SKILL.md` | S (1 SP) | Conditional on user-provided spec presence |
| T2 | Update Sub-Agent Prompt Template to include prior art context block | `delivery-team/skills/architect/SKILL.md` | XS (0.5 SP) | Add prior art summary to template's Context section |
| T3 | Add "respect prior art" guardrail to Architecture Guardrails section | `delivery-team/skills/architect/SKILL.md` | XS (0.5 SP) | One guardrail rule added to Software Architecture Guardrails |
| T4 | Dogfooding: invoke updated architect skill with a user-provided spec scenario | Manual execution | S (1 SP) | P0 gate -- must execute before UAT |
| **Total** | | | **3 SP** | |

### Estimate Calibration

- All tasks are markdown-only edits -- one tier lower than code changes per pre-loaded constraint
- T1-T3 modify a single file (`delivery-team/skills/architect/SKILL.md`)
- No reference files require modification -- prior art analysis is an orchestration-level behavior, not a role-specific pattern
- The 22 files in `delivery-team/skills/architect/references/` are unchanged

### Files Modified

| File | Change Type |
|------|-------------|
| `delivery-team/skills/architect/SKILL.md` | Modified -- add Prior Art Analysis section (~Phase 1.5), update prompt template, add guardrail |

### Files NOT Modified

The 22 reference files in `delivery-team/skills/architect/references/` contain role-specific architectural patterns (architecture-patterns.md, c4-model.md, security-patterns.md, game-systems.md, etc.). Prior art analysis is an orchestration concern that lives in SKILL.md, not a reference-level concern. No reference changes needed.

---

## Capacity Declaration

| Metric | Value | Rationale |
|--------|-------|-----------|
| Team size | 1 developer | Single-developer team |
| Velocity baseline | 5 SP/sprint | Markdown-focused BUG_FIX work, one tier lower than code |
| Sprint ceiling (80%) | 4 SP | 5 x 0.80 = 4 SP max commitment |
| Sprint commitment | 3 SP | Under ceiling; 1 SP buffer for dogfooding iteration |
| Utilization | 60% | Conservative -- leaves room for rework if dogfooding reveals instruction gaps |

The fellowship commits to 3 points against a 4-point ceiling. We march with strength to spare.

---

## Definition of Done

- [ ] Prior Art Analysis section exists in `delivery-team/skills/architect/SKILL.md` with clear conditional logic ("IF user-provided spec exists THEN...")
- [ ] Prior Art Analysis step slots between Phase 1 (Role Detection) and Phase 2 (Sub-Agent Invocation)
- [ ] Sub-Agent Prompt Template updated to pass prior art summary and decision classification to sub-agents
- [ ] Architecture Guardrails include "respect user-provided specifications" rule
- [ ] Backward compatibility confirmed: all new instructions are conditional on spec presence; pipelines without specs are unaffected
- [ ] Dogfooding executed: updated skill invoked with a scenario containing a user-provided spec; prior art summary and "decisions already made" list observed in architect output (P0 gate)
- [ ] All changes confined to `delivery-team/skills/architect/` directory (no schema changes, no new dependencies, no code changes)
- [ ] PR submitted with conventional commit message referencing Issue #55

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Prior art instructions too vague -- architect still overrides specs | High | Medium | Write explicit conditional logic with concrete examples; use "MUST" language for reading specs before design |
| Instructions conflict with existing Domain Discovery section | Medium | Low | Prior art analysis slots BEFORE domain discovery -- it gates entry, doesn't replace it. Review interaction during T1. |
| Backward compatibility break for pipelines without user-provided specs | Medium | Low | All new instructions are conditional on spec presence; default path unchanged |
| Dogfooding inconclusive -- hard to verify behavioral change from markdown edits | Medium | Medium | Define specific observable outputs: prior art summary section in architect output, explicit "decisions already made" vs "open questions" classification |

> "Hold your ground. Sons of the standup, of the retro -- I see in your eyes the same fatigue that would take the heart of me. But this sprint is not yet lost." The risks are known and the mitigations are concrete. We march forward.

---

## Execution Sequence

```
T1 (Prior Art section) --> T2 (Prompt template update) --> T3 (Guardrail addition) --> T4 (Dogfooding) --> UAT
```

All tasks are sequential within a single file. T4 validates T1-T3 before UAT submission. Dogfooding is a P0 gate -- code review alone is not sufficient.

---

*Three points. One sprint. One file. The road is short but the discipline is the same -- we do not skip the dogfooding, we do not declare done without evidence, and we do not let the architect override what the user has already decided.*
