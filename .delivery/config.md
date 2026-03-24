---
config_version: "1.3"
project_type: FEATURE
tech_stack:
  languages: [Python, Markdown, Shell, TypeScript, JavaScript]
  frameworks: []
  databases: []
  ci_cd: none
  paradigm: hybrid
  paradigm_by_language:
    python: hybrid
    typescript: hybrid
    javascript: hybrid
  nx_workspace: false
team:
  size: 4
  composition: [plugin-dev, skill-dev, qa, devops]
deployment:
  environment: cloud-aws
  containerized: false
timeline:
  risk_tolerance: standard
  deadline: null
compliance:
  frameworks: []
architecture:
  style: auto
  style_overrides: {}
  decomposition: volatility
  decision_matrix_inputs:
    team_size: 4
    deploy_independence: low
    domain_complexity: medium
    change_rate: high
pipeline:
  checkpoints: [refine, uat]
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
  categories: [web-users, enterprise, gamers, demographics]
  selected: []
  feedback_stages: [refine, design, dev, uat]
  count: 5
  overlays: []
  custom: []
aliases:
  theme: lotr
  custom_path: .delivery/aliases/
enforcement:
  source_code_hook: true
  retro_frequency: every-run
  retro_skip_allowed: false
wizard_completed: 2026-03-24
---

# Delivery Configuration

## Project Context
Claude Code plugin repository (Claude-Plugins). Contains 5 plugins with the delivery-team being the primary plugin (9 skills, 4 hooks). This is an ongoing feature-development project — most work is adding/improving skills, references, hooks, and pipeline features.

## Tech Stack Details
- Python 3.10+: scripts for agentic-flow-builder and prd-quality-gate-flow
- Markdown: all SKILL.md files and reference documents (primary content format)
- Shell (Bash 5+): hook scripts (flag-empirical-validation.sh, validate-gdscript.sh, check-config.sh)
- TypeScript/JavaScript: planned for future Nx plugin and frontend skill examples

## Constraints & Decisions
- No external dependencies or package managers — scripts run directly
- No CI/CD configured — manual deployment via git push
- Volatility-based decomposition preferred — skills/references change independently at different rates
- Strict enforcement: retrospectives mandatory after every run, no skip allowed
- 2 human checkpoints: after Refine (PRD approval) and at UAT (accept/reject)
- All 4 persona categories enabled for diverse user feedback

## Notes
- Plugin follows three-level context loading: metadata → SKILL.md → references
- Config schema versioned (currently v1.3) with migration protocol
- Always use plugin-dev skills when modifying plugin components (hook-development, skill-development, etc.)
