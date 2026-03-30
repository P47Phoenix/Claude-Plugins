# Deployment Strategy: Stage Health Hardening

**Version**: 1.0
**Author**: Samwise Gamgee (DevOps)
**Date**: 2026-03-29
**Status**: Draft
**Inputs**: Sprint Plan v1.0 (Aragorn/SM)

> *"I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline."*

---

## 1. Deployment Approach

This is a plugin marketplace repository. There are no containers, no cloud services, no runtime deployments. "Deploying" means commits merged to `main` on GitHub. Changes take effect the next time a user loads the delivery-flow skill.

**Branch strategy**:
- Create feature branch `feat/stage-health-hardening` from `main`
- All 5 stories developed on this single branch
- Single PR to `main` containing all 5 story commits
- PR description references PRD v1.1 and retro sources c8f2, k4m9
- Squash merge is NOT used -- preserve individual story commits for granular revert capability

**What ships**: Markdown-only edits to 5 existing reference/skill files. No new files created, no scripts, no schema changes, no config key additions.

| Target File | Modified By |
|-------------|-------------|
| `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | US-01, US-03, US-04, US-05 |
| `delivery-team/skills/delivery-flow/references/quality-gates.md` | US-02, US-03, US-04, US-05 |
| `delivery-team/skills/delivery-flow/references/artifact-contracts.md` | US-02 |
| `delivery-team/skills/delivery-flow/references/project-templates.md` | US-04 |
| `delivery-team/skills/quality/SKILL.md` | US-01 |

---

## 2. Commit Strategy

One conventional commit per completed story, in implementation order. Each commit is atomic and independently revertable.

| Order | Commit Message | Story | Milestone |
|-------|---------------|-------|-----------|
| 1 | `feat: add phantom reference detection and filename reconciliation (US-03)` | US-03 | M2 |
| 2 | `feat: add plan stage capacity and coverage guardrails (US-04)` | US-04 | M3 |
| 3 | `feat: add shared-module review at UAT stage (US-01)` | US-01 | M1 |
| 4 | `feat: add empirical-items tracking at UAT stage (US-02)` | US-02 | M1 |
| 5 | `feat: add derived artifact regeneration at dev DoD (US-05)` | US-05 | M4 |
| 6 | `chore: bump version to 2.12.0` | -- | -- |

**Commit rules**:
- Each commit includes ONLY the files listed for that story in the sprint plan
- No cross-story file changes in a single commit (even when stories touch the same file, each commit captures only that story's edits)
- Commit body includes: story ID, milestone, retro source(s), and list of modified files
- All commits use lowercase prefix per conventional commits spec

**Example commit body**:
```
feat: add phantom reference detection and filename reconciliation (US-03)

Story: US-03 (Milestone M2)
Retro source: k4m9
Files modified:
- delivery-team/skills/delivery-flow/references/quality-gates.md
- delivery-team/skills/delivery-flow/references/pipeline-stages.md
```

---

## 3. Rollback Procedure

Now, if something goes sideways -- and I have seen the Dead Marshes, so I know things go sideways -- here is how we come back safe.

### 3.1 Per-Story Revert

Because each story is a single commit, any story can be reverted independently:

```bash
# Identify the commit to revert
git log --oneline --grep="US-03"

# Revert that specific commit
git revert <commit-sha>
```

**Revert order matters**: If reverting US-02, check whether US-01 (its dependency) also needs reverting. The dependency chain is:

```
US-03 (independent)
US-04 (independent)
US-01 (independent)
US-02 (depends on US-01 -- shares UAT stage context)
US-05 (independent)
```

Only US-02 has a dependency. All others can be reverted in isolation.

### 3.2 Full Feature Revert

If the entire feature must be rolled back:

```bash
# Revert all 5 story commits in reverse order (exclude version bump)
git revert <US-05-sha> <US-02-sha> <US-01-sha> <US-04-sha> <US-03-sha>
```

This creates 5 revert commits preserving full history. Do NOT use `git reset --hard` on `main`.

### 3.3 Revert Triggers

Initiate rollback if any of the following occur post-merge:
- A pipeline run fails at a hardened gate due to a defect in the new gate criteria (not a legitimate quality failure)
- Step renumbering errors cause downstream stage references to break
- Token budget breach (NFR-04: >500 tokens added to any single stage) causes context window issues
- False positive rate on phantom reference detection exceeds 10% over 3 pipeline runs

### 3.4 Revert Window

- **Immediate** (within same session): Revert on `main` directly
- **After subsequent commits**: Create a revert PR following the same branch/PR workflow

---

## 4. Version Bump Plan

Current version: **2.11.0**

This feature adds new gate criteria and stage sub-steps to existing pipeline stages. It is additive, non-breaking, and backward-compatible. Per semver:

| Component | Bump | Rationale |
|-----------|------|-----------|
| Major | No | No breaking changes to config schema or skill interfaces |
| Minor | Yes | New pipeline capabilities (5 new guardrails across 4 stages) |
| Patch | No | This is not a bug fix |

**Target version**: **2.12.0**

**Bump procedure**:
1. After all 5 story commits pass dogfooding, create a 6th commit:
   ```
   chore: bump version to 2.12.0
   ```
2. Update version in `.claude-plugin/marketplace.json`
3. This commit goes on the feature branch, included in the PR
4. No config migration needed -- no new config keys, no schema version change

---

## 5. Post-Deployment Verification

After the PR merges to `main`, we do not just walk away from the campfire. We make sure the Shire is safe.

### 5.1 Immediate Verification (same session)

- [ ] PR merged without conflicts
- [ ] All 6 commits present on `main` (5 stories + version bump)
- [ ] `marketplace.json` shows version `2.12.0`
- [ ] Git log confirms correct commit order and conventional commit format

### 5.2 Structural Verification

- [ ] Load `delivery-team:delivery-flow` skill -- confirm it loads without errors
- [ ] Spot-check each modified file is readable and well-formed:
  - `pipeline-stages.md`: Step numbering is sequential in Stages 5, 6, and 7
  - `quality-gates.md`: Gates 3, 5, 6, 7 have new criteria in correct positions
  - `artifact-contracts.md`: Stage 6->7 contract table has new row
  - `project-templates.md`: Sprint Plan Mandatory Sections present at end
  - `quality/SKILL.md`: Shared-Module Review Protocol in correct section order

### 5.3 Functional Verification (first pipeline run post-merge)

On the first pipeline run after merge, observe:
- [ ] Phantom reference WARNING fires at Design stage (Gate 3)
- [ ] Filename reconciliation gate checked at Dev entry (Stage 6)
- [ ] Matrix validation step executes at Plan stage (Stage 5)
- [ ] Shared-module review checkpoint present at UAT (Stage 7)
- [ ] Empirical-items classification required at UAT (Gate 7)
- [ ] Derived artifact regeneration step present at Dev DoD (Stage 6)
- [ ] No regressions in Idea, Refine, or Architect stages

### 5.4 Monitoring (3-sprint window)

Track over the next 3 pipeline runs:
- First-try pass rate at Design, Plan, Dev, and UAT gates (target: measurable improvement over pre-hardening baseline)
- False positive rate on phantom reference detection (target: <10%)
- Pipeline throughput (target: no significant increase in stage duration)

If pass rates do not improve after 3 runs, revisit gate severity levels per PRD risk table.

---

## 6. Pre-Merge Checklist

Before the PR is approved for merge:

- [ ] All 5 stories implemented (Steps 2-6 of sprint plan)
- [ ] Cross-story verification pass complete (Step 7)
- [ ] Dogfooding BUG_FIX pipeline passed (Step 8 -- P0 gate)
- [ ] `plugin-dev:skill-development` was loaded before file edits
- [ ] Version bumped to 2.12.0
- [ ] PR references PRD v1.1 and retros c8f2, k4m9
- [ ] No files outside the 5 target files were modified (besides marketplace.json for version bump)

---

*"There's some good in this world, Mr. Frodo, and it's worth fighting for." These gates protect the good work this team does. Five stories, five commits, one clean merge to main. Steady as she goes -- that is how we carry the pipeline home.*
