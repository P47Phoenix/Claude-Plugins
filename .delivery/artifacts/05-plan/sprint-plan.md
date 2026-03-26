# Sprint Plan: Documentation Audit & CI/CD Bootstrap

**Pipeline**: DOCS_ONLY (Light)
**Date**: 2026-03-25
**Sprint Goal**: Eliminate all 28+ verified documentation inaccuracies, create missing contribution guidelines, and bootstrap CI/CD with semantic versioning and automated release notes.

---

## Stories

### Story 1: Update CLAUDE.md — Fix 6 Identified Gaps

**As a** Claude Code instance loading this repo as context, **I want** CLAUDE.md to accurately reflect the current codebase, **so that** I don't hallucinate capabilities or miss real ones when reasoning about this repository.

**Acceptance Criteria**:
- [ ] Skill count updated from 9 to 10 (alias-creator added to table)
- [ ] Developer language count updated from 10 to 14 (F#, Elixir, Haskell, Scala added)
- [ ] Hooks table expanded from 3 to all 7 hooks (add SessionStart/check_config, Stop/retrospective, PreToolUse/Agent/audit, PostToolUse/Agent/verify_skill_load)
- [ ] Missing features documented: Feature Knowledge System, session keepalive, pipeline resume/state persistence, git/GitHub integration, alias themes (13 themes), config validation toolchain
- [ ] Developer skill description includes FP patterns and Nx monorepo support
- [ ] Repo structure reference file counts verified against filesystem and corrected; delivery-team/scripts/ directory added

**Test Cases**:
- TC1: For each numeric claim in CLAUDE.md, run a filesystem count (ls/find) and confirm the number matches
- TC2: Every hook listed in hooks.json files across the repo appears in the hooks table
- TC3: Every skill directory under delivery-team/ has a corresponding row in the skills table

---

### Story 2: Update README.md — Fix 7 Identified Gaps

**As a** new user discovering this repo, **I want** the README to give me an accurate picture of what this project is and how to get started, **so that** I can evaluate and install plugins without hitting surprises.

**Acceptance Criteria**:
- [ ] Skill count updated from 9 to 10
- [ ] Developer language count updated from 10 to 14
- [ ] Repo structure: stale shell script references (flag-empirical-validation.sh, validate-gdscript.sh) removed and replaced with current Python scripts
- [ ] Reference file counts in repo structure verified against filesystem and corrected
- [ ] Missing entries added: alias-creator skill, scripts/ directory, alias themes
- [ ] Quick-start section added near top with "What is this?" opener for new users
- [ ] Contributing section links to CONTRIBUTING.md (Story 5)

**Test Cases**:
- TC1: Every file path shown in the repo structure tree exists on disk
- TC2: No file path in the repo structure tree references a deleted file
- TC3: Quick-start section includes at minimum: what the repo is, how to install a plugin, and a single working example command
- TC4: Read the README cold as a new user — can you answer "what is this?" and "how do I use it?" within the first screen

---

### Story 3: Update delivery-team/README.md — Fix 4 Identified Gaps

**As a** user evaluating the delivery-team plugin specifically, **I want** its README to accurately describe all skills, hooks, and features, **so that** I understand the full capability set before installing.

**Acceptance Criteria**:
- [ ] Skill count updated from 9 to 10 (alias-creator added)
- [ ] Hooks table expanded to all 7 hooks (add PreToolUse/Agent/audit, PostToolUse/Agent/verify_skill_load, SessionStart/check_config)
- [ ] Missing features documented: alias themes, config validation toolchain
- [ ] scripts/ directory referenced in structure or description

**Test Cases**:
- TC1: Every hook in delivery-team/hooks/hooks.json has a corresponding row in the README hooks table
- TC2: Every subdirectory under delivery-team/ that contains a SKILL.md is listed in the skills section
- TC3: Skill count in prose matches actual count of skill directories

---

### Story 4: Update marketplace.json — Fix Delivery-Team Metadata

**As a** plugin consumer browsing the marketplace, **I want** the delivery-team description to reflect its actual capabilities, **so that** I can make an informed install decision.

**Acceptance Criteria**:
- [ ] delivery-team description references 10 skills (not 9)
- [ ] delivery-team description references 14 languages (not 10)
- [ ] Description mentions: alias themes, FP patterns, Nx monorepo, Feature Knowledge System, session keepalive
- [ ] File remains valid JSON after edits

**Test Cases**:
- TC1: `python -m json.tool .claude-plugin/marketplace.json` exits 0 (valid JSON)
- TC2: Numeric claims in the description match filesystem counts
- TC3: Diff shows only description field changes — no structural modifications

---

### Story 5: Create CONTRIBUTING.md

**As a** potential contributor, **I want** clear guidelines on how to contribute plugins, skills, and fixes, **so that** my PRs meet expectations on the first review.

**Acceptance Criteria**:
- [ ] Plugin structure section explains required files (SKILL.md, LICENSE.txt, hooks/, scripts/, references/)
- [ ] Dev workflow section covers: fork, branch, develop, test, PR
- [ ] Code standards section covers: kebab-case naming, three-level context loading pattern, YAML correctness, JSON validity
- [ ] PR process section describes what reviewers look for
- [ ] Testing expectations section explains dogfooding and filesystem verification (no test runner exists)
- [ ] Config extension protocol section references delivery-flow/references/config-schema.md as source of truth
- [ ] File is referenced from README.md (Story 2)

**Test Cases**:
- TC1: A reader with no prior context can answer: "What files do I need to create a new plugin?"
- TC2: Every directory convention mentioned matches the actual repo structure
- TC3: The config extension protocol section is consistent with config-schema.md

---

### Story 6: Create GitHub Actions — Semantic Versioning

**As a** maintainer, **I want** automatic semantic version tags on push to main, **so that** releases are trackable without manual tagging.

**Acceptance Criteria**:
- [ ] Workflow file at `.github/workflows/release.yml` (or separate versioning file)
- [ ] Triggers on push to main branch
- [ ] Uses conventional commits or similar strategy to determine version bump (major/minor/patch)
- [ ] Creates a git tag with the new version
- [ ] Uses only GitHub-maintained or well-established actions (no obscure third-party actions)
- [ ] Workflow YAML is valid and passes `actionlint` or equivalent syntax check

**Test Cases**:
- TC1: Workflow YAML parses without errors
- TC2: Trigger conditions are correct (push to main only, not PRs)
- TC3: A dry-run review of the workflow logic confirms: patch bump for fix commits, minor bump for feat commits, major bump for breaking changes

---

### Story 7: Create GitHub Actions — Release Notes

**As a** user tracking updates, **I want** auto-generated release notes when a version tag is created, **so that** I can see what changed without reading commit logs.

**Acceptance Criteria**:
- [ ] Workflow triggers on version tag creation (from Story 6)
- [ ] Generates a GitHub Release with auto-generated release notes
- [ ] Uses GitHub's built-in release notes generation or a standard action
- [ ] Release notes group changes by type (features, fixes, docs, etc.) if possible
- [ ] Uses only GitHub-maintained or well-established actions

**Test Cases**:
- TC1: Workflow YAML parses without errors
- TC2: Trigger conditions are correct (tag push only, matching version pattern)
- TC3: Review confirms the workflow creates a GitHub Release (not just a tag)

---

## Sprint Notes

**Ordering**: Stories 1-4 (doc fixes) are independent and can run in parallel. Story 5 (CONTRIBUTING.md) is independent but Story 2 should link to it. Stories 6-7 (CI/CD) are independent of docs but Story 7 depends on Story 6's tagging output.

**Constraint reminder**: Every numeric claim must be re-verified against the filesystem at write time. The audit findings are a starting point, not gospel. If any number has changed since the audit, use the current truth.

**Dogfooding gate**: Before marking any doc story DONE, read the updated file as its target audience would. If you can't answer the key questions the audience would ask, the story is not done.
