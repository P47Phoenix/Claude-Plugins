---
run: run-2026-05-28-o48m
story: S1 (Guard)
role: qa validator (independent of producer of commit 6560e64)
note: delivery-team:qa skill not known in this session; role applied from the brief.
---

# S1 QA report

S1_QA: FAIL

Reason: 1 blocking defect (D1, fail-open from a subdirectory). Everything else passes. D1 is a 2-line fix; re-verify command at the end.

Files authored: `scripts/model_pin_fixtures.json`, `.delivery/artifacts/06-development/S1-guard-tests/mutation_and_floor.py`, this report. Guard script, hooks, workflows untouched.

## 1. Fixtures (AC-1.2a)

Counts: rule_a_must_hit 36 (>=25), rule_a_must_pass 15 (>=10), rule_b_must_hit 31 (>=15), rule_b_must_pass 25 (>=12), known_fp 9. 3+ `synthetic-future` must-hits (claude-newfamily-7, claude-opus-9, claude-fable-12, Opus 12, Fable-6). Provenance covers every string, origins from the PRD enum. Authored from PRD FR-1.2 / ADR rules and real-world variants, not from script source. PRD REQ strings all present.

known_fp (expect = current contract behaviour):
- pass: `6.8 kernels`, `4.7 V`, `4.7 uF`, `Sonnet 4 stories`
- hit (documented over-match, reword): `Opus 3 validators`, `claude-plugins-v2`, `built with 4.7 V rails`, `runs on 6.8 kernels`, `claude-code-2 style plugin ids`

Marker tests (AC-1.6b, PA-4): pin, stamp and prose lines carrying `model-pin-ok` are must-hit.

Raw:
```
$ python3 scripts/check_model_pins.py --check-fixtures
fixture failures 0 []
$ (PRD AC-1.2a dual-engine snippet, python re + grep -E + sed, extracted verbatim from prd.md)
fixture failures 0 []
```
First run had 1 failure: `the 4.7 V supply` in rule_b_must_pass. Fixture mistake (BARE_RE hits `the 4.7`, COUNT_RE has no V unit). Removed; `built with 4.7 V rails` kept as known_fp hit.

Fixture sensitivity (negative self-test, PA-12 idea), `S1-guard-tests/mutation_and_floor.py`:
```
mutation PIN never              fixture failures 27
mutation PIN always             fixture failures 46
mutation STAMP never            fixture failures 9
mutation PROSE never            fixture failures 26
mutation PROSE always           fixture failures 25
mutation BARE never             fixture failures 5
mutation COUNT never            fixture failures 8
mutation PIN drops -latest      fixture failures 2
mutation PIN case-sensitive     fixture failures 1
mutation PROSE drops Fable      fixture failures 2
MUTATION OK 10/10 killed
K=486 live=486 B=485
FLOOR OK
```

## 2. Real tree (PA-8, PA-3)

```
$ python3 scripts/check_model_pins.py --list      -> rc=1
files-scanned 486
guard-scope hits 85 files 30
```
`grep -c -E '^(pin|stamp|prose) '` on the listing = 85 = summary hits (PA-3 ok). Last line is the summary.

85/30 vs PRD 91/31: `git show 6560e64^:.github/workflows/stale-model-id-guard.yml` had 6 pin lines (23,24,25,30,31,39: the allowlist literals). Guard on that old file: `hits 6 files 1`. 91-6=85, 31-1=30. Exact. The producer rewrote the workflow, removing them.

PA-7 floor: K=486, live=486, B=485 (base-sha.txt line 1 is 40-hex, line 2 is 485, 2 lines). K==live and K>=B. But see O3: nothing in script or hooks owns this check; I shipped it in `mutation_and_floor.py`.

## 3. Independent tests

Canary: `canary ok`, rc 0.
`--help`: rc 0.
`--paths scripts/check_model_pins.py README.md`: `files-scanned 2`, `hits 0 files 0`, rc 0.
`--paths` (none), `--paths nonexist.md .delivery/x.md CHANGELOG.md a.json`: `files-scanned 0` / `hits 0 files 0`, rc 0 (matches PA-7).
`--paths <real pin file> --strict`: 6 listed hits, rc 1 (flag no effect on rc).

Exit 2 cases (temp dirs under $CLAUDE_JOB_DIR/tmp):
```
default scope outside repo         -> "git ls-files failed ... status 128"  rc=2
--paths non-UTF8 file              -> "unreadable in-scope file bad.md: 'utf-8' codec ..." rc=2
--paths chmod 000 file (uid 1000)  -> "unreadable in-scope file unread.md: Permission denied" rc=2
--paths missing file               -> files-scanned 0, hits 0, rc=0   (skipped by design, see N2)
--paths outside-repo pin file      -> pin pin.md:1, rc=1 (scanned, per FR-1.2)
repo + non-UTF8 in default scope   -> rc=2
empty repo default scope           -> "default scope empty" + files-scanned 0 + hits 0 files 0, rc=2
repo + unreadable in default scope -> rc=2
```
`-z` (temp repo): filenames `café-ünï.md`, `sp ace.md`, name containing a newline: all scanned and hit (4 hits incl. target.md). Symlink `link.md -> target.md` skipped (files-scanned 5, target counted once). Nested real worktree `.claude/worktrees/w1` containing a pin: 0 hits mention it (skipped as non-file).

Hooks (temp repo, `git -c core.hooksPath=<abs>/.githooks`, guard + budgets copied in):
```
pre-commit staged pin, advisory        -> advisory msg, commit rc=0
pre-commit staged pin, STRICT=1        -> "MODEL PIN VIOLATION - commit blocked", rc=1
pre-commit zero staged (allow-empty)   -> rc=0 (no abort under set -euo pipefail)
pre-commit json-only w/ pin text STRICT-> files-scanned 0, rc=0
pre-commit newline+space filename pin STRICT -> hit, blocked rc=1
pre-push non-main STRICT w/ pin        -> rc=0
pre-push main STRICT tracked pin       -> guard rc=1, push rejected rc=1
pre-push main advisory tracked pin     -> advisory, push rc=0
pre-push main STRICT clean             -> hits 0 + budgets pass, rc=0
pre-push nested worktree (untracked, has pin) clean STRICT -> rc=0 (pathspec skips it)
pre-push nested worktree + stray untracked file STRICT -> "working tree not clean", rejected rc=1
pre-push delete main STRICT            -> rc=0
pre-push empty stdin                   -> rc=0
pre-push sha mismatch STRICT           -> rc=1
pre-push guard script missing (rc 2) STRICT -> rc=1; advisory -> rc=0
```
PA-7 7 stub cases all covered above. The first hooks run was polluted by my temp repo (lint_known_debt drift, `__pycache__`); re-run with clean setup gave the results above.

CI checks: `grep` for a `claude` CLI invocation in `.github/workflows/`: no matches. YAML parse of all workflows: `${{ github.event` inside a `run:` in 0 files except `workflow-injection-lint.yml`, where it is the lint's own echo text (pre-existing, not a use). Guard workflow: `on` push[main] + pull_request + workflow_dispatch, no `paths:`, `permissions: {contents: read}`, checkout `persist-credentials: false`. Budget workflow: `push: branches [main]` + pull_request paths, `contents: read`, `persist-credentials: false`, `github.event` only in `env:`. `python3 scripts/check_skill_budgets.py` rc 0 (17 files).

## 4. Adversarial (27 of 44 probes differ from "should hit"; most are contract limits)

Held (hit): double space `Opus  4.7`; md link text `[Opus 4.7](..)`, `[claude-opus-4-7](..)`; inline code fence; old marker comment; `# noqa` marker; `<!-- markdownlint-disable --> Opus 4.7`; `Opus4.7`, `Opus-4.7`, `Opus 4,7`; upper-case pin; provider-prefix path; vertex `@date`.

Missed (should hit in my judgement):
- unicode digits `Opus ４.７` (fullwidth), Arabic-indic
- tab or nbsp or zero-width space between family and version
- `opus_4_7`, `Opus_4_7`, `claude_opus_4_7`, `claude.opus.4.7`, `claude opus 4-7` (in .md, lower `opus 4-7` misses since PROSE lower needs `-4` or `4` glued or `x.y`)
- mixed case `OpUs 4.7`
- `**Opus** 4.7`, `` `opus` 4.7 ``, `Opus (4.7)`, `[Opus](url) 4.7`
- `model: sonnet-4-6` in .py/.yml/.yaml/.txt/.sh (Rule B is .md only, by PRD)
- `model_awareness: 'sonnet-4-6'` and `pattern_library_version: '4-7-1'` (single-quoted YAML; STAMP_RE only allows `"`)
- `model_awareness : opus-4-7`, tab after colon, `model-awareness:` key
- `audited-4-7` bare stamp; non-breaking hyphens
Accepted misses: spelled out "four point seven", literal `\n` split.
Known FP: `claude-plugins-v2` hits (PIN_RE digit). Documented.

All patterns equal the PRD FR-1.2 values verbatim, so these are contract gaps, not producer bugs. See N3.

## 5. Producer open questions

- `--strict` flag: accepted, no effect on rc, consumed only by hooks via env var. Acceptable (not a defect). Recommend the docstring keep saying so; do not add callers that rely on it.
- `known_fp expect:"pass"` extension: acceptable and needed (my fixtures use it). Plain strings default to hit. Recommend the PRD/ADR text note it. Not a defect.
- Floor check ownership (PA-7): not a guard defect. Guard has no floor logic and hooks do not either. Owner must be the validator/ship gate. I supply `S1-guard-tests/mutation_and_floor.py` (K==live, K>=B, base-sha format). Recommend S7 Block A step runs it, from repo root. Note it depends on D1 being fixed to be meaningful from other cwds.

## 6. Defects

### D1 (BLOCKING): default scope fails open from a subdirectory
`git ls-files` prints paths relative to cwd and only under cwd. Running the guard from a subdir scans a subset and can print clean.
Repro:
```
cd scripts && python3 check_model_pins.py; echo rc=$?
files-scanned 5
guard-scope hits 0 files 0
rc=0
cd delivery-team && python3 ../scripts/check_model_pins.py   -> files-scanned 316, hits 40 (tree has 85)
```
Expected: fail closed (rc 2) or scan the whole repo. Fix: in `files()` run git with `-C <toplevel>` (`git rev-parse --show-toplevel`) and chdir there, or use `git ls-files --full-name` plus a toplevel-relative open. Hooks and workflow run from root so CI is safe; ship gate and the S7 canonical command are cwd-dependent. Re-verify: the two commands above must give rc 1 / 85 hits (or rc 2).

### Non-blocking
- N1: `--list` prints a filename containing a newline raw (`pin new` / `line.md:1` on two lines). A crafted name `pin x.md` could fake a hit line for prefix-counting callers (PA-3 awk). Low. Suggest escaping (`repr`-style) in output.
- N2: `--paths` silently skips a nonexistent path (rc 0). Intended for deleted staged files; a typo in a manual run gives a false clean. Acceptable, documented. Hooks pass real paths.
- N3: contract regex gaps listed in section 4 (single-quoted stamps, underscore forms, tab/nbsp, bold/backtick-split family + version, Rule B only .md). Owner: architect/PO if desired; would need a PRD contract change (constants are PRD-verbatim). Cheap wins if reopened: `["']?` in STAMP_RE (avoid a literal single quote via `[^a-z0-9 ]?`), `[ _-]` in PROSE/PIN separators.
- N4: `core.hooksPath` is currently `/var/home/.../Claude-Plugins/.git/hooks`, not `.githooks` (PA-9). Hooks are inert in this checkout until the orchestrator/devops installs it (`git config --local core.hooksPath .githooks`; shared-config note per PA-9). I did not touch git config.
- N5: empty default scope prints `guard-scope hits 0 files 0` then rc 2. Callers must judge on rc (PA-1 already says so).
- N6: pre-push treats any nonzero guard rc as failure but does not check the summary regex or K>0 (PA-1 caller rules). Guard already fails closed on K==0, so acceptable.

Re-verify after fix: rerun `--check-fixtures`, `mutation_and_floor.py`, and the D1 repro.
