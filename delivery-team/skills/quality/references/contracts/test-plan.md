# Output Contract: test-plan

The `test-plan` task type produces a release/feature test plan. Sub-agent output must match this template:

```
## Test Plan: [RELEASE/FEATURE NAME]

### Objective
[What this test plan validates]

### Scope
[In scope / out of scope]

### Strategy Summary
[Test types, levels, approach -- reference the test strategy]

### Test Schedule
| Phase | Activities | Duration | Dependencies |
|---|---|---|---|

### Test Cases
[Reference or embed the test case table]

### Entry / Exit Criteria
[Clear, measurable criteria]

### Risks and Mitigations
| Risk | Mitigation |
|---|---|

### Sign-Off
[Who approves, what evidence is required]
```
