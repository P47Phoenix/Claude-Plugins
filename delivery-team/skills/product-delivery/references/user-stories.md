# User Stories Reference

Templates, INVEST guide, acceptance criteria patterns, and story splitting strategies.

---

## Story Template (Canonical)

```
As a [specific user role]
I want [a specific capability]
So that [the business or user value delivered]

Acceptance Criteria:
Given [context]
When [action]
Then [observable outcome]
```

**Anti-patterns to avoid:**

| Anti-pattern | Problem | Fix |
|---|---|---|
| "As a user..." | Too vague — which user? | "As an authenticated customer", "As a site admin" |
| "I want the system to..." | System-centric, not user-centric | "I want to..." (user perspective) |
| "So that it works correctly" | No value stated | Articulate the business/user outcome |
| "Then it should work" | Not testable | Specific, observable, measurable outcome |
| "Given everything is set up" | Ambiguous precondition | Specific context state |

---

## INVEST Criteria Reference

| Criterion | Test Question | Fix If Failing |
|---|---|---|
| **Independent** | Can this be developed without another story from the same sprint? | Reorder dependencies; split into setup + feature stories |
| **Negotiable** | Does the story allow implementation flexibility? | Remove technical prescriptions; describe the outcome, not the solution |
| **Valuable** | Does this deliver value without other stories being done first? | If not, it may be a task, not a story — elevate to ensure value is self-contained |
| **Estimable** | Can the team give a size? | Too vague → add ACs; too large → split |
| **Small** | Does it fit in one sprint? | Apply splitting strategies below |
| **Testable** | Can a QA engineer write a test from the ACs? | Rewrite ACs in Given/When/Then format |

---

## Acceptance Criteria Patterns

### Given/When/Then (Behavioral — default)

Best for: UI interactions, API behaviors, business rules

```
Given [the user is on the checkout page and has items in their cart]
When [they click "Place Order"]
Then [an order confirmation email is sent within 30 seconds]
And [the order appears in their order history with status "Processing"]
And [inventory is decremented for each purchased item]
```

### Rule-Based (for complex business logic)

Best for: validation rules, eligibility checks, pricing logic

```
Rule: Discount eligibility
- Orders over $100 qualify for 10% discount
- Orders over $250 qualify for 15% discount
- Discount does not apply to sale items
- Only one discount applies per order (highest applicable)
```

### Checklist Format (for multi-condition stories)

Best for: settings pages, admin panels, configuration screens

```
Acceptance Criteria:
- [ ] User can enable/disable email notifications
- [ ] User can set notification frequency (immediate, daily digest, weekly)
- [ ] Changes are saved immediately without page reload
- [ ] Confirmation toast appears on save
- [ ] Preferences persist across sessions
```

---

## Story Splitting Strategies

When a story is too large (fails the Small INVEST criterion), use these techniques:

### 1. Split by Workflow Steps
*Large:* "As a user, I want to complete the checkout process"
*Split into:*
- Add item to cart
- Enter shipping address
- Enter payment details
- Review and confirm order
- Receive confirmation

### 2. Split by Business Rules
*Large:* "As an admin, I want to apply discounts to orders"
*Split into:*
- Apply percentage discount
- Apply fixed amount discount
- Apply free shipping discount
- Apply promo code (validates against code database)

### 3. Split by Data Variation
*Large:* "As a user, I want to pay with any payment method"
*Split into:*
- Pay with credit card
- Pay with PayPal
- Pay with Apple Pay / Google Pay
- Pay with store credit

### 4. Split by Happy Path vs. Edge Cases
*MVP story:* Happy path only (valid inputs, success scenario)
*Follow-up stories:* Error handling, validation failures, edge cases

### 5. Split by User Role
*Large:* "As any user, I want to manage documents"
*Split into:*
- As a viewer, I want to read documents
- As an editor, I want to update documents
- As an admin, I want to delete and archive documents

### 6. Split by CRUD Operations
- Create [entity]
- Read / View [entity]
- Update [entity]
- Delete / Archive [entity]

### 7. Spike Story (for unknowns)
When the team cannot estimate due to technical uncertainty:

```
As a team, I want to investigate [approach/technology]
So that we can estimate the implementation story with confidence

Time-boxed to: [X hours / days]
Output: documented findings + story estimate
```

---

## Sizing Guide (Fibonacci)

| Points | Complexity | Example |
|--------|-----------|---------|
| 1 | Trivial — change a label, update a config value | Update button copy |
| 2 | Simple — single component, clear requirements | Add a form field with validation |
| 3 | Small — 2–3 components, well-understood | Build a read-only data table |
| 5 | Medium — multiple components, some unknowns | Build a filterable, paginated list with API |
| 8 | Large — significant complexity or unknowns | Third-party OAuth integration |
| 13 | Too large — split this story | Anything at 13 should be decomposed |

**T-shirt sizing** (if team prefers):
- XS = 1–2 pts, S = 3 pts, M = 5 pts, L = 8 pts, XL = split required
