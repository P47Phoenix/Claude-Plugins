# Release Planning

## Release Train Model

### Cadence-Based Releases

A release train departs on schedule regardless of which features are ready. Features that miss the train wait for the next one. This model prioritizes predictability over scope.

- The train schedule is fixed and communicated to all stakeholders at the start of the planning cycle
- Features are planned for a specific train but can be bumped to the next train without delaying the current release
- Each train has a designated release manager responsible for coordination and communication
- Release trains work best when combined with feature flags -- incomplete features can ride the train with their flag disabled

### Feature Cutoff

- Define a feature cutoff date relative to the release date (e.g., 5 business days before release)
- After cutoff, only bug fixes and approved exceptions merge to the release branch
- Exceptions require explicit approval from the release manager and a justification for the risk
- Late additions after cutoff carry higher scrutiny: additional testing, smaller scope, lower risk tolerance

### Hardening Period

- The period between feature cutoff and release is dedicated to stabilization
- Activities during hardening: regression testing, performance testing, documentation review, deployment dry-run
- No new features during hardening -- only bug fixes for issues found during stabilization
- Hardening period length scales with release size: 1-2 days for small releases, 1 week for large releases

---

## Release Cadence Patterns

| Cadence | Release Frequency | Best For | Trade-Offs |
|---------|-------------------|----------|------------|
| **Continuous** | Every merge to main | SaaS products, web apps, teams with strong CI/CD | Requires mature automation, feature flags, fast rollback. Maximum velocity but highest infrastructure investment. |
| **Weekly** | Once per week | Products needing regular updates with some coordination | Good balance of velocity and stability. Requires dedicated release process but not full-time release manager. |
| **Biweekly** | Every 2 weeks | Products aligned with sprint cadence | Aligns with Scrum sprints. Enough time for hardening. Can become a bottleneck if scope grows. |
| **Monthly** | Once per month | Products with compliance review requirements, enterprise software | More time for testing and documentation. Larger releases carry more risk. Change advisory boards fit naturally. |

### Choosing a Cadence

- Start with the fastest cadence the team can sustain reliably
- If releases are consistently delayed, the cadence is too aggressive -- slow down and stabilize
- If releases are consistently small and uneventful, the cadence may be too slow -- consider accelerating
- Different components can have different cadences (API weekly, mobile app monthly) if they are independently deployable

---

## Scope Management

### Scope Freeze

- Scope freeze occurs at feature cutoff -- no new features added to the release after this point
- Scope freeze is enforced by the release manager, not suggested
- Bug fixes found during hardening are in scope only if they meet severity criteria (SEV1/SEV2 for the release)
- Scope creep after freeze is tracked and reported in the release retrospective

### Change Request Process

- Changes after scope freeze require a formal change request: what, why, risk assessment, testing plan
- Change requests are approved by the release manager and at minimum one engineering lead
- Approved changes get additional testing proportional to their risk
- Rejected changes are documented with the rejection reason and the target release for inclusion

### Emergency Hotfixes

- Hotfixes bypass the normal release process but still follow a defined expedited process
- Hotfix criteria: production incident affecting users (SEV1 or SEV2) with no workaround
- Hotfix process: branch from production tag, fix, test (abbreviated but not skipped), deploy, merge fix back to main
- Every hotfix triggers a postmortem to identify how to prevent the need for future hotfixes

---

## Release Checklist Template

### Pre-Release (T-5 days to T-1 day)

- [ ] Feature cutoff enforced -- no new features merged after cutoff
- [ ] All release-targeted items are merged and in the release candidate
- [ ] Regression test suite passes
- [ ] Performance test results reviewed -- no degradation beyond threshold
- [ ] Security scan results reviewed -- no critical or high vulnerabilities
- [ ] Database migrations tested against production-like data
- [ ] Release notes drafted and reviewed
- [ ] Rollback procedure documented and reviewed
- [ ] Deployment to staging environment completed and verified
- [ ] Go/no-go meeting scheduled with stakeholders

### Release Day (T-0)

- [ ] Go/no-go decision made and documented
- [ ] Stakeholders notified of release start
- [ ] Deployment initiated (automated pipeline or manual trigger)
- [ ] Health checks verified post-deployment
- [ ] Smoke tests passed in production
- [ ] Monitoring dashboards reviewed -- no anomalies
- [ ] Release announcement sent to stakeholders
- [ ] Status page updated if applicable

### Post-Release (T+1 day to T+3 days)

- [ ] Monitor error rates and performance for 24-48 hours
- [ ] Collect user feedback and bug reports
- [ ] Triage post-release issues -- hotfix if SEV1/SEV2, otherwise next release
- [ ] Release retrospective conducted
- [ ] Metrics captured: deployment duration, rollback count, hotfix count, issues found post-release
- [ ] Retrospective action items assigned and tracked

---

## Stakeholder Communication Templates

### Release Announcement

```
Subject: [Product] Release [Version] -- [Date]

Release [Version] is now live in production.

Key changes:
- [Feature 1: one-sentence summary]
- [Feature 2: one-sentence summary]
- [Bug fix: one-sentence summary]

Breaking changes:
- [If any -- include migration guidance link]

Known issues:
- [If any -- include workaround]

Full release notes: [link]
Questions or issues: [contact channel]
```

### Delay Notification

```
Subject: [Product] Release [Version] delayed to [New Date]

Release [Version] originally scheduled for [Original Date] has been delayed to [New Date].

Reason: [Brief, honest explanation -- e.g., critical bug found during staging validation]

Impact: [What stakeholders need to know or do differently]

Updated timeline:
- [New Date]: Target release date
- [Date]: Go/no-go meeting

Questions: [contact channel]
```

### Hotfix Communication

```
Subject: [Product] Hotfix [Version] deployed -- [Date]

A hotfix has been deployed to address [brief description of issue].

Issue: [What users experienced]
Root cause: [Brief technical summary]
Fix: [What was changed]
Verification: [How we confirmed the fix]

Impact: [Who was affected and for how long]

Postmortem will be shared within [timeframe].
```

---

## Change Advisory Board Process

### When a CAB Is Needed

- Regulated industries (healthcare, finance) where changes require formal approval
- Changes affecting shared infrastructure used by multiple teams
- Changes with broad blast radius (database migrations, authentication system changes)
- Organization-mandated governance for production changes

### CAB Composition

- Release manager (facilitator)
- Engineering lead (technical risk assessment)
- QA lead (test coverage assessment)
- Operations/SRE (infrastructure and monitoring readiness)
- Product owner (business impact assessment)
- Security representative (for security-relevant changes)

### Decision Criteria

- Risk assessment: what is the worst case if this change fails?
- Test coverage: what percentage of affected functionality is covered by automated tests?
- Rollback plan: is rollback tested and does the team have confidence in it?
- Monitoring: are alerts and dashboards in place to detect problems?
- Communication: are affected stakeholders informed?

---

## Release Retrospective

### What to Review

- **Timeline adherence** -- Did the release ship on the planned date? If not, what caused the delay?
- **Quality** -- How many bugs were found post-release? What severity? Were any hotfixes needed?
- **Process** -- Did the release process work smoothly? Where were the friction points?
- **Communication** -- Were stakeholders informed at the right times? Was any communication missing?
- **Tooling** -- Did the CI/CD pipeline, monitoring, and deployment tools work as expected?

### Metrics to Track Per Release

| Metric | Target | Actual |
|--------|--------|--------|
| Deployment duration | [target] | [actual] |
| Rollback count | 0 | [actual] |
| Hotfix count (within 48 hours) | 0 | [actual] |
| Post-release bugs (SEV1/SEV2) | 0 | [actual] |
| Release delay (days) | 0 | [actual] |

### Action Items

- Every retrospective produces concrete, assigned action items with due dates
- Action items focus on systemic improvements, not individual performance
- Review previous retrospective action items for completion before generating new ones
- Track action item completion rate -- unfinished items indicate process problems
