# Rollback Strategies

## Immediate Rollback

### Redeploy Previous Version

The fastest rollback: deploy the last known-good version using the same deployment mechanism used for the original deploy.

- The previous version's artifact (container image, binary, package) must still be available in the artifact registry
- Use the exact same artifact that was previously running -- do not rebuild from source
- Trigger rollback via the CI/CD pipeline or a dedicated rollback command -- never manual SSH and restart
- Verify the rollback by checking the version endpoint, health checks, and error rates

### Traffic Switch

For blue-green deployments, rollback is a traffic switch back to the previous environment.

- Switch load balancer or service mesh routing to the previous environment
- Rollback time is the time to switch traffic -- typically seconds
- The previous environment must still be running and healthy (do not tear it down immediately after deployment)
- Keep the previous environment available for a defined soak period after every deployment (minimum 4 hours, recommended 24 hours)

### Rollback Decision Criteria

- Error rate increased by more than a defined threshold (e.g., 2x baseline) and sustained for more than 5 minutes
- p99 latency exceeded SLO target and sustained for more than 10 minutes
- Health check failures across multiple instances
- Customer-reported issues confirmed by monitoring data
- Data integrity issues detected (even one confirmed case warrants immediate rollback)

---

## Gradual Rollback

### Reduce Canary Percentage

When a canary deployment shows problems, roll back by reducing canary traffic to zero.

- Reduce canary traffic percentage to 0% -- do not terminate canary instances immediately
- Wait for in-flight requests on canary instances to complete (connection draining)
- Verify that traffic is fully served by the stable version
- Investigate the canary failure before retrying the deployment

### Drain Connections

- Configure connection drain timeout (30-60 seconds is typical)
- During draining, the instance accepts no new connections but completes existing requests
- After drain timeout, forcefully close remaining connections
- Monitor for dropped requests during the drain period -- alert if the drop rate is non-zero

### Staged Rollback

For rolling deployments partially completed:

1. Halt the rolling update -- stop deploying to additional instances
2. Roll back already-updated instances to the previous version
3. Verify that all instances are running the previous version
4. Confirm error rates return to baseline

---

## Data Rollback Considerations

### Backward-Compatible Migrations

- Schema changes made during the deployment must be compatible with both the new and old application versions
- If the new version added a column, the old version must tolerate that column existing (it does not read or write to it)
- If the new version changed data formats, the old version must handle both old and new formats
- Design migrations using the expand-and-contract pattern to maintain backward compatibility

### Dual-Write Pattern

When migrating data from one schema to another:

1. New version writes to both old and new locations
2. Read from old location (source of truth) during migration
3. Backfill new location with historical data
4. Switch reads to new location once backfill is verified
5. Stop writing to old location and clean up

During rollback:
- The old version continues to read from the old location without issue
- Data written only to the new location during the migration period may need reconciliation

### Compensating Transactions

When a data change cannot be undone by simply reverting the migration:

- Write compensating transactions that reverse the business effect of the original transaction
- Example: if the deployment processed payments with incorrect amounts, the compensating transaction issues refunds
- Compensating transactions must be idempotent -- safe to apply multiple times
- Log all compensating transactions for audit purposes

### Data That Cannot Be Rolled Back

Some data changes are irreversible:

- Deleted data (unless soft-deleted or backed up)
- Emails, notifications, or webhooks already sent
- External API calls already made (payment charges, third-party state changes)
- Data distributed to downstream systems

For these cases:
- Identify irreversible operations during deployment planning
- Use feature flags to control irreversible operations independently from code deployment
- Implement dry-run modes for irreversible operations during initial rollout

---

## Database Migration Reversal

### Down Migrations

- Every migration should have a corresponding down migration that reverses the change
- Down migrations must be tested -- an untested down migration is unreliable
- Some migrations cannot be reversed (dropping a column with data) -- document this explicitly
- Run down migrations before rolling back the application to avoid schema mismatches

### Data Preservation

- Before applying migrations in production, take a database snapshot or backup
- Verify the backup is restorable before proceeding with the migration
- Retain the backup until the deployment is confirmed stable (minimum 48 hours)
- For large databases where full backups are slow, consider logical backups of affected tables only

### Ordering: Schema vs Application Rollback

1. If the new schema is backward-compatible with the old application: roll back application first, then schema (if needed)
2. If the new schema is NOT backward-compatible with the old application: roll back schema first, then application
3. If the schema change is destructive (dropped column with data): restore from backup, then roll back application

---

## Communication During Rollback

### Internal Stakeholders

- Notify the on-call channel immediately when rollback is initiated
- Provide: what is being rolled back, why, expected timeline, who is leading the response
- Update every 15 minutes during active rollback (SEV1/SEV2 cadence)
- Confirm when rollback is complete and service is restored

### External Users

- Update status page when rollback begins: "We are aware of an issue and are working to resolve it"
- Update status page when rollback completes: "The issue has been resolved"
- Do not provide technical details on the status page -- focus on user impact and resolution
- If the issue affected specific users, consider direct communication (email, in-app notification)

### Status Page Updates

| Phase | Status | Message |
|-------|--------|---------|
| Issue detected | Investigating | "We are investigating reports of [symptom]. Some users may experience [impact]." |
| Rollback initiated | Identified | "We have identified the issue and are deploying a fix. [Impact] may continue for approximately [time]." |
| Rollback complete | Monitoring | "A fix has been deployed. We are monitoring to confirm the issue is resolved." |
| Confirmed resolved | Resolved | "The issue has been resolved. All services are operating normally." |

---

## Post-Rollback RCA Process

### Timeline Construction

- Build a minute-by-minute timeline from deployment start to rollback completion
- Include: deployment events, monitoring alerts, human actions, communication timestamps
- Use logs, metrics, and chat transcripts to construct an accurate timeline
- Identify the gap between issue occurrence and detection (time to detect)
- Identify the gap between detection and rollback initiation (time to respond)

### Root Cause Analysis

- Distinguish between the root cause (why the issue existed) and the trigger (what exposed the issue)
- Ask "why" iteratively (5 Whys technique) to get beyond surface-level causes
- Common root cause categories: code bug, configuration error, infrastructure issue, dependency failure, data issue, process gap

### Prevention

| Root Cause Category | Preventive Action |
|--------------------|-------------------|
| Code bug missed in testing | Add test case for this scenario, review test coverage gaps |
| Configuration error | Validate configurations in CI, use typed configuration objects |
| Infrastructure issue | Improve infrastructure monitoring, add redundancy |
| Dependency failure | Add circuit breakers, improve dependency health checks |
| Data issue | Add data validation, improve migration testing with production-like data |
| Process gap | Update checklists, add automation, improve documentation |

---

## Rollback Testing

### Practice Rollbacks

- Regularly practice rollbacks in staging environments -- at least once per quarter
- Measure rollback time: from decision to fully rolled back and verified
- Identify bottlenecks in the rollback process and eliminate them
- Document actual rollback time and compare to target rollback time

### Chaos Engineering for Rollback Readiness

- Simulate deployment failures that require rollback
- Verify that auto-rollback triggers fire correctly
- Test rollback when the previous version's artifacts are at different ages (recently built vs weeks old)
- Test rollback when the database has been migrated -- can the old version work with the new schema?

### Rollback Readiness Checklist

Before every production deployment, verify:

- [ ] Previous version's artifact exists in the registry and is accessible
- [ ] Previous version is compatible with the current database schema
- [ ] Rollback procedure is documented and accessible to the on-call team
- [ ] Rollback can be triggered with a single command or pipeline
- [ ] Monitoring is in place to detect the need for rollback
- [ ] Communication templates are ready for rollback notification

---

## When NOT to Roll Back

### Forward-Fix Scenarios

Rolling back is not always the right answer. Consider fixing forward when:

- **The rollback would cause data loss** -- If the new version has written data in a format the old version cannot read, rolling back would lose that data. Fix forward with a patch.
- **The rollback itself is risky** -- If the deployment included a database migration that is difficult to reverse, fixing forward may be safer than attempting a complex rollback.
- **The fix is trivial and well-understood** -- A typo in configuration, a missing environment variable, or a simple logic error that can be patched in minutes.
- **The blast radius is contained** -- The issue affects a non-critical feature that can be disabled via feature flag while the fix is prepared.

### Requirements for Fix-Forward

- The root cause is identified and understood
- The fix is small, testable, and low risk
- The fix can be deployed in less time than the rollback
- The team has monitoring in place to verify the fix

### Decision Framework

| Factor | Roll Back | Fix Forward |
|--------|-----------|-------------|
| Root cause known | Not required | Required |
| Fix complexity | N/A | Must be simple |
| Data integrity risk | Low risk from rollback | Rollback would cause data issues |
| Time to fix vs rollback | Rollback is faster | Fix is faster |
| User impact severity | High -- roll back immediately | Low/medium -- can tolerate brief additional impact |
