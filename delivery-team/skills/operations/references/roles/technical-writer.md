# Technical Writer

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Technical Writer** | api-documentation.md, user-guides.md, runbook-templates.md, documentation-standards.md |

## Detection Keywords

API docs, documentation, user guide, runbook, release notes, tutorial, changelog, style guide, Diataxis, OpenAPI, Swagger, knowledge base, getting started, troubleshooting, how-to, reference docs, documentation plan, content type

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "API docs", "API documentation", "OpenAPI", "Swagger", "endpoint documentation" | **api-docs** | api-documentation.md |
| "user guide", "getting started", "how-to guide", "tutorial", "walkthrough" | **user-guide** | user-guides.md |
| "runbook", "operational procedure", "troubleshooting guide", "recovery procedure" | **runbook** | runbook-templates.md |
| "release notes", "changelog", "what's new" | **release-notes** | documentation-standards.md, release-planning.md |
| "knowledge base", "FAQ", "internal docs", "wiki" | **knowledge-base** | user-guides.md, documentation-standards.md |
| "tutorial", "learning path", "onboarding docs" | **tutorial** | user-guides.md |
| "documentation plan", "docs strategy", "content audit", "information architecture" | **documentation-plan** | documentation-standards.md, user-guides.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **api-docs** | Write API documentation: endpoint specifications, request/response examples, error catalog, auth guide |
| **user-guide** | Write user-facing documentation: getting started guides, how-to articles, tutorials with progressive complexity |
| **runbook** | Write operational runbooks: step-by-step procedures, troubleshooting trees, escalation matrices, recovery steps |
| **release-notes** | Write release notes: feature summaries, breaking changes, migration instructions, known issues |
| **knowledge-base** | Organize and write knowledge base content: FAQs, internal documentation, searchable reference material |
| **tutorial** | Write learning-oriented tutorials: step-by-step instruction, progressive complexity, working examples |
| **documentation-plan** | Create documentation strategy: content audit, information architecture, style guide, review process |

## Guardrails

- **Documentation matches the product** -- docs must reflect the current state of the system, not aspirational features
- **Audience is stated** -- every document declares its intended audience and prerequisite knowledge
- **Code examples must be tested** -- no untested code snippets in documentation; examples must actually work
- **Style guide compliance** -- all content follows the project's style guide for voice, tone, and formatting
- **No orphan pages** -- every document must be reachable from navigation; no floating, unlinked content
- **Maintenance plan exists** -- every document has an owner and a review cadence
- **Screenshots are a last resort** -- prefer text and code over screenshots; screenshots become stale quickly
