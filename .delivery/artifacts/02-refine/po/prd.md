# PRD: Stage Health Hardening

**Version**: 1.1
**Date**: 2026-03-29
**Author**: Product Owner (Gandalf)
**Project Type**: FEATURE
**Pipeline**: delivery-flow
**Retro Sources**: c8f2, k4m9

---

## 1. Problem Statement

Three pipeline stages have first-try pass rates well below acceptable thresholds:

| Stage | Current Pass Rate | Target | Gap |
|-------|------------------|--------|-----|
| Design | 50% | >= 70% | -20pp |
| UAT | 67% | >= 85% | -18pp |
| Idea | 67% | N/A (cascading fix from Design) | -- |

**Evidence from retrospectives c8f2 and k4m9:**

- **Phantom file references** survive into downstream stages -- Design artifacts cite files that do not exist on disk, causing rework when Architect/Developer discovers them (retro k4m9)
- **Missing shared-module review** in UAT -- changes touching shared modules pass UAT without verifying all consuming contexts, causing integration failures discovered post-pipeline (retros c8f2, k4m9)
- **Absent capacity planning** in Plan stage -- sprint plans with >100% allocation pass without warning, leading to scope cuts mid-Development (retros c8f2, k4m9)
- **Derived artifact drift** -- regenerated artifacts diverge from source files when Dev stage does not explicitly require regeneration before completion (retro c8f2)

These are not random failures. Each root cause maps to a specific retro action item (M1-M4) with a concrete stage-level fix.

> **Note on Design target (v1.1)**: The v1.0 target of >= 80% has been reduced to >= 70% for the initial validation period. The baseline of 50% is drawn from 6 attempts across 3 pipeline runs -- statistically thin. Phantom references are a confirmed root cause (retro k4m9) but may not account for all Design failures. After 5 pipeline runs under the hardened gates, the target will be re-evaluated with stronger data. If phantom references prove to be the dominant root cause (>=2 of observed failures), the target may be raised to 80%.

---

## 2. Goals & Success Metrics

| Goal | Metric | Baseline | Target | Measurement Method |
|------|--------|----------|--------|--------------------|
| G1: Reduce Design rework | Design stage first-try pass rate | 50% | >= 70% | Pipeline run logs (pass/fail on first DoD submission); re-evaluate after 5 runs |
| G2: Reduce UAT rework | UAT stage first-try pass rate | 67% | >= 85% | Pipeline run logs |
| G3: Prevent Plan overcommit | Sprint plans passing with >100% allocation | Unknown (no tracking) | 0 plans pass without acknowledgment | Plan stage validation warning count |
| G4: Eliminate derived drift | Derived artifact staleness at Dev DoD | Not tracked | 0 stale derived artifacts at Dev completion | Dev DoD checklist completion |

**Validation approach (Dogfooding)**: The hardened stages must be validated by running an actual pipeline through them. This is a P0 UAT gate. Dogfooding success is defined as: run a BUG_FIX pipeline that exercises at least the Design, Plan, and UAT stages. The pipeline must reach completion without regressions caused by the gate changes. Failures unrelated to the gate changes (e.g., unrelated DoD findings in non-modified stages) do not count as dogfooding failures. If the dogfooding pipeline fails due to a gate change defect, the defect must be fixed and dogfooding re-run.

---

## 3. User Personas

### P1: Plugin Contributor
Pipeline users who run delivery-flow on this repo. Currently experience avoidable rework loops at Design, UAT, and Plan stages.
**Goal**: Complete pipeline stages on first attempt without avoidable rework loops.
**Pain points**: Phantom references cause downstream rework; capacity overcommit forces mid-sprint scope cuts; shared-module gaps surface post-pipeline.

### P2: Delivery Team Sub-Agent (Architect, QA, Developer)
Sub-agents whose DoD validations currently catch issues too late.
**Goal**: Receive clean, validated inputs from upstream stages so downstream validation focuses on stage-specific concerns, not inherited defects.
**Pain points**: Phantom references from Design leak into Architect/Dev; missing shared-module context at UAT.

### P3: Pipeline Maintainer
Maintainers who update `quality-gates.md`, `pipeline-stages.md`, and related reference files.
**Goal**: Maintain clear, unambiguous gate criteria that sub-agents can consistently evaluate without interpretation variance.
**Pain points**: Current gate criteria are implicit or warning-level for issues that cause blocking rework.

---

## 4. Functional Requirements

### M1 -- UAT Stage Hardening (retros c8f2, k4m9)

| ID | Requirement | Priority | Acceptance Criteria | AC Type |
|----|-------------|----------|--------------------|----|
| FR-01 | Add shared-module review checkpoint to the UAT stage definition in `delivery-team/skills/delivery-flow/references/pipeline-stages.md`, requiring the QA validator to verify that changes touching shared modules have been tested in all consuming contexts. A **shared module** is defined as: a file that is explicitly referenced (by path or name) in 2+ stage artifacts across the current pipeline run. This makes the definition artifact-traceable -- the QA agent verifies it using Glob/Read on the `.delivery/artifacts/` directory, without requiring language-level import analysis. | P0 | **Given** a pipeline run where Development artifacts modify a shared module (a file referenced by path or name in 2+ stage artifacts across the current pipeline run), **When** the UAT stage DoD is evaluated, **Then** the DoD checklist includes a "shared-module review" item that requires listing all consuming contexts and their test status | structural |
| FR-02 | Add shared-module review guidance to `delivery-team/skills/quality/SKILL.md` so QA sub-agents know how to perform the review | P0 | **Given** the QA skill is loaded for a UAT validation, **When** the QA sub-agent checks shared-module changes, **Then** SKILL.md contains explicit instructions for identifying consuming contexts and verifying test coverage across them | structural |
| FR-03 | Create an empirical-items tracking artifact template in `delivery-team/skills/delivery-flow/references/artifact-contracts.md` that UAT sub-agents populate to record which acceptance criteria require runtime validation vs. static review | P0 | **Given** a UAT stage execution, **When** the UAT sub-agent evaluates acceptance criteria, **Then** an empirical-items tracking artifact is produced using the template from artifact-contracts.md, classifying each AC as "structural" or "empirical" with justification | structural |
| FR-04 | Add empirical-items tracking as a requirement in the UAT DoD validator criteria in `delivery-team/skills/delivery-flow/references/quality-gates.md` | P0 | **Given** a UAT stage DoD submission, **When** the validator checks completeness, **Then** the validator requires an empirical-items tracking artifact to be present and rejects the submission if missing | structural |

### M2 -- Design Stage Hardening (retro k4m9)

| ID | Requirement | Priority | Acceptance Criteria | AC Type |
|----|-------------|----------|--------------------|----|
| FR-05 | At Design DoD, phantom reference findings (file paths cited in artifacts that do not exist on disk and are not annotated with `[PLANNED]`) are reported as **WARNING** severity in `delivery-team/skills/delivery-flow/references/quality-gates.md`. File paths annotated with `[PLANNED]` in Design artifacts are exempt from phantom detection. This WARNING-level approach avoids false positives on GREENFIELD and FEATURE projects where Design routinely references files to be created in later stages. | P0 | **Given** a Design stage artifact references file path `X`, **When** file `X` does not exist on disk at DoD validation time and is not annotated with `[PLANNED]`, **Then** the validator reports a WARNING-severity finding that is logged and surfaced to the author but does not block stage completion | empirical |
| FR-06 | Add a filename reconciliation gate at Dev stage entry in `delivery-team/skills/delivery-flow/references/pipeline-stages.md` that verifies all file paths referenced in Design and Architect artifacts exist on disk or are explicitly planned for creation in the current sprint plan. At Dev entry, `[PLANNED]` annotations are no longer accepted as exemptions -- all referenced files must either exist or appear in the sprint plan's task list. Missing paths **block** Dev entry. | P0 | **Given** the pipeline transitions from Architect to Development, **When** the Dev stage entry gate runs, **Then** all file paths referenced in Design and Architect stage artifacts are checked: paths that exist on disk pass; paths listed in the sprint plan as planned deliverables pass; all other missing paths block Dev entry with a list of non-existent references | empirical |

### M3 -- Plan Stage Guardrails (retros c8f2, k4m9)

| ID | Requirement | Priority | Acceptance Criteria | AC Type |
|----|-------------|----------|--------------------|----|
| FR-07 | Update the Plan stage template in `delivery-team/skills/delivery-flow/references/project-templates.md` to include a mandatory capacity matrix (team members x estimated hours) | P0 | **Given** a Plan stage artifact is being authored, **When** the sprint plan is produced, **Then** the plan includes a capacity matrix table with columns: team member, available hours, allocated hours, and utilization percentage | structural |
| FR-08 | Update the Plan stage template in `delivery-team/skills/delivery-flow/references/project-templates.md` to include a mandatory coverage matrix (PRD FRs x planned tasks) | P0 | **Given** a Plan stage artifact is being authored, **When** the sprint plan is produced, **Then** the plan includes a coverage matrix mapping every PRD FR-ID to at least one planned task, with no FR left unmapped | structural |
| FR-09 | Add capacity matrix and coverage matrix as mandatory fields in the Plan stage definition in `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | P0 | **Given** a Plan stage DoD submission, **When** the validator checks the plan artifact, **Then** the validator rejects the submission if either the capacity matrix or coverage matrix is missing | structural |
| FR-10 | Add layered sprint capacity threshold validation in `delivery-team/skills/delivery-flow/references/quality-gates.md` and `delivery-team/skills/delivery-flow/references/pipeline-stages.md`. The thresholds are: **>80% utilization emits a WARNING** that must be acknowledged; **>100% utilization is BLOCKING** and requires allocation reduction or explicit justification with PO sign-off. This replaces the existing Gate 5 "80% blocking" criterion with an explicit two-tier model. **Rationale for relaxation**: the prior 80% hard block was overly conservative for teams that intentionally plan at 85-95% utilization; the new model warns early but only blocks at genuine overcommit. | P0 | **Given** a sprint plan where total allocated hours exceed 80% of total available hours, **When** the Plan stage DoD is evaluated, **Then**: (a) if utilization is >80% and <=100%, a WARNING is emitted stating the utilization percentage, and the plan can pass DoD only after the warning is acknowledged with brief justification; (b) if utilization is >100%, a BLOCKING finding is emitted, and the plan cannot pass DoD until allocation is reduced to <=100% or the PO provides explicit sign-off with justification | structural |

### M4 -- Dev Stage DoD (retro c8f2)

| ID | Requirement | Priority | Acceptance Criteria | AC Type |
|----|-------------|----------|--------------------|----|
| FR-11 | Add "regenerate derived artifacts" as an explicit checklist item in the Dev stage DoD in `delivery-team/skills/delivery-flow/references/pipeline-stages.md`, ensuring that any artifacts derived from modified source files are regenerated before Dev completion | P0 | **Given** the Development stage modifies source files that have derived artifacts (e.g., generated docs, compiled schemas, transformed configs), **When** the Dev stage DoD is evaluated, **Then** the DoD checklist includes a "regenerate derived artifacts" item, and the developer must confirm all derived artifacts have been regenerated from current sources | structural |
| FR-12 | Add derived artifact regeneration as a validator criterion in `delivery-team/skills/delivery-flow/references/quality-gates.md` | P0 | **Given** a Dev stage DoD submission, **When** the validator checks artifact freshness, **Then** the validator requires confirmation that derived artifacts have been regenerated and rejects the submission if the regeneration checklist item is not marked complete | structural |

### Retro Traceability Matrix

| Retro Item | FRs | Coverage |
|------------|-----|----------|
| M1: Shared-module review checkpoint (c8f2) | FR-01, FR-02 | Complete |
| M1: Empirical-items tracking template (k4m9) | FR-03, FR-04 | Complete |
| M2: Phantom reference high-severity (k4m9) | FR-05 | Complete |
| M2: Filename reconciliation gate (k4m9) | FR-06 | Complete |
| M3: Capacity + coverage matrix (c8f2) | FR-07, FR-08, FR-09 | Complete |
| M3: Sprint capacity threshold warning (k4m9) | FR-10 | Complete |
| M4: Regenerate derived artifacts (c8f2) | FR-11, FR-12 | Complete |

All 7 retro action items from M1-M4 are covered by FR-01 through FR-12.

---

## 5. Non-Functional Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| NFR-01 | All changes are markdown-only edits to existing delivery-team reference files -- no new Python scripts or external dependencies | No `.py`, `.js`, `.sh`, or other executable files are created or modified |
| NFR-02 | Changes preserve backward compatibility with config schema v2.3 | `.delivery/config.yml` files valid under schema v2.3 remain valid after changes; no new config keys are introduced |
| NFR-03 | No regression in existing stage pass rates | Stages not targeted by this PRD (Idea, Architect, Development) maintain their current first-try pass rates after changes are deployed |
| NFR-04 | Token budget impact is minimal | Added reference file content does not increase **per-stage** total context load by more than 500 tokens (measured by counting added markdown lines x ~1.3 tokens/word average). This is a per-stage constraint (not per-file). Validation is deferred to Dev stage DoD where actual line counts can be measured; it is not enforceable at Refine time. |
| NFR-05 | Each change is traceable to a specific retro action item | Every modified file section includes an inline comment or annotation identifying the retro source (c8f2 or k4m9) |

---

## 6. Out of Scope

- **Idea stage hardening** -- its 67% pass rate shares root causes with Design; M2 fixes (phantom reference elevation) will cascade to improve Idea stage outcomes
- **New Python hook scripts or automated enforcement tooling** -- this scope is markdown/template changes only; automated enforcement is a future iteration
- **Analytics dashboard updates** for tracking new metrics (capacity utilization, empirical-items counts)
- **Changes to setup wizard or config schema** -- no new config keys; schema remains at v2.3
- **Modifications to alias themes or personality injection**
- **Retrospective format changes**
- **Automated file-existence checking tooling** -- FR-05 and FR-06 define the gate criteria in markdown; the sub-agents perform the checks using existing Glob/Read tools

---

## 7. Dependencies & Risks

### Dependencies

| Dependency | Impact | Mitigation | Status |
|------------|--------|------------|--------|
| Existing pipeline-stages.md structure | FR-01, FR-06, FR-09, FR-10, FR-11 add content to this file; structural changes could conflict with concurrent edits | Coordinate via delivery-flow pipeline; single branch for all changes | Active |
| Existing quality-gates.md structure | FR-04, FR-05, FR-10, FR-12 add validator criteria; must align with current validator format | Review current validator format before authoring changes | Active |
| QA skill instructions (quality/SKILL.md) | FR-02 adds guidance; must not conflict with existing QA instructions | Additive change only; no existing content removed | Active |
| Artifact-contracts.md template format | FR-03 adds a new template; must follow existing template conventions | Review existing templates in artifact-contracts.md before authoring | Active |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Added gate criteria slow down pipeline execution without proportionate quality gain | Medium | Medium | Monitor first-try pass rates post-deployment; if pass rates don't improve within 3 pipeline runs, revisit gate severity |
| Capacity matrix adds overhead that teams shortcut by filling with placeholder values | Medium | Low | FR-10's threshold validation catches the most egregious case (>100% allocation); future iteration can add reasonableness checks |
| Phantom reference WARNING at Design DoD is too permissive -- phantoms survive to Dev entry | Medium | Medium | FR-06 provides the hard block at Dev entry; the two-tier model (warn at Design, block at Dev) catches phantoms before Development begins while avoiding Design-stage false positives on planned files |
| Two-tier capacity model (80% warn, 100% block) is more permissive than prior 80% block | Low | Medium | The 80% warning ensures visibility; teams planning at 85-95% must explicitly justify, creating an audit trail. If overcommit recurs, threshold can be tightened in a future iteration |
| Dogfooding validation adds pipeline run time | Low | Low | One additional pipeline run is the cost; the alternative (shipping un-dogfooded gate changes) has caused regressions before |

---

## 8. Assumptions

1. Sub-agents have access to Glob and Read tools for performing file-existence checks (FR-05, FR-06) and shared-module identification (FR-01) at runtime
2. Capacity matrix values provided by the SM/team will be good-faith estimates, not placeholder values; reasonableness checks are deferred to a future iteration
3. Retro action items M1-M4 from retrospectives c8f2 and k4m9 are correctly identified and their root-cause analysis is accurate
4. The `[PLANNED]` annotation convention (FR-05) will be adopted by Design stage authors without requiring tooling enforcement
5. The existing 6-attempt baseline for Design stage pass rate, while statistically thin, is directionally accurate enough to set a conservative >= 70% target

---

## 9. Light Mode Behavior

Pipeline Light Mode (used for BUG_FIX and DOCS_ONLY project types) reduces stage depth but does not skip stages. The following clarifies how each FR applies in Light Mode:

| FR | Light Mode Behavior | Rationale |
|----|--------------------|----|
| FR-01 (Shared-module review) | **Applies** regardless of mode | Bug fixes are arguably more likely to touch shared modules; shared-module review is high-risk to skip |
| FR-02 (QA skill guidance) | **Applies** -- skill instructions are mode-independent | Guidance is loaded into the QA agent regardless of mode |
| FR-03, FR-04 (Empirical-items tracking) | **Applies** -- empirical vs. structural classification is relevant for all project types | Even BUG_FIX UAT must distinguish testable criteria |
| FR-05 (Design phantom WARNING) | **Applies** -- warnings are low-cost and informational | Light mode reduces depth, not validation signals |
| FR-06 (Dev-entry reconciliation BLOCK) | **Applies** -- blocking on phantom references is critical for all types | Bug fixes that reference non-existent files are high-risk |
| FR-07, FR-08 (Capacity + coverage matrices) | **Waived** for BUG_FIX and DOCS_ONLY | Minimal plans for single-story fixes do not benefit from full matrix overhead |
| FR-09 (Mandatory matrix validation) | **Waived** for BUG_FIX and DOCS_ONLY (follows FR-07/FR-08) | Validators cannot require matrices that are waived |
| FR-10 (Capacity threshold) | **Applies** even in Light Mode | A single-story bug fix can still be overscoped; the >100% block prevents overcommit regardless of project type |
| FR-11, FR-12 (Derived artifact regeneration) | **Applies** | Derived artifacts must stay fresh regardless of project type |

---

## 10. Open Questions

| # | Question | Owner | Impact if Unresolved | Status |
|---|----------|-------|---------------------|--------|
| OQ-1 | ~~Should FR-06 distinguish planned vs. phantom files?~~ | Architect | ~~FR-06 could block legitimate Dev entry~~ | **RESOLVED in v1.1** -- FR-05 uses WARNING + `[PLANNED]` annotation at Design; FR-06 blocks at Dev entry where planned files must either exist or appear in the sprint plan |
| OQ-2 | ~~What is the threshold for "shared module"?~~ | QA / Developer | ~~Ambiguous definition could lead to inconsistent review~~ | **RESOLVED in v1.1** -- Defined as a file referenced by path/name in 2+ stage artifacts (artifact-traceable, not import-traceable) |
| OQ-3 | Should the empirical-items tracking artifact (FR-03) be a standalone file or a section within the existing UAT artifact? | Product Owner | Affects artifact-contracts.md template design and validator expectations | Open -- to be resolved at Design stage |

---

## Files Involved

| File | FRs | Change Type |
|------|-----|-------------|
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | FR-01, FR-06, FR-09, FR-10, FR-11 | Modify (add checkpoints, gates, checklist items) |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | FR-04, FR-05, FR-10, FR-12 | Modify (add/elevate validator criteria) |
| `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | FR-03 | Modify (add empirical-items tracking template) |
| `delivery-team/skills/delivery-flow/references/project-templates.md` | FR-07, FR-08 | Modify (add capacity + coverage matrix to Plan template) |
| `delivery-team/skills/quality/SKILL.md` | FR-02 | Modify (add shared-module review guidance) |
| `delivery-team/skills/delivery-flow/SKILL.md` | -- | Potentially modify (if orchestrator needs awareness of new gates) |

All 6 file paths verified on disk via Glob.

---

## Revision Notes (v1.1)

| Finding | Severity | Resolution | PRD Change |
|---------|----------|------------|------------|
| C1: Design 50%->80% target unsubstantiated | HIGH | Reduced target to >= 70% for initial validation period; added re-evaluation clause after 5 runs | Section 1 (note block), Section 2 (G1 target + measurement method) |
| C2: OQ-1 planned vs. phantom files -- false positive risk | HIGH | FR-05 changed from BLOCKING to WARNING at Design DoD; added `[PLANNED]` annotation mechanism; FR-06 blocks at Dev entry where files should exist or be in sprint plan | FR-05 (rewritten), FR-06 (expanded), OQ-1 (marked RESOLVED) |
| C4: Gate 5 capacity contradiction (80% block vs. 100% warning) | HIGH | Replaced with explicit two-tier model: >80% = WARNING with ack, >100% = BLOCKING. Documented rationale for relaxing the prior 80% hard block. | FR-10 (rewritten with layered thresholds), Risk table (new row for two-tier model) |
| C3: Shared-module definition ambiguity | MEDIUM | Redefined "shared module" as artifact-traceable (file referenced in 2+ stage artifacts) rather than import-traceable. Removes need for language-aware static analysis. | FR-01 (definition embedded in requirement text), OQ-2 (marked RESOLVED) |
| C6: Light Mode gap | MEDIUM | Added Section 9 specifying Light Mode behavior per FR. FR-01/FR-05/FR-06/FR-10/FR-11/FR-12 apply; FR-07/FR-08/FR-09 waived for BUG_FIX/DOCS_ONLY. | New Section 9 |
| C5: NFR-04 token budget scope unclear | LOW | Clarified as "per-stage" with validation deferred to Dev stage DoD | NFR-04 (expanded acceptance criteria) |
| C7: Dogfooding success criteria undefined | LOW | Added explicit success definition: BUG_FIX pipeline exercising Design/Plan/UAT, must complete without gate-change regressions | Section 2 (validation approach expanded) |
| W1: Personas lack explicit goals | QA WARNING | Added "Goal" statement to each persona | Section 3 (P1, P2, P3) |
| W2: Dependencies missing status column | QA WARNING | Added "Status" column to Dependencies table | Section 7 Dependencies table |
| S1: No assumptions section | QA SUGGESTION | Added Section 8 with 5 explicit assumptions | New Section 8 |
