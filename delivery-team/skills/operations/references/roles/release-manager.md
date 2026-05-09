# Release Manager

## Role -> Reference Mapping

| Role | Reference Files |
|------|----------------|
| **Release Manager** | release-planning.md, versioning-patterns.md, rollback-strategies.md, feature-flag-patterns.md |

## Detection Keywords

release plan, versioning, rollback, feature flag, go/no-go, release train, hotfix, change advisory, scope freeze, release cadence, release checklist, SemVer, CalVer, breaking change, deprecation, sunset, release retrospective

## Task Type Routing Table

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "release plan", "release train", "release schedule", "release cadence" | **release-plan** | release-planning.md |
| "versioning", "SemVer", "CalVer", "version strategy", "API version" | **versioning-strategy** | versioning-patterns.md |
| "rollback", "revert", "roll back", "undo deployment" | **rollback-procedure** | rollback-strategies.md, deployment-strategies.md |
| "feature flag", "feature toggle", "kill switch", "dark launch", "flag cleanup" | **feature-flags** | feature-flag-patterns.md |
| "go/no-go", "release readiness", "change advisory", "release approval" | **go-no-go** | release-planning.md, rollback-strategies.md |
| "release communication", "release announcement", "stakeholder update" | **release-communication** | release-planning.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **release-plan** | Create release plans: cadence, scope management, checklists, stakeholder communication, retrospectives |
| **versioning-strategy** | Define versioning approach: scheme selection, pre-release conventions, breaking change management |
| **rollback-procedure** | Design rollback procedures: triggers, automation, data considerations, communication, post-rollback RCA |
| **feature-flags** | Design feature flag strategy: flag types, lifecycle, targeting rules, cleanup process, testing approach |
| **go-no-go** | Create go/no-go decision framework: criteria checklist, risk assessment, stakeholder sign-off process |
| **release-communication** | Draft release communications: announcements, delay notifications, hotfix updates, stakeholder templates |

## Guardrails

- **Every release has a rollback plan** -- no release proceeds without a documented, tested rollback procedure
- **Breaking changes require migration guides** -- breaking changes without user-facing migration documentation are blocked
- **Feature flags have expiration dates** -- every flag must have a planned removal date; stale flags are technical debt
- **Go/no-go criteria are defined before release** -- criteria must be established at planning time, not at release time
- **Hotfix process is pre-defined** -- emergency releases follow a documented expedited process, not ad-hoc decisions
- **Communication is proactive** -- stakeholders are notified of release status changes before they ask
- **Version numbers follow the declared scheme** -- no ad-hoc versioning; the project's versioning contract is enforced
