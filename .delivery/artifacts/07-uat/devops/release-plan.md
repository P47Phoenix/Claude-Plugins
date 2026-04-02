# Release Plan: PRD Quality Gate Flow Refactoring

**Version**: 1.0
**Author**: Samwise Gamgee (DevOps)
**Date**: 2026-03-30
**Status**: Ready for Execution
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Deployment Strategy**: `.delivery/artifacts/05-plan/devops/deployment-strategy.md` v1.0
**Dev Notes**: `.delivery/artifacts/06-dev/developer/dev-notes.md`
**Issues**: #51 (God object), #52 (Duplicate entry points), #53 (Missing function structure)

> *"I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline."*

---

## 1. Pre-Release Checklist

Now, a proper release is like packing for a long journey -- you check everything twice, you do not leave the rope behind, and you make sure the path home is clear before you set out.

### 1.1 Code Completeness

- [ ] All 11 user stories at CODE_COMPLETE or DONE status (confirmed per dev notes: US-01 through US-11)
- [ ] All behavioral baselines verified PASS:
  - [ ] Node count: 15 (matches pre-refactoring baseline)
  - [ ] Rule count: 20 (matches pre-refactoring baseline)
  - [ ] Gate count: 7 (matches pre-refactoring baseline)
  - [ ] Gate rule distribution: [4,4,3,1,4,3,1] (matches baseline)
  - [ ] Node names and types: all 15 exact matches
- [ ] NFR compliance verified (all 6 NFRs PASS per dev notes):
  - [ ] NFR-01: Zero external dependencies (stdlib only)
  - [ ] NFR-02: Schema compatibility (CREATE IF NOT EXISTS, idempotent)
  - [ ] NFR-03: Python 3.9+ compatible
  - [ ] NFR-04: Behavioral compatibility (structural equivalence confirmed)
  - [ ] NFR-05: File size constraints met (all logic files <=300 lines; gate_definitions.py 411 lines is declarative data with justification)
  - [ ] NFR-06: Core modules untouched (`business_rules_engine.py`, `flow_orchestrator.py` zero diff)
- [ ] PRDFlowBuilder class body: 162 lines (target <=200)
- [ ] `builder.conn` remains accessible as public attribute (AC-03d2)
- [ ] Latent bug fix confirmed: `fix_and_run.py` uses `shared.get_connection()` with `ensure_schema()` (AC-03g)

### 1.2 File Inventory

Verify exactly these files are affected -- no more, no less:

| Action | Files |
|--------|-------|
| **NEW** (4) | `shared.py`, `schema.py`, `stage_definitions.py`, `gate_definitions.py` |
| **MODIFIED** (4) | `prd_flow_builder.py`, `prd_execute.py`, `fix_and_run.py`, `check_db.py` |
| **DELETED** (2) | `run_execute.py`, `run_builder.py` |
| **UNCHANGED** (2) | `business_rules_engine.py`, `flow_orchestrator.py` |

All files are in the `prd-quality-gate-flow/` directory. CLAUDE.md was verified clean -- already lists only the 4 canonical scripts, no references to deleted files. No CLAUDE.md changes needed.

### 1.3 Deletion Safety

- [ ] `grep -r "run_execute\|run_builder" prd-quality-gate-flow/*.py` returns zero matches
- [ ] `grep -r "from run_execute\|from run_builder\|import run_execute\|import run_builder" prd-quality-gate-flow/*.py` returns zero matches
- [ ] No other file in the repo references the deleted scripts

### 1.4 Hardcoded Path Elimination

- [ ] `grep -r '"prd_flows.db"' prd-quality-gate-flow/*.py` returns matches ONLY in `shared.py`
- [ ] All other `.py` files use `shared.DB_PATH` or `shared.get_connection()`

### 1.5 No Circular Imports

- [ ] `cd prd-quality-gate-flow && python -c "import shared; import schema; import stage_definitions; import gate_definitions; import prd_flow_builder; print('OK')"` succeeds

---

## 2. Commit Message Template

The deployment strategy specifies a single commit per refactoring step (11 commits total). However, per the task context, the team has agreed to a **single commit** for the refactoring. Here is the commit message:

```
refactor: decompose prd-quality-gate-flow god object and consolidate entry points

Structural refactoring of prd-quality-gate-flow/ plugin addressing three
issues of accumulated technical debt.

God object (#51):
- Decompose PRDFlowBuilder from 1,157 to 162 lines (class body)
- Extract 7 stage definitions into stage_definitions.py (269 lines)
- Extract 7 gate definitions + 20 business rules into gate_definitions.py (411 lines)
- Extract database schema into schema.py (174 lines)

Duplicate entry points (#52):
- Delete run_execute.py (duplicate of prd_execute.py)
- Delete run_builder.py (duplicate of prd_flow_builder.py __main__)
- Centralize DB_PATH and utilities in shared.py (60 lines)
- Consolidate EXAMPLE_PRODUCT_IDEAS to prd_execute.py only

Missing function structure (#53):
- Restructure fix_and_run.py with 5 named functions and main() guard
- Restructure check_db.py with 3 descriptive functions and error handling

Behavioral compatibility verified:
- Nodes: 15 | Rules: 20 | Gates: 7 | Distribution: [4,4,3,1,4,3,1]
- Core modules (business_rules_engine.py, flow_orchestrator.py): zero diff
- Latent bug fixed: fix_and_run.py schema ordering (AC-03g)

Closes #51, #52, #53
```

---

## 3. Post-Merge Verification Steps

After the PR merges to `main`, we do not just walk away from the campfire. We make sure the Shire is safe.

### 3.1 Immediate (same session, within 5 minutes of merge)

- [ ] PR merged without conflicts
- [ ] All commits present on `main`
- [ ] `git log --oneline` confirms correct commit message and conventional commit format
- [ ] No unexpected files changed: `git diff HEAD~1 --name-only` matches expected file list (10 files: 4 new, 4 modified, 2 deleted)
- [ ] No untracked or unstaged files remain (`git status` clean)

### 3.2 CLAUDE.md Verification (FR-08, AC-08a/b/c)

- [ ] CLAUDE.md `Running Scripts` section lists exactly 4 canonical scripts:
  ```
  python prd-quality-gate-flow/prd_flow_builder.py
  python prd-quality-gate-flow/prd_execute.py
  python prd-quality-gate-flow/check_db.py
  python prd-quality-gate-flow/fix_and_run.py
  ```
- [ ] No references to `run_execute.py` or `run_builder.py` anywhere in CLAUDE.md
- [ ] No references to deleted files anywhere in the repository

### 3.3 Structural Verification

Run from the `prd-quality-gate-flow/` directory:

```bash
# Verify node and rule counts
python -c "
from prd_flow_builder import PRDFlowBuilder
b = PRDFlowBuilder(':memory:')
fid = b.build_prd_flow()
print(f'Nodes: {b._count_nodes(fid)}')
print(f'Rules: {b._count_rules(fid)}')
b.close()
"
# Expected: Nodes: 15, Rules: 20
```

- [ ] Node count: 15
- [ ] Rule count: 20
- [ ] Gate count: 7
- [ ] `export_flow_diagram()` produces structurally equivalent output
- [ ] `PRDFlowBuilder` class body <=200 lines

### 3.4 CLI Entry Point Smoke Test (Dogfooding Gate -- P0)

This is the gate that matters most. If these four scripts do not run clean on a fresh database, the refactoring has failed and we revert.

```bash
cd prd-quality-gate-flow

# Clean slate
rm -f prd_flows.db

# 1. Build fresh flow
python prd_flow_builder.py
echo "builder exit: $?"

# 2. Execute against freshly built flow
python prd_execute.py
echo "execute exit: $?"

# 3. Inspect the DB
python check_db.py
echo "check_db exit: $?"

# 4. Full end-to-end run
python fix_and_run.py
echo "fix_and_run exit: $?"
```

- [ ] All 4 scripts exit with code 0
- [ ] `python check_db.py` against missing DB shows graceful error (no raw stack trace)
- [ ] `python fix_and_run.py` works on fresh DB (latent bug fix verified)

### 3.5 Dependency Constraints

```bash
# Core modules must have zero diff from main
git diff main -- prd-quality-gate-flow/business_rules_engine.py  # expect empty
git diff main -- prd-quality-gate-flow/flow_orchestrator.py      # expect empty

# No non-stdlib imports
grep -rn "^import\|^from" prd-quality-gate-flow/*.py | grep -v "sqlite3\|datetime\|json\|os\|sys\|textwrap\|io\|pathlib\|shared\|schema\|stage_definitions\|gate_definitions\|prd_flow_builder\|business_rules_engine\|flow_orchestrator"
# expect: no external package imports
```

- [ ] `business_rules_engine.py` zero diff
- [ ] `flow_orchestrator.py` zero diff
- [ ] No non-stdlib imports in any new or modified file

---

## 4. Issue Closure Commands

After the PR merges and all post-merge verification passes:

```bash
# Close all three issues via GitHub CLI
gh issue close 51 --comment "Closed by PRD Quality Gate Flow refactoring. PRDFlowBuilder decomposed from 1,157 to 162 lines (class body). Stage/gate definitions extracted to data modules."

gh issue close 52 --comment "Closed by PRD Quality Gate Flow refactoring. run_execute.py and run_builder.py deleted. DB_PATH centralized in shared.py. EXAMPLE_PRODUCT_IDEAS consolidated to prd_execute.py."

gh issue close 53 --comment "Closed by PRD Quality Gate Flow refactoring. fix_and_run.py restructured with 5 named functions and main() guard. check_db.py restructured with 3 descriptive functions and error handling."
```

Alternatively, the PR commit message contains `Closes #51, #52, #53` which will auto-close all three issues when the PR merges. The `gh issue close` commands above are a backup if auto-close does not trigger (e.g., if the merge commit does not carry the Closes footer).

**Traceability**:

| Issue | FRs Addressed | Verification |
|-------|--------------|--------------|
| #51 (God object) | FR-01, FR-02, FR-03 | 162-line class body, 7 stage dicts, 7 gate dicts, 20 rules |
| #52 (Duplicate entry points) | FR-04, FR-05, FR-08 | 2 files deleted, DB_PATH in shared.py only, CLAUDE.md verified |
| #53 (Missing function structure) | FR-06, FR-07 | fix_and_run.py: 5 functions + main(); check_db.py: 3 functions + main() |

---

## 5. Rollback Procedure

Now, if something goes sideways -- and I have seen enough bugs to know they will -- here is how we come back safe. We do not leave anyone behind.

### 5.1 Single-Commit Revert (Primary Path)

Since the refactoring lands as a single commit (or single PR merge commit), rollback is straightforward:

```bash
# Identify the merge commit
git log --oneline -5

# Revert the entire refactoring
git revert <merge-commit-sha> -m 1
# The -m 1 flag selects the main branch parent if this is a merge commit

# Commit message:
# revert: roll back prd-quality-gate-flow refactoring
#
# Reason: [describe the regression observed]
# Issues: #51, #52, #53 (will be reopened)
```

This preserves full history. Do NOT use `git reset --hard` on `main`. That road leads to Mordor and we are not going there today.

### 5.2 Revert Triggers

Initiate rollback if any of the following occur post-merge:

| Trigger | Severity | Action |
|---------|----------|--------|
| `python prd_flow_builder.py` fails to produce 15 nodes / 20 rules | Critical | Full revert |
| `python prd_execute.py` crashes on import | Critical | Full revert |
| `python fix_and_run.py` crashes on fresh DB | High | Full revert (latent bug regression) |
| `python check_db.py` crashes on missing DB (should show graceful error) | Medium | Fix-forward if isolated, else full revert |
| `business_rules_engine.py` or `flow_orchestrator.py` have any diff | Critical | Full revert (NFR-06 violation) |
| Non-stdlib import found in any modified file | Critical | Full revert (NFR-01 violation) |
| CLAUDE.md entry points reference deleted files | Low | Fix-forward (update docs) |
| Circular import error on any new module | High | Full revert |

### 5.3 Revert Window

- **Pre-merge** (on feature branch): `git reset` to the last known-good commit on the branch. No ceremony needed.
- **Post-merge, same session**: Revert commit directly on `main`.
- **Post-merge, after subsequent commits**: Create a revert PR following the standard branch/PR workflow.

### 5.4 Post-Revert Cleanup

If a full revert is performed:

1. Reopen issues #51, #52, #53 with a comment explaining the regression
2. File a new issue documenting the regression root cause
3. The reverted files (`run_execute.py`, `run_builder.py`) will be restored by the revert commit -- verify they are functional
4. CLAUDE.md requires no changes (it never referenced the deleted files)

---

## 6. PR Template

```markdown
## PRD Quality Gate Flow Refactoring

**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Design**: `.delivery/artifacts/03-design/ux/design-spec.md` v1.0
**Closes**: #51, #52, #53

### Summary

Structural refactoring of `prd-quality-gate-flow/` plugin:
- Decompose `PRDFlowBuilder` god object (1,157 -> 162 lines class body)
- Extract stage/gate definitions into data modules (stage_definitions.py, gate_definitions.py)
- Extract database schema into schema.py with ensure_schema() contract
- Centralize shared constants in shared.py (DB_PATH, get_connection(), utilities)
- Restructure flat scripts (fix_and_run.py, check_db.py) with named functions
- Delete duplicate entry points (run_execute.py, run_builder.py)
- Fix latent bug: fix_and_run.py schema ordering on fresh DB

### Behavioral Compatibility

| Metric | Before | After |
|--------|--------|-------|
| Nodes  | 15     | 15    |
| Rules  | 20     | 20    |
| Gates  | 7      | 7     |
| Gate distribution | [4,4,3,1,4,3,1] | [4,4,3,1,4,3,1] |
| CLI exit codes | 0 | 0 |
| Core modules diff | -- | zero |

### Test Plan

- [x] Pre-refactoring baseline captured
- [x] All 4 CLI entry points produce structurally equivalent output
- [x] Core modules (business_rules_engine.py, flow_orchestrator.py) have zero diff
- [x] "prd_flows.db" hardcoded only in shared.py
- [x] No non-stdlib imports added
- [x] No circular imports
- [x] Dogfooding: fresh DB end-to-end run successful
- [x] check_db.py graceful error on missing DB
- [x] fix_and_run.py latent bug fix verified on fresh DB
```

---

## 7. Version Bump

**No version bump required.** This is a structural refactoring with no new capabilities -- semver does not change. The version in `marketplace.json` stays as-is. The deployment strategy (Section 3, Commit Rule 5) explicitly states: "No version bump commit."

---

*"There's some good in this codebase, Mr. Frodo, and it's worth refactoring for." One clean commit, one atomic PR, three issues closed. We captured the baseline before we set out, we verified at every step, and we kept the road home clear. Now we carry this refactoring to main -- steady as she goes.*
