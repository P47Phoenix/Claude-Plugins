# Release Plan: Model-ID Migration on PR #88

SKILL_LOADED: delivery-team:operations
Role: DevOps / Release | Task: release-plan | Branch: delivery-team-agent-wrappers (origin at 337edb5)

Status: PLAN ONLY. Nothing staged, committed, or pushed. Repo rule: commit and push only with explicit user approval.

## 1. Files to stage

### Commit A (shipping, atomic) - 7 source files
1. `.github/workflows/stale-model-id-guard.yml` (guard allowlist per ADR-models-001)
2. `CHANGELOG.md`
3. `agentic-flow-builder/scripts/agent_registry.py` (literals)
4. `delivery-team/architecture/smoke-test-architecture.md` (literals)
5. `delivery-team/references/telemetry-schema.md` (literals)
6. `delivery-team/tests/smoke/tests/conftest.py` (fixtures)
7. `prompt-engineer/SKILL.md` (literals)

Stage by explicit path. Never `git add -A` (worktree has many unrelated modified files).

### Commit B (chore) - pipeline records
- `.delivery/state.md`, `.delivery/state-archive/`
- `.delivery/artifacts/**` (modified 01-idea..07-uat files plus new: `04-architect/adrs/ADR-models-001-guard-allowlist.md`, `06-development/{dev,developer/us-1.md,po,qa}`)
- `.delivery/backlog/BACKLOG-108-SUPERSEDED.md`, `BACKLOG-109-model-awareness-stamp-audit.md`, `BACKLOG-110-cache-prefix-hash-drift.md`, `BACKLOG-111-smoke-harness-live-baseline.md`, `BACKLOG-112-fable-adoption-conditional.md`
- `.delivery/defects/` (DEFECT-001..009 + index.md; stage only those changed or untracked per `git status`)

Pre-stage check: `git status --short` and `git diff --cached --stat` must show exactly the intended set. Anything outside both lists stays unstaged.

## 2. Commit split and messages (proposed, do NOT run)

Order: A first, then B. Reason: A is the revert unit; B is inert docs.

Commit A:
```
fix(models): migrate stale model IDs and update guard allowlist

Replace stale model-ID literals in agent_registry.py, smoke-test docs,
telemetry schema, conftest fixtures and prompt-engineer SKILL.md with
canonical IDs. Update stale-model-id-guard allowlist per
ADR-models-001. Add CHANGELOG entry.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_017gPgRHE5TGNyvvfHrQDP8G
```

Commit B:
```
chore: delivery pipeline artifacts for model-ID migration

Stage summaries, DoD reviews, ADR-models-001, backlog items 108-112,
defect log and state for the model-ID migration run.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_017gPgRHE5TGNyvvfHrQDP8G
```

Alternative rejected: one big commit. Mixes revert unit with records; a revert would drop the audit trail.

## 3. CI verification after push (needs user-approved push)

- `gh pr checks 88 --watch` then `gh pr checks 88`.
- Guard workflow `on.pull_request.paths`: `**/*.py`, `**/*.md`, `**/*.yml`, `**/*.yaml`, `**/*.json`, `**/*.txt`, `**/*.sh`, excluding `!.delivery/**`. Commit A touches .py/.md/.yml so it triggers. Commit B alone would NOT trigger it. Path filters evaluate against the whole PR diff, so the guard will run on the PR regardless once A is in.
- Expect green: `Stale model-ID guard`, `skill-line-budget` (prompt-engineer/SKILL.md edited; confirm within budget), `workflow-injection-lint` (workflow file edited; confirm no `${{ github.event.* }}` in `run:`).
- If guard is red: read the failing log, fix forward in a new commit (with approval), do not force-push.
- Local pre-push sanity (read-only): run the guard's scan step locally, and `python scripts/check_skill_budgets.py`.

## 4. Rollback

- Single unit: `git revert <commit-A-sha>` (new revert commit, safe on shared PR branch). Restores old guard plus old literals together, so guard and literals stay consistent. Needs approval to run and push.
- Never revert the guard alone: old literals + new guard, or new literals + old guard, may fail CI.
- Commit B needs no rollback (docs only). Revert optional.
- If PR already merged: revert on main via a new PR; same single SHA (or merge commit with `-m 1`).
- No runtime, data, or deploy impact: plugin markdown, one Python registry, test fixtures, CI config. Rollback risk low; RTO = one push plus one CI cycle.

## 5. PR #88 scope interplay

- This rides the branch the user asked for. It grows PR #88 beyond "agent wrappers" (CI fixes already added by 337edb5). Reviewer surface grows by 7 files.
- Option 1 (recommended if user wants PR green now): ride PR #88. The model-ID guard is likely what is failing/gating this PR, so it is coupled.
- Option 2: separate PR from a branch off main, cherry-pick commit A. Cleaner scope, but PR #88 stays red if it depends on the guard fix, and needs a rebase afterward.
- Decision belongs to the user. Default assumption: option 1.

Proposed PR-body addendum:
```
## Addendum: model-ID migration
- Migrates stale model-ID literals (agent_registry.py, smoke-test docs,
  telemetry schema, conftest fixtures, prompt-engineer SKILL.md) to
  canonical IDs.
- Updates stale-model-id-guard allowlist per ADR-models-001.
- Adds CHANGELOG entry.
- Pipeline artifacts and backlog items 108-112 in a separate chore commit
  (.delivery/, excluded from the guard).
- Rollback: `git revert` of the single shipping commit restores guard and
  literals together.
```
(Harness attribution footer applies if the PR body is written.)

## 6. Guardrail checks

- No `claude` CLI in CI: verified. The grep of `.github/workflows` for `claude ` found no CLI invocation; the guard is a shell scan step on ubuntu-latest using checkout only. Consistent with the rule that the claude CLI is local-dev only.
- Permission: commit, push, and PR edits require user approval. This plan performed no writes beyond this artifact.

## 7. Risks and open questions

- Risk: unrelated modified files accidentally staged. Mitigation: explicit paths only.
- Risk: guard allowlist too loose or tight; validated by CI run on the PR.
- Open: user picks ride-PR-88 vs separate PR; user approves commits and push.
