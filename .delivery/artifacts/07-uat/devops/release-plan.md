# Release Plan: Stage Health Hardening

**Version**: 1.0
**Author**: Samwise Gamgee (DevOps)
**Date**: 2026-03-29
**Status**: Ready for Execution
**Inputs**: Deployment Strategy v1.0, Consolidated Dev Notes (Gimli)

> *"I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline."*

---

## 1. Release Checklist

Now, a proper release is like packing for a long journey -- you do it in order, you check twice, and you do not leave the rope behind.

### 1.1 Pre-Commit Verification

Complete these before any commit is created on `feat/stage-health-hardening`:

- [ ] All 5 stories at CODE_COMPLETE or DONE status (confirmed per dev notes)
- [ ] 32 structural ACs verified PASS (confirmed -- 32/32 per dev notes)
- [ ] 0 deviations from design spec (confirmed per dev notes)
- [ ] 10 empirical validation items documented for UAT (confirmed per dev notes)
- [ ] `plugin-dev:skill-development` was loaded before all file edits
- [ ] Only the 5 target files were modified (no scope creep):
  - `delivery-team/skills/delivery-flow/references/pipeline-stages.md`
  - `delivery-team/skills/delivery-flow/references/quality-gates.md`
  - `delivery-team/skills/delivery-flow/references/artifact-contracts.md`
  - `delivery-team/skills/delivery-flow/references/project-templates.md`
  - `delivery-team/skills/quality/SKILL.md`
- [ ] Step renumbering verified sequential in all modified stages (5, 6, 7)
- [ ] Retro annotations present (`<!-- retro c8f2 -->` and `<!-- retro k4m9 -->`) per NFR-05
- [ ] No new config keys introduced (no schema version change needed)
- [ ] Token budget spot-check: no single stage gained >500 tokens (NFR-04)

### 1.2 Commit Execution

Create commits in this exact order, one per story. Each commit is atomic and independently revertable. No cross-story file changes in a single commit.

| # | Commit Message | Story | Files |
|---|---------------|-------|-------|
| 1 | `feat: add phantom reference detection and filename reconciliation (US-03)` | US-03 | quality-gates.md, pipeline-stages.md |
| 2 | `feat: add plan stage capacity and coverage guardrails (US-04)` | US-04 | pipeline-stages.md, quality-gates.md, project-templates.md |
| 3 | `feat: add shared-module review at UAT stage (US-01)` | US-01 | pipeline-stages.md, quality/SKILL.md |
| 4 | `feat: add empirical-items tracking at UAT stage (US-02)` | US-02 | artifact-contracts.md, quality-gates.md |
| 5 | `feat: add derived artifact regeneration at dev DoD (US-05)` | US-05 | pipeline-stages.md, quality-gates.md |
| 6 | `chore: bump version to 2.12.0` | -- | marketplace.json |

Each commit body must include: story ID, milestone, retro source(s), and list of modified files.

### 1.3 Post-Commit Checks

After all 6 commits are on the feature branch:

- [ ] `git log --oneline` shows 6 commits in correct order
- [ ] All commit messages follow conventional commits (lowercase prefix, parenthetical story ID)
- [ ] Each commit body contains story ID, milestone, retro sources, and file list
- [ ] No untracked or unstaged files remain (`git status` clean)
- [ ] Branch `feat/stage-health-hardening` is ahead of `main` by exactly 6 commits
- [ ] Dogfooding BUG_FIX pipeline run passed (P0 gate per deployment strategy Step 8)

---

## 2. Conventional Commit Messages

The full set of commits, ready to use:

```
feat: add phantom reference detection and filename reconciliation (US-03)

Story: US-03 (Milestone M2)
Retro source: k4m9
Files modified:
- delivery-team/skills/delivery-flow/references/quality-gates.md
- delivery-team/skills/delivery-flow/references/pipeline-stages.md
```

```
feat: add plan stage capacity and coverage guardrails (US-04)

Story: US-04 (Milestone M3)
Retro source: c8f2
Files modified:
- delivery-team/skills/delivery-flow/references/pipeline-stages.md
- delivery-team/skills/delivery-flow/references/quality-gates.md
- delivery-team/skills/delivery-flow/references/project-templates.md
```

```
feat: add shared-module review at UAT stage (US-01)

Story: US-01 (Milestone M1)
Retro source: c8f2
Files modified:
- delivery-team/skills/delivery-flow/references/pipeline-stages.md
- delivery-team/skills/quality/SKILL.md
```

```
feat: add empirical-items tracking at UAT stage (US-02)

Story: US-02 (Milestone M1)
Retro source: c8f2
Files modified:
- delivery-team/skills/delivery-flow/references/artifact-contracts.md
- delivery-team/skills/delivery-flow/references/quality-gates.md
```

```
feat: add derived artifact regeneration at dev DoD (US-05)

Story: US-05 (Milestone M4)
Retro source: k4m9
Files modified:
- delivery-team/skills/delivery-flow/references/pipeline-stages.md
- delivery-team/skills/delivery-flow/references/quality-gates.md
```

```
chore: bump version to 2.12.0
```

---

## 3. Version Bump Recommendation

| Field | Value |
|-------|-------|
| Current version | 2.11.0 |
| Target version | **2.12.0** |
| Bump type | **Minor** |
| Rationale | Additive, non-breaking changes: 5 new guardrails across 4 pipeline stages. No config schema changes, no breaking changes to skill interfaces. |

**Bump procedure**:
1. After all 5 story commits pass dogfooding, create commit #6: `chore: bump version to 2.12.0`
2. Update version string in `.claude-plugin/marketplace.json`
3. No config migration needed -- no new config keys, no schema version change

---

## 4. Rollback Procedure

If something goes sideways -- and I have seen the Dead Marshes, so I know things can go sideways -- here is how we come back safe.

### 4.1 Per-Story Revert

Each story is a single commit. Any story can be reverted independently:

```bash
git log --oneline --grep="US-03"
git revert <commit-sha>
```

**Dependency chain** (only US-02 has a dependency):

```
US-03 --> independent (revert freely)
US-04 --> independent (revert freely)
US-01 --> independent (revert freely)
US-02 --> depends on US-01 (revert both if reverting US-02)
US-05 --> independent (revert freely)
```

### 4.2 Full Feature Revert

Revert all 5 story commits in reverse order (exclude version bump):

```bash
git revert <US-05-sha> <US-02-sha> <US-01-sha> <US-04-sha> <US-03-sha>
```

This creates 5 revert commits preserving full history. Do NOT use `git reset --hard` on `main`.

### 4.3 Revert Triggers

Initiate rollback if any of the following occur post-merge:
- A hardened gate fails due to a defect in the new criteria (not a legitimate quality failure)
- Step renumbering errors cause downstream stage references to break
- Token budget breach (>500 tokens added to any single stage) causes context window issues
- False positive rate on phantom reference detection exceeds 10% over 3 pipeline runs

### 4.4 Revert Window

- **Same session**: Revert directly on `main`
- **After subsequent commits**: Create a revert PR following standard branch/PR workflow

---

## 5. Post-Release Verification Steps

After the PR merges to `main`, we do not just walk away from the campfire. We make sure the Shire is safe.

### 5.1 Immediate (same session, within 5 minutes of merge)

- [ ] PR merged without conflicts
- [ ] All 6 commits present on `main` (5 stories + version bump)
- [ ] `marketplace.json` shows version `2.12.0`
- [ ] `git log --oneline -6` confirms correct commit order and conventional commit format
- [ ] No unexpected files changed (`git diff HEAD~6 --name-only` matches expected 6 files)

### 5.2 Structural Verification (same session)

- [ ] Load `delivery-team:delivery-flow` skill -- confirm it loads without errors
- [ ] Spot-check each modified file:
  - `pipeline-stages.md`: Step numbering is sequential in Stages 5, 6, and 7
  - `quality-gates.md`: Gates 3, 5, 6, 7 have new criteria in correct positions
  - `artifact-contracts.md`: Stage 6->7 contract table has new Empirical Items row
  - `project-templates.md`: Sprint Plan Mandatory Sections present at end
  - `quality/SKILL.md`: Shared-Module Review Protocol in correct section order

### 5.3 Functional Verification (first pipeline run post-merge)

On the first delivery pipeline run after merge, observe and confirm:

- [ ] Phantom reference WARNING fires at Design stage (Gate 3)
- [ ] Filename reconciliation gate checked at Dev entry (Stage 6)
- [ ] Matrix validation step executes at Plan stage (Stage 5)
- [ ] Shared-module review checkpoint present at UAT (Stage 7)
- [ ] Empirical-items classification required at UAT (Gate 7)
- [ ] Derived artifact regeneration step present at Dev DoD (Stage 6)
- [ ] No regressions in Idea, Refine, or Architect stages (unmodified stages unaffected)

### 5.4 Monitoring (3-sprint window)

Track over the next 3 pipeline runs:

| Metric | Target | Action if missed |
|--------|--------|------------------|
| First-try pass rate at Design, Plan, Dev, UAT gates | Measurable improvement over baseline | Revisit gate severity levels per PRD risk table |
| Phantom reference false positive rate | <10% | Tune detection criteria or add exemptions |
| Pipeline throughput (stage duration) | No significant increase | Reduce gate verbosity or consolidate checks |

---

## 6. PR Details

| Field | Value |
|-------|-------|
| Branch | `feat/stage-health-hardening` |
| Target | `main` |
| Title | `feat: Stage Health Hardening — 5 new pipeline guardrails` |
| References | PRD v1.1, retro sources c8f2 and k4m9 |
| Merge strategy | Standard merge (NOT squash -- preserve individual story commits) |

---

*"There's some good in this world, Mr. Frodo, and it's worth fighting for." Five stories, six commits, one clean merge. Every gate checked, every step numbered, every rollback path mapped. That is how we carry the pipeline home.*
