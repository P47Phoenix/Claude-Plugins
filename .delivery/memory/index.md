# Delivery Pipeline Memory Index

- total_runs: 27
- last_updated: 2026-04-20
- last_run_id: run-2026-04-20-o4v7

## Stage Health (last 5 runs)
- Idea: 100% first-try pass
- Refine: 50% first-try pass (2 revisions common when research-heavy)
- Design: 100% first-try pass (when light, DX surface)
- Architect: 50% first-try pass (1 revision common when multi-ADR)
- Development: 100% first-try pass on BUG_FIX consolidations

## Hot Lessons (inject into ALL agent prompts — top 5 by validation count + impact)

1. **Developer DoD catches command-validity bugs that no reasoning-only validator finds.** On any artifact that names executable commands (grep, bash, path lookups, config keys), Developer DoD must actually run them — reading is not enough.
2. **PRD citation discipline is load-bearing for migration PRDs.** Every external claim cites a live URL; adversarial reviewer independently re-fetches load-bearing URLs.
3. **ADR status is binary.** "Accepted (contingent on unfinished spike)" is a process smell — mark Proposed until the contingency resolves.
4. **Scope terminus held by logging, not by saying no.** Defer-but-log `BACKLOG-*.md` items when out-of-scope-but-valuable work is surfaced during Refine.
5. **Pair similar plugins for efficient parallel dispatch** (past dev run) — agentic-flow-builder + prd-quality-gate-flow are a natural pair; keystones should be sequenced before dependent skills.

## Active Decisions
- [topics/claude-plugins-repo.md](topics/claude-plugins-repo.md) — keystone files, repo surface facts, config gotchas

## Stages
- [stages/refine.md](stages/refine.md) — citation discipline, Dev DoD dogfooding, two-loop convergence
- [stages/architect.md](stages/architect.md) — ADR-revision pattern, binary status rule, single-artifact transformation-plan fit
- [stages/development.md](stages/development.md) — BUG_FIX consolidation lessons

## Topics
- [topics/project-types.md](topics/project-types.md) — DESIGN + transformation-planning, BUG_FIX consolidation, documentation patterns
- [topics/gate-patterns.md](topics/gate-patterns.md) — validator selection by defect class, convergence heuristics, signal robustness
- [topics/claude-plugins-repo.md](topics/claude-plugins-repo.md) — project-specific facts (keystones, config, conventions)

## Archive
- [archive/run-2026-04-20-o4v7.md](archive/run-2026-04-20-o4v7.md) — DESIGN/transformation-planning for 4.6→4.7 skill migration
