# Clean Code Principles

Language-agnostic coding standards. Apply these alongside the language-specific reference for every task.

---

## Meaningful Names

- Use intention-revealing names: the name should answer why it exists, what it does, and how it is used
- Avoid abbreviations, single-letter variables (except short loop counters), and generic names like `data`, `info`, `temp`, `result`
- Use searchable names: longer, descriptive names over short cryptic ones
- Name booleans as predicates: `is_valid`, `has_access`, `can_retry`
- Avoid encoding type or scope into names (no Hungarian notation)
- Use consistent vocabulary: pick one word per concept and use it everywhere (e.g., choose `fetch` or `get`, not both)

## Functions

- Do one thing. If you can extract a meaningful sub-function, the original does too much
- Keep functions short: aim for 5-20 lines; treat 30+ lines as a refactoring signal
- Limit parameters to 3 or fewer; group related parameters into an object or struct
- Avoid flag arguments that switch behavior; split into separate functions instead
- Use descriptive verb-phrase names: `calculate_total`, `validate_input`, `send_notification`
- Minimize side effects: prefer pure functions where practical; document side effects when unavoidable
- Return early to reduce nesting; avoid deep conditional chains

## Comments

- Prefer self-documenting code over comments; rename or restructure before adding a comment
- Use comments for why, never for what: explain intent, constraints, or non-obvious trade-offs
- Delete commented-out code; version control preserves history
- Keep doc comments on public APIs accurate and current
- Mark workarounds and technical debt with TODO/HACK and a reason

## Formatting

- Maintain consistent indentation and brace style per project convention
- Group related code together; separate unrelated blocks with blank lines
- Keep files focused: one primary concept per file
- Order members by relevance: public API first, then private helpers
- Keep lines under the project's agreed length limit

## Error Handling

- Prefer exceptions over error codes in languages that support them
- Catch specific errors, not catch-all handlers
- Fail fast: validate inputs at boundaries and reject invalid state immediately
- Never swallow errors silently; log or propagate with context
- Keep error handling separate from business logic; avoid mixing happy path and error path in the same block
- Provide actionable error messages that help the caller fix the problem

## Boundaries

- Wrap third-party APIs behind your own interface; isolate external dependencies at the boundary
- Write integration tests for boundary code; mock the boundary in unit tests
- Define clear data contracts (DTOs, schemas) at system boundaries
- Minimize the surface area of external dependencies: import only what you use

## Unit Tests

- Follow Arrange-Act-Assert (or Given-When-Then) structure
- Test one behavior per test; name tests after the behavior they verify
- Keep tests fast, isolated, and repeatable with no shared mutable state
- Use test doubles (mocks, stubs, fakes) only at boundaries; avoid mocking internals
- Treat test code with the same quality standards as production code
- Aim for meaningful coverage of business logic, not arbitrary coverage percentages

## Classes

- Keep classes small and cohesive: every field and method should relate to the class's single purpose (see SRP in oop-patterns.md for the principle; apply it here as a size constraint)
- Treat 200+ lines or 5+ dependencies as a refactoring signal
- Hide internals: expose behavior through public methods, not raw data
- Prefer composition over inheritance for flexibility (see oop-patterns.md for patterns)
- Separate data-holding classes from behavior-rich classes; avoid god objects that do both

## Emergent Design

- Run all tests before committing; passing tests are the minimum quality bar
- Refactor after making it work: remove duplication, improve names, simplify structure
- Apply the Rule of Three: tolerate minor duplication until a pattern emerges; then extract
- Keep the design as simple as possible: fewest classes and methods that satisfy requirements
- Let architecture emerge from requirements, not from speculative abstraction

## Code Smells

- **Long function**: extract sub-functions when a function exceeds 30 lines or has multiple indent levels
- **Large class**: split when a class holds unrelated responsibilities or exceeds 200 lines
- **Feature envy**: move logic to the class whose data it uses most
- **Primitive obsession**: replace raw strings/ints with domain types (value objects, enums)
- **Divergent change**: if one class changes for multiple reasons, split by reason
- **Shotgun surgery**: if one change touches many files, consolidate the scattered logic
- **Dead code**: delete unreachable or unused code; do not comment it out
- **Magic values**: replace literal numbers and strings with named constants

---

## Language-Specific Naming Exceptions

These override the general naming rules above for language-idiomatic conventions.

**Python**: `snake_case` for functions, methods, variables, modules. `PascalCase` for classes. `UPPER_SNAKE_CASE` for module-level constants. Leading underscore `_private` for non-public members. Double underscore `__name_mangled` only for true name-mangling needs.

**GDScript**: `snake_case` for functions, variables, signals. `PascalCase` for classes and node names. `UPPER_SNAKE_CASE` for constants and enums. Prefix private members with underscore. Prefix signal names with verbs or events: `health_changed`, `item_collected`.

**Go**: `PascalCase` for exported identifiers, `camelCase` for unexported. No underscores in names. Acronyms stay all-caps (`HTTPClient`, `userID`). Short variable names are idiomatic in small scopes (`i`, `n`, `err`). Receivers use 1-2 letter abbreviations of the type name.
