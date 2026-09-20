# QA DoD Validation: Stage 2 Refine (PRD Revision 4), BACKLOG-108

Validator: QA Engineer (independent). Artifact: `.delivery/artifacts/02-refine/po/prd.md` (770 lines). Framing: TARGET-vs-CURRENT. Judged for well-formedness and testability, not for passing today.

Spot checks run from worktree root (stdlib only, no network, no `claude`):
- Canonical counting command, re-run: `guard-scope hits 91 files 31`, `pin 20 stamp 52 prose 19`. Matches PRD exactly.
- Probed PROSE_RE and BARE_RE with fresh strings (results in findings 1 and 2).

## Gate-result table

| # | Criterion | Result | Class |
|---|-----------|--------|-------|
| 1 | Every FR has an AC with a testable, unambiguous pass condition | PASS with warnings (FR-1.4, 2.4, 5.8, 7.3 are inspection-only, each names a concrete artifact line; FR-5.2 WARN check vague, finding 7) | blocking, met |
| 2 | ACs not satisfiable by a trivial edit defeating intent | FAIL (partial): AC-1.2a lacks a must-pass floor and can be gamed; AC-5.5 hand-editable | blocking |
| 3 | NFRs numeric with measurement method | PASS (NFR-1..13 all carry a number and a command; NFR-11 is inspection, acceptable) | blocking, met |
| 4 | Each gate closed by exactly one work item; each gate reachable after its own scope | PASS with warning: G-LIT closer AC-1.2c is authored in S1 but only satisfiable after S4; stated, ordered, and not listed under G1. G5 precondition list omits S1 to S3 (harmless) | blocking, met |
| 5 | Producer-validator separation (BINDING-4.5) enforceable and observable | FAIL (partial): observable only by self-reported manifest and a start-of-dispatch git status; finding 3 | blocking |
| 6 | Guard fixtures cover false positives and false negatives | FAIL (partial): must-hit floor exists (25/15), must-pass floor absent; must-pass set misses real false-positive classes; finding 1, 2 | blocking |
| 7 | Baseline/observed-model fails loudly on `unknown`/empty | PASS: FR-5.5 rules (a)(b)(c), AC-5.5b cases (i)-(iv), AC-5.5 asserts, AC-5.1 rejects `model_usage.unknown`. Warning on hand-edit, finding 4 | blocking, met |
| 8 | Edge cases and negative tests exist | PASS with warning: guard negative fixtures, capture-failure cases, `--strict-model`; no negative test for AC-1.6/AC-1.1b themselves | warning |
| 9 | Fixtures and test data have provenance | PASS: FR-5.10 sidecar (`claude_code_version`, `command`, date), AC-5.10 asserts real nesting; guard fixture provenance is weaker (finding 5) | warning |

## Findings

1. **Guard fixtures have no must-pass floor (FR-1.2 / AC-1.2a). Blocking.** AC-1.2a asserts `len(rule_a_must_hit) >= 25` and `len(rule_b_must_hit) >= 15` but nothing on `rule_a_must_pass` or `rule_b_must_pass`. An empty must-pass list makes the false-positive half of the test vacuous, and a regex loosened to `.` would still print `fixture failures 0 []` if must-pass is empty. Also the PRD names required strings (`run haiku 3 times`, `Section 5.5`, `Replace C12 with 4.7uF or greater`, etc.) but the AC never asserts those exact strings are present in the fixture file. Required fix: add `assert len(F['rule_a_must_pass']) >= N and len(F['rule_b_must_pass']) >= N` (suggest 10 each) and an assertion that each PRD-named string appears in the matching list.

2. **Real false-positive classes are unhandled and unfixtured (FR-1.2 PROSE_RE / BARE_RE). Blocking for guard quality.** Probed on this worktree: `Sonnet 4 stories`, `use Opus 2 times for review`, `the Opus 3 reviewers` all hit PROSE_RE. `in 5.0 seconds`, `for 4.5 hours`, `ship in 4.5 days` all hit BARE_RE (PRD only tests "under 2.5 seconds"; the major 4 to 9 range does not protect durations or counts). The PRD lists only the capitalised-family case as an accepted loophole and says use `model-pin-ok`, but FR-1.6 bans the marker at ship, so a legitimately worded sentence can never ship. Required fix: either add these strings to `rule_b_must_pass` and tighten the regexes so they pass, or add them to must-hit and document the wording rule ("write counts as words or digits before the family word"), and state how a legitimate sentence is reworded when the marker is banned. Round-trip both engines.

3. **BINDING-4.5 separation is weakly observable (FR-4.4, AC-5.2, AC-5.5b, AC-5.7, AC-5.9). Blocking.** Evidence is a dispatch manifest of self-reported agent IDs plus `git status --porcelain delivery-team/tests/smoke/lib` empty at validator start. It says nothing about `lib/` being modified during or after the validator dispatch, and nothing ties `test_meta.py` and `fixtures/` authorship to the validator ID. A producer could author the tests under a second label. Nothing requires that the meta-tests fail against the pre-fix parser. Required fix: add a check that (a) `git log --format=%an|%b` or a commit trailer `Dispatch-Id:` for files under `tests/` differs from that of `lib/` commits, and both are separate commits; (b) `git diff --name-only <validator-base>..<validator-end> -- delivery-team/tests/smoke/lib` is empty at validator END as well; (c) a mutation or red-first check: `-k real_shape` MUST FAIL on the unmodified `metrics.py` (documented today: `model_usage` keys `['unknown']`) and pass after FR-5.9.

4. **AC-5.5 / AC-5.4 hand-editable (FR-5.5). Warning.** The baseline JSON is checked for shape only; a hand-written JSON with `["claude-opus-x"]`, `mean>0` passes. Suggest an AC that ties the baseline to raw evidence: per-sample stream files (or hashes) whose `system/init` model equals `model_resolved[0]`, checked by a script independent of `metrics.py`.

5. **Guard fixture provenance (FR-1.2). Warning.** `scripts/model_pin_fixtures.json` is authored by the same S1 developer who copies the regexes; BINDING-4.5 does not cover it. The list is seeded from Challenger findings, which is fine, but the AC should record each must-hit string's origin (Challenger evasion, real repo line, or synthetic) in a `provenance` key.

6. **AC-2.1 and AC-2.5 remain floor-only for trivial edits. Warning.** AC-2.1 passes on any whitespace-insensitive change to a source line and does not account for a named line that legitimately appears twice in a file (false "still present"). AC-2.5 passes on keyword salad in one added line. Both are honestly labelled floor checks and paired with the adversarial reviewer and dispatch manifest, but the pairing is inspection-only. Suggest a checklist line in the adversarial artifact ("AC-2.1/2.5 intent verdict") required by AC-2.3b.

7. **AC-5.2 vague (FR-5.2). Warning.** "-rA output contains a WARN line per missing field" does not say how a WARN is emitted (log line, pytest warning, stdout) or its exact text. Specify the literal string, e.g. `WARN missing thinking_tokens`, so the check is greppable.

8. **AC-3.3a date floor (FR-3.3). Warning.** `>= 2026-09-20` accepts today's date for `fitness_review_due`, defeating the stated intent (a future review date per `governance/fitness-review.md`). Require `>` today and `<=` the governance interval.

9. **AC-1.1b regex. Warning.** `branches:\s*\[\s*main\s*\]|^\s+-\s*main\s*$` matches a `- main` list under `pull_request:` instead of `push:`, so a workflow with push only on a different branch could pass. Parse the `push:` block, or use the stdlib to split by top-level keys.

10. **AC-1.6 and AC-DISP negative tests absent. Warning.** No test proves AC-1.6 or AC-DISP actually fails on a violating tree. Add one negative case each in the meta-tests or a documented dry run.

## Verdict

STATUS: NOT_DONE. Findings 1, 2 and 3 fail blocking criteria 2, 5 and 6. All fixes are small edits to AC text; the rest of the PRD is well-formed, numeric, and shows executed evidence (canonical command reproduced exactly: 91 hits / 31 files). Findings 4 to 10 are warnings and need not block once 1 to 3 are fixed.
