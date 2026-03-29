# Gate Failure Patterns

**Entries**: 7 | **Last updated**: 2026-03-29

## Common Failure Patterns

- **Incomplete FR traceability**: Design and Plan stages fail when artifacts don't map to ALL PRD FRs. Validators check FR-by-FR. Solution: verify full traceability before submitting. (validated: 1, last: run-2026-03-27-c8f2)
- **Missing capacity declaration**: Plan stage fails without explicit velocity baseline, 80% ceiling, and per-sprint commitment. SM always checks this. (validated: 1, last: run-2026-03-27-c8f2)
- **Stale derived artifacts**: Dev stage fails when generated files (schema.json, docs) are not regenerated after source changes. Architect always checks this. (validated: 1, last: run-2026-03-27-c8f2)
- **Deferred P0 items**: UAT fails when P0 requirements (dogfooding, docs) are treated as follow-ups. PO always checks this. Execute P0s before submitting. (validated: 1, last: run-2026-03-27-c8f2)
- **Phantom file references**: Idea briefs and architecture docs reference files that don't exist (e.g., database.py). Architect validator catches these on first DoD round. Always verify file paths with Glob before citing them. (validated: 1, last: run-2026-03-28-k4m9)
- **Wrong filenames in scripts**: Scripts referencing wrong file names (routing.json vs stage-routing.json) are caught by QA structural verification in UAT. Reconcile filenames across scripts and rule files. (validated: 1, last: run-2026-03-28-k4m9)
- **Design positional references**: UX designs referencing wrong wizard question positions or file formats (state.json vs state.md) are caught by Architect validator. Cross-reference all filenames and positions against source of truth. (validated: 1, last: run-2026-03-28-k4m9)
