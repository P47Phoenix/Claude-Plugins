# Idea Brief: Orchestration Discipline Bundle

**Project Type**: FEATURE (bundled)
**Date**: 2026-04-05
**Source**: GitHub Issues #73, #71, #70, #69
**PO**: Gandalf

*"A pipeline is never late, nor early. It delegates precisely when it means to."*

## Problem Statement

The delivery-flow orchestrator has accumulated four discipline gaps that, taken together, allow it to silently corrupt its own pipeline. A frozen `project_type` in config lies to every run that isn't the one type setup happened to guess. The orchestrator grants itself "simple enough" exemptions and writes artifacts directly instead of delegating. Review patterns quietly collapse multiple reviewer roles into one sub-agent, defeating context isolation. And the Architect stage runs only a single adversarial pass, anchoring on the first issues found while deeper ones slip through. Each is small alone; together they erode the trust users place in the pipeline's verdicts.

These four issues all live in the same handful of files. Sequencing them as separate runs would force the same SKILL.md and reference docs to be edited three or four times, with merge churn and contradictory edits. They want to ship as one coherent act of remediation.

## Target Users

- **delivery-flow operators** running pipelines who currently get wrong-typed routing and invisible orchestrator shortcuts.
- **Plugin contributors** who rely on context isolation and adversarial review to keep agent outputs honest.
- **Future PO and Architect agents** in this repo, who need the orchestrator to be a delegator, not a doer.

## Goals

1. **Truthful project typing per run.** Phase 1 detection runs every pipeline invocation from the user's actual request; no frozen value lies in config.
2. **Delegation as prime directive.** The orchestrator never writes artifacts or source files directly during a pipeline run, regardless of perceived simplicity. Hooks enforce this, not just prose.
3. **One role, one sub-agent.** Every review pattern dispatches each reviewer role to its own isolated sub-agent. Compound multi-role prompts are detectable and discouraged.
4. **Iterative adversarial review at Architect.** Each adversarial loop runs in a fresh sub-agent with no knowledge of prior loops, repeating until clean or `max_self_correction` is reached.
5. **Coherent edits.** All four fixes ship in one bundle so the shared files (SKILL.md, pipeline-stages.md, team-patterns.md, quality-gates.md) are touched once with internally consistent guidance.

## Constraints

- **Backwards compatibility for config.** Removing `project_type` must not break existing `.delivery/config.yml` files; older configs should be tolerated (key ignored, deprecation noted) and the schema version bumped.
- **No new external dependencies.** Hook updates remain pure Python stdlib.
- **Hook performance budget.** `enforce_pipeline_scope.py` and `audit_agent_prompt.py` must stay fast enough not to noticeably slow tool calls.
- **Documentation parity.** CLAUDE.md, README.md, marketplace.json, and `references/config-schema.md` must reflect the new schema version and behavior before merge.
- **Self-consistency / dogfooding.** This bundle itself must run through delivery-flow; the orchestrator must demonstrate the very discipline it is being taught.
- **Plugin-dev skills required.** Any SKILL.md or hook edits load `plugin-dev:skill-development` and `plugin-dev:hook-development` first.

## Initial Scope

Four GitHub issues, ordered by WSJF, all bundled as one FEATURE pipeline run:

1. **#73 — Remove `project_type` from config (P0, WSJF 25.0).** Strip `project_type` from `.delivery/config.yml` and the setup wizard (drop Q1). Phase 1 detection runs every pipeline run from the user's current request. Bump schema version, document migration, update `config-schema.md`, `setup-wizard.md`, `project-types.md`, and SKILL.md routing guidance.

2. **#71 — Orchestrator bypasses delegation when "simple" (P0, WSJF 14.5).** Strengthen the delegation prime directive in SKILL.md with explicit anti-patterns. Update Step 4.5 to reject "simple" as a justification. Add a "Common Orchestrator Anti-Patterns" section. Extend `enforce_pipeline_scope.py` to block orchestrator self-writes to `.delivery/artifacts/` (except routing metadata) and to source files during pipeline runs.

3. **#70 — Enforce one-sub-agent-per-reviewer across all patterns (P0, WSJF 14.0).** Add a prominent "One Role = One Sub-Agent" rule to SKILL.md. Reinforce in `team-patterns.md` (every pattern leads with the dispatch rule), `quality-gates.md` (DoD protocol), and `pipeline-stages.md` (header note on `[PARALLEL]`/`[SEQUENTIAL]`). Optionally extend `audit_agent_prompt.py` to detect compound multi-role prompts.

4. **#69 — Architect adversarial loops with isolated context (P1, WSJF 11.0).** Add adversarial **loops** at the Architect stage. Each loop spawns a separate sub-agent that does not know what prior loops fixed. Run until either `max_self_correction` (default 3) is reached OR a loop returns zero issues. Document as the "Isolated Adversarial Loop" variant in `team-patterns.md` and reference from `pipeline-stages.md` Stage 4.

**Shared target files:**
- `delivery-team/skills/delivery-flow/SKILL.md`
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md`
- `delivery-team/skills/delivery-flow/references/team-patterns.md`
- `delivery-team/skills/delivery-flow/references/quality-gates.md`
- `delivery-team/skills/delivery-flow/references/config-schema.md`
- `delivery-team/skills/delivery-flow/references/setup-wizard.md`
- `delivery-team/skills/delivery-flow/references/project-types.md`
- `delivery-team/hooks/enforce_pipeline_scope.py`
- `delivery-team/hooks/audit_agent_prompt.py` (optional)
- `CLAUDE.md`, `README.md`, `.claude-plugin/marketplace.json` (doc parity)

## Out of Scope

- Rewriting Phase 1 project-type detection logic itself (only its invocation cadence changes).
- Introducing new collaboration patterns beyond the "Isolated Adversarial Loop" variant.
- Adversarial loops at stages other than Architect (Refine, Design, Plan loops are a separate future discussion).
- A general migration tool for old `.delivery/config.yml` files beyond tolerant parsing and a deprecation note.
- Refactoring hooks unrelated to delegation enforcement or prompt auditing.
- Net-new analytics, telemetry, or dashboard changes.
- Any non-delivery-flow plugin (`developer/`, `architect/`, `quality/`, etc.) — those are downstream consumers, not the subject of this bundle.

---

*All we have to decide is what to fix with the discipline that is given to us. And I decide we fix the orchestrator's shortcuts before we trust it with anything larger.*
