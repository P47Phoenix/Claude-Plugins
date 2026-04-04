## Idea Brief: Orchestrator Theme Surfacing

**Project Type**: FEATURE
**Date**: 2026-04-04
**Source**: GitHub Issue #59 (P47Phoenix/Claude-Plugins)
**Pipeline**: Orchestrator theme surfacing
**Skill Under Enhancement**: `delivery-team/skills/delivery-flow/`

---

### Problem Statement

When a non-business alias theme is configured (e.g., `lotr`, `star-wars`, `breaking-bad`), the delivery-flow orchestrator injects personality into each sub-agent's prompt via the ALIAS block (Phase 4 Step 4). Agents write their artifacts in character -- Gandalf counsels on priorities, Gimli builds code with dwarven pride, Aragorn rallies the standup. The artifacts carry the theme voice.

But the orchestrator strips all of that personality when reporting results to the user. The two-channel communication protocol (Phase 4) constrains the orchestrator to signal-only reporting: STATUS, file paths, summaries under 200 characters. Stage announcements, checkpoint summaries, and transition messages are written in neutral orchestrator voice regardless of theme. The user configured a theme expecting the entire experience to carry personality -- what they get is personality buried in files they have to open, wrapped in clinical status updates.

The disconnect is jarring. The orchestrator is the user's primary interface to the pipeline. If it speaks in corporate monotone while agents write in character behind the scenes, the theme feels bolted on rather than woven through.

### Target Users

- **Delivery pipeline users with non-business alias themes** who expect the orchestrator's chat output (stage announcements, checkpoint summaries, transition messages) to reflect the configured theme personality
- **Teams using themes for engagement** where the orchestrator's neutral voice breaks the immersion that makes themed aliases fun and effective

### Goals

| # | Goal | Measurable Target |
|---|------|-------------------|
| 1 | Orchestrator surfaces agent theme personality in chat when a non-business alias theme is configured | Stage headers, checkpoint summaries, and transition messages carry the theme's voice and reference agent character names |
| 2 | Orchestrator quotes or paraphrases memorable lines from agent artifacts to surface personality without violating the no-content-forwarding rule | Checkpoint summaries include at least one quoted line from the primary agent's artifact |
| 3 | Business theme behavior is unchanged | When `aliases.theme` is `business` (or unset), orchestrator output is identical to current behavior |

### Constraints

- **Single file change.** Only `delivery-team/skills/delivery-flow/SKILL.md` is modified. No config schema changes -- `aliases.theme` already exists and is sufficient.
- **Two-channel rule preserved.** The orchestrator still does not paste artifact content into downstream agent prompts. Theme surfacing applies only to user-facing chat output (stage headers, checkpoint summaries, transitions), not inter-agent routing.
- **No personality in routing decisions.** The orchestrator's internal logic (state management, stage advancement, validator dispatch) remains neutral. Personality is applied only to user-visible output text.
- **Business theme = no change.** The `business` theme produces default professional names with no personality injection. This feature is gated on `theme != business`.
- **Backward compatible.** Existing pipeline behavior, artifact formats, and agent invocation templates are unchanged.

### Initial Scope

**Theme-Gated Reporting Protocol:**
- Add a new sub-section to Phase 4 that defines how the orchestrator adapts its user-facing output when a non-business theme is active
- Stage headers reference the agent's character name (e.g., "Gandalf shall examine the product requirements" instead of "Product Owner will refine requirements")
- Checkpoint summaries include a brief quoted line from the primary agent's artifact to surface voice
- Transition messages between stages carry thematic flavor

**Orchestrator Neutrality Preserved:**
- Internal routing, state updates, and signal processing remain personality-free
- The signal block format (STATUS/ARTIFACT/SUMMARY) is unchanged
- Agent invocation templates are unchanged
- Downstream agents still receive paths, not content

**Business Theme Guard:**
- All theme surfacing behavior is gated on `aliases.theme != business`
- When theme is `business`, orchestrator output is identical to current behavior -- no regressions

### Out of Scope

- **Config schema changes.** No new config keys. `aliases.theme` and `aliases.custom_path` are sufficient.
- **Changes to agent invocation templates.** The ALIAS block injection (Phase 4 Step 4) is unchanged.
- **Changes to the two-channel communication architecture.** Artifact content still never flows through the orchestrator to other agents.
- **Theme-aware validator prompts.** DoD validators remain neutral regardless of theme.
- **New alias themes.** This feature enhances how existing themes surface, not which themes exist.
- **Changes to other skills.** Only the delivery-flow SKILL.md is modified.
