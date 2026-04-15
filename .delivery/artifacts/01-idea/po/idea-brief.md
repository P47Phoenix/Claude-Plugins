# Idea Brief — Defect Sweep: Wizard Drift + Injection Guard + DoD Self-Match

**Artifact**: Idea Brief (Gandalf / PO)
**Project type**: BUG_FIX (fused Idea-full + Plan-light)
**Pipeline**: delivery-flow
**Date**: 2026-04-14

## Context

Four surgical defects/follow-ups bundled into one BUG_FIX sweep. All are small, well-bounded, and independent. No architecture board, no new features.

## Scope IN

### DEFECT-003a — Quick-Start wizard still asks removed project_type question
- **Evidence**: `delivery-team/skills/delivery-flow/SKILL.md:142` — "**What are you building?** -- auto-detect project type from the answer" (question 1 of Quick-Start Mode).
- **Mirror**: `delivery-team/skills/delivery-flow/references/getting-started.md:15` — "Question 1: What are you building?"
- **Defect**: Schema v2.7 removed `project_type`; Phase 1 detects per-run. Wizard content never caught up.
- **Fix**: Drop the question from the Quick-Start list in SKILL.md and getting-started.md. Optionally add a "pin force_type? (advanced, rarely needed)" follow-up.

### DEFECT-003b — No v2.6 → v2.7 config migration path
- **Evidence**: `.delivery/config.yml` in-repo was v2.6 with `project_type: FEATURE` until recently bumped. No loader step strips/bumps pre-v2.7 configs.
- **Defect**: Users on pre-v2.7 configs silently keep stale `project_type` pin.
- **Fix**: Document the migration contract in SKILL.md (or setup-wizard.md reference): on load, if `config_version: "2.6"` or missing → strip `project_type`, bump to `"2.7"`, announce. In-repo config.yml is already v2.7, so this is a forward guard for others pulling the plugin.

### Follow-up TC-12 — `check_dod_constraints.py` self-matches the constraints file
- **Evidence**: `delivery-team/skills/delivery-flow/scripts/check_dod_constraints.py:141-163` — `check_forbidden_vocab` greps the artifact for every token in `forbidden_vocabulary`. When the artifact IS the constraints file (or any artifact that declares/cites the vocabulary), the tokens' own text triggers false-positive matches.
- **Fix**: Add a `--skip-declarations` CLI flag. When set, exclude lines inside the artifact's own `forbidden_vocabulary:` block (header + indented list items) before grepping. Add a fixture so the script lints its own constraints doc without false positives.

### Regression guard for DEFECT-004 — workflow injection CI lint
- **Evidence**: DEFECT-004 Proposed Fix §4 — add CI lint that greps `.github/workflows/*.yml` for `${{ github.event.* }}` (and similar attacker-controllable expressions) interpolated inside `run:` blocks.
- **Fix**: New workflow job (or added to existing lint workflow) that multiline-greps each YAML file's `run:` blocks for `${{ github.event.*`, `${{ github.head_ref`, `${{ github.pull_request.*` and fails if any match. Prevents reintroduction across all workflows (version.yml, release.yml, docs.yml, future).

## Scope OUT / Anti-scope

- No schema bumps past v2.7. No wizard UX redesign. No new features.
- Do NOT touch: architecture-board skill, constraints primitive, MTG plugin, any v2.7-current behavior.
- Do NOT re-edit `.github/workflows/version.yml` (DEFECT-004 primary fix already landed).

## Success Criteria

1. Quick-Start wizard no longer lists a project-type question.
2. v2.6 → v2.7 migration contract is documented and dogfood-testable.
3. `check_dod_constraints.py --skip-declarations` passes against the constraints file itself.
4. CI lint fails fast on `${{ github.event.* }}` interpolation in any `run:` block.

## Handoff

BUG_FIX pipeline skips Design + Architect. Routes Refine → Plan (light) → Development → UAT. Each fix is individually small; no architectural ambiguity requiring Architect review (per `feedback_architect_examine_first` — defect reports already supply the target state).
