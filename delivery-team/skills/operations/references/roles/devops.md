# DevOps

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **DevOps** | ci-cd-patterns.md, deployment-strategies.md, infrastructure-patterns.md, observability.md |

## Detection Keywords

CI/CD, pipeline, deployment, infrastructure, monitoring, Docker, Kubernetes, terraform, container, helm, build, artifact, registry, environment, provisioning, scaling, alerting, observability, incident, on-call, capacity, load balancer

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "CI/CD", "pipeline", "build pipeline", "continuous integration", "continuous delivery" | **ci-cd-pipeline** | ci-cd-patterns.md |
| "deployment strategy", "blue-green", "canary", "rolling deployment", "zero-downtime" | **deployment-strategy** | deployment-strategies.md |
| "infrastructure", "terraform", "IaC", "provision", "cloud architecture", "Kubernetes cluster" | **infrastructure** | infrastructure-patterns.md |
| "monitoring", "observability", "alerting", "SLO", "SLI", "dashboard", "tracing" | **monitoring** | observability.md |
| "environment", "staging", "production", "dev environment", "environment parity" | **environment-management** | infrastructure-patterns.md, deployment-strategies.md |
| "incident", "postmortem", "on-call", "escalation", "outage", "SEV1" | **incident-ops** | observability.md |
| "capacity", "scaling", "load testing", "right-sizing", "cost optimization" | **capacity-planning** | infrastructure-patterns.md, observability.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **ci-cd-pipeline** | Design or improve CI/CD pipelines: stages, branching strategy, artifact management, caching, security scanning |
| **deployment-strategy** | Select and design deployment strategy with rollback plan, health checks, and zero-downtime requirements |
| **infrastructure** | Design infrastructure-as-code solutions: cloud resources, networking, container orchestration, state management |
| **monitoring** | Design observability stack: metrics, logs, traces, SLOs, alerting rules, dashboards, incident detection |
| **environment-management** | Design environment strategy: parity, promotion, isolation, configuration management |
| **incident-ops** | Create incident response procedures: classification, escalation, communication, postmortem templates |
| **capacity-planning** | Analyze and plan capacity: scaling strategies, cost optimization, load testing, resource right-sizing |

## Guardrails

- **Pipelines must be reproducible** -- same commit must produce same artifact; no implicit dependencies on build environment
- **Secrets never in code or logs** -- all sensitive values injected at runtime via vault or environment; mask in CI output
- **Infrastructure must be codified** -- no manual changes to production; all infrastructure changes through version-controlled IaC
- **Health checks are mandatory** -- every deployed service must have readiness and liveness probes
- **Rollback must be possible** -- every deployment must have a documented rollback path before proceeding
- **Monitoring before launch** -- no service goes live without alerting on golden signals (latency, traffic, errors, saturation)
- **Environment parity** -- dev/staging/prod must use the same deployment mechanism; only configuration differs
