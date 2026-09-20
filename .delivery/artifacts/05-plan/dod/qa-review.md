---
verdict: DONE
run: run-2026-05-28-o48m
stage: 5
role: qa
round: 2
reviewer_note: skill delivery-team:qa unknown in this session; role applied from brief
blocking: []
blocking_count: 0
warning_count: 8
---
# QA DoD review, Stage 5 Plan (BACKLOG-108), round 2

Prose: caveman-lite. Read: round-1 review, plan.md rev 2 (changelog, 5.9, PA-1..PA-27), ADR-lmr-004 lines 76 and 109.

## Verdict
DONE. B1, B2, B3 closed. No new blockers. Eight warnings, all fixable by Stage 6 validators or a one-line plan edit.

## Round-1 blockers

B1 PA-15 WEAKENED: CLOSED.
- PA-15 now: WEAKENED = FAIL of AC-5.5c at UAT. Only exit is dated PO file `07-uat/ac-5.5c-waiver.md`; UAT DoD checks for the file. Command `check_distinct.py <baseline_or_streams>`: `AC-5.5c OK` rc 0, `WEAKENED` rc 1. Fail path is real.
- Prototype (scratch): 5 streams with non-overlapping `message.id` sets -> disjoint True; 5 identical copies -> overlap detected (disjoint False). Logic is cheap and does what PA-15 claims.
- W-A below asks for the negative case to be a required test.

B2 baseline writer untested: CLOSED.
- PA-24 runs `init_baseline` end to end on 5 validator-rewritten fixture copies, stub `claude` via PATH shim, temp baseline path, no spend (NFR-9 stated). Expected `DRYRUN OK` rc 0 with the AC-5.1/5.4/5.5c key list; injected non-zero outcome -> `DRYRUN ABORT_OK` and no file written; injected costs past ceiling -> `DRYRUN CEILING_OK` rc 3. Exercises abort and aggregate logic. Matches ADR-lmr-004 line 76 (a copied stream is rejected by init) and line 109 (ceiling rule).
- Re-entry rule 5.9 closes the loop: fix story back in Stage 6 (red-first if S5a code), Stage 6 DoD re-run on touched files, cache re-freeze if SKILL.md changed, PA-24 re-run if baseline/runner/report changed, aborted runs still count toward $15.00 and 7 runs, re-run past 5 needs fresh H2, prose change invalidates baseline (P6). Complete.
- Spend arithmetic prototype: `spent + 3.00 > 15.00` gives False at 12.00, True at 15.00 with 5 x 3.00 (so a 6th run is only legal when earlier runs cost less than cap; H2b text is true). Float sums of 0.1/2.9 combos showed no false stop, but see W-D.

B3 PA commands and gap: CLOSED.
- PA-9 exists (hooksPath install + log, expected `.githooks`). Numbering is now contiguous PA-1..PA-27 plus PA-13b.
- Commands with expected output present: PA-8, 9, 12, 13, 13b, 14 (`FIXTURE_HASH MATCH`), 15, 22, 23, 24, 25, 26, 27. Verified `comm -12 <(...) <(...) | wc -l` (bash) and `grep -vc` print counts as claimed.
- PA-1..PA-7, 10, 11, 16..21 are AC statements with observable values but no literal command. Per brief, checker scripts and snippets are Stage 6 validator work; each is falsifiable (rc values, exact lines, counts). Not a blocker.

## Warnings
W-A. PA-15/PA-24: add a required negative test. `check_distinct.py` on 5 identical copies (and on a stream set with no `message.id` and no `uuid`) must print `WEAKENED` rc 1. PA-24 only shows the OK path. Else a permissive checker passes.
W-B. PA-7 files-scanned floor. "K equals the tracked scanned-file count pinned from the baseline" will fail legitimately: S1 adds scripts and hook files; S5a adds `.py` files (in scope extensions) after the baseline. Also PA-8 says `base-sha.txt` line 1 is a 40-hex sha but does not say where the count lives (line 2?). Fix: K must equal the live `git ls-files -z` filtered count at run time, and the base count is only a floor (K >= base). State the file line. Also PA-7 opens with odd prefix "(Guard hardening, see below; hook install is PA-9) Guard hardening:". "see below" points nowhere; cosmetic, delete it.
W-C. PA-9 is not in the section 3.1 matrix row for S1 (only PA-6, PA-7 cited under FR-7.3) and no PRD FR owns it. Add PA-9 to an S1 row so the story-to-AC map stays complete.
W-D. PA-22 spend arithmetic on floats. Use `Decimal` (or cents ints) in `spend_check.py`; float sums of cent-level costs can land at 15.000000000000002 and stop a legal run, or the reverse. Also `spend_check.py` (PA-22) and the harness snippet (PA-16) are two implementations; PA-24 `CEILING_OK` should call the same `spend_check.py`, not a separate path. State that.
W-E. Checker location. PA-12/13/15/22/24 use `tests/...` with no root. Say `delivery-team/tests/smoke/tests/` and list `check_p0_gate.py`, `check_red_first.py`, `check_distinct.py`, `spend_check.py`, `dry_run_baseline.py` in the S5a validator file scope (currently only test_model_capture.py and fixture named). `spend_check.py` is consumed by S5b, so QA should publish it in the S5a report before H2.
W-F. PA-24 exit-code contract: "`DRYRUN OK` rc 0", "`DRYRUN CEILING_OK` rc 3" for one script. Say one invocation runs all three sub-cases and returns 0 only if all print their expected token (or use `--case` flags). Otherwise the single command line in PA-24 cannot produce both rc 0 and rc 3.
W-G. PA-21 in S7b: the fresh clone of `origin/main` has no `~/.claude/projects` transcripts and lacks the S7b manifest (H4 commit is after). Checker must take the transcript slug tree from the original project path and treat S7b's own manifest as written out of the clone. State this so `SKIPPED layout-drift` (= FAIL for S7b) is not tripped by topology.
W-H. Carried round-1 W2/W3 residue: PA-12 negative self-test is present (fixed). PA-13 checker also has "its own negative self-test as PA-12". Fine. Note only: PA-27 greps saved prompt files, which the orchestrator writes; it is a floor, not proof the agent loaded the skill. Acceptable for light stage.

## New contradictions from revision
- None blocking. S8, H6, H4-FAIL, PA-25/26 consistent: H3 covers ship push, H6 covers corrective push, H4 only on S7b PASS; PA-26 `UNVERIFIED manual` = FAIL matches H4-FAIL branch.
- H2 "up to 5 samples" vs 7 runs: consistent via PA-22 and section 5.6.
- Section 6 self-check says PA-8/12/13/22 fixed and PA-9, 13b, 23..27 added: matches the plan body.
- Gate protocol 1.4 vs PA-23: consistent (`operator_go:` line, `blocked_on: H<n>`).

## Evidence
- Prototype (python3, scratch): distinctness on disjoint vs identical `message.id` sets; spend check arithmetic incl. Decimal comparison; bash `comm -12` and `grep -vc` behaviour.
- ADR-lmr-004 line 76 (WEAKENED wording, copied-stream rejection) and line 109 (ceiling, 7 runs, extraction snippet) agree with PA-15, PA-16, PA-22, PA-24.
- Plan changelog (section 7) matches actual edits for QA B1..B3.
