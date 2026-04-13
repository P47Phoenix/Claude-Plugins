# Deployment Plan: hardware-team Plugin

**Role:** DevOps (Samwise Gamgee) | **Task:** deployment-strategy | **References:** deployment-strategies.md, rollback-strategies.md, versioning-patterns.md, release-planning.md
**Pipeline:** run-2026-04-12-hw01 | **Type:** GREENFIELD
**Date:** 2026-04-12

---

> "Now, Mr. Frodo, I know this deployment plan might seem like a long road through the Marshes, but I've packed every bit of lembas we'll need. Steady steps and careful planning -- that's how we get this plugin safely to its destination."

---

## 1. Plugin Installation

> "First things first -- you can't carry the Ring if you haven't packed your bag. Let's get this plugin properly installed."

### 1.1 Installation Method: Git-Based Plugin Registration

The hardware-team plugin is distributed as part of the `Claude-Plugins` repository. Installation follows the standard Claude Code plugin installation pattern.

**Step 1: Clone or update the repository**

```bash
# Fresh install
git clone https://github.com/P47Phoenix/Claude-Plugins.git
cd Claude-Plugins

# Existing install
cd Claude-Plugins
git pull origin main
```

**Step 2: Register the plugin with Claude Code**

The plugin is registered via the marketplace registry at `.claude-plugin/marketplace.json`. The hardware-team entry must be added to the `plugins` array:

```json
{
  "name": "hardware-team",
  "description": "Hardware delivery team with 8-stage pipeline orchestrator for structured hardware product development. Coordinates 6 hardware roles (HW Product Owner, Electrical Engineer, PCB Layout Engineer, Manufacturing Engineer, Compliance Engineer, Test Engineer) through concept-to-production pipeline. Consumes kicad-happy skills for component sourcing, fabrication, analysis, and documentation.",
  "source": "./",
  "strict": false,
  "skills": [
    "./hardware-team/skills/hardware-flow",
    "./hardware-team/skills/hw-product-owner",
    "./hardware-team/skills/electrical-engineer",
    "./hardware-team/skills/pcb-layout-engineer",
    "./hardware-team/skills/manufacturing-engineer",
    "./hardware-team/skills/compliance-engineer",
    "./hardware-team/skills/test-engineer"
  ]
}
```

**Step 3: Cache sync (local development)**

Source of truth: repository root `Claude-Plugins/hardware-team/`
Cache root: `~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/<hash>/hardware-team/`

```bash
# 1. Identify active cache hash
HASH=$(ls -t ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/ | head -1)

# 2. Sync source to cache
rsync -a --delete ./hardware-team/ \
  ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/$HASH/hardware-team/

# 3. Diff-verify: expect zero drift
diff -rq ./hardware-team/ \
  ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/$HASH/hardware-team/

# 4. Restart Claude Code session (cache read at session start)
```

**Step 4: Verify skill discovery**

After registration, Claude Code's harness loads Level 1 metadata (marketplace.json) automatically. Verify by checking that `hardware-team:hardware-flow` appears in the available skills list during a Claude Code session.

### 1.2 Installation Verification Checklist

| Check | Command / Method | Expected Result |
|-------|-----------------|-----------------|
| Plugin directory exists | `ls hardware-team/SKILL.md` | File exists |
| All 7 skill directories present | `ls hardware-team/skills/` | 7 directories listed |
| Each skill has SKILL.md | `find hardware-team/skills -name SKILL.md` | 7 SKILL.md files |
| Hooks directory present | `ls hardware-team/hooks/hooks.json` | File exists |
| 4 hook scripts present | `ls hardware-team/hooks/*.py` | 4 Python files |
| Marketplace entry valid | Parse `.claude-plugin/marketplace.json` | hardware-team entry with 7 skills |
| Shared scripts present | `ls hardware-team/scripts/*.py` | `config_schema.py`, `state_manager.py` |
| Test fixtures present | `ls hardware-team/references/test-fixtures/MANIFEST.md` | File exists |

---

## 2. Dependency Chain

> "You wouldn't go into Mordor without your rope, would you? The kicad-happy plugin is our rope -- we need it before we start climbing."

### 2.1 Required Dependency: kicad-happy Plugin

The hardware-team plugin has a **hard dependency** on the kicad-happy plugin. Hardware-team role skills invoke 11 kicad-happy skills via the Skill tool for schematic analysis, simulation, component sourcing, DFM, EMC, and documentation.

**Dependency relationship:**

```
hardware-team (consumer)
    |
    +-- kicad-happy:kicad        (EE, PCB Layout)
    +-- kicad-happy:spice        (EE)
    +-- kicad-happy:digikey      (EE)
    +-- kicad-happy:mouser       (EE)
    +-- kicad-happy:lcsc         (EE)
    +-- kicad-happy:element14    (EE)
    +-- kicad-happy:jlcpcb       (MfgE)
    +-- kicad-happy:pcbway       (MfgE)
    +-- kicad-happy:bom          (MfgE)
    +-- kicad-happy:emc          (CompE)
    +-- kicad-happy:kidoc        (CompE, MfgE)
```

### 2.2 Installation Order

1. **Install kicad-happy first** -- Must be available at `~/.claude/plugins/cache/kicad-happy/` before hardware-team pipeline execution
2. **Install hardware-team second** -- The SessionStart hook `check_kicad_happy.py` validates kicad-happy availability at session start

### 2.3 Version Compatibility

The `.hardware/config.yml` field `dependencies.kicad_happy_version` (default: `>=1.2.0`) specifies the minimum compatible kicad-happy version. The `check_kicad_happy.py` hook validates this at session start and warns on mismatch.

**Contract coupling**: hardware-team defines output contracts for all 11 consumed kicad-happy skills in `kicad-integration.md` (contract version 1.0, target kicad-happy >=1.2.x). Runtime contract validation (HW-KCH-004) catches breaking changes.

### 2.4 Graceful Degradation

If kicad-happy is not installed or partially available:

| Scenario | Behavior |
|----------|----------|
| kicad-happy not installed at all | SessionStart warning. Pipeline runs but role skills report `SKILL_UNAVAILABLE` for each missing capability. Manual data entry required. |
| Partial installation (e.g., 8/11 skills) | SessionStart reports missing skills. Affected stages degrade gracefully. Pipeline does NOT crash. |
| Version mismatch (below minimum) | SessionStart warning. Runtime contract validation catches structural drift. |
| Contract mismatch (kicad-happy output changed) | `HW-KCH-004` error at runtime. Sub-agent does NOT process malformed data. Gate evaluates on available data. |

---

## 3. Configuration: .hardware/config.yml Setup

> "Setting up camp properly before the night comes -- that's the secret, Mr. Frodo. A good config is like a well-pitched tent."

### 3.1 Directory Initialization

The hardware-team uses its own namespace (`.hardware/`) separate from delivery-flow's `.delivery/`. First-time setup creates the following structure:

```
.hardware/
├── config.yml              # Project configuration (created by setup wizard)
├── state.md                # Pipeline state (created by first pipeline run)
├── memory/                 # Self-learning memory (created by first pipeline completion)
│   └── index.md
└── artifacts/              # Pipeline artifacts (created per-stage)
    ├── 01-concept/
    ├── 02-schematic/
    ├── 03-layout/
    ├── 04-prototype/
    │   └── archived/       # Preserved rework artifacts (never deleted)
    ├── 05-dfm-dfa/
    ├── 06-compliance/
    ├── 07-pilot-run/
    └── 08-production-release/
```

### 3.2 Setup Wizard Flow (hw-setup)

The setup wizard creates `.hardware/config.yml` interactively. It follows the delivery-flow pattern of smart defaults with override options.

**Wizard questions:**

| # | Question | Config Key | Default | Options |
|---|----------|-----------|---------|---------|
| 1 | Project name? | `project_name` | (required) | Free text |
| 2 | Target fabricator? | `target_fab` | jlcpcb | jlcpcb, pcbway, custom |
| 3 | Compliance regions? | `compliance_regions` | [] | Multi-select: fcc, ce, ul, rohs, reach, none |
| 4 | BOM budget per unit (USD)? | `bom_budget` | null | Number or "no limit" |
| 5 | Require second source? | `second_source_required` | false | yes/no |
| 6 | Production volume? | `production_volume` | prototype | prototype, small-batch, production |
| 7 | Board layers? | `board_layers` | 2 | 1, 2, 4, 6, 8 |
| 8 | Gate strictness? | `gate_strictness` | standard | strict, standard, relaxed |
| 9 | Schematic review passes? | `review.schematic_review_passes` | 2 | 1-5 |

**Post-wizard actions:**

1. Write `.hardware/config.yml` with `schema_version: "1.0"` and `dependencies.kicad_happy_version: ">=1.2.0"`
2. Create `.hardware/artifacts/` directory tree (all 8 stage directories)
3. Create `.hardware/memory/` directory with empty `index.md`
4. Print confirmation: "hardware-team configured for [project_name]. Run `hardware-team:hardware-flow` to start the pipeline."

### 3.3 Config Validation at Session Start

The `check_hw_config.py` SessionStart hook validates the config on every session:

- **Missing config**: Warns user to run `hw-setup`
- **Schema version mismatch**: Reports migration guidance with new field defaults
- **Invalid field values**: Warns per-field, uses defaults (never blocks)
- **Paused pipeline detected**: Reports pipeline status and staleness (7-day warning, 30-day critical thresholds)
- **Always exits 0**: Informational only, never blocks session

### 3.4 Forward Compatibility Protocol

| Scenario | Behavior |
|----------|----------|
| Missing keys | Use defaults -- never fail on absent keys |
| Unknown keys | Ignore -- never fail on extra keys |
| Invalid values | Warn and use default -- never crash the pipeline |
| Old schema version | Announce: "Config uses schema vX.Y. Current is vA.B. New settings applied with defaults: [list]" |

---

## 4. Hooks Installation

> "These hooks are like the watchmen at the gate of Minas Tirith -- they see trouble coming before anyone else does."

### 4.1 Hook Architecture

The hardware-team plugin defines 4 hook scripts across 3 event types in `hardware-team/hooks/hooks.json`:

| Hook Script | Event Type | Matcher | Purpose | Timeout |
|-------------|-----------|---------|---------|---------|
| `check_hw_config.py` | SessionStart | `*` | Config validation + paused pipeline detection + staleness warning | 5s |
| `check_kicad_happy.py` | SessionStart | `*` | kicad-happy dependency check (11 skills, version compat) | 10s |
| `check_pipeline_bypass.py` | PreToolUse | `Skill` | Warns when role skills invoked outside pipeline | 5s |
| `check_kicad_file.py` | PostToolUse | `Write\|Edit` | Notifies when `.kicad_sch` or `.kicad_pcb` files modified | 5s |

### 4.2 Hook Installation

Hooks are installed automatically when the plugin is registered via marketplace.json. The Claude Code harness reads `hooks/hooks.json` from the plugin directory and registers the hooks.

**Manual verification:**

```bash
# 1. Validate hooks.json
python -c "import json; json.load(open('hardware-team/hooks/hooks.json')); print('OK')"

# 2. Syntax-check all hook scripts
for f in hardware-team/hooks/*.py; do
  python -c "import py_compile; py_compile.compile('$f', doraise=True)" && echo "$f OK"
done

# 3. Confirm Python is available
python --version  # Requires 3.8+
```

### 4.3 Hook Security Standards (SEC-06)

All hook scripts follow these mandatory standards:

- **JSON-only input parsing**: `json.loads()` -- never `eval()` or `exec()`
- **No shell execution of input data**: `subprocess.run(shell=False)` with argument lists only
- **Path validation**: File paths from `$TOOL_INPUT` validated against traversal sequences
- **Fail-safe**: Always exit 0 -- errors in input parsing logged as warnings, never block session
- **YAML safe loading**: All YAML parsing uses `yaml.safe_load()` (SEC-01)

### 4.4 Hook Environment Variables

| Variable | Provided By | Used In |
|----------|------------|---------|
| `$CLAUDE_PLUGIN_ROOT` | Claude Code harness | All hooks (path resolution to plugin directory) |
| `$TOOL_INPUT` | Claude Code harness | `check_pipeline_bypass.py` (skill name), `check_kicad_file.py` (file path) |

---

## 5. Version Management

> "Every good gardener labels the seeds, Mr. Frodo. You need to know what you planted and when."

### 5.1 Versioning Scheme: SemVer 2.0

The hardware-team plugin follows Semantic Versioning (MAJOR.MINOR.PATCH):

| Version Component | When to Increment | Example |
|-------------------|-------------------|---------|
| **MAJOR** | Breaking changes: SKILL.md contracts, hook behavior changes, config schema (breaking), pipeline stage semantics changed | 1.0.0 -> 2.0.0 |
| **MINOR** | New role skills, new pipeline features, additive config fields, new reference files, enhanced hooks | 1.0.0 -> 1.1.0 |
| **PATCH** | Bug fixes in hook scripts, reference file corrections, SKILL.md clarifications, typo fixes | 1.0.0 -> 1.0.1 |

### 5.2 Version Tracking Locations

| Location | What It Tracks |
|----------|---------------|
| `marketplace.json` (`metadata.version`) | Repository-wide version (all plugins) |
| `.hardware/config.yml` (`schema_version`) | Config schema version (currently "1.0") |
| `kicad-integration.md` (`contract_version`) | Output contract version per kicad-happy skill |
| `kicad-integration.md` (`kicad_happy_target_version`) | Target kicad-happy version range per contract |
| Git tags | Release versions (e.g., `hardware-team-v1.0.0`) |

### 5.3 Version Bump Protocol

1. Make changes to plugin files
2. Update version references:
   - Config schema changed? Bump `schema_version` in config-schema.md
   - kicad-happy contracts changed? Bump `contract_version` in kicad-integration.md
   - Breaking change? Update migration notes in SKILL.md
3. Bump repository-level `metadata.version` in marketplace.json
4. Commit with conventional commit format: `feat(hardware-team):`, `fix(hardware-team):`, `chore(hardware-team):`
5. Create git tag: `git tag hardware-team-v<VERSION>`
6. Push tag: `git push origin hardware-team-v<VERSION>`

### 5.4 Pre-Release Conventions

| Tag | Purpose | Example |
|-----|---------|---------|
| `-alpha.N` | Early development, structure may change | `hardware-team-v1.0.0-alpha.1` |
| `-beta.N` | Feature-complete, testing in progress | `hardware-team-v1.0.0-beta.1` |
| `-rc.N` | Release candidate, only critical fixes | `hardware-team-v1.0.0-rc.1` |

---

## 6. Rollback Strategy

> "If the road ahead is blocked, we go back the way we came. No shame in it -- Gandalf himself would say the same."

### 6.1 Rollback Mechanism: Git Revert + Cache Sync

Since the plugin is distributed via git, rollback means reverting to a previous known-good commit or tag, then syncing the cache.

**Immediate rollback procedure:**

```bash
# 1. Identify the last known-good version
git log --oneline -- hardware-team/

# 2. Option A: Revert to a specific tag (non-destructive)
git checkout hardware-team-v1.0.0 -- hardware-team/
git add hardware-team/
git commit -m "chore(hardware-team): rollback to v1.0.0"

# 3. Option B: Revert the breaking commit
git revert <commit-hash>

# 4. Cache sync (mandatory after any rollback)
HASH=$(ls -t ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/ | head -1)
rsync -a --delete ./hardware-team/ \
  ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/$HASH/hardware-team/

# 5. Diff-verify
diff -rq ./hardware-team/ \
  ~/.claude/plugins/cache/mec-claude-agent-skills/hardware-team/$HASH/hardware-team/

# 6. Restart Claude Code session
```

### 6.2 Config Schema Rollback

| Scenario | Rollback Behavior |
|----------|-------------------|
| Plugin downgrades from schema v1.1 to v1.0 | Unknown keys (v1.1 additions) ignored by v1.0 plugin. No user action needed. |
| Plugin downgrades from schema v2.0 to v1.0 (breaking) | Config may have incompatible values. SessionStart hook warns with specific invalid fields. User must regenerate config via `hw-setup`. |

### 6.3 Pipeline State Rollback

Pipeline state (`.hardware/state.md`) is forward-only within a run. Rollback of plugin code does NOT automatically invalidate an in-progress pipeline.

| Scenario | Action |
|----------|--------|
| Plugin rollback during active pipeline | Warn: "Plugin version changed during active pipeline run. Resume may behave differently. Consider: Restart pipeline, or complete current run first." |
| Plugin rollback with completed pipeline | No impact. Completed pipelines are read-only archives. |
| Plugin rollback with paused pipeline (awaiting human) | Staleness detection fires at next session start. User can Resume, Restart, or Abandon. |

### 6.4 kicad-happy Contract Rollback

If a kicad-happy upgrade introduces contract mismatches (HW-KCH-004):

1. Run test fixture (reference KiCad project) against new kicad-happy version to identify breaking contracts
2. **Option A: Roll back kicad-happy** to the previous compatible version
3. **Option B: Fix forward** -- update `kicad-integration.md` contracts to match new output structure
4. **Option C: Pin version** -- set `dependencies.kicad_happy_version` in config to the known-good version

### 6.5 Rollback Decision Framework

| Factor | Roll Back | Fix Forward |
|--------|-----------|-------------|
| Root cause identified | Not required | Required |
| Fix complexity | N/A | Must be small and testable |
| Active pipeline in progress | Prefer fix-forward to avoid state conflicts | Safe if change is isolated |
| kicad-happy contract broken | Roll back kicad-happy version | Update contracts if change is intentional |
| Multiple users affected | Roll back immediately | Only if fix deploys faster than rollback |

### 6.6 Stale Cache Risk

> Memory lesson: The #1 operational risk is stale cache. If you skip the rsync + diff-verify steps after a rollback, source edits are invisible to Claude Code. Always complete the full cache sync procedure.

---

## 7. Release Checklist

> "I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline. And I can make sure every item on this list is checked before we set out."

### 7.1 Pre-Release (T-2 days)

**Plugin structure integrity:**

- [ ] All 7 skill directories exist under `hardware-team/skills/`
- [ ] Each skill directory contains a valid SKILL.md with YAML frontmatter
- [ ] All reference files listed in SKILL.md files actually exist on disk
- [ ] `hardware-team/SKILL.md` (plugin entrypoint) is present and valid
- [ ] `hardware-team/LICENSE.txt` is present (Apache 2.0)
- [ ] `hardware-team/hooks/hooks.json` is valid JSON
- [ ] All 4 hook Python scripts parse without syntax errors
- [ ] `hardware-team/scripts/config_schema.py` and `state_manager.py` present
- [ ] `hardware-team/references/test-fixtures/MANIFEST.md` present with seeded defect list

**Marketplace registration:**

- [ ] `marketplace.json` contains hardware-team entry with 7 skill paths
- [ ] All skill paths in marketplace.json resolve to existing directories
- [ ] Plugin description is accurate and current

**Config schema:**

- [ ] `config-schema.md` documents all config fields with types, defaults, and validation rules
- [ ] `validate_config.py` handles all schema fields including new additions
- [ ] Forward compatibility verified: missing keys use defaults, unknown keys ignored
- [ ] Invalid values warn but use defaults (never crash)

**kicad-happy integration:**

- [ ] `kicad-integration.md` contracts match the target kicad-happy version
- [ ] Contract versions are correct and up to date
- [ ] Test fixture validates all 11 contracts against installed kicad-happy
- [ ] All role SKILL.md files correctly document their kicad-happy skill consumption
- [ ] Reimplementation guard text present in each role SKILL.md

**Hook scripts:**

- [ ] All hooks follow SEC-06 security standards (JSON parsing, no shell exec, path validation)
- [ ] All hooks exit 0 on all code paths (never block session)
- [ ] `check_hw_config.py`: detects missing config, invalid schema, paused pipeline, staleness
- [ ] `check_kicad_happy.py`: scans all 11 kicad-happy skills, validates version compatibility
- [ ] `check_pipeline_bypass.py`: identifies role skill invocations outside pipeline context
- [ ] `check_kicad_file.py`: detects `.kicad_sch` and `.kicad_pcb` file modifications

**Security (SEC-01 through SEC-06):**

- [ ] All YAML parsing uses `yaml.safe_load()` (never `yaml.load()`)
- [ ] All path construction uses `safe_join()` with `.hardware/` sandbox validation
- [ ] No pricing data captured in memory entry templates
- [ ] Hook scripts use `json.loads()` only, no `eval()`/`exec()`
- [ ] No secrets, API keys, or credentials in code, config, or reference files
- [ ] Path sanitization regex (`^[a-zA-Z0-9._-]+$`) applied at all construction points

**State management:**

- [ ] `state_manager.py` validates path components via whitelist regex
- [ ] `state_manager.py` canonicalizes paths and verifies `.hardware/` sandbox boundary
- [ ] State file integrity hash computed on write, verified on resume
- [ ] Resume protocol handles corrupted, incomplete, and tampered state files
- [ ] Staleness detection thresholds configurable (7-day warning, 30-day critical)

### 7.2 Release Day (T-0)

1. [ ] All pre-release checks pass
2. [ ] Version bumped in appropriate locations (see Section 5.3)
3. [ ] `git status` clean on main -- all feature PRs merged
4. [ ] Commit: `chore: bump version to X.Y.Z` with updated marketplace.json
5. [ ] Git tag created: `git tag hardware-team-v<VERSION>`
6. [ ] Tag pushed: `git push origin main && git push origin hardware-team-v<VERSION>`
7. [ ] Cache sync executed (rsync + diff-verify + session restart)
8. [ ] Verify plugin loads correctly in fresh Claude Code session
9. [ ] Run setup wizard (`hw-setup`) end-to-end and verify config creation
10. [ ] Run pipeline for at least 2 stages on the test fixture project
11. [ ] Verify both SessionStart hooks fire and report correctly
12. [ ] Verify PostToolUse hook fires on `.kicad_sch` file edit
13. [ ] Verify PreToolUse hook warns on direct role skill invocation

### 7.3 Post-Release (T+1 to T+3 days)

- [ ] Monitor for user-reported issues in GitHub Issues
- [ ] Check that kicad-happy contract validation is not firing false positives (HW-KCH-004)
- [ ] Verify hook scripts execute without errors on Windows, macOS, and Linux
- [ ] Confirm config forward-compatibility works with configs from previous schema versions
- [ ] Run full 8-stage pipeline on test fixture if not done during release day
- [ ] Capture release metrics: deployment duration, issues found, rollbacks needed
- [ ] Conduct release retrospective if any issues occurred

---

## 8. Trade-Off Analysis

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Git-based distribution + cache sync | Matches existing plugin pattern, version control built-in, no registry infra needed | Manual cache sync required, no auto-update notification | **Selected** -- proven pattern in this repo |
| Package registry (npm/pip-style) | Automatic updates, dependency resolution, version pinning | Overkill for Claude Code plugins, requires registry infrastructure, not how other plugins work | Rejected |
| Standalone installer script | One-command install | Maintenance burden, platform-specific, bypasses version control | Rejected |
| Monorepo version lock (all plugins share one version) | Simpler version management | Forces version bumps for unrelated plugin changes | Rejected for plugin-specific tags; repo version in marketplace.json remains shared |

---

## 9. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Stale cache after source changes | High | High | Mandatory rsync + diff-verify in every deploy/rollback procedure. SessionStart hooks provide early detection. |
| kicad-happy breaking change corrupts pipeline output | High | Medium | Runtime contract validation (HW-KCH-004), test fixture regression, version pinning in config |
| User manually edits `.hardware/state.md` | Medium | Medium | Integrity hash with advisory warning (accepted risk for local tool per SEC-05) |
| Hook scripts fail on non-standard Python installations | Medium | Low | Require Python 3.8+, stdlib-only (no pip install), syntax validation in release checklist |
| Config schema migration breaks existing projects | High | Low | Forward-compatibility protocol: missing keys default, unknown keys ignored, never crash |
| Platform path separator differences (Windows vs Unix) | Medium | Medium | `os.path` throughout, `safe_join()` for all path construction, cross-platform testing in release checklist |
| Cross-plugin trust boundary compromise | High | Very Low | Accepted platform-level risk per SEC-04. Contract validation catches structural mismatches but not semantic attacks. |

---

## 10. Assumptions

- The Claude Code plugin harness continues to support the `hooks.json` format as defined
- The Skill tool supports cross-plugin invocation via `<plugin>:<skill>` syntax (verified working)
- Python 3.8+ is available on all target platforms (no external dependencies required)
- The kicad-happy plugin is installed separately and maintained by its own release cycle
- Users have git access to the Claude-Plugins repository
- The marketplace.json format remains stable across Claude Code versions
- The `~/.claude/plugins/cache/` directory structure is the standard plugin cache location

---

## 11. Follow-Up

- [ ] Create `hardware-team/references/prerequisites.md` documenting kicad-happy installation steps with platform-specific notes
- [ ] Define automated test fixture execution as a pre-release gate (if CI is added to repository)
- [ ] Consider a `hw-doctor` diagnostic command that runs all verification checks on demand (install, config, hooks, kicad-happy, state)
- [ ] Document the contract update procedure in a contributor-facing guide for kicad-happy maintainers
- [ ] Add `.hardware/` to `.gitignore` template for user projects (config and state are project-specific, not committed to plugin repo)
- [ ] Evaluate whether `check_kicad_happy.py` should report installed kicad-happy version to sub-agents for contract version matching

---

> "There now, Mr. Frodo. The plan's all laid out, every provision accounted for, every watchman posted. When the time comes, we walk the road step by step. And if we stumble, we know exactly how to find our way back. That's the Gamgee way."
