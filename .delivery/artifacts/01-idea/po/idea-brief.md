## Idea Brief

**Project Type**: BUG_FIX
**Date**: 2026-04-04
**Source**: GitHub Issue #55 (P47Phoenix/Claude-Plugins#55)
**Pipeline**: run-2026-04-04-w7m3

### Problem Statement

The Architect agent proposes competing designs instead of building on user-provided specifications. When a user hands the team a detailed spec (e.g., a multi-agent system design), the Architect should validate feasibility, identify gaps, and map to implementation — not reimagine the solution from scratch. This erodes user trust and wastes pipeline cycles.

### Target Users

- **Plugin developers**: Users who provide detailed specs or existing designs and expect the delivery team to build ON them, not override them.
- **Delivery pipeline users**: Anyone running delivery-flow who provides upstream artifacts with established design decisions.

### Goals

1. Architect always reads and summarizes user-provided specs before proposing any architecture
2. Architect distinguishes "decisions already made" from "open questions" and respects the former
3. Architect only proposes alternatives when the existing design has clear, documented technical blockers
4. Reduction in wasted self-correction cycles caused by Architect overriding user intent

### Constraints

- Changes are confined to the `delivery-team/skills/architect/` directory (SKILL.md and/or reference files)
- No schema changes, no new dependencies, no code changes outside the architect skill
- Must be backward-compatible — existing pipelines without user-provided specs should be unaffected
- Must dogfood the fix by running the updated skill against a scenario with a user-provided spec

### Initial Scope

Update the architect skill to add a mandatory "Prior Art Analysis" step that:
1. Reads and summarizes the user-provided spec before any design work
2. Identifies what decisions are already made vs. what's open
3. Builds architecture ON the existing design (validates, fills gaps, maps to implementation)
4. Only proposes alternatives when the existing design has clear technical blockers

### Out of Scope (initial)

- Changes to other skills (developer, quality, operations, etc.)
- Config schema changes
- New pipeline stages or routing changes
- Retroactive fixes to past pipeline run artifacts
