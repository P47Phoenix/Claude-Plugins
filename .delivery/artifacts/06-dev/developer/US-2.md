# US-2 — constraints-model-guide.md authoring canon

**Stage**: 6 Development | **Role**: Developer (Gimli) | **Date**: 2026-04-08

## Work
Forged `delivery-team/skills/delivery-flow/references/constraints-model-guide.md` as the single canon for `constraints.yml`. Seven sections per spec: Purpose (Model-First, arXiv:2512.14474), File Locations (Refine + Architect sibling paths), Field Reference (table + 8 per-field subsections with type, required flag, purpose, example, common mistakes), Forbidden Vocabulary Canon (ADR-003, enumerated tokens verbatim), Löwy cross-link for `citations` on volatility runs, Authoring Workflow (PO at Refine, Architect at Decomposition, Plan/Dev read-only), Validation Workflow (points at `constraints-schema.json` + `validate_constraints.py`).

## Inputs consulted
- `.delivery/artifacts/04-architect/adrs/ADR-001-constraints-yml-schema.md`
- `.delivery/artifacts/04-architect/solution/architecture.md` §3, §7
- `delivery-team/skills/delivery-flow/references/constraints-schema.json` (US-1 output)

## Compliance
- Under 200 lines (~135 body lines).
- All 8 fields from ADR-001 documented with required/optional matching schema.
- Forbidden-vocab list restated verbatim per ADR-003 (no inheritance).
- Löwy citation shape matches architecture §3 minimal example.

STATUS: DONE
ARTIFACT: delivery-team/skills/delivery-flow/references/constraints-model-guide.md
