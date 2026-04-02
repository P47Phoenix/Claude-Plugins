## Idea Brief

**Project Type**: FEATURE
**Date**: 2026-03-30
**Source Issues**: #51, #52, #53

### Problem Statement

The `prd-quality-gate-flow/` module has accumulated significant technical debt identified during clean code dogfooding review. Three related issues need coordinated refactoring:

1. **God object** (#51): `PRDFlowBuilder` at ~1120 lines combines schema creation, flow building, 12 stage/gate factory methods, counting, and diagram export. Far exceeds the 200-line clean code signal.
2. **Duplicate entry points** (#52): `run_execute.py` duplicates `prd_execute.py`, `run_builder.py` duplicates `prd_flow_builder.py`'s `__main__` block, and `"prd_flows.db"` is hardcoded in 5+ files (shotgun surgery).
3. **Missing function structure** (#53): `fix_and_run.py` is flat procedural code (80+ line function), `check_db.py` has meaningless names (`p()`, `pp()`), bare `except Exception` blocks, and mixed concerns.

### Target Users

- **Plugin developers**: Maintainers who extend or modify the PRD quality gate flow
- **Pipeline users**: Users who run PRD workflows and need reliable, understandable tooling

### Goals

1. Reduce `PRDFlowBuilder` from ~1120 lines to ~200 lines by extracting stage/gate definitions into data files
2. Eliminate duplicate entry points — single canonical way to run each operation
3. Extract shared constants (`DB_PATH`, timestamp ID generator) into a shared module
4. Restructure flat scripts into well-named functions with proper error handling
5. Maintain 100% behavioral compatibility — all existing workflows must produce identical results

### Constraints

- Python-only changes (no new dependencies)
- Must preserve existing SQLite database schema and data compatibility
- All existing CLI entry points documented in CLAUDE.md must continue to work (or be consolidated with clear migration)
- No changes to the business rules engine or flow orchestrator — refactoring is structural only

### Initial Scope

- `prd_flow_builder.py` — decompose god object, extract data files
- `prd_execute.py` / `run_execute.py` — consolidate into single entry point
- `run_builder.py` — remove or consolidate
- `fix_and_run.py` — extract into named functions
- `check_db.py` — rename functions, fix error handling
- New `shared.py` — constants and utilities
- New data files (YAML/JSON) for stage/gate definitions

### Out of Scope (initial)

- Changes to `database.py`, `business_rules_engine.py`, `flow_orchestrator.py`, or `agent_registry.py`
- New features or capabilities
- Database schema changes
- Test framework setup (no existing tests to preserve)
