# Developer DoD Review — BACKLOG-108 PRD Revision 5 (Stage 2, round 2)

Role: Developer validator. Gate: implementability and command correctness. All fenced blocks (24) were extracted verbatim from the PRD with a script, dedented, and executed from the worktree root (bash / python3 stdlib, no network, no `claude` runs). Inline single-line commands were executed separately.

## 1. Command-execution table

| # | Command / AC | Exit | Output (today) | Matches PRD |
|---|---|---|---|---|
| 1 | Canonical count (sec 1) | 0 | `guard-scope hits 91 files 31`, `pin 20 stamp 52 prose 19`, 9 listing lines identical to PRD | YES, exact |
| 2 | Stamp census (sec 1) | 0 | `skill 34`; `26 25 {...frontmatter-only: 19, opus-4-7: 7}` | YES |
| 2b | pattern_library_version census grep | 0 | `26 pattern_library_version: 4-7-1` | YES |
| 3 | Tier-alias census grep | 0 | 9 lines | YES |
| 4 | AC-1.1b (triggers, self-tests) | 1 | self-tests pass; fails at `AssertionError: push-to-main, pull_request and workflow_dispatch triggers required` | YES (PRD says fails on today's file) |
| 5 | AC-1.1 grep | 0 | 6 | YES |
| 6 | AC-1.2a as written, with sim script (5 constants copied from PRD lines 32-36) + 29/11/20/15 fixtures incl. all REQ strings, 4 synthetic-future | 0 | `fixture failures 0 []` (python `re` AND `grep -E`) | YES; REQ strings all behave |
| 6b | AC-1.2a on today's tree (no script) | 1 | FileNotFoundError scripts/check_model_pins.py | expected (S1 artifact) |
| 7 | AC-1.2b | 0 / 2 | grep 0; `--help` exit=2 (no script) | expected, target |
| 8 | AC-1.2c | n/a | script absent; canonical prints 91/31 | matches PRD statement |
| 9 | AC-1.3 | rc 1 (grep -c) | `0` and `0` | YES |
| 10 | AC-1.5 | - | `0` and `0` | YES ("today: 0 and 0") |
| 11 | AC-1.6a | 0 | 0 | YES |
| 12 | AC-1.6b | 1 | IndexError on empty stdout (script absent) | well-formed; needs S1 script; see finding 3 |
| 13 | AC-2.1 | 0 | `25 source lines still present` | YES |
| 14 | AC-2.2 greps | - | 0, 1, 1, 1 | plausible today (target: 1,0,0,0) |
| 15 | AC-2.3 | 0 | `0` | YES |
| 16 | AC-2.3b (both commands) | 0 / 1 | `0`, `0` | YES |
| 17 | AC-2.5 | 0 | `FAIL` | YES |
| 18 | AC-2.6 | 0 | 1 | YES |
| 19 | AC-3.1 ledger | 1 | FileNotFoundError | YES (stated) |
| 20 | AC-3.1b | 0 | `0 19` (script absent) | see finding 1 |
| 21 | AC-3.2 | 0 | `34 26 25 {...opus-4-7...}` then `26 {...4-7-1: 26}` | YES |
| 22 | AC-3.3a | 0 | `36 violations` | YES |
| 23 | AC-3.3b | 0 | 2 | value fine today (target 2) |
| 24 | AC-6 budgets | 0 | `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` exit=0 | YES |
| 25 | AC-4.1 (ast snippet) | 1 | AssertionError need exactly one MODEL_TIER_ALIAS; py_compile rc 0; `opus-4-7` count 4 | well-formed, target |
| 26 | AC-4.2 snippet | 0 | `False 4` | YES |
| 27 | AC-4.2 pytest test_meta.py | 0 | `3 passed`, exit=0 | YES |
| 28 | AC-4.3 | 0 | 2 and 1 | YES |
| 29 | AC-4.4 | 1 | AssertionError producer and validator must each have commits | YES (stated) |
| 30 | AC-4.5 | 0 | 0 | YES |
| 31 | AC-4.5b | 1 | 1 and 0 | YES (today: 1) |
| 32 | AC-4.6 | 0 | `9 ['haiku', 'opus', 'sonnet'] violations 0` | YES |
| 33 | AC-5.3 | 1 | 0 | fine, target |
| 34 | AC-5.5 | 1 | AssertionError model_resolved non-empty list | well-formed, target |
| 35 | AC-5.5c | 1 | AssertionError baseline needs a samples list of 5 | YES (stated) |
| 36 | AC-5.9b procedure | exit=4 | `ERROR: file or directory not found`, `no tests ran`, exit=4 | NO, see finding 2 (PRD says exit 5) |
| 37 | AC-5.10 | 1 | FileNotFoundError fixture | expected (S5 artifact) |
| 38 | AC-5.2, AC-6.2, AC-7.1, AC-7.2 | - | 0 / no such file / 0 / 0 | expected (future) |
| 39 | AC-6.1 | 0 | `MATCH` | YES |
| 40 | AC-7.5 | 0 | `OK` | YES |
| 41 | AC-DISP | 0 | self-test passes; `4 violations [...]` | YES |
| 42 | NFR-8 `git diff main -- .github \| grep -c "pip install"` | 1 | `0` | YES |
| 43 | validate_constraints.py | 0 | `ok: ... is valid against constraints schema` | YES |
| 44 | FR-4.5 grep for anthropic imports | 0 | no file | YES |

## 2. Checks NOT run

- AC-1.2a against the real `scripts/check_model_pins.py` and `scripts/model_pin_fixtures.json`: S1 artifacts do not exist. Ran against a simulated script (constants copied from the PRD) with my own superset fixture file; the PRD's own 29/12/21/16 fixture file is not in the repo.
- AC-1.6b, AC-1.2c, AC-3.1b with a working script: no `--paths` / `--list` implementation exists (constants only simulated).
- AC-5.4, AC-5.4b, AC-5.5b, AC-5.7, AC-5.9, AC-5.10 with real content: need S5 artifacts, and a paid `claude` capture is out of scope.
- AC-2.3b adversarial artifact, AC-3.1 ledger, FR-1.4, FR-2.4, FR-5.8: inspection or future artifacts.
- AC-1.1b on a compliant workflow (PRD reports OK); only the self-tests plus today's-file failure were observed.
- NFR-13 timing of the guard script (script absent).

## 3. Gate-result table

| Criterion | Result | Class |
|---|---|---|
| Every executable snippet extracts and parses; fences balanced | PASS | - |
| TODAY values reproduce (91/31, 26/25, 25, 36, 9, 0s, MATCH, exit=0) | PASS | - |
| Snippets self-contained (no shared /tmp file) | PASS | - |
| Guard regexes correct in Python `re` and `grep -E` (no POSIX classes, lookaheads, single quotes) | PASS | - |
| Must-hit / must-pass fixtures incl. false-positive classes (Sonnet 4 stories, in 5.0 seconds, ...) | PASS | - |
| AC-5.9b stated today exit code | FAIL | warning |
| AC-3.1b vacuous pass when script fails | FAIL | warning |
| AC-1.6b robustness on script failure | FAIL | warning (minor) |

## 4. Findings

1. **AC-3.1b (section 3, S3) can pass vacuously.** It never checks the script's return code or that stdout is non-empty. With `check_model_pins.py` missing or crashing, stdout is empty, `n` is 0, and the AC prints `0 0` as soon as the `frontmatter-only` markers are gone, which is a false PASS. Today it prints `0 19` with the script absent, not `69 19` as the PRD states (the PRD flags that value as from a simulated script, so the claim is honest). Required fix: add `assert r.returncode in (0, 1) and out.strip().splitlines()[-1].startswith('guard-scope hits')` before counting.
2. **AC-5.9b (S5) states the wrong pytest exit code for today.** The PRD says the empty selection makes pytest exit 5. Executed against `main` plus overlay, pytest exits 4 (`ERROR: file or directory not found: .../test_model_capture.py`), because the file does not exist anywhere. Exit 5 occurs only once the file exists but `-k real_shape` selects nothing. The MUST (`exit=1` unfixed, `exit=0` branch) is still correct, and a wrong-exit 4 is not exit 1, so the AC discriminates. Required fix: change the prose to "exits 4 today (file absent); 5 if the file exists but selects nothing".
3. **AC-1.6b (S1) fails with IndexError rather than a clear message when the script is absent or prints nothing** (`r.stdout.strip().splitlines()[-1]`). Well-formed for its purpose; required fix (optional): guard for empty output so the failure is an assertion, not a traceback.
4. Minor: AC-1.1b regex requires exactly two-space indentation for `push:` and `pull_request:`; a four-space workflow would false-fail. The PRD documents its samples as two-space, so this is a note only. AC-5.9b block mixes `$T` shell and no `set -e`; acceptable.

No blocking defects found in any command. The canonical counting command is self-contained, reproduces exactly, and its scope matches the described guard scope. Guard regexes behave identically in Python `re` and `grep -E`; PRD's REQ-named must-hit and must-pass strings all classify correctly, and the mutation-style requirement (>= 3 synthetic-future) is satisfiable.

## 5. Verdict

PASS with 3 warnings (findings 1 to 3). All executable commands are well-formed and runnable; every TODAY value reproduces; future-artifact ACs are self-contained and well-formed. No blocking failures.
