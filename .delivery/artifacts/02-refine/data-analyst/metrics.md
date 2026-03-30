# Success Metrics: Stage Health Hardening

**Version**: 1.0
**Date**: 2026-03-29
**Author**: Data Analyst (Elrond)
**Source**: PRD v1.0 (Goals G1--G4)
**Baseline Period**: Last 3 pipeline runs

---

## G1: Reduce Design Rework

### Metric 1.1 — Design Stage First-Try Pass Rate

| Field | Value |
|-------|-------|
| **Name** | `design_first_try_pass_rate` |
| **Definition** | Percentage of pipeline runs where the Design stage passes DoD validation on the first submission, without any rework loop (re-entry to the same stage after a validator rejection). |
| **Baseline** | 50% (3 of 6 stage attempts passed on first try across last 3 runs) |
| **Target** | >= 80% |
| **Measurement Method** | From `.delivery/memory/` pipeline run logs: count Design stage executions where `dod_attempts == 1` (passed on first submission) divided by total Design stage executions. A "rework loop" is defined as any DoD submission that receives a FAIL verdict followed by a re-execution of the same stage within the same pipeline run. |
| **Cadence** | Per pipeline run (rolling 5-run window for trend) |

### Metric 1.2 — Phantom Reference Detection Rate

| Field | Value |
|-------|-------|
| **Name** | `design_phantom_ref_detection_rate` |
| **Definition** | Percentage of phantom file references (file paths cited in Design artifacts that do not exist on disk) caught at Design DoD, versus those discovered in downstream stages (Architect, Dev, UAT). |
| **Baseline** | 0% (phantom references currently surface downstream per retro k4m9) |
| **Target** | >= 95% of phantom references caught at Design DoD |
| **Measurement Method** | From pipeline run artifacts and DoD validator findings: count HIGH-severity phantom reference findings at Design stage divided by (Design phantom findings + downstream phantom findings in same run). Downstream phantom findings are file-not-found errors recorded in Architect, Dev, or UAT stage logs that trace to Design artifact references. |
| **Cadence** | Per pipeline run |

---

## G2: Reduce UAT Rework

### Metric 2.1 — UAT Stage First-Try Pass Rate

| Field | Value |
|-------|-------|
| **Name** | `uat_first_try_pass_rate` |
| **Definition** | Percentage of pipeline runs where the UAT stage passes DoD validation on the first submission, without any rework loop. |
| **Baseline** | 67% (2 of 3 runs passed UAT on first try across last 3 runs) |
| **Target** | >= 85% |
| **Measurement Method** | From `.delivery/memory/` pipeline run logs: count UAT stage executions where `dod_attempts == 1` divided by total UAT stage executions. |
| **Cadence** | Per pipeline run (rolling 5-run window for trend) |

### Metric 2.2 — Shared-Module Review Completion Rate

| Field | Value |
|-------|-------|
| **Name** | `uat_shared_module_review_rate` |
| **Definition** | Percentage of UAT stage executions involving shared-module changes where the shared-module review checklist item is completed (all consuming contexts listed and test status recorded). |
| **Baseline** | 0% (shared-module review checkpoint does not exist yet per retros c8f2, k4m9) |
| **Target** | 100% |
| **Measurement Method** | From UAT stage DoD artifacts: count UAT executions where shared-module changes exist AND the "shared-module review" checklist item is marked complete with consuming-context test status, divided by total UAT executions where shared-module changes exist. A shared module is defined as a file imported by 2+ other modules (per FR-01). |
| **Cadence** | Per pipeline run |

### Metric 2.3 — Empirical-Items Tracking Artifact Presence

| Field | Value |
|-------|-------|
| **Name** | `uat_empirical_items_artifact_rate` |
| **Definition** | Percentage of UAT stage executions where the empirical-items tracking artifact is produced and classifies each acceptance criterion as "structural" or "empirical" with justification. |
| **Baseline** | 0% (empirical-items tracking template does not exist yet per retro k4m9) |
| **Target** | 100% |
| **Measurement Method** | From UAT stage DoD submissions: check for presence of empirical-items tracking artifact (per FR-03 template). Count UAT executions with artifact present divided by total UAT executions. |
| **Cadence** | Per pipeline run |

---

## G3: Prevent Plan Overcommit

### Metric 3.1 — Plan Overcommit Pass Rate

| Field | Value |
|-------|-------|
| **Name** | `plan_overcommit_pass_rate` |
| **Definition** | Percentage of sprint plans that pass Plan stage DoD with >100% capacity allocation without explicit acknowledgment. A value of 0% means no overcommitted plans slip through unacknowledged. |
| **Baseline** | Unknown (no capacity tracking exists; retros c8f2 and k4m9 report overcommit incidents but no systematic measurement) |
| **Target** | 0% (zero plans pass with >100% allocation without acknowledgment) |
| **Measurement Method** | From Plan stage artifacts: parse the capacity matrix (FR-07) to compute total utilization percentage. Count plans where utilization > 100% AND no acknowledgment justification is present in the DoD submission. Divide by total Plan stage executions. |
| **Cadence** | Per pipeline run |

### Metric 3.2 — Capacity Matrix Presence Rate

| Field | Value |
|-------|-------|
| **Name** | `plan_capacity_matrix_rate` |
| **Definition** | Percentage of Plan stage artifacts that include a capacity matrix (team members x estimated hours) as required by FR-07. |
| **Baseline** | 0% (capacity matrix template does not exist yet) |
| **Target** | 100% |
| **Measurement Method** | From Plan stage artifacts: check for presence of a capacity matrix table with required columns (team member, available hours, allocated hours, utilization percentage). Count plans with matrix present divided by total Plan stage executions. |
| **Cadence** | Per pipeline run |

### Metric 3.3 — Coverage Matrix Completeness Rate

| Field | Value |
|-------|-------|
| **Name** | `plan_coverage_matrix_completeness` |
| **Definition** | Percentage of Plan stage artifacts where the coverage matrix maps every PRD FR-ID to at least one planned task with no FR left unmapped, as required by FR-08. |
| **Baseline** | 0% (coverage matrix template does not exist yet) |
| **Target** | 100% |
| **Measurement Method** | From Plan stage artifacts: extract the coverage matrix, compare mapped FR-IDs against the PRD's FR list. Count plans where all FRs are mapped divided by total Plan stage executions. |
| **Cadence** | Per pipeline run |

---

## G4: Eliminate Derived Artifact Drift

### Metric 4.1 — Derived Artifact Staleness at Dev DoD

| Field | Value |
|-------|-------|
| **Name** | `dev_derived_artifact_staleness` |
| **Definition** | Count of derived artifacts that are stale (not regenerated from current source files) at Development stage DoD submission. |
| **Baseline** | Not tracked (retro c8f2 reports derived artifact drift incidents but no count) |
| **Target** | 0 stale derived artifacts at Dev completion |
| **Measurement Method** | From Dev stage DoD submissions: check the "regenerate derived artifacts" checklist item (FR-11). Count derived artifacts where regeneration is not confirmed. A derived artifact is any file generated or transformed from a source file (e.g., generated docs, compiled schemas, transformed configs). |
| **Cadence** | Per pipeline run |

### Metric 4.2 — Derived Artifact Regeneration Checklist Completion Rate

| Field | Value |
|-------|-------|
| **Name** | `dev_regeneration_checklist_rate` |
| **Definition** | Percentage of Dev stage DoD submissions where the "regenerate derived artifacts" checklist item is present and marked complete. |
| **Baseline** | 0% (checklist item does not exist yet per retro c8f2) |
| **Target** | 100% |
| **Measurement Method** | From Dev stage DoD submissions: count submissions where the regeneration checklist item exists and is marked complete, divided by total Dev stage DoD submissions where source files with derived artifacts were modified. |
| **Cadence** | Per pipeline run |

---

## Non-Regression Guardrail (NFR-03)

### Metric NR.1 — Non-Targeted Stage Pass Rate Stability

| Field | Value |
|-------|-------|
| **Name** | `non_targeted_stage_stability` |
| **Definition** | First-try pass rates for stages NOT targeted by this PRD (Architect, and indirectly Idea) must not regress from their current baselines. |
| **Baselines** | Idea: 67%, Plan: 83%, Development: 83%, Architect: no failures in last 3 runs |
| **Target** | No decrease beyond 1 standard deviation from rolling 5-run mean |
| **Measurement Method** | From `.delivery/memory/` pipeline run logs: compute first-try pass rate per non-targeted stage on a rolling 5-run window. Flag if any stage drops more than 1 SD below the window mean. |
| **Cadence** | Per pipeline run (rolling 5-run window) |

---

## Metrics Summary Table

| ID | Metric | Baseline | Target | Goal |
|----|--------|----------|--------|------|
| 1.1 | Design first-try pass rate | 50% | >= 80% | G1 |
| 1.2 | Phantom reference detection rate | 0% | >= 95% | G1 |
| 2.1 | UAT first-try pass rate | 67% | >= 85% | G2 |
| 2.2 | Shared-module review completion | 0% | 100% | G2 |
| 2.3 | Empirical-items artifact presence | 0% | 100% | G2 |
| 3.1 | Plan overcommit pass rate | Unknown | 0% | G3 |
| 3.2 | Capacity matrix presence | 0% | 100% | G3 |
| 3.3 | Coverage matrix completeness | 0% | 100% | G3 |
| 4.1 | Derived artifact staleness count | Not tracked | 0 | G4 |
| 4.2 | Regeneration checklist completion | 0% | 100% | G4 |
| NR.1 | Non-targeted stage stability | Per-stage baselines | No regression | NFR-03 |

---

## Validation Cadence

- **Per-run metrics** (1.1, 1.2, 2.1--2.3, 3.1--3.3, 4.1--4.2): Evaluated after each pipeline run completes. Data sourced from stage artifacts and DoD validator findings in `.delivery/memory/`.
- **Rolling window metrics** (NR.1): Computed on a 5-run rolling window. Trend alerts trigger when a non-targeted stage drops below baseline minus 1 SD.
- **Post-deployment validation**: After the Stage Health Hardening changes ship, the first 3 pipeline runs constitute the validation period. All G1--G4 targets must be met within 3 runs to confirm success. If targets are not met, gate severity should be revisited per Risk mitigation (PRD Section 7).
