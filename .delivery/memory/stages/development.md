# Development Stage Lessons

**Entries**: 6 | **Last updated**: 2026-04-08

- Derived artifacts (config-schema.json from config-schema.md, generated docs from source) MUST be regenerated after modifying their source. Architect validator caught stale schema.json. Add "regenerate derived artifacts" to dev checklist. (validated: 1, last: run-2026-03-27-c8f2)
- When modifying config schema, always run `python delivery-team/scripts/generate-schema.py` after editing config-schema.md. (validated: 1, last: run-2026-03-27-c8f2)
- Known scope limitations need explicit user-facing disclaimers in output artifacts. If a capability is scoped to one data source, the output must state the limitation. PRD team knowing about it is not sufficient — the user must see it. (validated: 1, last: run-2026-04-02-k3r9)
- Developer should proactively diff source vs installed plugin files BEFORE DoD submission, not rely on the validator to catch sync gaps. The validator is a safety net, not the primary mechanism. Two consecutive runs (j8f2, w7m3) required correction rounds for the same class of issue. Add "run diff, sync if diverged" as an explicit pre-DoD step. (validated: 2, last: run-2026-04-04-w7m3)
- QA sweep scripts that invoke validators must use correct argument order. Stage 6 reported a fixture-data mismatch that was actually `check_dod_constraints.py` invoked as `<artifact> <constraints>` instead of `<constraints> <artifact>`. Document argument order in validator help text. (validated: 1, last: run-2026-04-08-a1f3)
- Board dogfood simulation (reviewers + judge) is a valid proof-of-design even without real orchestrator wiring — produces authoritative shape of artifacts the design calls for. Use when code wiring is out of scope. (validated: 1, last: run-2026-04-08-b2c7)
