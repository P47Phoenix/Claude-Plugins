# Developer DoD Review: BACKLOG-108 PRD (Revision 4), Stage 2 Refine

Validator: developer (implementability and command correctness). Run from the worktree root, bash and python3 stdlib only, no network, no paid `claude` run. Scratch files (walk.py copy, canonical script copy, simulated guard and fixtures) lived under `/tmp/dev-dod/`, not in the repo. No repo file modified other than this review.

Note on tool loss: the Bash tool stopped responding after the last batch (every call returned exit 1 with no output). All commands listed below as executed ran before that point. Items marked NOT RUN were not executed for that reason or because they need a later-stage artifact.

## 1. Command-execution table

"Today" = unedited tree. TARGET ACs are judged for well-formedness plus any TODAY value the PRD states.

| # | Command / AC | Exit | Output | Matches PRD |
|---|--------------|------|--------|-------------|
| 1 | Canonical counting command (section 1, extracted verbatim, walk.py copy) | 0 | `guard-scope hits 91 files 31`; `pin 20 stamp 52 prose 19`; 9 listing lines identical to the PRD listing (all line numbers equal) | YES, exact |
| 2 | Stamp census (section 1) | 0 | `skill 34`; `26 25 {'model_awareness: opus-4-7-frontmatter-only': 19, 'model_awareness: opus-4-7': 7}` | YES, exact |
| 3 | `grep -rh "^pattern_library_version:" --include=SKILL.md . \| sort \| uniq -c` | 0 | `26 pattern_library_version: 4-7-1` | YES |
| 4 | Tier-alias census `grep -rnE "^(model\|phase_1_detector_model):" --include=SKILL.md . \| wc -l` | 0 | 9 | YES |
| 5 | AC-4.6 vocabulary script | 0 | `9 ['haiku', 'opus', 'sonnet'] violations 0` | YES, exact |
| 6 | AC-1.1 `grep -cEi PIN_RE stale-model-id-guard.yml` | 0 | 6 | YES (today 6) |
| 7 | AC-1.1b (triggers), against today's file | 1 | AssertionError `push-to-main trigger missing` | YES (stated today failure) |
| 8 | AC-1.1b against a compliant sample workflow (push branches [main], pull_request, workflow_dispatch, script call) | 0 | `OK` | YES |
| 9 | AC-1.2a (fixtures, both engines) against a simulated `scripts/check_model_pins.py` (four constants copied verbatim) plus a 25/5/16/6 fixture file I authored from the PRD's named strings | 0 | `fixture failures 0 []` | YES (python `re` and `grep -E` agree on every string, including `run haiku 3 times`, `Replace C12 with 4.7uF or greater`, `Step 4.5: Delegation Self-Check`, `Section 5.5`, `Opus  5`, `regression mode on 4.7.`; portability asserts pass) |
| 10 | AC-1.2b `python3 scripts/check_model_pins.py --help` | 2 | No such file (script absent today) | YES (PRD says script does not exist today) |
| 11 | AC-1.2b `grep -c check_model_pins.py` workflow | 0 | 0 | consistent (target: >=1) |
| 12 | AC-1.2c `python3 scripts/check_model_pins.py` | 2 | file absent; canonical command gives 91/31 as PRD states | YES |
| 13 | AC-1.3 (`claude -p/--print/--model` in workflows; `smoke-*` workflows) | 0 | `0` and `0` | YES |
| 14 | AC-1.5 `grep -c check_model_pins.py .githooks/pre-commit` | 0 | 0 | YES (today 0) |
| 15 | AC-1.6 marker scan | 0 | `0 []` | passes today, target met |
| 16 | AC-2.1 source-line-removal script (`git show main:<file>`) | 0 | `25 source lines still present` | YES, exact |
| 17 | AC-2.2 four greps on `prompt-engineer/SKILL.md` | 0 | `MODEL_ID = os.environ`: 0; PIN_RE: 1; `canonical <YYYY`: 1; `Versioned Model Reference`: 1 | TARGET, well-formed (PRD states no today value) |
| 18 | AC-2.3 hedge scan | 0 | `0` | YES |
| 19 | AC-2.5 content gate | 0 | `FAIL` (0 added lines) | TARGET, well-formed; no today value stated |
| 20 | AC-2.6 `grep -c "^model: sonnet"` delivery-flow | 0 | 1 | YES |
| 21 | AC-3.1 ledger check | not run | ledger file does not exist; script is well-formed by reading (header, want/got, git diff --quiet) | PRD states FileNotFoundError today; not executed |
| 22 | AC-3.1b | not run | needs `scripts/check_model_pins.py` (absent). Equivalent count verified by hand from run 1: 16 prose lines in two SKILL.md (4 + 12) plus 1 pin (`prompt-engineer/SKILL.md:368`) plus 52 stamps | consistent with PRD text |
| 23 | AC-3.2 (stamp census after S3), first line | 0 | today `34 26 25 {...opus-4-7...}`; `26 {'pattern_library_version: 4-7-1': 26}` | YES (PRD states today shape) |
| 24 | AC-3.3a frontmatter date check | 0 | `36 violations` (25 `last_audited` + 11 `fitness_review_due`) | YES, exact |
| 25 | AC-3.3b `grep -c model_awareness: prompt-engineer/SKILL.md` | 0 | 2 | YES (target 2, already 2 lines) |
| 26 | AC-6 `python3 scripts/check_skill_budgets.py` | 0 | `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` | YES, exact |
| 27 | AC-4.1 (`py_compile`; `grep -c opus-4-7`; ast script) | 0 / 0 / n/a | `py_compile` exit 0; `opus-4-7` count 4 today; ast check finds 0 `MODEL_TIER_ALIAS` definitions and 3 `"model": "claude-` literals | TARGET, well-formed; ast logic reads correctly (module-level Assign, literal_eval, 3 usages) |
| 28 | AC-4.2 conftest count | 0 | `False 4` | TARGET (4 pins today; matches 105, 117, 129, 151) |
| 29 | AC-4.2 `pytest test_meta.py -q` | 0 | `3 passed in 0.03s` | YES |
| 30 | AC-4.3 greps | 0 | telemetry-schema 1, smoke-test-architecture 2 | YES (today "2 and 1") |
| 31 | AC-4.5 `grep -rlE "import anthropic\|from anthropic\|api.anthropic.com" --include=*.py . \| grep -v worktrees \| wc -l` | 0 | 0 | YES |
| 32 | AC-4.5b two greps | 0 | 1 and 0 | YES (today 1; target 0 and >=1) |
| 33 | AC-5.3 `run_smoke.py --help \| grep -cE -- "--(model\|effort)"` | 0 | 0 | TARGET; runs cleanly today |
| 34 | AC-5.5 / AC-5.10 | not run | baseline JSON has none of the new keys (`model_resolved` etc.), `n_samples` 1, `partial-1-of-5`, `cost_usd.mean` 0.0; fixtures dir has only `sample-workspace`. Snippets read as well-formed (AC-5.10 ran clean per PRD on a scratch copy; I have no real capture to test against) | consistent with PRD |
| 35 | AC-5.9 `pytest -k real_shape` | not run | test does not exist today (pytest would exit 5 on an empty selection) | expected |
| 36 | Parser claim check by reading `lib/metrics.py::parse_stream` | n/a | reads only top-level `usage` and `model`, buckets `event.get("model") or "unknown"`, uses `usage.cost_usd` | CONFIRMS PRD F5 analysis |
| 37 | AC-6.1 `sha256sum ... \| diff - governance/cache-prefix-hash.txt && echo MATCH` | 0 | `MATCH` | YES |
| 38 | AC-6.2 ADR ls grep | 0 | 0 | TARGET (Stage 4) |
| 39 | AC-7.1 / AC-7.2 | 0 | both 0 | TARGET (Stage 7) |
| 40 | AC-7.5 renamed-file `test` chain | 0 | `OK` | YES |
| 41 | NFR-8 `git diff main -- .github \| grep -c "pip install"` | not run (tool lost) | n/a | not verified |
| 42 | AC-DISP | not run | PRD gives no command, only "python asserts" | see finding 1 |
| 43 | `validate_constraints.py` | not run | no such file located in the repo tree (name-only `find`, result inconclusive when the tool failed); PRD does not reference it | see finding 6 |
| 44 | Canonical command wall clock | 0 | about 1.2 s real (`time`) | NFR-13 (<=10 s) fine; the PRD's "0.4 s" claim is not reproduced on this host, immaterial |

## 2. Gate results (Developer role: implementability and command correctness)

| Gate | Result | Severity | Notes |
|------|--------|----------|-------|
| Every TODAY value the PRD states reproduces (91/31, 20/52/19, census 26/25/19/7, 36 violations, 25 lines, 9 aliases, AC-6 pass, MATCH) | PASS | n/a | All exact |
| Regexes run in Python `re` AND `grep -E` against the PRD fixtures | PASS | n/a | 0 failures both engines; no POSIX class, lookahead, backreference, single quote in any of the four constants |
| Commands parse and are runnable from repo root with stdlib only | PASS with warnings | warning | see findings 2 to 5 |
| Every closing AC has an executable command | FAIL | warning (recommend fix before Stage 6) | AC-DISP has none (finding 1) |
| TARGET ACs well-formed | PASS | n/a | none crash for a reason other than the stated absent artifact |
| Inter-story ordering of commands is runnable (S1 script exists before S2/S3 ACs that import it) | PASS | n/a | AC-2.1 and AC-3.1b depend on S1 order, which the PRD fixes |
| Tools not installed | PASS | n/a | no `yq`, network or `claude` needed |

No blocking criterion fails.

## 3. Findings

1. AC-DISP (section FR-7.4, gate G8) is not runnable as written. It says "python asserts N == number of dispatch lines and all roles are distinct; MUST print `0 violations`" but supplies no script. Every other closing AC ships a snippet. Required fix: add a python-stdlib snippet that globs `.delivery/artifacts/*/dispatch-manifest.txt`, parses `expected_validators: N` on line 1 and `<role><TAB><agent-id>` after it, and prints `<n> violations`. Also state what to do for the stages that have no manifest yet (the PRD says "for every stage directory with a manifest", which passes vacuously). Non-blocking warning; should be fixed before Stage 6 so G8 is verifiable.
2. Shared `/tmp/walk.py` is a fragile dependency. Many ACs `exec(open('/tmp/walk.py').read())`. A stale, identical copy from 2026-09-19 already existed in `/tmp`, so a second run or parallel validator can overwrite it and a fresh machine or Stage 6 shell will not have it unless the section 1 heredoc is run first. Recommended fix: ship `walk.py` logic inside `scripts/check_model_pins.py` (import it) or state in section 3 that each AC session must first run the section 1 `cat > /tmp/walk.py` block. Warning.
3. AC-1.1b `push`-to-`main` check is loose. `re.search(r'branches:\s*\[\s*main\s*\]|^\s+-\s*main\s*$', ...)` is not tied to the `push:` block, and a quoted list item (`- 'main'`) or `branches: [main, 'release/**']` would fail or pass wrongly. Required fix: parse the `push:` block (slice text from `^  push:` to the next `^  \w+:`), and accept optional quotes. Warning; the current snippet did print `OK` on a compliant sample.
4. AC-4.5 uses an unquoted `--include=*.py`. It works today because the repo root has no `*.py` file, but an unquoted glob is expanded by the shell if one is added. Also `grep -r .` walks `.claude/worktrees` (nested worktrees) and `.delivery` before `grep -v worktrees` filters, which is slow and counts `.py` files under `.delivery`. Fix: quote the glob (`--include='*.py'` is a single-quote in the AC, acceptable here since the no-single-quote rule applies to the guard constants only) or use `--include="*.py" --exclude-dir=worktrees --exclude-dir=.delivery`. Warning.
5. AC-4.2 gives two commands in one fence and the second carries a trailing comment on the same line (`echo "exit=$?"   # MUST print exit=0`). It runs fine; note only that `re.findall` with a capture group in `pins` counts matches correctly but the group content is what is returned, so the guard-style expression should use `re.search` or a non-capturing group for clarity. Info.
6. Section of the task list names `validate_constraints.py`; the PRD does not reference it and I could not locate the script in the repo tree. If `constraints.yml` is meant to be validated, name the command in the PRD or drop it from the DoD list. Info (I could not read `constraints.yml` after the Bash tool failed; not reviewed by this validator).
7. NFR-13 states the canonical command ran in 0.4 s; here it took about 1.2 s. The 10 s target holds. Info.
8. Fixtures and constants are otherwise sound. Each must-hit and must-pass string named in the PRD behaves as stated in both engines using the verbatim constants. One accepted-loophole detail worth keeping in the fixture file: `pattern_library_version: rev-1` passes and `rev-1.2` would hit (dotted revision). Info.

## 4. Verdict

PASS (with warnings). All stated TODAY values reproduce exactly; all regexes are portable and correct in both engines; every TARGET AC is well-formed. No blocking criterion fails. Fix findings 1 to 4 before Stage 6 so the closing ACs (especially G8 AC-DISP) are executable, and confirm the status of `validate_constraints.py` (finding 6).
