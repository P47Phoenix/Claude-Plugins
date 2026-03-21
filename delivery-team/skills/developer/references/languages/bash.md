# Bash Best Practices

Version baseline: Bash 5+ (POSIX-compatible where noted)

## Style & Formatting

- Start every script with `#!/usr/bin/env bash`
- Add `set -euo pipefail` at the top of every script (see Anti-Patterns for explanation)
- Use `snake_case` for function and variable names; `UPPER_SNAKE_CASE` for exported/global constants
- Indent with 2 or 4 spaces consistently; never mix tabs and spaces
- Quote all variable expansions: `"$var"` not `$var`
- Use `shellcheck` to enforce style and catch common bugs

## Idioms & Patterns

- Use `[[ ... ]]` over `[ ... ]` (more features, safer string comparison, no word splitting)
- Use `(( ... ))` for arithmetic; not `expr` or `let`
- Prefer functions over duplicated code; define them at the top of the script
- Use `local` for all variables inside functions to avoid polluting global scope
- Use `mktemp` for temporary files/dirs; `trap` for cleanup on exit
- Use `printf` over `echo` for portable formatted output
- Use `"${array[@]}"` to expand arrays safely; `"${#array[@]}"` for length
- Use `$( )` for command substitution; not backticks
- Use `declare -r` for readonly variables; `declare -i` for integer variables

```bash
# Cleanup pattern
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
```

## Error Handling

- `set -e`: exit immediately on error
- `set -u`: exit on undefined variable (catches typos)
- `set -o pipefail`: pipeline fails if any stage fails (not just the last)
- Use `|| { echo "Error message" >&2; exit 1; }` for custom error messages after commands
- Write error messages to stderr: `echo "Error: ..." >&2`
- Use `exit 0` for success, non-zero for failure; document exit codes in comments
- Use `trap 'handler' ERR` for a global error handler in complex scripts

```bash
set -euo pipefail

err() {
    echo "[ERROR] $*" >&2
    exit 1
}

[[ -f "$config_file" ]] || err "Config file not found: $config_file"
```

## Testing

- Use `bats-core` (Bash Automated Testing System) for shell script unit tests
- Test scripts with `shellcheck` as a first pass before execution
- Test with edge cases: empty input, missing files, no permissions, spaces in filenames
- Use `--dry-run` flags or `DRY_RUN=true` variables to preview destructive operations during development
- Run scripts in a container or VM when testing destructive operations

## Security

- Never use `eval` with untrusted input — it executes arbitrary code
- Quote all variable expansions to prevent word splitting and glob expansion
- Validate inputs before using them: check file existence, type, permissions
- Do not store secrets in scripts; read from environment variables or secret files with restricted permissions
- Use `chmod 600` on files containing secrets; never commit them to version control
- Avoid `curl | bash` patterns — download, inspect, then execute
- Use absolute paths for executables in security-sensitive scripts to prevent PATH manipulation

```bash
# Unsafe
rm -rf $directory

# Safe
rm -rf "${directory:?directory is not set}"  # :? aborts if empty/unset
```

## Performance

- Prefer built-in Bash operations over spawning subprocesses for string manipulation
- Use `read` + `while` loops instead of `cat file | while` (avoids subshell; variables persist)
- Avoid unnecessary subshells: `$(cat file)` is slower than `$(<file)` for reading files
- Use `parallel` (GNU) for parallelizing independent tasks
- Profile with `bash -x script.sh 2>&1 | grep '^+'` to trace execution

## Anti-Patterns to Avoid

- **Missing `set -euo pipefail`:** silent failures corrupt state and continue execution
- **Unquoted variables:** `rm -rf $dir` fails catastrophically if `dir` is empty or contains spaces
- **Parsing `ls`:** use glob expansion or `find` instead: `for f in /path/*.txt`
- **Using `[` instead of `[[`:** `[` is POSIX but has more edge cases; use `[[` in Bash scripts
- **Backtick command substitution:** use `$( )` — backticks are harder to nest and read
- **`cat file | grep`:** use `grep pattern file` — useless use of cat (UUOC)
- **Hardcoded absolute paths like `/tmp/myfile`:** use `mktemp`; two concurrent runs will collide
- **No `local` in functions:** leaks variables into global scope

## Tooling

| Tool | Purpose | Command |
|------|---------|---------|
| `shellcheck` | Static analysis | `shellcheck script.sh` |
| `bats-core` | Unit testing | `bats tests/` |
| `shfmt` | Formatting | `shfmt -w script.sh` |
| `bash -x` | Execution tracing | `bash -x script.sh` |
| `bash -n` | Syntax check (no execute) | `bash -n script.sh` |
