## Idea Brief: Clean Code Foundational Standards

**Project Type**: FEATURE
**Date**: 2026-03-27

### Problem Statement

The delivery-team developer skill supports 14 languages and loads conditional references (OOP, FP, Frontend, Nx) based on project configuration, but has no foundational layer that enforces clean code principles across all coding tasks. Language-specific references tell developers *how to write* in a given language; they do not tell developers *how to write well* regardless of language.

This gap means:
- Code quality depends entirely on the individual developer's discipline -- the skill provides no baseline standard
- Clean code principles (meaningful names, small functions, proper error handling, code smell avoidance) are not embedded in generation prompts, so generated code may be technically correct but hard to read, maintain, or extend
- The PR review toolkit (`code-reviewer`, `code-simplifier`) has no shared reference for what "clean" means, so review feedback is subjective and inconsistent
- Teams with their own coding standards have no mechanism to inject them into the developer skill's context
- The Godot skill shares the same gap -- GDScript and C# code gets no clean code guidance

### Target Users

1. **Developers** using the developer skill for any of the 14 supported languages -- clean code principles apply universally
2. **Developers** using the Godot skill (GDScript, C#) -- game code benefits from the same foundational standards
3. **Teams with custom coding standards** -- organizations that want to replace the default guide with their own house style
4. **Code reviewers** using `pr-review-toolkit:code-reviewer` and `pr-review-toolkit:code-simplifier` -- need a shared reference to evaluate against

### Proposed Scope

#### 1. Reference File: `clean-code.md`

A new language-agnostic reference file in `delivery-team/skills/developer/references/` covering 10 sections drawn from Robert C. Martin's "Clean Code":

| Section | Focus |
|---------|-------|
| **Meaningful Names** | Intention-revealing names, avoiding disinformation, pronounceable/searchable names, noun classes, verb methods |
| **Functions** | Small, single-purpose, one level of abstraction, minimal arguments, no side effects, command-query separation |
| **Comments** | Good comments (legal, informative, clarifying, warning, TODO); bad comments (redundant, misleading, noise, commented-out code) |
| **Formatting** | Vertical openness, density, distance, ordering; horizontal alignment, indentation; team rules |
| **Error Handling** | Exceptions over return codes, provide context, define exception classes by caller needs, don't return/pass null |
| **Boundaries** | Clean integration with third-party code, learning tests, wrapping external APIs, adapter pattern |
| **Unit Tests** | TDD laws, clean tests, one assert/concept per test, F.I.R.S.T. principles |
| **Classes** | Small, single responsibility, cohesion, organizing for change, dependency inversion |
| **Emergent Design** | Kent Beck's 4 rules: runs all tests, no duplication, expresses intent, minimal classes/methods |
| **Code Smells** | Catalog of common smells organized by category (comments, environment, functions, general, names, tests) |

**Boundary with existing references**: SOLID principles remain in `oop-patterns.md`. The Classes section in `clean-code.md` references SRP at a practical level (class size, cohesion) without duplicating the SOLID theory.

#### 2. Foundational Loading (Not Conditional)

`clean-code.md` loads on EVERY developer and Godot task automatically. It is part of the base sub-agent prompt template, alongside the language reference. It does NOT go in the cross-language routing table (OOP/FP/Frontend/Nx) because it is not conditional on tech stack choices.

**Loading order**: Language reference -> Clean code -> Conditional patterns (OOP/FP/Frontend/Nx)

This ensures clean code principles are always present as baseline context, regardless of which conditional patterns are loaded.

#### 3. Code Review Enforcement

The `pr-review-toolkit:code-reviewer` and `pr-review-toolkit:code-simplifier` agents are extended to check code against clean code principles. The enforcement behavior is:

| Enforcement Level | Behavior |
|-------------------|----------|
| `block` (default) | Clean code violations are blockers -- review cannot pass until resolved |
| `warn` | Clean code violations are reported as warnings -- review can pass with acknowledged violations |

Enforcement level is configured via `tech_stack.clean_code_enforcement` in `.delivery/config.yml`.

#### 4. Configurable Guide

Teams can point to their own coding standards file via `tech_stack.clean_code_guide` in `.delivery/config.yml`:

```yaml
tech_stack:
  clean_code_guide: .delivery/standards/coding-standards.md
  clean_code_enforcement: block  # block | warn
```

- **Default**: Built-in `clean-code.md` (when key is absent or empty)
- **Custom**: Path to team's own file (replaces the default, not additive)
- **Validation**: Config check hook validates the custom path exists at session start

#### 5. Scaffold Command: `coding-standards`

A command that generates a starter `.delivery/standards/coding-standards.md` template:
- Pre-populated with the 10 sections from the default `clean-code.md`
- Each section includes customization placeholders (e.g., team-specific naming conventions, preferred formatting rules, project-specific error handling patterns)
- Teams edit the generated file, then point `tech_stack.clean_code_guide` to it

### Key Design Decisions

#### 1. Foundational layer, not conditional

**Decision**: Load `clean-code.md` on every developer and Godot task, not through the cross-language routing table.

**Rationale**:
- Clean code principles are universal -- they apply to Python, TypeScript, Go, Rust, GDScript, and every other supported language equally
- The routing table is for patterns that vary by tech stack choice (OOP vs FP vs Frontend). Clean code is not a choice; it is a baseline
- Conditional loading would mean teams could accidentally opt out of clean code by not selecting it in their config
- This follows the same pattern as language references -- always loaded, non-negotiable context

#### 2. Custom guide replaces default (not additive)

**Decision**: When `tech_stack.clean_code_guide` is set, the custom file replaces `clean-code.md` entirely.

**Rationale**:
- Additive loading would create conflicts when team standards disagree with default principles (e.g., team allows certain commented-out code patterns that the default flags)
- A single source of truth for coding standards is cleaner than merging two potentially contradictory guides
- The scaffold command gives teams a starting point based on the default, so they are not starting from scratch
- Teams that want the default plus additions can copy the default content into their custom file

#### 3. Block by default, warn as opt-in

**Decision**: Clean code violations are blockers by default in code review.

**Rationale**:
- Standards that are warnings-only tend to be ignored over time -- if the review passes anyway, there is no incentive to fix violations
- Teams that find blocking too strict can explicitly opt into `warn` mode via config
- This aligns with the delivery pipeline's philosophy of quality gates that enforce, not suggest

#### 4. Godot included identically

**Decision**: The Godot skill loads `clean-code.md` the same way the developer skill does.

**Rationale**:
- GDScript and C# benefit from the same clean code principles as any other language
- Having different code quality standards for game code vs application code creates an inconsistency
- The Godot skill already follows the same sub-agent pattern as the developer skill, so the loading mechanism is identical

### Risks & Open Questions

#### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Context window bloat from always-on reference | Reduces available context for actual task work, especially on complex multi-file tasks | Keep `clean-code.md` concise and principle-focused (target ~2000 tokens); avoid lengthy examples; reference external resources for deep dives |
| False positive violations in code review | Blocks legitimate code patterns that appear to violate clean code but are idiomatic for the language | Language-specific exceptions section in `clean-code.md`; `warn` mode as escape valve; team custom guide overrides |
| Teams confused by block vs warn distinction | Unclear why their PR review is failing | Clear error messages referencing the specific principle violated and how to configure enforcement level |
| Custom guide path breaks silently | Team points to a file that does not exist or is empty | Config check hook validates path at session start; clear error message with fix instructions |

#### Open Questions

1. **Should `clean-code.md` include brief code examples per principle?** Examples aid comprehension but increase token count. Could use a tiered approach: principles-only in the main file, examples in a separate reference loaded on demand.
2. **How should the scaffold command be invoked?** As a slash command (`/coding-standards`), a skill task type, or a script? The delivery-team pattern suggests a skill task type.
3. **Should the config check hook validate the content of custom guides?** Checking file existence is simple; checking that the file covers the expected sections is more complex and potentially intrusive.
4. **PR review toolkit integration depth**: Should the reviewers get the full `clean-code.md` in their prompt, or a condensed checklist version optimized for review (not generation)?
5. **Metrics**: Should clean code violations be tracked in pipeline analytics? This would enable trends over time (e.g., "clean code violations per sprint decreasing") but adds complexity to the analytics dashboard.
6. **Dogfooding plan**: The team should apply the clean code reference to its own Python scripts (`hooks/*.py`, `scripts/*.py`, `prd-quality-gate-flow/*.py`) before shipping. This validates the reference content and the enforcement mechanism on real code.
