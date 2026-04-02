# Dev Notes: US-02 -- Extract Database Schema to Standalone Module

**Story**: US-02 | **SP**: 3 | **Sprint**: 1
**FR Coverage**: FR-03 (AC-03b, AC-03g partial)
**File Created**: `prd-quality-gate-flow/schema.py` (174 lines)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-2.1 | PASS | `from schema import ensure_schema; print('OK')` succeeds |
| AC-2.2 | PASS | In-memory DB produces 9 tables and 7 indexes |
| AC-2.3 | PASS | Double-call to ensure_schema() is idempotent |
| AC-2.4 | PASS | Imports only sqlite3, zero internal imports |

## Notes

- SQL copied verbatim from original _create_schema()
- 9 tables, 7 indexes, all using CREATE IF NOT EXISTS
