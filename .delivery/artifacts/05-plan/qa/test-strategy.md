# Test Strategy: Stage Health Hardening

**Version**: 1.0
**Author**: Legolas (QA Engineer, delivery-team)
**Date**: 2026-03-29
**Status**: Implementation-Ready
**Traces To**: PRD v1.1, User Stories v1.0 (5 stories, 22 ACs, 45 test cases)

> *"That bug still only counts as one."*
>
> This test strategy covers 5 stories across 4 milestones, all targeting markdown-only changes to delivery-flow reference files. The testing approach is predominantly structural inspection -- we are verifying that the right words appear in the right places in the right files. The empirical items (AC-05a, AC-05b, AC-06a, AC-06b) require pipeline runtime validation and are addressed in the dogfooding plan.

---

## 1. Testing Philosophy

Three principles govern this strategy:

1. **Structural changes get structural tests.** 18 of 22 ACs are structural -- they require verifying that specific text, sections, and table rows exist in specific files at specific locations. These are inspected via Read/Grep, not by running a pipeline.
2. **Empirical changes get pipeline runs.** 4 ACs (AC-05a, AC-05b, AC-06a, AC-06b) define runtime gate behavior that can only be validated by running a pipeline through the affected stages. These are covered by the dogfooding plan.
3. **Regression is non-negotiable.** Every target file is shared across multiple pipeline stages. Changes to `pipeline-stages.md` or `quality-gates.md` must not break existing stage behavior. Non-modified stages must still pass their gates.

---

## 2. Test Approach per Story

### 2.1 US-01: Shared-Module Review at UAT

**Approach**: Structural inspection

**Target files**: `pipeline-stages.md`, `quality/SKILL.md`

**Rationale**: All 5 ACs (AC-01a through AC-02b) are typed "structural." Each requires verifying that specific content was inserted at a specific location in the target file, with no existing content removed or modified. Pure file inspection.

| AC | Test Approach | Inspection Method |
|----|--------------|-------------------|
| AC-01a | Read `pipeline-stages.md` Stage 7 DoD checklist, verify shared-module review item | Grep for "shared-module review" in Stage 7 DoD section |
| AC-01b | Read `pipeline-stages.md` Stage 7 Sub-Flow, verify step 5 insertion and renumbering | Read section, verify step numbering is consecutive, step 5 content matches spec |
| AC-01c | Read `pipeline-stages.md` Stage 7 DoD Validators, verify QA Engineer update | Grep for "shared-module review complete" in QA Engineer validator |
| AC-02a | Read `quality/SKILL.md`, verify Shared-Module Review Protocol section | Verify 4 subsections: Definition, Identification Steps (5), Review Checklist (4 items), Output Format |
| AC-02b | Read `quality/SKILL.md`, verify section placement | Confirm section appears after "Empirical Validation" and before "Sub-Agent Interface" |

**Regression concern**: Step renumbering in Stage 7 Sub-Flow. All subsequent step references in the file must be updated.

---

### 2.2 US-02: Empirical-Items Tracking at UAT

**Approach**: Structural inspection

**Target files**: `artifact-contracts.md`, `quality-gates.md`

**Rationale**: All 4 ACs (AC-03a through AC-04a) are typed "structural." Each verifies specific template content, table rows, or gate criteria in reference files.

| AC | Test Approach | Inspection Method |
|----|--------------|-------------------|
| AC-03a | Read `artifact-contracts.md`, verify empirical-items template references UAT test plan as output location | Grep for `.delivery/artifacts/07-uat/qa/test-plan.md` in template |
| AC-03b | Read `artifact-contracts.md` Stage 6->7 contract table, verify new row | Verify "Empirical Items Classification" row exists after "CODE_COMPLETE Items" |
| AC-03c | Read `artifact-contracts.md`, verify template section content | Verify table columns, classification rules, summary statistics, Light Mode note |
| AC-04a | Read `quality-gates.md` Gate 7, verify blocking criterion | Grep for empirical-items criterion with `[blocking]` tag |

**Regression concern**: `artifact-contracts.md` has existing contract tables and templates. New content must be purely additive.

---

### 2.3 US-03: Phantom Reference Detection and Filename Reconciliation

**Approach**: Mixed -- structural inspection (AC-05c, AC-06c) + empirical pipeline validation (AC-05a, AC-05b, AC-06a, AC-06b)

**Target files**: `quality-gates.md`, `pipeline-stages.md`

**Rationale**: This story contains the highest-risk changes. AC-05a/05b define runtime WARNING behavior at Design DoD, and AC-06a/06b define runtime BLOCKING behavior at Dev entry. These cannot be verified by reading files alone -- they require a pipeline run where phantom references are present and the gates fire correctly.

| AC | Test Approach | Inspection Method |
|----|--------------|-------------------|
| AC-05a | **Empirical** -- requires pipeline Design stage run with phantom references | Dogfooding plan step DF-3 |
| AC-05b | **Empirical** -- requires `[PLANNED]` annotated paths in Design artifacts | Dogfooding plan step DF-4 |
| AC-05c | Structural -- verify Gate 3 criterion placement and annotations | Read `quality-gates.md` Gate 3, verify `[warning]` tag and `<!-- retro k4m9 -->` |
| AC-06a | **Empirical** -- requires pipeline Dev entry with missing referenced files | Dogfooding plan step DF-5 |
| AC-06b | **Empirical** -- requires `[PLANNED]` annotated paths tested at Dev entry | Dogfooding plan step DF-6 |
| AC-06c | Structural -- verify Stage 6 entry condition content | Read `pipeline-stages.md` Stage 6, verify 5-step reconciliation, pass/fail criteria, Light Mode note |

**Regression concern**: Gate 3 and Stage 6 entry conditions are active for ALL project types. Changes must not introduce false positives on GREENFIELD projects where file creation is normal.

---

### 2.4 US-04: Plan Stage Capacity and Coverage Guardrails

**Approach**: Structural inspection

**Target files**: `project-templates.md`, `pipeline-stages.md`, `quality-gates.md`

**Rationale**: All 7 ACs (AC-07a through AC-10c) are typed "structural." They verify templates, validator text, step insertions, and gate criterion replacements.

| AC | Test Approach | Inspection Method |
|----|--------------|-------------------|
| AC-07a | Read `project-templates.md`, verify capacity matrix template columns | Verify: Team Member, Role, Available Hours, Allocated Hours, Utilization % |
| AC-07b | Read `project-templates.md`, verify "Sprint Plan Mandatory Sections" heading, placement, retro annotation, Light Mode waiver | Section at end of file, `<!-- retro c8f2 -->`, "WAIVED" for BUG_FIX/DOCS_ONLY |
| AC-08a | Read `project-templates.md`, verify coverage matrix template columns | Verify: PRD FR-ID, FR Description, Planned Task(s), Story ID(s), Status |
| AC-08b | Verify coverage matrix in same section as capacity matrix | Both under "Sprint Plan Mandatory Sections" |
| AC-09a | Read `pipeline-stages.md` Stage 5 DoD Validators, verify Scrum Bag validator | Grep for capacity and coverage matrix requirements |
| AC-09b | Read `pipeline-stages.md` Stage 5 Sub-Flow, verify step 4 insertion and renumbering | Step 4 "Matrix validation" with capacity/coverage checks, Light Mode waiver |
| AC-10a | Read `quality-gates.md` Gate 5, verify >80% WARNING tier | Verify acknowledgment requirement |
| AC-10b | Read `quality-gates.md` Gate 5, verify >100% BLOCKING tier | Verify reduction or PO sign-off requirement |
| AC-10c | Read `quality-gates.md` Gate 5, verify old criterion replaced | Grep confirms NO remaining "Commitment does not exceed 80% of available capacity [blocking]" |

**Regression concern**: AC-10c explicitly replaces an existing Gate 5 criterion. This is a modification, not an addition. Must verify the old text is gone AND the new text is present. Two-step verification.

---

### 2.5 US-05: Derived Artifact Regeneration at Dev DoD

**Approach**: Structural inspection

**Target files**: `pipeline-stages.md`, `quality-gates.md`

**Rationale**: All 4 ACs (AC-11a through AC-12b) are typed "structural." They verify validator text, step insertion, and gate criteria.

| AC | Test Approach | Inspection Method |
|----|--------------|-------------------|
| AC-11a | Read `pipeline-stages.md` Stage 6 DoD Validators, verify Developer validator | Grep for "derived artifacts regenerated from current sources" and "Derived Artifacts" section spec |
| AC-11b | Read `pipeline-stages.md` Stage 6 Sub-Flow, verify step 5 insertion and renumbering | Step 5 with 4 substeps, Light Mode note, `<!-- retro c8f2 -->` |
| AC-12a | Read `quality-gates.md` Gate 6, verify blocking criterion | Grep for derived artifact regeneration criterion with `[blocking]` tag |
| AC-12b | Read `quality-gates.md` Gate 6, verify placement after empirical validations item | Verify ordering and `<!-- retro c8f2 -->` annotation |

**Regression concern**: Stage 6 Sub-Flow step renumbering (same pattern as US-01 and US-04).

---

## 3. Test Coverage Matrix

Every AC mapped to its test cases and test approach.

### 3.1 US-01 (5 ACs, 9 TCs)

| AC | TC(s) | Approach | File Under Test |
|----|-------|----------|----------------|
| AC-01a | TC-01a-1, TC-01a-2 | Structural | `pipeline-stages.md` |
| AC-01b | TC-01b-1, TC-01b-2 | Structural | `pipeline-stages.md` |
| AC-01c | TC-01c-1 | Structural | `pipeline-stages.md` |
| AC-02a | TC-02a-1, TC-02a-2 | Structural | `quality/SKILL.md` |
| AC-02b | TC-02b-1, TC-02b-2 | Structural | `quality/SKILL.md` |

### 3.2 US-02 (4 ACs, 10 TCs)

| AC | TC(s) | Approach | File Under Test |
|----|-------|----------|----------------|
| AC-03a | TC-03a-1 | Structural | `artifact-contracts.md` |
| AC-03b | TC-03b-1, TC-03b-2 | Structural | `artifact-contracts.md` |
| AC-03c | TC-03c-1, TC-03c-2, TC-03c-3, TC-03c-4 | Structural | `artifact-contracts.md` |
| AC-04a | TC-04a-1, TC-04a-2, TC-04a-3 | Structural | `quality-gates.md` |

### 3.3 US-03 (6 ACs, 12 TCs)

| AC | TC(s) | Approach | File Under Test |
|----|-------|----------|----------------|
| AC-05a | TC-05a-1, TC-05a-2 | Structural + **Empirical (DF-3)** | `quality-gates.md` |
| AC-05b | TC-05b-1 | Structural + **Empirical (DF-4)** | `quality-gates.md` |
| AC-05c | TC-05c-1, TC-05c-2 | Structural | `quality-gates.md` |
| AC-06a | TC-06a-1, TC-06a-2, TC-06a-3 | Structural + **Empirical (DF-5)** | `pipeline-stages.md` |
| AC-06b | TC-06b-1 | Structural + **Empirical (DF-6)** | `pipeline-stages.md` |
| AC-06c | TC-06c-1, TC-06c-2 | Structural | `pipeline-stages.md` |

### 3.4 US-04 (7 ACs, 14 TCs)

| AC | TC(s) | Approach | File Under Test |
|----|-------|----------|----------------|
| AC-07a | TC-07a-1, TC-07a-2 | Structural | `project-templates.md` |
| AC-07b | TC-07b-1, TC-07b-2, TC-07b-3 | Structural | `project-templates.md` |
| AC-08a | TC-08a-1, TC-08a-2 | Structural | `project-templates.md` |
| AC-08b | TC-08b-1, TC-08b-2 | Structural | `project-templates.md` |
| AC-09a | TC-09a-1, TC-09a-2 | Structural | `pipeline-stages.md` |
| AC-09b | TC-09b-1, TC-09b-2, TC-09b-3 | Structural | `pipeline-stages.md` |
| AC-10a | TC-10a-1 | Structural | `quality-gates.md` |
| AC-10b | TC-10b-1 | Structural | `quality-gates.md` |
| AC-10c | TC-10c-1, TC-10c-2, TC-10c-3 | Structural | `quality-gates.md` |

### 3.5 US-05 (4 ACs, 10 TCs)

| AC | TC(s) | Approach | File Under Test |
|----|-------|----------|----------------|
| AC-11a | TC-11a-1, TC-11a-2, TC-11a-3 | Structural | `pipeline-stages.md` |
| AC-11b | TC-11b-1, TC-11b-2, TC-11b-3, TC-11b-4 | Structural | `pipeline-stages.md` |
| AC-12a | TC-12a-1, TC-12a-2 | Structural | `quality-gates.md` |
| AC-12b | TC-12b-1, TC-12b-2 | Structural | `quality-gates.md` |

### 3.6 Coverage Summary

| Metric | Count |
|--------|-------|
| Total ACs | 22 |
| ACs with structural tests | 22 (100%) |
| ACs requiring empirical validation | 4 (AC-05a, AC-05b, AC-06a, AC-06b) |
| Total test cases from stories | 45 |
| Total test cases mapped | 45 (100%) |
| Unmapped ACs | 0 |

---

## 4. Regression Testing Plan

### 4.1 Files Modified and Regression Scope

| File | Stories Modifying | Stages Affected | Regression Scope |
|------|-------------------|-----------------|-----------------|
| `pipeline-stages.md` | US-01, US-03, US-04, US-05 | Stage 5, 6, 7 | All 7 stage definitions, all sub-flows, all DoD validators, all entry conditions |
| `quality-gates.md` | US-02, US-03, US-04, US-05 | Gate 3, 5, 6, 7 | All 7 gate checklists |
| `artifact-contracts.md` | US-02 | Stage 6->7 contract | All contract tables, all templates |
| `project-templates.md` | US-04 | Plan stage | All project type templates |
| `quality/SKILL.md` | US-01 | UAT QA role | All existing skill sections |

### 4.2 Non-Modified Stages Regression Checks

These stages are NOT targeted by any story. After all changes, verify they are intact:

| Stage | Regression Check | Method |
|-------|-----------------|--------|
| Stage 1 (Idea) | Gate 1 checklist unchanged, Stage 1 sub-flow unchanged | Diff `quality-gates.md` and `pipeline-stages.md` -- zero changes in Stage 1 / Gate 1 sections |
| Stage 2 (Refine) | Gate 2 checklist unchanged, Stage 2 sub-flow unchanged | Diff -- zero changes in Stage 2 / Gate 2 sections |
| Stage 4 (Architect) | Gate 4 checklist unchanged, Stage 4 sub-flow unchanged | Diff -- zero changes in Stage 4 / Gate 4 sections |

### 4.3 Modified Stages Regression Checks

These stages receive new content. Verify existing content is preserved:

| Stage | What Must NOT Change | Verification |
|-------|---------------------|-------------|
| Stage 3 (Design) | All existing Gate 3 criteria remain; only additive change (new phantom ref WARNING criterion) | Count existing criteria before and after; all present, one new |
| Stage 5 (Plan) | All existing Gate 5 criteria remain except the explicit replacement (AC-10c); sub-flow steps before insertion point unchanged | Verify old "80% blocking" criterion is gone (intended), all other criteria present |
| Stage 6 (Dev) | All existing Gate 6 criteria remain; existing sub-flow steps before insertion point unchanged; existing entry conditions preserved | Count existing criteria and entry conditions before and after |
| Stage 7 (UAT) | All existing Gate 7 criteria remain; existing sub-flow steps before insertion point unchanged; existing DoD validators preserved | Verify all pre-existing validators still present with original text |

### 4.4 Cross-File Consistency Checks

| Check | Scope | Method |
|-------|-------|--------|
| Step numbering consistency | US-01 (Stage 7), US-04 (Stage 5), US-05 (Stage 6) | For each sub-flow, verify steps are numbered 1..N with no gaps or duplicates |
| Gate-to-stage alignment | Gates 3, 5, 6, 7 | Every gate criterion references a stage sub-flow step or validator that exists |
| Contract-to-gate alignment | Stage 6->7 contract | Every required contract artifact has a corresponding gate criterion |
| Retro annotations complete | All modified sections | Every change section contains the correct retro annotation (c8f2, k4m9, or both) per PRD traceability |

### 4.5 NFR Regression Checks

| NFR | Regression Check |
|-----|-----------------|
| NFR-01 (markdown-only) | Verify no `.py`, `.js`, `.sh` files created or modified in the changeset |
| NFR-02 (config v2.3 compat) | Verify no new keys added to config schema; no references to config keys not in v2.3 |
| NFR-03 (no pass rate regression) | Non-targeted stages (Idea, Architect, Development) have zero changes to their gates/sub-flows |
| NFR-04 (token budget) | Count added lines per stage; multiply by ~1.3 tokens/word, ~10 words/line; verify < 500 tokens per stage |
| NFR-05 (retro traceability) | Every modified section has inline retro annotation |

---

## 5. Dogfooding Test Plan

### 5.1 Objective

Run an actual delivery-flow pipeline through the hardened stages to validate that empirical ACs work at runtime and that structural changes do not cause regressions. Per PRD Section 2: "Dogfooding success is defined as: run a BUG_FIX pipeline that exercises at least the Design, Plan, and UAT stages."

### 5.2 Pipeline to Run

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Project type | BUG_FIX | PRD-specified; exercises Light Mode behavior for FR-07/08/09 waivers while keeping FR-01/05/06/10/11/12 active |
| Target stages | Design, Architect (transit), Plan, Development, UAT | Exercises all 4 milestones' target stages |
| Repo | This repo (Claude-Plugins) | Dogfooding on the repo being modified |
| Subject | A small BUG_FIX task touching at least one shared module | Exercises shared-module review (US-01) and derived artifact regeneration (US-05) |

### 5.3 Setup Preconditions

1. All 5 stories are implemented (markdown changes applied to all target files)
2. All 45 structural test cases pass
3. Branch is clean with no uncommitted changes
4. `.delivery/config.yml` is valid per schema v2.3

### 5.4 Execution Steps and Verification

| Step | Action | Verifies | Pass Criteria |
|------|--------|----------|--------------|
| DF-1 | Start BUG_FIX pipeline, reach Design stage | Pipeline infrastructure | Pipeline starts, project type detected as BUG_FIX |
| DF-2 | Author Design artifacts that reference at least one file that does NOT exist on disk (without `[PLANNED]` annotation) | AC-05a (phantom WARNING) | Design DoD surfaces WARNING for phantom reference; does NOT block completion |
| DF-3 | Author Design artifacts that reference one file with `[PLANNED]` annotation that does not exist on disk | AC-05b ([PLANNED] exemption) | `[PLANNED]` path does NOT trigger phantom WARNING at Design DoD |
| DF-4 | Progress to Dev entry gate with the phantom reference still unresolved (not in sprint plan) | AC-06a (Dev entry BLOCK) | Dev entry gate BLOCKS with list of non-existent references |
| DF-5 | Add the phantom reference file to the sprint plan, re-attempt Dev entry | AC-06a (sprint plan exemption) | Dev entry gate PASSES (file in sprint plan) |
| DF-6 | Verify `[PLANNED]` annotation is NOT accepted at Dev entry | AC-06b | `[PLANNED]` path that is not in sprint plan and not on disk is listed as blocking |
| DF-7 | At Plan stage, verify capacity matrix is WAIVED for BUG_FIX | AC-07b, AC-08b Light Mode | No capacity or coverage matrix required; Plan passes without them |
| DF-8 | At UAT, verify shared-module review step fires | AC-01a, AC-01b | UAT sub-flow includes shared-module review; QA agent identifies consuming contexts |
| DF-9 | At UAT, verify empirical-items classification is produced | AC-03a | UAT test plan contains empirical-items section classifying each AC |
| DF-10 | At UAT, verify empirical-items classification is checked by Gate 7 validator | AC-04a | Gate 7 checks for empirical-items section; would block if missing |
| DF-11 | At Dev DoD, verify derived artifact regeneration step fires | AC-11a, AC-11b | Dev sub-flow includes regeneration step; developer confirms regeneration status |
| DF-12 | At Dev DoD, verify Gate 6 checks derived artifact regeneration | AC-12a | Gate 6 includes blocking criterion for derived artifacts |
| DF-13 | Pipeline completes without regressions caused by gate changes | NFR-03 | Pipeline reaches completion; any failures are unrelated to this feature's changes |

### 5.5 Pass/Fail Criteria

**PASS**: All DF-1 through DF-13 steps produce expected results. Pipeline completes.

**FAIL**: Any of the following:
- A structural test case fails (the text is not where it should be)
- An empirical gate does not fire when expected (phantom WARNING missing, Dev entry block missing)
- An empirical gate fires incorrectly (false positive blocking on a valid reference)
- Pipeline fails at a non-modified stage due to a change in this feature
- A gate change causes a regression in an existing stage's behavior

### 5.6 Failure Protocol

1. Log the defect: which step failed, expected vs actual, relevant file excerpt
2. Fix the markdown in the affected reference file
3. Re-run structural tests for the affected story
4. Re-run dogfooding from the failed step (not from the beginning)
5. Add a regression test case for the specific failure mode

---

## 6. Risk-Based Test Prioritization

Tests are prioritized by risk of defect and impact of failure. Execute in this order.

### Priority 1: CRITICAL (execute first)

These have the highest blast radius or the highest likelihood of defect.

| Test Area | Risk | Impact | Why Critical |
|-----------|------|--------|-------------|
| AC-10c: Gate 5 criterion REPLACEMENT | High | Blocks all Plan stages | Only AC that modifies existing content rather than adding. If the old criterion remains, plans face contradictory blocking rules. If the new criterion is malformed, all Plan stages break. |
| Step renumbering (AC-01b, AC-09b, AC-11b) | High | Corrupts sub-flow execution | Three separate stories insert new steps in three different sub-flows. Each requires renumbering. A gap or duplicate number disrupts the sequential execution model. |
| AC-06a: Dev entry BLOCK behavior | High | Blocks all Dev stages | A false positive blocks every Dev entry. A false negative defeats the purpose of the fix. This is a runtime gate that must be dogfooded. |
| Regression: non-modified stages | Medium | Silent breakage | Changes to `pipeline-stages.md` and `quality-gates.md` are extensive. Unintended edits to non-targeted sections would silently corrupt other stages. |

### Priority 2: HIGH (execute second)

| Test Area | Risk | Impact | Why High |
|-----------|------|--------|---------|
| AC-05a/05b: Design phantom WARNING | Medium | False positives at Design DoD | WARNING is lower severity than BLOCK, but false positives erode trust in the gate system. `[PLANNED]` exemption logic must work correctly. |
| AC-04a: Gate 7 empirical-items blocking criterion | Medium | Blocks UAT completion | New blocking criterion. If malformed or placed incorrectly, UAT stages could block unexpectedly. |
| AC-09a/09b: Plan stage matrix validation | Medium | Plan stage slowdown | New mandatory validation step. If Light Mode waiver is missing, BUG_FIX plans would incorrectly require full matrices. |

### Priority 3: MEDIUM (execute third)

| Test Area | Risk | Impact | Why Medium |
|-----------|------|--------|-----------|
| AC-02a/02b: quality/SKILL.md additions | Low | QA guidance incomplete | Additive only, no existing content modified. Worst case: QA agent lacks new guidance but existing behavior unchanged. |
| AC-03a/03b/03c: artifact-contracts.md template | Low | Template incomplete | Additive only. Worst case: template missing a column, caught at UAT review. |
| AC-07a/07b, AC-08a/08b: project-templates.md additions | Low | Template incomplete | Additive only. Worst case: template column missing, caught at Plan review. |

### Priority 4: LOW (execute last)

| Test Area | Risk | Impact | Why Low |
|-----------|------|--------|--------|
| Retro annotations (TC-05c-2, TC-03c-4, TC-07b-3, TC-10c-3, TC-11b-4, TC-12b-2) | Very Low | Traceability gap | Missing annotations do not affect gate behavior. They affect auditability only. |
| NFR-04 token budget | Very Low | Slightly higher context load | Per-stage budget is generous (500 tokens). Markdown additions are unlikely to exceed this. |

---

## 7. Test Execution Order

Execute in priority order within each milestone, respecting dependencies.

### Phase 1: Priority 1 (Critical Path)

| # | Test | Story | TCs |
|---|------|-------|-----|
| 1 | Gate 5 criterion replacement verification | US-04 | TC-10c-1 (old text gone), TC-10a-1, TC-10b-1 |
| 2 | Stage 7 sub-flow step renumbering | US-01 | TC-01b-1, TC-01b-2 |
| 3 | Stage 5 sub-flow step renumbering | US-04 | TC-09b-1, TC-09b-2, TC-09b-3 |
| 4 | Stage 6 sub-flow step renumbering | US-05 | TC-11b-1, TC-11b-3 |
| 5 | Non-modified stages regression | Regression | Diff-based: Stages 1, 2, 4 unchanged |
| 6 | Cross-file consistency checks | Regression | Step numbering, gate-to-stage, contract-to-gate alignment |

### Phase 2: Priority 2 (High Risk)

| # | Test | Story | TCs |
|---|------|-------|-----|
| 7 | Gate 3 phantom reference criterion | US-03 | TC-05a-1, TC-05a-2, TC-05b-1, TC-05c-1 |
| 8 | Stage 6 entry condition (reconciliation gate) | US-03 | TC-06a-1, TC-06a-2, TC-06a-3, TC-06b-1, TC-06c-1, TC-06c-2 |
| 9 | Gate 7 empirical-items blocking criterion | US-02 | TC-04a-1, TC-04a-2, TC-04a-3 |
| 10 | Stage 5 Scrum Bag validator update | US-04 | TC-09a-1, TC-09a-2 |
| 11 | Gate 5 two-tier capacity model (full) | US-04 | TC-10c-2, TC-10c-3 |

### Phase 3: Priority 3 (Medium Risk)

| # | Test | Story | TCs |
|---|------|-------|-----|
| 12 | quality/SKILL.md additions | US-01 | TC-02a-1, TC-02a-2, TC-02b-1, TC-02b-2 |
| 13 | artifact-contracts.md template | US-02 | TC-03a-1, TC-03b-1, TC-03b-2, TC-03c-1, TC-03c-2, TC-03c-3, TC-03c-4 |
| 14 | project-templates.md capacity matrix | US-04 | TC-07a-1, TC-07a-2, TC-07b-1, TC-07b-2, TC-07b-3 |
| 15 | project-templates.md coverage matrix | US-04 | TC-08a-1, TC-08a-2, TC-08b-1, TC-08b-2 |
| 16 | Stage 7 DoD checklist and validators | US-01 | TC-01a-1, TC-01a-2, TC-01c-1 |
| 17 | Stage 6 DoD validators (derived artifacts) | US-05 | TC-11a-1, TC-11a-2, TC-11a-3, TC-11b-2, TC-11b-4 |
| 18 | Gate 6 derived artifact criterion | US-05 | TC-12a-1, TC-12a-2, TC-12b-1, TC-12b-2 |

### Phase 4: Priority 4 + NFRs

| # | Test | Story | TCs |
|---|------|-------|-----|
| 19 | Retro annotations (all stories) | All | TC-05c-2, TC-03c-4, TC-07b-3, TC-10c-3, TC-11b-4, TC-12b-2 |
| 20 | NFR-01: no executable files | NFR | Verify changeset is markdown-only |
| 21 | NFR-02: config v2.3 compat | NFR | No new config keys introduced |
| 22 | NFR-04: token budget | NFR | Count added lines per stage |
| 23 | NFR-05: retro traceability completeness | NFR | All modified sections annotated |

### Phase 5: Dogfooding

| # | Test | Scope |
|---|------|-------|
| 24 | Dogfooding pipeline run | DF-1 through DF-13 (Section 5.4) |

**Dogfooding is last because it depends on all structural tests passing first.** Running a pipeline with broken markdown wastes a full pipeline cycle.

---

## 8. FR Traceability Matrix

| FR | Story | ACs | TCs | Approach | Dogfooding Step |
|----|-------|-----|-----|----------|----------------|
| FR-01 | US-01 | AC-01a, AC-01b, AC-01c | TC-01a-1/2, TC-01b-1/2, TC-01c-1 | Structural | DF-8 |
| FR-02 | US-01 | AC-02a, AC-02b | TC-02a-1/2, TC-02b-1/2 | Structural | DF-8 |
| FR-03 | US-02 | AC-03a, AC-03b, AC-03c | TC-03a-1, TC-03b-1/2, TC-03c-1/2/3/4 | Structural | DF-9 |
| FR-04 | US-02 | AC-04a | TC-04a-1/2/3 | Structural | DF-10 |
| FR-05 | US-03 | AC-05a, AC-05b, AC-05c | TC-05a-1/2, TC-05b-1, TC-05c-1/2 | Structural + Empirical | DF-2, DF-3 |
| FR-06 | US-03 | AC-06a, AC-06b, AC-06c | TC-06a-1/2/3, TC-06b-1, TC-06c-1/2 | Structural + Empirical | DF-4, DF-5, DF-6 |
| FR-07 | US-04 | AC-07a, AC-07b | TC-07a-1/2, TC-07b-1/2/3 | Structural | DF-7 |
| FR-08 | US-04 | AC-08a, AC-08b | TC-08a-1/2, TC-08b-1/2 | Structural | DF-7 |
| FR-09 | US-04 | AC-09a, AC-09b | TC-09a-1/2, TC-09b-1/2/3 | Structural | DF-7 |
| FR-10 | US-04 | AC-10a, AC-10b, AC-10c | TC-10a-1, TC-10b-1, TC-10c-1/2/3 | Structural | -- |
| FR-11 | US-05 | AC-11a, AC-11b | TC-11a-1/2/3, TC-11b-1/2/3/4 | Structural | DF-11 |
| FR-12 | US-05 | AC-12a, AC-12b | TC-12a-1/2, TC-12b-1/2 | Structural | DF-12 |

**All 12 FRs covered. All 22 ACs covered. All 45 TCs mapped. Zero gaps.**
