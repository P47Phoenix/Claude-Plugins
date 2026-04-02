# Test Strategy: prd-quality-gate-flow Refactoring

**Version**: 1.0
**Author**: Legolas (QA Engineer, delivery-team)
**Date**: 2026-03-30
**Status**: Implementation-Ready
**Traces To**: PRD v1.1, User Stories v1.0 (11 stories, 42 ACs), Design Spec v1.0

> *"My eyes see far. That edge case you thought was unreachable -- I have already tested it."*
>
> This test strategy covers 11 user stories across 2 sprints, targeting a Python structural refactoring with zero behavioral changes. The testing approach is split between structural inspection (file existence, line counts, grep patterns, import verification) and empirical CLI execution (running Python scripts and comparing structural output). There is no test framework -- all verification is through CLI commands and manual inspection.

---

## 1. Testing Philosophy

Four principles govern this strategy:

1. **Structural refactoring gets structural tests.** The majority of ACs (32 of 42) can be verified by inspecting file existence, counting lines, grepping for patterns, and checking import statements. These do not require running the application.
2. **Behavioral compatibility gets empirical tests.** 10 ACs require actually running CLI commands and comparing output. Because timestamp-based IDs (`flow_*`, `node_*`, `rule_*`) are non-deterministic, comparison is by structural equivalence: node counts, rule counts, gate counts, flow structure, and exit codes. Direct stdout diff is not viable.
3. **Baselines before changes.** Pre-refactoring output baselines must be captured for all 4 CLI entry points before any code changes. Without baselines, behavioral compatibility cannot be verified. This is a P0 prerequisite.
4. **Core modules are untouchable.** `business_rules_engine.py` and `flow_orchestrator.py` must have zero diff after all changes. Any modification to these files is an automatic test failure, regardless of intent.

---

## 2. Pre-Refactoring Baseline Capture

Before any code changes, the following baselines must be captured in the `prd-quality-gate-flow/` directory. These are the reference points for all empirical tests.

| Baseline | Command | Captured Metrics |
|----------|---------|-----------------|
| BL-1: Builder output | `cd prd-quality-gate-flow && python prd_flow_builder.py` | Node count (expected: 15), rule count (expected: 20), flow name, diagram structure, exit code |
| BL-2: Executor import | `cd prd-quality-gate-flow && python -c "import prd_execute; print('OK')"` | Import succeeds, exit code 0 |
| BL-3: Fix-and-run output | `cd prd-quality-gate-flow && python fix_and_run.py` | Cleanup operation count, BRE evaluation structure, gate overview count, exit code |
| BL-4: Check-db output | `cd prd-quality-gate-flow && python check_db.py` | Flow count, node type breakdown, rule count, exit code |
| BL-5: Core module checksums | `sha256sum business_rules_engine.py flow_orchestrator.py` | SHA-256 hashes for NFR-06 verification |

**Storage**: Baselines are captured to stdout and recorded in the development session. They are not persisted as files.

---

## 3. Test Approach per Story

### 3.1 US-01: Create Shared Constants Module (`shared.py`)

**Approach**: Structural inspection + import verification

**Rationale**: All 4 ACs are structural -- they verify that specific exports exist, return expected values, and use only stdlib imports.

| AC | Type | Test Method |
|----|------|------------|
| AC-1.1 | Structural | `python -c "from shared import DB_PATH; assert DB_PATH == 'prd_flows.db'; print('PASS')"` |
| AC-1.2 | Structural | `python -c "from shared import generate_timestamp_id; ids = [generate_timestamp_id('test') for _ in range(3)]; assert all(i.startswith('test_') for i in ids); print('PASS')"` |
| AC-1.3 | Structural | `python -c "from shared import ensure_utf8_output; ensure_utf8_output(); print('PASS')"` |
| AC-1.4 | Structural | Grep `shared.py` for non-stdlib imports; expect zero matches |

**Regression concern**: None -- additive only, no existing code modified.

---

### 3.2 US-02: Extract Database Schema (`schema.py`)

**Approach**: Structural inspection + empirical schema verification

**Rationale**: AC-2.2 (table/index counts) and AC-2.3 (idempotency) require actual SQLite operations.

| AC | Type | Test Method |
|----|------|------------|
| AC-2.1 | Structural | `python -c "from schema import ensure_schema; print('OK')"` |
| AC-2.2 | Empirical | `python -c "import sqlite3; from schema import ensure_schema; c = sqlite3.connect(':memory:'); ensure_schema(c); tables = c.execute(\"SELECT count(*) FROM sqlite_master WHERE type='table'\").fetchone()[0]; assert tables == 9, f'Expected 9 tables, got {tables}'"` |
| AC-2.3 | Empirical | Call `ensure_schema(conn)` twice on same connection; no errors |
| AC-2.4 | Structural | Grep `schema.py` for non-stdlib imports; expect zero matches |

**Regression concern**: Schema SQL must produce identical tables and indexes as the current `_create_schema()`. Byte-for-byte fidelity of SQL statements.

---

### 3.3 US-03: Wire Schema into Shared Connection Helper

**Approach**: Empirical verification

**Rationale**: AC-3.1 requires demonstrating that `get_connection()` on a fresh database creates the full schema automatically.

| AC | Type | Test Method |
|----|------|------------|
| AC-3.1 | Empirical | `python -c "from shared import get_connection; conn = get_connection(':memory:'); tables = conn.execute(\"SELECT count(*) FROM sqlite_master WHERE type='table'\").fetchone()[0]; assert tables == 9; conn.close(); print('PASS')"` |
| AC-3.2 | Structural | `python -c "from shared import get_connection; print('OK')"` -- no ImportError |

**Regression concern**: Circular import risk between `shared.py` and `schema.py`. Verify `schema.py` has zero internal imports.

---

### 3.4 US-04: Extract Stage Definitions (`stage_definitions.py`)

**Approach**: Structural inspection + import verification

| AC | Type | Test Method |
|----|------|------------|
| AC-4.1 | Structural | `python -c "from stage_definitions import STAGE_DEFINITIONS; assert len(STAGE_DEFINITIONS) == 7; print('PASS')"` |
| AC-4.2 | Structural | `python -c "from stage_definitions import STAGE_DEFINITIONS; [s['config']['goal'] for s in STAGE_DEFINITIONS]; print('All goals present')"` |
| AC-4.3 | Empirical | Remove a required field from a stage dict, attempt import, verify `KeyError` is raised |
| AC-4.4 | Structural | Verify no `.yml`/`.yaml` data files exist in plugin directory |
| AC-4.5 | Empirical | Compare multi-line `goal` strings against original `prd_flow_builder.py` factory methods |
| AC-4.6 | Structural | Grep `stage_definitions.py` for imports from other plugin modules; expect zero |

**Regression concern**: Multi-line goal strings with triple-quoted formatting. Risk of whitespace corruption during extraction.

---

### 3.5 US-05: Extract Gate Definitions (`gate_definitions.py`)

**Approach**: Structural inspection + count verification

| AC | Type | Test Method |
|----|------|------------|
| AC-5.1 | Structural | `python -c "from gate_definitions import GATE_DEFINITIONS; assert len(GATE_DEFINITIONS) == 7; print('PASS')"` |
| AC-5.2 | Structural | `python -c "from gate_definitions import GATE_DEFINITIONS; rules = sum(len(g['rules']) for g in GATE_DEFINITIONS); assert rules == 20, f'Expected 20 rules, got {rules}'; print('PASS')"` |
| AC-5.3 | Structural | Verify every gate dict has `name`, `description`, `rules`; every rule dict has `name`, `rule_type`, `condition`, `action`, `priority` |
| AC-5.4 | Structural | Verify list ordering matches current `build_prd_flow()` gate creation order |
| AC-5.5 | Empirical | Remove a required field from a gate or rule dict, attempt import, verify `KeyError` |
| AC-5.6 | Structural | Grep `gate_definitions.py` for internal imports; expect zero |

**Regression concern**: Rule condition dicts with nested AND/OR logic. Transcription errors in complex conditions are the highest risk here.

---

### 3.6 US-06: Decompose PRDFlowBuilder

**Approach**: Mixed -- structural inspection + empirical build verification

**This is the highest-risk story.** The entire 1,157-line class is being rewritten. Every other consumer depends on this.

| AC | Type | Test Method |
|----|------|------------|
| AC-6.1 | Structural | Count lines from `class PRDFlowBuilder:` to end of class; assert <= 200 |
| AC-6.2 | Structural | `grep -c '_create_stage\|_create_gate' prd_flow_builder.py` returns `0` |
| AC-6.3 | Structural | Verify `create_flow()`, `create_node()`, `create_rule()` exist on class |
| AC-6.4 | Structural | `python -c "from prd_flow_builder import PRDFlowBuilder; b = PRDFlowBuilder(':memory:'); assert hasattr(b, 'conn'); b.close()"` |
| AC-6.5 | Structural | Verify `export_flow_diagram()` exists and is callable |
| AC-6.6 | **Empirical** | `python -c "from prd_flow_builder import PRDFlowBuilder; b = PRDFlowBuilder(':memory:'); fid = b.build_prd_flow(); assert b._count_nodes(fid) == 15; assert b._count_rules(fid) == 20; b.close(); print('PASS')"` |
| AC-6.7 | Structural | `grep -c '"prd_flows.db"' prd_flow_builder.py` returns `0` |
| AC-6.8 | Structural | `grep -c 'f"flow_{datetime.now' prd_flow_builder.py` returns `0` |
| AC-6.9 | Structural | Trace `PIPELINE_SEQUENCE` list against design spec section 7 ordering |

**Regression concern**: Node/rule creation order, parent-child chaining (each gate's `parent_id` must be the preceding stage, and vice versa). The consecutive gates (3-4) and consecutive stages (5-6) are the most likely failure points.

---

### 3.7 US-07: Consolidate prd_execute.py

**Approach**: Structural inspection

| AC | Type | Test Method |
|----|------|------------|
| AC-7.1 | Structural | `grep -c '"prd_flows.db"' prd_execute.py` returns `0`; `grep 'from shared import' prd_execute.py` finds `DB_PATH` |
| AC-7.2 | Structural | Verify `ensure_utf8_output()` call in `main()` |
| AC-7.3 | Structural | `grep -r 'EXAMPLE_PRODUCT_IDEAS' *.py` returns matches only in `prd_execute.py` |
| AC-7.4 | Structural | `python -c "import prd_execute; print('OK')"` succeeds |

**Regression concern**: UTF-8 setup absorption from deleted `run_execute.py`. Verify encoding works on non-ASCII output.

---

### 3.8 US-08: Restructure fix_and_run.py

**Approach**: Mixed -- structural + empirical execution

| AC | Type | Test Method |
|----|------|------------|
| AC-8.1 | Structural | `grep -c 'def main' fix_and_run.py` returns `1`; `grep '__name__' fix_and_run.py` confirms guard |
| AC-8.2 | Structural | Verify `clean_incomplete_executions()` function exists |
| AC-8.3 | Structural | Verify `demonstrate_bre_evaluation()` function exists |
| AC-8.4 | Structural | Verify `display_flow_structure()` function exists |
| AC-8.5 | Structural | Verify only imports and `if __name__` guard at top level |
| AC-8.6 | **Empirical** | Run `fix_and_run.py` against a fresh (non-existent) database; DELETE queries succeed because `get_connection()` calls `ensure_schema()` first |
| AC-8.7 | Structural | `grep -c '"prd_flows.db"' fix_and_run.py` returns `0` |
| AC-8.8 | **Empirical** | Run `python fix_and_run.py`; verify structurally equivalent output to BL-3 baseline |

**Regression concern**: The latent ordering bug fix (AC-8.6) changes behavior on fresh databases. This is an intentional improvement, not a regression. Verify the old behavior (crash on fresh DB) is gone.

---

### 3.9 US-09: Restructure check_db.py

**Approach**: Mixed -- structural + empirical execution

| AC | Type | Test Method |
|----|------|------------|
| AC-9.1 | Structural | `grep -c 'def main' check_db.py` returns `1` |
| AC-9.2 | Structural | Verify descriptive function names (`list_flows`, `list_nodes`, `list_rules` or equivalent) |
| AC-9.3 | Structural | Verify `with` context manager or `finally` block for connection |
| AC-9.4 | **Empirical** | Run `python check_db.py` with nonexistent DB path; verify graceful error message, no raw traceback |
| AC-9.5 | Structural | `grep -c '"prd_flows.db"' check_db.py` returns `0` |
| AC-9.6 | **Empirical** | Run `python check_db.py` against existing database; compare counts to BL-4 baseline |

**Regression concern**: Graceful error handling must not swallow legitimate errors from existing databases.

---

### 3.10 US-10: Delete Duplicate Entry Points

**Approach**: Structural inspection

| AC | Type | Test Method |
|----|------|------------|
| AC-10.1 | Structural | `ls run_execute.py 2>&1` returns "No such file or directory" |
| AC-10.2 | Structural | `ls run_builder.py 2>&1` returns "No such file or directory" |
| AC-10.3 | Structural | `grep -r 'run_execute\|run_builder' *.py` returns no output |

**Regression concern**: None -- deletion only. Git history preserves files.

---

### 3.11 US-11: Update CLAUDE.md

**Approach**: Structural inspection

| AC | Type | Test Method |
|----|------|------------|
| AC-11.1 | Structural | Verify `Running Scripts` section lists exactly 4 scripts |
| AC-11.2 | Structural | `grep -c 'run_execute\|run_builder' CLAUDE.md` returns `0` |
| AC-11.3 | Structural | Every `python <script>.py` in the section corresponds to an existing file |

**Regression concern**: Ensure no other sections of CLAUDE.md are inadvertently modified.

---

## 4. FR-by-FR Test Coverage Map

Every FR and AC from the PRD is mapped to a story, test approach, and specific verification command.

### FR-01: Extract Stage Definitions

| AC | Story | Approach | Verification |
|----|-------|----------|-------------|
| AC-01a | US-04 | Structural | `python -c "from stage_definitions import STAGE_DEFINITIONS"` succeeds; file exists |
| AC-01b | US-04 | Structural | Inspect each dict for required fields: `name`, `description`, `node_type`, `config.agent_type`, `config.goal`, `config.model`, `config.tools`, `config.working_memory_output`, `config.max_retries` |
| AC-01c | US-06 | Structural | `grep '_create_stageN' prd_flow_builder.py` returns 0; builder loops over `STAGE_DEFINITIONS` |
| AC-01d | US-04 | Structural | No `.yml`/`.yaml` data files in plugin directory |
| AC-01e | US-04 | Empirical | Remove required field, import fails with `KeyError` |

### FR-02: Extract Gate Definitions

| AC | Story | Approach | Verification |
|----|-------|----------|-------------|
| AC-02a | US-05 | Structural | `python -c "from gate_definitions import GATE_DEFINITIONS"` succeeds; file exists |
| AC-02b | US-05 | Structural | Every gate dict has `name`, `description`, `rules`; every rule dict has `name`, `rule_type`, `condition`, `action`, `priority` |
| AC-02c | US-06 | Structural | Builder loops over `GATE_DEFINITIONS`; no `_create_gateN` methods |
| AC-02d | US-05 | Structural | `GATE_DEFINITIONS` is an ordered list; index == pipeline position |
| AC-02e | US-05, US-06 | Empirical | `_count_rules(flow_id)` returns 20 after `build_prd_flow()` |
| AC-02f | US-05 | Empirical | Remove required field, import fails with `KeyError` |

### FR-03: Decompose PRDFlowBuilder

| AC | Story | Approach | Verification |
|----|-------|----------|-------------|
| AC-03a | US-06 | Structural | `wc -l` on class body <= 200 |
| AC-03b | US-02 | Structural | `from schema import ensure_schema` succeeds |
| AC-03c | US-06 | Structural | `build_prd_flow()` uses loops, not 12+ method calls |
| AC-03d | US-06 | Structural | `create_flow()`, `create_node()`, `create_rule()` exist on class |
| AC-03d2 | US-06 | Structural | `builder.conn` is a valid sqlite3.Connection |
| AC-03e | US-06 | Structural | `export_flow_diagram()` accessible |
| AC-03f | US-06 | Empirical | 15 nodes, 20 rules after build (compare to BL-1) |
| AC-03g | US-02, US-03 | Empirical | `get_connection(':memory:')` returns connection with 9 tables |

### FR-04: Consolidate Entry Points

| AC | Story | Approach | Verification |
|----|-------|----------|-------------|
| AC-04a | US-10 | Structural | `run_execute.py` does not exist |
| AC-04b | US-10 | Structural | `run_builder.py` does not exist |
| AC-04c | US-07 | Structural | `EXAMPLE_PRODUCT_IDEAS` in exactly one file (`prd_execute.py`) |
| AC-04d | US-07 | Structural | `ensure_utf8_output()` consolidated in `shared.py`; `grep TextIOWrapper *.py` returns only `shared.py` |

### FR-05: Create Shared Constants Module

| AC | Story | Approach | Verification |
|----|-------|----------|-------------|
| AC-05a | US-01 | Structural | `from shared import DB_PATH, generate_timestamp_id, ensure_utf8_output` succeeds |
| AC-05b | US-06, US-07, US-08, US-09 | Structural | All consumers `from shared import DB_PATH` |
| AC-05c | US-06, US-07, US-08, US-09 | Structural | `grep -r '"prd_flows.db"' *.py` returns only `shared.py` |
| AC-05d | US-06 | Structural | No inline `f"flow_{datetime.now..."` in modified files |
| AC-05e | N/A | N/A | Intentional scope boundary -- core modules unchanged (NFR-06) |

### FR-06: Restructure fix_and_run.py

| AC | Story | Approach | Verification |
|----|-------|----------|-------------|
| AC-06a | US-08 | Structural | `def main()` + `if __name__` guard |
| AC-06b | US-08 | Structural | `clean_incomplete_executions()` exists |
| AC-06c | US-08 | Structural | `demonstrate_bre_evaluation()` exists |
| AC-06d | US-08 | Structural | `display_flow_structure()` exists |
| AC-06e | US-08 | Structural | No bare top-level statements |
| AC-06f | US-08 | Empirical | `python fix_and_run.py` produces structurally equivalent output to BL-3 |

### FR-07: Restructure check_db.py

| AC | Story | Approach | Verification |
|----|-------|----------|-------------|
| AC-07a | US-09 | Structural | `def main()` + `if __name__` guard |
| AC-07b | US-09 | Structural | All functions have descriptive names |
| AC-07c | US-09 | Structural | Context manager or `finally` for connection |
| AC-07d | US-09 | Empirical | Graceful error on missing DB (no raw traceback) |
| AC-07e | US-09 | Empirical | Equivalent output against existing DB (compare to BL-4) |

### FR-08: Update CLAUDE.md

| AC | Story | Approach | Verification |
|----|-------|----------|-------------|
| AC-08a | US-11 | Structural | 4 canonical scripts listed |
| AC-08b | US-11 | Structural | No references to deleted scripts |
| AC-08c | US-11 | Structural | Every documented command maps to existing file |

---

## 5. Behavioral Compatibility Verification Plan

This is the P0 UAT gate. All 4 CLI entry points must produce structurally equivalent results before and after refactoring.

### 5.1 What "Structurally Equivalent" Means

| Dimension | Compared | NOT Compared | Rationale |
|-----------|----------|-------------|-----------|
| Node count | Yes | -- | Must be exactly 15 |
| Rule count | Yes | -- | Must be exactly 20 |
| Gate count | Yes | -- | Must be exactly 7 |
| Flow structure | Yes (stage/gate ordering, parent-child chain) | -- | Pipeline sequence must be preserved |
| Exit codes | Yes | -- | Must be 0 on success |
| Timestamp IDs | -- | NOT compared | `flow_*`, `node_*`, `rule_*` are non-deterministic per run |
| Stdout text | -- | NOT compared (except counts) | Formatting differences acceptable |
| Execution timing | -- | NOT compared | Performance is not a goal |

### 5.2 Entry Point Verification Matrix

| Entry Point | Pre-Refactoring Baseline | Post-Refactoring Check | Pass Criteria |
|------------|-------------------------|----------------------|--------------|
| `python prd_flow_builder.py` | BL-1: 15 nodes, 20 rules, diagram output, exit 0 | Same counts, diagram has same structure, exit 0 | `_count_nodes()` == 15, `_count_rules()` == 20 |
| `python prd_execute.py` | BL-2: Import succeeds, exit 0 | Import succeeds, exit 0 | `python -c "import prd_execute; print('OK')"` |
| `python fix_and_run.py` | BL-3: Cleanup + BRE demo + gate overview, exit 0 | Same operations execute, same gate count, exit 0 | Functional equivalence (formatting may differ) |
| `python check_db.py` | BL-4: Flow/node/rule counts, exit 0 | Same counts, exit 0 | Count-based comparison |

### 5.3 PIPELINE_SEQUENCE Verification

The non-trivial stage/gate ordering is the single highest-risk element. The expected sequence (from design spec section 7):

```
Stage 1 -> Gate 1 -> Stage 2 -> Gate 2 -> Stage 3 -> Gate 3 -> Gate 4 -> Stage 4 ->
Gate 5 -> Stage 5 -> Stage 6 -> Gate 6 -> Gate 7 -> Stage 7
```

Verification method: Read `PIPELINE_SEQUENCE` from `prd_flow_builder.py` and trace each `("stage", N)` / `("gate", N)` entry against the expected order above. Any deviation is a BLOCKING defect.

### 5.4 Parent-Child Chain Verification

After building a flow, query the database to verify parent-child relationships:

```python
# Verify parent chain: each node's parent_id matches the preceding node in PIPELINE_SEQUENCE
nodes = conn.execute("SELECT id, parent_id, name FROM flow_nodes WHERE flow_id = ? ORDER BY created_at", (flow_id,)).fetchall()
```

Each gate must have the preceding stage as its parent. Each stage (except Stage 1) must have the preceding gate as its parent. Stage 1's parent must be the root flow node.

---

## 6. Regression Detection Approach

### 6.1 Core Module Integrity (NFR-06)

**Method**: SHA-256 checksum comparison

```bash
# Pre-refactoring (BL-5):
sha256sum business_rules_engine.py flow_orchestrator.py

# Post-refactoring:
sha256sum business_rules_engine.py flow_orchestrator.py
```

**Pass criteria**: Identical checksums. Any difference is an automatic BLOCKING failure.

**Alternative**: `git diff business_rules_engine.py flow_orchestrator.py` shows zero diff.

### 6.2 Zero External Dependencies (NFR-01)

**Method**: Grep all new and modified `.py` files for non-stdlib imports.

```bash
grep -r '^import \|^from ' *.py | grep -v -E '(sqlite3|json|sys|io|datetime|typing|enum|asyncio|uuid|os|pathlib|textwrap)'
```

**Pass criteria**: Only imports from other plugin modules (`shared`, `schema`, `stage_definitions`, `gate_definitions`, `prd_flow_builder`, `flow_orchestrator`, `business_rules_engine`). No external packages.

### 6.3 Hardcoded DB Path Elimination (FR-05 / AC-05c)

**Method**: Grep sweep

```bash
grep -r '"prd_flows.db"' prd-quality-gate-flow/*.py
```

**Pass criteria**: Only `shared.py` contains the string `"prd_flows.db"`. Zero matches in all other files.

### 6.4 File Size Constraints (NFR-05)

| File | Max Lines | Type | Verification |
|------|----------|------|-------------|
| `shared.py` | 300 | Logic | `wc -l shared.py` |
| `schema.py` | 300 | Logic | `wc -l schema.py` |
| `stage_definitions.py` | No hard limit | Data (declarative dicts) | `wc -l` + manual review; excess must be declarative data |
| `gate_definitions.py` | No hard limit | Data (declarative dicts) | `wc -l` + manual review; excess must be declarative data |
| `prd_flow_builder.py` class body | 200 | Logic | Count from `class PRDFlowBuilder:` to end of class |
| `prd_flow_builder.py` total | 300 | Logic | `wc -l prd_flow_builder.py` |
| `prd_execute.py` | 300 | Logic | `wc -l prd_execute.py` |
| `fix_and_run.py` | 300 | Logic | `wc -l fix_and_run.py` |
| `check_db.py` | 300 | Logic | `wc -l check_db.py` |

### 6.5 Schema Compatibility (NFR-02)

**Method**: Load a pre-refactoring `prd_flows.db` with the post-refactoring code.

```bash
# 1. Run pre-refactoring builder to create prd_flows.db
# 2. Apply refactoring
# 3. Run post-refactoring check_db.py against the pre-refactoring DB
# 4. Verify counts match
```

**Pass criteria**: Pre-refactoring database loads and queries work identically with post-refactoring code. `CREATE TABLE IF NOT EXISTS` pattern makes schema creation idempotent.

### 6.6 Python 3.9+ Compatibility (NFR-03)

**Method**: Code review during development. Check for:
- No `match`/`case` statements (Python 3.10+)
- No `|` union type syntax in annotations (Python 3.10+)
- No `tomllib` usage (Python 3.11+)
- No `Self` type (Python 3.11+)

### 6.7 Deleted File Residual Check

**Method**: After US-10, verify no remaining references to deleted files.

```bash
grep -r 'run_execute\|run_builder' prd-quality-gate-flow/*.py
grep -r 'run_execute\|run_builder' CLAUDE.md
```

**Pass criteria**: Zero matches in both commands.

---

## 7. Risk-Based Test Prioritization

Tests are ordered by risk of defect and impact of failure.

### Priority 1: CRITICAL (execute first)

| Test Area | Risk | Impact | Why Critical |
|-----------|------|--------|-------------|
| AC-6.6: Node/rule count after decomposition | High | All consumers break | If `build_prd_flow()` produces wrong counts, every downstream operation (executor, BRE evaluation, gate checks) produces incorrect results. This is the single most important test. |
| AC-6.9: PIPELINE_SEQUENCE ordering | High | Silent data corruption | Wrong stage/gate ordering corrupts parent-child chain. Gates evaluate against wrong stages. No error, just wrong results. |
| NFR-06: Core modules untouched | High | Architectural violation | Any diff in `business_rules_engine.py` or `flow_orchestrator.py` is out of scope and may introduce regressions in the BRE or orchestrator. |
| AC-8.6: Fresh DB ordering bug fix | Medium | Crash on fresh databases | This is a known bug being fixed. Must verify the fix works AND does not break existing DB behavior. |

### Priority 2: HIGH (execute second)

| Test Area | Risk | Impact | Why High |
|-----------|------|--------|---------|
| AC-05c: Hardcoded DB path elimination | Medium | Shotgun surgery persists | If any file still hardcodes `"prd_flows.db"`, the centralization goal is defeated. |
| AC-6.1: Class line count <= 200 | Medium | God object persists | The primary decomposition goal. If the class is still > 200 lines, the refactoring has not achieved its purpose. |
| AC-4.5: Multi-line goal string fidelity | Medium | Agent behavior changes | If goal prompts are corrupted during extraction, pipeline agents receive different instructions. |
| AC-5.2: Total rule count == 20 | Medium | Gate evaluation changes | Missing or extra rules change which gates pass/fail. |

### Priority 3: MEDIUM (execute third)

| Test Area | Risk | Impact | Why Medium |
|-----------|------|--------|-----------|
| AC-7.1-7.4: prd_execute.py consolidation | Low | Entry point confusion | Low risk because changes are import replacements only. |
| AC-9.1-9.6: check_db.py restructuring | Low | Diagnostic tool degraded | Smallest file, simplest changes. |
| AC-10.1-10.3: File deletion | Low | Dead code remains | Trivial verification. |
| AC-11.1-11.3: CLAUDE.md update | Low | Documentation drift | Manual review. |

### Priority 4: LOW (execute last)

| Test Area | Risk | Impact | Why Low |
|-----------|------|--------|--------|
| Load-time validation (AC-01e, AC-02f, AC-4.3, AC-5.5) | Low | Missing validation | Failure means definitions are not validated at import, but runtime behavior is unaffected. |
| NFR-03: Python 3.9+ | Very Low | Version compat | Standard refactoring patterns are not version-sensitive. |
| NFR-05: File size limits | Very Low | Readability goal missed | Does not affect behavior. |

---

## 8. Test Execution Order

Execute in dependency order, respecting story dependencies and risk priority.

### Phase 1: Foundation Modules (US-01, US-02, US-03)

| # | Test | Story | Verification Commands |
|---|------|-------|----------------------|
| 1 | `shared.py` exports | US-01 | T-01.1, T-01.2, T-01.3 |
| 2 | `schema.py` table/index counts | US-02 | T-02.1, T-02.2, T-02.3 |
| 3 | `get_connection()` schema integration | US-03 | T-03.1, T-03.2 |

### Phase 2: Data Modules (US-04, US-05)

| # | Test | Story | Verification Commands |
|---|------|-------|----------------------|
| 4 | Stage definitions: count, fields, validation | US-04 | T-04.1, T-04.2, T-04.3 |
| 5 | Gate definitions: count, rules, fields, validation | US-05 | T-05.1, T-05.2, T-05.3 |

### Phase 3: Core Decomposition (US-06) -- CRITICAL PATH

| # | Test | Story | Verification Commands |
|---|------|-------|----------------------|
| 6 | **Node count == 15, Rule count == 20** | US-06 | T-06.1 (CRITICAL) |
| 7 | Class line count <= 200 | US-06 | T-06.3 |
| 8 | No factory methods remain | US-06 | T-06.4 |
| 9 | `builder.conn` preserved | US-06 | T-06.5 |
| 10 | `python prd_flow_builder.py` end-to-end | US-06 | T-06.2 |
| 11 | PIPELINE_SEQUENCE ordering | US-06 | Manual trace |
| 12 | Parent-child chain verification | US-06 | DB query |

### Phase 4: Consumer Scripts (US-07, US-08, US-09)

| # | Test | Story | Verification Commands |
|---|------|-------|----------------------|
| 13 | `prd_execute.py` imports, DB_PATH, EXAMPLE_PRODUCT_IDEAS | US-07 | T-07.1, T-07.2, T-07.3 |
| 14 | `fix_and_run.py` structure, functions, execution | US-08 | T-08.1, T-08.2, T-08.3, T-08.4 |
| 15 | `fix_and_run.py` fresh DB ordering bug fix | US-08 | T-08.3 on fresh DB (CRITICAL) |
| 16 | `check_db.py` structure, error handling, execution | US-09 | T-09.1, T-09.2, T-09.3, T-09.4 |

### Phase 5: Cleanup and Documentation (US-10, US-11)

| # | Test | Story | Verification Commands |
|---|------|-------|----------------------|
| 17 | Deleted files verification | US-10 | T-10.1, T-10.2 |
| 18 | CLAUDE.md entry points | US-11 | T-11.1, T-11.2 |

### Phase 6: Cross-Cutting Regression

| # | Test | Scope | Verification Commands |
|---|------|-------|----------------------|
| 19 | Core module checksums (NFR-06) | Global | `sha256sum` comparison to BL-5 |
| 20 | Zero external dependencies (NFR-01) | Global | Grep for non-stdlib imports |
| 21 | Hardcoded DB path sweep (FR-05) | Global | `grep -r '"prd_flows.db"' *.py` |
| 22 | File size constraints (NFR-05) | Global | `wc -l` on all new/modified files |
| 23 | Schema compatibility (NFR-02) | Global | Load pre-refactoring DB with post-refactoring code |
| 24 | Python 3.9+ compatibility (NFR-03) | Global | Code review |
| 25 | Deleted file residuals | Global | Grep for `run_execute`/`run_builder` |

### Phase 7: Behavioral Compatibility (P0 UAT Gate)

| # | Test | Scope | Verification |
|---|------|-------|-------------|
| 26 | `python prd_flow_builder.py` structural equivalence | BL-1 comparison | 15 nodes, 20 rules, diagram, exit 0 |
| 27 | `python prd_execute.py` import equivalence | BL-2 comparison | Import succeeds, exit 0 |
| 28 | `python fix_and_run.py` structural equivalence | BL-3 comparison | Cleanup + BRE + gates, exit 0 |
| 29 | `python check_db.py` structural equivalence | BL-4 comparison | Same counts, exit 0 |

---

## 9. Coverage Summary

| Metric | Count |
|--------|-------|
| Total FRs | 8 |
| Total ACs from PRD | 42 |
| ACs with structural tests | 32 (76%) |
| ACs with empirical tests | 10 (24%) |
| ACs with both | 0 |
| Total test cases from user stories | 37 |
| Total test cases mapped in this strategy | 37 (100%) |
| Additional regression tests | 7 (NFR checks) |
| Additional behavioral compatibility tests | 4 (P0 UAT gate) |
| Unmapped ACs | 0 |
| Unmapped FRs | 0 |

---

## 10. Pass/Fail Criteria

### Overall PASS

All of the following must be true:
1. All 37 test cases from user stories pass
2. All 7 NFR regression checks pass
3. All 4 behavioral compatibility checks pass (Phase 7)
4. Core module checksums match pre-refactoring baselines
5. `grep -r '"prd_flows.db"' *.py` returns only `shared.py`
6. `run_execute.py` and `run_builder.py` do not exist on disk

### Overall FAIL

Any of the following:
- Node count != 15 or rule count != 20 after `build_prd_flow()`
- `PRDFlowBuilder` class body > 200 lines
- Any diff in `business_rules_engine.py` or `flow_orchestrator.py`
- Any non-stdlib external import in new/modified files
- `builder.conn` is not accessible as a public attribute
- Any CLI entry point crashes with a non-zero exit code
- Pre-refactoring database fails to load with post-refactoring code

### Failure Protocol

1. Log defect: which test failed, expected vs actual, file and line reference
2. Fix the code in the affected module
3. Re-run the failed test AND all tests in the same phase
4. Re-run Phase 6 (cross-cutting regression) to verify fix did not introduce new issues
5. If Phase 7 (behavioral compatibility) was reached before failure: re-run from Phase 7

### Atomic PR Requirement

Per PRD R7: All changes must land in a single atomic PR. If any Phase 7 behavioral compatibility test fails after all code changes are complete, the correct action is to revert the entire PR and diagnose, not to patch individual files.
