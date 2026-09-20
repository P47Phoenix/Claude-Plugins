---
run: run-2026-05-28-o48m
unit: S1 (Guard) DoD QA, fresh reviewer, read-only on repo
note: skill delivery-team:qa unknown in this session; role applied from brief.
head: b082a0c
---

S1_DOD_QA: DONE

Blocking issues: none (0).

## D1 closed (raw)

Default scope, same output from every cwd:
```
cwd repo root      files-scanned 486 / guard-scope hits 85 files 30  rc=1
cwd scripts/       files-scanned 486 / guard-scope hits 85 files 30  rc=1
cwd delivery-team/ files-scanned 486 / guard-scope hits 85 files 30  rc=1
cwd /tmp           check_model_pins: not in a git repository          rc=2
cwd symlink -> repo/scripts   486 / 85 / 30  rc=1
GIT_DIR+GIT_WORK_TREE set, cwd /tmp   486 / 85 / 30  rc=1
```
Other required:
```
--check-fixtures   fixture failures 0 []   rc=0
--canary           canary ok               rc=0
real --list        rc=1, hits 85 files 30, files-scanned 486
base-sha.txt       f4fea7db...(40 hex), 485   -> 486 >= floor B 485
mutation_and_floor.py (root)  MUTATION OK 10/10 killed; K=486 live=486 B=485; FLOOR OK
--paths a b        files-scanned 2, hits 0, rc 0
--paths (none)     files-scanned 0, hits 0, rc 0
--paths nope.md    files-scanned 0, hits 0, rc 0 (documented skip)
```
Temp repo (spaces, subdir, newline name, unpacked nested dirs):
- `sub dir/deep/sp ace.md` and `nl\x0aname.md` both hit, from root and from `sub dir/deep` (identical 3 hits, files-scanned 4). Newline is escaped, one line per hit (N1 from QA report closed).
- `--paths "sub dir/deep/sp ace.md"` from the subdir: hit, rc 1 (toplevel-relative). Absolute path: hit.
- Real nested worktree `.claude/worktrees/w2` (git worktree add): root scan lists 0 lines for w2 (skipped). Run from inside w2: scans w2 as its own repo (pin2.md hit), correct.
- pre-push last line WITHOUT trailing newline, tracked pin, STRICT: guard ran (`hits 3`), `guard rc=1`, rc 1. With newline: same. Devops N1 closed.
- pre-commit STRICT, staged pin, run from `sub dir`: `MODEL PIN VIOLATION - commit blocked`, rc 1.
- Hook temp-repo `core.hooksPath` set via `git -c` per case; repo core.hooksPath not touched.

## Fixture independence

`scripts/model_pin_fixtures.json` history: one commit, 3337deb ("test(guard) S1: independent fixtures and QA report"), not in producer commit 6560e64 (0 fixture lines in its stat), untouched by producer fix b082a0c. Every fixture string has a `provenance` entry (qa-probe, challenger, prd origins). Dispatch manifest `dispatch-manifest-S1.txt` (untracked) lists qa a099373e856d0d420 distinct from developer a7f0e958e47ad9222. Git author is the same human on all commits, so authorship rests on commit order, message and manifest ids, not git identity. Fixtures pass with 0 failures on the fixed script and mutation kills 10/10, so they were not tuned to a broken script.

## Warnings (non-blocking)

- W1 GIT_DIR without GIT_WORK_TREE fails open. `GIT_DIR=<repo .git>` (or pointing at another repo) with cwd `scripts/` gives `files-scanned 5, hits 0, rc 0`, because `git rev-parse --show-toplevel` then returns cwd. Needs a hand-set env var, hooks and CI do not do it (hook run from a subdir blocked correctly). Cheap hardening: drop `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` from the env passed to git, or add the K >= B floor to the ship gate (already planned, PA-7).
- W2 `--paths` relative args resolve against the toplevel, not cwd. From a subdir `--paths "sp ace.md"` gives `files-scanned 0, rc 0` (silent false clean, same class as QA N2). Documented in docstring. Callers pass toplevel-relative or absolute paths (hooks do).
- W3 `mutation_and_floor.py` is root-cwd only: from `scripts/` it dies with FileNotFoundError `scripts/scripts/check_model_pins.py` (loud failure, not false pass). S7 must run it from repo root.
- W4 Hooks inert: `core.hooksPath` is not `.githooks` (PA-9, human/S7 decides). Ship gate must call scripts directly.
- W5 Guard is RED on the real tree (85 hits) by design until S2 to S4 reword. Untracked `dispatch-manifest-S1.txt` and `pre-s2-hashes.txt` are outside this task.
- W6 Contract regex gaps (QA N3) remain, PRD-verbatim, owner architect/PO.

Files: /var/home/meconnelly/Documents/GitHub/Claude-Plugins/.claude/worktrees/backlog-108-o48m/.delivery/artifacts/06-development/S1-dod-qa.md
