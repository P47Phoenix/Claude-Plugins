# QA DoD Review, Round 2 (Stage 2 Refine)

Validator: QA Engineer (independent). Input: PRD Revision 5 (`.delivery/artifacts/02-refine/po/prd.md`), constraints.yml, idea brief, backlog, memory topic. Framing: TARGET (well-formedness and testability of each AC), not whether it passes today.

Task Type: dod-validation | Reference: Gate 2 / QA, DoD Validator Prompt Template | Scope: PRD Rev 5

## Verdict

**DONE** (no blocking criterion fails). 9 warnings, all fixable inside Stage 2 without redesign. Round-1 blocking items (must-pass floors, false positives, observable separation) are resolved in form; residual weaknesses below.

## Gate-result table

| # | Criterion | Result | Severity |
|---|-----------|--------|----------|
| 1 | Every FR has an AC with an unambiguous pass condition | PASS (FR-1.4, 2.4, 5.8, 7.3 are "inspection" with a named report line; acceptable) | - |
| 2 | No AC trivially satisfiable by a defeating edit | PASS with warnings (W2, W3, W4) | warning |
| 3 | NFRs numeric with measurement method | PASS (NFR-11 partly inspection, stated) | - |
| 4 | Each gate closed by exactly one item, reachable after its own scope | PASS with warning (W8: orphan ACs) | warning |
| 5 | BINDING-4.5 separation enforceable and observable | PASS with warnings (W1, W5) | warning |
| 6 | Guard fixtures cover false negatives AND false positives | PASS in form; my probes found misfires (W6, W7) | warning |
| 7 | Baseline / observed-model fails loudly on unknown/empty; not hand-editable | PASS with warnings (W3, W9) | warning |
| 8 | Negative tests exist | PASS (AC-1.1b self-tests, AC-1.6b, AC-DISP self-test, AC-5.5b) | - |
| 9 | Fixtures have provenance | PASS for guard fixtures (provenance object); real stream fixture partial (W9) | warning |

## Discovery-command spot check (worktree root, executed)

- Canonical counting command: prints `guard-scope hits 91 files 31`, `pin 20 stamp 52 prose 19`, listing as documented. Reproduces.
- AC-1.6a: `0`. AC-1.3: `0`. AC-4.5: `0`. AC-1.1 grep on today's workflow: `6`. `pytest test_meta.py`: `3 passed`. All match the PRD's stated today-values.
- `scripts/` holds no `check_model_pins.py` today, so AC-1.2a/1.2b/1.2c/3.1b/1.6b cannot run (expected; TARGET framing).

## Own regex probes (Python `re` and `grep -E`/`sed -E` pipeline, the exact five constants)

Python and grep engines agreed on every string (no engine divergence). Probe files: `/tmp/qa2/p.py`, `/tmp/qa2/q.py`.

**False positives (legitimate text that is flagged; must be reworded, no escape exists):**

| Sentence | Rule that fires |
|----------|-----------------|
| `Spawn Opus 3 workers.` / `Opus 6 validators` / `Opus 5 validators` / `Opus 2 teams` / `Opus 3 dispatches` / `Opus 3 attempts` / `Haiku 8 threads` / `Haiku 4 batches` / `Sonnet 3 sub-agents` / `Sonnet 5 files at once` / `Opus 4 parallel reviewers` / `Opus 2 x faster` / `Sonnet 3 of 5 pass` | PROSE_RE (noun not in COUNT_RE list) |
| `Use Opus twice, then Haiku 2 more times.` | PROSE_RE ("Haiku 2") |
| `see Sonnet 4 below`, `Haiku 3 is a poem form`, `Fable 12 chapters were read`, `Sonnet 14 lines long`, `Sonnet 3.0 seconds later` | PROSE_RE |
| `the new 5.0 release of React`, `on 6.8 kernels`, `for 5.2 users`, `in 5.1 channel audio`, `with 5.5 stars` | BARE_RE (other software versions, major 4-9) |
| `with 4.7 V rail`, `under 5.0 V supply`, `the 4.7 uF cap` | BARE_RE (electronics values with a space; relevant to hardware-team docs) |
| `in 4.5 sprints`, `for 4.2 iterations`, `for 4.5 s`, `under 4.0 GiB` | BARE_RE (unit not in COUNT_RE list: `s`, `GiB`, `sprints`, `iterations`) |
| `claude-plugins-v2`, `claude-md-2` | PIN_RE (any digit after `claude-`; file/tool names) |

Correctly passed: `Run Sonnet 3 times and average.`, `Python 3.11`, `Node 18.2`, `PostgreSQL 15.4`, `Go 1.22`, `Ubuntu 22.04`, `Claude Code 2.1`, `KiCad 9.0`, `Use Opus in 3 phases`, `model: opus`, `pattern_library_version: rev-1`, `claude-opus-fixture`, and all PRD-named counts and durations.

**False negatives (real pins that pass):** `claude_opus_4_7`, `CLAUDE_OPUS_4_7`, `OPUS_4_7`, `opus_4_7` (underscore constants), `claude opus 5`, `claude.opus.5`, `models/opus.4.7`, `Opus<TAB>5`, `Opus<NBSP>5`, `Opus five`. Known accepted count-form loopholes confirmed: `Opus 4 agents`, `Opus 5 agents`, `Sonnet 5 stories`, `Opus 5 runs`, `Opus 5 items`, `Opus 5 personas`, `Opus 5 reviews`, `Mythos 5 agents`, `in 4.7 days`. All others real-version probes hit in both engines (`Opus 5 delegates`, `claude-opus-4-7-20260101`, `anthropic.claude-sonnet-4-5-v1:0`, `OPUS-5`, `opus4.7`, `Opus 4.7-aware`, `claude-opus-latest`, etc.).

## Findings

**W1 (warning) FR-4.4 / AC-4.4, red-first is not chronological.** AC-5.9b proves the `real_shape` test discriminates the unfixed parser (fails on an export of `main`), but a test written after seeing the fix also fails on `main`. Nothing shows the test existed before the fix. Also a `real_shape` test could fail on `main` for a wrong reason (missing symbol). Required fix: add to AC-4.4 an ordering assertion (the first validator commit is an ancestor of, or committed before, the first `lib/` fix commit, via `git merge-base --is-ancestor` or `git log --reverse` order), and require the red run's failure text to contain the documented defect (`unknown` in the `model_usage` keys, or `cost_usd` 0.0) so the failure is for the right reason.

**W2 (warning) AC-1.2a, must-pass floor is a count, not content.** `rule_a_must_pass >= 10` and `rule_b_must_pass >= 12` are checked by `len()`, but only 2 and 11 strings are pinned by REQ. Eight rule-A must-pass slots can be filled by duplicates or trivial strings (`x`). Required fix: assert list entries are unique, each must-pass string in rule A contains a `claude` or `model` token (or has provenance in `qa-probe`, `repo-line`, `challenger`), and REQ names at least 10 rule-A must-pass strings including `claude-plugins-v2`-style legitimate hyphen-digit names (see W6).

**W3 (warning) AC-5.5b, unknown/empty rule not fully tested.** FR-5.5 says `unknown` in any case and empty string are absent. AC-5.5b cases (i) to (iv) cover none-at-all, `unknown` (one case), init-without-model, and consistency; no case for `UNKNOWN`, empty string, or `unknown` only inside `modelUsage` or `message.model` while init is valid. Also unlike AC-5.2 the test names are not pinned and the check is "`-rA` output names each" (inspection). Required fix: name the tests (`test_capture_fails_no_model`, `..._unknown_only`, `..._unknown_uppercase`, `..._empty_string`, `..._init_missing_model`, `..._samples_disagree`) and check with `-k capture_fails -v | grep -c PASSED` >= N, as AC-5.2 does.

**W4 (warning) AC-5.5c, five identical streams pass.** The check re-hashes each file, requires init model equal to `model_resolved[0]`, and mean of `total_cost_usd` equal to the baseline. Copying one real stream five times (or fabricating five) passes. Required fix: assert the five `stream_sha256` values are distinct and the five `session_id` values in the trimmed init events (kept per FR-5.10) are distinct. State remaining forgery limit as already done.

**W5 (warning) FR-4.4 / AC-4.4, authorship evidence is self-declared.** `Dispatch-Id` trailers and `s5-separation.txt` (`validator_start`/`validator_end`) are written by the orchestrator or the dispatches themselves, and AC-DISP does not cross-check them. Required fix: AC-4.4 (or AC-DISP) asserts every `Dispatch-Id` in `lib/` commits appears in the S5 dispatch manifest under a developer role, and every validator `Dispatch-Id` appears under a qa role (roles differ). Also include `run_smoke.py` (a named producer file) in the `LIB` path list so one commit cannot touch it and the validator files together; FR-4.4 names it as a producer file but AC-4.4 only checks `lib/`.

**W6 (warning) FR-1.2 BARE_RE / PIN_RE, false positives on legitimate text outside the must-pass floors.** See probe table: `on 6.8 kernels`, `for 5.2 users`, `the new 5.0 release of React`, `the 4.7 uF cap`, `with 4.7 V rail`, `claude-plugins-v2`, `claude-md-2` misfire in both engines. Since no escape exists, each becomes a reword at best, and hardware-team electronics prose is a likely source. The floor names only `4.7uF` (no space). Required fix (choose): add these as `rule_b_must_pass` / `rule_a_must_pass` fixtures and adjust patterns (for example require a model-family word or the word `model`/`version` on the same line for BARE_RE, or extend the COUNT_RE unit list with `V`, `uF`, `kernels`, `users`), or state them in FR-1.2 as accepted false positives with the wording rule as the remedy. Current text claims R4 risk is L; the probes suggest M for hardware-team files.

**W7 (warning) FR-1.2 COUNT_RE noun list gaps and real false negatives.** Missing common count nouns: workers, validators, teams, dispatches, attempts, threads, batches, files, sub-agents (hyphenated), `x`; units `s`, `GiB`, `sprints`. For a repo about dispatching validators, `Opus 3 validators` is a likely legitimate sentence. The wording rule (write `3 Opus validators`) is the workaround, but the floor list should include these classes. Separately, underscore and separator variants (`claude_opus_4_7`, `OPUS_4_7`, tab/NBSP between family and digit, `claude.opus.5`) evade Rule A and B and are not in the accepted-loopholes list. Required fix: add `[ _.-]` and `[[:space:]]` tolerance to PROSE_RE separators (`[ _-]*` and POSIX-safe whitespace) and add `claude_opus_4_7`/`OPUS_4_7` to `rule_a_must_hit`, or list them as accepted loopholes in FR-1.2.

**W8 (warning) Section 5, orphan ACs.** AC-4.2, AC-4.3 (G4/G-LIT contributors), AC-5.1, AC-5.2, AC-5.3, AC-5.4, AC-5.6 and AC-2.2 are not named in any gate's closing-AC list, so passing a gate does not require them (AC-5.4, cost mean above 0, is one the G5 story most needs). Required fix: add them to the closing-AC column of G4/G-LIT and G5 (S5) and G7 (AC-2.2), keeping one closing story per gate. Also AC-4.4 is written in the S4 section but is evaluated at S5; note that in the gate row (it is already in G5, which is fine).

**W9 (warning) AC-1.5 / AC-1.2b / AC-5.10, string-presence ACs and self-declared provenance.** AC-1.5 greps for `check_model_pins.py --paths` and `MODEL_PIN_STRICT` in the hook; both could sit in a comment, and advisory-versus-strict behaviour is untested. AC-1.2b `grep -c check_model_pins.py` in the workflow can be met by a comment (AC-1.1b's `in t` check has the same limit). AC-5.10 requires `claude_code_version` and `command` keys in the sidecar but not that the fixture is a real capture (a hand-nested stream passes); provenance is self-reported. Required fix: add a behavioural check for the hook (run it in a temp git repo with a staged file containing a pin: exit 0 by default, exit 1 with `MODEL_PIN_STRICT=1`); require the workflow line to be a `run:` step (parse `run:` lines); require in AC-5.10 that the sidecar `command` contains `--output-format stream-json` and that the fixture `session_id` in init equals a session id in the sidecar, and record the honest forgery limit as in AC-5.5c.

## Positive observations

- Canonical command, AC snippets and negative self-tests are self-contained and reproduce today-values.
- Round-1 blockers (must-pass floors, QA-probed false positives, observable separation) are structurally addressed; guard fixtures now have both floors, provenance, and a `synthetic-future` executable NFR-11 check.
- Fails-loudly design for `unknown`/empty is enforced at capture time with raw-stream corroboration, not only JSON shape.

## Result

STATUS DONE. Address W1 to W9 in the Stage 2 revision if cheap; none block Stage 3.
