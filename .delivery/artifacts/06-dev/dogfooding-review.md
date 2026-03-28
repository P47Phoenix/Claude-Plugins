# Dogfooding Review: Clean Code Analysis (FR-23)

**Date**: 2026-03-27
**Reviewer**: Developer (dogfooding)
**Enforcement Level**: WARN
**Reference**: clean-code.md (language-agnostic + Python conventions)

---

## Scope

18 Python files across 3 directories:

| Directory | Files |
|-----------|-------|
| `delivery-team/hooks/` | 7 files (incl. lib/) |
| `delivery-team/scripts/` | 3 files |
| `prd-quality-gate-flow/` | 8 files |

---

## File-by-File Findings

### delivery-team/hooks/lib/hook_utils.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 50 | Error Handling | `read_hook_input()` catches `(json.JSONDecodeError, Exception)` -- `Exception` already subsumes `JSONDecodeError`, making the specific catch redundant. Returns empty dict silently, swallowing all parse errors without logging | WARN |
| 51 | Code Smells | `get_transcript_path()` constructs `Path(path)` twice (line 63 for `.exists()` check, line 64 for return). Should assign to a local variable | WARN |

**Verdict**: Clean and well-factored utility module. Small focused functions, good doc comments, clear naming. Only minor issues.

---

### delivery-team/hooks/audit_agent_prompt.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 1 | Magic Values | Magic number `5000` (prompt length threshold) and `2` (code fence count) lack named constants | WARN |

**Verdict**: Clean. Single-responsibility, short functions, clear names.

---

### delivery-team/hooks/flag_empirical_validation.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 2 | Function Size | `main()` is 58 lines (30+ line refactoring signal). Transcript parsing, AC filtering, and match reporting are mixed | WARN |
| 3 | Comment Quality | Inline comments like `# Visual / Rendering` are useful but the PATTERNS list lacks a module-level explanation of what constitutes "empirical" | WARN |

**Verdict**: Functional but main() does too many things. Extract `_extract_transcript_text()` and `_find_empirical_matches()`.

---

### delivery-team/hooks/validate_gdscript.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 4 | Error Handling | Three `exit_success()` calls silently swallow different failure conditions (file missing, godot missing, timeout). No logging distinguishes these | WARN |

**Verdict**: Clean structure. Silent swallowing is intentional (graceful degradation) but should at minimum log at DEBUG level.

---

### delivery-team/hooks/verify_skill_load.py

No findings. Clean, focused, short.

---

### delivery-team/hooks/enforce_pipeline_scope.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 5 | Function Size | `_parse_yaml_list()` is 37 lines with multiple parsing branches (inline vs block). Could extract `_parse_inline_yaml_list()` and `_parse_block_yaml_list()` | WARN |
| 6 | Comment Quality | Section divider comments (`# ---------------------------------------------------------------------------`) are formatting noise; the function names are already descriptive | WARN |
| 7 | Error Handling | Top-level `except Exception: sys.exit(0)` catches all errors silently. This is documented as intentional but violates "never swallow errors silently" | WARN |

**Verdict**: Well-structured with good separation of concerns. The regex-based YAML parsing is inherently complex but documented.

---

### delivery-team/hooks/check_config.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 8 | Function Size | `main()` is 55 lines. Config validation, clean code guide check, and enforcement check are all in one function | WARN |
| 9 | Meaningful Names | Variables `version_match`, `date_match`, `clean_code_guide_match`, `enforcement_match` follow a pattern but the regex extraction logic is duplicated 4 times | WARN |
| 10 | Code Smells | Primitive obsession: building `message` string via repeated concatenation (`message += ...`) across 15+ lines. Consider a list of message parts joined at the end | WARN |

**Verdict**: Works but should be refactored into `_validate_clean_code_guide()` and `_validate_enforcement()` helper functions.

---

### delivery-team/scripts/generate-schema.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 11 | Function Size | `parse_valid_values()` is 73 lines with 10+ conditional branches. Multiple concerns: range parsing, subset parsing, enum detection, generic pattern exclusion | WARN |
| 12 | Magic Values | `generic_patterns` list (lines 129-136) is an inline magic list. Should be a module-level constant `GENERIC_VALUE_PATTERNS` | WARN |
| 13 | Code Smells | `parse_default()` has a redundant boolean check on line 180: `type_val == "boolean" or (isinstance(type_val, str) and type_val == "boolean")` -- the second clause is always true when the first is | WARN |
| 14 | Function Parameters | `set_nested()` has 4 parameters and mutates `root` in place. Side effect is not obvious from the name | WARN |

**Verdict**: Functional script but `parse_valid_values()` is a clear long-function smell. Should be decomposed by value type.

---

### delivery-team/scripts/validate-config.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 15 | Error Handling | `sys.exit(2)` used in 4 places for different error conditions. Exit codes should be named constants or an enum | WARN |
| 16 | Meaningful Names | `labels` dict in `print_errors()` maps internal keys to display names -- good pattern, no issue. But `errs` is an unnecessary abbreviation of `errors` | WARN |

**Verdict**: Clean script with good separation of concerns. Minor naming nitpick.

---

### delivery-team/scripts/session_keepalive.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 17 | Class Size | `SessionKeepalive` is ~230 lines with 15+ methods. Approaching the 200-line refactoring signal | WARN |
| 18 | Magic Values | Magic numbers: `1_000_000` (log max bytes), `2` (backup count), `1` (sleep interval in seconds) lack named constants | WARN |
| 19 | Code Smells | `WindowsDriver._FOCUS_SCRIPT` embeds a multi-line C# + PowerShell script as a string constant. This is a boundary concern that could be extracted to a separate file | WARN |
| 20 | Comment Quality | Section divider comments (`# ---------------------------------------------------------------------------`) appear 5 times. Redundant with class/function structure | WARN |
| 21 | Error Handling | `WindowsDriver.is_target_focused()` and `send_text()` use bare `except Exception` catch-all handlers | WARN |

**Verdict**: Well-designed cross-platform architecture. The main class is at the upper bound of acceptable size. Driver pattern is a good use of polymorphism.

---

### prd-quality-gate-flow/business_rules_engine.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 22 | Function Size | `evaluate_gate()` is 85+ lines. Combines rule evaluation, score calculation, decision logic, and audit logging | WARN |
| 23 | Code Smells | Timestamp-based ID generation (`datetime.now().strftime('%Y%m%d%H%M%S%f')`) repeated in `_log_gate_evaluation()` -- should be a utility function | WARN |
| 24 | Dead Code | `if __name__ == "__main__"` block (lines 522-569) contains test code that should be in a separate test file | WARN |
| 25 | Meaningful Names | Type hints use `Dict` and `List` from `typing` module but Python 3.9+ supports `dict` and `list` natively | WARN |

**Verdict**: Core engine is solid with good separation of evaluation logic. `evaluate_gate()` is the main refactoring target.

---

### prd-quality-gate-flow/check_db.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 26 | Code Smells | No function structure -- entire script is top-level imperative code with no `main()` function | WARN |
| 27 | Error Handling | No error handling for database connection or query failures | WARN |
| 28 | Meaningful Names | Module docstring is `"""Check database contents"""` -- too vague. Does not explain what it checks or why | WARN |

**Verdict**: Quick utility script but violates basic clean code structure. Should have a `main()` function and error handling.

---

### prd-quality-gate-flow/fix_and_run.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 29 | Function Size | Entire script is ~210 lines of top-level imperative code with no function decomposition | WARN |
| 30 | Code Smells | Hardcoded database path `"prd_flows.db"` appears 2 times as a magic string | WARN |
| 31 | Dead Code | Large inline string (lines 180-212) duplicates README-style documentation as a print statement | WARN |
| 32 | Error Handling | No error handling around database operations or BRE evaluation | WARN |

**Verdict**: Demonstration script with no structure. The worst offender in the repo for clean code violations.

---

### prd-quality-gate-flow/flow_orchestrator.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 33 | Function Size | `_simulate_agent_output()` is 77 lines of hardcoded dictionaries. Should be loaded from fixtures or a data file | WARN |
| 34 | Class Size | `FlowOrchestrator` is ~260 lines. Beyond the 200-line refactoring signal | WARN |
| 35 | Code Smells | Timestamp-based ID generation pattern repeated (same as business_rules_engine.py) -- shotgun surgery smell | WARN |
| 36 | Meaningful Names | Type hints use deprecated `typing.Dict`, `typing.List`, `typing.Optional` instead of built-in `dict`, `list`, `X | None` | WARN |

**Verdict**: Good architecture with clear node execution pattern. Class is oversized due to simulation code that should be extracted.

---

### prd-quality-gate-flow/prd_execute.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 37 | Code Smells | `EXAMPLE_PRODUCT_IDEAS` dict (lines 151-187) duplicates data also found in `run_execute.py`. DRY violation | WARN |
| 38 | Function Size | `execute_prd_workflow()` is 90+ lines mixing orchestration, status reporting, audit trail printing, and file export | WARN |
| 39 | Error Handling | `traceback.print_exc()` imported inside except block (lazy import) rather than at module level | WARN |

**Verdict**: Functional but has significant duplication with `run_execute.py`.

---

### prd-quality-gate-flow/prd_flow_builder.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 40 | Class Size | `PRDFlowBuilder` is ~1120 lines. Far exceeds the 200-line signal. The class is a god object combining schema creation, flow building, 12 stage/gate factory methods, counting, and diagram export | WARN |
| 41 | Function Size | `_create_schema()` is ~150 lines of DDL. Should be loaded from a .sql file or use a migration pattern | WARN |
| 42 | Code Smells | Each `_create_stage*` and `_create_gate*` method follows an identical pattern with large inline config dicts. The data should be externalized | WARN |
| 43 | Magic Values | Hardcoded string `"prd_flows.db"` appears in both the class default and `__main__` block | WARN |
| 44 | Meaningful Names | Type hints use deprecated `typing.Dict`, `typing.List`, `typing.Optional` | WARN |

**Verdict**: The largest single-class file in the repo. The builder pattern is sound but the class has grown into a god object with all stage/gate definitions inlined.

---

### prd-quality-gate-flow/run_builder.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 45 | Code Smells | Thin wrapper that duplicates the `__main__` block of `prd_flow_builder.py`. One of these should be removed | WARN |
| 46 | Magic Values | Hardcoded `"prd_flows.db"` and `"prd_flow_diagram.txt"` | WARN |

**Verdict**: Unnecessary wrapper. Should either replace or defer to `prd_flow_builder.py`'s main block.

---

### prd-quality-gate-flow/run_execute.py

| # | Principle | Finding | Severity |
|---|-----------|---------|----------|
| 47 | Code Smells | `EXAMPLE_PRODUCT_IDEAS` is a full duplicate of the same dict in `prd_execute.py`. Shotgun surgery / DRY violation | WARN |
| 48 | Code Smells | `execute_prd_workflow()` is a near-duplicate of the same function in `prd_execute.py` with minor formatting differences | WARN |
| 49 | Magic Values | Hardcoded `"prd_flows.db"` appears twice | WARN |

**Verdict**: Nearly identical to `prd_execute.py`. These two files should be consolidated.

---

## Summary by Category

| Category | Count | Files Affected |
|----------|-------|----------------|
| Function Size (30+ lines) | 8 | flag_empirical_validation, check_config, generate-schema, business_rules_engine, fix_and_run, flow_orchestrator, prd_execute, prd_flow_builder |
| Class Size (200+ lines) | 3 | session_keepalive, flow_orchestrator, prd_flow_builder |
| Magic Values | 7 | audit_agent_prompt, generate-schema, session_keepalive, fix_and_run, prd_flow_builder, run_builder, run_execute |
| Code Smells (duplication, dead code, god object) | 11 | hook_utils, check_config, business_rules_engine, check_db, fix_and_run, flow_orchestrator, prd_execute, prd_flow_builder, run_builder, run_execute (x2) |
| Error Handling | 6 | hook_utils, validate_gdscript, enforce_pipeline_scope, validate-config, session_keepalive, check_db |
| Meaningful Names | 4 | check_db, validate-config, business_rules_engine, prd_flow_builder |
| Comment Quality | 3 | flag_empirical_validation, enforce_pipeline_scope, session_keepalive |
| **Total** | **51** | **18 files** |

---

## Overall Clean Code Health Assessment

**Health Rating**: FAIR

**Hooks directory** (7 files incl. lib/): GOOD. Small, focused scripts following the hook contract. `hook_utils.py` is a clean shared utility module. Minor issues around function size in 2 files and silent error swallowing.

**Scripts directory** (3 files): GOOD. `generate-schema.py` has the most complexity but is well-structured. `session_keepalive.py` demonstrates solid OOP design with the driver pattern.

**prd-quality-gate-flow** (8 files): NEEDS IMPROVEMENT. This directory has the highest density of clean code violations:
- `prd_flow_builder.py` is a 1100+ line god object
- `run_execute.py` and `prd_execute.py` are near-duplicates
- `run_builder.py` duplicates `prd_flow_builder.py`'s main block
- `fix_and_run.py` and `check_db.py` lack basic function structure
- Hardcoded `"prd_flows.db"` appears in 5+ files (shotgun surgery)

**Top 3 Recommended Refactorings**:
1. Consolidate `prd_execute.py` / `run_execute.py` and `run_builder.py` into single entry points (eliminates 10+ findings)
2. Extract `PRDFlowBuilder` stage/gate definitions into data files, reducing the class from 1100+ to ~200 lines
3. Extract shared constants (`DB_PATH`, timestamp ID generator) into a `shared.py` module to eliminate shotgun surgery
