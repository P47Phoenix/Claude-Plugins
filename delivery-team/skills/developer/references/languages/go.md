# Go Best Practices

Version baseline: Go 1.21+

## Style & Formatting

- Run `gofmt` (or `goimports`) on every file — there is one correct format; do not debate it
- Use `golangci-lint` with a standard config for additional checks
- Use `camelCase` for unexported identifiers; `PascalCase` for exported identifiers
- Package names: short, lowercase, no underscores (`userservice` not `user_service`)
- Receiver names: short, 1–2 letters matching the type (`u` for `User`); consistent across all methods
- Group imports: stdlib, then external, then internal (separated by blank lines)

## Idioms & Patterns

- Errors are values — return `(T, error)` from functions that can fail; check every error explicitly
- Accept interfaces, return structs — keeps dependencies minimal and code testable
- Use `context.Context` as the first parameter for any function doing I/O or that can be cancelled
- Prefer composition over inheritance — embed types rather than extending them
- Use channels and goroutines for concurrency; keep goroutine lifetimes bounded and explicit
- Use `sync.WaitGroup` or `errgroup.Group` to wait for goroutines; always ensure they are joined
- Use `defer` for cleanup (file close, unlock, cancel) — keep deferred logic simple
- Prefer table-driven tests for comprehensive coverage
- Use `errors.Is()` and `errors.As()` for error comparison — do not compare error strings

## Error Handling

- Handle every error: `if err != nil { return ..., err }` — never `_` an error from a function that can fail in production code
- Wrap errors with context: `fmt.Errorf("parsing config: %w", err)` — use `%w` to preserve the error chain
- Define sentinel errors as exported variables: `var ErrNotFound = errors.New("not found")`
- Define custom error types for errors with additional data: implement the `error` interface
- Do not use `panic` for expected error conditions; `panic` is for programmer errors and unrecoverable states
- Log errors at the call site where context exists; avoid logging and returning the same error (log once)

## Testing

- Use the standard `testing` package; `testify/assert` and `testify/require` are acceptable for assertions
- Name test functions `TestFunctionName_Scenario` (underscore-separated scenario)
- Use table-driven tests with `t.Run()` for sub-tests
- Use `httptest` for HTTP handler tests; `net/http/httptest.NewServer()` for integration tests
- Use interfaces to inject dependencies; replace real implementations with test doubles
- Use `t.TempDir()` for temporary directories — automatically cleaned up after test

## Security

- Validate and sanitize all external input — never trust user-provided data
- Use `html/template` (not `text/template`) for HTML generation to prevent XSS
- Use parameterized queries with `database/sql` — never format SQL with user data
- Use `crypto/rand` for security-sensitive randomness — not `math/rand`
- Use `golang.org/x/crypto` for password hashing (bcrypt); never MD5/SHA1 for passwords
- Run `govulncheck` in CI to scan for known vulnerabilities in dependencies
- Prefer `io.LimitReader` when reading from untrusted sources to prevent unbounded reads

## Performance

- Profile first: `go tool pprof` for CPU and memory profiling
- Avoid unnecessary allocations in hot paths; use `sync.Pool` to reuse objects
- Preallocate slices and maps when size is known: `make([]T, 0, n)`
- Use `strings.Builder` for string concatenation; avoid `+=` in loops
- Prefer passing structs by pointer when they are large (> 3–4 words); pass small structs by value
- Use `benchmarks` (`func BenchmarkXxx(b *testing.B)`) to validate performance changes
- Keep goroutine counts bounded — unbounded goroutine spawning leads to OOM

## Anti-Patterns to Avoid

- **Ignoring errors:** `result, _ := riskyOp()` is almost always wrong
- **`panic` for expected errors:** only panic for truly unrecoverable programmer errors
- **Goroutine leaks:** always ensure goroutines terminate; use `context.Done()` for cancellation
- **Using `interface{}` / `any` unnecessarily:** use generics (Go 1.18+) instead
- **Global state:** avoid package-level mutable variables; use dependency injection
- **`init()` with side effects:** keep `init()` minimal and free of I/O
- **Shadowing `err`:** `:=` in nested scopes creates new `err` variables; use `=` where appropriate
- **Named return values:** only use when they genuinely aid clarity; they cause subtle bugs with `defer`

## Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| `gofmt` / `goimports` | Formatting | `goimports -w .` |
| `golangci-lint` | Linting | `golangci-lint run` |
| `go test` | Testing | `go test ./... -race` |
| `govulncheck` | Security audit | `govulncheck ./...` |
| `go tool pprof` | Profiling | — |
| `go vet` | Static analysis | `go vet ./...` |
