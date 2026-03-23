# Haskell Best Practices

Version baseline: GHC 9.6+ / Haskell2010

---

## Style & Formatting

- Use **Ormolu** or **fourmolu** as the canonical formatter. Integrate into CI.
- 2-space or 4-space indentation (pick one per project, enforce with formatter).
- Use explicit export lists on all modules: `module Foo (bar, baz) where`.
- Organize imports: qualified imports for external libraries, unqualified for base/prelude.
- Prefer `qualified` imports with short aliases: `import qualified Data.Map.Strict as Map`.
- One data type declaration per module for large types; group small related types.
- Use Haddock comments (`-- |` and `-- ^`) on all exported functions and types.

## Idioms & Patterns

### Algebraic Data Types
- Model domain states with sum types. Make illegal states unrepresentable.
  ```haskell
  data PaymentStatus = Pending | Charged Amount | Refunded Amount | Failed Text
  ```
- Use `newtype` for zero-cost wrappers with distinct type identity: `newtype UserId = UserId Int`.
- Use `data` for types with multiple fields or constructors.
- Records: use `{-# LANGUAGE DuplicateRecordFields #-}` or prefix fields with type abbreviation.

### Pattern Matching
- Prefer pattern matching over accessor functions for sum types.
- Use `case` expressions or function clause matching; avoid partial functions (`head`, `tail`, `fromJust`).
- Enable `-Wincomplete-patterns` (on by default with `-Wall`).
- Use `@` for as-patterns when you need both the whole and parts: `f xs@(x:_) = ...`.

### Monads and Effects
- **IO**: only at the edges. Keep core logic pure; pass results into IO at `main`.
- **Maybe**: absence of value. Use `maybe` for defaults, `>>=` for chaining.
- **Either**: error handling with context. Left is error, Right is success.
- **Reader**: implicit configuration/environment. Use `asks` to extract fields.
- **State**: threaded mutable state in pure code. Prefer `StateT` over `IORef` when possible.
- **ExceptT / Either**: stack with `ReaderT` for app monad: `type App a = ReaderT Config (ExceptT AppError IO) a`.
- Use `mtl`-style type classes (`MonadReader`, `MonadError`) for polymorphic effect constraints.

### Do Notation
- Use `do` for sequential monadic operations. Avoid single-line `do` blocks.
- Prefer `>>=` and `<$>` / `<*>` for short expressions; `do` for multi-step sequences.
- Use `let` (not `let ... in`) inside `do` blocks for pure bindings.
- `pure` over `return` (more general, works with `Applicative`).

### Computation Patterns
- Applicative (`<$>`, `<*>`) when computations are independent. Prefer over Monad when possible.
- Traversable (`traverse`, `mapM`) for effectful mapping over structures.
- Foldable (`foldl'`, `foldr`) for reducing. Always use strict `foldl'` from `Data.List`.
- `Bifunctor` for mapping over `Either` and tuples: `bimap`, `first`, `second`.

### Module Organization
- `Internal` modules for implementation details; re-export public API from parent module.
- Separate pure logic from effectful code into different modules.
- `Types.hs` for shared data types within a package.
- Keep `Main.hs` minimal: parse args, build config, call library entry point.

## Error Handling

- Use `Either AppError a` for recoverable errors. Define `AppError` as a sum type.
- Use `ExceptT` for monadic error chaining in effectful code.
- Exceptions (from `Control.Exception`) only for truly exceptional, unrecoverable conditions.
- Never throw exceptions in pure code. Use `error` only for programmer bugs (unreachable branches).
- Catch exceptions at the boundary (e.g., `main`, HTTP handler), convert to `Either`.
- Avoid partial functions: use safe alternatives (`headMay`, `readMaybe`, pattern matching).
- Use `MonadError` constraint for generic error-handling code.

## Testing

- **HSpec**: BDD-style tests. `describe`, `it`, `shouldBe`, `shouldThrow`.
- **QuickCheck**: property-based testing. Define `Arbitrary` instances for domain types.
- **Hedgehog**: alternative property testing with integrated shrinking.
- **Tasty**: test runner combining HSpec, QuickCheck, HUnit under one framework.
- Test pure functions directly -- no setup/teardown needed.
- For IO-heavy code, use type class constraints and provide pure test implementations.
- Golden tests for output-sensitive code (parsing, rendering).
- Aim for property tests on core logic, unit tests on edge cases and integration points.

## Security

- Use `text` and `bytestring` for string handling; avoid `String` (linked list of chars).
- Validate all external input at parsing boundaries; use smart constructors.
- Use `crypton` or `cryptonite` for cryptographic operations.
- Parameterize database queries (use `postgresql-simple` with `Query` and `?` placeholders).
- Avoid `unsafePerformIO` except for top-level `IORef`/`MVar` initialization.
- Use `Safe Haskell` pragma for security-critical modules where appropriate.
- Secrets: read from environment variables via `System.Environment.lookupEnv`.

## Performance

### Strictness
- Enable `-O2` for production builds.
- Use strict data fields by default: `data Foo = Foo !Int !Text`.
- Use `BangPatterns` in performance-critical function arguments.
- `Data.Map.Strict` and `Data.HashMap.Strict` over lazy variants.
- Strict `foldl'` over lazy `foldl`. Never use lazy `foldl` on large lists.

### Data Structures
- `Text` over `String` always. `ByteString` for binary data.
- `Vector` for indexed access; `Seq` for efficient append-both-ends.
- `IntMap` / `HashMap` for high-performance lookups.
- Unboxed vectors (`Data.Vector.Unboxed`) for numeric arrays.

### Profiling
- Compile with `-prof -fprof-auto`. Run with `+RTS -p` for time profiling.
- Heap profiling: `+RTS -hc` (by cost center) or `+RTS -hy` (by type).
- Use `criterion` or `tasty-bench` for micro-benchmarks.
- Watch for space leaks: lazy thunks accumulating unevaluated expressions.

### Laziness Pitfalls
- Lazy evaluation is the default. This causes space leaks if unevaluated thunks accumulate.
- Use `seq`, `deepseq`, or `BangPatterns` to force evaluation where needed.
- Streaming I/O: use `conduit` or `streaming` instead of lazy I/O (`hGetContents`).

## Anti-Patterns to Avoid

- **String for text processing**: use `Text` or `ByteString`. `String = [Char]` is extremely slow.
- **Partial functions**: `head`, `tail`, `fromJust`, `read` crash on invalid input. Use safe alternatives.
- **Lazy I/O**: `hGetContents` and `readFile` cause unpredictable resource management. Use strict I/O or streaming.
- **Orphan instances**: type class instances defined outside the module of either the class or the type. Causes coherence issues.
- **Overly polymorphic code**: concrete types are easier to debug and read. Generalize only when reuse demands it.
- **Deep monad transformer stacks**: more than 3-4 layers become unwieldy. Consider effect systems (Polysemy, Effectful) or `ReaderT IO` pattern.
- **Ignoring `-Wall` warnings**: enable `-Wall -Werror` in CI.
- **Premature optimization with unsafePerformIO**: breaks referential transparency. Almost never needed.

## Tooling

- **Build**: `cabal build` (cabal-install 3.10+) or `stack build`. Cabal is now the recommended default.
- **Formatter**: Ormolu or fourmolu (integrate with CI).
- **Linter**: HLint (`hlint src/`). Apply suggestions selectively.
- **IDE**: HLS (Haskell Language Server) with VS Code or Neovim.
- **REPL**: `cabal repl` or `ghci` for interactive exploration.
- **Documentation**: Haddock (`cabal haddock`).
- **Dependency management**: Hackage (packages), Stackage (curated snapshots).
- **Common extensions** (enable per-file or in `.cabal`):
  - `OverloadedStrings` -- string literals as `Text`/`ByteString`
  - `DerivingStrategies` -- explicit `stock`, `newtype`, `anyclass`, `via`
  - `TypeApplications` -- `read @Int "42"`
  - `LambdaCase` -- `\case` syntax
  - `RecordWildCards` -- destructure records concisely
  - `ScopedTypeVariables` -- bring type variables into scope
  - `StrictData` -- strict fields by default per module
