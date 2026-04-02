# Dev Notes: US-05 -- Extract Gate Definitions and Business Rules into Data Module

**Story**: US-05 | **SP**: 5 | **Sprint**: 2
**FR Coverage**: FR-02 (AC-02a through AC-02f)
**File Created**: `prd-quality-gate-flow/gate_definitions.py` (411 lines)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-5.1 | PASS | len(GATE_DEFINITIONS) == 7 |
| AC-5.2 | PASS | sum(len(g['rules']) for g in GATE_DEFINITIONS) == 20 |
| AC-5.3 | PASS | All gates have name, description, gate_config, rules; all rules have name, rule_type, condition, priority |
| AC-5.4 | PASS | List index corresponds to pipeline position |
| AC-5.5 | PASS (structural) | Load-time validation raises KeyError on missing fields |
| AC-5.6 | PASS | Zero imports from other plugin modules |

## Notes

- Per-gate rule distribution: [4, 4, 3, 1, 4, 3, 1] -- verified exact match
- Complex nested AND/OR conditions copied verbatim (Gate 1 rule 1, Gate 2 rule 4, Gate 4 rule 1, Gate 5 rule 2, Gate 7 rule 1)
- Data file exceeds 300 lines (411) but is purely declarative data, per NFR-05 exemption
