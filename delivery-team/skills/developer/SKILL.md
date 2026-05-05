---
name: developer
description: Developer agent for writing, reviewing, and refactoring code in any language. This skill should be used when users want to write code, fix bugs, refactor existing code, add tests, or review code quality. Auto-detects the programming language and spawns a language-scoped sub-agent so only the relevant best-practices are loaded into context — never all languages at once. Triggers on phrases like "write code", "implement", "fix this bug", "refactor", "add tests", "code review", "write a function", "build a script", and on file extensions (.py, .ts, .js, .go, .rs, .cs, .java, .sql, .sh, .r, .R, .Rmd).
license: Apache License 2.0 - See repository LICENSE file
model_awareness: opus-4-7-frontmatter-only
last_audited: 2026-04-22
pattern_library_version: 4-7-1
tier: B
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---

# Developer Agent

## Design Principle: Language Context Isolation

This skill intentionally keeps language-specific knowledge **out of the main context window**. When a coding task is requested, a sub-agent is spawned carrying only the single relevant language reference. This means:

- A Python task loads only `references/languages/python.md`
- A TypeScript task loads only `references/languages/typescript.md`
- No other language files are loaded — ever

The main context receives only the finished code artifact. All language-specific reasoning happens inside the sub-agent's isolated context.

---

## Pipeline Context Check

Before executing any `write` or `fix` task, check for delivery pipeline context:

1. Check if `.delivery/config.yml` exists in the current working directory.
2. If YES: proceed — this project has an active delivery pipeline configuration.
3. If NO: announce a warning before proceeding:

> WARNING: No delivery pipeline config found. This implementation is not going through the delivery-flow pipeline. QA evaluator-optimizer loop, DoD validation, and defect prevention will NOT run. Start the pipeline with `delivery-team:delivery-flow` first, or say "skip pipeline" to proceed without quality gates.

This check does NOT block implementation — it warns. Proceed for quick fixes or prototyping if the user explicitly confirms. The warning makes bypass visible and intentional, not silent.

---

## Phase 1: Language Detection

Detect the target language from (in priority order):
1. File extension in context: `.py` → Python, `.ts` → TypeScript, `.js` → JavaScript, `.cs` → C#, `.go` → Go, `.rs` → Rust, `.java` → Java, `.sql` → SQL, `.sh`/`.bash` → Bash, `.r`/`.R`/`.Rmd`/`.qmd` → R, `.fs`/`.fsx` → F#, `.ex`/`.exs` → Elixir, `.hs`/`.lhs` → Haskell, `.scala`/`.sc` → Scala
2. Imports or syntax in pasted code
3. User's explicit statement
4. File being edited in the current session

**If language is ambiguous, ask before proceeding.** Do not assume.

**Declare before every task:**

> `Language: [LANG] | Task: [write / fix / refactor / review / test / explain / coding-standards] | Reference: references/languages/<lang>.md | Clean Code: [default | <custom-path>]`

The `Clean Code` field shows `default` when using the built-in `references/clean-code.md`, or the custom file path when `tech_stack.clean_code_guide` is set in `.delivery/config.yml`.

---

## Phase 2: Sub-Agent Invocation

**For every coding task, follow these steps exactly — do not skip:**

1. Detect the language (Phase 1)
2. Read **only** `references/languages/<detected-lang>.md` — do NOT read any other language file
3. Spawn a sub-agent using the `Agent` tool with the prompt template below
4. Return the sub-agent's output directly to the user

**Do not inline language best-practices into the main context.** The sub-agent is the execution boundary for all language-specific knowledge. This is the entire point of the architecture.

### Sub-Agent Prompt Template

```
You are an expert [LANGUAGE] developer. Apply these coding standards and best practices to everything you write:

---
[PASTE FULL CONTENTS OF references/languages/<lang>.md HERE]
---

## Clean Code Standards

[PASTE FULL CONTENTS OF clean code guide HERE]

---

[CONDITIONAL: OOP/FP/Frontend/Nx patterns inserted here by existing routing logic]

## Task

[TASK TYPE]: [DESCRIBE WHAT THE USER WANTS]

## Context

[Include any of the following that are relevant:]
- Existing code to modify or reference
- File paths in the project
- Constraints (performance, API compatibility, framework version)
- Related code or interfaces this must work with

## Output Requirements

Produce:
1. Complete, runnable code — no placeholders or TODO stubs unless explicitly asked
2. Inline comments on non-obvious logic only (do not comment obvious code)
3. A brief explanation of key decisions (3–5 sentences)
4. Test suggestions — how to verify the code works

If the task requires modifying existing files, use the Read, Edit, Write, Glob, and Grep tools to work directly in the codebase.
```

### Clean Code Guide Resolution

The clean code guide is **foundational** — it loads on EVERY developer task, for EVERY language. It is NOT in the cross-language routing table and is NOT conditional on any config value. Loading order: Language reference -> Clean code -> Conditional patterns (OOP/FP/Frontend/Nx).

**Resolution logic:**

1. Check if `.delivery/config.yml` exists and has `tech_stack.clean_code_guide` set to a non-empty string.
2. If YES and the file exists: load the custom guide file. The custom guide **REPLACES** the default — do not load both.
3. If YES but the file does NOT exist: emit a warning ("Custom clean code guide not found: {path}. Using built-in default.") and load the default `references/clean-code.md`.
4. If the key is absent, empty string, or no config exists: load the default `references/clean-code.md`.

**For `review` tasks**: also load `references/clean-code-review-checklist.md` into the prompt. Insert the checklist after the `## Clean Code Standards` block with the heading `## Clean Code Review Checklist`. Then append the enforcement instructions below based on `tech_stack.clean_code_enforcement` (default: `block`).

**Enforcement instructions to inject into the sub-agent prompt (after the checklist)**:

```
## Clean Code Enforcement

Enforcement mode: [block | warn]

Evaluate the code against EVERY item in the Clean Code Review Checklist above.
For each violation found, emit a finding in this exact format:

  [SEVERITY] [Section]: [description]
  Configure via tech_stack.clean_code_enforcement in .delivery/config.yml

Where:
- SEVERITY is VIOLATION when enforcement mode is "block", or WARNING when enforcement mode is "warn"
- Section is the checklist section name (e.g., "Functions", "Meaningful Names", "Error Handling")
- Description names the specific principle violated (e.g., "exceeds single responsibility", "swallowed exception in catch block")

After all findings, emit a result line:
- If enforcement mode is "block" and any violations exist: RESULT: BLOCKED (N violations)
- If enforcement mode is "warn": RESULT: PASSED with N warnings
- If no violations found: RESULT: PASSED
```

**For `simplify` and `refactor` tasks**: the clean code guide is already loaded (it loads on every task). Additionally, the sub-agent prompt must include this instruction after the clean code standards block:

```
Reference the clean code principles above when justifying simplification or refactoring decisions. Cite the specific section (e.g., "Functions", "Code Smells") for each change you make.
```

### Task Type Instructions for Sub-Agent

| Task Type | What the sub-agent does |
|---|---|
| **write** | Implement from scratch following all conventions in the language reference |
| **fix** | Identify the root cause, patch it, explain what was wrong and why |
| **refactor** | Improve structure, naming, and idioms without changing behavior; cite which clean code principles (by section name) and language best-practice violations were addressed |
| **review** | Audit the code against the language reference AND the clean code review checklist; produce annotated findings with severity per enforcement mode (see Clean Code Enforcement instructions above); each violation cites the specific checklist section |
| **test** | Write tests using the language's idiomatic test framework; cover happy path, edge cases, and error conditions |
| **explain** | Walk through the code with annotations; reference language idioms where relevant |
| **coding-standards** | Generate `.delivery/standards/coding-standards.md` template from the built-in clean code reference. All 10 sections with customization placeholders. Output config instruction for `tech_stack.clean_code_guide`. Check for existing file before overwriting. |

### `coding-standards` Task Type Implementation

When the task type is `coding-standards`, the sub-agent does NOT need a language reference file. Skip language detection. Use this dedicated prompt template instead of the standard sub-agent prompt:

**Pre-flight check**: Before spawning the sub-agent, check if `.delivery/standards/coding-standards.md` already exists. If it does, warn the user:

> WARNING: `.delivery/standards/coding-standards.md` already exists. Overwriting will replace your current customizations. Say "overwrite" to proceed or "cancel" to keep the existing file.

Wait for explicit confirmation before proceeding. Do not overwrite silently.

**Sub-agent prompt for `coding-standards`**:

```
You are a coding standards scaffold generator. Your job is to create a team-customizable coding standards template.

## Instructions

1. Create the directory `.delivery/standards/` if it does not exist (use Bash: `mkdir -p .delivery/standards/`).

2. Generate the file `.delivery/standards/coding-standards.md` with the following structure:

---BEGIN TEMPLATE---
# Team Coding Standards

This file defines your team's coding standards. It was generated from the built-in clean code reference and is designed to be customized for your project.

**How this integrates with the developer skill**: When you set `tech_stack.clean_code_guide: .delivery/standards/coding-standards.md` in your `.delivery/config.yml`, the developer skill will load THIS file instead of the built-in `clean-code.md` for every coding task. Your customizations will be applied automatically to all code generation, review, and refactoring.

**How to customize**: Each section below contains HTML comment placeholders. Replace the placeholder comments with your team's specific conventions. You can also modify, remove, or add to the built-in principles.

---

## Meaningful Names

- Use intention-revealing names: the name should answer why it exists, what it does, and how it is used
- Avoid abbreviations, single-letter variables (except short loop counters), and generic names like `data`, `info`, `temp`, `result`
- Use searchable names: longer, descriptive names over short cryptic ones
- Name booleans as predicates: `is_valid`, `has_access`, `can_retry`
- Avoid encoding type or scope into names (no Hungarian notation)
- Use consistent vocabulary: pick one word per concept and use it everywhere

<!-- Add your team's naming conventions here. Examples: preferred prefixes/suffixes, domain-specific terminology, naming patterns for services/repositories/handlers -->

## Functions

- Do one thing. If you can extract a meaningful sub-function, the original does too much
- Keep functions short: aim for 5-20 lines; treat 30+ lines as a refactoring signal
- Limit parameters to 3 or fewer; group related parameters into an object or struct
- Avoid flag arguments that switch behavior; split into separate functions instead
- Use descriptive verb-phrase names: `calculate_total`, `validate_input`, `send_notification`
- Minimize side effects: prefer pure functions where practical; document side effects when unavoidable
- Return early to reduce nesting; avoid deep conditional chains

<!-- Add your team's function conventions here. Examples: maximum line count, required parameter documentation, async/sync patterns -->

## Comments

- Prefer self-documenting code over comments; rename or restructure before adding a comment
- Use comments for why, never for what: explain intent, constraints, or non-obvious trade-offs
- Delete commented-out code; version control preserves history
- Keep doc comments on public APIs accurate and current
- Mark workarounds and technical debt with TODO/HACK and a reason

<!-- Add your team's comment conventions here. Examples: required doc comment format, TODO tag format, header comment requirements -->

## Formatting

- Maintain consistent indentation and brace style per project convention
- Group related code together; separate unrelated blocks with blank lines
- Keep files focused: one primary concept per file
- Order members by relevance: public API first, then private helpers
- Keep lines under the project's agreed length limit

<!-- Add your team's formatting conventions here. Examples: max line length, import ordering rules, file organization patterns -->

## Error Handling

- Prefer exceptions over error codes in languages that support them
- Catch specific errors, not catch-all handlers
- Fail fast: validate inputs at boundaries and reject invalid state immediately
- Never swallow errors silently; log or propagate with context
- Keep error handling separate from business logic
- Provide actionable error messages that help the caller fix the problem

<!-- Add your team's error handling conventions here. Examples: custom exception hierarchy, logging format, retry policies, error code catalog -->

## Boundaries

- Wrap third-party APIs behind your own interface; isolate external dependencies at the boundary
- Write integration tests for boundary code; mock the boundary in unit tests
- Define clear data contracts (DTOs, schemas) at system boundaries
- Minimize the surface area of external dependencies: import only what you use

<!-- Add your team's boundary conventions here. Examples: approved third-party libraries, API wrapper patterns, contract-first design requirements -->

## Unit Tests

- Follow Arrange-Act-Assert (or Given-When-Then) structure
- Test one behavior per test; name tests after the behavior they verify
- Keep tests fast, isolated, and repeatable with no shared mutable state
- Use test doubles (mocks, stubs, fakes) only at boundaries; avoid mocking internals
- Treat test code with the same quality standards as production code
- Aim for meaningful coverage of business logic, not arbitrary coverage percentages

<!-- Add your team's testing conventions here. Examples: minimum coverage thresholds, test naming patterns, required test categories, test data management -->

## Classes

- Keep classes small and cohesive: every field and method should relate to the class's single purpose
- Treat 200+ lines or 5+ dependencies as a refactoring signal
- Hide internals: expose behavior through public methods, not raw data
- Prefer composition over inheritance for flexibility
- Separate data-holding classes from behavior-rich classes; avoid god objects

<!-- Add your team's class design conventions here. Examples: maximum class size, required interfaces, dependency injection patterns, base class restrictions -->

## Emergent Design

- Run all tests before committing; passing tests are the minimum quality bar
- Refactor after making it work: remove duplication, improve names, simplify structure
- Apply the Rule of Three: tolerate minor duplication until a pattern emerges; then extract
- Keep the design as simple as possible: fewest classes and methods that satisfy requirements
- Let architecture emerge from requirements, not from speculative abstraction

<!-- Add your team's design conventions here. Examples: refactoring triggers, design review checkpoints, architecture decision record requirements -->

## Code Smells

- **Long function**: extract sub-functions when a function exceeds 30 lines or has multiple indent levels
- **Large class**: split when a class holds unrelated responsibilities or exceeds 200 lines
- **Feature envy**: move logic to the class whose data it uses most
- **Primitive obsession**: replace raw strings/ints with domain types (value objects, enums)
- **Divergent change**: if one class changes for multiple reasons, split by reason
- **Shotgun surgery**: if one change touches many files, consolidate the scattered logic
- **Dead code**: delete unreachable or unused code; do not comment it out
- **Magic values**: replace literal numbers and strings with named constants

<!-- Add your team's code smell thresholds here. Examples: custom line limits, additional smells to watch for, automated detection tool configuration -->
---END TEMPLATE---

3. After writing the file, output this message to the user:

   ## Next Steps

   Your coding standards template has been generated at `.delivery/standards/coding-standards.md`.

   To activate it, add this line to your `.delivery/config.yml` under `tech_stack`:

   ```yaml
   tech_stack:
     clean_code_guide: .delivery/standards/coding-standards.md
   ```

   Once configured, the developer skill will use YOUR standards instead of the built-in defaults for all code generation, review, and refactoring tasks.

   Customize each section by replacing the HTML comment placeholders (`<!-- ... -->`) with your team's specific conventions.
```

---

## Multi-Language Projects

When a task spans multiple languages (e.g., Python backend + TypeScript frontend):

1. Identify all languages involved
2. For each language, spawn **a separate sub-agent** with only that language's reference file
3. Run sub-agents **sequentially** when there are dependencies between outputs
4. Run sub-agents **in parallel** (single message, multiple Agent tool calls) when outputs are independent
5. Assemble and return the combined artifacts

The main context never accumulates multiple language reference files — each sub-agent holds exactly one.

---

## Language → Reference File Mapping

| Language | File Extension(s) | Reference |
|---|---|---|
| Python | `.py`, `.pyw` | `references/languages/python.md` |
| JavaScript | `.js`, `.mjs`, `.cjs` | `references/languages/javascript.md` |
| TypeScript | `.ts`, `.tsx` | `references/languages/typescript.md` |
| C# | `.cs` | `references/languages/csharp.md` |
| Go | `.go` | `references/languages/go.md` |
| Rust | `.rs` | `references/languages/rust.md` |
| Java | `.java` | `references/languages/java.md` |
| SQL | `.sql` | `references/languages/sql.md` |
| Bash/Shell | `.sh`, `.bash`, no extension | `references/languages/bash.md` |
| R | `.r`, `.R`, `.Rmd`, `.qmd` | `references/languages/r.md` |
| F# | `.fs`, `.fsx` | `references/languages/fsharp.md` |
| Elixir | `.ex`, `.exs` | `references/languages/elixir.md` |
| Haskell | `.hs`, `.lhs` | `references/languages/haskell.md` |
| Scala | `.scala`, `.sc` | `references/languages/scala.md` |

For languages not in this table: ask the user to confirm the language, then proceed without a language reference file — apply general clean code principles.

### OOP Cross-Language Reference

For tasks involving object-oriented design (class design, design patterns, SOLID principles, inheritance vs. composition, value objects, dependency injection) in **C#, TypeScript, C++, Java, Python, or Kotlin**: include `references/oop-patterns.md` in the sub-agent prompt alongside the language reference file.

Triggers: mentions of "design pattern", "SOLID", "factory", "singleton", "decorator", "strategy", "observer", "repository", "inheritance", "composition", "dependency injection", "refactor to OOP", "class design".

### Frontend Cross-Language Reference

For tasks involving frontend development (component architecture, CSS/styling, state management, responsive design, performance optimization, UI implementation) in **TypeScript** or **JavaScript**: include the relevant `references/frontend/*.md` file(s) in the sub-agent prompt alongside the language reference file.

Triggers: mentions of "component", "CSS", "styling", "state management", "responsive", "bundle", "web vitals", "frontend performance", "React", "Vue", "Svelte", "Angular", "Next.js", "Nuxt", "SvelteKit", "form handling", "lazy loading", "code splitting", "dark mode", "design tokens", "accessibility implementation".

Reference selection by concern:
- Component architecture or UI patterns → `references/frontend/component-patterns.md`
- CSS, styling, theming, responsive → `references/frontend/styling-systems.md`
- State management, data fetching, caching → `references/frontend/state-management.md`
- Performance, bundle size, web vitals → `references/frontend/performance.md`

Multiple frontend references may be loaded simultaneously (e.g., a "build a responsive form component" task loads component-patterns.md + styling-systems.md).

### Functional Programming Cross-Language Reference

For tasks involving functional programming patterns (pure functions, immutability, pattern matching, monads, function composition, algebraic data types) in **F#, Elixir, Haskell, Scala, TypeScript, JavaScript, Python, or R**: include `references/fp-patterns.md` in the sub-agent prompt alongside the language reference file.

Triggers: mentions of "functional", "pure function", "immutable", "immutability", "pattern matching", "monad", "pipe operator", "curry", "partial application", "fold", "reduce", "map/filter", "algebraic data type", "sum type", "discriminated union", "Option", "Maybe", "Result", "Either", "railway", "composition", "point-free", "referential transparency", "effect system".

### Paradigm Selection from Config

If `.delivery/config.yml` exists, check `tech_stack.paradigm` and `tech_stack.paradigm_by_language`:

- `paradigm: oop` → always load `references/oop-patterns.md` for multi-paradigm languages
- `paradigm: fp` → always load `references/fp-patterns.md` for multi-paradigm languages
- `paradigm: hybrid` → load both OOP and FP references for multi-paradigm languages
- `paradigm: auto` (default) → detect from task context using trigger keywords above

Per-language overrides in `paradigm_by_language` take precedence:
```yaml
tech_stack:
  paradigm: auto
  paradigm_by_language:
    python: oop        # Python defaults to OOP patterns
    typescript: fp     # TypeScript defaults to FP patterns
    scala: hybrid      # Scala loads both
```

Pure-FP languages (F#, Elixir, Haskell) always load `fp-patterns.md` regardless of settings. Pure-OOP languages (Java, C#) always load `oop-patterns.md` regardless of settings.

### Nx Monorepo Cross-Language Reference

For tasks in an **Nx workspace** (detected by presence of `nx.json` in the project or mentions of Nx): include `references/nx-monorepo.md` in the sub-agent prompt alongside the language reference file.

**CRITICAL**: When working in an Nx workspace, ALWAYS use `nx generate` to create projects and libraries. NEVER create project directories manually (`mkdir`, `npm init`). The Nx reference enforces this.

Triggers: "nx", "monorepo", "nx generate", "nx affected", "project.json", "nx.json", "@nx/", "@nrwl/", "workspace", "nx graph", "enforce-module-boundaries", "nx cloud".

To add a new language: create `references/languages/<lang>.md` using the template in `references/languages/README.md`, then add it to the table above.

---

## Sub-Agent Output Contract

The sub-agent should return output in this structure (markdown):

```
## Language: [LANG]
## Task: [TYPE]

### Code

[Complete code — file-by-file if multiple files]

### Key Decisions

[3–5 sentences on non-obvious choices: why this approach, what alternatives were rejected]

### Test Suggestions

- [How to run the code / what inputs to test]
- [Edge cases to verify]
- [How to confirm correctness]

### Verification Status

- **Verified by tests**: [list acceptance criteria covered by written tests]
- **Verified by inspection**: [list acceptance criteria verified by code structure review]
- **Requires runtime validation**: [list acceptance criteria that need the application running — visual output, user interaction, API responses, runtime behavior]
- **Verification gaps**: [any criteria the agent could not verify at all]

### Follow-Up

- [Anything left incomplete with reason]
- [Suggested next steps]
```

**Empirical validation rule**: If any acceptance criteria mention visual output, user interaction, API responses, database queries, or runtime behavior (see the quality skill's `references/empirical-validation.md` for the full keyword registry), list them under "Requires runtime validation" — do NOT mark them as verified by inspection.

---

## User Commands

| Command | Action |
|---|---|
| `lang <name>` | Override detected language (e.g., `lang rust`) |
| `review` | Switch task type to code review for current code |
| `test` | Generate tests for current code |
| `refactor` | Improve structure without behavior change |
| `explain` | Annotate and explain the code |
| `accept` | Finalize — write any pending files to disk |

---

## References

- `references/languages/README.md` — How language isolation works; how to add a new language
- `references/languages/python.md` — Python 3.10+ best practices
- `references/languages/javascript.md` — ES2022+ best practices
- `references/languages/typescript.md` — TypeScript 5.x best practices
- `references/languages/csharp.md` — C# 12 / .NET 8 best practices
- `references/languages/go.md` — Go 1.21+ best practices
- `references/languages/rust.md` — Rust 2021 edition best practices
- `references/languages/java.md` — Java 17 LTS best practices
- `references/languages/sql.md` — SQL / PostgreSQL best practices
- `references/languages/bash.md` — Bash 5+ best practices
- `references/languages/r.md` — R 4.x best practices (tidyverse, testthat, renv)
- `references/clean-code.md` — Language-agnostic clean code principles (foundational, loaded on every task)
- `references/clean-code-review-checklist.md` — Condensed pass/fail checklist for PR reviews (loaded on `review` tasks)
- `references/oop-patterns.md` — OOP patterns: SOLID, GoF patterns, composition, DI (C#, TypeScript, Java, C++)
- `references/frontend/component-patterns.md` — Component composition, forms, routing, error boundaries, accessibility
- `references/frontend/styling-systems.md` — CSS architecture, theming, responsive design, dark mode, performance
- `references/frontend/state-management.md` — State patterns, server state, URL state, optimistic updates, persistence
- `references/frontend/performance.md` — Bundle optimization, Core Web Vitals, lazy loading, service workers, CDN
- `references/languages/fsharp.md` — F# 8 / .NET 8: discriminated unions, computation expressions, railway-oriented programming
- `references/languages/elixir.md` — Elixir 1.16+ / OTP 26+: GenServer, Phoenix, Ecto, pipe operator, supervision trees
- `references/languages/haskell.md` — GHC 9.6+: IO monad, type classes, algebraic data types, strictness, QuickCheck
- `references/languages/scala.md` — Scala 3.3+: case classes, given/using, Cats Effect/ZIO, sbt, for-comprehensions
- `references/fp-patterns.md` — Functional programming: pure functions, immutability, HOFs, pattern matching, monads, composition, type-driven development
- `references/nx-monorepo.md` — Nx workspace: generators (NEVER manual mkdir), affected commands, caching, module boundaries, library categories
