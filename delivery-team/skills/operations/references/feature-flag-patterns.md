# Feature Flag Patterns

## Flag Types

### Release Flags (Temporary)

Enable incomplete or untested features to be merged to main without being visible to users.

- Purpose: Decouple deployment from release. Code ships to production with the flag disabled.
- Lifecycle: Created when development begins, removed when the feature is stable and fully rolled out.
- Duration: Days to weeks. Maximum lifespan: one release cycle after full rollout.
- Default state: OFF in production, configurable in staging/dev.
- Example: `enable_new_checkout_flow` -- guards a new checkout experience during development.

### Ops Flags (Circuit Breakers / Kill Switches)

Provide runtime control over system behavior for operational purposes.

- Purpose: Disable features or degrade gracefully during incidents without deploying code.
- Lifecycle: Created during development of the feature they protect. Persist for the lifetime of the feature.
- Duration: Permanent (as long as the feature exists).
- Default state: ON (feature enabled). Toggled OFF during incidents.
- Example: `enable_recommendation_engine` -- can be disabled if the recommendation service is overloaded.

### Experiment Flags (A/B Tests)

Route users to different feature variants for data-driven decision making.

- Purpose: Measure the impact of changes on user behavior (conversion rates, engagement, revenue).
- Lifecycle: Created when the experiment is designed, removed when the experiment concludes and a winner is selected.
- Duration: Weeks to months (experiment duration plus analysis period).
- Default state: Control variant. Treatment variants assigned to configured user segments.
- Example: `checkout_button_color` -- routes 50% of users to a green button variant.

### Permission Flags (Entitlements)

Control feature access based on user attributes, subscription tier, or organizational permissions.

- Purpose: Gate features by user segment without code changes. Enable per-customer feature availability.
- Lifecycle: Created when the feature is built. Persist for the lifetime of the feature.
- Duration: Permanent.
- Default state: OFF for all users. Enabled per-user, per-organization, or per-tier.
- Example: `enable_advanced_analytics` -- available only to enterprise-tier customers.

---

## Lifecycle Management

### Lifecycle Stages

1. **Create** -- Define the flag with a name, type, description, owner, and planned removal date.
2. **Implement** -- Add flag evaluation to the code. Wrap the new behavior in a conditional check.
3. **Test** -- Verify both flag-on and flag-off code paths in automated tests.
4. **Stage** -- Enable the flag in staging for validation.
5. **Rollout** -- Gradually enable in production (percentage rollout or targeted segments).
6. **GA (General Availability)** -- Flag is enabled for all users. Feature is stable.
7. **Remove** -- Delete the flag from configuration and remove conditional code paths. The feature is now always on.

### Stale Flag Detection

- Define a maximum lifespan per flag type: release flags (30 days after GA), experiment flags (90 days)
- Automated scanning: CI check that flags older than their maximum lifespan generate warnings
- Weekly report of stale flags sent to flag owners
- Flags past their removal date block new flag creation by the same owner (optional enforcement)

### Flag Naming Conventions

- Use descriptive, lowercase names with underscores: `enable_new_search`, `experiment_pricing_page_v2`
- Prefix with flag type for clarity: `release_`, `ops_`, `exp_`, `perm_` (optional but helpful at scale)
- Include the feature area: `checkout_enable_apple_pay`, not just `apple_pay`
- Never reuse flag names -- even after removal, the name is retired

---

## Flag Cleanup

### Technical Debt From Old Flags

- Every flag adds a conditional branch to the code, increasing complexity
- Old flags with unknown state become landmines -- no one knows what happens if they are toggled
- Test coverage must cover both flag states, doubling test paths per flag
- At scale (100+ flags), the combinatorial explosion makes reasoning about system behavior difficult

### Removal Process

1. Confirm the flag has been at GA (enabled for all users) for the defined stabilization period
2. Remove the flag evaluation from code -- make the enabled path the only path
3. Remove the disabled code path entirely -- do not leave dead code behind
4. Remove the flag definition from the flag management system
5. Update tests to remove flag-conditional test cases
6. Deploy the cleanup as a normal release -- the behavior should not change

### Code Review for Flag Cleanup

- Flag cleanup PRs should be reviewed with the same rigor as feature PRs
- Verify that the "enabled" behavior is preserved exactly
- Verify that the "disabled" code path is fully removed (no orphan functions, no dead imports)
- Verify that tests are updated to test the single remaining path

---

## Targeting Rules

### User Segments

Target flags to specific user groups based on attributes:

- User ID (specific users for internal testing or beta programs)
- Organization ID (enable for specific customers)
- User role (admin, editor, viewer)
- Subscription tier (free, pro, enterprise)
- Geography (country, region)
- User creation date (new users vs existing users)

### Percentage Rollout

- Enable the flag for a percentage of users: 1% --> 5% --> 10% --> 25% --> 50% --> 100%
- Percentage must be sticky: the same user always gets the same flag value (hash user ID to determine bucket)
- Increase percentage gradually, monitoring metrics at each step
- If metrics degrade at any step, hold or reduce the percentage

### Allow/Deny Lists

- **Allow list** -- Explicitly enable the flag for specific users or organizations, regardless of percentage rollout
- **Deny list** -- Explicitly disable the flag for specific users, even if they fall within the rollout percentage
- Allow/deny lists override percentage-based targeting
- Use allow lists for internal testing and beta programs before broader rollout

### Geography-Based Targeting

- Enable features by region for compliance (e.g., GDPR-specific features in EU)
- Stagger rollout by timezone to monitor during business hours
- Respect data residency requirements -- some features cannot be enabled in certain regions

---

## Kill Switches

### Emergency Disable

- Kill switches must evaluate in the fast path -- no network calls to flag service for critical kill switches
- Cache flag values locally with short TTL (30-60 seconds) for non-critical flags
- Kill switch toggle must take effect within seconds, not minutes
- Kill switch operation must not require a code deployment

### Fast Path Evaluation

```
Evaluation order for kill switches:
1. Check local cache (in-memory, no I/O)
2. If cache is fresh, use cached value
3. If cache is stale, use cached value AND refresh asynchronously
4. If flag service is unreachable, use cached value (fail open or fail closed based on flag type)
```

### Fail-Open vs Fail-Closed

- **Fail-open:** If the flag service is unavailable, treat the flag as enabled. Use for features that should be available by default.
- **Fail-closed:** If the flag service is unavailable, treat the flag as disabled. Use for features that are risky or under active rollout.
- Document the fail mode for every flag -- this is a critical operational decision

---

## Flag-Driven Testing

### Testing All Flag Combinations

- Test both flag-on and flag-off paths in unit tests
- For integration and end-to-end tests, test the default state plus the non-default state
- Do not test all combinations of all flags -- this is combinatorially explosive. Test each flag independently.
- Use test fixtures or test helpers that make it easy to set flag values in tests

### Default States

- Every flag must have a documented default state that is safe for production
- Default state is what the system uses if the flag service is unreachable
- Release flags default to OFF (feature hidden)
- Ops flags default to ON (feature enabled, but can be killed)
- Experiment flags default to control variant
- Permission flags default to OFF (feature gated)

### Testing in Production

- After enabling a flag in production, verify with smoke tests
- Monitor metrics for the specific feature controlled by the flag
- If the flag controls a user-facing change, verify the experience manually in production
- Keep a "flag verification" checklist for each flag rollout

---

## Flag Management Platforms

### Evaluation Architecture

| Approach | How It Works | Latency | Reliability |
|----------|-------------|---------|-------------|
| **Server-side SDK** | Application calls flag service SDK. SDK maintains local cache, syncs asynchronously. | Microseconds (cache hit) | High -- works with stale cache if service is down |
| **Client-side SDK** | Client app fetches flag values on startup or on-demand. | Milliseconds (network call) | Depends on network availability |
| **Edge evaluation** | Flag rules evaluated at CDN/edge. | Microseconds | High -- evaluation happens at the edge |

### Local vs Remote Evaluation

- **Local evaluation:** Flag rules are downloaded and evaluated in-process. Fastest. No per-request network calls.
- **Remote evaluation:** Each flag check makes a network call to the flag service. Simplest but adds latency and a point of failure.
- Prefer local evaluation for performance-critical paths.
- Use remote evaluation for admin tools and low-traffic paths where latency is acceptable.

### Caching Strategy

- Cache flag values in memory with a configurable TTL (30 seconds to 5 minutes)
- On cache miss, evaluate synchronously and populate cache
- On cache expiry, serve stale value and refresh asynchronously (stale-while-revalidate)
- Log cache hit/miss rates to detect caching issues

---

## Anti-Patterns

- **Flag-driven architecture** -- Using flags to control fundamental architectural decisions (which database to use, which service to call). Flags should control features, not architecture. Use proper configuration for infrastructure decisions.
- **Nested flags** -- Flag B is only meaningful when Flag A is enabled. Nested flags create hidden dependencies and make reasoning about system behavior exponentially harder. If nesting is required, combine into a single flag with explicit states.
- **Flags as permanent configuration** -- Using feature flags for settings that will never change (locale, theme, feature tier). Use proper configuration or user settings for permanent choices. Flags are for temporary conditional behavior.
- **Too many flags** -- Having hundreds of active flags simultaneously. Each flag increases cognitive load and test complexity. Set a team limit (e.g., max 20 active release flags) and enforce it.
- **No flag ownership** -- Flags without a clear owner who is responsible for rollout and cleanup. Every flag must have an owner assigned at creation time.
- **Testing only the happy path** -- Only testing the flag-on path and ignoring the flag-off path. Both paths are production code and must be tested.
- **Flag naming collisions** -- Reusing flag names after removal, causing confusion about whether the flag is the old or new version. Retire flag names permanently.
- **Global flags for per-user decisions** -- Using a global on/off flag when the decision should be per-user (entitlements, experiments). Use targeting rules for per-user decisions.
