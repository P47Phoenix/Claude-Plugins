# Configuration Reference

All configuration lives in `.delivery/config.yml` (pure YAML, no frontmatter). The setup wizard generates this file. Current schema version: **2.6**.

## Complete Config Key Reference

### Core Settings

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `config_version` | string | "2.6" | semver | Schema version for migration |
| `project_type` | string | FEATURE | GREENFIELD, FEATURE, BUG_FIX, GAME_DEV+GREENFIELD, GAME_DEV+FEATURE, GAME_DEV+BUG_FIX, SPIKE, DOCS_ONLY | Project type for stage routing |
| `wizard_completed` | string | auto | ISO date | When the wizard last ran |

### Tech Stack

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `tech_stack.languages` | list | [] | language names | Programming languages in use |
| `tech_stack.frameworks` | list | [] | framework names | Frameworks in use |
| `tech_stack.databases` | list | [] | database names | Databases in use |
| `tech_stack.ci_cd` | string | "none" | github-actions, circleci, jenkins, gitlab-ci, azure-pipelines, none | CI/CD platform |
| `tech_stack.paradigm` | string | "auto" | auto, oop, fp, hybrid | Default paradigm for multi-paradigm languages |
| `tech_stack.paradigm_by_language` | map | {} | language: oop/fp/hybrid | Per-language paradigm override |
| `tech_stack.nx_workspace` | boolean | false | true/false | Auto-detected from nx.json |
| `tech_stack.clean_code_guide` | string | "" | file path | Custom clean code guide (empty = built-in) |
| `tech_stack.clean_code_enforcement` | string | "block" | block, warn | Clean code enforcement level |

### Architecture

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `architecture.style` | string | "auto" | auto, layered, hexagonal, clean, modular-monolith, microservices, event-driven, serverless | Architecture style |
| `architecture.style_overrides` | map | {} | component: style | Per-component style override |
| `architecture.decomposition` | string | "auto" | auto, volatility, ddd, team-topology, event-storming, business-capability | Decomposition strategy |
| `architecture.decision_matrix_inputs` | object | auto | team_size, deploy_independence, domain_complexity, change_rate | Constraint-based recommendation inputs |

### Team & Deployment

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `team.size` | integer | 1 | 1+ | Team size (influences architecture decisions) |
| `team.composition` | list | [] | role identifiers | Team role composition |
| `deployment.environment` | string | "cloud-aws" | cloud-aws, cloud-gcp, cloud-azure, on-premise, edge, serverless, hybrid | Deployment target |
| `deployment.containerized` | boolean | false | true/false | Whether containers are used |
| `timeline.risk_tolerance` | string | "standard" | prototype, standard, mission-critical, regulated | Risk tolerance level |
| `timeline.deadline` | string/null | null | ISO date or null | Project deadline |

### Compliance

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `compliance.frameworks` | list | [] | HIPAA, GDPR, CCPA, PCI-DSS, SOC2, ISO27001 | Compliance frameworks to enforce |

### Pipeline Settings

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `pipeline.checkpoints` | list | [refine, architect, plan, uat] | subset of: refine, architect, plan, uat | Human checkpoint stages |
| `pipeline.collaboration_patterns` | list | all 6 | subset of 6 patterns | Active collaboration patterns |
| `pipeline.max_self_correction` | integer | 3 | 1-5 | Max self-correction iterations |
| `pipeline.max_dod_rounds` | integer | 3 | 1-5 | Max DoD validation cycles |
| `pipeline.max_parallel_agents` | integer | 3 | 1-10 | Parallel dispatch cap |
| `pipeline.parallel_stories` | boolean | true | true/false | Parallel story implementation |
| `pipeline.parallel_validators` | boolean | true | true/false | Parallel DoD validation |
| `pipeline.scope` | string | "code-only" | code-only, all, custom | Pipeline enforcement scope |
| `pipeline.scope_include` | list | [] | glob patterns | Custom scope patterns |
| `pipeline.scope_exclude` | list | [".delivery/", ".git/", ...] | glob patterns | Always excluded patterns |
| `pipeline.verify_skill_loading` | boolean | true | true/false | SKILL_LOADED marker check |
| `pipeline.delegation_retry_max` | integer | 2 | 1-5 | Retry failed delegations |
| `pipeline.isolation_audit` | string | "warn" | off, warn, block | Agent prompt audit level |
| `pipeline.metadata_max_chars` | integer | 200 | 50-500 | Signal summary character limit |
| `pipeline.agent_timeout` | integer | 120 | 30-600 | Per-agent timeout (seconds) |
| `pipeline.required_agent_retry_max` | integer | 2 | 1-5 | Retry for required agents in parallel groups |

### Enforcement

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `enforcement.source_code_hook` | boolean | true | true/false | Warn on edits outside pipeline |
| `enforcement.retro_frequency` | string | "every-run" | every-run, every-n-runs, manual | Retrospective frequency |
| `enforcement.retro_skip_allowed` | boolean | false | true/false | Whether "skip retro" is allowed |

### DoD Validators

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `dod_validators.idea` | list | [po, architect] | Stage 1 validators |
| `dod_validators.refine` | list | [po, architect, qa] | Stage 2 validators |
| `dod_validators.design` | list | [ux, po, qa, architect] | Stage 3 validators |
| `dod_validators.architect` | list | [architect, qa, devops, security] | Stage 4 validators |
| `dod_validators.plan` | list | [sm, po, qa, devops] | Stage 5 validators |
| `dod_validators.development` | list | [developer, qa, architect, tech-writer] | Stage 6 validators |
| `dod_validators.uat` | list | [qa, devops, po, tech-writer] | Stage 7 validators |

### Personas

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `personas.categories` | list | auto | gamers, web-users, enterprise, demographics | Persona categories |
| `personas.selected` | list | auto | persona names | Specific personas to include |
| `personas.feedback_stages` | list | [refine, design, dev, uat] | stage names | When to run persona feedback |
| `personas.count` | integer | 5 | 3-7 | Number of personas to spawn |
| `personas.overlays` | list | [] | demographic overlay names | Demographic overlays |
| `personas.custom` | list | [] | persona profile objects | Custom persona definitions |

### Aliases

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `aliases.theme` | string | "business" | any built-in or custom theme | Character theme for agents |
| `aliases.custom_path` | string | ".delivery/aliases/" | directory path | Custom theme directory |

### Git & GitHub

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `git.branch_strategy` | string | "github-flow" | trunk-based, github-flow, gitflow, none | Branching strategy |
| `git.auto_branch` | boolean | true | true/false | Auto-create branches at Plan |
| `git.commit_convention` | string | "conventional" | conventional, none | Commit message convention |
| `git.clean_tree_check` | boolean | true | true/false | UAT validates clean tree |
| `github.create_issues` | boolean | false | true/false | Create issues from stories |
| `github.create_pr` | boolean | false | true/false | Create PR at UAT |
| `github.link_commits` | boolean | true | true/false | Link commits to issues |

### Monorepo

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `monorepo.enabled` | boolean | false | true/false | Monorepo mode |
| `monorepo.tool` | string | "none" | nx, turbo, lerna, pnpm, none | Monorepo tool |
| `monorepo.scope` | string | "root" | root, per-package | Pipeline scope |

### Notifications

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `notifications.channels` | list | ["console"] | console, file, slack, github-discussion | Notification channels |
| `notifications.events` | list | ["complete", "abort", "escalation"] | complete, abort, escalation, checkpoint, defect-threshold | Events to notify on |

### Presentation

| Key | Type | Default | Valid Values | Description |
|-----|------|---------|-------------|-------------|
| `presentation.default_format` | string | "structured-markdown" | structured-markdown, marp, paste-ready, pptx | Output format |
| `presentation.default_audience` | string | "technical" | technical, executive, investor, client-facing, casual | Audience mode |
| `presentation.speaker_notes` | boolean | false | true/false | Include speaker notes |
| `presentation.save_to_artifacts` | boolean | true | true/false | Save approved output to `.delivery/artifacts/presentations/` |
| `presentation.marp_theme` | string | "default" | default, gaia, uncover, custom path | Marp theme |
| `presentation.staleness_warning_days` | integer | 7 | 1-30 | Days before staleness warning on source artifacts |
| `presentation.vocabulary_overrides` | map | {} | term: replacement pairs | Custom jargon translations |
| `presentation.pptx_template` | string | "" | file path to .pptx template (empty = blank) | PPTX template for branding |
| `presentation.pptx_font` | string | "Calibri" | font family name | PPTX font override |
| `presentation.pptx_accent_color` | string | "#2d5aa0" | hex color string (#RRGGBB) | PPTX accent color override |
| `presentation.narrative.emphasis` | boolean | true | true/false | Enable emphasis selection editorial pass |
| `presentation.narrative.cutting` | boolean | true | true/false | Enable information cutting editorial pass |
| `presentation.narrative.framing` | boolean | true | true/false | Enable audience-specific framing editorial pass |
| `presentation.narrative.tension` | boolean | true | true/false | Enable narrative tension editorial pass |
| `presentation.light_mode` | string | "auto" | auto, always, never | Light mode activation strategy |
| `presentation.thresholds` | map | {} | type-name: seconds pairs (e.g., sprint-review: 120). 0 = unlimited. | Per-type threshold overrides |
| `presentation.thresholds_default` | integer | 90 | 0-600 (0 = unlimited) | Global threshold override (seconds) |

---

## Full Example Config

```yaml
config_version: "2.6"
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
  clean_code_guide: ""
  clean_code_enforcement: block
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
  scope: code-only
  scope_include: []
  scope_exclude: [".delivery/", ".git/", "node_modules/", "__pycache__/"]
  checkpoints: [refine, architect, plan, uat]
  collaboration_patterns:
    - evaluator-optimizer
    - adversarial
    - review-board
    - debate
    - consensus
    - decision-routing
  max_self_correction: 3
  max_dod_rounds: 3
  max_parallel_agents: 3
  parallel_stories: true
  parallel_validators: true
  verify_skill_loading: true
  delegation_retry_max: 2
  isolation_audit: warn
  metadata_max_chars: 200
  agent_timeout: 120
  required_agent_retry_max: 2
dod_validators:
  idea: [po, architect]
  refine: [po, architect, qa]
  design: [ux, po, qa, architect]
  architect: [architect, qa, devops, security]
  plan: [sm, po, qa, devops]
  development: [developer, qa, architect, tech-writer]
  uat: [qa, devops, po, tech-writer]
personas:
  categories: [web-users]
  selected: []
  feedback_stages: [refine, design, dev, uat]
  count: 5
  overlays: []
  custom: []
aliases:
  theme: business
  custom_path: .delivery/aliases/
notifications:
  channels: [console]
  events: [complete, abort, escalation]
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
presentation:
  default_format: structured-markdown
  default_audience: technical
  speaker_notes: false
  save_to_artifacts: true
  marp_theme: default
  staleness_warning_days: 7
  vocabulary_overrides: {}
  narrative:
    emphasis: true
    cutting: true
    framing: true
    tension: true
  light_mode: auto
  thresholds: {}
  thresholds_default: 90
  pptx_template: ""
  pptx_font: Calibri
  pptx_accent_color: "#2d5aa0"
wizard_completed: 2026-03-22
```

---

## Defaults by Project Type

Some defaults vary by project type:

| Key | GREENFIELD | FEATURE | BUG_FIX | GAME_DEV+ | SPIKE | DOCS_ONLY |
|-----|-----------|---------|---------|-----------|-------|-----------|
| `pipeline.checkpoints` | all 4 | [refine, uat] | [uat] | all 4 | [] | [uat] |
| `personas.categories` | [web-users] | [web-users] | [] | [gamers] | [] | [] |
| `pipeline.collaboration_patterns` | all 6 | all 6 | [evaluator-optimizer, decision-routing] | all 6 | [evaluator-optimizer] | [evaluator-optimizer] |
