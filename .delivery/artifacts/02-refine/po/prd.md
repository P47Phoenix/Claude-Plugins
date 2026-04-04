# PRD: Orchestrator Theme Surfacing

**Version**: 1.0
**Date**: 2026-04-04
**Author**: Product Owner (Gandalf)
**Status**: DRAFT
**Project Type**: FEATURE
**Pipeline Routing**: Idea > Refine > Design > Architect > Plan > Development > UAT
**Source Issue**: #59 (P47Phoenix/Claude-Plugins)
**Skill Under Enhancement**: `delivery-team/skills/delivery-flow/`

---

> *"All we have to decide is what to surface with the voice that is given to us."*

The delivery-flow orchestrator injects alias theme personality into every sub-agent it dispatches -- Gandalf counsels on priorities, Gimli writes code with dwarven directness, Aragorn rallies the standup. The agents honor the theme in their artifacts. But the orchestrator itself, the user's primary interface to the pipeline, speaks in clinical monotone regardless of theme. Stage announcements, checkpoint summaries, and transition messages carry no trace of the personality the user configured. The theme feels bolted on rather than woven through.

This PRD adds a theme-gated reporting protocol to the orchestrator. When `aliases.theme` is not `business`, the orchestrator adapts its user-facing chat output to reflect the active theme -- referencing character names, quoting memorable lines from agent artifacts, and carrying thematic flavor in transitions. When `aliases.theme` is `business` (or unset), behavior is identical to today. The two-channel communication architecture is preserved: personality surfaces only in user-facing output, never in inter-agent routing.

**Scope**: `delivery-team/skills/delivery-flow/SKILL.md` only. No config changes. No new files.

---

## 1. Goals

| # | Goal | Measurable Target | Baseline | Measurement |
|---|------|-------------------|----------|-------------|
| G-01 | Orchestrator surfaces theme personality in user-facing chat output | Stage headers, checkpoint summaries, and transitions reference character names and carry thematic voice when a non-business theme is active | Orchestrator output is personality-free regardless of theme | Dogfooding: run pipeline with `lotr` theme and verify orchestrator output carries theme voice |
| G-02 | Agent voice is quoted at human checkpoints | Checkpoint summaries include at least one quoted or paraphrased line from the primary agent's artifact | Checkpoint summaries are neutral prose | Visual inspection at each of the 4 human checkpoints during dogfooding |
| G-03 | Business theme produces zero behavior change | When `aliases.theme` is `business` or unset, all orchestrator output is identical to current behavior | Current behavior | Dogfooding: run pipeline with `business` theme and diff output against a pre-feature baseline |
| G-04 | Two-channel architecture preserved | No artifact content flows through orchestrator to downstream agents; personality appears only in user-facing chat | Two-channel rule enforced | Code review of SKILL.md changes confirms no inter-agent content forwarding |

---

## 2. User Personas

| Persona | Role | Primary Need | Relevant Goals |
|---------|------|-------------|----------------|
| **Aria** | Solo developer using `lotr` theme | Wants the full Middle-earth experience when running the pipeline -- not just in files she opens, but in the chat output she reads in real time | G-01, G-02 |
| **Dev team lead** | Team using `star-wars` theme for engagement | Wants checkpoint summaries to feel like mission briefings, not corporate memos, so the team stays engaged during long pipeline runs | G-01, G-02 |
| **Enterprise user** | Corporate team using `business` theme | Wants professional, personality-free output -- no regressions from a feature they did not opt into | G-03 |

---

## 3. Functional Requirements

### Group A: Theme-Gated Reporting Protocol

#### FR-01: Theme-Aware Stage Announcements

The orchestrator shall adapt its Stage Announcement output (Phase 4 Step 1) to reference the active theme's character names and voice when a non-business alias theme is configured.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-01.1 | **Given** `aliases.theme` is set to a non-business theme (e.g., `lotr`), **When** the orchestrator announces a stage that dispatches a primary agent, **Then** the stage header references the agent's character name from the theme's `roles` map (e.g., "Gandalf shall examine the product requirements" instead of "Product Owner will refine requirements"). |
| FR-01.2 | **Given** `aliases.theme` is set to a non-business theme, **When** the orchestrator announces a stage, **Then** the announcement carries the theme's voice in its phrasing (e.g., thematic vocabulary, tone consistent with the theme's `personality_strength`). |
| FR-01.3 | **Given** `aliases.theme` is `business` or unset, **When** the orchestrator announces a stage, **Then** the announcement uses the current neutral format: `## Stage [N]: [NAME]\nPurpose: [one-line description]` with no character names or thematic language. |
| FR-01.4 | **Given** a non-business theme where the primary agent's role has no entry in the theme's `roles` map (partial theme), **When** the orchestrator announces that stage, **Then** it falls back to the neutral announcement format for that stage only. |

#### FR-02: Theme-Aware Checkpoint Summaries

The orchestrator shall include quoted or paraphrased lines from the primary agent's artifact in human checkpoint summaries when a non-business theme is active.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-02.1 | **Given** a non-business theme is active and a stage reaches a human checkpoint, **When** the orchestrator presents the checkpoint summary, **Then** it includes at least one brief quoted line (max 280 characters) from the primary agent's artifact that demonstrates the agent's themed voice. |
| FR-02.2 | **Given** a non-business theme is active and a stage reaches a human checkpoint, **When** the orchestrator reads the primary agent's artifact to extract a quote, **Then** it reads ONLY to select a representative quote -- it does NOT paste artifact content into downstream agent prompts. The two-channel rule is preserved. |
| FR-02.3 | **Given** `aliases.theme` is `business` or unset, **When** the orchestrator presents a checkpoint summary, **Then** no artifact quotes are included -- the summary remains a neutral status report. |
| FR-02.4 | **Given** a non-business theme is active but the primary agent's artifact contains no clearly themed language (e.g., the agent did not stay in character), **When** the orchestrator prepares the checkpoint summary, **Then** it omits the quote rather than quoting neutral prose and presents the standard summary format. |

#### FR-03: Theme-Aware Stage Transitions

The orchestrator shall carry thematic flavor in its transition messages between stages when a non-business alias theme is active.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-03.1 | **Given** a non-business theme is active, **When** the orchestrator advances from one stage to the next (Step 10), **Then** the STATE ANCHOR message carries thematic voice (e.g., "The Fellowship advances to the Architect stage. Gandalf's counsel is complete. Gimli prepares to build." instead of "Entering Stage 4: Architect. Previous stage 3 complete. CONTINUING pipeline protocol from Step 1."). |
| FR-03.2 | **Given** a non-business theme is active, **When** the orchestrator emits a transition message, **Then** the essential routing information (stage number, stage name, continuation directive) is still present within the themed message -- personality augments, it does not replace, the routing signal. |
| FR-03.3 | **Given** `aliases.theme` is `business` or unset, **When** the orchestrator advances between stages, **Then** the STATE ANCHOR message uses the current neutral format. |

### Group B: Orchestrator Neutrality Preservation

#### FR-04: Internal Routing Remains Personality-Free

The orchestrator's internal logic shall remain unaffected by theme configuration.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-04.1 | **Given** any theme (business or non-business), **When** the orchestrator writes to `.delivery/state.md`, **Then** the state file contains no themed language -- only structured routing data (stage numbers, artifact paths, timestamps). |
| FR-04.2 | **Given** any theme, **When** the orchestrator writes `stage-summary.md`, **Then** the summary contains agent signals (STATUS, ARTIFACT, SUMMARY) with no themed embellishment. |
| FR-04.3 | **Given** any theme, **When** the orchestrator constructs an Agent Invocation Template for a downstream agent, **Then** the template's INPUT ARTIFACTS section contains only file paths -- no quoted content from upstream artifacts, themed or otherwise. |
| FR-04.4 | **Given** any theme, **When** the orchestrator dispatches DoD validators (Step 7), **Then** validator prompts contain no themed language. Validators evaluate quality, not character consistency. |

#### FR-05: Signal Block Format Unchanged

The agent signal block format shall remain unchanged regardless of theme.

**Acceptance Criteria:**

| AC | Criterion |
|----|-----------|
| FR-05.1 | **Given** any theme, **When** a sub-agent responds to an invocation, **Then** the signal block format remains: `STATUS: {DONE | NOT_DONE | CODE_COMPLETE}\nARTIFACT: {path}\nSUMMARY: {text}` with no themed additions. |
| FR-05.2 | **Given** a non-business theme is active, **When** the orchestrator verifies an agent signal (Step 4 post-response), **Then** it checks for `SKILL_LOADED` and extracts STATUS/ARTIFACT/SUMMARY using the same parsing logic as today -- themed content in the agent's response body does not interfere with signal extraction. |

---

## 4. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR-01 | Orchestrator performance | Theme surfacing adds no additional agent invocations. The only new I/O is a single read of the primary agent's artifact at checkpoint time to extract a quote. |
| NFR-02 | Theme fallback resilience | If a theme file is malformed or missing a role, the orchestrator falls back to neutral output for that specific instance -- never crashes or stalls the pipeline. |
| NFR-03 | Maintainability | Theme surfacing logic is contained in a single clearly-demarcated section of SKILL.md. New themes added to `references/aliases/` require zero SKILL.md changes to surface correctly. |

---

## 5. Success Metrics

| Metric | Target | How Measured |
|--------|--------|-------------|
| Theme voice presence in orchestrator output | 100% of stage headers, transitions, and checkpoint summaries carry themed voice when non-business theme is active | Manual review of pipeline run transcript |
| Checkpoint quote rate | At least 1 quoted line at each of the 4 human checkpoints | Count quotes in checkpoint output |
| Business theme regression | Zero output differences when theme is `business` | Diff test: run pipeline with `business` theme before and after change |
| Two-channel compliance | Zero instances of artifact content in downstream agent prompts | Code review + runtime audit during dogfooding |
| Pipeline completion rate | No increase in pipeline failures attributable to theme surfacing | Compare failure rates pre/post feature |

---

## 6. Scope

### In Scope

- **SKILL.md modifications only**: Add theme-gated reporting protocol as a sub-section in Phase 4
- **Stage announcements** (Step 1): Theme-aware phrasing with character names
- **Checkpoint summaries** (Step 9): Quoted agent voice lines
- **Transition messages** (Step 10): Themed STATE ANCHOR messages
- **Business theme guard**: All new behavior gated on `aliases.theme != business`
- **Partial theme fallback**: Graceful degradation when a role has no theme entry

### Out of Scope

- Config schema changes (no new keys needed)
- Changes to agent invocation templates or the ALIAS block
- Changes to the two-channel communication architecture
- Theme-aware validator prompts or DoD gate criteria
- New alias themes
- Changes to any skill other than delivery-flow
- Changes to any file other than `delivery-team/skills/delivery-flow/SKILL.md`

---

## 7. User Stories

### US-01: Themed Stage Experience
**As a** delivery pipeline user with a non-business alias theme configured,
**I want** the orchestrator to reference agent character names and carry thematic voice in stage announcements,
**So that** the themed experience feels woven through the entire pipeline, not just buried in artifact files.

### US-02: Agent Voice at Checkpoints
**As a** delivery pipeline user reviewing an artifact at a human checkpoint,
**I want** the orchestrator to quote a memorable line from the agent's artifact in the checkpoint summary,
**So that** I get a taste of the agent's themed personality without having to open the full artifact file.

### US-03: Themed Transitions
**As a** delivery pipeline user watching stages advance,
**I want** stage transition messages to carry thematic flavor while preserving routing information,
**So that** the pipeline feels like a narrative journey, not a checklist.

### US-04: Business Theme Unchanged
**As a** delivery pipeline user with the default `business` theme,
**I want** orchestrator output to remain exactly as it is today,
**So that** I experience no regressions from a feature I did not opt into.

### US-05: Partial Theme Graceful Degradation
**As a** delivery pipeline user with a custom theme that only covers some roles,
**I want** stages with unmapped roles to fall back to neutral announcements,
**So that** the pipeline never crashes or produces garbled output from a missing theme entry.

---

## 8. Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| `aliases.theme` config key | Existing | Already in config schema v2.3 |
| `aliases.custom_path` config key | Existing | Already in config schema v2.3 |
| Theme YAML files in `references/aliases/` | Existing | 13 built-in themes + custom path support |
| Phase 0 theme loading logic | Existing | Already loads and stores `roles` mapping and `personality_strength` |
| Two-channel communication protocol | Existing | Preserved, not modified |

---

## 9. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Themed output confuses routing -- downstream agents misparse themed STATE ANCHOR | Low | High | FR-03.2 ensures routing signals (stage number, name, continuation directive) are always present within themed messages. Signal extraction uses structured markers, not free text. |
| Quote extraction violates two-channel rule by forwarding content to agents | Low | High | FR-02.2 explicitly scopes quote reading to user-facing checkpoint output only. FR-04.3 confirms agent prompts contain only paths. |
| Themed output becomes verbose, slowing pipeline perception | Medium | Low | Theme surfacing adds flavor to existing output slots (headers, transitions, checkpoints) -- it does not add new output blocks. NFR-01 confirms no new agent invocations. |
| Custom themes with unusual voice break orchestrator readability | Low | Medium | NFR-02 requires fallback to neutral on malformed or missing role entries. Personality is additive, never replacing structured routing data. |

---

## 10. Implementation Notes

This section is guidance for the Design and Architect stages, not prescriptive implementation.

**Where to add in SKILL.md:**
- The theme-gated reporting protocol should be a new sub-section within Phase 4, between "Two-Channel Communication" (current location around line 288) and "Plan-Mode Delegation" (around line 297), or as a companion to the Step 1/Step 9/Step 10 definitions.
- Alternatively, each affected step (Step 1, Step 9, Step 10) could have a conditional block: "If non-business theme is active, adapt output as follows..."

**Quote extraction at checkpoints:**
- The orchestrator already verifies artifact existence in Step 8. At Step 9 (checkpoint), it can read the artifact to select a representative themed quote. This is a narrow, bounded read -- not a violation of the two-channel rule, which prohibits forwarding artifact content to other agents.
- The quote should be selected based on presence of the character's name, catchphrase keywords, or strong thematic vocabulary. If no clearly themed line is found, omit the quote.

**Theme data already available:**
- Phase 0 already loads and stores the theme's `roles` map and `personality_strength`. The orchestrator has character names, personalities, styles, and catchphrases available in memory from pipeline initialization. No additional file reads are needed for stage announcements and transitions -- only the checkpoint quote requires a targeted artifact read.
