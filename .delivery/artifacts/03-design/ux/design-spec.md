# UX Design Specification: prd-quality-gate-flow Decomposition

**Version**: 1.0
**Date**: 2026-03-30
**Designer**: Galadriel (UX Designer)
**PRD**: `.delivery/artifacts/02-refine/po/prd.md` v1.1
**Role**: Module structure, dependency flow, refactoring sequence, CLI entry point mapping

---

## 1. Current State Diagram

### 1.1 File Inventory (Verified via `ls -la` and `wc -l`)

| File | Lines | Role | Hardcoded `"prd_flows.db"` |
|------|------:|------|:--------------------------:|
| `prd_flow_builder.py` | 1,157 | God object: schema + builder + 12 factory methods + diagram export + `__main__` | 2 (line 41 default, line 1131 explicit) |
| `prd_execute.py` | 227 | Canonical executor: `execute_prd_workflow()` + `EXAMPLE_PRODUCT_IDEAS` + `main()` | 2 (lines 31, 51) |
| `run_execute.py` | 210 | **Duplicate** of `prd_execute.py` with UTF-8 wrapper | 2 (lines 63, 82) |
| `run_builder.py` | 44 | **Duplicate** of `prd_flow_builder.py` `__main__` block with UTF-8 wrapper | 1 (line 17) |
| `fix_and_run.py` | 214 | Flat procedural: DB cleanup + BRE demo + flow display. No functions. | 2 (lines 17, 40) |
| `check_db.py` | 27 | Bare top-level: DB inspection. No functions, no error handling. | 1 (line 4) |
| `business_rules_engine.py` | 569 | Core module (NOT MODIFIED) | 0 |
| `flow_orchestrator.py` | 598 | Core module (NOT MODIFIED) | 0 |

**Total hardcoded `"prd_flows.db"` in `.py` files**: 10 occurrences across 6 files (plus 3 in `.md` docs).

### 1.2 Current Dependency Graph

```
prd_flow_builder.py
  imports: json, sqlite3, enum, typing, datetime
  exports: PRDFlowBuilder, NodeType, WorkflowPattern
  consumers: prd_execute.py, run_execute.py, run_builder.py, fix_and_run.py

prd_execute.py
  imports: asyncio, json, sys, datetime
  imports from: prd_flow_builder (PRDFlowBuilder), flow_orchestrator (FlowOrchestrator), business_rules_engine (BusinessRulesEngine)
  consumers: CLI user

run_execute.py  [DUPLICATE - to be deleted]
  imports: sys, io, asyncio, json, datetime
  imports from: prd_flow_builder (PRDFlowBuilder), flow_orchestrator (FlowOrchestrator), business_rules_engine (BusinessRulesEngine)
  consumers: CLI user

run_builder.py  [DUPLICATE - to be deleted]
  imports: sys, io
  imports from: prd_flow_builder (PRDFlowBuilder)
  consumers: CLI user

fix_and_run.py
  imports: sqlite3, uuid, sys, io
  imports from: prd_flow_builder (PRDFlowBuilder), business_rules_engine (BusinessRulesEngine)
  consumers: CLI user

check_db.py
  imports: sqlite3
  consumers: CLI user
```

### 1.3 Current `PRDFlowBuilder` Internal Structure (1,157 lines)

| Line Range | Responsibility | Lines |
|------------|---------------|------:|
| 21-36 | `NodeType` + `WorkflowPattern` enums | 16 |
| 38-46 | `__init__` (connect + schema) | 9 |
| 47-203 | `_create_schema` (9 tables + 7 indexes) | 157 |
| 205-278 | `create_flow`, `create_node`, `create_rule` (public API) | 74 |
| 280-360 | `build_prd_flow` orchestration | 81 |
| 362-403 | `_create_stage1_creation` | 42 |
| 405-490 | `_create_gate1_completeness` (4 rules) | 86 |
| 492-612 | Stage 2 + Gate 2 (4 rules) | 121 |
| 614-751 | Stage 3 + Gate 3 (3 rules) + Gate 4 (1 rule) | 138 |
| 753-868 | Stage 4 + Gate 5 (4 rules) | 116 |
| 870-1001 | Stage 5 + Stage 6 + Gate 6 (3 rules) | 132 |
| 1003-1068 | Gate 7 (1 rule) + Stage 7 | 66 |
| 1070-1127 | `_count_nodes`, `_count_rules`, `export_flow_diagram`, `_get_node_depth`, `close` | 58 |
| 1129-1157 | `__main__` block | 29 |

**Total business rules across 7 gates**: 20 rules.
**Total stage/gate factory methods**: 14 (7 `_create_stageN_*` + 7 `_create_gateN_*`).

---

## 2. Target State Diagram

### 2.1 New File Structure

```
prd-quality-gate-flow/
  shared.py               [NEW]  ~40 lines   Constants + utilities
  schema.py               [NEW]  ~170 lines  Database schema creation
  stage_definitions.py    [NEW]  ~230 lines  7 stage dicts (data module)
  gate_definitions.py     [NEW]  ~280 lines  7 gate dicts + 20 rules (data module)
  prd_flow_builder.py     [MOD]  ~180 lines  Thin orchestrator (from 1,157)
  prd_execute.py          [MOD]  ~220 lines  Canonical executor (absorbs run_execute.py UTF-8 setup)
  fix_and_run.py          [MOD]  ~210 lines  Restructured with named functions + main()
  check_db.py             [MOD]  ~50 lines   Restructured with functions + error handling
  business_rules_engine.py [UNCHANGED] 569 lines
  flow_orchestrator.py     [UNCHANGED] 598 lines
  run_execute.py           [DELETED]
  run_builder.py           [DELETED]
```

### 2.2 Expected Line Counts and Verification

| File | Current | Target | Delta | NFR-05 Check |
|------|--------:|-------:|------:|:------------:|
| `shared.py` | 0 (new) | ~40 | +40 | PASS (<=300) |
| `schema.py` | 0 (new) | ~170 | +170 | PASS (<=300) |
| `stage_definitions.py` | 0 (new) | ~230 | +230 | PASS (data file, declarative) |
| `gate_definitions.py` | 0 (new) | ~280 | +280 | PASS (data file, declarative) |
| `prd_flow_builder.py` | 1,157 | ~180 | -977 | PASS (<=200 class body) |
| `prd_execute.py` | 227 | ~220 | -7 | PASS (<=300) |
| `fix_and_run.py` | 214 | ~210 | -4 | PASS (<=300) |
| `check_db.py` | 27 | ~50 | +23 | PASS (<=300) |
| `run_execute.py` | 210 | 0 | -210 | DELETED |
| `run_builder.py` | 44 | 0 | -44 | DELETED |

**Net line delta**: +230 + 280 + 170 + 40 - 977 - 7 - 4 + 23 - 210 - 44 = **-499 lines** (net reduction; complexity moved from one monolith to focused modules).

---

## 3. Module Dependency Graph

### 3.1 Target Import Relationships

```
                    shared.py
                   /    |    \
                  /     |     \
                 v      v      v
          schema.py   stage_definitions.py   gate_definitions.py
               \         |                  /
                \        |                 /
                 v       v                v
              prd_flow_builder.py
              (imports all 4 above)
                 |           |
                 v           v
          prd_execute.py   fix_and_run.py
          (imports shared,  (imports shared,
           prd_flow_builder, prd_flow_builder,
           flow_orchestrator, business_rules_engine)
           business_rules_engine)

          check_db.py
          (imports shared only)

          business_rules_engine.py  [UNCHANGED - no new imports]
          flow_orchestrator.py      [UNCHANGED - no new imports]
```

### 3.2 Module-by-Module Import Specification

**`shared.py`** (leaf node -- no internal imports):
```python
import sys, io, sqlite3
from datetime import datetime
# Exports: DB_PATH, generate_timestamp_id(), ensure_utf8_output(), get_connection()
```

**`schema.py`** (depends on: nothing internal):
```python
import sqlite3
# Exports: ensure_schema(conn)
```

**`stage_definitions.py`** (depends on: nothing internal):
```python
# Pure data module -- no imports needed
# Exports: STAGE_DEFINITIONS (list of 7 dicts), REQUIRED_STAGE_FIELDS (set)
```

**`gate_definitions.py`** (depends on: nothing internal):
```python
# Pure data module -- no imports needed
# Exports: GATE_DEFINITIONS (list of 7 dicts, each with embedded rules), REQUIRED_GATE_FIELDS (set), REQUIRED_RULE_FIELDS (set)
```

**`prd_flow_builder.py`** (depends on: shared, schema, stage_definitions, gate_definitions):
```python
import json, sqlite3
from datetime import datetime
from typing import Dict, Optional
from enum import Enum
from shared import DB_PATH, generate_timestamp_id, get_connection
from schema import ensure_schema
from stage_definitions import STAGE_DEFINITIONS, REQUIRED_STAGE_FIELDS
from gate_definitions import GATE_DEFINITIONS, REQUIRED_GATE_FIELDS, REQUIRED_RULE_FIELDS
# Exports: PRDFlowBuilder, NodeType, WorkflowPattern
```

**`prd_execute.py`** (depends on: shared, prd_flow_builder, flow_orchestrator, business_rules_engine):
```python
import asyncio, json, sys
from shared import DB_PATH, ensure_utf8_output
from prd_flow_builder import PRDFlowBuilder
from flow_orchestrator import FlowOrchestrator
from business_rules_engine import BusinessRulesEngine
# Exports: execute_prd_workflow(), EXAMPLE_PRODUCT_IDEAS, main()
```

**`fix_and_run.py`** (depends on: shared, prd_flow_builder, business_rules_engine):
```python
import sys
from shared import DB_PATH, ensure_utf8_output, get_connection
from prd_flow_builder import PRDFlowBuilder
from business_rules_engine import BusinessRulesEngine
# Exports: clean_incomplete_executions(), demonstrate_bre_evaluation(), display_flow_structure(), main()
```

**`check_db.py`** (depends on: shared):
```python
import sys
from shared import DB_PATH, get_connection
# Exports: list_flows(), list_nodes(), list_rules(), main()
```

### 3.3 Dependency Rules (constraints)

1. `shared.py`, `schema.py`, `stage_definitions.py`, `gate_definitions.py` must have **zero internal imports** (leaf modules).
2. `prd_flow_builder.py` imports from all 4 new modules but NOT from any consumer scripts.
3. Consumer scripts (`prd_execute.py`, `fix_and_run.py`, `check_db.py`) never import from each other.
4. `business_rules_engine.py` and `flow_orchestrator.py` have **zero diff** (NFR-06). Consumer call sites pass `shared.DB_PATH` or `shared.get_connection()` to these modules.
5. No circular dependencies exist in the target graph.

---

## 4. Refactoring Sequence

The order of operations matters. Each step must leave the codebase in a working state.

### Step 1: Create `shared.py` (Foundation)

**What**: Create new file with `DB_PATH`, `generate_timestamp_id()`, `ensure_utf8_output()`, `get_connection()`.
**Why first**: Every subsequent step depends on this module for the centralized constant.
**Verification**: `python -c "from shared import DB_PATH; print(DB_PATH)"` prints `prd_flows.db`.
**Risk**: None -- additive only, no existing code changed.
**Mitigation**: N/A (additive step).

### Step 2: Create `schema.py` (Extract schema from builder)

**What**: Extract `_create_schema()` body (lines 47-203 of current `prd_flow_builder.py`) into `ensure_schema(conn)` standalone function. This is 9 CREATE TABLE statements and 7 CREATE INDEX statements.
**Why second**: `get_connection()` in `shared.py` should call `ensure_schema()` to satisfy AC-03g. Wire that up after `schema.py` exists.
**Verification**: `python -c "import sqlite3; from schema import ensure_schema; conn = sqlite3.connect(':memory:'); ensure_schema(conn); print('OK')"`.
**Risk**: Schema SQL must be byte-identical to current `_create_schema()` body.
**Mitigation**: Copy-paste, do not rewrite. Diff the SQL strings character-by-character.

### Step 3: Wire `shared.get_connection()` to call `ensure_schema()`

**What**: Update `shared.py` so `get_connection(db_path=DB_PATH)` opens a connection, sets `row_factory`, and calls `ensure_schema(conn)` before returning.
**Why now**: Establishes the schema initialization contract (AC-03g) before any consumers are modified.
**Verification**: `python -c "from shared import get_connection; conn = get_connection(); print('OK'); conn.close()"`.
**Risk**: Circular import if `shared` imports `schema` and `schema` imports `shared`.
**Mitigation**: `schema.py` has zero internal imports (dependency rule 1). Safe.

### Step 4: Create `stage_definitions.py` (Extract stage data)

**What**: Extract 7 stage configurations from `_create_stage1_creation` through `_create_stage7_completion` into `STAGE_DEFINITIONS` list. Each dict mirrors the arguments currently passed to `create_node()`: `name`, `description`, `node_type`, `config`. Include load-time validation that required fields are present (AC-01e).
**Why now**: Data extraction is safe and additive. The builder still works with its old factory methods.
**Verification**: `python -c "from stage_definitions import STAGE_DEFINITIONS; print(len(STAGE_DEFINITIONS))"` prints `7`.
**Risk**: Multi-line goal strings may lose formatting.
**Mitigation**: Use Python triple-quoted strings (PRD R6). Test that `repr()` of each goal matches original.

### Step 5: Create `gate_definitions.py` (Extract gate data + rules)

**What**: Extract 7 gate configurations and their 20 embedded business rules into `GATE_DEFINITIONS` list. Each gate dict includes `name`, `description`, `gate_config`, and `rules` (list of rule dicts). The ordering of the list IS the stage-to-gate ordering (AC-02d). Include load-time validation (AC-02f).
**Why now**: Same pattern as Step 4 -- additive, no existing code changed yet.
**Verification**: `python -c "from gate_definitions import GATE_DEFINITIONS; rules = sum(len(g['rules']) for g in GATE_DEFINITIONS); print(f'Gates: {len(GATE_DEFINITIONS)}, Rules: {rules}')"` prints `Gates: 7, Rules: 20`.
**Risk**: Rule condition dicts with nested AND/OR logic are complex. Transcription errors.
**Mitigation**: Copy-paste condition dicts verbatim. Verify rule count matches `_count_rules()` output (20).

### Step 6: Decompose `prd_flow_builder.py` (The critical transformation)

**What**: Rewrite `PRDFlowBuilder` to:
- Import from `shared`, `schema`, `stage_definitions`, `gate_definitions`
- Replace `_create_schema()` with call to `ensure_schema(self.conn)`
- Replace `build_prd_flow()` body with loops over `STAGE_DEFINITIONS` and `GATE_DEFINITIONS`
- Remove all 14 `_create_stageN_*` / `_create_gateN_*` factory methods
- Keep `create_flow()`, `create_node()`, `create_rule()` as public API (AC-03d)
- Keep `self.conn` as public attribute (AC-03d2)
- Keep `export_flow_diagram()`, `_get_node_depth()`, `_count_nodes()`, `_count_rules()`, `close()` (AC-03e)
- Keep `__main__` block
- Target: <=200 lines for the class body (AC-03a)

**Why now**: All 4 new modules exist and are verified. The builder can switch from factory methods to data-driven loops.
**Verification**:
1. `wc -l` on class body <= 200
2. `python prd_flow_builder.py` creates flow with same node count (15) and rule count (20)
3. `python -c "from prd_flow_builder import PRDFlowBuilder; b = PRDFlowBuilder(':memory:'); fid = b.build_prd_flow(); print(b._count_nodes(fid), b._count_rules(fid)); b.close()"` prints `15 20`

**Risk**: Highest risk step. Regression in node/rule creation order, missing rules, broken `build_prd_flow()` logic.
**Mitigation**:
- Capture pre-refactoring baseline: `python prd_flow_builder.py` output (node count, rule count, flow structure)
- Post-refactoring: compare counts. Run `export_flow_diagram()` and diff structure (ignoring timestamp IDs).
- This step should be its own atomic commit.

### Step 7: Update `prd_execute.py` (Consolidate executor)

**What**:
- Add `ensure_utf8_output()` call (absorb from deleted `run_execute.py`)
- Replace `"prd_flows.db"` with `shared.DB_PATH`
- Replace `FlowOrchestrator("prd_flows.db", bre)` with `FlowOrchestrator(shared.DB_PATH, bre)`
- Keep `EXAMPLE_PRODUCT_IDEAS` here (OQ-4 decision: execution-specific data)
- Remove `from datetime import datetime` if unused after DB_PATH centralization

**Why now**: Builder is stable. Executor depends on builder.
**Verification**: `python prd_execute.py` runs without import errors (full execution requires DB state, so structural import test suffices).
**Risk**: Low. Straightforward import replacement.
**Mitigation**: `grep -r '"prd_flows.db"' prd_execute.py` returns zero after change.

### Step 8: Restructure `fix_and_run.py` (Extract functions)

**What**:
- Extract DB cleanup into `clean_incomplete_executions(db_path)` using `shared.get_connection()`
- Extract BRE demo into `demonstrate_bre_evaluation(builder, flow_id)`
- Extract flow display into `display_flow_structure(builder, flow_id)`
- Extract gate overview into `display_all_gates(builder, flow_id)`
- Wrap in `main()` with `if __name__ == "__main__"` guard
- Replace `"prd_flows.db"` with `shared.DB_PATH`
- Fix latent ordering bug (AC-03g): `clean_incomplete_executions()` now uses `shared.get_connection()` which calls `ensure_schema()`, so DELETE queries on a fresh DB will succeed instead of crashing.

**Why now**: Depends on `shared.py` and `prd_flow_builder.py` being stable.
**Verification**: `python fix_and_run.py` produces functionally equivalent output.
**Risk**: Function extraction may accidentally change execution order.
**Mitigation**: Keep function call order in `main()` identical to current top-level execution order.

### Step 9: Restructure `check_db.py` (Add structure + error handling)

**What**:
- Extract into `list_flows(conn)`, `list_nodes(conn)`, `list_rules(conn)` functions
- Add `main()` with `if __name__ == "__main__"` guard
- Add graceful error when DB file doesn't exist (AC-07d)
- Use `shared.get_connection()` instead of raw `sqlite3.connect()`

**Why now**: Simplest script. Depends only on `shared.py`.
**Verification**: `python check_db.py` against existing DB produces equivalent output. `rm /tmp/test.db && DB_PATH=/tmp/test.db python check_db.py` shows graceful error.
**Risk**: Minimal.
**Mitigation**: N/A.

### Step 10: Delete `run_execute.py` and `run_builder.py`

**What**: `git rm run_execute.py run_builder.py`
**Why last**: All functionality is confirmed working in canonical scripts before deletion.
**Verification**: `grep -r "run_execute\|run_builder" *.py` returns zero.
**Risk**: Low. OQ-1 decided: delete outright. No external consumers.
**Mitigation**: Git history preserves files for rollback.

### Step 11: Update CLAUDE.md (Documentation)

**What**: Update `Running Scripts` section to reflect 4 canonical entry points. Remove references to deleted files.
**Why last**: Documentation reflects the final stable state.
**Verification**: Manual review.
**Risk**: None.
**Mitigation**: N/A.

---

## 5. CLI Entry Point Mapping

### 5.1 Current to Target Mapping

| Current Command | Current File | Target Command | Target File | Change Type |
|----------------|--------------|----------------|-------------|-------------|
| `python prd_flow_builder.py` | `prd_flow_builder.py` (1,157 lines) | `python prd_flow_builder.py` | `prd_flow_builder.py` (~180 lines) | **Preserved** (same command, decomposed internals) |
| `python prd_execute.py` | `prd_execute.py` (227 lines) | `python prd_execute.py` | `prd_execute.py` (~220 lines) | **Preserved** (adds UTF-8 setup) |
| `python prd_execute.py saas_platform` | `prd_execute.py` | `python prd_execute.py saas_platform` | `prd_execute.py` | **Preserved** (argument handling unchanged) |
| `python run_execute.py` | `run_execute.py` (210 lines) | `python prd_execute.py` | `prd_execute.py` | **Consolidated** (duplicate removed) |
| `python run_builder.py` | `run_builder.py` (44 lines) | `python prd_flow_builder.py` | `prd_flow_builder.py` | **Consolidated** (duplicate removed) |
| `python fix_and_run.py` | `fix_and_run.py` (214 lines) | `python fix_and_run.py` | `fix_and_run.py` (~210 lines) | **Preserved** (restructured internals) |
| `python check_db.py` | `check_db.py` (27 lines) | `python check_db.py` | `check_db.py` (~50 lines) | **Preserved** (adds error handling) |

### 5.2 Behavioral Compatibility Matrix

| Entry Point | Output Structure | Exit Code | DB Side Effects | Compatibility |
|------------|-----------------|-----------|-----------------|:------------:|
| `python prd_flow_builder.py` | Flow ID + node/rule counts + diagram | 0 on success | Creates flow + nodes + rules | Structurally equivalent (IDs differ) |
| `python prd_execute.py` | Execution report + audit trail + gate evals | 0 on success | Creates execution records | Structurally equivalent (IDs differ) |
| `python fix_and_run.py` | Cleanup count + BRE demo + gate overview | 0 on success | Deletes incomplete executions | Structurally equivalent (formatting may differ) |
| `python check_db.py` | Flow/node/rule counts | 0 on success, graceful error on missing DB | Read-only | Equivalent + improved error handling |

---

## 6. FR Traceability Matrix

Every functional requirement (FR-01 through FR-08) is mapped to specific design elements, modules, and refactoring steps.

| FR | AC | Design Element | Target Module(s) | Refactoring Step | Verification Method |
|----|----|---------------|-------------------|:----------------:|-------------------|
| FR-01 | AC-01a | `STAGE_DEFINITIONS` list of 7 dicts | `stage_definitions.py` | Step 4 | File exists, `len(STAGE_DEFINITIONS) == 7` |
| FR-01 | AC-01b | Each stage dict has required fields: `name`, `description`, `node_type`, `config` (with subfields) | `stage_definitions.py` | Step 4 | Load-time validation raises `KeyError` on missing field |
| FR-01 | AC-01c | `build_prd_flow()` loops over `STAGE_DEFINITIONS` | `prd_flow_builder.py` | Step 6 | Code review: no `_create_stageN_*` methods exist |
| FR-01 | AC-01d | No YAML files, Python dicts only | `stage_definitions.py` | Step 4 | No `.yml`/`.yaml` files in plugin directory |
| FR-01 | AC-01e | `REQUIRED_STAGE_FIELDS` set + validation at import time | `stage_definitions.py` | Step 4 | `python -c "from stage_definitions import STAGE_DEFINITIONS"` succeeds; removing a field causes `KeyError` |
| FR-02 | AC-02a | `GATE_DEFINITIONS` list of 7 dicts with embedded `rules` | `gate_definitions.py` | Step 5 | File exists, `len(GATE_DEFINITIONS) == 7` |
| FR-02 | AC-02b | Each gate dict has `name`, `description`, `rules` (list of rule dicts with required fields) | `gate_definitions.py` | Step 5 | Load-time validation raises `KeyError` on missing field |
| FR-02 | AC-02c | `build_prd_flow()` loops over `GATE_DEFINITIONS` to create gates and rules | `prd_flow_builder.py` | Step 6 | Code review: no `_create_gateN_*` methods exist |
| FR-02 | AC-02d | Ordered list structure makes gate-to-stage ordering explicit | `gate_definitions.py` | Step 5 | List index corresponds to pipeline position |
| FR-02 | AC-02e | Total rule count matches current 20 | `gate_definitions.py` + `prd_flow_builder.py` | Steps 5, 6 | `_count_rules()` returns 20 after build |
| FR-02 | AC-02f | `REQUIRED_GATE_FIELDS` + `REQUIRED_RULE_FIELDS` sets with load-time validation | `gate_definitions.py` | Step 5 | Removing a required field causes `KeyError` at import |
| FR-03 | AC-03a | Class body <=200 lines | `prd_flow_builder.py` | Step 6 | `wc -l` from `class PRDFlowBuilder:` to end of class |
| FR-03 | AC-03b | `ensure_schema(conn)` standalone function | `schema.py` | Step 2 | `from schema import ensure_schema` succeeds |
| FR-03 | AC-03c | `build_prd_flow()` uses `for stage in STAGE_DEFINITIONS` / `for gate in GATE_DEFINITIONS` loops | `prd_flow_builder.py` | Step 6 | Code review: loop-based, not 12+ method calls |
| FR-03 | AC-03d | `create_flow()`, `create_node()`, `create_rule()` remain on `PRDFlowBuilder` | `prd_flow_builder.py` | Step 6 | `hasattr(PRDFlowBuilder, 'create_flow')` etc. |
| FR-03 | AC-03d2 | `builder.conn` remains as public attribute | `prd_flow_builder.py` | Step 6 | `b = PRDFlowBuilder(); assert hasattr(b, 'conn')` |
| FR-03 | AC-03e | `export_flow_diagram()` remains accessible | `prd_flow_builder.py` | Step 6 | `hasattr(PRDFlowBuilder, 'export_flow_diagram')` |
| FR-03 | AC-03f | Identical DB content (node counts, rule counts, flow structure) | `prd_flow_builder.py` | Step 6 | Pre/post comparison: 15 nodes, 20 rules |
| FR-03 | AC-03g | `schema.py` exposes `ensure_schema(conn)`, `shared.py` provides `get_connection()` that calls it | `schema.py` + `shared.py` | Steps 2, 3 | `get_connection()` on fresh DB succeeds; `fix_and_run.py` no longer crashes on fresh DB |
| FR-04 | AC-04a | `run_execute.py` deleted | N/A | Step 10 | File does not exist on disk |
| FR-04 | AC-04b | `run_builder.py` deleted | N/A | Step 10 | File does not exist on disk |
| FR-04 | AC-04c | `EXAMPLE_PRODUCT_IDEAS` in exactly one file | `prd_execute.py` | Step 7 | `grep -r EXAMPLE_PRODUCT_IDEAS *.py` returns 1 file |
| FR-04 | AC-04d | UTF-8 encoding setup consolidated | `shared.py` (`ensure_utf8_output()`) | Steps 1, 7 | `grep -r "TextIOWrapper" *.py` returns only `shared.py` |
| FR-05 | AC-05a | `DB_PATH`, `generate_timestamp_id()`, `ensure_utf8_output()` in `shared.py` | `shared.py` | Step 1 | `from shared import DB_PATH, generate_timestamp_id, ensure_utf8_output` succeeds |
| FR-05 | AC-05b | All `.py` files import `DB_PATH` from `shared.py` | All consumer files | Steps 7, 8, 9 | `grep -r 'from shared import' *.py` shows all consumers |
| FR-05 | AC-05c | `grep -r '"prd_flows.db"'` returns only `shared.py` | All `.py` files | Steps 6-9 | Grep verification |
| FR-05 | AC-05d | `generate_timestamp_id()` replaces inline patterns in modified files | `prd_flow_builder.py` | Step 6 | No `f"flow_{datetime.now()..."` in builder (only in `shared.py`) |
| FR-05 | AC-05e | Core modules continue using injected `db_path`/`db_connection` parameters | `business_rules_engine.py`, `flow_orchestrator.py` | N/A (unchanged) | Zero diff on core modules |
| FR-06 | AC-06a | `main()` + `if __name__ == "__main__"` guard | `fix_and_run.py` | Step 8 | `grep "def main" fix_and_run.py` + `grep "__name__" fix_and_run.py` |
| FR-06 | AC-06b | `clean_incomplete_executions(db_path)` function | `fix_and_run.py` | Step 8 | `grep "def clean_incomplete" fix_and_run.py` |
| FR-06 | AC-06c | `demonstrate_bre_evaluation(builder, flow_id)` function | `fix_and_run.py` | Step 8 | `grep "def demonstrate_bre" fix_and_run.py` |
| FR-06 | AC-06d | `display_flow_structure(builder, flow_id)` function | `fix_and_run.py` | Step 8 | `grep "def display_flow" fix_and_run.py` |
| FR-06 | AC-06e | No bare top-level statements except imports and `__name__` guard | `fix_and_run.py` | Step 8 | Manual code review |
| FR-06 | AC-06f | Functionally equivalent output | `fix_and_run.py` | Step 8 | Before/after structural comparison |
| FR-07 | AC-07a | `main()` + `if __name__ == "__main__"` guard | `check_db.py` | Step 9 | `grep "def main" check_db.py` |
| FR-07 | AC-07b | Descriptive function names | `check_db.py` | Step 9 | No single-letter function names |
| FR-07 | AC-07c | Context manager or explicit close | `check_db.py` | Step 9 | `grep "with\|finally" check_db.py` |
| FR-07 | AC-07d | Graceful error on missing DB | `check_db.py` | Step 9 | Test with nonexistent path |
| FR-07 | AC-07e | Equivalent output against existing DB | `check_db.py` | Step 9 | Before/after comparison |
| FR-08 | AC-08a | CLAUDE.md reflects final entry points | `CLAUDE.md` | Step 11 | Manual review |
| FR-08 | AC-08b | No references to deleted scripts | `CLAUDE.md` | Step 11 | `grep "run_execute\|run_builder" CLAUDE.md` returns zero |
| FR-08 | AC-08c | 4 canonical scripts documented | `CLAUDE.md` | Step 11 | Lists `prd_flow_builder.py`, `prd_execute.py`, `check_db.py`, `fix_and_run.py` |

**FR coverage**: All 8 FRs mapped. All 42 acceptance criteria mapped. Zero gaps.

---

## 7. Design Decisions

### OQ-2 Resolution: `export_flow_diagram()` Location

**Decision**: Keep `export_flow_diagram()` and `_get_node_depth()` on `PRDFlowBuilder`.

**Rationale**: These methods query the database via `self.conn` and logically belong on the builder which owns the connection. Extracting them to a utility would require passing a connection, adding complexity for no clear benefit. The builder class at ~180 lines has room for these ~40 lines within the 200-line target.

### OQ-4 Confirmation: `EXAMPLE_PRODUCT_IDEAS` Location

**Decision**: Keep in `prd_execute.py` per PO recommendation.

**Rationale**: This is execution-specific test data, not a shared constant. Placing it in `shared.py` would conflate infrastructure constants with domain test data.

### Build Order in `build_prd_flow()`

The interleaved stage-then-gate ordering in the current code is critical to the parent-child chaining (each gate's `parent_id` is the preceding stage, and each stage's `parent_id` is the preceding gate). The target design preserves this by interleaving the `STAGE_DEFINITIONS` and `GATE_DEFINITIONS` lists in `build_prd_flow()`:

```
Pipeline order (encoded in list positions):
  STAGE_DEFINITIONS[0] (Stage 1) -> parent: root
  GATE_DEFINITIONS[0]  (Gate 1)  -> parent: Stage 1 output
  STAGE_DEFINITIONS[1] (Stage 2) -> parent: Gate 1 output
  GATE_DEFINITIONS[1]  (Gate 2)  -> parent: Stage 2 output
  STAGE_DEFINITIONS[2] (Stage 3) -> parent: Gate 2 output
  GATE_DEFINITIONS[2]  (Gate 3)  -> parent: Stage 3 output
  GATE_DEFINITIONS[3]  (Gate 4)  -> parent: Gate 3 output  [consecutive gate]
  STAGE_DEFINITIONS[3] (Stage 4) -> parent: Gate 4 output
  GATE_DEFINITIONS[4]  (Gate 5)  -> parent: Stage 4 output
  STAGE_DEFINITIONS[4] (Stage 5) -> parent: Gate 5 output
  STAGE_DEFINITIONS[5] (Stage 6) -> parent: Stage 5 output [consecutive stage]
  GATE_DEFINITIONS[5]  (Gate 6)  -> parent: Stage 6 output
  GATE_DEFINITIONS[6]  (Gate 7)  -> parent: Gate 6 output  [consecutive gate]
  STAGE_DEFINITIONS[6] (Stage 7) -> parent: Gate 7 output
```

This non-trivial ordering means `build_prd_flow()` cannot simply alternate between the two lists. It must follow an explicit **pipeline sequence** list that defines the order:

```python
PIPELINE_SEQUENCE = [
    ("stage", 0), ("gate", 0), ("stage", 1), ("gate", 1),
    ("stage", 2), ("gate", 2), ("gate", 3), ("stage", 3),
    ("gate", 4), ("stage", 4), ("stage", 5), ("gate", 5),
    ("gate", 6), ("stage", 6),
]
```

This list lives in `prd_flow_builder.py` (not in the data modules) because it is orchestration logic, not data definition.

---

## 8. Risk Mitigations Summary

| Step | Risk | Mitigation | Rollback |
|:----:|------|-----------|----------|
| 1 | None (additive) | N/A | `git rm shared.py` |
| 2 | Schema SQL mismatch | Copy-paste, character-by-character diff | `git rm schema.py` |
| 3 | Circular import | `schema.py` has zero internal imports | Revert `shared.py` edit |
| 4 | Multi-line string formatting loss | Triple-quoted strings, `repr()` comparison | `git rm stage_definitions.py` |
| 5 | Rule transcription errors | Verify total count = 20, copy-paste conditions | `git rm gate_definitions.py` |
| 6 | **Behavioral regression** (highest risk) | Pre/post node count (15), rule count (20), flow structure comparison | `git checkout prd_flow_builder.py` |
| 7 | Import path errors | Run `python -c "import prd_execute"` | `git checkout prd_execute.py` |
| 8 | Execution order change | Keep `main()` call order identical to current top-level order | `git checkout fix_and_run.py` |
| 9 | Missing error path | Test with nonexistent DB | `git checkout check_db.py` |
| 10 | User confusion | CLAUDE.md updated in Step 11 | `git checkout run_execute.py run_builder.py` |
| 11 | Stale documentation | Cross-reference against actual file list | `git checkout CLAUDE.md` |

**Global rollback**: All changes in a single atomic PR (PRD R7). Revert entire PR if regression found during UAT.

---

## 9. Structural Equivalence Verification Plan

For dogfooding validation (P0 UAT gate), each CLI entry point must be verified:

| Entry Point | Pre-Refactoring Baseline | Post-Refactoring Check | Comparison |
|------------|-------------------------|----------------------|------------|
| `python prd_flow_builder.py` | Capture: node count (15), rule count (20), flow name, diagram structure | Same counts, same name, same diagram structure | `_count_nodes()` == 15, `_count_rules()` == 20 |
| `python prd_execute.py` | Capture: execution status, audit event count, gate eval count | Same structural metrics | Count-based comparison |
| `python fix_and_run.py` | Capture: cleanup operation, BRE evaluation structure, gate overview | Same operations execute, same gate count in overview | Functional equivalence |
| `python check_db.py` | Capture: flow count, node type breakdown, rule count | Same counts | Exact count match |

Timestamp-based IDs (`flow_*`, `node_*`, `rule_*`) are excluded from comparison per PRD NFR-04.
