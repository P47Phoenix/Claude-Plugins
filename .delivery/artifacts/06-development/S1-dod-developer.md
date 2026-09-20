run: run-2026-05-28-o48m
unit: S1 (Guard) | role: DoD validator (developer) | commits: 6560e64, b082a0c
skills: delivery-team:developer, plugin-dev:hook-development (acknowledged)

S1_DOD_DEV: DONE

## Blocking issues
None. (count 0)

## Warnings (non-blocking)
W1. `--paths` drops any arg starting with `--` (main(): `named = [a for a in named if not a.startswith("--")]`). A tracked file named `--x.md` is skipped in `--paths` mode (pre-commit path) but caught in default scope. Evidence: `dash-name via --paths` gave rc 0 files-scanned 0; default scope gave `pin --x.md:1`. Fail-open edge, only in advisory hook path, pre-push/CI still catch. Fix later: stop flag filtering after `--paths`, or use `--` separator; hook xargs could pass `--`.
W2. pre-commit scans working-tree file, not staged blob (`--paths` opens path on disk). Partial staging (`git add -p`) can hide or invent a hit. Advisory hook, S7 strict run catches. Note only.
W3. pre-push `while read` loop: child processes inherit loop stdin (ref lines). Python guard does not read stdin, but `check_skill_budgets.py` unknown. Cheap hardening: `</dev/null` on both calls.
W4. shellcheck SC2034 on pre-push line 24 (`remote_sha` unused). Cosmetic; `_` would silence.
W5. Undecodable/non-UTF-8 in-scope file gives rc 2 for whole run (fail closed by design). Correct per contract, but one bad file blocks strict gate; message names path. Fine.
W6. Docstring says `--strict` accepted, rc unchanged; ok, but script ignores it silently (no validation of unknown flags). Typos like `--lst` run silently in default mode. Minor.

## Evidence
- Regex diff vs PRD lines 32-36 (parsed PRD file, compared strings with `==`): PIN_RE, STAMP_RE, PROSE_RE, BARE_RE, COUNT_RE all IDENTICAL. Flags: PIN/STAMP/BARE re.I true; PROSE/COUNT case-sensitive. Matches PRD rev 5/6 spec.
- ReDoS: 14 pathological 1MB lines (dash runs, space runs, `in `/`the 5.1 ` repeats, digit runs, decimal pairs, model_awareness/pattern_library_version runs). Max 0.30s (`in <1M digits>.<1M digits>`), typical 0.1s. No catastrophic backtracking. 3MB single line file: completes.
- Exit codes: non-repo default rc 2 (stderr msg); empty repo default rc 2 with summary lines printed; clean rc 0; hit rc 1; undecodable file rc 2 naming path; `--help` rc 0; `--paths` zero scannable rc 0; `--check-fixtures` rc 0 (`fixture failures 0 []`); `--canary` `canary ok` rc 0. Summary line `guard-scope hits N files M` last in every scan.
- Live scope run: `files-scanned 486`, `guard-scope hits 85 files 30`, rc 1 (expected pre-migration; S2+ work).
- Self-scan: `--paths scripts/check_model_pins.py` gives hits 0 (script passes own scan).
- subprocess safety: all 5 subprocess.run calls use list args, `shell=False`, `check=True` or rc checked; `git ls-files -z` split on NUL, `os.fsdecode` (surrogateescape safe); `-C top` explicit. Newline-in-name file: shown as `nl\x0afile.md` on one line via `_display`. cwd-independence: run from subdir gives identical result; non-repo cwd fails closed (default) as documented.
- Encoding: strict UTF-8 read; non-ASCII UTF-8 ok; CRLF ok (hit at line 2); symlinks skipped.
- Marker removal: `grep model-pin-ok` on script, both hooks, workflow: no match (rc 1).
- Stdlib only: imports json, os, re, subprocess, sys, tempfile.
- Python compat: `ast.parse(feature_version=(3,8))` ok; runs on 3.14.6 here. `capture_output`/`text=` need 3.7+; fine.
- Import-safety: scan only under `__main__`; module load via importlib executed with no output/side effects (used in ReDoS test).
- Hooks: `bash -n` ok on both; shellcheck only SC2034 (W4). `set -euo pipefail` hazards reviewed: pre-commit uses `|| pin_rc=$?` around xargs pipeline (safe under pipefail), zero staged guarded by `-n`, `xargs -0` with many files may run several chunks (multiple summary blocks, rc nonzero if any fail: acceptable, advisory). pre-push: `|| rc=$?` pattern, `|| [ -n "$local_ref" ]` handles missing trailing newline (last-line fix verified by reading), non-main refs and delete pushes skipped, dirty tree/non-HEAD go through `fail` (advisory unless strict). Idempotent: read-only on repo; canary uses mktemp repo removed by context manager; rerun gives same output.
- Workflow stale-model-id-guard.yml: push main + PR + dispatch, `contents: read`, `persist-credentials: false`, no `${{ }}` interpolation, no claude CLI. skill-line-budget.yml diff: additive push trigger + persist-credentials false (matches plan D4).
- Independence with QA: script reads `scripts/model_pin_fixtures.json` only via `load_fixtures()`; keys used exactly the documented schema (rule_a/b must_hit/pass, known_fp str-or-dict, canary uses first rule_a_must_hit). `provenance` key ignored. Absent file is a no-op. `grep -E "claude-[a-z]+-[0-9]|Opus [0-9]|4\.7"` on the script: no match; canary fallback pin built by string concat at runtime. No embedded must-hit literals.
- Scratch scripts (outside repo): /tmp/s1_rev.py, /tmp/s1_rt.py. Repo untouched, nothing committed.
