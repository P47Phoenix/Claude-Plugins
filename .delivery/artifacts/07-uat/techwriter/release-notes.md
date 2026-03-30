# Release Notes: Stage Health Hardening

**Version**: 2.11.0
**Date**: 2026-03-29
**Author**: Bilbo (Technical Writer)
**Retro Sources**: c8f2, k4m9

> "I think I'm quite ready for another documentation adventure." And what an adventure this one is -- four stages strengthened, five files refined, and not a single breaking change to speak of. A tale worth telling properly.

---

## What Changed

This release hardens four delivery pipeline stages (UAT, Design, Plan, Development) to address recurring first-try failure patterns identified in retrospectives c8f2 and k4m9. All changes are markdown-only edits to existing reference files -- no new scripts, no config schema changes, no external dependencies.

### UAT Stage Hardening (M1)

- **Shared-module review checkpoint** added to Stage 7 (UAT) in `pipeline-stages.md`. When Development artifacts modify a file referenced in 2+ stage artifacts, the QA validator now requires listing all consuming contexts and their test status before UAT can pass.
- **Shared-Module Review Protocol** added to `quality/SKILL.md` with a 5-step identification process and 4-item review checklist, giving QA sub-agents explicit guidance for performing shared-module reviews.
- **Empirical-items tracking template** added to `artifact-contracts.md`. UAT sub-agents now classify each acceptance criterion as "structural" or "empirical" with justification, producing a tracking artifact.
- **Empirical-items classification** added as a blocking criterion in Gate 7 (`quality-gates.md`). UAT submissions missing the empirical-items tracking artifact are rejected.

### Design Stage Hardening (M2)

- **Phantom reference WARNING** added to Gate 3 (`quality-gates.md`). File paths cited in Design artifacts that do not exist on disk and lack a `[PLANNED]` annotation now produce a WARNING-severity finding. This warns authors without blocking -- important for GREENFIELD and FEATURE projects where files are routinely planned for later creation.
- **Filename reconciliation gate** added to Stage 6 entry conditions (`pipeline-stages.md`). At Dev entry, all file paths from Design and Architect artifacts must either exist on disk or appear in the sprint plan. The `[PLANNED]` exemption no longer applies at this stage -- missing paths block Dev entry. This two-tier model (warn at Design, block at Dev) catches phantom references before Development begins.

### Plan Stage Guardrails (M3)

- **Capacity matrix template** (team members x estimated hours) and **coverage matrix template** (PRD FRs x planned tasks) added to `project-templates.md` as mandatory Plan stage sections.
- **Matrix validation step** added to Stage 5 (`pipeline-stages.md`). The Scrum Bag validator now checks for both matrices.
- **Two-tier capacity threshold** replaces the previous 80%-blocking model in Gate 5 (`quality-gates.md`):
  - **>80% utilization**: WARNING -- must be acknowledged with brief justification; does not block.
  - **>100% utilization**: BLOCKING -- requires allocation reduction or explicit PO sign-off.
  - **Rationale**: The prior 80% hard block was overly conservative for teams intentionally planning at 85-95% utilization. The new model warns early but only blocks at genuine overcommit.
- **Light Mode waiver**: Capacity and coverage matrices (FR-07, FR-08, FR-09) are waived for BUG_FIX and DOCS_ONLY project types. The capacity threshold (FR-10) still applies.

### Dev Stage DoD (M4)

- **Derived artifact regeneration step** added to Stage 6 (`pipeline-stages.md`). Developers must confirm all derived artifacts (generated docs, compiled schemas, transformed configs) have been regenerated from current sources before Dev completion.
- **Derived artifact regeneration** added as a blocking criterion in Gate 6 (`quality-gates.md`). Submissions are rejected if the regeneration checklist item is not marked complete.

---

## Why It Matters

These changes directly address measurable quality gaps:

| Stage | Baseline Pass Rate | Target | Root Cause Addressed |
|-------|-------------------|--------|---------------------|
| Design | 50% | >= 70% | Phantom file references surviving into downstream stages |
| UAT | 67% | >= 85% | Missing shared-module review; no empirical-items tracking |
| Plan | Not tracked | 0 plans pass >100% without acknowledgment | Absent capacity planning; overcommit without visibility |
| Development | Not tracked | 0 stale derived artifacts at completion | Derived artifacts drifting from source files |

The targets are conservative. The Design target of 70% (reduced from 80% in v1.0) acknowledges the thin statistical baseline (6 attempts across 3 runs) and will be re-evaluated after 5 pipeline runs.

---

## Impact on Users

### Plugin Contributors (pipeline users)

- **Plan stage**: You will now need to include a capacity matrix and coverage matrix in sprint plans (unless running a BUG_FIX or DOCS_ONLY pipeline). Plans with >80% utilization will prompt for acknowledgment; >100% will block until resolved.
- **Design stage**: File paths in Design artifacts that reference non-existent files will generate WARNINGs at Design DoD unless annotated with `[PLANNED]`. At Dev entry, all referenced paths must exist or appear in the sprint plan.
- **Dev stage**: A new "regenerate derived artifacts" checklist item appears in the Dev DoD. Confirm all derived artifacts are current before submitting.
- **UAT stage**: QA validation now includes shared-module review (if shared modules were modified) and empirical-items classification. Expect slightly more thorough UAT passes.

### Pipeline Maintainers

- Gate criteria in `quality-gates.md` now include 4 new validator criteria (Gates 3, 5, 6, 7). If you maintain custom gate logic, review the new criteria.
- The Gate 5 capacity threshold has changed from a single 80% block to a two-tier WARNING/BLOCKING model. Any tooling or documentation referencing the old 80% block should be updated.

### Sub-Agents (Architect, QA, Developer)

- QA agents receive new shared-module review guidance in `quality/SKILL.md`.
- Developer agents encounter a new filename reconciliation entry condition at Stage 6.
- All agents benefit from cleaner upstream inputs as phantom references and capacity overcommit are caught earlier.

---

## Files Modified

| File | Changes |
|------|---------|
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | Stage 7: shared-module review step. Stage 6: filename reconciliation entry condition + derived artifact regeneration step. Stage 5: matrix validation step. |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | Gate 7: empirical-items criterion. Gate 3: phantom reference WARNING. Gate 5: two-tier capacity threshold. Gate 6: derived artifact regeneration criterion. |
| `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | Empirical-items tracking template added. |
| `delivery-team/skills/delivery-flow/references/project-templates.md` | Capacity matrix and coverage matrix templates added with Light Mode waiver. |
| `delivery-team/skills/quality/SKILL.md` | Shared-Module Review Protocol section added. |

---

## Migration Notes

### Breaking Changes

**None.** This release introduces no breaking changes.

- **Config schema**: Remains at v2.3. No new config keys were introduced. Existing `.delivery/config.yml` files require no modifications.
- **Existing pipelines**: All changes are additive. Pipelines in progress will encounter the new gates and validators only when they reach the relevant stages. No mid-pipeline disruption.
- **Hook scripts**: No Python hooks were created or modified. All enforcement is through markdown reference file changes that sub-agents interpret at runtime.

### Behavioral Changes (non-breaking)

These are not breaking, but pipeline users should be aware:

1. **Gate 5 threshold relaxation**: The previous 80% hard block is now a WARNING. If your team relied on the hard block to prevent overcommit, note that >80% now only warns (with required acknowledgment). The hard block is now at >100%.
2. **New `[PLANNED]` annotation convention**: Design stage authors should annotate file paths that will be created in later stages with `[PLANNED]` to avoid phantom reference WARNINGs. This is a convention, not a tooling requirement -- unannotated phantom paths produce warnings but do not block at Design.
3. **Dev entry gate**: The filename reconciliation gate at Dev entry is new. Pipelines that previously passed from Architect to Dev with unresolved file references will now be blocked until references are resolved.

### Upgrade Steps

No manual migration steps required. The changes take effect on the next pipeline run that loads the updated reference files.

---

## Documentation Updates Needed

| Document | Update Required | Priority |
|----------|----------------|----------|
| `CLAUDE.md` | Update the "delivery-team Plugin" table to mention stage health hardening (new gate criteria, shared-module review, capacity matrices). Add note about two-tier capacity threshold model under "Delivery-flow pipeline architecture". | P1 |
| `delivery-team/skills/delivery-flow/SKILL.md` | If the orchestrator references gate criteria or stage steps by number, verify step renumbering in Stages 5, 6, and 7 is reflected. Check for any hardcoded step references. | P1 |
| `CHANGELOG.md` (if exists) | Add v2.11.0 entry summarizing Stage Health Hardening. | P1 |
| `README.md` | No update needed unless it documents specific gate criteria or stage steps (it currently does not at this level of detail). | P2 -- verify |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | No update needed -- schema remains v2.3 with no new keys. | None |

### CLAUDE.md Specific Updates

The following sections of `CLAUDE.md` should be updated:

1. **"Delivery-flow pipeline architecture" bullet list**: Add a bullet noting the two-tier capacity threshold model (>80% WARNING, >100% BLOCKING) and the `[PLANNED]` annotation convention for phantom reference handling.
2. **"delivery-team Hooks" table**: No changes needed -- no new hooks were added.

---

## Retro Traceability

Every change in this release traces to a specific retrospective action item:

| Retro Item | FRs Delivered | Status |
|------------|--------------|--------|
| M1: Shared-module review checkpoint (c8f2) | FR-01, FR-02 | Done |
| M1: Empirical-items tracking template (k4m9) | FR-03, FR-04 | Done |
| M2: Phantom reference detection (k4m9) | FR-05 | Done |
| M2: Filename reconciliation gate (k4m9) | FR-06 | Done |
| M3: Capacity + coverage matrices (c8f2) | FR-07, FR-08, FR-09 | Done |
| M3: Sprint capacity threshold (k4m9) | FR-10 | Done |
| M4: Derived artifact regeneration (c8f2) | FR-11, FR-12 | Done |

All 12 functional requirements across 5 user stories are code-complete. All 32 acceptance criteria passed structural verification. 10 empirical validations remain pending for UAT runtime confirmation.

---

## Pending Empirical Validations

The following items require runtime pipeline execution during UAT to confirm behavioral correctness. They are documented here for UAT testers:

1. Shared-module review step triggers correctly in Stage 7
2. QA validator catches missing shared-module review
3. Phantom reference WARNING surfaces in Gate 3 without blocking
4. `[PLANNED]` exemption works at Gate 3, fails at Dev entry
5. Filename reconciliation blocks Stage 6 entry on missing files
6. Capacity matrix >80% triggers WARNING with acknowledgment
7. Capacity matrix >100% blocks with PO sign-off option
8. Coverage matrix unmapped FR = BLOCKING
9. Derived artifact regeneration step runs in Stage 6 sub-flow
10. Gate 6 blocks when derived artifacts not regenerated

> And there you have it -- the full tale of Stage Health Hardening, from phantom references to capacity matrices, all neatly documented and ready for the road ahead. Now, where did I put my second breakfast?
