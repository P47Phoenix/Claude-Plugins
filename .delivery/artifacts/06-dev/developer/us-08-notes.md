# Dev Notes: US-08 -- Restructure fix_and_run.py with Named Functions

**Story**: US-08 | **SP**: 3 | **Sprint**: 3
**FR Coverage**: FR-06 (AC-06a through AC-06f), FR-05 (AC-05b/c partial)
**File Modified**: `prd-quality-gate-flow/fix_and_run.py` (214 -> 290 lines)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-8.1 | PASS | def main() exists, called via `if __name__ == "__main__"` |
| AC-8.2 | PASS | clean_incomplete_executions() function exists |
| AC-8.3 | PASS | demonstrate_bre_evaluation() function exists |
| AC-8.4 | PASS | display_flow_structure() function exists |
| AC-8.5 | PASS | Only imports and __name__ guard at top level |
| AC-8.6 | PASS (structural) | Uses get_connection() which calls ensure_schema() -- latent bug fixed |
| AC-8.7 | PASS | grep '"prd_flows.db"' returns 0 |
| AC-8.8 | PENDING (empirical) | Full CLI run requires existing DB with flow data |

## Functions Extracted

1. `clean_incomplete_executions(db_path)` -- DB cleanup using get_connection()
2. `display_flow_structure(builder, flow_id)` -- Node type breakdown
3. `demonstrate_bre_evaluation(builder, flow_id)` -- Gate 1 BRE demo with test context
4. `display_all_gates(builder, flow_id)` -- All gates overview
5. `display_summary()` -- Demonstration summary text
6. `main()` -- Orchestrates all steps in original execution order

## Latent Bug Fix

Old code: `conn = sqlite3.connect("prd_flows.db")` followed by DELETE queries.
On fresh DB with no tables, this crashes.
New code: `conn = get_connection(db_path)` calls ensure_schema() first.

## Line Count Deviation

290 lines vs design spec estimate of ~210. Increase due to:
- Docstrings on all 6 functions
- test_context dict moved into demonstrate_bre_evaluation()
- Still under NFR-05 limit of 300 lines
