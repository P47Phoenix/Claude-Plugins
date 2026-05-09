# Delivery Pipeline Memory Index

- total_runs: 33
- last_updated: 2026-05-09
- last_run_id: run-2026-05-09-tk4

## Stage Health (last 5 runs)
- Idea: 80% first-try (tk4 first-try; tk3 R2)
- Refine: 80% first-try (tk4 + tk3 first-try)
- Design: 100% first-try (when light); valid SKIP for DX-only deviation (tk4)
- Architect: 60% first-try (tk4 R2 godot ceiling under mandatory-rollout; tk3 R2 byte-offset)
- Plan: 80% first-try (tk4 R2 QA coverage tally; tk3 first-try)
- Development: ~80% first-try per-story (tk4 5/7=71%; tk3 first-try via mid-impl extraction)
- UAT: 100% first-try (tk4 first-try GO_WITH_NOTES; tk3 R2)

## Hot Lessons (inject into ALL agent prompts — top 6 by validation count + impact)

1. **Developer DoD runs the command, does not read the command.** On any artifact that names executable commands (grep, bash, path lookups, config keys), Developer DoD must actually run them from the repo root — reading is not enough. 10x validated across waves; tk4 caught Stage-5 QA tally drift (49 vs 52). Light mode = reduced depth, NOT reduced command execution.
2. **PRD citation discipline is load-bearing for migration PRDs.** Every external claim cites a live URL; adversarial reviewer independently re-fetches load-bearing URLs.
3. **Mixed-version CI guards need allowlist-over-deny.** Canonical set pinned in `.github/workflows/stale-model-id-guard.yml`; provenance-comment exemption (`^\s*#`) travels with ADR-002.
4. **Honest readiness markers beat uniform.** Two-tier stamp (`opus-4-7` vs `opus-4-7-frontmatter-only`) names the work state.
5. **Dogfood-before-edit is the highest-leverage tone-risk discipline.** Runs-the-command at Refine + runs-the-dogfood at Development. Prose edits only if empirical check fails.
6. **QA coverage validator MUST enumerate ALL initiative ACs by ID** (count carefully; don't trust upstream tally). tk4 Pippin caught BACKLOG-104 had 10 init ACs (not 7); 3 unmapped. Same risk class as runs-the-command. (validated:1)

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
- [archive/run-2026-05-09-tk4.md](archive/run-2026-05-09-tk4.md) — FEATURE Wave 3: 7 stories/35 ACs/0 defects; 7 over-budget files cleared; 6 carry-forwards discharged; paradigm pattern shipped; INITIATIVE COMPLETE 5/5
- [archive/run-2026-05-05-tk3.md](archive/run-2026-05-05-tk3.md) — FEATURE caveman-lite: Tier-A 500/500 held via mid-impl extraction; cache re-freeze (ADR-tk3-001); producer-validator + stale-sweep lessons
- [archive/run-2026-05-05-tk2.md](archive/run-2026-05-05-tk2.md) — FEATURE Wave 2: doctrine extract + contracts/patterns + model split; 8 WIs in 5 stories
## Initiative Retros
- [initiative-retros/skill-token-economy-meta-retro-2026-05-09.md] — delivery-team token-economy: INITIATIVE COMPLETE 2026-05-09 (5/5 waves; amended post-Wave-3)
