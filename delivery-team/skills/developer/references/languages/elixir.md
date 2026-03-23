# Elixir Best Practices

Version baseline: Elixir 1.16+ / OTP 26+

---

## Style & Formatting

- Use `mix format` (built-in formatter). Configure in `.formatter.exs`.
- 2-space indentation. No tabs.
- One module per file. Module name matches directory structure: `lib/my_app/accounts/user.ex` -> `MyApp.Accounts.User`.
- Organize by context (Phoenix conventions): `accounts/`, `billing/`, `notifications/`.
- Pipes start on a new line when chaining more than two operations.
- Use `@moduledoc` and `@doc` on every public function. Use `@doc false` to explicitly hide helpers.
- Credo for additional linting: `mix credo --strict`.

## Idioms & Patterns

### Pattern Matching
- Match in function heads instead of conditional logic inside function bodies.
- Multi-clause functions: order from most specific to most general.
- Pin operator `^` to match against existing bindings.
- Destructure maps, tuples, and structs directly in function signatures.
  ```elixir
  def process(%User{role: :admin} = user), do: grant_all(user)
  def process(%User{} = user), do: grant_basic(user)
  ```

### Pipe Operator
- Use `|>` for sequential data transformations. First argument flows through.
- Start the pipeline with a raw value or variable, not a function call.
- Each step should be a single, clear transformation.
- Avoid single-pipe expressions (`x |> f()` is less clear than `f(x)`).
- Use `then/1` for inline anonymous functions in pipelines.

### OTP Patterns
- **GenServer**: stateful processes. Keep state minimal; derive data instead of caching.
- **Supervisor**: define supervision trees in `application.ex`. Use `one_for_one` unless processes are coupled.
- **DynamicSupervisor**: for runtime-spawned children (e.g., per-user workers).
- **Registry**: named process lookup without global atoms.
- **Task / Task.Supervisor**: short-lived async work. Use `Task.async_stream` for bounded concurrency.
- Let processes crash and restart. Do not defend against every failure inside a process.
- Separate state ownership from business logic: GenServer handles state, pure functions handle logic.

### Processes and Message Passing
- Prefer `GenServer.call/2` (sync) for queries, `GenServer.cast/2` (async) for commands.
- Keep messages small; pass references (IDs, keys) rather than large data.
- Use `Process.monitor/1` or `Process.link/1` to detect failures.
- Avoid long message queues; apply backpressure via `GenStage` or manual flow control.

### Phoenix Conventions
- Thin controllers: validate params, delegate to context modules.
- Context modules (`Accounts`, `Billing`) encapsulate business logic and Ecto queries.
- Use changesets for all data validation, even for non-database operations.
- LiveView: keep `assign` calls in `mount/3` and `handle_event/3`. Minimize assigns.
- Use `live_session` for shared auth checks across LiveView routes.

### Ecto
- Define changesets on the schema module. Separate `create_changeset` from `update_changeset`.
- Use `Ecto.Multi` for transactional operations spanning multiple changesets.
- Composable queries: build queries with functions that accept and return `Ecto.Query`.
  ```elixir
  def active(query \\ User), do: where(query, [u], u.active == true)
  def by_role(query, role), do: where(query, [u], u.role == ^role)
  ```
- Preload associations explicitly; never rely on lazy loading (it does not exist in Ecto).
- Use database constraints (`unique_constraint`, `foreign_key_constraint`) alongside validations.

## Error Handling

- Use `{:ok, result}` / `{:error, reason}` tuples for expected failures.
- Use `with` for chaining multiple `{:ok, _}` results; handle errors in the `else` clause.
- Raise exceptions (`raise`, `throw`) only for truly unexpected programmer errors.
- Bang functions (`!`) are for cases where failure is a bug, not a normal condition.
- Define custom exception modules for domain-specific errors: `defexception message: "..."`.
- In Phoenix, use `action_fallback` to centralize error rendering.
- In OTP processes, let it crash. The supervisor handles recovery.

## Testing

- **ExUnit**: built-in test framework. Use `describe` blocks to group related tests.
- `setup` and `setup_all` for fixtures. Prefer `setup` for test isolation.
- Use `Ecto.Adapters.SQL.Sandbox` for concurrent database tests.
- Mocking: use `Mox` for behavior-based mocks. Define behaviours (`@callback`) for external dependencies.
- Avoid mocking internal modules; test through the public API of context modules.
- Property-based testing with `StreamData`.
- Use `assert_receive` / `refute_receive` for testing message-passing processes.
- Use tags (`@tag :integration`) to separate fast unit tests from slow integration tests.
- DocTests (`## Examples` in `@doc`) serve as both documentation and tests.

## Security

- Validate and cast all external input through Ecto changesets or custom validation.
- Use parameterized queries exclusively; Ecto prevents SQL injection by default.
- Hash passwords with `Bcrypt` (via `bcrypt_elixir` or `Argon2` via `argon2_elixir`).
- Store secrets in runtime config (`config/runtime.exs`) reading from environment variables.
- Enable CSRF protection in Phoenix (enabled by default). Do not disable for HTML forms.
- Use `Plug.SSL` to enforce HTTPS in production.
- Rate-limit with `Hammer` or similar. Apply at plug level for API endpoints.

## Performance

- Profile with `:observer.start()`, `:recon`, or `Benchee` before optimizing.
- Use ETS tables for read-heavy shared state across processes.
- Stream large datasets with `Stream` module to avoid loading everything into memory.
- Binary pattern matching for parsing protocols and file formats (zero-copy).
- Pool database connections with `DBConnection` (Ecto default).
- Use `Task.async_stream` with `max_concurrency` for bounded parallel work.
- Avoid atoms from user input (atoms are not garbage collected).
- For CPU-bound work, consider NIFs (Rust via Rustler) or Ports.

## Anti-Patterns to Avoid

- **God GenServers**: processes doing too much. Split into focused processes.
- **Overusing GenServer**: not everything needs a process. Pure functions in modules are fine.
- **Atom exhaustion**: never convert user input to atoms (`String.to_atom/1`). Use `String.to_existing_atom/1` only when safe.
- **Ignoring OTP principles**: do not build custom retry/restart logic; use supervisors.
- **Fat controllers**: business logic belongs in context modules, not controllers.
- **Deeply nested `case`/`cond`**: refactor into multi-clause functions or `with` chains.
- **Shared mutable state without a process**: there is no mutable state outside processes and ETS.
- **Skipping dialyzer**: add `@spec` to public functions. Run `mix dialyzer` in CI.
- **Premature NIFs**: NIFs crash the entire VM on failure. Exhaust pure Elixir options first.

## Tooling

- **Build**: `mix` (compile, test, deps, release, format).
- **Formatter**: `mix format` (built-in, opinionated, zero-config).
- **Linter**: Credo (`mix credo --strict`).
- **Type checking**: Dialyzer via `dialyxir` (`mix dialyzer`). Add `@spec` annotations.
- **REPL**: `iex -S mix` for interactive exploration with project context.
- **Releases**: `mix release` for self-contained deployments. Use `config/runtime.exs` for env-specific config.
- **Documentation**: `ex_doc` (`mix docs`). Publish to HexDocs.
- **Dependency management**: Hex (`mix hex.info <package>`).
- **Debugging**: `IO.inspect/2` with labels, `dbg/2` (Elixir 1.14+), `:debugger` for breakpoints.
- **Observability**: Telemetry library for metrics; Logger for structured logging.
