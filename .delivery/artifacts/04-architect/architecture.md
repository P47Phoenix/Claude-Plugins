# Technical Architecture: Clean Code Foundational Standards

**Version**: 1.0
**Date**: 2026-03-27
**Author**: Solution Architect (delivery-team)
**Status**: Draft
**Inputs**: PRD v1.0, UX Design v1.0, Developer SKILL.md, Godot SKILL.md, Config Schema v2.2, Config Check Hook

---

## 1. Component Map

### 1.1 New Files

| File | Description |
|------|-------------|
| `delivery-team/skills/developer/references/clean-code.md` | Language-agnostic clean code reference. 10 sections (Meaningful Names, Functions, Comments, Formatting, Error Handling, Boundaries, Unit Tests, Classes, Emergent Design, Code Smells). Actionable principles only, no code examples. Language-specific exceptions subsection covering Python, GDScript, Go naming conventions. Target: <=2000 tokens. |
| `delivery-team/skills/developer/references/clean-code-review-checklist.md` | Condensed checklist version of clean-code.md optimized for PR review context. Maps each of the 10 sections to pass/fail criteria. Used by PR review toolkit session context. Target: <=800 tokens. |

### 1.2 Modified Files

| File | Change Description |
|------|-------------------|
| `delivery-team/skills/developer/SKILL.md` | (1) Add clean code loading instruction to Sub-Agent Prompt Template -- insert clean code content block between language reference and task section. (2) Add `Clean Code:` field to declaration line template. (3) Add `coding-standards` task type to Task Type Instructions table. (4) Add `clean-code.md` and `clean-code-review-checklist.md` to References section. |
| `delivery-team/skills/godot/SKILL.md` | (1) Add clean code loading instruction to Sub-Agent Prompt Template -- insert clean code content block between reference files and task section. (2) Add `Clean Code:` field to declaration line template. |
| `delivery-team/hooks/check_config.py` | (1) Add validation of `tech_stack.clean_code_guide` custom path existence. (2) Add validation of `tech_stack.clean_code_enforcement` value (block/warn). (3) Add token size warning for custom guides exceeding 4000 tokens. (4) Add info line confirming which guide is active when custom path is set. |
| `delivery-team/skills/delivery-flow/references/config-schema.md` | (1) Add `tech_stack.clean_code_guide` key. (2) Add `tech_stack.clean_code_enforcement` key. (3) Bump `config_version` from 2.2 to 2.3. (4) Update Config File Template with new keys. (5) Add Version History entry for v2.3. |
| `delivery-team/scripts/generate-schema.py` | Regenerate `config-schema.json` after schema update (Step 6.5 of extension protocol). No hand-edits to JSON. |

### 1.3 Files NOT Modified (Session Context Approach)

| File | Rationale |
|------|-----------|
| `pr-review-toolkit` plugin files | PR review integration uses session context injection, not file modification. The developer skill loads `clean-code-review-checklist.md` into the sub-agent prompt when the task type is `review`. The PR review toolkit's `code-reviewer` and `code-simplifier` agents inherit this context because they delegate to the developer skill. No changes to external plugin files required. |

---

## 2. Integration Points

### 2.1 Developer Skill Sub-Agent Prompt Template

**Insertion point**: Between the language reference block and the `## Task` section in the Sub-Agent Prompt Template (SKILL.md lines 65-92).

**Current template structure**:

```
You are an expert [LANGUAGE] developer. Apply these coding standards...

---
[PASTE FULL CONTENTS OF references/languages/<lang>.md HERE]
---

## Task
```

**New template structure**:

```
You are an expert [LANGUAGE] developer. Apply these coding standards...

---
[PASTE FULL CONTENTS OF references/languages/<lang>.md HERE]
---

## Clean Code Standards

[PASTE FULL CONTENTS OF clean code guide HERE -- either references/clean-code.md or custom guide from config]

---

[CONDITIONAL: OOP/FP/Frontend/Nx patterns inserted here by existing routing logic]

## Task
```

**Loading order enforced**: Language reference -> Clean code guide -> Conditional patterns (OOP/FP/Frontend/Nx) -> Task description. This matches FR-07.

**Declaration line change** (SKILL.md line 47):

Current:
```
Language: [LANG] | Task: [write / fix / refactor / review / test / explain] | Reference: references/languages/<lang>.md
```

New:
```
Language: [LANG] | Task: [write / fix / refactor / review / test / explain] | Reference: references/languages/<lang>.md | Clean Code: [default | <custom-path>]
```

**Review task type addition**: When task type is `review`, also load `clean-code-review-checklist.md` and append review instructions that cite specific principles, enforce block/warn behavior per `tech_stack.clean_code_enforcement`, and format violations per the UX design template.

**Coding-standards task type addition** (Task Type Instructions table):

| Task Type | What the sub-agent does |
|---|---|
| **coding-standards** | Generate `.delivery/standards/coding-standards.md` template from the built-in clean code reference. All 10 sections with customization placeholders. Output config instruction for `tech_stack.clean_code_guide`. Check for existing file before overwriting. |

### 2.2 Godot Skill Sub-Agent Prompt Template

**Insertion point**: Between the reference files block and the `## Task` section in the Sub-Agent Prompt Template (SKILL.md lines 63-107).

**Current template structure**:

```
You are an expert Godot 4.x game developer. Apply these best practices...

---
[PASTE FULL CONTENTS OF EACH RELEVANT REFERENCE FILE]
---

## Task
```

**New template structure**:

```
You are an expert Godot 4.x game developer. Apply these best practices...

---
[PASTE FULL CONTENTS OF EACH RELEVANT REFERENCE FILE]
---

## Clean Code Standards

[PASTE FULL CONTENTS OF clean code guide HERE -- either references/clean-code.md or custom guide from config]

---

## Task
```

**Declaration line change** (SKILL.md line 44):

Current:
```
Language: [GDScript | C#] | Task: [...] | References: [list of reference files used]
```

New:
```
Language: [GDScript | C#] | Task: [...] | References: [list of reference files used] | Clean Code: [default | <custom-path>]
```

**Note**: The Godot skill does NOT have its own copy of `clean-code.md`. It reads from the developer skill's `references/clean-code.md` path. One file, two consumers.

### 2.3 PR Review Toolkit (Session Context Approach)

The PR review toolkit is an external plugin (`pr-review-toolkit`). We do NOT modify its files. Instead, integration works through the existing delegation chain:

1. `pr-review-toolkit:code-reviewer` delegates code review work to `delivery-team:developer` with task type `review`.
2. The developer skill's `review` task type already loads clean code context into the sub-agent prompt (Section 2.1).
3. The sub-agent receives `clean-code-review-checklist.md` as part of its prompt and applies it during review.
4. Review output follows the violation format from the UX design (Section 2 of ux-design.md).

**Enforcement behavior**:
- The developer skill reads `tech_stack.clean_code_enforcement` from `.delivery/config.yml` at sub-agent spawn time.
- `block` (default): Violations use `VIOLATION` severity and the result line says `BLOCKED`.
- `warn`: Violations use `WARNING` severity and the result line says `PASSED with N warnings`.

**Why this works**: The developer skill is the execution layer for all code tasks. Any tool that delegates to it automatically gets clean code enforcement. No coupling to the PR review toolkit's internal structure.

### 2.4 Config Schema (New Keys)

Two new keys added to `tech_stack` section:

| Key | Type | Required | Default | Valid Values | Wizard Q# | Consumed By |
|-----|------|----------|---------|-------------|-----------|-------------|
| `tech_stack.clean_code_guide` | string | no | "" (empty = use built-in default) | file path or empty string | defaults | developer (clean code loading), godot (clean code loading) |
| `tech_stack.clean_code_enforcement` | string | no | "block" | block, warn | defaults | developer (review enforcement), godot (review enforcement) |

These keys are NOT added to the setup wizard. They are advanced configuration for teams with custom standards. Default behavior (built-in guide, block enforcement) requires zero configuration.

### 2.5 Config Check Hook (New Validation Logic)

Three new validation blocks added to `check_config.py` after existing version/date extraction:

**Block 1: Custom guide path validation**

```python
# After existing version/date extraction
clean_code_guide_match = re.search(r'clean_code_guide:\s*(\S+)', content)
if clean_code_guide_match:
    guide_path = clean_code_guide_match.group(1).strip('"').strip("'")
    if guide_path:
        full_path = cwd / guide_path
        if full_path.exists():
            # Append info to existing message
            message += f"\nCustom clean code guide: {guide_path}"
            # Token size warning
            token_estimate = len(full_path.read_text(encoding="utf-8")) // 4
            if token_estimate > 4000:
                message += f"\nWARNING: Custom clean code guide is large (~{token_estimate} tokens): {guide_path}"
                message += "\n  The built-in guide targets <=2000 tokens to preserve context for code generation."
                message += "\n  Large guides may reduce available context for complex tasks."
        else:
            message += f"\nWARNING: Custom clean code guide not found: {guide_path}"
            message += "\n  The file at this path does not exist or is not readable."
            message += "\n  Fix: Either create the file, update the path in .delivery/config.yml under tech_stack.clean_code_guide, or remove the key to use the built-in default."
            message += "\n  Falling back to built-in clean-code.md for this session."
```

**Block 2: Enforcement value validation**

```python
enforcement_match = re.search(r'clean_code_enforcement:\s*(\S+)', content)
if enforcement_match:
    enforcement = enforcement_match.group(1).strip('"').strip("'")
    if enforcement not in ('block', 'warn'):
        message += f"\nWARNING: Invalid clean_code_enforcement value: '{enforcement}'"
        message += "\n  Valid values: block, warn"
        message += "\n  Defaulting to: block"
```

**Block 3: Version check update**

The existing version detection already handles version comparison. The new keys are added with defaults during migration (existing migration protocol handles this).

---

## 3. Loading Algorithm

### 3.1 Clean Code Guide Resolution

```
FUNCTION resolve_clean_code_guide(cwd):
    config_path = cwd / ".delivery" / "config.yml"

    IF config_path does NOT exist:
        RETURN (builtin_path("references/clean-code.md"), "default")

    config = parse_yaml(config_path)
    custom_path = config.get("tech_stack", {}).get("clean_code_guide", "")

    IF custom_path is empty or null:
        RETURN (builtin_path("references/clean-code.md"), "default")

    full_path = cwd / custom_path

    IF full_path exists and is readable:
        RETURN (full_path, custom_path)
    ELSE:
        EMIT WARNING "Custom clean code guide not found: {custom_path}"
        EMIT WARNING "Using built-in clean-code.md for this task."
        RETURN (builtin_path("references/clean-code.md"), "default")
```

### 3.2 Prompt Assembly (Developer Skill)

```
FUNCTION assemble_developer_prompt(language, task_type, user_request, cwd):
    # Step 1: Language reference (existing)
    lang_ref = read("references/languages/{language}.md")

    # Step 2: Clean code guide (NEW)
    (guide_path, guide_label) = resolve_clean_code_guide(cwd)
    clean_code_content = read(guide_path)

    # Step 3: Conditional patterns (existing, unchanged)
    patterns = []
    IF task matches OOP triggers OR config.paradigm == "oop":
        patterns.append(read("references/oop-patterns.md"))
    IF task matches FP triggers OR config.paradigm == "fp":
        patterns.append(read("references/fp-patterns.md"))
    # ... frontend, nx patterns as before

    # Step 4: Review-specific additions (NEW)
    review_checklist = ""
    enforcement = "block"  # default
    IF task_type == "review":
        review_checklist = read("references/clean-code-review-checklist.md")
        enforcement = config.get("tech_stack.clean_code_enforcement", "block")

    # Step 5: Declare
    PRINT "Language: {language} | Task: {task_type} | Reference: references/languages/{language}.md | Clean Code: {guide_label}"

    # Step 6: Assemble prompt
    prompt = """
    You are an expert {language} developer...

    ---
    {lang_ref}
    ---

    ## Clean Code Standards
    {clean_code_content}
    ---

    {patterns joined by ---}

    {IF review_checklist:
        ## Clean Code Review Checklist
        {review_checklist}

        Enforcement mode: {enforcement}
        - If "block": use VIOLATION severity, BLOCKED result for any violations
        - If "warn": use WARNING severity, PASSED with warnings result
    }

    ## Task
    {task_type}: {user_request}
    ...
    """

    RETURN prompt
```

### 3.3 Prompt Assembly (Godot Skill)

Identical to developer skill algorithm except:
- Step 1 reads Godot reference files (gdscript.md, scenes-nodes.md, etc.) instead of language files
- Step 3 does not apply (Godot has no OOP/FP conditional routing)
- Guide resolution uses the same `resolve_clean_code_guide()` function
- `clean-code.md` is read from the developer skill's references path (shared file)

### 3.4 Config Check Hook Validation

```
FUNCTION validate_clean_code_config(config_content, cwd):
    # 1. Check custom guide path
    guide_path = extract_yaml_value(config_content, "tech_stack.clean_code_guide")

    IF guide_path is not empty:
        full_path = cwd / guide_path
        IF full_path exists:
            EMIT INFO "Custom clean code guide: {guide_path}"
            # Token estimate (chars / 4 approximation)
            token_count = len(full_path.read_text()) / 4
            IF token_count > 4000:
                EMIT WARNING "Custom clean code guide is large (~{token_count} tokens): {guide_path}"
        ELSE:
            EMIT WARNING "Custom clean code guide not found: {guide_path}"
            EMIT WARNING "Falling back to built-in clean-code.md for this session."

    # 2. Check enforcement value
    enforcement = extract_yaml_value(config_content, "tech_stack.clean_code_enforcement")

    IF enforcement is not empty AND enforcement NOT IN ("block", "warn"):
        EMIT WARNING "Invalid clean_code_enforcement value: '{enforcement}'"
        EMIT WARNING "Valid values: block, warn. Defaulting to: block"
```

---

## 4. Architecture Decision Records

See [ADR-001: Foundational Layer vs Conditional Routing](adrs/ADR-001-foundational-clean-code.md).

---

## 5. Config Schema Extension

### 5.1 New Schema Table Rows

Add these rows to the Complete Schema table in `config-schema.md`, in the `tech_stack` section after `tech_stack.nx_workspace`:

| Key | Type | Required | Default | Valid Values | Wizard Q# | Consumed By |
|-----|------|----------|---------|-------------|-----------|-------------|
| `tech_stack.clean_code_guide` | string | no | "" | file path (relative to project root) or empty string | defaults | developer (clean code loading), godot (clean code loading) |
| `tech_stack.clean_code_enforcement` | string | no | "block" | block, warn | defaults | developer (review enforcement), godot (review enforcement) |

### 5.2 Config File Template Additions

Add to the `tech_stack` section of the template:

```yaml
tech_stack:
  languages: [TypeScript, Python]
  frameworks: [Next.js, FastAPI]
  databases: [PostgreSQL]
  ci_cd: github-actions
  paradigm: auto
  paradigm_by_language:
    python: hybrid
    typescript: hybrid
  nx_workspace: false
  clean_code_guide: ""
  clean_code_enforcement: block
```

### 5.3 Version Bump

Update `config_version` default from `"2.2"` to `"2.3"` in the schema table header and template.

### 5.4 Version History Entry

| Version | Date | Changes |
|---------|------|---------|
| 2.3 | 2026-03-27 | Added tech_stack.clean_code_guide (custom clean code reference path), tech_stack.clean_code_enforcement (block/warn review enforcement mode). Config check hook validates custom guide path existence and enforcement value at session start. |

### 5.5 Extension Protocol Checklist

| Step | Action | Status |
|------|--------|--------|
| Step 1: Add to Schema | Two new rows in Complete Schema table | Defined in 5.1 |
| Step 2: Bump Version | 2.2 -> 2.3 | Defined in 5.3 |
| Step 3: Add Wizard Question | Not applicable -- defaults only, no wizard question | N/A |
| Step 4: Add to Pipeline Config Table | Not applicable -- consumed by developer/godot skills, not delivery-flow pipeline directly | N/A |
| Step 5: Add Migration Note | Version History entry | Defined in 5.4 |
| Step 6: Update Consuming Skill | Developer SKILL.md and Godot SKILL.md updated to read new keys | Defined in 2.1, 2.2 |
| Step 6.5: Regenerate JSON Schema | Run `python delivery-team/scripts/generate-schema.py` | Post-implementation |

---

## 6. Dependency Graph

```
clean-code.md (new)
    |
    +---> Developer SKILL.md (modified: prompt template, declaration line, coding-standards task)
    |         |
    |         +---> Sub-agent prompt (runtime: clean code injected after lang ref)
    |         |
    |         +---> PR review toolkit (runtime: inherits via delegation to developer review task)
    |
    +---> Godot SKILL.md (modified: prompt template, declaration line)
    |         |
    |         +---> Sub-agent prompt (runtime: clean code injected after Godot refs)
    |
    +---> clean-code-review-checklist.md (new, derived from clean-code.md)

config-schema.md (modified: two new keys, version bump)
    |
    +---> check_config.py (modified: validates new keys at session start)
    |
    +---> config-schema.json (regenerated by generate-schema.py)
    |
    +---> .delivery/config.yml (runtime: teams add keys as needed)
```

---

## 7. Risk Mitigations

| Risk | Mitigation | Owner |
|------|------------|-------|
| Token budget exceeded for clean-code.md | Author targets <=2000 tokens. Review with tokenizer before merging. No code examples in the reference. | Developer |
| Shared file path fragility (Godot reads from developer's references/) | Document the shared path in both SKILL.md files. If the developer skill moves, Godot must update. Consider symlink if paths diverge. | Architect |
| Config check hook regex parsing breaks on complex YAML | Use the same regex pattern style already proven in the hook (line 19-28 of check_config.py). Keep patterns simple: key-value on a single line. | Developer |
| PR review toolkit coupling | Session context approach means zero coupling. If the toolkit changes its delegation model, clean code still works because it lives in the developer skill. | Architect |
| Backward compatibility of config | Both new keys have sensible defaults (empty guide = built-in, enforcement = block). Existing configs without these keys work unchanged. | Developer |

---

## 8. Implementation Sequence

This is the recommended build order for the developer implementing the plan. Each milestone is independently testable.

| Order | Milestone | Dependencies | Testable By |
|-------|-----------|-------------|-------------|
| 1 | Author `clean-code.md` | None | Token count check, content review against PRD 10 sections |
| 2 | Author `clean-code-review-checklist.md` | clean-code.md | Content review, token count check |
| 3 | Modify Developer SKILL.md (prompt template + declaration line) | clean-code.md | Spawn developer sub-agent, verify clean code in prompt |
| 4 | Modify Godot SKILL.md (prompt template + declaration line) | clean-code.md | Spawn Godot sub-agent, verify clean code in prompt |
| 5 | Update config-schema.md (new keys, version bump) | None | Schema review, generate-schema.py produces valid JSON |
| 6 | Modify check_config.py (validation logic) | config-schema.md | Session start with custom guide path (exists/missing/invalid enforcement) |
| 7 | Add `coding-standards` task type to Developer SKILL.md | clean-code.md | Run scaffold, verify output file with 10 sections and placeholders |
| 8 | Dogfooding: review existing Python scripts | clean-code.md, review checklist | All hooks/*.py and scripts/*.py pass review at warn level |
