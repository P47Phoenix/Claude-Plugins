run: run-2026-05-28-o48m
purpose: running ledger of Stage 6 decisions, plan/ADR amendments, and residuals (orchestrator-owned)

## Amendments (recorded here, PRD/ADR text untouched; PO confirms at Stage 7 acceptance)

A-1 PA-9 (core.hooksPath install) moves from S1 to S7/human. Reason: `git config --local core.hooksPath` writes the SHARED .git/config and would arm the blocking pre-commit hook for the user's main checkout and every other session. S1 tested hooks with `-c core.hooksPath` and temp repos. Hooks are inert in this checkout. S7 handoff prints `git config --local core.hooksPath .githooks` and `git config --unset core.hooksPath` plus a `hooksPath=` log line. Owner: PO/Michael.
A-2 ADR-lmr-002 amendment (S1 DoD architect W4): `--strict` flag accepted, inert (hooks own strictness via MODEL_PIN_STRICT); `--paths` implies listing; relative `--paths` resolve against the repo toplevel; known_fp `expect:"pass"` supported; empty default scope prints `hits 0 files 0` but exits 2 (judge on rc).
A-3 Pre-push is advisory unless MODEL_PIN_STRICT=1 (ADR reference hook always strict). The S7 ship gate MUST run the guard strictly itself (blocking control), export MODEL_PIN_STRICT=1, run `python3 .delivery/artifacts/06-development/S1-guard-tests/mutation_and_floor.py` from the REPO ROOT (PA-7 floor lives there), and call scripts directly because hooks are inert.
A-4 The guard workflow is RED on main until S4 brings hits to 0. Do NOT push to main before S4 (post-push PA-26 would fail). Branch pushes do not trigger the main workflows.
A-5 Stage 6 manifests list only roles in config `dod_validators.development` [developer, qa, architect, tech-writer]. Devops reviews are recorded via Dispatch-Id commit trailers, not manifests.

## Residuals (accepted, non-blocking; owner PO unless noted)

R-S1-1 GIT_DIR set without GIT_WORK_TREE makes the guard fail open from a subdir. Trigger: any caller sets GIT_DIR. Hardening: strip GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE before calling git.
R-S1-2 `--paths` drops args starting with `--`; relative `--paths` resolve against toplevel not cwd (`--paths "sp ace.md"` from a subdir scans 0 files, rc 0). Trigger: hook or script passes cwd-relative paths from a subdir.
R-S1-3 pre-commit scans the working-tree file, not the staged blob. Trigger: partial staging false negatives observed.
R-S1-4 pre-push loop children inherit stdin (`</dev/null` hardening); `remote_sha` unused (SC2034); unknown flags ignored silently; one non-UTF-8 scanned file exits 2 (by design).
R-S1-5 Regex gaps (QA N3), PRD-verbatim contract gaps: single-quoted stamps, `opus_4_7`, odd whitespace/zero-width, mixed case, fullwidth digits, `**Opus** 4.7`, non-.md files for Rule B. Trigger: any real miss.
R-S1-6 pre-push N2: `Budget-Exception:` cannot apply to a direct push (main-push run red); consistent with plan rule PA-20.
R-S1-7 QA independence rests on commit order and manifest ids (all commits share one git author).

## Unit ledger

S1 Guard: producer ab0a6adcdaa36cc80 (6560e64), fix a3a4092db05792c5f (b082a0c); story validators af9b0fca71235419d (qa, 3337deb), afcc7a46ca9bd20ac (devops review, b870843: APPROVE); QA first verdict FAIL (D1 subdir fail-open) fixed; DoD round 1: qa a099373e856d0d420 DONE, developer a7f0e958e47ad9222 DONE, architect a9046d102caf82988 DONE (0 blocking). Manifest: dispatch-manifest-S1.txt. Guard on real tree: files-scanned 486, `guard-scope hits 85 files 30` (91/31 minus the 6 pin literals of the rewritten old workflow).

S2 Keystone prose: producers 31ae759 and 1e36eb2, fix a46a11ee66de0147b (1304e2a). Round 1 validators: architect afcab787efc283126, tech-writer a12643ec9e60f1ec8, qa a3708e71fa6f798db (B1 API shape fixed; the fix round dropped the delegation anchors, then restored). DoD round 2: architect a1f6316f53fa69575 DONE, qa a87b8afed927a9cbc DONE (dispatch-manifest-S2-r2.txt). S2 DONE.
A-6 Deliberate exception: tech-writer's "subagents" to "sub-agent" wording change in delivery-flow lines 275-276 rejected, because the AC-2.5 regex requires the literal word `subagents`.
Carry to S3: prompt-engineer stamp examples at lines 415/417 (`opus-4-7`, `4-7-1`) must be cleared or AC-3.1b fails. "Claude 4.7 and later" at prompt-engineer lines 351/359 is doc-accurate but may trip the AC-3.1b bare-version rule (guard shows no hit today). S3 ledger rows: delivery-flow REVIEWED_CHANGED, prompt-engineer REVIEWED_CHANGED, product-delivery NO_CHANGE_NEEDED (only stamps at lines 5 and 7), orchestrator-doctrine REVIEWED_CHANGED. S6 records the telemetry prefix 8c2ebf97... to 6c9664d9... and re-freezes the governance hash after S3.

S3 Stamps: producer ad327ebadca5dc613 (23d181f, amended trailer). Validators qa afd266c8d4c382638 DONE; architect ad19db62c11d6d0a6 BLOCKING then fixed by orchestrator (ledger verdict token CHANGED, agent_id = architect id; a value-only fix, no prose change). Guard: 13 pin hits left, all S4-owned, 0 stamp/prose. Manifest: dispatch-manifest-S3.txt. S6 must re-freeze governance/cache-prefix-hash.txt (delivery-flow changed).

S4 Pins: producer a42e8bef5d73b9ce8 (24409b6, trailer amended). Validator qa a95c25529b5b5ff71 DONE (dispatch-manifest-S4.txt). Guard on real tree: files-scanned 486, guard-scope hits 0 files 0, rc 0; mutation 10/10 killed. AC-4.6 not run by QA (S4 touches no SKILL.md); AC-4.4 belongs to S5. A-4 is lifted for the guard hit count, but main pushes still need the H3 gate.

S5a P0 stub: producer a09bb224d9d7f3689 (committed with Dispatch-Id, base_sha 515dcbc for the PA-12 P0 gate; the amend changed the head sha, so read head from git log, not the producer report). Offline: 3 passed, guard hits 0, budgets pass. Pending: QA-authored checkers (check_p0_gate, check_red_first, check_distinct, spend_check, dry_run_baseline), red validator test_model_capture.py, then P1 by a different producer. Fixture capture blocked_on: H1 (needs operator_go: H1 from a human turn, max 2 x $0.25). H2 (S5b baseline), H3 (push main) still closed.

S5a validators: QA a950caefe7b2173e4 (checkers + red test_model_capture.py, two commits after the P0 stub; trailer set to real id). Self-tests: spend_check 15/15, check_p0_gate 17/17, check_red_first 27/27, check_distinct 10/10. Red test on stub: 28 failed, 7 skipped, 0 void. check_red_first prints RED_FIRST FAIL only because 7 real_shape tests are BLOCKED on H1 (no real fixture; none fabricated). PA-24 dry-run uses a labelled synthetic template until H1. Open for P1 developer: WARN-missing-field location (tests check build_report advisory_warnings + _render_summary_md), copied-stream exception type (tests use pytest.raises(Exception)). Next: after H1 fixture capture + sidecar -> RED_FIRST OK -> P1 by a different producer than a950caefe7b2173e4 and a09bb224d9d7f3689? (P1 producer must differ from validator id per PA-13b). blocked_on: H1.
