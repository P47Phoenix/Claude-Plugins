# Claude Plugins

A collection of plugins for [Claude Code](https://code.claude.com) that extend Claude's capabilities with specialized skills, delivery workflows, and development tools.

## What is this?

Claude Plugins is an open-source marketplace of installable plugins for Claude Code. Each plugin adds specialized capabilities — from a full delivery team that orchestrates software projects end-to-end, to research agents, prompt engineering tools, and multi-agent workflow builders. Install one plugin or the whole set. Everything runs locally in your Claude Code session with no external services required.

## Installation

```
claude mcp add-skill https://github.com/P47Phoenix/Claude-Plugins
```

Or add to your project's `.claude/settings.json`:

```json
{
  "plugins": [
    "https://github.com/P47Phoenix/Claude-Plugins"
  ]
}
```

Then install individual plugins:

```
/plugin install delivery-team
/plugin install agentic-flow-builder
/plugin install prompt-engineer
/plugin install research-agent
```

Or browse interactively:
```
/plugin
```

## Plugins

### Delivery Team

A full software delivery team with 10 specialized skills covering the complete delivery lifecycle — from idea to release. Designed for both standalone use and multi-agent orchestration.

**10 Skills:**

| Skill | Roles | What It Does |
|-------|-------|-------------|
| **Delivery Flow** | Pipeline orchestrator | 7-stage pipeline (Idea → Refine → Design → Architect → Plan → Dev → UAT) with auto-detect project type, team DoD, self-correction, adversarial review, debate, consensus, and self-learning memory |
| **Product Delivery** | Product Owner, Scrum Bag, Data Analyst | User stories, PRDs, backlogs, sprint plans, retrospectives, metrics, A/B testing |
| **Developer** | 14 languages + OOP + FP + Frontend + Nx | Code implementation with language context isolation (Python, TypeScript, JavaScript, Go, Rust, C#, Java, SQL, Bash, R, F#, Elixir, Haskell, Scala) |
| **Godot** | GDScript, C#, Scenes, Signals | Godot 4.x game dev with headless validation and defect prevention |
| **Architect** | 11 roles | Solution, Enterprise, Data, Security, Compliance, Privacy, Incident Response + Game Systems, Level/World, Network/Multiplayer, Graphics/Rendering |
| **Quality** | QA Engineer | Test strategy, test cases, automation, quality metrics, empirical validation registry |
| **Operations** | DevOps, Release Manager, Technical Writer | CI/CD, deployment, infrastructure, release planning, versioning, API docs, runbooks |
| **UI** | UX Designer, UI Designer, Game UI Designer | User flows, wireframes, design systems, accessibility, HUD, game menus, inventory UI |
| **User Feedback** | 20+ simulated personas | Persona-based testing across gamers, web users, enterprise, and demographics with consensus detection |
| **Alias Creator** | 13 built-in themes | Create and manage agent personality themes (LOTR, Marvel, Star Wars, etc.) |

**Key Features:**
- **Setup wizard**: 10-question config wizard with auto-detection from codebase
- **Team DoD**: Every artifact validated by multiple roles before advancing
- **6 collaboration patterns**: Evaluator-optimizer, adversarial review, review board, decision ownership routing, debate, consensus
- **Self-learning memory**: Tiered chunked retrieval in `.delivery/memory/`
- **Defect tracking**: Self-improvement feedback loop that opens PRs to the plugin repo
- **Pipeline enforcement**: 3-layer system prevents bypassing quality gates
- **Empirical validation**: Detects runtime-only acceptance criteria (CODE_COMPLETE status)
- **Feature Knowledge System**: Impact analysis across features with dependency tracking
- **Session keepalive**: Cross-platform companion for long-running tasks
- **Pipeline state persistence**: Save and resume pipeline state across sessions
- **13 alias themes**: Personality injection with built-in themes (LOTR, Marvel, Star Wars, and more)
- **Config-driven architecture**: 4 decomposition strategies with YAML-based configuration
- **Git/GitHub integration**: Branching, commits, issues, and PR workflows built in

### Agentic Flow Builder

Build dynamic multi-agent workflows using ReAcTree hierarchical decomposition.

- Business Rules Engine (BRE) for deterministic gate decisions
- Dynamic agent assignment with hot-reload
- Dual memory system (episodic + working)
- 5 workflow patterns with SQLite audit trails

### Prompt Engineer

Expert prompt optimization for LLMs and AI systems.

- Comprehensive prompt engineering techniques
- Model-specific optimization
- Always shows complete prompt text

### PRD Quality Gate Flow

Production-grade PRD workflow with 7 quality gates.

- Business rules engine for deterministic decisions
- Episodic memory and complete audit trails
- Evidence-based Stage-Gate process

### Research Agent

Production-grade research agent with 5 research types.

- Academic frameworks (PICO, SPICE, PECO, GRADE, ReAct)
- Systematic review protocol
- Root cause analysis (5 Whys + Fishbone)

## Repository Structure

```
.
├── .claude-plugin/
│   └── marketplace.json              # Plugin registry
├── .github/
│   ├── ISSUE_TEMPLATE/               # Bug, feature, defect pattern templates
│   ├── PULL_REQUEST_TEMPLATE/        # Enhancement, bug fix templates
│   └── pull_request_template.md      # Default PR template
├── delivery-team/                    # Full delivery team plugin
│   ├── hooks/                        # Pipeline enforcement + validation hooks
│   │   ├── hooks.json
│   │   ├── check_config.py
│   │   ├── validate_gdscript.py
│   │   ├── verify_skill_load.py
│   │   ├── audit_agent_prompt.py
│   │   ├── flag_empirical_validation.py
│   │   ├── enforce_pipeline_scope.py
│   │   └── lib/
│   │       └── hook_utils.py
│   ├── scripts/                      # Utility scripts
│   │   ├── validate-config.py
│   │   ├── generate-schema.py
│   │   └── session_keepalive.py
│   ├── skills/
│   │   ├── delivery-flow/            # Pipeline orchestrator (18+ references)
│   │   ├── product-delivery/         # PO + SM + Data Analyst (15 references)
│   │   ├── developer/                # 14 languages + OOP + FP + Frontend + Nx (21 references)
│   │   ├── godot/                    # Godot 4.x (6 references)
│   │   ├── architect/                # 11 roles (22 references)
│   │   ├── quality/                  # QA (8 references)
│   │   ├── operations/               # DevOps + Release + TechWriter (12 references)
│   │   ├── ui/                       # UX + UI + Game UI (12 references)
│   │   ├── user-feedback/            # Persona testing (4 references)
│   │   └── alias-creator/            # 13 personality themes
│   └── LICENSE.txt
├── agentic-flow-builder/             # Multi-agent workflow plugin
├── prompt-engineer/                  # Prompt optimization plugin
├── prd-quality-gate-flow/            # PRD quality gate plugin
├── research-agent/                   # Research agent plugin
├── CLAUDE.md                         # Claude Code project instructions
└── README.md                         # This file
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines on plugin structure, development workflow, code standards, and the PR process.

**Issue templates** are available for bug reports, feature requests, and defect patterns.

**PR templates** include enhancement and bug fix formats, with a defect data section for `[DEFECT-FIX]` PRs from the delivery team's self-improvement loop.

## License

See individual plugin directories for license information.
