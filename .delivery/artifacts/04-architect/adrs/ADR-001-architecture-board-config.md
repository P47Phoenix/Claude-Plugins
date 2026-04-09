# ADR-001 — `architecture_board` Config Block Schema

**Status:** Accepted
**Date:** 2026-04-08
**Stage:** 4 Architect (light)
**Forged by:** Celebrimbor

## Context

PRD FR-1 requires a config block to specify reviewer roster, iteration ceiling, convergence criterion, and judge persona for the new configurable architecture board. Today `config-schema.md` has no such block; the existing Multi-Perspective Review Board (team-patterns.md:334) is hardcoded. We must choose how and where a human declares board composition per run, without breaking backwards compatibility (NFR-2) and without inflating the schema beyond constraints.yml `schema_field_count_max: 8` at any nested tier.

## Decision

Introduce a single optional top-level block in `.delivery/config.yml` named `architecture_board`:

```yaml
architecture_board:
  enabled: false        # default — backwards compat
  reviewers:
    - volatility-architect
    - ddd-architect
    - risk-architect
  max_iterations: 2
  convergence: all-done  # all-done | judge-pass | majority-pass
  judge: chief-architect
  cross_persona_iteration2: true
```

Seven fields, all optional except `enabled`. Absent block = disabled (NFR-2). Validated by `validate_config.py` (existing toolchain). Documented in `delivery-team/skills/delivery-flow/references/config-schema.md` under the v2.8 extension protocol.

## Alternatives Considered

### A1 — Inline reviewers in `pipeline-stages.md`

Hardcode the reviewer list in the Stage 4 spec. **Rejected:** defeats FR-1's "configurable per run" requirement; forces a schema edit for every roster change; violates the PRD's dogfooding goal of per-run composition.

### A2 — Nest under existing `review_board` key

Extend the existing Multi-Perspective Review Board config (if one existed) or piggyback on another block. **Rejected:** no such block exists today; inventing one and overloading it conflates the fixed Pattern 3 with the new configurable Pattern 3b and risks breaking Pattern 3 consumers. A new sibling block preserves isolation.

## Consequences

**Positive**
- Backwards compatible — absent block = no-op (NFR-2, AC-9).
- Per-run composition via a single config edit (FR-1).
- Field count well under `schema_field_count_max: 8`.
- `validate_config.py` extension is additive.

**Negative**
- Adds one top-level config concept humans must learn (mitigated by config-schema.md docs + constraints-model-guide.md cross-link).
- Two review-board patterns now coexist in `team-patterns.md` (Pattern 3 fixed, Pattern 3b configurable); documentation must be explicit about which to use when.

## Rationale

A separate, opt-in, flat config block is the cheapest reversible decision that satisfies FR-1, FR-2, and NFR-2 simultaneously. It preserves the existing Review Board contract, keeps schema growth bounded, and lets the dogfood run (FR-8) enable the board without touching any Markdown reference file.

## References

- PRD: `.delivery/artifacts/02-refine/po/prd.md` FR-1, FR-8, NFR-2, AC-9
- Constraints: `.delivery/artifacts/02-refine/po/constraints.yml` (`schema_field_count_max: 8`)
- Augments: `delivery-team/skills/delivery-flow/references/team-patterns.md` Pattern 3 (line 334)
- Target: `delivery-team/skills/delivery-flow/references/config-schema.md`
