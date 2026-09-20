---
verdict: DONE
role: developer (DoD validator)
stage: 4 (Architect)
run: run-2026-05-28-o48m
backlog: BACKLOG-108
artifact_reviewed: architecture.md rev 3, ADR-lmr-001..005
blocking_count: 0
warning_count: 6
prose_style: caveman-lite
---

# Developer DoD review, Stage 4, BACKLOG-108 (fresh review of rev 3)

Question: can a dev implement S1..S7 without guessing? Answer: yes. No blocker. Six gaps, all small, each has a sane default a dev would pick. Fix at Plan or in dispatch prompts.

## Blocking issues

None.

## Non-blocking warnings

### W1. `run_smoke.py` argparse for `--model` / `--effort` not pinned; `_spawn_and_tee` missing from interface table
- PRD AC-5.3: `run_smoke.py --help | grep -cE -- "--(model|effort)"` must be >= 2.
- ADR-lmr-004 s2 pins `_build_claude_command` and `run_pipeline` only. It says "`run_smoke.py` exposes no `--model` other than `opus`". Reads two ways: flag exists with only `opus` allowed, or flag absent. Absent would fail AC-5.3.
- Real code: `run_pipeline` (runner.py:304) calls `_spawn_and_tee` (runner.py:167), which calls `_build_claude_command(workspace, prompt_path)` at runner.py:175. `_spawn_and_tee` is not in the table, so nobody is told to thread `model`/`effort`/cap through it. `_execute_single_run` in run_smoke.py also not named.
- Evidence:
  - `grep -n "add_argument" ...run_smoke.py` -> flags today: `--init-baseline --cost-cap --timeout --baseline --out-dir --prompt --config --stream-fixture --repo-root`. No `--model`, no `--effort`.
  - `grep -n "_build_claude_command" runner.py` -> lines 112, 175.
- Ask: pin `--model` (default `opus`, choices `[opus]`) and `--effort` (default `xhigh`), and add `_spawn_and_tee` to the table, in the P0 stub list.

### W2. Source of new report fields not stated
- ADR-lmr-004 s2 adds `session_id`, `stream_file`, `host_context.bare`, `model_pin_env` to report/baseline. `Metrics` (ADR s1 item 6) has no `session_id` field, and no text says who reads it from `system/init` or who passes `stream_path`/`session_id` into `build_report`. Same for `bare` (bool) and `model_pin_env` (read four env vars).
- Evidence: `build_report(*, run_id, repo_root, plugin_load_strategy, outcome, metrics, aggregator_dict, advisory_warnings, hard_failures)` at report.py:61; no session or stream args today.
- Ask: one line: `_execute_single_run` extracts `session_id` from the `system/init` event and passes it plus `stream_path`; env vars read in `init_baseline` or report.

### W3. Content of `smoke-streams/sample-<n>.jsonl` ambiguous
- ADR-lmr-004 s5: "per-sample raw stream (trimmed `system/init`: `type`, `subtype`, `model`, `session_id`)". Architecture s3 says "5 raw streams and their hashes". Full stream or a trimmed init line? Affects hash rule (distinct hashes) and repo size.
- Ask: state "full stream" or "trimmed init only".

### W4. Stale step number in ADR-lmr-001
- ADR-lmr-001 decision 4 says "Re-check at ship (S7 step 5)". ADR-lmr-005 item 8 has the hash `MATCH` at Block B step 7; step 5 is the R12 count equivalence.
- Evidence: `grep -n "step 5" ADR-lmr-001*.md` vs ADR-lmr-005 steps list (1 fetch, 2 clean tree, 3 SHIP_SHA, 4 guard, 5 R12, 6 budgets, 7 hash, 8 DISP, 9 push).
- Ask: change to "step 7".

### W5. Ship-gate step 5 variables undefined
- ADR-lmr-005 step 5: `test "$canonical_count" = "$script_list_count"`. No text says how to get each. Canonical = PRD s1 python heredoc (its last summary line, parse `hits N`). Script side = `--list` lines; D5 says `--list` also prints the summary line, so count must drop it.
- Evidence: PRD lines 30-65 heredoc prints `guard-scope hits 91 files 31` (ran it, see below). ADR-lmr-002 D5 "`--list` prints `category file:line` per hit before the summary".
- Ask: give the two extraction one-liners (for example `bash canonical | sed -n '1s/.*hits \([0-9]*\) .*/\1/p'` and `script --list | grep -c '^\(pin\|stamp\|prose\) '`).

### W6. Fixture sidecar is inside guard scope
- `stream_real_shape.provenance.txt` is `.txt`, so scanned (scope `.py .md .yml .yaml .txt .sh`). A natural provenance note ("model observed: <full id>") is a pin hit and fails AC-1b. The `.jsonl` is out of scope. ADR-lmr-002 D9 names tests and README, not the sidecar.
- Ask: add sidecar to the D9 "no literal model id" rule; record `command:` (alias only) and CLI version, not the resolved id.

## Verified references (design matches real code)

| Claim in design | Check | Result |
|---|---|---|
| Guard scope 91 hits / 31 files (pin 20, stamp 52, prose 19) | ran PRD s1 heredoc: `bash /tmp/lmr/count.sh` | `guard-scope hits 91 files 31` / `pin 20 stamp 52 prose 19`. Exact match. |
| `governance/cache-prefix-hash.txt` = whole-file sha256 of delivery-flow SKILL.md | `cat` + `sha256sum` | both `43067c9e...b8328`, identical |
| delivery-flow 499 lines / 28,616 bytes | `wc -lc` | `499 28616` |
| 2048-byte hash `8c2ebf97` | `head -c 2048 ... \| sha256sum` | `8c2ebf9705bc...37750` |
| First byte difference 854; stamps start by byte 927; 25 of 25 inside 2048 | grep -bo `opus-4-7`; python offset scan over 25 stamped files | 854; max first-stamp offset 927; `25 stamped ... inside 2048: 25` |
| telemetry `PREFIX_READ_BYTES = 2048`, `_compute_prefix_hash` sha256[:8] | `grep -n` telemetry.py | line 21, line 46-49 |
| 25 stamped SKILL.md, 26 model_awareness lines, 11 with `fitness_review_due` | grep -rl / grep -rn | 25 / 26 / 11 |
| 13 stamped delivery-team skills | counted from ADR table | 13 |
| Version blocks at delivery-flow lines 27-30 and 273-276, 4 lines each; doctrine 77-82 | `sed -n` | match |
| Proposed rewrite blocks are guard-clean | ran PIN/STAMP/PROSE/BARE on all 8 lines | all False |
| `MODEL_TIER_ALIAS` placement: after imports, above class; registry lines 148/149, 173/174, 189/190 | read agent_registry.py 1-40, 146-190 | imports end line 17, first class line 21, config lines and comment lines match |
| Budgets: 17 files, delivery-flow 499/500, product-delivery 300/300 | `check_skill_budgets.py` | `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).`; `wc -l` 499 and 300 |
| `--out-dir` at run_smoke.py line 57 | `grep -n` | line 57 |
| `run_smoke.py` exit-code table; `_init_baseline_flow` aborts only on (2,3,4) | read lines 184-207 | matches; design fix (abort on any non-zero) is a real change, correctly called out |
| runner in-loop kill at lines 95 and 252 | `grep -n _running_cost` | 95, 252 |
| `parse_stream` reads top-level `usage`/`model`, buckets `unknown` | read metrics.py 62-128 | matches ADR context |
| `_collect_metric_values` collects only fixed keys plus `skill_loads.*`; `_classify` returns hard/advisory only | read baseline.py 39-135 | matches; design's "skip is a no-op, real work is collect" is right |
| `SCHEMA_VERSION = "1"` in baseline.py:12 and report.py:13 | grep | match |
| `test_meta.py` = 3 passing | `pytest -q` | `3 passed` |
| conftest has 4 `claude-opus-4-7` model values (105,117,129,151) | grep | match |
| `config.yml` `dod_validators` at lines 56-63 | sed | match |
| `.claude/worktrees` absent from `.gitignore`; `core.hooksPath` = `.git/hooks` (hooks inert) | grep, `git config --show-origin` | confirmed; P23 correct |
| Ship step 2 pathspec form and `! git ls-files -v \| grep -q` form | ran on this worktree | porcelain with pathspec lists only .delivery review files; `grep -c '^[a-zS]'` printed 0 (exit 1, so the design's move away from `grep -c` is right) |
| `.githooks/pre-commit` structure (set -euo pipefail, ends `budget + lint OK.`) | read file | insertion point valid |
| `skill-line-budget.yml` is `on: pull_request` with `paths:` | sed | match |
| prompt-engineer/SKILL.md 520 lines, no tier; lines 363/365/368/371/420/421 as named | wc, sed | match |

No wrong line number, name or behavior found in the checked references.

## Note (not a finding)

Stage dirs: `git status` shows other reviewers' files (`devops-review.md`, `security-review.md`, modified `architect-review.md`) as dirty. That is normal mid-DoD and not a defect in the design.

## Verdict

DONE. A developer can implement S1..S7 from this design. W1 to W6 are small clarifications to fold into Plan or dispatch prompts; none blocks.
