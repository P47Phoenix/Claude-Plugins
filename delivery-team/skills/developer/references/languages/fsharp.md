# F# Best Practices

Version baseline: F# 8 / .NET 8

---

## Style & Formatting

- Use **Fantomas** as the canonical formatter. Configure via `.editorconfig` or `fantomas-config`.
- 4-space indentation. No tabs.
- Module-per-file convention: one module per `.fs` file, module name matches filename.
- Order files in `.fsproj` by dependency (F# requires top-down compilation order).
- Prefer `module` over `namespace` for leaf files; use `namespace` for shared types.
- Prefix private helpers with underscore by convention (`_helper`), or use `let private`.
- Keep lines under 120 characters. Fantomas handles wrapping automatically.

## Idioms & Patterns

### Discriminated Unions
- Model domain states explicitly. Prefer DUs over class hierarchies.
- Single-case DUs for type safety on primitives: `type EmailAddress = EmailAddress of string`.
- Use `[<Struct>]` attribute on small DUs (1-2 cases, no recursive types) to avoid heap allocation.

### Pattern Matching
- Always handle all cases. Enable `--warnon:3262` to catch incomplete matches.
- Use active patterns for reusable decomposition:
  ```fsharp
  let (|Even|Odd|) n = if n % 2 = 0 then Even else Odd
  ```
- Partial active patterns return `Option`: `(|ParseInt|_|)`.
- Avoid nested matches deeper than 2 levels; extract into named active patterns or helper functions.

### Computation Expressions
- `task { }` for async I/O (preferred over `async { }` in .NET 8 for interop and performance).
- `result { }` for railway-oriented programming with `Result<'T, 'E>`.
- Custom CEs for domain-specific workflows (validation, logging, retry).
- Use `let!` for binding, `do!` for side effects, `return` for wrapping.

### Railway-Oriented Programming
- Chain operations with `Result.bind` or `result { }` CE.
- Define domain errors as a DU: `type AppError = NotFound | ValidationError of string`.
- Use `Result.map` for transforming success values, `Result.mapError` for error translation.
- At system boundaries (HTTP, CLI), convert `Result` to appropriate response codes.

### Module Organization
- Group related types and functions in a module.
- Place types at top of module, functions below.
- Use `[<AutoOpen>]` sparingly -- only for truly ubiquitous helpers.
- Companion modules: `type Widget = ...` in one file, `module Widget` with functions in another.

### Immutability
- All bindings are immutable by default. Use `mutable` only in performance-critical hot paths.
- Prefer `{| record with field = newValue |}` for updates (anonymous record copy-and-update).
- Use `Map`, `Set`, `list` over mutable collections. Switch to `ResizeArray` or `Dictionary` only when profiling justifies it.

### Type Providers
- Use for compile-time schema verification (JSON, SQL, CSV, Swagger).
- Prefer erasing type providers in libraries (no runtime dependency on provider assembly).
- Pin schema files in source control for reproducible builds.

## Error Handling

- Use `Result<'T, 'E>` for expected, recoverable errors (validation, business rules).
- Use exceptions for unexpected, unrecoverable errors (corrupted state, infrastructure failure).
- Never catch `System.Exception` broadly; catch specific exception types.
- Define error DUs per bounded context; translate at boundaries.
- `Option` for absence of value (not for errors). Do not encode error info in `None`.
- `ValueOption` for performance-sensitive code paths.

## Testing

- **Expecto**: preferred for property-based and unit testing. Provides `testList`, `testCase`, `Expect` API.
- **FsCheck**: property-based testing. Define custom generators via `Arb.generate<'T>`.
- **FsUnit**: NUnit/xUnit assertion wrappers with F# syntax (`should equal`, `should throw`).
- Test modules mirror source modules: `MyModule.fs` -> `MyModuleTests.fs`.
- Use inline test data with list comprehensions; avoid heavy mocking frameworks.
- Test pure functions directly. For effectful code, inject dependencies as function parameters.
- Prefer `Expect.equal actual expected "message"` over assertion-less tests.

## Security

- Validate all inputs at system boundaries; use single-case DUs with smart constructors.
- Use `System.Security.Cryptography` for hashing/encryption, never roll custom crypto.
- Sanitize SQL via parameterized queries (Dapper, Npgsql, or type providers).
- Mark sensitive data types as `[<Struct; NoComparison; NoEquality>]` to prevent accidental logging.
- Use `ConfigurationBuilder` with user secrets or Azure Key Vault for secrets management.

## Performance

- Prefer `task { }` over `async { }` for .NET interop (avoids `Async.StartAsTask` overhead).
- Use `[<Struct>]` on small DUs and records to reduce GC pressure.
- `Array` for random access and bulk processing; `list` for recursive/head-tail patterns.
- `Span<'T>` and `Memory<'T>` for zero-copy parsing in hot paths.
- Profile with `dotnet-trace` and `dotnet-counters` before optimizing.
- Tail-recursive functions: use `rec` and ensure the recursive call is in tail position, or use `List.fold`.
- Avoid `Seq` in hot paths (lazy, no caching); use `Array` or `ResizeArray`.

## Anti-Patterns to Avoid

- **Overusing classes**: F# is not C#. Prefer modules + functions + DUs over OOP class hierarchies.
- **Ignoring exhaustive matching warnings**: always handle all DU cases.
- **Stringly-typed code**: use DUs and single-case wrappers instead of raw strings.
- **Mutable state by default**: reach for `mutable` only after profiling proves necessity.
- **Deep nesting of `match` expressions**: extract active patterns or decompose into smaller functions.
- **Using `obj` or `dynamic`**: defeats the type system. Use generics or DUs instead.
- **Ignoring file order in `.fsproj`**: compilation order matters; misorder causes confusing errors.
- **`async { }` for everything**: use `task { }` for I/O-bound work in .NET 8+.

## Tooling

- **IDE**: Rider (JetBrains) or VS Code + Ionide extension.
- **Formatter**: Fantomas (integrate into CI with `dotnet fantomas --check`).
- **Linter**: FSharpLint (optional, covers style rules Fantomas does not).
- **Build**: `dotnet build` / `dotnet publish`. Use FAKE for complex build scripts.
- **Package management**: NuGet via `<PackageReference>` in `.fsproj`.
- **REPL**: `dotnet fsi` for interactive exploration and scripting.
- **Fable**: F# to JavaScript compiler. Use with SAFE Stack (Saturn, Azure, Fable, Elmish) for full-stack F#.
- **Documentation**: `dotnet fsdocs` for API docs from XML comments.
