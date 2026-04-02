# Dev Notes: US-03 -- Wire Schema Initialization into Shared Connection Helper

**Story**: US-03 | **SP**: 1 | **Sprint**: 1
**FR Coverage**: FR-03 (AC-03g), FR-05 (AC-05a partial)
**File Modified**: `prd-quality-gate-flow/shared.py`

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-3.1 | PASS | get_connection(':memory:') returns conn with 9 tables, 7 indexes |
| AC-3.2 | PASS | No ImportError -- schema.py has zero internal imports |

## Notes

- get_connection() uses lazy import of ensure_schema to avoid circular imports
- Sets row_factory = sqlite3.Row for dict-like access
- Fixes the latent fresh-database bug documented in PRD AC-03g
