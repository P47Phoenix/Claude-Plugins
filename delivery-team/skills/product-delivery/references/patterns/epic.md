# Pattern: Epic Decomposition

**Format:** Map one epic to a complete set of stories with ordering rationale.

```
## Epic: [Epic Name]

**Epic Goal:** [What problem does this solve for users? What business outcome?]
**Success Metric:** [How will we know this epic succeeded?]
**Out of Scope:** [Explicit exclusions to prevent scope creep]

### Story Map

| # | Story Title | Value | Effort | Priority | Dependencies |
|---|-------------|-------|--------|----------|--------------|
| 1 | [Title]     | High  | M      | P1       | None         |
| 2 | [Title]     | High  | S      | P1       | Story 1      |
| 3 | [Title]     | Med   | L      | P2       | Story 1      |

### MVP Slice
Stories required for a shippable minimum: [#1, #2]
Rationale: [Why these form a complete, valuable increment]

### Full Story Definitions
[Expand each story using the User Story pattern format]
```
