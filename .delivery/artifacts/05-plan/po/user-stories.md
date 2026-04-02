# User Stories: prd-quality-gate-flow Refactoring

**Version**: 1.0
**Date**: 2026-03-30
**Author**: Product Owner (Gandalf)
**PRD**: v1.1 | **Design Spec**: v1.0
**Issues**: #51 (God object), #52 (Duplicate entry points), #53 (Missing function structure)

> "Even the smallest refactoring can change the course of the codebase."

---

## Capacity Declaration

| Parameter | Value |
|-----------|-------|
| Velocity baseline | Solo developer, Python refactoring |
| Capacity ceiling | 80% (hard cap -- do NOT overcommit) |
| Total estimated points | 34 SP |
| Sprint commitment (80%) | 27 SP |
| Sprint count | 2 sprints (Sprint 1: 27 SP, Sprint 2: 7 SP) |
| Estimation basis | Standard Python code refactoring estimates (this is CODE, not markdown) |

---

## Dependency Chain

Stories must be completed in this order. The dependency chain mirrors the 11-step safe refactoring sequence from the design spec.

```
US-01 (shared.py)
  |
  +---> US-02 (schema.py) ---> US-03 (wire get_connection)
  |
  +---> US-04 (stage_definitions.py) ---+
  |                                      |
  +---> US-05 (gate_definitions.py) ----+
                                         |
                                         v
                                    US-06 (decompose PRDFlowBuilder)
                                         |
                          +--------------+--------------+
                          |              |              |
                          v              v              v
                     US-07           US-08           US-09
                 (prd_execute.py) (fix_and_run.py)  (check_db.py)
                          |              |              |
                          +--------------+--------------+
                                         |
                                         v
                                    US-10 (delete duplicates)
                                         |
                                         v
                                    US-11 (update CLAUDE.md)
```

**Critical path**: US-01 -> US-02 -> US-03 -> US-04 -> US-05 -> US-06 -> US-10 -> US-11

**Parallel opportunities**:
- US-04 and US-05 can be done in parallel after US-01
- US-07, US-08, and US-09 can be done in parallel after US-06

---

## Sprint Allocation

### Sprint 1 (27 SP) -- Foundation + Core Transformation

| Story | Points | Rationale |
|-------|-------:|-----------|
| US-01 | 2 | Small new file, well-defined contents |
| US-02 | 3 | Careful SQL extraction, byte-for-byte fidelity required |
| US-03 | 1 | Wiring call, small edit to existing file |
| US-04 | 5 | Extract 7 stage configs with multi-line strings, add validation |
| US-05 | 5 | Extract 7 gate dicts + 20 business rules, add validation |
| US-06 | 8 | Highest risk: rewrite 1,157-line class to <=200 lines |
| US-07 | 3 | Import replacements + absorb UTF-8 setup |
| **Total** | **27** | **80% of 34 SP capacity** |

### Sprint 2 (7 SP) -- Restructuring + Cleanup + Documentation

| Story | Points | Rationale |
|-------|-------:|-----------|
| US-08 | 3 | Extract 4+ functions, fix latent ordering bug |
| US-09 | 2 | Small file, add functions + error handling |
| US-10 | 1 | Delete 2 files, verify no references |
| US-11 | 1 | Documentation update |
| **Total** | **7** | |

---

## Story Index

| Story | Description | Sprint | Points | FRs Covered |
|-------|-------------|--------|-------:|-------------|
| US-01 | Create shared constants module | S1 | 2 | FR-05 |
| US-02 | Extract database schema to standalone module | S1 | 3 | FR-03 |
| US-03 | Wire schema initialization into shared connection helper | S1 | 1 | FR-03, FR-05 |
| US-04 | Extract stage definitions into data module | S1 | 5 | FR-01 |
| US-05 | Extract gate definitions and business rules into data module | S1 | 5 | FR-02 |
| US-06 | Decompose PRDFlowBuilder into thin orchestrator | S1 | 8 | FR-01, FR-02, FR-03, FR-05 |
| US-07 | Consolidate prd_execute.py as canonical executor | S1 | 3 | FR-04, FR-05 |
| US-08 | Restructure fix_and_run.py with named functions | S2 | 3 | FR-06, FR-05 |
| US-09 | Restructure check_db.py with functions and error handling | S2 | 2 | FR-07, FR-05 |
| US-10 | Delete duplicate entry point scripts | S2 | 1 | FR-04 |
| US-11 | Update CLAUDE.md entry points documentation | S2 | 1 | FR-08 |

---

## US-01: Create Shared Constants Module

**FR Coverage**: FR-05 (AC-05a, AC-05b partial, AC-05c partial, AC-05d partial)
**Design Spec Step**: 1
**Sprint**: 1 | **Story Points**: 2

### Description

**As a** plugin maintainer,
**I want** a `shared.py` module containing `DB_PATH`, `generate_timestamp_id()`, and `ensure_utf8_output()`,
**So that** constants and utilities are defined once and never hardcoded across multiple files.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-1.1 | **Given** the prd-quality-gate-flow plugin directory, **When** I run `python -c "from shared import DB_PATH; print(DB_PATH)"`, **Then** the output is `prd_flows.db` | structural |
| AC-1.2 | **Given** shared.py has been created, **When** I call `generate_timestamp_id("flow")`, **Then** the returned string starts with `flow_` followed by a timestamp in `YYYYMMDD_HHMMSS` format | structural |
| AC-1.3 | **Given** shared.py has been created, **When** I call `ensure_utf8_output()`, **Then** `sys.stdout` and `sys.stderr` are wrapped in UTF-8 `TextIOWrapper` instances | structural |
| AC-1.4 | **Given** shared.py exists, **When** I inspect its import statements, **Then** only Python standard library modules are imported (sys, io, datetime, sqlite3) and there are zero imports from other plugin modules | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-01.1 | AC-1.1, AC-1.2, AC-1.3 | `python -c "from shared import DB_PATH, generate_timestamp_id, ensure_utf8_output; print('OK')"` | Prints `OK`, exit code 0 |
| T-01.2 | AC-1.2 | `python -c "from shared import generate_timestamp_id; ids = [generate_timestamp_id('test') for _ in range(3)]; assert all(i.startswith('test_') for i in ids); print('OK')"` | Prints `OK` -- all IDs have correct prefix |
| T-01.3 | AC-1.1 | `python -c "from shared import DB_PATH; assert DB_PATH == 'prd_flows.db'; print('PASS')"` | Prints `PASS` |

### Dependencies

- None (foundation module -- first story in sequence)

---

## US-02: Extract Database Schema to Standalone Module

**FR Coverage**: FR-03 (AC-03b, AC-03g partial)
**Design Spec Step**: 2
**Sprint**: 1 | **Story Points**: 3

### Description

**As a** plugin maintainer,
**I want** the database schema creation logic extracted from `PRDFlowBuilder` into a standalone `schema.py` module,
**So that** schema initialization can be called independently without instantiating the entire builder class.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-2.1 | **Given** the prd-quality-gate-flow plugin directory, **When** I run `python -c "from schema import ensure_schema; print('OK')"`, **Then** it prints `OK` with exit code 0 | structural |
| AC-2.2 | **Given** an in-memory SQLite database, **When** I call `ensure_schema(conn)`, **Then** exactly 9 tables and 7 indexes are created, matching the current `_create_schema()` output byte-for-byte in SQL | structural |
| AC-2.3 | **Given** an existing database with schema already applied, **When** I call `ensure_schema(conn)` a second time, **Then** no errors occur (CREATE TABLE IF NOT EXISTS pattern) | structural |
| AC-2.4 | **Given** schema.py exists, **When** I inspect its import statements, **Then** it imports only `sqlite3` from the standard library and has zero imports from other plugin modules | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-02.1 | AC-2.2 | `python -c "import sqlite3; from schema import ensure_schema; c = sqlite3.connect(':memory:'); ensure_schema(c); tables = c.execute(\"SELECT count(*) FROM sqlite_master WHERE type='table'\").fetchone()[0]; print(f'Tables: {tables}'); assert tables == 9"` | `Tables: 9` |
| T-02.2 | AC-2.3 | `python -c "import sqlite3; from schema import ensure_schema; c = sqlite3.connect(':memory:'); ensure_schema(c); ensure_schema(c); print('Idempotent: OK')"` | `Idempotent: OK` -- no errors on double call |
| T-02.3 | AC-2.2 | `python -c "import sqlite3; from schema import ensure_schema; c = sqlite3.connect(':memory:'); ensure_schema(c); indexes = c.execute(\"SELECT count(*) FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'\").fetchone()[0]; print(f'Indexes: {indexes}'); assert indexes == 7"` | `Indexes: 7` |

### Dependencies

- US-01 (shared.py must exist, though schema.py does not import from it directly)

---

## US-03: Wire Schema Initialization into Shared Connection Helper

**FR Coverage**: FR-03 (AC-03g), FR-05 (AC-05a partial)
**Design Spec Step**: 3
**Sprint**: 1 | **Story Points**: 1

### Description

**As a** plugin maintainer,
**I want** `shared.get_connection()` to automatically call `ensure_schema()` before returning a connection,
**So that** any code path that opens a database connection is guaranteed to have the schema initialized, preventing the latent fresh-database crash bug in `fix_and_run.py`.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-3.1 | **Given** a fresh database file that does not yet exist, **When** I call `shared.get_connection(db_path)` for the first time, **Then** the returned connection has all 9 tables and 7 indexes already created | structural |
| AC-3.2 | **Given** shared.py imports from schema.py, **When** I run `python -c "from shared import get_connection; print('OK')"`, **Then** it succeeds with no ImportError (schema.py has zero internal imports, no circular dependency) | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-03.1 | AC-3.1 | `python -c "from shared import get_connection; conn = get_connection(':memory:'); tables = conn.execute(\"SELECT count(*) FROM sqlite_master WHERE type='table'\").fetchone()[0]; print(f'Tables: {tables}'); assert tables == 9; conn.close()"` | `Tables: 9` |
| T-03.2 | AC-3.1 | `python -c "from shared import get_connection; conn = get_connection(':memory:'); conn.execute('DELETE FROM flow_executions WHERE 1=0'); print('Schema preloaded: OK'); conn.close()"` | `Schema preloaded: OK` -- DELETE on fresh DB succeeds because schema exists |

### Dependencies

- US-01 (shared.py must exist)
- US-02 (schema.py must exist with `ensure_schema()`)

---

## US-04: Extract Stage Definitions into Data Module

**FR Coverage**: FR-01 (AC-01a, AC-01b, AC-01c partial, AC-01d, AC-01e)
**Design Spec Step**: 4
**Sprint**: 1 | **Story Points**: 5

### Description

**As a** plugin maintainer,
**I want** all 7 stage definitions extracted into a `stage_definitions.py` data module as Python dicts,
**So that** I can add or modify pipeline stages by editing declarative data without touching the builder class.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-4.1 | **Given** stage_definitions.py has been created, **When** I run `python -c "from stage_definitions import STAGE_DEFINITIONS; print(len(STAGE_DEFINITIONS))"`, **Then** the output is `7` | structural |
| AC-4.2 | **Given** STAGE_DEFINITIONS is loaded, **When** I inspect each stage dict, **Then** every dict contains: `name`, `description`, `node_type`, and `config` (with subfields `agent_type`, `goal`, `model`, `tools`, `working_memory_output`, `max_retries`) | structural |
| AC-4.3 | **Given** a stage dict with a required field removed, **When** the module is imported, **Then** a `KeyError` is raised at import time identifying the missing field | empirical |
| AC-4.4 | **Given** stage_definitions.py uses Python dicts, **When** I check the plugin directory for .yml or .yaml files, **Then** no YAML data files exist for stage definitions | structural |
| AC-4.5 | **Given** stage definitions contain multi-line `goal` prompts, **When** extracted to Python triple-quoted strings, **Then** the content of each goal preserves the original formatting from prd_flow_builder.py | empirical |
| AC-4.6 | **Given** stage_definitions.py exists, **When** I inspect its import statements, **Then** it has zero imports from other plugin modules (pure data module) | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-04.1 | AC-4.1, AC-4.2 | `python -c "from stage_definitions import STAGE_DEFINITIONS, REQUIRED_STAGE_FIELDS; print(f'Stages: {len(STAGE_DEFINITIONS)}, Required fields: {len(REQUIRED_STAGE_FIELDS)}'); assert len(STAGE_DEFINITIONS) == 7"` | `Stages: 7, Required fields: N` (N >= 4) |
| T-04.2 | AC-4.2 | `python -c "from stage_definitions import STAGE_DEFINITIONS; [s['config']['goal'] for s in STAGE_DEFINITIONS]; print('All goals present: OK')"` | `All goals present: OK` -- no KeyError |
| T-04.3 | AC-4.4 | Verify `stage_definitions.py` contains no `.yml`/`.yaml` references and no `import yaml` | No YAML usage found |

### Dependencies

- US-01 (shared.py exists; stage_definitions.py does not import it but is part of the same module graph)

---

## US-05: Extract Gate Definitions and Business Rules into Data Module

**FR Coverage**: FR-02 (AC-02a, AC-02b, AC-02c partial, AC-02d, AC-02e, AC-02f)
**Design Spec Step**: 5
**Sprint**: 1 | **Story Points**: 5

### Description

**As a** plugin maintainer,
**I want** all 7 gate definitions and their 20 business rules extracted into a `gate_definitions.py` data module,
**So that** I can add or modify quality gates and their rules declaratively without touching the builder class.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-5.1 | **Given** gate_definitions.py has been created, **When** I run `python -c "from gate_definitions import GATE_DEFINITIONS; print(len(GATE_DEFINITIONS))"`, **Then** the output is `7` | structural |
| AC-5.2 | **Given** GATE_DEFINITIONS is loaded, **When** I sum all rules across all gate dicts, **Then** the total is exactly 20 rules | structural |
| AC-5.3 | **Given** GATE_DEFINITIONS is loaded, **When** I inspect each gate dict, **Then** every dict contains: `name`, `description`, and `rules` (list of rule dicts), and every rule dict contains: `name`, `rule_type`, `condition`, `action`, `priority` | structural |
| AC-5.4 | **Given** GATE_DEFINITIONS is an ordered list, **When** I inspect the list structure, **Then** the list index corresponds to the pipeline position, matching the ordering in the current `build_prd_flow()` method | structural |
| AC-5.5 | **Given** a gate dict or rule dict with a required field removed, **When** the module is imported, **Then** a `KeyError` is raised at import time identifying the missing field | empirical |
| AC-5.6 | **Given** gate_definitions.py exists, **When** I inspect its import statements, **Then** it has zero imports from other plugin modules (pure data module) | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-05.1 | AC-5.1, AC-5.2 | `python -c "from gate_definitions import GATE_DEFINITIONS; rules = sum(len(g['rules']) for g in GATE_DEFINITIONS); print(f'Gates: {len(GATE_DEFINITIONS)}, Rules: {rules}'); assert rules == 20"` | `Gates: 7, Rules: 20` |
| T-05.2 | AC-5.3 | `python -c "from gate_definitions import GATE_DEFINITIONS, REQUIRED_GATE_FIELDS, REQUIRED_RULE_FIELDS; print(f'Gate fields: {REQUIRED_GATE_FIELDS}'); print(f'Rule fields: {REQUIRED_RULE_FIELDS}')"` | Prints both field sets |
| T-05.3 | AC-5.3 | `python -c "from gate_definitions import GATE_DEFINITIONS; assert all('rules' in g for g in GATE_DEFINITIONS); print('All gates have rules: OK')"` | `All gates have rules: OK` |

### Dependencies

- US-01 (shared.py exists; gate_definitions.py does not import it but is part of the same module graph)

---

## US-06: Decompose PRDFlowBuilder into Thin Orchestrator

**FR Coverage**: FR-01 (AC-01c), FR-02 (AC-02c), FR-03 (AC-03a, AC-03c, AC-03d, AC-03d2, AC-03e, AC-03f), FR-05 (AC-05b partial, AC-05c partial, AC-05d)
**Design Spec Step**: 6
**Sprint**: 1 | **Story Points**: 8

### Description

**As a** plugin maintainer,
**I want** `PRDFlowBuilder` reduced to a thin orchestrator of <=200 lines that loops over data definitions,
**So that** I can understand the entire orchestration logic at a glance without reading 1,157 lines.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-6.1 | **Given** the refactored prd_flow_builder.py, **When** I count lines from `class PRDFlowBuilder:` to end of class, **Then** the count is <=200 lines | structural |
| AC-6.2 | **Given** the refactored PRDFlowBuilder, **When** I inspect `build_prd_flow()`, **Then** it uses `for` loops over STAGE_DEFINITIONS and GATE_DEFINITIONS via a PIPELINE_SEQUENCE list, and no `_create_stageN_*` or `_create_gateN_*` factory methods exist | structural |
| AC-6.3 | **Given** the refactored PRDFlowBuilder, **When** I check for `create_flow()`, `create_node()`, `create_rule()`, **Then** all three methods exist on the class | structural |
| AC-6.4 | **Given** a PRDFlowBuilder instance, **When** I access `builder.conn`, **Then** it returns a valid sqlite3.Connection object (public attribute preserved per AC-03d2) | structural |
| AC-6.5 | **Given** the refactored PRDFlowBuilder, **When** I call `export_flow_diagram(flow_id)`, **Then** it returns a text diagram of the flow structure | structural |
| AC-6.6 | **Given** the refactored builder creates a new flow, **When** I call `_count_nodes(flow_id)` and `_count_rules(flow_id)`, **Then** the node count is 15 and the rule count is 20 | empirical |
| AC-6.7 | **Given** the refactored prd_flow_builder.py, **When** I grep for `"prd_flows.db"`, **Then** zero matches are found (DB_PATH imported from shared.py) | structural |
| AC-6.8 | **Given** the refactored prd_flow_builder.py, **When** I grep for inline timestamp ID patterns like `f"flow_{datetime.now`, **Then** zero matches are found (generate_timestamp_id from shared.py used instead) | structural |
| AC-6.9 | **Given** the PIPELINE_SEQUENCE list in prd_flow_builder.py, **When** I trace through it, **Then** it produces the exact stage/gate ordering from the design spec section 7, including consecutive gates 3-4 and consecutive stages 5-6 | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-06.1 | AC-6.3, AC-6.6 | `python -c "from prd_flow_builder import PRDFlowBuilder; b = PRDFlowBuilder(':memory:'); fid = b.build_prd_flow(); print(b._count_nodes(fid), b._count_rules(fid)); b.close()"` | `15 20` |
| T-06.2 | AC-6.1, AC-6.5 | `python prd_flow_builder.py` in the plugin directory | Creates flow, prints node/rule counts and diagram, exit code 0 |
| T-06.3 | AC-6.1 | `wc -l` on class body (from `class PRDFlowBuilder:` to end of class) | <=200 lines |
| T-06.4 | AC-6.2 | `grep -c '_create_stage\|_create_gate' prd_flow_builder.py` | `0` -- no factory methods remain |
| T-06.5 | AC-6.4 | `python -c "from prd_flow_builder import PRDFlowBuilder; b = PRDFlowBuilder(':memory:'); assert hasattr(b, 'conn'); print('conn exists: OK'); b.close()"` | `conn exists: OK` |

### Dependencies

- US-01 (shared.py), US-02 (schema.py), US-03 (get_connection wired), US-04 (stage_definitions.py), US-05 (gate_definitions.py)

---

## US-07: Consolidate prd_execute.py as Canonical Executor

**FR Coverage**: FR-04 (AC-04c, AC-04d), FR-05 (AC-05b partial, AC-05c partial)
**Design Spec Step**: 7
**Sprint**: 1 | **Story Points**: 3

### Description

**As a** pipeline user,
**I want** `prd_execute.py` to be the single canonical execution script with UTF-8 support,
**So that** I know exactly which script to run and never encounter encoding errors.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-7.1 | **Given** the updated prd_execute.py, **When** I grep for `"prd_flows.db"`, **Then** zero matches are found, and `from shared import DB_PATH` is present | structural |
| AC-7.2 | **Given** the updated prd_execute.py, **When** I inspect the `main()` function, **Then** `ensure_utf8_output()` is called (imported from shared.py), absorbing the functionality from deleted run_execute.py | structural |
| AC-7.3 | **Given** all .py files in the plugin directory, **When** I grep for `EXAMPLE_PRODUCT_IDEAS`, **Then** matches are found only in prd_execute.py (exactly one file) | structural |
| AC-7.4 | **Given** the refactored codebase, **When** I run `python -c "import prd_execute; print('OK')"`, **Then** it prints `OK` with exit code 0 | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-07.1 | AC-7.1 | `grep -c '"prd_flows.db"' prd_execute.py` | `0` |
| T-07.2 | AC-7.3 | `grep -c 'EXAMPLE_PRODUCT_IDEAS' prd_execute.py` | `>= 1` (definition + usage) |
| T-07.3 | AC-7.3 | `grep -r 'EXAMPLE_PRODUCT_IDEAS' *.py \| grep -v prd_execute.py` | No output (no matches outside prd_execute.py) |

### Dependencies

- US-06 (PRDFlowBuilder must be decomposed and stable before modifying its consumer)

---

## US-08: Restructure fix_and_run.py with Named Functions

**FR Coverage**: FR-06 (AC-06a through AC-06f), FR-05 (AC-05b partial, AC-05c partial)
**Design Spec Step**: 8
**Sprint**: 2 | **Story Points**: 3

### Description

**As a** plugin maintainer,
**I want** `fix_and_run.py` restructured into named functions with a `main()` guard,
**So that** I can understand, test, and reuse individual pieces of the cleanup/demo workflow.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-8.1 | **Given** the refactored fix_and_run.py, **When** I inspect the file, **Then** a `def main()` function exists and is called via `if __name__ == "__main__"` guard | structural |
| AC-8.2 | **Given** fix_and_run.py, **When** I inspect the file, **Then** a function `clean_incomplete_executions()` (or similar descriptive name) exists for database cleanup logic | structural |
| AC-8.3 | **Given** fix_and_run.py, **When** I inspect the file, **Then** a function `demonstrate_bre_evaluation()` (or similar) exists for BRE demonstration logic | structural |
| AC-8.4 | **Given** fix_and_run.py, **When** I inspect the file, **Then** a function `display_flow_structure()` (or similar) exists for flow structure display | structural |
| AC-8.5 | **Given** the refactored fix_and_run.py, **When** I inspect lines outside of function definitions, **Then** only import statements and the `if __name__ == "__main__"` guard exist at top level | structural |
| AC-8.6 | **Given** fix_and_run.py uses `shared.get_connection()`, **When** I run it against a fresh (non-existent) database, **Then** the DELETE queries succeed because `ensure_schema()` has been called first (latent ordering bug fixed) | empirical |
| AC-8.7 | **Given** the refactored fix_and_run.py, **When** I grep for `"prd_flows.db"`, **Then** zero matches are found | structural |
| AC-8.8 | **Given** the refactored fix_and_run.py, **When** I run `python fix_and_run.py`, **Then** it produces structurally equivalent output to the pre-refactoring version (formatting differences acceptable) | empirical |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-08.1 | AC-8.1 | `grep -c 'def main' fix_and_run.py` | `1` |
| T-08.2 | AC-8.2, AC-8.3, AC-8.4 | `grep -c 'def clean_incomplete\|def demonstrate_bre\|def display_flow' fix_and_run.py` | `>= 3` (all three named functions) |
| T-08.3 | AC-8.8 | `python fix_and_run.py` in plugin directory | Runs to completion, exit code 0, output includes cleanup + BRE demo + flow structure |
| T-08.4 | AC-8.7 | `grep -c '"prd_flows.db"' fix_and_run.py` | `0` |

### Dependencies

- US-06 (PRDFlowBuilder must be decomposed and stable)
- US-01, US-03 (shared.py with get_connection must be wired)

---

## US-09: Restructure check_db.py with Functions and Error Handling

**FR Coverage**: FR-07 (AC-07a through AC-07e), FR-05 (AC-05b partial, AC-05c partial)
**Design Spec Step**: 9
**Sprint**: 2 | **Story Points**: 2

### Description

**As a** plugin maintainer,
**I want** `check_db.py` restructured with descriptive function names, a `main()` guard, and graceful error handling,
**So that** the DB inspection tool is readable, importable, and does not crash with raw stack traces.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-9.1 | **Given** the refactored check_db.py, **When** I inspect the file, **Then** a `def main()` function exists and is called via `if __name__ == "__main__"` guard | structural |
| AC-9.2 | **Given** check_db.py, **When** I inspect all function definitions, **Then** every function has a descriptive name (no single-letter names), including at minimum: `list_flows()`, `list_nodes()`, `list_rules()` (or equivalently descriptive names) | structural |
| AC-9.3 | **Given** check_db.py opens a database connection, **When** I inspect the connection usage, **Then** it uses `with` context manager or has explicit `conn.close()` in a `finally` block | structural |
| AC-9.4 | **Given** the database file does not exist at the expected path, **When** I run `python check_db.py`, **Then** a human-readable error message is printed (not a raw Python stack trace), and the exit code is non-zero | empirical |
| AC-9.5 | **Given** the refactored check_db.py, **When** I grep for `"prd_flows.db"`, **Then** zero matches are found, and `from shared import` is present | structural |
| AC-9.6 | **Given** an existing prd_flows.db with data, **When** I run `python check_db.py`, **Then** it produces the same flow counts, node type breakdowns, and rule counts as the pre-refactoring version | empirical |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-09.1 | AC-9.1 | `grep -c 'def main' check_db.py` | `1` |
| T-09.2 | AC-9.2 | `grep -c 'def list_' check_db.py` | `>= 2` (descriptive function names) |
| T-09.3 | AC-9.4 | Run `python check_db.py` with a nonexistent DB path | Graceful error message, no traceback |
| T-09.4 | AC-9.5 | `grep -c '"prd_flows.db"' check_db.py` | `0` |

### Dependencies

- US-01 (shared.py must exist with get_connection)

---

## US-10: Delete Duplicate Entry Point Scripts

**FR Coverage**: FR-04 (AC-04a, AC-04b)
**Design Spec Step**: 10
**Sprint**: 2 | **Story Points**: 1

### Description

**As a** plugin maintainer,
**I want** `run_execute.py` and `run_builder.py` deleted from the codebase,
**So that** there is exactly one canonical entry point per operation and no confusion about which script to run.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-10.1 | **Given** the refactoring is complete, **When** I check the plugin directory, **Then** `run_execute.py` does not exist on disk | structural |
| AC-10.2 | **Given** the refactoring is complete, **When** I check the plugin directory, **Then** `run_builder.py` does not exist on disk | structural |
| AC-10.3 | **Given** run_execute.py and run_builder.py are deleted, **When** I grep all .py files for `run_execute` or `run_builder`, **Then** zero matches are found | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-10.1 | AC-10.1, AC-10.2 | `ls run_execute.py run_builder.py 2>&1` in the plugin directory | Both files report "No such file or directory" |
| T-10.2 | AC-10.3 | `grep -r 'run_execute\|run_builder' *.py` in the plugin directory | No output |

### Dependencies

- US-07 (prd_execute.py consolidated as canonical executor)
- US-06 (prd_flow_builder.py decomposed, __main__ block preserved)

---

## US-11: Update CLAUDE.md Entry Points Documentation

**FR Coverage**: FR-08 (AC-08a, AC-08b, AC-08c)
**Design Spec Step**: 11
**Sprint**: 2 | **Story Points**: 1

### Description

**As a** pipeline user,
**I want** CLAUDE.md updated to reflect the 4 canonical entry points,
**So that** documented commands match the actual codebase and I am never directed to run a deleted script.

### Acceptance Criteria

| AC ID | Given / When / Then | Type |
|-------|---------------------|------|
| AC-11.1 | **Given** the CLAUDE.md file, **When** I read the `Running Scripts` section for prd-quality-gate-flow, **Then** it lists exactly 4 scripts: `prd_flow_builder.py`, `prd_execute.py`, `check_db.py`, `fix_and_run.py` | structural |
| AC-11.2 | **Given** the updated CLAUDE.md, **When** I grep for `run_execute` or `run_builder`, **Then** zero matches are found | structural |
| AC-11.3 | **Given** the CLAUDE.md Running Scripts section, **When** I read each documented command, **Then** every `python <script>.py` command corresponds to an existing file with a `main()` entry point | structural |

### Test Cases

| TC ID | Tests AC | Test Description | Expected Result |
|-------|----------|------------------|-----------------|
| T-11.1 | AC-11.2 | `grep -c 'run_execute\|run_builder' CLAUDE.md` | `0` |
| T-11.2 | AC-11.1, AC-11.3 | `grep 'python.*prd-quality-gate-flow' CLAUDE.md` | Lists exactly: prd_flow_builder.py, prd_execute.py, check_db.py, fix_and_run.py |

### Dependencies

- US-10 (duplicate files deleted, so documentation reflects final state)

---

## FR-to-Story Traceability Matrix

Every FR and AC from the PRD is covered by at least one user story. QA can verify FR-by-FR.

| FR | AC | Story | Test Cases |
|----|----|-------|------------|
| FR-01 | AC-01a | US-04 | T-04.1 |
| FR-01 | AC-01b | US-04 | T-04.2 |
| FR-01 | AC-01c | US-06 | T-06.4 |
| FR-01 | AC-01d | US-04 | T-04.3 |
| FR-01 | AC-01e | US-04 | T-04.1 |
| FR-02 | AC-02a | US-05 | T-05.1 |
| FR-02 | AC-02b | US-05 | T-05.2, T-05.3 |
| FR-02 | AC-02c | US-06 | T-06.4 |
| FR-02 | AC-02d | US-05 | T-05.1 |
| FR-02 | AC-02e | US-05 | T-05.1 |
| FR-02 | AC-02f | US-05 | T-05.2 |
| FR-03 | AC-03a | US-06 | T-06.3 |
| FR-03 | AC-03b | US-02 | T-02.1 |
| FR-03 | AC-03c | US-06 | T-06.4 |
| FR-03 | AC-03d | US-06 | T-06.1 |
| FR-03 | AC-03d2 | US-06 | T-06.5 |
| FR-03 | AC-03e | US-06 | T-06.2 |
| FR-03 | AC-03f | US-06 | T-06.1 |
| FR-03 | AC-03g | US-02, US-03 | T-02.1, T-03.1, T-03.2 |
| FR-04 | AC-04a | US-10 | T-10.1, T-10.2 |
| FR-04 | AC-04b | US-10 | T-10.1, T-10.2 |
| FR-04 | AC-04c | US-07 | T-07.2, T-07.3 |
| FR-04 | AC-04d | US-07 | T-07.1 |
| FR-05 | AC-05a | US-01 | T-01.1, T-01.3 |
| FR-05 | AC-05b | US-06, US-07, US-08, US-09 | T-06.1, T-07.1, T-08.4, T-09.4 |
| FR-05 | AC-05c | US-06, US-07, US-08, US-09 | T-06.1, T-07.1, T-08.4, T-09.4 |
| FR-05 | AC-05d | US-06 | T-06.1 |
| FR-05 | AC-05e | N/A (scope boundary) | N/A (core modules unchanged per NFR-06) |
| FR-06 | AC-06a | US-08 | T-08.1 |
| FR-06 | AC-06b | US-08 | T-08.2 |
| FR-06 | AC-06c | US-08 | T-08.2 |
| FR-06 | AC-06d | US-08 | T-08.2 |
| FR-06 | AC-06e | US-08 | T-08.1 |
| FR-06 | AC-06f | US-08 | T-08.3 |
| FR-07 | AC-07a | US-09 | T-09.1 |
| FR-07 | AC-07b | US-09 | T-09.2 |
| FR-07 | AC-07c | US-09 | T-09.1 |
| FR-07 | AC-07d | US-09 | T-09.3 |
| FR-07 | AC-07e | US-09 | T-09.1 |
| FR-08 | AC-08a | US-11 | T-11.2 |
| FR-08 | AC-08b | US-11 | T-11.1 |
| FR-08 | AC-08c | US-11 | T-11.2 |

**Coverage**: All 8 FRs mapped. All 42 acceptance criteria covered. Zero gaps.

---

## NFR Verification Across Stories

| NFR | Verification Point | Method |
|-----|--------------------|--------|
| NFR-01 (Zero external deps) | All stories | `grep` for non-stdlib imports in every new/modified file |
| NFR-02 (Schema compat) | US-02, US-06 | Load pre-refactoring DB, run queries, compare results |
| NFR-03 (Python 3.9+) | All stories | Code review during development |
| NFR-04 (Behavioral compat) | US-06, US-07, US-08, US-09 | Structural equivalence checks (counts, not stdout diff) |
| NFR-05 (File size) | All stories | `wc -l` on every modified/new file; data files may exceed 300 with justification |
| NFR-06 (Core modules untouched) | All stories | `git diff business_rules_engine.py flow_orchestrator.py` shows zero diff |

---

## Target Files by Story

| Story | Files Created | Files Modified | Files Deleted |
|-------|---------------|----------------|---------------|
| US-01 | `shared.py` | -- | -- |
| US-02 | `schema.py` | -- | -- |
| US-03 | -- | `shared.py` | -- |
| US-04 | `stage_definitions.py` | -- | -- |
| US-05 | `gate_definitions.py` | -- | -- |
| US-06 | -- | `prd_flow_builder.py` | -- |
| US-07 | -- | `prd_execute.py` | -- |
| US-08 | -- | `fix_and_run.py` | -- |
| US-09 | -- | `check_db.py` | -- |
| US-10 | -- | -- | `run_execute.py`, `run_builder.py` |
| US-11 | -- | `CLAUDE.md` | -- |

All files are within the `prd-quality-gate-flow/` directory except US-11 which modifies the repo-root `CLAUDE.md`.
