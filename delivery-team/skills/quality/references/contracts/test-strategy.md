# Output Contract: test-strategy

The `test-strategy` task type produces a test strategy document. Sub-agent output must match this template:

```
## Test Strategy: [FEATURE/SYSTEM NAME]

### Scope
[What is being tested and what is explicitly out of scope]

### Test Types
| Type | Purpose | Level | Tools/Approach |
|---|---|---|---|

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

### Entry Criteria
- [List of conditions that must be met before testing begins]

### Exit Criteria
- [List of conditions that must be met before testing is complete]

### Environment Requirements
- [Test environments needed, data requirements, access]

### Approach
[Narrative description of the testing approach: what gets tested first, how risk drives prioritization, shift-left opportunities]
```
