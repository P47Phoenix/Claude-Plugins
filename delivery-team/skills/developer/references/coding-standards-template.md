# Team Coding Standards

This file defines your team's coding standards. It was generated from the built-in
clean code reference and is designed to be customized for your project.

**How this integrates with the developer skill**: When you set
`tech_stack.clean_code_guide: .delivery/standards/coding-standards.md` in your
`.delivery/config.yml`, the developer skill will load THIS file instead of the
built-in `clean-code.md` for every coding task. Your customizations will be applied
automatically to all code generation, review, and refactoring.

**How to customize**: Each section below contains HTML comment placeholders. Replace
the placeholder comments with your team's specific conventions. You can also modify,
remove, or add to the built-in principles.

---

## Meaningful Names

- Use intention-revealing names: the name should answer why it exists, what it does, and how it is used
- Avoid abbreviations, single-letter variables (except short loop counters), and generic names like `data`, `info`, `temp`, `result`
- Use searchable names: longer, descriptive names over short cryptic ones
- Name booleans as predicates: `is_valid`, `has_access`, `can_retry`
- Avoid encoding type or scope into names (no Hungarian notation)
- Use consistent vocabulary: pick one word per concept and use it everywhere

<!-- Add your team's naming conventions here. Examples: preferred prefixes/suffixes, domain-specific terminology, naming patterns for services/repositories/handlers -->

## Functions

- Do one thing. If you can extract a meaningful sub-function, the original does too much
- Keep functions short: aim for 5-20 lines; treat 30+ lines as a refactoring signal
- Limit parameters to 3 or fewer; group related parameters into an object or struct
- Avoid flag arguments that switch behavior; split into separate functions instead
- Use descriptive verb-phrase names: `calculate_total`, `validate_input`, `send_notification`
- Minimize side effects: prefer pure functions where practical; document side effects when unavoidable
- Return early to reduce nesting; avoid deep conditional chains

<!-- Add your team's function conventions here. Examples: maximum line count, required parameter documentation, async/sync patterns -->

## Comments

- Prefer self-documenting code over comments; rename or restructure before adding a comment
- Use comments for why, never for what: explain intent, constraints, or non-obvious trade-offs
- Delete commented-out code; version control preserves history
- Keep doc comments on public APIs accurate and current
- Mark workarounds and technical debt with TODO/HACK and a reason

<!-- Add your team's comment conventions here. Examples: required doc comment format, TODO tag format, header comment requirements -->

## Formatting

- Maintain consistent indentation and brace style per project convention
- Group related code together; separate unrelated blocks with blank lines
- Keep files focused: one primary concept per file
- Order members by relevance: public API first, then private helpers
- Keep lines under the project's agreed length limit

<!-- Add your team's formatting conventions here. Examples: max line length, import ordering rules, file organization patterns -->

## Error Handling

- Prefer exceptions over error codes in languages that support them
- Catch specific errors, not catch-all handlers
- Fail fast: validate inputs at boundaries and reject invalid state immediately
- Never swallow errors silently; log or propagate with context
- Keep error handling separate from business logic
- Provide actionable error messages that help the caller fix the problem

<!-- Add your team's error handling conventions here. Examples: custom exception hierarchy, logging format, retry policies, error code catalog -->

## Boundaries

- Wrap third-party APIs behind your own interface; isolate external dependencies at the boundary
- Write integration tests for boundary code; mock the boundary in unit tests
- Define clear data contracts (DTOs, schemas) at system boundaries
- Minimize the surface area of external dependencies: import only what you use

<!-- Add your team's boundary conventions here. Examples: approved third-party libraries, API wrapper patterns, contract-first design requirements -->

## Unit Tests

- Follow Arrange-Act-Assert (or Given-When-Then) structure
- Test one behavior per test; name tests after the behavior they verify
- Keep tests fast, isolated, and repeatable with no shared mutable state
- Use test doubles (mocks, stubs, fakes) only at boundaries; avoid mocking internals
- Treat test code with the same quality standards as production code
- Aim for meaningful coverage of business logic, not arbitrary coverage percentages

<!-- Add your team's testing conventions here. Examples: minimum coverage thresholds, test naming patterns, required test categories, test data management -->

## Classes

- Keep classes small and cohesive: every field and method should relate to the class's single purpose
- Treat 200+ lines or 5+ dependencies as a refactoring signal
- Hide internals: expose behavior through public methods, not raw data
- Prefer composition over inheritance for flexibility
- Separate data-holding classes from behavior-rich classes; avoid god objects

<!-- Add your team's class design conventions here. Examples: maximum class size, required interfaces, dependency injection patterns, base class restrictions -->

## Emergent Design

- Run all tests before committing; passing tests are the minimum quality bar
- Refactor after making it work: remove duplication, improve names, simplify structure
- Apply the Rule of Three: tolerate minor duplication until a pattern emerges; then extract
- Keep the design as simple as possible: fewest classes and methods that satisfy requirements
- Let architecture emerge from requirements, not from speculative abstraction

<!-- Add your team's design conventions here. Examples: refactoring triggers, design review checkpoints, architecture decision record requirements -->

## Code Smells

- **Long function**: extract sub-functions when a function exceeds 30 lines or has multiple indent levels
- **Large class**: split when a class holds unrelated responsibilities or exceeds 200 lines
- **Feature envy**: move logic to the class whose data it uses most
- **Primitive obsession**: replace raw strings/ints with domain types (value objects, enums)
- **Divergent change**: if one class changes for multiple reasons, split by reason
- **Shotgun surgery**: if one change touches many files, consolidate the scattered logic
- **Dead code**: delete unreachable or unused code; do not comment it out
- **Magic values**: replace literal numbers and strings with named constants

<!-- Add your team's code smell thresholds here. Examples: custom line limits, additional smells to watch for, automated detection tool configuration -->
