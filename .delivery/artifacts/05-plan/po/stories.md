# Stories: Fix PR #88 failing CI checks (BUG_FIX, LIGHT)

Consolidation note: stories are grouped by file scope. Story 1 touches only `delivery-flow/SKILL.md` plus one new reference file and `manifest.yml` (one dev unit, one commit). Story 2 touches only `smoke-test-architecture.md` (one-line change). Story 3 touches no repo files (PR metadata text only). No further split or merge is warranted.

All commands run from repo root, using GNU grep (not ugrep; ugrep breaks `\b`). Dev DoD: run each command, do not just read it.

## Story 1: Bring delivery-flow SKILL.md under the Tier-A budget (file scope: delivery-flow SKILL.md, references/)

As a delivery-team maintainer, I want the role-agent-first dispatch text moved out of `delivery-flow/SKILL.md` into a reference file, so that `budget-check` passes without a `Budget-Exception:` and PR behavior is unchanged.

Scope of move (verbatim, no rewording):
- Step 4 first paragraph: the `delivery-<role>` agent list, dispatch via `Agent` tool, fallback to the inline Agent Invocation Template, and the required-fields list.
- Step 4 autonomous-run hand-off paragraph to `delivery-orchestrator`.
- Step 5 "Same role-agent-first rule as Step 4..." sentence.

Destination: new `delivery-team/skills/delivery-flow/references/role-agent-dispatch.md` (chosen over a `pipeline-stages.md` section so pipeline-stages.md stays stable and the file has one purpose). Register it in `references/manifest.yml` with a `purpose:` entry (manifest lists every reference file). SKILL.md keeps a short pointer per step that still tells the orchestrator to prefer `delivery-<role>` agents and names `references/role-agent-dispatch.md`.

Design constraints:
- Net line target: SKILL.md at 497 or fewer (margin of 3+ under 500; a pure pointer swap lands at exactly 500, which is too tight). Main is 499, so the pointers must be net negative versus main, or other lines tightened without semantic loss.
- The PROSE STYLE block injection paragraph, signal block, and Verify signal text stay inline and untouched.
- No claim in repo docs about the reference count needs change unless grep shows one (see TC-1.6).

Acceptance criteria:
- AC-1.1: `python3 scripts/check_skill_budgets.py; echo $?` prints no `BUDGET VIOLATION` and ends with `0`.
- AC-1.2: `wc -l < delivery-team/skills/delivery-flow/SKILL.md` prints a number `<= 497`.
- AC-1.3: `test -f delivery-team/skills/delivery-flow/references/role-agent-dispatch.md && echo ok` prints `ok`.
- AC-1.4: `grep -c "role-agent-dispatch" delivery-team/skills/delivery-flow/SKILL.md` prints `>= 2` (Step 4 and Step 5 pointers), and `grep -c "role-agent-dispatch" delivery-team/skills/delivery-flow/references/manifest.yml` prints `1`.
- AC-1.5: Verbatim preservation. For each of the strings `delivery-developer`, `delivery-presentation`, `delivery-alias-creator`, `delivery-orchestrator`, `Agent Invocation Template`, `role-agent-first`, `grep -c "<string>" delivery-team/skills/delivery-flow/references/role-agent-dispatch.md` prints `>= 1`. Moved paragraphs match the origin/main...HEAD text character for character (compare `git show HEAD:delivery-team/skills/delivery-flow/SKILL.md` lines 333-346 and the Step 5 sentence against the new file body with `diff`; only the file header and whitespace-free wrapping may differ).
- AC-1.6: SKILL.md pointers still instruct role-agent preference: `grep -n "prefer" delivery-team/skills/delivery-flow/SKILL.md` shows a hit within Steps 4 and 5.
- AC-1.7: `python3 scripts/check_skill_budgets.py` output contains no new `KNOWN_DEBT` entry and `git diff origin/main...HEAD -- governance/skill-budgets.json` is empty (no exception path used).
- AC-1.8: `lint` and `header-warn` workflow commands (read `.github/workflows/lint-known-debt.yml` and `.github/workflows/skill-md-header-warn.yml`, run the `run:` commands locally) exit 0 (header-warn: no new warnings for the new reference or SKILL.md).

Test cases:
- TC-1.1: Run AC-1.1; expect exit 0 (was 514/500 violation).
- TC-1.2: `python3 scripts/check_skill_budgets.py | grep delivery-flow`; expect line count shown at most 497 of 500.
- TC-1.3: `diff <(git show origin/main:delivery-team/skills/delivery-flow/SKILL.md | sed -n '1,332p') <(sed -n '1,332p' delivery-team/skills/delivery-flow/SKILL.md)`; expect empty (everything before Step 4 unchanged).
- TC-1.4: Behavior audit: `git diff origin/main...HEAD -- delivery-team/skills/delivery-flow/SKILL.md | grep '^-' | grep -v '^---'` lines removed are all present in the new reference (spot check each removed sentence with `grep -F`).
- TC-1.5: Negative check: `grep -n "delivery-orchestrator" delivery-team/skills/delivery-flow/SKILL.md` still shows a pointer or mention so the hand-off is discoverable from SKILL.md; if it does not, the pointer wording must be extended.
- TC-1.6: `grep -rn "reference files\|references/ (.* files" delivery-team/ARCHITECTURE.md delivery-team/skills/delivery-flow/references/manifest.yml README* 2>/dev/null`; if a numeric file-count claim exists, it is incremented by 1; if none, no doc change.
- TC-1.7: Manifest still parses: `python3 -c "import yaml,sys; yaml.safe_load(open('delivery-team/skills/delivery-flow/references/manifest.yml'))"` exits 0 (skip if PyYAML is absent and use a visual check).

## Story 2: Fix stale model ID in smoke-test architecture doc (file scope: smoke-test-architecture.md)

As a maintainer, I want `claude-sonnet-4-5` at `delivery-team/architecture/smoke-test-architecture.md:116` replaced by canonical `claude-sonnet-4-6`, so that `stale-id-guard` passes. This is a pre-existing defect on main (commit 91e1297) fixed inside PR #88 because it blocks this PR's merge. Provenance marking does not apply (line is inside a JSON block). Do not change the guard.

Consumer check already done at plan time: repo grep for `claude-sonnet-4-5` finds only this fixture line plus `.delivery/` artifacts (prose, excluded by the guard via `':!:.delivery/*'`) and a dated `claude-sonnet-4-5-20250929` in a dev log (also under `.delivery/`). No code or test consumes the fixture value. Dev re-runs the grep before editing.

Acceptance criteria:
- AC-2.1: The FULL guard pipeline from `.github/workflows/stale-model-id-guard.yml` (GNU grep; the `git ls-files ... | xargs grep -En ... | grep -vE ...` chain including the `#` provenance and `>` blockquote filters) is the check. Pre-edit it prints exactly one line, `delivery-team/architecture/smoke-test-architecture.md:116:...claude-sonnet-4-5...`. Post-edit it prints nothing and `HITS` is empty (exit 0). Note: a raw `grep -n "claude-sonnet-4-5"` also matches `agentic-flow-builder/scripts/agent_registry.py:148`, a `#` provenance comment; the guard's `^[^:]+:[^:]+:[[:space:]]*#` filter exempts it, so it is not a hit and must not be edited. Verified 2026-09-18 with GNU grep 3.12: pre-edit output is the single line-116 hit.
- AC-2.2: `sed -n 116p delivery-team/architecture/smoke-test-architecture.md` prints `    {"model": "claude-sonnet-4-6", "dispatches": 5, "input_tokens": 4345, "output_tokens": 2589}` (only the model string differs; the diff is exactly 1 line).
- AC-2.3: The guard pipeline from `.github/workflows/stale-model-id-guard.yml` (the `HITS=$(...)` block, run with GNU grep via a temp script) leaves `HITS` empty and prints `No stale 4.x model IDs found.`
- AC-2.4: `git diff origin/main...HEAD --stat -- delivery-team/architecture/smoke-test-architecture.md` shows 1 insertion, 1 deletion.
- AC-2.5: `git diff origin/main...HEAD -- .github/workflows/stale-model-id-guard.yml` is empty (guard not weakened).

Test cases:
- TC-2.1: Run the guard pipeline before the edit; expect exactly one hit at line 116 (proves the local replica is faithful, and the failing state).
- TC-2.2: Run it after the edit; expect no hits and exit 0.
- TC-2.3: `python3 -c "import json;json.loads('{\"m\":[{\"model\":\"claude-sonnet-4-6\"}]}')"`-style check is unnecessary; instead confirm the surrounding JSON block still has the same structure via `git diff` showing only the model string changed.
- TC-2.4: Run the guard after Story 1 lands too, since the new reference file is `*.md` and in scope; expect no hits (the new file must not contain any 4.x model ID).

## Story 3: PR #88 hygiene text (file scope: none; proposed text only, PR is not edited by this team step)

As a reviewer, I want the PR body to disclose the 7-role SKILL.md rewrite, the CI fixes, and a test plan of checks actually run, so that the diff matches the description.

Proposed PR body additions (fill the checkbox states only after running the commands):

```
## Also in this PR
- Rewrites 7 role SKILL.md files (architect, developer, godot, operations, product-delivery, quality, ui): net deletions, about -170 lines. Intentional: dynamic sub-agent spawning removed from role skills' internal dispatch, since the thin `delivery-<role>` agents are now the execution boundary (see commits bd83591, da2771b).
- Moves the role-agent-first dispatch and `delivery-orchestrator` hand-off text from delivery-flow/SKILL.md into references/role-agent-dispatch.md (verbatim) to fit the Tier-A 500-line budget. No behavior change.
- Fixes a pre-existing main defect: stale `claude-sonnet-4-5` in delivery-team/architecture/smoke-test-architecture.md:116 (introduced in 91e1297) changed to `claude-sonnet-4-6`, needed for stale-id-guard.

## Test plan
- [ ] python3 scripts/check_skill_budgets.py exits 0 (delivery-flow SKILL.md at N/500)
- [ ] stale-model-id-guard grep pipeline (GNU grep) returns no hits
- [ ] lint and header-warn workflow commands pass
- [ ] moved text diffed against origin/main; matches verbatim
- [ ] all 4 required checks green on the PR
```

Acceptance criteria:
- AC-3.1: Proposed text is delivered to the maintainer in the final report; `gh pr view 88 --json body` is unchanged by this step (no PR edit).
- AC-3.2: Each test-plan checkbox is checked only after its command was run in Development; otherwise it is marked PARTIAL with a reason.
- AC-3.3: `git diff origin/main...HEAD --stat | grep -c "SKILL.md"` is consistent with the "7 role SKILL.md files plus delivery-flow" claim (8 SKILL.md files); the maintainer confirms the count before editing the PR.

Test cases:
- TC-3.1: `git diff origin/main...HEAD --stat -- '*/SKILL.md'`; expect 7 role files with net deletions plus delivery-flow.
- TC-3.2: After the maintainer edits the PR, `gh pr view 88 --json body -q .body | grep -c "7 role SKILL.md"` prints `1`.

## Final verification sweep (Development DoD, after all stories)
1. `python3 scripts/check_skill_budgets.py` exit 0.
2. Guard pipeline exit 0 with no hits.
3. lint and header-warn commands exit 0.
4. `git status --short` shows only: delivery-flow/SKILL.md, references/role-agent-dispatch.md, references/manifest.yml, smoke-test-architecture.md (plus `.delivery/` artifacts).

## Open items
- Maintainer decision: keep Fix B in PR #88 (recommended) or split to a separate PR against main.
- Reference filename `role-agent-dispatch.md` is proposed; dev may confirm no naming clash in `references/`.
