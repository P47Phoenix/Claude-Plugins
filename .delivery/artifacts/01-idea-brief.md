## Idea Brief

**Project Type**: DOCS_ONLY
**Date**: 2026-03-25
**Applies To**: repository documentation, marketplace metadata, CI/CD workflows

### Problem Statement

The Claude-Plugins repository documentation has drifted significantly from the actual codebase. A full audit comparing documentation claims against the filesystem reveals **28+ factual inaccuracies** spread across 5 files, plus 1 missing file that should exist.

**CLAUDE.md** (6 gaps):
- States "9 skills" when there are 10 (missing alias-creator)
- States "10 languages" when developer skill covers 14 (missing F#, Elixir, Haskell, Scala)
- Hooks table documents 3 of 7 hooks (missing SessionStart/check_config, Stop/retrospective, PreToolUse/Agent/audit, PostToolUse/Agent/verify_skill_load)
- Missing features: Feature Knowledge System, session keepalive, pipeline resume/state persistence, git/GitHub integration, alias themes (13 themes), config validation toolchain
- Developer skill description omits FP patterns and Nx monorepo support
- Repo structure section has wrong reference file counts and is missing delivery-team/scripts/

**README.md** (7 gaps):
- States "9 skills" when there are 10
- States "10 languages" when there are 14
- Repo structure lists shell scripts (flag-empirical-validation.sh, validate-gdscript.sh) that no longer exist — they were replaced by Python scripts
- Reference file counts in repo structure are wrong (e.g., "9 reference files" for delivery-flow should be 18+)
- Missing: alias-creator skill, scripts/ directory, alias themes
- Missing quick-start section and "What is this?" opener for new users
- Contributing section is thin with no link to a CONTRIBUTING.md

**delivery-team/README.md** (4 gaps):
- States "9 skills" when there are 10 (missing alias-creator)
- Hooks table shows 4 of 7 hooks (missing PreToolUse/Agent/audit, PostToolUse/Agent/verify_skill_load, SessionStart/check_config)
- Missing: alias themes, config validation toolchain, scripts directory

**marketplace.json** (2 gaps):
- delivery-team description says "9 skills" and "10 languages" — should be 10 skills and 14 languages
- Missing mention of: alias themes, FP patterns, Nx monorepo, Feature Knowledge System, session keepalive

**Missing entirely** (1 file):
- CONTRIBUTING.md — no contribution guidelines exist for external contributors

**Separately**, the repository has no CI/CD automation. There are no GitHub Actions workflows for versioning or release notes, making it difficult to track what changed between releases.

### Target Users

1. **New users** discovering the repo — need accurate README and quick-start guidance
2. **Claude Code itself** — CLAUDE.md is loaded as system context; inaccuracies cause incorrect assumptions and hallucinated capabilities
3. **Contributors** — need accurate repo structure docs and contribution guidelines
4. **Plugin consumers** — rely on marketplace.json metadata to evaluate plugins before installing

### Goals

1. Fix all verified factual inaccuracies in CLAUDE.md (skill count, language count, hooks table, repo structure, feature coverage)
2. Fix all verified factual inaccuracies in README.md (counts, stale shell script references, repo structure, missing sections)
3. Fix all verified factual inaccuracies in delivery-team/README.md (skill count, hooks table, missing sections)
4. Fix marketplace.json metadata (skill count, language count, feature descriptions)
5. Create CONTRIBUTING.md with guidelines for plugin contributions, skill authoring, and PR expectations
6. Add a quick-start section and "What is this?" opener to README.md
7. Set up GitHub Actions workflow for semantic versioning (tag-based or conventional-commits-based)
8. Set up GitHub Actions workflow for automated release notes generation

### Constraints

- **Accuracy over speed**: Every number and claim must be re-verified against the filesystem before writing. Do not propagate the audit findings blindly — confirm each one at write time.
- **No code changes**: This is DOCS_ONLY. Do not modify any Python scripts, SKILL.md files, hooks, or plugin logic.
- **No new features**: Document what exists today. Do not describe planned or aspirational capabilities.
- **YAML correctness**: marketplace.json edits must preserve valid JSON. Config references must match the config-schema.md source of truth.
- **Preserve voice**: CLAUDE.md is terse and directive (it is machine-consumed context). README.md is human-friendly. Keep each file's tone consistent with its audience.
- **GitHub Actions must be minimal**: Workflows should use standard GitHub-maintained actions where possible. No third-party actions without justification.

### Scope

**Files to update**:
- `CLAUDE.md` — fix counts, hooks table, repo structure, add missing features
- `README.md` — fix counts, remove stale references, add quick-start, fix repo structure
- `delivery-team/README.md` — fix counts, hooks table, add missing sections
- `.claude-plugin/marketplace.json` — fix metadata descriptions

**Files to create**:
- `CONTRIBUTING.md` — contribution guidelines
- `.github/workflows/release.yml` — semantic versioning + release notes workflow

### Out of Scope

- Modifying any plugin code, scripts, hooks, or SKILL.md files
- Changing the plugin architecture or directory structure
- Adding new plugins or skills
- Updating .delivery/config.yml or config-schema.md
- Writing user guides or tutorials beyond what README covers
- Setting up CI for testing (no test runner exists)
- NPM/PyPI publishing workflows
