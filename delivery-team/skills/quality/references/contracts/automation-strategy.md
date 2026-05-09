# Output Contract: automation-strategy

The `automation-strategy` task type produces an automation strategy document. Sub-agent output must match this template:

```
## Automation Strategy: [PROJECT/SYSTEM NAME]

### Automation Scope
| Level | What to Automate | What to Keep Manual | Rationale |
|---|---|---|---|

### Framework Recommendation
| Criterion | Recommendation | Alternatives |
|---|---|---|

### CI/CD Integration
[When tests run, pipeline stages, parallelization, gating]

### Maintenance Plan
[How flaky tests are handled, review cadence, ownership]

### ROI Estimate
[Which tests save the most manual effort, break-even timeline]
```

Note: pedagogical reference content (automation pyramid, framework selection, flaky-test mitigation, mocking strategies) lives in `../test-automation.md`. Load both when generating an automation strategy.
