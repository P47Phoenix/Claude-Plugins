# Test Case Patterns Reference

This reference provides test design techniques and patterns for writing effective test cases. The sub-agent should apply these techniques when producing test cases, test data specifications, and test plans.

---

## Equivalence Partitioning

Divide input data into classes (partitions) where all values in a class are expected to behave the same way. Test one representative value from each class instead of exhaustively testing every value.

### Steps

1. Identify all inputs and their valid ranges
2. Divide each input into valid and invalid equivalence classes
3. Select one representative value from each class
4. Write one test case per representative value

### Example: Age Input (Valid Range 18-65)

| Class | Range | Representative Value | Expected Behavior |
|---|---|---|---|
| Below minimum (invalid) | < 18 | 10 | Rejected with error |
| Valid range | 18-65 | 30 | Accepted |
| Above maximum (invalid) | > 65 | 80 | Rejected with error |
| Non-numeric (invalid) | "abc" | "abc" | Rejected with type error |
| Empty (invalid) | "" | "" | Rejected with required error |
| Negative (invalid) | < 0 | -5 | Rejected with error |

### When to Use

- Large or infinite input domains that cannot be tested exhaustively
- Any input with clearly defined valid and invalid ranges
- As a first pass before applying boundary value analysis

---

## Boundary Value Analysis

Defects cluster at the boundaries of equivalence classes. Test values at, just below, and just above each boundary.

### Boundary Points

For a range [min, max]:
- **On-boundary**: min, max
- **Off-boundary (just inside)**: min + 1, max - 1
- **Off-boundary (just outside)**: min - 1, max + 1

### Example: Age Input (Valid Range 18-65)

| Test Point | Value | Expected Behavior |
|---|---|---|
| Just below minimum | 17 | Rejected |
| At minimum (boundary) | 18 | Accepted |
| Just above minimum | 19 | Accepted |
| Just below maximum | 64 | Accepted |
| At maximum (boundary) | 65 | Accepted |
| Just above maximum | 66 | Rejected |

### Special Boundaries

- Zero (0) -- transition between positive and negative
- Empty string vs single character
- Null vs empty vs whitespace
- Maximum integer, maximum string length, maximum array size
- Midnight (00:00), end of month, end of year, leap year boundaries

---

## Decision Table Testing

When behavior depends on combinations of conditions, a decision table enumerates all combinations and their expected actions.

### Structure

| Conditions | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|---|---|---|---|---|
| Condition A | True | True | False | False |
| Condition B | True | False | True | False |
| **Actions** | | | | |
| Action X | Yes | Yes | No | No |
| Action Y | No | Yes | Yes | No |

### Simplification

- If a condition does not affect the action, mark it as "don't care" (--)
- Merge rules that produce the same action when one condition is "don't care"
- For N conditions, the full table has 2^N rules -- simplify aggressively for large tables

### When to Use

- Business rules with multiple interacting conditions
- Permission systems (role + action + resource combinations)
- Pricing rules, discount logic, eligibility checks
- Any logic with "if A and B but not C, then do X"

---

## State Transition Testing

When the system behaves differently based on its current state, model the states and transitions explicitly.

### Components

- **States**: Distinct conditions the system can be in (e.g., Draft, Submitted, Approved, Rejected)
- **Transitions**: Events that cause state changes (e.g., submit, approve, reject, revise)
- **Guards**: Conditions that must be true for a transition to occur
- **Actions**: Side effects triggered by a transition (e.g., send notification)

### State Transition Table

| Current State | Event | Guard | Next State | Action |
|---|---|---|---|---|
| Draft | Submit | All fields valid | Submitted | Send to reviewer |
| Draft | Submit | Missing fields | Draft | Show validation errors |
| Submitted | Approve | Reviewer role | Approved | Send confirmation |
| Submitted | Reject | Reviewer role | Rejected | Send rejection notice |
| Rejected | Revise | Author role | Draft | Clear rejection |

### Test Cases from State Transitions

1. **Valid transitions**: One test per row in the transition table
2. **Invalid transitions**: Attempt events that should not be possible from a given state (e.g., Approve from Draft)
3. **Transition sequences**: Multi-step paths through the state diagram (Draft -> Submitted -> Rejected -> Draft -> Submitted -> Approved)

---

## Pairwise / Combinatorial Testing

When full combination testing is impractical (too many inputs), pairwise testing ensures every pair of input values is tested at least once.

### When to Use

- 3 or more input parameters, each with multiple values
- Full combinatorial testing would produce hundreds or thousands of test cases
- Interactions between pairs of inputs are more likely to reveal defects than three-way or higher interactions

### Example

Three inputs: Browser (Chrome, Firefox, Safari), OS (Windows, Mac, Linux), Language (EN, FR, DE)

Full combinations: 3 x 3 x 3 = 27 test cases. Pairwise coverage can be achieved in approximately 9 test cases.

### Tools

Use pairwise generation tools (PICT, AllPairs, pairwise.org) to generate the minimal set. Do not construct pairwise tables manually for more than 3 inputs.

---

## Given-When-Then Format

Structure test cases as scenarios using the Given-When-Then format for clarity and traceability to acceptance criteria.

### Template

```
Given [precondition / initial state]
  And [additional precondition if needed]
When [action / event]
  And [additional action if needed]
Then [expected outcome]
  And [additional expected outcome if needed]
```

### Example

```
Scenario: Successful login with valid credentials
  Given the user is on the login page
    And the user has a verified account
  When the user enters a valid email and password
    And clicks the "Sign In" button
  Then the user is redirected to the dashboard
    And a welcome message displays the user's name
    And the session token is stored in a secure cookie
```

### Guidelines

- **Given**: State, not action. Describes the world before the test.
- **When**: Exactly one action (or tightly coupled sequence). If you need multiple When clauses, consider splitting into separate scenarios.
- **Then**: Observable outcome. Must be verifiable. Avoid vague assertions like "works correctly."

---

## Test Case Template

Every test case should include these fields:

| Field | Description | Example |
|---|---|---|
| **ID** | Unique identifier | TC-LOGIN-001 |
| **Title** | Brief descriptive name | Valid login with correct credentials |
| **Type** | Functional, negative, boundary, performance, security | Functional |
| **Priority** | Critical, High, Medium, Low | High |
| **Preconditions** | State that must exist before the test | User account exists and is verified |
| **Steps** | Numbered actions to perform | 1. Navigate to /login 2. Enter valid email 3. Enter valid password 4. Click Sign In |
| **Expected Result** | Observable, verifiable outcome | User redirected to /dashboard, welcome message shown |
| **Test Data** | Specific values used | Email: test@example.com, Password: ValidPass123 |
| **Traceability** | Link to requirement or acceptance criterion | US-001 AC-3 |

---

## Negative Testing Patterns

Negative tests verify the system handles invalid input and error conditions gracefully.

### Common Negative Test Categories

| Category | Examples |
|---|---|
| **Missing required input** | Submit form with blank required fields |
| **Invalid data type** | Enter text in a numeric field, negative number for quantity |
| **Boundary violations** | Exceed max length, below minimum value |
| **Unauthorized access** | Access admin page as regular user, access another user's data |
| **Invalid state transitions** | Approve an already-rejected item, cancel a completed order |
| **Concurrent modifications** | Two users edit the same record simultaneously |
| **Resource exhaustion** | Upload file exceeding size limit, request when rate-limited |
| **Malformed input** | SQL injection strings, XSS payloads, special characters, Unicode edge cases |
| **Network failures** | Request during timeout, retry after connection drop |

### Negative Test Design Rule

For every positive test case, ask: "What could go wrong?" Then write a test case for each failure mode. The system should fail gracefully -- with a clear error message, no data corruption, and no security exposure.

---

## Test Data Generation Strategies

### Synthetic Data

- Generate data programmatically using factories or builders
- Use libraries like Faker (Python/JS), Bogus (C#), or DataFactory (Java)
- Ensure synthetic data covers all equivalence classes and boundary values

### Edge Case Data

- Empty strings, null values, whitespace-only strings
- Maximum-length strings (at limit, one over limit)
- Special characters: quotes, backslashes, angle brackets, Unicode, emoji
- Date edge cases: Feb 29, Dec 31, Jan 1, timezone boundaries
- Numeric edge cases: 0, -1, MAX_INT, MIN_INT, NaN, Infinity

### Representative Data Sets

- **Minimum viable set**: Smallest data set that exercises all paths
- **Stress set**: Large data set to verify performance under volume
- **Realistic set**: Data that resembles production patterns (anonymized if derived from production)

---

## Common Test Case Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| **No expected result** | Cannot determine pass/fail | Always specify the observable outcome |
| **Vague steps** | "Test the login" -- not reproducible | Write numbered, specific actions |
| **Happy path only** | Misses defects in error handling | Add negative tests for every positive test |
| **Duplicate coverage** | Multiple tests verify the same thing | Review for overlap, consolidate |
| **Test depends on another test** | Failure cascades, hard to isolate | Each test sets up its own preconditions |
| **Hardcoded environment data** | Tests break when environment changes | Use configurable test data and relative references |
| **Testing implementation, not behavior** | Breaks on refactoring | Test what the system does, not how it does it |
| **Missing boundary tests** | Defects at edges go undetected | Apply boundary value analysis to every bounded input |
