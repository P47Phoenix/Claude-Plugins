# Test Strategy Reference

This reference provides foundational knowledge for building test strategies. The sub-agent should apply these concepts when producing test strategy documents, test plans, regression plans, and exploratory testing charters.

---

## Test Pyramid

The test pyramid defines the ideal distribution of tests across levels. More tests at the base, fewer at the top.

| Level | Proportion | Speed | Cost | Confidence in Isolation | Confidence in Integration |
|---|---|---|---|---|---|
| Unit | 60-70% | Fastest | Lowest | Highest | Lowest |
| Integration | 20-30% | Moderate | Moderate | Moderate | Moderate |
| End-to-End | 5-10% | Slowest | Highest | Lowest | Highest |

### When to Adjust the Pyramid

- **CRUD-heavy applications**: Shift toward more integration tests (database interactions matter more than isolated logic)
- **Complex business logic**: Shift toward more unit tests (rules engines, calculations, state machines)
- **UI-intensive applications**: Add a thin layer of visual regression tests above E2E
- **Microservices**: Add contract tests between integration and E2E layers
- **Legacy systems without unit tests**: Start with E2E for safety net, then backfill unit tests during refactoring

### Anti-Pattern: The Ice Cream Cone

When most tests are E2E/manual and few are unit tests, the pyramid is inverted. This leads to slow feedback, flaky pipelines, and high maintenance cost. Correct by investing in lower-level tests first.

---

## Risk-Based Testing

Not all features carry equal risk. Test effort should be proportional to risk.

### Risk Matrix

| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Likelihood** | Medium priority | High priority | Critical priority |
| **Medium Likelihood** | Low priority | Medium priority | High priority |
| **Low Likelihood** | Minimal testing | Low priority | Medium priority |

### Risk Factors

- **Business impact**: Revenue loss, reputation damage, regulatory penalty, user safety
- **Technical complexity**: New technology, complex algorithms, third-party dependencies
- **Change frequency**: Code that changes often is more likely to break
- **Historical defects**: Areas with past defects tend to have more defects
- **Integration points**: Boundaries between systems are high-risk areas

### Test Effort Allocation

- **Critical risk**: Full coverage -- unit, integration, E2E, performance, security. Automate everything feasible.
- **High risk**: Strong unit and integration coverage. Key E2E scenarios. Automate regression.
- **Medium risk**: Targeted unit tests on complex logic. Integration tests on key paths. Manual exploratory.
- **Low risk**: Basic happy-path testing. Smoke tests only.

---

## Shift-Left Testing

Testing earlier in the development lifecycle is cheaper and faster than finding defects later.

### Shift-Left Activities by Phase

| Phase | Testing Activity |
|---|---|
| Requirements | Review acceptance criteria for testability. Identify ambiguities. |
| Design | Review architecture for testability. Identify integration risks. |
| Development | Unit tests written with code (TDD or test-alongside). Static analysis. |
| Code Review | Verify test coverage. Check for common defect patterns. |
| Integration | Automated integration tests run on every merge. Contract tests for APIs. |
| Pre-Release | E2E tests, performance tests, security scans. Exploratory testing sessions. |

### Prevention vs Detection

- **Prevention**: Requirements reviews, design reviews, coding standards, static analysis, TDD
- **Detection**: Testing, monitoring, user reports

Prevention is 10-100x cheaper than detection in production. Prioritize prevention activities when building a test strategy.

---

## Test Types Taxonomy

| Type | Purpose | When to Use |
|---|---|---|
| **Functional** | Verify behavior matches requirements | Every feature |
| **Non-Functional** | Verify quality attributes (performance, security, usability) | Per risk assessment |
| **Regression** | Verify existing functionality is not broken by changes | Every release |
| **Smoke** | Quick verification that critical paths work after deployment | Every deployment |
| **Sanity** | Focused check on specific functionality after a targeted fix | After bug fixes |
| **Exploratory** | Unscripted investigation to find defects through learning | New features, risky areas |
| **Acceptance** | Verify the system meets business requirements | Before release sign-off |
| **Integration** | Verify components work together correctly | Multi-component features |
| **Performance** | Verify response times, throughput, resource usage under load | Performance-sensitive features |
| **Security** | Verify the system resists unauthorized access and attacks | Authentication, authorization, data handling |

---

## Entry and Exit Criteria Templates

### Entry Criteria (Start Testing When)

- Code is deployed to the test environment and verified accessible
- Build is green -- no compilation or deployment errors
- Unit tests pass with agreed coverage threshold
- Test data is loaded and verified
- Test environment matches production configuration (or deviations are documented)
- Required test accounts and access are provisioned
- Acceptance criteria are reviewed and unambiguous

### Exit Criteria (Stop Testing When)

- All planned test cases are executed
- All critical and high-severity defects are resolved and verified
- Test coverage meets the agreed threshold (specify: 80% code coverage, 100% acceptance criteria coverage, etc.)
- No open blockers or critical defects
- Regression suite passes
- Performance benchmarks are met
- Stakeholder sign-off is obtained

---

## Test Environment Strategy

### Environment Isolation

- Each test level should have its own environment when feasible (dev, QA, staging, production)
- Shared environments require coordination to avoid test interference
- Containerized environments (Docker, Kubernetes) enable on-demand isolated environments

### Data Management

- Test data should be independent and reproducible
- Use seed scripts or data factories to create known starting states
- Clean up test data after test runs to prevent pollution
- Never use production data in test environments without anonymization

### Environment Parity

- Staging should mirror production as closely as possible (same OS, same versions, same configuration)
- Document all known deviations between test and production environments
- Infrastructure-as-code ensures environment consistency

---

## Test Planning Process

When building a test plan, address these elements in order:

1. **Scope**: What features, components, or integrations are being tested. What is explicitly excluded and why.
2. **Approach**: Which test types apply. What is automated vs manual. How risk drives prioritization.
3. **Schedule**: When each testing phase starts and ends. Dependencies on development milestones.
4. **Resources**: Who is testing. What tools are needed. What environments are required.
5. **Risks**: What could go wrong with the testing itself (environment instability, data dependencies, skill gaps). Mitigations for each.
6. **Communication**: How defects are reported. Status reporting cadence. Escalation path for blockers.

---

## When to Stop Testing

Testing can continue indefinitely. These criteria help decide when to stop:

- **Coverage thresholds met**: Code coverage, requirement coverage, and risk coverage all meet targets
- **Defect discovery rate declining**: The rate of new defects found per test hour is decreasing (diminishing returns)
- **Risk appetite satisfied**: Remaining untested areas are low-risk and stakeholders accept the residual risk
- **Time and budget constraints**: Testing must stop by a deadline -- document what was not tested and the associated risk
- **Confidence level**: The team has sufficient confidence that the software meets its requirements

Never stop testing solely because of a deadline. If testing is cut short, the risk of untested areas must be documented and communicated to stakeholders.

---

## Godot-Specific Test Strategy

For GAME_DEV projects using Godot, layer tests with GdUnit4:

| Layer | Tool | What It Catches | Run When |
|-------|------|----------------|----------|
| Static analysis | Editor type warnings (strict mode) | Type inference errors, missing methods | Every save |
| Lint | gdlint | Style violations, naming conventions | Pre-commit |
| Unit tests | GdUnit4 | Logic bugs, calculations, state management | After each story |
| Signal tests | GdUnit4 signal assertions | Orphaned signals, wrong parameters | After wiring changes |
| Integration tests | GdUnit4 scene runner | Visual bugs, input handling, AI behavior | After each sprint |
| Headless validation | godot --headless | Parse errors, autoload failures | After every write |
| CI/CD | GdUnit4 GitHub Action | Regressions across all of the above | Every push |

### Test naming convention
- Test files: `test_<source_file_name>.gd`
- Test classes: `TestClassName extends GdUnitTestSuite`
- Test methods: `test_<behavior_being_tested>()`
- Directory: `res://tests/` mirroring `res://src/` structure
