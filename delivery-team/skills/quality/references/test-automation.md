# Test Automation Reference

This reference provides guidance on test automation strategy, framework selection, CI/CD integration, and maintenance practices. The sub-agent should apply these concepts when producing automation strategies and recommendations.

---

## Automation Pyramid

The automation pyramid mirrors the test pyramid but focuses on what to automate at each level.

### What to Automate at Each Level

| Level | What to Automate | What to Keep Manual |
|---|---|---|
| **Unit** | Business logic, calculations, data transformations, state machines, validation rules | Trivial getters/setters, framework-generated code |
| **API / Integration** | Contract validation, schema checks, status codes, error responses, data flow between services | One-off investigative API calls |
| **UI / E2E** | Critical user journeys (login, checkout, signup), smoke tests for deployments | Exploratory testing, visual design review, usability |

### Ideal Automation Ratios

| Level | Percentage of Automated Tests | Typical Execution Time |
|---|---|---|
| Unit | 70-80% | Seconds to low minutes |
| API / Integration | 15-20% | Minutes |
| UI / E2E | 5-10% | Minutes to tens of minutes |

### What Should Never Be Automated

- Exploratory testing (by definition, unscripted)
- Usability and accessibility evaluation (requires human judgment)
- Tests that change faster than they can be maintained
- One-time verification that will never be repeated

---

## Framework Selection Criteria

When recommending an automation framework, evaluate these criteria:

| Criterion | Questions to Answer |
|---|---|
| **Language alignment** | Does the framework use the same language as the application? Can the development team contribute? |
| **Community and support** | Is the framework actively maintained? Are there docs, tutorials, and community answers? |
| **Reporting** | Does it produce clear pass/fail reports? Can reports be published to CI/CD dashboards? |
| **CI/CD integration** | Does it run headlessly? Does it integrate with common CI tools (GitHub Actions, Jenkins, GitLab CI)? |
| **Parallel execution** | Can tests run in parallel to reduce execution time? |
| **Maintenance cost** | How much effort is required to update tests when the application changes? |
| **Learning curve** | How quickly can the team become productive with the framework? |

### Common Framework Choices by Stack

| Stack | Unit | API | UI/E2E |
|---|---|---|---|
| Python | pytest | pytest + requests/httpx | Playwright, Selenium |
| JavaScript/TypeScript | Jest, Vitest | Supertest, Axios | Playwright, Cypress |
| C# / .NET | xUnit, NUnit | RestSharp, HttpClient | Playwright, Selenium |
| Java | JUnit 5, TestNG | REST Assured | Selenium, Playwright |
| Go | testing (stdlib) | net/http/httptest | Rod, Chromedp |

---

## Page Object Model for UI Testing

The Page Object Model (POM) separates test logic from page structure. Each page or component is represented by a class that encapsulates its elements and interactions.

### Structure

```
tests/
  pages/
    login_page.py        # Element locators and page actions
    dashboard_page.py
  test_login.py          # Test cases that use page objects
  test_dashboard.py
```

### Principles

1. **One class per page or component.** The class exposes methods for user actions (login, search, submit_form), not raw element interactions.
2. **Locators are private.** Tests never reference CSS selectors or XPaths directly -- they call page object methods.
3. **No assertions in page objects.** Page objects return data; tests make assertions.
4. **Methods return page objects.** Navigation methods return the page object for the destination page, enabling fluent chaining.

### Benefits

- When the UI changes, only the page object needs updating -- not every test
- Tests read like user stories: `login_page.login(user, password)` instead of `driver.find_element(...).click()`
- Reusable across multiple test cases

---

## API Test Patterns

### Contract Testing

Verify that the API conforms to its contract (OpenAPI spec, JSON Schema, or agreed interface).

- Validate response schema against the specification
- Verify required fields are present
- Check data types match the spec
- Test that new versions do not break existing consumers (backward compatibility)

### Schema Validation

```
For each endpoint:
1. Send a valid request
2. Verify response status code
3. Validate response body against JSON Schema
4. Verify required headers are present
5. Check content-type matches expected format
```

### Status Code Verification

| Scenario | Expected Status | Verify Also |
|---|---|---|
| Successful create | 201 Created | Location header, response body |
| Successful read | 200 OK | Response body matches request |
| Not found | 404 Not Found | Error message is descriptive |
| Validation error | 400 Bad Request | Error details identify the field |
| Unauthorized | 401 Unauthorized | No sensitive data leaked |
| Forbidden | 403 Forbidden | Error message does not reveal resource existence |
| Server error | 500 Internal Server Error | Error is logged, no stack trace in response |

### API Test Organization

- Group tests by resource (users, orders, products)
- Within each resource, test CRUD operations in order: Create, Read, Update, Delete
- Test authentication/authorization separately from business logic
- Use test fixtures or factories to create test data -- do not depend on data from other tests

---

## CI/CD Integration

### When to Run Which Tests

| Pipeline Stage | Tests to Run | Gate? | Max Duration |
|---|---|---|---|
| Pre-commit (local) | Linting, unit tests for changed files | Advisory | < 30 seconds |
| Pull request | Full unit tests, integration tests | Blocking | < 10 minutes |
| Merge to main | Full unit + integration + API contract tests | Blocking | < 15 minutes |
| Pre-deployment (staging) | E2E smoke tests, performance baseline | Blocking | < 30 minutes |
| Post-deployment (production) | Smoke tests, synthetic monitoring | Alerting | < 5 minutes |

### Parallel Execution

- Split test suites by module or test file for parallel execution
- Use test runners that support parallel mode (pytest-xdist, Jest --workers, xUnit parallel collections)
- Ensure tests are independent -- no shared state, no ordering dependencies
- Use separate databases or schemas per parallel worker to avoid data conflicts

### Test Splitting Strategies

- **By file**: Distribute test files across workers. Simple but uneven if file sizes vary.
- **By timing**: Use historical execution times to balance workers evenly.
- **By tag/label**: Run critical tests first, then the rest.

---

## Flaky Test Management

Flaky tests pass and fail intermittently without code changes. They erode trust in the test suite.

### Detection

- Track test results over time -- flag tests that fail > 2% of runs without code changes
- Run failed tests in retry mode to distinguish flaky failures from real failures
- CI systems like GitHub Actions support automatic retry; use it for detection, not as a permanent fix

### Root Cause Categories

| Category | Common Causes | Fix |
|---|---|---|
| **Timing** | Race conditions, async operations, animations | Use explicit waits for conditions, not sleep |
| **Test order dependency** | Test relies on state from a previous test | Make each test set up its own state |
| **Shared state** | Tests share a database, file, or global variable | Isolate state per test (transactions, temp dirs) |
| **Environment** | Network latency, resource contention, clock skew | Mock external dependencies, use fixed timestamps |
| **Non-determinism** | Random data, current date/time, UUIDs in assertions | Control randomness with seeds, mock clocks |

### Quarantine Process

1. Identify the flaky test
2. Move it to a quarantine suite that runs separately (does not block the pipeline)
3. File a ticket with root cause investigation
4. Fix and move back to the main suite
5. Monitor for recurrence

### Prevention

- Never use `sleep()` or fixed delays -- wait for a specific condition
- Never assert on generated values (timestamps, UUIDs) unless they are controlled
- Always clean up test data in teardown, even if the test fails
- Run the full suite multiple times before merging new tests

---

## Test Data Management in Automation

### Fixtures

- Static data loaded before test execution (JSON files, SQL scripts, CSV)
- Good for read-only reference data
- Version-controlled alongside tests

### Factories

- Programmatic data creation with sensible defaults and overrides
- Example: `UserFactory.create(role="admin", verified=True)`
- Preferred over fixtures for data that varies between tests

### Cleanup

- Use database transactions that roll back after each test (fastest)
- If transactions are not feasible, delete created data in teardown
- Never rely on test ordering for cleanup -- each test cleans up after itself

---

## Mocking and Stubbing Strategies

### When to Mock

- External services (payment gateways, email providers, third-party APIs)
- Slow or unreliable dependencies (network calls, file systems in unit tests)
- Components that are not the subject of the current test

### What Not to Mock

- The system under test itself
- Database interactions in integration tests (use a real test database)
- Simple, fast, deterministic functions (mocking adds complexity without value)

### Mock Boundaries

- Mock at the boundary of the system under test, not deep inside it
- If mocking requires reaching into private internals, the design may need refactoring
- Prefer dependency injection over monkey-patching for testability

### Contract Verification

When mocking an external service, verify that the mock matches the real service's behavior:
- Use contract tests (Pact, Spring Cloud Contract) to validate mock accuracy
- Periodically run a subset of tests against the real service to detect drift

---

## Test Reporting and Dashboards

### What to Report

| Audience | Metrics | Format |
|---|---|---|
| Developers | Failed test details, stack traces, execution time | CI output, IDE integration |
| QA team | Pass rate, coverage, flaky test list, trends | Dashboard (Allure, ReportPortal) |
| Management | Quality gate status, defect trends, release readiness | Summary dashboard, email digest |

### Report Essentials

- Total tests: passed, failed, skipped, errored
- Execution time per suite and per test
- Failure details with screenshots (UI tests), request/response (API tests), logs
- Trend over the last N runs -- is quality improving or degrading?

---

## Automation Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| **Brittle selectors** | Tests break when CSS/HTML changes | Use data-testid attributes or accessible roles |
| **Sleep-based waits** | Tests are slow and still flaky | Wait for specific conditions (element visible, API returns) |
| **Shared mutable state** | Tests interfere with each other | Isolate state per test |
| **God test** | One test verifies too many things | Split into focused tests with single assertions |
| **Copy-paste tests** | Maintenance burden multiplies | Extract shared logic into helpers or fixtures |
| **Ignoring flaky tests** | Trust in the suite degrades | Quarantine, investigate, fix |
| **Testing framework code** | Tests verify the framework, not the application | Test application behavior only |
| **No cleanup** | Test data accumulates, causing failures | Always clean up in teardown |
| **Automating everything** | Diminishing returns on low-value tests | Apply ROI analysis -- automate high-frequency, high-risk tests first |
| **No test review** | Low-quality tests go unnoticed | Review test code with the same rigor as production code |
