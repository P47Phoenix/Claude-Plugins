# Architect DoD Review -- PRD: prd-quality-gate-flow Refactoring

**Reviewer**: Architect (Celebrimbor)
**Date**: 2026-03-30
**Artifact**: `.delivery/artifacts/02-refine/po/prd.md` (v1.1)
**Status**: DONE

---

## Gate 2 Architect Criteria

### 1. Technical Feasibility

I verified every claim in the PRD against the actual codebase.

| PRD Claim | Verified | Evidence |
|-----------|----------|----------|
| `prd_flow_builder.py` is 1,157 lines | YES | `wc -l` confirms exactly 1,157 lines |
| `PRDFlowBuilder` contains 14 factory methods (`_create_stageN`, `_create_gateN`) | YES | `grep` confirms 7 stage creators + 7 gate creators, lines 362-1080 |
| Schema creation spans lines 47-203 | YES | `_create_schema()` confirmed at lines 47-203 (8 tables + 7 indexes) |
| `"prd_flows.db"` hardcoded in 5+ Python files | YES | `grep` confirms occurrences in `check_db.py`, `fix_and_run.py` (2x), `prd_execute.py` (2x), `prd_flow_builder.py` (2x), `run_builder.py`, `run_execute.py` (2x) -- 10 occurrences across 6 `.py` files |
| `run_execute.py` duplicates `prd_execute.py` | YES | Both define `execute_prd_workflow()`, both define `EXAMPLE_PRODUCT_IDEAS`, near-identical `main()` functions. 209 vs 226 lines. |
| `run_builder.py` duplicates `prd_flow_builder.py` `__main__` block | YES | 43-line wrapper that only calls `PRDFlowBuilder("prd_flows.db").build_prd_flow()` |
| `fix_and_run.py` has zero functions | YES | Flat procedural: bare `sqlite3.connect()` at line 17, bare DELETE queries at lines 20-24, all at module scope |
| `check_db.py` has no functions | YES | 26 lines, no function definitions, no `main()`, no error handling |
| `builder.conn` is used by 3 consumer files | YES | 14 direct `builder.conn.execute()` calls across `fix_and_run.py` (6), `prd_execute.py` (4), `run_execute.py` (4) |
| `fix_and_run.py` has latent schema ordering bug | YES | Line 17 opens raw `sqlite3.connect("prd_flows.db")` and runs DELETE queries (lines 20-24) before builder import at line 40. Fresh DB with no tables would fail. |

All factual claims are accurate. The decomposition is straightforward Python refactoring -- extracting methods into standalone modules and converting inline factory method bodies into declarative dicts. No algorithmic complexity, no concurrency concerns, no external service dependencies.

**Verdict**: PASS -- no feasibility blockers

### 2. NFRs Are Realistic and Achievable

| NFR | Assessment |
|-----|-----------|
| NFR-01 (Zero external deps) | Achievable. All proposed modules use only `sqlite3`, `json`, `datetime`, `enum`, `typing` -- all stdlib. Python dicts for data definitions require no dependencies. |
| NFR-02 (SQLite schema compat) | Achievable. `CREATE TABLE IF NOT EXISTS` is idempotent. Schema extraction to `schema.py` changes file location, not SQL content. Existing `.db` files will load without migration. |
| NFR-03 (Python 3.9+ compat) | Achievable. Nothing in the proposed design requires features beyond 3.9. Current code already uses `typing.Optional`, `typing.Dict` (not `X | Y` union syntax). |
| NFR-04 (Behavioral equivalence) | Achievable. Structural comparison (node/rule/gate counts, flow structure, exit codes) is the correct approach. The PRD correctly identified that timestamp-based IDs make stdout diff non-viable. |
| NFR-05 (File size <= 300 lines for logic, exemption for data) | Realistic. `schema.py` at ~160 lines (8 CREATE TABLE + 7 CREATE INDEX). `shared.py` at ~40 lines. `PRDFlowBuilder` trimmed to ~150-200 lines. Data files may exceed 300 lines but the exemption is explicitly scoped and justified. |
| NFR-06 (Core modules untouched) | Achievable. `business_rules_engine.py` (569 lines) and `flow_orchestrator.py` (598 lines) accept `db_path`/`db_connection` as parameters. Consumer-side changes (passing `shared.DB_PATH`) do not require modifying these files. The intentional scope boundary (AC-05e) is architecturally correct -- core modules should remain injectable. |

**Verdict**: PASS

### 3. Architecture Decisions Are Sound

**Python dicts vs YAML vs JSON (OQ-3)**: The PRD correctly recommends Python dicts. YAML requires `pyyaml` (violates NFR-01). JSON cannot represent multi-line strings without `\n` escaping, which would make the multi-paragraph `goal` prompts in stage configs unreadable. Python dicts with triple-quoted strings are the only option that satisfies both constraints. This is the right call.

**Schema extraction to `schema.py` (OQ-5)**: Sound. The `_create_schema()` method is 156 lines of pure DDL with no business logic dependencies. Extracting it to a standalone `ensure_schema(conn)` function enables the schema initialization contract (AC-03g) that fixes the `fix_and_run.py` ordering bug. The `shared.get_connection()` helper composing `sqlite3.connect()` + `ensure_schema()` is a clean pattern.

**`builder.conn` preserved as public attribute (AC-03d2)**: Pragmatically correct. Introducing a query accessor method would expand scope beyond structural refactoring. The 14 direct accesses across 3 files are documented; a future migration to a proper query API is a separate scope item. No objection.

**Shared module with `DB_PATH`, `generate_timestamp_id()`, `ensure_utf8_output()` (FR-05)**: Appropriate granularity. These are genuinely cross-cutting concerns. The intentional exclusion of core modules from `shared.py` usage (AC-05e) preserves their testability through dependency injection. This is not inconsistency -- it is correct layering.

**`export_flow_diagram()` placement (OQ-2)**: Correctly deferred to Design stage. Whether it stays on the builder or moves to a utility affects the 200-line budget but not feasibility.

**Verdict**: PASS -- all architectural decisions are sound

### 4. No Contradictory Requirements

I checked for conflicts across all FRs, NFRs, and acceptance criteria:

- **FR-03 (builder <= 200 lines) vs AC-03d (public API preserved)**: No conflict. `create_flow()`, `create_node()`, `create_rule()` are ~25 lines each. `build_prd_flow()` as a loop over data defs is ~30-40 lines. Init + schema delegation + these methods fit within 200 lines.
- **FR-04 (delete `run_execute.py`) vs NFR-04 (behavioral equivalence)**: No conflict. `prd_execute.py` is the surviving canonical script; equivalence is measured against it.
- **NFR-05 (300-line limit) vs estimated data file sizes**: No conflict. The exemption for declarative data files is explicit and scoped.
- **NFR-06 (core modules untouched) vs FR-05 (centralize `DB_PATH`)**: No conflict. AC-05e explicitly documents that consumer-side call sites pass `shared.DB_PATH` to core modules, while core modules retain their own parameter-based injection. Zero diff on core module source.
- **AC-03g (schema initialization contract) vs NFR-02 (schema compat)**: No conflict. `ensure_schema()` wraps existing `CREATE TABLE IF NOT EXISTS` DDL -- same SQL, same idempotent behavior, different call site.

**Verdict**: PASS -- no contradictions detected

### 5. Observations for Downstream Stages (Non-Blocking)

1. **Data definition ordering**: Gate-to-stage ordering is called out (AC-02d) but the specific mechanism (ordered list vs explicit `after` field vs positional index) is left to Design. This is appropriate -- the PRD specifies the constraint, Design specifies the mechanism.

2. **`export_flow_diagram()` line budget impact**: If this method stays on `PRDFlowBuilder`, the 200-line target is tighter. The method itself is likely 30-50 lines. Design should resolve OQ-2 before Dev begins to avoid mid-sprint rework.

3. **Structural equivalence verification**: The PRD describes this as "structural comparison script or manual count verification" (NFR-04). The Plan stage should specify whether this is automated (preferred) or manual, and what the exact comparison protocol is (e.g., query `SELECT COUNT(*) FROM nodes GROUP BY node_type` before/after).

---

## Summary

The PRD is technically feasible, architecturally sound, and free of contradictions. All factual claims about the codebase are verified. The Python-dicts-over-YAML decision is correct given the zero-dependency constraint. The scope boundary between consumer-side refactoring and core module preservation is well-drawn. The `fix_and_run.py` ordering bug fix is a welcome correctness improvement folded into the refactoring scope. No blocking concerns.
