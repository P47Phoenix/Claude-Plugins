<!-- run: run-2026-09-18-pr88 | stage: 07-uat | role: DevOps | task_type: release-plan -->

# Release Plan: PR #88 CI fixes (branch delivery-team-agent-wrappers)

Small change. Two source fixes, one PR text edit. Nothing committed yet. Project rule: commit and push only after user approves. All commands below are proposals, not executed.

## 1. Files to stage

Source (4 files, the actual CI fixes):

| File | Change |
|------|--------|
| `delivery-team/skills/delivery-flow/SKILL.md` | 514 to 497 lines (budget-check fix) |
| `delivery-team/skills/delivery-flow/references/role-agent-dispatch.md` | NEW, verbatim moved dispatch text |
| `delivery-team/skills/delivery-flow/references/manifest.yml` | register new reference (23 to 24) |
| `delivery-team/architecture/smoke-test-architecture.md` | line 116 `claude-sonnet-4-5` to `claude-sonnet-4-6` (stale-id-guard fix) |

Pipeline artifacts (`.delivery/`, tracked in this repo): 14 modified plus 6 new files under `.delivery/artifacts/01-idea`, `05-plan`, `06-development`, `07-uat`, and `.delivery/state.md`. Commit them, because the repo tracks `.delivery/` as the pipeline record (Wave-N precedent). Keep them in a separate commit so the source fix stays revertable and reviewable alone. Stage by explicit path, never `git add -A`.

## 2. Commits (proposed, do not run)

Commit 1, source:
```
fix(delivery-team): fix PR #88 CI (skill budget, stale model id)

Move role-agent-first dispatch text out of delivery-flow/SKILL.md into
references/role-agent-dispatch.md (verbatim, 514 -> 497 lines, under the
Tier-A 500 budget, no exception). Register it in manifest.yml.
Replace stale claude-sonnet-4-5 with claude-sonnet-4-6 in
smoke-test-architecture.md:116 to satisfy stale-model-id-guard.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_017gPgRHE5TGNyvvfHrQDP8G
```

Commit 2, pipeline records:
```
chore(delivery): record run-2026-09-18-pr88 pipeline artifacts

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_017gPgRHE5TGNyvvfHrQDP8G
```

Optional split: put the stale-id line in its own `fix(delivery-team): update stale model id in smoke-test architecture doc` commit. That makes it cherry-pickable to main (see section 5). Recommended, costs nothing.

## 3. Pre-push checks (local)

1. `python3 scripts/check_skill_budgets.py; echo $?` expect exit 0, no BUDGET VIOLATION.
2. Stale-id guard pipeline from `.github/workflows/stale-model-id-guard.yml` (GNU grep, not ugrep) expect no hits.
3. Run `lint` and `header-warn` workflow `run:` commands, expect exit 0.
4. `git status --short` shows only the files listed in section 1.

## 4. Verify CI after push (only after user approves push)

- `git push` (tracks origin, no force).
- `gh pr checks 88 --watch` until all 4 required checks are green: budget-check, stale-id-guard, lint, header-warn.
- If any red: `gh run view <id> --log-failed`, fix forward with a new commit. No amend, no force push.
- Note: `manifest.yml` line 49 YAML parse error pre-exists on origin/main and was not fixed here. Watch that no check newly trips on it.

## 5. Risk: stale-id fix unrelated to PR

Real. The stale id came from commit 91e1297 already on main, so main's guard also fails. Fixing it inside PR #88 is pragmatic (it blocks merge) but mixes an unrelated fix into a review-scoped PR.

Options:
- A (recommended): keep in PR #88, in its own commit, disclosed in PR body. Fast, one merge.
- B: separate PR to main with the one-line fix (`git cherry-pick <sha>` onto a branch off main). Then rebase PR #88 onto main. Cleaner history and heals main immediately, costs an extra PR and a wait.
- Conflict risk if B is chosen: none expected, identical one-line change; git drops the duplicate on rebase.

Maintainer decision needed (also open item in stories.md). Default A unless told otherwise.

## 6. Rollback

- Source commit: `git revert <commit-1-sha>` restores SKILL.md at 514 lines and removes the new reference. This re-breaks budget-check, so a revert is only for a bad behavior change, not a clean fallback.
- Artifacts commit: `git revert <commit-2-sha>`. Harmless, docs only.
- Stale-id commit alone: `git revert <sha>` restores the stale id; guard fails again.
- Pre-merge: simplest rollback is a revert commit pushed to the branch. No force push, no history rewrite.
- No DB, config, infra, or workflow files touched. Guard and budget config unchanged (`governance/skill-budgets.json` and stale-id workflow diffs are empty). Revert time under a minute.

## 7. PR body edit (Story 3 text, proposed, PR not edited by this step)

Apply with `gh pr edit 88 --body-file <file>` only after approval. Append to the existing body:

```
## Also in this PR
- Rewrites 7 role SKILL.md files (architect, developer, godot, operations, product-delivery, quality, ui): net deletions, about -170 lines. Intentional: dynamic sub-agent spawning removed from role skills' internal dispatch, since the thin `delivery-<role>` agents are now the execution boundary (see commits bd83591, da2771b).
- Moves the role-agent-first dispatch and `delivery-orchestrator` hand-off text from delivery-flow/SKILL.md into references/role-agent-dispatch.md (verbatim) to fit the Tier-A 500-line budget. No behavior change.
- Fixes a pre-existing main defect: stale `claude-sonnet-4-5` in delivery-team/architecture/smoke-test-architecture.md:116 (introduced in 91e1297) changed to `claude-sonnet-4-6`, needed for stale-id-guard.

## Test plan
- [x] python3 scripts/check_skill_budgets.py exits 0 (delivery-flow SKILL.md at 497/500)
- [x] stale-model-id-guard grep pipeline (GNU grep) returns no hits
- [x] lint and header-warn workflow commands pass
- [x] moved text diffed against origin/main; matches verbatim
- [ ] all 4 required checks green on the PR (tick after `gh pr checks 88`)
```

Tick boxes 1-4 only if Stage 6/7 QA evidence confirms them (QA reported 16/16 ACs). Confirm the "7 role SKILL.md files" count with `git diff origin/main...HEAD --stat -- '*/SKILL.md'` before editing.

## Trade-offs

| Decision | Alternative | Why |
|----------|-------------|-----|
| Two commits (source, artifacts) | One commit | Source fix revertable alone; artifacts are noise for reviewers |
| Fix stale id in PR | Separate PR to main | Blocks this merge; separate commit keeps option B open |
| Revert, no reset or force push | reset | Non-destructive, safe on shared branch |

## Assumptions

- Branch tracks origin; no other pushes landed since last fetch (run `git fetch` and `git status -sb` first).
- GNU grep available locally for the guard replica.

## Risks

- Reviewer confusion from mixed-scope PR: mitigated by PR body disclosure and separate commit.
- Hidden CI failure beyond the 2 known: mitigated by watching all 4 required checks; fix forward.
- Pre-existing manifest.yml parse error could surface in a check: low likelihood, exists on main already.

## Open questions

- Keep stale-id fix in PR #88 (default) or split to a PR against main?
- User approval required before any commit, push, or PR body edit.
