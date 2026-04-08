# Deployment Plan: Orchestration Discipline Bundle

**Stage**: 05 — Plan (DevOps sub-flow)
**DevOps**: Samwise Gamgee
**Source Architecture**: `.delivery/artifacts/04-architect/solution/architecture.md`
**Source Stories**: `.delivery/artifacts/05-plan/po/stories.md`
**Branch strategy** (from `.delivery/config.yml`): `github-flow`, `auto_branch: true`

> *"Share and share alike, Mr. Frodo. One basket, one trip down the hill, and nothing left behind in the pantry."*

---

## 1. What "Deployment" Means Here

This is a plugin repository. There is no runtime, no server, no artifact registry. "Deployment" means:

1. A feature branch in git
2. A sequence of commits
3. A single Pull Request on GitHub
4. A squash-or-merge into `main`
5. A documented rollback path via `git revert`

No tags, no release build, no CI deploy pipeline. The only automated gates are whatever GitHub Actions are wired on PR (see `.github/workflows/docs.yml` — MkDocs build check).

---

## 2. Branch Strategy (github-flow)

Per config, we are strict github-flow: short-lived feature branch off `main`, PR back to `main`, delete on merge.

| Item | Value |
|---|---|
| Base branch | `main` |
| Feature branch | `feature/orchestration-discipline-bundle` |
| Lifetime | One sprint (single-sprint target per stories.md capacity declaration) |
| Auto-create | Yes (`git.auto_branch: true`) — orchestrator creates at Development stage entry |
| Protection | None needed beyond repo defaults; no force-push to main |
| Rebase policy | Rebase onto `main` once at PR-open time to keep history linear; avoid mid-sprint rebases to prevent merge churn across the 11 markdown stories |

**Branch naming rationale**: `feature/` prefix matches conventional commit / github-flow norms; the slug names the bundle (not any single issue number) because this branch closes four issues atomically per NFR-08.

---

## 3. Commit Plan

**Decision: one commit per story (13 commits), not one-per-issue and not one bundle commit.**

### Why not one bundle commit

- Hides the dependency order (OD-01 → OD-04 → OD-03 → SKILL.md block → hook → sweep) that Gandalf laid out in the execution order.
- Makes `git bisect` useless if any single story introduces a regression.
- Violates the "granular, reviewable history" norm the repo's recent log already follows (e.g. `35ffd58 fix: replace sys.exit with exceptions... (#65, #66)` — one commit, small scope, multi-issue tag).

### Why not one commit per issue (4 commits)

- Issue #73 alone spans OD-01 through OD-04, which is four stories with real internal ordering. Collapsing them loses that ordering.
- Issue #71 spans OD-05 through OD-08 and includes the hook code change (OD-07, 8 points). Burying 8 points of code under a doc commit is hostile to reviewers.

### Chosen plan: one commit per story, ordered by the execution order in stories.md §Sprint Roll-Up

| # | Commit subject (conventional commits) | Story | Closes / Refs |
|---|---|---|---|
| 1 | `docs(delivery-flow): deprecate project_type in config schema (OD-01)` | OD-01 | refs #73 |
| 2 | `docs(delivery-flow): bump config schema v2.6 -> v2.7 (OD-04)` | OD-04 | refs #73 |
| 3 | `docs(delivery-flow): add routing.force_type opt-in override key (OD-03)` | OD-03 | refs #73 |
| 4 | `docs(delivery-flow): add Delegation Prime Directive and anti-patterns (OD-05)` | OD-05 | refs #71 |
| 5 | `docs(delivery-flow): Phase 1 detection runs per invocation (OD-02)` | OD-02 | refs #73 |
| 6 | `docs(delivery-flow): reject simplicity shortcut in Step 4.5 (OD-06)` | OD-06 | refs #71 |
| 7 | `docs(delivery-flow): enforce one-role-one-subagent dispatch rule (OD-08)` | OD-08 | refs #70 |
| 8 | `docs(delivery-flow): dispatch rules across team-patterns and quality-gates (OD-09)` | OD-09 | refs #70 |
| 9 | `docs(delivery-flow): document Isolated Adversarial Loop pattern (OD-11)` | OD-11 | refs #69 |
| 10 | `docs(delivery-flow): Stage 4 Architect sub-flow uses loop pattern (OD-12)` | OD-12 | refs #69 |
| 11 | `feat(delivery-flow): layered origin detection in enforce_pipeline_scope hook (OD-07)` | OD-07 | refs #71 |
| 12 | `feat(delivery-flow): compound-reviewer-prompt detector in audit_agent_prompt hook (OD-10)` | OD-10 (optional) | refs #70 |
| 13 | `docs: align CLAUDE.md, README.md, marketplace.json, docs/** to v2.7 (OD-13)` | OD-13 | refs #73 #71 #70 #69 |

**Notes on the commit plan**:

- Only the final commit (OD-13) or the PR body closes all four issues; intermediate commits use `refs #NN` so GitHub doesn't close issues early mid-bundle.
- If OD-10 is dropped (named pressure-relief valve per stories.md §Sprint Roll-Up), commit #12 is skipped and the sequence becomes 12 commits.
- Every commit message body ends with the co-author trailer per repo convention.
- Commits touching a hook script (#11, #12) must load `plugin-dev:hook-development` per NFR-07 — DevOps enforces this at pre-commit by refusing to stage hook edits made outside a developer sub-agent run (honor system; no automated check available).
- **Atomicity gate (NFR-08)**: no commit is pushed to the feature branch until the entire sprint is green locally. Early pushes are acceptable only if the feature branch is not yet visible as a draft PR — i.e., the four issues stay open atomically until PR open.

### Staging discipline

Per the root CLAUDE.md git safety rules:

- Never `git add -A` or `git add .` — each commit stages only the files named in the corresponding story's edit map.
- Never amend a previous commit. If a pre-commit hook fails, fix and create a new commit; squash is handled at PR merge.
- Never `--no-verify`.

---

## 4. PR Plan

**Single PR closing all four issues (#73, #71, #70, #69).** This is mandated by NFR-08 (atomic merge) and reaffirmed by stories.md §Sprint Goal.

### PR metadata

| Field | Value |
|---|---|
| Title | `feat(delivery-flow): orchestration discipline bundle (v2.7)` |
| Base | `main` |
| Head | `feature/orchestration-discipline-bundle` |
| Draft first | Yes — open as draft the moment the feature branch has OD-01 committed, so the team can watch CI (docs build) as each commit lands |
| Closes | `Closes #73`, `Closes #71`, `Closes #70`, `Closes #69` (all four, in the PR body, NOT in individual commits) |
| Labels | `delivery-flow`, `discipline`, `schema-bump`, `atomic-merge` |
| Reviewers | Self-review via delivery-flow adversarial review stage; human checkpoint at UAT stage gate before merge |
| Merge strategy | **Merge commit** (not squash) — preserves the 12–13-commit story history and the dependency order in `git log`. Squash would undo the whole point of commit-per-story. |

### PR body outline

```
## Summary
- Bundle of four orchestration discipline fixes: config drift (#73),
  delegation bypass (#71), one-role-one-subagent (#70), adversarial loop
  convergence (#69).
- Schema bumped v2.6 -> v2.7; project_type deprecated; routing.force_type
  added; pipeline.enforce_self_write_block added (default-true, gated).
- Hook: enforce_pipeline_scope.py gains layered origin detection + Bash
  coverage. Optional: audit_agent_prompt.py gains compound-reviewer detector.
- 25 docs pages (MkDocs), CLAUDE.md, README.md, marketplace.json swept for
  parity.

## Traceability
- FRs: 16/16 covered (see stories.md Test Coverage Audit)
- NFRs: 8/8 covered
- ADRs: ADR-001, ADR-002, ADR-003 in architecture.md

## Test plan
- [ ] Manual walkthrough: two-run thought experiment (OD-02-T2)
- [ ] grep gates in OD-13 all clean
- [ ] Hook unit behavior verified via harness replay for Layer 1/2/3 (OD-07)
- [ ] MkDocs build (docs.yml workflow) green
- [ ] Dogfood: this PR's delivery-flow run used sub-agent dispatch end-to-end

Closes #73
Closes #71
Closes #70
Closes #69
```

### PR gates (must be green before merge)

1. MkDocs Material build workflow (`.github/workflows/docs.yml`) — the only automated CI.
2. Human checkpoint at UAT stage (per delivery-flow pipeline).
3. Doc parity grep gates from OD-13 run manually and recorded in the PR conversation.
4. Hook smoke test recorded (manual — no test runner in this repo).

---

## 5. Rollback Plan

Everything in this bundle is git-revertable. Nothing is stateful. There is no database migration, no cache to invalidate, no external service to notify.

### Rollback levels, cheapest to heaviest

| Level | Trigger | Action |
|---|---|---|
| **L1 — Single-story revert** | One story introduces a defect after merge (e.g., OD-07 hook regression bricks a user pipeline) | `git revert <commit-sha>` for just that commit. Push to a new branch, open a hotfix PR. Because the commit plan is one-per-story, this cleanly removes one story's edits without disturbing the others. |
| **L2 — Issue-scoped revert** | A full issue (e.g., all of #71) regresses | `git revert <sha1> <sha2> <sha3> <sha4>` for the four commits tied to that issue (see commit table). One hotfix PR. |
| **L3 — Full bundle revert** | The schema v2.7 bump itself causes widespread breakage for downstream users | `git revert -m 1 <merge-commit-sha>` of the PR merge commit. This rewinds the whole bundle in one shot and restores v2.6 as the live schema. |
| **L4 — Emergency pin** | Revert is too slow and users need relief within minutes | Publish a short README notice instructing users to pin their `.delivery/config.yml` to `schema_version: 2.6` and set `pipeline.enforce_self_write_block: false`. This exploits the activation gating from architecture §2.5 and ADR-001 — the dogfood was deliberately forward-looking for exactly this reason. |

### Hook-specific rollback notes (OD-07, OD-10)

- **OD-07 is the only load-bearing code change.** If it misbehaves, the `try/except → sys.exit(0)` wrapper (NFR-05) means the worst-case user impact is a dropped warning, not a broken pipeline. This raises the revert threshold: prefer a follow-up fix over an L1 revert unless users report actual blocking.
- **OD-10 is non-blocking by construction** (`systemMessage` only, per FR-12 MAY). A revert is essentially cosmetic; fixing forward is almost always cheaper.
- The activation gating (`schema_version >= 2.7` AND `pipeline.enforce_self_write_block: true`) means users on tolerantly-parsed v2.6 configs are untouched by OD-07's deny behavior by default. This is itself a rollback-like escape hatch already baked into the design.

### Schema rollback

- A v2.7 → v2.6 revert via L3 is safe because v2.6 tolerantly parses any stray `routing.force_type` or `pipeline.enforce_self_write_block` keys users may have already added (they become unknown keys, ignored).
- No data migration exists, so there is no "down migration" to run.

### Doc parity rollback

- OD-13's changes to CLAUDE.md, README.md, marketplace.json, and docs/** are pure prose. L3 revert restores them cleanly. The MkDocs site rebuilds on next `docs.yml` run.

### Rollback rehearsal (recommended, not required)

Before merge, DevOps should dry-run `git revert -m 1 <candidate-merge-sha>` locally against a scratch clone of the branch-to-be-merged, confirm the revert applies without conflict, then discard. This is a five-minute sanity check and it has saved more than one Shire from an unrecoverable afternoon.

---

## 6. Deployment Timeline (sprint-local)

| Phase | Actor | Output |
|---|---|---|
| T0 | Orchestrator, Dev-stage entry | `feature/orchestration-discipline-bundle` branch created off `main` |
| T1..T13 | Developer sub-agent per story | 12–13 commits landed locally in execution order |
| T14 | DevOps | Rebase onto latest `main`; push branch; open draft PR |
| T15 | Delivery-flow UAT stage + human checkpoint | PR moves from draft → ready for review |
| T16 | Human reviewer | Merge via merge commit (not squash), auto-delete branch, verify all four issues auto-closed |
| T17 | DevOps | Post-merge smoke: verify MkDocs site builds, verify `grep -rn "schema_version: 2.6"` across `docs/**` returns only historical hits |

---

## 7. Risks and Mitigations (deployment-only)

| Risk | Mitigation |
|---|---|
| Squash-merge habit erases the 13-commit history | PR description explicitly requests **merge commit**; DevOps checks merge method in the GitHub UI before clicking. |
| Mid-sprint `main` drift forces multiple rebases | Open PR as draft, keep sprint short (single sprint per capacity declaration), rebase at most once at PR-ready time. |
| A story's edits sneak into the wrong commit (atomicity violation) | `git add <specific files>` only — never `git add -A`. Pre-commit, run `git diff --cached --stat` and confirm file list matches the story's edit map from architecture §5. |
| An intermediate commit closes an issue early via a stray `Closes #` keyword | Intermediate commits use `refs #NN` only; `Closes #` appears only in the PR body. |
| Revert leaves a half-bundle in place (L1/L2 rollback breaks atomicity retroactively) | Documented trade-off: post-merge partial rollback is an acceptable break of NFR-08's pre-merge atomicity because the alternative (L3 full-bundle revert) punishes the other three stories for one story's defect. L3 remains available if the surviving stories can't stand alone. |

---

*"There and back again, Mr. Frodo — and if we must go back, we go back by the same road, one step at a time, and we leave the path clear for them as come after."*

— Samwise Gamgee, DevOps
