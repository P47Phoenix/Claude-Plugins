# Dev Notes: US-06 -- Decompose PRDFlowBuilder into Thin Orchestrator

**Story**: US-06 | **SP**: 8 | **Sprint**: 2
**FR Coverage**: FR-01 (AC-01c), FR-02 (AC-02c), FR-03 (AC-03a/c/d/d2/e/f), FR-05 (AC-05b/c/d)
**File Modified**: `prd-quality-gate-flow/prd_flow_builder.py` (1,157 -> 259 lines)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-6.1 | PASS | Class body: 162 lines (<=200 target) |
| AC-6.2 | PASS | build_prd_flow() uses for loop over PIPELINE_SEQUENCE; 0 factory methods |
| AC-6.3 | PASS | create_flow(), create_node(), create_rule() all present on class |
| AC-6.4 | PASS | builder.conn is public sqlite3.Connection attribute |
| AC-6.5 | PASS | export_flow_diagram() returns text diagram |
| AC-6.6 | PASS | _count_nodes() returns 15, _count_rules() returns 20 |
| AC-6.7 | PASS | grep '"prd_flows.db"' returns 0 matches |
| AC-6.8 | PASS | No inline timestamp patterns; uses generate_timestamp_id() |
| AC-6.9 | PASS | PIPELINE_SEQUENCE produces exact node ordering including consecutive gates 3-4 and consecutive stages 5-6 |

## Key Design Decisions

- PIPELINE_SEQUENCE defined as module-level constant (orchestration logic, not data)
- Each entry is (type, index) tuple referencing STAGE_DEFINITIONS or GATE_DEFINITIONS
- Stage 3 node_type handled via NodeType(stage["node_type"]) -- works for both "agent" and "control_flow"
- Gate rules created inline during gate node creation (not separate pass)
- __main__ block preserved for CLI compatibility
