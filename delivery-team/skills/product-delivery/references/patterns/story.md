# Pattern: User Story

**Format:** Always produce stories in standard form with INVEST validation.

```
## User Story: [Short Title]

**As a** [specific user role -- not "user"]
**I want** [a specific capability or action]
**So that** [the business value or outcome]

**Story Points:** [Fibonacci: 1, 2, 3, 5, 8, 13 -- or T-shirt if requested]
**Priority:** [Critical / High / Medium / Low]

### Acceptance Criteria

Given [initial context / state]
When [action or event occurs]
Then [expected observable outcome]

Given [alternative context]
When [...]
Then [...]

[Add as many Given/When/Then as needed to fully define behavior]

### Definition of Ready Checklist
- [ ] Story is understood by the team
- [ ] Acceptance criteria are clear and testable
- [ ] Dependencies identified
- [ ] Story is sized and fits within one sprint
- [ ] No unresolved blockers

### Notes / Constraints
[Technical constraints, UX notes, out-of-scope clarifications, edge cases not covered by ACs]
```

**INVEST validation** (apply silently, surface issues):
- **I**ndependent -- can be developed without depending on another story in the same sprint
- **N**egotiable -- implementation details are flexible
- **V**aluable -- delivers value to the user or business
- **E**stimable -- team can size it
- **S**mall -- fits in one sprint
- **T**estable -- acceptance criteria are verifiable

If any INVEST criterion fails, flag it: `[INVEST ISSUE: Not Small -- consider splitting at: ...]`
