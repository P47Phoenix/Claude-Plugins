# SM Review R2: Sprint Plan v2.0 — Stage Health Hardening

**Reviewer**: Aragorn (Scrum Master)
**Date**: 2026-03-29
**Artifact**: `.delivery/artifacts/05-plan/sm/sprint-plan.md` v2.0
**Stories**: `.delivery/artifacts/05-plan/po/user-stories.md` v1.0
**Mode**: FULL / FEATURE
**Prior Review**: `.delivery/artifacts/05-plan/dod/sm-review.md` (v1.0 — NOT_DONE, capacity overcommitment)

> *"The board is set, the pieces are moving. And this time, the pack is balanced."*

---

## Gate 5: Plan Readiness — SM Criteria (Re-validation)

### Blocking Criteria

- [x] **Sprint goal is a single sentence expressing business value**
  - PASS. Unchanged from v1.0. Single sentence expressing clear business value: raising first-try pass rates and eliminating rework traced to retros c8f2 and k4m9. Verbose but grammatically one sentence. No change needed.

- [x] **All committed stories have acceptance criteria**
  - PASS. Unchanged from v1.0. All 5 stories (US-01 through US-05) retain full AC tables in Given/When/Then format with structural/empirical classification. 29 acceptance criteria across 5 stories. No stories added or removed -- scope is preserved, only sizing changed.

- [x] **Commitment does not exceed 80% of capacity**
  - **PASS.** This was the sole blocking failure in v1.0. The revised plan provides a detailed re-estimation rationale (Section 2, "Re-estimation Rationale v2.0") applying a markdown-edit calibration:
    - v1.0: 3L + 1M + 1S = 3.5L equivalent (117% of ceiling -- FAILED)
    - v2.0: 3M + 2S = 2.0L equivalent (83% of ceiling -- PASS)
  - The calibration logic is sound: all work is constrained by NFR-01 to additive markdown edits in existing files with well-defined insertion points. No code, no schema changes, no new files. This legitimately places each story one tier below general FEATURE velocity assumptions. Each story's re-estimation is individually justified in the comparison table.
  - 2.0L against 2.4L ceiling = 83% utilization of the 80% ceiling, or approximately 67% of the raw 3L baseline. This is a comfortable margin. The fellowship no longer overreaches.

- [x] **Dogfooding planned as P0 gate**
  - PASS. Unchanged from v1.0. Step 8 remains "Dogfooding validation (P0 UAT gate)" with bold P0 declaration. Section 8 provides 9 verification items and clear success criteria. The lesson holds.

- [x] **Capacity declaration present (velocity baseline, 80% ceiling, commitment %)**
  - PASS. Section 2 now declares: velocity baseline (2-3 stories/sprint L-sized), 80% ceiling (2.4L equivalent), committed (2.0L equivalent, 83% of ceiling). All three components present, calculated correctly, and the v1-to-v2 delta is transparently documented. The numbers are honest and the arithmetic checks out.

### Warning Criteria

- [~] **Capacity accounts for ceremonies, PTO, and known interruptions**
  - WARNING (carried from v1.0, now explicitly addressed). The plan adds row "Ceremony/interruption budget: None (solo contributor, no PTO) -- Explicitly stated per SM Review advisory." The plan acknowledges this advisory and makes an explicit declaration rather than leaving it implicit. For a solo contributor on a FEATURE sprint with comfortable margin (67% of baseline), this explicit declaration is acceptable. The advisory stands as a note for future sprints with tighter margins.

- [x] **Test approach referenced per story**
  - PASS. Unchanged from v1.0. Each story has a full Test Cases table (TC-01a-1 through TC-12b-2). Sprint plan references Step 7 (cross-story verification) and Step 8 (dogfooding empirical validation).

- [x] **Deployment approach referenced**
  - PASS. Unchanged from v1.0. Section 6 specifies feature branch, one conventional commit per story, single PR to main.

- [x] **Dogfooding planned as P0 gate**
  - PASS. Already validated above as blocking criterion.

---

## Resolution of v1.0 Findings

| v1.0 Finding | Severity | Resolution in v2.0 | Status |
|--------------|----------|---------------------|--------|
| Capacity overcommitment (117% of ceiling) | BLOCKING | Re-estimated stories using markdown-edit calibration. New total: 2.0L (83% of ceiling). No scope reduction -- all 5 stories and 12 FRs retained. | RESOLVED |
| Ceremony/interruption budget implicit | WARNING | Explicit declaration added to capacity table: "None (solo contributor, no PTO) -- Explicitly stated per SM Review advisory" | ADDRESSED |

---

## Additional Observations

1. **Re-estimation approach is defensible**: The plan does not simply hand-wave smaller numbers. It states the calibration principle (markdown-only edits size one tier lower), applies it per-story with individual justifications, and shows the v1-to-v2 comparison table. The methodology is transparent and auditable. A ranger respects honest measurement.

2. **No scope was sacrificed**: All 5 stories and all 12 FRs are retained. The re-estimation reflects the actual nature of the work more accurately rather than artificially reducing scope to fit a ceiling. This is the right approach -- the ceiling exists to prevent overcommitment, not to penalize accurate estimation.

3. **Coverage matrix (Section 5)**: All 12 PRD FRs mapped to planned tasks. No unmapped FRs. The plan practices what US-04 will preach.

4. **Plugin-dev skill loading (Section 9)**: Mandatory `plugin-dev:skill-development` loading before any file edits. Repo conventions honored.

5. **Implementation ordering unchanged**: M2 -> M3 -> M1 -> M4 sequence with dependency rationale preserved from v1.0.

---

## Verdict

**STATUS: DONE**

All 5 blocking criteria pass. All 3 warning criteria pass (one with carried advisory). The sole blocking failure from v1.0 -- capacity overcommitment -- is resolved through a well-justified re-estimation that brings commitment to 83% of the 80% ceiling while retaining full scope.

The sprint plan is ready for Development. The weight of the pack is honest, the path is charted, and every requirement has a home.

*"There is always hope. And now there is also a balanced sprint."*
