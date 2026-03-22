# Deployment Strategies

## Blue-Green Deployment

### How It Works

Maintain two identical production environments: Blue (current live) and Green (new version). Deploy the new version to the inactive environment, run validation, then switch traffic.

- Both environments must be identical in infrastructure configuration, differing only in application version
- A router or load balancer controls which environment receives production traffic
- The switch is near-instantaneous -- DNS change, load balancer rule update, or service mesh routing
- The old environment remains running as an immediate rollback target

### Traffic Switching

- **Load balancer swap** -- Update backend pool from Blue to Green. Fastest method, sub-second cutover.
- **DNS switch** -- Update DNS records to point to the Green environment. Slower due to TTL propagation. Use low TTLs (30-60 seconds) if this method is required.
- **Service mesh routing** -- Update virtual service routes. Provides the most control and observability during the switch.

### Rollback

- Switch traffic back to the Blue environment. The rollback is the reverse of the deployment.
- Rollback time equals the switching mechanism latency -- seconds for load balancer, minutes for DNS.
- Keep the Blue environment running for a defined soak period (hours to days) before decommissioning.

### Trade-Offs

- **Pro:** Near-zero downtime, instant rollback, full environment validation before go-live
- **Con:** Doubles infrastructure cost during deployment, database schema changes require coordination, session state must be externalized

---

## Canary Deployment

### How It Works

Deploy the new version to a small subset of production infrastructure. Route a percentage of traffic to the new version. Monitor for errors and performance degradation. Gradually increase traffic if metrics are healthy.

### Percentage-Based Rollout

- Start with 1-5% of traffic to the canary
- Monitor for a defined soak period at each step (15 minutes to several hours depending on traffic volume)
- Increase in steps: 5% --> 10% --> 25% --> 50% --> 100%
- Each step requires metrics validation before proceeding

### Metrics to Watch

| Metric | Signal | Action |
|--------|--------|--------|
| Error rate | Higher than baseline by threshold | Auto-rollback |
| Latency (p50, p95, p99) | Degradation beyond threshold | Pause and investigate |
| CPU/memory utilization | Abnormal resource consumption | Pause and investigate |
| Business metrics (conversion, API success rate) | Drop below baseline | Pause and investigate |
| Saturation | Queue depth, connection pool exhaustion | Auto-rollback |

### Auto-Rollback Triggers

- Error rate exceeds baseline by more than a configured threshold (e.g., 2x baseline)
- p99 latency exceeds SLO target
- Health check failures on canary instances
- Manual trigger by on-call engineer

### Trade-Offs

- **Pro:** Limits blast radius, real production traffic validation, data-driven promotion decisions
- **Con:** Requires robust metrics and observability, more complex routing, users may have inconsistent experiences during rollout

---

## Rolling Deployment

### How It Works

Replace instances of the old version with the new version one at a time (or in batches). At any point during the rollout, both versions are running simultaneously.

### In-Place Updates

- Update instances sequentially: remove from load balancer, deploy new version, health check, add back to load balancer
- Configure batch size: update N instances at a time (e.g., 25% of fleet)
- Set max unavailable: how many instances can be down simultaneously (e.g., 1 or 25%)
- Set max surge: how many extra instances can exist during the rollout (e.g., 1 or 25%)

### Health Check Gates

- Each newly deployed instance must pass health checks before the rollout continues
- **Readiness check** -- Confirms the instance can serve traffic (dependencies available, warm-up complete)
- **Minimum ready time** -- Instance must remain healthy for a defined period (e.g., 60 seconds) before the next batch proceeds
- If a health check fails, the rollout pauses and alerts the operator

### Connection Draining

- Before removing an instance from the load balancer, allow in-flight requests to complete
- Configure drain timeout: how long to wait for connections to close (e.g., 30 seconds)
- New connections are not routed to the draining instance
- After drain timeout, forcefully close remaining connections

### Trade-Offs

- **Pro:** No additional infrastructure required, works with any orchestrator, gradual rollout
- **Con:** Both versions run simultaneously (must handle compatibility), slower than blue-green, rollback requires re-rolling to old version

---

## Recreate Deployment

### When Acceptable

Replace all instances at once. The service is down during the transition.

- **Development/staging environments** -- downtime is acceptable; simplicity is preferred
- **Batch processing jobs** -- no live traffic to disrupt; jobs complete and new version starts next run
- **Stateful applications that cannot run two versions** -- when data format changes prevent coexistence
- **Cost-constrained environments** -- cannot afford duplicate infrastructure for blue-green or canary

### Process

1. Stop all instances of the current version
2. Deploy the new version to all instances
3. Start all instances
4. Verify health checks pass

---

## A/B Deployment

### Feature-Flag-Driven (Not Traffic-Split)

A/B deployment routes specific users to different application behaviors based on feature flags, user attributes, or experiment assignments -- not random traffic splitting.

- Traffic routing is deterministic: the same user always sees the same variant
- Controlled by a feature flag service, not by infrastructure routing
- Used for validating user experience changes with measurable outcomes
- Distinct from canary deployment, which is infrastructure-level and non-deterministic per user

---

## Health Check Patterns

### Readiness Probes

- Indicates the instance is ready to accept traffic
- Checks that dependencies (database, cache, external services) are reachable
- Fails if the instance is still warming up (loading caches, building indexes)
- Failing readiness removes the instance from the load balancer but does not restart it

### Liveness Probes

- Indicates the instance is alive and functioning
- Detects deadlocks, infinite loops, or corrupted state
- Failing liveness triggers instance restart
- Keep liveness checks simple -- they should not depend on external services

### Startup Probes

- Used for slow-starting applications
- Provides a longer initial timeout before liveness checks begin
- Prevents liveness checks from killing instances that are still initializing
- Configure with generous timeout and failure threshold for the initial startup period

### Health Check Design Rules

- Health endpoints must be fast (under 100ms) and must not have side effects
- Distinguish between shallow health (process is running) and deep health (dependencies are reachable)
- Include version information in health check response for deployment verification
- Do not include sensitive information in health check responses -- they may be publicly accessible

---

## Rollback Automation

### Automated Triggers

- Error rate exceeds threshold for sustained period (not just a spike)
- Health check failures across multiple instances
- SLO violation detected by monitoring system
- Manual trigger with one-command rollback

### Automated Procedures

1. Halt any in-progress deployment
2. Switch traffic to the previous known-good version
3. Verify the rollback by checking health and error rate
4. Notify on-call and stakeholders
5. Preserve logs and metrics from the failed deployment for investigation

### Verification

- After rollback, confirm error rate returns to baseline
- Verify that the correct previous version is serving traffic (check version endpoint)
- Run a subset of smoke tests against the rolled-back deployment
- Open an incident ticket for investigation

---

## Zero-Downtime Deployment Requirements

### Application Requirements

- **Graceful shutdown** -- Application handles SIGTERM, completes in-flight requests, closes connections cleanly
- **Backward-compatible changes** -- New version must coexist with old version during transition (API contracts, message formats, database schemas)
- **Health check endpoints** -- Application exposes readiness and liveness endpoints
- **Externalized state** -- No in-memory session state; sessions stored in external store (Redis, database)
- **Idempotent startup** -- Application startup must be safe to repeat (migrations run only if needed, no duplicate side effects)

### Infrastructure Requirements

- Load balancer with health-check-based routing
- Connection draining support
- Rolling or blue-green deployment mechanism
- Automated rollback capability

---

## Database Migration Deployment Coordination

### The Challenge

Database schema changes and application code changes must be coordinated. The old application version and the new version must both work with the database at the same time during the deployment transition.

### Expand-and-Contract Pattern

1. **Expand** -- Add new columns/tables without removing old ones. Both old and new code works.
2. **Migrate** -- Deploy new application code that writes to both old and new structures. Backfill existing data.
3. **Contract** -- Remove old columns/tables after all application instances are on the new version.

### Rules

- Never rename a column in a single deployment -- add new column, migrate data, remove old column in separate deployments
- Never drop a column that the current running version uses
- Make migrations reversible where possible -- include down migrations
- Run migrations before deploying new application code (the database must be ready before the app expects it)
- Test migrations against a copy of production data -- not just empty databases

---

## Deployment Anti-Patterns

- **Friday deployments** -- Deploying before weekends or holidays when fewer people are available to respond to issues. Deploy early in the work week.
- **Big-bang deployment** -- Accumulating weeks of changes into a single large deployment. Smaller, frequent deployments are safer and easier to diagnose.
- **Deploy and pray** -- No monitoring, no health checks, no rollback plan. Hope is not a strategy.
- **Manual deployment scripts** -- SSH-ing into servers and running commands manually. All deployments must be automated and repeatable.
- **Deploying untested artifacts** -- Skipping staging or pre-production validation. Every artifact must pass through a pre-production environment.
- **Coupling deployment and release** -- Deployment (putting code in production) and release (enabling features for users) should be independent. Use feature flags to decouple.
- **Ignoring database migrations** -- Treating database changes as an afterthought. Schema changes require explicit coordination with application deployments.
