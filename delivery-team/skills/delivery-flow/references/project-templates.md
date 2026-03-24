# Template Library for Common Project Types

Pre-built starting-point artifacts for common technology stacks. Templates save 2-3 pipeline stages by providing pre-filled artifacts that the user confirms or modifies rather than starting from scratch.

---

## Template Format

Each template provides a set of pre-filled artifacts:

| Artifact | Contents |
|----------|----------|
| Idea Brief | Problem statement, target users, success criteria |
| PRD Outline | Functional requirements skeleton, NFRs, out-of-scope |
| Architecture Pattern | Recommended style, component diagram outline, key decisions |
| Tech Stack | Languages, frameworks, databases, infrastructure |
| Common User Stories | 5-10 starter stories covering the most typical features |
| Suggested DoD Validators | Role assignments tuned to the stack |

Templates are starting points, not prescriptions. Every template artifact must be reviewed and confirmed by the user before the pipeline treats it as a stage output.

---

## Available Templates

### `nextjs-api`

**Stack:** Next.js (App Router) + REST/GraphQL API backend
**Architecture:** Layered with API routes or separate backend service
**Tech:** TypeScript, React, Next.js, Prisma/Drizzle, PostgreSQL
**Common Stories:** Auth flow, CRUD for primary entity, API integration, responsive layout, error handling
**NFRs:** < 200ms API response, Core Web Vitals targets, SSR/SSG strategy
**DoD Validators:** developer, qa, architect, tech-writer

### `python-cli`

**Stack:** Python CLI tool with Click or Typer
**Architecture:** Command pattern with dependency injection
**Tech:** Python 3.11+, Click/Typer, Rich (terminal UI), pytest
**Common Stories:** Core command implementation, help text, config file support, error handling, output formatting
**NFRs:** < 500ms startup time, cross-platform compatibility, pip-installable
**DoD Validators:** developer, qa

### `godot-game`

**Stack:** Godot 4.x game project
**Architecture:** Scene-tree composition with signal-based communication
**Tech:** GDScript (primary), C# (optional), Godot 4.x
**Common Stories:** Player controller, main menu, level loading, save/load system, input mapping
**NFRs:** 60 FPS target, input latency < 16ms, asset loading strategy
**DoD Validators:** developer, qa, architect

### `dotnet-microservice`

**Stack:** .NET microservice with clean architecture
**Architecture:** Clean/Hexagonal architecture with CQRS
**Tech:** C# .NET 8+, MediatR, Entity Framework Core, Docker, xUnit
**Common Stories:** Health endpoint, CRUD operations, domain event publishing, API versioning, Dockerfile
**NFRs:** < 100ms p99 response, container startup < 5s, structured logging
**DoD Validators:** developer, qa, architect, devops

### `react-spa`

**Stack:** React single-page application
**Architecture:** Feature-based folder structure with state management
**Tech:** TypeScript, React 18+, Vite, React Router, Zustand/Redux Toolkit, Vitest
**Common Stories:** Auth flow, routing setup, API client, form handling, responsive layout
**NFRs:** Bundle size < 200KB gzipped, LCP < 2.5s, accessibility (WCAG 2.1 AA)
**DoD Validators:** developer, qa, ui

### `express-api`

**Stack:** Node.js Express REST API
**Architecture:** Layered (routes, controllers, services, repositories)
**Tech:** TypeScript, Express, Prisma/TypeORM, PostgreSQL, Jest, Docker
**Common Stories:** Auth middleware, CRUD endpoints, validation, error handling, health check
**NFRs:** < 100ms p99 response, rate limiting, structured logging
**DoD Validators:** developer, qa, architect

### `fullstack-nx`

**Stack:** Nx monorepo with React frontend + Node backend
**Architecture:** Monorepo with shared libraries, feature-based structure
**Tech:** TypeScript, React, Express/NestJS, Nx, shared types library
**Common Stories:** Workspace setup, shared types, API client generation, CI pipeline, dev proxy
**NFRs:** Incremental builds, affected-only CI, shared lint/test config
**DoD Validators:** developer, qa, architect, devops

---

## Usage Protocol

### At Idea Stage

When the pipeline enters Stage 1 (Idea), after project type detection:

1. Check if a template matches the detected project type and tech stack
2. If a match is found, offer: `> Template available: [template name]. Start from this template? (Yes / No / Customize)`
3. **Yes**: Load all pre-filled artifacts. Present each to the user for confirmation before marking the stage complete.
4. **No**: Proceed with normal Idea stage (blank slate).
5. **Customize**: Load the template, then walk through each artifact asking what to keep, modify, or remove.

### Template Artifact Flow

Template artifacts feed into the pipeline as if they were produced by the normal stage flow:

- Idea Brief from template feeds into Refine stage
- PRD Outline feeds into Design stage
- Architecture Pattern feeds into Architect stage
- All template artifacts are subject to the same DoD validation as normally-produced artifacts

### Skipping Stages

If a template provides a sufficiently complete artifact for a stage, the pipeline may offer to skip that stage:

```
> Template provides a complete PRD outline for [template]. Skip Refine stage? (Yes / No)
```

Skipped stages are recorded in `state.md` with reason: `template-provided`.

---

## Custom Templates

Users can create custom templates in `.delivery/templates/`:

```
.delivery/templates/
  my-template/
    idea-brief.md
    prd-outline.md
    architecture.md
    stories.md
    config.yaml       # Template metadata: name, description, stack, NFRs
```

Custom templates take precedence over built-in templates when names match. The `config.yaml` in a custom template directory defines the template metadata:

```yaml
name: my-template
description: Custom template for internal microservices
stack:
  languages: [Go]
  frameworks: [Chi, Wire]
  databases: [CockroachDB]
nfrs:
  - "p99 latency < 50ms"
  - "Zero-downtime deployments"
dod_validators: [developer, qa, architect, devops, security]
```
