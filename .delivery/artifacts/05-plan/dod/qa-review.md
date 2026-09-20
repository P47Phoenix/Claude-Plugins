---
verdict: NOT_DONE
run: run-2026-05-28-o48m
stage: 5
role: qa
reviewer_note: skill delivery-team:qa unknown in this session; role applied from brief
blocking_count: 3
warning_count: 7
---
# QA DoD review, Stage 5 Plan (BACKLOG-108)

Prose: caveman-lite. Read: plan.md, stage-summary.md, PRD, ADR-lmr-004 (P0 rules 1a..1d, red-first), ADR-lmr-005 (items 1..9).

## Verdict
NOT_DONE. Plan is strong: id matrix complete, PA ACs mostly have observable results, red-first and P0 rules faithfully carried. Three gaps let a requirement go unmet while checks pass. All cheap to fix in plan text.

## Blocking issues

B1. PA-15 (AC-5.5c) lets distinctness fail soft.
- PA-15 says: no `message.id` and no `uuid` fallback -> "report WEAKENED, never silent". Plan gives WEAKENED no pass/fail consequence. S5b validator (qa) can PASS AC-5.5c with WEAKENED, so five identical or fabricated streams pass. PRD AC-5.5c is a hard check; plan thins it (D15 says PA supersedes).
- Fix: WEAKENED = AC-5.5c FAIL at UAT unless PO writes a waiver in `07-uat/`; UAT DoD checks for that file.

B2. Stage 6 skip list leaves baseline writer code untested until the paid run.
- D1a defers AC-5.1, 5.4, 5.5, 5.5c, 5.6 to UAT. Stage 6 tests cover only parser, command, consistency failures (5.4b, 5.5b) and abort-on-nonzero (PA-18). No S5a AC runs `init_baseline` end to end on fixture streams (runner stubbed, no `claude`) and asserts the AC-5.1 keys (`tokens.cache_hit_ratio`, `model_usage.*`, no `unknown`), `model_requested`/`model_resolved`/`model_pin_env`/`host_context`, `samples[]` with `stream_sha256`, `hard_max` 3.0. First real exercise of that code is the $15 UAT run.
- No re-entry path: if S5b fails, code defect found after Stage 6 DoD "DONE". Plan silent on returning to S5a (red-first, fresh validator, DoD re-run) and S6 re-freeze.
- Fix: add PA (S5a) dry-run of `init_baseline` on the real-shape fixture x5 copies (mocked runner) with the AC-5.1/5.4/5.5c snippets pointed at the temp baseline, expected `OK`. Add a rule: S5b defect reopens S5a under 5.3 rules and repeats H2 only for re-runs.

B3. PA ACs are not all concrete; numbering gap.
- No PA-9 (list runs PA-8 -> PA-10). Either dropped AC or typo; carry item could be lost. Plan must say which.
- Self-check (section 6, qa row) admits "PA text is prose, validators write the runnable snippets". Several have no command and no expected output: PA-8 (whole-tree run "lists hits", no pass value), PA-12 (points to a section, not a command; "real checker written by the validator"), PA-22 (no check for the max-7-runs or wall ceiling), PA-13 ("cross-checked" without stating the pass output).
- Fix: for each PA give the command form and the exact expected line or rc, or state that Stage 6 QA must publish snippets in the S-unit report before the producer starts (and QA reviews them at the red step).

## Warnings

W1. AC-DISP transcript check can pass on typed ids. PA-21/ADR-005 item 8: layout drift prints `TRANSCRIPT_CHECK=SKIPPED layout-drift <id>` and "never fails the ship on its own". Non-recovered manifests (Stages 5..7) are then unverified. Require: SKIPPED on any Stage 6/7 manifest needs PO note in S7b report, or fail S7b.
W2. PA-1 `files-scanned K > 0` is a weak floor. A guard that scans 1 file passes. Add K equals count of tracked in-scope files (`git ls-files -z` filtered by the six extensions) or a floor.
W3. Guard-gate checker for P0 (PA-12) authored by validator with no negative self-test required (PA-21 has one, PA-12 does not). A permissive checker passes any P0. Require the ADR experiments (computed key, method added, real impl in stub) as self-tests: each must FAIL the checker.
W4. Producer/validator disjointness is enforced only for S5a (PA-13). Section 2 says "differs on every row" but no AC checks trailer sets for S1..S4, S6. Add one snippet: producer `Dispatch-Id` set disjoint from manifest ids per unit.
W5. S1 file scope lists `scripts/model_pin_fixtures.json` under the producer, while the validator "independent fixtures" are also required. If the producer owns AC-1.2a fixtures (>= 25/10/15/12 strings) the guard passes its own tests. State who authors must-hit/must-pass strings; validator owns them.
W6. Fixture genuineness. H1 capture is real, but nothing checks the committed `stream_real_shape.jsonl` is that capture (hand-edited files pass PA-14 and PA-15 presence). Add: sha256 in provenance equals file hash, and provenance carries the exact capture command; QA verifies at H1 time.
W7. FR-1.4 and FR-2.4 close by "inspection" of the dispatch report (self-reported acknowledgement). Acceptable for light stage, but note as floor only; commit trailer or dispatch-prompt grep is cheap.

## Two ways a plan-level check passes while a requirement is unmet
1. AC-5.5c: five identical copies of one real stream, no `message.id`, no `uuid`: PA-15 reports WEAKENED, S5b qa records "reported, not silent", UAT passes. NFR-6 (five independent samples) unmet. (B1)
2. Stage 6 DoD DONE for G5: parser and fixture tests green, `init_baseline` never run end to end; a writer that omits `samples` or `model_pin_env` only shows at the paid run, after ship-readiness is declared. AC-5.1/5.5 are then judged on a baseline produced by the same untested code. (B2)
3. AC-DISP: an executor types ids in a Stage 6 manifest; CLI layout changes; check prints SKIPPED layout-drift, ship proceeds. (W1)
4. Guard: rc check and canary pass while `files-scanned 3` because a listing bug filters to 3 files; real pins elsewhere never seen. (W2)

## Evidence (checked)
- PRD AC ids vs plan matrix (grep): every PRD AC appears in plan sections 3.1/3.2. Parents `AC-2`, `AC-5`, `AC-1.6`, `AC-S3` are group or docstring ids, not gaps. `AC-3.x`, `AC-4.x` in the plan are shorthand for listed ids.
- D1a skip list matches PRD reading: AC-5.1 (line 508) reads baseline; correct to defer; but see B2.
- Red-first: PA-13 and section 5.3 match ADR-lmr-004 items 1a..1d and void-types list; hard-coded-constant case covered by "every test FAILED".
- PRD AC-2.3b PASS-verdict requirement stays in force (plan does not amend it).
- Story to validator to stage mapping: every story has a validator role differing from producer role; separation observable only for S5a (W4).
- Stage 6/7 exit lists G5 partial then closed at UAT: consistent.
