# Java Best Practices

Version baseline: Java 17 LTS (with Java 21 features noted where applicable)

## Style & Formatting

- Follow Google Java Style Guide or Oracle's Code Conventions; enforce with Checkstyle
- Format with `google-java-format` or IDE formatter tied to a shared config
- Use `PascalCase` for classes and interfaces; `camelCase` for methods and variables; `UPPER_SNAKE_CASE` for constants; lowercase for packages (no underscores)
- Keep classes focused — Single Responsibility Principle; split large classes
- Use `final` for fields that should not be reassigned; prefer immutability

## Idioms & Patterns

- Use `record` types (Java 16+) for immutable data carriers instead of verbose POJOs
- Use `sealed` classes and interfaces (Java 17+) to restrict inheritance hierarchies
- Use `var` for local variables where the type is obvious from context (Java 10+)
- Use pattern matching for `instanceof` (Java 16+): `if (obj instanceof String s) { ... }`
- Use `switch` expressions with arrow syntax over `switch` statements (Java 14+)
- Use the Stream API for collection transformations; avoid it for side effects
- Use `Optional<T>` as return types to signal absent values — do not pass `Optional` as parameters
- Use dependency injection (Spring, Guice) rather than `new` for service-layer objects
- Use `text blocks` (Java 15+) for multiline strings

## Error Handling

- Distinguish checked exceptions (recoverable, caller must handle) from unchecked (bugs, propagate up)
- Do not catch `Throwable` or `Error` — only `Exception` or specific subtypes
- Never swallow exceptions: `catch (Exception e) { }` — at minimum, log
- Use try-with-resources for `AutoCloseable` resources — never `finally { resource.close() }`
- Translate low-level exceptions to domain exceptions at layer boundaries
- Use structured logging (`slf4j` + `logback`/`log4j2`) — never `System.out.println` in production

## Testing

- Use `JUnit 5` (`@Test`, `@ParameterizedTest`, `@ExtendWith`) as the test framework
- Use `Mockito` for mocking; `AssertJ` for fluent assertions
- Name tests: `methodName_scenario_expectedResult` or use `@DisplayName` for natural language
- Use `@ParameterizedTest` with `@MethodSource` or `@CsvSource` for data-driven tests
- Use `Testcontainers` for integration tests that need real databases or services
- Keep unit tests fast; use integration tests for cross-layer behavior

## Security

- Use parameterized queries or JPA/Hibernate — never concatenate SQL
- Never serialize untrusted data with Java native serialization; use JSON or Protobuf
- Use `BCrypt` or `Argon2` for password hashing (`spring-security-crypto`)
- Validate all input; use Bean Validation (`@NotNull`, `@Size`) at API boundaries
- Keep dependencies updated; use `OWASP Dependency-Check` in CI
- Do not log sensitive data (passwords, tokens, PII)
- Use HTTPS; configure security headers in the web tier

## Performance

- Profile with `async-profiler` or JFR (Java Flight Recorder) before optimizing
- Avoid `String` concatenation in loops — use `StringBuilder`
- Use `HashMap`/`HashSet` for O(1) lookups; know when to use `LinkedHashMap` (insertion order) or `TreeMap` (sorted)
- Preallocate collections when size is known: `new ArrayList<>(size)`
- Use `CompletableFuture` or virtual threads (Java 21) for non-blocking I/O
- Avoid `synchronized` on large blocks; prefer `java.util.concurrent` classes (`ReentrantLock`, `ConcurrentHashMap`)

## Anti-Patterns to Avoid

- **Raw types:** `List list` instead of `List<String> list` — always parameterize generics
- **`null` as a method return value for "not found":** use `Optional<T>`
- **`catch (Exception e)` with no body:** always handle or rethrow
- **`static` mutable state:** makes code non-thread-safe and hard to test
- **God classes:** classes with dozens of methods and fields — split by responsibility
- **Primitive obsession:** wrap primitives in value objects for domain concepts (e.g., `EmailAddress`, `Money`)
- **Finalizers:** use `Cleaner` (Java 9+) or try-with-resources instead

## Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| `maven` / `gradle` | Build | `mvn verify` / `gradle build` |
| `Checkstyle` | Style enforcement | Via build plugin |
| `SpotBugs` | Static analysis | Via build plugin |
| `OWASP Dependency-Check` | Security audit | Via build plugin |
| `JUnit 5` + `Mockito` | Testing | `mvn test` |
| `JaCoCo` | Code coverage | Via build plugin |
