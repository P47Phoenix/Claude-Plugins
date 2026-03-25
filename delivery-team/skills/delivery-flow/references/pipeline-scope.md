# Pipeline Scope Configuration

## Scope Modes

### code-only (default)

Pipeline enforcement triggers only on source code files. Documentation, config, and infrastructure changes pass through without pipeline governance.

**File extensions monitored**: .py, .ts, .js, .go, .rs, .cs, .java, .gd, .scala, .hs, .ex, .fs, .tsx, .jsx, .vue, .svelte, .sh, .rb, .kt, .swift

**Best for**: Fast iteration, minimal ceremony, teams that only need code review governance.

### all

Pipeline enforcement triggers on ALL file changes except explicitly excluded paths. Docs, config, infra, data, and project management files all go through the pipeline.

**Excluded by default**: .delivery/, .git/, node_modules/, __pycache__/, *.lock files

**Best for**: Compliance-required projects, plugin repos (where docs ARE the product), regulated environments.

**Stage depth by content type** (when scope=all):
- Source code changes -- full pipeline depth
- Documentation changes -- light pipeline (Idea, Plan, Dev, UAT; skip Design + Architect)
- Config/infra changes -- light pipeline with Architect review (infra changes need architecture approval)
- Data/migration changes -- full pipeline with Data Architect involvement

### custom

Pipeline enforcement triggers only on files matching user-defined glob patterns.

**Example**: Only govern .py and .md files:
```yaml
pipeline:
  scope: custom
  scope_include: ["*.py", "*.md", "*.yml"]
```

**Best for**: Selective governance -- e.g., code + docs but not config.

## Always Excluded

These paths are NEVER governed regardless of scope:
- `.delivery/` -- pipeline's own state
- `.git/` -- version control
- `node_modules/`, `__pycache__/`, `target/`, `bin/`, `obj/` -- build artifacts
- `*.lock` files -- dependency locks

## Configuration

```yaml
pipeline:
  scope: code-only          # code-only | all | custom
  scope_include: []          # glob patterns (only used when scope=custom)
  scope_exclude:             # always excluded from enforcement
    - ".delivery/"
    - ".git/"
    - "node_modules/"
    - "__pycache__/"
```

## Interaction with Other Settings

- `enforcement.source_code_hook`: When false, the PreToolUse hook is not installed at all, regardless of scope.
- `pipeline.checkpoints`: Scope determines WHICH files trigger the pipeline; checkpoints determine WHERE human review happens within it.
- `timeline.risk_tolerance`: When set to "regulated" or "mission-critical", consider using scope=all to ensure full governance coverage.
- `compliance.frameworks`: If any compliance framework is active, scope=all is recommended but not enforced.

## Migration from Pre-1.9 Configs

Configs without `pipeline.scope` default to "code-only", which preserves the pre-1.9 behavior exactly. No action required for existing projects. To opt in to broader governance, set scope to "all" or "custom" in `.delivery/config.yml`.
