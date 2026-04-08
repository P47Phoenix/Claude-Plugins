# Release Plan: Orchestration Discipline Bundle (v2.7)

**Stage**: 07 — UAT (DevOps)
**DevOps**: Samwise Gamgee
**Bundle**: Orchestration Discipline (OD-01..OD-13), schema v2.6 -> v2.7
**Branch**: `feature/orchestration-discipline-bundle`
**Closes**: #73, #71, #70, #69
**Marketplace version bump**: `2.17.1` -> `2.18.0`

> *"Now that's a proper send-off, Mr. Frodo. Pack the lembas, double-knot the laces, and look back once at the door before you go — just to be sure it's still there when we come home."*

---

## 1. Pre-Release Checklist

Run top to bottom. Every box must be ticked before a single commit is pushed to the remote.

### 1.1 Local working tree

- [ ] `git status` clean except for the OD bundle edits — no stray untracked files outside the bundle's edit map.
- [ ] On branch `feature/orchestration-discipline-bundle` (created by orchestrator at Dev-stage entry per `auto_branch: true`).
- [ ] Local `main` fast-forwarded; feature branch rebased onto latest `main` exactly once.
- [ ] No accidental edits to files outside the OD-01..OD-13 edit map (compare to `06-dev/developer/OD-all.md` Files-touched lists from Round 1, Round 2, Round 3).

### 1.2 Artifact and content gates

- [ ] All OD-01..OD-13 acceptance criteria green per QA artifacts in `06-dev/quality/`.
- [ ] Round 2 + Round 3 self-correction items closed (D-01, M-01, M-04, M-05, D2-01, D2-02, SKILL.md wizard count).
- [ ] `grep '^### Q' delivery-team/skills/delivery-flow/references/setup-wizard.md` returns exactly nine headers, Q1..Q9 contiguous.
- [ ] `grep -rn "project_type" delivery-team/skills/delivery-flow/` returns only ADR/migration history references — no live config rows.
- [ ] `grep -rn "schema_version: 2.6\|config_version: \"2.6\"" docs/` returns only historical/migration mentions.
- [ ] `grep -rn "9 questions\|9-question\|down from 10"` returns the new wording across CLAUDE.md, README.md, delivery-team/README.md, setup-wizard.md.

### 1.3 Schema and derived artifacts

- [ ] `delivery-team/skills/delivery-flow/references/config-schema.md` Current Version reads `2.7`.
- [ ] `delivery-team/skills/delivery-flow/references/config-schema.json` regenerated via `python3 delivery-team/scripts/generate-schema.py` and committed alongside its source markdown.
- [ ] `.claude-plugin/marketplace.json` version reads `2.18.0`.

### 1.4 Hook syntax + behavior

- [ ] `python3 -m py_compile delivery-team/hooks/enforce_pipeline_scope.py` clean.
- [ ] `python3 -m py_compile delivery-team/hooks/audit_agent_prompt.py` clean.
- [ ] `_activation_gated` confirmed default-OFF for tolerantly-parsed v2.6 configs (manual replay against a scratch v2.6 fixture).
- [ ] `_detect_subagent_origin` Layer 1/Layer 2 manually replayed against three hook-input fixtures (env-var present, parent_tool_use_id present, neither present).
- [ ] `audit_agent_prompt.py` negation guard verified against the "do not act as both X and Y" fixture.

### 1.5 Documentation site

- [ ] Local MkDocs build succeeds: `mkdocs build --strict` (or whatever command the `docs.yml` workflow runs) — no broken links, no missing pages introduced by OD-13's doc parity sweep.
- [ ] `docs/user-guide/config.md`, `docs/skills/delivery-flow.md`, `docs/contributing/index.md` render correctly.

### 1.6 Pipeline self-discipline (dogfood)

- [ ] This very delivery-flow run used one-role-one-subagent dispatch end-to-end. Compound prompts: zero. Self-writes outside the orchestrator allowlist: zero. (NFR-08, OD-04, OD-08.)
- [ ] Retrospective artifact present in `.delivery/` so the SessionStop hook does not block release.

### 1.7 Issue and PR readiness

- [ ] All four issues (#73, #71, #70, #69) still open and assigned to this sprint.
- [ ] Architecture, stories, deploy plan, release plan all linked from the upcoming PR body draft.

---

## 2. Release Steps

The deploy plan committed us to **one commit per story** (12–13 commits) and a **single PR closing all four issues atomically**. We do not deviate.

### Step 2.1 — Final local sanity sweep

```
cd /var/home/meconnelly/Documents/GitHub/Claude-Plugins
git status
git log --oneline main..HEAD
git diff --stat main..HEAD
```

Confirm: 12 or 13 commits ahead of main, file list matches the bundle edit map, no surprises.

### Step 2.2 — Verify commit-per-story discipline

For each commit:

```
git show --stat <sha>
```

Each commit must:

- Touch only the files named in its story's edit map.
- Use a conventional-commits subject (`docs(delivery-flow): …` or `feat(delivery-flow): …`) per the deploy plan §3 commit table.
- Reference its issue with `refs #NN` (NOT `Closes #NN`) — `Closes` is reserved for the PR body.
- Carry the `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>` trailer.

If any commit violates these, **do not amend** (per CLAUDE.md git safety). Instead, create a corrective new commit, or `git reset --soft` the offending range and rebuild it cleanly **only** if the branch has not yet been pushed.

### Step 2.3 — Rebase onto latest main (one time only)

```
git fetch origin
git rebase origin/main
```

Resolve any conflicts (none expected — bundle is mostly net-new content in delivery-flow references and hooks). If conflicts touch the OD edit map, escalate to the Architect before proceeding.

### Step 2.4 — Push the feature branch

```
git push -u origin feature/orchestration-discipline-bundle
```

Per the deploy plan: pushing is the moment the bundle becomes externally visible. Do not push until §1 and §2.1–§2.3 are all green.

### Step 2.5 — Open a draft PR

Use `gh pr create --draft` with the title and body from the deploy plan §4. Title:

```
feat(delivery-flow): orchestration discipline bundle (v2.7)
```

Body (HEREDOC, exactly as in deploy plan §4 "PR body outline"), with `Closes #73`, `Closes #71`, `Closes #70`, `Closes #69` in the body — never in any individual commit.

### Step 2.6 — Watch CI

Wait for `.github/workflows/docs.yml` (MkDocs build) to go green on the PR. This is the only automated gate. If it fails:

1. Read the workflow log via `gh run view --log-failed`.
2. Fix the offending markdown in a new commit (do not amend).
3. Push the new commit. Re-watch CI.

### Step 2.7 — Mark PR ready for review

Once CI is green and §1.6 dogfood proof is recorded as a PR comment:

```
gh pr ready
```

This advances the PR from draft to ready-for-review and triggers the human checkpoint at the UAT stage gate.

### Step 2.8 — Human review checkpoint

The human reviewer must:

- Confirm the PR closes all four issues in its body.
- Confirm the merge method dropdown in the GitHub UI is set to **Merge commit** (NOT squash, NOT rebase). Squash would erase the 12–13-commit history that the deploy plan §3 fought to preserve.
- Click Merge.
- Confirm the feature branch auto-deletes on merge.
- Confirm all four issues auto-close from the PR body's `Closes` keywords.

### Step 2.9 — Announce

Post a one-paragraph release note to the team channel (or commit a `.delivery/release-notes/v2.7-orchestration-discipline.md` if the project uses file-based notes) summarizing:

- Schema v2.7 is live; v2.6 still tolerantly parses.
- `project_type` deprecated, warn-and-drop on next pipeline run.
- `routing.force_type` and `pipeline.enforce_self_write_block` available.
- `enforce_pipeline_scope.py` and `audit_agent_prompt.py` upgraded with discipline detectors.
- Marketplace bumped to `2.18.0`.

---

## 3. Rollback Procedure

Inherits the four-level ladder from the deploy plan §5. This section is the operational playbook — what to actually type and in what order.

### 3.1 Decide which level

| Symptom | Level |
|---|---|
| One story's edits cause a regression, others fine | L1 — single-commit revert |
| All commits tied to one issue regress (e.g. all of #71) | L2 — issue-scoped revert |
| Schema v2.7 itself breaks downstream users | L3 — full-bundle revert via merge commit |
| Revert too slow, users need relief in minutes | L4 — emergency pin notice |

### 3.2 L1 — Single-story revert

```
git checkout main
git pull
git checkout -b hotfix/od-revert-<storyid>
git revert <commit-sha>
git push -u origin hotfix/od-revert-<storyid>
gh pr create --title "fix(delivery-flow): revert <story-id> due to <symptom>" --body "Reverts <sha>. Tracking issue: #<NN>."
```

Watch CI. Merge via merge commit. Notify users in the same channel that announced the original release.

### 3.3 L2 — Issue-scoped revert

Same as L1, but pass multiple SHAs to `git revert`:

```
git revert <sha1> <sha2> <sha3> <sha4>
```

The four SHAs come from the deploy plan §3 commit table, filtered to the affected issue. Reverts are applied newest-first by `git revert` automatically. Resolve any cross-commit conflicts in a single follow-up commit on the same hotfix branch.

### 3.4 L3 — Full bundle revert

```
git checkout main
git pull
git checkout -b hotfix/od-bundle-revert
git revert -m 1 <merge-commit-sha>
git push -u origin hotfix/od-bundle-revert
gh pr create --title "revert: orchestration discipline bundle (v2.7)" --body "Reverts merge commit <sha>. Restores schema v2.6 as live. Reason: <symptom>. Issues #73 #71 #70 #69 will re-open via manual reopen after merge."
```

After merge:

- Manually reopen issues #73, #71, #70, #69 (`gh issue reopen <NN>`) — reverting a merge commit does NOT auto-reopen the issues that the original PR closed.
- Bump `.claude-plugin/marketplace.json` back to `2.17.1` in a follow-up commit on `main` (the revert restores the file content, but the version bump is a deliberate signal to users).
- Re-run rollback rehearsal so the next attempt is informed by the failure.

### 3.5 L4 — Emergency pin notice

When even L3 is too slow:

1. Open `README.md` and add a top-of-file admonition:
   > Users on schema v2.7 experiencing <symptom>: pin `.delivery/config.yml` to `schema_version: "2.6"` and set `pipeline.enforce_self_write_block: false`. v2.6 tolerantly parses any v2.7 keys.
2. Commit and push directly to `main` (this is the one and only time direct-to-main is acceptable, and only because it touches a single doc file).
3. Open a tracking issue describing the incident and link the L3 revert PR that will follow.

### 3.6 Rollback rehearsal (do this BEFORE merging the release PR)

```
git fetch origin
git checkout -b scratch/rollback-rehearsal origin/feature/orchestration-discipline-bundle
git merge --no-ff --no-commit main          # simulate the merge that's about to happen
# manually craft the merge commit, note its SHA, then:
git revert -m 1 HEAD --no-commit
git status                                   # confirm clean revert, no conflicts
git reset --hard origin/main                 # discard the rehearsal
git checkout feature/orchestration-discipline-bundle
git branch -D scratch/rollback-rehearsal
```

If the dry-run revert had conflicts, fix them in the source branch BEFORE merging the release PR. Five minutes here saves an unrecoverable afternoon — that's a Gaffer-grade truth.

---

## 4. Post-Release Verification

Run within thirty minutes of merge. None of these are optional.

### 4.1 GitHub state

- [ ] PR shows merged with **merge commit** method (check the PR timeline icon — should be a purple merge icon, not the squash icon).
- [ ] Feature branch deleted (`gh api repos/:owner/:repo/branches/feature/orchestration-discipline-bundle` returns 404).
- [ ] Issues #73, #71, #70, #69 all show CLOSED status with the PR linked as the closer.
- [ ] `git log --oneline main` on a fresh clone shows the 12–13 OD commits in their original execution order, plus the merge commit at the tip.

### 4.2 CI / docs site

- [ ] `.github/workflows/docs.yml` ran on `main` post-merge and is green.
- [ ] MkDocs site (if hosted) reflects v2.7: `docs/user-guide/config.md` shows the new schema version banner; deprecated `project_type` row absent from the live page.

### 4.3 Schema parity

```
grep -rn "schema_version\|config_version" delivery-team/skills/delivery-flow/references/config-schema.md
grep -rn "\"2.7\"" delivery-team/skills/delivery-flow/references/config-schema.json
grep -rn "2.18.0" .claude-plugin/marketplace.json
```

All three should return the v2.7 / 2.18.0 hits.

### 4.4 Hook smoke test

On a clean clone of `main` post-merge:

```
python3 -m py_compile delivery-team/hooks/enforce_pipeline_scope.py
python3 -m py_compile delivery-team/hooks/audit_agent_prompt.py
```

Then replay the three hook fixtures from §1.4 against the merged hooks. All three must produce the expected behavior:

- Layer 1 env-var fixture: pass-through, no warning.
- Layer 2 metadata fixture: pass-through, no warning.
- Neither layer + artifact write under `.delivery/artifacts/**` + activation gate ON: emit Delegation Prime Directive systemMessage, exit 0 (soft-deny).

Negation fixture for `audit_agent_prompt.py`: "do not act as both X and Y" must NOT trigger the compound-role warning.

### 4.5 Dogfood the next pipeline run

The first delivery-flow invocation after merge is the real verification. Watch for:

- [ ] Phase 1 detection runs (no `project_type` skip).
- [ ] Tolerant warn-and-drop banner appears if a v2.6 `project_type` is still in `.delivery/config.yml`.
- [ ] No compound-role agent prompts emitted by the orchestrator (`audit_agent_prompt.py` warnings = 0 in normal use).
- [ ] No orchestrator self-writes outside the allowlist (`enforce_pipeline_scope.py` soft-deny systemMessages = 0 in normal use).
- [ ] If Stage 4 runs, the Isolated Adversarial Loop pattern is used (fresh sub-agent per loop).

### 4.6 User-facing follow-up

- [ ] Release note posted (per Step 2.9).
- [ ] Tracking issue opened for the known follow-ups documented in `06-dev/developer/OD-all.md` §"Known follow-ups" (Bash redirection bypass; centralized sub-agent dispatch wrapper). These do NOT block release — they are the next sprint's grist.
- [ ] Defect log in `.delivery/defects/` reviewed; any new defects auto-logged from this release flow get prioritized in the next planning round.

### 4.7 Memory write-back

- [ ] Self-learning memory updated in `.delivery/memory/` with one tier-3 chunk capturing the lesson "schema bumps ship as merge-commit PRs to preserve story-level history". Future releases inherit the discipline.

---

## 5. Sign-Off

When §4 is fully ticked, DevOps signs off in `.delivery/state.md` with:

```
Release sign-off: Orchestration Discipline Bundle v2.7 — DevOps (Samwise Gamgee), <ISO timestamp>
```

And the bundle is done. Properly done. Boots off, kettle on.

---

*"That's the end of the road for this parcel, Mr. Frodo. Schema v2.7 sits in its little house on the hill, the door's locked, the key's under the mat where the next gardener can find it, and there's still a bit of daylight left for second breakfast."*

— Samwise Gamgee, DevOps
