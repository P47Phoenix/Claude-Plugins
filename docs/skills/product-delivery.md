# Product Delivery

**Invocation**: `delivery-team:product-delivery`

Product delivery agent with three specialized roles that cover the full product lifecycle.

## Roles

### Product Owner

Handles business value, requirements, and stakeholder alignment.

**Task types**: User stories, epic decomposition, backlog management, PRDs, sprint planning, roadmap planning, stakeholder communications, Definition of Done/Ready, prioritization (RICE, MoSCoW, WSJF, Kano)

### Scrum Master

Facilitates agile ceremonies and drives process improvement.

**Task types**: Retrospectives (5 formats), process improvement, velocity analysis, ceremony facilitation, impediment removal, team health assessments, agile maturity assessments

### Data Analyst

Defines metrics, designs experiments, and builds analytics foundations.

**Task types**: Analytics requirements, metrics definition (HEART, AARRR, OKR, North Star), dashboard design, A/B testing, data quality assessment, data exploration, reporting

## How to Trigger

The skill auto-detects the relevant role from your request:

- **Product Owner**: "write user stories", "prioritize backlog", "create PRD", "sprint goal"
- **Scrum Master**: "retrospective", "velocity", "ceremony", "impediment", "team health"
- **Data Analyst**: "analytics", "metrics", "KPI", "dashboard", "A/B test", "experiment"

## Key Task Types

### User Stories (Product Owner)

Produces stories in standard format with INVEST validation:

```
As a [specific user role]
I want [capability]
So that [business value]
```

Each story includes acceptance criteria in Given/When/Then format, a Definition of Ready checklist, and INVEST validation flags.

### Epic Decomposition (Product Owner)

Maps one epic to a complete set of stories with an MVP slice and ordering rationale.

### Retrospective (Scrum Master)

Supports 5 formats: Start/Stop/Continue, 4Ls, Sailboat, Mad/Sad/Glad, and Timeline. Every retrospective produces action items with assigned owners and due dates.

### A/B Test Plan (Data Analyst)

Produces experiment plans with hypothesis, primary metric, guardrail metrics, sample size calculation, success criteria, and risk mitigations.

## Example Usage

```
User: "Write user stories for a search feature"

Role: Product Owner | Task: Story Writing | References: user-stories.md

Output: Structured user stories with acceptance criteria,
        INVEST validation, and Definition of Ready checklists
```

## Cross-Role Tasks

Tasks that span roles load all relevant references into a single sub-agent:

| Scenario | Roles |
|----------|-------|
| Sprint planning with ceremony facilitation | PO + Scrum Master |
| Feature launch with success metrics | PO + Data Analyst |
| Retrospective with velocity analysis | Scrum Master + Data Analyst |
| OKR setting with metric definitions | PO + Data Analyst |
