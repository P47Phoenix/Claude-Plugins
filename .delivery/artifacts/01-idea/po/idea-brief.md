## Idea Brief

**Project Type**: BUG_FIX
**Date**: 2026-04-04
**Source Issues**: #60, #61, #62

### Problem Statement

The delivery-flow SKILL.md file duplicates approximately 400 lines of stage definitions that also exist in `references/pipeline-stages.md`. Over time, these two copies have drifted out of sync, creating two observable defects:

1. **Wrong artifact paths (Issue #60)**: SKILL.md uses flat artifact paths (e.g., `.delivery/artifacts/01-idea-brief.md`) while pipeline-stages.md uses the correct namespaced paths (e.g., `.delivery/artifacts/01-idea/po/idea-brief.md`). Agents following SKILL.md write artifacts to the wrong locations, breaking downstream pipeline stages that look for namespaced paths.

2. **DoD template violates two-channel rule (Issue #61)**: SKILL.md's Team Definition of Done Protocol section contains a validator prompt template that pastes artifact content inline (`[ARTIFACT CONTENT]`). This violates the two-channel communication principle established in Phase 4. The correct template in pipeline-stages.md uses file-path references, letting validators read artifacts from disk.

3. **Root cause -- content duplication (Issue #62)**: Both symptoms stem from SKILL.md duplicating detailed stage definitions (agent invocations, artifact paths, DoD templates) that should exist in a single authoritative source: `references/pipeline-stages.md`.

### Target Users

- The delivery-flow orchestrator (the primary consumer of SKILL.md)
- All delivery-team sub-agents that receive artifact paths from the orchestrator
- Plugin maintainers who need a single source of truth for stage definitions

### Goals

1. Establish `references/pipeline-stages.md` as the single source of truth for detailed stage sub-flows, agent invocations, artifact output paths, and DoD validator templates.
2. Remove duplicated detailed definitions from SKILL.md while preserving its role as the high-level orchestration guide.
3. Fix the artifact path inconsistency so all agents write to the correct namespaced locations.
4. Fix the DoD validator template so artifact content is never pasted inline.
5. Ensure the pipeline continues to function correctly after the refactoring.

### Constraints

- Single file modified: `delivery-team/skills/delivery-flow/SKILL.md`
- Markdown-only edits (no code changes)
- Must not break existing pipeline execution (backward compatible)
- SKILL.md must retain: Stage Routing Matrix, high-level stage descriptions, collaboration pattern assignments, human checkpoint assignments

### Initial Scope

Remove ~400 lines of duplicated stage definitions from SKILL.md and replace them with explicit cross-references to `references/pipeline-stages.md`. Replace the inline DoD validator template with a reference to the correct template in pipeline-stages.md.
