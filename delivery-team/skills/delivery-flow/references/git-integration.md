# Git Integration

Reference for git branching strategies, conventional commits, and pipeline integration points. Loaded by delivery-flow when `git.*` config keys are set.

---

## Branching Strategies

### Decision Matrix

| Strategy | Team Size | Release Cadence | Best For |
|----------|-----------|----------------|----------|
| **Trunk-based** | 1-3 | Continuous (daily+) | Small teams, CI/CD mature, feature flags available |
| **GitHub Flow** | 1-10 | Frequent (weekly) | Most teams, PR-based review, single production branch |
| **GitFlow** | 5+ | Scheduled (sprints, releases) | Larger teams, versioned releases, parallel release tracks |
| **None** | any | any | Non-code projects (DOCS_ONLY, SPIKE with no repo) |

### Trunk-Based Development

- All commits go directly to `main`.
- Short-lived branches (< 1 day) allowed for PRs but not required.
- Requires: feature flags, strong CI, high test coverage.
- Best when: solo developer, pair programming, or very small team with continuous deployment.

### GitHub Flow

- `main` is always deployable.
- Feature branches created from `main` for each piece of work.
- Pull request required before merging back to `main`.
- Best when: team uses PRs for code review, deploys from `main` after merge.

### GitFlow

- Two long-lived branches: `main` (production) and `develop` (integration).
- Feature branches created from `develop`.
- Release branches cut from `develop` when ready to ship.
- Hotfix branches created from `main` for emergency fixes.
- Best when: versioned releases, multiple environments, parallel development streams.

---

## Branch Naming Convention

Format: `<type>/<issue-number>-<short-description>`

| Type | When | Example |
|------|------|---------|
| `feature/` | New functionality (user stories, enhancements) | `feature/12-git-integration` |
| `bugfix/` | Bug fixes from backlog | `bugfix/45-login-timeout` |
| `hotfix/` | Urgent production fixes | `hotfix/session-expiry-crash` |
| `docs/` | Documentation-only changes | `docs/47-api-reference` |
| `spike/` | Investigative / throwaway work | `spike/redis-caching-feasibility` |

Rules:
- Use kebab-case for the description portion.
- Keep descriptions to 3-5 words maximum.
- Include the issue number when one exists.
- For GitFlow hotfixes, branch from `main`. For all others, branch from `main` (GitHub Flow) or `develop` (GitFlow).

---

## Conventional Commits

Format: `<type>(<scope>): <description>`

### Types

| Type | When to Use | Story Mapping |
|------|-------------|---------------|
| `feat` | New feature or capability | User stories |
| `fix` | Bug fix | Bug fix stories |
| `docs` | Documentation only | Documentation tasks |
| `refactor` | Code restructuring (no behavior change) | Technical debt stories |
| `test` | Adding or updating tests | Test tasks |
| `chore` | Build, CI, tooling, dependency updates | Infrastructure tasks |
| `style` | Formatting, whitespace (no logic change) | Cleanup tasks |
| `perf` | Performance improvement | Performance stories |

### Scope

The scope is optional but recommended. Use the component, module, or feature area:
- `feat(auth): add OAuth2 login flow`
- `fix(api): handle null response from payment gateway`
- `docs(readme): add deployment instructions`
- `refactor(database): extract connection pooling to shared module`

### Rules

- Subject line: imperative mood, lowercase, no period, max 72 characters.
- Body (optional): explain WHY, not WHAT. Wrap at 80 characters.
- Footer (optional): `Closes #<issue>`, `BREAKING CHANGE: <description>`.

### Examples

```
feat(delivery): add git branch auto-creation at Plan stage

Closes #12

fix(parser): prevent crash on empty config file

The YAML parser threw an unhandled exception when config.md had
no frontmatter. Now returns empty dict with a warning.

docs(api): add rate limiting section to API reference

chore(ci): upgrade Node.js to v20 in GitHub Actions workflow
```

---

## Pipeline Integration Points

### Stage 5 (Plan) -- Branch Creation

When `git.auto_branch` is `true`:

1. **Check preconditions**:
   - Verify inside a git repository (`git rev-parse --is-inside-work-tree`).
   - Verify working tree is clean (`git status --porcelain` is empty). If dirty, warn the user and ask to commit or stash before proceeding.
   - Determine the base branch from strategy:
     - trunk-based: `main`
     - github-flow: `main`
     - gitflow: `develop`
2. **Generate branch name**: `feature/<issue-number>-<short-description>` derived from the idea brief or PRD title. Sanitize: lowercase, replace spaces with hyphens, strip special characters.
3. **Check if branch exists**: `git branch --list <branch-name>`. If it exists, append a numeric suffix (`-2`, `-3`).
4. **Create and switch**: `git checkout -b <branch-name>`.
5. **Announce**: `> Branch created: <branch-name> from <base-branch>`.
6. **Record in state**: Add `branch: <branch-name>` to `.delivery/state.md`.

For `git.branch_strategy: none` or `git.auto_branch: false`, skip branch creation entirely.

### Stage 6 (Development) -- Commit Suggestions

When `git.commit_convention` is `"conventional"`:

After each story passes its DoD validation:

1. **Determine commit type** from story type:
   - User story (new capability) -> `feat`
   - Bug fix story -> `fix`
   - Documentation task -> `docs`
   - Refactoring task -> `refactor`
   - Test task -> `test`
   - Infrastructure/tooling -> `chore`
2. **Determine scope** from story context (component name, module, feature area).
3. **Generate message**: `<type>(<scope>): <story-title-as-imperative>`
4. **Present to user** (do NOT auto-commit):
   ```
   > Suggested commit:
   >   git add -A && git commit -m "feat(auth): add OAuth2 login flow"
   > Adjust the message as needed. Stage and commit when ready.
   ```
5. **If story closes an issue**, append to suggestion: `\n\nCloses #<issue-number>`

For `git.commit_convention: none`, skip commit suggestions.

### Stage 7 (UAT) -- Working Tree Validation

When `git.clean_tree_check` is `true`:

Before the human checkpoint (step 9 in the UAT sub-flow):

1. **Run check**: `git status --porcelain`
2. **If clean** (empty output): proceed to human checkpoint.
3. **If dirty** (non-empty output):
   - List the uncommitted changes.
   - Warn: `> Working tree has uncommitted changes. Commit or stash before UAT acceptance.`
   - Do NOT block the pipeline -- present the warning and let the user decide.
   - If the user proceeds without committing, note it in the UAT report.

For `git.clean_tree_check: false`, skip the validation.

---

## Config Defaults by Project Type

| Config Key | GREENFIELD | FEATURE | BUG_FIX | GAME_DEV+ | SPIKE | DOCS_ONLY |
|-----------|-----------|---------|---------|-----------|-------|-----------|
| `git.branch_strategy` | github-flow | github-flow | github-flow | github-flow | none | none |
| `git.auto_branch` | true | true | true | true | false | false |
| `git.commit_convention` | conventional | conventional | conventional | conventional | none | none |
| `git.clean_tree_check` | true | true | true | true | false | false |
