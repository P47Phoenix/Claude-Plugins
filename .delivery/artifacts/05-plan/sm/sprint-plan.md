# Sprint Plan: prd-quality-gate-flow Refactoring

**Version**: 1.1
**Author**: Aragorn (Scrum Master)
**Date**: 2026-03-30
**Status**: Committed
**Inputs**: User Stories v1.0 (Gandalf/PO), PRD v1.1, Design Spec v1.0 (Galadriel/UX)
**Project Type**: FEATURE (structural refactoring)
**Issues**: #51, #52, #53

> *"I do not know what strength is in my blood, but I swear to you I will not let the sprint fail."*

---

## 1. Sprint Goal

Decompose the `prd-quality-gate-flow` god object, eliminate duplicate entry points, and restructure flat scripts -- resolving issues #51, #52, and #53 in a single atomic PR with zero behavioral regression and zero new dependencies.

---

## 2. Capacity Declaration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Team size | 1 developer (solo) | Solo contributor; all roles handled by one person |
| Velocity baseline | 20 SP per sprint | **Assumed** velocity for solo Python refactoring (no historical data). This is real code (not markdown), so standard estimates apply per lesson #3. **Sprint 1 actuals will recalibrate Sprint 2/3 commitments -- see Section 2.3.** |
| 80% ceiling | 16 SP | Hard cap: 20 x 0.80 = 16 SP. No sprint may commit above this. |
| Sprint 1 commitment | 11 SP | 69% of ceiling -- buffer for transcription complexity (see Section 2.2) |
| Sprint 2 commitment | 16 SP | At ceiling -- entry verification + highest-risk story with buffer from recalibration (see Section 2.2) |
| Sprint 3 commitment | 7 SP | 44% of ceiling -- cleanup + dogfooding |
| Ceremony/interruption budget | 0 | Solo contributor, no PTO, no ceremonies |

### 2.1 Capacity Overcommitment Flag (Sprint 1)

The PO's user stories document allocates 27 SP to Sprint 1. Against a 20 SP baseline with an 80% ceiling of 16 SP, this is **169% of ceiling** -- a clear overcommitment and the #1 Plan stage failure mode per lesson #2.

**SM Resolution: Re-plan into 3 sprints.**

The dependency chain is strict (US-01 through US-11 are largely sequential), and the PO's story point estimates reflect genuine Python refactoring complexity. I will not reduce estimates to fit the ceiling -- that is dishonest forecasting. Instead, I redistribute the same 34 SP across 3 sprints, each within the 16 SP ceiling.

### 2.2 Revised Capacity Plan (3 Sprints)

| Sprint | Stories | SP | % of Ceiling | Status |
|--------|---------|---:|:------------:|--------|
| Sprint 1 | US-01, US-02, US-03, US-04 | 11 | 69% | Under ceiling (foundation work, additive-only, buffer for transcription complexity) |
| Sprint 2 | US-05, US-06, US-07 | 16 | 100% | At ceiling (US-05 completes data extraction, US-06 is highest-risk decomposition) |
| Sprint 3 | US-08, US-09, US-10, US-11 | 7 | 44% | Under ceiling (cleanup sprint + dogfooding validation) |
| **Total** | **11 stories** | **34** | | |

**Why US-05 moved to Sprint 2**: The challenger correctly identified that Sprint 1 at 100% ceiling with ungrounded velocity is riskier than claimed. US-05 (gate definitions with 20 business rules) involves transcribing 700+ lines of heterogeneous nested Python dicts -- the most error-prone extraction work. Moving it to Sprint 2 gives Sprint 1 a 31% buffer to absorb transcription issues in US-04, and US-05 lands in the same sprint as US-06 which consumes it -- zero dependency gap.

**Why Sprint 2 is at ceiling**: US-06 (Decompose PRDFlowBuilder) is the highest-risk story at 8 SP. Sprint 2 starts with US-05 (5 SP) which completes the data extraction, then US-06 consumes it immediately. US-07 (3 SP) follows. The entry verification step (Section 4) ensures Sprint 1 foundation is solid before committing. The fellowship does not march into Mordor blind.

**Why Sprint 1 is at 100% of revised ceiling**: All 4 stories are additive (new files) with zero modification of existing code except US-03 (1 SP wire-up of `shared.py` created in the same sprint). Risk is low -- no regression possible since no existing code changes. The ceiling is a guideline, not a wall, when the risk profile justifies it.

### 2.3 Velocity Recalibration Protocol

The 20 SP baseline is an assumption, not a measurement. No prior sprints exist for this codebase.

**Sprint 1 retrospective MUST recalibrate before Sprint 2 begins:**
- Measure actual Sprint 1 throughput (SP completed / time spent)
- If actual velocity < 16 SP: reduce Sprint 2/3 commitments proportionally
- If actual velocity >= 16 SP: Sprint 2/3 commitments stand as planned
- Document the recalibration decision in the retrospective artifact

---

## 3. Sprint 1: Foundation Modules (11 SP)

### Sprint 1 Goal

Create 3 new foundation modules (`shared.py`, `schema.py`, `stage_definitions.py`), wire the schema initialization contract, and create a `verify.py` verification script. At sprint end, all new modules import cleanly and pass their verification tests, but `prd_flow_builder.py` is not yet modified.

### Committed Stories

| Order | Story | Title | SP | Files Created | Files Modified |
|------:|-------|-------|----|---------------|----------------|
| 1 | US-01 | Create shared constants module | 2 | `shared.py` | -- |
| 2 | US-02 | Extract database schema to standalone module | 3 | `schema.py` | -- |
| 3 | US-03 | Wire schema initialization into shared connection helper | 1 | -- | `shared.py` |
| 4 | US-04 | Extract stage definitions into data module | 5 | `stage_definitions.py` | -- |

**Note**: US-05 (gate definitions) moved to Sprint 2 -- see Section 2.2.

### Sprint 1 Dependency Chain

```
US-01 (shared.py) ──> US-02 (schema.py) ──> US-03 (wire get_connection)
US-01 (shared.py) ──> US-04 (stage_definitions.py)   [parallel with US-02]
```

**Parallel opportunities**: After US-01 completes, US-02 and US-04 can proceed in parallel. US-03 requires US-02 to be done first.

### Sprint 1 Implementation Sequence

**Step 1: US-01 -- Create `shared.py`**
- Create `prd-quality-gate-flow/shared.py` with `DB_PATH`, `generate_timestamp_id()`, `ensure_utf8_output()`
- Verification: `python -c "from shared import DB_PATH; print(DB_PATH)"` prints `prd_flows.db`
- Risk: None (additive, no existing code touched)

**Step 2: US-02 -- Create `schema.py`**
- Extract `_create_schema()` body (lines 47-203 of `prd_flow_builder.py`) into `ensure_schema(conn)`
- SQL must be byte-identical to current implementation -- copy-paste, do not rewrite
- Verification: `python -c "import sqlite3; from schema import ensure_schema; c = sqlite3.connect(':memory:'); ensure_schema(c); tables = c.execute(\"SELECT count(*) FROM sqlite_master WHERE type='table'\").fetchone()[0]; assert tables == 9; print('OK')"` prints `OK`
- Risk: Medium -- schema SQL fidelity. Mitigation: character-by-character diff of SQL strings.

**Step 3: US-03 -- Wire `get_connection()`**
- Add `get_connection(db_path=DB_PATH)` to `shared.py` that calls `ensure_schema(conn)` before returning
- Verification: `python -c "from shared import get_connection; conn = get_connection(':memory:'); tables = conn.execute(\"SELECT count(*) FROM sqlite_master WHERE type='table'\").fetchone()[0]; assert tables == 9; print('OK')"` prints `OK`
- Risk: Low -- circular import concern is eliminated since `schema.py` has zero internal imports

**Step 4: US-04 -- Create `stage_definitions.py`** (can run parallel with Step 2)
- Extract 7 stage configs from `_create_stage1_creation` through `_create_stage7_completion`
- Use Python triple-quoted strings for multi-line `goal` prompts (PRD R6)
- Include load-time validation for required fields
- Verification: `python -c "from stage_definitions import STAGE_DEFINITIONS; assert len(STAGE_DEFINITIONS) == 7; print('OK')"` prints `OK`
- Risk: Medium -- multi-line goal string formatting. Mitigation: triple-quoted strings preserve formatting.

**Step 5: Create `verify.py` verification script** (after all stories complete)
- Single script that runs all Sprint 1 structural checks in sequence and reports pass/fail
- Checks: `shared.py` imports, `schema.py` table/index counts, `get_connection()` contract, `stage_definitions.py` count (7 stages)
- Extend in Sprint 2 to cover gate definitions, per-gate rule counts, and behavioral baselines
- Persist baselines to `baseline.json` rather than relying on session memory
- Add explicit database cleanup (`rm prd_flows.db`) before empirical test runs
- This is a verification script, not a test framework -- consistent with NFR-01 (zero new dependencies)

### Sprint 1 Exit Criteria

- [ ] `shared.py` exists with `DB_PATH`, `generate_timestamp_id()`, `ensure_utf8_output()`, `get_connection()`
- [ ] `schema.py` exists with `ensure_schema(conn)` producing 9 tables and 7 indexes
- [ ] `get_connection()` returns a connection with schema already initialized
- [ ] `stage_definitions.py` exports `STAGE_DEFINITIONS` with exactly 7 stage dicts
- [ ] `verify.py` exists and runs all Sprint 1 checks with pass/fail reporting
- [ ] All new modules have zero internal imports (leaf dependency rule)
- [ ] All new modules import only Python stdlib (NFR-01)
- [ ] No existing `.py` files modified (zero regression risk)
- [ ] Conventional commit per story (4 commits + verify.py commit)

---

## 4. Sprint 2: Data Extraction + Core Transformation (16 SP)

### Sprint 2 Goal

Complete the gate definitions extraction (US-05), execute the critical decomposition of `PRDFlowBuilder` from 1,157 lines to <=200 lines, then consolidate `prd_execute.py` as the canonical executor. At sprint end, `python prd_flow_builder.py` produces 15 nodes and 20 rules, matching the pre-refactoring baseline.

### Committed Stories

| Order | Story | Title | SP | Files Created/Modified |
|------:|-------|-------|----|------------------------|
| 1 | US-05 | Extract gate definitions and business rules into data module | 5 | `gate_definitions.py` (new) |
| 2 | US-06 | Decompose PRDFlowBuilder into thin orchestrator | 8 | `prd_flow_builder.py` (mod) |
| 3 | US-07 | Consolidate prd_execute.py as canonical executor | 3 | `prd_execute.py` (mod) |

### Sprint 2 Dependency Chain

```
US-05 (gate_definitions.py) ──> US-06 (decompose builder) ──> US-07 (consolidate executor)
```

No parallel opportunities -- strict sequential chain.

### Sprint 2 Implementation Sequence

**Step 0: Entry Verification (prerequisite -- 5 minutes)**
- Re-verify ALL Sprint 1 exit criteria before starting any Sprint 2 work
- Run `python verify.py` to confirm Sprint 1 modules are intact
- This eliminates context loss risk at the sprint boundary
- If any check fails: fix before proceeding (do NOT start US-05 on a broken foundation)

**Step 1: US-05 -- Create `gate_definitions.py`**
- Extract 7 gate configs with all 20 business rules
- Ordering must be explicit via list position (AC-02d)
- Include load-time validation for required gate and rule fields
- Verification: `python -c "from gate_definitions import GATE_DEFINITIONS; rules = sum(len(g['rules']) for g in GATE_DEFINITIONS); assert rules == 20; print('OK')"` prints `OK`
- **Per-gate rule count verification**: `[4, 4, 3, 1, 4, 3, 1]` -- must match exactly
- Risk: Medium -- transcription errors in nested rule condition dicts. Mitigation: copy-paste verbatim, verify per-gate rule distribution matches baseline.

**Step 2: Capture pre-refactoring baseline (prerequisite for US-06)**
- Run `python prd_flow_builder.py` and record: node count (expected: 15), rule count (expected: 20), flow structure from `export_flow_diagram()`, exit code
- **Persist baseline to `baseline.json`** via `verify.py` -- do not rely on session memory
- **Capture per-gate rule distribution**: `SELECT gate_node_id, COUNT(*) FROM business_rules WHERE flow_id = ? GROUP BY gate_node_id` -- expected: `[4, 4, 3, 1, 4, 3, 1]`
- This baseline is the P0 verification target for US-06

**Step 3: US-06 -- Decompose PRDFlowBuilder (THE critical step)**
- Replace `_create_schema()` with call to `ensure_schema(self.conn)`
- Replace `build_prd_flow()` with loops over `STAGE_DEFINITIONS` and `GATE_DEFINITIONS` via `PIPELINE_SEQUENCE`
- **PIPELINE_SEQUENCE irregularities** (must be handled explicitly in the loop):
  - Gates 3 and 4 are consecutive (no stage between them: stage3 -> gate3 -> gate4 -> stage4)
  - Stages 5 and 6 are consecutive (no gate between them: gate5 -> stage5 -> stage6 -> gate6)
  - Stage 3 uses `NodeType.CONTROL_FLOW` instead of `NodeType.AGENT` -- the sequence must carry node_type per entry
- Remove all 14 factory methods (`_create_stageN_*`, `_create_gateN_*`)
- Preserve public API: `create_flow()`, `create_node()`, `create_rule()`, `builder.conn`, `export_flow_diagram()`, `_count_nodes()`, `_count_rules()`, `close()`
- Replace all hardcoded `"prd_flows.db"` with `shared.DB_PATH`
- Replace inline timestamp ID generation with `shared.generate_timestamp_id()`
- Target: <=200 lines for class body
- Verification:
  - `wc -l` on class body <= 200
  - `python prd_flow_builder.py` produces 15 nodes, 20 rules (match baseline)
  - **Per-gate rule count verification (HARD GATE)**: distribution must equal `[4, 4, 3, 1, 4, 3, 1]`
  - **`export_flow_diagram()` output comparison (HARD GATE)**: diff against baseline diagram must show zero structural divergence
  - `grep -c '_create_stage\|_create_gate' prd_flow_builder.py` returns 0
  - `grep -c '"prd_flows.db"' prd_flow_builder.py` returns 0
  - Run `python verify.py` for automated pass/fail across all checks
- Risk: **HIGHEST** -- regression in node/rule creation order, missing rules, broken orchestration
- Mitigation: Atomic commit. Compare per-gate rule distribution + diagram output to baseline. If either differs, revert and investigate.
- **This step should be its own atomic commit.**

**Step 4: US-07 -- Consolidate prd_execute.py**
- Replace `"prd_flows.db"` with `shared.DB_PATH`
- Add `ensure_utf8_output()` call (absorb from `run_execute.py`)
- Verify `EXAMPLE_PRODUCT_IDEAS` exists only in `prd_execute.py`
- Verification:
  - `grep -c '"prd_flows.db"' prd_execute.py` returns 0
  - `python -c "import prd_execute; print('OK')"` succeeds
  - `grep -r 'EXAMPLE_PRODUCT_IDEAS' *.py | grep -v prd_execute.py` returns nothing

### Sprint 2 Exit Criteria

- [ ] `gate_definitions.py` exports `GATE_DEFINITIONS` with exactly 7 gates and 20 total rules
- [ ] Per-gate rule distribution matches `[4, 4, 3, 1, 4, 3, 1]` exactly
- [ ] `PRDFlowBuilder` class body is <=200 lines (`wc -l`)
- [ ] `build_prd_flow()` uses loops over data definitions, no factory methods remain
- [ ] Node count: 15, Rule count: 20 (match baseline)
- [ ] `export_flow_diagram()` output matches pre-refactoring baseline (hard gate)
- [ ] `builder.conn` accessible as public attribute
- [ ] Zero occurrences of `"prd_flows.db"` in `prd_flow_builder.py` and `prd_execute.py`
- [ ] `EXAMPLE_PRODUCT_IDEAS` exists in exactly one file (`prd_execute.py`)
- [ ] `prd_execute.py` calls `ensure_utf8_output()` in `main()`
- [ ] `business_rules_engine.py` and `flow_orchestrator.py` have zero diff (NFR-06)
- [ ] `verify.py` updated with Sprint 2 checks (per-gate counts, baseline comparison) and all checks pass
- [ ] Conventional commit per story (3 commits)

---

## 5. Sprint 3: Cleanup + Validation (7 SP)

### Sprint 3 Goal

Restructure remaining flat scripts, delete duplicate entry points, update documentation, and execute the P0 dogfooding validation gate. At sprint end, all 4 CLI entry points work, deleted scripts are gone, CLAUDE.md is current, and structural equivalence is confirmed.

### Committed Stories

| Order | Story | Title | SP | Files Modified/Deleted |
|------:|-------|-------|----|------------------------|
| 1 | US-08 | Restructure fix_and_run.py with named functions | 3 | `fix_and_run.py` (mod) |
| 2 | US-09 | Restructure check_db.py with functions and error handling | 2 | `check_db.py` (mod) |
| 3 | US-10 | Delete duplicate entry point scripts | 1 | `run_execute.py` (del), `run_builder.py` (del) |
| 4 | US-11 | Update CLAUDE.md entry points documentation | 1 | `CLAUDE.md` (mod) |

### Sprint 3 Dependency Chain

```
US-08 (fix_and_run.py) ──┐
US-09 (check_db.py)   ──┤──> US-10 (delete duplicates) ──> US-11 (update CLAUDE.md)
                         │
                    [parallel]
```

**Parallel opportunity**: US-08 and US-09 can proceed in parallel.

### Sprint 3 Implementation Sequence

**Step 1: US-08 -- Restructure `fix_and_run.py`** (parallel with Step 2)
- Extract `clean_incomplete_executions(db_path)` using `shared.get_connection()` -- fixes latent ordering bug
- Extract `demonstrate_bre_evaluation(builder, flow_id)`
- Extract `display_flow_structure(builder, flow_id)`
- Wrap in `main()` with `if __name__ == "__main__"` guard
- Replace `"prd_flows.db"` with `shared.DB_PATH`
- No bare top-level statements except imports and `if __name__` guard
- Verification: `python fix_and_run.py` runs to completion with exit code 0

**Step 2: US-09 -- Restructure `check_db.py`** (parallel with Step 1)
- Add descriptive functions: `list_flows()`, `list_nodes()`, `list_rules()` (or equivalently descriptive)
- Add `main()` with `if __name__ == "__main__"` guard
- Use `with` context manager for DB connection
- Graceful error when DB file does not exist (no raw stack trace)
- Replace `"prd_flows.db"` with `shared.DB_PATH`
- Verification: `python check_db.py` with nonexistent DB prints human-readable error

**Step 3: US-10 -- Delete duplicate scripts**
- Delete `run_execute.py` and `run_builder.py`
- Verify `grep -r 'run_execute\|run_builder' *.py` returns zero matches
- Verification: `ls run_execute.py run_builder.py 2>&1` reports "No such file or directory" for both

**Step 4: US-11 -- Update CLAUDE.md**
- Update `Running Scripts` section to list exactly 4 canonical scripts
- Remove any references to `run_execute.py` or `run_builder.py`
- Verification: `grep -c 'run_execute\|run_builder' CLAUDE.md` returns 0

**Step 5: Dogfooding Validation (P0 UAT Gate)**
- Run all 4 canonical CLI entry points:
  - `python prd_flow_builder.py` -- creates flow, prints counts and diagram
  - `python prd_execute.py` -- structural import test (full execution requires DB state)
  - `python check_db.py` -- inspects existing DB
  - `python fix_and_run.py` -- cleanup + BRE demo + flow display
- Structural equivalence check:
  - Node count matches baseline (15)
  - Rule count matches baseline (20)
  - Gate count matches baseline (7)
  - Flow structure preserved (stage/gate ordering)
  - Exit codes: 0 for all scripts
- Core module integrity: `git diff business_rules_engine.py flow_orchestrator.py` shows zero diff
- Hardcoded DB path eliminated: `grep -r '"prd_flows.db"' *.py` returns only `shared.py`

**This dogfooding gate is P0. The refactoring does not ship without it.**

### Sprint 3 Exit Criteria

- [ ] `fix_and_run.py` has `main()` guard, named functions, no bare top-level statements
- [ ] `check_db.py` has `main()` guard, descriptive functions, graceful error handling
- [ ] `run_execute.py` and `run_builder.py` deleted from disk
- [ ] Zero references to deleted scripts in any `.py` file
- [ ] CLAUDE.md lists exactly 4 canonical scripts for prd-quality-gate-flow
- [ ] All 4 CLI entry points run successfully (dogfooding)
- [ ] Structural equivalence confirmed (15 nodes, 20 rules, 7 gates)
- [ ] `business_rules_engine.py` and `flow_orchestrator.py` have zero diff
- [ ] `grep -r '"prd_flows.db"' *.py` matches only `shared.py`
- [ ] Conventional commit per story (4 commits)

---

## 6. Coverage Matrix

| PRD FR-ID | FR Description | Planned Task(s) | Story ID(s) | Sprint | Status |
|-----------|---------------|------------------|-------------|--------|--------|
| FR-01 | Extract stage definitions into data module | S1 Steps 4 | US-04 | S1 | Planned |
| FR-02 | Extract gate definitions into data module | S2 Step 1 | US-05 | S2 | Planned |
| FR-03 | Decompose PRDFlowBuilder class | S1 Steps 2-3, S2 Step 2 | US-02, US-03, US-06 | S1-S2 | Planned |
| FR-04 | Consolidate entry points | S2 Step 3, S3 Step 3 | US-07, US-10 | S2-S3 | Planned |
| FR-05 | Create shared constants module | S1 Steps 1, 3 | US-01, US-03 | S1 | Planned |
| FR-06 | Restructure fix_and_run.py | S3 Step 1 | US-08 | S3 | Planned |
| FR-07 | Restructure check_db.py | S3 Step 2 | US-09 | S3 | Planned |
| FR-08 | Update CLAUDE.md entry points | S3 Step 4 | US-11 | S3 | Planned |

**Unmapped FRs**: None. All 8 FRs mapped to at least one planned task.

---

## 7. Deployment Approach

- **Branching**: Feature branch `refactor/prd-quality-gate-decomposition` from `main`
- **Commit strategy**: One conventional commit per story (11 commits total), enabling clean revert per story
  - S1: `feat: create shared constants module (US-01)`
  - S1: `feat: extract database schema to schema.py (US-02)`
  - S1: `feat: wire schema initialization into get_connection (US-03)`
  - S1: `feat: extract stage definitions into data module (US-04)`
  - S1: `feat: add verify.py verification script`
  - S2: `feat: extract gate definitions and business rules into data module (US-05)`
  - S2: `refactor: decompose PRDFlowBuilder into thin orchestrator (US-06)`
  - S2: `refactor: consolidate prd_execute.py as canonical executor (US-07)`
  - S3: `refactor: restructure fix_and_run.py with named functions (US-08)`
  - S3: `refactor: restructure check_db.py with functions and error handling (US-09)`
  - S3: `chore: delete duplicate entry point scripts (US-10)`
  - S3: `docs: update CLAUDE.md entry points for prd-quality-gate-flow (US-11)`
- **PR**: Single atomic PR with all 12 commits (PRD R7: all changes in one PR, revert entire if regression found)
- **Post-merge**: No schema changes, no config migration. Closes #51, #52, #53.

---

## 8. Risks and Contingencies

| Risk | Likelihood | Impact | Sprint | Contingency |
|------|-----------|--------|--------|-------------|
| R1: Behavioral regression during US-06 decomposition | Medium | High | S2 | Pre-refactoring baseline captured. Structural equivalence check (15 nodes, 20 rules). Atomic commit enables clean revert. |
| R2: Stage/gate ordering bugs in data-driven loop | Medium | High | S2 | PIPELINE_SEQUENCE list makes ordering explicit. Verify `export_flow_diagram()` output matches baseline structure. |
| R3: Multi-line goal strings lose formatting in extraction | Medium | Medium | S1 | Python triple-quoted strings (not JSON). `repr()` comparison against original. |
| R4: Rule condition transcription errors | Medium | High | S2 | Copy-paste verbatim. Per-gate rule distribution must equal `[4,4,3,1,4,3,1]`. Automated check in `verify.py`. |
| R5: Schema SQL divergence | Low | High | S1 | Byte-identical copy-paste. Verify 9 tables, 7 indexes. Idempotent `CREATE TABLE IF NOT EXISTS`. |
| R6: Hardcoded DB path missed in some file | Low | Medium | S2-S3 | `grep -r '"prd_flows.db"'` as acceptance criterion. Must return only `shared.py`. |
| R7: US-06 takes longer than 8 SP estimate | Medium | Medium | S2 | Sprint 2 has 31% buffer (5 SP headroom). If still insufficient, US-07 slides to Sprint 3 (Sprint 3 is at 44% capacity). |
| R8: Partial merge leaves codebase in worse state | Low | High | S3 | Single atomic PR per PRD R7. Revert entire PR if regression in dogfooding. |

---

## 9. NFR Verification Plan

| NFR | Target | Verification Method | Sprint |
|-----|--------|---------------------|--------|
| NFR-01 | Zero external dependencies | `grep` for non-stdlib imports in every new/modified file | All |
| NFR-02 | Schema compatibility | Load pre-refactoring DB, run queries, compare results | S2 |
| NFR-03 | Python 3.9+ compatibility | Code review -- no walrus operator misuse, no 3.10+ features | All |
| NFR-04 | Behavioral compatibility | Structural equivalence: 15 nodes, 20 rules, 7 gates, matching flow structure, exit code 0 | S2-S3 |
| NFR-05 | File size <=300 lines (logic), data files may exceed with justification | `wc -l` on every modified/new file | All |
| NFR-06 | Core modules untouched | `git diff business_rules_engine.py flow_orchestrator.py` shows zero diff | S3 |

---

## 10. Sprint Summary

| Item | Detail |
|------|--------|
| Sprint goal | Decompose god object, eliminate duplicates, restructure flat scripts for prd-quality-gate-flow (#51, #52, #53) |
| Total stories | 11 (US-01 through US-11) |
| Total story points | 34 SP |
| Sprint count | 3 sprints |
| Sprint 1 | 11 SP -- Foundation modules (3 new files + verify.py, zero existing code modified) |
| Sprint 2 | 16 SP -- Gate extraction + core transformation (US-05, decompose builder, consolidate executor) |
| Sprint 3 | 7 SP -- Cleanup, deletion, docs, dogfooding |
| Capacity ceiling | 16 SP per sprint (80% of 20 SP baseline) |
| Max utilization | Sprint 2 at 100% (justified by entry verification + buffer from Sprint 1 recalibration) |
| Validation gate | Dogfooding (P0) -- all 4 CLI entry points with structural equivalence |
| Deployment | Single atomic PR, 12 conventional commits, closes #51/#52/#53 |
| Key constraint | Zero new dependencies (NFR-01), core modules untouched (NFR-06), behavioral compatibility (NFR-04) |

---

*"There is always hope." But hope is not a plan. This plan carries 34 story points across 3 sprints with velocity recalibration after Sprint 1, per-gate rule verification as a hard gate, and entry verification at every sprint boundary. The god object will fall. The duplicates will be purged. The flat scripts will stand upright with named functions. And at the end, the four canonical entry points will march in formation, each knowing its purpose. The fellowship has listened to its challengers, and is stronger for it.*
