# Deployment Strategy: Rules Engine Integration

**Version**: 1.0
**Date**: 2026-03-28
**Author**: Samwise Gamgee, DevOps (delivery-team)
**Status**: Draft
**Inputs**: Architecture v1.0, config-schema.md v2.3, SKILL.md, marketplace.json

> *"I can't deploy the feature for you, Mr. Frodo, but I can carry the pipeline."*

---

## 1. Distribution Model

This plugin is distributed via git clone/pull. There is no package registry, no build step, no compiled artifacts. Users get new features by pulling the latest from `main`.

**What this means for deployment**:
- "Deploying" = merging to `main` and users running `git pull`
- New Python scripts (C1-C4) land in `delivery-team/scripts/` — immediately available after pull
- New JSON rule files (C5-C11) land in `delivery-team/skills/delivery-flow/references/rules/` — immediately available after pull
- Modified files (SKILL.md, config-schema.md, etc.) update in place
- No install step, no migration runner, no database schema changes
- Python scripts use only stdlib (no `pip install` required)

---

## 2. Config Migration: v2.3 to v2.4

### 2.1 Migration Path

The config schema bumps from v2.3 to v2.4. Existing users have a `.delivery/config.yml` with `version: "2.3"` (or no version field).

**Forward compatibility**: v2.3 configs work with the v2.4 codebase unchanged. The rules engine has sensible defaults for every `rules.*` key:

| Key | Default if absent |
|-----|-------------------|
| `rules.preset` | `"standard"` |
| `rules.strict_mode` | `false` |
| `rules.escalation_sensitivity` | `"balanced"` |
| `rules.pass_threshold` | `{}` (use preset defaults) |
| `rules.routing_overrides` | `{}` (use preset defaults) |
| `rules.required_validators` | `{}` (use preset defaults) |
| `rules.custom` | `[]` (no custom rules) |

**This means**: A user who does nothing after `git pull` gets the standard preset with all defaults. The pipeline behaves the same as before — routing decisions that were previously made by AI judgment will now be made deterministically using the same routing table the AI was following from prose.

### 2.2 Migration Triggers

The `check_config.py` hook (SessionStart) is modified in Phase 2 to:

1. Detect `version: "2.3"` (or missing version)
2. Print an informational message (not blocking): `"Config v2.3 detected. Rules engine defaults apply. Run the setup wizard to configure rules.* options (questions W-15 through W-17)."`
3. NOT block the session — the pipeline runs fine without explicit rules config
4. If the user runs the setup wizard, the wizard appends the `rules.*` section and bumps the version to `"2.4"`

### 2.3 Manual Migration (for users who skip the wizard)

Add to `.delivery/config.yml`:

```yaml
version: "2.4"

# --- Rules Engine Configuration ---
rules:
  preset: standard          # solo | standard | strict
  strict_mode: false
  escalation_sensitivity: balanced  # relaxed | balanced | aggressive
```

That is the minimal migration. All other `rules.*` keys are optional.

---

## 3. Feature Flagging and Rollback

### 3.1 Feature Flag: `rules.enabled`

The architecture does not include a top-level kill switch. We add one:

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `rules.enabled` | boolean | `true` | Master switch for the rules engine |

**Behavior when `rules.enabled: false`**:

- `evaluate_rules.py` exits immediately with exit code 0 and a passthrough response:
  ```json
  {
    "decision_type": "routing",
    "bypassed": true,
    "reason": "Rules engine disabled via config (rules.enabled: false)"
  }
  ```
- SKILL.md orchestrator protocol includes a check: if the response contains `"bypassed": true`, the orchestrator falls back to the pre-rules-engine behavior (AI-interpreted prose decisions)
- This flag is checked BEFORE any rule loading, context validation, or evaluation — zero overhead when disabled

**Why this matters**: If the rules engine produces unexpected routing or gate decisions, the user can disable it with a one-line config change and immediately return to the previous AI-driven behavior. No git revert needed. No branch switching. One line.

### 3.2 Rollback Procedure

**Level 1 — Disable via config** (seconds, no git changes):
```yaml
rules:
  enabled: false
```
Pipeline reverts to AI-interpreted decisions. All rules engine code remains on disk but is never invoked. This is the fastest rollback.

**Level 2 — Revert to pre-rules SKILL.md** (minutes, git revert):
If the modified SKILL.md itself causes issues (not just rule outcomes), revert the SKILL.md changes:
```bash
git log --oneline delivery-team/skills/delivery-flow/SKILL.md
# Find the commit before Phase 3 SKILL.md changes
git checkout <pre-phase-3-commit> -- delivery-team/skills/delivery-flow/SKILL.md
```
The Python scripts and JSON rules remain on disk but are never called because the orchestrator prompt no longer references them.

**Level 3 — Full revert** (minutes, git revert):
```bash
# Revert the merge commit(s) for rules engine phases
git revert <phase-3-merge> <phase-2-merge> <phase-1-merge> <phase-0-merge>
```
This removes all rules engine code. The config.yml `rules.*` section becomes dead config (ignored by v2.3 check_config).

### 3.3 Rollback Decision Matrix

| Symptom | Rollback Level | Action |
|---------|---------------|--------|
| Wrong routing (stages too light/heavy) | 1 | Set `rules.enabled: false` or adjust `rules.routing_overrides` |
| Gate too strict/lenient | 1 | Adjust `rules.pass_threshold.<stage>` or set `rules.enabled: false` |
| evaluate_rules.py crashes (exit code 1) | 1 | Set `rules.enabled: false`, file bug |
| SKILL.md orchestrator loop (infinite context assembly) | 2 | Revert SKILL.md to pre-Phase-3 |
| Fundamental design flaw discovered | 3 | Full revert of all phase PRs |

---

## 4. Branch Strategy

### 4.1 Branch Layout

The implementation has 4 phases with clear dependency ordering. Each phase gets its own feature branch off `main`:

```
main
 ├── feature/rules-engine-phase-0    (C1 extraction + routing spec)
 ├── feature/rules-engine-phase-1    (C2-C4 + C5, C9-C11: adapter, CLI, routing rules, presets)
 ├── feature/rules-engine-phase-2    (C6-C8 + config v2.4 + hook updates + audit trail)
 └── feature/rules-engine-phase-3    (SKILL.md integration + wizard + dogfooding)
```

### 4.2 Dependency Chain

```
Phase 0 ──merge──> main
                     |
Phase 1 (branch from post-Phase-0 main) ──merge──> main
                                                      |
Phase 2 (branch from post-Phase-1 main) ──merge──> main
                                                      |
Phase 3 (branch from post-Phase-2 main) ──merge──> main
```

Each phase branches from `main` AFTER the previous phase is merged. No long-lived feature branches. No rebasing across phases.

### 4.3 Why Sequential, Not Parallel

Phases 1-3 each depend on the prior phase's merged code:
- Phase 1 imports from `condition_evaluator.py` (Phase 0)
- Phase 2 uses `delivery_rules_adapter.py` (Phase 1) for gate/escalation rules
- Phase 3 invokes `evaluate_rules.py` (Phase 1) from SKILL.md and references config schema v2.4 (Phase 2)

Parallel branches would require cross-branch imports or duplicated code. Sequential is cleaner for a 4-person-week feature.

---

## 5. PR Strategy

### 5.1 One PR Per Phase

| PR | Branch | Content | Size Estimate |
|----|--------|---------|---------------|
| PR-1 | `feature/rules-engine-phase-0` | `condition_evaluator.py` + `routing-decision-spec.md` | ~400 lines new Python + 1 reference doc |
| PR-2 | `feature/rules-engine-phase-1` | `delivery_rules_adapter.py` + `yaml_to_rules.py` + `evaluate_rules.py` + `routing.json` + 3 preset JSONs | ~800 lines new Python + ~300 lines JSON |
| PR-3 | `feature/rules-engine-phase-2` | `dod-gates.json` + `escalation.json` + `collaboration.json` + config-schema v2.4 + `check_config.py` mod + audit trail | ~200 lines Python changes + ~500 lines JSON |
| PR-4 | `feature/rules-engine-phase-3` | SKILL.md changes + setup-wizard.md + quality-gates.md + dogfooding results | ~200 lines prompt changes + validation report |

### 5.2 Why Not One Large PR

- The architecture defines 11 components across 4 phases with explicit exit criteria per phase
- One large PR would be ~2000+ lines touching scripts, JSON data, markdown prompts, and hooks — unreviewable
- Sequential PRs let each phase be validated independently (Phase 0's exit criteria: "All BRE condition tests pass against extracted module")
- If Phase 2 reveals a design issue, we haven't yet modified SKILL.md (Phase 3) — easier to course-correct

### 5.3 PR Review Checklist (All Phases)

Each PR must include:

- [ ] All new Python scripts run without errors: `python <script> --help` (or `--dry-run`)
- [ ] No external dependencies added (stdlib only)
- [ ] JSON files are valid: `python -m json.tool <file>.json`
- [ ] Exit criteria from architecture Section 8 are met
- [ ] `rules.enabled: false` bypass path tested (PR-2 onward)

---

## 6. JSON Rules Versioning

### 6.1 Version Field

Each JSON rule file includes a `"version": "1.0"` field at the top level. This is a documentation version, not a runtime-enforced schema version.

### 6.2 Update Strategy

Rule files are plugin code, not user data. They update when users pull from `main`. There is no merge conflict risk because users never edit these files — user customization goes in `.delivery/config.yml` (Layer 3) which is git-ignored per project.

**Version bump policy**:
- Patch (1.0 -> 1.1): Adding new rules, adjusting weights/thresholds
- Minor (1.0 -> 2.0): Changing rule IDs, removing rules, changing condition structure
- Breaking changes require a migration note in the PR description and a `check_config.py` warning

### 6.3 Preset Stability

Presets (`solo.json`, `standard.json`, `strict.json`) define the user-facing behavior contract. Changes to presets are user-visible behavior changes and must be:

1. Documented in the PR description with before/after `--dry-run --compare` output
2. Called out in release notes (version bump changelog)
3. Announced with a `check_config.py` informational message on first session after update

---

## 7. Deployment Sequence (The Road There and Back Again)

### 7.1 Phase 0 — The Foundation Stone

```
1. Create branch: feature/rules-engine-phase-0
2. Implement condition_evaluator.py (extracted from BRE)
3. Author routing-decision-spec.md (PO deliverable)
4. Validate: python condition_evaluator.py (unit-level verification)
5. PR-1 -> main, merge after review
```

**Rollback**: Delete the file. Nothing depends on it yet.

### 7.2 Phase 1 — The Main Road

```
1. Create branch: feature/rules-engine-phase-1 (from post-Phase-0 main)
2. Implement C2 (adapter), C3 (yaml_to_rules), C4 (evaluate_rules CLI)
3. Author routing.json + 3 preset JSONs
4. Add rules.enabled feature flag to evaluate_rules.py
5. Validate:
   - python evaluate_rules.py --dry-run --context test-context.json --rules-dir rules/
   - 10 identical runs produce byte-identical output (determinism check)
   - rules.enabled: false produces bypassed response
6. PR-2 -> main, merge after review
```

**Rollback**: `rules.enabled: false` or delete scripts + JSON directory.

### 7.3 Phase 2 — The Deep Places

```
1. Create branch: feature/rules-engine-phase-2 (from post-Phase-1 main)
2. Author dod-gates.json, escalation.json, collaboration.json
3. Bump config-schema.md to v2.4, add rules.* keys
4. Update check_config.py for v2.3->v2.4 migration messaging
5. Implement audit trail in evaluate_rules.py
6. Regenerate JSON schema via generate-schema.py
7. Validate:
   - Gate evaluations return correct decisions
   - Escalation rules trigger at correct thresholds
   - check_config.py prints migration message for v2.3 configs
   - Audit JSONL written correctly
8. PR-3 -> main, merge after review
```

**Rollback**: `rules.enabled: false`. Config v2.4 is backward-compatible; v2.3 configs still work.

### 7.4 Phase 3 — There and Back Again

```
1. Create branch: feature/rules-engine-phase-3 (from post-Phase-2 main)
2. Update SKILL.md with Rules Engine Invocation Protocol
3. Extend setup-wizard.md with W-15, W-16, W-17
4. Update quality-gates.md preamble
5. DOGFOODING: Run a real pipeline through delivery-flow using the rules engine
6. Capture dogfooding results as validation evidence
7. Validate:
   - Full pipeline run completes with rules engine active
   - rules.enabled: false reverts to pre-rules behavior
   - Setup wizard writes correct rules.* config
8. PR-4 -> main, merge after review
9. Bump version (2.10.1 -> 2.11.0 — this is a feature, not a patch)
```

**Rollback**: Level 1 (config flag) or Level 2 (revert SKILL.md).

---

## 8. Post-Deployment Monitoring

There is no telemetry, no logging service, no uptime monitor. This is a local plugin. "Monitoring" means:

1. **Audit trail review**: After each pipeline run, check `.delivery/audit/audit-<id>.jsonl` for unexpected decisions
2. **Determinism check**: Periodically run `evaluate_rules.py --dry-run` and diff against previous output
3. **User feedback**: GitHub issues on the plugin repo
4. **Self-improvement loop**: The delivery-flow pipeline already has a defect tracking system that triggers plugin self-improvement PRs — rules engine bugs flow through this existing mechanism

---

## 9. Version Bump Plan

| Merge Event | Version | Rationale |
|------------|---------|-----------|
| PR-1 (Phase 0) | No bump | Internal extraction, no user-facing change |
| PR-2 (Phase 1) | No bump | New scripts exist but nothing invokes them yet |
| PR-3 (Phase 2) | No bump | Config schema updated but backward-compatible |
| PR-4 (Phase 3) | 2.11.0 | User-facing behavior change: rules engine active in pipeline |

Single version bump at the end. Users who pull mid-implementation get inert files that do nothing until Phase 3 lands.

---

## 10. Summary

The road is long, but we take it one step at a time. The key decisions:

1. **Zero-friction migration**: v2.3 configs work unchanged. Defaults match current behavior.
2. **One-line rollback**: `rules.enabled: false` disables everything instantly.
3. **Sequential PRs**: 4 PRs matching 4 architecture phases. Each independently reviewable and revertable.
4. **No build step**: Python stdlib only. `git pull` is the deployment.
5. **Presets are the UX**: Solo developers write 2 lines of config. Power users get 4 layers of customization.

Now, Mr. Frodo, the road goes ever on — but at least we know where it leads.
