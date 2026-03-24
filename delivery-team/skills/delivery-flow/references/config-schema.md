# Config Schema Reference

Single source of truth for `.delivery/config.md` format. The setup wizard, pipeline, and all skills reference this file for config keys, types, defaults, and valid values.

## Current Version: 1.6

When adding new config keys, bump the version and add a migration note.

## Complete Schema

| Key | Type | Required | Default | Valid Values | Wizard Q# | Consumed By |
|-----|------|----------|---------|-------------|-----------|-------------|
| `config_version` | string | yes | "1.5" | semver string | auto | delivery-flow (migration check) |
| `project_type` | string | yes | FEATURE | GREENFIELD, FEATURE, BUG_FIX, GAME_DEV+GREENFIELD, GAME_DEV+FEATURE, GAME_DEV+BUG_FIX, SPIKE, DOCS_ONLY | Q1 | delivery-flow (stage routing) |
| `tech_stack.languages` | list[string] | yes | [] | language names | Q2 | developer (language detection), architect |
| `tech_stack.frameworks` | list[string] | no | [] | framework names | Q2 | architect, developer (frontend) |
| `tech_stack.databases` | list[string] | no | [] | database names | Q2 | architect (data modeling) |
| `tech_stack.ci_cd` | string | no | "none" | github-actions, circleci, jenkins, gitlab-ci, azure-pipelines, none | Q2 (auto) | operations (DevOps) |
| `tech_stack.paradigm` | string | no | "auto" | auto, oop, fp, hybrid | Q2 | developer (cross-language reference selection) |
| `tech_stack.paradigm_by_language` | map[string, string] | no | {} | language → oop/fp/hybrid | Q2 | developer (per-language paradigm override) |
| `tech_stack.nx_workspace` | boolean | no | false (auto-detected from nx.json) | true/false | Q2 (auto) | developer (Nx reference loading) |
| `architecture.style` | string | no | "auto" | auto, layered, hexagonal, clean, modular-monolith, microservices, event-driven, serverless | Q11 | architect (pattern selection) |
| `architecture.style_overrides` | map[string, string] | no | {} | component → style | Q11 | architect (per-component style) |
| `architecture.decomposition` | string | no | "auto" | auto, volatility, ddd, team-topology, event-storming, business-capability | Q11 | architect (decomposition strategy) |
| `architecture.decision_matrix_inputs` | object | no | auto | team_size, deploy_independence, domain_complexity, change_rate (each: low/medium/high) | Q11 | architect (constraint-based recommendation) |
| `enforcement.source_code_hook` | boolean | no | true | true/false | Q12 | setup wizard (project-level hook installation) |
| `enforcement.retro_frequency` | string | no | "every-run" | every-run, every-n-runs, manual | Q12 | delivery-flow (Stop hook behavior) |
| `enforcement.retro_skip_allowed` | boolean | no | false | true/false (default varies by risk_tolerance) | Q12 | delivery-flow (Stop hook) |
| `team.size` | integer | yes | 1 | 1+ | Q3 | architect (microservices viability) |
| `team.composition` | list[string] | no | [] | role identifiers | Q3 | pipeline routing |
| `deployment.environment` | string | no | "cloud-aws" | cloud-aws, cloud-gcp, cloud-azure, on-premise, edge, serverless, hybrid | Q4 | architect, operations |
| `deployment.containerized` | boolean | no | false | true/false | Q4 (derived) | operations (DevOps) |
| `timeline.risk_tolerance` | string | no | "standard" | prototype, standard, mission-critical, regulated | Q5 | pipeline (pattern depth, ceremony level) |
| `timeline.deadline` | string/null | no | null | ISO date or null | Q5 | product-delivery (sprint planning) |
| `compliance.frameworks` | list[string] | no | [] | HIPAA, GDPR, CCPA, PCI-DSS, SOC2, ISO27001 | Q6 | architect (compliance/privacy roles) |
| `pipeline.checkpoints` | list[string] | no | [refine, architect, plan, uat] | subset of: refine, architect, plan, uat | Q7 | delivery-flow (human checkpoint gates) |
| `pipeline.collaboration_patterns` | list[string] | no | [evaluator-optimizer, adversarial, review-board, debate, consensus, decision-routing] | subset of the 6 patterns | Q8 | delivery-flow (stage collaboration) |
| `pipeline.max_self_correction` | integer | no | 3 | 1-5 | Q8 (default) | delivery-flow (iteration limit) |
| `pipeline.max_dod_rounds` | integer | no | 3 | 1-5 | Q8 (default) | delivery-flow (DoD validation) |
| `dod_validators.idea` | list[string] | no | [po, architect] | role identifiers | defaults | delivery-flow (Stage 1 DoD) |
| `dod_validators.refine` | list[string] | no | [po, architect, qa] | role identifiers | defaults | delivery-flow (Stage 2 DoD) |
| `dod_validators.design` | list[string] | no | [ux, po, qa, architect] | role identifiers | defaults | delivery-flow (Stage 3 DoD) |
| `dod_validators.architect` | list[string] | no | [architect, qa, devops, security] | role identifiers | defaults | delivery-flow (Stage 4 DoD) |
| `dod_validators.plan` | list[string] | no | [sm, po, qa, devops] | role identifiers | defaults | delivery-flow (Stage 5 DoD) |
| `dod_validators.development` | list[string] | no | [developer, qa, architect, tech-writer] | role identifiers | defaults | delivery-flow (Stage 6 DoD) |
| `dod_validators.uat` | list[string] | no | [qa, devops, po, tech-writer] | role identifiers | defaults | delivery-flow (Stage 7 DoD) |
| `personas.categories` | list[string] | no | auto (from project_type) | gamers, web-users, enterprise, demographics | Q10 | user-feedback (library selection) |
| `personas.selected` | list[string] | no | auto (from categories) | persona names from library | Q10 | user-feedback (specific personas) |
| `personas.feedback_stages` | list[string] | no | [refine, design, dev, uat] | subset of: refine, design, dev, uat | Q10 | delivery-flow (when to invoke user-feedback) |
| `personas.count` | integer | no | 5 | 3-7 | Q10 | user-feedback (how many to spawn) |
| `personas.overlays` | list[string] | no | [] | Gen Z Zara, Millennial Mike, Gen X Grace, Boomer Bob | Q10 | user-feedback (demographic overlays) |
| `personas.custom` | list[object] | no | [] | persona profile objects | Q10 | user-feedback (custom personas) |
| `aliases.theme` | string | no | "business" | any built-in or custom theme name | Q13 | delivery-flow (personality injection) |
| `aliases.custom_path` | string | no | ".delivery/aliases/" | directory path | defaults | delivery-flow (custom theme lookup) |
| `git.branch_strategy` | string | no | "github-flow" | trunk-based, github-flow, gitflow, none | Q14 | delivery-flow (branch creation) |
| `git.auto_branch` | boolean | no | true | true/false | Q14 | delivery-flow (auto-create branches at Plan) |
| `git.commit_convention` | string | no | "conventional" | conventional, none | Q14 | delivery-flow (commit suggestions at Dev) |
| `git.clean_tree_check` | boolean | no | true | true/false | Q14 | delivery-flow (UAT validation) |
| `github.create_issues` | boolean | no | false | true/false | Q14 | delivery-flow (issue creation at Refine) |
| `github.create_pr` | boolean | no | false | true/false | Q14 | delivery-flow (PR creation at UAT) |
| `github.link_commits` | boolean | no | true | true/false | Q14 | delivery-flow (commit linking at Development) |
| `monorepo.enabled` | boolean | no | false (auto-detected) | true/false | Q2 (auto) | delivery-flow (monorepo mode) |
| `monorepo.tool` | string | no | "none" | nx, turbo, lerna, pnpm, none | Q2 (auto) | delivery-flow (tool-specific commands) |
| `monorepo.scope` | string | no | "root" | root, per-package | Q2 | delivery-flow (pipeline scope) |
| `wizard_completed` | string | yes | auto | ISO date | auto | delivery-flow (staleness check) |

---

## Defaults by Project Type

When a key is not set, use the default from the schema above. Some defaults vary by project type:

| Key | GREENFIELD | FEATURE | BUG_FIX | GAME_DEV+ | SPIKE | DOCS_ONLY |
|-----|-----------|---------|---------|-----------|-------|-----------|
| `pipeline.checkpoints` | all 4 | [refine, uat] | [uat] | all 4 | [] | [uat] |
| `personas.categories` | [web-users] | [web-users] | [] | [gamers] | [] | [] |
| `pipeline.collaboration_patterns` | all 6 | all 6 | [evaluator-optimizer, decision-routing] | all 6 | [evaluator-optimizer] | [evaluator-optimizer] |

---

## Extension Protocol

When adding a new feature that needs configuration:

### Step 1: Add to Schema

Add the new key to the schema table above with:
- Type, required/optional, default value
- Valid values
- Which wizard question populates it (or "auto" / "defaults")
- Which skill(s) consume it

### Step 2: Bump Version

Increment `config_version` (e.g., 1.0 to 1.1). Document what changed in the Version History table below.

### Step 3: Add Wizard Question (if interactive)

If the key should be asked during wizard setup:
- Add a question (Q11, Q12, etc.) to `setup-wizard.md`
- Follow the existing pattern: auto-detect, present, options (3-5 + Custom + Skip + Let's discuss)

If the key is auto-detected or uses defaults only, mark it "auto" in the Wizard Q# column.

### Step 4: Add to Pipeline Config Table

Add the key to the "Config Settings Applied to Pipeline" table in `delivery-flow/SKILL.md`.

### Step 5: Add Migration Note

Add an entry to the Version History table. When the pipeline detects an older `config_version`, it knows which keys to add with defaults.

### Step 6: Update Consuming Skill

Update the skill that reads the new key to reference `config-schema.md` for the default value.

---

## Migration Protocol

When the pipeline reads a config with an older `config_version`:

1. **Detect**: Compare config's `config_version` to current schema version.
2. **List changes**: Show which keys were added since that version.
3. **Apply defaults**: For each missing key, use the default from this schema.
4. **Offer wizard re-run**: "Your config is version [old]. Current schema is [new]. New settings available: [list]. Run `setup` to configure these, or defaults will be used."
5. **Update version**: After applying defaults, update `config_version` in the file.
6. **Never remove keys**: Migration is always additive. Old keys are never deleted.

### Handling Missing `config_version`

Configs created before versioning was added have no `config_version` field. Treat these as version 0.9 (pre-versioning) and apply all 1.0 defaults for missing keys.

---

## Config File Template

The complete template (generated by the wizard):

```yaml
---
config_version: "1.6"
project_type: GREENFIELD
tech_stack:
  languages: [TypeScript, Python]
  frameworks: [Next.js, FastAPI]
  databases: [PostgreSQL]
  ci_cd: github-actions
  paradigm: auto
  paradigm_by_language:
    python: hybrid
    typescript: hybrid
  nx_workspace: false
architecture:
  style: auto
  style_overrides: {}
  decomposition: auto
  decision_matrix_inputs:
    team_size: 4
    deploy_independence: medium
    domain_complexity: high
    change_rate: medium
enforcement:
  source_code_hook: true
  retro_frequency: every-run
  retro_skip_allowed: false
team:
  size: 4
  composition: [frontend, backend, qa, devops]
deployment:
  environment: cloud-aws
  containerized: true
timeline:
  risk_tolerance: standard
  deadline: null
compliance:
  frameworks: [GDPR]
pipeline:
  checkpoints: [refine, architect, plan, uat]
  collaboration_patterns: [evaluator-optimizer, adversarial, review-board, debate, consensus, decision-routing]
  max_self_correction: 3
  max_dod_rounds: 3
dod_validators:
  idea: [po, architect]
  refine: [po, architect, qa]
  design: [ux, po, qa, architect]
  architect: [architect, qa, devops, security]
  plan: [sm, po, qa, devops]
  development: [developer, qa, architect, tech-writer]
  uat: [qa, devops, po, tech-writer]
personas:
  categories: [gamers, web-users]
  selected: [Casual Casey, Hardcore Hank, Accessible Alex]
  feedback_stages: [refine, design, dev, uat]
  count: 5
  overlays: []
  custom: []
aliases:
  theme: business
  custom_path: .delivery/aliases/
monorepo:
  enabled: false
  tool: none
  scope: root
git:
  branch_strategy: github-flow
  auto_branch: true
  commit_convention: conventional
  clean_tree_check: true
github:
  create_issues: false
  create_pr: false
  link_commits: true
wizard_completed: 2026-03-22
---
```

---

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-22 | Initial schema: project_type, tech_stack, team, deployment, timeline, compliance, pipeline, dod_validators, personas, wizard_completed |
| 1.1 | 2026-03-23 | Added tech_stack.paradigm (oop/fp/hybrid/auto), tech_stack.paradigm_by_language (per-language override), tech_stack.nx_workspace (auto-detected) |
| 1.2 | 2026-03-23 | Added architecture.style, architecture.style_overrides, architecture.decomposition, architecture.decision_matrix_inputs |
| 1.3 | 2026-03-24 | Added enforcement.source_code_hook, enforcement.retro_frequency, enforcement.retro_skip_allowed; SessionStart hook for config check |
| 1.4 | 2026-03-24 | Added aliases.theme, aliases.custom_path for agent alias theme system |
| 1.5 | 2026-03-23 | Added git.branch_strategy, git.auto_branch, git.commit_convention, git.clean_tree_check for pipeline git integration; added github.create_issues, github.create_pr, github.link_commits for GitHub issue/PR integration |
| 1.6 | 2026-03-23 | Added monorepo.enabled (auto-detected), monorepo.tool (nx/turbo/lerna/pnpm/none), monorepo.scope (root/per-package) for multi-project monorepo orchestration |
