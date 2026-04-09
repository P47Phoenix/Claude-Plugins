# constraints.yml Templates

Templates for the Paired Constraints Primitive (see
`../constraints-model-guide.md` for the canonical 8-field schema and
`../../../../delivery-team/skills/delivery-flow/references/config-schema.md`
for pipeline integration).

| Template | Stage | Authored at | Purpose |
|---|---|---|---|
| `constraints-refine.yml` | Stage 2 Refine | `.delivery/artifacts/02-refine/po/constraints.yml` | Domain-scoped constraints authored by the PO: domain nouns, problem invariants. |
| `constraints-architect.yml` | Stage 4 Architect | `.delivery/artifacts/04-architect/solution/constraints.yml` | Decomposition-scoped constraints authored by the Solution Architect: bounded contexts, volatility classes, forbidden implementation vocabulary, Löwy citation when volatility decomposition is used. |

Copy the appropriate template verbatim into the canonical stage path, then
fill in the `<fill in: ...>` markers. Preserve field order for glance-ability
at human checkpoints. The DoD validator enforces required fields, forbidden
vocabulary, mandatory artifacts, and citation rules deterministically per
ADR-001 and ADR-003.
