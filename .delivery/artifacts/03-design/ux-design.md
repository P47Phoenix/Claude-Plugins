# UX Design: Clean Code Foundational Standards

**Version**: 1.0
**Date**: 2026-03-27
**Author**: UX Designer (delivery-team)
**Status**: Draft
**Input**: PRD v1.0

---

## Design Principles

1. **Silent by default** -- Clean code loading should be invisible when working correctly. Developers should not manage it.
2. **Loud on failure** -- When something is wrong (missing file, blocked review), messages must be specific, actionable, and show the fix.
3. **Consistent with existing patterns** -- Error formats, config keys, and hook outputs follow the same style as existing delivery-team components.
4. **One source of truth** -- Never show ambiguity about which guide is active. State it explicitly in the sub-agent declaration line.

---

## 1. Automatic Clean Code Loading (Silent UX)

### 1.1 What the developer sees

Nothing new. Clean code loading is silent -- it happens inside the sub-agent prompt assembly, which the developer never sees directly. The only visible change is in the **declaration line** that the developer skill already prints before every task.

**Current declaration line:**

```
Language: Python | Task: write | Reference: references/languages/python.md
```

**New declaration line (default guide):**

```
Language: Python | Task: write | Reference: references/languages/python.md | Clean Code: default
```

**New declaration line (custom guide):**

```
Language: Python | Task: write | Reference: references/languages/python.md | Clean Code: .delivery/standards/coding-standards.md
```

### 1.2 Rationale

- Adding `Clean Code: default` confirms the feature is active without cluttering the output. It is a single key-value pair appended to an existing line.
- Showing the custom path when a custom guide is set makes it explicit which guide is loaded -- critical for teams switching between projects with different standards.
- The declaration line is already expected output; extending it is lower-friction than adding a new output section.
- No "loading clean code..." progress message. The file is small (<2000 tokens) and loads instantly. Progress indicators for instantaneous operations erode user trust.

### 1.3 Combined loading with OOP/FP patterns

When OOP or FP patterns also load, the declaration line stacks references:

```
Language: TypeScript | Task: refactor | Reference: references/languages/typescript.md | Clean Code: default | Patterns: oop-patterns.md
```

```
Language: Scala | Task: write | Reference: references/languages/scala.md | Clean Code: default | Patterns: fp-patterns.md, oop-patterns.md
```

No special interaction message is needed. Clean code and paradigm patterns are complementary layers -- clean code covers naming, functions, error handling; paradigm patterns cover design structure. The sub-agent receives both in its prompt and applies both. There is no conflict to surface to the user.

### 1.4 Loading order (internal, not shown to user)

1. Language reference (e.g., `python.md`)
2. Clean code guide (default or custom)
3. Conditional patterns (OOP, FP, Frontend, Nx)

This order is not displayed. It matters only for prompt construction and is documented here for the architect and developer implementing it.

### 1.5 Language exception suppression (FR-03)

When a clean code violation is suppressed because it conflicts with a language idiom, the developer sees a `SUPPRESSED` notice in the review output. This makes suppressions visible without blocking the review.

**Example: Go naming convention conflict**

The clean code guide says "use descriptive multi-word names." Go idiom says receivers should be single-letter. The review output shows:

```
--- Clean Code Review ---

[CLEAN CODE] SUPPRESSED: Meaningful Names -- single-letter variable name 'r'
  File: internal/handler/user.go:15
  Reason: Go convention -- method receivers use single-letter abbreviation of type name
  Guide rule: "Avoid single-letter names except loop counters"
  Language idiom: Go Effective Go § Receivers

No actionable clean code violations found.

RESULT: PASSED
```

**What the developer learns from this:**

| Part | Purpose |
|------|---------|
| `SUPPRESSED` severity | This was checked but intentionally not enforced |
| `Reason` line | Why the suppression happened (language idiom cited) |
| `Guide rule` line | Which clean code rule would have fired |
| `Language idiom` line | Which language convention takes precedence |

Suppressions are informational only -- they never block and never count as warnings. They appear so the developer knows the system evaluated the code and made a deliberate decision, not that it missed something.

**When no suppressions occur:** Nothing is shown. Suppressions only appear when a rule was actively overridden by a language exception.

### 1.6 Godot skill declaration

The Godot skill follows the same pattern. Its declaration line already differs slightly (includes scene info); clean code appends to it:

```
Language: GDScript | Task: write | Scene: player_controller.tscn | Clean Code: default
```

---

## 2. Code Review Enforcement Flow

### 2.1 Violation message format

Every violation follows this template:

```
[CLEAN CODE] <severity>: <principle> -- <specific finding>
  File: <path>:<line range>
  Fix: <concrete action to resolve>
```

Severity levels:
- `VIOLATION` -- used in `block` mode (stops review from passing)
- `WARNING` -- used in `warn` mode (reported but review passes)

### 2.2 Block mode output (default)

When `tech_stack.clean_code_enforcement: block` (the default when key is absent):

```
--- Clean Code Review ---

[CLEAN CODE] VIOLATION: Functions -- function exceeds single responsibility
  File: src/data_processor.py:42-89
  Fix: Extract the validation logic (lines 55-78) into a separate validate_input() function

[CLEAN CODE] VIOLATION: Meaningful Names -- variable name is ambiguous
  File: src/data_processor.py:23
  Fix: Rename 'd' to 'processed_records' to convey what the variable holds

[CLEAN CODE] VIOLATION: Error Handling -- bare except clause hides errors
  File: src/data_processor.py:91
  Fix: Catch specific exceptions (e.g., ValueError, KeyError) instead of bare except

RESULT: BLOCKED -- 3 clean code violations must be resolved before review passes.
To report violations without blocking, set tech_stack.clean_code_enforcement: warn in .delivery/config.yml
```

### 2.3 Warn mode output

When `tech_stack.clean_code_enforcement: warn`:

```
--- Clean Code Review ---

[CLEAN CODE] WARNING: Functions -- function exceeds single responsibility
  File: src/data_processor.py:42-89
  Fix: Extract the validation logic (lines 55-78) into a separate validate_input() function

[CLEAN CODE] WARNING: Meaningful Names -- variable name is ambiguous
  File: src/data_processor.py:23
  Fix: Rename 'd' to 'processed_records' to convey what the variable holds

RESULT: PASSED with 2 clean code warnings.
```

### 2.4 Clean review output (no violations)

```
--- Clean Code Review ---

No clean code violations found.

RESULT: PASSED
```

### 2.5 How the developer knows what was violated and how to fix

Each message has three parts that answer distinct questions:

| Part | Question it answers | Example |
|------|-------------------|---------|
| Principle name | "What rule did I break?" | `Functions` |
| Specific finding | "What exactly is wrong?" | `function exceeds single responsibility` |
| Fix line | "How do I fix it?" | `Extract the validation logic (lines 55-78) into a separate validate_input() function` |

The principle names map directly to the 10 sections of `clean-code.md`: Meaningful Names, Functions, Comments, Formatting, Error Handling, Boundaries, Unit Tests, Classes, Emergent Design, Code Smells. This gives the developer a lookup path if they want to read the full principle.

### 2.6 Multiple files in one review

When a review covers multiple files, violations are grouped by file:

```
--- Clean Code Review ---

src/data_processor.py:
  [CLEAN CODE] VIOLATION: Functions -- function exceeds single responsibility
    File: src/data_processor.py:42-89
    Fix: Extract the validation logic (lines 55-78) into a separate validate_input() function

src/utils/helpers.py:
  [CLEAN CODE] VIOLATION: Code Smells -- dead code
    File: src/utils/helpers.py:112-130
    Fix: Remove the unused format_legacy_output() function

RESULT: BLOCKED -- 2 clean code violations across 2 files.
To report violations without blocking, set tech_stack.clean_code_enforcement: warn in .delivery/config.yml
```

---

## 3. Configuration Flow

### 3.1 Setting a custom clean code guide

The developer edits `.delivery/config.yml` directly. There is no wizard question for this -- it is an advanced configuration for teams that have their own standards. The keys are:

```yaml
tech_stack:
  languages: [python, typescript]
  clean_code_guide: .delivery/standards/coding-standards.md
  clean_code_enforcement: block
```

No confirmation message at edit time. The config file is YAML -- changes take effect on next session start or next sub-agent spawn.

### 3.2 Session start validation (config check hook)

On next session start, the config check hook (`check_config.py`) validates the custom path.

**Custom guide exists:**

```
Delivery pipeline configured (v2.3, 2026-03-27). Use delivery-team:delivery-flow to start the pipeline.
Custom clean code guide: .delivery/standards/coding-standards.md
```

This is a single info line appended to the existing config check output. It confirms which guide is active.

**Custom guide path does not exist:**

```
WARNING: Custom clean code guide not found: .delivery/standards/coding-standards.md
  The file at this path does not exist or is not readable.
  Fix: Either create the file, update the path in .delivery/config.yml under tech_stack.clean_code_guide, or remove the key to use the built-in default.
  Falling back to built-in clean-code.md for this session.
```

**Scope: file existence only (FR-17).** Session-start validation checks ONLY that the custom guide file exists and is readable. It does NOT parse, validate, or inspect the file's content or structure. Content validation is intentionally omitted -- the guide is a freeform markdown document with no required schema, and validating its structure would impose constraints on how teams write their standards. The file is loaded as-is into the sub-agent prompt at task time.

**Key design decision: graceful fallback, not hard failure.** A missing custom guide should not block the entire session. The hook warns loudly and falls back to the default. This matches the existing config check pattern -- `check_config.py` today warns about missing config but does not block session start.

### 3.3 Enforcement level switch

When a developer changes `tech_stack.clean_code_enforcement` from `block` to `warn` (or vice versa), there is no confirmation output. The change takes effect on the next code review. The review output itself communicates the active mode via the severity labels (`VIOLATION` vs `WARNING`) and the `RESULT` line.

If the key is absent or empty, the default is `block`. This is stated in the config schema but not announced at runtime -- it is the expected default behavior.

### 3.4 Invalid enforcement value

If `tech_stack.clean_code_enforcement` is set to something other than `block` or `warn`:

```
WARNING: Invalid clean_code_enforcement value: 'strict'
  Valid values: block, warn
  Defaulting to: block
```

This warning is emitted at session start by the config check hook and on first code review that encounters the invalid value.

---

## 4. Scaffold Command Flow

### 4.1 Invocation

The developer invokes the scaffold as a task through the developer skill. This is not a standalone slash command -- it follows the delivery-team pattern where skills handle specific task types.

The developer says something like:
- "Generate coding standards template"
- "Scaffold our team's coding standards"
- "Create a coding standards file"
- "Run the coding-standards task"

The developer skill recognizes this as the `coding-standards` task type.

### 4.2 Step-by-step interaction

**Step 1: Task detection and confirmation**

```
Task: coding-standards | Generating team coding standards template

Creating .delivery/standards/coding-standards.md from the built-in clean code template...
```

**Step 2: File generation (silent)**

The skill creates the directory (`.delivery/standards/`) if it does not exist, then writes the template file. No progress indicator -- this is a single file write.

**Step 3: Completion output**

```
Created: .delivery/standards/coding-standards.md

The template contains all 10 clean code sections with customization placeholders:
  1. Meaningful Names
  2. Functions
  3. Comments
  4. Formatting
  5. Error Handling
  6. Boundaries
  7. Unit Tests
  8. Classes
  9. Emergent Design
  10. Code Smells

Next step: Edit the generated file to add your team's standards, then add this to .delivery/config.yml:

  tech_stack:
    clean_code_guide: .delivery/standards/coding-standards.md
```

### 4.3 What the developer does next

1. Opens `.delivery/standards/coding-standards.md` in their editor
2. Customizes sections -- each section contains guidance comments like `<!-- Add your team's naming conventions here -->`
3. Adds the `tech_stack.clean_code_guide` key to `.delivery/config.yml`
4. Continues working -- the custom guide takes effect on next sub-agent spawn

### 4.4 File already exists

If `.delivery/standards/coding-standards.md` already exists:

```
File already exists: .delivery/standards/coding-standards.md
Overwrite? This will replace your current customizations.
```

Proceed only with explicit user confirmation. Do not silently overwrite.

---

## 5. Error States and Edge Cases

### 5.1 Custom guide file deleted after config is set

**Scenario:** Developer sets `tech_stack.clean_code_guide: .delivery/standards/coding-standards.md`, then the file is deleted (git clean, branch switch, accidental removal).

**On next session start:** The config check hook detects the missing file and produces the warning from Section 3.2. The session falls back to the built-in default. The developer sees the warning and can either restore the file or update the config.

**On sub-agent spawn mid-session (file deleted while session is running):** The developer skill attempts to read the custom file, fails, and produces:

```
WARNING: Custom clean code guide not found: .delivery/standards/coding-standards.md
  Using built-in clean-code.md for this task.
```

This is a per-task warning, not a session-blocking error. The task proceeds with the default guide.

### 5.2 Developer switches from custom back to default

**Scenario:** Developer removes the `tech_stack.clean_code_guide` key from config or sets it to an empty string.

**Behavior:** Silent. The built-in `clean-code.md` loads on the next task. The declaration line shows `Clean Code: default` instead of the custom path. No confirmation message -- absence of the key means default, which is the expected baseline.

### 5.3 Token budget exceeded (custom guide too large)

**Scenario:** A team creates a lengthy coding standards document and sets it as their custom guide.

**On session start**, if the custom guide exceeds 4000 tokens, the config check hook produces a warning:

```
WARNING: Custom clean code guide is large (~6200 tokens): .delivery/standards/coding-standards.md
  The built-in guide targets <=2000 tokens to preserve context for code generation.
  Large guides may reduce available context for complex tasks.
  Consider condensing or splitting into sections loaded on demand.
```

This is advisory only -- it does not block or truncate. The team may have good reasons for a longer guide, and truncation would produce unpredictable behavior. The warning threshold (4000 tokens) is 2x the built-in target, giving teams room to expand while flagging obvious outliers.

### 5.4 Config file exists but clean_code_guide key has invalid YAML

**Scenario:** Malformed YAML in the config file (e.g., unquoted path with special characters).

**Behavior:** This is caught by the existing config YAML parser. The config check hook already handles YAML parse errors. No new error handling needed -- the existing error path applies.

### 5.5 Both clean_code_guide and clean_code_enforcement are absent

**Scenario:** A project has `.delivery/config.yml` but neither clean code key is set (the most common case for existing projects).

**Behavior:** Completely silent. Built-in `clean-code.md` loads as default. Enforcement defaults to `block`. No messages about "using defaults" -- defaults are the expected state, not a noteworthy event.

---

## 6. Pipeline Analytics Dashboard -- Clean Code Violations (FR-22)

### 6.1 Where violation data appears

Clean code violation counts are included in the pipeline analytics dashboard alongside existing delivery metrics. The data is per-pipeline-run, not cumulative across runs.

### 6.2 Sample dashboard output

```
--- Pipeline Analytics: Run #47 ---

Stage        | Duration | Status
-------------|----------|--------
Idea         | 2m       | DONE
Refine       | 8m       | DONE
Design       | 12m      | DONE
Architect    | 15m      | DONE
Plan         | 5m       | DONE
Development  | 45m      | DONE
UAT          | 10m      | DONE

Clean Code Violations (Development stage):
  Total violations found:  7
  Resolved before pass:    7
  Unresolved (warn mode):  0

  By principle:
    Functions            3
    Meaningful Names     2
    Error Handling       1
    Code Smells          1

  By file:
    src/data_processor.py      4
    src/utils/helpers.py       2
    src/config/loader.py       1

  Enforcement mode: block
```

### 6.3 When no violations occurred

```
Clean Code Violations (Development stage):
  Total violations found:  0
  No clean code violations were detected during this run.
```

### 6.4 Data source

Violation counts are collected from code review outputs during the Development stage. No separate database or persistence is needed -- the analytics dashboard reads from the existing pipeline run artifacts.

---

## 7. Dogfooding Review Format (FR-23)

### 7.1 Format reuse

The dogfooding review (where the delivery-team validates its own changes by using them) uses the **same code review output format** defined in Section 2. There are no format differences -- dogfooding reviews produce the same `[CLEAN CODE]` violation messages, the same severity levels, and the same `RESULT` line.

### 7.2 Rationale

Dogfooding means using the feature as a real user would. Using a different review format for internal validation would defeat the purpose. If the standard format is insufficient for dogfooding, that is a signal the standard format needs improvement -- not that dogfooding needs a special format.

### 7.3 What makes a dogfooding review different

The difference is not in output format but in scope and intent:

| Aspect | Standard code review | Dogfooding review |
|--------|---------------------|-------------------|
| **Who triggers it** | Developer during normal workflow | Team during validation of the clean code feature itself |
| **What is reviewed** | Application code | The clean code guide, hook scripts, and skill changes |
| **Output format** | Section 2 format | Section 2 format (identical) |
| **Purpose** | Enforce coding standards | Confirm the feature works correctly end-to-end |

---

## Flow Summary

```
Session Start
    |
    v
Config check hook runs
    |
    +--> tech_stack.clean_code_guide set?
    |       |
    |       +--> YES: File exists?
    |       |       |
    |       |       +--> YES: "Custom clean code guide: <path>" (info)
    |       |       |
    |       |       +--> NO: "WARNING: not found..." (warn + fallback to default)
    |       |
    |       +--> NO: Silent (default guide, no message)
    |
    v
Developer/Godot task triggered
    |
    v
Declaration line printed: "... | Clean Code: default|<path>"
    |
    v
Sub-agent spawned with:
  1. Language reference
  2. Clean code guide (custom or default)
  3. Conditional patterns (OOP/FP/Frontend/Nx)
    |
    v
Code review requested
    |
    v
Review checks code against clean code guide
    |
    +--> Violations found?
    |       |
    |       +--> YES + block mode: BLOCKED with violation details
    |       |
    |       +--> YES + warn mode: PASSED with warning details
    |       |
    |       +--> NO: PASSED (clean)
    |
    v
Done
```

---

## Design Validation Checklist

| PRD Requirement | Addressed In |
|-----------------|-------------|
| FR-01: Built-in clean-code.md reference file | Section 1.1 (default guide, declaration line shows `Clean Code: default`) |
| FR-02: 10 clean code principles coverage | Section 4.3, Section 2.5 (principle names map to 10 sections) |
| FR-03: Language-specific exceptions | Section 1.5 (suppression UX with SUPPRESSED severity) |
| FR-04: Token budget target (<=2000 tokens) | Section 5.3 (warning when custom guide exceeds 4000 tokens) |
| FR-05: Automatic loading on developer tasks | Section 1 (silent loading, declaration line) |
| FR-06: Automatic loading on Godot tasks | Section 1.6 (Godot declaration line) |
| FR-07: Loading order (lang -> clean code -> patterns) | Section 1.4 |
| FR-08: Not conditional, not in routing table | Section 1.1 (always loads, no opt-in) |
| FR-09: Code review checks against clean code guide | Section 2 (violation format, block/warn modes) |
| FR-10: Violations cite principle and provide fix | Section 2.5 (three-part message design) |
| FR-11: Block/warn config | Section 3.3 (enforcement level switch) |
| FR-12: Violation messages cite principle + config path | Section 2.2, 2.5 |
| FR-13: Custom guide via config key | Section 3.1 |
| FR-14: Custom guide overrides default | Section 3.1, 1.1 (declaration line shows custom path) |
| FR-15: Custom guide fallback on missing file | Section 3.2, 5.1 (graceful fallback) |
| FR-16: Config check validates path at session start | Section 3.2 |
| FR-17: Session-start checks file existence only, not content | Section 3.2 (explicit no-content-validation statement) |
| FR-18: Scaffold command generates template | Section 4.1, 4.2 |
| FR-19: Template contains all 10 sections | Section 4.2 (completion output lists all 10) |
| FR-20: Template includes customization placeholders | Section 4.3 (guidance comments) |
| FR-21: Scaffold warns before overwriting existing file | Section 4.4 |
| FR-22: Analytics dashboard shows violation data | Section 6 (sample output with counts per principle/file) |
| FR-23: Dogfooding uses standard review format | Section 7 (format reuse confirmation) |
| US-08: Clear error messages for violations | Section 2.5 (three-part message design) |
