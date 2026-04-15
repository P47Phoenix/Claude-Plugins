# FIX-4 — CI Regression Guard for DEFECT-004 (Workflow Injection)

**Author**: Gimli (developer)
**Date**: 2026-04-14
**Scope**: Add CI lint that blocks `${{ github.event.* }}` inside `run:` blocks across all GitHub Actions workflows.

## Files Changed
- **NEW**: `.github/workflows/workflow-injection-lint.yml` — runs on PRs and push-to-main whenever any workflow file changes. Python-based YAML scanner detects indentation-aware `run: |` blocks and flags the injection pattern. Self-excludes by basename to avoid tripping on its own FAIL message.

## Audit Results (manual inspection + grep)
| File | State | Finding |
|------|-------|---------|
| `.github/workflows/version.yml` | Clean | Line 25 uses `env: COMMIT_MSG: ${{ github.event.head_commit.message }}` — correct post-DEFECT-004 pattern. Zero `${{ github.event.* }}` references inside any `run:` block. |
| `.github/workflows/release.yml` | Clean | No `github.event.*` references anywhere. Only trusted interpolations (`steps.*.outputs.*`, `github.repository`, `secrets.GITHUB_TOKEN` via `env:`). |
| `.github/workflows/docs.yml` | Clean | Untracked-but-present (per DEFECT-004 scope-check note). Minimal workflow: checkout, setup-python, install mkdocs-material, `mkdocs gh-deploy --force`. No user-text interpolation, no `run:` blocks with `github.event.*`. No fix needed. |

**No in-flight fixes required** — repo is already in a clean post-DEFECT-004 state across all three existing workflows.

## Local Test Results
Extracted scanner logic to `/tmp/scan.py` and ran against:

1. **All three current workflows**: all three return `OK` (exit 0). Matches expected clean state.
2. **Synthetic bad workflow** (`/tmp/bad-workflow.yml` with `MSG="${{ github.event.head_commit.message }}"` inside `run: |`): scanner reports
   ```
   INJECTION ANTIPATTERN in /tmp/bad-workflow.yml:
     line 9: MSG="${{ github.event.head_commit.message }}"
   ```
   and exits 1. Regression guard demonstrably catches the DEFECT-004 pattern.

## Push Caveat (IMPORTANT)
Per the DEFECT-004 hotfix notes, the user's current git token lacks the `workflow` scope. This commit adds a NEW file under `.github/workflows/`, so GitHub's PAT-workflow-scope check will likely reject the push with:

```
! [remote rejected] main -> main (refusing to allow a Personal Access Token to create or update workflow `.github/workflows/workflow-injection-lint.yml` without `workflow` scope)
```

**Resolution options for the user**:
1. Push with a token that has `workflow` scope (preferred, one-shot).
2. Merge via GitHub web UI / PR created from a branch pushed by a scoped token.
3. Accept the file as committed-but-unpushed locally until scope is provisioned.

File is committed locally regardless; pushing is a separate step.

## Acceptance Criteria
- [x] New lint workflow created at the specified path.
- [x] Workflow triggers on PR + push-to-main, scoped to `.github/workflows/**`.
- [x] Permissions: `contents: read` only (no write needed).
- [x] Self-excludes to avoid false positive on its own FAIL message.
- [x] Audits release.yml + docs.yml: both clean, no fixes needed.
- [x] Local scan confirms clean state for current workflows.
- [x] Local scan confirms bad-case detection (injection pattern → exit 1 with line number).
- [x] Log under 60 lines.
