<!-- run: run-2026-05-28-o48m -->
---
verdict: NOT_DONE
role: qa (DoD validator, fresh reviewer)
stage: 4 Architect (light)
run: run-2026-05-28-o48m
backlog: BACKLOG-108
blocking_count: 1
warning_count: 8
inputs: architecture.md rev 3, ADR-lmr-001..005, PRD rev 6 ACs, challenger loop-1..3
note: delivery-team:qa skill failed to load (unknown skill); role applied from the task brief.
---

# QA DoD review: Stage 4 design, BACKLOG-108

Overall: design is mostly testable. Most PRD ACs have a runnable path and loop 1-3 closed real holes. One internal contradiction makes the red-first evidence AC unsatisfiable as written. Small fix, but Plan cannot write a passing AC from the text today. Everything else is warning-level, carry to Plan.

## Blocking issues

### B1. P0 "stub" rule contradicts itself and contradicts the red-first check (ADR-lmr-004 section 2 and 6)

Two contradictions, one mechanism (the F6 fix from loop 3).

1. AST-body gate vs pinned stub. Section 6 item 1 says the BODY of every pre-existing function, and lists `build_report` and `init_baseline` among them, must be unchanged at P0 (Plan AC: `ast.dump` body at `base_sha` equals body at `validator_start`). Section 2 says the P0 stub of `build_report` "gains ... new keys present with `None`/empty defaults, existing keys unchanged". Adding keys to the returned dict is a body edit. A correct P0 fails the AST gate; a P0 that passes the AST gate cannot carry the pinned keys the validator needs for AC-5.5b(iv) and AC-5.5c tests. Evidence: ADR-lmr-004 section 2 table row `build_report` vs section 6 item 1 function list.
2. Stub behaviour vs "fails by AssertionError". Section 6 item 1 lets new functions "raise `NotImplementedError`" (for example `check_model_capture`). Section 6 item 2 requires the `real_shape` and capture-failure tests to fail at `validator_start` "with `AssertionError`, not ImportError or TypeError". A test that calls a NotImplementedError stub fails with NotImplementedError. A test written as `pytest.raises(ModelCaptureError)` against a non-raising stub fails with `Failed: DID NOT RAISE`, which is pytest's outcome exception, not AssertionError. So the AC passes only if every such test is written in bare-`assert` style and every stub returns a value. Neither is stated.

Effect: the Plan writes an AC that either fails a correct P0 (red-first evidence "void", per the ADR's own words) or forces the stub author to guess. Dev and UAT cannot verify BINDING-4.5 red-first.

Fix (architect, small): (a) drop `build_report` from the unchanged-body list, or say the stub adds keys via a new helper called from the pre-existing body and the AST gate excludes that one call, or exempt `build_report` explicitly; (b) replace "AssertionError" with a rule that survives: failing outcome, exception type not in {ImportError, ModuleNotFoundError, TypeError, NotImplementedError, `Failed: DID NOT RAISE`}, or require stubs to return legacy-equivalent values and tests to use bare `assert`; state which.

## Non-blocking warnings

### W1. Vacuous pass: AC-3.1b passes when the guard script is broken or missing
PRD AC-3.1b reads `subprocess.run([... '--list'], capture_output=True).stdout` and never checks `returncode`. If `scripts/check_model_pins.py` crashes, is renamed, or prints only to stderr, stdout is empty, `n = 0`. After S3 `frontmatter-only` count is also 0, so it prints `0 0` and passes with zero scanning. Concrete way to meet the AC and miss the requirement. Mitigation exists only indirectly (AC-1.2c and AC-1b would catch a broken script, but AC-3.1b itself proves nothing). Plan fix: assert returncode in {0,1}, assert the last stdout line matches `guard-scope hits \d+ files \d+`, and compare `n` to the summary count.

### W2. Vacuous pass: guard that scans nothing looks identical to a clean tree
Summary line `guard-scope hits 0 files 0` means zero files WITH hits, not zero scanned (ADR-lmr-002 D5). Nothing requires the scan to be non-empty or fail closed if `git ls-files` errors, cwd is wrong, or `isfile` filters everything. AC-1.2c, AC-1b, ship step 4 and S7b step 4 all print the same line for a scanner that saw no files. Step 5 (canonical count vs `--list` count) does not help because both are 0 in the same broken state. Pre-migration the 91 hits / 31 files count proves default mode works, but only at S1 close, not at ship or in the S7b fresh clone. Plan fix: add a canary AC (write a temp untracked `.md` with a synthetic pin in the repo, expect exit 1 and the file in `--list`, delete it), and state that the script exits non-zero if `git ls-files` fails. Add a `files scanned N` line if the PRD format allows.

### W3. Five identical streams pass the AC-5.5c text as written
PRD AC-5.5c script re-hashes each file and checks init model and cost mean, but has no distinctness check. Five copies of one real stream (same hash, same `session_id`) pass. ADR-lmr-004 section 5 says init-baseline rejects duplicates and "AC-5.5c also checks it independently", but the PRD snippet does not, and the producer-side rejection is bypassed by a hand-built baseline, which is what AC-5.5c exists for. Second route: edit `session_id` in each trimmed init line so hashes differ; init trims to four keys so `session_id` is the only distinguishing field in the trimmed line. Plan fix: AC-5.5c adds distinct hashes and distinct `session_id` across 5 files, and also requires that the sets of `message.id` (or result `uuid`/`duration_ms`) in the verbatim assistant/result events do not overlap across samples, which a hand-edit of `session_id` alone cannot fake.

### W4. AC-DISP transcript check is skippable and role-blind
ADR-lmr-005 item 6: transcript check is "supporting", skipped with a note when the directory is absent, layout UNVERIFIED across CLI versions. Item 4a makes it mandatory only for `transcript-recovered` manifests. A manifest with invented ids (`qa<TAB>a1`, `architect<TAB>a2`) passes every rule (shape, N, distinct roles, distinct ids, roles in config list, ids unique across manifests). Also the transcript, when present, is only checked to exist, not to match the role or unit. A real agent id from an unrelated dispatch satisfies it. Accepted limit is stated (F9) but the checker should at least fail (not skip) when the session directory is present and an id has no file, and the recovered-form lookup must search all session directories of the project slug, since Stage 4 rounds may span sessions.

### W5. Producer manifest ambiguity blocks writing the AC-4.4 cross-check
ADR-lmr-005 item 5 says a unit's producer dispatches "are not validators and are not listed". Item 6 says producer ids appear "under a developer role in the S5 producer manifest". Both cannot hold. The PRD AC-4.4 script itself only needs disjoint `Dispatch-Id` trailer sets (which does catch a shared producer/validator id), but the manifest cross-check that item 6 adds cannot be written until the ambiguity is resolved. Plan must pick one.

### W6. Live-paid steps: owner and aggregate budget not pinned
- S5a fixture capture (about $0.04) is authored by the validator dispatch per PRD FR-5.10, but no `--max-budget-usd` is required for that ad hoc capture. Only the runner path has the cap.
- S5b (about $15, five samples at a $3 hard cap each) is placed in Stage 7 (P1, unresolved "needs Plan confirmation"). No role is named as the executor. UAT roles are qa, devops, po, tech-writer. The S5b manifest lists validators, not the executor.
- $3 x 5 = $15 equals the NFR-2 envelope. `--init-baseline` aborts on any non-zero exit (loop-3 F9) and there is no cumulative ceiling or retry limit, so one abort plus a re-run overspends with no rule to stop it. The layer-2 post-check is per sample.
- G5 closing ACs (5.4, 5.5, 5.5c, 5.6) move to UAT under this design; Stage 6 DoD cannot pass them. Plan must record that, or Stage 6 stalls.
S7b is clean (devops, different dispatch, no live `claude`). Plan fix: name the S5b executor role, give a total spend ceiling and max attempts, require `--max-budget-usd` on the fixture capture, and state the human consent point for paid spend.

### W7. Per-unit manifests do not enforce the stage cap the shipped prose states
The S2 block rewrite says `dod_validators.<stage>` is "the cap: at most that many subagents per stage". ADR-lmr-005 bounds each manifest to `N <=` list length, but per-unit and per-round manifests multiply. Over-spawning across units in one stage (for example S5b + S7 + S7b in `07-uat`, each up to 4) is not detected. Reconcile the wording ("per DoD checkpoint") or add a per-stage total.

### W8. Smaller items
- Guard false positives ("on 6.8 kernels", "with 4.7 V rail", "the 4.7 uF cap", `claude-plugins-v2`) are documented as accepted, but no fixture pins them as known-hit, so a later pattern change flips them silently, and AC-1.2a has no must-pass string for hardware-team style prose. Add them as `known-fp` fixtures. S1 whole-tree run (P5) is the only check; the tree has none today so no rework is expected.
- AC-1.6b tests only the `pin` category with the marker text. A marker exemption added to the `prose` or `stamp` rule would not be caught. Add one prose-shaped and one stamp-shaped bypass case.
- AC-4.4 `validator_start` and `validator_end` come from `s5-separation.txt`, written by the orchestrator. Add a derived check: `validator_start` equals the parent of the first validator commit, and `validator_end` equals the last validator commit.
- Loop-3 residuals R-1 (uniform `latest` stamp on 22 unreviewed files) and R-2 (non-`.md` version words pass Rule B) stay open and are owned by PO. Not verifiable by any AC. Confirmed acceptable as recorded.

## Traceability check (PRD AC to design path)

| Area | Verifiable path in design | Status |
|---|---|---|
| Guard AC-1.1..1.6b, 1b, 1.2c | ADR-lmr-002 D1-D8, fixtures both engines, hook temp-repo test (P4 to Plan) | OK, see W1, W2, W8 |
| Stamps, prose, budgets AC-2.x, 3.x, 6 | ADR-lmr-003 line math with scratch simulation, ledgers, stagger | OK, R-1 stays |
| Smoke AC-5.x, parser fix for `unknown` | ADR-lmr-004 sections 1-5, real-shape fixture, capture failure classes | OK except B1 and W3 |
| Red-first, P0 stub AST check | ADR-lmr-004 section 6 | BLOCKED by B1 |
| AC-DISP dispatch manifests | ADR-lmr-005 items 1-6 | Checkable, see W4, W5, W7 |
| Ship gate steps 0-9, S7b | ADR-lmr-005 item 8, exit-status forms, out-of-tree log | OK; residual RR-1 detect-only, accepted with owner |
| BINDING-4.5 separation | order plus trailers plus manifest ids | Enforceable as order and fusion control; authorship self-declared (accepted limit F9) |
| S5a/S5b/S7b split | architecture.md section 5 | Ownership and budget gaps, W6 |

## Verdict

NOT_DONE: 1 blocking (B1). After the small fix in ADR-lmr-004 section 2/6, the design is DONE for Stage 4 with W1-W8 carried to Plan as AC text.
