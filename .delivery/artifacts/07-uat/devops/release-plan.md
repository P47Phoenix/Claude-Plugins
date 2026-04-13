# Release Plan: hardware-team Plugin v1.0.0

**Role:** Release Manager (Samwise Gamgee) | **Task:** release-plan | **References:** release-planning.md, rollback-strategies.md, versioning-patterns.md
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12

---

> "I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline. And carry it I shall -- every step of this release, from branch to merge, checked and double-checked like provisions for a long journey."

---

## Release Overview

**What:** Initial release (v1.0.0) of the hardware-team plugin -- a Claude Code plugin providing an 8-stage hardware delivery pipeline with 6 specialized roles (HW Product Owner, Electrical Engineer, PCB Layout Engineer, Manufacturing Engineer, Compliance Engineer, Test Engineer) and integration with the kicad-happy plugin for component sourcing, fabrication, analysis, and documentation.

**Scope:** All plugin files committed to the `Claude-Plugins` repository, marketplace registration, and git tag for the initial version.

**Stakeholders:** Repository owner (Michael Connelly), kicad-happy plugin maintainers, Claude Code users consuming the plugin.

**Timeline:**

| Milestone | Target Date | Notes |
|-----------|-------------|-------|
| Pre-release validation | 2026-04-12 | Same-day -- all files already in working tree |
| Feature branch creation | 2026-04-12 | Branch from main |
| PR creation and review | 2026-04-12 | Self-review for initial release |
| Merge to main | 2026-04-12 | After PR approval |
| Git tag `hardware-team-v1.0.0` | 2026-04-12 | Post-merge |
| Post-release verification | 2026-04-13 | Fresh session validation |

---

## 1. Pre-Release Checklist

> "Before we leave the Shire, Mr. Frodo, we check the pack. Every bit of rope, every wafer of lembas. Nothing gets left behind."

### 1.1 Plugin Structure Integrity

| # | Check | Verification Command | Expected |
|---|-------|---------------------|----------|
| 1 | Plugin entrypoint exists | `ls hardware-team/SKILL.md` | File exists |
| 2 | License present | `ls hardware-team/LICENSE.txt` | Apache 2.0 |
| 3 | All 7 skill directories | `ls hardware-team/skills/` | hardware-flow, hw-product-owner, electrical-engineer, pcb-layout-engineer, manufacturing-engineer, compliance-engineer, test-engineer |
| 4 | Each skill has SKILL.md | `find hardware-team/skills -name SKILL.md \| wc -l` | 7 |
| 5 | Hooks directory | `ls hardware-team/hooks/hooks.json` | Valid JSON |
| 6 | Hook scripts present | `ls hardware-team/hooks/*.py` | validate_session.py, check_kicad_happy.py, check_pipeline_bypass.py, check_kicad_file.py, drc_check.py, bom_drift.py |
| 7 | Hook scripts parse | `for f in hardware-team/hooks/*.py; do python -c "import py_compile; py_compile.compile('$f', doraise=True)"; done` | All OK |
| 8 | Shared scripts | `ls hardware-team/scripts/` | validate_config.py, security.py |
| 9 | Test fixtures | `ls hardware-team/references/test-fixtures/README.md` | File exists |
| 10 | Getting started guide | `ls hardware-team/references/getting-started.md` | File exists |
| 11 | Prerequisites doc | `ls hardware-team/references/prerequisites.md` | File exists |

### 1.2 Marketplace Registration

| # | Check | Expected |
|---|-------|----------|
| 1 | `marketplace.json` contains `hardware-team` entry | Entry present with name, description, source, skills array |
| 2 | Skills array lists 7 skill paths | `./hardware-team/skills/hardware-flow`, `./hardware-team/skills/hw-product-owner`, `./hardware-team/skills/electrical-engineer`, `./hardware-team/skills/pcb-layout-engineer`, `./hardware-team/skills/manufacturing-engineer`, `./hardware-team/skills/compliance-engineer`, `./hardware-team/skills/test-engineer` |
| 3 | All skill paths resolve to existing directories | Each path has a SKILL.md |
| 4 | Description is accurate | Matches plugin capabilities |

### 1.3 Config Schema Validation

| # | Check | Expected |
|---|-------|----------|
| 1 | `config-schema.md` documents all fields | Types, defaults, validation rules present |
| 2 | `validate_config.py` handles all schema fields | Covers schema_version "1.0" |
| 3 | Forward compatibility | Missing keys use defaults, unknown keys ignored, invalid values warn but don't crash |

### 1.4 Hook Security (SEC-01 through SEC-06)

| # | Check | Expected |
|---|-------|----------|
| 1 | JSON-only input parsing | All hooks use `json.loads()`, no `eval()`/`exec()` |
| 2 | No shell execution of input data | `subprocess.run(shell=False)` with argument lists only |
| 3 | Path validation | Traversal sequences rejected |
| 4 | YAML safe loading | All YAML uses `yaml.safe_load()` |
| 5 | All hooks exit 0 | Never block session on error |
| 6 | No secrets in code/config/references | Manual review |

### 1.5 kicad-happy Integration

| # | Check | Expected |
|---|-------|----------|
| 1 | `kicad-integration.md` contracts present | Contract version 1.0, target kicad-happy >=1.2.x |
| 2 | All 11 kicad-happy skill contracts documented | kicad, spice, digikey, mouser, lcsc, element14, jlcpcb, pcbway, bom, emc, kidoc |
| 3 | Role SKILL.md files document consumption | Each role lists which kicad-happy skills it invokes |
| 4 | Reimplementation guard text present | Each role SKILL.md warns against reimplementing kicad-happy functionality |

---

## 2. Git Operations

> "One step at a time, Mr. Frodo. Branch, commit, push, merge. Steady as she goes."

### 2.1 Branch Strategy

```
main (target)
  \
   feat/hardware-team-v1.0.0   <-- feature branch for initial release
```

**Branch naming:** `feat/hardware-team-v1.0.0`

### 2.2 Step-by-Step Git Operations

**Step 1: Create feature branch**

```bash
cd Claude-Plugins
git checkout main
git pull origin main
git checkout -b feat/hardware-team-v1.0.0
```

**Step 2: Stage all hardware-team files**

```bash
# Stage plugin files (excluding __pycache__)
git add hardware-team/SKILL.md
git add hardware-team/LICENSE.txt
git add hardware-team/hooks/hooks.json
git add hardware-team/hooks/check_kicad_happy.py
git add hardware-team/hooks/check_pipeline_bypass.py
git add hardware-team/hooks/check_kicad_file.py
git add hardware-team/hooks/validate_session.py
git add hardware-team/hooks/drc_check.py
git add hardware-team/hooks/bom_drift.py
git add hardware-team/scripts/validate_config.py
git add hardware-team/scripts/security.py
git add hardware-team/skills/
git add hardware-team/references/
git add .claude-plugin/marketplace.json
```

**Do NOT stage:**
- `hardware-team/hooks/__pycache__/` (bytecode cache)
- `hardware-team/scripts/__pycache__/` (bytecode cache)
- `.delivery/` artifacts (pipeline state, not plugin code)

**Step 3: Commit with conventional commit format**

```bash
git commit -m "feat(hardware-team): initial release v1.0.0

8-stage hardware delivery pipeline with 6 specialized roles,
kicad-happy integration (11 skills), 6 hooks, and setup wizard.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

**Step 4: Push branch and create PR**

```bash
git push -u origin feat/hardware-team-v1.0.0
```

### 2.3 Pull Request

**Title:** `feat(hardware-team): initial release v1.0.0`

**Body:**

```markdown
## Summary
- New hardware-team plugin with 8-stage pipeline orchestrator for structured hardware product development
- 6 hardware roles: HW Product Owner, Electrical Engineer, PCB Layout Engineer, Manufacturing Engineer, Compliance Engineer, Test Engineer
- kicad-happy integration consuming 11 skills with contract validation
- 6 hooks (SessionStart, PreToolUse, PostToolUse) for config validation, dependency checking, and file monitoring
- Setup wizard for `.hardware/config.yml` initialization

## Pre-Release Checklist
- [ ] All 7 skill directories present with valid SKILL.md
- [ ] hooks.json valid, all hook scripts parse without errors
- [ ] marketplace.json updated with hardware-team entry
- [ ] kicad-integration.md contracts match target kicad-happy version
- [ ] SEC-01 through SEC-06 security standards verified
- [ ] No __pycache__ directories committed
- [ ] No secrets or credentials in any file

## Test Plan
- [ ] Fresh Claude Code session loads hardware-team skills
- [ ] `hw-setup` wizard creates valid `.hardware/config.yml`
- [ ] SessionStart hooks fire (config check + kicad-happy check)
- [ ] PreToolUse hook warns on direct role skill invocation
- [ ] PostToolUse hook detects `.kicad_sch` / `.kicad_pcb` modifications
- [ ] Pipeline runs for at least 2 stages on test fixture
```

**Labels:** `enhancement`, `new-plugin`

**Reviewers:** Repository owner

### 2.4 Post-Merge: Tag and Push

After PR is merged to main:

```bash
git checkout main
git pull origin main
git tag hardware-team-v1.0.0
git push origin hardware-team-v1.0.0
```

### 2.5 Version Bump Commit

After tagging, bump the repository-level version:

```bash
# Update marketplace.json metadata.version
git checkout main
# Edit marketplace.json to bump version to 2.23.0
git add .claude-plugin/marketplace.json
git commit -m "chore: bump version to 2.23.0

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push origin main
```

---

## 3. Rollback Strategy

> "If the road ahead is blocked, we go back the way we came. No shame in it -- Gandalf himself would say the same."

### 3.1 Rollback Triggers

| Trigger | Severity | Action |
|---------|----------|--------|
| Plugin fails to load in Claude Code | Critical | Immediate rollback |
| Hook scripts crash or block sessions | Critical | Immediate rollback |
| kicad-happy contract validation fires false positives | High | Evaluate fix-forward vs rollback |
| SKILL.md content incorrect but non-blocking | Medium | Fix-forward (patch release) |
| Missing reference files cause agent errors | High | Fix-forward if quick, else rollback |

### 3.2 Rollback Procedure

**Option A: Revert the merge commit (preferred for initial release)**

```bash
# 1. Identify the merge commit
git log --oneline --merges -5

# 2. Revert the merge
git revert -m 1 <merge-commit-hash>

# 3. Push the revert
git push origin main

# 4. Delete the tag
git tag -d hardware-team-v1.0.0
git push origin --delete hardware-team-v1.0.0
```

**Option B: Revert specific files (surgical rollback)**

```bash
# 1. Remove hardware-team from marketplace.json (edit to remove the entry)
# 2. Commit the change
git add .claude-plugin/marketplace.json
git commit -m "chore(hardware-team): remove from marketplace (rollback)"
git push origin main
```

**Option C: Restore previous marketplace.json state**

```bash
# 1. Find the commit before hardware-team was added
git log --oneline -- .claude-plugin/marketplace.json

# 2. Restore marketplace.json from that commit
git checkout <pre-hw-commit> -- .claude-plugin/marketplace.json
git add .claude-plugin/marketplace.json
git commit -m "chore(hardware-team): rollback marketplace registration"
git push origin main
```

### 3.3 Cache Sync After Rollback

This step is mandatory after any rollback:

```bash
# 1. Identify active cache hash
HASH=$(ls -t ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/ | head -1)

# 2. If rolling back the entire plugin, remove cache
rm -rf ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/

# 3. If rolling back to a previous version, sync
rsync -a --delete ./hardware-team/ \
  ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/$HASH/hardware-team/

# 4. Restart Claude Code session
```

### 3.4 Rollback Decision Framework

| Factor | Roll Back | Fix Forward |
|--------|-----------|-------------|
| Root cause identified | Not required | Required |
| Fix complexity | N/A | Must be small and testable |
| Session-blocking issue | Roll back immediately | Only if fix deploys in < 5 minutes |
| Non-blocking issue | Not needed | Preferred |
| Multiple users affected | Roll back immediately | Only if fix deploys faster than rollback |

### 3.5 Rollback Communication

Since this is a repository-hosted plugin (not a live service), communication is via:

1. **GitHub Issue:** Create an issue documenting the rollback reason, affected version, and resolution timeline
2. **Commit message:** Conventional commit with clear rollback reason: `revert(hardware-team): rollback v1.0.0 due to [reason]`
3. **Tag cleanup:** Remove the `hardware-team-v1.0.0` tag to prevent users from referencing a broken version

---

## 4. Post-Release Verification

> "We don't just drop the Ring into Mount Doom and walk away, Mr. Frodo. We make sure it's properly destroyed. Same goes for a release -- we verify everything works."

### 4.1 Fresh Session Validation (T+0 to T+1)

| # | Verification | How | Expected Result |
|---|-------------|-----|-----------------|
| 1 | Plugin loads | Start fresh Claude Code session in a project directory | `hardware-team` appears in available skills |
| 2 | Skill discovery | Check available skills list | All 7 skills visible: hardware-flow, hw-product-owner, electrical-engineer, pcb-layout-engineer, manufacturing-engineer, compliance-engineer, test-engineer |
| 3 | SessionStart hooks fire | Check session start output | Config check and kicad-happy check hooks report status |
| 4 | Setup wizard works | Invoke `hardware-team:hardware-flow` with setup intent | `.hardware/config.yml` created with schema_version "1.0" |
| 5 | Pipeline starts | Run pipeline on test fixture | Concept stage (Stage 1) completes successfully |
| 6 | Pipeline continues | Continue pipeline | Schematic stage (Stage 2) accepts input from Stage 1 |
| 7 | PreToolUse hook | Invoke a role skill directly (outside pipeline) | Warning message about pipeline bypass |
| 8 | PostToolUse hook | Edit a `.kicad_sch` file | Notification about KiCad file modification |
| 9 | Config validation | Introduce an invalid config value | Hook warns but does not block session |
| 10 | Forward compatibility | Remove a config key | Hook uses default, does not crash |

### 4.2 Cross-Platform Verification (T+1 to T+3)

| Platform | Verified By | Status |
|----------|------------|--------|
| Windows 11 | Primary development platform | Verify during release |
| macOS | Secondary verification | Post-release |
| Linux | Secondary verification | Post-release |

Key cross-platform concerns:
- Path separators in hook scripts (`os.path` usage)
- Python 3.8+ availability
- `safe_join()` path construction in `security.py`
- YAML parsing compatibility

### 4.3 Regression Monitoring (T+1 to T+7)

| Metric | Target | Monitoring Method |
|--------|--------|-------------------|
| GitHub Issues filed | 0 critical, 0 high | GitHub Issue tracker |
| Hook script errors | 0 | User reports, session logs |
| kicad-happy contract false positives (HW-KCH-004) | 0 | Pipeline execution logs |
| Config forward-compatibility failures | 0 | User reports |
| Pipeline stage failures (non-user-error) | 0 | Pipeline execution logs |

### 4.4 Post-Release Retrospective Criteria

Conduct a release retrospective if any of the following occur:
- Any rollback was needed
- Any hotfix was needed within 48 hours
- Any SEV1/SEV2 issue reported
- Release timeline slipped by more than 1 day
- Pre-release checklist missed an issue found post-release

---

## 5. Version Management

> "Every good gardener labels the seeds, Mr. Frodo. You need to know what you planted and when."

### 5.1 Initial Version: 1.0.0

This is version 1.0.0 -- the first stable release defining the public API (skill contracts, config schema, hook behavior, pipeline stages).

**Version tracking locations for v1.0.0:**

| Location | Value | Purpose |
|----------|-------|---------|
| Git tag | `hardware-team-v1.0.0` | Release identifier |
| `marketplace.json` `metadata.version` | `2.23.0` (repo-level bump) | Repository-wide version |
| `.hardware/config.yml` `schema_version` | `"1.0"` | Config schema version |
| `kicad-integration.md` `contract_version` | `1.0` | kicad-happy output contract version |
| `kicad-integration.md` `kicad_happy_target_version` | `>=1.2.0` | Target kicad-happy compatibility |

### 5.2 Versioning Scheme: SemVer 2.0

| Version Component | When to Increment | Example |
|-------------------|-------------------|---------|
| **MAJOR** | Breaking: SKILL.md contracts changed, hook behavior changed, config schema (breaking), pipeline stage semantics changed | 1.0.0 -> 2.0.0 |
| **MINOR** | Additive: new role skills, new pipeline features, additive config fields, new references, enhanced hooks | 1.0.0 -> 1.1.0 |
| **PATCH** | Fixes: hook script bugs, reference corrections, SKILL.md clarifications, typos | 1.0.0 -> 1.0.1 |

### 5.3 Version Bump Protocol (Future Releases)

1. Make changes to plugin files
2. Update version references as needed:
   - Config schema changed? Bump `schema_version` in config-schema.md
   - kicad-happy contracts changed? Bump `contract_version` in kicad-integration.md
   - Breaking change? Update migration notes in SKILL.md
3. Bump repository-level `metadata.version` in marketplace.json
4. Commit with conventional commit: `feat(hardware-team):`, `fix(hardware-team):`, or `chore(hardware-team):`
5. Create git tag: `git tag hardware-team-v<VERSION>`
6. Push: `git push origin main && git push origin hardware-team-v<VERSION>`

### 5.4 Pre-Release Tags (If Needed)

| Tag | When to Use |
|-----|-------------|
| `hardware-team-v1.0.0-alpha.N` | Early development, structure may change |
| `hardware-team-v1.0.0-beta.N` | Feature-complete, testing in progress |
| `hardware-team-v1.0.0-rc.N` | Release candidate, only critical fixes |

For this initial release, we are going straight to v1.0.0 -- the plugin has been through a full delivery pipeline (Idea through UAT) and all artifacts are validated.

---

## Gitignore Considerations

Ensure `.gitignore` excludes:

```
# Python bytecode (must not be committed)
hardware-team/hooks/__pycache__/
hardware-team/scripts/__pycache__/

# User project config (project-specific, not plugin code)
.hardware/
```

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| __pycache__ directories accidentally committed | Low | Medium | Explicit `.gitignore` entries, PR review |
| Stale cache after merge | High | High | Mandatory cache sync in post-merge procedure |
| kicad-happy not installed by users | Medium | High | Graceful degradation documented; SessionStart hook warns |
| Hook scripts fail on Python < 3.8 | Medium | Low | Require Python 3.8+ in prerequisites; stdlib-only |
| marketplace.json merge conflict | Medium | Low | Single-purpose PR; merge promptly |
| Config schema v1.0 missing edge cases | Medium | Medium | Forward-compatibility protocol handles gracefully |

---

## Assumptions

- The Claude Code plugin harness supports the `hooks.json` format as defined
- Cross-plugin skill invocation via `<plugin>:<skill>` syntax works (verified for kicad-happy)
- Python 3.8+ is available on target platforms
- The kicad-happy plugin is installed separately by users who need full pipeline functionality
- Repository owner is available for PR review on release day
- No other PRs will create merge conflicts with marketplace.json during this release window

---

## Follow-Up (Post-Release)

- [ ] Add `hardware-team/hooks/__pycache__/` and `hardware-team/scripts/__pycache__/` to `.gitignore` if not already present
- [ ] Add `.hardware/` to `.gitignore` template documentation for user projects
- [ ] Evaluate `hw-doctor` diagnostic command for on-demand verification
- [ ] Document contract update procedure for kicad-happy maintainers
- [ ] Consider automated test fixture execution as a CI gate for future releases
- [ ] Capture release metrics: deployment duration, issues found, rollbacks needed

---

> "There now, Mr. Frodo. The plan's laid out proper -- every branch, every commit, every check. We know the way forward and we know the way back if things go sideways. That's the Gamgee way of doing things: careful, steady, and always with a plan for second breakfast... I mean, a rollback."
