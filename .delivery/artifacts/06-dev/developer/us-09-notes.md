# Dev Notes: US-09 -- Restructure check_db.py with Functions and Error Handling

**Story**: US-09 | **SP**: 2 | **Sprint**: 3
**FR Coverage**: FR-07 (AC-07a through AC-07e), FR-05 (AC-05b/c partial)
**File Modified**: `prd-quality-gate-flow/check_db.py` (27 -> 69 lines)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-9.1 | PASS | def main() exists, called via `if __name__ == "__main__"` |
| AC-9.2 | PASS | list_flows(), list_nodes(), list_rules() -- all descriptive names |
| AC-9.3 | PASS | try/finally with conn.close() |
| AC-9.4 | PASS (structural) | os.path.exists() check with human-readable error + sys.exit(1) |
| AC-9.5 | PASS | grep '"prd_flows.db"' returns 0; `from shared import DB_PATH` present |
| AC-9.6 | PENDING (empirical) | Requires existing DB for output comparison |

## Notes

- Graceful error on missing DB: prints message to stderr, exits with code 1
- get_connection() imported inside main() to avoid triggering DB creation on import
- Output format preserved: same flow/node/rule counts as original
