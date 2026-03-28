# ADR-001: Foundational Layer vs Conditional Routing for Clean Code

**Status**: Accepted
**Date**: 2026-03-27
**Deciders**: Solution Architect, Product Owner
**Context**: Clean Code Foundational Standards feature (PRD v1.0)

---

## Context

The developer skill uses a conditional routing system for cross-language references. OOP patterns load when task context contains OOP triggers ("design pattern", "SOLID", "factory", etc.) or when `tech_stack.paradigm` is set to `oop`. FP patterns load similarly. Frontend and Nx references also use conditional routing based on context signals.

The question: should `clean-code.md` follow this same conditional routing pattern, or should it load unconditionally as a foundational layer on every task?

## Decision

Clean code loads unconditionally on every developer and Godot sub-agent task. It is a **foundational layer**, not a conditionally-routed reference.

Specifically:
- `clean-code.md` does NOT appear in the cross-language routing table
- It does NOT have trigger keywords
- It does NOT depend on any `tech_stack` config value to activate
- It loads between the language reference and conditional patterns in the prompt assembly order

## Rationale

### 1. Clean code is universal; paradigm patterns are contextual

OOP patterns apply when you are doing object-oriented design. FP patterns apply when you are doing functional programming. These are task-dependent -- a developer writing a simple script has no use for GoF patterns or monad composition.

Clean code principles (meaningful names, small functions, proper error handling, avoiding code smells) apply to ALL code regardless of paradigm, language, or task type. There is no coding task where "use meaningful names" or "handle errors properly" is irrelevant. Making clean code conditional would mean some tasks get clean code guidance and others do not, based on whether the user happened to say a trigger word. This creates an inconsistent quality floor.

### 2. Trigger-based loading creates a false opt-in

If clean code were trigger-based, a developer would need to say something like "write clean code" or "follow clean code principles" to activate it. This inverts the expected behavior -- clean code should be the default, not something you request. Developers who forget to say the trigger get lower-quality output. The whole point of the feature is to raise the quality floor without requiring developer action.

### 3. Token budget makes always-on feasible

The primary argument against always-on loading is context window consumption. However, `clean-code.md` is budgeted at <=2000 tokens -- roughly 1-2% of a typical context window. This is significantly smaller than language references (which are always loaded) and comparable to the overhead of a few extra chat messages. The cost of always loading clean code is negligible compared to the cost of inconsistent code quality.

### 4. Conditional routing adds complexity with no benefit

Adding clean code to the routing table would require:
- Defining trigger keywords (which keywords? "clean"? "quality"? "good code"?)
- Adding a `tech_stack.clean_code` config toggle (adding a toggle for something that should always be on)
- Handling the case where clean code triggers overlap with OOP/FP triggers
- Explaining to users why some tasks get clean code and others do not

All of this complexity exists to solve a problem that does not exist. No team will say "I want clean code on some tasks but not others." Teams that want different standards use the custom guide override (`tech_stack.clean_code_guide`); they do not want to disable clean code entirely.

### 5. Precedent: language references are already always-on

The developer skill already loads the language reference unconditionally on every task. Clean code is the same category of concern -- it is baseline guidance that applies to all code in the detected language. Adding it as another always-on layer is consistent with the existing architecture.

## Consequences

### Positive

- Every developer and Godot task gets clean code guidance without any user action or configuration
- The quality floor for generated code is raised across all 14 languages + GDScript
- Code reviews have a consistent, shared standard to evaluate against
- No trigger keyword ambiguity or missed-loading scenarios
- Simpler implementation: no routing logic, no triggers, no toggle

### Negative

- ~2000 tokens consumed on every sub-agent spawn, even for trivial tasks (mitigated by strict token budget)
- Teams cannot disable clean code entirely without using a custom guide that is intentionally empty (this is an acceptable edge case -- teams that want no standards at all can set `tech_stack.clean_code_guide` to an empty file)
- If `clean-code.md` grows beyond its token budget in future iterations, the always-on cost increases (mitigated by the <=2000 token NFR and review process)

## Alternatives Considered

### Alternative A: Conditional routing with trigger keywords

Load clean code only when task context contains keywords like "clean", "quality", "naming", "refactor". Rejected because it creates inconsistent quality and false opt-in behavior (see Rationale points 1-2).

### Alternative B: Config toggle (`tech_stack.clean_code: true/false`)

Add a config key to enable/disable clean code loading. Rejected because it adds a toggle for something that should always be on. Teams wanting custom standards already have `tech_stack.clean_code_guide`. A disable toggle invites teams to turn off quality guidance, which contradicts the feature's purpose.

### Alternative C: Load only for review/refactor task types

Load clean code only when the task type is `review` or `refactor`, not for `write` or `fix`. Rejected because it is better to write clean code the first time than to fix it in review. Loading clean code during `write` tasks prevents violations rather than detecting them after the fact.
