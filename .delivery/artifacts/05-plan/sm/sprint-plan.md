# Sprint Plan: Stage Health Hardening

**Version**: 2.0
**Author**: Aragorn (Scrum Master)
**Date**: 2026-03-29
**Status**: Committed
**Inputs**: User Stories v1.0 (Gandalf/PO), PRD v1.1, SM Review v1.0
**Project Type**: FEATURE
**Revision Note**: v2.0 addresses capacity overcommitment finding from SM Review. Stories re-estimated to reflect markdown-only edit complexity. No scope removed; all 5 stories and 12 FRs retained.

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."*

---

## 1. Sprint Goal

Harden the Design, Plan, UAT, and Dev pipeline stages with guardrails that catch phantom references, missing capacity planning, untracked empirical items, shared-module gaps, and derived artifact drift -- raising first-try pass rates and eliminating avoidable rework loops traced to retros c8f2 and k4m9.

---

## 2. Capacity Declaration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Team size | 1 contributor (all roles) | Solo contributor model; sub-agents handle role specialization |
| Velocity baseline | 2-3 stories/sprint (L-sized) | Based on prior FEATURE sprints in this repo |
| 80% ceiling | 2.4L equivalent | 80% of 3L baseline |
| Committed this sprint | 5 stories (3M + 2S = 2.0L equivalent) | Within 80% ceiling |
| Utilization | ~83% of 80% ceiling (~67% of baseline) | Comfortable margin |
| Ceremony/interruption budget | None (solo contributor, no PTO) | Explicitly stated per SM Review advisory |

### Re-estimation Rationale (v2.0)

The v1.0 plan sized stories using general FEATURE velocity assumptions. However, NFR-01 constrains ALL work in this sprint to additive markdown edits in existing reference files. No new scripts, no schema changes, no external dependencies, no new files. Each story's implementation is inserting defined text blocks at specified locations in existing documents.

The re-estimation applies a **markdown-edit calibration**: stories whose implementation is purely additive text insertion into existing files with well-defined placement instructions are sized one tier lower than stories requiring code, schema changes, or new file creation.

| Story | v1.0 Size | v2.0 Size | Justification |
|-------|-----------|-----------|---------------|
| US-01 | L | M | 3 sub-tasks, all additive text sections with exact placement (after X, before Y). No logic, no code, no file creation. |
| US-02 | L | M | 1 table row insertion, 1 template section, 1 gate criterion. All have precise insertion points defined in ACs. Depends on US-01 context but does not increase complexity. |
| US-03 | M | S | 2 targeted insertions: 1 warning criterion in Gate 3, 1 entry condition block in Stage 6. Both have exact placement and content defined in ACs. |
| US-04 | L | M | Most sub-tasks (4), but all are template creation (copy-paste structure) and single-line gate criteria. Templates are tables with defined columns -- structured fill-in, not creative authoring. |
| US-05 | S | S | Smallest story, unchanged. 2 sub-tasks: 1 validator update, 1 sub-flow step insertion, 1 gate criterion. |

**v1.0 total**: 3L + 1M + 1S = ~3.5L equivalent (117% of ceiling -- FAILED)
**v2.0 total**: 3M + 2S = 1.5L + 0.5L = **2.0L equivalent (83% of ceiling -- PASS)**

The fellowship no longer carries more than it promised. The weight of the pack is honest.

---

## 3. Committed Stories (Dependency + Priority Order)

| Order | ID | Title | Points | Milestone | Target Files |
|-------|----|-------|--------|-----------|--------------|
| 1 | US-03 | Phantom Reference Detection and Filename Reconciliation | S | M2 | `quality-gates.md`, `pipeline-stages.md` |
| 2 | US-04 | Plan Stage Capacity and Coverage Guardrails | M | M3 | `project-templates.md`, `pipeline-stages.md`, `quality-gates.md` |
| 3 | US-01 | Shared-Module Review at UAT | M | M1 | `pipeline-stages.md`, `quality/SKILL.md` |
| 4 | US-02 | Empirical-Items Tracking at UAT | M | M1 | `artifact-contracts.md`, `quality-gates.md` |
| 5 | US-05 | Derived Artifact Regeneration at Dev DoD | S | M4 | `pipeline-stages.md`, `quality-gates.md` |

**Ordering rationale**: The PO recommended M2 first so Design-stage fixes cascade early into downstream stages. M3 follows because it is independent and touches Plan stage. M1 stories (US-01 then US-02) are sequenced by their internal dependency -- US-02 depends on US-01's shared UAT stage context. M4 (US-05) is last as the smallest and fully independent.

---

## 4. Implementation Sequence

The road is long, but the path is clear. Each step builds on the last -- we do not scatter the fellowship.

### Step 1: Load plugin-dev skill (prerequisite for ALL steps)

Load `plugin-dev:skill-development` before modifying any SKILL.md or reference files. These are plugin component modifications; the skill-development conventions must be active throughout.

**Dependency**: None. This is the gate before all work begins.

### Step 2: US-03 -- Phantom Reference Detection (M2)

**Files**: `quality-gates.md`, `pipeline-stages.md`

2a. Add phantom reference WARNING criterion to Gate 3 in `quality-gates.md`:
- Place after "Design aligns with PRD requirements"
- Severity: `[warning]` (does not block)
- Include `[PLANNED]` annotation exemption language
- Add `<!-- retro k4m9 -->` annotation

2b. Add filename reconciliation blocking gate to Stage 6 entry conditions in `pipeline-stages.md`:
- 5-step reconciliation process (extract paths from Design + Architect artifacts, check disk, cross-reference sprint plan, report)
- `[PLANNED]` is NOT an exemption at Dev entry
- Pass/fail criteria with blocking behavior
- Resolution guidance (create files, add to sprint plan, or remove references)
- Light Mode applicability note
- Add `<!-- retro k4m9 -->` annotation

**Dependency**: None.

### Step 3: US-04 -- Plan Stage Guardrails (M3)

**Files**: `project-templates.md`, `pipeline-stages.md`, `quality-gates.md`

3a. Add "Sprint Plan Mandatory Sections" section at end of `project-templates.md`:
- Capacity matrix template (Team Member, Role, Available Hours, Allocated Hours, Utilization %, Total row)
- Coverage matrix template (PRD FR-ID, FR Description, Planned Task(s), Story ID(s), Status, Unmapped FRs area)
- Light Mode waiver for BUG_FIX and DOCS_ONLY on both matrices
- Add `<!-- retro c8f2 -->` annotation

3b. Add step 4 "Matrix validation" to Stage 5 Sub-Flow in `pipeline-stages.md`:
- Insert after step 3 (Invoke Supporting Agents)
- Validate capacity matrix presence + completeness
- Validate coverage matrix with all FRs mapped (unmapped FR = BLOCKING)
- Light Mode waiver for BUG_FIX/DOCS_ONLY
- Renumber subsequent steps

3c. Update Scrum Bag validator in Stage 5 DoD Validators in `pipeline-stages.md`:
- Add matrix requirements: capacity matrix present with utilization calculated, coverage matrix with all FRs mapped
- Add threshold language: >80% WARNING requiring acknowledgment, >100% BLOCKING

3d. Replace Gate 5 capacity criterion in `quality-gates.md`:
- Remove old "Commitment does not exceed 80% of available capacity [blocking]"
- Add two-tier model: >80% WARNING with acknowledgment, >100% BLOCKING with reduction or PO sign-off
- Light Mode applicability note
- Add `<!-- retros c8f2, k4m9 -->` annotation

**Dependency**: None (independent of Step 2).

### Step 4: US-01 -- Shared-Module Review at UAT (M1)

**Files**: `pipeline-stages.md`, `quality/SKILL.md`

4a. Insert step 5 "Shared-module review" into Stage 7 Sub-Flow in `pipeline-stages.md`:
- Place after step 4 (Exploratory testing sessions), before current step 5 (Invoke Supporting Agents)
- SEQUENTIAL tag, required marker
- Include shared-module definition, identification method, review requirements, output location
- Light Mode applicability note
- Renumber subsequent steps

4b. Update QA Engineer validator in Stage 7 DoD Validators in `pipeline-stages.md`:
- Add "shared-module review complete (if shared modules were modified)"

4c. Add "Shared-Module Review Protocol" section to `quality/SKILL.md`:
- Place after "Empirical Validation and CODE_COMPLETE Status" section, before "Sub-Agent Interface" section
- Definition of shared module (file referenced in 2+ stage artifacts)
- 5-step identification process using Glob/Read
- 4-item review checklist
- Output format template

**Dependency**: None (independent of Steps 2-3, but sequenced here per milestone ordering).

### Step 5: US-02 -- Empirical-Items Tracking (M1)

**Files**: `artifact-contracts.md`, `quality-gates.md`

5a. Add "Empirical Items Classification" row to Stage 6->7 contract table in `artifact-contracts.md`:
- Place after "CODE_COMPLETE Items" row
- Required = YES

5b. Add "Empirical-Items Tracking Template" section to `artifact-contracts.md`:
- Place after "Contract Summary Matrix" section
- Template with table columns: FR/AC ID, AC Summary, Classification, Justification, Validation Method
- Summary statistics block
- Classification rules (structural vs. empirical definitions with 2+ examples each)
- Integration notes with Light Mode applicability
- Add `<!-- retros c8f2, k4m9 -->` annotation

5c. Add blocking criterion to Gate 7 in `quality-gates.md`:
- Require empirical-items classification section in UAT test plan
- Every PRD AC classified; empirical items have documented validation methods
- Place after "All pending empirical validations from Stage 6..." item
- Severity: `[blocking]`

**Dependency**: US-01 (shares UAT stage context).

### Step 6: US-05 -- Derived Artifact Regeneration (M4)

**Files**: `pipeline-stages.md`, `quality-gates.md`

6a. Update Developer validator in Stage 6 DoD Validators in `pipeline-stages.md`:
- Add "derived artifacts regenerated from current sources"
- Require "Derived Artifacts" section in DoD review (columns: derived artifact path, source file(s), regeneration status)

6b. Insert step 5 "Regenerate derived artifacts" into Stage 6 Sub-Flow in `pipeline-stages.md`:
- Place after step 4 (Technical Writer), before current step 5 (Commit suggestion)
- 4-substep process: identify, regenerate, verify (no unexpected diffs), document
- Light Mode applicability note
- Add `<!-- retro c8f2 -->` annotation
- Renumber subsequent steps

6c. Add blocking criterion to Gate 6 in `quality-gates.md`:
- Require derived artifact regeneration confirmation and documentation
- Place after "Empirical validation requirements identified..." item
- Severity: `[blocking]`
- Add `<!-- retro c8f2 -->` annotation

**Dependency**: None (independent of Steps 2-5, but sequenced last per milestone ordering).

### Step 7: Cross-story verification pass

Walk every test case from all 5 stories (TC-01a-1 through TC-12b-2) by inspecting the modified files. This is the structural verification gate -- every AC must be traceable to its target file location.

**Dependency**: Steps 2-6 complete.

### Step 8: Dogfooding validation (P0 UAT gate)

Run a BUG_FIX pipeline through the hardened stages (Design, Plan, UAT minimum) per PRD Section 2 dogfooding criteria. Verify:

- Phantom reference WARNING fires at Design DoD when non-existent paths are cited without `[PLANNED]`
- Dev entry gate blocks when phantom references remain unresolved
- Capacity matrix and coverage matrix are validated at Plan stage
- Shared-module review checkpoint fires at UAT
- Empirical-items classification is required at UAT
- Derived artifact regeneration is checked at Dev DoD
- No regressions in non-modified stages

**This is a P0 gate. The hardened stages do not ship without dogfooding.**

**Dependency**: Step 7 complete.

---

## 5. Coverage Matrix

| PRD FR-ID | FR Description | Planned Task(s) | Story ID(s) | Status |
|-----------|---------------|------------------|-------------|--------|
| FR-01 | Shared-module review checkpoint in UAT stage | Step 4a, 4b | US-01 | Planned |
| FR-02 | Shared-module review guidance in QA SKILL.md | Step 4c | US-01 | Planned |
| FR-03 | Empirical-items tracking template in artifact-contracts | Step 5a, 5b | US-02 | Planned |
| FR-04 | Empirical-items tracking in UAT DoD validator | Step 5c | US-02 | Planned |
| FR-05 | Phantom reference WARNING at Design DoD | Step 2a | US-03 | Planned |
| FR-06 | Filename reconciliation BLOCK at Dev entry | Step 2b | US-03 | Planned |
| FR-07 | Capacity matrix in Plan template | Step 3a | US-04 | Planned |
| FR-08 | Coverage matrix in Plan template | Step 3a | US-04 | Planned |
| FR-09 | Mandatory matrix validation in Plan stage | Step 3b, 3c | US-04 | Planned |
| FR-10 | Two-tier capacity threshold (80% warn, 100% block) | Step 3c, 3d | US-04 | Planned |
| FR-11 | Derived artifact regeneration checklist at Dev DoD | Step 6a, 6b | US-05 | Planned |
| FR-12 | Derived artifact regeneration validator criterion | Step 6c | US-05 | Planned |

**Unmapped FRs**: None. All 12 FRs mapped to at least one planned task.

---

## 6. Deployment Approach

- **Branching**: Feature branch `feat/stage-health-hardening` from `main`
- **Commit strategy**: One conventional commit per story (5 commits total), enabling clean revert if any story causes regression
  - `feat: Add phantom reference detection and filename reconciliation (US-03)`
  - `feat: Add plan stage capacity and coverage guardrails (US-04)`
  - `feat: Add shared-module review at UAT stage (US-01)`
  - `feat: Add empirical-items tracking at UAT stage (US-02)`
  - `feat: Add derived artifact regeneration at dev DoD (US-05)`
- **PR**: Single PR with all 5 commits, referencing the PRD and retro sources c8f2 and k4m9
- **Post-merge**: No schema changes, no config migration needed. Changes take effect on next pipeline run.

---

## 7. Risks and Contingencies

| Risk | Likelihood | Impact | Contingency |
|------|-----------|--------|-------------|
| Step renumbering in pipeline-stages.md introduces inconsistencies across stories that modify the same file | Medium | High | US-03 and US-04 modify different stages (Stage 6 entry vs Stage 5 sub-flow); US-01 modifies Stage 7; US-05 modifies Stage 6 sub-flow. Execute US-03 before US-05 since both touch Stage 6 but different sections. Verify numbering after each story. |
| Added gate criteria slow pipeline execution without proportionate quality gain | Medium | Medium | Monitor first-try pass rates over 3 pipeline runs post-deployment. If pass rates do not improve, revisit gate severity per PRD risk table. |
| Token budget breach -- NFR-04 limits per-stage context growth to 500 tokens | Medium | Medium | Measure line counts after each story. If any stage exceeds budget, compress wording. Imperative numbered steps are token-efficient by design. |
| Concurrent edits to target files from other work | Low | High | All work goes through the delivery pipeline on a feature branch. No concurrent feature branches should touch these reference files. |
| Dogfooding BUG_FIX pipeline reveals gate change defects | Medium | Medium | Per PRD, fix defect and re-run dogfooding. Budget time for one defect cycle. |
| Capacity matrix template adds overhead that teams shortcut with placeholders | Medium | Low | FR-10 threshold validation catches the worst case (>100% allocation). Reasonableness checks deferred to future iteration per PRD assumptions. |

---

## 8. Dogfooding Plan

**What**: Run a BUG_FIX pipeline through the hardened delivery-flow stages on this repo.

**Why**: PRD Section 2 declares dogfooding as a P0 UAT gate. The hardened stages must be validated by running an actual pipeline through them.

**Pipeline to run**: BUG_FIX project type exercising at minimum: Design, Plan, and UAT stages.

**What to verify**:

- [ ] Design stage: Phantom reference WARNING fires for non-existent paths without `[PLANNED]` annotation
- [ ] Design stage: `[PLANNED]` annotated paths are exempt from phantom detection
- [ ] Plan stage: Capacity matrix and coverage matrix are required (or waived for BUG_FIX per FR-07/08)
- [ ] Plan stage: Capacity threshold validation functions (>80% warn, >100% block)
- [ ] Dev entry: Filename reconciliation gate blocks on unresolved phantom references
- [ ] Dev stage: Derived artifact regeneration step is present and Developer validator enforces it
- [ ] UAT stage: Shared-module review checkpoint fires
- [ ] UAT stage: Empirical-items classification is required in test plan
- [ ] No regressions in non-targeted stages (Idea, Architect, Development flow)

**Success criteria** (per PRD): Pipeline reaches completion without regressions caused by the gate changes. Failures unrelated to gate changes do not count. If the pipeline fails due to a gate change defect, fix and re-run.

---

## 9. Plugin-Dev Skill Loading Requirement

**Mandatory**: Load `plugin-dev:skill-development` before any file modifications begin.

Files modified in this sprint include:
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` (US-01, US-03, US-04, US-05)
- `delivery-team/skills/delivery-flow/references/quality-gates.md` (US-02, US-03, US-04, US-05)
- `delivery-team/skills/delivery-flow/references/artifact-contracts.md` (US-02)
- `delivery-team/skills/delivery-flow/references/project-templates.md` (US-04)
- `delivery-team/skills/quality/SKILL.md` (US-01)

All are plugin components. The plugin-dev skill provides conventions for reference file structure, section ordering, and annotation format that must be followed.

---

## Sprint Summary

| Item | Detail |
|------|--------|
| Sprint goal | Harden Design, Plan, UAT, and Dev stages to raise first-try pass rates and eliminate rework from retros c8f2/k4m9 |
| Stories committed | 5 (US-01 M, US-02 M, US-03 S, US-04 M, US-05 S) |
| Capacity | 2.0L equivalent -- 83% of 80% ceiling, within bounds |
| Files modified | 5 existing reference/skill files (markdown-only, NFR-01 compliant) |
| Key constraint | No new scripts, no schema changes, no config keys -- additive markdown edits only |
| Validation gate | Dogfooding (P0) -- BUG_FIX pipeline through hardened stages |
| Plugin-dev skill required | `plugin-dev:skill-development` (must load before any file edits) |
| Deployment | Feature branch, 5 conventional commits (one per story), single PR to main |

---

*"The way is shut. It was made by those who are Dead, and the Dead keep it." But these gates -- these we open ourselves, with clear criteria and honest measurement. The fellowship carries 12 functional requirements across 5 stages, and not one shall be left behind. The pack is balanced now, and we march at dawn.*
