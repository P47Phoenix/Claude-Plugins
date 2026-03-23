# Functional Programming Patterns

Cross-language functional programming reference. Load alongside the language reference when FP patterns are relevant.

Applicable languages: F#, Elixir, Haskell, Scala, TypeScript, JavaScript, Python, R

---

## Pure Functions and Referential Transparency

A pure function always returns the same output for the same input and produces no side effects (no I/O, no mutation, no global state changes).

**Benefits**: testable without mocks, safe to compose, safe to parallelize, easy to reason about.

**Pure vs impure**:
- Pure: `fun add(a, b) -> a + b` -- deterministic, no side effects.
- Impure: reads a database, writes to a file, accesses current time, generates random numbers.

**Practical rule**: push impure operations to the edges of your system. Core business logic should be pure functions that receive data and return results. The outer shell handles I/O, then calls pure core functions.

## Immutability

Prefer immutable data structures. Mutation is the primary source of bugs in concurrent and complex systems.

**Persistent data structures** use structural sharing to create "modified" copies efficiently without cloning everything. Supported natively in Haskell, F#, Elixir, Scala, Clojure. In JS/TS, use Immer or manual spread syntax.

**When mutation is acceptable**:
- Localized mutation inside a function (invisible to callers)
- Performance-critical inner loops after profiling proves the need
- Builder patterns that produce an immutable result

**Language-specific immutability defaults**:
- Haskell, Elixir, Erlang: immutable by default, no escape hatch at language level
- F#: `let` bindings immutable, `mutable` keyword opts in
- Scala: `val` (immutable) vs `var` (mutable); prefer `val`
- Rust: `let` immutable, `let mut` opts in
- JS/TS: `const` prevents rebinding (not deep immutability); use `Object.freeze` or Immer
- Python: no enforcement; convention and discipline only

## Higher-Order Functions

Functions that take functions as arguments or return functions.

**Core trio** -- prefer these over manual loops:
- `map`: transform each element. `[1,2,3].map(x => x * 2)` -> `[2,4,6]`
- `filter`: select elements. `[1,2,3].filter(x => x > 1)` -> `[2,3]`
- `reduce`/`fold`: accumulate into a single value. `[1,2,3].reduce((a,b) => a+b, 0)` -> `6`

**Additional patterns**:
- `flatMap`/`bind`/`>>=`: map then flatten. Essential for monadic chaining.
- `zip`: combine two sequences pairwise.
- `partition`: split into two groups by predicate.
- `tap`/`inspect`: side-effect observation without modifying the pipeline.
- `compose`/`pipe`: combine functions into a new function.

## Pattern Matching and Algebraic Data Types

### Sum Types (Tagged Unions)
Types with multiple variants, each potentially carrying different data.
- F#: `type Shape = Circle of float | Rect of float * float`
- Rust: `enum Shape { Circle(f64), Rect(f64, f64) }`
- Scala: `sealed trait Shape` with case classes
- Haskell: `data Shape = Circle Double | Rect Double Double`
- Elixir: tagged tuples `{:circle, radius}` or structs
- TS: discriminated unions with `type` field

### Product Types
Types combining multiple values (tuples, records, structs). All fields present in every value.

### Exhaustive Matching
The compiler (or runtime in dynamic languages) verifies all variants are handled. This is the key safety benefit of ADTs over plain conditionals.

**When to use pattern matching vs alternatives**:
- Pattern matching: data transformation, parsing, state machines, protocol handling
- Polymorphism (method dispatch): when behavior varies by type and new types are added frequently
- If/else: simple boolean conditions with no structural decomposition

## Option/Maybe and Result/Either

### Eliminating Null
Wrap potentially absent values in an Option/Maybe type instead of using null/nil.

| Language | Option type | None variant |
|----------|-------------|-------------|
| F# | `Option<'T>` | `None` |
| Rust | `Option<T>` | `None` |
| Scala | `Option[A]` | `None` |
| Haskell | `Maybe a` | `Nothing` |
| Elixir | `nil` (convention: `{:ok, v}` / `nil`) | `nil` |
| TS/JS | fp-ts `Option`, neverthrow | `none` |

### Result/Either for Errors
Encode success or failure in the type system. Chain operations with `map`/`flatMap`.

| Language | Success | Failure |
|----------|---------|---------|
| F# | `Ok value` | `Error err` |
| Rust | `Ok(value)` | `Err(err)` |
| Scala | `Right(value)` | `Left(err)` |
| Haskell | `Right value` | `Left err` |
| Elixir | `{:ok, value}` | `{:error, reason}` |
| TS/JS | neverthrow `ok(v)` | neverthrow `err(e)` |

**Railway-oriented programming**: chain `Result`-returning functions. On first error, skip remaining steps and propagate the error. Implemented via `bind`/`flatMap`/`and_then`.

## Function Composition and Piping

### Pipe Operator
Left-to-right data flow. Read top-to-bottom.
- Elixir: `data |> transform1() |> transform2()`
- F#: `data |> transform1 |> transform2`
- JS (proposed): `data |> transform1(%) |> transform2(%)`
- Haskell: `transform2 . transform1 $ data` (right-to-left with `.`), or `data & transform1 & transform2`

### Point-Free Style
Defining functions without naming their arguments: `let increment = List.map ((+) 1)`.
Use when it is clearer than the explicit version. Abandon when it becomes a puzzle.

## Currying and Partial Application

**Currying**: transforming a multi-argument function into a chain of single-argument functions.
- Auto-curried: Haskell, F# (all functions are curried by default).
- Manual: JS/TS (`const add = a => b => a + b`), Python (`functools.partial`).

**Practical uses**:
- Pre-configuring dependencies: `const fetchWithAuth = fetch(authToken)`.
- Specializing generic functions: `let doubleAll = List.map ((*) 2)`.
- Event handlers: `onClick={handleClick(itemId)}`.

**When it hurts**: deeply curried functions with many similar-typed arguments obscure meaning. Use named parameters or objects instead.

## Recursion Patterns

**Tail recursion**: the recursive call is the last operation. Optimized to a loop by the compiler (Haskell, F#, Scala with `@tailrec`, Elixir/Erlang, Rust -- but not JS/TS without explicit trampolining).

**Fold as recursion abstraction**: most recursive list processing can be expressed as `fold`/`reduce`. Prefer folds over manual recursion for clarity.

**Trampolining**: for languages without TCO (JavaScript), wrap recursive calls in thunks and iterate. Libraries: `trampoline` pattern or `fp-ts` Trampoline.

**Recursive data structures**: trees, linked lists, nested JSON. Process with pattern matching and recursive functions, or use fold/catamorphism.

## Type-Driven Development

### Making Illegal States Unrepresentable
Design types so invalid combinations cannot be constructed.

Instead of:
```
type User = { name: string, email: string | null, isVerified: boolean }
// Bug: isVerified = true but email = null
```
Use:
```
type User = Unverified of { name, email } | Verified of { name, email, verifiedAt }
```

### Smart Constructors
Private data constructor + public factory function that validates invariants.
```fsharp
type EmailAddress = private EmailAddress of string
let createEmail s = if isValid s then Ok (EmailAddress s) else Error "invalid"
```

### Phantom Types and Newtype
- Phantom types: type parameters used for compile-time tagging, not runtime data.
- Newtype: zero-cost wrapper distinguishing otherwise identical types (`UserId` vs `OrderId`, both `Int`).

## Effect Systems

**The problem**: tracking which functions do I/O, throw errors, or access state.

**Approaches by language**:
- Haskell: `IO` monad separates pure from effectful. Advanced: Polysemy, Effectful for fine-grained effects.
- Scala: Cats Effect `IO`, ZIO with typed errors and environment.
- F#: Computation expressions (`task { }`, `result { }`, `async { }`).
- Elixir/Rust/TS: no formal effect system. Use `Result` types and explicit error channels.

**Practical advice**: you do not need a full effect system in most languages. `Result` types for errors and clear separation of pure/impure code cover 90% of the benefit.

## Lazy Evaluation

**Lazy by default**: Haskell. All values are evaluated only when needed.
**Lazy on demand**: Scala `LazyList`, F# `seq { }`, JS generators, Python generators, Rust iterators.

**Benefits**: work with infinite sequences, avoid computing unused values, compose pipelines without intermediate collections.

**Pitfalls**:
- Space leaks: unevaluated thunks accumulate in memory (Haskell).
- Debugging difficulty: evaluation order is non-obvious.
- Performance: lazy overhead in hot loops (use strict alternatives).

## When to Use FP vs OOP

| Scenario | Recommended approach |
|----------|---------------------|
| Data transformation pipelines | FP: map/filter/reduce chains |
| Complex domain with many entity types | OOP: objects with identity and behavior |
| Event processing, parsing, validation | FP: pattern matching, Result types |
| GUI/game entities with mutable state | OOP: encapsulated state with methods |
| Concurrency and parallelism | FP: immutable data eliminates shared-state bugs |
| API request/response handling | FP: transform input to output through a pipeline |
| Large team with mixed experience | Hybrid: FP for data flow, classes for domain modeling |

Most production codebases benefit from a hybrid approach. Use FP for data flow and transformations. Use OOP (or modules with encapsulated state) for domain entities that have identity and lifecycle.

## Anti-Patterns

- **Impure functions pretending to be pure**: functions that read global state, perform I/O, or depend on mutable references without declaring it. Makes code unpredictable and untestable.
- **Forcing Haskell patterns into Python/JS**: monadic chaining, custom functor types, and category theory abstractions add complexity without benefit in languages not designed for them.
- **Premature abstraction**: introducing type classes, monads, or effect systems before the codebase has enough complexity to justify them. Start concrete, generalize when you see duplication.
- **Ignoring language idioms**: write idiomatic code for your language. Elixir has its own patterns distinct from Haskell; Rust is not Scala. Adapt the FP principles to your ecosystem.
- **Deep composition chains**: `compose(f, g, h, i, j, k)` is unreadable. Break into named intermediate steps with descriptive variable names.
- **Monad tutorial fallacy**: understanding monads through analogies (burritos, boxes) instead of using them. Learn by writing code with `Maybe`/`Result`/`IO`, not by reading metaphors.
- **Purity at all costs**: sometimes a well-scoped mutable variable is clearer than threading state through six function parameters. Pragmatism over dogma.
