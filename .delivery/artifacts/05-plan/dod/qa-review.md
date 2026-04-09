# QA DoD Review — Stage 5 Plan

**Reviewer**: Legolas (QA) | **Date**: 2026-04-08 | **Pipeline**: run-2026-04-08-a1f3
**Feature**: Paired Constraints Primitive (`constraints.yml`)

> *"My eyes see far. I find no shadow on this ridge."*

## Gate Checks

1. **FR→TC traceability (memory c8f2 lesson)** — PASS. test-strategy.md §1 maps all 8 FRs + 6 NFRs to 24 TCs, 1:1. No FR unmapped, no orphan TC.
2. **Story AC testability** — PASS. US-1..US-9 ACs are rule-checkable: file presence, schema conformance, grep exit codes, validator non-zero exits. No hand-wavy verbs. AC-9.3 explicitly names the US-8 check path.
3. **Forbidden vocabulary oracle is a concrete command** — PASS. §3 ships one runnable `grep -rEiw` with enumerated token list, scoped to `.delivery/artifacts/04-architect/`. Exit 1 = PASS, any match = FAIL with file+line.
4. **Empirical/deferred honesty** — PASS. §6 flags AC-6/NFR-1, NFR-5, and ADR-003 false-positive rate as `[EMPIRICALLY DEFERRED — UAT + 5 runs]`. Labeled, not hidden.
5. **Rollback test defined** — PASS. §5 TC-ROLL-1/2/3 cover behind-flag dormancy, no gate fire, and ignored-on-disk `constraints.yml`. Binary oracle.
6. **US-9 dogfood pass/fail** — PASS. AC-9.1 (exact path), AC-9.2 (schema validator), AC-9.3 (US-8 DoD). Binary outcome. S4 sequencing honors "no DoD before dogfood" memory lesson.
7. **Plan coherence with test effort** — PASS. SM's S3 hard-cap placement does not collide with QA work. 11 QA pts land alongside US-8/US-9 in S4 without displacing story points.

## Minor Observations (non-blocking)

- §1 TC-FR3-2 validates the PRD FR-3 enumerated list; §3 oracle uses a superset (stricter). Lock the verbatim list in US-4 DoD — already tracked as CR-1 / I-1 by PO/SM.
- NFR-5 token delta owned by Data Analyst at UAT per SM I-3. No gap.

## Verdict

All 7 gate criteria satisfied. The bow is strung; every arrow is counted; every mark has a name.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/dod/qa-review.md
SUMMARY: All 7 gates pass. 24 TCs trace 1:1 to 8 FRs + 6 NFRs. Oracle is one grep. Deferrals labeled honestly. Rollback clean. The bow is strung.
```
