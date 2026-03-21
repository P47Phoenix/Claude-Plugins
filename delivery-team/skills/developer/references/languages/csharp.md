# C# Best Practices

Version baseline: .NET 8 / C# 12

## Style & Formatting

- Follow Microsoft's C# coding conventions; enforce with EditorConfig + Roslyn analyzers
- Use `PascalCase` for types, methods, properties, events, namespaces; `camelCase` for local variables and parameters; `_camelCase` for private fields
- Use `var` when the type is obvious from the right-hand side; use explicit types when it aids clarity
- Enable nullable reference types: `<Nullable>enable</Nullable>` in `.csproj`
- Use file-scoped namespace declarations (`namespace Foo;`) in new code
- One type per file; file name matches type name

## Idioms & Patterns

- Use `record` types for immutable data transfer objects
- Use `record struct` for small value-type DTOs
- Use pattern matching (`switch` expressions, `is` patterns) over long `if-else` chains and `as` casts
- Use `init`-only properties for immutable construction: `public string Name { get; init; }`
- Use primary constructors (C# 12) for simple dependency injection
- Use `required` modifier for properties that must be set during construction
- Prefer LINQ for collection transformations, but avoid LINQ in performance-critical paths
- Use `IReadOnlyList<T>` / `IReadOnlyDictionary<K,V>` for outgoing collection types
- Use `async`/`await` throughout the stack — avoid `.Result` and `.Wait()` (deadlock risk)
- Use `CancellationToken` in all async methods that do I/O

## Error Handling

- Do not use exceptions for control flow (expected cases) — return result types or use `bool TryXxx(out T result)` patterns
- Catch specific exception types; avoid bare `catch (Exception)`
- Use `when` clause in catch to filter: `catch (HttpRequestException ex) when (ex.StatusCode == 404)`
- Always log exceptions before swallowing; never `catch { }` silently
- Use `ILogger<T>` for structured logging; avoid `Console.WriteLine` in production code
- Wrap external I/O in try/catch at the boundary; let domain code stay exception-free

## Testing

- Use `xUnit` as the test framework; `NSubstitute` or `Moq` for mocking
- Name test classes `<SystemUnderTest>Tests`; test methods `<Method>_<Scenario>_<ExpectedResult>`
- Use `[Theory]` with `[InlineData]` or `[MemberData]` for parameterized tests
- Use `FluentAssertions` for readable assertions
- Write integration tests with `WebApplicationFactory<TProgram>` for ASP.NET Core
- Use `Testcontainers` for database and external service integration tests

## Security

- Use parameterized queries or an ORM; never concatenate SQL strings
- Use `SecureString` or Azure Key Vault for secrets — never store in `appsettings.json`
- Enable HTTPS redirection and HSTS in ASP.NET Core
- Use `[Authorize]` and policy-based authorization — never roll your own auth
- Avoid `dynamic` type — it bypasses compile-time type safety
- Use `System.Security.Cryptography` for crypto operations — never implement your own
- Keep NuGet packages updated; use `dotnet list package --vulnerable` in CI

## Performance

- Use `Span<T>`, `Memory<T>`, and `ArrayPool<T>` in high-throughput code to reduce allocations
- Profile with `dotnet-trace` and `dotnet-counters` before optimizing
- Use `StringBuilder` for string concatenation in loops
- Prefer `ValueTask<T>` over `Task<T>` for frequently awaited, often-synchronous operations
- Use `IAsyncEnumerable<T>` for streaming large datasets
- Avoid `async void` — use `async Task` instead

## Anti-Patterns to Avoid

- **`.Result` / `.Wait()` on Tasks:** causes deadlocks in synchronization contexts
- **`async void`:** exceptions are unobservable; use `async Task`
- **`Thread.Sleep` in async code:** use `await Task.Delay()`
- **Catching and ignoring exceptions:** always log at minimum
- **Large `switch` on type:** use polymorphism or pattern matching
- **Public mutable collections on exposed types:** expose `IReadOnlyList<T>`
- **Nullable obliviousness:** enable nullable reference types and fix all warnings

## Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| `dotnet build /p:TreatWarningsAsErrors=true` | Enforce analyzer rules | — |
| `dotnet test` | Run tests | `dotnet test --collect:"XPlat Code Coverage"` |
| `dotnet format` | Format code | `dotnet format` |
| `dotnet list package --vulnerable` | Security audit | — |
| `Roslyn analyzers` | Code quality | Via `<Nullable>enable</Nullable>` + `<WarningsAsErrors>` |
