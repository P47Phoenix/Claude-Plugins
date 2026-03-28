# Gate Failure Patterns

**Entries**: 4 | **Last updated**: 2026-03-27

## Common Failure Patterns

- **Incomplete FR traceability**: Design and Plan stages fail when artifacts don't map to ALL PRD FRs. Validators check FR-by-FR. Solution: verify full traceability before submitting. (validated: 1, last: run-2026-03-27-c8f2)
- **Missing capacity declaration**: Plan stage fails without explicit velocity baseline, 80% ceiling, and per-sprint commitment. SM always checks this. (validated: 1, last: run-2026-03-27-c8f2)
- **Stale derived artifacts**: Dev stage fails when generated files (schema.json, docs) are not regenerated after source changes. Architect always checks this. (validated: 1, last: run-2026-03-27-c8f2)
- **Deferred P0 items**: UAT fails when P0 requirements (dogfooding, docs) are treated as follow-ups. PO always checks this. Execute P0s before submitting. (validated: 1, last: run-2026-03-27-c8f2)
