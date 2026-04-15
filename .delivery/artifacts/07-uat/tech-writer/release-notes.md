# Release Notes — Architecture Flow Docs

**Audience:** Claude-Plugins contributors
**Run:** run-2026-04-11-i0j7
**Date:** 2026-04-11

## What shipped

Six new detailed architecture flow documents under `delivery-team/architecture/`, supplementing the high-level `delivery-team/ARCHITECTURE.md`:

- `adversarial-review-triggers.md` — when and why adversarial review fires (FLOW-1)
- `deterministic-gating.md` — rule-based gate evaluation with BRE honesty note (FLOW-2)
- `hook-firing-timeline.md` — hook event sequence across a pipeline run (FLOW-3, MERGE)
- `dod-self-correction.md` — DoD validation and self-correction loops (FLOW-4, MERGE)
- `empirical-lifecycle.md` — CODE_COMPLETE and empirical validation lifecycle (FLOW-5)
- `sub-agent-dispatch.md` — role-scoped sub-agent dispatch mechanics (FLOW-6)

Each document includes 2 Mermaid diagrams (12 total). Mermaid renders natively in GitHub — no additional tooling required to view.

## Cross-links added

- `delivery-team/ARCHITECTURE.md` — new "Detailed flow documents" section
- `delivery-team/README.md` — one-line pointer to `architecture/`
- `CLAUDE.md` — mention under Architecture Patterns

## Notes

- FLOW-2 preserves BRE honesty: delivery-team has no deterministic BRE module; gating is convention-enforced via SKILL.md rules and hook validation.
- FLOW-3 and FLOW-4 are MERGE docs honoring multi-author brainstorm input.
- No behavior change; documentation-only release.
