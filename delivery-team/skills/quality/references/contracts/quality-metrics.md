# Output Contract: quality-metrics

The `quality-metrics` task type produces a quality metrics dashboard or analysis. Sub-agent output must match this template:

```
## Quality Metrics Dashboard: [PROJECT/RELEASE NAME]

### Summary Metrics
| Metric | Current | Target | Trend |
|---|---|---|---|

### Defect Analysis
| Category | Count | Severity Distribution | Escape Rate |
|---|---|---|---|

### Coverage
| Coverage Type | Percentage | Gap Areas |
|---|---|---|

### Recommendations
- [Actionable improvements based on the data]
```

Note: pedagogical reference content (defect density formulas, coverage definitions, escape rate, MTTR/MTTF, cost of quality) lives in `../quality-metrics.md`. Load both when generating a metrics dashboard.
