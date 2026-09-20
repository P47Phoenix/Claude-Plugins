---
run: run-2026-05-28-o48m
unit: S1 (Guard)
role: architect (DoD validator, fresh reviewer)
commits: 6560e64, 3337deb, b870843, b082a0c
---

# S1 DoD: architect conformance

S1_DOD_ARCH: DONE

## D1..D9 conformance

| Decision | Evidence | Verdict |
|---|---|---|
| D1 one definition point, 5 constants, import-safe | check_model_pins.py:74-78 constants; :311 scan only under `__main__`; `--check-fixtures`/`--canary` run OK | OK |
| D2 rule order pin, stamp, prose (COUNT blank first) | :94-104 `classify`; one category per line; hits per line :157-160 | OK |
| D3 scope ls-files cached+others, isfile, 6 exts, no CHANGELOG, no .delivery | :129-148, :80, :107-115; symlink/nested worktree skipped :145 | OK (better: toplevel-based, cwd independent) |
| D4 no exemptions, no marker | no skip logic in classify/scan_file; docstring :5-6; marker fixtures in QA report | OK |
| D5 CLI: no args, `--paths`, `--list`, `--help` rc0, last line `guard-scope hits N files M`, rc1 on hits, sorted | :256-308; sort :171; last line :304 | OK, plus disclosed extras (below) |
| D6 fixtures JSON, 5 keys, provenance, both engines | model_pin_fixtures.json (QA-owned); `--check-fixtures` prints `fixture failures 0 []`; canary ok | OK (known_fp `expect` extension, below) |
| D7 workflow: push main + PR + dispatch, no paths filter, one script call, no ID, no `github.event` in run, no pip, no claude | stale-model-id-guard.yml diff: on push/PR/dispatch, `permissions: contents: read`, `persist-credentials: false`, `python3 scripts/check_model_pins.py --list` | OK |
| D8 pre-commit: staged, NUL-safe, advisory default, strict via env, tolerant of zero staged, placed after budget checks | .githooks/pre-commit diff (+18): `-z`, `xargs -0`, `pin_rc` guard, skip on missing script | OK |
| D8 pre-push: main only, sha==HEAD, clean tree w/ pathspec, guard + budgets, non-main pass, delete pass | .githooks/pre-push:24-43 all conditions present; pathspec :32; zero-sha :26 | DEVIATION: advisory unless MODEL_PIN_STRICT=1 (ADR ref is strict) |
| D9 self-scan, synthetic IDs, canary | docstring uses `claude-opus-fixture`; canary builds pin at runtime :220; `--canary` ok; script scanned within default scope (no self-hit listed) | OK |

Also: skill-line-budget.yml gets push trigger + `persist-credentials: false` (ADR-lmr-005 hygiene): OK.

## Disclosed deviations

1. pre-push advisory unless `MODEL_PIN_STRICT=1`. ADR reference is strict; pre-push only acts on main, so WIP-branch tolerance (the usual reason for advisory) does not apply. Hook is inert today (no hooksPath). The mandatory blocking control is the S7 ship gate steps 0-8, not this hook. Verdict: acceptable ONLY as recorded amendment; WARNING W1. Preferred fix: default strict for pre-push (invert env to `MODEL_PIN_ADVISORY=1`), or S7 gate exports `MODEL_PIN_STRICT=1` and never relies on hook default. Not blocking because ship gate independently blocks and ADR-lmr-005 already calls the hook defence in depth.
2. `--strict` flag inert (rc unchanged). Acceptable: flag documented in docstring :45-46; env is what hooks read. Amend D5 to say so. Minor.
3. `--paths` implies listing. Acceptable: superset of D5 (list line prefix contract kept `pin `/`stamp `/`prose `). Amend D5.
4. `--paths` relative args resolve against toplevel (chdir at :263). Acceptable and correct for hooks (git emits toplevel-relative names) and for the cwd-independence goal. Amend D5. Edge: a user passing cwd-relative path from a subdir gets toplevel resolution; documented in docstring :23-24.
5. known_fp `expect: "pass"` extension (fixtures :208-212, plain str stays hit). Acceptable: backward compatible with D6 five keys; amend D6/AC-1.2a wording (known_fp entries may carry `expect`).
6. core.hooksPath not installed (PA-9). Acceptable at S1 (shared `.git/config` write affects main checkout and all worktrees; needs human/S7 decision). NOT a silent skip: QA N4 and devops review both log "hooks inert". WARNING W2: PA-9 is unmet as written; S7 must install (or state inert) and log `hooksPath=`; record a plan amendment moving PA-9 to S7.

## Scope check

`git diff --stat 6e536bf..HEAD`: 10 files. Guard script, fixtures JSON, pre-commit, pre-push, two workflows, base-sha.txt (all planned S1 paths), plus QA/devops artifacts (S1-qa-report.md, S1-devops-review.md, S1-guard-tests/mutation_and_floor.py). No SKILL.md, no other plugin file touched (`git diff --stat 6e536bf..HEAD -- '*SKILL.md'` empty). Scope respected. Untracked `pre-s2-hashes.txt` is a later-step artifact, not in S1 commits.

## base-sha.txt and PA-7/8 floor

- Content: line 1 `f4fea7db5b39da374ab0d24e529da7a049abb150` (40 hex; equals current `main` tip), line 2 `485` (2 lines). Matches PA-8 format. OK.
- Baseline B=485; live K=486 now (guard file added). Floor semantic (K==live, K>=B) holds: 486 == 486 >= 485. Verified by me: default run prints `files-scanned 486`.
- Gap: script and hooks implement no floor; only QA's `mutation_and_floor.py` does (QA O3). PA-7 words the floor as a checker duty, and plan lists "guard, budgets, hash steps built and dry-run in S1". Acceptable if S7 gate invokes that checker; WARNING W3: ship gate must run the floor check explicitly, else a silently shrinking scope (the fail-closed rc 2 only covers K==0) passes.

## cwd assumption for ship gate

True now. Ran from repo root and from `scripts/`: both `files-scanned 486`, `hits 85 files 30`. From `/tmp` (no repo): `check_model_pins: not in a git repository`, rc 2, fail closed. Ship gate runs in the main checkout, so it holds; the nested-worktree caveat is handled by isfile skip.

## Other observations

- Current tree is red (85 hits, 30 files) by design until S2..S4 sweep; workflow would fail on push of S1 alone (P14: never push S1..S3 alone). Not an S1 defect.
- `--check-fixtures` 0 failures; `--canary` ok (I ran both).
- D3 latent hole (`.githooks/*` and Makefile executable, out of scan) unchanged; PO item P19, not S1.

## Blocking issues

None.

## Warnings

- W1: pre-push default advisory; amend ADR-lmr-002 D8 (or flip default to strict) and make S7 gate export `MODEL_PIN_STRICT=1`.
- W2: PA-9 not done at S1; amend plan to S7 ownership, log `hooksPath=`.
- W3: PA-7 floor lives only in QA script; S7 gate must call it.
- W4: record ADR-lmr-002 amendment for items 2-5 (D5/D6 extras).
