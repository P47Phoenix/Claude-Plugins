# Delivery Pipeline Memory Index

- total_runs: 31
- last_updated: 2026-05-05
- last_run_id: run-2026-05-05-tk2

## Stage Health (last 5 runs)
- Idea: 60% first-try pass (run-2026-05-04-tk1: 1 revision — Architect caught BACKLOG-101 phantom filename `agent_audit.py` vs actual `audit_agent_prompt.py`; same lesson family as Wave 0)
- Refine: 50% first-try pass (run-2026-05-04-tk1: 1 revision — Dev R1 misread gate criteria TARGET vs CURRENT)
- Design: 100% first-try pass (when light, DX surface) — also valid SKIP for DX-only deviation
- Architect: 80% first-try pass (Wave 1 first-try; Wave 0 first-try)
- Plan: 80% first-try pass — Wave 1 caught real budget-math defect (W1-7 -1 + W1-4 +1 = 201 not 200) requiring revision
- Development: ~85% first-try pass per-story (Wave 1: 5/9 stage-stories first-try; one Story 1 QA false-positive on path lookup)
- UAT: 90% first-try (Wave 1 first-try; Wave 0 needed R2 for cross-doc consistency that's now standard)

## Hot Lessons (inject into ALL agent prompts — top 5 by validation count + impact)

1. **Developer DoD runs the command, does not read the command.** On any artifact that names executable commands (grep, bash, path lookups, config keys), Developer DoD must actually run them from the repo root — reading is not enough. Three consecutive validations (04-20, 04-22, 05-03) confirm: this catches regex/path/type bugs that all reasoning-only validators miss. Most recent: caught PRD's "11 SKILL.md files" claim (actually 13). "Light mode" means reduced prose depth, not reduced command execution.
2. **PRD citation discipline is load-bearing for migration PRDs.** Every external claim cites a live URL; adversarial reviewer independently re-fetches load-bearing URLs.
3. **Mixed-version CI guards need allowlist-over-deny.** Canonical set pinned in `.github/workflows/stale-model-id-guard.yml`; everything else dated is stale. Provenance-comment exemption (`^\s*#`) travels with ADR-002.
4. **Honest readiness markers beat uniform.** Two-tier stamp (`opus-4-7` vs `opus-4-7-frontmatter-only`) names the work state. Uniform stamping lies cheaply.
5. **Dogfood-before-edit is the highest-leverage tone-risk discipline.** Runs-the-command at Refine + runs-the-dogfood at Development. Prose edits only if the empirical check fails — prevents drift-by-edit.

## Active Decisions
- [topics/claude-plugins-repo.md](topics/claude-plugins-repo.md) — keystone files, repo surface facts, config gotchas

## Stages
- [stages/idea.md](stages/idea.md) — plugin-dev skill routing MUST be in PO upfront context (NEW)
- [stages/refine.md](stages/refine.md) — citation discipline, Dev DoD runs-the-command, two-loop convergence, no-new-CLI-deps, success-gate ownership, PRDs-from-audit-prose-MUST-run-discovery (NEW)
- [stages/architect.md](stages/architect.md) — ADR-revision pattern, binary status rule, single-artifact transformation-plan fit
- [stages/development.md](stages/development.md) — BUG_FIX consolidation, 14-WI FEATURE-execution pattern
- [stages/plan.md](stages/plan.md) — per-wave vs per-WI commit cadence rule of thumb
- [stages/design.md](stages/design.md) — DX-surface light mode (single artifact + 2-validator DoD)
- [stages/uat.md](stages/uat.md) — PASS_WITH_NOTES convention; seven-gate PO rubric; cross-doc consistency check (NEW)

## Topics
- [topics/project-types.md](topics/project-types.md) — DESIGN + transformation-planning; FEATURE-execution-of-plan pattern; DX-only Design-skip; per-wave commits; two-tier stamps; binding-decisions-in-memory (NEW)
- [topics/gate-patterns.md](topics/gate-patterns.md) — validator selection, convergence, signal robustness, allowlist-over-deny CI guards, provenance+allowlist pair, success-gate ownership, mid-run flag protocol, mandatory-rollout-side-effects (NEW)
- [topics/claude-plugins-repo.md](topics/claude-plugins-repo.md) — project-specific facts (keystones, config, conventions)
- [topics/human-preferences.md](topics/human-preferences.md) — user-facing preferences; lotr theme performance (NEW)
- [topics/defect-patterns.md](topics/defect-patterns.md) — defect-root-cause patterns
- [topics/skill-token-economy.md](topics/skill-token-economy.md) — 5 binding rulings + per-skill model map + tiered line budgets (audit 2026-05-03)

## Archive
- [archive/run-2026-05-05-tk2.md](archive/run-2026-05-05-tk2.md) — FEATURE Wave 2: doctrine extract + per-skill contracts/patterns + model split; GO with PASS_WITH_NOTES; 8 WIs in 5 stories; 4 known-debt files cleared (delivery-flow 497, developer 296, product-delivery 299, architect Tier-A 500); architect Tier-B + 6 others remain for Wave 3
- [archive/run-2026-05-04-tk1.md](archive/run-2026-05-04-tk1.md) — FEATURE Wave 1: cache freeze + stages.yml + frontmatter rollout + challenger hook; GO; 7 WIs shipped via 3 file-scope stories, 0 defects, alias-creator graduated from known-debt
- [archive/run-2026-05-03-tk0e.md](archive/run-2026-05-03-tk0e.md) — FEATURE Wave 0: telemetry hook + line-budget CI gate; GO; 2 stories shipped, 0 defects, 4/7 stages first-try DoD
- [archive/run-2026-04-22-4x7e.md](archive/run-2026-04-22-4x7e.md) — FEATURE: 14-WI Opus 4.7 execution engagement; GO; PR #86
- [archive/run-2026-04-20-o4v7.md](archive/run-2026-04-20-o4v7.md) — DESIGN/transformation-planning for 4.6→4.7 skill migration
