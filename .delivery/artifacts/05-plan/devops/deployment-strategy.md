# Deployment Strategy: PRD Quality Gate Flow Refactoring

**Version**: 1.0
**Author**: Samwise Gamgee (DevOps)
**Date**: 2026-03-30
**Status**: Draft
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Design Spec**: `.delivery/artifacts/03-design/ux/design-spec.md` v1.0
**Issues**: #51 (God object), #52 (Duplicate entry points), #53 (Missing function structure)

> *"I can't carry the codebase for you, but I can carry the deployment."*

---

## 1. Deployment Approach

This is a plugin marketplace repository with no build step, no containers, no cloud services. "Deploying" means commits merged to `main` on GitHub. Changes take effect when a user next runs any `prd-quality-gate-flow/` script.

**What ships**: A structural refactoring of 6 Python files in `prd-quality-gate-flow/`, plus 4 new Python modules, minus 2 deleted duplicates. No new external dependencies. No database schema changes. No config changes. Behavioral output must be structurally equivalent before and after.

### Scope Summary

| Action | Files |
|--------|-------|
| **NEW** (4) | `shared.py`, `schema.py`, `stage_definitions.py`, `gate_definitions.py` |
| **MODIFIED** (4) | `prd_flow_builder.py`, `prd_execute.py`, `fix_and_run.py`, `check_db.py` |
| **DELETED** (2) | `run_execute.py`, `run_builder.py` |
| **MODIFIED (docs)** | `CLAUDE.md` (entry point section only) |
| **UNCHANGED** (2) | `business_rules_engine.py`, `flow_orchestrator.py` (NFR-06: zero diff) |

---

## 2. Git Branching Approach

### Branch Strategy

```
main ─────────────────────────────────────────────── merge ──▶
  \                                                   /
   feat/prd-qgf-refactoring ── c1 ── c2 ── ... ── c10
```

- **Branch name**: `feat/prd-qgf-refactoring`
- **Created from**: `main` at current HEAD
- **Single feature branch** for all refactoring work
- **Single PR** to `main` containing all commits (PRD R7: atomic PR requirement)
- **Merge strategy**: Standard merge commit -- do NOT squash. Individual commits must be preserved for granular revert capability.
- **No long-lived branches**: Feature branch is deleted after merge.

### Branch Creation

```bash
git checkout main
git pull origin main
git checkout -b feat/prd-qgf-refactoring
```

---

## 3. Commit Strategy (Conventional Commits)

One commit per refactoring step from the design spec's 10-step sequence. Each commit leaves the codebase in a working state. Commits follow the conventional commits specification with lowercase prefix.

### Commit Sequence

| Order | Commit Message | Design Step | Files Touched |
|-------|---------------|-------------|---------------|
| 1 | `refactor: add shared constants module for prd-quality-gate-flow` | Step 1 | `shared.py` (new) |
| 2 | `refactor: extract database schema from PRDFlowBuilder into schema module` | Step 2 | `schema.py` (new) |
| 3 | `refactor: wire shared.get_connection() to schema initialization` | Step 3 | `shared.py` |
| 4 | `refactor: extract 7 stage definitions into data module` | Step 4 | `stage_definitions.py` (new) |
| 5 | `refactor: extract 7 gate definitions and 20 business rules into data module` | Step 5 | `gate_definitions.py` (new) |
| 6 | `refactor: decompose PRDFlowBuilder from 1157 to <=200 lines` | Step 6 | `prd_flow_builder.py` |
| 7 | `refactor: consolidate prd_execute.py as canonical executor` | Step 7 | `prd_execute.py` |
| 8 | `refactor: restructure fix_and_run.py with named functions and main guard` | Step 8 | `fix_and_run.py` |
| 9 | `refactor: restructure check_db.py with functions and error handling` | Step 9 | `check_db.py` |
| 10 | `refactor: remove duplicate entry points run_execute.py and run_builder.py` | Step 10 | `run_execute.py` (deleted), `run_builder.py` (deleted) |
| 11 | `docs: update CLAUDE.md entry points for prd-quality-gate-flow refactoring` | FR-08 | `CLAUDE.md` |

### Commit Rules

1. Each commit includes ONLY the files listed for that step -- no cross-step changes in a single commit.
2. Every commit must leave the codebase importable and runnable (`python prd_flow_builder.py` must succeed after every commit from Step 6 onward).
3. Commit body includes: design step reference, files modified, and the verification command from the design spec.
4. All commits use `refactor:` prefix (this is structural refactoring, not a new feature or bug fix). The final docs commit uses `docs:` prefix.
5. No version bump commit. This is a refactoring with no new capabilities -- semver does not change. The version in `marketplace.json` stays as-is.

### Commit Body Template

```
refactor: decompose PRDFlowBuilder from 1157 to <=200 lines

Design step: 6
Issues: #51
Files modified:
- prd-quality-gate-flow/prd_flow_builder.py

Verification: python -c "from prd_flow_builder import PRDFlowBuilder; \
  b = PRDFlowBuilder(':memory:'); fid = b.build_prd_flow(); \
  print(b._count_nodes(fid), b._count_rules(fid)); b.close()"
Expected: 15 20
```

---

## 4. Pre-Refactoring Baseline Capture

Before any code changes are made, capture the structural baseline. This is the reference for behavioral compatibility verification (NFR-04, G6).

Now, before we set out on this journey, we need to know exactly what the Shire looks like today. If we do not measure it now, we cannot prove we brought it back safe.

### Baseline Commands

Run these from `prd-quality-gate-flow/` directory and save output:

```bash
# 1. Capture node and rule counts from builder
python -c "
from prd_flow_builder import PRDFlowBuilder
b = PRDFlowBuilder(':memory:')
fid = b.build_prd_flow()
print(f'Nodes: {b._count_nodes(fid)}')
print(f'Rules: {b._count_rules(fid)}')
b.close()
" > ../.delivery/artifacts/05-plan/devops/baseline-counts.txt 2>&1

# 2. Capture flow diagram structure (ignoring timestamp IDs)
python -c "
from prd_flow_builder import PRDFlowBuilder
b = PRDFlowBuilder(':memory:')
fid = b.build_prd_flow()
b.export_flow_diagram(fid)
b.close()
" >> ../.delivery/artifacts/05-plan/devops/baseline-counts.txt 2>&1

# 3. Capture exit codes for all 4 CLI entry points
python prd_flow_builder.py; echo "builder exit: $?"
python prd_execute.py; echo "execute exit: $?"
python check_db.py; echo "check_db exit: $?"
python fix_and_run.py; echo "fix_and_run exit: $?"

# 4. Record hardcoded DB path count (should be 10)
grep -r '"prd_flows.db"' *.py | wc -l
```

**Store baseline file at**: `.delivery/artifacts/05-plan/devops/baseline-counts.txt`

This baseline is the P0 comparison target during UAT (Stage 7).

---

## 5. Rollback Procedure

Now, if something goes sideways -- and I have seen enough bugs to know they will -- here is how we come back safe.

### 5.1 Per-Step Revert (Granular)

Because each refactoring step is a single commit, any step can be reverted. However, the dependency chain constrains revert order:

```
Step 1: shared.py          ← foundation (reverting this requires reverting ALL)
Step 2: schema.py          ← depends on nothing internal
Step 3: shared + schema    ← wires 1 to 2
Step 4: stage_definitions  ← pure data, independent
Step 5: gate_definitions   ← pure data, independent
Step 6: prd_flow_builder   ← depends on 1-5 (THE critical step)
Step 7: prd_execute        ← depends on 1
Step 8: fix_and_run        ← depends on 1
Step 9: check_db           ← depends on 1
Step 10: delete duplicates ← depends on 7 being stable
Step 11: CLAUDE.md         ← depends on 10
```

**Safe individual reverts** (no cascade needed): Steps 4, 5, 9 (if shared.py still exists), 11.

**Cascade reverts**: Reverting Step 1 requires reverting Steps 3, 6, 7, 8, 9, 10. Reverting Step 6 requires reverting Steps 7, 8, 10.

```bash
# Revert a specific step
git log --oneline --grep="Step 6"
git revert <commit-sha>
```

### 5.2 Full Refactoring Revert (Nuclear Option)

If the entire refactoring must be rolled back after merge to `main`:

```bash
# Revert all 11 commits in reverse order
git log --oneline feat/prd-qgf-refactoring..main  # identify merge
git revert --no-commit <step-11-sha> <step-10-sha> ... <step-1-sha>
git commit -m "revert: roll back prd-quality-gate-flow refactoring

Reason: [describe regression]
Issues: #51, #52, #53 (reopened)"
```

This preserves full history. Do NOT use `git reset --hard` on `main`. Ever. That road leads to Mordor and we are not going there today.

### 5.3 Revert Triggers

Initiate rollback if any of the following occur post-merge:

| Trigger | Severity | Action |
|---------|----------|--------|
| `python prd_flow_builder.py` fails to produce 15 nodes / 20 rules | Critical | Full revert |
| `python prd_execute.py` crashes on import | Critical | Full revert |
| `python fix_and_run.py` crashes on fresh DB (latent bug regression) | High | Revert Step 8 |
| `python check_db.py` crashes on missing DB (should show graceful error) | Medium | Revert Step 9 |
| `business_rules_engine.py` or `flow_orchestrator.py` have any diff | Critical | Full revert (NFR-06 violation) |
| Non-stdlib import found in any modified file | Critical | Full revert (NFR-01 violation) |
| CLAUDE.md entry points reference deleted files | Medium | Fix-forward (update docs) |

### 5.4 Revert Window

- **Pre-merge** (on feature branch): `git reset` to the last known-good commit on the branch. No ceremony needed.
- **Post-merge, same session**: Revert commits directly on `main`.
- **Post-merge, after subsequent commits**: Create a revert PR following the same branch/PR workflow.

---

## 6. CLAUDE.md Update Requirements

The PRD (FR-08) requires updating CLAUDE.md to reflect consolidated entry points. This is the **final commit** (Step 11) -- it ships only after all code changes are verified.

### Current State (CLAUDE.md `Running Scripts` section)

```markdown
# PRD quality gate flow
python prd-quality-gate-flow/prd_flow_builder.py
python prd-quality-gate-flow/prd_execute.py
python prd-quality-gate-flow/check_db.py       # Inspect SQLite DB state
python prd-quality-gate-flow/fix_and_run.py    # Automated end-to-end run
```

### Required Changes

1. **No new entry points to add** -- the 4 canonical scripts remain the same.
2. **No deleted scripts to remove** -- `run_execute.py` and `run_builder.py` were never listed in CLAUDE.md.
3. **Verify the existing 4 entries still work post-refactoring** -- this is AC-08c.

### Change Assessment

After careful review: the CLAUDE.md `Running Scripts` section already lists only the 4 canonical scripts. The deleted files (`run_execute.py`, `run_builder.py`) were never documented there. **The CLAUDE.md section may require no changes at all** -- but the verification commit (Step 11) must confirm this explicitly and document the confirmation.

If any import paths, module names, or script behaviors change in a way that affects usage instructions, the `docs:` commit captures those changes. The commit message should state either "confirmed no changes needed" or describe what was updated.

---

## 7. Pre-Merge Verification Checklist

Before the PR from `feat/prd-qgf-refactoring` is approved for merge to `main`, every item below must pass. This is our last gate before the road home.

### 7.1 Structural Verification

- [ ] **Node count**: `PRDFlowBuilder(':memory:').build_prd_flow()` produces exactly 15 nodes (matches baseline)
- [ ] **Rule count**: Exactly 20 business rules created (matches baseline)
- [ ] **Gate count**: Exactly 7 gates (matches baseline)
- [ ] **Flow structure**: `export_flow_diagram()` output structurally matches baseline (ignoring timestamp IDs)
- [ ] **Class size**: `PRDFlowBuilder` class body is <=200 lines (`wc -l` measurement)

### 7.2 CLI Entry Point Verification

- [ ] `cd prd-quality-gate-flow && python prd_flow_builder.py` -- exits cleanly, prints flow summary
- [ ] `cd prd-quality-gate-flow && python prd_execute.py` -- exits cleanly (may require existing DB)
- [ ] `cd prd-quality-gate-flow && python check_db.py` -- exits cleanly against existing DB, shows graceful error on missing DB
- [ ] `cd prd-quality-gate-flow && python fix_and_run.py` -- exits cleanly, no crash on fresh DB (latent bug fix verified)

### 7.3 Deletion Safety

- [ ] `grep -r "run_execute\|run_builder" prd-quality-gate-flow/*.py` returns zero matches
- [ ] `grep -r "from run_execute\|from run_builder\|import run_execute\|import run_builder" prd-quality-gate-flow/*.py` returns zero matches
- [ ] No other file in the repo references the deleted scripts

### 7.4 Hardcoded Path Elimination

- [ ] `grep -r '"prd_flows.db"' prd-quality-gate-flow/*.py` returns matches ONLY in `shared.py`
- [ ] All other `.py` files use `shared.DB_PATH` or `shared.get_connection()`

### 7.5 Dependency Constraints

- [ ] `git diff main -- prd-quality-gate-flow/business_rules_engine.py` shows zero changes (NFR-06)
- [ ] `git diff main -- prd-quality-gate-flow/flow_orchestrator.py` shows zero changes (NFR-06)
- [ ] No non-stdlib imports in any new or modified file (NFR-01): `grep -rn "^import\|^from" prd-quality-gate-flow/*.py` shows only stdlib modules and internal project imports
- [ ] No circular imports: `python -c "import shared; import schema; import stage_definitions; import gate_definitions; import prd_flow_builder; print('OK')"` succeeds

### 7.6 File Size Constraints (NFR-05)

- [ ] `prd_flow_builder.py` <=200 lines (class body)
- [ ] `shared.py` <=300 lines
- [ ] `schema.py` <=300 lines
- [ ] `prd_execute.py` <=300 lines
- [ ] `fix_and_run.py` <=300 lines
- [ ] `check_db.py` <=300 lines
- [ ] `stage_definitions.py` -- if >300 lines, header documents justification (data file exemption)
- [ ] `gate_definitions.py` -- if >300 lines, header documents justification (data file exemption)

### 7.7 Documentation

- [ ] CLAUDE.md `Running Scripts` section verified accurate (AC-08a, AC-08b, AC-08c)
- [ ] PR description references PRD v1.1 and issues #51, #52, #53
- [ ] PR description includes before/after node/rule/gate counts

### 7.8 Final Smoke Test (Dogfooding Gate -- P0)

- [ ] Delete any existing `prd_flows.db` in the working directory
- [ ] Run `python prd_flow_builder.py` -- creates fresh DB, prints flow summary
- [ ] Run `python prd_execute.py` -- executes against freshly built flow
- [ ] Run `python check_db.py` -- inspects the DB just created
- [ ] Run `python fix_and_run.py` -- runs full end-to-end sequence
- [ ] All 4 scripts exit with code 0
- [ ] Node count (15), rule count (20), gate count (7) match pre-refactoring baseline

---

## 8. PR Template

```markdown
## PRD Quality Gate Flow Refactoring

**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Design**: `.delivery/artifacts/03-design/ux/design-spec.md` v1.0
**Closes**: #51, #52, #53

### Summary

Structural refactoring of `prd-quality-gate-flow/` plugin:
- Decompose `PRDFlowBuilder` god object (1,157 -> <=200 lines)
- Extract stage/gate definitions into data modules
- Centralize shared constants (`DB_PATH`, utilities)
- Restructure flat scripts (`fix_and_run.py`, `check_db.py`)
- Delete duplicate entry points (`run_execute.py`, `run_builder.py`)

### Behavioral Compatibility

| Metric | Before | After |
|--------|--------|-------|
| Nodes  | 15     | 15    |
| Rules  | 20     | 20    |
| Gates  | 7      | 7     |
| CLI exit codes | 0 | 0 |

### Test Plan

- [x] Pre-refactoring baseline captured
- [x] All 4 CLI entry points produce structurally equivalent output
- [x] Core modules (`business_rules_engine.py`, `flow_orchestrator.py`) have zero diff
- [x] `"prd_flows.db"` hardcoded only in `shared.py`
- [x] No non-stdlib imports added
- [x] Dogfooding: fresh DB end-to-end run successful
```

---

*"There's some good in this codebase, Mr. Frodo, and it's worth refactoring for." Eleven commits, one clean branch, one atomic PR. We capture the baseline before we set out, we verify at every step, and we keep the road home clear in case we need it. Steady as she goes -- that is how we carry this refactoring to main.*
