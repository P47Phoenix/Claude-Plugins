# User Stories: Stage Health Hardening

**Version**: 1.0
**Date**: 2026-03-29
**Author**: Product Owner (Gandalf)
**Source PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Source Design**: `.delivery/artifacts/03-design/ux/user-flows.md` v1.0

> "A product owner is never late, nor early. They prioritize precisely when they mean to."

---

## Story Index

| Story | Milestone | Points | FRs Covered |
|-------|-----------|--------|-------------|
| US-01 | M1 | L | FR-01, FR-02 |
| US-02 | M1 | L | FR-03, FR-04 |
| US-03 | M2 | M | FR-05, FR-06 |
| US-04 | M3 | L | FR-07, FR-08, FR-09, FR-10 |
| US-05 | M4 | S | FR-11, FR-12 |

**Total**: 5 stories (1 per milestone, M1 split into 2 due to scope)

---

## US-01: Shared-Module Review at UAT

**Milestone**: M1 -- UAT Stage Hardening
**Story Points**: L
**Retro Sources**: c8f2, k4m9

### Description

**As a** pipeline user (P1) running delivery-flow on this repo,
**I want** the UAT stage to include a shared-module review checkpoint that identifies files referenced across multiple stage artifacts and verifies test coverage for each consuming context,
**So that** changes touching shared modules are caught at UAT rather than surfacing as integration failures post-pipeline.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-01a | **Given** a pipeline run where Development artifacts modify a shared module (a file referenced by path or name in 2+ stage artifacts across the current pipeline run), **When** the UAT stage DoD is evaluated, **Then** the DoD checklist includes a "shared-module review" item that requires listing all consuming contexts and their test status | structural |
| AC-01b | **Given** the UAT sub-flow in `pipeline-stages.md`, **When** a new step 5 "Shared-module review" is inserted after step 4 (Exploratory testing sessions) and before the current step 5 (Invoke Supporting Agents), **Then** the step includes the shared-module definition, identification method, review requirements, output location, and Light Mode applicability, and all subsequent steps are renumbered | structural |
| AC-01c | **Given** the Stage 7 DoD Validators section in `pipeline-stages.md`, **When** the QA Engineer validator is updated, **Then** the validator description includes "shared-module review complete (if shared modules were modified)" | structural |
| AC-02a | **Given** the QA skill is loaded for a UAT validation, **When** the QA sub-agent checks shared-module changes, **Then** `quality/SKILL.md` contains a "Shared-Module Review Protocol" section with: definition, identification steps (5-step process using Glob/Read), review checklist (4 items), and output format template | structural |
| AC-02b | **Given** the new section in `quality/SKILL.md`, **When** it is inserted, **Then** it is placed after the "Empirical Validation and CODE_COMPLETE Status" section and before the "Sub-Agent Interface" section, and no existing content is removed or modified | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| TC-01a-1 | AC-01a | Read `pipeline-stages.md` Stage 7 DoD checklist and verify "shared-module review" item exists | Checklist contains shared-module review item with consuming-contexts and test-status requirements |
| TC-01a-2 | AC-01a | Verify the shared-module definition matches PRD: "file referenced by path or name in 2+ stage artifacts across the current pipeline run" | Definition text matches exactly |
| TC-01b-1 | AC-01b | Read `pipeline-stages.md` Stage 7 Sub-Flow and verify step 5 is "Shared-module review" | Step 5 exists with SEQUENTIAL tag, required marker, quality skill reference, definition, identification, review, output, and Light Mode note |
| TC-01b-2 | AC-01b | Count Stage 7 Sub-Flow steps and verify sequential numbering | Steps are numbered consecutively with no gaps or duplicates; prior step 5+ are incremented by 1 |
| TC-01c-1 | AC-01c | Read `pipeline-stages.md` Stage 7 DoD Validators and find QA Engineer entry | QA Engineer validator includes "shared-module review complete (if shared modules were modified)" |
| TC-02a-1 | AC-02a | Read `quality/SKILL.md` and verify "Shared-Module Review Protocol" section exists | Section contains Definition, Identification Steps (5 steps), Review Checklist (4 items), and Output Format subsections |
| TC-02a-2 | AC-02a | Verify the identification steps reference Glob/Read tools | Steps 1-5 include Glob and Read tool references for artifact scanning |
| TC-02b-1 | AC-02b | Verify section placement in `quality/SKILL.md` | Section appears after "Empirical Validation and CODE_COMPLETE Status" and before "Sub-Agent Interface" |
| TC-02b-2 | AC-02b | Diff `quality/SKILL.md` and verify no existing content removed | Only additive changes; no deletions in existing sections |

### Dependencies

- None (first story in M1)

### FR Traceability

| FR | Covered By |
|----|------------|
| FR-01 | AC-01a, AC-01b, AC-01c |
| FR-02 | AC-02a, AC-02b |

---

## US-02: Empirical-Items Tracking at UAT

**Milestone**: M1 -- UAT Stage Hardening
**Story Points**: L
**Retro Sources**: c8f2, k4m9

### Description

**As a** QA sub-agent (P2) performing UAT validation,
**I want** a standardized template for classifying each acceptance criterion as structural or empirical, with the classification enforced as a mandatory section in the UAT test plan,
**So that** empirical items requiring runtime validation are explicitly tracked and not accidentally treated as structural pass-by-inspection items.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-03a | **Given** a UAT stage execution, **When** the UAT sub-agent evaluates acceptance criteria, **Then** an empirical-items tracking section is produced within the UAT test plan (`.delivery/artifacts/07-uat/qa/test-plan.md`) using the template from `artifact-contracts.md`, classifying each AC as "structural" or "empirical" with justification | structural |
| AC-03b | **Given** the `artifact-contracts.md` Stage 6 to Stage 7 contract table, **When** the table is updated, **Then** a new row "Empirical Items Classification / YES / Classification of each AC as structural or empirical with justification" is added after the "CODE_COMPLETE Items" row | structural |
| AC-03c | **Given** `artifact-contracts.md`, **When** the Empirical-Items Tracking Template section is added, **Then** it appears after the "Contract Summary Matrix" section and contains: template with table columns (FR/AC ID, summary, classification, justification, validation method), summary statistics block, classification rules (structural vs. empirical definitions), and integration notes including Light Mode applicability | structural |
| AC-04a | **Given** a UAT stage DoD submission, **When** the validator checks completeness, **Then** the Gate 7 checklist in `quality-gates.md` includes a blocking criterion requiring the empirical-items classification section to be present in the UAT test plan with every PRD AC classified and empirical items having documented validation methods | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| TC-03a-1 | AC-03a | Read `artifact-contracts.md` and verify the empirical-items template specifies output location as a section within the UAT test plan | Template references `.delivery/artifacts/07-uat/qa/test-plan.md` as the output location (section, not standalone file) |
| TC-03b-1 | AC-03b | Read `artifact-contracts.md` Stage 6->7 table and verify "Empirical Items Classification" row exists | Row present with Required=YES and correct description |
| TC-03b-2 | AC-03b | Verify the new row appears after the "CODE_COMPLETE Items" row | Row ordering is correct in the table |
| TC-03c-1 | AC-03c | Read the Empirical-Items Tracking Template section and verify table columns | Template contains columns: FR/AC ID, Acceptance Criterion (summary), Classification, Justification, Validation Method |
| TC-03c-2 | AC-03c | Verify classification rules define both "structural" and "empirical" with examples | Both definitions present with at least 2 examples each |
| TC-03c-3 | AC-03c | Verify Light Mode applicability note is present | Section states "Applies to all project types including BUG_FIX and DOCS_ONLY" |
| TC-03c-4 | AC-03c | Verify retro traceability annotation exists | Section contains `<!-- retros c8f2, k4m9 -->` or `<!-- retro k4m9 -->` annotation |
| TC-04a-1 | AC-04a | Read `quality-gates.md` Gate 7 checklist and verify empirical-items criterion exists | Blocking criterion present requiring empirical-items classification section with full coverage |
| TC-04a-2 | AC-04a | Verify the criterion is marked `[blocking]` | Severity tag is `[blocking]`, not `[warning]` |
| TC-04a-3 | AC-04a | Verify criterion placement after existing empirical validations item | New criterion appears after "All pending empirical validations from Stage 6 included as mandatory UAT test cases" |

### Dependencies

- US-01 (shared UAT stage context; both modify Stage 7 sub-flow area)

### FR Traceability

| FR | Covered By |
|----|------------|
| FR-03 | AC-03a, AC-03b, AC-03c |
| FR-04 | AC-04a |

---

## US-03: Phantom Reference Detection and Filename Reconciliation

**Milestone**: M2 -- Design Stage Hardening
**Story Points**: M
**Retro Sources**: k4m9

### Description

**As a** delivery team sub-agent (P2) receiving artifacts from upstream stages,
**I want** phantom file references (paths cited in Design artifacts that do not exist on disk) to be surfaced as warnings at Design DoD and blocked at Dev stage entry unless accounted for in the sprint plan,
**So that** I do not waste effort on downstream work built on references to non-existent files.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-05a | **Given** a Design stage artifact references file path `X`, **When** file `X` does not exist on disk at DoD validation time and is not annotated with `[PLANNED]`, **Then** the Gate 3 checklist in `quality-gates.md` reports a WARNING-severity finding that is logged and surfaced to the author but does not block stage completion | empirical |
| AC-05b | **Given** a Design stage artifact references file path `X` annotated with `[PLANNED]`, **When** the Gate 3 phantom check runs, **Then** file `X` is exempt from phantom detection | empirical |
| AC-05c | **Given** the new checklist item in `quality-gates.md` Gate 3, **When** it is added, **Then** it is placed after "Design aligns with PRD requirements" and includes the `[warning]` severity tag and `<!-- retro k4m9 -->` annotation | structural |
| AC-06a | **Given** the pipeline transitions from Architect to Development, **When** the Dev stage entry gate runs, **Then** all file paths referenced in Design (Stage 3) and Architect (Stage 4) artifacts are checked: paths existing on disk pass; paths listed in the sprint plan as planned deliverables pass; all other missing paths block Dev entry with a list of non-existent references | empirical |
| AC-06b | **Given** a file path annotated `[PLANNED]` in Design artifacts, **When** the Dev entry reconciliation gate runs, **Then** the `[PLANNED]` annotation is NOT accepted as an exemption -- the file must either exist on disk or appear in the sprint plan | empirical |
| AC-06c | **Given** the new entry condition in `pipeline-stages.md` Stage 6, **When** it is added, **Then** it includes: 5-step reconciliation process, pass/fail criteria, resolution guidance, Light Mode applicability note, and `<!-- retro k4m9 -->` annotation | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| TC-05a-1 | AC-05a | Read `quality-gates.md` Gate 3 checklist and verify phantom reference criterion exists with `[warning]` severity | Criterion present with WARNING severity, not blocking |
| TC-05a-2 | AC-05a | Verify the criterion specifies that warnings do NOT block stage completion | Text explicitly states does not block completion |
| TC-05b-1 | AC-05b | Verify the criterion grants `[PLANNED]` annotated paths exemption from phantom detection | Text includes `[PLANNED]` exemption language |
| TC-05c-1 | AC-05c | Verify criterion placement in Gate 3 | Item appears after "Design aligns with PRD requirements" |
| TC-05c-2 | AC-05c | Verify retro annotation | Criterion contains `<!-- retro k4m9 -->` |
| TC-06a-1 | AC-06a | Read `pipeline-stages.md` Stage 6 Entry Conditions and verify filename reconciliation gate exists | Entry condition present with Glob/Read extraction, disk existence check, sprint plan cross-reference, and blocking behavior |
| TC-06a-2 | AC-06a | Verify the gate checks BOTH Design and Architect artifacts | Text references `.delivery/artifacts/03-design/` and `.delivery/artifacts/04-architect/` |
| TC-06a-3 | AC-06a | Verify blocking behavior on FAIL | Text states "Any FAIL blocks Dev entry" with list of non-existent references |
| TC-06b-1 | AC-06b | Verify `[PLANNED]` is NOT an exemption at Dev entry | Text explicitly states `[PLANNED]` annotations are not accepted as exemptions at Dev entry |
| TC-06c-1 | AC-06c | Verify Light Mode applicability | Entry condition states "Applies to all project types including BUG_FIX and DOCS_ONLY" |
| TC-06c-2 | AC-06c | Verify the reconciliation includes resolution guidance | Text includes resolution steps: create files, add to sprint plan, or remove references |

### Dependencies

- None (independent milestone, though Design-stage changes should ship before M3/M4 for cascading benefit)

### FR Traceability

| FR | Covered By |
|----|------------|
| FR-05 | AC-05a, AC-05b, AC-05c |
| FR-06 | AC-06a, AC-06b, AC-06c |

---

## US-04: Plan Stage Capacity and Coverage Guardrails

**Milestone**: M3 -- Plan Stage Guardrails
**Story Points**: L
**Retro Sources**: c8f2, k4m9

### Description

**As a** pipeline user (P1) authoring sprint plans,
**I want** the Plan stage to require a capacity matrix (team members x hours x utilization) and a coverage matrix (PRD FRs mapped to tasks), with a two-tier capacity threshold (>80% warns, >100% blocks),
**So that** I am prevented from overcommitting and from shipping plans that leave PRD requirements unmapped.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-07a | **Given** a Plan stage artifact is being authored, **When** the sprint plan is produced, **Then** the plan includes a capacity matrix table with columns: Team Member, Role, Available Hours, Allocated Hours, Utilization % | structural |
| AC-07b | **Given** the capacity matrix template in `project-templates.md`, **When** it is added, **Then** it appears within a new "Sprint Plan Mandatory Sections" section at the end of the file, includes the retro annotation `<!-- retro c8f2 -->`, and notes that Light Mode (BUG_FIX, DOCS_ONLY) waives the capacity matrix | structural |
| AC-08a | **Given** a Plan stage artifact is being authored, **When** the sprint plan is produced, **Then** the plan includes a coverage matrix mapping every PRD FR-ID to at least one planned task, with no FR left unmapped | structural |
| AC-08b | **Given** the coverage matrix template in `project-templates.md`, **When** it is added, **Then** it appears within the same "Sprint Plan Mandatory Sections" section as the capacity matrix, includes the retro annotation `<!-- retro c8f2 -->`, and notes that Light Mode waives the coverage matrix | structural |
| AC-09a | **Given** a Plan stage DoD submission, **When** the validator checks the plan artifact, **Then** the Scrum Bag validator in `pipeline-stages.md` rejects the submission if either the capacity matrix or coverage matrix is missing | structural |
| AC-09b | **Given** the Plan sub-flow in `pipeline-stages.md`, **When** a new step 4 "Matrix validation" is inserted after step 3 (Invoke Supporting Agents), **Then** the step validates capacity matrix presence and completeness, coverage matrix presence with all FRs mapped (unmapped FR = BLOCKING), and includes Light Mode waiver for BUG_FIX/DOCS_ONLY | structural |
| AC-10a | **Given** a sprint plan where total allocated hours exceed 80% but do not exceed 100% of total available hours, **When** the Plan stage DoD is evaluated, **Then** a WARNING is emitted stating the utilization percentage, and the plan can pass DoD only after the warning is acknowledged with brief justification | structural |
| AC-10b | **Given** a sprint plan where total allocated hours exceed 100% of total available hours, **When** the Plan stage DoD is evaluated, **Then** a BLOCKING finding is emitted, and the plan cannot pass DoD until allocation is reduced to <=100% or the PO provides explicit sign-off with justification | structural |
| AC-10c | **Given** the Gate 5 checklist in `quality-gates.md`, **When** the existing "Commitment does not exceed 80% of available capacity [blocking]" is replaced, **Then** it is replaced with the two-tier model: >80% WARNING with acknowledgment, >100% BLOCKING with reduction or PO sign-off, and Light Mode applicability note | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| TC-07a-1 | AC-07a | Read `project-templates.md` and verify capacity matrix template exists with required columns | Template contains columns: Team Member, Role, Available Hours, Allocated Hours, Utilization % |
| TC-07a-2 | AC-07a | Verify Total row exists in the template | Template includes a Total summary row |
| TC-07b-1 | AC-07b | Verify "Sprint Plan Mandatory Sections" section exists at end of file | Section heading present, positioned after all project type templates |
| TC-07b-2 | AC-07b | Verify Light Mode waiver for capacity matrix | Text states "WAIVED" for BUG_FIX and DOCS_ONLY |
| TC-07b-3 | AC-07b | Verify retro annotation | Section contains `<!-- retro c8f2 -->` |
| TC-08a-1 | AC-08a | Read `project-templates.md` and verify coverage matrix template exists with required columns | Template contains columns: PRD FR-ID, FR Description (summary), Planned Task(s), Story ID(s), Status |
| TC-08a-2 | AC-08a | Verify "Unmapped FRs" section exists in template | Template includes an "Unmapped FRs" annotation area |
| TC-08b-1 | AC-08b | Verify coverage matrix is in same "Sprint Plan Mandatory Sections" as capacity matrix | Both templates under same parent section heading |
| TC-08b-2 | AC-08b | Verify Light Mode waiver for coverage matrix | Text states "WAIVED" for BUG_FIX and DOCS_ONLY |
| TC-09a-1 | AC-09a | Read `pipeline-stages.md` Stage 5 DoD Validators and verify Scrum Bag validator includes matrix requirements | Scrum Bag validator text includes "capacity matrix present with utilization calculated, coverage matrix present with all PRD FRs mapped to at least one task" |
| TC-09a-2 | AC-09a | Verify capacity threshold language in Scrum Bag validator | Validator text includes ">80% utilization emits WARNING requiring acknowledgment; >100% utilization is BLOCKING" |
| TC-09b-1 | AC-09b | Read `pipeline-stages.md` Stage 5 Sub-Flow and verify step 4 "Matrix validation" exists | Step 4 present with SEQUENTIAL tag, required marker, capacity and coverage validation items, and Light Mode waiver |
| TC-09b-2 | AC-09b | Verify unmapped FR is BLOCKING | Step states unmapped FR causes a BLOCKING finding |
| TC-09b-3 | AC-09b | Verify subsequent steps are renumbered | Steps after the new step 4 are consecutively numbered |
| TC-10a-1 | AC-10a | Read `quality-gates.md` Gate 5 and verify two-tier capacity threshold exists | Gate 5 contains >80% WARNING tier with acknowledgment requirement |
| TC-10b-1 | AC-10b | Verify >100% BLOCKING tier in Gate 5 | Gate 5 contains >100% BLOCKING tier with reduction or PO sign-off requirement |
| TC-10c-1 | AC-10c | Verify the old "80% blocking" criterion is REPLACED, not duplicated | No remaining "Commitment does not exceed 80% of available capacity [blocking]" text in Gate 5 |
| TC-10c-2 | AC-10c | Verify Light Mode applicability on capacity threshold | Threshold section states "Applies to all project types" |
| TC-10c-3 | AC-10c | Verify retro annotations | Both quality-gates.md and pipeline-stages.md changes contain `<!-- retros c8f2, k4m9 -->` |

### Dependencies

- None (independent milestone)

### FR Traceability

| FR | Covered By |
|----|------------|
| FR-07 | AC-07a, AC-07b |
| FR-08 | AC-08a, AC-08b |
| FR-09 | AC-09a, AC-09b |
| FR-10 | AC-10a, AC-10b, AC-10c |

---

## US-05: Derived Artifact Regeneration at Dev DoD

**Milestone**: M4 -- Dev Stage DoD
**Story Points**: S
**Retro Sources**: c8f2

### Description

**As a** pipeline maintainer (P3) ensuring gate criteria are unambiguous,
**I want** the Dev stage DoD to include an explicit "regenerate derived artifacts" checklist item and a corresponding blocking validator criterion,
**So that** derived artifacts (generated docs, compiled schemas, transformed configs) never drift from their source files when Development modifies those sources.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-11a | **Given** the Development stage modifies source files that have derived artifacts, **When** the Dev stage DoD is evaluated, **Then** the Developer validator in `pipeline-stages.md` includes "derived artifacts regenerated from current sources" and requires a "Derived Artifacts" section in the DoD review listing each derived artifact path, source file(s), and regeneration status | structural |
| AC-11b | **Given** the Dev sub-flow in `pipeline-stages.md`, **When** a new step 5 "Regenerate derived artifacts" is inserted after step 4 (Technical Writer) and before the current step 5 (Commit suggestion), **Then** the step includes: identification of derived artifacts, regeneration, verification (no unexpected diffs), documentation requirement, and Light Mode applicability note with `<!-- retro c8f2 -->` | structural |
| AC-12a | **Given** a Dev stage DoD submission, **When** the validator checks artifact freshness, **Then** the Gate 6 checklist in `quality-gates.md` includes a blocking criterion requiring confirmation that derived artifacts have been regenerated and documented in the story's DoD review | structural |
| AC-12b | **Given** the new criterion in Gate 6, **When** it is added, **Then** it is placed after "Empirical validation requirements identified..." and includes the `[blocking]` severity tag and `<!-- retro c8f2 -->` annotation | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| TC-11a-1 | AC-11a | Read `pipeline-stages.md` Stage 6 DoD Validators and verify Developer validator includes derived artifact regeneration | Developer validator text includes "derived artifacts regenerated from current sources" |
| TC-11a-2 | AC-11a | Verify "Derived Artifacts" section requirement in DoD review | Developer validator specifies a "Derived Artifacts" section with columns: derived artifact path, source file(s), regeneration status |
| TC-11a-3 | AC-11a | Verify regeneration status values are defined | Accepted statuses include "regenerated" and "not applicable" |
| TC-11b-1 | AC-11b | Read `pipeline-stages.md` Stage 6 Sub-Flow and verify step 5 "Regenerate derived artifacts" exists | Step 5 present with SEQUENTIAL tag, required marker, 4-substep process (identify, regenerate, verify, document) |
| TC-11b-2 | AC-11b | Verify Light Mode applicability | Step includes "Applies to all project types" note |
| TC-11b-3 | AC-11b | Verify subsequent steps are renumbered | Current step 5 (Commit suggestion) becomes step 6; no gaps |
| TC-11b-4 | AC-11b | Verify retro annotation | Step contains `<!-- retro c8f2 -->` |
| TC-12a-1 | AC-12a | Read `quality-gates.md` Gate 6 checklist and verify derived artifact regeneration criterion exists | Blocking criterion present requiring regeneration confirmation and documentation |
| TC-12a-2 | AC-12a | Verify the criterion is marked `[blocking]` | Severity tag is `[blocking]` |
| TC-12b-1 | AC-12b | Verify criterion placement in Gate 6 | Item appears after "Empirical validation requirements identified..." |
| TC-12b-2 | AC-12b | Verify retro annotation | Criterion contains `<!-- retro c8f2 -->` |

### Dependencies

- None (independent milestone; Dev stage changes do not conflict with M1-M3 target files)

### FR Traceability

| FR | Covered By |
|----|------------|
| FR-11 | AC-11a, AC-11b |
| FR-12 | AC-12a, AC-12b |

---

## Cross-Story Dependency Map

```
US-01 (M1: Shared-module review)
  └──> US-02 (M1: Empirical-items tracking) [same stage, shared context]

US-03 (M2: Phantom refs) ── independent

US-04 (M3: Plan guardrails) ── independent

US-05 (M4: Dev DoD) ── independent
```

**Recommended execution order**: M2 (US-03) first to get Design-stage fixes cascading early, then M3 (US-04), then M1 (US-01, US-02), then M4 (US-05). However, all milestones target different stages and can be parallelized if capacity allows.

---

## Full FR Traceability Matrix

| FR | Story | ACs |
|----|-------|-----|
| FR-01 | US-01 | AC-01a, AC-01b, AC-01c |
| FR-02 | US-01 | AC-02a, AC-02b |
| FR-03 | US-02 | AC-03a, AC-03b, AC-03c |
| FR-04 | US-02 | AC-04a |
| FR-05 | US-03 | AC-05a, AC-05b, AC-05c |
| FR-06 | US-03 | AC-06a, AC-06b, AC-06c |
| FR-07 | US-04 | AC-07a, AC-07b |
| FR-08 | US-04 | AC-08a, AC-08b |
| FR-09 | US-04 | AC-09a, AC-09b |
| FR-10 | US-04 | AC-10a, AC-10b, AC-10c |
| FR-11 | US-05 | AC-11a, AC-11b |
| FR-12 | US-05 | AC-12a, AC-12b |

**All 12 FRs covered. No gaps.**

---

## Target Files by Story

| Story | Files Modified |
|-------|----------------|
| US-01 | `delivery-team/skills/delivery-flow/references/pipeline-stages.md`, `delivery-team/skills/quality/SKILL.md` |
| US-02 | `delivery-team/skills/delivery-flow/references/artifact-contracts.md`, `delivery-team/skills/delivery-flow/references/quality-gates.md` |
| US-03 | `delivery-team/skills/delivery-flow/references/quality-gates.md`, `delivery-team/skills/delivery-flow/references/pipeline-stages.md` |
| US-04 | `delivery-team/skills/delivery-flow/references/project-templates.md`, `delivery-team/skills/delivery-flow/references/pipeline-stages.md`, `delivery-team/skills/delivery-flow/references/quality-gates.md` |
| US-05 | `delivery-team/skills/delivery-flow/references/pipeline-stages.md`, `delivery-team/skills/delivery-flow/references/quality-gates.md` |
