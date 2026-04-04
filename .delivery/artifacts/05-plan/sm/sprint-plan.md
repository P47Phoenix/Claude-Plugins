# Sprint Plan: Orchestrator Theme Surfacing

**Version**: 1.0
**Date**: 2026-04-04
**Scrum Master**: Aragorn
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.0
**Stories**: `.delivery/artifacts/05-plan/po/stories.md` v1.0 (GOVERNING)
**Issue**: #59
**Team Size**: 1 developer
**Pipeline Type**: FEATURE

---

> *"One does not simply walk into a SKILL.md without a plan. But this plan is clear: one story, one file, one sprint. The Fellowship has carried heavier burdens."*

---

## 1. Sprint Goal

**Add theme-gated reporting protocol to the delivery-flow orchestrator (SKILL.md only), so that non-business alias themes surface personality in stage announcements, checkpoint summaries, and transitions — while preserving neutral output for business theme and keeping internal routing personality-free.**

---

## 2. Capacity Declaration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Team size | 1 developer | Solo contributor |
| Sprint length | 1 sprint | Single story, single file, markdown-only tier |
| Velocity baseline | 8 SP/sprint | Established from prior sprints |
| Utilization ceiling | 80% = 6.4 SP | Reserve 20% for interrupts and context switching |
| Story committed | US-01 (5 SP) | Only story in scope |
| Utilization | 63% (5 / 8) | Well under ceiling; 1.4 SP buffer |

**Estimation tier**: Markdown-only edits (SKILL.md sections) — one tier below code. 5 SP reflects the breadth of 5 FRs touching 3 distinct output slots (announcements, checkpoints, transitions) plus neutrality preservation rules, plus 3 dogfooding validation passes.

---

## 3. Task Breakdown and Sequencing

### Phase 1: Theme-Gated Reporting Protocol (2.75 SP)

> *"First, we teach the orchestrator to speak with the voice it has been given."*

| Task | Description | Est | Depends On |
|------|-------------|-----|------------|
| T-01 | Add "Theme-Gated Reporting Protocol" sub-section to Phase 4 of SKILL.md with theme detection guard (`aliases.theme != business`) | 0.5 SP | — |
| T-02 | Add theme-aware stage announcement logic to Step 1 (conditional: non-business theme uses character name from `roles` map + thematic voice; business/unset uses neutral format) | 0.5 SP | T-01 |
| T-03 | Add partial-theme fallback rule: if role has no entry in theme's `roles` map, fall back to neutral announcement for that stage | 0.25 SP | T-02 |
| T-04 | Add theme-aware checkpoint summary logic to Step 9 (read artifact, select themed quote max 280 chars, include in checkpoint output; omit if no themed language found) | 0.75 SP | T-01 |
| T-05 | Add two-channel enforcement clause: quote extraction is user-facing only, never forwarded to downstream agent prompts | 0.25 SP | T-04 |
| T-06 | Add theme-aware transition logic to Step 10 (STATE ANCHOR carries thematic voice while preserving routing signals: stage number, name, continuation directive) | 0.5 SP | T-01 |

### Phase 2: Neutrality Preservation (0.75 SP)

> *"And then we ensure the internal roads remain unmarked by personality — routing data must stay clean."*

| Task | Description | Est | Depends On |
|------|-------------|-----|------------|
| T-07 | Add explicit neutrality preservation rules for internal routing (state.md, stage-summary.md, Agent Invocation Templates, DoD validator prompts) | 0.5 SP | T-01 |
| T-08 | Add signal block format invariance rule (format unchanged regardless of theme; extraction logic unchanged) | 0.25 SP | T-07 |

### Phase 3: Dogfooding Validation (1.5 SP)

> *"We do not ship what we have not walked. Three runs. Three themes. Three verdicts."*

| Task | Description | Est | Depends On |
|------|-------------|-----|------------|
| T-09 | Dogfood: run pipeline end-to-end with `lotr` theme, verify all 3 themed output slots carry theme voice | 0.75 SP | T-06, T-08 |
| T-10 | Dogfood: run pipeline with `business` theme, verify zero behavior change vs. pre-feature baseline | 0.5 SP | T-08 |
| T-11 | Dogfood: run pipeline with partial custom theme (missing roles), verify graceful fallback to neutral | 0.25 SP | T-09 |

---

## 4. Dependency Graph

```
T-01 (Protocol section)
├── T-02 (Announcements) ──> T-03 (Partial fallback)
├── T-04 (Checkpoints) ──> T-05 (Two-channel clause)
├── T-06 (Transitions)
└── T-07 (Neutrality rules) ──> T-08 (Signal invariance)

T-06 + T-08 ──> T-09 (Dogfood: lotr)
T-08 ──> T-10 (Dogfood: business)
T-09 ──> T-11 (Dogfood: partial theme)
```

**Critical path**: T-01 > T-04 > T-05 > T-07 > T-08 > T-09 > T-11

---

## 5. Sprint Summary

| Sprint | Stories | SP Committed | Ceiling | Utilization | Buffer |
|--------|---------|-------------|---------|-------------|--------|
| Sprint 1 | US-01 | 5 | 6.4 | 63% | 1.4 SP |

---

## 6. File Impact Summary

| File | Change Type | Tasks |
|------|------------|-------|
| `delivery-team/skills/delivery-flow/SKILL.md` | Modification (add sub-section to Phase 4, conditional blocks in Steps 1/9/10, neutrality rules) | T-01 through T-08 |

No other files are modified. No new files are created. No config schema changes.

---

## 7. Definition of Done

A story is DONE when ALL of the following are true:

| # | Criterion |
|---|-----------|
| DoD-1 | All 11 tasks are complete |
| DoD-2 | All 17 acceptance criteria from stories.md are met |
| DoD-3 | SKILL.md is syntactically valid markdown (renders correctly) |
| DoD-4 | No regression: `business` theme output is identical to pre-feature behavior |
| DoD-5 | Two-channel architecture preserved: no artifact content in downstream agent prompts |
| DoD-6 | All 3 dogfooding runs pass (lotr, business, partial custom theme) |
| DoD-7 | Theme surfacing logic is contained in a single clearly-demarcated section of SKILL.md |

---

## 8. Risk Assessment

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|-----------|------------|
| R1 | Themed STATE ANCHOR confuses downstream agents | High | Low | AC-10 requires routing signals always present within themed messages. TC-07 validates coexistence. |
| R2 | Quote extraction violates two-channel rule | High | Low | T-05 adds explicit enforcement clause. TC-11 validates agent templates contain only paths. |
| R3 | Scope creep from dogfooding discoveries | Medium | Medium | Dogfooding validates, it does not discover new features. Issues found are logged as follow-ups, not added to the sprint. |
| R4 | Partial themes produce garbled output | Medium | Low | T-03 adds explicit fallback rule. TC-03 validates graceful degradation. |

---

> *"Five story points. Sixty-three percent utilization. A buffer of one and four-tenths. This is a sprint built for certainty, not heroism. We walk this road at a pace the Fellowship can sustain."*

---

*Planned by Scrum Master (Aragorn) — delivery-team:product-delivery*
