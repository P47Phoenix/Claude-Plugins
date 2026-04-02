# Dev Notes: US-04 -- Extract Stage Definitions into Data Module

**Story**: US-04 | **SP**: 5 | **Sprint**: 1
**FR Coverage**: FR-01 (AC-01a through AC-01e)
**File Created**: `prd-quality-gate-flow/stage_definitions.py` (269 lines)

---

## Verification

| AC | Status | Method |
|----|--------|--------|
| AC-4.1 | PASS | len(STAGE_DEFINITIONS) == 7 |
| AC-4.2 | PASS | All dicts have name, description, node_type, config (with agent_type, goal, model) |
| AC-4.3 | PASS (structural) | Load-time validation loop raises KeyError on missing fields |
| AC-4.4 | PASS | No YAML files, Python dicts only |
| AC-4.5 | PASS (structural) | Triple-quoted strings preserve multi-line goal formatting |
| AC-4.6 | PASS | Zero imports from other plugin modules |

## Notes

- REQUIRED_STAGE_FIELDS and REQUIRED_CONFIG_FIELDS validated at import time
- Stage 3 uses node_type="control_flow" (not "agent") -- correctly preserved
- Data file exceeds 300 lines but is purely declarative, per NFR-05 exemption
