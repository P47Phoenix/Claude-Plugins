# Sprint Plan: Fix Alias Theme Not Injected into Agent Prompts (Issue #58)

**Project Type**: BUG_FIX (light mode)
**Date**: 2026-04-04
**GitHub Issue**: #58
**Inputs**: Idea Brief v1.0

---

## Sprint Goal

Ensure every agent dispatched by the orchestrator -- primary, supporting, and DoD validator -- receives the `--- ALIAS ---` block when an alias theme is active, by adding a standardized Agent Invocation Template to `pipeline-stages.md`.

---

## Capacity Declaration

| Metric | Value |
|--------|-------|
| Velocity baseline | 8 pts/sprint |
| 80% ceiling | 6 pts |
| Committed this sprint | 2 pts |
| Buffer | 4 pts (conservative; markdown-only change) |

> **Calibration note**: This is a markdown-only edit to `pipeline-stages.md`. Per team convention, markdown-only estimates are one tier lower than code changes. A comparable code fix would be 3 pts; this is 2 pts.

---

## Story: Add Alias Injection Template to Pipeline Stages

**ID**: BUG-58
**Points**: 2
**Priority**: P1

### User Story

**As a** delivery-team user who has configured an alias theme (e.g., `aliases.theme: lotr`),
**I want** every agent the orchestrator dispatches to receive the `--- ALIAS ---` personality block in its prompt,
**So that** the configured personality is consistently applied across the entire pipeline run, not just a handful of agents.

### Acceptance Criteria

#### AC-1: Primary agent dispatch includes alias block

**Given** a user has configured `aliases.theme: lotr` and `personality_strength: full` in `.delivery/config.yml`
**When** the orchestrator dispatches a primary agent for any pipeline stage
**Then** the agent prompt includes an `--- ALIAS ---` block matching the configured theme and personality strength

#### AC-2: Supporting agent dispatch includes alias block

**Given** an active alias theme is configured
**When** the orchestrator dispatches a supporting agent (e.g., secondary research, analysis, or review agents)
**Then** the agent prompt includes the `--- ALIAS ---` block

#### AC-3: DoD validator dispatch includes alias block

**Given** an active alias theme is configured
**When** the orchestrator dispatches DoD validator agents
**Then** the validator prompt includes the `--- ALIAS ---` block

#### AC-4: Template references personality_strength protocol

**Given** the Agent Invocation Template has been added to `pipeline-stages.md`
**When** the template's alias block is reviewed
**Then** it references the `personality_strength` protocol from SKILL.md Phase 4 Step 4, supporting light, moderate, and full levels

#### AC-5: Dogfooding validation

**Given** a BUG_FIX pipeline run with `aliases.theme: lotr` and `personality_strength: full`
**When** the pipeline executes from start to finish
**Then** all dispatched agents display LOTR personality consistent with the theme

---

### Test Cases

#### TC-1: Primary agent alias injection (covers AC-1)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Configure `aliases.theme: lotr`, `personality_strength: full` | Config accepted |
| 2 | Start a pipeline run; observe the first primary agent dispatch | Agent prompt contains `--- ALIAS ---` block |
| 3 | Grep `pipeline-stages.md` for `--- ALIAS ---` in primary agent template | Match found in primary agent invocation template |
| 4 | Verify alias block content | Block includes role name, style, catchphrase, and examples per LOTR theme |

#### TC-2: Supporting agent alias injection (covers AC-2)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | With active theme, trigger a stage that dispatches supporting agents | Supporting agents are dispatched |
| 2 | Inspect the supporting agent prompt | Prompt contains `--- ALIAS ---` block |
| 3 | Grep `pipeline-stages.md` for `--- ALIAS ---` in supporting agent template | Match found in supporting agent invocation template |

#### TC-3: DoD validator alias injection (covers AC-3)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | With active theme, reach a DoD validation point | DoD validators are dispatched |
| 2 | Inspect the DoD validator prompt | Prompt contains `--- ALIAS ---` block |
| 3 | Grep `pipeline-stages.md` for `--- ALIAS ---` in validator template | Match found in validator invocation template |

#### TC-4: Personality strength protocol reference (covers AC-4)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `pipeline-stages.md` Agent Invocation Template | Template is present |
| 2 | Review alias block instructions | Block references SKILL.md Phase 4 Step 4 personality_strength protocol |
| 3 | Verify light/moderate/full levels are documented | All three levels described or referenced |

#### TC-5: Dogfooding -- full pipeline with LOTR theme (covers AC-5)

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run this BUG_FIX pipeline with `aliases.theme: lotr`, `personality_strength: full` | Pipeline starts with LOTR theme loaded in Phase 0 |
| 2 | Monitor each dispatched agent (primary, supporting, validator) | Every agent speaks in LOTR personality |
| 3 | Check for agents reverting to default professional tone | Zero agents use default tone when theme is active |
| 4 | Confirm personality includes role name, style, catchphrase, and examples | Full personality_strength contract met |

---

### Implementation Scope

All changes target `delivery-team/delivery-flow/references/pipeline-stages.md`:

1. **Agent Invocation Template** -- Add a standardized template section that all agent dispatches (primary, supporting, validator) must follow, including the `--- ALIAS ---` placeholder block
2. **Alias block structure** -- Mirror the pattern already established in `team-patterns.md` collaboration templates
3. **Personality strength reference** -- Include a reference to SKILL.md Phase 4 Step 4 so the orchestrator applies the correct level (light/moderate/full)

### Test Approach

- **Structural verification** (TC-1 through TC-4): Grep-based confirmation that `--- ALIAS ---` blocks exist in all three dispatch template types within `pipeline-stages.md`
- **Behavioral verification** (TC-5): Dogfooding via live pipeline execution with an active LOTR theme at full personality strength

### Definition of Done

- [ ] All 5 acceptance criteria verified via test cases
- [ ] Dogfooding gate passed (TC-5)
- [ ] Template aligns with existing `--- ALIAS ---` pattern in `team-patterns.md`
- [ ] No regression in pipeline behavior for runs without an alias theme

---

## Sprint Summary

| Item | Detail |
|------|--------|
| Sprint goal | Fix alias injection across all agent dispatch types in pipeline-stages.md (issue #58) |
| Stories committed | 1 (BUG-58: 2 pts) |
| Capacity used | 2 / 6 pts (33%) |
| Risk | Low -- markdown-only change to a single file; pattern already proven in team-patterns.md |
| Validation gate | Dogfooding with LOTR theme at full personality strength (P0) |
