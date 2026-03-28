# Sprint Plan: Clean Code Foundational Standards

**Version**: 1.0
**Date**: 2026-03-27
**Author**: Product Owner (delivery-team)
**Total Points**: 41
**Sprints**: 4
**Inputs**: PRD v1.0, Architecture v1.0

---

## Capacity & Velocity

| Metric | Value |
|--------|-------|
| Team size | 4 (plugin development team) |
| Velocity baseline | 14 pts/sprint |
| Available capacity | 14 pts/sprint (no known absences) |
| Commitment ceiling (80%) | 11.2 pts max per sprint |

**Sprint commitment validation** (all sprints within 80% ceiling):

| Sprint | Committed | Ceiling | Within? |
|--------|-----------|---------|---------|
| Sprint 1 | 11 pts | 11.2 pts | Yes |
| Sprint 2 | 11 pts | 11.2 pts | Yes |
| Sprint 3 | 8 pts | 11.2 pts | Yes |
| Sprint 4 | 11 pts | 11.2 pts | Yes |

---

## Sprint 1: Foundation (11 pts)

### Story 1.1: Create `clean-code.md` Reference

**Points**: 8
**FRs**: FR-01, FR-02, FR-03, FR-04
**Priority**: P0

> As a developer using the developer or Godot skill,
> I want a language-agnostic clean code reference covering 10 foundational sections with actionable principles,
> So that all generated code follows established best practices regardless of language.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-1.1.1 | **Given** the file `delivery-team/skills/developer/references/clean-code.md` exists, **When** I inspect its structure, **Then** it contains exactly 10 sections: Meaningful Names, Functions, Comments, Formatting, Error Handling, Boundaries, Unit Tests, Classes, Emergent Design, Code Smells. |
| AC-1.1.2 | **Given** the file `clean-code.md`, **When** I count its tokens using a tokenizer, **Then** the count is at or below 2000 tokens. |
| AC-1.1.3 | **Given** the file `clean-code.md`, **When** I inspect the content, **Then** each section contains actionable principles (imperative statements, not theory or history) and no code examples. |
| AC-1.1.4 | **Given** the file `clean-code.md`, **When** I look for a language-specific exceptions subsection, **Then** it exists and covers at minimum Python, GDScript, and Go naming convention exceptions. |
| AC-1.1.5 | **Given** the file `clean-code.md` and the existing `oop-patterns.md`, **When** I compare the Classes section of `clean-code.md` against the SOLID definitions in `oop-patterns.md`, **Then** there is no overlap -- `clean-code.md` references SRP at a practical level (class size, cohesion) without redefining SOLID. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-1.1.1a | AC-1.1.1 | Verify file exists at `delivery-team/skills/developer/references/clean-code.md`. Parse headings and confirm all 10 sections are present as H2 or H3 headers. |
| TC-1.1.1b | AC-1.1.1 | Verify no extra top-level sections exist beyond the 10 specified plus language exceptions. |
| TC-1.1.2a | AC-1.1.2 | Run a tokenizer (e.g., `tiktoken` cl100k_base or chars/4 approximation) against the file. Assert count <= 2000. |
| TC-1.1.3a | AC-1.1.3 | Grep for fenced code blocks (triple backticks). Assert zero matches. |
| TC-1.1.3b | AC-1.1.3 | Review each section and confirm at least 3 actionable principle statements per section (imperative voice: "Use...", "Avoid...", "Keep..."). |
| TC-1.1.4a | AC-1.1.4 | Search for "Python", "GDScript", and "Go" within the language exceptions subsection. Assert all three are mentioned with specific exception guidance. |
| TC-1.1.5a | AC-1.1.5 | Search `clean-code.md` Classes section for the terms "Single Responsibility Principle", "Open/Closed", "Liskov", "Interface Segregation", "Dependency Inversion". Assert none appear as definitions. Confirm SRP is referenced only by application (e.g., class size limits, cohesion checks). |
| TC-1.1.5b | AC-1.1.5 | Diff the Classes section of `clean-code.md` against the SOLID section of `oop-patterns.md`. Assert no duplicated sentences or paragraphs. |

---

### Story 1.2: Create `clean-code-review-checklist.md`

**Points**: 3
**FRs**: Derived from FR-09, FR-10 (architecture Section 1.1)
**Priority**: P0

> As a code reviewer using the PR review toolkit,
> I want a condensed clean code review checklist optimized for review context,
> So that PR reviews have a consistent, objective reference with pass/fail criteria for each principle.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-1.2.1 | **Given** the file `delivery-team/skills/developer/references/clean-code-review-checklist.md` exists, **When** I inspect its structure, **Then** it maps all 10 sections from `clean-code.md` to pass/fail review criteria. |
| AC-1.2.2 | **Given** the checklist file, **When** I count its tokens, **Then** the count is at or below 800 tokens. |
| AC-1.2.3 | **Given** the checklist file, **When** I compare it to `clean-code.md`, **Then** every section in `clean-code.md` has a corresponding checklist entry -- no sections are missing. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-1.2.1a | AC-1.2.1 | Parse the checklist and verify each of the 10 sections has at least one pass/fail criterion. |
| TC-1.2.1b | AC-1.2.1 | Verify each criterion is phrased as a binary check (pass or fail), not as guidance or advice. |
| TC-1.2.2a | AC-1.2.2 | Run tokenizer against the file. Assert count <= 800. |
| TC-1.2.3a | AC-1.2.3 | Extract section names from both files. Assert the checklist covers all 10 sections from the reference. |

---

## Sprint 2: Integration (11 pts)

### Story 2.1: Add Foundational Clean Code Loading to Developer SKILL.md

**Points**: 5
**FRs**: FR-05, FR-07, FR-08
**Priority**: P0
**Dependencies**: Stories 1.1, 1.2

> As a developer using the developer skill,
> I want clean code principles loaded automatically into every sub-agent prompt after the language reference and before conditional patterns,
> So that generated code follows clean code standards without requiring me to opt in.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-2.1.1 | **Given** the developer SKILL.md Sub-Agent Prompt Template, **When** I inspect the template structure, **Then** a `## Clean Code Standards` block appears after the language reference block and before the `## Task` section (or any conditional pattern blocks). |
| AC-2.1.2 | **Given** any of the 14 supported languages, **When** a developer sub-agent is spawned, **Then** the prompt includes the clean code guide content. |
| AC-2.1.3 | **Given** the cross-language routing table in developer SKILL.md, **When** I inspect it, **Then** clean code is NOT listed as a conditional entry -- it loads independently of `tech_stack` config values. |
| AC-2.1.4 | **Given** the developer SKILL.md declaration line template, **When** I inspect it, **Then** it includes a `Clean Code: [default | <custom-path>]` field. |
| AC-2.1.5 | **Given** a task type of `review`, **When** a developer sub-agent is spawned, **Then** the prompt also includes `clean-code-review-checklist.md` content and enforcement mode behavior. |
| AC-2.1.6 | **Given** the developer SKILL.md References section, **When** I inspect it, **Then** both `clean-code.md` and `clean-code-review-checklist.md` are listed. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-2.1.1a | AC-2.1.1 | Read developer SKILL.md. Locate the Sub-Agent Prompt Template. Verify `## Clean Code Standards` heading exists between the language reference `---` separator and the `## Task` heading. |
| TC-2.1.2a | AC-2.1.2 | Spawn a developer sub-agent for Python. Inspect the assembled prompt. Assert it contains clean code content. Repeat for at least 2 other languages (e.g., Go, TypeScript). |
| TC-2.1.3a | AC-2.1.3 | Read the routing table. Assert no row references `clean-code.md`. Assert no conditional logic gates clean code loading on any config value. |
| TC-2.1.4a | AC-2.1.4 | Search the declaration line template for `Clean Code:`. Assert the field is present with the format `[default | <custom-path>]`. |
| TC-2.1.5a | AC-2.1.5 | Spawn a developer sub-agent with task type `review`. Verify the prompt contains `clean-code-review-checklist.md` content. Verify the prompt contains enforcement mode instructions (block/warn behavior). |
| TC-2.1.6a | AC-2.1.6 | Search the References section for both `clean-code.md` and `clean-code-review-checklist.md`. Assert both are listed. |
| TC-2.1.7a | AC-2.1.4 (FR-14) | Set `tech_stack.clean_code_guide` to a custom file path (e.g., `.delivery/standards/coding-standards.md`). Create the custom file with unique content. Spawn a developer sub-agent. Assert the prompt contains ONLY the custom guide content and does NOT contain any content from the default `clean-code.md`. |
| TC-2.1.8a | AC-2.1.4 (FR-15) | Remove the `tech_stack.clean_code_guide` key from config entirely. Spawn a developer sub-agent. Assert the prompt contains the default `clean-code.md` content. |
| TC-2.1.8b | AC-2.1.4 (FR-15) | Set `tech_stack.clean_code_guide: ""` (empty string) in config. Spawn a developer sub-agent. Assert the prompt contains the default `clean-code.md` content. |

---

### Story 2.2: Add Foundational Clean Code Loading to Godot SKILL.md

**Points**: 3
**FRs**: FR-06
**Priority**: P0
**Dependencies**: Story 1.1

> As a Godot developer using the Godot skill,
> I want clean code principles loaded automatically into every Godot sub-agent prompt,
> So that GDScript and C# game code receives the same clean code standards as application code.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-2.2.1 | **Given** the Godot SKILL.md Sub-Agent Prompt Template, **When** I inspect the template structure, **Then** a `## Clean Code Standards` block appears after the Godot reference files block and before the `## Task` section. |
| AC-2.2.2 | **Given** the Godot SKILL.md, **When** it references the clean code file, **Then** it reads from the developer skill's `references/clean-code.md` path (shared file, not a copy). |
| AC-2.2.3 | **Given** the Godot SKILL.md declaration line template, **When** I inspect it, **Then** it includes a `Clean Code: [default | <custom-path>]` field. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-2.2.1a | AC-2.2.1 | Read Godot SKILL.md. Locate the Sub-Agent Prompt Template. Verify `## Clean Code Standards` heading exists between the reference files `---` separator and the `## Task` heading. |
| TC-2.2.2a | AC-2.2.2 | Search Godot SKILL.md for the clean code file path. Assert it references `delivery-team/skills/developer/references/clean-code.md` or a relative path resolving to the same location. Assert no file named `clean-code.md` exists under `delivery-team/skills/godot/`. |
| TC-2.2.3a | AC-2.2.3 | Search the Godot declaration line template for `Clean Code:`. Assert the field is present. |

---

### Story 2.3: Update Config Schema to v2.3

**Points**: 3
**FRs**: FR-13, FR-11
**Priority**: P0
**Dependencies**: None (can start in parallel with Stories 2.1/2.2)

> As a team lead,
> I want `tech_stack.clean_code_guide` and `tech_stack.clean_code_enforcement` config keys defined in the schema,
> So that teams can point to custom coding standards and control enforcement level through the standard config mechanism.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-2.3.1 | **Given** the file `config-schema.md`, **When** I inspect the Complete Schema table, **Then** `tech_stack.clean_code_guide` is defined as type `string`, not required, default `""`, with valid values of file path or empty string. |
| AC-2.3.2 | **Given** the file `config-schema.md`, **When** I inspect the Complete Schema table, **Then** `tech_stack.clean_code_enforcement` is defined as type `string`, not required, default `"block"`, with valid values `block` and `warn`. |
| AC-2.3.3 | **Given** the file `config-schema.md`, **When** I check the `config_version` default, **Then** it reads `"2.3"`. |
| AC-2.3.4 | **Given** the Config File Template in `config-schema.md`, **When** I inspect the `tech_stack` section, **Then** both `clean_code_guide: ""` and `clean_code_enforcement: block` are present. |
| AC-2.3.5 | **Given** the Version History table, **When** I inspect it, **Then** a v2.3 entry exists dated 2026-03-27 describing the two new keys. |
| AC-2.3.6 | **Given** existing configs without the new keys, **When** they are loaded, **Then** default behavior applies (built-in guide, block enforcement) with no errors. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-2.3.1a | AC-2.3.1 | Read `config-schema.md`. Search for `clean_code_guide` in the schema table. Verify type, required, default, and valid values columns match specification. |
| TC-2.3.2a | AC-2.3.2 | Read `config-schema.md`. Search for `clean_code_enforcement` in the schema table. Verify type, required, default, and valid values columns match specification. |
| TC-2.3.3a | AC-2.3.3 | Search `config-schema.md` for `config_version`. Assert default is `"2.3"`. |
| TC-2.3.4a | AC-2.3.4 | Locate the Config File Template YAML block. Assert it contains `clean_code_guide: ""` and `clean_code_enforcement: block` under `tech_stack`. |
| TC-2.3.5a | AC-2.3.5 | Search the Version History table for a row with version `2.3`. Assert it exists and describes both new keys. |
| TC-2.3.6a | AC-2.3.6 | Create a test config with `config_version: "2.2"` and no `clean_code_guide` or `clean_code_enforcement` keys. Run config parsing logic. Assert no errors and defaults are applied (built-in guide, block enforcement). |
| TC-2.3.6b | AC-2.3.6 | Run `python delivery-team/scripts/generate-schema.py` after schema update. Assert it produces valid JSON without errors. |

---

## Sprint 3: Config & Enforcement (8 pts)

### Story 3.1: Add Config Check Hook Validation for Custom Guide

**Points**: 3
**FRs**: FR-16, FR-17
**Priority**: P0
**Dependencies**: Story 2.3

> As a team lead with a custom coding standards file,
> I want the config check hook to validate that my custom guide path exists at session start,
> So that broken paths fail fast with clear instructions instead of silently falling back.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-3.1.1 | **Given** a `.delivery/config.yml` with `tech_stack.clean_code_guide` pointing to an existing file, **When** a session starts, **Then** the hook emits an info message confirming the custom guide is active and shows the path. |
| AC-3.1.2 | **Given** a `.delivery/config.yml` with `tech_stack.clean_code_guide` pointing to a non-existent file, **When** a session starts, **Then** the hook emits a WARNING with: the missing path, a fix instruction (create the file, update the path, or remove the key), and a note that the built-in default will be used for this session. |
| AC-3.1.3 | **Given** a `.delivery/config.yml` with `tech_stack.clean_code_enforcement` set to an invalid value (not `block` or `warn`), **When** a session starts, **Then** the hook emits a WARNING stating the invalid value, listing valid values, and confirming the default (`block`) will be used. |
| AC-3.1.4 | **Given** a custom guide file exceeding 4000 tokens, **When** a session starts, **Then** the hook emits a WARNING about the large file size with the estimated token count and a note about context impact. |
| AC-3.1.5 | **Given** a `.delivery/config.yml` with no `clean_code_guide` key, **When** a session starts, **Then** no clean-code-related warnings or info messages are emitted -- existing behavior is unchanged. |
| AC-3.1.6 | **Given** any custom guide validation, **When** the hook checks the file, **Then** it validates file existence only -- it does NOT inspect or validate the file's content structure. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-3.1.1a | AC-3.1.1 | Set `clean_code_guide: .delivery/standards/coding-standards.md` in config. Create the file. Run hook. Assert output contains "Custom clean code guide:" and the path. |
| TC-3.1.2a | AC-3.1.2 | Set `clean_code_guide: nonexistent/path.md` in config. Run hook. Assert output contains "WARNING", "not found", the path, and fix instructions mentioning three options (create, update path, remove key). |
| TC-3.1.3a | AC-3.1.3 | Set `clean_code_enforcement: strict` in config. Run hook. Assert output contains "WARNING", "Invalid", "strict", and lists "block, warn" as valid values. |
| TC-3.1.4a | AC-3.1.4 | Create a custom guide file >16000 characters (>4000 estimated tokens). Set config to point to it. Run hook. Assert output contains "WARNING" and "large" and an estimated token count. |
| TC-3.1.5a | AC-3.1.5 | Use a config with no `clean_code_guide` key. Run hook. Assert output does NOT contain "clean code guide" or related messages. |
| TC-3.1.6a | AC-3.1.6 | Create a custom guide file with random text (not valid coding standards). Set config to point to it. Run hook. Assert no warnings about content -- only the info message confirming the guide is active. |

---

### Story 3.2: Add Clean Code Enforcement to Code Review Flow

**Points**: 5
**FRs**: FR-09, FR-10, FR-11, FR-12
**Priority**: P0
**Dependencies**: Stories 1.2, 2.1

> As a code reviewer,
> I want PR reviews to check code against clean code principles with configurable enforcement (block/warn) and clear violation messages citing specific principles,
> So that review feedback is objective, consistent, and actionable.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-3.2.1 | **Given** a developer sub-agent spawned with task type `review`, **When** the prompt is assembled, **Then** it includes the `clean-code-review-checklist.md` content. |
| AC-3.2.2 | **Given** `tech_stack.clean_code_enforcement` set to `block` (or absent/default), **When** the review finds clean code violations, **Then** each violation uses `VIOLATION` severity and the result line says `BLOCKED`. |
| AC-3.2.3 | **Given** `tech_stack.clean_code_enforcement` set to `warn`, **When** the review finds clean code violations, **Then** each violation uses `WARNING` severity and the result line says `PASSED with N warnings`. |
| AC-3.2.4 | **Given** a clean code violation found during review, **When** the violation message is formatted, **Then** it names the specific principle violated (e.g., "Functions: exceeds single responsibility") and states "Configure via tech_stack.clean_code_enforcement". |
| AC-3.2.5 | **Given** the `pr-review-toolkit:code-reviewer` delegates to the developer skill, **When** it invokes task type `review`, **Then** clean code enforcement is inherited via session context -- no modifications to `pr-review-toolkit` files are needed. |
| AC-3.2.6 | **Given** the `pr-review-toolkit:code-simplifier` delegates to the developer skill, **When** it invokes a simplification task, **Then** the clean code guide content is available in the prompt for reference. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-3.2.1a | AC-3.2.1 | Spawn a developer sub-agent with task type `review`. Inspect the prompt. Assert it contains content from `clean-code-review-checklist.md` (verify at least 3 checklist items are present). |
| TC-3.2.2a | AC-3.2.2 | Set enforcement to `block` (or remove the key for default). Submit code with a known violation (e.g., a 50-line function). Assert the review output contains `VIOLATION` and `BLOCKED`. |
| TC-3.2.2b | AC-3.2.2 | Submit code with no violations. Assert the review output does NOT contain `BLOCKED`. |
| TC-3.2.3a | AC-3.2.3 | Set enforcement to `warn`. Submit code with a known violation. Assert the review output contains `WARNING` and `PASSED with` and a warning count. |
| TC-3.2.4a | AC-3.2.4 | Trigger a violation. Inspect the violation message text. Assert it contains a principle name from one of the 10 sections (e.g., "Functions:", "Meaningful Names:"). Assert it contains the string "tech_stack.clean_code_enforcement". |
| TC-3.2.5a | AC-3.2.5 | Verify no files under `pr-review-toolkit/` are modified. Assert clean code enforcement works end-to-end through the delegation chain by running a code review via `pr-review-toolkit:code-reviewer`. |
| TC-3.2.6a | AC-3.2.6 | Inspect the developer skill prompt for a non-review task. Assert `clean-code.md` content is present (covers `code-simplifier` delegation). |

---

## Sprint 4: Scaffold & Polish (11 pts)

### Story 4.1: Implement `coding-standards` Scaffold Task Type

**Points**: 5
**FRs**: FR-18, FR-19, FR-20, FR-21
**Priority**: P1
**Dependencies**: Story 2.1

> As a team lead,
> I want to invoke a `coding-standards` task in the developer skill that generates a starter template pre-populated with all 10 sections and customization placeholders,
> So that I have a structured starting point for defining my team's coding standards.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-4.1.1 | **Given** the developer SKILL.md Task Type Instructions table, **When** I inspect it, **Then** a `coding-standards` task type row exists describing the scaffold behavior. |
| AC-4.1.2 | **Given** a user invokes the `coding-standards` task type, **When** the sub-agent runs, **Then** it generates a file at `.delivery/standards/coding-standards.md`. |
| AC-4.1.3 | **Given** the generated template file, **When** I inspect its structure, **Then** it contains all 10 sections from the built-in `clean-code.md` (Meaningful Names, Functions, Comments, Formatting, Error Handling, Boundaries, Unit Tests, Classes, Emergent Design, Code Smells). |
| AC-4.1.4 | **Given** the generated template file, **When** I inspect each section, **Then** customization placeholders with HTML comment guidance are present (e.g., `<!-- Add your team's naming conventions here -->`). |
| AC-4.1.5 | **Given** the scaffold completes, **When** the sub-agent outputs its post-generation message, **Then** it includes an instruction to set `tech_stack.clean_code_guide: .delivery/standards/coding-standards.md` in `.delivery/config.yml`. |
| AC-4.1.6 | **Given** a file already exists at `.delivery/standards/coding-standards.md`, **When** the scaffold task is invoked, **Then** the sub-agent checks for the existing file and warns before overwriting. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-4.1.1a | AC-4.1.1 | Read developer SKILL.md. Locate the Task Type Instructions table. Assert a row with `coding-standards` exists and its description mentions template generation. |
| TC-4.1.2a | AC-4.1.2 | Run the `coding-standards` task type. Assert file exists at `.delivery/standards/coding-standards.md`. |
| TC-4.1.3a | AC-4.1.3 | Read the generated file. Parse headings. Assert all 10 section names are present. |
| TC-4.1.4a | AC-4.1.4 | Search the generated file for HTML comment placeholders (`<!-- ... -->`). Assert at least 5 placeholder comments exist across the 10 sections. |
| TC-4.1.4b | AC-4.1.4 | Verify placeholder comments contain actionable guidance (e.g., "Add your team's...", "Customize...", "Define your..."). |
| TC-4.1.5a | AC-4.1.5 | Run the scaffold task. Capture the sub-agent output text. Assert it mentions `tech_stack.clean_code_guide` and the path `.delivery/standards/coding-standards.md`. |
| TC-4.1.6a | AC-4.1.6 | Create a file at `.delivery/standards/coding-standards.md` with content. Run the scaffold task again. Assert the sub-agent warns about the existing file before proceeding. |

---

### Story 4.2: Pipeline Analytics Integration

**Points**: 3
**FRs**: FR-22
**Priority**: P2
**Dependencies**: Story 3.2

> As a team lead,
> I want clean code violation counts tracked per pipeline run in the analytics dashboard,
> So that I can observe quality trends over time and measure whether clean code adoption is improving.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-4.2.1 | **Given** a pipeline run that includes code review with clean code enforcement, **When** the run completes, **Then** the violation count for that run is recorded in the analytics data store. |
| AC-4.2.2 | **Given** recorded violation data, **When** I query the analytics dashboard, **Then** violation counts are visible per pipeline run with timestamps. |
| AC-4.2.3 | **Given** multiple pipeline runs with violation data, **When** I view the analytics, **Then** I can observe a trend over time (violation counts per run, chronologically ordered). |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-4.2.1a | AC-4.2.1 | Run a pipeline with code that triggers 3 clean code violations. After completion, query the analytics data store. Assert a record exists with violation_count = 3 and the correct pipeline run ID. |
| TC-4.2.1b | AC-4.2.1 | Run a pipeline with no violations. Assert a record exists with violation_count = 0. |
| TC-4.2.2a | AC-4.2.2 | Query the analytics dashboard output. Assert violation count data includes a run identifier and a timestamp. |
| TC-4.2.3a | AC-4.2.3 | Generate 3 pipeline runs with varying violation counts (5, 3, 1). Query analytics. Assert all three entries appear in chronological order. |

---

### Story 4.3: Dogfooding Pass on Repo Python Scripts

**Points**: 3
**FRs**: FR-23
**Priority**: P0
**Dependencies**: Stories 1.1, 1.2, 3.2

> As a delivery team member,
> I want all existing Python scripts in the repo reviewed against the clean code standards before shipping,
> So that the feature is validated by applying it to our own codebase and we practice what we preach.

**Acceptance Criteria**:

| AC | Criteria |
|----|----------|
| AC-4.3.1 | **Given** all Python scripts in `delivery-team/hooks/*.py`, **When** reviewed against the clean code guide at `warn` level, **Then** each script either passes or has findings documented. |
| AC-4.3.2 | **Given** all Python scripts in `delivery-team/scripts/*.py`, **When** reviewed against the clean code guide at `warn` level, **Then** each script either passes or has findings documented. |
| AC-4.3.3 | **Given** all Python scripts in `prd-quality-gate-flow/*.py`, **When** reviewed against the clean code guide at `warn` level, **Then** each script either passes or has findings documented. |
| AC-4.3.4 | **Given** documented findings from the review, **When** critical violations are identified (functions > 30 lines, unclear names, missing error handling), **Then** they are either fixed or tracked as tech debt with justification. |
| AC-4.3.5 | **Given** the dogfooding review is complete, **When** a review summary is produced, **Then** it lists each file reviewed, its pass/warn status, and any findings -- validating both the reference content and the enforcement mechanism. |

**Test Cases**:

| TC | For AC | Test |
|----|--------|------|
| TC-4.3.1a | AC-4.3.1 | List all `*.py` files in `delivery-team/hooks/`. For each, run the developer skill `review` task type with enforcement `warn`. Assert each produces a review result (PASSED or PASSED with N warnings). |
| TC-4.3.2a | AC-4.3.2 | List all `*.py` files in `delivery-team/scripts/`. For each, run review. Assert each produces a review result. |
| TC-4.3.3a | AC-4.3.3 | List all `*.py` files in `prd-quality-gate-flow/`. For each, run review. Assert each produces a review result. |
| TC-4.3.4a | AC-4.3.4 | Inspect all findings with `WARNING` severity. For each, assert it is either (a) fixed in a commit, or (b) documented as accepted tech debt with a rationale. |
| TC-4.3.5a | AC-4.3.5 | Verify a review summary artifact exists listing every reviewed file, its status, and findings. Assert no files from the three directories are missing from the summary. |

---

## Summary

| Sprint | Stories | Points | Key Deliverables |
|--------|---------|--------|-----------------|
| Sprint 1 | 1.1, 1.2 | 11 | `clean-code.md`, `clean-code-review-checklist.md` |
| Sprint 2 | 2.1, 2.2, 2.3 | 11 | Developer SKILL.md integration, Godot SKILL.md integration, config schema v2.3 |
| Sprint 3 | 3.1, 3.2 | 8 | Config check hook validation, code review enforcement |
| Sprint 4 | 4.1, 4.2, 4.3 | 11 | Scaffold task type, analytics integration, dogfooding validation |
| **Total** | **10** | **41** | |

## Dependency Graph

```
Story 1.1 (clean-code.md)
  ├── Story 1.2 (review checklist) ──── Story 3.2 (enforcement)
  ├── Story 2.1 (developer SKILL.md) ── Story 3.2 (enforcement)
  │                                  └── Story 4.1 (scaffold)
  ├── Story 2.2 (godot SKILL.md)
  └── Story 4.3 (dogfooding) ────────── Story 3.2 (enforcement)

Story 2.3 (config schema) ──────────── Story 3.1 (config hook)

Story 3.2 (enforcement) ────────────── Story 4.2 (analytics)
```
