# User Stories: Orchestrator Theme Surfacing

**Version**: 1.0
**Date**: 2026-04-04
**Author**: Product Owner (Gandalf)
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.0
**Source Issue**: #59
**Scope**: `delivery-team/skills/delivery-flow/SKILL.md` (single file)

---

> *"A wizard's voice is not a decoration — it is a signal. When the theme speaks through every agent yet the orchestrator remains silent, the Fellowship hears a gap where continuity should be."*

---

## US-01: Orchestrator Theme Surfacing

**As a** delivery pipeline user with a non-business alias theme configured,
**I want** the orchestrator to surface the active theme's personality in stage announcements, checkpoint summaries, and stage transitions — while preserving neutral output for the `business` theme and keeping internal routing personality-free,
**So that** the themed experience feels woven through the entire pipeline interaction, not just buried in artifact files I must open separately.

**Issue**: #59
**FRs Covered**: FR-01, FR-02, FR-03, FR-04, FR-05
**Tier**: Markdown-only (SKILL.md edits)
**Story Points**: 5

---

### Acceptance Criteria

#### Group A: Theme-Gated Reporting Protocol

| AC | Criterion | FR |
|----|-----------|-----|
| AC-01 | **Given** `aliases.theme` is set to a non-business theme (e.g., `lotr`), **When** the orchestrator announces a stage that dispatches a primary agent, **Then** the stage header references the agent's character name from the theme's `roles` map (e.g., "Gandalf shall examine the product requirements" instead of "Product Owner will refine requirements"). | FR-01.1 |
| AC-02 | **Given** `aliases.theme` is set to a non-business theme, **When** the orchestrator announces a stage, **Then** the announcement carries the theme's voice in its phrasing (thematic vocabulary, tone consistent with the theme's `personality_strength`). | FR-01.2 |
| AC-03 | **Given** `aliases.theme` is `business` or unset, **When** the orchestrator announces a stage, **Then** the announcement uses the current neutral format: `## Stage [N]: [NAME]\nPurpose: [one-line description]` with no character names or thematic language. | FR-01.3 |
| AC-04 | **Given** a non-business theme where the primary agent's role has no entry in the theme's `roles` map (partial theme), **When** the orchestrator announces that stage, **Then** it falls back to the neutral announcement format for that stage only. | FR-01.4 |
| AC-05 | **Given** a non-business theme is active and a stage reaches a human checkpoint, **When** the orchestrator presents the checkpoint summary, **Then** it includes at least one brief quoted line (max 280 characters) from the primary agent's artifact that demonstrates the agent's themed voice. | FR-02.1 |
| AC-06 | **Given** a non-business theme is active and a stage reaches a human checkpoint, **When** the orchestrator reads the primary agent's artifact to extract a quote, **Then** it reads ONLY to select a representative quote — it does NOT paste artifact content into downstream agent prompts. The two-channel rule is preserved. | FR-02.2 |
| AC-07 | **Given** `aliases.theme` is `business` or unset, **When** the orchestrator presents a checkpoint summary, **Then** no artifact quotes are included — the summary remains a neutral status report. | FR-02.3 |
| AC-08 | **Given** a non-business theme is active but the primary agent's artifact contains no clearly themed language, **When** the orchestrator prepares the checkpoint summary, **Then** it omits the quote rather than quoting neutral prose, and presents the standard summary format. | FR-02.4 |
| AC-09 | **Given** a non-business theme is active, **When** the orchestrator advances from one stage to the next (Step 10), **Then** the STATE ANCHOR message carries thematic voice (e.g., "The Fellowship advances to the Architect stage. Gandalf's counsel is complete. Gimli prepares to build."). | FR-03.1 |
| AC-10 | **Given** a non-business theme is active, **When** the orchestrator emits a transition message, **Then** the essential routing information (stage number, stage name, continuation directive) is still present within the themed message — personality augments, it does not replace, the routing signal. | FR-03.2 |
| AC-11 | **Given** `aliases.theme` is `business` or unset, **When** the orchestrator advances between stages, **Then** the STATE ANCHOR message uses the current neutral format. | FR-03.3 |

#### Group B: Orchestrator Neutrality Preservation

| AC | Criterion | FR |
|----|-----------|-----|
| AC-12 | **Given** any theme (business or non-business), **When** the orchestrator writes to `.delivery/state.md`, **Then** the state file contains no themed language — only structured routing data (stage numbers, artifact paths, timestamps). | FR-04.1 |
| AC-13 | **Given** any theme, **When** the orchestrator writes `stage-summary.md`, **Then** the summary contains agent signals (STATUS, ARTIFACT, SUMMARY) with no themed embellishment. | FR-04.2 |
| AC-14 | **Given** any theme, **When** the orchestrator constructs an Agent Invocation Template for a downstream agent, **Then** the template's INPUT ARTIFACTS section contains only file paths — no quoted content from upstream artifacts, themed or otherwise. | FR-04.3 |
| AC-15 | **Given** any theme, **When** the orchestrator dispatches DoD validators (Step 7), **Then** validator prompts contain no themed language. Validators evaluate quality, not character consistency. | FR-04.4 |
| AC-16 | **Given** any theme, **When** a sub-agent responds to an invocation, **Then** the signal block format remains: `STATUS: {DONE | NOT_DONE | CODE_COMPLETE}\nARTIFACT: {path}\nSUMMARY: {text}` with no themed additions. | FR-05.1 |
| AC-17 | **Given** a non-business theme is active, **When** the orchestrator verifies an agent signal (Step 4 post-response), **Then** it checks for `SKILL_LOADED` and extracts STATUS/ARTIFACT/SUMMARY using the same parsing logic as today — themed content in the agent's response body does not interfere with signal extraction. | FR-05.2 |

---

### Test Cases

#### Group A: Theme-Gated Reporting Protocol

| TC | Covers AC | Test | Expected Result |
|----|-----------|------|-----------------|
| TC-01 | AC-01, AC-02 | Configure `aliases.theme: lotr` in `.delivery/config.yml`. Run pipeline through Stage 2 (Refine). Inspect the stage announcement output in the chat transcript. | Stage header references "Gandalf" (or the mapped character name for the PO role) and uses thematic vocabulary (e.g., counsel, fellowship, journey). |
| TC-02 | AC-03 | Configure `aliases.theme: business` (or leave unset). Run pipeline through Stage 2. Inspect stage announcement. | Stage header reads `## Stage 2: Refine\nPurpose: [description]` with no character names or themed language. Output identical to pre-feature behavior. |
| TC-03 | AC-04 | Create a custom theme YAML that maps only 3 of 7 roles (omitting the role dispatched at Stage 4). Run pipeline through Stage 4. | Stages with mapped roles show themed announcements. Stage 4 (unmapped role) falls back to neutral format. No errors or crashes. |
| TC-04 | AC-05, AC-06 | Configure `aliases.theme: lotr`. Run pipeline to a human checkpoint (e.g., post-Refine). Inspect checkpoint summary in chat output. | Summary includes a quoted line (max 280 chars) from the PO agent's artifact that demonstrates themed voice. No artifact content appears in any subsequent agent invocation template. |
| TC-05 | AC-07 | Configure `aliases.theme: business`. Run pipeline to a human checkpoint. Inspect checkpoint summary. | Summary is a neutral status report with no artifact quotes. Identical to pre-feature behavior. |
| TC-06 | AC-08 | Configure a non-business theme. Manually ensure the primary agent's artifact contains only neutral prose (no character names, no themed language). Run to checkpoint. | Checkpoint summary omits the quote section and presents the standard summary format. No neutral prose is quoted. |
| TC-07 | AC-09, AC-10 | Configure `aliases.theme: lotr`. Run pipeline from Stage 2 to Stage 3. Inspect the transition/STATE ANCHOR message. | Transition carries thematic voice AND includes stage number, stage name, and continuation directive. Both personality and routing data are present. |
| TC-08 | AC-11 | Configure `aliases.theme: business`. Run pipeline from Stage 2 to Stage 3. Inspect transition message. | STATE ANCHOR uses current neutral format. Identical to pre-feature behavior. |

#### Group B: Orchestrator Neutrality Preservation

| TC | Covers AC | Test | Expected Result |
|----|-----------|------|-----------------|
| TC-09 | AC-12 | Configure `aliases.theme: lotr`. Run pipeline through 2+ stages. Inspect `.delivery/state.md`. | State file contains only structured routing data (stage numbers, artifact paths, timestamps). Zero themed language. |
| TC-10 | AC-13 | Configure `aliases.theme: lotr`. Complete a stage. Inspect `stage-summary.md`. | Summary contains agent signals (STATUS, ARTIFACT, SUMMARY) with no themed embellishment. |
| TC-11 | AC-14 | Configure `aliases.theme: lotr`. Run pipeline. Inspect the Agent Invocation Template dispatched to the Stage 3 agent. | INPUT ARTIFACTS section contains only file paths. No quoted content from Stage 2's artifact. |
| TC-12 | AC-15 | Configure `aliases.theme: lotr`. Reach a DoD validation step. Inspect validator prompts. | Validator prompts contain quality criteria only. No themed language, character names, or personality injection. |
| TC-13 | AC-16 | Configure `aliases.theme: lotr`. Complete a stage. Inspect the sub-agent's signal block. | Signal block is exactly `STATUS: {value}\nARTIFACT: {path}\nSUMMARY: {text}`. No themed additions to the signal format. |
| TC-14 | AC-17 | Configure `aliases.theme: lotr`. Complete a stage where the agent writes heavily themed content in the response body (around the signal block). Inspect orchestrator's signal extraction. | Orchestrator correctly extracts STATUS, ARTIFACT, and SUMMARY values. Themed content in the response body does not interfere with parsing. |

---

### Task Breakdown

| Task | Description | Tier | Est |
|------|-------------|------|-----|
| T-01 | Add "Theme-Gated Reporting Protocol" sub-section to Phase 4 of SKILL.md with theme detection guard (`aliases.theme != business`) | Markdown | 0.5 SP |
| T-02 | Add theme-aware stage announcement logic to Step 1 (conditional block: if non-business theme, reference character name from `roles` map, apply thematic voice; else use neutral format) | Markdown | 0.5 SP |
| T-03 | Add partial-theme fallback rule: if role has no entry in theme's `roles` map, fall back to neutral announcement for that stage | Markdown | 0.25 SP |
| T-04 | Add theme-aware checkpoint summary logic to Step 9 (read primary agent artifact, select representative themed quote max 280 chars, include in checkpoint output; omit if no themed language found) | Markdown | 0.75 SP |
| T-05 | Add two-channel enforcement clause: quote extraction is for user-facing output only, never forwarded to downstream agent prompts | Markdown | 0.25 SP |
| T-06 | Add theme-aware transition logic to Step 10 (STATE ANCHOR carries thematic voice while preserving routing signals: stage number, name, continuation directive) | Markdown | 0.5 SP |
| T-07 | Add explicit neutrality preservation rules for internal routing (state.md, stage-summary.md, Agent Invocation Templates, DoD validator prompts) | Markdown | 0.5 SP |
| T-08 | Add signal block format invariance rule (signal format unchanged regardless of theme; extraction logic unchanged) | Markdown | 0.25 SP |
| T-09 | Dogfood: run pipeline end-to-end with `lotr` theme, verify all 3 themed output slots (announcements, checkpoints, transitions) carry theme voice | Validation | 0.75 SP |
| T-10 | Dogfood: run pipeline with `business` theme, verify zero behavior change vs. pre-feature baseline | Validation | 0.5 SP |
| T-11 | Dogfood: run pipeline with partial custom theme (missing roles), verify graceful fallback to neutral | Validation | 0.25 SP |
| **Total** | | | **5 SP** |

---

### Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| `aliases.theme` config key | Existing | In config schema v2.3 |
| Phase 0 theme loading (roles map, personality_strength) | Existing | Already loads at pipeline init |
| Two-channel communication protocol | Existing | Preserved, not modified |
| Theme YAML files in `references/aliases/` | Existing | 13 built-in themes available |

---

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Themed STATE ANCHOR confuses downstream routing | Low | High | AC-10 requires routing signals always present. TC-07 validates both personality and routing data coexist. |
| Quote extraction leaks content to downstream agents | Low | High | AC-06/AC-14 explicitly prohibit it. TC-11 validates agent templates contain only paths. |
| Custom themes with unusual voice break readability | Low | Medium | AC-04 provides fallback to neutral. TC-03 validates partial theme graceful degradation. |

---

> *"One story. Five requirements. Seventeen acceptance criteria. Fourteen test cases. The path is clear, the burden is light, and the single file we must touch is well-known to us. Let us walk it wisely."*

---

*Written by Product Owner (Gandalf) — delivery-team:product-delivery*
