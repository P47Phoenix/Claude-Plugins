# US-3 — Refine PO constraints template + invocation update

**Alias:** Gimli (Developer)
**Status:** DONE

## Deliverables
1. `delivery-team/skills/delivery-flow/references/templates/constraints-refine.yml`
   — 8-field YAML template, PO-scoped (problem vocabulary, business
   invariants, sprint ceilings, downstream artifacts). Mirrors structure
   of US-4's constraints-architect.yml; distinct scope comments make
   clear this is PROBLEM-scoped, not decomposition-scoped.
2. `delivery-team/skills/delivery-flow/references/fixtures/constraints-refine-sample.yml`
   — Sample emission used to satisfy AC-3.3 (placeholder-only templates
   cannot pass minItems:1 so an instantiated sample is the correct
   self-test target, matching the existing fixtures/ pattern).
3. `pipeline-stages.md` Stage 2 Refine, step 1 — surgical one-line
   addition requiring PO to emit `.delivery/artifacts/02-refine/po/constraints.yml`
   from the template, validated by `scripts/validate_constraints.py`.

## Acceptance Criteria
- AC-3.1: template has all 8 fields in ADR-001 order — PASS
- AC-3.2: Stage 2 Refine invocation requires constraints.yml — PASS
- AC-3.3: sample emission passes US-1 validator — PASS

## Validator self-test
```
$ python delivery-team/skills/delivery-flow/scripts/validate_constraints.py \
    delivery-team/skills/delivery-flow/references/fixtures/constraints-refine-sample.yml
ok: .../constraints-refine-sample.yml is valid against constraints schema
EXIT=0
```
PyYAML present in environment (primary path exercised, not fallback).

## US-7 coordination check
grep confirms both present in pipeline-stages.md:
- Line 250: Stage 2 Refine new line (this US)
- Line 416: `## Stage 5: Plan` header (US-7 renumber intact)
- Line 434: Stage 5 constraints.yml inputs (US-7 content intact)
No conflict.
