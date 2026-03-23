# Nx Monorepo Patterns

Cross-language reference for Nx workspace management. Load when Nx workspace context is detected (nx.json exists, mentions of "nx", "monorepo", "workspace").

## CRITICAL RULE

**ALWAYS use Nx CLI generators to create projects and libraries. NEVER create project directories, package.json, tsconfig.json, or project structure manually.**

Bad:
```bash
mkdir libs/my-lib
cd libs/my-lib
npm init -y
# WRONG -- Nx doesn't know about this project
```

Good:
```bash
nx generate @nx/js:library my-lib
# Nx creates the project, registers it, sets up build/test/lint
```

This rule is non-negotiable. Manual project creation breaks the project graph, caching, affected commands, and dependency tracking.

## Nx Version Note

Commands target Nx 19+ (current as of 2025). Key differences from older versions:
- Project inference from package.json (no workspace.json)
- `nx.json` is the primary config file
- `project.json` per-project (optional with inference)
- `@nx/js`, `@nx/react`, `@nx/node` etc. replace `@nrwl/*` packages

## Project Creation Commands

### Libraries (shared code)

```bash
# JavaScript/TypeScript library
nx generate @nx/js:library shared-utils --directory=libs/shared-utils

# React component library
nx generate @nx/react:library ui-components --directory=libs/ui-components

# Node.js library
nx generate @nx/js:library api-models --directory=libs/api-models

# Nest.js library
nx generate @nx/nest:library auth --directory=libs/auth
```

### Applications

```bash
# React application
nx generate @nx/react:application web-app --directory=apps/web-app

# Next.js application
nx generate @nx/next:application marketing-site --directory=apps/marketing-site

# Angular application
nx generate @nx/angular:application admin-panel --directory=apps/admin-panel

# Node/Express API
nx generate @nx/node:application api --directory=apps/api

# Nest.js API
nx generate @nx/nest:application api-gateway --directory=apps/api-gateway
```

### Component and Module Generation Within Projects

```bash
# React component in a library
nx generate @nx/react:component Button --project=ui-components

# Nest controller
nx generate @nx/nest:controller users --project=api-gateway

# Angular service
nx generate @nx/angular:service auth --project=admin-panel
```

## Workspace Structure

Standard Nx monorepo layout:

```
my-workspace/
├── nx.json                 # Workspace config: caching, task runner, plugins
├── package.json            # Root dependencies
├── tsconfig.base.json      # Shared TypeScript config (path aliases)
├── apps/                   # Deployable applications
│   ├── web-app/
│   │   ├── project.json    # Project-specific config
│   │   ├── src/
│   │   └── tsconfig.json
│   └── api/
│       ├── project.json
│       └── src/
├── libs/                   # Shared libraries
│   ├── shared-utils/
│   │   ├── project.json
│   │   ├── src/
│   │   │   └── index.ts    # Public API (barrel export)
│   │   └── tsconfig.json
│   └── ui-components/
└── tools/                  # Custom generators, scripts
```

## Library Categories

Organize shared libraries by type:

| Category | Purpose | Naming | Example |
|----------|---------|--------|---------|
| **feature** | Smart components, pages, workflows | `feature-<name>` | `feature-auth`, `feature-dashboard` |
| **data-access** | API calls, state management, services | `data-access-<name>` | `data-access-users`, `data-access-products` |
| **ui** | Presentational components, design system | `ui-<name>` | `ui-buttons`, `ui-forms` |
| **util** | Pure utility functions, helpers | `util-<name>` | `util-formatting`, `util-validation` |
| **model** | Types, interfaces, DTOs | `model-<name>` | `model-user`, `model-api` |

## Tags and Module Boundaries

Enforce architectural boundaries with tags in project.json:

```json
// libs/feature-auth/project.json
{
  "tags": ["scope:auth", "type:feature"]
}
```

In `.eslintrc.json` (root):
```json
{
  "rules": {
    "@nx/enforce-module-boundaries": ["error", {
      "depConstraints": [
        { "sourceTag": "type:feature", "onlyDependOnLibsWithTags": ["type:data-access", "type:ui", "type:util", "type:model"] },
        { "sourceTag": "type:data-access", "onlyDependOnLibsWithTags": ["type:util", "type:model"] },
        { "sourceTag": "type:ui", "onlyDependOnLibsWithTags": ["type:util", "type:model"] },
        { "sourceTag": "type:util", "onlyDependOnLibsWithTags": ["type:model"] },
        { "sourceTag": "type:model", "onlyDependOnLibsWithTags": [] }
      ]
    }]
  }
}
```

Dependency flow: feature -> data-access/ui/util/model, data-access -> util/model, ui -> util/model, util -> model, model -> nothing. Apps can depend on any lib. Libs never depend on apps.

## Task Running

```bash
# Run single task
nx build web-app
nx test shared-utils
nx lint api

# Run affected (only what changed)
nx affected -t build
nx affected -t test
nx affected -t lint

# Run for all projects
nx run-many -t build
nx run-many -t test --parallel=5

# Visualize project graph
nx graph
```

## Caching

Nx caches task results by default (locally in `.nx/cache/`).

Configure cacheable tasks in `nx.json`:
```json
{
  "targetDefaults": {
    "build": { "cache": true, "dependsOn": ["^build"] },
    "test": { "cache": true },
    "lint": { "cache": true }
  }
}
```

For distributed caching: Nx Cloud (`nx connect`).

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Install
  run: npm ci
- name: Lint affected
  run: npx nx affected -t lint --base=origin/main
- name: Test affected
  run: npx nx affected -t test --base=origin/main
- name: Build affected
  run: npx nx affected -t build --base=origin/main
```

Key CI principles:
- Use `affected` to skip unchanged projects
- Set `--base` to the merge target branch
- Parallel execution with `--parallel`
- Cache across CI runs with Nx Cloud

## Importing Between Projects

```typescript
// In apps/web-app/src/app.tsx
import { Button } from '@my-workspace/ui-components';
import { formatDate } from '@my-workspace/util-formatting';

// NEVER do this:
import { something } from '../../apps/api/src/...';       // Never import from another app
import { something } from '../../../libs/ui/src/internal/...';  // Use barrel export only
```

Path aliases are defined in `tsconfig.base.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@my-workspace/ui-components": ["libs/ui-components/src/index.ts"],
      "@my-workspace/util-formatting": ["libs/util-formatting/src/index.ts"]
    }
  }
}
```

## Custom Generators

For project-specific patterns, create custom generators:

```bash
nx generate @nx/plugin:generator my-component --directory=tools/generators
```

Use custom generators instead of manual file creation for repeated patterns.

## Anti-Patterns

| Anti-Pattern | Why It Breaks Things | Do This Instead |
|-------------|----------------------|-----------------|
| Manual `mkdir` for projects | Breaks project graph, caching, affected | `nx generate` |
| `npm init` inside monorepo | Creates untracked project | `nx generate @nx/js:library` |
| Import between apps | Tight coupling, breaks boundaries | Extract to shared lib |
| One giant shared lib | Everything depends on it, cache invalidation | Split by domain/type |
| Circular dependencies | Build failures, design smell | Restructure with interface libs |
| Skipping `nx affected` in CI | Rebuilds everything every time | Always use `affected` |
| Hardcoded paths in imports | Breaks when projects move | Use tsconfig path aliases |
| Putting config outside project.json | Nx cannot track it | Use project.json targets |
