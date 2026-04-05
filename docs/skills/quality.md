# Quality

**Invocation**: `delivery-team:quality`

QA Engineer agent for test planning, test case design, automation strategy, and quality metrics.

## How to Trigger

- "test cases", "test plan", "test strategy", "regression"
- "test data", "exploratory testing", "quality metrics"
- "automation strategy", "QA", "test coverage"

## Task Types

| Type | Signal Keywords | What It Does |
|------|----------------|-------------|
| **test-strategy** | "test strategy", "testing approach" | Define overall testing approach for a system |
| **test-cases** | "test cases", "edge cases", "smoke test" | Design specific test scenarios |
| **test-plan** | "test plan", "regression plan" | Comprehensive test planning |
| **test-data** | "test data", "test fixtures" | Design test data and fixtures |
| **regression-plan** | "regression", "regression suite" | Plan regression testing |
| **exploratory-testing** | "exploratory testing", "charter" | Session-based exploratory testing plans |
| **quality-metrics** | "quality metrics", "defect density" | Quality measurement and dashboards |
| **automation-strategy** | "automate tests", "CI testing" | Test automation planning |

## Example Usage

```
User: "Create test cases for the user authentication feature"

Task Type: test-cases | References: test-case-patterns.md

Output: Structured test cases covering happy path, edge cases,
        boundary conditions, and error scenarios
```
