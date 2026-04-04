# Sprint Plan: Presentation Skill v1.1 Enhancements

**Version**: 2.0
**Date**: 2026-04-04
**Scrum Master**: Aragorn
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.0
**Architecture**: `.delivery/artifacts/04-architect/solution/architecture.md` v1.0
**Stories**: `.delivery/artifacts/05-plan/po/stories.md` (GOVERNING)
**Issues**: #43, #44, #45, #46
**Team Size**: 1 developer
**Pipeline Type**: FEATURE

---

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall. Four sprints. Eight stories. Twenty-four points. We walk the long road — at a pace that does not break us."*

---

## 1. Sprint Goal

**Deliver all 20 functional requirements across 4 enhancement groups (new types, narrative intelligence, fallback degradation, PPTX output) as additive enhancements to the presentation skill v1.1, validated through dogfooding with real pipeline artifacts.**

The fellowship carries four burdens across four sprints. We carry them in the right order, at a sustainable pace, or we do not carry them at all.

---

## 2. Capacity Declaration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Team size | 1 developer | Solo contributor |
| Sprint length | Standard sprint | Each sprint ships a cohesive group |
| Velocity baseline | 8 SP/sprint | Estimated sustainable throughput for solo developer on markdown + Python mixed work |
| Utilization ceiling | 80% = 6.4 SP | Reserve 20% for interrupts, context switching, unexpected complexity |
| Total estimated effort | 24 SP across 8 stories, 4 sprints | Aligned with PO stories.md |
| Sprint count | 4 sprints | PO-governed structure; Groups A → D → C → B |

**Per-sprint commitment verification**:

| Sprint | SP Committed | Ceiling (6.4) | Utilization | Status |
|--------|-------------|---------------|-------------|--------|
| Sprint 1 | 5 | 6.4 | 63% | PASS — 1.4 SP buffer |
| Sprint 2 | 6 | 6.4 | 75% | PASS — 0.4 SP buffer |
| Sprint 3 | 5 | 6.4 | 63% | PASS — 1.4 SP buffer |
| Sprint 4 | 8 | 8.0* | 100% | PASS — final sprint, push to ceiling per PO |

*Sprint 4 is the final sprint and may push to velocity ceiling per PO guidance. US-03 is the only code-tier story and carries the bulk.

**Estimation tiers**:
- Markdown-only edits (SKILL.md sections, reference docs): 1 SP per logical unit
- Mixed markdown + logic (type definitions with content gate rules, narrative patterns): 2-3 SP per unit
- Python script (generate_pptx.py): Code-tier, 5 SP
- Dogfooding validation: included within story estimates per PO sizing

---

## 3. Story Breakdown and Sequencing

### Sprint 1: New Type Foundations — Group A (5 SP committed, 63% utilization)

> *"The journey begins with first steps. Five types. Five pillars of a larger structure."*

---

#### US-01: Add 5 New Presentation Type Definitions (3 SP)
**Issue**: #43 | **FRs**: FR-01, FR-02, FR-03, FR-04, FR-05
**Priority**: P1 — Critical (unblocks all other stories)

| Task | File | Tier | Est |
|------|------|------|-----|
| T1.1 Add 5 type entries to SKILL.md detection table (keywords, pipeline auto-detect mappings) | `SKILL.md` | markdown | 0.5 SP |
| T1.2 Add content gate rules for each new type (required/enhancing artifacts) | `SKILL.md` | markdown+logic | 0.5 SP |
| T1.3 Add role dispatch tables for each new type in Step 3 | `SKILL.md` | markdown | 0.5 SP |
| T1.4 Add Retro Summary sensitivity filter logic to Step 4 (FR-05.4, FR-05.5, FR-05.6) | `SKILL.md` | markdown+logic | 0.5 SP |
| T1.5 Update error handling table to list all 9 types (FR-06.1, FR-06.2) | `SKILL.md` | markdown | 0.25 SP |
| T1.6 Add Product Demo `[DEMO]` placeholder conventions to Step 4 (FR-03.4, FR-03.5) | `SKILL.md` | markdown | 0.25 SP |
| T1.7 Add Onboarding default audience logic (FR-04.4) | `SKILL.md` | markdown | 0.25 SP |
| T1.8 Add 5 slide sequences to slide-structure.md | `slide-structure.md` | markdown | 0.5 SP |
| T1.9 Add 5 narrative frameworks to narrative-patterns.md with default mappings | `narrative-patterns.md` | markdown+logic | 0.5 SP |

**DoD**: All 5 types detected by keyword, content gates defined, role dispatch tables complete, slide sequences documented, narrative frameworks documented with default mappings, error message lists 9 types.

---

#### US-02: Update Error Handling and Content Gate for New Types (2 SP)
**Issue**: #43 | **FRs**: FR-06
**Priority**: P1 — Critical (completes the type definitions)
**Depends on**: US-01

| Task | File | Tier | Est |
|------|------|------|-----|
| T2.1 Verify none of the 5 new types trigger "Unknown type" error | `SKILL.md` | markdown | 0.5 SP |
| T2.2 Update error message to list all 9 supported types | `SKILL.md` | markdown | 0.5 SP |
| T2.3 Dogfood: each new type end-to-end with real artifacts (AC-07) | — | validation | 0.5 SP |
| T2.4 Dogfood: request unsupported type, verify 9-type error message (AC-03) | — | validation | 0.5 SP |

**DoD**: All 5 new types do not trigger error. Unsupported type error lists exactly 9 types. End-to-end dogfood of all 5 new types passes.

---

### Sprint 2: Narrative Intelligence — Group D (6 SP committed, 75% utilization)

> *"Now we give them judgment. The editorial mind that knows what to lead with, what to cut, and where to place the climax."*

---

#### US-07: Implement Editorial Passes (5 SP)
**Issue**: #46 | **FRs**: FR-16, FR-17, FR-18, FR-19
**Priority**: P1 — High (core differentiator for v1.1)
**Depends on**: US-01 (all types must exist)

| Task | File | Tier | Est |
|------|------|------|-----|
| T3.1 Add emphasis selection pass to SKILL.md Step 4 (FR-16) | `SKILL.md` | markdown+logic | 0.5 SP |
| T3.2 Add "no reorder" / "keep chronological" command + config toggle | `SKILL.md` | markdown | 0.25 SP |
| T3.3 Add information cutting pass to SKILL.md Step 4 (FR-17) | `SKILL.md` | markdown+logic | 0.5 SP |
| T3.4 Add "restore" command + config toggle | `SKILL.md` | markdown | 0.25 SP |
| T3.5 Add audience framing pass to SKILL.md Step 4 (FR-18) | `SKILL.md` | markdown+logic | 0.5 SP |
| T3.6 Add "Audience Framing Rules" section to narrative-patterns.md (FR-18.4) | `narrative-patterns.md` | markdown+logic | 0.5 SP |
| T3.7 Add narrative tension pass to SKILL.md Step 4 (FR-19) | `SKILL.md` | markdown+logic | 0.5 SP |
| T3.8 Add type-specific tension patterns to narrative-patterns.md | `narrative-patterns.md` | markdown | 0.5 SP |
| T3.9 Add type-specific emphasis weight modifiers to narrative-patterns.md (OQ-3) | `narrative-patterns.md` | markdown | 0.5 SP |
| T3.10 Add sensitivity filter rules to narrative-patterns.md (Retro Summary) | `narrative-patterns.md` | markdown | 0.5 SP |
| T3.11 Dogfood: 10+ slide presentation with all 4 passes visible (AC-08) | — | validation | 0.5 SP |

**DoD**: All 4 editorial passes documented in SKILL.md Step 4 with strict ordering (Emphasis > Cutting > Framing > Tension). Supporting rules in narrative-patterns.md. Config toggles for reorder and cutting. Dogfood shows measurable editorial changes.

---

#### US-08: Add Narrative Intelligence Config and Review Gate Criteria (1 SP)
**Issue**: #46 | **FRs**: FR-20
**Priority**: P2 — Medium
**Depends on**: US-07 (editorial passes must exist for review criteria to reference)

| Task | File | Tier | Est |
|------|------|------|-----|
| T4.1 Add expanded TW review criteria for narrative quality (FR-20.1) | `SKILL.md` | markdown | 0.25 SP |
| T4.2 Add expanded UX review criteria for climax positioning (FR-20.2) | `SKILL.md` | markdown | 0.25 SP |
| T4.3 Add "Narrative Cuts" and "Emphasis Order" sections to Step 6 output | `SKILL.md` | markdown | 0.25 SP |
| T4.4 Dogfood: verify Review Gate catches narrative issues (AC-03) | — | validation | 0.25 SP |

**DoD**: Review Gate has narrative quality criteria for TW and UX. Step 6 shows transparency sections. Dogfood confirms reviewers evaluate narrative quality.

---

### Sprint 3: Fallback & Progress — Group C (5 SP committed, 63% utilization)

> *"Even the wisest cannot see all ends — so we build the guardrails and the progress markers before the final push."*

---

#### US-05: Implement Light Mode and Threshold Degradation (3 SP)
**Issue**: #45 | **FRs**: FR-13, FR-14, FR-15
**Priority**: P2 — High
**Depends on**: US-01 (all types must exist for per-type thresholds)

| Task | File | Tier | Est |
|------|------|------|-----|
| T5.1 Add light mode evaluation logic before Step 3 (FR-13) | `SKILL.md` | markdown+logic | 0.5 SP |
| T5.2 Add `--full` and `--light` command flags (FR-13.3) | `SKILL.md` | markdown | 0.25 SP |
| T5.3 Add per-type threshold configuration and resolution logic (FR-14) | `SKILL.md` | markdown+logic | 0.5 SP |
| T5.4 Add degradation behavior at 75%/100% thresholds (FR-15) | `SKILL.md` | markdown+logic | 0.5 SP |
| T5.5 Add light mode + threshold interaction matrix | `SKILL.md` | markdown | 0.25 SP |
| T5.6 Add config keys to config-schema.md (light_mode, thresholds, thresholds_default) | `config-schema.md` | markdown | 0.5 SP |
| T5.7 Dogfood: light mode with simple type, verify reduced dispatch (AC-07) | — | validation | 0.5 SP |

**DoD**: Light mode evaluates correctly (auto/always/never). Threshold degradation warns at 75%, degrades at 100%. Interaction matrix documented. Config keys in schema v2.4. Dogfood confirms light mode activates.

---

#### US-06: Add Progress Indicators (2 SP)
**Issue**: #45 | **FRs**: FR-12
**Priority**: P2 — Medium
**Depends on**: None (can parallel with US-05)

| Task | File | Tier | Est |
|------|------|------|-----|
| T6.1 Add step-begin progress indicator format to each of 6 steps (FR-12) | `SKILL.md` | markdown | 0.5 SP |
| T6.2 Add step-completion summary format to each of 6 steps | `SKILL.md` | markdown | 0.5 SP |
| T6.3 Add context-specific information per step (role count, reviewer count, etc.) | `SKILL.md` | markdown | 0.5 SP |
| T6.4 Dogfood: verify all 12 indicators display (6 begin + 6 complete) (AC-03) | — | validation | 0.5 SP |

**DoD**: All 6 steps have begin and completion indicators with contextual information. Dogfood confirms all 12 indicators display.

---

### Sprint 4: PPTX Output — Group B (8 SP committed, 100% of ceiling)

> *"The last sprint. The code-tier. We forge the script that turns words into slides a stakeholder can hold in their hands."*

*Note: Sprint 4 is the final sprint and pushes to velocity ceiling (8 SP). This is acceptable per PO guidance — US-03 is the only code-tier story and carries the bulk. No sprint follows, so overrun risk is bounded.*

---

#### US-03: Implement python-pptx Generation Script (5 SP)
**Issue**: #44 | **FRs**: FR-07, FR-08, FR-09
**Priority**: P1 — High (headline feature, only code-tier story)
**Depends on**: US-07 (JSON intermediate format defined in Step 4)

| Task | File | Tier | Est |
|------|------|------|-----|
| T7.1 Create `scripts/` directory and `generate_pptx.py` skeleton with import guard (FR-07.3) | `generate_pptx.py` | code | 0.5 SP |
| T7.2 Implement JSON parsing and slide iteration | `generate_pptx.py` | code | 0.5 SP |
| T7.3 Implement slide layout mapping (title, content, metrics, comparison, CTA, timeline, architecture) (FR-08) | `generate_pptx.py` | code | 1.5 SP |
| T7.4 Implement template loading with name-first/index-fallback layout matching (FR-09) | `generate_pptx.py` | code | 1 SP |
| T7.5 Implement font and accent color application (FR-11) | `generate_pptx.py` | code | 0.5 SP |
| T7.6 Implement speaker notes population (OQ-5) | `generate_pptx.py` | code | 0.5 SP |
| T7.7 Implement CLI argument parsing (--input, --output, --template, --font, --accent-color) | `generate_pptx.py` | code | 0.5 SP |

**DoD**: Script runs standalone, produces valid `.pptx` from JSON input, handles all 7 layout types, supports template/font/color args, graceful import failure. Dogfood with 2+ types validates output opens in LibreOffice.

---

#### US-04: Add PPTX Format Config, Help Text, and Fallback (3 SP)
**Issue**: #44 | **FRs**: FR-10, FR-11
**Priority**: P2 — Medium (completes the PPTX user experience)
**Depends on**: US-03 (script must exist for format integration)

| Task | File | Tier | Est |
|------|------|------|-----|
| T8.1 Add PPTX format option to SKILL.md (format=pptx, JSON intermediate in Step 4) | `SKILL.md` | markdown+logic | 0.5 SP |
| T8.2 Add fallback-to-markdown when python-pptx missing (FR-10.4) | `SKILL.md` | markdown | 0.25 SP |
| T8.3 Add help text listing pptx as valid format | `SKILL.md` | markdown | 0.25 SP |
| T8.4 Add 3 PPTX config keys to config-schema.md (pptx_font, pptx_accent_color, pptx_template) | `config-schema.md` | markdown | 0.5 SP |
| T8.5 Bump config schema version to v2.4 (if not already bumped in Sprint 3) | `config-schema.md` | markdown | 0.25 SP |
| T8.6 Dogfood: PPTX output for 2+ types, verify opens in LibreOffice (AC-06, AC-07) | — | validation | 0.75 SP |
| T8.7 Dogfood: fallback when python-pptx missing (AC-07 TC-07.2) | — | validation | 0.5 SP |

**DoD**: PPTX is a recognized format in SKILL.md. Config keys documented. Fallback to structured-markdown works. Help text updated. Dogfood validates PPTX output and fallback behavior.

---

## 4. Dependency Graph

```
Sprint 1 (Group A):
  US-01 (Type Definitions, 3 SP)
    └──> US-02 (Error Handling, 2 SP)     [sequential]

Sprint 2 (Group D):
  US-01 ──> US-07 (Editorial Passes, 5 SP)
               └──> US-08 (Narrative Config, 1 SP)   [sequential]

Sprint 3 (Group C):
  US-01 ──> US-05 (Light Mode + Thresholds, 3 SP)
  US-06 (Progress Indicators, 2 SP)                   [parallel with US-05]

Sprint 4 (Group B):
  US-07 ──> US-03 (PPTX Script, 5 SP)
               └──> US-04 (PPTX Config, 3 SP)        [sequential]
```

**Critical path**: US-01 → US-07 → US-03 → US-04

---

## 5. Sprint Summary

| Sprint | Stories | SP Committed | Ceiling | Utilization | Buffer | Focus |
|--------|---------|-------------|---------|-------------|--------|-------|
| Sprint 1 | US-01, US-02 | 5 | 6.4 | 63% | 1.4 SP | New type foundations (Group A) |
| Sprint 2 | US-07, US-08 | 6 | 6.4 | 75% | 0.4 SP | Narrative intelligence (Group D) |
| Sprint 3 | US-05, US-06 | 5 | 6.4 | 63% | 1.4 SP | Fallback & progress (Group C) |
| Sprint 4 | US-03, US-04 | 8 | 8.0* | 100%* | 0 SP | PPTX output (Group B) |
| **Total** | **8 stories** | **24 SP** | — | — | — | **20 FRs, 8 NFRs, 4 modified files, 1 new file** |

*Sprint 4 pushes to velocity ceiling (not utilization ceiling) — acceptable as final sprint per PO guidance.

All sprints except Sprint 4 are under the 80% utilization ceiling. Sprint 4 is at 100% of velocity but is bounded by being the final sprint with no subsequent sprints at risk.

---

## 6. Definition of Done

A story is DONE when ALL of the following are true:

| # | Criterion |
|---|-----------|
| DoD-1 | All tasks in the story are complete |
| DoD-2 | All acceptance criteria from the PRD for the story's FRs are met |
| DoD-3 | Modified files are syntactically valid (markdown renders, Python runs) |
| DoD-4 | No regression: existing 4 types and 3 formats function identically |
| DoD-5 | New config keys have defaults; skill works without config changes |
| DoD-6 | Dogfooding tasks within the story pass |

The plan is DONE when:
- All 8 stories meet their individual DoD
- All 5 new types produce complete presentations from real artifacts (NFR-07)
- PPTX output opens without error (NFR-08)
- Config schema is at v2.4 (NFR-06)
- Plugin structure compliance verified (NFR-05)

---

## 7. Risk Assessment

| # | Risk | Impact | Likelihood | Mitigation | Sprint |
|---|------|--------|-----------|------------|--------|
| R1 | Narrative editorial passes interact in unexpected ways during dogfooding | Medium | Medium | Sequential pass design (ADR-02) isolates each pass. Config toggles allow disabling individual passes. Sprint 2 has 0.4 SP buffer + Sprint 3 buffer absorbs any bleed. | Sprint 2 |
| R2 | python-pptx layout matching fails on non-standard templates | Low | High | Name-first/index-fallback strategy (FR-09.3). Dogfood with default + custom template. Accept "good enough to edit." | Sprint 4 |
| R3 | Scope creep from dogfooding discoveries | Medium | Medium | Dogfooding is validation, not feature discovery. Issues found during dogfooding are logged as follow-up issues, not added to the sprint. | All |
| R4 | Sprint 4 at 100% leaves no buffer for code-tier surprises | High | Medium | US-03 tasks are well-decomposed (7 tasks, largest is 1.5 SP). Template matching (T7.4) is the highest-risk task — if it overruns, speaker notes (T7.6) can be deferred to a follow-up. | Sprint 4 |
| R5 | Single-developer bus factor | High | Low | All work is in-repo with PRD + architecture docs. Any developer can pick up from artifacts. | All |
| R6 | 5 new narrative frameworks are internally inconsistent | Medium | Low | Frameworks are authored against existing patterns in narrative-patterns.md. US-01 includes cross-reference verification. | Sprint 1 |

---

## 8. Delivery Sequence Rationale

The PO's delivery sequence (Group A → D → C → B) is adopted directly:

1. **Sprint 1 (Group A)** — Type definitions unblock everything. After Sprint 1, all 9 types are functional. Dogfooding of new types begins immediately.

2. **Sprint 2 (Group D)** — Narrative intelligence applies to all 9 types including the new ones from Sprint 1. Delivers the core v1.1 differentiator early.

3. **Sprint 3 (Group C)** — Fallback and progress features require types to exist (Sprint 1) and benefit from narrative intelligence being stable (Sprint 2). Comfortable 63% utilization provides recovery space if Sprint 2 bled.

4. **Sprint 4 (Group B)** — PPTX is an independent output path that consumes the composed output from all prior sprints. Validated last because it depends on all types and narrative intelligence being stable. At ceiling, but bounded as the final sprint.

This matches the PRD Section 11 recommended ordering.

---

## 9. File Impact Summary

| File | Stories | Change Type |
|------|---------|------------|
| `delivery-team/skills/presentation/SKILL.md` | US-01, US-02, US-04, US-05, US-06, US-07, US-08 | Major modification (all groups) |
| `delivery-team/skills/presentation/references/narrative-patterns.md` | US-01, US-07 | Major modification (frameworks + rules) |
| `delivery-team/skills/presentation/references/slide-structure.md` | US-01 | Moderate modification (5 new sections) |
| `delivery-team/skills/presentation/scripts/generate_pptx.py` | US-03 | New file (Python, code-tier) |
| `delivery-flow/references/config-schema.md` | US-04, US-05 | Minor modification (6-8 keys, version bump) |

---

## 10. Correction Log

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| v1.0 | 2026-04-04 | Initial 2-sprint plan | Original draft |
| v2.0 | 2026-04-04 | Rewritten to 4-sprint plan aligned with PO stories.md | DoD review rejected v1.0: Sprint 2 at 100% ceiling (0 buffer), plan divergence from PO's 4-sprint / 24 SP structure. Adopted PO's sprint assignments and SP totals as governing plan. |

---

> *"There is always hope. But hope is not a sprint plan. A sprint plan has stories, dependencies, and a Definition of Done. Four sprints, not two. Twenty-four points, not thirty-one. We walk the long road at a pace the fellowship can sustain — with buffers for the unexpected and a final push that is earned, not reckless."*

---

*Planned by Scrum Master (Aragorn) — delivery-team:product-delivery*
