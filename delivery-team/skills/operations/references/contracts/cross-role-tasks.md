# Cross-Role Tasks (operations plugin)

When a task spans multiple roles, load all relevant reference files into a single sub-agent:

1. Identify all roles involved
2. Load all relevant reference files (godot pattern -- multiple references in one sub-agent)
3. Spawn a **single sub-agent** with combined references
4. If concerns are truly independent, spawn separate sub-agents sequentially

## Common cross-role combinations

| Scenario | Roles | References Loaded |
|----------|-------|-------------------|
| Release notes for a deployment | Technical Writer + Release Manager | documentation-standards.md + release-planning.md |
| Incident runbook with alerting setup | DevOps + Technical Writer | observability.md + runbook-templates.md |
| Feature flag rollout with docs | Release Manager + Technical Writer | feature-flag-patterns.md + user-guides.md |
| Deployment with rollback plan | DevOps + Release Manager | deployment-strategies.md + rollback-strategies.md |
| API deployment with documentation | DevOps + Technical Writer | deployment-strategies.md + api-documentation.md |
| Full release cycle | All three roles | release-planning.md + deployment-strategies.md + documentation-standards.md |
| Versioned API with migration guide | Release Manager + Technical Writer | versioning-patterns.md + api-documentation.md |
