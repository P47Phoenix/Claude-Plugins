# Cross-Skill Reference Convention

How skills in the delivery-team plugin reference files owned by other skills.

---

## How It Works

Skills can reference files from other skills using paths relative to the plugin root. Claude resolves these paths using the `Read` tool with absolute filesystem paths.

The plugin root is the `delivery-team/` directory inside the plugin installation location (e.g., `~/.claude/plugins/marketplaces/mec-claude-agent-skills/delivery-team/`). In a development/repo context, it is the `delivery-team/` directory at the repository root.

## Path Format

```
delivery-team/skills/<owner-skill>/references/<file>.md
```

Example -- the godot skill references the developer skill's clean code guide:

```
delivery-team/skills/developer/references/clean-code.md
```

Claude reads this file using the `Read` tool with the full absolute path resolved from the plugin installation root.

## Rules

1. **Files stay with their owner.** The referenced file remains in the owner skill's `references/` directory. Do not copy it into the consumer skill's directory.
2. **The owner skill maintains the file.** Consumers read it but do not modify it. If you need a modified version, copy it, adapt it, and document why it diverged.
3. **Declare cross-references in SKILL.md.** Every SKILL.md that references another skill's file MUST declare the reference in a `## Cross-Skill References` section (see format below).
4. **Verify the file exists** before adding a cross-reference. Run the validation script to catch phantom references.
5. **Renaming a skill directory is a breaking change.** Cross-references use string paths containing the skill directory name. If `developer/` were renamed to `dev/`, every consumer's SKILL.md would need updating. Treat skill directory names as stable identifiers.

## SKILL.md Declaration Format

Add this section to any SKILL.md that uses cross-skill references:

```markdown
## Cross-Skill References

| File | Owner Skill | Purpose |
|------|-------------|---------|
| `delivery-team/skills/developer/references/clean-code.md` | developer | Clean code standards (loaded on every task) |

> Path stability: these paths are contracts. Renaming the owner skill's directory is a breaking change.
```

## Current Cross-References

| Consumer Skill | Referenced Path | Owner Skill | What It Provides |
|----------------|----------------|-------------|------------------|
| godot | `skills/developer/references/clean-code.md` | developer | Foundational clean code standards, loaded on every godot task unless overridden by config |
| alias-creator | `skills/delivery-flow/references/aliases/*.yml` | delivery-flow | 13 built-in alias theme definitions (YAML files) |

## Adding a New Cross-Reference

1. Verify the target file exists at the expected path
2. Add a `## Cross-Skill References` section to your SKILL.md (if not already present)
3. Add a row to the table with the file path, owner skill, and purpose
4. Update the "Current Cross-References" table in this document
5. Run `python delivery-team/scripts/validate_cross_refs.py delivery-team/` to verify all references resolve

## When NOT to Cross-Reference

- **Intentionally distinct content**: `architect/references/security-patterns.md` and `quality/references/security-scanning.md` serve different roles with different audiences. These are not duplicates -- they are specialized perspectives on the same domain.
- **Ephemeral or experimental content**: Do not cross-reference files that are likely to move or be restructured.
- **If you need modifications**: Copy the file, adapt it, and document why it diverged from the original. A cross-reference implies you consume the file as-is.

## Validation

Run the CI validation script to verify all declared cross-references point to existing files:

```bash
python delivery-team/scripts/validate_cross_refs.py /path/to/delivery-team/
```

Exit code 0 means all references are valid. Exit code 1 means broken references were found.

## Review Triggers

Revisit this convention when any of these conditions are met:

- More than 5 files are cross-referenced between skills
- More than 3 skills reference the same single file
- A new skill author reports difficulty discovering cross-reference patterns
- Claude Code's plugin platform adds native shared resource support
