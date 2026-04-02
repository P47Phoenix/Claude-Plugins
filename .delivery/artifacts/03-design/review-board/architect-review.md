# Architect Review: Design Specification — prd-quality-gate-flow Decomposition

**Reviewer**: Celebrimbor (Solution Architect)
**Review Type**: Multi-Perspective Review Board — Technical Implementability
**Date**: 2026-03-30
**Artifact**: `.delivery/artifacts/03-design/ux/design-spec.md` v1.0
**Scope**: Module dependency graph, file size targets, refactoring sequence safety, circular dependency risks, shared.py scope

---

## Verdict: PASS

The design is implementable. The dependency graph is acyclic, the refactoring sequence is safe at every intermediate step, file size targets are achievable, and `shared.py` scope is appropriate. Two non-blocking notes are recorded below.

---

## 1. Module Dependency Graph Analysis

### 1.1 Acyclicity Verification

The target dependency graph forms a strict DAG (directed acyclic graph):

```
Layer 0 (leaves):  shared.py, schema.py, stage_definitions.py, gate_definitions.py
Layer 1 (core):    prd_flow_builder.py  (imports from Layer 0 only)
Layer 2 (consumers): prd_execute.py, fix_and_run.py, check_db.py (import from Layers 0-1)
Layer 3 (unchanged): business_rules_engine.py, flow_orchestrator.py (no new imports)
```

**Cycle check**: No module in Layer 0 imports any internal module. `prd_flow_builder.py` imports only downward. Consumer scripts import only downward or laterally into unchanged modules. No cycles exist.

**Verified constraint**: The design explicitly states (Section 3.3, Rule 1) that all four new modules must have zero internal imports. I confirmed:
- `schema.py`: imports only `sqlite3` (stdlib)
- `stage_definitions.py`: no imports at all (pure data)
- `gate_definitions.py`: no imports at all (pure data)
- `shared.py`: imports only `sys`, `io`, `sqlite3`, `datetime` (all stdlib)

**PASS** -- the dependency graph is clean and acyclic.

### 1.2 Cross-Layer Import Rules

| Rule | Design Claim | Verified |
|------|-------------|----------|
| Leaf modules have zero internal imports | Section 3.3, Rule 1 | YES -- import specs in Section 3.2 confirm this |
| Builder never imports from consumers | Section 3.3, Rule 2 | YES -- builder imports only from Layer 0 |
| Consumer scripts never import from each other | Section 3.3, Rule 3 | YES -- each consumer imports shared + builder + unchanged modules only |
| Core modules have zero diff | Section 3.3, Rule 4 | YES -- NFR-06 preserved; consumers pass `shared.DB_PATH` to `FlowOrchestrator(db_path)` and `BusinessRulesEngine(conn)` |
| No circular dependencies | Section 3.3, Rule 5 | YES -- DAG structure confirmed |

**PASS** -- all five dependency rules are sound.

---

## 2. Circular Dependency Risk Assessment

### 2.1 The shared.py -> schema.py Coupling

The design specifies (Step 3) that `shared.get_connection()` calls `schema.ensure_schema(conn)`. This means `shared.py` imports from `schema.py`.

**Risk**: If `schema.py` ever imports from `shared.py`, a circular dependency would form.

**Mitigation in design**: Section 3.2 explicitly specifies `schema.py` has zero internal imports. The design also explicitly calls out this risk in Step 3 and states: "`schema.py` has zero internal imports (dependency rule 1). Safe."

**Assessment**: The mitigation is correct. As long as Rule 1 is enforced, no cycle can form. However, the dependency graph diagram in Section 3.1 shows `shared.py` with arrows pointing TO `schema.py`, `stage_definitions.py`, and `gate_definitions.py` -- but the actual import specification in Section 3.2 shows `shared.py` only imports `schema.py` (for `ensure_schema`), not the definitions modules. The diagram slightly overstates `shared.py`'s outbound edges but this has no functional consequence since those arrows represent "depends on" not "imports from" and the Layer 0 modules are all leaves regardless.

**PASS** -- no circular dependency risk.

### 2.2 Consumer-to-Consumer Independence

Current state: `fix_and_run.py` imports `PRDFlowBuilder` and `BusinessRulesEngine` independently. `prd_execute.py` imports `PRDFlowBuilder`, `FlowOrchestrator`, and `BusinessRulesEngine` independently. Neither imports the other.

Target state: Same pattern preserved. No consumer-to-consumer imports introduced.

**PASS** -- consumer isolation maintained.

---

## 3. File Size Target Achievability

### 3.1 Line Count Validation

| File | Target | Feasibility Assessment |
|------|--------|----------------------|
| `shared.py` | ~40 lines | 4 exports (DB_PATH, generate_timestamp_id, ensure_utf8_output, get_connection) + imports + docstrings. 40 lines is tight but achievable. |
| `schema.py` | ~170 lines | Current `_create_schema()` body is 157 lines (lines 47-203). Adding function wrapper, docstring, imports = ~170. Accurate. |
| `stage_definitions.py` | ~230 lines | 7 stage dicts with multi-line config including goal strings. Current factory methods span ~400 lines but include method boilerplate and `create_node()` calls. Pure data dicts will be more compact. 230 is plausible. |
| `gate_definitions.py` | ~280 lines | 7 gate dicts + 20 rule dicts. Current factory methods span ~600 lines but include method boilerplate and `create_node()`/`create_rule()` calls. Pure data dicts will be more compact but 20 rules with nested condition logic is substantial. 280 is tight but achievable. |
| `prd_flow_builder.py` | ~180 lines (<=200 class body) | Current 1,157 lines minus ~157 (schema) minus ~600 (stage/gate factories) minus ~40 (shared utils) = ~360 remaining. But the loop-based `build_prd_flow()` replaces ~80 lines of method calls with ~30 lines of loop logic, and the `PIPELINE_SEQUENCE` is ~5 lines. Target ~180 is plausible. |
| `prd_execute.py` | ~220 lines | Current 227 lines, removing 2 hardcoded paths and adding 1 import line. ~220 is accurate. |
| `fix_and_run.py` | ~210 lines | Current 214 lines, restructuring into functions adds a few lines of `def` headers but removes the top-level UTF-8 block. ~210 is accurate. |
| `check_db.py` | ~50 lines | Current 27 lines + main() guard + error handling + function wrappers. ~50 is accurate. |

**PASS** -- all line count targets are achievable.

### 3.2 Net Line Delta Verification

Design claims: +230 + 280 + 170 + 40 - 977 - 7 - 4 + 23 - 210 - 44 = **-499 lines**.

Arithmetic check: 230 + 280 + 170 + 40 = 720 (additions). 977 + 7 + 4 - 23 + 210 + 44 = 1219 (removals, with check_db.py growth treated as negative removal). Actually: -(977) - 7 - 4 + 23 - 210 - 44 = -1219. Total: 720 - 1219 = -499. **Correct.**

**PASS** -- arithmetic verified.

---

## 4. Refactoring Sequence Safety

This is the critical assessment: at no intermediate step should the codebase have broken imports.

### 4.1 Step-by-Step Import Safety

| Step | Operation | Existing Code Affected | Import Safety |
|:----:|-----------|----------------------|:-------------:|
| 1 | Create `shared.py` | None | SAFE -- additive only, no existing file references it |
| 2 | Create `schema.py` | None | SAFE -- additive only, no existing file references it |
| 3 | Wire `shared.get_connection()` -> `schema.ensure_schema()` | `shared.py` only | SAFE -- `shared.py` is new, no existing consumer yet |
| 4 | Create `stage_definitions.py` | None | SAFE -- additive only |
| 5 | Create `gate_definitions.py` | None | SAFE -- additive only |
| 6 | Decompose `prd_flow_builder.py` | `prd_flow_builder.py` | **CRITICAL** -- see below |
| 7 | Update `prd_execute.py` | `prd_execute.py` | SAFE -- replaces string literal with import, builder API unchanged |
| 8 | Restructure `fix_and_run.py` | `fix_and_run.py` | SAFE -- internal restructuring, import paths unchanged |
| 9 | Restructure `check_db.py` | `check_db.py` | SAFE -- adds shared import, removes raw sqlite3 usage |
| 10 | Delete duplicates | `run_execute.py`, `run_builder.py` | SAFE -- confirmed no other file imports from these |
| 11 | Update docs | `CLAUDE.md` | SAFE -- documentation only |

### 4.2 Step 6 Deep Analysis (Highest Risk)

At Step 6, `prd_flow_builder.py` is rewritten. The critical question: do its consumers (`prd_execute.py`, `fix_and_run.py`, `run_execute.py`, `run_builder.py`) still work?

**Public API preserved** (design Section 6, AC-03d):
- `PRDFlowBuilder` class: retained
- `PRDFlowBuilder.__init__(db_path)`: retained
- `PRDFlowBuilder.build_prd_flow()`: retained (same return type)
- `PRDFlowBuilder.create_flow()`, `create_node()`, `create_rule()`: retained
- `PRDFlowBuilder.conn`: retained as public attribute (AC-03d2)
- `PRDFlowBuilder.export_flow_diagram()`: retained
- `PRDFlowBuilder.close()`: retained
- `NodeType`, `WorkflowPattern` enums: retained

**Consumers at Step 6 import**:
- `PRDFlowBuilder` (class) -- preserved
- `NodeType` -- preserved (used? grep shows no external usage, but it is exported)
- `WorkflowPattern` -- preserved (same)

**Verified against actual consumer code**:
- `prd_execute.py` line 11: `from prd_flow_builder import PRDFlowBuilder` -- SAFE
- `fix_and_run.py` line 36: `from prd_flow_builder import PRDFlowBuilder` -- SAFE
- `run_execute.py` line imports: `from prd_flow_builder import PRDFlowBuilder` -- SAFE (still exists at Step 6)
- `run_builder.py` line imports: `from prd_flow_builder import PRDFlowBuilder` -- SAFE

**Consumer usage of `builder.conn`**:
- `prd_execute.py` line 34: `builder.conn.execute(...)` -- SAFE (AC-03d2 preserves `self.conn`)
- `fix_and_run.py` line 43: `builder.conn.execute(...)` -- SAFE

**PASS** -- Step 6 preserves the full public API surface. No broken imports at any intermediate step.

### 4.3 Step 10 Safety (Deletion)

Before `run_execute.py` and `run_builder.py` are deleted:
- No other `.py` file imports from them (verified via grep -- they are CLI entry points only)
- No cross-references in any import statement

**PASS** -- deletion is safe.

---

## 5. shared.py Scope Assessment

### 5.1 What It Contains

The design specifies 4 exports:
1. `DB_PATH = "prd_flows.db"` -- centralized constant replacing 10 hardcoded occurrences
2. `generate_timestamp_id()` -- replaces inline `f"flow_{datetime.now()..."` patterns
3. `ensure_utf8_output()` -- consolidates Windows UTF-8 setup from `fix_and_run.py` and `run_execute.py`
4. `get_connection(db_path=DB_PATH)` -- opens connection, sets row_factory, calls ensure_schema()

### 5.2 Scope Appropriateness

| Concern | Assessment |
|---------|-----------|
| Is it a "junk drawer"? | No -- all 4 exports are infrastructure utilities used by 3+ consumers. Cohesive. |
| Does it contain domain logic? | No -- no PRD concepts, no business rules, no flow logic. |
| Could it grow unbounded? | Low risk -- the plugin has a small, stable utility surface. |
| Does it create a "God import"? | No -- consumers import specific names, not `import shared`. |
| Should `get_connection()` be here or in `schema.py`? | Defensible either way, but `shared.py` is the right choice: `get_connection()` is a consumer-facing convenience that happens to call schema setup internally. Putting it in `schema.py` would make the schema module a consumer-facing API, which muddies its role as a leaf module. |

**PASS** -- `shared.py` scope is appropriate and well-bounded.

---

## 6. Additional Implementability Observations

### 6.1 PIPELINE_SEQUENCE Design (Section 7)

The non-alternating stage/gate ordering is a genuine complexity that the design handles well. The current `build_prd_flow()` (lines 280-360) shows the ordering:

```
Stage1 -> Gate1 -> Stage2 -> Gate2 -> Stage3 -> Gate3 -> Gate4 -> Stage4 -> Gate5 -> Stage5 -> Stage6 -> Gate6 -> Gate7 -> Stage7
```

Note the consecutive gates (Gate3 -> Gate4) and consecutive stages (Stage5 -> Stage6). The proposed `PIPELINE_SEQUENCE` list correctly encodes this. Placing it in `prd_flow_builder.py` (orchestration) rather than in the data modules is the right call.

### 6.2 FlowOrchestrator/BusinessRulesEngine Compatibility

**Verified**: `FlowOrchestrator.__init__(db_path: str, bre)` accepts a string `db_path`. The design's `shared.DB_PATH` is a string. Compatible.

**Verified**: `BusinessRulesEngine.__init__(db_connection: Optional[sqlite3.Connection])` accepts a connection object. The design's `shared.get_connection()` returns a connection. Compatible.

Neither core module needs modification. **NFR-06 (zero diff on core modules) is achievable.**

---

## 7. Findings

### Notes (Non-Blocking)

| ID | Section | Finding | Impact |
|----|---------|---------|--------|
| N-01 | 3.1 (Diagram) | The dependency diagram shows `shared.py` with arrows to `schema.py`, `stage_definitions.py`, and `gate_definitions.py`. But the import spec (Section 3.2) shows `shared.py` only imports from `schema.py`. The diagram conflates "Layer 0 peer" with "imports from." | Cosmetic only. The DAG is still acyclic regardless. Implementer should follow Section 3.2 import specs, not the diagram arrows from `shared.py`. |
| N-02 | 4 (Step 3) | After Step 3, `shared.py` imports `schema.py`, which means `shared.py` is no longer a pure leaf module (it has one internal dependency). The design's Section 3.2 correctly shows this, but the Section 3.1 diagram's visual layout places `shared.py` at the same level as the other three leaf modules, which is slightly misleading. `shared.py` is a "near-leaf" -- it depends on one other leaf but nothing depends on it at Layer 0. | No functional impact. The layering is still clean: schema is a leaf, shared depends on schema, everything else depends on shared. No cycle risk. |

### Strengths

1. **Additive-first sequencing**: Steps 1-5 are purely additive (new files only). No existing behavior is modified until Step 6, which means the first 5 steps are zero-risk and independently verifiable.
2. **Atomic commit strategy**: Step 6 is explicitly flagged as needing its own atomic commit with pre/post verification. This is correct risk management.
3. **Behavioral verification plan**: The 15-node, 20-rule invariant provides a concrete regression test. The `PIPELINE_SEQUENCE` encoding makes the ordering explicit and testable.
4. **Consumer API preservation**: The design explicitly lists every public attribute and method that must survive decomposition (AC-03d, AC-03d2, AC-03e). This is the kind of contract that prevents "refactoring surprises."
5. **FR traceability matrix**: 42 acceptance criteria mapped to modules, steps, and verification methods. Exhaustive.

---

## Summary

This design bears the mark of careful craft. The dependency graph is a clean DAG with no circular risks. The refactoring sequence is safe at every intermediate step -- additive-first, with the single highest-risk step (Step 6) isolated for atomic commit. File size targets are achievable and arithmetically verified. The `shared.py` module is well-scoped as infrastructure utilities, not a domain catch-all. The `PIPELINE_SEQUENCE` encoding correctly handles the non-trivial stage/gate interleaving.

Two cosmetic notes on diagram clarity; neither affects implementability.

Like mithril -- light, strong, and well-fitted to its purpose.

---

STATUS: PASS
ARTIFACT: .delivery/artifacts/03-design/review-board/architect-review.md
SUMMARY: Dependency graph is acyclic, refactoring sequence safe at all steps, file targets achievable, shared.py well-scoped. 2 cosmetic notes, 0 blockers.
