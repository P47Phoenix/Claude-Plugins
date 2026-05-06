# Delivery Flow Config Keys Reference

All settings applied to the pipeline when a `.delivery/config.yml` is loaded.
Defaults for missing keys are sourced from `references/config-schema.md`.

| Config Key | Pipeline Behavior |
|-----------|-------------------|
| `routing.force_type` | Optional opt-in pin. Phase 1 detection still runs, but routing uses the pin. Banner announces the override. Valid values: same enum as Phase 1 detection. Default: null. |
| `pipeline.enforce_self_write_block` | When true (default on fresh v2.7 configs), activates `enforce_pipeline_scope.py` soft-deny for orchestrator-origin writes to `.delivery/artifacts/**`. False for tolerantly-parsed v2.6 configs. |
| `pipeline.checkpoints` | Enables/disables human checkpoints per stage |
| `pipeline.collaboration_patterns` | Enables/disables patterns per stage |
| `pipeline.max_self_correction` | Overrides default iteration limit (default: 3) |
| `pipeline.max_dod_rounds` | Overrides default DoD rounds (default: 3) |
| `dod_validators.*` | Sets per-stage validator roles |
| `compliance.frameworks` | Triggers Compliance Officer and Privacy Engineer involvement |
| `team.size` | Influences architecture decisions (microservices viability, etc.) |
| `deployment.environment` | Influences DevOps and operations planning |
| `timeline.risk_tolerance` | Influences pattern depth and ceremony level |
| `tech_stack.*` | Passed to Developer and Architect for language/framework context |
| `tech_stack.paradigm` | Default paradigm for multi-paradigm languages (auto/oop/fp/hybrid) |
| `tech_stack.paradigm_by_language` | Per-language paradigm override (e.g., python: oop, typescript: fp) |
| `tech_stack.nx_workspace` | Whether Nx monorepo reference is loaded (auto-detected from nx.json) |
| `personas.categories` | Which persona categories to load (gamers, web-users, enterprise, demographics) |
| `personas.selected` | Specific persona names to include in every feedback round |
| `personas.feedback_stages` | Which pipeline stages run persona feedback (default: refine, design, dev, uat) |
| `personas.custom` | Custom persona definitions (see user-feedback skill's `references/custom-personas.md`) |
| `enforcement.source_code_hook` | Whether project-level PreToolUse hook warns on Edit/Write outside pipeline |
| `enforcement.retro_frequency` | How often retrospectives are required (every-run / every-n-runs / manual) |
| `enforcement.retro_skip_allowed` | Whether "skip retro" is allowed (false for mission-critical) |
| `git.branch_strategy` | Branching strategy for feature branches |
| `git.auto_branch` | Whether to auto-create branches at Plan stage |
| `git.commit_convention` | Commit message convention (conventional commits) |
| `git.clean_tree_check` | Whether UAT validates clean working tree |
| `github.create_issues` | Whether to create GitHub issues from user stories at Refine |
| `github.create_pr` | Whether to create a PR at UAT stage |
| `github.link_commits` | Whether commit messages reference issue numbers |
| `notifications.channels` | Which notification channels to use (console, file, slack, github-discussion) |
| `notifications.events` | Which events trigger notifications (complete, abort, escalation, checkpoint, defect-threshold) |
| `pipeline.scope` | What file types go through the pipeline (code-only / all / custom) |
| `pipeline.scope_include` | Custom glob patterns for pipeline scope (when scope=custom) |
| `pipeline.scope_exclude` | Patterns always excluded from pipeline enforcement |
| `aliases.theme` | Which alias theme to load for agent personality injection (default: business) |
| `aliases.custom_path` | Directory for custom theme files (default: `.delivery/aliases/`) |
