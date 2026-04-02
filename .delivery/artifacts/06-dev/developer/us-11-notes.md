# Dev Notes: US-11 -- Update CLAUDE.md Entry Points Documentation

**Story**: US-11 | **SP**: 1 | **Sprint**: 3
**FR Coverage**: FR-08 (AC-08a, AC-08b, AC-08c)
**File**: `CLAUDE.md` (root)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-11.1 | PASS | Running Scripts section lists exactly 4 scripts: prd_flow_builder.py, prd_execute.py, check_db.py, fix_and_run.py |
| AC-11.2 | PASS | `grep -c 'run_execute\|run_builder' CLAUDE.md` returns 0 |
| AC-11.3 | PASS | All 4 documented commands correspond to existing files with main() entry points |

## Notes

- No changes were needed -- CLAUDE.md already listed exactly the 4 canonical scripts
- No references to run_execute.py or run_builder.py were present
- This was verified rather than modified
