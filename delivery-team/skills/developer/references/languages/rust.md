# Rust Best Practices

Version baseline: Rust 2021 edition

## Style & Formatting

- Run `rustfmt` on all code — no exceptions; CI should fail without it
- Use `clippy` for lints: `cargo clippy -- -D warnings` (deny warnings)
- Use `snake_case` for variables, functions, modules, crates; `PascalCase` for types, traits, enums; `UPPER_SNAKE_CASE` for constants and statics
- Keep functions short and focused; Rust's ownership system rewards small, composable functions
- Organize with modules; expose minimal public API

## Idioms & Patterns

- Use `Result<T, E>` for recoverable errors; `Option<T>` for optional values — never return sentinel values like `-1` or `null`
- Use the `?` operator to propagate errors; avoid deeply nested `match` on `Result`
- Prefer owned types in function signatures when in doubt; refine to borrowing when profiling shows it matters
- Use `impl Trait` in function signatures for flexibility; use concrete types in struct fields
- Use `derive` macros for common traits: `Debug`, `Clone`, `PartialEq`, `Serialize`, `Deserialize`
- Use iterators and adaptors (`map`, `filter`, `fold`, `collect`) over manual loops where possible
- Use `Arc<Mutex<T>>` for shared mutable state across threads; prefer message passing (`std::sync::mpsc`) when it fits
- Use `tokio` or `async-std` for async runtimes; `tokio` is the de facto standard for server applications

## Error Handling

- Never use `unwrap()` or `expect()` in production code — use `?` or explicit error handling
- Use `expect()` in tests and examples with a descriptive message explaining the invariant
- Use `thiserror` for library error types (derive-based, implements `std::error::Error`)
- Use `anyhow` for application error types (context-rich, easy propagation)
- Do not mix `thiserror` and `anyhow` in the same crate — `thiserror` for libraries, `anyhow` for binaries
- Provide context when propagating errors: `context("failed to open config file")`

## Testing

- Use `cargo test` with built-in test framework for unit tests
- Place unit tests in `#[cfg(test)] mod tests { ... }` in the same file as the code
- Place integration tests in the `tests/` directory at the crate root
- Use `#[should_panic(expected = "...")]` for tests that must panic
- Use `proptest` or `quickcheck` for property-based testing of core logic
- Use `mockall` for mock generation when testing traits
- Benchmark with `criterion` for performance-critical code

## Security

- Avoid `unsafe` unless absolutely necessary; justify every `unsafe` block with a comment explaining the invariant being upheld
- Audit `unsafe` code in dependencies: `cargo-geiger` counts unsafe usage
- Do not use `std::mem::transmute` without a proven safety argument
- Validate all untrusted input at the boundary before processing
- Use `secrecy` crate for sensitive values to prevent accidental logging
- Keep dependencies minimal; run `cargo audit` in CI to check for known vulnerabilities
- Do not store secrets in source code; use environment variables or secret managers

## Performance

- Profile with `perf`, `cargo flamegraph`, or `samply` before optimizing
- Use `cargo bench` with `criterion` to measure performance changes
- Prefer stack allocation; use `Box<T>` only when heap is needed
- Use `Cow<'a, T>` to avoid unnecessary cloning in mixed owned/borrowed scenarios
- Avoid excessive cloning in hot paths — use references or `Arc` for shared data
- Use `#[inline]` on small, frequently-called functions; trust the compiler for the rest
- Use `rayon` for data-parallel workloads — straightforward parallelism without unsafe

## Anti-Patterns to Avoid

- **`unwrap()` / `expect()` in production:** program will panic; use `?` instead
- **Cloning to avoid borrow checker:** usually indicates a design problem; reconsider ownership
- **`unsafe` for convenience:** Rust's whole value proposition is safety; justify it rigorously
- **Global mutable state (`static mut`):** use `once_cell::sync::Lazy<Mutex<T>>` or `tokio::sync`
- **Recursive async functions without boxing:** causes infinite type sizes; use `Box::pin`
- **`String` where `&str` suffices:** accept `&str` in function parameters; return `String` from constructors
- **Ignoring `clippy` warnings:** `clippy` lints encode Rust idioms; fix them

## Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| `rustfmt` | Formatting | `cargo fmt` |
| `clippy` | Linting | `cargo clippy -- -D warnings` |
| `cargo test` | Testing | `cargo test` |
| `cargo audit` | Security audit | `cargo audit` |
| `cargo-geiger` | Unsafe usage audit | `cargo geiger` |
| `criterion` | Benchmarking | `cargo bench` |
