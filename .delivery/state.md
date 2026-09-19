---
pipeline_id: run-2026-09-19-models
status: completed
project_type: FEATURE
detected_at: 2026-09-19
current_stage: 7
stages_completed: [1, 2, 4, 5, 6, 7]
stages_skipped: [3]
human_checkpoints_passed: []
routing:
  idea: light
  refine: light
  design: skip
  architect: light
  plan: light
  development: full
  uat: full
config_snapshot:
  config_version: "2.7"
  prose_style: caveman-lite
  aliases.theme: lotr
  parallel_validators: true
  max_self_correction: 3
  max_dod_rounds: 3
artifacts:
  stories: .delivery/artifacts/05-plan/po/stories.md
  architecture: .delivery/artifacts/04-architect/solution/architecture.md
  adr: .delivery/artifacts/04-architect/adrs/ADR-models-001-guard-allowlist.md
  prd: .delivery/artifacts/02-refine/po/prd.md
  constraints: .delivery/artifacts/02-refine/po/constraints.yml
  idea-brief: .delivery/artifacts/01-idea/po/idea-brief.md
final_verdict: GO_WITH_NOTES
last_updated: 2026-09-19
initiative: Update all hard-coded model IDs in repo to latest (claude-fable-5-1, claude-opus-5, claude-sonnet-5, claude-haiku-4-5-20251001) on PR #88 branch
binding_notes:
  - "User chose scope: ALL model literals repo-wide (not just PR line), on branch delivery-team-agent-wrappers in .claude/worktrees/pr88"
  - "User added 2026-09-19: Fable 5.1 (claude-fable-5-1) is also a current model; include in allowlist decisions"
  - "Out of scope unless PO decides otherwise: model_awareness stamps in 34 SKILL.md; .delivery/ historical artifacts"
  - "Conflicts with unshipped BACKLOG-108 (Opus 4.8 migration, untracked in main checkout): retarget, do not duplicate"
  - "Guard is static grep only, no claude CLI in CI (memory: feedback_claude_code_local_only.md)"
  - "Commit/push only on user approval"
---

# Pipeline State — run-2026-09-19-models
