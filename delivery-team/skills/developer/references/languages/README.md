# Language Best Practices Files

Each file in this directory defines the coding standards, idioms, and anti-patterns for one programming language. The developer skill loads **only the file matching the detected language** into a sub-agent — no other language files are loaded into context.

## How Language Isolation Works

1. The developer SKILL.md detects the target language
2. It reads **only** `references/languages/<lang>.md`
3. It spawns a sub-agent with that single file's content as context
4. All other language files remain unloaded

This means a Python task never loads TypeScript best practices, and vice versa.

## Adding a New Language

Create a new file `references/languages/<language>.md` using this template:

```markdown
# [Language] Best Practices

## Style & Formatting
[Naming conventions, indentation, line length, file/module organization]

## Idioms & Patterns
[Language-idiomatic approaches to common problems — prefer X over Y]

## Error Handling
[How errors, exceptions, or result types should be handled]

## Testing
[Preferred test framework, test structure, naming, assertion style]

## Security
[Language-specific security pitfalls and safe alternatives]

## Performance
[Common performance anti-patterns and preferred approaches]

## Anti-Patterns to Avoid
[Named anti-patterns with brief explanation of why]

## Tooling
[Linter, formatter, package manager, build tool conventions]
```

Then register the language in the developer SKILL.md's detection table so it is auto-detected and routed correctly.

## Current Languages

| File | Language | Version Baseline |
|------|----------|-----------------|
| `python.md` | Python | 3.10+ |
| `javascript.md` | JavaScript | ES2022+ |
| `typescript.md` | TypeScript | 5.x |
| `csharp.md` | C# / .NET | .NET 8 / C# 12 |
| `go.md` | Go | 1.21+ |
| `rust.md` | Rust | 2021 edition |
| `java.md` | Java | Java 17 LTS |
| `sql.md` | SQL | ANSI SQL / PostgreSQL |
| `bash.md` | Bash / Shell | Bash 5+ |
