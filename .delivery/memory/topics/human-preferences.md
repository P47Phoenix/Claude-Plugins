# Human Preferences

**Entries**: 9 | **Last updated**: 2026-03-25

## Process Enforcement

- ALL implementation must go through delivery-flow pipeline — never spawn developer/godot agents directly for story work. (validated: 3)
- Only bypass pipeline for: quick one-off fixes explicitly approved by user.
- When user says "keep going" or "continue until done", route ALL work through delivery-flow stages, not direct agent calls.
- Plans are PROMPTS to the team — not implementation details the orchestrator executes directly. (validated: 2)
- Route work through the PO (Gandalf) first. Log issues, then invoke delivery-flow. (validated: 2)

## Pipeline Stages

- Light stages MUST execute. Light means reduced depth, NOT skipped. Never conflate light with skip. (validated: 1)
- Every stage in the routing matrix that is not "skip" must produce an artifact before advancing. (validated: 1)

## Dogfooding

- Team must validate changes by actually USING them before shipping — not just code review. (validated: 1)
- After hook changes: trigger the hook and verify it fires correctly.
- After config changes: re-run the wizard and verify new values work.
- After skill changes: invoke the skill with a representative task.
- After pipeline changes: run a mini pipeline and verify all stages execute.
- "A cook who does not taste his own soup serves poison with confidence."

## Config Preferences

- Config files should be pure YAML (.yml), not markdown with YAML frontmatter. (validated: 1)
- User values correctness over convenience — prefer the cleaner option even if it has more blast radius.

## Plugin Development

- Always use plugin-dev skills (hook-development, skill-development, etc.) when creating or modifying plugin components in this repo. (validated: 1)

## Self-Improvement

- Team members should open GitHub issues on this repo when they spot something in the plugin that could be fixed or improved. (validated: 1)
- During reviews, dogfooding, QA validation, or any pipeline work — if you see a gap, inconsistency, or improvement opportunity, log it as an issue using the appropriate template (bug_report, feature_request, or defect_pattern).
- "The team that files its own bugs ships better software."

## Team Autonomy

- Team makes prioritization and execution decisions autonomously when technical basis is clear. (validated: 1)
- Never bring problems without solutions + evidence. Always present recommended solution with rationale.
- Don't escalate what the team can decide.

## Documentation

- Keep ALL documentation (CLAUDE.md, README.md, delivery-team/README.md, marketplace.json) up to date when planning future work. (validated: 1)
- After any pipeline run that changes features, hooks, skills, or config: update affected doc files as part of the Dev or UAT stage — not as a separate follow-up.
- "Stale docs are worse than no docs — they teach the wrong thing with authority."
