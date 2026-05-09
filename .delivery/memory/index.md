# Delivery Pipeline Memory Index

- total_runs: 32
- last_updated: 2026-05-09
- last_run_id: run-2026-05-05-tk3

## Stage Health (last 5 runs)
- Idea: 60% first-try (tk3 required R2 — caught upstream scope clarification)
- Refine: 60% first-try (tk3 first-try; tk1 R1 misread gate criteria TARGET vs CURRENT)
- Design: 100% first-try (when light, DX surface) — also valid SKIP for DX-only deviation
- Architect: 60% first-try (tk3 required R2 — Phase-0 byte-offset inversion caught at Dev DoD; Wave 1+0 first-try)
- Plan: 100% first-try (tk3 first-try; Wave 1 caught real budget-math defect via Dev runs-the-command)
- Development: ~90% first-try per-story (tk3 first-try via mid-impl reference-extraction)
- UAT: 80% first-try (tk3 required R2 — producer-validator separation + stale Wave-N-1 carry-over sweep)

## Hot Lessons (inject into ALL agent prompts — top 6 by validation count + impact)

1. **Developer DoD runs the command, does not read the command.** On any artifact that names executable commands (grep, bash, path lookups, config keys), Developer DoD must actually run them from the repo root — reading is not enough. Three consecutive validations (04-20, 04-22, 05-03) confirm: this catches regex/path/type bugs that all reasoning-only validators miss. Most recent: caught PRD's "11 SKILL.md files" claim (actually 13). "Light mode" means reduced prose depth, not reduced command execution.
2. **PRD citation discipline is load-bearing for migration PRDs.** Every external claim cites a live URL; adversarial reviewer independently re-fetches load-bearing URLs.
3. **Mixed-version CI guards need allowlist-over-deny.** Canonical set pinned in `.github/workflows/stale-model-id-guard.yml`; everything else dated is stale. Provenance-comment exemption (`^\s*#`) travels with ADR-002.
4. **Honest readiness markers beat uniform.** Two-tier stamp (`opus-4-7` vs `opus-4-7-frontmatter-only`) names the work state. Uniform stamping lies cheaply.
5. **Dogfood-before-edit is the highest-leverage tone-risk discipline.** Runs-the-command at Refine + runs-the-dogfood at Development. Prose edits only if the empirical check fails — prevents drift-by-edit.
6. **Architect runs-the-command at DoD is binding for cache-prefix-impacting ADRs.** Run-2026-05-05-tk3 caught a Phase-0 byte-offset inversion (3603 vs actual 1803) that would have shipped a contract with backwards cache-prefix logic.

## Active Decisions
- [topics/claude-plugins-repo.md](topics/claude-plugins-repo.md) — keystone files, repo surface facts, config gotchas

## Stages
- [stages/idea.md](stages/idea.md) — plugin-dev skill routing MUST be in PO upfront context
- [stages/refine.md](stages/refine.md) — citation discipline, Dev DoD runs-the-command, two-loop convergence, success-gate ownership, PRDs-from-audit-prose-MUST-run-discovery
- [stages/architect.md](stages/architect.md) — ADR-revision pattern, binary status rule, single-artifact transformation-plan, cache-prefix-impacting ADRs need Dev runs-the-command (NEW)
- [stages/development.md](stages/development.md) — BUG_FIX consolidation, 14-WI FEATURE-execution, mid-implementation reference-extraction (NEW)
- [stages/plan.md](stages/plan.md) — per-wave vs per-WI commit cadence rule of thumb
- [stages/design.md](stages/design.md) — DX-surface light mode (single artifact + 2-validator DoD)
- [stages/uat.md](stages/uat.md) — PASS_WITH_NOTES; seven-gate PO rubric; cross-doc consistency; producer-validator separation; stale-carry-over sweep (NEW)

## Topics
- [topics/project-types.md](topics/project-types.md) — DESIGN + transformation-planning; FEATURE-execution-of-plan; DX-only Design-skip; per-wave commits; binding-decisions-in-memory
- [topics/gate-patterns.md](topics/gate-patterns.md) — validator selection, convergence, allowlist-over-deny CI guards, success-gate ownership, mid-run flag protocol
- [topics/claude-plugins-repo.md](topics/claude-plugins-repo.md) — project-specific facts (keystones, config, conventions)
- [topics/human-preferences.md](topics/human-preferences.md) — user-facing preferences; lotr theme performance
- [topics/defect-patterns.md](topics/defect-patterns.md) — defect-root-cause patterns
- [topics/skill-token-economy.md](topics/skill-token-economy.md) — 5 binding rulings + per-skill model map + tiered budgets; Wave 0/1/2/caveman-lite SHIPPED, Wave 3 PENDING (NEW)

## Archive
- [archive/run-2026-05-05-tk3.md](archive/run-2026-05-05-tk3.md) — FEATURE caveman-lite: Tier-A 500/500 ceiling held via mid-impl extraction; cache-prefix re-freeze accepted (ADR-tk3-001); GO; AC-13 telemetry deferred; producer-validator + stale-sweep lessons surfaced
- [archive/run-2026-05-05-tk2.md](archive/run-2026-05-05-tk2.md) — FEATURE Wave 2: doctrine extract + per-skill contracts/patterns + model split; GO with PASS_WITH_NOTES; 8 WIs in 5 stories
- [archive/run-2026-05-04-tk1.md](archive/run-2026-05-04-tk1.md) — FEATURE Wave 1: cache freeze + stages.yml + frontmatter rollout + challenger hook; GO; 7 WIs in 3 file-scope stories, 0 defects
## Initiative Retros
- [initiative-retros/skill-token-economy-meta-retro-2026-05-09.md] — delivery-team token-economy: 4/5 waves SHIPPED, Wave 3 deferred
