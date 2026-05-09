# Output Contract: test-cases

The `test-cases` task type produces a test case set. Sub-agent output must match this template:

```
## Test Cases: [FEATURE/SCENARIO NAME]

### Test Case Table
| ID | Title | Type | Priority | Preconditions | Steps | Expected Result |
|---|---|---|---|---|---|---|

### Boundary Values
| Input | Lower Bound | Upper Bound | On-Boundary | Off-Boundary |
|---|---|---|---|---|

### Negative Test Cases
| ID | Title | Invalid Input | Expected Error |
|---|---|---|---|

### Coverage Notes
[Which equivalence classes are covered, what remains untested, known gaps]
```
