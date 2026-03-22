# Quality Metrics Reference

## Defect Density

### Formula

```
Defect Density = Number of Confirmed Defects / Size of the Component
```

Size can be measured in lines of code (KLOC), function points, story points, or number of features.

### Benchmarks

| Quality Level | Defect Density (per KLOC) |
|---|---|
| Industry average | 15-50 defects per KLOC (pre-release) |
| Good | 1-5 defects per KLOC (post-release) |
| High quality | < 1 defect per KLOC (post-release) |
| Safety-critical | < 0.1 defects per KLOC (post-release) |

### Trend Analysis

- Track defect density per sprint/release to identify trends
- Rising density in a component signals increasing technical debt or insufficient testing
- Compare density across components to identify risk areas
- Normalize by component size to avoid penalizing larger modules unfairly

---

## Test Coverage Metrics

### Code Coverage Types

| Type | What It Measures | Target | Limitations |
|---|---|---|---|
| **Line coverage** | Percentage of code lines executed | > 80% | Does not ensure correctness, misses logic in expressions |
| **Branch coverage** | Percentage of decision branches taken | > 75% | Better than line coverage, still misses value combinations |
| **Condition coverage** | Each boolean sub-expression evaluated true and false | > 70% | More thorough, harder to achieve and measure |
| **Path coverage** | All possible execution paths tested | Impractical for most code | Combinatorial explosion makes 100% infeasible |
| **MC/DC** | Modified Condition/Decision Coverage | Required for safety-critical | Each condition independently affects the decision |

### Requirement Coverage

```
Requirement Coverage = Requirements with at least one test / Total requirements * 100
```

- Every acceptance criterion should have at least one test case
- Track in a traceability matrix (requirement ID to test case ID)
- Coverage gaps indicate untested requirements, not necessarily missing code

### Risk Coverage

```
Risk Coverage = High-risk areas with adequate test coverage / Total high-risk areas * 100
```

- Define "adequate" based on the risk level (critical areas need more techniques)
- Use the risk matrix from the test strategy to identify high-risk areas
- Risk coverage is more actionable than code coverage for business decisions

---

## Defect Escape Rate

### Formula

```
Defect Escape Rate = Defects Found in Production / Total Defects Found * 100
```

### What It Indicates

| Escape Rate | Interpretation |
|---|---|
| < 5% | Strong testing process, most defects caught before release |
| 5-15% | Acceptable for most applications, room for improvement |
| 15-30% | Testing gaps exist, review test strategy and coverage |
| > 30% | Significant quality process issues, immediate action needed |

### How to Improve

1. Analyze escaped defects for root cause patterns (which test phase should have caught them)
2. Add test cases that would have caught each escaped defect
3. Review test design techniques -- are you using equivalence partitioning, BVA, and negative testing?
4. Implement shift-left practices to catch defects earlier
5. Add monitoring and alerting for production to detect escapes faster

---

## MTTR / MTTF / MTBF

### Definitions

| Metric | Full Name | Formula | Use |
|---|---|---|---|
| **MTTR** | Mean Time to Repair | Total repair time / Number of failures | How quickly defects are fixed |
| **MTTF** | Mean Time to Failure | Total operational time / Number of failures | Reliability of non-repairable components |
| **MTBF** | Mean Time Between Failures | Total time / Number of failures | Reliability of repairable systems |

### Calculation Example

System operates for 720 hours in a month. It fails 3 times. Repairs take 2, 4, and 6 hours.

- **MTTR** = (2 + 4 + 6) / 3 = 4 hours
- **MTBF** = 720 / 3 = 240 hours
- **Availability** = MTBF / (MTBF + MTTR) = 240 / 244 = 98.4%

### Use Cases

- **MTTR** is the primary metric for incident response effectiveness
- **MTBF** indicates system stability and reliability trends
- Tracking MTTR by severity shows whether critical bugs get prioritized appropriately
- Comparing MTBF across releases shows whether quality is improving or degrading

---

## Test Execution Metrics

### Key Metrics

| Metric | Formula | Target |
|---|---|---|
| **Pass rate** | Passed tests / Total executed * 100 | > 95% per cycle |
| **Execution rate** | Tests executed / Tests planned * 100 | 100% before release |
| **Blocked rate** | Blocked tests / Total planned * 100 | < 5% |
| **Execution time** | Total time to run all tests | Trending down or stable |
| **Defects found per test hour** | Defects found / Test execution hours | Trending down over cycles |

### What the Numbers Tell You

- **Pass rate dropping**: New defects introduced, unstable build, or environment issues
- **High blocked rate**: Environment problems, dependency issues, or insufficient test data
- **Execution time increasing**: Test suite growing without optimization, flaky retries
- **Defects per hour decreasing**: Either quality is improving or tests are not finding bugs (investigate which)

---

## Quality Gates

### Definition

A quality gate is a checkpoint where predefined criteria must be met before the project can proceed to the next phase.

### Common Quality Gates

| Gate | Phase Transition | Typical Criteria |
|---|---|---|
| **Code quality gate** | Development to QA | Static analysis passes, unit tests > 80% coverage, no critical SonarQube issues |
| **Test readiness gate** | Before test execution | Test environment ready, test data loaded, entry criteria met |
| **Release candidate gate** | QA to staging | All test cases executed, pass rate > 95%, no open critical/high defects |
| **Production release gate** | Staging to production | Smoke tests pass, performance benchmarks met, stakeholder sign-off |
| **Post-release gate** | After production deploy | No critical production incidents in 24h, error rate below threshold |

### Pass/Fail Criteria

Each gate must have:
1. **Measurable criteria**: Specific numbers, not subjective judgments
2. **Automated checks where possible**: Pipeline enforces the gate, not humans remembering
3. **Escalation path**: What happens when the gate fails (who decides to proceed anyway, with what risk acceptance)
4. **Documentation**: Record the gate result and any exceptions granted

---

## Quality Dashboard Design

### What to Show

| Section | Metrics | Visualization |
|---|---|---|
| Overall health | Pass rate, defect trend, coverage | Traffic light status, trend line |
| Current sprint | Test execution progress, blockers | Progress bar, blocker list |
| Defect status | Open by severity, age, component | Bar chart, aging report |
| Coverage | Code coverage, requirement coverage | Coverage map, gap list |
| Automation | Automated vs manual ratio, flake rate | Pie chart, trend line |
| Trends | Quality metrics over last 6 sprints | Line charts |

### Audience and Cadence

| Audience | Update Frequency | Focus |
|---|---|---|
| Development team | Real-time (CI dashboard) | Test results, failures, flaky tests |
| QA team | Daily | Execution progress, blockers, defect trends |
| Engineering leadership | Weekly | Quality trends, risk areas, release readiness |
| Stakeholders | Per release | Go/no-go summary, risk assessment |

### Dashboard Anti-Patterns

- Showing too many metrics (information overload, nothing stands out)
- Metrics without targets (numbers without context are not actionable)
- Vanity metrics (high pass rate on trivial tests while critical areas are untested)
- Stale data (dashboard updated weekly when decisions are made daily)
- No drill-down capability (summary without the ability to investigate)

---

## Leading vs. Lagging Quality Indicators

### Leading Indicators (Predict Future Quality)

| Indicator | What It Predicts |
|---|---|
| Code review coverage | Lower defect introduction rate |
| Static analysis trend | Code health trajectory |
| Unit test coverage trend | Future defect density |
| Requirements clarity score | Defect rate in upcoming development |
| Technical debt ratio | Future maintenance burden and defect rate |
| Build stability | Testing reliability and team velocity |

### Lagging Indicators (Measure Past Quality)

| Indicator | What It Measures |
|---|---|
| Defect density | Quality of delivered code |
| Defect escape rate | Effectiveness of testing process |
| Customer-reported defects | Quality as perceived by users |
| MTTR | Incident response effectiveness |
| Production incident count | System reliability |
| Cost of quality | Total investment in quality activities |

A healthy quality program tracks both. Leading indicators enable proactive improvement. Lagging indicators validate whether improvements are working.

---

## Cost of Quality

### Categories

| Category | Definition | Examples |
|---|---|---|
| **Prevention** | Cost to prevent defects | Training, code reviews, test planning, static analysis tools, process improvement |
| **Appraisal** | Cost to detect defects | Test execution, inspections, audits, monitoring, test environment maintenance |
| **Internal failure** | Cost of defects found before release | Rework, retesting, defect triage, delayed releases |
| **External failure** | Cost of defects found after release | Customer support, patches, reputation damage, SLA penalties, incident response |

### Cost Ratios

The cost of fixing a defect increases dramatically as it moves through the lifecycle:

| Phase Found | Relative Cost |
|---|---|
| Requirements | 1x |
| Design | 3-6x |
| Development | 10x |
| Testing | 15-40x |
| Production | 30-100x |

### Using Cost of Quality

- Track spending across all four categories over time
- A mature organization spends more on prevention and less on failure
- If external failure costs are high, invest more in prevention and appraisal
- Use cost of quality data to justify investment in testing tools, training, and process improvement
- Target ratio: 50-60% prevention, 20-30% appraisal, 10-20% failure (internal + external)
