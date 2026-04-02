# Release Plan: Pipeline Integrity Fixes

**Version**: 2.12.1
**Author**: Samwise Gamgee (DevOps)
**Date**: 2026-04-01
**Status**: Ready for Execution
**Pipeline Run**: BUG_FIX run-2026-04-01-m7v3
**Dev Notes**: `.delivery/artifacts/06-dev/developer/dev-notes.md`
**Issue**: #54

> *"I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline."*

---

## 1. Commit Strategy

Single commit, conventional format. All four files are markdown-only edits to delivery-flow reference documents -- they travel together as one pack, not scattered across the road.

```
fix: enforce pipeline integrity for branch strategy, confidence scoring, and architect routing

Add blocking enforcement directives for branch creation (Stage 5),
branch targeting (Stage 6), and PR creation (Stage 7) to SKILL.md
and git-integration.md. Cap review board confidence at 4/5 without
empirical validation in quality-gates.md. Add refactoring sub-type
detection with 8 signals and narrow Architect skip conditions in
project-types.md.

13/13 acceptance criteria verified (structural).

Closes #54
```

### Files Changed (4, all markdown)

| File | Changes |
|------|---------|
| `delivery-flow/SKILL.md` | Branch creation (Stage 5), branch enforcement (Stage 6), PR creation (Stage 7) |
| `delivery-flow/references/git-integration.md` | ENFORCEMENT blockquote, Stage 6 branch enforcement subsection, Stage 7 PR creation subsection |
| `delivery-flow/references/quality-gates.md` | Confidence cap at 4/5, empirical validation limitation documentation requirement |
| `delivery-flow/references/project-types.md` | Refactoring sub-type with 8 signals, narrowed skip conditions |

All files are in the installed plugin directory at `~/.claude/plugins/marketplaces/mec-claude-agent-skills/delivery-team/skills/delivery-flow/`.

---

## 2. Pre-Commit Verification

Before we set out, we check the pack twice. No ropes left behind.

- [ ] All 13 ACs confirmed PASS in dev notes (structural verification)
- [ ] No new files created -- only 4 existing files modified
- [ ] No config schema changes (all config keys already exist in v2.3)
- [ ] No new dependencies added
- [ ] `git diff --stat` shows exactly 4 files, all `.md` extension
- [ ] No changes to any `.py`, `.json`, `.yml`, or other non-markdown files
- [ ] Conventional commit message format validated (`fix:` prefix, `Closes #54` footer)
- [ ] Existing content in all 4 files is preserved -- changes are additive insertions only

---

## 3. Rollback Procedure

If something goes sideways -- and markdown-only changes rarely do, but a Gamgee is always prepared -- the road home is short and clear.

### 3.1 Single-Commit Revert

```bash
# Identify the commit
git log --oneline -3

# Revert cleanly
git revert <commit-sha>

# Commit message:
# revert: roll back pipeline integrity fixes
#
# Reason: [describe the regression observed]
# Issue: #54 (will be reopened)
```

No `git reset --hard`. That road leads to Mordor and we are not going there today.

### 3.2 Revert Triggers

| Trigger | Action |
|---------|--------|
| Delivery-flow pipeline fails to load or parse SKILL.md | Full revert |
| Branch enforcement fires when `git.branch_strategy: none` | Full revert |
| Existing project-type routing broken (non-refactoring FEATURE misrouted) | Full revert |
| Confidence scoring applied outside Gate 7 context | Fix-forward if isolated, else full revert |

### 3.3 Post-Revert Cleanup

1. Reopen issue #54 with regression description
2. File new issue documenting root cause
3. All 4 files restore to pre-fix state via the revert commit

---

## 4. Post-Merge Verification

After the commit lands on `main`, we make sure the Shire is safe.

- [ ] `git log --oneline -1` shows `fix:` prefix and `Closes #54`
- [ ] `git diff HEAD~1 --name-only` shows exactly 4 markdown files
- [ ] `git status` is clean (no untracked or unstaged files)
- [ ] Issue #54 auto-closed by GitHub (or close manually: `gh issue close 54 --comment "Fixed by pipeline integrity enforcement commit"`)
- [ ] **Dogfooding gate (P0)**: Run a delivery-flow pipeline session that exercises at least one of the three fix areas (branch enforcement, confidence cap, or refactoring sub-type routing) to confirm the instructions are correctly parsed and applied

---

*"These fixes are like good rope, Mr. Frodo -- you don't notice them until you need them, and then you're glad someone packed them proper." Four files, one commit, one issue closed. The pipeline holds.*
