# Delivery Pipeline Memory Index

- total_runs: 28
- last_updated: 2026-04-23
- last_run_id: run-2026-04-22-4x7e

## Stage Health (last 5 runs)
- Idea: 100% first-try pass
- Refine: 60% first-try pass (run-2026-04-22-4x7e: 1 round of G-1..G-6 self-correction; rounds-to-green = 2)
- Design: 100% first-try pass (when light, DX surface)
- Architect: 67% first-try pass (1 revision common when multi-ADR; run-2026-04-22-4x7e was drift-check-only, first-try)
- Plan: 100% first-try pass on FEATURE-execution engagements
- Development: 100% first-try pass on BUG_FIX consolidations + on run-2026-04-22-4x7e FEATURE execution (14/14 WIs, all dogfoods PASS first-try)
- UAT: 100% first-try PASS_WITH_NOTES pattern emerging

## Hot Lessons (inject into ALL agent prompts — top 5 by validation count + impact)

1. **Developer DoD runs the command, does not read the command.** On any artifact that names executable commands (grep, bash, path lookups, config keys), Developer DoD must actually run them from the repo root — reading is not enough. Two consecutive validations (04-20, 04-22) confirm: this catches regex/path/type bugs that all reasoning-only validators miss. "Light mode" means reduced prose depth, not reduced command execution.
2. **PRD citation discipline is load-bearing for migration PRDs.** Every external claim cites a live URL; adversarial reviewer independently re-fetches load-bearing URLs.
3. **Mixed-version CI guards need allowlist-over-deny.** Canonical set pinned in `.github/workflows/stale-model-id-guard.yml`; everything else dated is stale. Provenance-comment exemption (`^\s*#`) travels with ADR-002.
4. **Honest readiness markers beat uniform.** Two-tier stamp (`opus-4-7` vs `opus-4-7-frontmatter-only`) names the work state. Uniform stamping lies cheaply.
5. **Dogfood-before-edit is the highest-leverage tone-risk discipline.** Runs-the-command at Refine + runs-the-dogfood at Development. Prose edits only if the empirical check fails — prevents drift-by-edit.

## Active Decisions
- [topics/claude-plugins-repo.md](topics/claude-plugins-repo.md) — keystone files, repo surface facts, config gotchas

## Stages
- [stages/refine.md](stages/refine.md) — citation discipline, Dev DoD runs-the-command, two-loop convergence, no-new-CLI-deps, success-gate ownership
- [stages/architect.md](stages/architect.md) — ADR-revision pattern, binary status rule, single-artifact transformation-plan fit
- [stages/development.md](stages/development.md) — BUG_FIX consolidation, 14-WI FEATURE-execution pattern
- [stages/plan.md](stages/plan.md) — per-wave vs per-WI commit cadence rule of thumb
- [stages/design.md](stages/design.md) — DX-surface light mode (single artifact + 2-validator DoD)
- [stages/uat.md](stages/uat.md) — PASS_WITH_NOTES convention; seven-gate PO rubric

## Topics
- [topics/project-types.md](topics/project-types.md) — DESIGN + transformation-planning; FEATURE-execution-of-plan pattern; DX-only Design-skip; per-wave commits; two-tier stamps
- [topics/gate-patterns.md](topics/gate-patterns.md) — validator selection, convergence, signal robustness, allowlist-over-deny CI guards, provenance+allowlist pair, success-gate ownership, mid-run flag protocol
- [topics/claude-plugins-repo.md](topics/claude-plugins-repo.md) — project-specific facts (keystones, config, conventions)
- [topics/human-preferences.md](topics/human-preferences.md) — user-facing preferences
- [topics/defect-patterns.md](topics/defect-patterns.md) — defect-root-cause patterns

## Archive
- [archive/run-2026-04-22-4x7e.md](archive/run-2026-04-22-4x7e.md) — FEATURE: 14-WI Opus 4.7 execution engagement; GO; PR #86
- [archive/run-2026-04-20-o4v7.md](archive/run-2026-04-20-o4v7.md) — DESIGN/transformation-planning for 4.6→4.7 skill migration
