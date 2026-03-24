# Multi-Project / Monorepo Orchestration

## Purpose

Enable the delivery pipeline to operate correctly in monorepo environments where multiple packages, applications, or services share a single repository. Detect the monorepo tool, scope pipeline runs to affected packages, and manage shared vs. per-package architecture decisions.

---

## Detection

On pipeline initialization (or during setup wizard), scan for monorepo configuration files:

| File | Tool | Detection Confidence |
|------|------|---------------------|
| `nx.json` | Nx | High |
| `turbo.json` | Turborepo | High |
| `lerna.json` | Lerna | High |
| `pnpm-workspace.yaml` | pnpm workspaces | High |
| `package.json` with `workspaces` field | Yarn/npm workspaces | Medium |
| Multiple `go.mod` files | Go multi-module | Medium |
| `Cargo.toml` with `[workspace]` | Rust workspace | High |

### Auto-Detection Protocol

1. Scan the repository root for the files above
2. If found, set `monorepo.enabled: true` and `monorepo.tool` to the detected tool
3. If multiple tool configs are found (e.g., `nx.json` + `pnpm-workspace.yaml`), prefer the build orchestrator (Nx > Turbo > Lerna > pnpm)
4. If no monorepo config is found, set `monorepo.enabled: false` and skip all monorepo logic

---

## Configuration

Three config keys control monorepo behavior (see config-schema.md):

```yaml
monorepo:
  enabled: true          # Auto-detected; can be overridden
  tool: nx               # nx, turbo, lerna, pnpm, none
  scope: root            # root = single .delivery/ at repo root
                         # per-package = each package has its own .delivery/
```

### Scope Modes

| Mode | `.delivery/` Location | Config | Artifacts | Memory |
|------|----------------------|--------|-----------|--------|
| **root** | Repo root only | Shared across all packages | Shared, tagged by package | Shared |
| **per-package** | Each package directory | Per-package config | Per-package artifacts | Per-package with shared root memory |

**Default: root.** Use `per-package` when packages have fundamentally different tech stacks, team ownership, or delivery cadences.

---

## Pipeline Routing

When monorepo is detected, the pipeline asks which package(s) to target before starting:

```
Monorepo detected (Nx workspace with 5 packages).

Which package(s) should this pipeline run target?
1. All packages
2. Affected packages only (based on git changes)
3. Specific package(s): [list]
4. Root-level only (shared config, ADRs, CI)
```

### Affected-Only Pipeline

Run the pipeline only for packages with changes since the last pipeline run or since the base branch diverged.

| Tool | Affected Detection Command |
|------|---------------------------|
| Nx | `npx nx affected --base=main --head=HEAD` |
| Turborepo | `npx turbo run build --filter=...[main...HEAD]` (list affected) |
| Lerna | `npx lerna changed` |
| pnpm | `pnpm -r --filter "...[main]" exec echo` |
| Git (fallback) | `git diff --name-only main...HEAD` and map files to packages |

When using affected-only mode:
1. Determine which packages have changes
2. Include packages that depend on changed packages (transitive dependents)
3. Run the pipeline stages only for the affected set
4. Tag all artifacts with the package name: `.delivery/artifacts/05-plan-[package-name].md`

---

## Cross-Package Dependencies

Track dependencies between packages in the monorepo. These are distinct from story dependencies (see product-delivery dependency-tracking.md) — these are structural, code-level dependencies.

### Detection

- **Nx**: Read `project.json` dependency graph or `nx graph --file=output.json`
- **Turborepo**: Read `turbo.json` pipeline dependencies
- **Lerna**: Read `package.json` dependencies across packages
- **pnpm**: Read `pnpm-workspace.yaml` + package `dependencies`

### Shared Package Warnings

When a changed file belongs to a shared/library package that other packages depend on:

```
[CROSS-PACKAGE WARNING] Changes detected in shared package "ui-components"
The following packages depend on ui-components:
  - web-app (direct)
  - admin-dashboard (direct)
  - mobile-web (transitive via web-app)

Consider running affected-only pipeline to validate dependents.
```

---

## Shared Architecture Decisions

ADRs (Architecture Decision Records) follow a two-level hierarchy in monorepos:

### Root-Level ADRs

Stored in `.delivery/artifacts/` at the repo root. Apply to all packages unless overridden.

Examples:
- Authentication strategy (shared across all services)
- API versioning convention
- Logging and observability standards
- Database migration strategy

### Package-Level ADRs

Stored in `[package]/.delivery/artifacts/` (per-package scope) or tagged with the package name (root scope). Override root ADRs for that package only.

Examples:
- Package-specific framework choice (React for web-app, Vue for admin)
- Package-specific data model decisions
- Package-specific deployment configuration

### Override Rules

1. Package-level ADR explicitly referencing a root ADR supersedes it for that package
2. If no package-level override exists, the root ADR applies
3. Conflicts between root and package ADRs are flagged at the Architect stage:
   ```
   [ADR CONFLICT] Package "admin-dashboard" ADR-005 conflicts with root ADR-002
   Root ADR-002: "Use REST for all inter-service communication"
   Package ADR-005: "Use GraphQL for admin API"
   Resolution needed: Is this an intentional override or an inconsistency?
   ```

---

## Stage-Specific Behavior

### Idea / Refine / Design (Stages 1-3)

- Ask which package(s) the feature targets
- Load package-specific context (tech stack, existing architecture)
- If the feature spans packages, note cross-package coordination needs

### Architect (Stage 4)

- Load both root and package-level ADRs
- Validate new decisions against existing root ADRs
- Flag cross-package impacts: "This decision in package A affects package B because..."

### Plan (Stage 5)

- Map stories to packages
- Identify cross-package stories (stories that touch multiple packages)
- Sequence cross-package stories to minimize integration risk

### Development (Stage 6)

- Scope code changes to the target package(s)
- After writing code, check: did changes touch a shared package? If so, warn about dependents
- Run package-specific linting/build validation if configured

### UAT (Stage 7)

- Run validation for affected packages
- If cross-package changes were made, validate integration points
- Include package scope in UAT summary

---

## Anti-Patterns

| Anti-Pattern | Problem | Alternative |
|-------------|---------|-------------|
| Running full pipeline for every package on every change | Wastes time; most changes affect 1-2 packages | Use affected-only mode |
| Single `.delivery/config.md` for packages with different tech stacks | Config becomes contradictory | Use per-package scope |
| Ignoring cross-package dependencies | Changes to shared packages break dependents silently | Always check transitive dependents |
| Per-package configs that duplicate root settings | Config drift; updates missed | Use root for shared settings, per-package only for overrides |
| Skipping affected detection and always running "all" | Defeats the purpose of monorepo-aware pipeline | Default to affected-only; use "all" only for release validation |
