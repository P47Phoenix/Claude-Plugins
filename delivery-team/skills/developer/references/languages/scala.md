# Scala Best Practices

Version baseline: Scala 3.3+ (Scala 2.13 differences noted where critical)

---

## Style & Formatting

- Use **Scalafmt** as the canonical formatter. Configure in `.scalafmt.conf`.
- 2-space indentation. Max line length 100-120 characters.
- Scala 3 uses significant indentation (optional braces). Choose braces or indentation per project and be consistent.
- Package structure mirrors directory structure: `src/main/scala/com/example/accounts/User.scala`.
- Use `given`/`using` (Scala 3) instead of `implicit` (Scala 2). Migrate incrementally.
- ScalaDoc (`/** ... */`) on all public types and methods.
- Prefer `val` over `var`. Use `var` only when mutability is truly required.

## Idioms & Patterns

### Case Classes and Sealed Traits
- Use case classes for immutable value objects. They provide `equals`, `hashCode`, `copy`, and pattern matching.
- Sealed traits for sum types (ADTs). The compiler enforces exhaustive matching.
  ```scala
  sealed trait PaymentResult
  case class Success(transactionId: String) extends PaymentResult
  case class Failure(reason: String, retryable: Boolean) extends PaymentResult
  ```
- Scala 3: prefer `enum` for simple ADTs:
  ```scala
  enum Color:
    case Red, Green, Blue
  enum Shape:
    case Circle(radius: Double)
    case Rectangle(width: Double, height: Double)
  ```

### Pattern Matching
- Match on sealed types for exhaustive checks. The compiler warns on missing cases.
- Use guards sparingly: `case x if x > 0 =>`.
- Extract patterns into named extractors (`unapply`) for reuse.
- Avoid catch-all `case _ =>` unless you genuinely handle all remaining cases.
- Scala 3 `match` types for type-level programming (advanced use only).

### Given/Using (Implicits in Scala 2)
- `given` instances provide type class implementations and contextual values.
- `using` clauses declare contextual parameters.
- Scala 2: `implicit val`, `implicit def`, `implicit class`. Migrate to Scala 3 syntax.
- Place `given` instances in companion objects for automatic resolution.
- Avoid implicit conversions. Use extension methods instead.
- Limit implicit scope: too many implicits cause slow compilation and confusing errors.

### Extension Methods
- Scala 3: `extension (s: String) def words: List[String] = s.split(" ").toList`.
- Scala 2: `implicit class StringOps(s: String) { def words: List[String] = ... }`.
- Use for adding domain methods to third-party types. Do not overuse.

### For-Comprehensions
- Syntactic sugar for `flatMap`/`map`/`withFilter` chains.
- Use for chaining `Option`, `Either`, `Try`, `Future`, or any monad.
  ```scala
  for
    user  <- findUser(id)
    order <- findOrder(user.orderId)
    item  <- findItem(order.itemId)
  yield item
  ```
- Each `<-` line is a `flatMap` except the last, which is `map`.

### Option/Either/Try
- `Option`: presence or absence. Use `map`, `flatMap`, `getOrElse`. Never use `.get`.
- `Either[E, A]`: right-biased error handling. `Left` for error, `Right` for success.
- `Try`: wraps exceptions into `Success`/`Failure`. Use at boundaries with Java code.
- Convert between them: `Try(...).toEither`, `option.toRight(error)`.

### Opaque Types (Scala 3)
- Zero-cost type wrappers: `opaque type UserId = Long`.
- Define companion with apply and extension methods for the public API.
- Replaces `extends AnyVal` (Scala 2 value classes) with fewer limitations.

## Error Handling

- Use `Either[AppError, A]` for business logic errors. Define `AppError` as a sealed trait.
- Use `Try` only at Java interop boundaries; convert to `Either` immediately.
- Exceptions for truly unexpected failures only (JVM errors, assertion violations).
- With Cats Effect / ZIO, use typed error channels rather than exceptions.
- Never catch `Throwable` or `Exception` broadly. Use `NonFatal` from `scala.util.control`.
- Accumulate validation errors with `Validated` (Cats) or `ZIO.validate`.

## Testing

- **MUnit**: lightweight, Scala-native test framework. Preferred for new projects.
- **ScalaTest**: feature-rich, multiple styles (`FunSuite`, `FlatSpec`, `WordSpec`). Most widely used.
- **Specs2**: BDD-style specifications.
- **ScalaCheck**: property-based testing. Define `Gen` and `Arbitrary` for domain types.
- Test organization: `src/test/scala/` mirrors `src/main/scala/`.
- Use `testcontainers-scala` for integration tests with databases and external services.
- Mock sparingly. Prefer dependency injection via constructor parameters or type classes.
- For effectful code (Cats Effect / ZIO), use their test runtimes.

## Security

- Validate input at API boundaries. Use refined types or opaque types for validated data.
- Parameterize all SQL queries (Doobie `sql"..."`, Slick, Quill).
- Use `scala.sys.env` or configuration libraries (pureconfig, HOCON) for secrets.
- Avoid `asInstanceOf` type casts; they bypass the type system.
- Sanitize user input before rendering in HTML (Play/http4s do this by default in templates).
- Keep dependencies updated; use `sbt-dependency-check` for vulnerability scanning.
- Use HTTPS everywhere. Configure SSL in the application server, not the application.

## Performance

- Prefer immutable collections from `scala.collection.immutable` (default).
- Use `Vector` for general-purpose indexed sequences; `List` for prepend-heavy recursive code.
- `LazyList` (was `Stream` in 2.12) for lazy sequences; watch for memory retention of head.
- Avoid `scala.collection.mutable` unless profiling shows a bottleneck.
- Use `view` for lazy intermediate transformations on collections (avoids intermediate allocations).
- JMH (`sbt-jmh`) for micro-benchmarks. Never trust wall-clock timing.
- Enable `-opt:l:inline` for production builds (method-level inlining).
- ZIO/Cats Effect fiber-based concurrency scales better than thread-per-request.
- Profile with JVisualVM, async-profiler, or YourKit.

## Anti-Patterns to Avoid

- **`.get` on Option/Try/Either**: throws exceptions, defeating the purpose. Use `getOrElse`, `fold`, or pattern match.
- **Wildcard imports of implicits**: `import com.lib._` pulls in unexpected implicit conversions. Import specifically.
- **Implicit conversions**: use extension methods instead. Conversions hide type mismatches.
- **Mutable state shared between threads**: use `Ref` (Cats Effect / ZIO), `AtomicReference`, or actors.
- **Blocking on `Future`**: never `Await.result` in production code. Compose with `map`/`flatMap`.
- **Over-engineering with type-level programming**: keep it practical. Fancy types that no one can read are a liability.
- **Mixing Scala 2 and Scala 3 syntax**: pick one style per codebase during migration.
- **Catching `Throwable`**: catches `OutOfMemoryError` and `StackOverflowError`. Use `NonFatal`.
- **Ignoring compiler warnings**: enable `-Xfatal-warnings` in CI.

## Tooling

- **Build**: sbt (most common), Mill (faster, simpler), Gradle (for mixed Java/Scala).
- **Formatter**: Scalafmt. Configure in `.scalafmt.conf`, integrate with CI and IDE.
- **Linter**: Scalafix for automated rewrites and linting rules. WartRemover for additional checks.
- **IDE**: IntelliJ IDEA with Scala plugin (most mature) or Metals (VS Code, Neovim).
- **REPL**: `scala` CLI (Scala 3), `sbt console`, or Ammonite.
- **Documentation**: Scaladoc (`sbt doc`).
- **Dependency management**: sbt with Coursier resolver. Use `dependencyTree` to inspect transitive deps.
- **Effect libraries**:
  - Cats Effect: purely functional I/O. `IO` monad, `Resource`, fibers.
  - ZIO: typed errors, layers for dependency injection, built-in concurrency primitives.
  - Akka/Pekko: actor model for distributed systems (Pekko is the Apache fork of Akka).
- **Web frameworks**: http4s (functional), Play (full-stack), Tapir (type-safe API definitions).
- **Compile speed**: enable sbt incremental compilation, Zinc, and consider Bloop for IDE builds.
