## Idea Brief

**Project Type**: FEATURE
**Date**: 2026-03-29
**Source**: Retrospective action items M1-M4 (from retros c8f2, k4m9)

### Problem Statement

Three pipeline stages have first-try pass rates well below acceptable thresholds: Design (50%), UAT (67%), and Idea (67%). These failures are not random -- retrospectives c8f2 and k4m9 identified specific, recurring root causes: phantom file references surviving into downstream stages, missing shared-module review in UAT, absent capacity planning in Plan stage, over-allocated sprint plans passing without warning, and derived artifacts drifting from source after regeneration. Four MUST HAVE retro action items (M1-M4) directly address these root causes with concrete stage-level fixes.

### Target Users

- **Plugin contributors** running delivery-flow pipelines on this repo, who currently experience avoidable rework loops at Design, UAT, and Plan stages
- **Delivery team sub-agents** (Architect, QA, Developer) whose DoD validations catch issues too late that should be prevented by earlier gates
- **Pipeline maintainers** who update quality-gates.md, pipeline-stages.md, and related reference files

### Goals

1. Raise Design stage first-try pass rate from 50% to >= 80% by catching phantom references and filename mismatches before they reach downstream stages
2. Raise UAT stage first-try pass rate from 67% to >= 85% by adding shared-module review and empirical-items tracking
3. Reduce Plan stage rework by adding capacity validation (>100% sprint allocation triggers warning) and mandatory coverage matrix
4. Eliminate derived-artifact drift by adding "regenerate derived artifacts" to the Dev stage DoD checklist

### Constraints

- All changes are to delivery-team skill reference files (markdown) -- no new Python scripts or external dependencies
- Changes must preserve backward compatibility with config schema v2.3
- Each change must be traceable to a specific retro action item (c8f2 or k4m9)
- Must use plugin-dev skills when modifying plugin components
- Dogfooding is a P0 UAT gate -- the hardened stages must be validated by running an actual pipeline through them before DoD submission

### Initial Scope

**M1 -- UAT stage hardening (retros c8f2, k4m9):**
1. Add a shared-module review checkpoint to the UAT stage definition, requiring the QA validator to verify that changes touching shared modules have been tested in all consuming contexts
2. Create an empirical-items tracking artifact template that UAT sub-agents populate to record which acceptance criteria require runtime validation vs. static review

**M2 -- Design stage hardening (retro k4m9):**
3. Elevate phantom reference findings (file paths cited in artifacts that do not exist on disk) to high-severity in the DoD validator criteria, so they block stage completion rather than appearing as warnings
4. Implement a filename reconciliation gate at Dev stage entry that verifies all file paths referenced in Design/Architect artifacts exist before development begins

**M3 -- Plan stage guardrails (retros c8f2, k4m9):**
5. Update the Plan stage template to include a mandatory capacity matrix (team members x estimated hours) and a coverage matrix (PRD FRs x planned tasks)
6. Add a sprint capacity threshold validation: if total allocated effort exceeds 100% of available capacity, emit a Plan-stage validation warning that must be acknowledged or resolved

**M4 -- Dev stage DoD (retro c8f2):**
7. Add "regenerate derived artifacts" as an explicit checklist item in the Dev stage DoD, ensuring that any artifacts derived from modified source files are regenerated before Dev completion

### Out of Scope (initial)

- Idea stage hardening (its 67% pass rate shares root causes with Design; M2 fixes will cascade)
- New Python hook scripts or automated enforcement tooling (this scope is markdown/template changes only)
- Analytics dashboard updates for tracking the new metrics
- Changes to the setup wizard or config schema
- Modifications to alias themes or personality injection
- Retrospective format changes

### Files Involved

| File | Role | Change |
|------|------|--------|
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | Stage definitions | Add shared-module review checkpoint to UAT (M1), filename reconciliation gate at Dev entry (M2), capacity + coverage matrix to Plan (M3), regenerate-derived-artifacts to Dev DoD (M4) |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | DoD validator criteria | Elevate phantom references to high-severity (M2), add capacity threshold warning (M3), add empirical-items tracking requirement (M1) |
| `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | Artifact templates | Add empirical-items tracking artifact template for UAT (M1) |
| `delivery-team/skills/delivery-flow/references/project-templates.md` | Project type templates | Update Plan template with mandatory capacity + coverage matrix fields (M3) |
| `delivery-team/skills/delivery-flow/SKILL.md` | Orchestrator instructions | Reference updates if stage flow changes require orchestrator awareness |
| `delivery-team/skills/quality/SKILL.md` | QA skill instructions | Add shared-module review guidance for UAT validation (M1) |

### Retro Traceability

| Action Item | Retro Source | Stage Target | Files |
|-------------|-------------|--------------|-------|
| M1: Shared-module review checkpoint | c8f2 | UAT | pipeline-stages.md, quality-gates.md |
| M1: Empirical-items tracking template | k4m9 | UAT | artifact-contracts.md, quality-gates.md |
| M2: Phantom reference high-severity | k4m9 | Design DoD | quality-gates.md |
| M2: Filename reconciliation gate | k4m9 | Dev entry | pipeline-stages.md |
| M3: Capacity + coverage matrix | c8f2 | Plan | pipeline-stages.md, project-templates.md |
| M3: Sprint capacity threshold warning | k4m9 | Plan | quality-gates.md, pipeline-stages.md |
| M4: Regenerate derived artifacts | c8f2 | Dev DoD | pipeline-stages.md, quality-gates.md |
