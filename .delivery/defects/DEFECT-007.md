# DEFECT-007: No published CHANGELOG.md across 5 waves of skill-token-economy initiative

**Status**: Open (will move to Resolved on this commit when CHANGELOG.md lands + systemic-fix carry-forward registered in next initiative's backlog)
**Severity**: P2 (process gap — user-visible quality issue; no functional break)
**Type**: Documentation-process / Release-management
**Discovered**: 2026-05-13 by user inquiry ("did the team update the changelog?")
**Pipeline**: cross-run (5 prior waves) — surfaced post-Wave-3
**Reporter**: PO (auto-log per `feedback_po_logs_issues.md` — user inquiry surfaced gap)
**Classification**: Documentation-process / Release-management (systemic gap across 5 shipped waves; not specific to one wave)

## Summary

User asked "did that team update the change log?" after Wave 3 of the skill-token-economy initiative shipped. Answer: NO. There is no `CHANGELOG.md` in the repo. None of the 5 waves (Wave 0, Wave 1, Wave 2, caveman, Wave 3) touched a changelog. Releases are tracked via git tags + `marketplace.json` version bumps + per-wave commit message bodies + scratch `.delivery/artifacts/07-uat/tech-writer/release-notes.md` artifacts. There is no published consolidated changelog at the repo root that a user can read to understand what shipped.

## Affected scope

All 5 prior waves of the skill-token-economy initiative:

| Wave | Run | Commit (head) | Tech-Writer release-notes scratch? | CHANGELOG.md updated? |
|------|-----|--------------|:---------------------------------:|:---------------------:|
| Wave 0 | run-2026-04-30-* | `d0e0928` | Yes (scratch only) | No |
| Wave 1 | run-2026-05-04-tk1 | `b412a40` | Yes (scratch only) | No |
| Wave 2 | run-2026-05-05-tk3 | (Wave 2 R2 commit) | Yes (scratch only) | No |
| caveman | run-2026-05-05-tk3 (caveman-lite) | (same PR) | Yes (scratch only) | No |
| Wave 3 | run-2026-05-09-tk4 | `2609272` | Yes (scratch only) | No |

The gap is systemic, not specific to any single wave's Tech-Writer. Every wave produced a release-notes scratch artifact and shipped without promoting it.

## Root cause

Tech-Writer UAT artifact `release-notes.md` is **run-scoped** at `.delivery/artifacts/07-uat/tech-writer/release-notes.md` (scratch — overwritten each run). It is never promoted to a published top-level `CHANGELOG.md`. No stage in delivery-flow pipeline explicitly produces a repo-level CHANGELOG entry; the closest artifact is the per-run scratch file. The Tech-Writer cross-doc-consistency-report UAT gate did not flag the gap because CHANGELOG.md was never in scope to check against — you cannot find drift between two artifacts when one of them does not exist.

Three reinforcing failure modes:

1. **Artifact-scope mismatch**: release-notes lives in `07-uat/tech-writer/` (run-scoped) instead of repo root (release-scoped). Scratch artifacts are not durable release records.
2. **Pipeline-stage gap**: Stage 7 UAT has no explicit "promote release-notes to CHANGELOG" step. Tech-Writer's DoD checklist does not require a CHANGELOG update.
3. **Retro blind spot**: 5 consecutive retros (Wave 0 → Wave 3) did not surface the gap. Retro template does not prompt "is the change log updated?" The user's inquiry is the surfacing event.

## Fix (this commit — same-PR, parallel Tech-Writer dispatch)

Tech-Writer authors `CHANGELOG.md` at repo root, derived from:
- The 5-wave commit history (`d0e0928`, `b412a40`, Wave 2 commit, caveman commit, `2609272`)
- Per-wave Tech-Writer release-notes scratch artifacts where retrievable
- `marketplace.json` version bumps for version markers

**Format**: Keep-a-Changelog (https://keepachangelog.com), single `## [Initiative] skill-token-economy delivery-team` heading covering all 5 waves as sub-entries. Parallel Bilbo dispatch (same PR as this defect log).

## Systemic fix (carry-forward, NEXT INITIATIVE)

Add a CHANGELOG-update step to delivery-flow Stage 7 UAT (Tech-Writer responsibility). Two implementation options to be chosen at next initiative's authoring time:

- **Option (a)** — patch-fragment model: Tech-Writer authors a `CHANGELOG.md` patch fragment at Stage 7 and DevOps applies it at merge time. Lower coupling; merge-time apply allows multi-PR rollups.
- **Option (b)** — promotion model: the existing `release-notes.md` scratch artifact gets explicitly promoted to `CHANGELOG.md` (prepend or section-merge) as a named Stage 7 step. Simpler; reuses existing artifact; no new template.

Pick (a) vs (b) at next initiative's authoring time. Either way, Tech-Writer DoD checklist must include "CHANGELOG.md updated (or patch fragment authored)" as a gate.

## Carry-forward backlog

File the systemic fix as a Work Item at next-initiative authoring time. Two slot options:

- Append as a WI in **BACKLOG-105** (mtg-commander Wave 0) admin Story, OR
- Stand up **BACKLOG-106** "delivery-flow Stage-7 CHANGELOG promotion step" as its own backlog item.

PO decides at BACKLOG-105 authoring (next initiative kickoff). Either path closes this defect's systemic-fix obligation.

## References

- Wave 3 commit `2609272` — the most recent wave commit that should have shipped a CHANGELOG.md update but did not
- Wave 3 retro `.delivery/memory/archive/run-2026-05-09-tk4.md` — did not surface the gap (retro blind spot)
- User inquiry 2026-05-12 — surfacing event ("did that team update the change log?")
- This fix-commit — parallel Tech-Writer CHANGELOG.md dispatch (same PR)
- `feedback_po_logs_issues.md` — auto-log mandate (PO logs issues from user inquiries immediately)
- DEFECT-006 — adjacent run-record hygiene defect; same family (release-time documentation drift)

## Defects/story impact

- Stories this commit: 0 (defect-log + Tech-Writer parallel dispatch; no story execution)
- Defects this commit: 1 (this defect, P2, non-blocking — fix lands same PR)
- Rate impact: not a per-run rate event; this is a cross-initiative process defect surfaced retrospectively. Not counted against the BACKLOG-102 0.4 stop-rule rolling window.

## Decision (per `feedback_team_autonomy.md`)

PO autonomously logging with severity, root cause, same-PR fix, and systemic carry-forward plan. Not escalated. Decision: GO on same-PR CHANGELOG.md fix (parallel Tech-Writer Bilbo dispatch in flight); systemic fix queued for next initiative's backlog at BACKLOG-105 authoring time.
