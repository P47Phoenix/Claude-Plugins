# PRD: Clean Code Foundational Standards

**Version**: 1.0
**Date**: 2026-03-27
**Author**: Product Owner (delivery-team)
**Project Type**: FEATURE
**Status**: Draft

---

## 1. Problem Statement

The delivery-team developer skill supports 14 languages and loads conditional references (OOP, FP, Frontend, Nx) based on project configuration, but has no foundational layer that enforces clean code principles across all coding tasks. Language-specific references tell developers *how to write* in a given language; they do not tell developers *how to write well* regardless of language.

**Impact of the gap:**

- Code quality depends entirely on the individual developer's discipline -- the skill provides no baseline standard
- Clean code principles (meaningful names, small functions, proper error handling, code smell avoidance) are not embedded in generation prompts, so generated code may be technically correct but hard to read, maintain, or extend
- The PR review toolkit (`code-reviewer`, `code-simplifier`) has no shared reference for what "clean" means, so review feedback is subjective and inconsistent
- Teams with their own coding standards have no mechanism to inject them into the developer skill's context
- The Godot skill shares the same gap -- GDScript and C# code gets no clean code guidance

## 2. Goals & Success Metrics

| Goal | Metric | Baseline | Target |
|------|--------|----------|--------|
| Embed clean code principles in all code generation | % of developer/Godot tasks that load clean code context | 0% | 100% |
| Provide consistent code review standards | Code review violations reference a shared standard | No shared reference | All clean code findings cite specific principle from guide |
| Keep token overhead minimal | Token count of `clean-code.md` | N/A | <=2000 tokens |
| Enable team customization | Teams can override the default guide via config | Not possible | Config key `tech_stack.clean_code_guide` supported |
| Track clean code quality trends | Clean code violations tracked in pipeline analytics | No tracking | Violation counts per pipeline run visible in analytics |
| Validate via dogfooding | Apply clean code review to existing repo Python scripts | Not applied | All `hooks/*.py`, `scripts/*.py`, `prd-quality-gate-flow/*.py` reviewed |

## 3. User Personas

### Primary: Developers using the developer skill

- Use the developer skill daily across any of the 14 supported languages
- Expect generated code to follow best practices without manual intervention
- Benefit from a baseline standard that raises code quality floor across all tasks

### Primary: Developers using the Godot skill

- Write GDScript and C# code for game development
- Need the same clean code principles applied to game code as application code
- Currently receive no clean code guidance from the skill

### Secondary: Code reviewers using PR review toolkit

- Use `pr-review-toolkit:code-reviewer` and `pr-review-toolkit:code-simplifier`
- Need a shared, objective reference to evaluate code against
- Currently provide subjective feedback with no consistent baseline

### Secondary: Teams with custom coding standards

- Organizations with established house styles and naming conventions
- Need to inject their own standards into the developer skill's context
- Want a starting template rather than writing standards from scratch

## 4. User Stories (Summary)

### Component 1: Reference File (`clean-code.md`)

- US-01: As a developer, I want a language-agnostic clean code reference covering 10 foundational sections so that generated code follows established best practices
- US-02: As a developer, I want the reference to stay under 2000 tokens so that it does not consume excessive context window

### Component 2: Foundational Loading

- US-03: As a developer, I want clean code principles loaded automatically on every developer task so that I never have to opt in
- US-04: As a Godot developer, I want clean code principles loaded automatically on every Godot task so that game code gets the same standards
- US-05: As a developer, I want clean code to load after the language reference and before conditional patterns so that the layering order is predictable

### Component 3: Code Review Enforcement

- US-06: As a code reviewer, I want PR reviews to check code against clean code principles so that review feedback is objective and consistent
- US-07: As a team lead, I want to configure enforcement level (block/warn) so that I can control how strictly violations are handled
- US-08: As a developer, I want clear error messages when clean code violations block a review so that I know exactly what to fix

### Component 4: Configurable Guide

- US-09: As a team lead, I want to point to my own coding standards file via config so that the skill uses our house style
- US-10: As a team lead, I want the config check hook to validate my custom guide path exists at session start so that broken paths fail fast
- US-11: As a developer, I want the custom guide to fully replace the default (not merge) so that there is one source of truth

### Component 5: Scaffold Command

- US-12: As a team lead, I want to generate a starter coding standards template so that I have a starting point based on the default
- US-13: As a team lead, I want the template pre-populated with customization placeholders so that I know what to fill in

## 5. Functional Requirements

### Reference File

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-01 | Create `clean-code.md` in `delivery-team/skills/developer/references/` covering 10 sections: Meaningful Names, Functions, Comments, Formatting, Error Handling, Boundaries, Unit Tests, Classes, Emergent Design, Code Smells | P0 | File exists with all 10 sections; each section contains actionable principles (not theory) |
| FR-02 | Keep `clean-code.md` at or below 2000 tokens | P0 | Token count verified <= 2000 using a tokenizer; no code examples in main file |
| FR-03 | Include a language-specific exceptions subsection for principles that conflict with language idioms | P1 | Subsection exists; covers at minimum Python, GDScript, and Go naming convention exceptions |
| FR-04 | Reference SRP at a practical level (class size, cohesion) without duplicating SOLID theory from `oop-patterns.md` | P0 | No overlap with `oop-patterns.md` SOLID definitions; Classes section references SRP by application, not definition |

### Foundational Loading

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-05 | Load `clean-code.md` (or custom guide) on every developer sub-agent task as part of the base prompt template | P0 | Developer sub-agent prompt includes clean code content for all 14 supported languages |
| FR-06 | Load `clean-code.md` (or custom guide) on every Godot sub-agent task as part of the base prompt template | P0 | Godot sub-agent prompt includes clean code content for GDScript and C# tasks |
| FR-07 | Loading order: Language reference -> Clean code -> Conditional patterns (OOP/FP/Frontend/Nx) | P0 | Verified via prompt template inspection; clean code appears after language ref and before conditional patterns |
| FR-08 | Clean code loading is NOT conditional -- it does not appear in the cross-language routing table | P0 | Routing table unchanged; clean code loads regardless of `tech_stack` config values |

### Code Review Enforcement

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-09 | `pr-review-toolkit:code-reviewer` checks code against loaded clean code guide | P0 | Code reviewer agent prompt includes clean code principles; review output cites specific principles when violations found |
| FR-10 | `pr-review-toolkit:code-simplifier` checks code against loaded clean code guide | P1 | Code simplifier agent prompt includes clean code principles; simplification suggestions reference clean code principles |
| FR-11 | Support `tech_stack.clean_code_enforcement` config key with values `block` (default) and `warn` | P0 | When `block`: violations prevent review from passing. When `warn`: violations reported but review can pass. Default is `block` when key is absent |
| FR-12 | Violation messages cite the specific clean code principle violated and include the config path to change enforcement level | P1 | Each violation message names the principle (e.g., "Functions: exceeds single responsibility") and states "Configure via tech_stack.clean_code_enforcement" |

### Configurable Guide

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-13 | Support `tech_stack.clean_code_guide` config key pointing to a custom file path | P0 | When set, the custom file is loaded instead of the default `clean-code.md` |
| FR-14 | Custom guide replaces default entirely (not additive) | P0 | Only one guide is loaded per task -- either custom or default, never both |
| FR-15 | Default to built-in `clean-code.md` when config key is absent or empty | P0 | Absent key and empty string both result in default guide loading |
| FR-16 | Config check hook validates custom guide path exists at session start | P0 | Session start with non-existent custom path produces clear error with fix instructions |
| FR-17 | Config check hook validates file existence only, not content structure | P0 | No content validation -- only checks that the file at the path exists and is readable |

### Scaffold Command

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-18 | Implement `coding-standards` as a skill task type in the developer skill | P1 | Invocable as a developer skill task; consistent with delivery-team skill patterns |
| FR-19 | Generate `.delivery/standards/coding-standards.md` template pre-populated with all 10 sections | P1 | Generated file contains all 10 sections from the default `clean-code.md` |
| FR-20 | Each section includes customization placeholders with guidance comments | P1 | Placeholders present (e.g., "<!-- Add your team's naming conventions here -->"); guidance comments explain what to customize |
| FR-21 | Output includes instruction to set `tech_stack.clean_code_guide` to the generated file path | P1 | Post-generation message tells user to add `tech_stack.clean_code_guide: .delivery/standards/coding-standards.md` to config |

### Metrics & Dogfooding

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-22 | Track clean code violation counts in pipeline analytics per pipeline run | P2 | Analytics dashboard shows violation count per run; data queryable for trend analysis |
| FR-23 | Apply clean code review to all existing Python scripts in the repo (`hooks/*.py`, `scripts/*.py`, `prd-quality-gate-flow/*.py`) before shipping | P0 | All existing Python scripts pass clean code review at `warn` level minimum; findings documented |

## 6. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Token budget for `clean-code.md` | <= 2000 tokens |
| NFR-02 | Loading latency impact on developer/Godot sub-agent spawn | Negligible -- file read only, no computation |
| NFR-03 | Compatibility with all 14 supported languages in developer skill | Principles apply to Python, TypeScript, JavaScript, Go, Rust, C#, Java, SQL, Bash, R, F#, Elixir, Haskell, Scala |
| NFR-04 | Compatibility with Godot skill (GDScript, C#) | Same loading mechanism as developer skill |
| NFR-05 | No new external dependencies | Pure markdown reference + config keys + prompt template changes only |
| NFR-06 | Config schema backward compatibility | Existing configs without new keys continue to work with defaults |

## 7. Out of Scope

- **Code examples in `clean-code.md`**: Keep principle-focused for token economy. Examples belong in language-specific references or a separate on-demand reference.
- **Content validation of custom guides**: Only file existence is validated, not whether the file covers expected sections or follows a particular format.
- **Additive/merge loading of custom + default guides**: Custom guide fully replaces default. Teams wanting both must copy default content into their custom file.
- **Auto-fix of clean code violations**: The feature detects and reports violations. Automated fixing is a separate future feature.
- **New language support**: This feature works with the existing 14 languages + GDScript. No new languages are added.
- **SOLID principles coverage**: SOLID remains in `oop-patterns.md`. Clean code references SRP at a practical level only.
- **IDE/editor integrations**: This feature operates entirely within the Claude Code skill and hook system.

## 8. Dependencies & Risks

### Dependencies

| Dependency | Component | Impact if unavailable |
|------------|-----------|----------------------|
| Developer skill sub-agent prompt template | FR-05, FR-07 | Cannot inject clean code into generation context |
| Godot skill sub-agent prompt template | FR-06 | Cannot inject clean code into Godot generation context |
| `pr-review-toolkit:code-reviewer` agent | FR-09 | Cannot add clean code enforcement to reviews |
| `pr-review-toolkit:code-simplifier` agent | FR-10 | Cannot add clean code enforcement to simplification |
| Config check hook (`hooks/config_check.py`) | FR-16 | Cannot validate custom guide path at session start |
| `.delivery/config.yml` schema | FR-11, FR-13 | Cannot add new config keys |
| Pipeline analytics system | FR-22 | Cannot track violation metrics (P2 -- deferrable) |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Context window bloat from always-on reference | Medium | High -- reduces available context for complex multi-file tasks | Keep `clean-code.md` concise (<=2000 tokens); no code examples; principle-focused |
| False positive violations in code review | Medium | Medium -- blocks legitimate idiomatic code patterns | Language-specific exceptions section; `warn` mode as escape valve; custom guide override |
| Teams confused by block vs warn distinction | Low | Low -- unclear why PR review is failing | Clear error messages citing specific principle and config path to change enforcement |
| Custom guide path breaks silently | Low | Medium -- team thinks their guide is loaded but it is not | Config check hook validates path at session start with clear error and fix instructions |
| Overlap between `clean-code.md` Classes section and `oop-patterns.md` SOLID | Medium | Low -- redundant context wastes tokens | Explicit boundary: Classes section covers practical SRP (size, cohesion) only; SOLID theory stays in `oop-patterns.md` |

## 9. Timeline & Milestones

| Milestone | Description | Exit Criteria |
|-----------|-------------|---------------|
| M1: Reference File | `clean-code.md` authored and reviewed | File exists with 10 sections; <= 2000 tokens; no overlap with `oop-patterns.md`; language exceptions subsection present |
| M2: Foundational Loading | Developer and Godot skills load clean code on every task | Both skill prompt templates include clean code; loading order verified (lang -> clean code -> conditional); routing table unchanged |
| M3: Config & Scaffold | Custom guide config key and scaffold task type | `tech_stack.clean_code_guide` and `tech_stack.clean_code_enforcement` keys functional; config check hook validates custom path; scaffold generates template with placeholders |
| M4: Code Review Enforcement | PR review toolkit enforces clean code | `code-reviewer` and `code-simplifier` reference clean code; block/warn behavior works per config; violation messages cite specific principles |
| M5: Metrics & Dogfooding | Analytics tracking and self-validation | Violation counts in pipeline analytics; all existing Python scripts in repo reviewed; findings documented and addressed |
| M6: Config Schema Update | Config schema docs updated | `config-schema.md` updated with new keys following extension protocol; JSON Schema generation script updated if applicable |

## 10. Open Questions (Resolved)

| # | Question | Resolution | Rationale |
|---|----------|------------|-----------|
| 1 | Should `clean-code.md` include brief code examples? | NO | Keep principle-focused for token economy. Examples belong in language-specific references. |
| 2 | How should the scaffold command be invoked? | Skill task type | Consistent with delivery-team patterns. Not a slash command or standalone script. |
| 3 | Should the config check hook validate custom guide content? | NO -- file existence only | Keep it simple. Content validation is complex, potentially intrusive, and out of scope. |
| 4 | PR review integration depth? | Condensed checklist version | Load a checklist optimized for review, not the full reference. Review context differs from generation context. |
| 5 | Should clean code violations be tracked in pipeline analytics? | YES | Enables trend analysis (violations per sprint decreasing). Adds complexity but provides measurable improvement signal. |
| 6 | Dogfooding plan? | Apply to existing Python scripts | Review `hooks/*.py`, `scripts/*.py`, `prd-quality-gate-flow/*.py` before shipping to validate both reference content and enforcement mechanism. |
