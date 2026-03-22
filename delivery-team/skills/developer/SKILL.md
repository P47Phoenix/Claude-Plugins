---
name: developer
description: Developer agent for writing, reviewing, and refactoring code in any language. This skill should be used when users want to write code, fix bugs, refactor existing code, add tests, or review code quality. Auto-detects the programming language and spawns a language-scoped sub-agent so only the relevant best-practices are loaded into context — never all languages at once. Triggers on phrases like "write code", "implement", "fix this bug", "refactor", "add tests", "code review", "write a function", "build a script", and on file extensions (.py, .ts, .js, .go, .rs, .cs, .java, .sql, .sh, .r, .R, .Rmd).
license: Apache License 2.0 - See repository LICENSE file
---

# Developer Agent

## Design Principle: Language Context Isolation

This skill intentionally keeps language-specific knowledge **out of the main context window**. When a coding task is requested, a sub-agent is spawned carrying only the single relevant language reference. This means:

- A Python task loads only `references/languages/python.md`
- A TypeScript task loads only `references/languages/typescript.md`
- No other language files are loaded — ever

The main context receives only the finished code artifact. All language-specific reasoning happens inside the sub-agent's isolated context.

---

## Phase 1: Language Detection

Detect the target language from (in priority order):
1. File extension in context: `.py` → Python, `.ts` → TypeScript, `.js` → JavaScript, `.cs` → C#, `.go` → Go, `.rs` → Rust, `.java` → Java, `.sql` → SQL, `.sh`/`.bash` → Bash, `.r`/`.R`/`.Rmd`/`.qmd` → R
2. Imports or syntax in pasted code
3. User's explicit statement
4. File being edited in the current session

**If language is ambiguous, ask before proceeding.** Do not assume.

**Declare before every task:**

> `Language: [LANG] | Task: [write / fix / refactor / review / test / explain] | Reference: references/languages/<lang>.md`

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

### Task Type Instructions for Sub-Agent

| Task Type | What the sub-agent does |
|---|---|
| **write** | Implement from scratch following all conventions in the language reference |
| **fix** | Identify the root cause, patch it, explain what was wrong and why |
| **refactor** | Improve structure, naming, and idioms without changing behavior; cite which best-practice violations were addressed |
| **review** | Audit the code against the language reference; produce annotated findings with severity (critical / warning / suggestion) |
| **test** | Write tests using the language's idiomatic test framework; cover happy path, edge cases, and error conditions |
| **explain** | Walk through the code with annotations; reference language idioms where relevant |

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

### Follow-Up

- [Anything left incomplete with reason]
- [Suggested next steps]
```

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
- `references/oop-patterns.md` — OOP patterns: SOLID, GoF patterns, composition, DI (C#, TypeScript, Java, C++)
- `references/frontend/component-patterns.md` — Component composition, forms, routing, error boundaries, accessibility
- `references/frontend/styling-systems.md` — CSS architecture, theming, responsive design, dark mode, performance
- `references/frontend/state-management.md` — State patterns, server state, URL state, optimistic updates, persistence
- `references/frontend/performance.md` — Bundle optimization, Core Web Vitals, lazy loading, service workers, CDN
