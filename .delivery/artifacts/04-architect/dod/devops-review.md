---
verdict: DONE
round: 2
role: devops
stage: 4-architect
run: run-2026-05-28-o48m
backlog: BACKLOG-108
reviewed_commit: 0bd698b
blocking_issues: []
---

# DevOps DoD review, Stage 4 (revision 4, round 2)

Rev 4 snippets and guard rules work. Exit-status safe. No blockers. Three warnings.

## Blocking issues

None.

## Checks and evidence

Scratch dir `$CLAUDE_JOB_DIR/tmp/r` (test scripts `t.sh`, `t2.sh`). The real guard script does not exist yet, so I used a stand-in that follows ADR-lmr-002 D9 exactly (`git ls-files --cached --others --exclude-standard -z`, `shell=False`, NUL split, skip non-regular files, `files-scanned K` before the summary, exit 2 on empty scope or listing failure).

| Check | Result | Evidence |
|---|---|---|
| `-z` with non-ASCII plus newline filename | OK | Name `café nu<LF>l.md`. Plain `git ls-files` prints it quoted as `"caf\303\251 nu\nl.md"` (would fail to open, so fail-closed exit 2 rather than silent skip). With `-z` it is one entry and was scanned (`files-scanned 3`). |
| Non-UTF-8 filename | OK | `bad\xff.md` scanned via surrogateescape, rc 0. Unreadable or undecodable file CONTENT is the fail-closed case per D9. |
| Nested worktree in scope | OK | `--others` lists `.claude/worktrees/w1/` as a directory entry; the non-regular-file skip drops it. `files-scanned` did not count it. Matches ADR-005 claim. |
| Step 4 own-rc capture | OK | `( set -euo pipefail; rc=0; out=$(guard) \|\| rc=$?; ... )` printed `step=4 exit=0` and the summary regex `^guard-scope hits [0-9]+ files [0-9]+$` matched. `\|\| rc=$?` survives `set -e`. |
| Step 5 extraction, clean tree | OK | `canonical_count` (`tail -n 1 \| awk '{print $3}'`) = `0`; `script_list_count` (`awk '/^(pin\|stamp\|prose) /{n++} END{print n+0}'`) = `0`, awk rc 0 on empty input. `files-scanned` and the summary line do not match the hit-line regex. |
| Step 5 extraction, one hit | OK | `cc=1 sc=1`, guard rc 1 (allowed set 0 or 1). Field 3 of `guard-scope hits N files M` is N; correct. |
| Canary | OK | Fresh `mktemp -d` clone plus untracked `canary.md` with synthetic pin: rc 1, `pin canary.md:1` listed, `files-scanned 4`. After delete: rc 0. Untracked file is caught because of `--others`. |
| Scan-nothing | OK | Empty repo: rc 2, no summary printed. Run outside a repo: rc 2 with stderr. Missing script (`python3 nope.py`): rc 2 (127 only if python itself missing). Both fail step 4 by the rc rule. |
| Hooks `-z` / `xargs -0` | OK | `git ls-files -z -- '*.md' \| xargs -0 -r wc -l` works on the odd-name repo. |
| Workflow `permissions:` and `persist-credentials` | OK | `permissions: contents: read` at workflow level is valid (existing `stale-model-id-guard.yml` and 8 other workflows already do it). `persist-credentials: false` is a valid `with:` input of `actions/checkout@v4`. Parsed a sample YAML with `push`/`pull_request`/`workflow_dispatch` plus those keys: valid. Guard needs no token; only local `git ls-files`, so no credential is needed with the default depth 1. |
| No `claude` in `.github/workflows/` | OK | `grep -rnE '(^\|[ ;\|&(])claude( \|$)' .github/workflows` = no hits. Only matches are `.claude-plugin/` paths and model-ID text in the old guard. Rev 4 ADR text adds only Python and shell steps; smoke harness stays local (feedback rule respected). |
| Ship-gate hazard rules (rev 2/3 items) | OK, unchanged | `test "$(...)" = 0` wrappers and `grep -q` negation still present in steps 1, 2, 9. |
| `MUST NOT exceed` vs PRD AC-2.5 | OK | Ran the AC-2.5 regexes on the 4 new block lines: `cond` True (When ... latest Opus, 48 chars gap, limit 80); `cap` True (line 3 has `dod_validators`, `at most`, `subagents`). Block stays 4 lines replacing shipped lines 273-276 (current text at SKILL.md 272-276), so 499 lines unchanged and Tier A budget (500) holds. |
| `check_skill_budgets.py` and cache-prefix (ADR-lmr-001) | OK | Checker has no reference to `MUST`, `equal` or `dod_validators` (grep). No script consumes the prose. Edit sits past byte 2048, so the telemetry prefix hash (`PREFIX_READ_BYTES = 2048`) is unaffected; the whole-file `governance/cache-prefix-hash.txt` changes as designed and S6 recomputes it (rev 4 states no hash pinned by the reword). |
| Round-1 warnings W2, W3, W4 | Resolved | W2: aggregate `spent <= 15.00` check plus operator go (ADR-005 step 9, ADR-004 s8). W3: no exception route on push; `known_debt[]` with `target_wave:` committed before ship. W4: squash to one push, never push S1-S3 alone. |

## Non-blocking warnings

- **W1, step 5 depends on `--list` hit-line prefixes.** The count regex hardcodes `pin `, `stamp `, `prose `. A new category name in the script silently drops out (count 0 vs summary N), which fails the equality check loudly, so it is safe, but the Plan AC should pin the three prefixes in a fixture test.
- **W2, `spent` extraction not specified.** ADR-005 step 9 says sum `total_cost_usd` over reports but gives no snippet. Plan should give a python one-liner that fails on a missing or null field (missing = failure, not 0). Same exit-status trap class as `grep -c`.
- **W3, workflow checkout tag is floating (`@v4`).** Consistent with all existing workflows; not a blocker. Optional: pin by SHA later.
- Carry-over from round 1, unchanged: W1 hook bypass (RR-1, accepted), P19 Makefile/`.githooks/*` outside scope.

## Verdict

DONE. 0 blocking issues, 3 new warnings.
