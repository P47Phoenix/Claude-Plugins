# Product Owner Review -- Idea Brief (Gate 1)

**Reviewer**: Product Owner (Gandalf)
**Date**: 2026-04-05
**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Project**: Orchestration Discipline Bundle (FEATURE, bundled)
**Sources**: GitHub Issues #73, #71, #70, #69
**Verdict**: DONE

*"A product owner is never late, nor early. They prioritize precisely when they mean to."*

---

## Criteria Evaluation

### [PASS] [blocking] Problem statement present and clear

The Problem Statement names all four discipline gaps with precision: (1) a frozen `project_type` in config that lies to runs of any other type, (2) the orchestrator granting itself "simple enough" exemptions and writing artifacts directly, (3) review patterns silently collapsing multiple reviewer roles into a single sub-agent and defeating context isolation, and (4) the Architect stage running only one adversarial pass and anchoring on first-pass findings. The compounding harm -- erosion of trust in the pipeline's verdicts -- is named explicitly. The bundling rationale (shared files, merge churn, contradictory edits) is included and is itself a piece of problem framing. A reader can reproduce each failure mode from the description.

### [PASS] [blocking] Target users identified

Three distinct user groups are enumerated, each with the specific pain this bundle addresses:

1. **delivery-flow operators** -- currently get wrong-typed routing and invisible orchestrator shortcuts.
2. **Plugin contributors** -- depend on context isolation and adversarial review for honest agent outputs.
3. **Future PO and Architect agents** -- need the orchestrator to be a delegator, not a doer.

The user list maps cleanly onto the four issues, so each fix has a constituency.

### [PASS] [blocking] Goals are measurable

Five goals, each with an observable, binary acceptance signal:

| # | Goal | Measurable? | Assessment |
|---|------|-------------|------------|
| 1 | Truthful project typing per run | Yes -- inspect a pipeline run and verify Phase 1 detection executed from the user's request, not from config | Binary: detection ran or did not |
| 2 | Delegation as prime directive | Yes -- run the pipeline; verify zero orchestrator writes to `.delivery/artifacts/` (except routing metadata) and to source files; hook enforcement present | Hook either blocks self-writes or it does not |
| 3 | One role, one sub-agent | Yes -- audit any pipeline run; each reviewer role appears in its own sub-agent invocation; compound prompts detectable | Hook flags compound prompts or not |
| 4 | Iterative adversarial review at Architect | Yes -- inspect Architect stage; loops are isolated, fresh-context, and bounded by `max_self_correction` (default 3) or zero-issue exit | Loops behave as specified or not |
| 5 | Coherent edits | Yes -- verify named shared files are touched once with internally consistent guidance | Single PR diff is reviewable for consistency |

Each goal is testable in DoD without further clarification.

### [PASS] [blocking] Constraints documented

Six constraints are named, all well-targeted:

1. **Backwards compatibility for config** -- removing `project_type` must not break existing `.delivery/config.yml`; key tolerated, deprecation noted, schema version bumped.
2. **No new external dependencies** -- hook updates remain pure Python stdlib.
3. **Hook performance budget** -- `enforce_pipeline_scope.py` and `audit_agent_prompt.py` must not noticeably slow tool calls.
4. **Documentation parity** -- CLAUDE.md, README.md, marketplace.json, `references/config-schema.md` updated before merge.
5. **Self-consistency / dogfooding** -- this bundle itself must run through delivery-flow.
6. **Plugin-dev skills required** -- `plugin-dev:skill-development` and `plugin-dev:hook-development` loaded before any SKILL.md or hook edits.

These constraints prevent scope drift, protect backward compatibility, and operationalize repo memory (dogfooding, plugin-dev skills, doc parity).

### [PASS] [blocking] Initial scope defined (4 bundled issues)

Four GitHub issues are scoped, ordered by WSJF, each with priority and a concrete edit list:

1. **#73 -- Remove `project_type` from config** (P0, WSJF 25.0). Strip from config and setup wizard, run Phase 1 every invocation, bump schema, document migration, update `config-schema.md`, `setup-wizard.md`, `project-types.md`, SKILL.md.
2. **#71 -- Orchestrator bypasses delegation when "simple"** (P0, WSJF 14.5). Strengthen delegation directive in SKILL.md, reject "simple" justification at Step 4.5, add anti-patterns section, extend `enforce_pipeline_scope.py` to block orchestrator self-writes.
3. **#70 -- Enforce one-sub-agent-per-reviewer** (P0, WSJF 14.0). Add "One Role = One Sub-Agent" rule to SKILL.md, reinforce in `team-patterns.md`, `quality-gates.md`, `pipeline-stages.md`; optionally extend `audit_agent_prompt.py`.
4. **#69 -- Architect adversarial loops with isolated context** (P1, WSJF 11.0). Add isolated adversarial loops at Architect, bounded by `max_self_correction` or zero-issue exit; document as "Isolated Adversarial Loop" in `team-patterns.md`.

A consolidated **Shared Target Files** list names exactly which SKILL.md, references, hooks, and doc-parity files will be touched. The bundling justification is sound: the same files would otherwise be edited 3-4 times across separate runs with merge churn and contradictory edits.

### [PASS] [blocking] Out of scope defined

Seven explicit exclusions, each blocking a plausible scope-creep path:

1. Rewriting Phase 1 project-type detection logic itself (only invocation cadence changes).
2. New collaboration patterns beyond the "Isolated Adversarial Loop" variant.
3. Adversarial loops at stages other than Architect.
4. A general migration tool for old configs beyond tolerant parsing and a deprecation note.
5. Refactoring hooks unrelated to delegation enforcement or prompt auditing.
6. Net-new analytics, telemetry, or dashboard changes.
7. Any non-delivery-flow plugin (`developer/`, `architect/`, `quality/`, etc.) -- those are downstream consumers, not the subject of this bundle.

Boundaries are crisp. A developer tempted to "fix Refine loops while we're in there" or "add a migration CLI" knows those are out of bounds.

### [PASS] [blocking] Business value evident

The through-line is **trust in pipeline verdicts**, named in the Problem Statement and reinforced by every goal. Each fix protects a specific axis of trust: truthful routing (#73), enforced delegation (#71), honest review isolation (#70), and deeper architectural critique (#69). The bundling itself adds value: one coherent PR over four churning ones, with internally consistent guidance across the shared files. For users currently shipping work through delivery-flow, the value is concrete -- the orchestrator stops silently corrupting its own pipeline.

---

## Notes for Downstream Stages

- **Refine**: turn each of the five goals into explicit acceptance criteria, with the hook or doc edit that enforces each one.
- **Architect**: examine `enforce_pipeline_scope.py` and `audit_agent_prompt.py` deeply before proposing extensions. Validate and build on the existing designs; do not reimagine them.
- **Plan**: documentation parity is a hard constraint -- CLAUDE.md, README.md, marketplace.json, and `config-schema.md` edits are first-class tasks, not afterthoughts.
- **UAT**: this bundle dogfoods delivery-flow; the orchestrator's behavior during this run is itself UAT evidence. Any orchestrator self-write or compound reviewer prompt observed during execution is a failure of the bundle, not an aside.

---

## Summary

*"Even the smallest discipline gap can unsettle an entire pipeline. But this brief has traced the shadows to their sources."*

All seven Gate 1 criteria pass. The brief is well-structured: four issues bundled with sound rationale, five measurable goals, six well-targeted constraints, seven crisp out-of-scope items, and a consolidated shared-target-files list that makes the coherent-edits goal actionable. The bundle is fit to advance to Stage 2 (Refine).

*All we have to decide is what to fix with the discipline that is given to us. And I decide we fix the orchestrator's shortcuts before we trust it with anything larger. Forward to Refine.*
