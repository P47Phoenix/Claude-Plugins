# Developer

**Invocation**: `delivery-team:developer`

Developer agent for writing, reviewing, and refactoring code. Auto-detects the programming language and loads only the relevant best-practices reference.

## Supported Languages

| Language | Extensions | Reference |
|----------|-----------|-----------|
| Python | `.py` | Python 3.10+ best practices |
| TypeScript | `.ts`, `.tsx` | TypeScript 5.x best practices |
| JavaScript | `.js`, `.mjs`, `.cjs` | ES2022+ best practices |
| C# | `.cs` | C# 12 / .NET 8 best practices |
| Go | `.go` | Go 1.21+ best practices |
| Rust | `.rs` | Rust 2021 edition best practices |
| Java | `.java` | Java 17 LTS best practices |
| SQL | `.sql` | SQL / PostgreSQL best practices |
| Bash | `.sh`, `.bash` | Bash 5+ best practices |
| R | `.r`, `.R`, `.Rmd` | R 4.x (tidyverse, testthat, renv) |
| F# | `.fs`, `.fsx` | F# 8 / .NET 8 |
| Elixir | `.ex`, `.exs` | Elixir 1.16+ / OTP 26+ |
| Haskell | `.hs`, `.lhs` | GHC 9.6+ |
| Scala | `.scala`, `.sc` | Scala 3.3+ |

## How to Trigger

- "write code", "implement", "fix this bug", "refactor", "add tests", "code review"
- Any mention of a file with a supported extension
- "write a function", "build a script"

## Task Types

| Type | What It Does |
|------|-------------|
| **write** | Implement from scratch following all language conventions |
| **fix** | Identify root cause, patch, explain what was wrong |
| **refactor** | Improve structure and naming without changing behavior |
| **review** | Audit against language reference and clean code checklist |
| **test** | Write tests using idiomatic test framework |
| **explain** | Walk through code with annotations |
| **coding-standards** | Generate customizable coding standards template |

## Cross-Language References

Additional references load automatically based on context:

| Pattern | Loaded When | Languages |
|---------|-------------|-----------|
| **OOP Patterns** | SOLID, design patterns, DI mentioned | C#, TypeScript, Java, Python, Kotlin |
| **FP Patterns** | Pure functions, immutability, monads mentioned | F#, Elixir, Haskell, Scala, TypeScript, Python, R |
| **Frontend Patterns** | Component, CSS, state management mentioned | TypeScript, JavaScript |
| **Nx Monorepo** | `nx.json` detected or Nx mentioned | Any |

### Paradigm Configuration

Set default paradigm in config:

```yaml
tech_stack:
  paradigm: auto  # auto, oop, fp, hybrid
  paradigm_by_language:
    python: oop
    typescript: fp
    scala: hybrid
```

## Clean Code Standards

A foundational clean code guide loads on **every** task, for **every** language. It covers: meaningful names, functions, comments, formatting, error handling, boundaries, unit tests, classes, emergent design, and code smells.

For `review` tasks, a condensed pass/fail checklist is also loaded with enforcement:

- **block** (default): Violations prevent approval
- **warn**: Violations produce warnings but do not block

### Custom Standards

Generate a customizable standards template:

```
User: "generate coding standards"
```

This creates `.delivery/standards/coding-standards.md` with all 10 sections and placeholder comments for team customization. Activate it in config:

```yaml
tech_stack:
  clean_code_guide: .delivery/standards/coding-standards.md
```

## Example Usage

```
User: "Write a Python function to validate email addresses"

Language: Python | Task: write | Reference: references/languages/python.md
Clean Code: default

Output: Complete Python function with type hints, docstring,
        edge case handling, and test suggestions
```

## Pipeline Integration

When invoked outside the delivery pipeline, the developer skill warns:

!!! warning
    No delivery pipeline config found. QA evaluator-optimizer loop, DoD validation, and defect prevention will NOT run. Start with `delivery-team:delivery-flow` first, or say "skip pipeline" to proceed.
