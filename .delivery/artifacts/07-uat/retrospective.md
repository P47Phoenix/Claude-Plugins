# Retrospective — run-2026-04-11-e6f3

**Facilitator**: Aragorn (Retro Lead)
**Date**: 2026-04-11
**Project Type**: FEATURE
**Pipeline Duration**: Full 7-stage

## What Went Well

1. **Session evidence drove guardrail design** — Real session log (0876a59e) provided the exact anti-pattern quote that became the SKILL.md guardrail language. Evidence-first design produces stronger constraints than theoretical spec.

2. **Compound value delivery** — DEFECT-001 and DEFECT-002 addressed in the same release as the adversarial enhancement. The challengers ARE the fix mechanism, not a separate patch.

3. **Mid-pipeline PO additions landed cleanly** — Two additions (sub-agent dispatch mandate + session evidence integration) were injected mid-Development without restarting the pipeline. Constraints.yml and SKILL.md absorbed them in-stride.

## What Didn't Go Well

1. **API overload on Wave 1** — First attempt hit rate limits; retry succeeded but added latency. Consider batching sub-agent dispatches in future.

2. **SKILL.md size (1179 lines)** — Approaching decomposition threshold. Future BACKLOG item: extract challenger definitions into `references/challenger-guide.md` to keep SKILL.md under 1000 lines.

## Key Insight

The strongest guardrail is **STRUCTURAL** — the sub-agent task blocks use language ("your output", "write to disk", "signal format") that ONLY makes sense for a spawned agent. This is the real defense against inlining, not just the "NEVER inline" text. If an orchestrator tries to inline, the instructions produce nonsensical behavior, creating a natural deterrent beyond policy language.

## Action Items

- [ ] BACKLOG: Decompose SKILL.md challenger sections into reference file (when >1200 lines)
- [x] Memory write: structural guardrail insight -> stages/development.md
