# PRD: prd-quality-gate-flow Refactoring

**Version**: 1.1
**Date**: 2026-03-30
**Author**: Product Owner (Gandalf)
**Source Issues**: #51, #52, #53
**Project Type**: FEATURE (structural refactoring)
**Pipeline Stage**: 02-Refine

---

## 1. Problem Statement

The `prd-quality-gate-flow/` plugin has accumulated structural technical debt that impairs maintainability, readability, and extensibility. Three interrelated issues were identified during a clean code dogfooding review:

1. **God object** (#51): `PRDFlowBuilder` in `prd_flow_builder.py` spans 1,157 lines in a single class. It combines database schema creation (lines 47-203), flow construction helpers (`create_flow`, `create_node`, `create_rule`), 12 stage/gate factory methods (`_create_stage1_creation` through `_create_stage7_completion`, plus 7 gate creators), node/rule counting utilities, and diagram export. This is ~6x the 200-line clean code signal and makes the class impossible to reason about in isolation.

2. **Duplicate entry points** (#52): `run_execute.py` (210 lines) is a near-copy of `prd_execute.py` (227 lines) — both define identical `EXAMPLE_PRODUCT_IDEAS` dictionaries, identical `execute_prd_workflow()` functions, and identical `main()` functions. Similarly, `run_builder.py` (44 lines) duplicates the `__main__` block of `prd_flow_builder.py`. The string `"prd_flows.db"` is hardcoded in at least 5 files (shotgun surgery anti-pattern).

3. **Missing function structure** (#53): `fix_and_run.py` (214 lines) is flat procedural code — the entire file executes top-to-bottom at module load with zero function extraction. `check_db.py` (27 lines) has no functions at all — bare top-level statements with no error handling and no descriptive structure.

These issues create compounding risk: any change to stage/gate definitions requires modifying the god object, any change to the database path requires editing 5+ files, and the duplicate entry points create confusion about which script to run.

**Evidence**: All three issues were filed during clean code dogfooding review. `prd_flow_builder.py` confirmed at 1,157 lines via `wc -l`. `"prd_flows.db"` confirmed hardcoded in `prd_flow_builder.py`, `prd_execute.py`, `run_execute.py`, `run_builder.py`, and `fix_and_run.py`. `run_execute.py` and `prd_execute.py` confirmed as near-duplicates via side-by-side read. Git history shows a single commit (`f6264ed`) — no prior refactoring attempts.

---

## 2. Goals and Success Metrics

| Goal | Metric | Baseline | Target | Measurement |
|------|--------|----------|--------|-------------|
| G1: Decompose god object | `PRDFlowBuilder` class line count | 1,157 lines | <=200 lines | `wc -l` on class definition |
| G2: Externalize definitions | Stage/gate definitions in separate data modules | 0 (all inline) | 7 stages + 7 gates in data files | File count + grep for factory methods |
| G3: Eliminate duplicate entry points | Files containing `execute_prd_workflow()` | 2 (prd_execute + run_execute) | 1 | `grep -r execute_prd_workflow` |
| G4: Centralize shared constants | Hardcoded `"prd_flows.db"` occurrences | 5+ files | 1 (shared.py only) | `grep -r '"prd_flows.db"'` |
| G5: Restructure flat scripts | Files with bare top-level statements (no `main()`) | 2 (fix_and_run, check_db) | 0 | Manual review |
| G6: Behavioral compatibility | CLI commands producing structurally equivalent results | N/A | 100% pass on structural equivalence check | Structural comparison: node counts, rule counts, gate counts, flow structure, and exit codes match before/after. Direct stdout diff is not viable because timestamp-based IDs (`flow_*`, `node_*`, `rule_*`) are non-deterministic per run. |
| G7: Zero new dependencies | External packages in import statements | 0 | 0 | `grep -r import` for non-stdlib |

**Dogfooding validation**: This refactoring must be validated by actually running each CLI entry point (`python prd_flow_builder.py`, `python prd_execute.py`, `python check_db.py`, `python fix_and_run.py`) against an existing `prd_flows.db` and comparing structural output (node counts, rule counts, gate counts, flow structure, exit codes) to a pre-refactoring baseline. Direct stdout diff is not viable due to non-deterministic timestamp-based IDs. This is a P0 UAT gate.

---

## 3. User Personas

### P1: Plugin Maintainer (Primary)

- **Who**: A developer extending or modifying the PRD quality gate flow
- **Goal**: Understand module boundaries quickly and add new stages/gates without modifying a 1,157-line class
- **Pain**: Cannot understand `PRDFlowBuilder` without reading the entire file. Cannot add a new stage without touching the god object. Does not know whether to run `prd_execute.py` or `run_execute.py`. Changing the database path requires editing 5+ files.
- **Success**: Can add a new stage by editing only a data file and a small registration function. Can find the canonical entry point for any operation in under 30 seconds.

### P2: Pipeline User (Secondary)

- **Who**: A user running PRD workflows via the documented CLI commands in CLAUDE.md
- **Goal**: Run PRD workflows reliably using documented commands
- **Pain**: Unclear which execution script to use. `fix_and_run.py` has no `--help`, no function structure, and executes everything at import time.
- **Success**: Existing documented commands continue to work (or have clear migration guidance). Each script has a `main()` entry point.

---

## 4. User Stories (Summary)

Detailed stories with task breakdowns and estimates will be produced in the Plan stage (Stage 5). These are summaries for scoping and prioritization.

| ID | Story | Priority |
|----|-------|----------|
| US-01 | As a maintainer, I want stage definitions in a data module so I can add/modify stages without touching the builder class | P0 |
| US-02 | As a maintainer, I want gate definitions (with their business rules) in a data module so I can add/modify gates declaratively | P0 |
| US-03 | As a maintainer, I want `PRDFlowBuilder` under 200 lines so I can understand the orchestration logic at a glance | P0 |
| US-04 | As a maintainer, I want a `shared.py` module with `DB_PATH` and utility functions so constants are never hardcoded | P0 |
| US-05 | As a user, I want one canonical entry point per operation so I know which script to run | P0 |
| US-06 | As a user, I want existing CLI commands documented in CLAUDE.md to keep working so my workflows are not broken | P0 |
| US-07 | As a maintainer, I want `fix_and_run.py` restructured into named functions with a `main()` guard so I can test/reuse parts | P1 |
| US-08 | As a maintainer, I want `check_db.py` to have descriptive function names and proper error handling | P1 |
| US-09 | As a maintainer, I want `EXAMPLE_PRODUCT_IDEAS` in exactly one location to eliminate copy-paste drift | P1 |

---

## 5. Functional Requirements

### FR-01: Extract Stage Definitions into Data Module

**Description**: Move the 7 stage definitions (currently inline in `_create_stage1_creation` through `_create_stage7_completion`) into a standalone Python module using Python dicts.

**Acceptance Criteria**:
- [ ] AC-01a: A new file `stage_definitions.py` exists containing all 7 stage definitions as Python dicts
- [ ] AC-01b: Each stage dict includes at minimum: `name`, `description`, `node_type`, `config` (with `agent_type`, `goal`, `model`, `tools`, `working_memory_output`, `max_retries`)
- [ ] AC-01c: `PRDFlowBuilder` imports and iterates over these dicts instead of calling individual `_create_stageN_*` factory methods
- [ ] AC-01d: No YAML files are used (constraint: no pyyaml dependency)
- [ ] AC-01e: Stage definitions are validated at load time — `KeyError` raised if required fields are missing

### FR-02: Extract Gate Definitions into Data Module

**Description**: Move the 7 gate definitions and their associated business rules into a standalone Python module using Python dicts.

**Acceptance Criteria**:
- [ ] AC-02a: A new file `gate_definitions.py` exists containing all 7 gate definitions with their associated business rules
- [ ] AC-02b: Each gate dict includes: `name`, `description`, `rules` (list of rule dicts with `name`, `rule_type`, `condition`, `action`, `priority`)
- [ ] AC-02c: `PRDFlowBuilder` imports and iterates over these dicts to create gates and rules
- [ ] AC-02d: Gate-to-stage ordering is explicit in the data structure (e.g., ordered list or explicit `after` field), not implicit in code call order
- [ ] AC-02e: The total number of business rules created matches the current count (verify via `_count_rules()` before/after)
- [ ] AC-02f: Gate definitions are validated at load time -- `KeyError` raised if required fields are missing (mirrors AC-01e)

### FR-03: Decompose PRDFlowBuilder Class

**Description**: Reduce `PRDFlowBuilder` to a thin orchestrator that uses the extracted data modules.

**Acceptance Criteria**:
- [ ] AC-03a: `PRDFlowBuilder` class is <=200 lines (measured by `wc -l` on the class definition, from `class PRDFlowBuilder:` to end of class)
- [ ] AC-03b: Schema creation (`_create_schema`) is extracted to a new file `schema.py` as a standalone function
- [ ] AC-03c: `build_prd_flow()` is a loop over data definitions, not 12+ individual method calls
- [ ] AC-03d: Public API methods `create_flow()`, `create_node()`, `create_rule()` remain on the builder class
- [ ] AC-03d2: `builder.conn` remains as a public attribute on `PRDFlowBuilder`. This is a de facto public API surface: 14 direct accesses across 3 consumer files (`prd_execute.py`, `run_execute.py`, `fix_and_run.py`) use `builder.conn.execute()` for flow lookup, BRE initialization, and gate evaluation queries. Schema extraction to `schema.py` and connection management in `shared.py` must not break this access pattern. If a future release introduces a query accessor method, consumer migration is a separate scope item.
- [ ] AC-03e: `export_flow_diagram()` remains accessible (on builder or extracted to utility)
- [ ] AC-03f: The builder creates identical database content as the current version (verified by comparing node counts, rule counts, and flow structure)
- [ ] AC-03g: Schema initialization contract: `schema.py` exposes an `ensure_schema(conn)` function. Any code path that queries the database must call `ensure_schema()` before executing queries (or rely on a code path that already has). `shared.py` should provide a `get_connection()` helper that opens a connection and ensures the schema exists. **Note**: `fix_and_run.py` currently has a latent bug where it opens a raw `sqlite3.connect("prd_flows.db")` and runs DELETE queries (line 17-24) before the builder is imported (line 36). On a fresh database with no tables, this fails. The refactoring should fix this ordering bug as part of FR-06 restructuring.

### FR-04: Consolidate Entry Points

**Description**: Eliminate duplicate execution scripts. Establish one canonical script per operation.

**Acceptance Criteria**:
- [ ] AC-04a: `run_execute.py` is deleted from the codebase. Its functionality is fully covered by `prd_execute.py`.
- [ ] AC-04b: `run_builder.py` is deleted from the codebase. Its functionality is fully covered by `prd_flow_builder.py`'s `__main__` block.
- [ ] AC-04c: `EXAMPLE_PRODUCT_IDEAS` exists in exactly one file
- [ ] AC-04d: UTF-8 encoding setup (currently duplicated in `run_execute.py` and `run_builder.py`) is consolidated into `shared.py`

### FR-05: Create Shared Constants Module

**Description**: Create `shared.py` containing all shared constants and utility functions.

**Acceptance Criteria**:
- [ ] AC-05a: `shared.py` exists with at minimum: `DB_PATH` constant, `generate_timestamp_id(prefix)` function, `ensure_utf8_output()` function
- [ ] AC-05b: All `.py` files in the plugin import `DB_PATH` from `shared.py` instead of hardcoding `"prd_flows.db"`
- [ ] AC-05c: `grep -r '"prd_flows.db"'` across the plugin directory returns only `shared.py`
- [ ] AC-05d: `generate_timestamp_id()` replaces all inline `f"flow_{datetime.now().strftime(...)}"` and similar patterns in modified files only
- [ ] AC-05e: **Intentional scope boundary**: Core modules (`business_rules_engine.py`, `flow_orchestrator.py`) will continue to accept `db_path`/`db_connection` as parameters and generate their own timestamp IDs internally. Consumer-side call sites (e.g., `prd_execute.py` line 51) will pass `shared.DB_PATH` or `shared.get_connection()` to these modules. This is architecturally correct -- core modules remain configurable and testable with injected dependencies. The visual inconsistency is intentional and documented.

### FR-06: Restructure fix_and_run.py

**Description**: Refactor from flat procedural code into well-named functions with a `main()` guard.

**Acceptance Criteria**:
- [ ] AC-06a: File has a `main()` function called via `if __name__ == "__main__"` guard
- [ ] AC-06b: Database cleanup logic is in a named function (e.g., `clean_incomplete_executions(db_path)`)
- [ ] AC-06c: BRE demonstration logic is in a named function (e.g., `demonstrate_bre_evaluation(builder, flow_id)`)
- [ ] AC-06d: Flow structure display is in a named function (e.g., `display_flow_structure(builder, flow_id)`)
- [ ] AC-06e: No bare top-level statements except imports and the `if __name__` guard
- [ ] AC-06f: Running `python fix_and_run.py` produces functionally equivalent output (formatting differences acceptable)

### FR-07: Restructure check_db.py

**Description**: Refactor to have meaningful function names, a `main()` guard, and proper error handling.

**Acceptance Criteria**:
- [ ] AC-07a: File has a `main()` function called via `if __name__ == "__main__"` guard
- [ ] AC-07b: All functions have descriptive names (no single-letter names)
- [ ] AC-07c: Database connection uses context manager (`with`) or explicit close in `finally` block
- [ ] AC-07d: Graceful error message when database file does not exist (no raw stack trace)
- [ ] AC-07e: Running `python check_db.py` against an existing database produces equivalent output

### FR-08: Update CLAUDE.md Entry Points

**Description**: Update CLAUDE.md to reflect the consolidated entry point structure.

**Acceptance Criteria**:
- [ ] AC-08a: CLAUDE.md `Running Scripts` section reflects the final canonical entry points
- [ ] AC-08b: Deleted scripts (`run_execute.py`, `run_builder.py`) are not listed as commands
- [ ] AC-08c: Entry point documentation reflects only the 4 canonical scripts: `prd_flow_builder.py`, `prd_execute.py`, `check_db.py`, `fix_and_run.py`

---

## 6. Non-Functional Requirements

| ID | Requirement | Target | Verification |
|----|------------|--------|-------------|
| NFR-01 | Zero external dependencies | No non-stdlib imports added | `grep` for non-stdlib imports |
| NFR-02 | SQLite schema compatibility | Existing `prd_flows.db` files work without migration | Load pre-refactoring DB, run queries |
| NFR-03 | Python 3.9+ compatibility | No syntax or stdlib features requiring >3.9 | Code review |
| NFR-04 | Behavioral compatibility | Before/after structurally equivalent for all 4 CLI entry points (node counts, rule counts, gate counts, flow structure, exit codes). Timestamp-based IDs are excluded from comparison. | Structural comparison script or manual count verification |
| NFR-05 | File size constraint | Every modified/new `.py` file <=300 lines for logic files. Pure data-definition files (`stage_definitions.py`, `gate_definitions.py`) may exceed 300 lines if the excess is declarative data (dicts/lists), documented with a brief justification in the file header. | `wc -l` + manual review for data files |
| NFR-06 | Core modules untouched | `business_rules_engine.py` and `flow_orchestrator.py` have zero diff (these are the only two core modules in `prd-quality-gate-flow/`; `database.py` and `agent_registry.py` do not exist in this plugin) | `git diff` on those files |

---

## 7. Out of Scope

- Changes to `business_rules_engine.py` or `flow_orchestrator.py` (core modules; `database.py` and `agent_registry.py` do not exist in this plugin)
- New features or capabilities beyond structural refactoring
- Database schema migrations or changes
- Test framework setup (no existing tests to preserve; test strategy is before/after output comparison)
- YAML data files (would require pyyaml dependency — use Python dicts instead)
- Changes to SKILL.md or plugin marketplace registration
- Performance optimization (structural clarity is the goal, not performance)
- Changes to `DEMONSTRATION_RESULTS.md`, `IMPLEMENTATION_SUMMARY.md`, `QUICKSTART.md`, `README.md`, or `prd_flow_diagram.txt`

---

## 8. Dependencies and Risks

### Dependencies

| Dependency | Type | Impact | Status |
|-----------|------|--------|--------|
| Python stdlib only | Technical | Data files must be Python dicts or JSON (no pyyaml) | Confirmed |
| Existing SQLite schema | Data | Schema creation must produce identical tables and indexes | Active — verify in Dev |
| CLAUDE.md documentation | Documentation | Entry point changes require CLAUDE.md update (FR-08) | Active |
| GitHub issues #51, #52, #53 | Process | All three issues must be closeable by this work | Active |
| Pre-refactoring output baselines | Testing | Must capture CLI output before any code changes | Active — capture in Dev stage setup |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| R1: Behavioral regression during refactoring | Medium | High | Before/after structural comparison (node counts, rule counts, gate counts, flow structure, exit codes) for all 4 CLI commands as P0 UAT gate. Stdout diff excluded due to non-deterministic timestamp IDs. |
| R2: Stage/gate data extraction introduces ordering bugs | Medium | High | Gate-to-stage ordering must be explicit in data structures; verify node/rule counts match before/after |
| R3: Hardcoded DB path missed in some file | Low | Medium | Grep verification as acceptance criterion (FR-05, AC-05c) |
| R4: Backward compat break for users with existing scripts | Low | Low | Internal plugin repo with no external consumers. CLAUDE.md is the single source of truth for entry points. Git history preserves deleted files if rollback is needed. |
| R5: Schema extraction breaks existing DB loading | Low | High | Test against existing `prd_flows.db` before and after; `CREATE TABLE IF NOT EXISTS` pattern is idempotent |
| R6: Multi-line goal strings in stage configs lose formatting during extraction | Medium | Medium | Use Python triple-quoted strings in data dicts (not JSON, which requires escaped newlines) |
| R7: Partial merge leaves codebase in worse state than before | Low | High | All changes must land in a single atomic PR. If regression is discovered during UAT, revert the entire PR. |

---

## 9. Open Questions

| # | Question | Owner | Impact if Unresolved | Status |
|---|----------|-------|---------------------|--------|
| OQ-1 | Should `run_execute.py` and `run_builder.py` be deleted outright or kept as thin deprecation wrappers? | PO | Users with existing scripts may break | **DECIDED (revised v1.1)**: Delete outright. This is an internal plugin repo with no external consumers. CLAUDE.md documents the canonical entry points. Deprecation wrappers with no release cadence or removal mechanism would persist indefinitely as dead code. If deletion causes issues, git history preserves the files. |
| OQ-2 | Should `export_flow_diagram()` stay on `PRDFlowBuilder` or move to a separate utility? | Architect | Affects class line count target | Open — resolve at Design stage |
| OQ-3 | Should stage/gate definitions use Python dicts (`.py` files) or JSON files? | Architect | Affects multi-line string handling for agent goals | **Recommendation**: Python dicts — more expressive, no JSON string escaping needed for multi-line `goal` prompts. Architect risk note confirms: YAML requires pyyaml, so Python dicts or JSON are the options. |
| OQ-4 | Should `EXAMPLE_PRODUCT_IDEAS` live in `shared.py` or stay in `prd_execute.py`? | PO | Minor — affects where test data is maintained | **Recommendation**: Keep in `prd_execute.py` — it is execution-specific test data, not a shared constant |
| OQ-5 | Should schema creation stay in `prd_flow_builder.py` as a standalone function, or move to a new `schema.py`? | Architect | Affects file count and import structure | **DECIDED**: Extract to new file `schema.py` as a standalone function |

---

## New Files (Proposed)

| File | Purpose | Estimated Size |
|------|---------|---------------|
| `shared.py` | Constants (`DB_PATH`), utilities (`generate_timestamp_id`, `ensure_utf8_output`) | ~30-50 lines |
| `stage_definitions.py` | 7 stage definitions as Python dicts | ~200-250 lines (mostly config data) |
| `gate_definitions.py` | 7 gate definitions + business rules as Python dicts | ~200-300 lines (mostly rule conditions) |
| `schema.py` (tentative) | Database schema creation extracted from builder | ~150-180 lines |

## Modified Files

| File | Changes | Estimated Final Size |
|------|---------|---------------------|
| `prd_flow_builder.py` | Decompose from 1,157 to <=200 lines; import from data modules | ~150-200 lines |
| `prd_execute.py` | Import `DB_PATH` from `shared.py`; consolidate as canonical executor | ~200-220 lines |
| `fix_and_run.py` | Extract into named functions with `main()` guard | ~200-214 lines |
| `check_db.py` | Add functions, error handling, `main()` guard | ~40-60 lines |
| `run_execute.py` | Deleted (functionality covered by `prd_execute.py`) | N/A |
| `run_builder.py` | Deleted (functionality covered by `prd_flow_builder.py`) | N/A |

## Traceability Matrix

| Issue | FRs | Coverage |
|-------|-----|----------|
| #51 (God object) | FR-01, FR-02, FR-03 | Complete — class decomposed via data extraction |
| #52 (Duplicate entry points) | FR-04, FR-05, FR-08 | Complete — consolidated + shared constants |
| #53 (Missing function structure) | FR-06, FR-07 | Complete — restructured with named functions |

---

## Adversarial Challenge Response (v1.1)

**Source**: `.delivery/artifacts/02-refine/challenger/challenge.md` (8 challenges, 3 blocking)

| # | Challenge | Verdict | Disposition | PRD Changes |
|---|-----------|---------|-------------|-------------|
| 1 | `builder.conn` undeclared public API | **VALID -- FIXED** | Challenger is correct. 14 direct `builder.conn.execute()` accesses across 3 consumer files. | Added AC-03d2: `builder.conn` explicitly preserved as public attribute. |
| 2 | NFR-06 lists non-existent files | **VALID -- FIXED** | Challenger is correct. `database.py` and `agent_registry.py` do not exist in `prd-quality-gate-flow/`. Copy-paste error from CLAUDE.md's agentic-flow-builder description. | NFR-06 corrected to list only `business_rules_engine.py` and `flow_orchestrator.py`. Out of Scope section also corrected. |
| 3 | Output diff unverifiable with timestamp IDs | **VALID -- FIXED** | Challenger is correct. Every run generates different `flow_*`, `node_*`, `rule_*` IDs via `datetime.now().strftime()`. Naive diff always fails. | G6, NFR-04, R1, and dogfooding paragraph all redefined to use structural equivalence (node/rule/gate counts, flow structure, exit codes) instead of stdout diff. |
| 4 | Line count targets unsupported | **VALID -- MITIGATED** | The 300-line ceiling is tight for pure data files. `gate_definitions.py` estimate of 200-300 lines is at the boundary. | NFR-05 amended: 300-line limit applies to logic files; data-definition files may exceed with documented justification. |
| 5 | Schema initialization ordering risk | **VALID -- INCORPORATED** | `fix_and_run.py` does have a latent bug: raw DELETE queries before builder import. On fresh DB, this fails. | Added AC-03g: schema initialization contract with `ensure_schema()`. Pre-existing bug documented; fix included in FR-06 scope. |
| 6 | Out-of-scope boundary creates inconsistency | **VALID -- DOCUMENTED** | Core modules will retain their own `db_path` parameters and timestamp ID generation. This is intentional (dependency injection). | Added AC-05e: explicit documentation that this is an intentional scope boundary, architecturally correct. |
| 7 | Deprecation wrappers will persist indefinitely | **VALID -- DECISION REVISED** | No release cadence, no removal mechanism. Wrappers would become permanent dead code. | OQ-1 revised: delete `run_execute.py` and `run_builder.py` outright. FR-04 AC-04a/AC-04b updated. |
| 8 | No atomicity requirement | **VALID -- ADDED** | Git makes this trivial. Single PR + revert is the correct pattern. | Added R7: all changes in a single atomic PR with revert as rollback. |
