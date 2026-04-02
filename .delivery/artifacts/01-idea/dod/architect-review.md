## Architect Review -- Gate 1 (Idea)

**Reviewer**: Celebrimbor (Architect DoD Validator)
**Date**: 2026-03-30
**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Verdict**: DONE

---

### 1. Buildability Assessment

This refactoring is straightforward and fully buildable. The scope is Python-only structural refactoring of existing, working code with no new dependencies, no database schema changes, and no changes to the core engines (`business_rules_engine.py`, `flow_orchestrator.py`, `database.py`, `agent_registry.py`). Every target file exists and I have verified the claimed problems:

- `prd_flow_builder.py`: 1,157 lines confirmed. God object with schema creation, flow building, 12+ factory methods, counting, and diagram export all in one class.
- `run_builder.py` (43 lines) duplicates `prd_flow_builder.py`'s `__main__` block; `run_execute.py` (209 lines) duplicates `prd_execute.py` (226 lines) with minor wrapper differences (UTF-8 encoding, example data).
- `check_db.py`: 26 lines, no function structure, bare module-level execution.
- `fix_and_run.py`: 214 lines, flat procedural code with inline SQL, no function extraction.
- `"prd_flows.db"` hardcoded in 10+ locations across 6 Python files -- confirmed shotgun surgery risk.

No technical blockers identified. All proposed changes are well-understood refactoring patterns.

### 2. Feasibility of Specific Goals

| Goal | Assessment |
|------|------------|
| Reduce `PRDFlowBuilder` from ~1120 to ~200 lines via data file extraction | **Feasible.** The 12 stage/gate factory methods are repetitive data definitions (node names, descriptions, rule configs). Extracting to YAML/JSON data files is a standard pattern. The remaining ~200 lines for schema creation, data loading, and orchestration is realistic. |
| Eliminate duplicate entry points | **Feasible.** `run_builder.py` and `run_execute.py` are thin wrappers adding only UTF-8 encoding. Consolidating the encoding logic into the canonical scripts and removing the wrappers is trivial. |
| Extract `shared.py` for constants | **Feasible.** `DB_PATH` string appears 10+ times. A single constants module eliminates the shotgun surgery. |
| Restructure flat scripts into functions | **Feasible.** `fix_and_run.py` and `check_db.py` are small files; extracting named functions is mechanical. |
| 100% behavioral compatibility | **Feasible with care.** No logic changes are proposed. The risk is import path changes if modules are renamed or restructured. Mitigation: keep existing module names as entry points or add compatibility shims. |

### 3. Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| CLAUDE.md documents `prd_flow_builder.py`, `prd_execute.py`, `check_db.py`, `fix_and_run.py` as CLI entry points. Consolidation must update CLAUDE.md or preserve these paths. | Medium | Brief explicitly calls this out ("or be consolidated with clear migration"). Ensure CLAUDE.md update is in scope for the Plan stage. |
| Data file format choice (YAML vs JSON) affects maintainability. YAML requires `pyyaml` which would violate the "no new dependencies" constraint. | Medium | Use JSON for data files, or use Python dict literals in a separate module. Do not introduce YAML without resolving the dependency constraint. |
| `check_db.py` is referenced in CLAUDE.md as an inspection tool. Renaming functions inside it is safe, but renaming the file itself requires CLAUDE.md update. | Low | Keep filename, improve internals only. |

### 4. Architectural Observations (Non-blocking)

- The brief correctly scopes the work as structural-only. The `business_rules_engine.py` (569 lines) and `flow_orchestrator.py` (598 lines) are intentionally excluded, which is the right call -- they are the core engines and should not be touched in a refactoring pass.
- The proposed `shared.py` module is the right pattern. Consider whether it should also hold the common UTF-8 encoding setup that `run_builder.py` and `run_execute.py` currently duplicate.
- The initial scope section mentions "New data files (YAML/JSON)" -- this must be resolved to JSON-only given the no-new-dependencies constraint, unless Python dict modules are used instead.

---

*What is forged with precision endures. This brief defines clean boundaries and achievable goals -- a worthy foundation.*
