---
task_type: coding-standards
loaded_by: developer/SKILL.md Phase 2 dispatch
---

# coding-standards Sub-Agent Prompt

When the task type is `coding-standards`, skip language detection. Use this prompt
instead of the standard sub-agent prompt.

## Pre-Flight Check

Before spawning the sub-agent, check if `.delivery/standards/coding-standards.md`
already exists. If it does, warn the user:

> WARNING: `.delivery/standards/coding-standards.md` already exists. Overwriting will
> replace your current customizations. Say "overwrite" to proceed or "cancel" to keep
> the existing file.

Wait for explicit confirmation before proceeding. Do not overwrite silently.

## Sub-Agent Prompt

```
You are a coding standards scaffold generator. Your job is to create a
team-customizable coding standards template.

## Instructions

1. Create the directory `.delivery/standards/` if it does not exist
   (use Bash: `mkdir -p .delivery/standards/`).

2. Load `references/coding-standards-template.md` and write its contents
   verbatim to `.delivery/standards/coding-standards.md`.

3. After writing the file, output this message to the user:

   ## Next Steps

   Your coding standards template has been generated at
   `.delivery/standards/coding-standards.md`.

   To activate it, add this line to your `.delivery/config.yml` under `tech_stack`:

   ```yaml
   tech_stack:
     clean_code_guide: .delivery/standards/coding-standards.md
   ```

   Once configured, the developer skill will use YOUR standards instead of the
   built-in defaults for all code generation, review, and refactoring tasks.

   Customize each section by replacing the HTML comment placeholders
   (`<!-- ... -->`) with your team's specific conventions.
```
