# GitHub Integration Reference

This reference covers the delivery pipeline's optional GitHub integration: creating issues from user stories, linking commits to issues, creating pull requests at UAT, and reading existing issues as pipeline input.

All GitHub integration is config-driven and optional. It requires:
- The `gh` CLI installed and authenticated
- A git remote configured for the current repository
- The relevant config flags enabled in `.delivery/config.yml`

If `gh` is not available or the repo has no remote, all GitHub integration steps are silently skipped.

---

## Prerequisites Check

Before any GitHub operation, verify:

```bash
# Check gh CLI is available and authenticated
gh auth status

# Check repo has a remote
git remote -v
```

If either check fails, skip all GitHub integration for this pipeline run and log a note in the stage artifact: "GitHub integration skipped: [reason]."

---

## Config Keys

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `github.create_issues` | boolean | false | Create GitHub issues from user stories at Refine |
| `github.create_pr` | boolean | false | Create a pull request at UAT |
| `github.link_commits` | boolean | true | Include issue numbers in commit messages |

---

## Issue Creation from User Stories (Refine Stage)

**When**: `github.create_issues` is true, after PRD is finalized at Stage 2 (Refine).

**Process**:

1. For each user story in the PRD, create a GitHub issue:

```bash
gh issue create --title "Story: <story title>" --body "<story body with acceptance criteria>" --label "<priority label>"
```

2. Map story priority to GitHub labels:
   - P1 / Critical --> label: `priority: critical`
   - P2 / High --> label: `priority: high`
   - P3 / Medium --> label: `priority: medium`
   - P4 / Low --> label: `priority: low`

3. Include in the issue body:
   - Full user story text ("As a ... I want ... So that ...")
   - Acceptance criteria (as a checklist)
   - Link to the PRD artifact path: `See .delivery/artifacts/02-prd.md`

4. Record created issue numbers in the PRD artifact under a new "GitHub Issues" section:

```markdown
### GitHub Issues
| Story | Issue |
|-------|-------|
| <story title> | #<number> |
```

5. If issue creation fails for any story, log the error and continue with remaining stories. Do not fail the stage.

---

## Reading Existing Issues as Pipeline Input (Idea Stage)

**When**: GitHub integration prerequisites pass, at Stage 1 (Idea).

**Process**:

1. Offer to list open issues:

```bash
gh issue list --state open --limit 20
```

2. Present the list to the user: "There are N open GitHub issues. Would you like to use one as the idea input?"

3. If the user selects an issue, read its details:

```bash
gh issue view <number>
```

4. Use the issue title, body, labels, and comments as the raw idea input instead of asking the user to describe the idea from scratch.

5. Record the source issue number in the idea brief artifact:

```markdown
**Source**: GitHub Issue #<number>
```

---

## Commit Linking (Development Stage)

**When**: `github.link_commits` is true, during Stage 6 (Development).

**Process**:

1. When producing commit messages for implemented stories, append the issue reference:

```
feat(module): implement user login (#12)
```

2. Use conventional commit format with the issue number in parentheses as a suffix.

3. If multiple issues relate to a single commit, include all:

```
feat(auth): implement login and registration (#12, #13)
```

4. The issue number comes from the "GitHub Issues" section recorded during Refine, or from the source issue recorded at Idea.

5. If no issue numbers are available (issues were not created or integration was disabled at Refine), omit the suffix. Do not fabricate issue numbers.

---

## PR Creation at UAT (UAT Stage)

**When**: `github.create_pr` is true, after all stories pass DoD at Stage 7 (UAT).

**Process**:

1. Determine PR metadata:
   - **Title**: From the sprint goal in `05-sprint-plan.md`, or from the idea brief title if no sprint plan exists
   - **Labels**: Derived from project type (e.g., `enhancement` for FEATURE, `bug` for BUG_FIX, `documentation` for DOCS_ONLY)
   - **Base branch**: The branch the current work should merge into (typically `main` or `develop`)

2. Build the PR body with structured sections:

```markdown
## Summary
<1-3 sentence summary of what this PR delivers>

## Stories Implemented
- [x] <Story title> (Closes #<issue number>)
- [x] <Story title> (Closes #<issue number>)

## Changes
<Bulleted list of key changes from 06-dev-notes.md>

## Test Results
<Summary from 07-uat-report.md: total tests, pass rate, any known issues>

## Release Notes
<From 07b-documentation.md release notes section>
```

3. The "Closes #N" syntax in the Stories section auto-links and auto-closes issues when the PR merges.

4. Create the PR:

```bash
gh pr create --title "<title>" --body "<body>" --label "<labels>"
```

5. Record the PR URL in the UAT report artifact:

```markdown
### Pull Request
- PR: <url from gh pr create output>
- Issues closed on merge: #<n1>, #<n2>, ...
```

6. After creation, verify the PR was created:

```bash
gh pr view --json number,url,title
```

---

## Error Handling

- **gh not installed**: Skip all GitHub integration. Log: "gh CLI not found, GitHub integration disabled."
- **Not authenticated**: Skip all GitHub integration. Log: "gh not authenticated, GitHub integration disabled."
- **No remote**: Skip all GitHub integration. Log: "No git remote configured, GitHub integration disabled."
- **API rate limit**: Retry once after 5 seconds. If still failing, skip the operation and log the error.
- **Issue creation failure**: Log the error, continue with remaining stories. Do not fail the pipeline stage.
- **PR creation failure**: Log the error, present the PR body to the user so they can create it manually.

---

## Security Considerations

- Never include secrets, tokens, or credentials in issue or PR bodies.
- Do not include full file paths from the local filesystem in issue bodies -- use repository-relative paths only.
- PR descriptions should summarize test results, not include raw test output that might contain environment details.
