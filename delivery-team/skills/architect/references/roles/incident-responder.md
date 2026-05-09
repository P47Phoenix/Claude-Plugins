# Incident Responder — Role Manifest

The Incident Responder designs incident response plans, severity classifications, communication templates, containment strategies, and post-incident review processes. Routes on IR-specific signals.

## Reference Files Loaded

- `references/incident-response.md` — IR lifecycle, severity classification, communication templates, chain of custody, containment strategies, tabletop exercises
- `references/security-patterns.md` — paired for incident-ready architecture work

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "incident response plan", "severity classification", "IR lifecycle", "tabletop exercise", "post-incident review" | **incident-response-plan** | incident-response.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **incident-response-plan** | Create an incident response plan with severity classification, communication templates, containment strategies, and post-incident review process |

## Recommended Model

- `sonnet` for `incident-response-plan` (template / classification)

## Cross-Role Combinations

- **+ Security Architect** — incident-ready architecture: security-patterns.md + incident-response.md + compliance-frameworks.md
