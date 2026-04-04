# Development Stage Lessons

**Entries**: 3 | **Last updated**: 2026-04-03

- Derived artifacts (config-schema.json from config-schema.md, generated docs from source) MUST be regenerated after modifying their source. Architect validator caught stale schema.json. Add "regenerate derived artifacts" to dev checklist. (validated: 1, last: run-2026-03-27-c8f2)
- When modifying config schema, always run `python delivery-team/scripts/generate-schema.py` after editing config-schema.md. (validated: 1, last: run-2026-03-27-c8f2)
- Known scope limitations need explicit user-facing disclaimers in output artifacts. If a capability is scoped to one data source, the output must state the limitation. PRD team knowing about it is not sufficient — the user must see it. (validated: 1, last: run-2026-04-02-k3r9)
