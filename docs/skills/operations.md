# Operations

**Invocation**: `delivery-team:operations`

Operations agent with three roles covering the full deployment and documentation lifecycle.

## Roles

### DevOps Engineer

CI/CD pipelines, deployment strategies, infrastructure, monitoring, and observability.

**Task signals**: "CI/CD", "pipeline", "deployment", "Docker", "Kubernetes", "terraform", "monitoring", "alerting"

### Release Manager

Release planning, versioning, rollback strategies, and feature flags.

**Task signals**: "release plan", "versioning", "rollback", "feature flag", "go/no-go", "SemVer", "hotfix"

### Technical Writer

API documentation, user guides, runbooks, and documentation standards.

**Task signals**: "API docs", "user guide", "runbook", "release notes", "tutorial", "changelog", "OpenAPI"

## Reference Files

| Role | References |
|------|-----------|
| DevOps | ci-cd-patterns.md, deployment-strategies.md, infrastructure-patterns.md, observability.md |
| Release Manager | release-planning.md, versioning-patterns.md, rollback-strategies.md, feature-flag-patterns.md |
| Technical Writer | api-documentation.md, user-guides.md, runbook-templates.md, documentation-standards.md |

## Example Usage

```
User: "Design a CI/CD pipeline for our Python API"

Role: DevOps | Task: ci-cd-design
References: ci-cd-patterns.md, deployment-strategies.md

Output: Pipeline design with stages, artifact management,
        environment promotion, and rollback strategy
```
