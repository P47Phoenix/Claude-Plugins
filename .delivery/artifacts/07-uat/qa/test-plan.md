<!-- run: run-2026-09-18-pr88 -->
# UAT Test Plan: PR #88 CI fixes (BUG_FIX, LIGHT)

Acceptance source: stories.md (Story 1 budget, Story 2 stale ID, Story 3 PR text) + idea brief. No PRD.
Env: uncommitted working tree on branch delivery-team-agent-wrappers, worktree pr88. Each CI workflow `run:` command replayed locally. Guard replica run via `bash` with /usr/bin/grep (GNU). Note: the interactive shell aliases `grep` to ugrep; replica script run in fresh bash, unaffected.

## 1. Test plan

Scope: 4 CI checks + story ACs. Risk order: budget-check (P0, was failing) > stale-id-guard (P0, was failing) > lint/header-warn (regression guards) > behavior preservation of moved text.
Entry: Dev DoD 3/3 done, working tree has changes. Exit: all CI-equivalent commands exit 0, no verbatim-loss, no new defects caused by PR.
Assumptions: (a) CI runs on merge-ref of commit; uncommitted tree is a proxy, so real CI still needed after commit. (b) `origin/main` ref not fetched locally; `HEAD` (f4fea7d parent chain, = main content for these files) used as baseline. (c) Guard uses `git ls-files`, so untracked new reference file is skipped locally AND until `git add`; scanned manually.

## 2. Executed test cases

| ID | Check / command | Expected | Actual | Result |
|---|---|---|---|---|
| CI-1 budget-check | `python3 scripts/check_skill_budgets.py` | exit 0, no violation | `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` exit=0 | PASS |
| CI-1b permissive scan (warn-only) | `--warn-permissive` | never blocks | prints PERMISSIVE-LANGUAGE warnings (user-feedback etc., unrelated files); `|| true` in workflow | PASS (warn) |
| CI-2 stale-id-guard | workflow HITS pipeline, GNU grep, temp script | no hits, exit 0 | `No stale 4.x model IDs found.` exit=0 | PASS |
| CI-2b untracked new file | `grep -En 'claude-(opus\|sonnet\|haiku)-4[-.]' references/role-agent-dispatch.md` | no match | no match (grep exit 1) | PASS |
| CI-3 lint | `python3 scripts/lint_known_debt.py` | exit 0 | `LINT OK: known_debt JSON-Python in sync; all SKILL.md frontmatter complete.` exit=0 | PASS |
| CI-4 header-warn | `git ls-files '*SKILL.md' ':!:.delivery/*' \| xargs grep -L model_awareness:` | continue-on-error, warn only | 9 files listed (4 user-feedback personas, 5 research-agent types). None touched by PR; delivery-flow SKILL.md not listed | PASS (pre-existing warn, non-blocking) |
| AC-1.2 | `wc -l < SKILL.md` | <=497 | 497 (was 514) | PASS |
| AC-1.3 | reference file exists | ok | exists | PASS |
| AC-1.4 | pointer count | SKILL.md >=2, manifest =1 | 2 and 1 | PASS |
| AC-1.5 | verbatim strings in reference | each >=1 | developer 1, presentation 1, alias-creator 1, orchestrator 2, Invocation Template 1, role-agent-first 2 | PASS |
| AC-1.5b | moved paragraphs vs HEAD SKILL.md | char-for-char | Read side-by-side of `git diff`: removed text present in reference; Step 4 fields/roles intact; wrapping of one line differs (whitespace only) | PASS |
| AC-1.6 | "prefer" in Steps 4 and 5 | hit each | SKILL.md:335 and :368 | PASS |
| AC-1.7 | governance/skill-budgets.json + workflows diff | empty | empty | PASS |
| TC-1.3 | diff lines 1-332 vs HEAD | empty | identical | PASS |
| TC-1.5 | `delivery-orchestrator` in SKILL.md | present | SKILL.md:336 | PASS |
| TC-1.6 | numeric ref-count claims | +1 if any | SKILL.md:459 says 24 files; manifest self-entry says 24; manifest has 24 `- file:` rows. Consistent | PASS |
| TC-1.7 | manifest YAML parse | exit 0 | ScannerError line 49 col 29; SAME error on HEAD version | FAIL-PREEXISTING (DEFECT-008) |
| AC-2.2/2.4 | smoke-test-architecture diff | 1 line, model string only | +1/-1 at line 116, sonnet-4-5 -> 4-6 | PASS |
| AC-2.5 | guard workflow unchanged | empty diff | empty | PASS |
| NEG-1 | negative: reintroduce check - pre-edit hit was single line 116 | n/a | post-edit zero hits proves the filter chain does not mask (agent_registry.py:148 `#` comment exempt by design) | PASS |
| AC-3.x | Story 3 PR text | no PR edit | not testable locally; PR body untouched by this step | N/A |

## 3. Exploratory session (Cross-Story Interaction)

Charter: Explore Story 1 (moved dispatch text) x Story 2 (doc edit) x agents/hooks/scripts using HICCUPPS (Claims, Comparable product, History) to discover whether moving text out of SKILL.md broke any pointer, anchor or link. Time-box: 30 min. Tour: dependency tour.

Observations:
1. Reachability: SKILL.md Step 4 (line 335-336) and Step 5 (368-369) name `references/role-agent-dispatch.md`; manifest row registered (line 106). Orchestrator hand-off discoverable from Step 4 pointer. OK.
2. `delivery-team/agents/delivery-orchestrator.md` refs Steps 4, 5, 7, 4.5 and "Agent Invocation Template" by name only, no line numbers. Steps still exist with same headings. OK. Its Step 4 semantic text now lives one hop away; orchestrator must follow pointer (same as any reference). Minor note, not defect.
3. Old anchors: grep of hooks/, scripts/, .claude-plugin/, governance/, delivery-team/ for moved text or SKILL.md line numbers found only `architecture/sub-agent-dispatch.md:51` ("SKILL.md line 699", already wrong vs 497-line file) -> DEFECT-009, pre-existing.
4. Relative links in new file: `references/pipeline-stages.md` (exists, relative to skill dir, same as original SKILL context) and `agents/` (relative to plugin root; copied verbatim, was same in SKILL.md). Text is written from SKILL.md's viewpoint, so `references/...` is skill-root relative, not file-relative. Resolves per convention; low confusion risk.
5. Step 5 wording is condensed (not verbatim: "Role-agent-first rule as Step 4: prefer..."). Reference retains original full sentence. Meaning identical. Step 5 line 368 is now over-long (long line) - cosmetic.
6. Story 2 x Story 1: new .md is in guard scope only once tracked; scanned manually, clean.
7. `delivery-team/tests/smoke/README.md` references smoke-test-architecture.md; only a doc pointer, fixture value not consumed by code.

No new bugs caused by PR. Two pre-existing defects logged.

## 4. Shared-Module Review <!-- retro c8f2 -->

**Shared modules identified**: 3 (files modified in Dev and referenced by 2+ stage dirs: 05-plan, 06-development, 07-uat)

| Module Path | Stages Referencing | Modified in Dev | Test Coverage | Status |
|---|---|---|---|---|
| delivery-team/skills/delivery-flow/SKILL.md | 05, 06, 07 | Yes | CI-1, CI-3, CI-4, AC-1.x, TC-1.3, exploratory 1-3 | PASS |
| delivery-team/skills/delivery-flow/references/manifest.yml | 05, 06, 07 | Yes | AC-1.4, TC-1.6, TC-1.7 (pre-existing parse fail) | PASS with note |
| delivery-team/architecture/smoke-test-architecture.md | 05, 06, 07 | Yes | CI-2, AC-2.x | PASS |

New file references/role-agent-dispatch.md: also referenced in 3 stages, new; covered by AC-1.5, CI-2b.
Consumers (grep, excl. .delivery): SKILL.md is consumed by delivery-orchestrator agent (by step name), scripts/check_skill_budgets.py + lint_known_debt.py + governance/skill-budgets.json (line-count only), CI workflows. manifest.yml consumed by SKILL.md count claim only; no code parses it. smoke-test-architecture.md consumed by tests/smoke/README.md (link only).
**Findings**: every consumer context exercised; no assumption broken. Dev DoD 16/16 ACs corroborated.

## 5. Verdict: GO_WITH_NOTES

All 4 CI checks reproduce green locally against the working tree; behavior of moved text preserved.

Residual risks / notes:
- Nothing is committed. Local pass is a proxy; real CI must be green after commit/push (guard's `git ls-files` only sees the new reference once `git add`ed; ensure it is added or SKILL.md pointer dangles).
- manifest.yml line-49 YAML parse error pre-exists on main (DEFECT-008); story TC-1.7 unmeetable; separate fix.
- governance/cache-prefix-hash.txt stale (whole-file hash 43067c...; prefix hash 8c2e... unchanged by PR). Pre-existing (DEFECT-009).
- header-warn lists 9 SKILL.md without model_awareness: warn-only, unrelated.
- PR-body test-plan checkboxes (Story 3, "all 4 required checks green on the PR", verbatim diff vs origin/main) need a live PR run/dogfood and maintainer edit; not possible here. origin/main not fetched; HEAD used as baseline.
- Behavioral risk: orchestrator now needs one extra file read for dispatch detail; not dogfooded with a live pipeline run.
