---
pipeline_id: run-2026-05-28-o48m
status: in_progress
project_type: FEATURE
detected_at: 2026-05-28
force_type: FEATURE
current_stage: 6
stages_completed: [1, 2, 4, 5]
stages_skipped: [3]
human_checkpoints_passed: []
final_verdict: null
follow_up: null
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
  pipeline.checkpoints: []
artifacts:
  idea-brief: .delivery/artifacts/01-idea/po/idea-brief.md
  prd: .delivery/artifacts/02-refine/po/prd.md
  constraints: .delivery/artifacts/02-refine/po/constraints.yml
  architecture: .delivery/artifacts/04-architect/solution/architecture.md
  adrs: .delivery/artifacts/04-architect/adrs/ADR-lmr-001..005 (Accepted)
  stage-4-summary: .delivery/artifacts/04-architect/stage-summary.md
  plan: .delivery/artifacts/05-plan/plan.md
  stage-5-summary: .delivery/artifacts/05-plan/stage-summary.md
last_updated: 2026-09-20
initiative: Latest-model references — remove version pinning repo-wide, adopt "latest version of model X", migrate stale 4.7 pins + smoke-test extension (BACKLOG-108)
binding_notes:
  - "One Role = One Sub-Agent (model-independent invariant; do not fuse roles); refer to the latest version of a model family, never pin a version string (user decision 2026-09-20; Opus 5 is the effective current model, cited only in dated citations and observed baselines); effort xhigh is a project choice (docs recommend high as start, see PRD OQ-5)"
  - "Local-only — no .github/workflows/smoke-*.yml (memory: feedback_claude_code_local_only.md)"
  - "Producer-validator separation: meta-test fixtures CANNOT share author with parser code"
  - "Behavioral claims MUST be doc-verified via WebFetch; adversarial reviewer independently re-fetches >=3 load-bearing claims"
  - "Post-merge: squash-rebase + ff-merge + push origin/main (no PR); Wave-N pattern"
  - "topics/latest-model-references.md (renamed from opus-5-migration.md) is the binding-decisions file; Section 0 records the latest-version reframing"
---

# Pipeline State — run-2026-05-28-o48m

Initiative: Latest-model references — version-free stamps and prose, pin-forbidding CI guard, central tier aliases, smoke-test extension recording the observed model (BACKLOG-108).

Routing (FEATURE, user-specified):
- Stage 1 Idea: light
- Stage 2 Refine: light
- Stage 3 Design: SKIP (DX-only — no end-user UX surface)
- Stage 4 Architect: light (single cache-fingerprint ADR; name may be version-free, PRD FR-6.2)
- Stage 5 Plan: light (file-scope stories S1-S7)
- Stage 6 Development: full
- Stage 7 UAT: full (includes live --init-baseline 5× on the latest Opus via alias `opus`, resolved model recorded; ~$15 budget acknowledged)
