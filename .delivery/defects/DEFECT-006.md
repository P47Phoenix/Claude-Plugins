# DEFECT-006: Stale Wave-2 UAT artifacts share `07-uat/dod/` directory without archive demarcation

**Status**: Open
**Severity**: P1 (process / documentation hygiene; not BLOCKING merge)
**Type**: Run-record drift / artifact-directory hygiene
**Discovered**: 2026-05-05 (run-2026-05-05-tk3, Stage 7 PO DoD review)
**Pipeline**: run-2026-05-05-tk3
**Reporter**: PO (DoD validator, FRESH dispatch — final go/no-go authority)
**Classification**: Documentation / run-record hygiene (single occurrence; precedent for systemic fix in `delivery-flow/SKILL.md`)

## Summary

Three Wave-2 (predecessor `run-2026-05-05-tk2`) DoD review files share `.delivery/artifacts/07-uat/dod/` with the new tk3 review files written this run, with no archive demarcation. A reader landing in `07-uat/dod/` cannot tell which review pertains to which run without opening each file's front-matter.

## Affected files

| File | Front-matter | Body refers to | Status this run |
|------|--------------|----------------|-----------------|
| `.delivery/artifacts/07-uat/dod/qa-review.md` | 2026-05-03; "Wave 2 R2 Final Validation" | Wave 2 scenarios | Stale (kept) |
| `.delivery/artifacts/07-uat/dod/devops-review.md` | 2026-05-05; "Wave 2 DevOps Cross-Validation R2" | Wave 2 (47 files / 5 stories) | Stale (kept) |
| `.delivery/artifacts/07-uat/dod/techwriter-review.md` | 2026-05-05; "Wave 2 UAT TW DoD" | Wave 2 numeric bindings | Stale (kept) |
| `.delivery/artifacts/07-uat/dod/po-review.md` | 2026-05-03; "Wave 2 PO Go/No-Go" | Wave 2 ACs (497-line trim) | **Overwritten** by this tk3 PO review (resolves one file) |

Tech-Writer cross-doc-consistency-report.md §"Stale-artifact drift" §line 38-46 lists six files (including QA `test-plan.md` and `test-cases.md` from `07-uat/qa/`); however, on PO inspection those two QA files ARE tk3-fresh (header `run-2026-05-05-tk3`). Only 4 files are actually stale, and one (po-review.md) is overwritten this run, leaving 3 residual.

## Severity rationale

P1, not BLOCKING:
- Numeric drift across the 9 canonical values (Tier-A budget, schema v2.9, hash, etc.) is **zero** within tk3 artifacts — the stale files describe a different release, they do not contradict tk3 values.
- Risk is reader confusion (a future reader sweeping `07-uat/dod/*.md` for the "current" review state cannot disambiguate by directory).
- Does not block merge; the tk3 artifact set (release-plan, dogfood-report, cross-doc-consistency-report, release-notes, user-guide, four go-no-go-input files, this PO review) forms a complete and internally consistent record.

## Recommended fix (proposed solution — autonomy per `feedback_team_autonomy.md`)

**Option A (minimal-touch, recommended)**: prepend a single banner line to each of the 3 residual stale files:

```markdown
> ARCHIVE — Wave 2 (predecessor run-2026-05-05-tk2). Superseded by tk3 artifacts in same directory. See `.delivery/artifacts/07-uat/dod/po-review.md` (this run).
```

**Option B (cleaner, follow-on)**: move the 3 residual stale files to `.delivery/artifacts/07-uat/_archive-tk2/` (matches the `.delivery/memory/archive/` precedent). Single `git mv` per file; no rewrite needed.

**Decision**: Option A this run (zero-risk; preserves history in place); Option B as a follow-up batch when the next Wave runs and the same directory hygiene problem manifests.

## Systemic root cause

`delivery-team/skills/delivery-flow/SKILL.md` Stage 7 dispatch instructions do NOT prescribe a stale-artifact archival step at the start of UAT for a successor run that reuses the `07-uat/` directory. The orchestrator pattern is: each run's UAT subagents write to fresh subdirectories under `07-uat/<role>/` (qa, devops, tech-writer) and the predecessor's reviews remain in `07-uat/dod/` as read-only history. There is no automated demarcation step.

## Follow-up wave

- **This run (run-2026-05-05-tk3)**: PO writes new `po-review.md` (overwrite). Apply Option A to `qa-review.md`, `devops-review.md`, `techwriter-review.md` as a same-PR follow-up if the orchestrator agrees, OR queue as the first item of the next-run UAT.
- **Next wave (BACKLOG-103 or successor)**: add a Stage 7 entry-step to delivery-flow/SKILL.md: "If `07-uat/dod/*-review.md` exists with prior-run provenance, prepend ARCHIVE banner OR move to `_archive-<prev-run>/` before writing this run's reviews." Link this defect from the change.

## Sub-finding (P3 cosmetic)

`.delivery/artifacts/07-uat/qa/go-no-go-input.md` line 9 cites `test-plan.md` and `test-cases.md` as evidence — both pointers DO resolve to the correct tk3-fresh files (verified by PO this run). The Tech-Writer cross-doc-consistency-report.md §line 51 P3 finding ("retarget evidence pointers to `dogfood-report.md`") is itself based on a misclassification — the QA files are not stale, so the P3 fix is unnecessary. No action required for this sub-finding; close as not-a-defect.

## Cross-doc-consistency-report self-correction

Tech-Writer's cross-doc-consistency-report.md §line 38-46 should be amended to list 4 stale files (the 4 dod reviews), not 6. Recommended single-line correction during the next run's UAT to reflect the actual state. Filed here so the trail is preserved.

## Defects/story impact

- Stories this run: 1
- Defects this run: 1 (this defect, P1, non-blocking)
- Rate: 1.0 — exceeds the 0.4 stop-rule threshold IF measured per-story per-run.
- However, the BACKLOG-102 stop-rule is "defects/story rate >0.4 across any 3-PR window" — single-run rate is not the trigger. PO judgment: this defect is documentation hygiene, not a code/process regression; continue stop-rule arming and revisit with the next two PRs as the rolling window.

## Decision (per `feedback_team_autonomy.md`)

PO autonomously logging this defect with both severity classification and proposed fix (Options A and B) as required by `feedback_po_logs_issues.md`. Not escalated. Decision: GO on the merge; apply Option A as a same-PR follow-up at orchestrator's discretion; defer Option B systemic fix to the next wave.
