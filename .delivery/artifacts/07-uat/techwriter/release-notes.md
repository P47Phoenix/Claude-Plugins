# Release Notes: PRD Quality Gate Flow Refactoring

**Version**: 2.12.0
**Date**: 2026-03-30
**Author**: Bilbo (Technical Writer)
**Source Issues**: #51, #52, #53

> "I think I'm quite ready for another documentation adventure." This is the tale of slaying a god object -- a beast of 1,157 lines, lurking in the depths of `prd_flow_builder.py`, hoarding stage definitions, gate logic, schema creation, and shared constants all in one dreadful class. It has been dismantled, and the Shire is safer for it.

---

## Summary

This is a **pure structural refactoring** of the `prd-quality-gate-flow/` plugin. No new features were added. No behavioral changes were introduced. The god object `PRDFlowBuilder` (1,157 lines) has been decomposed into focused modules, duplicate entry points have been deleted, and flat procedural scripts have been restructured with proper function boundaries.

### By the Numbers

| Metric | Before | After |
|--------|-------:|------:|
| `PRDFlowBuilder` class lines | 1,157 | 259 (162 class body) |
| Hardcoded `"prd_flows.db"` occurrences | 5 files | 1 (`shared.py`) |
| Duplicate entry point scripts | 2 | 0 |
| Scripts without `main()` guard | 2 | 0 |
| Modules in plugin | 7 | 9 (4 new, 2 deleted) |
| Node count | 15 | 15 |
| Rule count | 20 | 20 |
| Gate count | 7 | 7 |

All behavioral baselines pass: node counts, rule counts, gate counts, gate-rule distribution `[4,4,3,1,4,3,1]`, node names/types, and exit codes are identical before and after.

---

## What Changed

### God Object Decomposition (Issue #51)

The monolithic `PRDFlowBuilder` class has been split into four focused modules:

- **`shared.py`** (60 lines) -- Centralized constants (`DB_PATH`), utility functions (`generate_timestamp_id()`, `ensure_utf8_output()`), and a `get_connection()` helper that ensures the schema exists before returning a database connection.
- **`schema.py`** (174 lines) -- Database schema creation extracted into a standalone `ensure_schema(conn)` function. Covers 9 tables, 7 indexes, fully idempotent via `CREATE TABLE IF NOT EXISTS`.
- **`stage_definitions.py`** (269 lines) -- All 7 stage definitions as Python dicts with load-time validation. Each stage dict includes `name`, `description`, `node_type`, and full `config` block.
- **`gate_definitions.py`** (411 lines) -- All 7 gate definitions and 20 business rules as Python dicts with load-time validation. Gate-to-stage ordering is explicit in the data structure.

`PRDFlowBuilder` is now a thin orchestrator: `build_prd_flow()` iterates over data definitions instead of calling 12+ individual factory methods.

### Duplicate Entry Points Eliminated (Issue #52)

- **`run_execute.py` deleted** -- Was a near-copy of `prd_execute.py` (identical `EXAMPLE_PRODUCT_IDEAS`, identical `execute_prd_workflow()`, identical `main()`).
- **`run_builder.py` deleted** -- Duplicated the `__main__` block of `prd_flow_builder.py`.
- `EXAMPLE_PRODUCT_IDEAS` now exists in exactly one file (`prd_execute.py`).
- UTF-8 encoding setup consolidated into `shared.ensure_utf8_output()`.

### Flat Scripts Restructured (Issue #53)

- **`fix_and_run.py`** -- Extracted into 5 named functions with a `main()` guard. No bare top-level statements remain (except imports and `if __name__`). Also fixes a latent bug where raw `sqlite3.connect()` was called before schema creation, which would fail on a fresh database.
- **`check_db.py`** -- Restructured with 3 descriptive functions, a `main()` guard, context-managed database connections, and graceful error handling when the database file does not exist.

### Shared Constants Centralized

All `.py` files in the plugin now import `DB_PATH` from `shared.py`. The string `"prd_flows.db"` appears in exactly one location.

---

## Breaking Changes

### Deleted Files

| File | Replacement |
|------|-------------|
| `run_execute.py` | Use `python prd_execute.py` instead |
| `run_builder.py` | Use `python prd_flow_builder.py` instead |

If you have scripts, aliases, or automation that invoke `run_execute.py` or `run_builder.py`, update them to use the canonical entry points listed above. Both deleted files are preserved in git history if rollback is needed.

### No Other Breaking Changes

- The SQLite schema is unchanged. Existing `prd_flows.db` files work without migration.
- The public API surface of `PRDFlowBuilder` is preserved: `create_flow()`, `create_node()`, `create_rule()`, `export_flow_diagram()`, and `builder.conn` all remain accessible.
- All 4 canonical CLI commands produce structurally equivalent output.
- Core modules `business_rules_engine.py` and `flow_orchestrator.py` have zero diff.

---

## Migration Guide

### If you used `run_execute.py`

```bash
# Before
python prd-quality-gate-flow/run_execute.py

# After
python prd-quality-gate-flow/prd_execute.py
```

The functionality is identical. `prd_execute.py` was always the canonical executor; `run_execute.py` was an accidental duplicate.

### If you used `run_builder.py`

```bash
# Before
python prd-quality-gate-flow/run_builder.py

# After
python prd-quality-gate-flow/prd_flow_builder.py
```

The `__main__` block of `prd_flow_builder.py` provides the same functionality.

### If you imported from `prd_flow_builder.py` directly

The `PRDFlowBuilder` class remains in `prd_flow_builder.py` with the same public API. No import changes needed. Internal factory methods (`_create_stage1_creation`, etc.) have been removed -- if you were calling those directly, use the data definitions in `stage_definitions.py` and `gate_definitions.py` instead.

---

## Canonical Entry Points

After this release, the plugin has exactly 4 CLI entry points (unchanged from prior CLAUDE.md documentation):

```bash
python prd-quality-gate-flow/prd_flow_builder.py   # Build PRD flow
python prd-quality-gate-flow/prd_execute.py         # Execute PRD workflow
python prd-quality-gate-flow/check_db.py            # Inspect SQLite DB state
python prd-quality-gate-flow/fix_and_run.py         # Automated end-to-end run
```

---

## Files Added / Modified / Deleted

### Files Added (4)

| File | Lines | Purpose |
|------|------:|---------|
| `prd-quality-gate-flow/shared.py` | 60 | DB_PATH, generate_timestamp_id(), ensure_utf8_output(), get_connection() |
| `prd-quality-gate-flow/schema.py` | 174 | ensure_schema(conn) -- 9 tables, 7 indexes, idempotent |
| `prd-quality-gate-flow/stage_definitions.py` | 269 | 7 stage definitions as Python dicts with load-time validation |
| `prd-quality-gate-flow/gate_definitions.py` | 411 | 7 gate definitions, 20 business rules with load-time validation |

### Files Modified (4)

| File | Before | After | Change |
|------|-------:|------:|--------|
| `prd-quality-gate-flow/prd_flow_builder.py` | 1,157 | 259 | Decomposed to thin orchestrator (-898 lines) |
| `prd-quality-gate-flow/prd_execute.py` | 227 | 228 | Imports DB_PATH from shared.py (+1 line) |
| `prd-quality-gate-flow/fix_and_run.py` | 214 | 290 | Restructured into 5 named functions with main() guard; latent bug fixed |
| `prd-quality-gate-flow/check_db.py` | 27 | 69 | Restructured with descriptive functions, error handling, main() guard |

### Files Deleted (2)

| File | Lines | Reason |
|------|------:|--------|
| `prd-quality-gate-flow/run_execute.py` | 210 | Duplicate of prd_execute.py |
| `prd-quality-gate-flow/run_builder.py` | 44 | Duplicate of prd_flow_builder.py __main__ block |

### Files Unchanged (verified zero diff)

| File | Lines | Reason |
|------|------:|--------|
| `prd-quality-gate-flow/business_rules_engine.py` | 569 | Core module -- out of scope per NFR-06 |
| `prd-quality-gate-flow/flow_orchestrator.py` | 598 | Core module -- out of scope per NFR-06 |

---

## Bug Fix

This release includes a fix for a **pre-existing latent bug** in `fix_and_run.py`: the script previously opened a raw `sqlite3.connect("prd_flows.db")` and ran DELETE queries before the builder (and therefore the schema) was initialized. On a fresh database with no tables, this would fail with a missing table error. The restructured version uses `shared.get_connection()`, which calls `ensure_schema()` first.

---

## Issue Traceability

| Issue | Title | Resolution |
|-------|-------|------------|
| #51 | God object in prd_flow_builder.py | Decomposed: 1,157 -> 259 lines via 4 extracted modules |
| #52 | Duplicate entry points | Deleted run_execute.py and run_builder.py; constants centralized |
| #53 | Missing function structure | fix_and_run.py and check_db.py restructured with named functions |

---

## Technical Notes

- **Zero external dependencies**: All imports are Python stdlib only (NFR-01).
- **Python 3.9+ compatible**: No walrus operators or 3.10+ features used (NFR-03).
- **Schema compatibility**: `ensure_schema()` uses `CREATE TABLE IF NOT EXISTS` -- existing databases load without migration (NFR-02).
- **Data file size**: `gate_definitions.py` exceeds the 300-line guideline at 411 lines. This is expected and documented -- the file is purely declarative data (dicts/lists), not logic (NFR-05).
- **Scope boundary**: Core modules (`business_rules_engine.py`, `flow_orchestrator.py`) intentionally retain their own `db_path` parameters and internal timestamp ID generation. Consumer files pass `shared.DB_PATH` to these modules. This asymmetry is architecturally correct -- core modules remain independently configurable and testable.

> And so the god object falls, the duplicates are swept away, and every script has a proper `main()` to call home. Four new modules stand where one unwieldy beast once sat, and the pipeline counts -- 15 nodes, 20 rules, 7 gates -- remain exactly as they were. A refactoring done right changes everything and nothing at the same time. Now then, I believe elevenses is calling.
