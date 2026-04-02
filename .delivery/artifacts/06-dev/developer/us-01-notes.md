# Dev Notes: US-01 -- Create Shared Constants Module

**Story**: US-01 | **SP**: 2 | **Sprint**: 1
**FR Coverage**: FR-05 (AC-05a, AC-05b partial, AC-05c partial, AC-05d partial)
**File Created**: `prd-quality-gate-flow/shared.py` (60 lines)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-1.1 | PASS | `from shared import DB_PATH; print(DB_PATH)` returns `prd_flows.db` |
| AC-1.2 | PASS | `generate_timestamp_id("flow")` returns `flow_YYYYMMDD_HHMMSS` format |
| AC-1.3 | PASS | `ensure_utf8_output()` wraps stdout/stderr on Windows, no-op elsewhere |
| AC-1.4 | PASS | Imports only sys, io, sqlite3, datetime (all stdlib) |

## Notes

- `generate_timestamp_id()` uses microseconds for non-flow prefixes to avoid collisions in rapid node/rule creation
- `get_connection()` added in US-03 wiring step
- No deviations from design spec
