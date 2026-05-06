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
1. File extension in context — see the Language → Reference File Mapping table below for all supported extensions
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

The clean code guide loads on EVERY task for EVERY language. Loading order: Language reference → Clean code → Conditional patterns (OOP/FP/Frontend/Nx).

**Resolution logic** (check `tech_stack.clean_code_guide` in `.delivery/config.yml`):
1. Key set + file exists → load custom guide (REPLACES default, do not load both)
2. Key set + file missing → warn "Custom clean code guide not found: {path}. Using built-in default." then load `references/clean-code.md`
3. Key absent / empty / no config → load `references/clean-code.md`

**For `review` tasks**: also load `references/clean-code-review-checklist.md`. Insert after `## Clean Code Standards` as `## Clean Code Review Checklist`. Append the enforcement block below (mode from `tech_stack.clean_code_enforcement`, default: `block`).

**Enforcement block to inject after the checklist**:

```
## Clean Code Enforcement
Enforcement mode: [block | warn]
Evaluate code against EVERY item in the Clean Code Review Checklist.
For each violation: [SEVERITY] [Section]: [description]
  Configure via tech_stack.clean_code_enforcement in .delivery/config.yml
SEVERITY = VIOLATION (block mode) or WARNING (warn mode).
Result line: RESULT: BLOCKED (N violations) | RESULT: PASSED with N warnings | RESULT: PASSED
```

**For `simplify`/`refactor` tasks**: append to the sub-agent prompt: "Cite the specific clean code section (e.g., 'Functions', 'Code Smells') for each change you make."

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

### `coding-standards` Task Type — Dispatch

Load `references/agent-prompts/coding-standards.md` for the sub-agent prompt.
Load `references/coding-standards-template.md` for the template content.
Skip language detection. Follow pre-flight and output instructions in the agent-prompt file.

---

## Multi-Language Projects

Spawn a **separate sub-agent per language** (one language reference each). Run sequentially when outputs are dependent; in parallel (single message, multiple Agent calls) when independent. Assemble and return the combined artifacts. The main context never accumulates multiple language reference files.

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

Include `references/oop-patterns.md` for **C#, TypeScript, C++, Java, Python, Kotlin** tasks involving class design, design patterns, SOLID, inheritance/composition, DI, or value objects.

Triggers: "design pattern", "SOLID", "factory", "singleton", "decorator", "strategy", "observer", "repository", "inheritance", "composition", "dependency injection", "class design".

### Frontend Cross-Language Reference

Include the relevant `references/frontend/*.md` for **TypeScript/JavaScript** tasks involving component architecture, CSS/styling, state management, responsive design, or UI performance.

- Component architecture / UI patterns → `references/frontend/component-patterns.md`
- CSS, styling, theming, responsive → `references/frontend/styling-systems.md`
- State management, data fetching, caching → `references/frontend/state-management.md`
- Performance, bundle size, web vitals → `references/frontend/performance.md`

Triggers: "component", "CSS", "state management", "responsive", "bundle", "web vitals", "React", "Vue", "Svelte", "Angular", "Next.js", "Nuxt", "lazy loading", "dark mode", "accessibility".

Multiple frontend refs may load simultaneously (e.g., "responsive form component" → component-patterns + styling-systems).

### Functional Programming Cross-Language Reference

Include `references/fp-patterns.md` for **F#, Elixir, Haskell, Scala, TypeScript, JavaScript, Python, R** tasks involving pure functions, immutability, pattern matching, monads, or function composition.

Triggers: "functional", "pure function", "immutable", "pattern matching", "monad", "pipe operator", "curry", "fold", "reduce", "algebraic data type", "discriminated union", "Option/Maybe/Result/Either", "railway", "point-free", "effect system".

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
- **Verified by tests**: [acceptance criteria covered by tests]
- **Verified by inspection**: [acceptance criteria verified by code structure review]
- **Requires runtime validation**: [criteria needing the app running — visual, API, user interaction]
- **Verification gaps**: [criteria the agent could not verify]
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

Language files: see `references/languages/<lang>.md` (paths in the mapping table above).
See `references/languages/README.md` for how to add a new language.

- `references/clean-code.md` — foundational clean code principles (loaded on every task)
- `references/clean-code-review-checklist.md` — pass/fail checklist for `review` tasks
- `references/oop-patterns.md` — SOLID, GoF patterns, composition, DI
- `references/fp-patterns.md` — pure functions, immutability, HOFs, monads, composition
- `references/frontend/component-patterns.md` — component composition, forms, routing, accessibility
- `references/frontend/styling-systems.md` — CSS architecture, theming, responsive, dark mode
- `references/frontend/state-management.md` — state patterns, server state, optimistic updates
- `references/frontend/performance.md` — bundle optimization, Core Web Vitals, lazy loading
- `references/nx-monorepo.md` — Nx: generators (NEVER manual mkdir), affected, caching
- `references/agent-prompts/coding-standards.md` — sub-agent prompt for coding-standards task
- `references/coding-standards-template.md` — template written to `.delivery/standards/`
