<!-- run: run-2026-05-28-o48m -->
# Adversarial review, loop 3: BACKLOG-108 Stage 4 architecture (revision 2)

Role: challenger (fresh reviewer, attacks the design only; does not author or revise it). Decision to use latest-version references is binding and not re-debated. Read from disk: `solution/architecture.md`, `adrs/ADR-lmr-001..005`. PRD sections consulted as baseline. Scratch work under `/tmp/lmr-ch3-run/` (copy of tracked files; worktree not modified, `git status --porcelain` empty at end).

Result: 0 blocking, 7 significant, 8 minor. CONFIDENCE 3/5 (ready for Plan once the significant items are folded into Plan or ADR text; none needs a redesign).

## Findings

### F1. significant, class coupling: ship-gate step 2 (clean tree) fails in any checkout that holds a nested worktree; the checkout used for ship is unspecified
Evidence:
- `.gitignore` has no `.claude/worktrees` entry (only `.claude/settings.local.json`, line 187). `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.git/info/exclude` holds only the stock comment lines; global ignore `~/.config/git/ignore` holds only `**/.claude/settings.local.json`.
- Reproduced in a scratch repo with a nested worktree under `.claude/worktrees/w1` (no ignore): `git status --porcelain --untracked-files=all` printed `?? .claude/worktrees/w1/`, and `git ls-files --cached --others --exclude-standard` printed `.claude/worktrees/w1/` as an entry.
- ADR-lmr-005 item 8 preamble: gate runs "in the checkout whose HEAD will be pushed ... after the squash-rebase and ff-merge"; step 2 `test -z "$(git status --porcelain --untracked-files=all)"`. The ADR never says whether that is the main checkout (which holds this worktree under `.claude/worktrees/`, so step 2 fails deterministically) or the worktree itself (where `main` cannot also be checked out for the ff-merge). The pre-push hook (ADR-lmr-002 D8) has the same dirty-tree test.
Required fix: name the ship checkout in ADR-lmr-005 item 8; change step 2 and the hook to exclude nested worktrees (`-- . ':!.claude/worktrees'`) or add `.claude/worktrees/` to `.gitignore` (state it is a repo-file addition and that the guard treats it as out of scope); add a Plan AC that step 2 prints clean in the chosen checkout.

### F2. significant, class coupling: smoke harness writes unignored run output into the tree, so the clean-tree gate fails after the live capture
Evidence:
- `run_smoke.py` line 55: `--out-dir` default is `here / "artifacts"` = `delivery-team/tests/smoke/artifacts/`; each run creates `<ts>/stream.jsonl`, `report.json`, `stderr.log`.
- `git check-ignore -v delivery-team/tests/smoke/artifacts/x/stream.jsonl` returned exit 1 (not ignored); `.gitignore` grep for `smoke|artifacts` finds only the `lib/` exceptions; only `*.log` is ignored (line 64).
- S5b runs 5 samples plus the fixture capture before S7. Nothing in architecture.md or ADR-004/005 mentions `--out-dir`, an ignore entry, or cleanup (`grep -n -i 'out-dir|smoke/artifacts|untracked'` finds only the porcelain lines).
Required fix: S5b/S5a dispatch prompts pass `--out-dir` outside the repo (for example `$TMPDIR`), or S5 adds `delivery-team/tests/smoke/artifacts/` to `.gitignore`; add to the S7 handoff list.

### F3. significant, class coupling: ship gate is internally ordered wrong (step 0 needs history the preamble has already squashed)
Evidence: ADR-lmr-005 item 8 preamble puts the gate "after the squash-rebase and ff-merge, immediately before `git push`". Step 0 runs the pre-ship-only ACs (AC-2.1, AC-2.5, AC-4.4, AC-5.9b). PRD FR-7.3 says these "read `main` or the branch history and stop being meaningful after the ff-merge", and PRD FR-4.4 says AC-4.4 is pre-ship "because the trailers and commits are squashed away by the ship". AC-4.4 needs per-commit `Dispatch-Id` trailers and `git merge-base --is-ancestor first-validator first-fix` (ADR-004 section 6 item 4); after a squash there is one commit. A literal executor either fails step 0 or runs it before the squash and ignores the preamble.
Required fix: split the gate into a pre-squash block (step 0, on the branch) and a post-squash block (steps 1 to 9); state which commit each step evaluates.

### F4. significant, class coupling: per-story manifest set is circular for S7 and does not name S5a/S5b
Evidence: ADR-lmr-005 item 5 requires `dispatch-manifest-S<k>.txt` in `06-development` for every story S1..S7, and item 8 step 8 (AC-DISP) is inside S7's own ship block. S7's DoD validators review S7's report, which cites the gate log, which contains step 8, which needs the S7 manifest. Also S7 executes after UAT (architecture.md section 5), not in Stage 6, while the manifest lives under `06-development`. S5 is split S5a (Stage 6) and S5b (Stage 7, `07-uat`); the required-name set S1..S7 has no S5a/S5b, and S7b is named in `07-uat`.
Required fix: define which validator round the S7 manifest covers (pre-ship deliverables only: CHANGELOG, memory) and that the ship log is validated by S7b; rename the required set to the real units (S1..S4, S5a, S5b, S6, S7, S7b) and state the directory for each.

### F5. significant, class data-integrity: AC-DISP requires a `02-refine` manifest that cannot be written truthfully
Evidence: `find .delivery -name 'dispatch-manifest*'` prints nothing. `02-refine` is finished (`stages_completed: [1, 2]`), and `04-architect` is under way. ADR-lmr-005 decision 1 lists `02-refine` and `04-architect` as REQUIRED and excludes `01-idea` because it "predates the manifest rule", but Stage 2 predates it equally. Item 6 says ids are pasted verbatim from the Agent tool result, never typed. No artifact recorded the Stage 2 dispatch ids, so a Stage 2 manifest can only be reconstructed by typing ids, which the ADR itself forbids and the checker cannot detect. Also item 5 requires ids unique across all manifests; a reconstruction with placeholder ids would pass.
Required fix: either drop `02-refine` from REQUIRED (with reason, as for `01-idea`) or define a retroactive-manifest form that is clearly marked `reconstructed` and is exempt from the transcript cross-check and from the "agent ids copied" claim; do the same for the part of `04-architect` already dispatched before the manifest writer exists.

### F6. significant, class testability: red-first evidence is measured against `main`, not against the validator's start commit; the P0 "stub" is never checked to be a stub
Evidence: PRD AC-5.9b exports `main` and overlays the branch `tests/`; ADR-004 section 6 follows it. Against `main`, most new tests fail by ImportError/TypeError (new names, new kwargs), so red proves nothing about the defect. Nothing constrains P0 (Dispatch-Id A, "legacy-compatible bodies") to be a stub: a producer can land the complete fix in P0, the validator then writes tests that pass at once, and the `main`-based red run and the ancestor check (`validator commit is an ancestor of first P1 commit`) both still pass. The clause "every real_shape assertion message states the defect" narrows this to one test file convention but does not close it.
Required fix: evaluate red-first at `validator_start` (HEAD after P0) for the `real_shape` and capture-failure tests, require they fail there by assertion (not ImportError), and add an AC that `git diff <base_sha>..<validator_start> -- delivery-team/tests/smoke/lib/metrics.py` changes no behaviour of `parse_stream` (signatures and exception classes only).

### F7. significant, class data-integrity: a uniform `latest` stamp on files nobody reviewed repeats a failure the team already recorded
Evidence: 19 of the 26 `model_awareness` lines are `opus-4-7-frontmatter-only` (git grep: `19 model_awareness: opus-4-7-frontmatter-only`, `7 model_awareness: opus-4-7`). Under NARROW (BINDING-6.1) only 3 SKILL.md get a prose review, but all 25 stamped files get `last_audited: 2026-09-20` and `latest`. Memory records the opposite rule twice: `.delivery/memory/archive/retrospective-run-2026-04-20-o4v7.md` line 79 ("`model_awareness: opus-4-7` on a file that was not prose-reviewed is a false claim wearing a truthful sleeve ... Do not optimize for zero-cost backfill at the cost of marker trust") and `.delivery/memory/archive/run-2026-04-22-4x7e.md` line 46 ("mechanical uniform stamping would lie cheaply"). ADR-lmr-003 A6 defines `latest` as "written for whichever model is latest at `last_audited`", which 22 files do not certify. The falsifiable distinction (`-frontmatter-only`) is deleted with no replacement. The PRD fixes the stamp value, but the design can still keep it honest.
Required fix: add to ADR-lmr-003 A6 a stated limit that for the 22 non-reviewed files `last_audited` records the mechanical stamp only, and require the S3 ledger (or a second census file) to list those 22 paths as `stamp-only, not prose-reviewed`; raise the residual risk to the PO as a Plan decision.

### F8. minor, class testability: the S5 interface table omits the report and `init_baseline` shapes the validator must test against
Evidence: `lib/report.py::build_report` (read) emits no `model_requested`, `model_resolved`, `effort`, `host_context`, `session_id`, `tokens.cache_hit_ratio`, and no stream path; `init_baseline(reports, out_path)` (baseline.py line 138) receives none of it. ADR-004 section 2 pins nine functions but not `build_report`'s new keys or how `init_baseline` learns each sample's stream file and `session_id` (needed for the distinct-`session_id` rule and `samples[]`). The validator must write AC-5.5b(iv) and AC-5.5c tests before the producer fix, so it must invent these names.
Required fix: add `build_report` output keys and the `init_baseline` inputs (or a `sample` record type) to the P0 stub table.

### F9. minor, class data-integrity: an outcome-failed sample (exit 1) is averaged into the baseline
Evidence: `run_smoke.py::_init_baseline_flow` aborts only on `code in (2, 3, 4)`; exit 1 (`outcome.success is False`, or the new strict-model FAIL) continues and the report is passed to `init_baseline`. ADR-004 section 4 restates "aborts on exit 2 ... as it already does for 2, 3 and 4" and adds nothing for 1.
Required fix: abort `--init-baseline` on 1 as well, or record the failed sample's outcome in `samples[]` and refuse `sample_status: active`.

### F10. minor, class testability: version words in non-`.md` in-scope files pass the guard and the accepted-loophole list omits the class
Evidence (my own run of the five PRD constants, `/tmp/lmr-ch3-run/guard.py`): `.py` `MODEL = "opus-4-7"`, `.py` `# tuned for Opus 4.7`, `.yml` `model: sonnet-4-6`, `.sh` `claude --model opus-4.7` all print `pass`; `.md` `Opus 4.7` prints `HIT`. PROSE_RE and BARE_RE apply only to `.md` (ADR-002 D2 item 3). ADR-002 lists accepted loopholes and out-of-scope extensions but not this in-scope gap. Baseline check: my re-implementation reproduces the PRD numbers (`stamp 52, pin 20, prose 19`, 31 files) on the current tree, and no such line exists today.
Required fix: add the class to ADR-002 Consequences (accepted loopholes) and to the PO decision list with P17/P19, or extend Rule B to `.py .sh .yml .txt` comment lines if the PO wants it.

### F11. minor, class docs: gate steps 1, 5 and 9 are "judged by exit status" but the commands always exit 0
Evidence: ADR-lmr-005 item 8 rule "a step is judged by its exit status", fixed for step 2 only. Step 1 `git rev-list --count HEAD..origin/main prints 0`, step 5 (count equality) and step 9 `rev-list --count origin/main..HEAD prints 0` are prints. Reproduced: `git rev-list --count main..b2` printed `1` and the shell reported no error (exit 0). Step 1 is harmless (git rejects a non-ff push) but step 5 and 9 are silent.
Required fix: write them as `test "$(git rev-list --count ...)" = 0` and `test "$a" = "$b"`.

### F12. minor, class coupling: parallel S2 dispatches share one git index with no commit protocol
Evidence: architecture.md section 5 window 1 lets three developer dispatches run in parallel in one working tree; nothing says how they commit. Concurrent `git commit` in one worktree contends for `.git/index.lock`, and an un-pathspec'd commit picks up another dispatch's staged edits, mis-attributing the `Dispatch-Id` trailer the design leans on. Not run (reasoning from git semantics; see the unverified list).
Required fix: state that the orchestrator commits serially after the window, or each dispatch uses `git commit -- <its files>` with a retry on lock.

### F13. minor, class docs: cited effort-default facts are already stale versus the live pages
Evidence: see doc table. architecture.md section 6 OQ-8 and section 11 UNVERIFIED (7) say the default for the latest Opus is undocumented. The live API overview lists `Default effort | high` for `claude-opus-5` and `claude-sonnet-5`, and the Claude Code page says `high` is "the default on every model except Opus 4.7". The CLI reference now lists `--effort` options `low, medium, high, xhigh, max, or ultracode`; the architecture lists five levels.
Required fix: update OQ-8 and UNVERIFIED (7) to "high, by the two pages above"; note `ultracode`; no requirement changes (the runner still passes `--effort xhigh` for `opus` only, so `xhigh` is documented as non-default for the latest Opus).

### F14. minor, class docs: the `.githooks` hooks are inert in this repository and the design does not say so
Evidence: `git config --show-origin core.hooksPath` prints `file:/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.git/config  /var/home/meconnelly/Documents/GitHub/Claude-Plugins/.git/hooks`, and that directory holds only `*.sample` files. So neither the existing pre-commit hook nor the new pre-push hook runs here unless the operator changes the shared config. The design calls them "opt-in" but relies on P4 and D8 as if installed.
Required fix: add to the S1 and S7 handoff: install command (`git config core.hooksPath .githooks`) and log line that records whether it is set; state that the pre-push hook is inert otherwise.

### F15. minor, class performance: all 11 `fitness_review_due` are reset to the same date
Evidence: ADR-lmr-003 A4 sets `2026-12-19` on all 11; `governance/fitness-review.md` line 34 says the field is "staggered across an 80-100-day window so the load distributes"; `fitness-review.yml` opens reminders per due date, so 11 reminders fire in one week.
Required fix: stagger within (today, today+90] as the governance file says; AC-3.3a still passes.

## Class summary

| Class | blocking | significant | minor | total |
|---|---|---|---|---|
| coupling | 0 | 4 (F1, F2, F3, F4) | 1 (F12) | 5 |
| security | 0 | 0 | 0 | 0 |
| data-integrity | 0 | 2 (F5, F7) | 1 (F9) | 3 |
| naming | 0 | 0 | 0 | 0 |
| testability | 0 | 1 (F6) | 2 (F8, F10) | 3 |
| performance | 0 | 0 | 1 (F15) | 1 |
| docs | 0 | 0 | 3 (F11, F13, F14) | 3 |
| misc | 0 | 0 | 0 | 0 |
| **total** | **0** | **7** | **8** | **15** |

## Verified claims (confirm, no finding)

| Claim | My command / output | Result |
|---|---|---|
| Stamp edits on 25 files are line-neutral | scratch copy, regex value replacement: `stamped 25 9056 9056`, every file same line count | CONFIRMED |
| delivery-flow stays 499 after stamps plus the two 4-line blocks | `lines 499 bytes 28684`; `check_skill_budgets.py` in scratch: `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` exit 0; product-delivery 300 to 300 | CONFIRMED |
| Byte deltas | stamps only 28,616 to 28,614 (-2); with blocks 28,684 (+68) | CONFIRMED |
| Whole-file hash changes; re-freeze gives MATCH | before re-freeze `MISMATCH`; whole `f5329b59fc9b...`; after `sha256sum > governance/cache-prefix-hash.txt` prints `MATCH`, `wc -l` 499 | CONFIRMED |
| First-2048-byte hash for delivery-flow | `66bcaa25` (ADR predicted `66bcaa25`); all 25 stamped files change in the first 2048 bytes (`pfx2048-changed` 25 of 25); 13 are under `delivery-team/skills/` | CONFIRMED |
| Guard on the rewritten text | delivery-flow shows 0 pin/prose/stamp hits after S2/S3 simulation; stamp hits 0 across all 25 (`rev-1` is not matched by STAMP_RE) | CONFIRMED |
| Current tree counts | `Counter({'stamp': 52, 'pin': 20, 'prose': 19}) files 31` | CONFIRMED (matches PRD) |
| `lint_known_debt.py` after stamps | `LINT OK: known_debt JSON<->Python in sync; all SKILL.md frontmatter complete.` rc 0 | CONFIRMED |
| `test_meta.py` baseline | `3 passed` | CONFIRMED |

## Consumers of any hash or prefix notion (enumerated)

`git grep -n -I -i -E 'cache-prefix|prefix_hash|PREFIX_READ|cache_prefix|prefix hash|2048|sha256sum|fingerprint'` outside `.delivery/` and `CHANGELOG.md`, plus `git grep -l -E 'hashlib|sha256|md5|sha1'`:
- `governance/cache-prefix-hash.txt` (whole-file sha256): read by no script or workflow; only AC-6.1 and the S7 gate. Mentioned in `governance/fitness-review.md` line 9 and the delivery-flow `## Volatile` comment (lines 480-482).
- `delivery-team/hooks/telemetry.py` (`PREFIX_READ_BYTES = 2048`, `sha256[:8]`): only code consumer; documented in `delivery-team/references/telemetry-schema.md` lines 23 and 44-52.
- Stale docs (no reader): `delivery-team/artifacts/06-dev/**` three files.
- `hashlib` users unrelated to this notion: `agentic-flow-builder/scripts/flow_orchestrator.py`, `hardware-team/scripts/security.py`.
- No workflow reads a hash (grep of `.github/workflows` for `SKILL.md` finds only presence, budget, known-debt, fitness-date checks). Architecture's consumer list (ADR-lmr-001) is complete. Readers of `model_awareness` / `pattern_library_version` / `last_audited`: `skill-md-header-warn.yml` (presence of `model_awareness:` only), `prompt-engineer/SKILL.md` lines 420-422 (definition), `delivery-flow/SKILL.md` line 491; `lint_known_debt.py` requires `fitness_review_due`, `context_budget`, `tier`, `maintainer`; `fitness-review.yml` reads `fitness_review_due`. No other reader; ADR-lmr-003 A6a list matches.

## Doc re-fetch (WebFetch, 2026-09-20)

| URL | Claim in architecture | Live page | Verdict |
|---|---|---|---|
| https://code.claude.com/docs/en/model-config | alias `opus` and `sonnet` are "latest"; `haiku` is "the fast and efficient Haiku model for simple tasks" (no "latest") | table rows: "Uses the latest Opus model for complex reasoning tasks"; "Uses the latest Sonnet model for daily coding tasks"; "Uses the fast and efficient Haiku model for simple tasks" | MATCH |
| same | "Aliases point to the recommended version for your provider and update over time. To pin ... use the full model name ... or set ... `ANTHROPIC_DEFAULT_OPUS_MODEL`" | same sentence, verbatim, with example `claude-opus-5` | MATCH |
| same | `high` default except Opus 4.7 (`xhigh`); levels low, medium, high, xhigh, max | "`high`: ... The default on every model except Opus 4.7"; "`xhigh`: ... The default on Opus 4.7"; table also lists `ultracode` | MISMATCH (minor): level list is now six; see F13 |
| https://code.claude.com/docs/en/headless | "The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins" (no field name) | "The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins." field name not given | MATCH |
| same | "`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release." | verbatim in a Note | MATCH |
| same | `total_cost_usd` and per-model breakdown with `--output-format json`; subagent messages carry `parent_tool_use_id`, null for main | "the response payload includes `total_cost_usd` and a per-model cost breakdown"; "`parent_tool_use_id` field is the ID of the tool call that spawned the subagent. Messages from the main conversation carry `null`". Also new: by default a subagent's text blocks are not forwarded, only `tool_use`/`tool_result` (text needs `--forward-subagent-text`) | MATCH; the default-forwarding fact is not in ADR-004 parser rule 3 (note for the validator fixture; not a finding) |
| https://code.claude.com/docs/en/cli-reference | `--max-budget-usd` "before stopping (print mode only)"; subagent spawn fails with `Budget limit reached`; effort levels depend on model | row: "Maximum dollar amount to spend on API calls before stopping (print mode only). ... spawning another subagent fails with `Budget limit reached` ... require Claude Code v2.1.217 or later"; `--effort` "Available levels depend on the model" | MATCH |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | latest Opus "delegates to subagents more readily" (block 1 anchor) | "Claude Opus 5 delegates to subagents more readily than prior models." Also: "Start with the default (`high`) and adjust based on your evals" | MATCH (the shipped sentence is version-free and true today; it will go stale on a future model, risk R7 already carried) |
| https://platform.claude.com/docs/en/about-claude/models/overview (redirects to /docs/en/models/overview) | API has no evergreen alias; config values need a configured ID (ADR-003 A2) | "**Claude API ID:** Every Claude model ID is a pinned snapshot, including the dateless IDs used from the 4.6 generation on."; `Default effort` row: `high` for Fable 5.1, Opus 5, Sonnet 5 | MATCH; extends OQ-8 (F13) |

Web summaries are produced by the fetch tool's small model; I quote only text it returned inside quotation marks.

## Commands run (abridged, outputs used above)

| Command | Output used |
|---|---|
| `wc -l` on architecture and ADRs | 341 / 91 / 97 / 103 / 103 / 73 lines |
| `git ls-files > files.txt`; python copy of 843 tracked files to `/tmp/lmr-ch3-run/repo` | `copied 843` |
| `python3 sim.py` (regex value replacement of the four stamp keys in the 25 stamped files) | `stamped 25 9056 9056`; every file `pfx2048-changed` |
| `python3 prose.py` (the two 4-line blocks from architecture.md section 4 into the scratch delivery-flow) | `lines 499 bytes 28684`; whole `f5329b59...`; first2048 `66bcaa25` |
| `python3 scripts/check_skill_budgets.py` in scratch | `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` exit 0 |
| `sha256sum ... > governance/cache-prefix-hash.txt` then `diff` in scratch | `MATCH`; `wc -l` 499 |
| `python3 guard.py <worktree>` and `<scratch>` (five PRD constants) | `stamp 52, pin 20, prose 19, files 31`; scratch after S2/S3: no stamp hits, none in delivery-flow |
| `python3 scripts/lint_known_debt.py` in scratch | `LINT OK ...` |
| `git grep -n -E '^(model_awareness|...):' -- '*SKILL.md'` census | `19 model_awareness: opus-4-7-frontmatter-only`, `7 ... opus-4-7`, 26 `pattern_library_version: 4-7-1`, 18+8 `last_audited`, 11 `fitness_review_due: 2026-08-09` |
| scratch nested-worktree repo: `git worktree add .claude/worktrees/w1`, then `git status --porcelain --untracked-files=all` and `git ls-files --cached --others --exclude-standard` | `?? .claude/worktrees/w1/` and `.claude/worktrees/w1/a.md` listing |
| `git check-ignore -v .claude/worktrees/x/y`; same for `delivery-team/tests/smoke/artifacts/x/stream.jsonl` | both exit 1 (not ignored) |
| `git config --show-origin core.hooksPath`; `ls .git/hooks` | pinned to `.git/hooks`, samples only |
| `find .delivery -name 'dispatch-manifest*'` | no output |
| scratch: `git rev-list --count main..b2` | printed `1`, tool reported success (exit 0) |
| `python3 -m pytest delivery-team/tests/smoke/tests/test_meta.py -q` | `3 passed`; `git status --porcelain` afterwards empty |
| `claude --version`; `claude --help` grep | `2.1.278 (Claude Code)`; `--effort`, `--max-budget-usd`, `--model`, `--bare` present |
| reads: `run_smoke.py`, `lib/metrics.py`, `lib/runner.py`, `lib/baseline.py`, `lib/report.py`, `lib/aggregator.py`, `tests/conftest.py`, `.githooks/pre-commit`, `skill-line-budget.yml`, `fitness-review.yml`, `stale-model-id-guard.yml`, `.delivery/config.yml`, `state.md` | facts cited in F1 to F15 |
| WebFetch x5 | doc table above |

## Not verified

- No run of the pre-push hook or the pre-commit hook body (ADR says it ran seven cases against a stubbed git; I did not rerun them).
- F12 (index-lock contention and mis-attributed trailers) is argued from git semantics, not reproduced.
- I did not run `git status` in the main checkout (constraint: touch only the worktree); F1 rests on the ignore-file reads plus a scratch reproduction.
- The ship checkout and whether `main` is pushed from the main checkout or via `HEAD:main` are unspecified in the design; F1 covers both readings.
- Real stream facts (`message.id` on assistant events, budget-stop subtype, whether the cap stops between turns) not tested; no `claude` model run was made (no paid runs).
- Full PRD not read; consulted FR-3.x, FR-4.4, FR-5.x ACs, FR-7.3/7.4, AC-DISP, guard constants only. PRD-vs-code contradictions beyond those listed (F5, F9, F13) were not found in the sections read; other sections unchecked.
- Did not fetch `platform.claude.com/.../model-ids-and-versions` or the agent-sdk typescript page; the overview page covers the evergreen-alias claim; the `error_max_budget_usd` subtype remains UNVERIFIED.
- Did not read stale files in `04-architect/`, other stages' challenger/dod/evaluator directories, or earlier challenger loops, per instruction.
- Guard simulation used my own copy of the PRD constants, not the (not yet written) `scripts/check_model_pins.py`.

## Confidence

3 of 5 that the design is ready for Plan. No blocking finding; the design is broadly sound and its numeric claims (line neutrality, bytes, hashes, budgets) all reproduce. The seven significant items are ship-gate and manifest mechanics (F1 to F5), a red-first loophole (F6), and a stamp honesty gap (F7); each is a text fix in ADR-lmr-005, ADR-lmr-004 or ADR-lmr-003, or a Plan AC, and none forces re-architecture. Not escalating to a human on confidence alone; F7 is a Plan decision for the PO.
