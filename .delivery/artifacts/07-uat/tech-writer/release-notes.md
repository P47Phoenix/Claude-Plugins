# Release Notes — paradigm-as-skill extraction (run d5e2)

**Role:** Bilbo (Technical Writer) | 2026-04-10

## What Changed

The `delivery-team:architect` skill's decomposition paradigms (Volatility-Based Decomposition and Domain-Driven Design) have been extracted from inline reference files into standalone sub-skills under `paradigms/`. Each paradigm is now a self-contained skill directory with its own `SKILL.md` and `references/` folder, loaded on demand via a new Paradigm Router in the architect skill.

## New Capability

- **Paradigm Router** in architect SKILL.md dispatches to `paradigms/{paradigm_id}/SKILL.md` based on the selected decomposition strategy, loading only the relevant paradigm context.
- **82-90% context reduction**: volatility paradigm sub-skill is 66 lines vs 667-line monolithic architect skill. Only paradigm-relevant content enters the context window.
- **Redirect stubs** at original reference paths preserve backwards compatibility for any existing references or bookmarks.
- **Design Sprint reference** added to delivery-flow for design-stage support.

## Backwards Compatibility

Default routing falls back to the monolithic architect skill. Existing pipelines that do not use paradigm routing are unaffected. Redirect stubs at original paths point to new locations.

## Known Limitations

- **Functional decomposition** and **event-storming** paradigms are not yet extracted -- tracked as future work in the transformation roadmap.
- Paradigm sub-skills are intentionally not registered in `marketplace.json` per ADR-001 (internal sub-skills, not marketplace-visible).

## Fellowship Credits

- Gandalf -- PO / FR validation and final verdict
- Celebrimbor -- Architect / paradigm extraction and router design
- Legolas -- QA / 15-TC verification suite
- Sam -- DevOps / release plan
- Bilbo -- Technical Writer / these notes
- Aragorn -- Delivery Lead / retrospective

## References

- BACKLOG-005: paradigm-as-skill extraction (this work)
- BACKLOG-006: transformation-planning orchestrator dispatch (related)
