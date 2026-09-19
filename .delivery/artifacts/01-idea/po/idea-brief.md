## Idea Brief

**Project Type**: BUG_FIX
**Date**: 2026-09-18
**Source**: PR #88 "Add thin delivery-<role> agents and orchestrator for delivery-team" (branch `delivery-team-agent-wrappers`)

### Problem Statement
Two required CI checks fail on PR #88, blocking merge. Both were re-verified from the repo root.

1. **budget-check (caused by this PR).** `python3 scripts/check_skill_budgets.py` reports `BUDGET VIOLATION: delivery-team/skills/delivery-flow/SKILL.md 514/500 lines (Tier-A)`. The file is 499 lines on origin/main and 514 on the branch. The PR adds the role-agent-first dispatch rule and the `delivery-orchestrator` hand-off text in Step 4 and Step 5. The diff is 21 lines changed in that file (+15 net, +499 to +514). Main sits 1 line under the cap, so the net addition allowed inline is at most 1 line.
2. **stale-id-guard (pre-existing, not caused by this PR).** `delivery-team/architecture/smoke-test-architecture.md:116` contains `{"model": "claude-sonnet-4-5", ...}` inside a JSON example. It was introduced in commit 91e1297 (BACKLOG-106) and exists on origin/main. The PR does not touch the file. `.github/workflows/stale-model-id-guard.yml` allowlists `claude-opus-4-7`, `claude-sonnet-4-6` and `claude-haiku-4-5-20251001`. It exempts lines whose content starts with `#` or `>`. The JSON line at 116 starts with `{`, so neither exemption applies.

Passing checks that must stay passing: `lint`, `header-warn`.

Secondary observations (hygiene, not CI failures):
- The PR body test plan is unchecked.
- The PR rewrites 7 role SKILL.md files (architect, developer, godot, operations, product-delivery, quality, ui; net deletions, about -170 lines). The title and summary do not mention this. Reviewers cannot tell it is intentional.

### Target Users
- PR #88 author and maintainer (Michael Connelly): needs green CI to merge.
- Delivery-team contributors: need `delivery-flow` SKILL.md to stay within its Tier-A budget and CI guards to be trustworthy.
- Reviewers: need the PR description to match the diff.

### Goals
1. `python3 scripts/check_skill_budgets.py` exits 0 with `delivery-flow/SKILL.md` at 500 lines or fewer. Target is 499 or fewer plus a short pointer, no `Budget-Exception:` line.
2. The stale-id-guard step of `stale-model-id-guard.yml` exits clean on the branch, replicating the workflow's grep pipeline locally.
3. The role-agent-first dispatch semantics (Step 4, Step 5) and the `delivery-orchestrator` hand-off text are preserved verbatim in their new location. PR behavior is unchanged.
4. `lint` and `header-warn` remain green.
5. The PR body test plan is updated with checks actually run, and the 7-role SKILL.md rewrite is disclosed in the summary.

### Constraints
- Do not change PR behavior. The moved text must be verbatim: the `delivery-<role>` agent list, the fallback to the inline Agent Invocation Template, and the autonomous-run hand-off to `delivery-orchestrator`.
- The inline pointer in Step 4/5 must be about 1 net line or fewer, or else other lines must be tightened, because main is at 499/500. The pointer must still tell the orchestrator to prefer role agents.
- Tier-A cap is 500 lines (`governance/skill-budgets.json`). `Budget-Exception:` in the PR body is the disfavored path. It needs a `known_debt[]` entry with `target_wave:`.
- No `claude` CLI in CI (memory: `feedback_claude_code_local_only`). Verification uses only grep and python.
- Follow the config, ADR and reference conventions of the repo: allowlist-over-deny for model-ID guards, and the `#` provenance exemption that goes with ADR-002. Do not weaken the guard.
- Lessons applied: the Developer DoD must run every named command from repo root, not just read it. Verify before editing. Use honest readiness markers (PARTIAL where a step was not executed).

### Initial Scope
**Fix A, budget (in PR #88).** Move the Step 4 role-agent-first dispatch paragraph and the Step 5 addendum, plus the orchestrator hand-off paragraph, into a `references/` file. Candidate: a new `delivery-team/skills/delivery-flow/references/role-agent-dispatch.md`, or a section in `pipeline-stages.md`. Leave a short pointer in SKILL.md. Re-run `check_skill_budgets.py`. If the new reference is registered anywhere (manifest.yml or reference indexes), update it.

**Fix B, stale ID (recommendation).** The occurrence is a fabricated sample-data value in a JSON example, not provenance. Recommended fix: change the value to canonical `claude-sonnet-4-6`. The example is an illustrative model_usage record, so nothing depends on the old string. A quick grep for other consumers of that fixture is required before editing. Provenance marking (`#` or `>`) does not fit, because the line is inside a JSON code block and a `#` prefix would break the JSON. Belongs in PR #88: the failing check blocks this PR's merge, and the fix is a one-line, zero-risk change. Splitting it into a separate PR would leave #88 red until that one lands. The PR description should call the fix out as a pre-existing main defect. The alternative (a separate PR against main, then rebase) is acceptable only if the maintainer prefers a clean history, and is decided by the maintainer, not the team.

**Fix C, PR hygiene.** Update the PR title or summary to state the 7-role SKILL.md rewrite, and check off test-plan items only after running them.

**Verification (must run, from repo root):**
- `python3 scripts/check_skill_budgets.py`
- the guard's grep pipeline from `.github/workflows/stale-model-id-guard.yml`, run locally
- `git diff origin/main...HEAD` on delivery-flow SKILL.md, to confirm the moved text matches character for character
- the lint and header-warn commands, per the workflows

### Out of Scope (initial)
- Refactoring other role SKILL.md files or re-litigating the 7-role rewrite content.
- Raising the Tier-A budget or adding a `known_debt[]` exception (only if the reference move proves infeasible).
- Changing the stale-model-id-guard allowlist or logic.
- Auditing other stale model IDs elsewhere in the repo, unless the local guard run surfaces them.
- Any change to delivery-orchestrator or role-agent behavior, or any CI that shells out to `claude`.
- Stages 2 to 4 (refine, design, architect) are skipped for this bug fix, per `.delivery/state.md`.

### Risks and Open Questions
- A new reference file may itself trip other checks (lint, header-warn). Run them after the change.
- Whether the reference-file location fits the existing Level-3 conventions. The Plan stage should pick the file name and confirm.
- Whether any other file in the repo consumes the `claude-sonnet-4-5` fixture value. Check with grep before changing it.
