# Development Artifact: BF-62-001 — Remove Duplicated Stage Definitions from SKILL.md

**Story**: BF-62-001
**Issues**: #60, #61, #62
**Developer**: Gimli

## Implementation Summary

And my code! Refactored `delivery-team/skills/delivery-flow/SKILL.md` to remove ~270 lines of duplicated stage definitions, fix flat artifact paths, and fix the DoD template violation. The stone was heavy with duplication, but a Dwarf's axe knows how to carve it clean.

## Changes Made

### 1. Stage Definitions Section (lines 522-652)

Replaced ~400 lines of detailed stage definitions with ~130 lines of concise summaries. Each stage now contains ONLY orchestrator-level routing information:

- Stage name and number
- Runs for / Skipped for (project types)
- Purpose (one line)
- Primary agent (skill + role, brief)
- Upstream artifacts (namespaced paths)
- Collaboration patterns assigned
- DoD validators (role list)
- Human checkpoint (if any)
- Max self-correction iterations
- Output artifact path(s) using namespaced format
- Game dev additions (brief note)
- Reference directive to `references/pipeline-stages.md`

**Removed** from each stage:
- Detailed sub-flow steps (Input/Output per agent)
- Supporting agent descriptions with Input/Output details
- Inline content duplicating pipeline-stages.md

**Added** authoritative-source directive at the top of Stage Definitions:
> `references/pipeline-stages.md` is the single source of truth for stage sub-flows, agent invocation details, artifact output paths (namespaced), and DoD Validator Dispatch Templates.

### 2. DoD Template Fix (Team Definition of Done Protocol)

Replaced the inline validator prompt template that contained `[ARTIFACT CONTENT]` with a reference to the DoD Validator Dispatch Template in `references/pipeline-stages.md`. The validator now reads the artifact from the file path -- the orchestrator never pastes artifact content into validator prompts.

### 3. Artifact Path Migration (flat -> namespaced)

All artifact paths converted from flat format to namespaced format:

| Old (flat) | New (namespaced) |
|-----------|-----------------|
| `.delivery/artifacts/01-idea-brief.md` | `.delivery/artifacts/01-idea/po/idea-brief.md` |
| `.delivery/artifacts/02-prd.md` | `.delivery/artifacts/02-refine/po/prd.md` |
| `.delivery/artifacts/03-ux-design.md` | `.delivery/artifacts/03-design/ux/user-flows.md` (+ wireframes, component-specs, accessibility) |
| `.delivery/artifacts/04-architecture.md` | `.delivery/artifacts/04-architect/solution/architecture.md` |
| `.delivery/artifacts/04a-adrs/ADR-001.md` | `.delivery/artifacts/04-architect/adrs/ADR-001.md` |
| `.delivery/artifacts/05-sprint-plan.md` | `.delivery/artifacts/05-plan/po/stories.md`, `sm/sprint-plan.md`, `qa/test-strategy.md`, `devops/deploy-plan.md` |
| `.delivery/artifacts/06-dev-notes.md` | `.delivery/artifacts/06-dev/developer/{story-id}.md` |
| `.delivery/artifacts/07-uat-report.md` | `.delivery/artifacts/07-uat/qa/test-plan.md`, `qa/test-cases.md` |
| `.delivery/artifacts/07a-release-plan.md` | `.delivery/artifacts/07-uat/devops/release-plan.md` |
| `.delivery/artifacts/07b-documentation.md` | `.delivery/artifacts/07-uat/tech-writer/release-notes.md`, `user-guide.md` |

### 4. Cross-Stage Artifact Flow Table

Updated to use generic artifact names without hardcoded flat paths. Added footer referencing `references/pipeline-stages.md` for exact file paths.

## Verification Status

| Check | Result |
|-------|--------|
| No `[ARTIFACT CONTENT]` in file | PASS |
| No flat artifact paths (e.g., `01-idea-brief.md`, `02-prd.md`) | PASS |
| All 7 stages present in Stage Definitions | PASS (lines 529-652) |
| Each stage has: purpose, runs-for, collaboration patterns, DoD validators, checkpoint, max iterations, output path | PASS |
| Each stage references `pipeline-stages.md` | PASS (7/7 stages) |
| Authoritative-source directive present | PASS (line 524) |
| Phase 4 Step 3 references pipeline-stages.md | PASS (line 363) |
| DoD template references pipeline-stages.md | PASS (line 667) |
| Stage Routing Matrix intact | PASS (lines 251-259) |
| Cross-Stage Artifact Flow updated | PASS (lines 741-755) |
| All namespaced paths match pipeline-stages.md | PASS |
| Line count reduced | PASS (944 lines, down from ~1240 — net reduction of ~296 lines) |

## Deviation from Plan

None. All acceptance criteria addressed as specified.

## Known Issues

None.
