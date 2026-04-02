# Adversarial Challenge: PRD Quality Gate Flow Refactoring

**Challenger**: Adversarial Reviewer
**Date**: 2026-03-30
**PRD Version**: 1.0
**Overall Confidence**: 3/5 (Proceed with caution -- several challenges require resolution)

---

## Challenge 1: `builder.conn` is a Public API Surface the PRD Ignores

**Confidence: 2/5 -- Serious concern**

The PRD says the refactoring will extract schema creation to `schema.py` and decompose `PRDFlowBuilder`. But it never acknowledges that **consumers access `builder.conn` directly** as a de facto public API. Evidence:

- `prd_execute.py` lines 34, 50, 98, 108: `builder.conn.execute(...)` for flow lookup, BRE initialization, and gate evaluation queries
- `run_execute.py` lines 66, 81, 126: identical pattern
- `fix_and_run.py` lines 43, 54, 65, 109, 122, 161: six direct `builder.conn.execute()` calls for flow lookup, node queries, rule queries, and gate queries

The PRD's FR-03 (AC-03d) says "Public API methods `create_flow()`, `create_node()`, `create_rule()` remain on the builder class." But `builder.conn` is the **most-used public API** in practice -- 14 direct accesses across 3 consumer files. If schema extraction to `schema.py` changes when/how `self.conn` is initialized, or if `shared.py` centralizes DB connection management, every consumer that touches `builder.conn` breaks.

**What must change**: The PRD must explicitly acknowledge `builder.conn` as a public API surface and either (a) declare it will remain as an attribute on the builder, (b) provide a query accessor method and update consumers, or (c) add the consumer access pattern to the modification scope with explicit acceptance criteria. Without this, "100% behavioral compatibility" is unverifiable.

---

## Challenge 2: NFR-06 Lists Non-Existent Files as Protected

**Confidence: 1/5 -- Factual error**

NFR-06 states: "Core modules untouched: `database.py`, `business_rules_engine.py`, `flow_orchestrator.py`, `agent_registry.py` have zero diff."

**`database.py` and `agent_registry.py` do not exist in the plugin directory.** The actual files in `prd-quality-gate-flow/` are:

```
business_rules_engine.py  fix_and_run.py      prd_flow_builder.py  run_builder.py
check_db.py               flow_orchestrator.py  prd_execute.py       run_execute.py
```

The PRD references `database.py` and `agent_registry.py` from the CLAUDE.md description of the agentic-flow-builder shared pattern, not from the actual prd-quality-gate-flow plugin. This is a copy-paste error that signals the NFR was not validated against the actual codebase.

The metrics document (M9) correctly lists only `business_rules_engine.py` and `flow_orchestrator.py`, contradicting the PRD's own NFR-06.

**What must change**: NFR-06 must be corrected to list only the two files that actually exist: `business_rules_engine.py` and `flow_orchestrator.py`.

---

## Challenge 3: "100% Behavioral Compatibility" is Unverifiable via Output Diff

**Confidence: 2/5 -- Serious concern**

Goal G6 and NFR-04 require "Before/after output identical for all 4 CLI entry points" verified by output capture and diff. The metrics document (M6) prescribes a specific capture protocol using `diff`.

But the codebase generates **timestamp-based IDs** everywhere:

- `flow_id = f"flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"`  (line 207)
- `node_id = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"` (line 227)
- `rule_id = f"rule_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"` (line 257)

Every run produces different flow IDs, node IDs, and rule IDs in the output. A naive `diff` of before/after stdout will **always show differences**. The metrics document says "formatting differences are acceptable; structural differences are failures" but does not define these terms or provide a comparison strategy that handles non-deterministic IDs.

Additionally, the PRD proposes centralizing ID generation into `shared.py` via `generate_timestamp_id()` (FR-05, AC-05d). If the format string changes even slightly (e.g., from `f"flow_{datetime...}"` to `generate_timestamp_id("flow")`), the IDs themselves may have a different format, further invalidating direct comparison.

**What must change**: The verification strategy must be concrete. Options: (a) a normalization script that strips IDs before diffing, (b) structural comparison only (node counts, rule counts, node types -- already partially in FR-03 AC-03f), or (c) redefine M6 as structural equivalence rather than output-level diff. Option (b) is the most robust and is already partially specified.

---

## Challenge 4: The 200-Line and 300-Line Targets are Unsupported by Evidence

**Confidence: 3/5 -- Moderate concern**

The PRD sets:
- `PRDFlowBuilder` class body: <= 200 lines (G1, AC-03a)
- Every modified/new `.py` file: <= 300 lines (NFR-05)

The only justification is "~6x the 200-line clean code signal," which is not attributed to any standard, study, or team convention documented in this repository.

More critically, the PRD's own estimates strain these limits:
- `stage_definitions.py`: estimated 200-250 lines. Seven stages averaging 35 lines each (with triple-quoted multi-line goal/prompt strings) yields ~245 lines before module-level boilerplate.
- `gate_definitions.py`: estimated 200-300 lines. Seven gates with multiple rules each -- the current gate factory methods average 54 lines each per the metrics document, totaling ~378 lines of pure definition data.

The 300-line ceiling for `gate_definitions.py` is already at risk based on the PRD's own estimates. If definitions do not fit, the team must either (a) split data files further (4+ new files instead of 2, adding import complexity), (b) compress formatting at the expense of readability, or (c) violate the constraint and justify an exception. None of these outcomes is planned for.

**Recommendation**: Validate the estimates by extracting and counting actual lines in the current factory methods. Convert the hard ceiling to "target 300, document exceptions" or increase the limit for pure data-definition files.

---

## Challenge 5: Schema Extraction Creates an Initialization Ordering Risk

**Confidence: 3/5 -- Moderate concern**

FR-03 (AC-03b) extracts `_create_schema` to `schema.py` as a standalone function. Currently, schema creation is guaranteed to run first because `PRDFlowBuilder.__init__()` calls `_create_schema()`, and every entry point instantiates the builder before doing anything else.

But multiple entry points open **independent database connections** that assume the schema already exists:

1. `FlowOrchestrator.__init__` (line 56): opens its own `sqlite3.connect(db_path)` -- relies on builder having already created the schema.
2. `fix_and_run.py` (line 17): opens a raw `sqlite3.connect("prd_flows.db")` connection and runs DELETE queries **before** the builder is even imported (the builder import is on line 36).
3. `check_db.py` (line 4): opens a raw connection and queries tables directly.

The PRD's proposed restructuring of `fix_and_run.py` (FR-06) will wrap code in functions with a `main()` guard. If the refactored `main()` changes the initialization order -- for example, calling `clean_incomplete_executions()` before instantiating the builder -- it will fail on a fresh database (no tables to DELETE from).

The current code "works" on fresh databases only because `fix_and_run.py`'s raw connection DELETE statements silently succeed on non-existent tables (SQLite does not error on `DELETE FROM` for tables that don't exist... actually it does error if the table doesn't exist). On a truly fresh database, `fix_and_run.py` already fails at line 20. The refactoring inherits this latent bug.

**Recommendation**: The PRD should specify that `schema.py`'s function is called as a guaranteed initialization step in `shared.py` or that every entry point must ensure schema existence before queries. This also reveals a pre-existing bug worth documenting.

---

## Challenge 6: The "Out of Scope" Boundary Will Create Visible Inconsistency

**Confidence: 3/5 -- Moderate concern**

The PRD declares `flow_orchestrator.py` and `business_rules_engine.py` as zero-diff out-of-scope (NFR-06). But the refactoring will create an inconsistency that looks like incomplete work:

1. After refactoring, `prd_execute.py`, `fix_and_run.py`, and `check_db.py` will import `DB_PATH` from `shared.py`. But `flow_orchestrator.py` (line 56) will continue to accept `db_path` as a raw string parameter, and callers will pass `"prd_flows.db"` directly -- or will they pass `shared.DB_PATH`? The PRD does not address this call site.

2. `prd_execute.py` line 51 currently passes the hardcoded string: `orchestrator = FlowOrchestrator("prd_flows.db", bre)`. After refactoring, this should become `FlowOrchestrator(DB_PATH, bre)`. This is a consumer-side change (in scope) but the resulting code passes `shared.DB_PATH` to a core module that still internally uses a local `db_path` parameter -- visually inconsistent but functionally correct.

3. `fix_and_run.py` line 130 instantiates `BusinessRulesEngine()` with **no arguments** (no connection). This is a different code path from `prd_execute.py` which passes `builder.conn`. The temptation to "fix" this inconsistency during refactoring will pull the BRE into scope.

**Recommendation**: Acknowledge explicitly that core modules will continue to accept `db_path`/`db_connection` parameters and that callers will pass the centralized constant. This is architecturally correct (core modules remain configurable) but should be documented as intentional.

---

## Challenge 7: Deprecation Wrappers Will Persist Indefinitely

**Confidence: 4/5 -- Minor concern**

FR-04 converts `run_execute.py` and `run_builder.py` to thin deprecation wrappers. OQ-1 says "remove in next release."

There is no release cadence, no versioning scheme for individual plugins, and no mechanism to track when "next release" occurs. The plugin has a single commit in its git history (`f6264ed`). These wrappers will likely persist forever, adding two files that exist only to print warnings nobody reads.

CLAUDE.md documents the canonical entry points. This is an internal plugin repo, not a distributed package with external consumers. The PRD's own evidence shows `run_execute.py` and `run_builder.py` are near-copies with zero unique functionality.

**Recommendation**: Delete `run_execute.py` and `run_builder.py` outright instead of wrapping them. If wrappers are kept, define a concrete removal date or condition (e.g., "remove after 2 pipeline runs with no usage").

---

## Challenge 8: No Rollback or Atomicity Requirement

**Confidence: 4/5 -- Minor concern**

The PRD has a risk table (R1-R6) with mitigations but no rollback plan. The refactoring touches 6 existing files and creates 4 new files across 8 functional requirements. If a regression is discovered during UAT after half the changes are merged, the codebase is in a worse state than before -- partially decomposed, with some files importing from `shared.py` and others still hardcoding paths.

**Recommendation**: Add a requirement that all changes land in a single PR (atomic merge). Given git, a simple "revert the PR" note in the risk table would close this gap.

---

## Summary Table

| # | Challenge | Confidence | Verdict |
|---|-----------|-----------|---------|
| 1 | `builder.conn` is undeclared public API | 2/5 | **MUST FIX** before Design |
| 2 | NFR-06 lists non-existent files | 1/5 | **MUST FIX** -- factual error |
| 3 | Output diff unverifiable with timestamp IDs | 2/5 | **MUST FIX** -- redefine verification strategy |
| 4 | Line count targets unsupported | 3/5 | Recommend validating estimates or softening targets |
| 5 | Schema extraction initialization risk | 3/5 | Recommend specifying initialization contract |
| 6 | Out-of-scope boundary creates inconsistency | 3/5 | Recommend explicit acknowledgment |
| 7 | Deprecation wrappers add permanent debt | 4/5 | Recommend deletion over wrappers |
| 8 | No atomicity requirement | 4/5 | Recommend single-PR requirement |

---

## Blocking Assessment

**Three challenges scored <= 2 and must be resolved before proceeding to Design:**

1. **Challenge 2 (confidence 1/5)**: NFR-06 contains phantom file references (`database.py`, `agent_registry.py`). This is a factual error. Fix: correct the file list.

2. **Challenge 1 (confidence 2/5)**: The most-used public interface (`builder.conn`, 14 direct accesses across 3 files) is not acknowledged in the API preservation requirements. Fix: add `builder.conn` to FR-03's public API list or add consumer migration to scope.

3. **Challenge 3 (confidence 2/5)**: The primary success metric (G6/M6: before/after output diff) is not achievable as specified due to non-deterministic timestamp-based IDs. Fix: redefine behavioral compatibility as structural equivalence (node counts, rule counts, gate counts, flow structure) rather than stdout diff.
