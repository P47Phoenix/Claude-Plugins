# US-1 Developer Log — constraints.yml schema + validator

**Author**: Gimli (developer) | **Date**: 2026-04-08 | **Status**: DONE

## Files Created

1. `delivery-team/skills/delivery-flow/references/constraints-schema.json` — JSON Schema draft-07. 8 top-level props per ADR-001. `entities` + `invariants` required. `additionalProperties: true` for forward-compat (AC-1.4). Citations shape `{work, chapter, page}` enforced.
2. `delivery-team/skills/delivery-flow/scripts/validate_constraints.py` — Python 3 headless validator. Prefers PyYAML (already in BRE stack), falls back to a minimal line-based parser if PyYAML is absent so the narrow required-field check still runs. Validation is hand-rolled (stdlib-only, no `jsonschema` dep): top level must be a mapping; `entities`/`invariants` required and non-empty list-of-strings; optional fields shape-checked if present; unknown top-level keys ignored. Exit 0 / 1. Errors to stderr.
3. `delivery-team/skills/delivery-flow/references/fixtures/constraints-valid.yml` — all 8 fields populated minimally.
4. `delivery-team/skills/delivery-flow/references/fixtures/constraints-invalid-missing-entities.yml` — red fixture, no `entities`.
5. `delivery-team/skills/delivery-flow/references/fixtures/constraints-forward-compat.yml` — required fields + unknown `future_field`.

## Test Results

```
$ python3 validate_constraints.py constraints-valid.yml
ok: ... is valid against constraints schema    → exit 0  PASS

$ python3 validate_constraints.py constraints-forward-compat.yml
ok: ... is valid against constraints schema    → exit 0  PASS (AC-1.4)

$ python3 validate_constraints.py constraints-invalid-missing-entities.yml
error: ... is INVALID against constraints schema:
  - missing required field: entities          → exit 1  PASS (AC-1.3)
```

All three ACs exercised:
- AC-1.1: 8 top-level fields defined in schema.
- AC-1.2: only `entities` + `invariants` marked required.
- AC-1.3: red fixture exits non-zero with clear stderr message.
- AC-1.4: forward-compat fixture with unknown field exits zero.

## Deviations from Plan

- Validator does not depend on the `jsonschema` package. The story plan permitted either `jsonschema` or a narrow hand-rolled check; I chose the narrow check to honour the stdlib-only repo convention. PyYAML is used when available (it's already present here: 6.0.2) with a graceful fallback parser for environments without it.
- PyYAML was available in this environment, so the empirical run above used the real YAML loader, not the fallback path. Fallback path is unit-reachable via `_load_yaml_fallback` but not exercised by these fixtures.

## DoD Check

- [x] Schema under `delivery-team/skills/delivery-flow/references/`
- [x] Validator headless (pure CLI, no prompts)
- [x] Red fixture fails with non-zero exit + clear error
- [x] Green fixtures pass with exit 0
- [x] Forward-compat fixture passes (AC-1.4)
